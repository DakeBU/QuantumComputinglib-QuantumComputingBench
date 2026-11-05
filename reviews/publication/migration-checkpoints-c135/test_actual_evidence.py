"""Check delivered evidence, without executing archived candidate code."""
import hashlib,json,re,unittest
from pathlib import Path
from zipfile import ZipFile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest()

class ActualEvidence(unittest.TestCase):
    def test_four_exact_releases(self):
        index=json.loads((HERE/'index.json').read_bytes())
        self.assertEqual((index['archive_count'],index['member_count']),(4,52))
        for row in index['archives']:
            archive=HERE/row['archive']
            self.assertEqual(sha(archive.read_bytes()),row['sha256'])
            with ZipFile(archive) as z:
                self.assertEqual(set(z.namelist()),set(row['members']))
                for name,item in row['members'].items():
                    raw=z.read(name)
                    self.assertEqual((len(raw),sha(raw)),(item['bytes'],item['sha256']))
                    self.assertNotIn('PRIVATE/',name)
                    self.assertIsNone(re.search(rb'(?<![A-Za-z0-9])[A-Za-z]:[\\/]',raw))
                self.assertEqual(sha(z.read(row['manifest'])),row['manifest_sha256'])
                self.assertEqual(sha(z.read(row['seal'])),row['seal_sha256'])
        self.assertFalse(index['production_changed'])
        self.assertFalse(index['source_admission'])

    def test_exact_observation_transport(self):
        index=json.loads((HERE/'observation-transports.json').read_bytes())
        archive=HERE/index['exact_archive']
        self.assertEqual(sha(archive.read_bytes()),index['exact_archive_sha256'])
        with ZipFile(archive) as z:
            self.assertEqual(set(z.namelist()),set(index['members']))
            for name,row in index['members'].items():
                folder,filename=name.split('/')
                dest=HERE/filename if folder==HERE.name else ROOT/'experiments/uncompute-2610-22367'/folder/filename
                raw=z.read(name);flat=dest.read_bytes()
                self.assertEqual(sha(raw),row['original_sha256'])
                self.assertEqual(sha(flat),row['transport_sha256'])
                self.assertEqual(flat,raw.replace(b'\r\n',b'\n'))
                self.assertIsNone(re.search(rb'(?<![A-Za-z0-9])[A-Za-z]:[\\/]',raw))

    def test_real_historical_failure_and_success(self):
        for run,code,errors in [(2,1,1),(3,0,0)]:
            execution=json.loads((HERE/f'historical-run-{run}-execution.json').read_bytes())
            outcome=json.loads((HERE/f'historical-run-{run}-stdout.sanitized.txt').read_bytes())
            self.assertEqual(execution['exitCode'],code)
            self.assertFalse(execution['timedOut'])
            self.assertTrue(execution['afterInventoriesEqual'])
            self.assertTrue(execution['afterControlPinsEqual'])
            self.assertEqual(execution['sourceCommit'],'1a4d0522f1f76ba26bd7a1fa20b9fb2bb4cf6fe4')
            self.assertEqual((outcome['testsRun'],outcome['failures'],outcome['errors'],outcome['skipped'],outcome['expectedFailures']),(35,0,errors,0,0))
            self.assertEqual(outcome['complete35Passed'],run==3)
            for flag in ['nativeExecuted','currentHEADAcceptance','scientificAcceptance']:
                self.assertFalse(outcome[flag])
            self.assertFalse(execution['nativeExecutionAuthorized'])
            self.assertGreater(execution['PID'],0)
            self.assertGreater(execution['wallSeconds'],0)

    def test_parent_tests_and_no_new_lean(self):
        for version,count in [('v2',28),('v3',29)]:
            row=json.loads((HERE/f'parent-{version}-outer-observations.json').read_bytes())
            self.assertEqual(row['records'][0]['stage'],'new-synthetic-tests')
            self.assertEqual(row['records'][0]['exit_code'],0)
            self.assertFalse(row['Lean_launched'])
            self.assertFalse(row['current_head_acceptance'])
            self.assertFalse(row['scientific_ROOT'])

    def test_bounded_runtime_association(self):
        row=json.loads((HERE/'parent-runtime-association-rehash.json').read_bytes())
        self.assertEqual((row['file_bindings'],row['git_blob_bindings'],row['zip_member_bindings'],row['total_bindings'],row['exact_members']),(198,428,2,628,14))
        self.assertTrue(row['additional_three_control_pins_not_backfilled_into_original211'])
        for flag in ['new_compile_or_native_run','new_current_build','clean_TCB','source_or_publication_admission','scientific_ROOT']:
            self.assertFalse(row[flag])

if __name__=='__main__':unittest.main()
