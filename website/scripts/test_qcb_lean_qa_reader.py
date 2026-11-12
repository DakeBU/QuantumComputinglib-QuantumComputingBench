"""Exercise the versioned public reader and its private-data boundary."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from website.scripts import quantumcomputingbench as site
from website.scripts import qcb_lean_qa_reader as reader

import qcb_course_hamiltonian as hamiltonian
import qcb_sparse_study as sparse
from qcb_core import digest, read_json


class LeanQAReaderTests(unittest.TestCase):
    def test_pending_evidence_does_not_publish_and_stale_evidence_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            with patch.object(hamiltonian, "EVIDENCE", folder), patch.object(
                sparse, "QUALIFICATION", folder / "sparse.json"
            ), patch.object(hamiltonian, "qualified", side_effect=ValueError("stale reference")):
                self.assertIsNone(reader.publication("1" * 40))
                self.assertEqual(reader.entry_links(reader.HUB + "lean/", None), "")
                (folder / "reference-checks.json").touch()
                with self.assertRaisesRegex(ValueError, "stale reference"):
                    reader.publication("1" * 40)

    def test_qualified_projection_links_exact_anchors_without_private_metadata(self):
        commit = "1" * 40
        plan = read_json(hamiltonian.PLAN)
        entries = [row for row in plan["entries"] if row["core_id"] in reader.TOPICS]
        graph = {node: {"id": node, "source": "QuantumBlockEncoding/GHLHamiltonian.lean", "line": i + 1}
                 for i, node in enumerate(dict.fromkeys(node for row in entries for node in row["source_node_ids"]))}
        views = {row["view_id"]: {
            "entry": {key: row[key] for key in ("core_id", "task_hash", "split")},
            "formal_scope": "Exact matrix claim",
            "task": {"nodes": [{"id": "root", "target": "True", "depends_on": []}]},
        } for row in entries}
        catalog = {"cores": [{"core_id": row["core_id"], "split": "train"} for row in entries],
                   "graph_source_commit": commit, "snapshot_id": plan["snapshot_id"]}
        status = {"reference_lineage": {"recorded_code_revision": commit},
                  "new_mathematical_cores": 0, "new_canonical_formal_admissions": 0}
        seal = {"probe_count": 4, "contrast_count": 2, "source_group": "banded_sparse_address_semantics",
                "formal_scope": "decision_polarity_only", "public_source_exposure": "available",
                "private_files_sha256": {"private-sentinel.json": "private-sentinel-digest"}}
        profile = {"profile_id": "software-fixture", "projection_training_fingerprint": "a" * 64,
                   "excluded_core_ids": ["excluded-fixture"]}
        training = {"study_training_profile": profile, "profile_digest": digest(profile),
                    "counts": {"distinct_existing_cores": 2, "nl_and_semantic_views": 2, "lean_views": 2},
                    "actual_model_exposure_authenticated": False}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "reference-checks.json").touch()
            (root / "sparse.json").touch()
            with patch.object(hamiltonian, "EVIDENCE", root), patch.object(
                sparse, "QUALIFICATION", root / "sparse.json"
            ), patch.object(hamiltonian, "qualified", return_value=(views, status, catalog, graph)), patch.object(
                sparse, "load_seal", return_value=seal
            ), patch.object(sparse, "validate_qualification") as gate, patch("lean_qa_training.export", return_value=training):
                record = reader.publication(commit)
                pages = {}
                summary = reader.publish(
                    lambda route, title, body, deck: pages.update({route + "index.html": body}),
                    lambda title, deck: f"<div><h1>{title}</h1><p>{deck}</p>",
                    site.section, site.disclosure,
                    lambda path, line: f"https://example.test/{commit}/{path}#L{line}",
                    root / Path(reader.DATA).parent, record, graph,
                )
                gate.assert_called_once_with(seal)
                self.assertEqual(len(pages), 4)
                self.assertEqual(set(summary["routes"]), set(pages))
                for entry in entries:
                    core_id = entry["core_id"]
                    html = pages[reader.companion_route(core_id) + "index.html"]
                    self.assertIn(f"/cores/{core_id}/index.html#question", html)
                    self.assertIn("/lean-graph/index.html?focus=declaration%3A", html)
                    self.assertIn("reference-checks.json#L1", html)
                sparse_page = pages[reader.SPARSE + "index.html"]
                self.assertIn("4 propositions in 2 contrasts", sparse_page)
                self.assertIn("training-profile.json", sparse_page)
                self.assertNotIn("private-sentinel", str(pages) + str(record[0]))
                manifest = {"source_commit": commit, "routes": list(pages), "lean_qa_v1": summary}
                reader.check(root, manifest)
                (root / reader.DATA / "extra-private.json").touch()
                with self.assertRaisesRegex(ValueError, "file inventory"):
                    reader.check(root, manifest)


if __name__ == "__main__":
    unittest.main()
