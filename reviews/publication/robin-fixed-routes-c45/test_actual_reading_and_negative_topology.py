"""Actual independent reading and negative graph results must not turn green."""
import hashlib,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'reviews/publication/robin-fixed-routes-c45'
class IndependentReadingNegativeTests(unittest.TestCase):
    def test_all_actual_decoder_payloads_match_the_original_seal(self):
        with zipfile.ZipFile(BASE/'formal-decoder-original7.zip') as z:
            seal=json.loads(z.read('seal.json'))
            self.assertEqual(seal['scope']['explicit_target_declarations'],215)
            self.assertFalse(seal['independence']['natural_source_read'])
            for row in seal['integrity']['artifacts']:
                self.assertEqual(hashlib.sha256(z.read(row['path'])).hexdigest(),row['sha256'])
                self.assertEqual(len(z.read(row['path'])),row['bytes'])
    def test_full_source_formal_reading_keeps_its_limits(self):
        with zipfile.ZipFile(BASE/'source-review-phase2-original10.zip') as z:
            seal=json.loads(z.read('stage2-seal.json'))
            self.assertEqual(seal['coverage']['target_declarations'],215)
            self.assertEqual(seal['coverage']['target_lines'],2694)
            self.assertFalse(seal['cross_reader_or_author_classification_material_read'])
            for row in seal['artifacts']:
                self.assertEqual(hashlib.sha256(z.read(row['path'])).hexdigest(),row['sha256'])
            text=z.read('static-comparison.md').decode()
            self.assertIn('pureAncilla=0',text)
            self.assertIn('two pure ancilla wires',text)
    def test_negative_topology_is_required_changes_not_source_proof(self):
        with zipfile.ZipFile(BASE/'topology-v1-requires-changes-original6.zip') as z:
            seal=json.loads(z.read('seal.json'))
            self.assertEqual(seal['source_first_coverage_verdict'],'ACCEPTED_BOUNDED_LOCAL')
            self.assertEqual(seal['source_first_topology_verdict'],'REQUIRES_CHANGES')
            self.assertEqual(seal['author_topology_verdict'],'REQUIRES_CHANGES')
            self.assertEqual(seal['finding_ids'],['F01','F02','F03','F04','F05','F06'])
            self.assertFalse(seal['validation']['formal_artifact_access'])
            for row in seal['artifacts']:
                self.assertEqual(hashlib.sha256(z.read(row['path'].split('/')[-1])).hexdigest(),row['sha256'])
if __name__=='__main__':unittest.main()
