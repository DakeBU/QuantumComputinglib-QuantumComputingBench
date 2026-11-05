"""Frozen actual-reading integrity and finite diagnostics, not Lean admission."""
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[3]
REPORT = 'reports/lean-433-migration/c44-ghl-actual-independent-reading-staging.json'


def read_report():
    return json.loads((ROOT / REPORT).read_bytes())


def check_capsule(root, row):
    name = row['path']
    path = PurePosixPath(name)
    if path.is_absolute() or PureWindowsPath(name).is_absolute() or '..' in path.parts or '\\' in name:
        raise ValueError('non-portable capsule path')
    full = root / path
    if not full.is_file():
        raise ValueError('missing mandatory capsule')
    if hashlib.sha256(full.read_bytes()).hexdigest() != row['sha256']:
        raise ValueError('stale capsule bytes')
    with zipfile.ZipFile(full) as archive:
        if set(archive.namelist()) != set(row['members']) or len(archive.namelist()) != len(row['members']):
            raise ValueError('capsule member inventory mismatch')
        for member, expected in row['members'].items():
            if hashlib.sha256(archive.read(member)).hexdigest() != expected:
                raise ValueError('stale capsule member')


class IndependentGHLStagingTests(unittest.TestCase):
    def test_all_five_actual_capsules_and_every_member_are_mandatory(self):
        report = read_report()
        self.assertEqual(len(report['packets']), 5)
        for row in report['packets']:
            check_capsule(ROOT, row)

    def test_missing_capsule_fails_instead_of_skipping(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, 'missing mandatory capsule'):
                check_capsule(Path(folder), read_report()['packets'][0])

    def test_stale_capsule_fails(self):
        row = read_report()['packets'][0]
        with tempfile.TemporaryDirectory() as folder:
            full = Path(folder) / row['path']
            full.parent.mkdir(parents=True)
            full.write_bytes(b'not the independently frozen capsule')
            with self.assertRaisesRegex(ValueError, 'stale capsule bytes'):
                check_capsule(Path(folder), row)

    def test_current_whole_target_and_local_source_are_bound(self):
        report = read_report()
        self.assertEqual(hashlib.sha256((ROOT / report['target']).read_bytes()).hexdigest(), report['target_sha256'])
        self.assertEqual(hashlib.sha256((ROOT / report['natural_lesson']).read_bytes()).hexdigest(), report['natural_lesson_sha256'])
        self.assertEqual(report['target_explicit_declarations'], 405)
        self.assertEqual(report['target_catalogued_public'] + report['target_private'], 405)
        self.assertEqual(report['full_formal_lines'], 10027)

    def test_real_identities_and_non_admission_boundary(self):
        report = read_report()
        self.assertEqual(report['decoder_identity'], '/root/ghl_formal_decoder_c43')
        self.assertEqual(report['reviewer_identity'], '/root/ghl_local_source_first_c43')
        self.assertNotEqual(report['decoder_identity'], report['reviewer_identity'])
        self.assertEqual(report['historical_formalizer'], 'UNKNOWN')
        self.assertFalse(report['registry_changed'])
        self.assertFalse(report['main_migration_complete'])
        self.assertFalse(report['scientific_ROOT'])
        self.assertFalse(report['PURIFIED'])
        self.assertEqual(report['local_Lean_native_calls'], 0)

    def test_off_width_precision_delta_finite_diagnostic_only(self):
        # Exact integer transcription of the three inspected extractor formulas.
        # This execution is not a Lean bridge, uniform family theorem or paper refutation.
        def sparse_values(n, kappa, j):
            ell = max(0, kappa - 1).bit_length()
            padding = max(0, n - ell)
            od = (j >> (1 + n)) & ((1 << n) - 1)
            mask = (1 << ell) - 1
            return ((od >> padding) & mask, (j >> (1 + n + padding)) & mask)
        self.assertEqual(sparse_values(1, 8, 8), (0, 2))
        for n in range(1, 7):
            for kappa in range(1, (1 << n) + 1):
                for j in (0, 1, 8, 32, 112, (1 << (2*n+2))-1):
                    a, b = sparse_values(n, kappa, j)
                    self.assertEqual(a, b)

    def test_inactive_slot_collision_finite_diagnostic_only(self):
        # n=3,kappa=7,w=0. This only checks the exact total-map witness;
        # it does not contradict the existing active slot<7 theorem.
        def image(j):
            row = (j >> 1) & 7
            slot = (j >> 4) & 7
            offsets = (6, 7, 0, 1, 2, 5, 3)
            address = ((offsets[slot] if slot < 7 else 0) + row) % 8
            return (j % 16) + address * 16 + (j // 128) * 128
        self.assertEqual(image(32), 0)
        self.assertEqual(image(112), 0)
        self.assertNotEqual(32, 112)
        self.assertEqual((112 >> 4) & 7, 7)


if __name__ == '__main__':
    unittest.main()
