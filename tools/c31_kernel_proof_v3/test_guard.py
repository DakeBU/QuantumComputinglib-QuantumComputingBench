import copy
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
import entry
from unittest.mock import patch

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


class SharedHelperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project=Path(os.environ.get('C31_KERNEL_TEST_PROJECT',Path.cwd())).resolve()
        cls.runtime=entry.load_code(BASE,PROFILE['baseFiles'])
        cls.ci4,cls.ci2,cls.base,cls.p1,cls.original,cls.api=cls.runtime.load_runtime(
            cls.project,entry.read(BASE/'kernel-profile.json'))
        cls.derived=entry.read(BASE/'profile.json')
        cls.data=(cls.project/entry.SHARED_PATH).read_bytes()
        if entry.sha(cls.project/entry.SHARED_PATH)!=entry.SHARED_SHA: raise ValueError('fixture source pin drift')

    def fixture(self,root):
        project=root/'project'; work=root/'work'; project.mkdir(); work.mkdir()
        helper=project/entry.SHARED_PATH; helper.parent.mkdir(parents=True); helper.write_bytes(self.data)
        return project,work

    def test_exact_copy_original_api_and_unchanged_base_shadow_pin(self):
        with tempfile.TemporaryDirectory(prefix='.fixture-',dir=PACKAGE) as name:
            project,work=self.fixture(Path(name)); origin=self.api.__file__
            row=entry.copy_shared_helper(project,work,self.derived,self.api)
            self.assertEqual(self.api.verify_pins(work,{entry.SHARED_PATH:entry.SHARED_SHA})[0]['sha256'],entry.SHARED_SHA)
            self.base.recheck_rows([row],self.api)
            self.assertEqual(row['sourceSHA256Before'],row['destinationSHA256'])
            self.assertEqual(row['sourceSHA256After'],entry.SHARED_SHA)
            self.assertFalse(row['copiedHelperExecuted']); self.assertEqual(self.api.__file__,origin)
            self.assertNotEqual(Path(origin).resolve(),Path(row['destination']).resolve())

    def test_wrong_source_and_wrong_profile_pin_or_path_fail_closed(self):
        with tempfile.TemporaryDirectory(prefix='.fixture-',dir=PACKAGE) as name:
            project,work=self.fixture(Path(name))
            for key,value in [('sha256','0'*64),('path','tools/elsewhere.py')]:
                bad=copy.deepcopy(self.derived); bad['sharedInstrumentation'][key]=value
                with self.assertRaises(ValueError): entry.copy_shared_helper(project,work,bad,self.api)
            source=project/entry.SHARED_PATH; source.write_bytes(b'wrong helper')
            with self.assertRaises(ValueError): entry.copy_shared_helper(project,work,self.derived,self.api)
            self.assertFalse((work/entry.SHARED_PATH).exists())

    def test_wrong_destination_and_collision_never_overwrite(self):
        with tempfile.TemporaryDirectory(prefix='.fixture-',dir=PACKAGE) as name:
            root=Path(name); project,work=self.fixture(root)
            fake=SimpleNamespace(safe_child=lambda r,p:self.api.safe_child(r,'wrong.py') if r==work else self.api.safe_child(r,p))
            with self.assertRaises(ValueError): entry.copy_shared_helper(project,work,self.derived,fake)
            target=work/entry.SHARED_PATH; target.parent.mkdir(parents=True); target.write_bytes(b'existing output')
            with self.assertRaises(FileExistsError): entry.copy_shared_helper(project,work,self.derived,self.api)
            self.assertEqual(target.read_bytes(),b'existing output')
            with self.assertRaises(ValueError): entry.copy_shared_helper(project,project,self.derived,self.api)

    def test_continuous_original_and_destination_drift_refused(self):
        for key in ('source','destination'):
            with tempfile.TemporaryDirectory(prefix='.fixture-',dir=PACKAGE) as name:
                project,work=self.fixture(Path(name)); row=entry.copy_shared_helper(project,work,self.derived,self.api)
                Path(row[key]).write_bytes(b'drift')
                with self.assertRaises(ValueError): self.base.recheck_rows([row],self.api)

    def test_real_v1_source_prepare_plus_v3_hook_satisfies_pre_target_pin(self):
        # Real v1 prepare copies 31 inputs and real immutable collector files.
        # Provider binary seeding is stubbed: no native call or compilation.
        calls=[]; original_prepare=self.runtime.prepare
        with tempfile.TemporaryDirectory(prefix='.fixture-',dir=PACKAGE) as name:
            root=Path(name); (root/'private').mkdir(); work=root/'work'; run_package=root/'runtime-input-view'
            provider_stub=SimpleNamespace(copy_providers=lambda *args:[])
            with patch.object(self.api,'native_call',side_effect=AssertionError('NO_NATIVE')) as native:
                with entry.guarded_hooks(self.runtime,lambda:calls.append(True) or {'syntheticGuard':True}):
                    inputs,seed,files=self.runtime.prepare(self.project,BASE,work,run_package,self.derived,provider_stub,self.api)
                    self.api.verify_pins(work,self.derived['projectInputs'])
                    self.api.verify_pins(work,{entry.SHARED_PATH:entry.SHARED_SHA})
                    self.base.recheck_rows(seed,self.api)
                    receipt=entry.read(root/'private/shared-helper-copy.json')
                    self.assertEqual(len(inputs),31); self.assertEqual(len(seed),1)
                    self.assertEqual(receipt['kind'],'SHARED_HELPER_PIN_COPY_NOT_PROVIDER_ARTIFACT')
                    self.assertEqual(files['profile.json'],entry.sha(BASE/'profile.json'))
                native.assert_not_called()
            self.assertIs(self.runtime.prepare,original_prepare)
        self.assertGreaterEqual(len(calls),2)

    def test_prepare_hook_restores_on_copy_failure_and_does_not_call_native(self):
        original=(self.runtime.verify,self.runtime.write,self.runtime.prepare)
        with tempfile.TemporaryDirectory(prefix='.fixture-',dir=PACKAGE) as name:
            root=Path(name); project,work=self.fixture(root)
            source=project/entry.SHARED_PATH; source.write_bytes(b'bad')
            stub=lambda *args:([],[],{})
            with patch.object(self.runtime,'prepare',stub),patch.object(self.api,'native_call',side_effect=AssertionError('NO_NATIVE')) as native:
                with self.assertRaises(ValueError):
                    with entry.guarded_hooks(self.runtime,lambda:{}):
                        self.runtime.prepare(project,BASE,work,root/'runtime',self.derived,self.base,self.api)
                self.assertIs(self.runtime.prepare,stub); native.assert_not_called()
            self.assertEqual((self.runtime.verify,self.runtime.write,self.runtime.prepare),original)

    def test_v2_entry_cannot_masquerade_as_v3(self):
        runtime=entry.load_code(BASE,PROFILE['baseFiles'])
        previous=PACKAGE.parent/'.c31-kernel-proof-v2-guard-staging/entry.py'
        for key in ('entry_file','argv0','main_file'):
            observed=dict(entry_file=str(PACKAGE/'entry.py'),argv0=str(PACKAGE/'entry.py'),main_file=str(PACKAGE/'entry.py'),entry_sha=entry.sha(PACKAGE/'entry.py'))
            observed[key]=str(previous)
            with self.assertRaises(ValueError): entry.execution_record(PACKAGE,BASE,PROFILE['baseFiles'],runtime,**observed)


if __name__=='__main__': unittest.main()


