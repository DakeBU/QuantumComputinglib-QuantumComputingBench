"""Public projection and reader hierarchy checks; no proof execution or model calls."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "benchmarks/quantumcomputingbench/src"))
sys.path.insert(0, str(ROOT / "benchmarks/quantumcomputingbench/scripts"))
from website.scripts import qcb_linear_circuit_reader as reader
from website.scripts.quantumcomputingbench import disclosure, section


class LinearCircuitReaderTests(unittest.TestCase):
    def record(self):
        entries, views, graph = [], {}, {}
        for number, core_id in enumerate(reader.TOPICS):
            key, view_id = "declaration:Example." + str(number), "view-" + str(number)
            entry = {"core_id": core_id, "view_id": view_id, "split": "train",
                     "difficulty": {"construction_band": "D" + str(3 + number), "imported_shortcut": "Public source is available."},
                     "source_node_ids": [key]}
            entries.append(entry)
            graph[key] = {"id": key, "source": "QuantumBlockEncoding/Example.lean", "line": 12}
            views[view_id] = {"formal_scope": "Synthetic software test only.", "task": {
                "nodes": [{"id": "root", "depends_on": [], "target": "True"}]}}
        artifacts = {name + "-inputs.json": {"reference_answers_projected": False, "tasks": []}
                     for name in ("train", "dev", "test_public")}
        artifacts.update({"train-references.json": {"train_only": True}, "coverage.json": {
            "distinct_shared_cores": 25, "task_anchor_node_count": 72, "by_construction_band": {"D3": 9, "D4": 6}}})
        manifest = {"source_commit": "a" * 40, "entries": entries}
        return manifest, artifacts, views, graph

    def test_downloads_are_exact_and_details_are_collapsed(self):
        record = self.record()
        with tempfile.TemporaryDirectory() as temp:
            root, pages = Path(temp), {}
            summary = reader.publish(
                lambda route, title, body, deck: pages.update({route + "index.html": body}),
                lambda title, deck: f"<div><h1>{title}</h1><p>{deck}</p>", section, disclosure,
                lambda path, line: f"https://example.test/{path}#L{line}",
                root / "data/quantumcomputingbench", record, record[3])
            self.assertEqual(len(pages), 4)
            for core in reader.TOPICS:
                html = pages[reader.route_for(core) + "index.html"]
                self.assertIn('id="setup"', html)
                self.assertIn('data-qcb-math-deferred', html)
                self.assertNotIn('<details open', html)
                self.assertIn('lean-graph/index.html?focus=', html)
                self.assertIn(f'cores/{core}/index.html#question', html)
                self.assertIn('reference-checks.json#L1', html)
            publication = {"source_commit": "a" * 40, "routes": list(pages), "lean_course_v6": summary}
            with patch.object(reader, "publication", return_value=record):
                reader.check(root, publication)
                # Adding any unlisted file, including private material, fails publication.
                (root / reader.DATA / "unlisted.json").write_text("{}")
                with self.assertRaisesRegex(ValueError, "inventory"):
                    reader.check(root, publication)

    def test_missing_anchor_fails_instead_of_drawing_an_unbacked_graph(self):
        record = self.record()
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "anchor missing"):
                reader.publish(lambda *args: None, lambda *args: "<div>", section, disclosure,
                               lambda *args: "https://example.test/", Path(temp), record, {})

    def test_unpublished_checkout_renders_paths_without_invented_source_links(self):
        record, pages = self.record(), {}
        with tempfile.TemporaryDirectory() as temp:
            reader.publish(lambda route, title, body, deck: pages.update({route: body}),
                           lambda *args: "<div>", section, disclosure, lambda *args: None,
                           Path(temp), record, record[3])
        html = pages[reader.route_for("qcb-core-la-013")]
        self.assertIn("source link unavailable", html)
        self.assertIn("reports/lean-course-linear-circuit-v1/comparison.json", html)
        self.assertNotIn('href="None"', html)

    def test_no_receipt_means_no_public_course_download(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch("qcb_course_linear_circuit.EVIDENCE", Path(temp)):
                self.assertIsNone(reader.publication("a" * 40))

    def test_no_receipt_rejects_orphaned_html_or_route_entry(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(reader, "publication", return_value=None):
            root = Path(temp)
            manifest = {"source_commit": "a" * 40, "routes": []}
            reader.check(root, manifest)
            path = reader.route_for("qcb-core-la-013") + "index.html"
            manifest["routes"] = [path]
            with self.assertRaisesRegex(ValueError, "no qualified source"):
                reader.check(root, manifest)
            manifest["routes"] = []
            (root / path).parent.mkdir(parents=True)
            (root / path).write_text("stale page")
            with self.assertRaisesRegex(ValueError, "no qualified source"):
                reader.check(root, manifest)

    def test_displayed_math_cannot_outlive_its_exact_review(self):
        import json
        from qcb_course_linear_circuit import EVIDENCE
        reader.check_exposition(EVIDENCE)
        records = {name: json.loads((EVIDENCE / name).read_text(encoding="utf-8"))
                   for name in ("displayed-derivation-review.json", "comparison.json")}
        records["displayed-derivation-review.json"]["function_text_sha256"] = "0" * 64
        with patch.object(reader, "read_json", side_effect=lambda path: records[path.name]):
            with self.assertRaisesRegex(ValueError, "content-bound review"):
                reader.check_exposition(EVIDENCE)


if __name__ == "__main__":
    unittest.main()
