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

class CostFrontierTests(unittest.TestCase):
    def test_actual_gate_and_own_output(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes());a,b=r['records']
        self.assertEqual(r['status'],'PROVED_LOCALLY_FOCUSED');self.assertEqual(r['actual_proved_roots'],1)
        self.assertEqual([a['exit_code'],b['exit_code']],[0,0])
        self.assertEqual(b['selected_direct_provider_hashes'],[a['own_output_sha256']])
        self.assertEqual(sha((ROOT/'ExplicitFiveBlockCostProof.lean').read_bytes()),a['source_sha256'])
        self.assertEqual(sha((ROOT/'ExplicitFiveBlockCostChecks.lean').read_bytes()),b['source_sha256'])
    def test_axiom_gate_and_nonclaims(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes());rows=r['records'][1]['axiom_reports']
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['name'],'HermiteExplicitCachedStored.produceExplicitStored_cost_counters')
        self.assertEqual(set(rows[0]['axioms']),{'Classical.choice','Quot.sound','propext'})
        for key in ['scientific_ROOT','main_merged','clean_transitive_TCB','independent_proof_review',
                    'value_refinement_or_full_same_run_closed','native_bit_GCD_evaluator_allocation_sharing_or_full_SP_resources']:
            self.assertFalse(r[key],key)
    def test_failed_predecessors_are_preserved(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            for folder in ['hermite-c256-explicit-five-block-cost-proof','hermite-c259-explicit-five-block-cost-successor-proof']:
                r=json.loads(z.read(folder+'/proof-result.json'))
                self.assertEqual(r['records'][0]['exit_code'],1)
                self.assertIsNone(r['records'][0]['own_output_sha256'])
    def test_same_result_signature_no_added_premises(self):
        s=(ROOT/'ExplicitFiveBlockCostChecks.lean').read_text(encoding='utf-8')
        self.assertIn('let result := produceExplicitStored k n R delta',s)
        self.assertIn('result.run.cost',s);self.assertIn('result.quotientCalls',s);self.assertIn('result.remainderCalls',s)
        self.assertNotIn('hR',s);self.assertNotIn('axiom ',s);self.assertNotIn('sorry',s)
