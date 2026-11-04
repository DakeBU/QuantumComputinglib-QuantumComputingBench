"""Source/graph reconciliation regressions, independent of Lean execution."""
import copy
import unittest

from website.scripts import qcb_expert as expert

FROZEN = 'a' * 40
PUBLISHED = 'b' * 40
A = 'declaration:QuantumBlockEncoding.A.target'
B = 'declaration:QuantumBlockEncoding.A.support'
C = 'concept:normalization'
M = 'module:QuantumBlockEncoding.A'
N = 'module:QuantumBlockEncoding.B'
CORE = 'qcb-core-sp-001'
OTHER = 'qcb-core-sp-002'


def fixture():
    nodes = [
        {'id': A, 'label': 'target', 'kind': 'declaration', 'source': 'QuantumBlockEncoding/A.lean', 'line': 23,
         'inventory_status': 'Compiled', 'status': 'legacy_source_semantic_debt', 'open_obligation': False},
        {'id': B, 'label': 'support', 'kind': 'declaration', 'source': 'QuantumBlockEncoding/A.lean', 'line': 10,
         'inventory_status': 'Partial route', 'open_obligation': True},
        {'id': C, 'label': 'Normalization', 'kind': 'concept', 'source': 'website/research/atlas.json', 'status': 'planned'},
        {'id': M, 'label': 'A', 'kind': 'module', 'source': 'QuantumBlockEncoding/A.lean'},
        {'id': N, 'label': 'B', 'kind': 'module', 'source': 'QuantumBlockEncoding/B.lean'},
    ]
    graph = {n['id']: n for n in nodes}
    edges = [{'source': M, 'target': A, 'type': 'module-declares-leaf'},
             {'source': M, 'target': B, 'type': 'module-declares-leaf'},
             {'source': N, 'target': M, 'type': 'module-supports-importer'}]
    snapshot = {'snapshot_id': 'frozen-graph', 'commit': FROZEN, 'nodes': nodes,
                'edges': edges + [copy.deepcopy(edges[0])],
                'hyperedges': [{'id': 'planned-join', 'label': 'A planned combination', 'tails': [C],
                                'heads': [A, 'concept:missing'], 'status': 'proposal',
                                'failure_boundary': 'A construction bridge is still open.'}]}
    cores = []
    items = {}
    for core_id, targets, supports in [(CORE, [A], [B, C]), (OTHER, [B], [A])]:
        raw = {'core_id': core_id, 'title': 'A mathematical contract', 'contract_hash': 'c' * 64,
               'part': 'state-preparation', 'topic': 'isometry', 'family': 'one-family', 'split': 'train',
               'target_nodes': targets, 'supporting_nodes': supports, 'evidence_relation': 'local_source_supported',
               'question_source_record': 'data/public/qa.json', 'answer_source_record': 'data/authored/repair.json',
               'editorial_second_pass': 'review_accepted', 'views': {'non-lean': {'status': 'admitted'}}}
        cores.append(raw)
        items[core_id] = {k: copy.deepcopy(raw[k]) for k in ('core_id', 'split', 'target_nodes', 'supporting_nodes')}
        items[core_id]['rubric'] = [{'criterion': 'Actual explanation'}]
    catalog = {'cores': cores, 'graph_source_commit': FROZEN, 'snapshot_id': 'frozen-graph', 'catalog_hash': 'd' * 64}
    task = {'core_id': CORE, 'contract_hash': 'c' * 64, 'split': 'train', 'root_id': 'join',
            'nodes': [{'id': 'left', 'target': 'P', 'depends_on': []},
                      {'id': 'right', 'target': 'Q', 'depends_on': []},
                      {'id': 'join', 'target': 'P ∧ Q', 'depends_on': ['left', 'right']}]}
    plan = {'entries': [{'core_id': CORE, 'contract_hash': 'c' * 64, 'split': 'train', 'view_id': 'view-1',
                         'task_hash': expert._hash(task), 'source_node_ids': [B],
                         'difficulty': {'construction_band': 'D3'}}]}
    views = {'view-1': {'task': task}}
    diagnostics = {'snapshot_id': 'frozen-graph', 'probes': [
        {'probe_id': '01234567-89ab-cdef-0123-456789abcdef', 'cluster_id': 'norms', 'split': 'train',
         'parent_core_ids': [CORE], 'parent_contracts': {CORE: 'c' * 64}, 'source_nodes': [A, B]}]}
    return catalog, items, graph, {A, M, N}, PUBLISHED, snapshot, plan, views, diagnostics


