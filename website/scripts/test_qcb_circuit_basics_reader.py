"""Validate public v7 navigation and exact, split-separated downloads."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "benchmarks/quantumcomputingbench/src"))
sys.path.insert(0, str(ROOT / "benchmarks/quantumcomputingbench/scripts"))
from website.scripts import qcb_circuit_basics_reader as reader
from website.scripts.quantumcomputingbench import disclosure, section


class CircuitBasicsReaderTests(unittest.TestCase):
    def record(self):
        entries, views, graph = [], {}, {}
        for i, (core, split) in enumerate(zip(reader.TOPICS, ("test_public", "dev", "train", "train"))):
            view, node = f"view-{i}", f"declaration:source{i}"
            entries.append({"core_id": core, "view_id": view, "split": split,
                "difficulty": {"construction_band": "D2", "imported_shortcut": "fixture"}, "source_node_ids": [node]})
            views[view] = {"formal_scope": "Exact fixture", "task": {"question": "State the mathematical claim.",
                "assumptions": ["Assume the domain is finite."], "conventions": ["Row order is fixed."],
                "nodes": [{"id": "root", "depends_on": [], "target": "True"}]}}
            graph[node] = {"source": "QuantumBlockEncoding/Basic.lean", "line": 1}
        artifacts = {s + "-inputs.json": {"tasks": [], "reference_answers_projected": False} for s in reader.SPLITS}
        artifacts.update({"train-references.json": {"references": ["train-only"]}, "coverage.json": {
            "distinct_shared_cores": 29, "task_anchor_node_count": 84, "by_construction_band": {"D2": 29}}})
        return {"source_commit": "a" * 40, "entries": entries}, artifacts, views, graph

    def test_hierarchy_and_downloads(self):
        record, pages = self.record(), {}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary = reader.publish(lambda route, title, body, desc: pages.update({route + "index.html": body}),
                lambda title, deck: f"<div><h1>{title}</h1><p>{deck}</p>", section, disclosure,
                lambda path, line: f"https://example.test/{path}#L{line}", root / "data/quantumcomputingbench", record, record[3])
            self.assertEqual(len(pages), 6)
            for entry in record[0]["entries"]:
                core, split = entry["core_id"], entry["split"]
                page = pages[reader.route_for(core) + "index.html"]
                self.assertIn('id="question"', page)
                self.assertIn('id="obligations"', page)
                self.assertIn('data-qcb-math-deferred', page)
                self.assertNotIn('<details open', page)
                self.assertIn('lean-graph/index.html?focus=', page)
                self.assertIn('reference-checks.json#L1', page)
                self.assertEqual('train-references.json' in page, split == 'train')
            manifest = {"source_commit": "a" * 40, "routes": list(pages), "lean_course_v7": summary}
            with patch.object(reader, "publication", return_value=record):
                reader.check(root, manifest)
                (root / reader.DATA / "test_public-inputs.json").write_text('{}', encoding='utf-8')
                with self.assertRaisesRegex(ValueError, "qualified projection"):
                    reader.check(root, manifest)

    def test_missing_anchor_and_orphan_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaisesRegex(ValueError, "anchor missing"):
                reader.publish(lambda *args: None, lambda *args: '<div>', section, disclosure, lambda *args: None,
                               root, self.record(), {})
            with patch.object(reader, "publication", return_value=None):
                reader.check(root, {"source_commit": "a" * 40, "routes": []})
                with self.assertRaisesRegex(ValueError, "no qualified source"):
                    reader.check(root, {"source_commit": "a" * 40, "routes": [reader.RUN + 'index.html']})

    def test_reference_absence_refuses_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp, patch("qcb_course_circuit_basics.EVIDENCE", Path(tmp)):
            self.assertIsNone(reader.publication("a" * 40))

    def test_notation_requires_exact_review_inputs(self):
        from qcb_course_circuit_basics import EVIDENCE
        comparison = reader.read_json(EVIDENCE / "comparison-input.json")
        questions = {row["core_id"]:row["source_semantics"]["question"] for row in comparison["views"]}
        reader.check_notation(EVIDENCE, questions)
        changed = dict(reader.NOTATION)
        changed["qcb-core-la-004"] += " A fabricated extra premise."
        with patch.object(reader, "NOTATION", changed), self.assertRaisesRegex(ValueError, "exact independent"):
            reader.check_notation(EVIDENCE, questions)


if __name__ == "__main__":
    unittest.main()
