"""Focused reader regressions; mocked qualification is not execution evidence.

Use the actual committed questions/gold, without starting Lean/models or writing
to any benchmark evidence. Full builds and browser checks belong to integration.
"""
import sys
import tempfile
import unittest
from copy import deepcopy
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "benchmarks/quantumcomputingbench/src"))

import qcb_learning_reference as reference
import qcb_learning_validity as validity
from qcb_core import digest, read_json

from website.scripts import quantumcomputingbench as reader


class DisclosureParser(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.open_disclosures = []
        self.outside = []
        self.links = []
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "details":
            self.depth += 1
            if "open" in values:
                self.open_disclosures.append(values)
        if tag == "a":
            self.links.append(values.get("href", ""))

    def handle_endtag(self, tag):
        if tag == "details":
            self.depth -= 1

    def handle_data(self, data):
        if not self.depth:
            self.outside.append(data)


def qualifying_fixture(packet):
    """Routing fixture, never an actual reference or semantic certificate."""
    return {"status": "PUBLIC_SEMANTIC_REFERENCE_PILOT_QUALIFIED", "cohort_digest": digest(packet),
            "reference_receipt_digest": digest("SOFTWARE MOCK RECEIPT; not actual Lean"),
            "formal_coverage": "decision_polarity_only", "actual_model_performance_measured": False,
            "learning_gain": None, "hidden_holdout": False, "canonical_admissions_changed": False,
            "reference_replay_count": 38}


class DiagnosticReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = read_json(validity.COHORT)
        cls.qualification = qualifying_fixture(cls.packet)
        cls.commit = "ab" * 20

    def render(self, packet=None):
        packet = self.packet if packet is None else packet
        pages = {}

        def write(route, title, body, description):
            pages[route + "index.html"] = {"title": title, "body": body, "description": description}

        def intro(title, subtitle):
            return '<div class="qcb-reader"><h1>' + reader.esc(title) + '</h1>' + reader.prose(subtitle)

        manifest = reader.publish_diagnostics(write, intro, packet, qualifying_fixture(packet), self.commit)
        return pages, manifest

    def test_reader_calls_actual_qualifier_and_fails_when_receipt_missing(self):
        def missing_receipt(path):
            if Path(path) == validity.COHORT:
                return deepcopy(self.packet)
            raise FileNotFoundError("missing actual reference-checks.json")

        with patch.object(validity, "load_cohort", return_value=(self.packet, {})), \
                patch.object(reference, "check_semantics", return_value={"software_mock": True}), \
                patch.object(reference, "read_json", side_effect=missing_receipt), \
                self.assertRaisesRegex(FileNotFoundError, "reference-checks"):
            reader.diagnostic_reader()

    def test_stale_receipt_is_not_replaced_by_authored_questions_or_old_course(self):
        def stale_receipt(path):
            if Path(path) == validity.COHORT:
                return deepcopy(self.packet)
            return {"schema_version": "qcb.learning_validity_references.v1", "cohort_digest": digest("stale cohort")}

        with patch.object(validity, "load_cohort", return_value=(self.packet, {})), \
                patch.object(reference, "check_semantics", return_value={"software_mock": True}), \
                patch.object(reference, "read_json", side_effect=stale_receipt), \
                self.assertRaisesRegex(ValueError, "checkpoint scope or cohort binding"):
            reader.diagnostic_reader()

    def test_qualification_is_rechecked_instead_of_cached(self):
        with patch.object(validity, "load_cohort", return_value=(self.packet, {})), \
                patch.object(reference, "qualify", side_effect=[self.qualification, ValueError("receipt drift")]) as qualify:
            self.assertEqual(reader.diagnostic_reader()[0], self.packet)
            with self.assertRaisesRegex(ValueError, "receipt drift"):
                reader.diagnostic_reader()
            self.assertEqual(qualify.call_count, 2)

    def test_missing_qualification_aborts_publisher_before_output_mutations(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            with patch.object(reader, "load_catalog", return_value=({"cores": []}, {}, {})), \
                    patch.object(reader, "course_reader", return_value=({}, {}, {})), \
                    patch.object(reader, "diagnostic_reader", side_effect=ValueError("no qualified actual receipt")), \
                    self.assertRaisesRegex(ValueError, "actual receipt"):
                reader.publish(output)
            self.assertEqual(list(output.iterdir()), [])

    def test_exact_questions_premises_and_closed_gold_cover_all_sixteen_candidates(self):
        before = deepcopy(self.packet)
        pages, manifest = self.render()
        self.assertEqual(len(pages), 5)
        self.assertEqual(set(pages), set(manifest["routes"]))
        self.assertEqual(len(self.packet["probes"]), 16)
        for key in reader.DIAGNOSTIC_CLUSTERS:
            route = reader.HUB + "diagnostics/" + key + "/index.html"
            page = pages[route]["body"]
            parsed = DisclosureParser(page)
            visible = ''.join(parsed.outside)
            self.assertEqual(parsed.open_disclosures, [])
            self.assertEqual(parsed.depth, 0)
            self.assertIn("provisional", visible)
            for probe in (p for p in self.packet["probes"] if p["cluster_id"] == key):
                self.assertIn(reader.prose(probe["question"]), page)
                from website.scripts.qcb_render_test_support import recover_prose_source
                self.assertEqual(recover_prose_source(page, probe["question"]), probe["question"])
                self.assertNotIn(probe["gold"]["answer"], visible)
                self.assertNotIn(probe["gold"]["reference_proof"], visible)
                self.assertIn(reader.prose(probe["gold"]["answer"]), page)
                self.assertIn(reader.esc(probe["gold"]["reference_proof"]), page)
                for field in ("assumptions", "conventions"):
                    expected = '<ul data-qcb-diagnostic-' + field + '>' + ''.join('<li>' + reader.esc(v) + '</li>' for v in probe[field]) + '</ul>'
                    self.assertIn(expected, page)
                rubric = '<ol>' + ''.join('<li>' + reader.esc(row["criterion"]) + ' <small>(weight ' + reader.esc(row["weight"]) + ')</small></li>' for row in probe["gold"]["rubric"]) + '</ol>'
                self.assertIn(rubric, page)
                target = probe["formal_context"]["proposition"]
                if probe["gold"]["decision"] == "refuted":
                    target = "¬ (" + target + ")"
                self.assertIn(reader.esc(target), page)
        self.assertEqual(self.packet, before)

    def test_all_sources_are_bound_to_publication_context_and_parent_links_resolve(self):
        pages, manifest = self.render()
        for route, page in pages.items():
            links = DisclosureParser(page["body"]).links
            source_links = [link for link in links if link.startswith(reader.REPO)]
            self.assertTrue(source_links)
            self.assertTrue(all('/blob/' + self.commit + '/' in link for link in source_links))
            self.assertFalse(any('/main/' in link or reader.SOURCE_COMMIT in link for link in source_links))
            for source in self.packet["source_bindings"]:
                self.assertIn(reader.esc(source["path"]), page["body"])
                self.assertIn(reader.esc(source["sha256_lf"]), page["body"])
            for link in (h for h in links if '/cores/' in h):
                from urllib.parse import urljoin
                self.assertTrue(urljoin('https://example.test/' + route, link).startswith('https://example.test/' + reader.HUB + 'cores/'))
        self.assertEqual(manifest["source_commit"], self.commit)
        self.assertEqual(manifest["cohort_digest"], digest(self.packet))
        self.assertEqual(manifest["reference_receipt_digest"], self.qualification["reference_receipt_digest"])

    def test_candidate_inventory_is_additive_without_canonical_count_changes(self):
        _, diagnostic = self.render()
        manifest = {"native_core_ids": 198, "admitted_native_lean_views": 3,
                    "experimental_course": {"distinct_shared_cores": 18}}
        before = deepcopy(manifest)
        manifest["public_semantic_diagnostics"] = diagnostic
        self.assertEqual({k: manifest[k] for k in before}, before)
        self.assertEqual(diagnostic["diagnostic_candidates"], 16)
        self.assertEqual(diagnostic["contrast_pairs"], 8)
        self.assertEqual(len(diagnostic["clusters"]), 4)
        for field in ("new_canonical_core_ids", "new_canonical_lean_admissions", "new_course_companions"):
            self.assertEqual(diagnostic[field], 0)
        self.assertEqual(diagnostic["admission"], "candidate_not_counted")
        self.assertFalse(diagnostic["hidden_holdout"])
        self.assertFalse(diagnostic["model_performance_measured"])
        self.assertIsNone(diagnostic["learning_gain"])

    def test_escaping_preserves_reviewed_prose_without_executing_html(self):
        packet = deepcopy(self.packet)
        probe = packet["probes"][0]
        probe["question"] += '<script>alert("question")</script>'
        probe["assumptions"] = ['<img src=x onerror="bad">']
        probe["gold"]["answer"] += '<svg onload="bad"></svg>'
        probe["gold"]["rubric"][0]["criterion"] += '<iframe src="bad"></iframe>'
        probe["gold"]["reference_proof"] += '\n-- <script>bad</script>'
        with self.assertRaisesRegex(ValueError, "notation is stale"):
            self.render(packet)
        # A fresh unannotated software fixture still exercises HTML escaping.
        probe["probe_id"] = 'ffffffff-ffff-4fff-8fff-ffffffffffff'
        pages, _ = self.render(packet)
        page = pages[reader.HUB + "diagnostics/" + probe["cluster_id"] + "/index.html"]["body"]
        for tag in ("script", "img", "svg", "iframe"):
            self.assertNotIn('<' + tag, page)
            self.assertIn('&lt;' + tag, page)

    def test_source_link_rejects_path_injection_and_has_no_floating_fallback(self):
        for path in ("../private", "/root/private", "javascript:alert(1)", "C:\\private"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                reader.diagnostic_source_link(path, self.commit)
        invalid = reader.diagnostic_source_link("QuantumBlockEncoding/HermitePolynomial.lean", "main")
        self.assertNotIn('href=', invalid)
        self.assertIn("unavailable", invalid)

    def test_projection_check_detects_stale_binding_and_opened_or_changed_answers(self):
        pages, diagnostic = self.render()
        manifest = {"public_semantic_diagnostics": diagnostic, "source_commit": self.commit}
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            for route, page in pages.items():
                path = output / route
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(page["body"], encoding="utf-8")
            reader.check_diagnostic_pages(output, self.packet, self.qualification, manifest)
            altered = deepcopy(manifest)
            altered["public_semantic_diagnostics"]["reference_receipt_digest"] = digest("stale")
            with self.assertRaisesRegex(ValueError, "stale cohort, receipt"):
                reader.check_diagnostic_pages(output, self.packet, self.qualification, altered)
            probe = self.packet["probes"][0]
            route = reader.HUB + "diagnostics/" + probe["cluster_id"] + "/index.html"
            path = output / route
            page = path.read_text(encoding="utf-8")
            path.write_text(page.replace('id="answer-' + probe["probe_id"] + '"', 'open id="answer-' + probe["probe_id"] + '"'), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "closed answer"):
                reader.check_diagnostic_pages(output, self.packet, self.qualification, manifest)


if __name__ == "__main__":
    unittest.main()
