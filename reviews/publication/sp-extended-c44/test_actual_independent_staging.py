"""Actual finite-SP capsules are mandatory evidence, not a new proof gate."""
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[3]
REPORT = 'reports/lean-433-migration/c44-sp-extended-actual-independent-staging.json'


def check_capsule(root, row):
    name = row['path']
    path = PurePosixPath(name)
    if path.is_absolute() or PureWindowsPath(name).is_absolute() or '..' in path.parts or '\\' in name:
        raise ValueError('non-portable capsule')
    full = root / path
    if not full.is_file():
        raise ValueError('missing mandatory independent capsule')
    if hashlib.sha256(full.read_bytes()).hexdigest() != row['sha256']:
        raise ValueError('stale capsule')
    with zipfile.ZipFile(full) as archive:
        if len(archive.namelist()) != len(row['members']) or set(archive.namelist()) != set(row['members']):
            raise ValueError('incomplete or duplicate members')
        for member, expected in row['members'].items():
            if hashlib.sha256(archive.read(member)).hexdigest() != expected:
                raise ValueError('stale member')


class ActualSPReadingTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((ROOT / REPORT).read_bytes())

    def test_all_seven_actual_capsules_and_every_member(self):
        self.assertEqual(len(self.report['packets']), 7)
        for row in self.report['packets']:
            check_capsule(ROOT, row)

    def test_missing_capsule_fails_not_skips(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, 'missing mandatory independent capsule'):
                check_capsule(Path(folder), self.report['packets'][0])

    def test_stale_capsule_is_rejected(self):
        row = copy.deepcopy(self.report['packets'][0])
        row['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'stale capsule'):
            check_capsule(ROOT, row)

    def test_every_whole_target_is_still_exact(self):
        self.assertEqual(len(self.report['modules']), 3)
        for row in self.report['modules']:
            self.assertEqual(hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest(), row['sha256'])
        self.assertEqual(self.report['target_catalogued_public'] + self.report['target_private'], 140)
        self.assertEqual(self.report['provider_retained_declarations'], 206)
        self.assertEqual(self.report['target_ambient_commands'], 27)

    def test_actual_distinct_roles_and_limited_scope(self):
        identities = [self.report[k] for k in ('decoder_identity', 'source_reviewer', 'topology_reviewer')]
        self.assertEqual(len(identities), len(set(identities)))
        self.assertEqual(self.report['historical_formalizer'], 'UNKNOWN')
        self.assertEqual(self.report['source_nodes'], 51)
        self.assertEqual(self.report['source_hyperedges'], 30)
        self.assertFalse(self.report['registry_changed'])
        self.assertFalse(self.report['scientific_ROOT'])
        self.assertFalse(self.report['main_migration_complete'])
        self.assertFalse(self.report['PURIFIED'])
        self.assertEqual(self.report['local_Lean_native_calls'], 0)

    def test_refinements_do_not_rewrite_original_decoder(self):
        capsule = next(row for row in self.report['packets'] if row['path'].endswith('sp-extended-c44-formal-decoder.zip'))
        self.assertEqual(capsule['members']['reconstruction.md'], '2130a3ac4fa6239928aac94e9a2c2873aecd1a87da729402ac1aa0d660bb824d')
        self.assertEqual(len(self.report['precision_notes']), 3)
        self.assertIn('lexicographic', self.report['precision_notes'][2])


if __name__ == '__main__':
    unittest.main()
