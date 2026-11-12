"""Actual full CI artifact integrity is not publication/scientific acceptance."""
import hashlib,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent
class InstalledFullLeanEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=(BASE/'installed-full-lean-1b072e8-original.zip').read_bytes()
        cls.report=json.loads((ROOT/'reports/lean-433-migration/c47-installed-full-lean-tests-success.json').read_bytes())
        with zipfile.ZipFile(BASE/'installed-full-lean-1b072e8-original.zip') as z:
            cls.snapshot=json.loads(z.read('snapshot.json'));cls.result=json.loads(z.read('result.json'))
    def test_exact_original_GitHub_artifact_and_both_raw_members(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(),'551f5bcb7ca64335e7b2aaa3e3ab92ba3108efc2adb342a8af9f087eea656054')
        self.assertEqual(self.report['artifact']['GitHub_reported_digest'],'sha256:'+hashlib.sha256(self.raw).hexdigest())
        with zipfile.ZipFile(BASE/'installed-full-lean-1b072e8-original.zip') as z:
            self.assertEqual(set(z.namelist()),{'snapshot.json','result.json'})
            for row in self.report['artifact']['members']:
                self.assertEqual(hashlib.sha256(z.read(row['name'])).hexdigest(),row['sha256'])
    def test_actual_commands_and_success_only_after_both_steps(self):
        self.assertEqual(self.report['actual_full_commands'],['lake build','lake build Tests'])
        self.assertEqual(self.report['job']['conclusion'],'success')
        self.assertEqual(self.report['run']['conclusion'],'success')
        steps=self.report['job']['steps']
        build=next(s for s in steps if s['name']=='Full default library and every Tests target')
        record=next(s for s in steps if s['name']=='Record success only after both real full commands')
        self.assertEqual(build['conclusion'],'success');self.assertEqual(record['conclusion'],'success')
        self.assertLess(build['number'],record['number']);self.assertFalse(self.snapshot['full_Lean_Tests_success'])
        self.assertTrue(self.result['full_Lean_Tests_success']);self.assertGreaterEqual(len(self.report['actual_terminal_build_lines']),2)
    def test_complete_frozen_input_vector_and_real_Lean_version_are_retained(self):
        self.assertEqual(self.result['inputs'],self.snapshot['inputs']);self.assertEqual(len(self.result['inputs']),211)
        self.assertEqual(self.result['commit'],'1b072e87f59a6825597e4b6d49cd3b3ac4f1c9fb')
        self.assertIn('version 4.33.0',self.result['Lean_version']);self.assertEqual(len(self.result['Lean_binary_sha256']),64)
        self.assertEqual(self.report['current_contribution'],'142d10f098a6337b141368ad5683ac2238692d1a')
        self.assertTrue(self.report['current_committed_input_hashes_equal']);self.assertEqual(self.report['compared_input_files'],211)
        self.assertTrue(self.result['input_bytes_unchanged'])
    def test_publication_reader_and_finitebit_root_are_not_accepted_by_Lean_build(self):
        for field in ('publication_complete','website_gate','main_admitted','scientific_ROOT'):
            self.assertFalse(self.result[field])
        self.assertEqual(len(self.result['publication_missing_modules']),12)
        self.assertFalse(self.report['main_admitted']);self.assertFalse(self.report['Hermite_finitebit_family_root']);self.assertFalse(self.report['PURIFIED'])
        self.assertEqual(self.report['main_actual_Lean'],'4.29.1');self.assertTrue(self.report['raw_host_path_bearing_log_not_published'])
if __name__=='__main__':unittest.main()
