"""Mechanical migration fixtures; none is mathematical approval or catalog admission."""
from copy import deepcopy
from html.parser import HTMLParser
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from uuid import uuid4

B = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(B / 'src'), str(B / 'scripts'), str(B.parents[1])]
import release
import qcb_textbook_policy as policy
import qcb_curriculum as curriculum
import qcb_formal_views as formal
from qcb_core import digest, read_json, write_json, model_input, score, content_hash
from website.scripts import quantumcomputingbench as reader


class PremisesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.role, self.in_li, self.text, self.lists = None, False, '', {}
        self.math_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.math_depth:
            self.math_depth += 1
        elif self.in_li and 'data-qcb-math-source' in attrs:
            self.text += attrs['data-qcb-math-source']
            self.math_depth = 1
        if tag == 'ul':
            self.role = next((key for key in attrs if key.startswith('data-qcb-')), None)
            if self.role:
                self.lists[self.role] = []
        if tag == 'li' and self.role:
            self.in_li, self.text = True, ''

    def handle_data(self, data):
        if self.in_li and not self.math_depth:
            self.text += data

    def handle_endtag(self, tag):
        if self.math_depth:
            self.math_depth -= 1
            return
        if tag == 'li' and self.in_li:
            self.lists[self.role].append(self.text)
            self.in_li = False
        if tag == 'ul':
            self.role = None


class AssumptionSuccessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = next(i for i in release.checked()[2] if i['core_id'] == 'qcb-core-plan-208')
        cls.catalog, _, cls.graph = curriculum.load_catalog()

    def fixture(self):
        old = deepcopy(self.original)
        withdrawal = next(r for r in read_json(B / 'shared/current-policy.json')['withdrawals']
                          if r['core_id'] == old['core_id'])
        row = {'core_id': old['core_id'], 'predecessor_key': old['key'],
               'predecessor_item_digest': digest(old), 'prior_withdrawal': withdrawal,
               'repair': 'shared/repairs/fixture-assumptions.json',
               'review': 'reports/textbook-v1/fixture-assumptions-review.json'}
        # Deliberately equal prefixes: exact lists, never substring bans, decide active premises.
        assumptions = [old['assumptions'][0] + ' [CURRENT MECHANICAL FIXTURE ONLY]', old['assumptions'][1]]
        source = read_json(B / withdrawal['review'])['items'][0]['source_checks']
        candidate = {'schema_version': 'qcb.textbook_question_successor.v3', 'core_id': old['core_id'],
            'supersedes_key': old['key'], 'supersedes_item_digest': digest(old),
            'supersedes_contract_hash': digest(curriculum.core_contract(old)),
            'author': 'mechanical-fixture-author-not-math-approval',
            'key': old['core_id'] + '-textbook-question-v2-mechanical-fixture', 'question_version': 2,
            'admission': 'pending_distinct_review', 'change_scope': 'Unit fixture, never admitted.',
            'question': 'Mechanical current question: ' + assumptions[0], 'assumptions': assumptions,
            'reference_answer': 'Mechanical answer marker, not a mathematical claim.',
            'rubric': [{'id': 'fixture', 'weight': 1, 'criterion': 'Mechanical current criterion only.'}],
            'exposition': {'core_summary': 'Mechanical current summary.',
                          'semantic_steps': deepcopy(old['semantic_steps'])},
            'source_checks': source, 'execution': {'status': 'test_fixture_only'}}
        candidate['exposition']['semantic_steps'][0]['claim'] = 'Mechanical current semantic step.'
        review = {'method': 'independent-assumption-successor-review',
            'reviewer': 'mechanical-fixture-reviewer-not-math-approval', 'core_id': old['core_id'],
            'original_item_digest': digest(old), 'original_contract_hash': digest(curriculum.core_contract(old)),
            'question_version': 2, 'verdict': 'accept',
            'changed_contract_fields': ['question', 'assumptions'],
            'original_assumptions': deepcopy(old['assumptions']), 'current_assumptions': assumptions,
            'substantive_reconstruction': {'fixture': 'Structure only, not genuine mathematics review.'},
            'contract_change_assessment': {'fixture': 'Two explicit fields only.'},
            'assumption_change_assessment': {'fixture': 'Replaced first literal, retained second literal.'},
            'semantic_slot_assessment': {k: 'Mechanical fixture only; not a truth certificate.'
                                         for k in policy.ASSUMPTION_REVIEW_SLOTS},
            'assumption_edit_map': [
                {'disposition': action, 'old_index': n, 'new_index': n,
                 'old_assumption': old['assumptions'][n], 'new_assumption': assumptions[n],
                 'reason': 'Exact fixture edit, not semantic approval.'}
                for n, action in enumerate(('replaced', 'retained'))], 'source_checks': source}
        self.rebind(old, candidate, review)
        return row, old, candidate, review

    @staticmethod
    def rebind(old, candidate, review):
        review['repair_record_digest'] = digest(candidate)
        review['successor_contract_hash'] = digest({**curriculum.core_contract(old),
            'question': candidate['question'], 'assumptions': candidate.get('assumptions')})

    def execute(self, row, old, candidate, review):
        rp, vp = B / row['repair'], B / row['review']
        actual_file = Path.is_file
        with patch.object(policy, 'read_json', side_effect=lambda path:
                candidate if Path(path) == rp else review if Path(path) == vp else read_json(path)), \
                patch.object(Path, 'is_file', lambda path: path == vp or actual_file(path)):
            return policy.question_successor(row, old)

    def test_exact_current_contract_and_derived_hashes_no_old_receipt_transfer(self):
        row, old, candidate, review = self.fixture()
        old['verification_receipts'] = [{'status': 'old-receipt-fixture'}]
        row['predecessor_item_digest'] = candidate['supersedes_item_digest'] = digest(old)
        # Bypass only the historical withdrawal binder for this receipt injection fixture.
        review['original_item_digest'] = digest(old)
        self.rebind(old, candidate, review)
        with patch.object(policy, 'check_withdrawal'):
            current, _ = self.execute(row, old, candidate, review)
        self.assertEqual(current['assumptions'], candidate['assumptions'])
        self.assertEqual(current['context_hash'], digest({k: current[k] for k in
            ('assumptions', 'conventions', 'formal_context')}))
        self.assertEqual(current['task_hash'], digest({'question': current['question'], 'context': current['context_hash']}))
        self.assertNotEqual(current['task_hash'], old['task_hash'])
        self.assertNotEqual(current['context_hash'], old['context_hash'])
        self.assertNotIn('authored_hash', current)
        self.assertEqual(current['verification_receipts'], [])
        self.assertEqual(current['inherited_predecessor_verification_receipts'], old['verification_receipts'])
        self.assertEqual(current['reviews'], [review])
        self.assertEqual(current['question_successor']['current_contract_hash'], digest(curriculum.core_contract(current)))
        for k in set(policy.CONTRACT_FIELDS) - {'question', 'assumptions'}:
            self.assertEqual(current[k], old[k])

    def test_actual_prompt_download_reader_search_grading_and_formal_consumers(self):
        row, old, candidate, review = self.fixture()
        current, _ = self.execute(row, old, candidate, review)
        core = {**next(c for c in self.catalog['withheld_cores'] if c['core_id'] == old['core_id']),
                'part': next(p['id'] for p in self.catalog['parts'] if old['topic'] in p['topics']),
                'title': current['native_nl']['core_summary'], 'question_version': 2,
                'question_successor': current['question_successor'], 'item_digest': digest(current),
                'contract_hash': digest(curriculum.core_contract(current)), 'views': {},
                'semantic_steps': current['semantic_step_count'], 'evidence_relation': current['evidence_relation']}
        prompt = model_input(current)
        self.assertEqual(prompt['assumptions'], candidate['assumptions'])
        self.assertEqual(prompt['task_hash'], current['task_hash'])
        self.assertNotIn('reference_answer', prompt)
        exported = policy.public_reader_item(current)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'reader-items.json'
            write_json(path, {'items': [exported]})
            downloaded = read_json(path)['items'][0]
        self.assertEqual(downloaded['assumptions'], candidate['assumptions'])
        self.assertEqual(downloaded['context_hash'], current['context_hash'])
        self.assertEqual(downloaded['semantic_steps'], candidate['exposition']['semantic_steps'])
        self.assertEqual(downloaded['rubric'], candidate['rubric'])
        parser = PremisesParser()
        body = reader.core_body(core, current, self.catalog, self.graph, set(self.graph), '../../../')
        parser.feed(body)
        self.assertEqual(parser.lists['data-qcb-active-assumptions'], candidate['assumptions'])
        self.assertEqual(parser.lists['data-qcb-original_assumptions'], old['assumptions'])
        self.assertEqual(parser.lists['data-qcb-current_assumptions'], candidate['assumptions'])
        self.assertLess(body.index('id="assumptions"'), body.index('id="question"'))
        self.assertIn('<details class="qcb-disclosure" id="revision">', body)
        cards = reader.exercise_cards([core], '../../../', {current['core_id']: current})
        self.assertIn(reader.esc(candidate['question']), cards)
        self.assertNotIn(reader.esc(old['question']), cards)
        prediction = {'id': current['id'], 'answer': 'fixture prediction'}
        rating = {'id': current['id'], 'prediction_hash': digest(prediction['answer']),
                  'item_hash': content_hash(old), 'reviewer': 'fixture', 'kind': 'human_rubric',
                  'criteria': {'fixture': 1}, 'semantic_fidelity': 'faithful'}
        with self.assertRaisesRegex(ValueError, 'unbound'):
            score([current], [prediction], [rating])
        proposal = {'proposal_id': str(uuid4()), 'track': 'lean', 'author': 'fixture',
            'source_nodes': core['target_nodes'], **{k: core[k] for k in
                ('core_id', 'contract_hash', 'family', 'split', 'snapshot_id')}}
        catalog = {'cores': [core], 'withheld_cores': []}
        curriculum.validate_proposals(catalog, [proposal])
        proposal['contract_hash'] = current['question_successor']['predecessor_contract_hash']
        with self.assertRaises(ValueError):
            curriculum.validate_proposals(catalog, [proposal])
        batch = deepcopy(read_json(formal.CANDIDATE))
        view = batch['views'][0]
        batch['views'] = [view]
        view.update(core_id=core['core_id'], **{k: core[k] for k in ('family', 'split', 'snapshot_id')})
        view['contract_hash'] = proposal['contract_hash']
        view['item_digest'] = digest(old)
        with patch.object(formal, 'read_json', return_value=batch), self.assertRaisesRegex(ValueError, 'contract'):
            formal.candidates([core])

    def test_cross_schema_fields_and_malformed_lists_fail_even_rebound(self):
        for field, value in (('schema_version', 'qcb.textbook_question_successor.v2'),
                ('schema_version', 'qcb.textbook_question_successor.v1'), ('assumptions', None),
                ('assumptions', []), ('assumptions', [' ']), ('assumptions', [True]),
                ('assumptions', ['a', 'a']), ('assumptions', ['a', ' a ']),
                ('question_version', 2.0), ('question_version', 3), ('change_scope', True),
                ('change_scope', ' '), ('conventions', ['new']),
                ('family', 'new'), ('split', 'new'), ('source_refs', []), ('target_nodes', [])):
            with self.subTest(field=field, value=value):
                row, old, candidate, review = self.fixture()
                candidate[field] = value
                self.rebind(old, candidate, review)
                with self.assertRaises(ValueError):
                    self.execute(row, old, candidate, review)
        row, old, candidate, review = self.fixture()
        candidate['assumptions'] = old['assumptions']
        self.rebind(old, candidate, review)
        with self.assertRaises(ValueError):
            self.execute(row, old, candidate, review)

    def test_actual_publisher_download_and_search_use_resolved_premises(self):
        """Exercise the question publisher; independent site/ecosystem projections are stubbed."""
        from website.scripts import build_site, research_atlas
        row, old, candidate, review = self.fixture()
        current, _ = self.execute(row, old, candidate, review)
        core = {**next(c for c in self.catalog['withheld_cores'] if c['core_id'] == old['core_id']),
            'part': next(p['id'] for p in self.catalog['parts'] if old['topic'] in p['topics']),
            'title': current['native_nl']['core_summary'], 'question_version': 2,
            'question_successor': current['question_successor'], 'item_digest': digest(current),
            'contract_hash': digest(curriculum.core_contract(current)), 'views': {},
            'semantic_steps': current['semantic_step_count'], 'evidence_relation': current['evidence_relation']}
        catalog = {**deepcopy(self.catalog), 'cores': [core], 'withheld_cores': [], 'reader_decisions': []}
        catalog['catalog_hash'] = digest({k: v for k, v in catalog.items() if k != 'catalog_hash'})
        commit = '1' * 40
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'static').mkdir()
            (root / 'index.html').write_text('<head></head><main id="main-content"></main>', encoding='utf-8')
            write_json(root / 'data/lean-graph.json', {'nodes': list(self.graph.values())})
            write_json(root / 'build-report.json', {'coverage': {}, 'leanGate': {'passed': True, 'commit': commit}})
            write_json(root / 'site-metadata.json', {})
            write_json(root / 'search-index.json', {'entries': []})
            with patch.object(reader, 'load_catalog', return_value=(catalog, {current['core_id']: current}, self.graph)), \
                    patch.object(reader, 'math_notation_contract', return_value={'unit_fixture': True}), \
                    patch('website.scripts.qcb_expert.build_expert_index', return_value=None), \
                    patch('website.scripts.qcb_expert.publish_expert', return_value={'unit_fixture': True, 'routes': []}), \
                    patch.object(reader, 'stable_readiness', return_value={'stable': False, 'fixture_only': True}), \
                    patch.object(reader, 'formal_warmups', return_value=[]), \
                    patch.object(build_site, 'git_context', return_value={'commit': commit}), \
                    patch.object(build_site, 'page_template', side_effect=lambda **kwargs: kwargs['body']), \
                    patch.object(research_atlas, 'patch_navigation'):
                reader.publish(root)
            download = read_json(root / 'data/quantumcomputingbench/reader-items.json')
            self.assertFalse(download['stable'])
            self.assertEqual(download['items'][0], policy.public_reader_item(current))
            self.assertEqual(download['items'][0]['assumptions'], candidate['assumptions'])
            self.assertEqual(download['items'][0]['task_hash'], current['task_hash'])
            search = read_json(root / 'search-index.json')['entries']
            entry = next(e for e in search if '/cores/' in e['url'])
            self.assertEqual(entry['summary'], candidate['question'])
            self.assertNotEqual(entry['summary'], old['question'])
            parser = PremisesParser()
            parser.feed((root / entry['url']).read_text(encoding='utf-8'))
            self.assertEqual(parser.lists['data-qcb-active-assumptions'], candidate['assumptions'])
            self.assertEqual(parser.lists['data-qcb-original_assumptions'], old['assumptions'])

    def test_assumption_revision_requires_its_exact_browser_gate(self):
        catalog = deepcopy(self.catalog)
        core = next(c for c in catalog['cores'] if c.get('question_successor'))
        core['question_successor']['changed_contract_fields'] = ['question', 'assumptions']
        browser = {'catalog_hash': catalog['catalog_hash'], 'reader_source_digest': curriculum.reader_source_digest(),
            'all_core_mobile_checks': len(catalog['cores']), 'failures': [],
            'checks': {k: True for k in ('mobile_no_overflow', 'desktop_no_overflow', 'themes',
                'solution_disclosure', 'graph_links', 'search_excludes_answers', 'native_formal_panels',
                'quarantined_content_excluded', 'question_revision_lineage', 'convention_revision_lineage')}}
        actual = Path.is_file
        with patch.object(curriculum, 'read_json', side_effect=lambda path:
                browser if Path(path).name == 'browser-report.json' else read_json(path)), \
                patch.object(Path, 'is_file', lambda path: path.name == 'browser-report.json' or actual(path)):
            self.assertFalse(curriculum.stable_readiness(catalog)['gates']['rendered_browser_checks'])
            browser['checks']['assumption_revision_lineage'] = True
            self.assertTrue(curriculum.stable_readiness(catalog)['gates']['rendered_browser_checks'])
            browser['reader_source_digest'] = 'older renderer'
            self.assertFalse(curriculum.stable_readiness(catalog)['gates']['rendered_browser_checks'])

    def test_exact_distinct_review_required_and_no_obstruction_or_design_approval(self):
        for field, value in (('method', 'independent-question-convention-successor-review'),
                ('method', 'independent-assumption-migration-design-review'),
                ('method', 'independent-question-successor-review'), ('repair_record_digest', 'stale'),
                ('original_contract_hash', 'stale'), ('successor_contract_hash', 'stale'),
                ('original_assumptions', []), ('current_assumptions', ['stale']),
                ('changed_contract_fields', ['question']), ('assumption_change_assessment', {}),
                ('semantic_slot_assessment', {}), ('question_version', 2.0),
                ('original_conventions', []), ('convention_change_assessment', {'stale': 'V2 review'}),
                ('reviewer', 'mechanical-fixture-author-not-math-approval')):
            row, old, candidate, review = self.fixture()
            review[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.execute(row, old, candidate, review)
        row, old, candidate, review = self.fixture()
        candidate['rubric'][0]['criterion'] = 'Changed after review'
        with self.assertRaises(ValueError):
            self.execute(row, old, candidate, review)
        row, old, candidate, review = self.fixture()
        review['verdict'] = 'uncertain'
        self.assertIsNone(self.execute(row, old, candidate, review)[0])
        vp = B / row['review']
        actual = Path.is_file
        with patch.object(Path, 'is_file', lambda path: False if path == vp else actual(path)):
            # execute() patches file existence; call directly with candidate-only dispatch instead.
            with patch.object(policy, 'read_json', side_effect=lambda path:
                    candidate if Path(path) == B / row['repair'] else read_json(path)):
                self.assertIsNone(policy.question_successor(row, old)[0])

    def test_edit_map_coverage_literals_dispositions_and_retained_precision_fail_closed(self):
        for mutation in ('omit', 'duplicate', 'literal', 'index-bool', 'retain-changed', 'precision', 'extra'):
            row, old, candidate, review = self.fixture()
            if mutation == 'omit':
                review['assumption_edit_map'].pop()
            elif mutation == 'duplicate':
                review['assumption_edit_map'].append(deepcopy(review['assumption_edit_map'][0]))
            elif mutation == 'literal':
                review['assumption_edit_map'][0]['old_assumption'] += ' wrong'
            elif mutation == 'index-bool':
                review['assumption_edit_map'][0]['old_index'] = False
            elif mutation == 'retain-changed':
                review['assumption_edit_map'][0]['disposition'] = 'retained'
            elif mutation == 'precision':
                candidate['assumptions'][1] += ' altered'
                review['assumption_edit_map'][1].update(disposition='replaced', new_assumption=candidate['assumptions'][1])
                self.rebind(old, candidate, review)
            else:
                review['assumption_edit_map'][0]['unbounded_override'] = True
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.execute(row, old, candidate, review)

    def test_complete_exposition_and_original_ordered_node_assignments_required(self):
        for mutation in ('empty', 'missing-summary', 'missing-steps', 'empty-summary', 'reassign-nodes', 'blank-claim'):
            row, old, candidate, review = self.fixture()
            exposition = candidate['exposition']
            if mutation == 'empty':
                candidate['exposition'] = {}
            elif mutation == 'missing-summary':
                del exposition['core_summary']
            elif mutation == 'missing-steps':
                del exposition['semantic_steps']
            elif mutation == 'empty-summary':
                exposition['core_summary'] = ' '
            elif mutation == 'blank-claim':
                exposition['semantic_steps'][0]['claim'] = ' '
            else:
                exposition['semantic_steps'][0]['supporting_nodes'], exposition['semantic_steps'][1]['supporting_nodes'] = (
                    exposition['semantic_steps'][1]['supporting_nodes'], exposition['semantic_steps'][0]['supporting_nodes'])
            self.rebind(old, candidate, review)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.execute(row, old, candidate, review)

    def test_no_second_successor_or_duplicate_frozen_predecessor_decision(self):
        row, old, candidate, review = self.fixture()
        current, _ = self.execute(row, old, candidate, review)
        with self.assertRaisesRegex(ValueError, 'first'):
            policy.question_successor(row, current)
        current_policy = deepcopy(read_json(B / 'shared/current-policy.json'))
        current_policy['question_successors'].append(deepcopy(current_policy['question_successors'][0]))
        with patch.object(policy, 'read_json', side_effect=lambda path:
                current_policy if Path(path) == B / 'shared/current-policy.json' else read_json(path)), \
                self.assertRaisesRegex(ValueError, 'conflicting'):
            policy.apply_current_reader_policy(release.checked()[2])


if __name__ == '__main__':
    unittest.main()
