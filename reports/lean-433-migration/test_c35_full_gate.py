"""Do not confuse a full cached Lean gate with a finite-bit family certificate."""
import hashlib,json,subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class FullGateEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=json.loads((ROOT/'reports/lean-433-migration/c35-full-lean-export-existing-ci.json').read_bytes())
    def test_actual_full_commands_and_terminal_successes(self):
        self.assertEqual(self.r['full_Lean_commands'],['lake build QuantumBlockEncoding.HermiteStatePreparation','lake build','lake build Tests'])
        self.assertEqual(self.r['full_Lean_success_job_counts'],[3165,3399,3460])
        for job in self.r['jobs']:
            self.assertEqual(job['conclusion'],'success')
            lines=job['selected_verbatim_lines']
            for row in lines:self.assertEqual(hashlib.sha256(row['verbatim'].encode()).hexdigest(),row['line_sha256'])
            self.assertTrue(any(self.r['checkout_merge_commit_observed_in_both_logs'] in r['verbatim'] for r in lines))
        lines='\n'.join(x['verbatim'] for x in self.r['jobs'][0]['selected_verbatim_lines'])
        for count in [3165,3399,3460]:self.assertIn(f'Build completed successfully ({count} jobs).',lines)
    def test_checked_merge_tree_and_current_committed_proof_inputs(self):
        self.assertTrue(self.r['merge_tree_equals_51d_tree'])
        self.assertEqual(self.r['api_merge_parents'],['f2cba045611a0d11c5995c29607569726bf1d6c5','51d959e6c09200f890e44ea13ad122ca58384720'])
        tree=subprocess.check_output(['git','-C',str(ROOT),'rev-parse',self.r['api_merge_parents'][1]+'^{tree}']).decode().strip()
        self.assertEqual(tree,self.r['merge_tree_sha'])
        for row in self.r['committed_inputs']:
            raw=subprocess.check_output(['git','-C',str(ROOT),'show','HEAD:'+row['path']])
            self.assertEqual(hashlib.sha256(raw).hexdigest(),row['committed_raw_sha256'])
    def test_finite_baseline_replay_never_becomes_polynomial_root(self):
        r=self.r['finite_replay']
        self.assertTrue(r['passed']);self.assertFalse(r['lean_certificate_claimed'])
        self.assertEqual(r['parameters'],{'L':1.0,'k':1,'n':3})
        self.assertEqual(r['evidence_class'],'independent-finite-replay')
        self.assertEqual(self.r['finite_self_tests'],15)
        self.assertIn('EXPONENTIAL_REFERENCE',self.r['finite_export_task'])
        for key in ['main_merged','scientific_ROOT','PURIFIED','nativeAccepted','production_sources_changed']:self.assertFalse(self.r[key])
if __name__=='__main__':unittest.main()
