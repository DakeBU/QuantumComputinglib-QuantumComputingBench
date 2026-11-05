"""Sparse graph/content checks, not source-graph completeness or native admission."""
import copy
import hashlib
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
load = lambda path: json.loads(path.read_bytes())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()


class GraphV4Tests(unittest.TestCase):
    def test_same_independent_reviewer_resolves_only_bound_graph_finding(self):
        receipt = load(HERE/'parent-v4-review-transport-c30.json')
        self.assertEqual(len(receipt['files']), 3)
        for row in receipt['files']:
            self.assertEqual(sha(ROOT/row['path']), row['sha256'])
        seal = load(HERE/'reviewer-c30/phase2-v4-static-seal.json')
        self.assertEqual(seal['status'], 'BOUNDED_STATIC_GRAPH_FINDING_RESOLVED_ONLY')
        self.assertEqual(seal['finding_disposition']['status'], 'RESOLVED_FOR_EXACT_V4_GRAPH_ONLY')
        self.assertTrue(seal['independent_static_checks']['entire_graph_equal_after_only_these_three_reversions'])
        self.assertFalse(seal['finding_disposition']['extra_public_premises'])
        self.assertFalse(seal['prospective_binding_boundary']['whole_project_binding_independently_recomputed'])
        self.assertFalse(receipt['native_acceptance'])

    def test_transport_preserves_exact_sparse_and_inherited_bytes(self):
        receipt = load(HERE/'parent-v4-transport-c30.json')
        self.assertEqual(len(receipt['files']), 23)
        self.assertEqual(receipt['inherited_existing_files_not_regenerated'], 8)
        self.assertFalse(receipt['native_acceptance'])
        for row in receipt['files']:
            self.assertEqual(sha(ROOT/row['path']), row['sha256'])
            self.assertEqual((ROOT/row['path']).stat().st_size, row['bytes'])

    def test_exactly_three_complete_and_tails_change(self):
        before = load(HERE/'author-graph-views.json')
        after = load(HERE/'metadata-v4/author-graph-views.json')
        expected = copy.deepcopy(before)
        changes = {
            'construction:conditional-witness': 'result:transpose-matrix',
            'construction:swap-permutation': 'result:layout-data',
            'construction:indicator-permutation': 'result:layout-data',
        }
        seen = set()
        for edge in expected['views']['source-construction-graph']['AND_hyperedges']:
            if edge['id'] in changes:
                edge['tails'].append(changes[edge['id']])
                seen.add(edge['id'])
        self.assertEqual(seen, set(changes))
        self.assertEqual(after, expected)
        graph = after['views']['source-construction-graph']
        self.assertEqual(len(graph['AND_hyperedges']), 21)
        self.assertEqual(len(graph['open_source_gap_ids']), 10)
        self.assertTrue(all(n['status']=='OPEN' for n in graph['nodes'] if n['kind']=='SOURCE_GAP'))

    def test_candidate_binding_changes_only_prospectively(self):
        candidate = load(HERE/'metadata-v4/publication-candidate-GHL2025.json')
        self.assertEqual(candidate['binding_sha256'], '9100758d53afd5b635159fd4026ab08b090d789d7f4267350c70d509cbcf9d53')
        self.assertEqual(candidate['graph_contribution']['source_graph_sha256'], sha(HERE/'metadata-v4/author-graph-views.json'))
        self.assertFalse(candidate['independent_acceptance'])
        self.assertEqual(load(HERE/'publication-candidate-GHL2025.json')['binding_sha256'],
                         'fc897ca51a04dd6519125fec941fff8a9247d85fdf27a02b268606ff875bed0c')

    def test_export_derivatives_are_not_claimed_original_bytes(self):
        receipt = load(HERE/'metadata-v4/public-export/exact-redaction-receipt.json')
        self.assertEqual(len(receipt['derivatives']), 2)
        for row in receipt['derivatives']:
            self.assertFalse(row['raw_byte_alias'])
            self.assertNotEqual(row['original']['sha256'], row['derived']['sha256'])
            self.assertEqual(sha(HERE/'metadata-v4/public-export'/row['derived']['path']), row['derived']['sha256'])
            self.assertEqual(len(row['edits']), 1)
            self.assertEqual(row['edits'][0]['replacement_utf8'], 'REPOSITORY_ROOT')


if __name__ == '__main__':
    unittest.main()
