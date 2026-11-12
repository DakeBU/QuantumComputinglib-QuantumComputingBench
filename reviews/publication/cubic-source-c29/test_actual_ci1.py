"""Exact external CI failure regression; archive is not successful proof evidence."""
import hashlib
import io
import json
from pathlib import Path
import unittest
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


class ActualCI1Tests(unittest.TestCase):
    def setUp(self):
        self.receipt = json.loads((ROOT/'reports/lean-433-migration/c29-actual-ci1-failure.json').read_bytes())
        raw = (ROOT/self.receipt['archive']).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), self.receipt['archive_sha256'])
        self.assertEqual(len(raw), self.receipt['archive_bytes'])
        self.archive = zipfile.ZipFile(io.BytesIO(raw))

    def tearDown(self):
        self.archive.close()

    def test_entire_public_archive_is_byte_bound(self):
        self.assertEqual(len(self.archive.infolist()), 24)
        self.assertEqual({row['path'] for row in self.receipt['files']}, set(self.archive.namelist()))
        for row in self.receipt['files']:
            raw = self.archive.read(row['path'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])
            self.assertEqual(len(raw), row['bytes'])

    def test_actual_failure_precedes_any_target_compile(self):
        compiled = json.loads(self.archive.read('03-fixture-compile.result.json'))
        probe = json.loads(self.archive.read('04-fixture-probe.result.json'))
        result = json.loads(self.archive.read('result.json'))
        self.assertEqual(compiled['exitCode'], 0)
        self.assertEqual(probe['exitCode'], 1)
        self.assertGreater(probe['PID'], 0)
        self.assertFalse(probe['timedOut'])
        self.assertFalse(result['nativeAccepted'])
        self.assertFalse(self.receipt['target_Lean_compile_observed'])
        self.assertFalse(any(name.startswith('05-target') for name in self.archive.namelist()))

    def test_old_fixture_import_mistake_is_preserved(self):
        old = (ROOT/'tools/cubic_c29_diagnostic/FixtureProbe-v4.lean').read_bytes()
        self.assertEqual(hashlib.sha256(old).hexdigest(), '5cdb144bf235b45dca334984a306fa8e73c709afdf1cee60a7194de1e9fa6160')
        self.assertTrue(old.startswith(b'import QuantumBlockEncoding.CubicStatePreparation\n'))
        failure = self.archive.read('04-fixture-probe.stdout.raw.sanitized.txt').decode()
        self.assertIn('CubicStatePreparation.olean', failure)
        self.assertIn('does not exist', failure)


if __name__ == '__main__':
    unittest.main()
