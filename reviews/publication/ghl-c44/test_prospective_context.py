"""Graph/metadata regression checks; independent acceptance is never inferred."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'reviews/publication/ghl-c44'


class ProspectiveContextTests(unittest.TestCase):
    def setUp(self):
        self.context = json.loads((BASE / 'prospective-context.json').read_bytes())
        self.graph = json.loads((BASE / 'source-topology-v2-proposal.json').read_bytes())
        with zipfile.ZipFile(BASE / 'ghl-c43-source-first.zip') as archive:
            self.old_graph = json.loads(archive.read('natural-topology.json'))

    def gate(self):
        spec = importlib.util.spec_from_file_location('original_gate_for_ghl_tests', ROOT / 'website/scripts/check_research_publications.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def inventory(self):
        return {r['fullName']: r for r in json.loads((ROOT / 'web/library/declarations.json').read_bytes())['declarations']}

    def test_conditional_record_is_not_explicit_candidate_construction(self):
        edges = {e['id']: e for e in self.graph['hyperedges']}
        self.assertEqual(edges['E19']['head'], ['M12.conditional-record-consequences'])
        self.assertEqual(edges['E20']['head'], ['M12.constructed-record'])
        self.assertNotIn('OR.record-construction', {x['id'] for x in self.graph['or_structure']})
        old_edges = {e['id']: e for e in self.old_graph['hyperedges']}
        self.assertEqual(edges['E20'], old_edges['E20'])
        self.assertEqual(edges['E21'], old_edges['E21'])

    def test_weaker_encoded_interface_has_explicit_local_gap_not_fake_closure(self):
        nodes = {n['id']: n for n in self.graph['nodes']}
        self.assertEqual(nodes['G.local-encoded-image-details']['kind'], 'SOURCE_GAP')
        self.assertEqual(nodes['M12.encoded-image-interface']['kind'], 'local-interface-mentioned')
        self.assertFalse(any('M12.encoded-image-interface' in e['head'] for e in self.graph['hyperedges']))
        self.assertIn('active specialization', nodes['M12.candidate-image']['claim'])

    def test_every_established_hyperedge_has_complete_resolved_nodes(self):
        ids = {n['id'] for n in self.graph['nodes']}
        self.assertEqual(len(ids), len(self.graph['nodes']))
        for edge in self.graph['hyperedges']:
            self.assertEqual(edge['mode'], 'AND')
            self.assertTrue(edge['tail'])
            self.assertTrue(edge['head'])
            self.assertLessEqual(set(edge['tail'] + edge['head']), ids)

    def test_prospective_record_binds_whole_actual_public_module(self):
        gate = self.gate()
        record = self.context['record']
        inventory = self.inventory()
        public = {name for name, row in inventory.items() if row.get('source') == record['module']}
        self.assertEqual(set(record['declarations']), public)
        self.assertEqual(len(public), 403)
        self.assertEqual(record['binding_sha256'], gate.binding_digest(ROOT, record))
        self.assertFalse(self.context['publication_acceptance'])
        self.assertFalse(self.context['main_merged'])
        self.assertEqual(self.context['historical_formalizer'], 'UNKNOWN')

    def test_missing_actual_decoder_is_rejected_by_original_gate(self):
        record = copy.deepcopy(self.context['record'])
        record['decoder_evidence'] = 'reviews/publication/ghl-c44/mandatory-nonexistent-decoder-test.json'
        self.assertFalse((ROOT / record['decoder_evidence']).exists())
        with self.assertRaisesRegex(ValueError, 'missing evidence file'):
            self.gate().validate_record(ROOT, record, self.inventory())

    def test_stale_source_statement_is_rejected_before_acceptance(self):
        record = copy.deepcopy(self.context['record'])
        record['source_statement'] += ' Unauthorized stronger statement.'
        with self.assertRaisesRegex(ValueError, 'publication binding is stale'):
            self.gate().validate_record(ROOT, record, self.inventory())

    def test_graph_repair_leaves_raw_source_and_active_root_unchanged(self):
        proposal = json.loads((BASE / 'topology-v2-repair-proposal.json').read_bytes())
        self.assertFalse(proposal['source_changed'])
        self.assertFalse(proposal['Lean_changed'])
        self.assertTrue(proposal['active_E21_tail_unchanged'])
        self.assertEqual(proposal['proposed_graph_sha256'], hashlib.sha256((BASE / 'source-topology-v2-proposal.json').read_bytes()).hexdigest())

    def test_post_reference_clarification_preserves_every_edge(self):
        clarified = json.loads((BASE / 'source-topology-v3-proposal.json').read_bytes())
        self.assertEqual(clarified['hyperedges'], self.graph['hyperedges'])
        self.assertEqual(clarified['or_structure'], self.graph['or_structure'])
        post = next(n for n in clarified['nodes'] if n['id'] == 'M12.post')
        self.assertIn('No preservation of the pre-swap low row prefix', post['claim'])
        self.assertIn('candidate C(j)', post['claim'])
        for node in clarified['nodes']:
            if node['id'] != 'M12.post':
                self.assertEqual(node, next(n for n in self.graph['nodes'] if n['id'] == node['id']))

    def test_pre_swap_low_is_not_post_low_finite_diagnostic_only(self):
        # Exact n=3,kappa=7,j=0 witness; not a uniform Lean proof.
        j, address_image = 0, 96
        row, address = (address_image >> 1) & 7, (address_image >> 4) & 7
        difference = row ^ address
        post = address_image ^ (difference << 1) ^ (difference << 4)
        candidate = (post % 16) + 4 * 16 + (post // 128) * 128
        self.assertEqual(post, 12)
        self.assertEqual(candidate, 76)
        self.assertNotEqual(j % 16, post % 16)
        self.assertEqual(candidate % 16, post % 16)


if __name__ == '__main__':
    unittest.main()
