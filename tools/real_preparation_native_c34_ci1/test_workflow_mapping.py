"""Focused guard for the exact previously escaped YAML run indentation."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def check_runs(text):
    lines=text.splitlines();runs=[r for r in lines if r.lstrip().startswith('run:')]
    if len(runs)!=3 or any(not r.startswith('        run: ') for r in runs):
        raise ValueError('all three run directives must be step mappings, not top-level keys')
    if any('\t' in r for r in lines):raise ValueError('tabs are not workflow indentation')
    return runs
class WorkflowIndentationTests(unittest.TestCase):
    def test_current_three_steps_have_exact_mapping_indentation(self):
        w=(ROOT/'.github/workflows/c34-real-preparation-native.yml').read_text()
        self.assertEqual(len(check_runs(w)),3)
        self.assertIn('        run: python3 -B tools/real_preparation_native_c34_ci5/launch.py --python-tests',w)
    def test_parent_previous_unindented_patch_is_rejected(self):
        w=(ROOT/'.github/workflows/c34-real-preparation-native.yml').read_text()
        for row in check_runs(w):
            with self.assertRaises(ValueError):check_runs(w.replace(row,row.lstrip(),1))
if __name__=='__main__':unittest.main()
