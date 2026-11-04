"""Supplemental math intake: source identity, split boundaries and public views."""
import json
import shutil
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'benchmarks/quantumcomputingbench/src'))
import qcb_nonlean_workbook as source

from website.scripts import qcb_workbook_reader as view
from website.scripts.qcb_render_test_support import recover_prose_source


class WorkbookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = source.load_workbook()
        _, _, cls.graph = source.load_catalog()

    def test_two_archives_do_not_create_twenty_four_tasks_or_new_splits(self):
        w = self.workbook
        self.assertEqual(len(w['entries']), 12)
        self.assertEqual(w['counts']['existing_core_expositions'], 4)
        self.assertEqual(w['counts']['unassigned_candidates'], 8)
        self.assertEqual(w['counts']['by_band'], {'D2': 3, 'D3': 5, 'D4': 4})
        self.assertEqual(w['counts']['scored_training_or_evaluation_rows_added'], 0)
        self.assertFalse(w['human_expert_approval'])
        for entry in w['entries']:
            if entry['packet']['contribution_type'] == 'new_candidate':
                self.assertEqual(entry['packet']['split'], 'unassigned_pending_reconciliation')

    def test_questions_and_references_are_separate_exact_projections(self):
        payloads = source.download_payloads(self.workbook)
        questions = [json.loads(line) for line in payloads['questions.jsonl'].splitlines()]
        references = [json.loads(line) for line in payloads['references.jsonl'].splitlines()]
        self.assertEqual(len(questions), 12)
        for row, answer, entry in zip(questions, references, self.workbook['entries']):
            self.assertEqual(set(row), {'schema_version', 'view_id', 'question_sha256', 'input'})
            self.assertEqual(set(row['input']), {'question', 'assumptions', 'conventions'})
            self.assertEqual(row['input']['question'], entry['packet']['question'])
            self.assertEqual(answer['reference_answer'], entry['packet']['reference_answer'])
            self.assertFalse(answer['new_lean_verification'])

    def test_rehashed_answer_leak_does_not_pass_download_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            source.write_downloads(tmp, self.workbook)
            source.verify_downloads(tmp, self.workbook)
            target = Path(tmp) / 'questions.jsonl'
            row = json.loads(target.read_text().splitlines()[0])
            row['input']['answer'] = 'leaked reference'
            target.write_text(json.dumps(row) + '\n')
            manifest = Path(tmp) / 'download-manifest.json'
            value = json.loads(manifest.read_text())
            value['files']['questions.jsonl']['sha256'] = source.sha(target)
            manifest.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError, 'projection changed'):
                source.verify_downloads(tmp, self.workbook)

    def test_no_reference_or_premise_is_lost_by_typesetting(self):
        for entry in self.workbook['entries']:
            p = entry['packet']
            body = view.page_body(entry, self.workbook, self.graph, set(self.graph), 'a' * 40)
            fields = [p['question'], p['reference_answer']] + p['assumptions'] + p['conventions']
            fields += [r['criterion'] for r in entry['display_rubric']]
            for original in fields:
                with self.subTest(slot=entry['slot'], text=original[:40]):
                    recovered = recover_prose_source(body, original)
                    self.assertEqual(' '.join(recovered.split()), ' '.join(original.split()))
            self.assertIn('<details class="qcb-disclosure" id="solution">', body)
            self.assertNotIn('<details open', body)
            self.assertIn('No human expert approval or new Lean proof execution', body)

    def test_clarified_rubric_accepts_equivalent_form_without_rewriting_original(self):
        entry = next(e for e in self.workbook['entries'] if e['slot'] == 'B2')
        old = next(r for r in entry['packet']['rubric'] if r['id'] == 'r2')
        new = next(r for r in entry['display_rubric'] if r['id'] == 'r2')
        self.assertIn('partial credit', old['criterion'])
        self.assertIn('full credit', new['criterion'])
        self.assertEqual(old['weight'], new['weight'])

    def test_precision_and_boundary_routes_do_not_inherit_replaced_premises(self):
        for slot, node, forbidden in (('C2', 'C2-S7', 'C2-I4'),
                                      ('C3', 'C3-S7', 'C3-I4'),
                                      ('C4', 'C4-S7', 'C4-I3b')):
            m = next(e for e in self.workbook['entries'] if e['slot'] == slot)['display_reasoning_map']
            steps = {s['id']: s for s in m['steps']}
            def ancestors(key, dag=steps):
                result = set()
                for predecessor in dag.get(key, {}).get('required_inputs', []):
                    result.add(predecessor)
                    result.update(ancestors(predecessor, dag))
                return result
            self.assertNotIn(forbidden, ancestors(node))

    def test_mutated_raw_payload_or_notation_cannot_reuse_review(self):
        for relative in (source.PACKAGE.relative_to(source.R) / 'qa/A2.json',
                         source.AUDIT.relative_to(source.R) / 'A-notation.json'):
            with self.subTest(path=str(relative)), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                for directory in (source.PACKAGE, source.CONTINUATION, source.AUDIT):
                    shutil.copytree(directory, root / directory.relative_to(source.R))
                proposals = source.B / 'tracks/non-lean/proposals'
                shutil.copytree(proposals, root / proposals.relative_to(source.R))
                changed = root / relative
                changed.write_bytes(changed.read_bytes() + b' ')
                with patch.multiple(source, R=root, B=root / source.B.relative_to(source.R),
                                    PACKAGE=root / source.PACKAGE.relative_to(source.R),
                                    CONTINUATION=root / source.CONTINUATION.relative_to(source.R),
                                    AUDIT=root / source.AUDIT.relative_to(source.R)), \
                        self.assertRaisesRegex(ValueError, 'changed'):
                    source.load_workbook()

    def test_removed_notation_binding_cannot_license_unreviewed_tex(self):
        original_read = source.read_json
        def changed(path):
            value = original_read(path)
            if Path(path).name == 'reader-comparison.json':
                value['reviewed_file_sha256'].pop((source.AUDIT / 'B-notation.json').relative_to(source.R).as_posix())
            return value
        with patch.object(source, 'read_json', changed), self.assertRaisesRegex(ValueError, 'bind every'):
            source.load_workbook()

    def test_publication_cannot_pin_new_sources_to_an_old_commit(self):
        with self.assertRaisesRegex(ValueError, 'not committed'):
            source.check_publication_sources(self.workbook, 'e31696ea27811d5679154b8d6a4f78fd7cbbb3a7')

    def test_graph_routes_use_real_snapshot_ids(self):
        pages = {}
        def write(route, title, body, description):
            pages[route] = body
        def intro(title, subtitle):
            return '<div class="qcb-reader"><h1>' + title + '</h1><p>' + subtitle + '</p>'
        before = deepcopy(self.workbook)
        report = view.publish_workbook(write, intro, self.workbook, self.graph, set(self.graph), 'a' * 40)
        self.assertEqual(len(pages), 20)
        self.assertEqual(report['new_canonical_cores'], 0)
        self.assertIn(view.BASE + 'graph/', pages)
        self.assertEqual(self.workbook, before)


if __name__ == '__main__':
    unittest.main()
