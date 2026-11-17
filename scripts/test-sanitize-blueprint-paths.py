#!/usr/bin/env python3
"""Regression tests for portable Blueprint publication paths."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path, PurePosixPath, PureWindowsPath


SCRIPT = Path(__file__).with_name("sanitize-blueprint-paths.py")
SPEC = importlib.util.spec_from_file_location("sanitize_blueprint_paths", SCRIPT)
assert SPEC and SPEC.loader
SANITIZER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SANITIZER)

# Artificial source locations: both spellings are tested on every host.
# These are string-processing fixtures, never filesystem destinations.
WINDOWS_SOURCE_ROOT = PureWindowsPath("Z:/Users/fixture/ABEIS")
POSIX_SOURCE_ROOT = PurePosixPath("/home/fixture/ABEIS")


class SanitizerTests(unittest.TestCase):
    def _find_page(self, inline: str) -> str:
        return (
            '<!doctype html><html><head><script>\n      window.xref = '
            + inline + SANITIZER.FIND_XREF_DRIVER_PREFIX
            + 'let params = new URLSearchParams(document.location.search);\n'
            + '</script></head><body>Search the theorem library.</body></html>'
        )

    def _inline_value(self, page: str):
        start = SANITIZER.FIND_XREF_ASSIGNMENT_RE.search(page).end()
        end = page.index(SANITIZER.FIND_XREF_DRIVER_PREFIX)
        return json.loads(page[start:end])

    def test_xref_without_source_paths_is_already_safe(self) -> None:
        value, changed, seen = SANITIZER._normalize_source_paths(
            {"declarations": []}, Path.cwd().resolve()
        )
        self.assertEqual(value, {"declarations": []})
        self.assertEqual(changed, 0)
        self.assertEqual(seen, 0)

    def test_repository_path_becomes_portable(self) -> None:
        root = Path.cwd().resolve()
        source = root / "QuantumBlockEncoding" / "Core.lean"
        value, changed, seen = SANITIZER._normalize_source_paths(
            {"sourcePath": str(source)}, root
        )
        self.assertEqual(value["sourcePath"], "QuantumBlockEncoding/Core.lean")
        self.assertEqual(changed, 1)
        self.assertEqual(seen, 1)

    def test_outside_absolute_path_is_rejected(self) -> None:
        root = Path.cwd().resolve()
        with self.assertRaises(ValueError):
            SANITIZER._normalize_source_paths(
                {"sourcePath": str(root.parent / "outside.lean")}, root
            )

    def test_embedded_json_paths_are_scrubbed(self) -> None:
        for root in (WINDOWS_SOURCE_ROOT, POSIX_SOURCE_ROOT):
            with self.subTest(path_flavor=type(root).__name__):
                value, changed = SANITIZER._scrub_json_strings(
                    {
                        "sourceHref": str(root / "QuantumBlockEncoding" / "Core.lean"),
                        "html": (
                            '<a href="'
                            + str(root.parent / "external" / "Core.lean")
                            + '">source</a>'
                        ),
                    },
                    root,
                )
                self.assertGreaterEqual(changed, 2)
                self.assertEqual(
                    value["sourceHref"], "QuantumBlockEncoding/Core.lean"
                )
                self.assertIn("external-source", value["html"])
                self.assertNotIn(str(root), str(value))

    def test_mathematical_colon_backslash_is_preserved(self) -> None:
        text = r"the set \{x:\mathcal V(x)=1\}"
        scrubbed, changed = SANITIZER._scrub_local_paths_from_text(
            text, Path.cwd().resolve()
        )
        self.assertEqual(scrubbed, text)
        self.assertEqual(changed, 0)

    def test_publication_scan_rejects_derived_repository_path(self) -> None:
        root = Path.cwd().resolve()
        with tempfile.TemporaryDirectory(dir=root) as temporary:
            output = Path(temporary)
            (output / "safe.html").write_text(
                '<a href="https://example.org/library/">safe URL</a>',
                encoding="utf-8",
            )
            self.assertEqual(
                SANITIZER._assert_no_local_paths(output, root), 1
            )
            (output / "unsafe.json").write_text(
                '{"path": "' + str(root).replace("\\", "/") + '/source.lean"}',
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                SANITIZER._assert_no_local_paths(output, root)

    def test_publication_scan_allows_mathjax_control_protocol(self) -> None:
        root = Path.cwd().resolve()
        with tempfile.TemporaryDirectory(dir=root) as temporary:
            output = Path(temporary)
            (output / "formula.html").write_text(
                r'<div class="math-block">\[I:\quad\mathrm{toggle};C(U)\]</div>',
                encoding="utf-8",
            )
            self.assertEqual(
                SANITIZER._assert_no_local_paths(output, root), 1
            )

    def test_inline_xref_preserves_every_entry_html_and_source_anchor(self) -> None:
        # This regression needs JSON-escaped Windows separators even on Linux.
        root = WINDOWS_SOURCE_ROOT
        source = str(root / "QuantumBlockEncoding" / "Core.lean")
        url = "https://github.com/DakeBU/Quantum-Computing-Block-Encoding/blob/abc123/" + source + "#L14-L16"
        original = {"Lean": {"contents": {
            "first": [{"sourceHref": url, "html": '<a href="' + url + '">theorem & proof</a>'}],
            "second": [{"statement": r"f : X → Y", "proof": "by\n  exact h"}],
        }}}
        normalized, _ = SANITIZER._scrub_json_strings(original, root)
        expected_url = "https://github.com/DakeBU/Quantum-Computing-Block-Encoding/blob/abc123/QuantumBlockEncoding/Core.lean#L14-L16"
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            page = output / "index.html"
            serialized = json.dumps(original)
            self.assertIn(r"Z:\\Users\\fixture\\ABEIS", serialized)
            before = self._find_page(serialized)
            # Reproduce the old raw-text pass before the fail-closed scan.
            before, _ = SANITIZER._scrub_local_paths_from_text(before, root)
            page.write_text(before, encoding="utf-8")
            with self.assertRaises(ValueError):
                SANITIZER._assert_no_local_paths(output, root)
            changed, _ = SANITIZER._rewrite_find_xref(page, normalized, root)
            self.assertEqual(changed, 1)
            rewritten = page.read_text(encoding="utf-8")
            self.assertEqual(self._inline_value(rewritten), normalized)
            self.assertEqual(normalized["Lean"]["contents"]["first"][0]["sourceHref"], expected_url)
            self.assertEqual(normalized["Lean"]["contents"]["first"][0]["html"], '<a href="' + expected_url + '">theorem & proof</a>')
            self.assertEqual(normalized["Lean"]["contents"]["second"], original["Lean"]["contents"]["second"])
            self.assertTrue(rewritten.endswith(before[before.index(SANITIZER.FIND_XREF_DRIVER_PREFIX):]))
            self.assertEqual(SANITIZER._assert_no_local_paths(output, root), 1)
            self.assertEqual(SANITIZER._rewrite_find_xref(page, normalized, root), (0, 0))

    def test_inline_xref_posix_source_preserves_links_and_cached_html(self) -> None:
        root = POSIX_SOURCE_ROOT
        source = str(root / "QuantumBlockEncoding" / "Core.lean")
        prefix = "https://github.com/DakeBU/Quantum-Computing-Block-Encoding/blob/abc123/"
        url = prefix + source + "#L14-L16"
        original = {"sourceHref": url, "html": '<a href="' + url + '">theorem & proof</a>'}
        normalized, _ = SANITIZER._scrub_json_strings(original, root)
        expected_url = prefix + "QuantumBlockEncoding/Core.lean#L14-L16"
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            page = output / "index.html"
            before, _ = SANITIZER._scrub_local_paths_from_text(
                self._find_page(json.dumps(original)), root
            )
            page.write_text(before, encoding="utf-8")
            # Unlike the Windows regression, POSIX roots were removed by the
            # old pass. A local-path scan should accept this spelling on all OSes.
            self.assertEqual(SANITIZER._assert_no_local_paths(output, root), 1)
            SANITIZER._rewrite_find_xref(page, normalized, root)
            rewritten = page.read_text(encoding="utf-8")
            self.assertEqual(self._inline_value(rewritten), {
                "sourceHref": expected_url,
                "html": '<a href="' + expected_url + '">theorem & proof</a>',
            })
            self.assertEqual(SANITIZER._assert_no_local_paths(output, root), 1)

    def test_inline_xref_repairs_previously_corrupted_json_from_canonical_data(self) -> None:
        root = Path.cwd().resolve()
        normalized = {"entries": [{"html": '<a href="https://example.org/Core.lean#L1-L2">proof</a>'}]}
        # Shape left by the previous URL regex: a JSON-escaped attribute quote
        # became a path separator. The canonical xref remains valid JSON.
        damaged = '{"entries":[{"html":"<a href=\\"https://example.org/Core.lean#L1-L2/">proof</a>"}]}'
        with self.assertRaises(json.JSONDecodeError):
            json.loads(damaged)
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / "index.html"
            page.write_text(self._find_page(damaged), encoding="utf-8")
            SANITIZER._rewrite_find_xref(page, normalized, root)
            self.assertEqual(self._inline_value(page.read_text(encoding="utf-8")), normalized)

    def test_inline_serialization_cannot_terminate_script_and_roundtrips_html(self) -> None:
        value = {"html": '</script><script>alert("not executable")</script><!-- & >',
                 "text": "line\u2028paragraph\u2029end", "entries": [1, 2, 3]}
        serialized = SANITIZER._script_safe_json(value)
        for character in ("<", ">", "&", "\u2028", "\u2029"):
            self.assertNotIn(character, serialized)
        self.assertEqual(json.loads(serialized), value)

    def test_unknown_inline_layout_fails_without_modification(self) -> None:
        root = Path.cwd().resolve()
        valid = self._find_page("{}")
        for text in ("<html>no inline data</html>", valid + valid,
                     valid.replace("// @ts-check", "// unexpected driver")):
            with self.subTest(prefix=text[:25]), tempfile.TemporaryDirectory() as temporary:
                page = Path(temporary) / "index.html"
                page.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    SANITIZER._rewrite_find_xref(page, {}, root)
                self.assertEqual(page.read_text(encoding="utf-8"), text)

    def test_missing_inline_page_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(FileNotFoundError):
                SANITIZER._rewrite_find_xref(Path(temporary) / "missing.html", {}, Path.cwd())


if __name__ == "__main__":
    unittest.main()
