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

class CommonDenominator(unittest.TestCase):
    def test_actual_same_own_output_and_exact_axioms(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes());a,b=r['records']
        self.assertEqual(r['actual_own_consumed_roots'],1)
        self.assertEqual([a['exit_code'],b['exit_code']],[0,0])
        self.assertEqual(b['selected_direct_provider_hashes'],[a['own_output_sha256']])
        self.assertEqual({x['name'] for x in b['axiom_reports']},{'HermiteRationalHeight.commonDenominator','C293ExactChecks.commonDenominatorExpandedCheck'})
        for x in b['axiom_reports']:self.assertEqual(set(x['axioms']),{'propext','Classical.choice','Quot.sound'})
    def test_no_other_primitive_or_producer_credit(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes())
        for k in ['primitive_roots_proved','actual_producer_height_native_GCD_evaluator_allocation_or_scientific_ROOT','independent_review','clean_transitive_TCB','main_merged']:self.assertFalse(r[k],k)
        self.assertFalse(r['source_zero_axiom_rows_are_empty_axiom_proof'])
