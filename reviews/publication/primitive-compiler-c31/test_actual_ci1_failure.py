"""Actual failed native observation, not a theorem or admission success."""
import hashlib
import json
from pathlib import Path
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[3]
sha=lambda b:hashlib.sha256(b).hexdigest()

class ActualCI1FailureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt=json.loads((ROOT/'reports/lean-433-migration/c31-actual-ci1-native-memory-failure.json').read_bytes())
        cls.raw=(ROOT/cls.receipt['archive']).read_bytes()
        with zipfile.ZipFile(ROOT/cls.receipt['archive']) as z:
            cls.names=z.namelist()
            cls.files={n:z.read(n) for n in cls.names}

    def test_exact_actual_archive_and_member_bytes(self):
        self.assertEqual(sha(self.raw),'a2edbb904f6be270e3b1c7dabc1090808390667ecf95f8dee323dbbe9de70dd6')
        self.assertEqual(sha(self.raw),self.receipt['archive_sha256'])
        self.assertEqual(len(self.raw),self.receipt['archive_bytes'])
        self.assertEqual(len(self.names),21)
        self.assertEqual(len(set(self.names)),21)
        self.assertEqual(set(self.files),{r['path'] for r in self.receipt['files']})
        for row in self.receipt['files']:
            self.assertEqual(sha(self.files[row['path']]),row['sha256'])
            self.assertEqual(len(self.files[row['path']]),row['bytes'])

    def test_three_observed_calls_not_three_successes(self):
        calls=self.receipt['actual_calls']
        self.assertEqual([c['label'] for c in calls],['01-help','02-prefix','11-target'])
        self.assertEqual([c['PID'] for c in calls],[13278,13281,13289])
        self.assertEqual([c['exitCode'] for c in calls],[0,0,-6])
        for call in calls:
            self.assertFalse(call['timedOut'])
            self.assertEqual({k:v for k,v in call.items() if k!='label'},json.loads(self.files[call['label']+'.result.json']))

    def test_raw_and_public_streams_are_not_conflated(self):
        rows=json.loads(self.files['raw-derivation-receipts.json'])['files']
        derivation={r['publicRelativePath']:r for r in rows}
        for name,row in derivation.items():
            self.assertEqual(sha(self.files[name]),row['publicSHA256'])
        for call in self.receipt['actual_calls']:
            for stream in ('stdout','stderr'):
                name=call['label']+'.'+stream+'.raw.sanitized.txt'
                self.assertEqual(call[stream+'SHA256'],derivation[name]['rawSHA256'])
        prefix=derivation['02-prefix.stdout.raw.sanitized.txt']
        self.assertNotEqual(prefix['rawSHA256'],prefix['publicSHA256'])

    def test_failure_is_actual_internal_cap_not_timeout_or_mathematics(self):
        setup=json.loads(self.files['11-target.setup.json'])
        self.assertIn('--memory=3072',setup['argv'])
        self.assertIn('--threads=1',setup['argv'])
        self.assertEqual(setup['argv'][-1],'QuantumBlockEncoding/PrimitiveMacros.lean')
        self.assertIn(b'lean::memory_exception',self.files['11-target.stderr.raw.sanitized.txt'])
        self.assertIn(b"at 'interpreter'",self.files['11-target.stderr.raw.sanitized.txt'])
        self.assertEqual(self.files['11-target.stdout.raw.sanitized.txt'],b'')
        self.assertEqual(self.receipt['status'],'ENV_BLOCKED_LEAN_INTERNAL_MEMORY_CAP_NOT_MATHEMATICAL_REFUTATION')

    def test_no_collector_output_or_native_acceptance_invented(self):
        self.assertFalse(self.receipt['collector_executed'])
        self.assertEqual(self.receipt['actual_signatures_collected'],0)
        self.assertEqual(self.receipt['actual_fresh_target_success_count'],0)
        self.assertFalse(any('probe' in n.lower() or 'collector' in n.lower() for n in self.names))
        actual=json.loads(self.files['result.json'])
        for row in (actual,self.receipt):
            self.assertFalse(row['nativeAccepted'])
            self.assertFalse(row['trustClosure'])
            self.assertIsNone(row['sourceAgreement'])
            self.assertIsNone(row['axiomPolicyPass'])
            self.assertIsNone(row['publicationBinding'])
        self.assertFalse(self.receipt['scientific_ROOT'])

    def test_source_pins_and_same_frozen_profile(self):
        inputs=json.loads(self.files['input-bindings.json'])
        self.assertEqual(len(inputs['projectInputs']),31)
        for row in inputs['projectInputs']:
            data=(ROOT/row['relativePath']).read_bytes()
            self.assertEqual(sha(data),row['sha256'])
            self.assertEqual(len(data),row['bytes'])
        self.assertEqual(inputs['profileSHA256'],self.receipt['profile_sha256'])
        self.assertEqual(sha((ROOT/'tools/primitive_compiler_native_profile_v1/profile.json').read_bytes()),inputs['profileSHA256'])

    def test_public_archive_has_no_private_job_log_or_host_paths(self):
        self.assertFalse(any(n.startswith('job.raw') or n.startswith('artifact.raw') for n in self.names))
        for name,data in self.files.items():
            self.assertNotIn('/',name)
            self.assertNotIn('\\',name)
            for forbidden in (b'C:\\Users\\',b'C:/Users/',b'D:\\Users\\',b'D:/Users/',b'/home/runner/',b'github_pat_',b'ghp_'):
                self.assertNotIn(forbidden,data)

if __name__=='__main__':unittest.main()
