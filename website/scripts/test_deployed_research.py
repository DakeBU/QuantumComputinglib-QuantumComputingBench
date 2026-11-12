"""Regression checks for the four-part, independently deployed reader gate."""
from __future__ import annotations

from copy import deepcopy
import json
import unittest
from unittest.mock import patch

from website.scripts import check_deployed_research as live
from website.scripts.research_browser_contract import ROUTES, WIDTHS, THEMES, validate_browser_report
from website.scripts.proof_inputs import proof_input_digest, lean_module_targets
from website.scripts import research_atlas as atlas


def browser_report() -> dict:
    return {
        "automated_browser_checks": [
            {"route": route, "width": width, "theme": theme,
             "math_errors": 0, "scroll_width": width}
            for route in ROUTES for width in WIDTHS for theme in THEMES
        ],
        "failures": [], "blueprint_search_required": True,
        "blueprint_search_passed": True,
    }


class BrowserCoverageTests(unittest.TestCase):
    def test_complete_matrix_passes(self):
        self.assertEqual(validate_browser_report(browser_report()), 42)

    def test_old_thirty_rows_are_not_enough(self):
        report = browser_report()
        report["automated_browser_checks"] = [r for r in report["automated_browser_checks"]
                                              if r["route"] not in ROUTES[-2:]]
        self.assertEqual(len(report["automated_browser_checks"]), 30)
        with self.assertRaisesRegex(ValueError, "incomplete"):
            validate_browser_report(report)

    def test_duplicate_cannot_replace_a_missing_route(self):
        report = browser_report()
        report["automated_browser_checks"][-1] = deepcopy(report["automated_browser_checks"][0])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate_browser_report(report)

    def test_invalid_or_missing_evidence_fails(self):
        for field, value in (("math_errors", 1), ("math_errors", None),
                             ("scroll_width", 5000), ("scroll_width", None),
                             ("route", "unknown"), ("width", 100), ("theme", "unknown")):
            with self.subTest(field=field, value=value):
                report = browser_report()
                report["automated_browser_checks"][0][field] = value
                with self.assertRaises(ValueError):
                    validate_browser_report(report)

    def test_failed_report_or_skipped_blueprint_fails(self):
        for field, value in (("failures", ["runtime error"]), ("failures", None),
                             ("automated_browser_checks", None),
                             ("blueprint_search_required", False),
                             ("blueprint_search_passed", False)):
            with self.subTest(field=field):
                report = browser_report()
                report[field] = value
                with self.assertRaises(ValueError):
                    validate_browser_report(report)


