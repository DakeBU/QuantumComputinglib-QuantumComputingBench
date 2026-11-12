"""Keep formal-memory version claims aligned with the active toolchain."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import check_technical_lemma_registry as registry


class TechnicalLemmaRegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "lean-toolchain").write_text("leanprover/lean4:v4.33.0\n", encoding="utf-8")
        (self.root / "Leaf.lean").write_text("theorem leaf : True := True.intro\n", encoding="utf-8")
        self.path = self.root / "registry.json"

    def check(self, version):
        entry = {field: [] for field in registry.REQUIRED_FIELDS}
        entry.update(id="leaf", theorem="leaf", fully_qualified_name="leaf",
                     source_file="Leaf.lean", verification_status="compiled",
                     local_declaration_status="complete", lean_version=version)
        self.path.write_text(json.dumps({"entries": [entry]}), encoding="utf-8")
        with patch.object(registry, "ROOT", self.root), patch.object(registry, "REGISTRY", self.path), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return registry.main()

    def test_current_version_is_accepted(self):
        self.assertEqual(self.check("4.33.0"), 0)

    def test_old_compiled_version_cannot_receive_green_status(self):
        self.assertEqual(self.check("4.29.1"), 1)

    def test_unpinned_toolchain_is_rejected(self):
        (self.root / "lean-toolchain").write_text("leanprover/lean4:nightly\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "pinned Lean"):
            registry.pinned_lean_version(self.root)


if __name__ == "__main__":
    unittest.main()
