"""A subsequent scoped reviewer judgment never rewrites its predecessor."""
import hashlib,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
class CurrentTypesOriginalReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/'reports/lean-433-migration/c29-current-two-types-original-review.json').read_bytes())
        with zipfile.ZipFile(ROOT/cls.r['bundle']) as z:cls.f={n:z.read(n) for n in z.namelist()}
        cls.s=json.loads(cls.f['kernel-two-types-actual-v2-seal.json'])
    def test_exact_three_file_transport(self):
        self.assertEqual(hashlib.sha256((ROOT/self.r['bundle']).read_bytes()).hexdigest(),self.r['bundle_sha256'])
        self.assertEqual(len(self.f),3)
        for row in self.r['members']:
            self.assertEqual(hashlib.sha256(self.f[row['name']]).hexdigest(),row['sha256'])
            self.assertEqual(len(self.f[row['name']]),row['bytes'])
    def test_current_actual_types_and_old_bytes_remain_distinct(self):
        s=self.s;c=s['scopedConclusions'];self.assertTrue(s['sameOriginalSourceFirstReviewer'])
        self.assertTrue(s['all36PriorHashesUnchanged']);self.assertEqual(len(s['preservedPriorReviewerArtifacts']),36)
        self.assertTrue(c['R1CurrentActualTypeTextResolved']);self.assertTrue(c['newSameFreshObservationNotOldRunRelabel'])
        self.assertEqual([t['characters'] for t in s['actualTypeComparison']['types']],[163920,189640])
        with zipfile.ZipFile(ROOT/'reviews/publication/cubic-source-c29/kernel-two-types-v2-actual-public.zip') as z:
            for row in s['actualTypeComparison']['zipMembers']:
                self.assertEqual(hashlib.sha256(z.read(row['path'].split('/',1)[1])).hexdigest(),row['sha256'])
    def test_no_admission_or_invented_value_printing_gate(self):
        c=self.s['scopedConclusions'];self.assertEqual(c['remainingValueOmissionRows'],96)
        self.assertTrue(c['noUniversalAllOrdinaryProofTokensMustBeLosslesslyPrintedRuleInvented'])
        for obj in (self.s,self.r):
            self.assertIsNone(obj['sourceAgreement']);self.assertIsNone(obj['publicationBinding'])
            self.assertFalse(obj['nativeAccepted']);self.assertFalse(obj['scientific_ROOT'])
if __name__=='__main__':unittest.main()
