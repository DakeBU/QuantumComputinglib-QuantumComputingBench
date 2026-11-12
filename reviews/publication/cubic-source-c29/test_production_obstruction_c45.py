"""Historical source cohorts and independent obstruction cannot be conflated."""
import hashlib,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
class ProductionObstructionC45Tests(unittest.TestCase):
    def test_frozen_nine_proof_delta_exactly_reconstructs_kernel_candidate(self):
        with zipfile.ZipFile(ROOT/'tools/cubic_c29_kernel_ci1/public-runtime-package.zip') as z:
            original=z.read('original/CubicStatePreparation.lean');candidate=z.read('candidate/CubicStatePreparation.lean')
        self.assertEqual(hashlib.sha256(original).hexdigest(),'d125f8c239bca1c15e6e4fa6e788df6dd8984394630cb2dcc9be8946c4cbcb55')
        self.assertEqual(hashlib.sha256(candidate).hexdigest(),'6ee53311b5d6e18c46afb3e068341689acb86f1bdbc425e774705e81c9142f44')
        self.assertEqual(original.count(b'native_decide'),9)
        replacement=original.replace(b'native_decide',b'decide +kernel')
        before=b'have hzero : (0 : Rat) - 0 = 0 := by decide +kernel'
        self.assertEqual(replacement.count(before),1)
        replacement=replacement.replace(before,b'have hzero : (0 : Rat) - 0 = 0 := by exact Rat.sub_self')
        self.assertEqual(replacement,candidate)
        self.assertNotEqual(original,candidate)
    def test_sealed_diagnosis_does_not_authorize_unchanged_native_admission(self):
        with zipfile.ZipFile(ROOT/'reviews/publication/cubic-source-c29/production-obstruction-c45-original6.zip') as z:
            seal=json.loads(z.read('seal.json'))
            self.assertIn('NATIVE_AUTHORIZATION_UNESTABLISHED',seal['status'])
            self.assertTrue(seal['oldSealedEvidencePreservation']['allHashesUnchanged'])
            for row in seal['payloads']:
                self.assertEqual(hashlib.sha256(z.read(row['path'].split('/')[-1])).hexdigest(),row['sha256'])
            self.assertFalse(any(n.endswith('-reviewer.json') for n in z.namelist()))
if __name__=='__main__':unittest.main()
