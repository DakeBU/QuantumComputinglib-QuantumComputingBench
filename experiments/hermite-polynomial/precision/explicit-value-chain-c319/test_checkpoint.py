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

class ValueRefinement(unittest.TestCase):
    def test_exact_new_own_chain_consumed(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes());a,b=r['records']
        self.assertEqual(r['actual_own_consumed_public_roots'],7)
        self.assertEqual([a['exit_code'],b['exit_code']],[0,0])
        self.assertEqual(b['selected_provider_hashes'],[a['own_output_sha256']])
        self.assertEqual(len(a['axiom_reports']),9);self.assertEqual(len(b['axiom_reports']),7)
        allowed={'propext','Classical.choice','Quot.sound'}
        for row in a['axiom_reports']+b['axiom_reports']:
            self.assertTrue(set(row['axioms'])<=allowed);self.assertTrue(row['axioms'])
        expected={'decode_value','comparisonQ_value','translationQ_actual_factorials','produceExplicitQData_value','produceExplicitData_window','produceExplicitStored_refines','produceExplicitStored_source'}
        self.assertEqual({x['name'].split('.')[-1] for x in b['axiom_reports']},expected)
        self.assertFalse(r['same_run_cost_or_finitebit_or_scientific_ROOT'])
        self.assertFalse(r['independent_proof_review']);self.assertFalse(r['clean_transitive_TCB'])
    def test_exact_author_consumer_and_two_carrier_checkpoints(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            old=z.read('hermite-c319-explicit-chain-common-carriers/ValueProofChecks.lean')
            self.assertEqual(old,(ROOT/'ValueProofChecks.lean').read_bytes())
            m=json.loads(z.read('hermite-c319-explicit-chain-common-carriers/input-manifest.json'))
            self.assertEqual(m['source_scope_checks']['statement_count'],13)
            self.assertTrue(m['binding_preservation']['all_13_public_private_statement_texts_identical'])
        s=(ROOT/'ExplicitChainValueProof.lean').read_text()
        self.assertIn('C319_TYPECHECK_K',s);self.assertIn('C319_TYPECHECK_Q',s)
        self.assertNotIn('produceExplicitStored_same_run',(ROOT/'ValueProofChecks.lean').read_text())
    def test_plan_metadata_does_not_claim_a_new_scalar_gate(self):
        c=json.loads((ROOT/'plan-field-clarification.json').read_bytes())
        self.assertFalse(c['new_scalar_closure_credit']);self.assertTrue(c['preserve_original_plan_and_wrapper'])
        r=json.loads((ROOT/'proof-result.json').read_bytes())
        self.assertEqual([x['module'] for x in r['records']],['ExplicitChainValueProof','ValueProofChecks'])
