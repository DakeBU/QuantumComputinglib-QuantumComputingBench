"""Actual preflight refusal is neither low-host-memory nor Lean failure proof."""
import hashlib
import json
from pathlib import Path
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[3]
sha=lambda b:hashlib.sha256(b).hexdigest()

class ActualCI2PreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/'reports/lean-433-migration/c31-actual-ci2-preflight-refusal.json').read_bytes())
        cls.raw=(ROOT/cls.r['archive']).read_bytes()
        with zipfile.ZipFile(ROOT/cls.r['archive']) as z:
            cls.names=z.namelist();cls.files={n:z.read(n) for n in cls.names}
        cls.pre=json.loads(cls.files['ci2-01-help.preflight.json'])
        cls.result=json.loads(cls.files['result.json'])

    def test_exact_four_member_archive_and_each_member(self):
        self.assertEqual(sha(self.raw),'88cf00aa01965456ffd2c37ec61c7abcf0a84bdd3f0e79ff9aef55522b9e1a88')
        self.assertEqual(sha(self.raw),self.r['archive_sha256'])
        self.assertEqual(len(self.raw),self.r['archive_bytes'])
        self.assertEqual(len(self.names),4);self.assertEqual(len(set(self.names)),4)
        self.assertEqual(set(self.names),{'ci2-01-help.preflight.json','raw-derivation-receipts.json','input-bindings.json','result.json'})
        for row in self.r['files']:
            self.assertEqual((sha(self.files[row['path']]),len(self.files[row['path']])),(row['sha256'],row['bytes']))

    def test_measured_host_headroom_is_not_complete_effective_accounting(self):
        p=self.pre
        self.assertEqual(p['memAvailableBytes'],15220740096)
        self.assertEqual(p['requiredHeadroomBytes'],7516192768)
        self.assertGreater(p['memAvailableBytes'],p['requiredHeadroomBytes'])
        self.assertIsNone(p['effectiveHeadroomBytes'])
        self.assertFalse(p['observationComplete']);self.assertFalse(p['gatePassed'])
        self.assertEqual(p['failureType'],'FileNotFoundError')
        self.assertEqual((p['budgetMiB'],p['reserveMiB']),(5120,2048))

    def test_two_groups_and_nine_successful_file_reads_do_not_fill_missing_root(self):
        p=self.pre
        self.assertEqual(len(p['cgroups']),2);self.assertEqual(len(p['fileReads']),9)
        self.assertEqual([g['logicalPath'] for g in p['cgroups']],['$CGROUP_ANCESTOR_0','$CGROUP_ANCESTOR_1'])
        for g in p['cgroups']:
            self.assertEqual(g['memoryMaxRaw'],'max')
            self.assertIsNone(g['memoryMaxBytes'])
            self.assertEqual(g['memoryEvents']['oom_kill'],0)
        self.assertFalse(self.r['exact_missing_path_established'])
        self.assertIsNone(self.r['failed_read_logical_coordinate'])
        self.assertNotIn('failedReadLogicalPath',p)

    def test_refusal_is_before_even_help_native_child(self):
        self.assertEqual(self.pre['wrapperPID'],13394)
        self.assertEqual(self.result['failureType'],'PreflightRefused')
        self.assertEqual(self.result['failure'],'NO_CHILD_STARTED: resource observation incomplete')
        self.assertFalse(any(n.endswith('.started.json') or n.endswith('.result.json') for n in self.names))
        for key in ('actual_native_child_count','actual_Lean_child_count','actual_fresh_target_success_count'):
            self.assertEqual(self.r[key],0)
        self.assertFalse(self.r['collector_executed'])

    def test_raw_to_public_snapshots_keep_separate_hashes(self):
        rows=json.loads(self.files['raw-derivation-receipts.json'])['files']
        self.assertEqual(len(rows),3)
        for row in rows:
            self.assertEqual(sha(self.files[row['publicRelativePath']]),row['publicSHA256'])
        row=next(r for r in rows if r['publicRelativePath']=='ci2-01-help.preflight.json')
        self.assertNotEqual(row['rawSHA256'],row['publicSHA256'])

    def test_same_current_thirty_one_source_and_config_pins(self):
        rows=json.loads(self.files['input-bindings.json'])['projectInputs']
        self.assertEqual(len(rows),31)
        for row in rows:
            data=(ROOT/row['relativePath']).read_bytes()
            self.assertEqual((sha(data),len(data)),(row['sha256'],row['bytes']))
        self.assertEqual(self.pre['binding']['ci2ProfileSHA256'],'7047f441d8f6afe7a85b547d2f58b9156a4bf5792d1260f962221e1c03836ee3')

    def test_no_acceptance_or_private_path_leak(self):
        for row in (self.r,self.pre,self.result):
            self.assertFalse(row['nativeAccepted']);self.assertIsNone(row['sourceAgreement'])
            self.assertIsNone(row['axiomPolicyPass']);self.assertIsNone(row['publicationBinding'])
        self.assertFalse(self.r['scientific_ROOT'])
        for data in self.files.values():
            for forbidden in (b'C:/Users/',b'C:\\Users\\',b'D:/Users/',b'D:\\Users\\',b'/home/runner/',b'github_pat_',b'ghp_'):
                self.assertNotIn(forbidden,data)

if __name__=='__main__':unittest.main()
