"""Bounded patch, fail-closed path checks, and cross-platform regression tests."""

from __future__ import annotations

import json
from pathlib import Path
import stat
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

from tools import apply_verso_windows_compat as compat


class VersoWindowsCompatibilityTests(unittest.TestCase):
    def test_compatibility_pin_matches_committed_dependency_manifest(self) -> None:
        manifest = json.loads((compat.ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
        verso = next(package for package in manifest["packages"] if package["name"] == "verso")
        self.assertEqual(verso["rev"], compat.VERSO_REV)
        self.assertEqual(verso["url"], compat.VERSO_URL)

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.target = self.root / compat.TARGET
        self.target.parent.mkdir(parents=True)
        self.manifest = self.root / "lake-manifest.json"
        self.manifest_data = {
            "packagesDir": ".lake/packages",
            "packages": [{
                "name": "verso", "type": "git", "subDir": None,
                "rev": compat.VERSO_REV, "url": compat.VERSO_URL,
            }],
        }
        self.manifest.write_text(json.dumps(self.manifest_data), encoding="utf-8")
        self.original = ("-- fixture\n" + compat.ORIGINAL + "\n-- end\n").encode("utf-8")
        self.target.write_bytes(self.original)

    def apply(self) -> str:
        return compat.apply_compat(self.root, platform="win32")

    def test_exact_patch_and_idempotence(self) -> None:
        self.assertEqual(self.apply(), "applied")
        expected = self.original.replace(compat.ORIGINAL.encode(), compat.PATCHED.encode(), 1)
        self.assertEqual(self.target.read_bytes(), expected)
        timestamp = self.target.stat().st_mtime_ns
        self.assertEqual(self.apply(), "already-applied")
        self.assertEqual(self.target.read_bytes(), expected)
        self.assertEqual(self.target.stat().st_mtime_ns, timestamp)

    def test_crlf_is_preserved(self) -> None:
        self.target.write_bytes(self.original.replace(b"\n", b"\r\n"))
        self.assertEqual(self.apply(), "applied")
        actual = self.target.read_bytes()
        self.assertNotIn(b"\n", actual.replace(b"\r\n", b""))
        self.assertIn(compat.PATCHED.replace("\n", "\r\n").encode(), actual)

    def test_unrelated_bytes_and_line_endings_are_preserved(self) -> None:
        before = b"-- prefix\n" + compat.ORIGINAL.replace("\n", "\r\n").encode() + b"\r\n-- suffix\n"
        self.target.write_bytes(before)
        self.assertEqual(self.apply(), "applied")
        self.assertEqual(self.target.read_bytes(), before.replace(
            compat.ORIGINAL.replace("\n", "\r\n").encode(),
            compat.PATCHED.replace("\n", "\r\n").encode(), 1))

    def test_non_windows_noop_does_not_access_repository(self) -> None:
        for platform in ("linux", "darwin"):
            with self.subTest(platform=platform):
                self.assertEqual(compat.apply_compat(self.root / "missing", platform=platform), "not-windows")
        self.assertEqual(self.target.read_bytes(), self.original)

    def test_unknown_and_ambiguous_patterns_fail_unchanged(self) -> None:
        for source in (b"-- missing declaration\n", self.original.replace(b"filterMap", b"map"),
                       self.original + self.original):
            with self.subTest(source=source[:35]):
                self.target.write_bytes(source)
                with self.assertRaises(compat.CompatibilityError):
                    self.apply()
                self.assertEqual(self.target.read_bytes(), source)

    def test_unknown_pin_or_package_location_fails_unchanged(self) -> None:
        for field, value in (("rev", "unknown"), ("url", "https://invalid.example/verso"),
                             ("subDir", "elsewhere"), ("type", "path")):
            with self.subTest(field=field):
                data = json.loads(json.dumps(self.manifest_data))
                data["packages"][0][field] = value
                self.manifest.write_text(json.dumps(data), encoding="utf-8")
                with self.assertRaises(compat.CompatibilityError):
                    self.apply()
                self.assertEqual(self.target.read_bytes(), self.original)
        data = dict(self.manifest_data, packagesDir="../outside")
        self.manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(compat.CompatibilityError):
            self.apply()
        self.assertEqual(self.target.read_bytes(), self.original)

    def test_missing_or_malformed_manifest_fails(self) -> None:
        self.manifest.unlink()
        with self.assertRaises(compat.CompatibilityError):
            self.apply()
        self.manifest.write_text("{}", encoding="utf-8")
        with self.assertRaises(compat.CompatibilityError):
            self.apply()
        self.assertEqual(self.target.read_bytes(), self.original)

    def test_missing_or_directory_target_fails(self) -> None:
        self.target.unlink()
        with self.assertRaises(compat.CompatibilityError):
            self.apply()
        self.target.mkdir()
        with self.assertRaises(compat.CompatibilityError):
            self.apply()

    def test_absolute_and_traversal_target_are_rejected(self) -> None:
        for target in (Path("../outside"), self.root):
            with self.subTest(target=target.name), mock.patch.object(compat, "TARGET", target):
                with self.assertRaises(compat.CompatibilityError):
                    self.apply()
        self.assertEqual(self.target.read_bytes(), self.original)

    def test_symlink_and_windows_reparse_metadata_are_rejected(self) -> None:
        # Simulate both modes without requiring Windows symlink privileges.
        original_lstat = Path.lstat
        for kind in ("symlink", "reparse"):
            for suspicious in (self.root, self.target.parent, self.target):
                with self.subTest(kind=kind, component=suspicious.name):
                    def simulated_lstat(path: Path):
                        real = original_lstat(path)
                        if path == suspicious:
                            return SimpleNamespace(
                                st_mode=stat.S_IFLNK if kind == "symlink" else real.st_mode,
                                st_file_attributes=0x400 if kind == "reparse" else 0,
                            )
                        return real
                    with mock.patch.object(Path, "lstat", simulated_lstat):
                        with self.assertRaisesRegex(compat.CompatibilityError, "symlink or reparse"):
                            self.apply()
                    self.assertEqual(self.target.read_bytes(), self.original)

    def test_concurrent_source_change_is_not_overwritten(self) -> None:
        original_read = Path.read_bytes
        reads = 0
        changed = b"-- concurrent edit\n"
        def changing_read(path: Path) -> bytes:
            nonlocal reads
            if path == self.target:
                reads += 1
                if reads == 2:
                    path.write_bytes(changed)
            return original_read(path)
        with mock.patch.object(Path, "read_bytes", changing_read):
            with self.assertRaisesRegex(compat.CompatibilityError, "changed during"):
                self.apply()
        self.assertEqual(self.target.read_bytes(), changed)


if __name__ == "__main__":
    unittest.main()
