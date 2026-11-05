"""Exact evidence/negative boundary regressions, not semantic truth tests."""
import hashlib
import json
from pathlib import Path
import re
import unittest
from zipfile import ZipFile

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest()
class FrozenStageTests(unittest.TestCase):
    def archive(self,name,file):
        with ZipFile(BASE/(name+'-original.zip')) as z:return z.read(file)
    def obj(self,name,file):return json.loads(self.archive(name,file))
    def test_exact_archives_and_all_original_members(self):
        index=json.loads((BASE/'index.json').read_bytes())
        self.assertEqual(len(index['archives']),7)
        self.assertEqual(sum(len(a['members']) for a in index['archives']),65)
        for row in index['archives']:
            self.assertEqual(sha((BASE/row['archive']).read_bytes()),row['sha256'])
            with ZipFile(BASE/row['archive']) as z:
                self.assertEqual(set(z.namelist()),set(row['members']))
                for n,v in row['members'].items():
                    self.assertEqual(sha(z.read(n)),v['sha256'])
                    self.assertEqual(len(z.read(n)),v['bytes'])
    def test_no_private_images_or_host_paths_in_public_payloads(self):
        for path in BASE.glob('*.zip'):
            with ZipFile(path) as z:
                for n in z.namelist():
                    self.assertNotIn('_private/',n)
                    self.assertFalse(n.lower().endswith(('.png','.pdf')))
                    s=z.read(n).decode('utf-8-sig')
                    for _ in range(2):s=s.replace('\\\\','\\')
                    self.assertIsNone(re.search(r'(?<![A-Za-z0-9])[A-Za-z]:[/\\]',s),n)
                    self.assertNotIn('/'+'home/runner/',s)
    def test_hbi_real_positive_negative_and_nonlaunch_preserved(self):
        o=self.obj('hbi-c100-raw-runtime-association','runtime-observations.json')
        self.assertEqual([r['exit_code'] for r in o['executions']],[None,0,1,0])
        self.assertEqual([r['launched'] for r in o['executions']],[False,True,True,True])
        self.assertEqual(o['inherited_provider_modules'],29)
        self.assertFalse(o['final_admission'])
        self.assertFalse(o['repository_cache_written_or_built'])
        self.assertEqual(o['actual_repaired_audit_stdout'].count('depends on axioms: [propext,'),2)
        self.assertEqual(len(o['private_retained_inventory']),118)
    def test_robin_exact_narrow_successor_preserves_all_other_source_lines(self):
        old=BASE.parent/'migration-checkpoints-c109/robin-source-only-original4.zip'
        with ZipFile(old) as z:before=z.read('whole-natural-source.md').decode().splitlines()
        after=self.archive('robin-c111-source-successor','natural-source-v2.md').decode().splitlines()
        self.assertEqual(len(before),113);self.assertEqual(len(after),113)
        self.assertEqual([i+1 for i,(a,b) in enumerate(zip(before,after)) if a!=b],[103])
        seal=self.obj('robin-c104-source-successor-review','source-successor-review-seal.json')
        self.assertEqual(seal['verdict'],'ACCEPT_NARROW_SOURCE_TOPOLOGY_SUCCESSOR_F01_T02_ONLY')
        self.assertTrue(all(v is False for v in seal['not_granted'].values()))
    def test_temporary_and_own_formal_freeze_retains_source_input_and_limits(self):
        manifest=self.obj('temporary-and-c110-own-formal-first','manifest.json')
        self.assertEqual(manifest['state'],'OWN_FORMAL_ONLY')
        self.assertFalse(manifest['prior_source_only_freeze']['rewritten_in_this_phase'])
        self.assertEqual(manifest['prior_source_only_freeze']['seal_sha256'],
                         'dddfc589403e962639008468f253c39dfb5cc5a7bf49b5a2d6c74dda13b28e47')
        self.assertIn('operation/composition',self.archive('temporary-and-c110-own-formal-first','findings.md').decode())
    def test_actual_decoder_remains_source_blind_not_compiler_evidence(self):
        e=self.obj('temporary-and-c107-blind-decoder','evidence.json')
        self.assertEqual(e['inventory_counts']['target_definitions'],6)
        self.assertEqual(e['inventory_counts']['target_theorems'],5)
        self.assertFalse(e['source_blindness']['natural_source_or_title_supplied'])
        self.assertFalse(e['execution']['lean_or_compiler_run'])
    def test_actual_c34_diagnostic_is_two_pins_not_a_math_refutation(self):
        r=json.loads((ROOT/'reports/lean-433-migration/c112-c34-frozen-candidate-drift.json').read_bytes())
        self.assertEqual(r['candidate_count'],220);self.assertEqual(r['mismatch_count'],2)
        self.assertEqual({x['path'] for x in r['mismatches']},
            {'QuantumBlockEncoding/CubicAmplitudePrimitive.lean','QuantumBlockEncoding/CubicStatePreparation.lean'})
        self.assertFalse(r['lean_launched_by_this_CI_step'])
        self.assertFalse(r['nativeAccepted']);self.assertFalse(r['scientific_ROOT'])
        self.assertEqual((r['python_tests_run'],r['python_errors']),(35,1))

if __name__=='__main__':unittest.main()
