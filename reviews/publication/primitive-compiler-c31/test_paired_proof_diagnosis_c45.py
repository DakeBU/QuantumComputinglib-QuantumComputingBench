"""C31 frozen diagnosis must not conflate candidate and production evidence."""
import hashlib,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
class PairedProofDiagnosisC45Tests(unittest.TestCase):
    def test_three_proof_successor_and_actual_original_diagnosis(self):
        with zipfile.ZipFile(ROOT/'reviews/publication/primitive-compiler-c31/production-obstruction-c45-original6.zip') as z:
            seal=json.loads(z.read('seal.json'))
            self.assertEqual(seal['kind'],'SEALED_DIAGNOSIS_NOT_ACCEPTED_ROLE_EVIDENCE')
            self.assertFalse(seal['production_modified'])
            self.assertFalse(seal['accepted_role_JSON_created'])
            self.assertTrue(seal['findings']['Cubic_exact_three_proof_only_bytes'])
            self.assertTrue(seal['findings']['standard3_axioms_not_axiomfree'])
            for row in seal['payload']:
                self.assertEqual(hashlib.sha256(z.read(row['name'])).hexdigest(),row['sha256'])
            self.assertEqual(hashlib.sha256(z.read('public-allowlist.json')).hexdigest(),seal['public_allowlist_sha256'])
        candidate=(ROOT/'tools/c31_kernel_proof_v1/candidate/QuantumBlockEncoding/CubicAmplitudePrimitive.lean').read_bytes()
        self.assertEqual(hashlib.sha256(candidate).hexdigest(),seal['findings']['candidate_Cubic'])
        self.assertEqual(candidate.count(b'decide +kernel +revert'),3)
        original=candidate.replace(b'decide +kernel +revert',b'native_decide +revert')
        self.assertEqual(hashlib.sha256(original).hexdigest(),seal['findings']['production_Cubic'])
if __name__=='__main__':unittest.main()
