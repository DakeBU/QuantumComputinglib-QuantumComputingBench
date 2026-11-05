import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class ExactCheckpoint(unittest.TestCase):
    def test_exact_archived_originals(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes())
        for n,h in b['payloads'].items():self.assertEqual(sha((ROOT/n).read_bytes()),h,n)
        self.assertEqual(sha((ROOT/'original-freezes.zip').read_bytes()),b['archive_sha256'])
        with ZipFile(ROOT/'original-freezes.zip') as z:
            self.assertEqual(set(z.namelist()),set(b['original_members']))
            for n,r in b['original_members'].items():
                raw=z.read(n);self.assertEqual((len(raw),sha(raw)),(r['bytes'],r['sha256']))
        self.assertFalse(b['main_merged']);self.assertFalse(b['scientific_ROOT'])

class ErrorAnalysis(unittest.TestCase):
    def test_existing_interface_not_new_acceptance(self):
        r=json.loads((ROOT/'parent-intake.json').read_bytes())
        self.assertTrue(r['all_hashes_match']);self.assertEqual(r['current_inputs'],55)
        for n in ['new_proofs','new_compilations']:self.assertEqual(r[n],0)
        for n in ['budget_or_target_changed','scientific_ROOT','independent_review','full_arbitrary_Real_L_representation']:self.assertFalse(r[n])
    def test_wrong_exponent_preserved_and_explicitly_corrected(self):
        c=json.loads((ROOT/'explicit-source-correction.json').read_bytes())
        self.assertEqual(c['corrected_original_analysis_sha256'],sha((ROOT/'ANALYSIS.md').read_bytes()))
        self.assertEqual(c['corrected_original_manifest_sha256'],sha((ROOT/'INPUT_MANIFEST.json').read_bytes()))
        self.assertIn(b'actual exponential input is -p^2',(ROOT/'ANALYSIS.md').read_bytes())
        self.assertTrue(c['all_actual_exponential_inputs_nonpositive']);self.assertTrue(c['original_target_not_Gaussian'])
        self.assertEqual(set(c['correct_literal_branches']),{'left','middle','right'})
        self.assertFalse(c['scientific_target_changed']);self.assertFalse(c['existing_error_budget_changed'])
