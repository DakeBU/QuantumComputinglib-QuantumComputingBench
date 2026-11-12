"""Synthetic integrity tests, NOT reviews or real Lean/publication acceptance.

Only Git responses and the two exact-case constants are mocked. Files, hashes,
inventory completeness, receipt binding and stale-evidence failures are real.
"""
from __future__ import annotations
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('maintenance_candidate', Path(__file__).with_name('check_toolchain_maintenance.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class MaintenanceTests(unittest.TestCase):
    def put(self, name, content):
        data = content if isinstance(content, bytes) else content.encode()
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return m.sha(data)

    def dump(self, name, value):
        return self.put(name, json.dumps(value, sort_keys=True).encode())

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        module = m.APPROVED_CASE['module']
        self.put(module, 'theorem synthetic_current : True := True.intro\n')
        for i in range(7):
            self.put(f'QuantumBlockEncoding/SyntheticProvider{i}.lean', '-- synthetic provider\n')
        self.put('ABEISTests/SyntheticTest.lean', '-- synthetic test\n')
        for name in ('QuantumBlockEncoding.lean', 'Tests.lean', 'lakefile.lean'):
            self.put(name, '-- synthetic context\n')
        self.put('lean-toolchain', 'leanprover/lean4:v4.33.0\n')
        self.put('lake-manifest.json', '{"synthetic":true}\n')
        for name in ('website/scripts/check_research_publications.py',
                     'website/scripts/check_toolchain_maintenance.py',
                     'docs/theorem-publication-protocol.md'):
            self.put(name, 'synthetic fixture only\n')
        self.put('docs/lessons/synthetic.md', 'No scientific claim.\n')
        self.diff = b'synthetic exact diff\n'
        self.put('reviews/synthetic.patch', self.diff)
        self.old = b'theorem synthetic_old : True := True.intro\n'
        self.old_manifest = b'{"synthetic":"old"}\n'
        self.case = dict(m.APPROVED_CASE,
                         old_source_sha256=m.sha(self.old),
                         new_source_sha256=m.sha((self.root/module).read_bytes()),
                         old_manifest_sha256=m.sha(self.old_manifest),
                         new_manifest_sha256=m.sha((self.root/'lake-manifest.json').read_bytes()),
                         diff_sha256=m.sha(self.diff))
        self.inventory = {f'SYNTHETIC_ONLY.leaf{i}': {'source':module, 'experimental':True, 'openProof':False}
                          for i in range(395)}
        names = [module] + [f'QuantumBlockEncoding/SyntheticProvider{i}.lean' for i in range(7)]
        names += ['lean-toolchain', 'lakefile.lean', 'lake-manifest.json']
        original = {'inputs':[{'path':n, 'production_raw_sha256':m.sha((self.root/n).read_bytes())} for n in names]}
        original_sha = self.dump('reviews/original-inputs.json', original)
        self.put('reviews/original-seal.json', '{"fixture":"not a real review"}\n')
        self.r = dict(schema=1, kind='exact-toolchain-maintenance', case=self.case,
                      scope='BE-only compatibility; no scientific promotion', declarations=sorted(self.inventory),
                      coverage={'raw_declarations':677,'structure_fields':1950,'public_exports':395},
                      maintainer='SYNTHETIC-author', historical_formalizer='UNKNOWN',
                      scientific_claims={k:False for k in m.SCIENTIFIC_KEYS},
                      remaining_BE_obligations=['SYNTHETIC: full physical BE remains open'],
                      proof_context=m.proof_context(self.root), lesson_path='docs/lessons/synthetic.md',
                      diff_path='reviews/synthetic.patch', evidence={})
        self.receipts = {}
        for role in sorted(m.ROLES):
            artifact_path = 'reviews/'+role+'.txt'
            artifact_sha = self.put(artifact_path, 'SYNTHETIC ONLY: '+role+'\n')
            ref = {'path':'reviews/'+role+'.json', 'artifact_path':artifact_path, 'artifact_sha256':artifact_sha}
            self.r['evidence'][role] = ref
            e = dict(role=role, identity='SYNTHETIC-'+role, run_id='SYNTHETIC-RUN', purpose='compatibility-only',
                     artifact_path=artifact_path, artifact_sha256=artifact_sha)
            if role in {'whole-module-decoder','whole-module-review','raw-association'}:
                e.update(receipt_kind='exact-input-reuse', new_review_performed=False,
                         original_raw_module_sha256=self.case['new_source_sha256'],
                         original_input_manifest_path='reviews/original-inputs.json',
                         original_seal_path='reviews/original-seal.json',
                         original_seal_sha256=m.sha((self.root/'reviews/original-seal.json').read_bytes()),
                         original_scope_preserved=True)
            if role == 'whole-module-decoder': e['source_blind'] = True
            if role in {'compatibility-review','policy-review'}:
                e.update(verdict='accepted-for-compatibility-only', anti_anchored=True)
            if role == 'compiled-runtime':
                e.update(proof_context=self.r['proof_context'], full_library_and_Tests=True, trust_gate=True,
                         workflow_run_id='SYNTHETIC-1', job_id='SYNTHETIC-2', native_trust_disclosure='NOT ordinary-three axioms')
            self.receipts[role] = e
        for name, value in (('APPROVED_CASE', self.case), ('ORIGINAL_INPUT_MANIFEST_SHA256', original_sha)):
            mock = patch.object(m, name, value); mock.start(); self.addCleanup(mock.stop)
        mock = patch.object(m, 'git_bytes', side_effect=self.git)
        mock.start(); self.addCleanup(mock.stop)
        self.refresh()

    def git(self, root, *args):
        self.assertEqual(root, self.root)
        if args == ('show', self.case['base_commit']+':'+self.case['module']): return self.old
        if args == ('show', self.case['base_commit']+':lean-toolchain'): return b'leanprover/lean4:v4.29.1\n'
        if args == ('show', self.case['base_commit']+':lake-manifest.json'): return self.old_manifest
        if args == ('diff','--no-ext-diff','--no-renames','--abbrev=8',self.case['base_commit'],'--',self.case['module']): return self.diff
        self.fail('unexpected Git request: '+repr(args))

    def refresh(self):
        # Simulate a COMPLETE new cross-role binding, not one actor updating
        # its own receipt. Tests of that attack deliberately do NOT call this.
        for role, e in self.receipts.items():
            if role in self.r['evidence']:
                self.r['evidence'][role]['expected_fields'] = {k:v for k,v in e.items() if k != 'binding_sha256'}
        self.r['binding_sha256'] = m.binding_digest(self.root, self.r)
        for role, e in self.receipts.items():
            if role not in self.r['evidence']: continue
            e['binding_sha256'] = self.r['binding_sha256']
            self.r['evidence'][role]['sha256'] = self.dump(self.r['evidence'][role]['path'], e)

    def validate(self): m.validate_record(self.root, self.r, self.inventory)
    def rejects(self, text):
        with self.assertRaisesRegex(ValueError, text): self.validate()

    def test_synthetic_valid_integrity_only(self): self.validate()

    def test_no_silent_lane_mixing_or_duplicate(self):
        module = self.case['module']
        with self.assertRaisesRegex(ValueError, 'mix'):
            m.partition_records({'records':[{'module':module}], 'maintenance_records':[self.r]})
        for registry in ({'records':[{'module':module}]*2},
                         {'records':[], 'maintenance_records':[self.r]*2}):
            with self.assertRaisesRegex(ValueError, 'duplicate'): m.partition_records(registry)
        self.assertEqual(m.partition_records({'records':[]}), ({},{}))

    def test_all_scientific_claims_must_be_explicit_false(self):
        for key in sorted(m.SCIENTIFIC_KEYS):
            with self.subTest(key=key):
                self.r['scientific_claims'][key] = True
                self.rejects('cannot claim')
                self.r['scientific_claims'][key] = False
        self.r['scientific_claims'].pop('PURIFIED'); self.rejects('cannot claim')

    def test_different_or_future_case_rejected(self):
        for key in sorted(self.case):
            original = self.r['case']
            self.r['case'] = dict(self.case, **{key:'different'})
            with self.subTest(key=key): self.rejects('exact maintenance case')
            self.r['case'] = original

    def test_changed_source_definition_or_target_rejected(self):
        self.put(self.case['module'], 'changed target\n'); self.rejects('source changed')

    def test_changed_dependency_or_context_rejected(self):
        self.put('QuantumBlockEncoding/SyntheticProvider0.lean', 'changed provider\n')
        self.rejects('full source/config context')

    def test_partial_context_rejected(self):
        self.r['proof_context'].pop('Tests.lean'); self.rejects('full source/config context')

    def test_all_config_bytes_bound(self):
        for name in ('lean-toolchain','lake-manifest.json','lakefile.lean','Tests.lean','QuantumBlockEncoding.lean'):
            raw = (self.root/name).read_bytes(); self.put(name, raw+b'changed\n')
            with self.subTest(name=name):
                with self.assertRaises(ValueError): self.validate()
            self.put(name,raw)

    def test_actual_diff_file_bound(self):
        self.put(self.r['diff_path'], b'not actual diff\n'); self.rejects('compatibility diff')

    def test_all_395_inventory_required(self):
        self.r['declarations'].pop(); self.rejects('whole public inventory')

    def test_duplicate_declaration_rejected(self):
        self.r['declarations'].append(self.r['declarations'][0]); self.rejects('whole public inventory')

    def test_flag_removal_or_proof_hole_rejected(self):
        row = next(iter(self.inventory.values()))
        row['experimental']=False; self.rejects('experimental flags')
        row['experimental']=True; row['openProof']=True; self.rejects('experimental flags')

    def test_whole_module_fields_not_subset(self):
        self.r['coverage']['structure_fields']=1949; self.rejects('whole-module coverage')

    def test_missing_role_rejected(self):
        self.r['evidence'].pop('raw-association'); self.refresh(); self.rejects('complete independent')

    def test_missing_actual_result_file_rejected(self):
        (self.root/self.receipts['compatibility-review']['artifact_path']).unlink()
        self.rejects('missing maintenance evidence file')

    def test_tampered_receipt_rejected(self):
        self.put(self.r['evidence']['compatibility-review']['path'],'{}'); self.rejects('evidence bytes changed')

    def test_changed_result_cannot_refresh_own_receipt_only(self):
        e=self.receipts['compatibility-review']
        e['artifact_sha256']=self.put(e['artifact_path'],'different result')
        self.refresh(); self.rejects('differs from the reviewed binding')

    def test_new_lesson_or_checker_invalidates_all_receipts(self):
        for name in (self.r['lesson_path'], 'website/scripts/check_research_publications.py',
                     'website/scripts/check_toolchain_maintenance.py', 'docs/theorem-publication-protocol.md'):
            raw=(self.root/name).read_bytes(); self.put(name,raw+b'changed')
            with self.subTest(name=name): self.rejects('stale maintenance binding')
            self.put(name,raw)

    def test_self_review_and_decoder_collisions(self):
        for role in ('whole-module-decoder','whole-module-review','compatibility-review','policy-review'):
            e=self.receipts[role]; old=e['identity']; e['identity']=self.r['maintainer']; self.refresh()
            with self.subTest(role=role): self.rejects('must differ|cannot be the author')
            e['identity']=old; self.refresh()

    def test_unaccepted_or_anchored_review_rejected(self):
        for role in ('compatibility-review','policy-review'):
            e=self.receipts[role]
            for key,value in (('verdict','rejected'),('anti_anchored',False)):
                old=e[key];e[key]=value;self.refresh()
                with self.subTest(role=role,key=key):self.rejects('actual accepted independent review')
                e[key]=old;self.refresh()

    def test_source_blind_status_required(self):
        self.receipts['whole-module-decoder']['source_blind']=False;self.refresh();self.rejects('source-blind')

    def test_runtime_not_inferred_from_success_json(self):
        e=self.receipts['compiled-runtime']
        for key,value in (('full_library_and_Tests',False),('trust_gate',False),('proof_context',{}),
                          ('workflow_run_id',''),('job_id',''),('native_trust_disclosure','')):
            old=e[key];e[key]=value;self.refresh()
            with self.subTest(key=key):self.rejects('actual full|provenance/native')
            e[key]=old;self.refresh()

    def test_historical_reuse_never_new_review(self):
        e=self.receipts['whole-module-review'];e['new_review_performed']=True
        self.refresh();self.rejects('explicitly reused')

    def test_historical_seal_and_manifest_required(self):
        self.put('reviews/original-inputs.json','{}');self.rejects('eleven-input formal manifest')

    def test_historical_scope_not_retroactively_enlarged(self):
        self.receipts['whole-module-review']['original_scope_preserved']=False
        self.refresh();self.rejects('seal/scope association')

    def test_missing_remaining_obligations_rejected(self):
        self.r['remaining_BE_obligations']=[];self.rejects('must stay explicit')

    def test_paths_reject_drive_relative_absolute_and_traversal(self):
        for name in ('../escape','C:/escape','C:escape','/escape','x\\y','x:y'):
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError,'non-portable'): m.local_file(self.root,name)

    def test_one_wrapper_cannot_refresh_any_stable_semantics(self):
        for role in sorted(self.receipts):
            original = dict(self.receipts[role])
            for key in sorted(k for k in original if k != 'binding_sha256'):
                with self.subTest(role=role, key=key):
                    altered = dict(original, **{key:'forged-wrapper-value'})
                    ref=self.r['evidence'][role]
                    old_hash=ref['sha256']
                    ref['sha256']=self.dump(ref['path'],altered)
                    self.rejects('receipt semantics differ')
                    ref['sha256']=self.dump(ref['path'],original)
                    self.assertEqual(ref['sha256'],old_hash)

    def test_changed_expected_metadata_without_new_cross_role_binding_rejected(self):
        self.r['evidence']['whole-module-review']['expected_fields']['identity']='fake-new-reviewer'
        self.rejects('stale maintenance binding')

    def test_new_root_digest_does_not_refresh_old_receipts(self):
        self.put(self.r['lesson_path'], 'Genuine changed lesson needs new reviews.\n')
        self.r['binding_sha256']=m.binding_digest(self.root,self.r)
        self.rejects('scope/context mismatch')

    def test_lean_names_are_case_sensitive(self):
        self.inventory['SYNTHETIC_ONLY.Leaf0']=self.inventory.pop('SYNTHETIC_ONLY.leaf1')
        self.r['declarations']=sorted(self.inventory)
        self.refresh();self.validate()
        self.r['declarations']=[n.lower() for n in self.r['declarations']]
        self.rejects('whole public inventory')

    def test_json_number_boolean_and_float_are_not_interchangeable(self):
        e=self.receipts['compiled-runtime']
        for expected, altered in ((1,True),(1,1.0),(True,1),(0,False),(False,0)):
            # Unknown extra metadata is still bound: nested fields must have
            # the same JSON type, not merely compare equal in Python.
            e['synthetic_type_marker']={'value':expected}
            self.refresh();self.validate()
            e['synthetic_type_marker']={'value':altered}
            ref=self.r['evidence']['compiled-runtime']
            ref['sha256']=self.dump(ref['path'],e)
            with self.subTest(expected=repr(expected),altered=repr(altered)):
                self.rejects('receipt semantics differ')
            e['synthetic_type_marker']={'value':expected}
            self.refresh()

    def test_runtime_identifier_true_cannot_replace_number_one(self):
        e=self.receipts['compiled-runtime'];e['workflow_run_id']=1
        self.refresh();self.validate()
        e['workflow_run_id']=True
        ref=self.r['evidence']['compiled-runtime'];ref['sha256']=self.dump(ref['path'],e)
        self.rejects('receipt semantics differ')

class RealGitDiffFormatTests(unittest.TestCase):
    def test_fixed_abbreviation_ignores_repository_default(self):
        import subprocess
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            def git(*args):
                return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.PIPE)
            git('init','--quiet')
            git('config','core.autocrlf','false')
            module='sample.lean'
            (root/module).write_bytes(b'theorem sample : True := by trivial\n')
            git('add','--',module)
            git('-c','user.name=synthetic-test','-c','user.email=synthetic@example.invalid','commit','--quiet','-m','synthetic fixture')
            base=git('rev-parse','HEAD').decode().strip()
            (root/module).write_bytes(b'theorem sample : True := True.intro\n')
            stable=[];defaults=[]
            for width in ('7','8','12','40'):
                git('config','core.abbrev',width)
                fixed=m.git_bytes(root,'diff','--no-ext-diff','--no-renames','--abbrev=8',base,'--',module)
                stable.append(fixed)
                defaults.append(m.git_bytes(root,'diff','--no-ext-diff','--no-renames',base,'--',module))
                index=next(x for x in fixed.splitlines() if x.startswith(b'index '))
                before,after=index.split()[1].split(b'..')
                self.assertEqual((len(before),len(after)),(8,8))
            self.assertTrue(all(x==stable[0] for x in stable))
            self.assertEqual(len(set(defaults)),4)

if __name__ == '__main__': unittest.main()
