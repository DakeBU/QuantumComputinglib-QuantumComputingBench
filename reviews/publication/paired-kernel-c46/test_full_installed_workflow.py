"""The full installed-source observation cannot silently become a weaker gate."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
class FullInstalledWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.text=(ROOT/'.github/workflows/installed-lean433-full.yml').read_text()
    def test_full_library_and_tests_commands_are_unconditional_and_ordered(self):
        self.assertIn('          lake build\n          lake build Tests\n',self.text)
        for bad in ('--old','--allow-empty','continue-on-error','|| true'):self.assertNotIn(bad,self.text)
        self.assertGreater(self.text.index('Record success only after'),self.text.index('lake build Tests'))
    def test_publication_debt_is_preserved_and_current_records_are_checked(self):
        self.assertIn('for row in records:gate.validate_record(root,row,inventory)',self.text)
        self.assertIn('publication_missing_modules=missing,publication_complete=not missing',self.text)
        self.assertIn('main_admitted=False,scientific_ROOT=False',self.text)
        self.assertIn('website_gate=False',self.text)
    def test_new_workflow_runs_on_scoped_WIP_push_without_main_registration(self):
        self.assertIn('branches: ["work/lean433-curriculum-20261008"]',self.text)
        self.assertIn('".github/workflows/installed-lean433-full.yml"',self.text)
        self.assertNotIn("pages: write",self.text)
        self.assertNotIn("pull_request_target",self.text)
    def test_real_source_binary_and_missing_artifact_guards_remain(self):
        self.assertIn('full_Lean_Tests_success=False',self.text)
        self.assertIn('before[\'inputs\'].items()',self.text)
        self.assertIn("assert 'version 4.33.0' in version",self.text)
        self.assertIn('if-no-files-found: error',self.text)
        self.assertIn('cancel-in-progress: false',self.text)
if __name__=='__main__':unittest.main()
