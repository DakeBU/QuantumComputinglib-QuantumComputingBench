"""The Lean route reuses qualified targets without multiplying task identity."""
from copy import deepcopy
from html.parser import HTMLParser
from pathlib import PurePosixPath
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from website.scripts import quantumcomputingbench as reader
from website.scripts.qcb_lean_reader import publish_lean_route
from website.scripts import qcb_lean_downloads as downloads


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.cards, self.details = [], [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if 'data-qcb-course-core' in attrs:
            self.cards.append(attrs['data-qcb-course-core'])
        if tag == 'details':
            self.details.append(attrs)


class LeanReaderTests(unittest.TestCase):
    def render(self, plan, catalog):
        pages = {}
        report = publish_lean_route(lambda route, title, body, deck: pages.update({route: body}),
            lambda title, deck: '<div class="qcb-reader"><h1>' + title + '</h1><p>' + deck + '</p>',
            catalog, plan, reader.course_label, '<p>Existing native cards</p>', '<p>Existing subject links</p>')
        return pages, report

    def test_real_course_has_one_identity_and_two_views_at_every_stage(self):
        catalog, _, _ = reader.load_catalog()
        plan, _, _ = reader.course_reader()
        before = deepcopy((catalog, plan))
        pages, report = self.render(plan, catalog)
        expected = {entry['core_id'] for entry in plan['entries']}
        self.assertEqual(report['distinct_shared_cores'], len(expected))
        self.assertEqual(report['new_mathematical_cores'], 0)
        self.assertEqual(set(report['routes']), {route + 'index.html' for route in pages})
        all_cards = set()
        for route, body in pages.items():
            parsed = Links(body)
            self.assertEqual(len(parsed.cards), len(set(parsed.cards)))
            all_cards.update(parsed.cards)
            for core in parsed.cards:
                math = [link for link in parsed.links if '/' + core + '/index.html#question' in link]
                formal = [link for link in parsed.links if '/' + core + '/index.html#course' in link]
                self.assertEqual(len(math), 1)
                self.assertEqual(len(formal), 1)
                self.assertEqual(math[0].split('#')[0], formal[0].split('#')[0])
                self.assertEqual(PurePosixPath(route, math[0]).parts[-4:], ('..', 'cores', core, 'index.html#question'))
            self.assertTrue(all('open' not in details for details in parsed.details))
        self.assertEqual(all_cards, expected)
        self.assertEqual((catalog, plan), before)
        landing = pages['quantumcomputingbench/lean/']
        self.assertIn('D0 studies these same questions; it adds no core', landing)
        self.assertIn('provisional construction routes, not measured model difficulty', landing)
        self.assertIn('not an interactive Lean REPL', landing)
        self.assertIn('separate from isolated generated-proof evaluation', landing)

    def test_counts_and_grouping_follow_the_supplied_plan(self):
        catalog = {'cores': [{'views': {}}, {'views': {'lean': {}}}]}
        plan = {'course_id': 'future-fixture', 'entries': [
            {'core_id': 'qcb-core-fixture-1', 'split': 'train', 'difficulty': {'construction_band': 'D2'}},
            {'core_id': 'qcb-core-fixture-2', 'split': 'dev', 'difficulty': {'construction_band': 'D4'}},
        ]}
        pages, report = self.render(plan, catalog)
        self.assertIn('data-qcb-lean-course-count="2"', pages['quantumcomputingbench/lean/'])
        self.assertEqual(report['by_construction_band'], {'D2': 1, 'D4': 1})
        self.assertEqual(Links(pages['quantumcomputingbench/lean/local/']).cards, ['qcb-core-fixture-1'])
        self.assertEqual(Links(pages['quantumcomputingbench/lean/compose/']).cards, [])
        plan['entries'].append({'core_id': 'qcb-core-fixture-3', 'split': 'test_public', 'difficulty': {'construction_band': 'D3'}})
        pages, report = self.render(plan, catalog)
        self.assertIn('data-qcb-lean-course-count="3"', pages['quantumcomputingbench/lean/'])
        self.assertEqual(Links(pages['quantumcomputingbench/lean/compose/']).cards, ['qcb-core-fixture-3'])
        self.assertEqual(report['course_id'], 'future-fixture')

    def test_duplicate_core_is_rejected_before_publication(self):
        entry = {'core_id': 'same-core', 'split': 'train', 'difficulty': {'construction_band': 'D2'}}
        with self.assertRaisesRegex(ValueError, 'unique shared course cores'):
            self.render({'course_id': 'fixture', 'entries': [entry, deepcopy(entry)]}, {'cores': []})

    def test_downloads_reject_changed_bytes_and_unexpected_files(self):
        qualification = {'suite_id': 'software-fixture', 'registry_digest': 'f' * 64}
        artifacts = {'train-references.json': {'software_fixture_only': True},
                     'dev-inputs.json': {'reference_answers_projected': False}}
        with tempfile.TemporaryDirectory() as temporary, patch.object(downloads, 'payloads', return_value=(qualification, artifacts)):
            root = Path(temporary)
            summary = downloads.write_downloads(root)
            downloads.check_downloads(root, summary)
            self.assertTrue(summary['artifacts']['train-references.json']['contains_references'])
            self.assertFalse(summary['artifacts']['dev-inputs.json']['contains_references'])
            path = root / 'dev-inputs.json'
            original = path.read_bytes()
            path.write_bytes(original + b' ')
            with self.assertRaises(ValueError):
                downloads.check_downloads(root, summary)
            path.write_bytes(original)
            (root / 'unexpected.json').write_text('{}')
            with self.assertRaises(ValueError):
                downloads.check_downloads(root, summary)

    def test_actual_download_splits_separate_train_proofs_from_evaluation_inputs(self):
        qualification, artifacts = downloads.payloads()
        training = artifacts['train-references.json']
        train_ids = {row['core_id'] for row in training['examples']}
        by_split = {split: {row['input']['task']['core_id'] for row in artifacts[split + '-inputs.json']['tasks']}
                    for split in ('train', 'dev', 'test_public')}
        self.assertEqual(train_ids, by_split['train'])
        self.assertFalse(train_ids & (by_split['dev'] | by_split['test_public']))
        self.assertFalse(by_split['dev'] & by_split['test_public'])
        self.assertEqual(len(set.union(*by_split.values())), qualification['distinct_shared_core_ids'])
        self.assertTrue(all(row['split'] == 'train' and row['target']['proof'].startswith('by') for row in training['examples']))
        for split in by_split:
            self.assertFalse(artifacts[split + '-inputs.json']['reference_answers_projected'])
            self.assertTrue(all('target' not in row and 'reference_lineage' not in row
                                for row in artifacts[split + '-inputs.json']['tasks']))


if __name__ == '__main__':
    unittest.main()
