"""Terminal helper absence is not an attempted proof or mathematical failure."""
import hashlib,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
class KernelHelperFailureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/'reports/lean-433-migration/c31-kernel-ci1-shadow-helper-failure.json').read_bytes())
        with zipfile.ZipFile(ROOT/cls.r['bundle']) as z:cls.f={n:z.read(n) for n in z.namelist()}
    def test_exact26_terminal_public_capture(self):
        self.assertEqual(hashlib.sha256((ROOT/self.r['bundle']).read_bytes()).hexdigest(),self.r['bundle_sha256'])
        self.assertEqual(len(self.f),26)
        for row in self.r['members']:self.assertEqual(hashlib.sha256(self.f[row['path']]).hexdigest(),row['sha256'])
    def test_two_queries_zero_compiled_targets_and_real_helper_exception(self):
        self.assertEqual(self.r['actual_fresh_target_compiles'],0)
        self.assertNotIn('fresh-target-cohort.json',self.f);self.assertNotIn('30-observe.result.json',self.f)
        for step in ['01-help','02-prefix']:
            self.assertEqual(json.loads(self.f[step+'.result.json'])['exitCode'],0)
        r=json.loads(self.f['result.json']);self.assertEqual(r['failureType'],'FileNotFoundError')
        self.assertIn('$CANDIDATE_WORKSPACE/tools/cubic_c29_diagnostic/runner.py',r['failure'])
    def test_execution_guard_receipt_and_no_admission(self):
        e=json.loads(self.f['executing-code-bindings.json'])
        self.assertEqual(len(e['modules']),3);self.assertFalse(e['OSAttestation']);self.assertFalse(e['codeObjectAttestation'])
        r=json.loads(self.f['kernel-successor-result.json'])
        self.assertFalse(r['nativeAccepted']);self.assertIsNone(r['sourceAgreement'])
        self.assertIn('NOT_MATHEMATICAL_REFUTATION',r['status'])
if __name__=='__main__':unittest.main()
