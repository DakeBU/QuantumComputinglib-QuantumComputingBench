import copy
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
import entry

PACKAGE=Path(__file__).parent
BASE=Path(os.environ.get('C31_KERNEL_V1_TEST_PACKAGE',PACKAGE.parent/'.c31-kernel-proof-v1-staging')).resolve()
PROFILE=entry.read(PACKAGE/'profile.json')


class GuardTests(unittest.TestCase):
    def setUp(self): self.runtime=entry.load_code(BASE,PROFILE['baseFiles'])
    def record(self,runtime=None,**changes):
        observed=dict(entry_file=str(PACKAGE/'entry.py'),argv0=str(PACKAGE/'entry.py'),main_file=str(PACKAGE/'entry.py'),
            entry_sha=entry.sha(PACKAGE/'entry.py'))
        observed.update(changes)
        return entry.execution_record(PACKAGE,BASE,PROFILE['baseFiles'],self.runtime if runtime is None else runtime,**observed)

    def test_all_actual_module_file_paths_and_sha_are_observed(self):
        row=self.record(); self.assertEqual(len(row['modules']),3)
        self.assertEqual({Path(m['actualFile']).name for m in row['modules']},{'runtime.py','compare.py','proof_patch.py'})
        self.assertTrue(all(len(m['sourceSHA256'])==64 for m in row['modules']))
        self.assertEqual(row['entry']['sourceSHA256'],entry.sha(PACKAGE/'entry.py'))
        self.assertFalse(row['OSAttestation']); self.assertFalse(row['codeObjectAttestation'])

    def test_wrong_module_file_and_hash_rejected(self):
        for name in entry.MODULE_FILES:
            expected=BASE/entry.MODULE_FILES[name]
            fake=SimpleNamespace(__file__=str(PACKAGE/'not-the-module.py'),__name__=name)
            with self.assertRaises(ValueError): entry.module_file(fake,expected,PROFILE['baseFiles'][expected.name])
            with self.assertRaises(ValueError): entry.module_file(SimpleNamespace(__file__=str(expected)),expected,'0'*64)

    def test_fake_preloaded_module_is_refused_before_import(self):
        for name in ('compare','proof_patch'):
            original=sys.modules[name]; sys.modules[name]=SimpleNamespace(__file__=str(PACKAGE/'fake.py'))
            try:
                with self.assertRaises(ValueError): entry.load_code(BASE,PROFILE['baseFiles'])
            finally: sys.modules[name]=original

    def test_fake_same_path_module_object_and_runtime_identity_rejected(self):
        actual=self.runtime.compare
        self.runtime.compare=SimpleNamespace(__file__=actual.__file__,__name__=actual.__name__)
        try:
            with self.assertRaises(ValueError): self.record()
        finally: self.runtime.compare=actual
        fake=SimpleNamespace(**vars(self.runtime))
        with self.assertRaises(ValueError): self.record(runtime=fake)

    def test_fake_entry_argv0_main_and_entry_hash_rejected(self):
        for key in ('entry_file','argv0','main_file'):
            with self.assertRaises(ValueError): self.record(**{key:str(PACKAGE/'wrong-entry.py')})
            with self.assertRaises(ValueError): self.record(**{key:None})
        with self.assertRaises(ValueError): self.record(entry_sha='0'*64)

    def test_startup_receipt_and_per_operation_guards_and_rollback(self):
        calls=[]; guard=lambda:(calls.append(True) or self.record())
        verify=self.runtime.verify; write=self.runtime.write
        with tempfile.TemporaryDirectory(prefix='.fixture-',dir=PACKAGE) as name:
            private=Path(name)/'private'; private.mkdir()
            with self.assertRaises(RuntimeError):
                with entry.guarded_hooks(self.runtime,guard):
                    self.runtime.verify(BASE,PROFILE['baseFiles'])
                    self.runtime.write(private/'candidate-preparation-resource.json',{'scope':'SYNTHETIC_METADATA_TEST'})
                    self.assertEqual(len(entry.read(private/'executing-code-bindings.json')['modules']),3)
                    with self.assertRaises(ValueError): self.runtime.write(private/'candidate-preparation-resource.json',{})
                    raise RuntimeError('SYNTHETIC_ROLLBACK')
            self.assertIs(self.runtime.verify,verify); self.assertIs(self.runtime.write,write)
        self.assertGreaterEqual(len(calls),3)

    def test_v1_19_bytes_transport_and_candidate_sha_unchanged(self):
        entry.verify(BASE,PROFILE['baseFiles']); self.assertEqual(len(PROFILE['baseFiles']),19)
        manifest=entry.read(BASE/'bindings.json')['files']
        candidate='candidate/QuantumBlockEncoding/CubicAmplitudePrimitive.lean'
        self.assertEqual(entry.sha(BASE/candidate),manifest[candidate])
        self.assertEqual(entry.sha(BASE/'seal.json'),'5ed9c0c9d9dcb5ce75bd79748e42efc504a631b5c61c326d5e8f6e66cd6ccf80')
        self.assertTrue(PROFILE['sourceBlindReviewExclusionNotConfidential'])
        self.assertTrue(PROFILE['publicRepoCandidateTransportAllowed'])
        self.assertFalse(PROFILE['nativeAccepted'])


if __name__=='__main__': unittest.main()
