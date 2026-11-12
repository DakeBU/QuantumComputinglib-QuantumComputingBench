"""Guard explicit catalog coverage before Blueprint publication starts."""

from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
WRAPPER = runpy.run_path(str(ROOT / "scripts" / "generate-aspbe-catalog.py"))


class BlueprintCatalogTests(unittest.TestCase):
    def setUp(self):
        self.catalog = WRAPPER["load_generator"]()
        WRAPPER["register_public_modules"](self.catalog)

    def test_every_current_source_and_declaration_has_exactly_one_catalog(self):
        WRAPPER["validate_public_modules"](self.catalog)
        declarations, _ = self.catalog.collect()
        self.assertTrue(declarations)
        for declaration in declarations:
            with self.subTest(declaration=declaration.full_name):
                source = declaration.source.removeprefix("QuantumBlockEncoding/")
                owners = [(name, slug) for name, slug, sources in self.catalog.CATALOGS
                          if source in sources]
                self.assertEqual(len(owners), 1)
                self.assertEqual(self.catalog.catalog_for(declaration), owners[0])

    def test_new_reusable_and_source_specific_roots_have_intended_chapters(self):
        expected = {
            "QuantumBlockEncoding.AdjacentGivens.rotateRows": "Semantics",
            "QuantumBlockEncoding.SelectedRyTrace.selected_refines": "Semantics",
            "QuantumBlockEncoding.StoredTensorTrain.canonicalize_refines": "Semantics",
            "QuantumBlockEncoding.StoredIsometryCompletion.complete_spec": "Semantics",
            "QuantumBlockEncoding.ConstructiveHermitePreparation.prepare_spec": "PaperAndExamples",
            "QuantumBlockEncoding.HermiteBoundaryInjection.hermiteKernel_eq_sample": "PaperAndExamples",
        }
        declarations, _ = self.catalog.collect()
        actual = {declaration.full_name: self.catalog.catalog_for(declaration)[0]
                  for declaration in declarations}
        for name, chapter in expected.items():
            with self.subTest(name=name):
                self.assertEqual(actual[name], chapter)

    def test_lean_433_statement_anchor_matches_inspected_renderer(self):
        declarations, _ = self.catalog.collect()
        declaration = next(decl for decl in declarations if decl.full_name ==
                           "QuantumBlockEncoding.ConstructiveHermitePreparation.prepare_spec")
        self.assertEqual(
            self.catalog.blueprint_declaration_url(declaration, "catalog-paper-and-examples"),
            "../blueprint/html-multi/catalog-paper-and-examples/"
            "QuantumBlockEncoding___ConstructiveHermitePreparation___lean/"
            "#--informal-preview-_FLQQ_QuantumBlockEncoding___ConstructiveHermitePreparation"
            "___prepare_spec_FLQQ_--statement",
        )

    def test_no_preview_mode_emits_official_page_runtime(self):
        source = (ROOT / "ABEISBlueprintMain.lean").read_text(encoding="utf-8")
        self.assertIn("Informal.PreviewManifest.writeBlueprintRuntimeModules", source)
        self.assertIn("(extraSteps := [emitPageRuntime])", source)
        self.assertIn('| .multi => "html-multi"', source)
        self.assertIn('| .single => "html-single"', source)

    def test_missing_mapping_fails_closed_with_relative_module_name(self):
        for _name, _slug, sources in self.catalog.CATALOGS:
            sources.discard("AdjacentGivens.lean")
        with self.assertRaisesRegex(ValueError, "unassigned module: AdjacentGivens.lean"):
            WRAPPER["validate_public_modules"](self.catalog)

    def test_duplicate_mapping_is_not_silently_first_match(self):
        self.catalog.CATALOGS[0][2].add("AdjacentGivens.lean")
        with self.assertRaisesRegex(ValueError, "module assigned more than once: AdjacentGivens.lean"):
            WRAPPER["validate_public_modules"](self.catalog)

    def test_stale_mapping_fails_closed(self):
        self.catalog.CATALOGS[0][2].add("NoSuchCatalogModule.lean")
        with self.assertRaisesRegex(ValueError, "catalog module does not exist: NoSuchCatalogModule.lean"):
            WRAPPER["validate_public_modules"](self.catalog)

    def test_even_an_empty_new_module_requires_explicit_review(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for _name, _slug, sources in self.catalog.CATALOGS:
                for source in sources:
                    path = root / source
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.touch()
            (root / "UnclassifiedEmpty.lean").touch()
            with patch.object(self.catalog, "SOURCE_ROOT", root):
                with self.assertRaisesRegex(ValueError, "unassigned module: UnclassifiedEmpty.lean"):
                    WRAPPER["validate_public_modules"](self.catalog)

    def test_registration_is_idempotent_and_validates_before_generation(self):
        before = [(name, slug, frozenset(sources)) for name, slug, sources in self.catalog.CATALOGS]
        WRAPPER["register_public_modules"](self.catalog)
        self.assertEqual(before,
                         [(name, slug, frozenset(sources)) for name, slug, sources in self.catalog.CATALOGS])
        for _name, _slug, sources in self.catalog.CATALOGS:
            sources.discard("Core.lean")
        with patch.object(self.catalog, "generate") as generate:
            with self.assertRaisesRegex(ValueError, "unassigned module: Core.lean"):
                WRAPPER["register_public_modules"](self.catalog)
            generate.assert_not_called()

    def test_publication_entrypoints_run_catalog_regression_tests(self):
        for filename, command in [
            ("scripts/build-all.sh", "python3 -m unittest tools.test_blueprint_catalog"),
            ("scripts/build-all.ps1", "& $PythonCommand -m unittest tools.test_blueprint_catalog"),
            (".github/workflows/pages.yml", "python3 -m unittest tools.test_blueprint_catalog"),
        ]:
            with self.subTest(filename=filename):
                text = (ROOT / filename).read_text(encoding="utf-8")
                self.assertIn(command, text)
                generator = ("& $PythonCommand" if filename.endswith(".ps1") else "python3")
                self.assertLess(text.index(command),
                                text.index(generator + " scripts/generate-aspbe-catalog.py"))


if __name__ == "__main__":
    unittest.main()
