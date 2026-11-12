"""Prospective finite-SP whole-module binding and fail-closed evidence tests."""
import copy,hashlib,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'reviews/publication/sp-extended-c44'
class ProspectiveFiniteSPTests(unittest.TestCase):
    def setUp(self):
        spec=importlib.util.spec_from_file_location('original_sp_prospective_gate',ROOT/'website/scripts/check_research_publications.py')
        self.gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.gate)
        self.context=json.loads((BASE/'prospective-context.json').read_bytes())
        self.inventory={r['fullName']:r for r in json.loads((ROOT/'web/library/declarations.json').read_bytes())['declarations']}
    def test_all_three_bindings_and_exact_public_inventory(self):
        self.assertEqual(len(self.context['records']),3)
        self.assertEqual(sum(len(r['declarations']) for r in self.context['records']),67)
        for record in self.context['records']:
            self.assertEqual(record['binding_sha256'],self.gate.binding_digest(ROOT,record))
            self.assertEqual(set(record['declarations']),{n for n,r in self.inventory.items() if r.get('source')==record['module']})
    def test_exact_local_source_and_retrospective_scope(self):
        source=self.context['source_row']
        self.assertEqual(hashlib.sha256((ROOT/source['lesson_path']).read_bytes()).hexdigest(),self.context['source_contract_sha256'])
        self.assertEqual(source['provenance'],'RETROSPECTIVE_IMPLEMENTATION_INFORMED_NOT_PREPROOF')
        self.assertEqual(self.context['historical_formalizer'],'UNKNOWN')
        self.assertFalse(self.context['publication_acceptance']);self.assertFalse(self.context['PURIFIED'])
    def test_graph_retains_conditional_cost_boundary(self):
        for record in self.context['records']:
            graph=record['graph_contribution']; raw=(ROOT/graph['graph_context']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),graph['graph_context_sha256'])
            self.assertIn('conditional',json.loads(raw)['H3_serialized_cost_condition'])
            self.assertFalse(graph['proof_term_dependency_claim'])
    def test_absent_actual_decoder_is_rejected_for_each_module(self):
        for original in self.context['records']:
            record=copy.deepcopy(original)
            record['decoder_evidence']='reviews/publication/sp-extended-c44/mandatory-never-created-decoder.json'
            self.assertFalse((ROOT/record['decoder_evidence']).exists())
            with self.assertRaisesRegex(ValueError,'missing evidence file'):
                self.gate.validate_record(ROOT,record,self.inventory)
    def test_changed_source_statement_invalidates_each_binding(self):
        for original in self.context['records']:
            record=copy.deepcopy(original);record['source_statement']+=' Unsupported family claim.'
            with self.assertRaisesRegex(ValueError,'publication binding is stale'):
                self.gate.validate_record(ROOT,record,self.inventory)
if __name__=='__main__':unittest.main()