def build(data=None, **overrides):
    data = data or fixture()
    c, i, g, live, revision, s, p, v, d = data
    options = {'snapshot': s, 'course_plan': p, 'course_views': v, 'diagnostics': d}
    options.update(overrides)
    return expert.build_expert_index(c, i, g, live, revision, **options)


class ExpertGraphTests(unittest.TestCase):
    def test_every_anchor_has_exact_reverse_roles_and_views_do_not_add_cores(self):
        index = build()
        self.assertEqual(index['counts'], {'shared_cores': 2, 'diagnostic_candidates': 1,
                         'supplied_course_views': 1, 'distinct_cited_anchors': 3, 'context_nodes': 2,
                         'live_anchor_identity_matches': 1, 'frozen_only_anchors': 2})
        self.assertEqual({r['role'] for r in index['reverse_index'][B]}, {'target', 'support', 'course_source', 'diagnostic_source'})
        self.assertEqual(index['new_mathematical_cores'], 0)
        self.assertFalse(index['canonical_admissions_changed'])
        self.assertEqual(index['cores'][CORE]['contract_hash'], 'c' * 64)
        self.assertEqual(index['cores'][CORE]['split'], 'train')

    def test_frozen_source_lines_are_not_attached_to_the_publication_commit(self):
        index = build()
        self.assertEqual(index['nodes'][A]['frozen_source_url'], expert.REPO + '/blob/' + FROZEN + '/QuantumBlockEncoding/A.lean#L23')
        self.assertIn('/blob/' + PUBLISHED + '/', index['cores'][CORE]['source_url'])
        panel = expert.expert_panel(CORE, index)
        self.assertIn('Frozen source:23', panel)
        self.assertIn(index['nodes'][A]['frozen_source_url'], panel)
        self.assertNotIn('/blob/main/', panel)
        self.assertIn('exact live identity does not certify source equality', panel)

    def test_missing_anchor_or_changed_roles_fail_instead_of_fuzzy_remapping(self):
        for change in ('missing', 'roles', 'snapshot'):
            data = list(fixture())
            if change == 'missing':
                data[0]['cores'][0]['target_nodes'][0] = 'declaration:QuantumBlockEncoding.A.target_typo'
                data[1][CORE]['target_nodes'][0] = data[0]['cores'][0]['target_nodes'][0]
            elif change == 'roles':
                data[1][CORE]['supporting_nodes'] = [A]
            else:
                data[5]['commit'] = PUBLISHED
            with self.subTest(change=change), self.assertRaises(ValueError):
                build(data)

    def test_live_identity_matches_are_exact_and_frozen_only_anchors_stay_inspectable(self):
        data = list(fixture())
        data[3] = {A + '_almost'}
        index = build(data)
        summary = expert.graph_summary(CORE, index)
        self.assertNotIn('data-qcb-graph=""', summary)
        self.assertIn('frozen anchor', summary)
        self.assertIn('expert/node/index.html?node=', summary)
        good = expert.graph_summary(CORE, build())
        self.assertIn('data-qcb-graph', good)
        self.assertIn('focus=declaration%3AQuantumBlockEncoding.A.target', good)

    def test_structural_edges_and_curated_gaps_remain_distinct_from_supplied_proofs(self):
        index = build()
        self.assertEqual(len(index['structural_edges']), 3)
        self.assertEqual(index['duplicate_snapshot_edge_records_collapsed'], 1)
        self.assertFalse(any(e['source'] == B and e['target'] == A for e in index['structural_edges']))
        self.assertTrue(all(e['evidence_class'].endswith('not_proof_entailment') for e in index['structural_edges']))
        self.assertEqual(index['curated_hyperedges'][0]['unmapped_endpoint_ids'], ['concept:missing'])
        course = index['supplied_courses'][CORE]
        self.assertEqual(course['nodes'][-1]['depends_on'], ['left', 'right'])
        self.assertIn('not_extracted_proof', course['evidence_class'])
        self.assertIn('All inputs: left, right', expert.expert_panel(CORE, index))

    def test_changed_course_contract_hash_or_dependency_join_cannot_reuse_the_map(self):
        for change in ('contract', 'task_hash', 'dependency', 'split'):
            data = list(fixture())
            if change == 'contract':
                data[6]['entries'][0]['contract_hash'] = '0' * 64
            elif change == 'task_hash':
                data[7]['view-1']['task']['nodes'][-1]['target'] = 'P ∨ Q'
            elif change == 'dependency':
                task = data[7]['view-1']['task']
                task['nodes'][0]['depends_on'] = ['join']
                data[6]['entries'][0]['task_hash'] = expert._hash(task)
            else:
                data[6]['entries'][0]['split'] = 'test_public'
            with self.subTest(change=change), self.assertRaises(ValueError):
                build(data)

    def test_changed_diagnostic_parent_contract_or_split_is_not_a_new_view(self):
        for change in ('parent', 'split', 'snapshot'):
            data = list(fixture())
            if change == 'parent':
                data[8]['probes'][0]['parent_contracts'][CORE] = '0' * 64
            elif change == 'split':
                data[8]['probes'][0]['split'] = 'dev'
            else:
                data[8]['snapshot_id'] = 'other-graph'
            with self.subTest(change=change), self.assertRaises(ValueError):
                build(data)

    def test_invalid_source_paths_commits_and_lines_cannot_escape_to_host_or_javascript(self):
        for path in ('/home/private/secret', '../secret', 'C:\\private\\secret', 'javascript:alert(1)', 'foo\nbar'):
            data = list(fixture())
            data[2][A]['source'] = path
            with self.subTest(path=path), self.assertRaises(ValueError):
                build(data)
        for line in (0, -1, True, '10'):
            data = list(fixture())
            data[2][A]['line'] = line
            with self.subTest(line=line), self.assertRaises(ValueError):
                build(data)
        data = list(fixture())
        data[4] = 'main'
        with self.assertRaises(ValueError):
            build(data)

    def test_unavailable_publication_context_never_assumes_a_branch(self):
        data = list(fixture())
        data[4] = None
        index = build(data)
        panel = expert.expert_panel(CORE, index)
        self.assertIn('source link unavailable', panel)
        self.assertIn('/blob/' + FROZEN + '/', panel)
        self.assertNotIn('/blob/main/', panel)

    def test_html_labels_and_ids_are_text_and_dossiers_stay_closed(self):
        data = list(fixture())
        data[2][A]['label'] = '<img src=x onerror=alert(1)>'
        index = build(data)
        panel = expert.expert_panel(CORE, index)
        self.assertIn('&lt;img src=x onerror=alert(1)&gt;', panel)
        self.assertNotIn('<img ', panel)
        self.assertNotIn(' open', panel)
        summary = expert.graph_summary(CORE, index)
        self.assertIn('&lt;img ', summary)
        self.assertNotIn('<img ', summary)

    def test_three_bounded_pages_preserve_all_reverse_links_without_a_page_per_graph_node(self):
        index = build()
        pages = {}
        def write(route, title, body, description):
            pages[route + 'index.html'] = body
        def intro(title, subtitle):
            return '<div class="qcb-reader"><h1>' + expert._e(title) + '</h1><p>' + expert._e(subtitle) + '</p>'
        manifest = expert.publish_expert(write, intro, index)
        self.assertEqual(set(pages), set(expert.ROUTES))
        self.assertEqual(manifest['index_digest'], index['index_digest'])
        node_page = pages[expert.HUB + 'expert/nodes/index.html']
        for node in index['anchor_node_ids']:
            self.assertIn('id="' + index['nodes'][node]['anchor'] + '"', node_page)
            for ref in index['reverse_index'][node]:
                self.assertIn('../../../' + ref['href'], node_page)
        viewer = pages[expert.HUB + 'expert/node/index.html']
        self.assertIn('data-qcb-expert-viewer', viewer)
        self.assertIn('Static node-to-question index', viewer)

    def test_diagnostic_sources_are_context_not_mislabeled_as_a_named_root(self):
        index = build()
        probe_id = next(iter(index['diagnostics']))
        panel = expert.diagnostic_panel(probe_id, index)
        self.assertIn('id="expert-' + probe_id + '"', panel)
        self.assertIn(index['cores'][CORE]['href'] + '#expert', panel)
        self.assertIn('separate from the named source declarations', panel)
        self.assertNotIn('Target statement', panel)
        self.assertIn('reference-checks.json', panel)
        self.assertIn('/blob/' + PUBLISHED + '/', panel)
        self.assertIn('/blob/' + FROZEN + '/', panel)
        self.assertNotIn(' open', panel)

    def test_build_is_deterministic_and_does_not_mutate_source_records(self):
        data = fixture()
        before = copy.deepcopy(data)
        first = build(data)
        self.assertEqual(data, before)
        self.assertEqual(first, build(data))
        self.assertEqual(first['index_digest'], expert._hash({k: v for k, v in first.items() if k != 'index_digest'}))
        first['cores'][CORE]['target_nodes'].clear()
        first['supplied_courses'][CORE]['nodes'][-1]['depends_on'].clear()
        first['diagnostics'][next(iter(first['diagnostics']))]['source_nodes'].clear()
        first['curated_hyperedges'][0]['tails'].clear()
        self.assertEqual(data, before)


if __name__ == '__main__':
    unittest.main()
