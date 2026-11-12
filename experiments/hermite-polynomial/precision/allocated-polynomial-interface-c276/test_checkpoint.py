import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class ExactBindings(unittest.TestCase):
    def test_payloads_and_exact_originals(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes())
        for n,h in b['payloads'].items():self.assertEqual(sha((ROOT/n).read_bytes()),h,n)
        with ZipFile(ROOT/'original-freezes.zip') as z:
            self.assertEqual(set(z.namelist()),set(b['original_members']))
            for n,r in b['original_members'].items():
                raw=z.read(n);self.assertEqual(len(raw),r['bytes']);self.assertEqual(sha(raw),r['sha256'])
        self.assertFalse(b['scientific_ROOT']);self.assertFalse(b['main_merged'])

class TypedNotProved(unittest.TestCase):
    def test_three_typed_zero_proofs(self):
        r=json.loads((ROOT/'type-probe-result.json').read_bytes())
        self.assertEqual((r['proposition_formations'],r['proved_roots']),(3,0))
        a,b=r['records'];self.assertEqual([a['exit_code'],b['exit_code']],[0,0])
        self.assertEqual(b['selected_direct_provider_hashes'],[a['own_output_sha256']])
    def test_real_seal_does_not_authorize_or_prove(self):
        s=json.loads((ROOT/'STATEMENT_SEAL.json').read_bytes())
        self.assertEqual(s['definition_sha256'],sha((ROOT/'AllocatedPolynomialCostInterface.lean').read_bytes()))
        self.assertEqual(s['actual_proved_roots'],0);self.assertFalse(s['proof_search_authorized'])
        self.assertFalse(s['actual_native_bit_GCD_evaluator_allocator_quantum_resources_or_scientific_ROOT'])
