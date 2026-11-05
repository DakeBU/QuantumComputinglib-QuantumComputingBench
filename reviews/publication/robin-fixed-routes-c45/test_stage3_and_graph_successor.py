"""Preserve actual comparison and unapproved graph successor as distinct objects."""
import hashlib,json,unittest,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
class Stage3AndGraphSuccessorTests(unittest.TestCase):
    def test_actual_comparison_is_complete_but_not_admission(self):
        with zipfile.ZipFile(BASE/'source-review-phase3-original9.zip') as z:
            seal=json.loads(z.read('stage3-seal.json'))
            self.assertEqual(seal['actual_read_scope']['declaration_interpretations_read'],215)
            self.assertEqual(seal['actual_read_scope']['slots'],77)
            self.assertFalse(seal['opaque_wrapper_or_final_binding_created'])
            self.assertFalse(seal['purification_publication_or_main_admission_claimed'])
            self.assertIn('G01-G06',seal['residuals'][0])
            for row in seal['artifacts']:
                self.assertEqual(hashlib.sha256(z.read(row['path'])).hexdigest(),row['sha256'])
                self.assertEqual(len(z.read(row['path'])),row['bytes'])
    def test_author_successor_is_not_independent_acceptance(self):
        with zipfile.ZipFile(BASE/'graph-v2-author-proposal-original12.zip') as z:
            seal=json.loads(z.read('seal.json'))
            self.assertEqual(seal['state'],'SEALED_AUTHOR_REORGANIZATION_PROPOSAL')
            self.assertEqual(seal['independent_new_source_only_review'],'PENDING')
            self.assertIsNone(seal['expected_acceptance'])
            self.assertTrue(seal['validation']['source_reconstruction_exact'])
            self.assertTrue(seal['validation']['G01_G06_unchanged'])
            self.assertFalse(seal['validation']['graph_math_accepted'])
            for row in seal['artifacts']:
                self.assertEqual(hashlib.sha256(z.read(row['path'])).hexdigest(),row['sha256'])
if __name__=='__main__':unittest.main()
