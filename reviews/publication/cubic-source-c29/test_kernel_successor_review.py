"""Original successor review is scoped evidence, not source/root admission."""
import hashlib,json,re,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
class KernelSuccessorReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt=json.loads((ROOT/'reports/lean-433-migration/c29-kernel-successor-review-transport.json').read_bytes())
        cls.raw=(ROOT/cls.receipt['bundle']).read_bytes()
        with zipfile.ZipFile(ROOT/cls.receipt['bundle']) as z:cls.files={n:z.read(n) for n in z.namelist()}
        cls.seal=json.loads(cls.files['kernel-successor-actual-v1-seal.json'])
    def test_exact_eight_members_no_host_paths(self):
        r=self.receipt;self.assertEqual(hashlib.sha256(self.raw).hexdigest(),r['bundle_sha256'])
        self.assertEqual(len(self.files),8);self.assertEqual(set(self.files),{m['name'] for m in r['members']})
        for m in r['members']:
            raw=self.files[m['name']];self.assertEqual(len(raw),m['bytes'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(),m['sha256'])
            self.assertIsNone(re.search(rb'(?:[A-Za-z]:[\\/](?:Users|qb261009)|/home/runner/|github_pat_|ghp_)',raw))
    def test_native_delta_and_historical_discrepancy_are_distinct(self):
        s=self.seal;self.assertEqual(s['observations']['generatedRemovedNativeAxioms'],9)
        self.assertEqual(s['observations']['newOrdinaryTheoremHelpers'],8)
        self.assertTrue(s['observations']['perOldRecordRecursiveAxiomsExactlyOldMinusNine'])
        self.assertTrue(s['oldArtifacts']['historicalD1NotErased']);self.assertTrue(s['oldArtifacts']['allOriginalHashesUnchanged'])
    def test_residuals_and_no_admission_preserved(self):
        s=self.seal;self.assertTrue(s['residuals']['newFreshCompleteTwoTypeSupplementAbsent'])
        self.assertEqual(len(s['residuals']['currentPPTypeOmissionNames']),2)
        self.assertEqual(s['residuals']['valueOmissionRows'],96)
        self.assertTrue(s['residuals']['noUniversalAllProofPPTokenReadingRequirement'])
        for obj in (s,self.receipt):
            self.assertIsNone(obj['sourceAgreement']);self.assertIsNone(obj['publicationBinding'])
            self.assertFalse(obj['nativeAccepted']);self.assertFalse(obj['scientific_ROOT'])
if __name__=='__main__':unittest.main()