class DeployedReaderTests(unittest.TestCase):
    def setUp(self):
        self.commit = "a" * 40
        self.responses = {
            "build-report.json": {"commit": self.commit, "leanGate": {
                "passed": True, "proofInputsSha256": proof_input_digest(live.ROOT),
                "compiledModules": lean_module_targets(live.ROOT)}},
            "data/research/progress.json": {"commit": self.commit, "paper_frontier": ["fixture"]},
            "data/research/browser-report.json": browser_report(),
            "data/curriculum-parts.json": json.loads((live.ROOT / "website/curriculum-parts.json").read_text(encoding="utf-8")),
        }
        projected = atlas.public_catalog(atlas.load_catalog(live.ROOT / "website/research"))
        for name, filename in atlas.FILES.items():
            self.responses["data/research/" + filename] = projected[name]
        self.pages = []

    def fetch(self, path, commit):
        self.assertEqual(commit, self.commit)
        if path in self.responses:
            return json.dumps(self.responses[path]).encode()
        self.pages.append(path)
        labels = ["Underlying Lean Graph of Libraries", "Mathematical methods",
                  "Functor Hypergraph", "StatePreparationWiki", "Current Progress",
                  "ASPBE publication and graph protocol", "four peer parts", "Four peer textbook parts"]
        labels += [p["title"] for p in self.responses["data/curriculum-parts.json"]["parts"]]
        labels += [f["label"] for f in self.responses["data/research/atlas.json"]["families"]]
        labels += [r["title"] for r in self.responses["data/research/state-preparation-wiki.json"]["routes"]]
        return (" ".join(labels) + self.commit[:12]
                + ' data-taxonomy-nav="papers" data-taxonomy-nav="example-cases" research-nav:start').encode()

    def test_live_check_covers_home_map_and_four_parts(self):
        with patch.object(live, "fetch", side_effect=self.fetch):
            report = live.check(self.commit)
        self.assertEqual(report["browser_combinations"], 42)
        self.assertTrue(report["curriculum_parts_match"])
        self.assertTrue(report["source_author_display_projection_match"])
        self.assertTrue({"index.html", "learning/index.html", "quantum-information/index.html",
                         "quantum-scientific-computing/index.html"}.issubset(self.pages))

    def test_changed_curriculum_is_rejected(self):
        self.responses["data/curriculum-parts.json"]["parts"].pop()
        with patch.object(live, "fetch", side_effect=self.fetch):
            with self.assertRaisesRegex(ValueError, "curriculum"):
                live.check(self.commit)

    def test_live_catalog_comparison_rejects_every_source_field_tamper(self):
        key = "data/research/sources.json"
        original = deepcopy(self.responses[key])
        for field in ("id", "title", "url", "authors", "status", "anchor", "scope", "formal_status"):
            with self.subTest(field=field):
                self.responses[key] = deepcopy(original)
                self.responses[key]["sources"][0][field] = "tampered"
                with patch.object(live, "fetch", side_effect=self.fetch):
                    with self.assertRaisesRegex(ValueError, "canonical source mismatch: sources.json"):
                        live.check(self.commit)
        self.responses[key] = original

    def test_live_catalog_comparison_includes_projection_disclosure_and_all_records(self):
        key = "data/research/sources.json"
        original = deepcopy(self.responses[key])
        for mutation in (lambda value: value.pop("public_projection"),
                         lambda value: value["public_projection"].update(review_boundary="reviewed"),
                         lambda value: value["sources"].pop(),
                         lambda value: value["sources"][0].update(extra_metadata={"unexpected": True})):
            self.responses[key] = deepcopy(original)
            mutation(self.responses[key])
            with patch.object(live, "fetch", side_effect=self.fetch):
                with self.assertRaisesRegex(ValueError, "canonical source mismatch: sources.json"):
                    live.check(self.commit)
        self.responses[key] = original

    def test_live_gate_rejects_unprojected_sources_and_other_catalog_changes(self):
        projected_sources = deepcopy(self.responses["data/research/sources.json"])
        self.responses["data/research/sources.json"] = atlas.load_catalog()["sources"]
        with patch.object(live, "fetch", side_effect=self.fetch):
            with self.assertRaisesRegex(ValueError, "canonical source mismatch: sources.json"):
                live.check(self.commit)
        self.responses["data/research/sources.json"] = projected_sources
        for filename in ("atlas.json", "state-preparation-wiki.json"):
            with self.subTest(filename=filename):
                key = "data/research/" + filename
                original = deepcopy(self.responses[key])
                self.responses[key]["unexpected"] = "tampered"
                with patch.object(live, "fetch", side_effect=self.fetch):
                    with self.assertRaisesRegex(ValueError, "canonical source mismatch: " + filename):
                        live.check(self.commit)
                self.responses[key] = original

    def test_live_gate_rejects_a_forged_display_identity(self):
        sources = self.responses["data/research/sources.json"]["sources"]
        source = next(s for s in sources if s["id"] == "aspbe-local-stored-rectangular-elimination-v1")
        source["authors"] = source["authors"].replace("agent-task:root/", "agent-task:root/forged_")
        with patch.object(live, "fetch", side_effect=self.fetch):
            with self.assertRaisesRegex(ValueError, "canonical source mismatch: sources.json"):
                live.check(self.commit)

    def test_live_gate_validates_original_canonical_schema(self):
        canonical = atlas.load_catalog()
        canonical["sources"]["schema_version"] = 2
        with patch.object(atlas, "load_catalog", return_value=canonical), \
             patch.object(live, "fetch", side_effect=self.fetch):
            with self.assertRaisesRegex(ValueError, "unsupported sources schema"):
                live.check(self.commit)

    def test_missing_new_part_is_rejected(self):
        def fetch(path, commit):
            if path == "quantum-information/index.html":
                raise OSError("missing deployed page")
            return self.fetch(path, commit)
        with patch.object(live, "fetch", side_effect=fetch):
            with self.assertRaisesRegex(OSError, "missing"):
                live.check(self.commit)

    def test_wrong_commit_and_changed_proof_inputs_are_rejected(self):
        for field, value in (("commit", "b" * 40), ("proofInputsSha256", "bad")):
            with self.subTest(field=field):
                original = deepcopy(self.responses["build-report.json"])
                target = (self.responses["build-report.json"] if field == "commit"
                          else self.responses["build-report.json"]["leanGate"])
                target[field] = value
                with patch.object(live, "fetch", side_effect=self.fetch):
                    with self.assertRaises(ValueError):
                        live.check(self.commit)
                self.responses["build-report.json"] = original


if __name__ == "__main__":
    unittest.main()
