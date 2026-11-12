"""Mechanical WIP integrity only; not Lean, source equivalence or admission."""
import base64
import hashlib
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
load = lambda p: json.loads(p.read_bytes())
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

class GHLCheckpointTests(unittest.TestCase):
    def test_exact_manifest_and_transport(self):
        self.assertEqual(digest(HERE/'outputs-manifest.json'), 'e2b4f1bbfd09ece530434802cfe54913add3c5cc4364718366df9b67b588cfbb')
        receipt = load(HERE/'parent-author-transport-c30.json')
        self.assertEqual(len(receipt['files']), 18)
        self.assertFalse(receipt['native_acceptance'])
        for row in receipt['files']:
            self.assertEqual(digest(ROOT/row['path']), row['sha256'])
            self.assertEqual((ROOT/row['path']).stat().st_size, row['bytes'])

    def test_original_and_supplemented_source_are_distinct(self):
        original = (HERE/'original-source/source-only.md').read_bytes()
        supplement = (HERE/'source-clarification-v2.md').read_bytes()
        lesson = (ROOT/'docs/lessons/ghl-global-slot-clean-domain-and-transpose-boundary.md').read_bytes()
        self.assertEqual(lesson, original + b'\n' + supplement)
        self.assertEqual(hashlib.sha256(original).hexdigest(), 'c774ecaf66c3d3c9586c41f7441b416ee77bfd54a3314e1d9ee66ff7151db6f5')
        self.assertEqual(hashlib.sha256(supplement).hexdigest(), '4f5bbe1ae34abad5a7c3ffeb46c2d876ccc325e802a974f954efb821ca3cf9eb')
        self.assertIn('not the arbitrary-parameter interval', supplement.decode())

    def test_whole_inventory_is_source_not_compiler_count(self):
        context = load(HERE/'author-formal-context.json')
        roots = context['inventory']
        self.assertEqual(len(roots), 405)
        self.assertEqual(sum(r['private'] for r in roots), 2)
        self.assertEqual(sum(r['kind']=='structure' for r in roots), 38)
        self.assertEqual(len(context['whole_ambient_binding_inputs']), 202)
        for row in context['target_files'] + context['provider_index'] + context['dependency_context']:
            raw = base64.b64decode(''.join(row['full_source_utf8_base64_chunks']))
            self.assertEqual(raw, ''.join(row['full_source_lines']).encode())
            self.assertEqual(raw, (ROOT/row['path']).read_bytes())
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])

    def test_lossless_paragraph_coverage(self):
        coverage = load(HERE/'author-source-coverage.json')
        lesson = (ROOT/'docs/lessons/ghl-global-slot-clean-domain-and-transpose-boundary.md').read_bytes()
        self.assertEqual(len(coverage['source_paragraphs']), 82)
        self.assertEqual(''.join(p['exact_text'] for p in coverage['source_paragraphs']).encode(), lesson)
        self.assertEqual({r['name'] for r in coverage['whole_module_inventory']}, {r['name'] for r in load(HERE/'author-formal-context.json')['inventory']})

    def test_graph_preserves_full_and_open_gaps_and_case_types(self):
        graph = load(HERE/'author-graph-views.json')['views']['source-construction-graph']
        ids = {n['id'] for n in graph['nodes']}
        self.assertEqual(len(graph['AND_hyperedges']), 21)
        self.assertEqual(len(graph['case_splits']), 6)
        self.assertEqual(graph['construction_OR_routes'], [])
        for edge in graph['AND_hyperedges']:
            self.assertEqual(edge['logic'], 'AND')
            self.assertTrue(set(edge['tails'] + edge['heads']) <= ids)
        for node in graph['nodes']:
            if node['kind']=='SOURCE_GAP':
                self.assertEqual(node['status'], 'OPEN')

    def test_candidate_does_not_self_admit(self):
        record = load(HERE/'publication-candidate-GHL2025.json')
        self.assertEqual(record['status'], 'AUTHOR_WIP_NOT_ADMITTED')
        self.assertFalse(record['independent_acceptance'])
        self.assertFalse(record['main_admission'])
        self.assertEqual(record['binding_sha256'], 'fc897ca51a04dd6519125fec941fff8a9247d85fdf27a02b268606ff875bed0c')

if __name__ == '__main__':
    unittest.main()
