"""WIP integrity tests. Passing these is neither Lean nor publication admission."""
import base64
import hashlib
import json
from pathlib import Path
import re
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
load = lambda p: json.loads(p.read_bytes())
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

class CubicCheckpointTests(unittest.TestCase):
    def test_frozen_author_manifest(self):
        self.assertEqual(digest(HERE/'outputs-manifest.json'), '555194f534a537e7d68c450caa8605a3d4a2a37dc02d5ac39f97422b28d0fd0c')
        for row in load(HERE/'outputs-manifest.json')['artifacts']:
            file = ROOT/row['planned_canonical_path']
            self.assertEqual(digest(file), row['sha256'], row['path'])
            self.assertEqual(file.stat().st_size, row['bytes'])

    def test_raw_transport_receipts(self):
        for name, count in [('parent-author-transport-c29.json', 20), ('parent-decoder-initial-transport-c29.json', 16)]:
            receipt = load(HERE/name)
            self.assertFalse(receipt['native_acceptance'])
            self.assertFalse(receipt['main_admission'])
            self.assertFalse(receipt['scientific_ROOT'])
            self.assertEqual(len(receipt['files']), count)
            for row in receipt['files']:
                file = ROOT/row['path']
                self.assertEqual(digest(file), row['sha256'])
                self.assertEqual(file.stat().st_size, row['bytes'])

    def test_retained_partial_is_not_valid_context(self):
        receipt = load(HERE/'parent-author-transport-c29.json')
        partial = receipt['historical_invalid_partial']
        self.assertFalse(partial['valid_formal_input'])
        with self.assertRaises(json.JSONDecodeError):
            load(ROOT/partial['path'])
        context = load(HERE/'author-formal-context.json')
        self.assertEqual(len(context['inventory']), 319)

    def test_inventory_includes_private_structures_and_opaque(self):
        roots = load(HERE/'author-formal-context.json')['inventory']
        self.assertEqual(len({r['name'] for r in roots}), 319)
        self.assertEqual(sum(r['private'] for r in roots), 50)
        self.assertEqual(sum(not r['private'] for r in roots), 269)
        self.assertEqual(sum(r['kind']=='structure' for r in roots), 11)
        self.assertEqual(sum(r['kind']=='opaque' for r in roots), 7)

    def test_formal_raw_source_not_transformed_copy(self):
        context = load(HERE/'author-formal-context.json')
        for row in context['target_files'] + context['dependency_context']:
            raw = base64.b64decode(''.join(row['full_source_utf8_base64_chunks']))
            self.assertEqual(raw, ''.join(row['full_source_lines']).encode())
            self.assertEqual(raw, (ROOT/row['path']).read_bytes())
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])

    def test_lossless_source_coverage_and_complete_name_mapping(self):
        coverage = load(HERE/'author-source-coverage.json')
        source = (HERE/'source-only.md').read_bytes()
        self.assertEqual(''.join(p['exact_text'] for p in coverage['source_paragraphs']).encode(), source)
        inventory = load(HERE/'author-formal-context.json')['inventory']
        self.assertEqual({r['name'] for r in coverage['whole_module_inventory']}, {r['name'] for r in inventory})
        for row in coverage['whole_module_inventory']:
            self.assertTrue(row['source_paragraphs'])
        for paragraph in coverage['source_paragraphs']:
            self.assertIn(paragraph['disposition'], ('NODE', 'EXCLUDED'))
            if paragraph['source_region']=='S13':
                self.assertFalse(paragraph['counts_as_scientific_closure'])

    def test_complete_and_edges_and_open_boundaries(self):
        views = load(HERE/'author-graph-views.json')['views']
        graph = views['source-construction-graph']
        ids = {n['id'] for n in graph['nodes']}
        self.assertEqual(len(graph['AND_hyperedges']), 26)
        self.assertEqual(len(graph['open_source_gap_ids']), 10)
        for edge in graph['AND_hyperedges'] + views['functor-hypergraph']['hyperedges']:
            self.assertEqual(edge['logic'], 'AND')
            self.assertTrue(set(edge['tails'] + edge['heads']) <= ids)
        self.assertEqual(len(views['lean-graph']['ownership_edges']), 319)

    def test_initial_decoder_is_zero_call_environment_evidence(self):
        packet = load(HERE/'decoder-c29/packet.json')
        self.assertEqual(packet['leanInvocationCount'], 0)
        self.assertFalse(packet['nativeAccepted'])
        self.assertFalse(packet['cleanTransitive'])
        self.assertIsNone(packet['sourceAgreement'])
        self.assertIsNone(packet['publicationBinding'])
        self.assertEqual(packet['compile'], 'NOT_RUN_ENV_BLOCKED')
        self.assertFalse(packet['importClosure']['compilerBackedImportInventory'])

    def test_publication_candidate_stays_wip(self):
        candidate = load(HERE/'publication-candidate-CubicStatePreparation.json')
        self.assertEqual(candidate['status'], 'AUTHOR_WIP_NOT_ADMITTED')
        self.assertFalse(candidate['independent_acceptance'])
        self.assertFalse(candidate['main_admission'])
        self.assertEqual(candidate['binding_sha256'], '5c23037871778ce883584e8aed865321c69ace57eff995915104a600253ff2bc')
        self.assertEqual(len(candidate['declarations']), 269)

    def test_v2_transport_preserves_formal_input_and_original_manifest(self):
        v2 = HERE/'metadata-v2'
        self.assertEqual(digest(v2/'outputs-manifest.json'), '5e00c0cb2e0bb2faa74fdf9ae0d609db4fa67da1e1a479439fa2bd4f238de44d')
        self.assertEqual((v2/'author-formal-context.json').read_bytes(), (HERE/'author-formal-context.json').read_bytes())
        receipt = load(HERE/'parent-v2-transport-c29.json')
        self.assertFalse(receipt['native_acceptance'])
        self.assertEqual(len(receipt['files']), 20)
        for row in receipt['files']:
            self.assertEqual(digest(ROOT/row['path']), row['sha256'])
        self.assertEqual(digest(HERE/'outputs-manifest.json'), '555194f534a537e7d68c450caa8605a3d4a2a37dc02d5ac39f97422b28d0fd0c')

    def test_v2_prop_field_and_construction_case_boundaries(self):
        v2 = HERE/'metadata-v2'
        bundles = load(v2/'author-binder-definition-audit.json')['project_owned_bundle_expansions']
        witness = next(b for b in bundles.values() if b['name'].endswith('.ExpandedControlledRyWorkspaceReadonlyWitness'))
        angle = next(f for f in witness['field_audit'] if f['name']=='angleConvention')
        self.assertEqual(angle['classification'], 'SOURCE')
        self.assertEqual(len(angle['nested_logical_expansion']), 3)
        for bundle in bundles.values():
            for field in bundle['field_audit']:
                self.assertIsNone(re.search(r'(?m)^(?:namespace|end|deriving)\b', field['exact_source_field_region']))
        graph = load(v2/'author-graph-views.json')['views']['source-construction-graph']
        self.assertNotIn('guarded_OR_cases', graph)
        self.assertEqual(len(graph['typed_guarded_partitions']), 8)
        self.assertEqual(len(graph['construction_alternatives']), 2)
        routes = [e for e in graph['AND_hyperedges'] if e['id'].startswith('route:rank-one-')]
        self.assertEqual(len(routes), 2)
        for route in routes:
            self.assertEqual(route['heads'], ['target:rank-one-physical'])
            self.assertEqual(sum(t.startswith('OPEN:') for t in route['tails']), 6)
            self.assertEqual(route['status'], 'OPEN_PROPOSED_SUFFICIENT_CONSTRUCTION_NOT_A_PROOF')

    def test_independent_v2_static_resolution_is_not_native_acceptance(self):
        reviewer = HERE/'reviewer-c29'
        allow = load(reviewer/'phase2-v2-public-allowlist.json')
        self.assertEqual(digest(reviewer/'phase2-v2-public-allowlist.json'), 'bb659badd04efa71d38c550c450b88a15c08d0e51a0d8f3bf08d07a2b6aa5dbc')
        self.assertEqual(allow['new_static_result'], 'STATIC_METADATA_REFINEMENTS_RESOLVED')
        self.assertFalse(allow['native_accepted'])
        self.assertFalse(allow['Lean_pass_claim'])
        self.assertFalse(allow['main_admission'])
        for row in allow['allowed_artifacts']:
            file = reviewer/row['path'].removeprefix('$REVIEWER/')
            self.assertEqual(digest(file), row['sha256'])
            self.assertEqual(file.stat().st_size, row['bytes'])

    def test_later_transport_is_exact_and_not_acceptance(self):
        receipt = load(HERE/'parent-later-transport-c29.json')
        self.assertFalse(receipt['native_acceptance'])
        self.assertFalse(receipt['Lean_success'])
        self.assertEqual(len(receipt['reviewer_files']), 5)
        self.assertEqual(len(receipt['resume1_files']), 6)
        for row in receipt['reviewer_files'] + receipt['resume1_files']:
            self.assertEqual(digest(ROOT/row['path']), row['sha256'])
            self.assertEqual((ROOT/row['path']).stat().st_size, row['bytes'])
        seal = load(HERE/'reviewer-c29/phase2-static-seal.json')
        self.assertEqual(seal['phase'], 2)
        self.assertEqual(seal['mode'], 'STATIC_ONLY')
        self.assertIn('REFINEMENTS_REQUIRED', seal['state'])
        report = (HERE/'reviewer-c29/phase2-static-report.md').read_text(encoding='utf-8')
        for finding in ('F1', 'F2', 'F3', 'F4', 'F5'):
            self.assertIn(finding, report)

    def test_resume1_zero_lean_and_sanitized_phase1_not_raw_aliases(self):
        summary = load(HERE/'decoder-c29/resume1/summary.json')
        self.assertEqual(summary['leanInvocations'], 0)
        self.assertEqual(summary['failureClass'], 'ENV_BLOCKED')
        self.assertLess(summary['actualStartVirtualKiB'], summary['minimumVirtualKiB'])
        allow = load(HERE/'reviewer-c29/public-sanitized-allowlist.json')
        self.assertEqual(len(allow['original_phase1_bindings_retained']), 2)
        for original in allow['original_phase1_bindings_retained']:
            self.assertFalse(original['raw_public_export_allowed'])
        self.assertEqual(digest(HERE/'reviewer-c29/sanitized-phase1-seal.json'), '54a5ed5be1ffed9adb8459fc4dd0d059c76ab290e240bc0cebc05c16ba935474')

    def test_exported_frozen_files_have_no_private_machine_path(self):
        pattern = re.compile(r'(?i)(?<![A-Za-z0-9])[a-z]:[\\/]|' + 'file:' + '///|/' + 'Users/|/' + 'home/')
        for receipt in ['parent-author-transport-c29.json', 'parent-decoder-initial-transport-c29.json']:
            for row in load(HERE/receipt)['files']:
                self.assertIsNone(pattern.search((ROOT/row['path']).read_text(encoding='utf-8')), row['path'])

if __name__ == '__main__':
    unittest.main()
