"""Exercise real Git checkout transport without changing the trusted checker."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from website.scripts.check_research_publications import binding_digest, validate_record


ROOT = Path(__file__).resolve().parents[2]


class PublicationByteTransportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="publication-transport-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        self.root.mkdir()
        self.record = {"module": "QuantumBlockEncoding/ThinLQ.lean",
                       "lesson_path": "docs/lessons/pilot.md", "source_id": "pilot"}
        self.files = {
            ".gitattributes": (ROOT / ".gitattributes").read_bytes(),
            "QuantumBlockEncoding/ThinLQ.lean": b"-- fixture, not a certificate\n",
            "QuantumBlockEncoding/Nested/Helper.lean": b"-- ambient nested\n",
            "ABEISTests/Nested/Helper.lean": b"-- ambient test\n",
            "lean-toolchain": b"leanprover/lean4:v4.33.0\n",
            "lake-manifest.json": b"{}\n",
            "lakefile.lean": b"-- mixed frozen configuration fixture\r\nimport Lake\n",
            "website/scripts/check_research_publications.py":
                b"# transport fixture, not the real verifier\r\n",
            "docs/lessons/pilot.md": b"Local fixture.\n",
            # A historical independently hashed packet must stay CRLF.
            "reviews/publication/historical/evidence.json": b'{"prior": true}\r\n',
            "reviews/publication/new/evidence.json": b'{"fresh": true}\n',
            "experiments/hermite-polynomial/precision/frozen.lean":
                b"-- frozen experimental fixture, not a certificate\r\n",
            "experiments/hermite-polynomial/precision/result.json":
                b'{"historical": true}\r\n',
            "failure-memory/frozen.json": b'{"historicalFailure": true}\r\n',
            "reports/lean-433-migration/fixture.json":
                b'{"fixture": "not an acceptance record"}\r\n',
            "reports/lean-433-migration/fixture-context.md":
                b"Frozen explanatory context fixture.\r\n",
            "website/research/sources.json": json.dumps({"sources": [
                {"id": "pilot", "status": "primary-text-checked"}]}).encode(),
        }
        for name, data in self.files.items():
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        self.git(self.root, "init", "-q")
        self.git(self.root, "config", "core.autocrlf", "true")
        self.git(self.root, "add", ".")
        self.git(self.root, "-c", "user.name=Transport fixture",
                 "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture")

    @staticmethod
    def git(root, *args):
        return subprocess.run(["git", *args], cwd=root, check=True,
                              capture_output=True).stdout

    def test_actual_git_checkouts_keep_bound_and_review_bytes(self):
        expected = binding_digest(self.root, self.record)
        for autocrlf in ("true", "false", "input"):
            with self.subTest(autocrlf=autocrlf):
                dest = Path(self.temp.name) / ("checkout-" + autocrlf)
                self.git(Path(self.temp.name), "clone", "-q", "--no-checkout",
                         str(self.root), str(dest))
                self.git(dest, "config", "core.autocrlf", autocrlf)
                self.git(dest, "checkout", "-q", "HEAD")
                self.assertEqual(expected, binding_digest(dest, self.record))
                for name, data in self.files.items():
                    if name.startswith(("QuantumBlockEncoding/", "ABEISTests/",
                                        "docs/lessons/", "reviews/publication/",
                                        "experiments/", "failure-memory/",
                                        "reports/lean-433-migration/")) or name in (
                                            "lean-toolchain", "lake-manifest.json",
                                            "lakefile.lean",
                                            "website/scripts/check_research_publications.py"):
                        self.assertEqual(data, (dest / name).read_bytes(), name)

    def test_raw_checker_still_rejects_ambient_byte_drift(self):
        expected = binding_digest(self.root, self.record)
        ambient = self.root / "ABEISTests/Nested/Helper.lean"
        ambient.write_bytes(ambient.read_bytes().replace(b"\n", b"\r\n"))
        self.assertNotEqual(expected, binding_digest(self.root, self.record))

    def test_missing_bound_file_still_fails_closed(self):
        (self.root / "lean-toolchain").unlink()
        with self.assertRaises(ValueError):
            binding_digest(self.root, self.record)

    def test_actual_c25_runtime_inputs_keep_original_raw_bytes(self):
        """No normalization exception or rewritten frozen report is allowed."""
        packet = ROOT / "reviews/publication/finite-real-tensor-train/final-review-inputs-c25.json"
        self.assertTrue(packet.is_file())
        frozen = json.loads(packet.read_text(encoding="utf-8"))["input_sha256"]
        names = ("lakefile.lean", "website/scripts/check_research_publications.py",
                 "reports/lean-433-migration/c25-cf77-context.md")
        import hashlib
        before = {name: (ROOT / name).read_bytes() for name in names}
        for name, raw in before.items():
            self.assertEqual(hashlib.sha256(raw).hexdigest(), frozen[name])
        projection = Path(self.temp.name) / "actual-runtime-projection"
        projection.mkdir()
        files = {".gitattributes": (ROOT / ".gitattributes").read_bytes(), **before}
        for name, raw in files.items():
            target = projection / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        self.git(projection, "init", "-q")
        self.git(projection, "config", "core.autocrlf", "true")
        self.git(projection, "add", ".")
        self.git(projection, "-c", "user.name=Transport fixture",
                 "-c", "user.email=fixture@example.invalid", "commit", "-qm", "runtime projection")
        for autocrlf in ("true", "false", "input"):
            with self.subTest(runtime_autocrlf=autocrlf):
                dest = Path(self.temp.name) / ("runtime-" + autocrlf)
                self.git(Path(self.temp.name), "clone", "-q", "--no-checkout", str(projection), str(dest))
                self.git(dest, "config", "core.autocrlf", autocrlf)
                self.git(dest, "checkout", "-q", "HEAD")
                for name, raw in before.items():
                    self.assertEqual(raw, (dest / name).read_bytes(), name)
        for name, raw in before.items():
            self.assertEqual(raw, (ROOT / name).read_bytes())

    def test_current_thin_lq_frozen_context_round_trip(self):
        """Check the actual complete bound tree, not only the small fixture."""
        candidate = ROOT / "reviews/publication/thin-lq-lf/publication-candidate.json"
        self.assertTrue(candidate.is_file(), "required ThinLQ LF pilot is missing")
        frozen = json.loads(candidate.read_text(encoding="utf-8"))
        records = json.loads((ROOT / "website/research/publications.json").read_bytes())["records"]
        selected = [row for row in records if row["module"] == frozen["module"]]
        self.assertEqual(len(selected), 1, "one current reviewed ThinLQ record is required")
        record = selected[0]
        for key in ("module", "source_id", "source_statement", "source_anchor", "lesson_path",
                    "declarations", "obligation_map", "assumption_deltas", "graph_contribution",
                    "formalizer", "residual_boundary"):
            self.assertEqual(record[key], frozen[key], key)
        inventory = {row["fullName"]: row for row in json.loads(
            (ROOT / "web/library/declarations.json").read_bytes())["declarations"]}
        # Select an actually reviewed current record, never rehash an old one.
        validate_record(ROOT, record, inventory)
        expected = binding_digest(ROOT, record)
        self.assertEqual(record["binding_sha256"], expected)
        names = {".gitattributes", record["module"], record["lesson_path"],
                 "lean-toolchain", "lake-manifest.json", "website/research/sources.json"}
        for directory in ("QuantumBlockEncoding", "ABEISTests"):
            names.update(p.relative_to(ROOT).as_posix()
                         for p in (ROOT / directory).rglob("*.lean"))
        # Preserve genuine historical and newly exported packets alike.
        names.update(p.relative_to(ROOT).as_posix() for p in
                     (ROOT / "reviews/publication/thin-lq").glob("*.json"))
        names.update(p.relative_to(ROOT).as_posix() for p in
                     (ROOT / "reviews/publication/thin-lq-lf").glob("*.json"))
        for key in ("decoder_evidence", "reviewer_evidence"):
            names.add(record[key])
            role = json.loads((ROOT / record[key]).read_bytes())
            names.update((role["packet_path"], role["artifact_path"]))
        projection = Path(self.temp.name) / "current-projection"
        projection.mkdir()
        before = {name: (ROOT / name).read_bytes() for name in names}
        for name, data in before.items():
            target = projection / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        self.git(projection, "init", "-q")
        self.git(projection, "config", "core.autocrlf", "true")
        self.git(projection, "add", ".")
        self.git(projection, "-c", "user.name=Transport fixture",
                 "-c", "user.email=fixture@example.invalid", "commit", "-qm", "projection")
        for autocrlf in ("true", "false", "input"):
            with self.subTest(current_autocrlf=autocrlf):
                dest = Path(self.temp.name) / ("current-" + autocrlf)
                self.git(Path(self.temp.name), "clone", "-q", "--no-checkout",
                         str(projection), str(dest))
                self.git(dest, "config", "core.autocrlf", autocrlf)
                self.git(dest, "checkout", "-q", "HEAD")
                self.assertEqual(expected, binding_digest(dest, record))
                validate_record(dest, record, inventory)
                for name in names:
                    if name.startswith("reviews/publication/"):
                        self.assertEqual(before[name], (dest / name).read_bytes(), name)
        for name, data in before.items():
            self.assertEqual(data, (ROOT / name).read_bytes(),
                             "live frozen context changed during test: " + name)

    def test_original_thin_lq_frozen_epoch_remains_replayable_without_rehash(self):
        """Replay immutable predecessor bytes, not a projection of the new tree."""
        import hashlib
        import zipfile
        fixture = ROOT / "reviews/publication/paired-kernel-c46/thin-lq-original-bound-epoch-c47.zip"
        self.assertEqual(hashlib.sha256(fixture.read_bytes()).hexdigest(),
                         "ac8cccd9520498ebaa5efd2be6a31517d8fad49ec17ba0f99768494a194d1b03")
        dest = Path(self.temp.name) / "original-thin-lq-epoch"
        dest.mkdir()
        with zipfile.ZipFile(fixture) as archive:
            for name in archive.namelist():
                target = dest / name
                self.assertTrue(target.resolve().is_relative_to(dest.resolve()))
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(name))
        candidate = "reviews/publication/thin-lq-lf/publication-candidate.json"
        self.assertEqual((ROOT / candidate).read_bytes(), (dest / candidate).read_bytes())
        frozen = json.loads((dest / candidate).read_bytes())
        self.assertEqual(frozen["binding_sha256"], binding_digest(dest, frozen))
        # The kernel proof successor must not make the historical packet fresh.
        self.assertNotEqual(frozen["binding_sha256"], binding_digest(ROOT, frozen))


if __name__ == "__main__":
    unittest.main()
