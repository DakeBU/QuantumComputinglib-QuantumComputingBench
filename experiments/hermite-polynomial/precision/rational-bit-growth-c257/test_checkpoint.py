import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class BindingTests(unittest.TestCase):
    def test_exact_payloads(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes())
        for n,h in b['payloads'].items():self.assertEqual(sha((ROOT/n).read_bytes()),h,n)
        self.assertFalse(b['scientific_ROOT']);self.assertFalse(b['main_merged'])
    def test_exact_original_archive(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes());a=b['archive']
        self.assertEqual(sha((ROOT/a['file']).read_bytes()),a['sha256'])
        with ZipFile(ROOT/a['file']) as z:
            self.assertEqual(set(z.namelist()),set(a['members']))
            for n,row in a['members'].items():
                raw=z.read(n);self.assertEqual(len(raw),row['bytes']);self.assertEqual(sha(raw),row['sha256'])

class BitFrontierTests(unittest.TestCase):
    def test_is_design_not_proof(self):
        s=json.loads((ROOT/'FRONTIER_SEAL.json').read_bytes())
        self.assertEqual(s['classification'],'INTERNAL_SOURCE_ONLY_MATHEMATICAL_BOUND_DESIGN_NOT_PROVED')
        self.assertFalse(s['actual_actions']['compiler']);self.assertFalse(s['actual_actions']['new_Lean_proof_search'])
        self.assertIn('not yet admitted',' '.join(s['essential_dependencies']))
    def test_original_precision_and_radius_boundary(self):
        m=json.loads((ROOT/'INPUT_MANIFEST.json').read_bytes())
        self.assertEqual(m['allocated_precision_dependency']['unchanged_original'],
                         'sourceDelta=epsilon/(4*2^(n+1)*(k+1)^2*2^(2k)).')
        self.assertTrue(m['allocated_precision_dependency']['original_state_error_budget_unchanged'])
        self.assertTrue(m['allocated_precision_dependency']['no_pi_or_unspecified_L_representation_assumption'])
        self.assertTrue(m['allocated_precision_dependency']['radius_height'].startswith('OPEN'))
