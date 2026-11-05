"""Privacy and immutable-output gates independent of the secret evaluation set."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / 'src'))
import qcb_assessment_bank as bank

spec = importlib.util.spec_from_file_location('assessment_cli_test', B / 'scripts/assessment.py')
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class SealedAssessmentGates(unittest.TestCase):
    def test_public_metadata_ignores_gold_question_and_answer_hinting_rationale(self):
        probe = {k: [] for k in bank.META_FIELDS if k != 'difficulty_band'}
        probe.update(difficulty={'band': 'D3', 'rationale': 'Private answer: false.'},
                     question='Private question.', gold={'answer': 'Private proof.'})
        before = bank.probe_metadata(probe)
        probe['gold'] = {'answer': 'Opposite secret answer.'}
        probe['question'] = 'Different secret question.'
        probe['difficulty']['rationale'] = 'Private intended polarity: true.'
        self.assertEqual(before, bank.probe_metadata(probe))
        self.assertNotIn('Private', json.dumps(before))
        before['source_nodes'].append('injected')
        self.assertEqual(probe['source_nodes'], [])

    def test_public_checkout_cannot_hold_the_private_bank_or_evaluation_outputs(self):
        with self.assertRaisesRegex(ValueError, 'outside'):
            bank.load_private_bank(bank.R / '_out/private')
        with self.assertRaisesRegex(ValueError, 'outside'):
            cli._private(bank.R / '_out/student.json')

    def test_changed_private_file_rejected_before_any_question_loading(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / 'cohort.json').write_text('{"changed":true}')
            with patch.object(bank, 'load_seal', return_value={
                    'private_files_sha256_lf': {'cohort.json': '0' * 64}}):
                with self.assertRaisesRegex(ValueError, 'private file changed'):
                    bank.load_private_bank(p, require_qualified=False)

    def test_public_qualification_rejects_added_secret_payload(self):
        with patch.object(bank, 'read_json', return_value={'question': 'Secret assessment.'}):
            with self.assertRaisesRegex(ValueError, 'qualification'):
                bank.validate_qualification({})

    def test_cli_never_overwrites_a_first_answer_or_previous_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'first.json'
            cli._write(p, {'first': True}, private=False)
            with self.assertRaises(FileExistsError):
                cli._write(p, {'first': False}, private=False)
            self.assertEqual(json.loads(p.read_text()), {'first': True})


if __name__ == '__main__':
    unittest.main()
