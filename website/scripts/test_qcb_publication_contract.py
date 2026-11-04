"""Source preservation and evidence gates for the richer benchmark reader."""
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'benchmarks/quantumcomputingbench/src'))
from qcb_bench_runtime import build_registry

from website.scripts import qcb_math
from website.scripts import quantumcomputingbench as reader
from website.scripts.qcb_render_test_support import recover_prose_source


class PublicationContractTests(unittest.TestCase):
    def test_all_ordinary_questions_and_answers_preserve_the_source_tokens(self):
        registry = build_registry()
        for task in registry['tasks']:
            if task['track'] == 'lean':
                continue
            for original in (task['input']['question'], task['reference']['answer']):
                with self.subTest(task=task['task_id'], source=original[:45]):
                    recovered = recover_prose_source(qcb_math.render_prose(original), original)
                    self.assertEqual(' '.join(recovered.split()), ' '.join(original.split()))

    def test_unchanged_question_hash_does_not_license_changed_displayed_math(self):
        review = reader.read_json(reader.B / 'reports/ecosystem-v1/math-notation-review.json')
        reader.math_notation_contract(review['catalog_hash'])
        edited = deepcopy(qcb_math._QUESTION_COMPANIONS)
        edited[next(iter(edited))]['tex'] += r'\quad 0=1'
        with patch.object(qcb_math, '_QUESTION_COMPANIONS', edited), \
                self.assertRaisesRegex(ValueError, 'notation changed'):
            reader.math_notation_contract(review['catalog_hash'])

    def test_unexecuted_and_stale_container_evidence_are_different(self):
        registry = {'registry_hash': 'expected-registry', 'source_commit': 'a' * 40}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(reader, 'ROOT', root):
                absent = reader.environment_record(registry)
                self.assertEqual(absent['execution_status'], 'not_run')
                self.assertIsNone(absent['passed'])
                location = root / '_out/qcb-container-smoke/public-summary.json'
                location.parent.mkdir(parents=True)
                location.write_text(json.dumps({'schema_version': 'qcb.portable_environment_smoke.v1',
                    'execution_status': 'passed', 'passed': True, 'registry_hash': 'stale-registry'}))
                with self.assertRaisesRegex(ValueError, 'does not match'):
                    reader.environment_record(registry)


if __name__ == '__main__':
    unittest.main()
