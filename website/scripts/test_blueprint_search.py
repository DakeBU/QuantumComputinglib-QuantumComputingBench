import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from website.scripts.augment_blueprint_search import (
    ADAPTER, BEGIN, DOMAIN, PREFIX, SEARCH_IMPORT, SEARCH_IMPORT_433, SearchContractError,
    augment, declaration_entries,
)


NAME = "QuantumBlockEncoding.HermiteStatePreparation.hermiteStatePreparation_complete"


class BlueprintSearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "-verso-search").mkdir()
        (self.root / "catalog").mkdir()
        self.entry = {"address": "/catalog/", "id": "hermite-root", "data": {"target": NAME}}
        self.xref = {DOMAIN: {"contents": {PREFIX + NAME: [self.entry]}}}
        self.write_xref()
        self.write("catalog/index.html", '<article id="hermite-root">Exact declaration</article>')
        self.write("-verso-search/domain-mappers.js", "export const domainMappers = {};\n")
        self.write("-verso-search/search-init.js", SEARCH_IMPORT + "\nregisterSearch({ searchWrapper, data, domainMappers });")
        self.write("-verso-search/search-box.js", "domainMappers[key].dataToSearchables(value)")

    def write(self, relative, text):
        (self.root / relative).write_text(text, encoding="utf-8")

    def write_xref(self):
        self.write("xref.json", json.dumps(self.xref, ensure_ascii=False))

    def test_exact_target_and_anchor_idempotent_check(self):
        self.assertEqual(augment(self.root), 1)
        before = (self.root / "-verso-search" / ADAPTER).read_bytes()
        self.assertIn(NAME.encode(), before)
        self.assertIn(b"/catalog/#hermite-root", before)
        self.assertEqual(augment(self.root, check=True), 1)
        self.assertEqual(augment(self.root), 1)
        self.assertEqual(before, (self.root / "-verso-search" / ADAPTER).read_bytes())
        self.assertNotIn(b"\r", before)
        self.assertEqual((self.root / "-verso-search/domain-mappers.js").read_text().count(BEGIN), 1)

    def test_lean_433_priority_aware_search_is_preserved(self):
        init = (SEARCH_IMPORT_433 + "\nregisterSearch({\n"
                "  searchWrapper, data, domainMappers, searchPriorities,\n"
                "  docPriorities, searchPagePath,\n});")
        self.write("-verso-search/search-init.js", init)
        self.assertEqual(augment(self.root), 1)
        self.assertEqual(augment(self.root, check=True), 1)
        self.assertEqual((self.root / "-verso-search/search-init.js").read_text(), init)

    def test_unknown_or_mismatched_search_initialization_fails_before_write(self):
        for init in (
            SEARCH_IMPORT_433 + "\nregisterSearch({searchWrapper,data,domainMappers});",
            SEARCH_IMPORT + "\nregisterSearch({searchWrapper,data,domainMappers,unknown});",
            SEARCH_IMPORT + "\n" + SEARCH_IMPORT + "\nregisterSearch({searchWrapper,data,domainMappers});",
            SEARCH_IMPORT + "\nregisterSearch({searchWrapper,data,domainMappers});\nregisterSearch({other});",
        ):
            with self.subTest(init=init):
                self.write("-verso-search/search-init.js", init)
                with self.assertRaisesRegex(SearchContractError, "initialization contract"):
                    augment(self.root)
                self.assertFalse((self.root / "-verso-search" / ADAPTER).exists())

    def test_duplicate_renderings_and_other_domains_do_not_duplicate_results(self):
        self.xref[DOMAIN]["contents"][PREFIX + NAME].append(dict(self.entry))
        self.xref["«Informal.Block.informal»"] = {"contents": {NAME: [self.entry]}}
        self.assertEqual(len(declaration_entries(self.root, self.xref)), 1)

    def test_missing_inputs_fail_before_write(self):
        for name in ["xref.json", "-verso-search/domain-mappers.js", "-verso-search/search-init.js", "-verso-search/search-box.js", "catalog/index.html"]:
            with self.subTest(name=name):
                file = self.root / name
                before = file.read_bytes()
                file.unlink()
                with self.assertRaises(SearchContractError):
                    augment(self.root)
                file.write_bytes(before)
                self.assertFalse((self.root / "-verso-search" / ADAPTER).exists())

    def test_empty_or_unknown_domain_fails(self):
        for xref in [{}, {DOMAIN: {"contents": {}}}, {DOMAIN: []}]:
            with self.subTest(xref=xref), self.assertRaises(SearchContractError):
                declaration_entries(self.root, xref)

    def test_missing_anchor_and_changed_target_fail(self):
        for field, value in [("id", "absent"), ("data", {"target": "Different.name"})]:
            old = self.entry[field]
            self.entry[field] = value
            with self.subTest(field=field), self.assertRaises(SearchContractError):
                declaration_entries(self.root, self.xref)
            self.entry[field] = old

    def test_escaping_and_machine_addresses_fail(self):
        for address in ["../private/", "/../private/", "/%2e%2e/private/", "//host/private/", "Z:/private/", "/Z:/private/", "/catalog\\private/", "/catalog/?query"]:
            self.entry["address"] = address
            with self.subTest(address=address), self.assertRaises(SearchContractError):
                declaration_entries(self.root, self.xref)

    def test_check_rejects_missing_tampered_or_stale_adapter(self):
        with self.assertRaises(SearchContractError):
            augment(self.root, check=True)
        augment(self.root)
        self.write("-verso-search/" + ADAPTER, "forged")
        with self.assertRaises(SearchContractError):
            augment(self.root, check=True)
        augment(self.root)
        self.entry["id"] = "new-anchor"
        self.write_xref()
        self.write("catalog/index.html", '<article id="new-anchor"></article>')
        with self.assertRaises(SearchContractError):
            augment(self.root, check=True)

    def test_upstream_shape_change_fails_closed(self):
        self.write("-verso-search/domain-mappers.js", "export default {};\n")
        with self.assertRaises(SearchContractError):
            augment(self.root)

    def test_required_hermite_root_cannot_silently_disappear(self):
        self.entry["data"]["target"] = "QuantumBlockEncoding.Other.name"
        self.xref[DOMAIN]["contents"] = {PREFIX + "QuantumBlockEncoding.Other.name": [self.entry]}
        self.write_xref()
        with self.assertRaisesRegex(SearchContractError, "Required Hermite root"):
            augment(self.root)

    def test_truncated_adapter_marker_fails(self):
        self.write("-verso-search/domain-mappers.js", "export const domainMappers = {};\n" + BEGIN)
        with self.assertRaises(SearchContractError):
            augment(self.root)

    def test_redirected_output_parent_fails_before_write(self):
        original_resolve = Path.resolve
        search_dir = self.root / "-verso-search"

        def resolve(file, *args, **kwargs):
            if file == search_dir:
                return self.root.parent / "outside-blueprint-output"
            return original_resolve(file, *args, **kwargs)

        with patch.object(Path, "resolve", resolve):
            with self.assertRaisesRegex(SearchContractError, "output parent escapes"):
                augment(self.root)
        self.assertFalse((search_dir / ADAPTER).exists())


if __name__ == "__main__":
    unittest.main()
