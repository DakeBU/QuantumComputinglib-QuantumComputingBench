"""Real kernel candidate success is scoped to the captured isolated cohort."""
import hashlib
import json
from pathlib import Path
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[3]
class ActualKernelCandidateTests(unittest.TestCase):
    def test_actual_archive_and_all30_original_public_members(self):
        r=json.loads((ROOT/'reports/lean-433-migration/c29-actual-kernel-ci1.json').read_bytes())
        self.assertEqual(hashlib.sha256((ROOT/r['archive']).read_bytes()).hexdigest(),r['archive_sha256'])
        with zipfile.ZipFile(ROOT/r['archive']) as z:
            self.assertEqual(len(z.namelist()),30)
            for row in r['members']:
                raw=z.read(row['name']);self.assertEqual(len(raw),row['bytes'])
                self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])

    def test_actual_fresh_compile_and_probe_not_synthetic_or_timeout(self):
        r=json.loads((ROOT/'reports/lean-433-migration/c29-actual-kernel-ci1.json').read_bytes())
        for row,limit in zip(r['calls'],(600,300)):
            self.assertGreater(row['PID'],0);self.assertEqual(row['exitCode'],0)
            self.assertFalse(row['timedOut']);self.assertEqual(row['timeoutSeconds'],limit)
            self.assertEqual((row['memoryMiB'],row['threads']),(3072,1))
        self.assertEqual(r['fresh_artifacts']['files'][0]['sha256'],'a570144205d89df5604c2f0096df773c8a9174a01d42043bc73a40dd420adb71')

    def test_nine_removed_eight_aux_and_dynamic449_not450_or441(self):
        r=json.loads((ROOT/'reports/lean-433-migration/c29-actual-kernel-ci1.json').read_bytes())
        q=r['parent_relational_replay']
        self.assertEqual((q['explicitRoots'],q['generatedObserved']),(319,449))
        self.assertEqual(len(q['removedNativeAxiomsAbsent']),9)
        self.assertEqual(len(q['additionalGeneratedTheorems']),8)
        self.assertEqual(q['newRecursiveAxiomUnion'],['Classical.choice','Quot.sound','propext'])
        self.assertTrue(q['generatedCountWasNotAssumed450'])
        self.assertTrue(r['parent_replayed_actual_stdout_not_synthetic'])

    def test_source_production_and_scientific_acceptance_not_promoted(self):
        r=json.loads((ROOT/'reports/lean-433-migration/c29-actual-kernel-ci1.json').read_bytes())
        self.assertFalse(r['production_Lean_changed'])
        for field in ('nativeAccepted','scientific_ROOT','main_admission','PURIFIED'):
            self.assertFalse(r[field])
        self.assertIsNone(r['sourceAgreement']);self.assertIsNone(r['axiomPolicyPass'])
        self.assertFalse(r['historical_wrapper_D1_retroactively_fixed'])

if __name__=='__main__':unittest.main()
