"""Synthetic metadata tests do not establish mathematical difficulty or proofs."""
import sys
import unittest
from copy import deepcopy
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_core import digest
from qcb_lean_course import coverage, export_course, topology, validate_course
from test_proof_session import task


def fixture():
    views, cores, entries, graph = {}, [], [], {}
    # Lexical order deliberately disagrees with same-band prerequisite order.
    for key in ("z", "a"):
        fixed = task()
        fixed.update(core_id="fixture-" + key, contract_hash=key*64, family="family-" + key)
        core = {k: fixed[k] for k in ("core_id", "contract_hash", "family", "split", "snapshot_id")}
        core.update(item_digest=digest(key), part="fixture", target_nodes=["declaration:" + key], supporting_nodes=[])
        graph["declaration:" + key] = {"kind": "declaration", "open_obligation": False, "inventory_status": "Compiled", "source": key + ".lean"}
        entry = {k: core[k] for k in ("core_id", "contract_hash", "family", "split", "snapshot_id")}
        entry.update(view_id="view-" + key, task_hash=digest(fixed), source_item_digest=core["item_digest"],
                     difficulty={"construction_band": "D2", "rationale": "Synthetic metadata fixture only.",
                                 "imported_shortcut": "Synthetic fixture; no actual mathematical proof.", "measured_model_difficulty": None},
                     skills=["statement_understanding"], topology=topology(fixed), source_node_ids=core["target_nodes"],
                     prerequisite_core_ids=[] if key == "z" else ["fixture-z"])
        entries.append(entry); cores.append(core); views[entry["view_id"]] = {"task": fixed}
    catalog = {"catalog_hash": "catalog", "snapshot_id": "fixture-snapshot", "cores": cores}
    plan = {"schema_version": "qcb.lean_course.v1", "catalog_hash": "catalog", "snapshot_id": "fixture-snapshot",
            "difficulty_status": "provisional_author_mathematical_assessment", "measured_model_difficulty": None,
            "prerequisite_edge_kind": "pedagogical_not_theorem_dependency",
            "blind_test": False, "new_mathematical_cores": 0, "canonical_formal_admissions_changed": False, "entries": entries}
    return plan, views, catalog, graph


class LeanCourseTests(unittest.TestCase):
    def test_coverage_and_export_do_not_create_cores_proofs_or_empirical_difficulty(self):
        plan, views, catalog, graph = fixture()
        report = coverage(plan, views, catalog, graph)
        self.assertEqual(report["distinct_shared_cores"], 2)
        self.assertEqual(report["task_anchor_node_count"], 2)
        self.assertFalse(report["difficulty_empirically_calibrated"])
        self.assertFalse(report["node_wide_source_semantic_debt_cleared"])
        exported = export_course(plan, views, catalog, graph, split="train")
        self.assertEqual([t["view_id"] for t in exported["tasks"]], ["view-z", "view-a"])
        self.assertFalse(exported["model_performance_measured"])
        self.assertEqual(exported["new_mathematical_cores"], 0)
        self.assertEqual(plan, fixture()[0])

    def test_train_course_rejects_test_answer_prerequisite(self):
        plan, views, catalog, graph = fixture()
        entry, core = plan["entries"][0], catalog["cores"][0]
        views[entry["view_id"]]["task"]["split"] = entry["split"] = core["split"] = "test_public"
        entry["task_hash"] = digest(views[entry["view_id"]]["task"])
        with self.assertRaisesRegex(ValueError, "leaks"):
            validate_course(plan, views, catalog, graph)

    def test_declared_graph_inventory_is_not_automatic_verified_gold(self):
        for change in (lambda n: n.update(kind="research_obligation"), lambda n: n.update(open_obligation=True),
                       lambda n: n.update(inventory_status="Planned")):
            plan, views, catalog, graph = fixture();change(graph["declaration:z"])
            with self.assertRaises(ValueError):
                validate_course(plan, views, catalog, graph)

    def test_stale_contract_difficulty_and_padded_topology_fail(self):
        for change in (lambda p: p["entries"][0].update(task_hash="stale"),
                       lambda p: p["entries"][0]["difficulty"].update(measured_model_difficulty=0.8),
                       lambda p: p["entries"][0]["topology"].update(longest_obligation_chain_nodes=999),
                       lambda p: p["entries"].append(deepcopy(p["entries"][0]))):
            plan, views, catalog, graph = fixture();change(plan)
            with self.assertRaises(ValueError):
                validate_course(plan, views, catalog, graph)

    def test_cycles_and_reversed_bands_are_rejected(self):
        plan, views, catalog, graph = fixture()
        plan["entries"][0]["prerequisite_core_ids"] = ["fixture-a"]
        with self.assertRaisesRegex(ValueError, "cycle"):
            validate_course(plan, views, catalog, graph)
        plan, views, catalog, graph = fixture()
        plan["entries"][0]["difficulty"]["construction_band"] = "D4"
        with self.assertRaisesRegex(ValueError, "band"):
            validate_course(plan, views, catalog, graph)

    def test_shape_labels_describe_supplied_graph_and_real_reconvergence(self):
        fixed = task()
        self.assertEqual(topology(fixed)["tags"], ["chain"])
        fixed["nodes"] = [{"id": "base", "target": "True", "depends_on": []},
                          {"id": "left", "target": "True", "depends_on": ["base"]},
                          {"id": "right", "target": "True", "depends_on": ["base"]},
                          {"id": "root", "target": "True", "depends_on": ["left", "right"]}]
        result = topology(fixed)
        self.assertIn("reconvergent_diamond", result["tags"])
        self.assertIn("shared_prerequisite", result["tags"])
        self.assertEqual(result["longest_obligation_chain_nodes"], 3)
        self.assertFalse(result["is_semantic_reasoning_depth"])
        fixed["nodes"][1]["depends_on"] = []
        self.assertNotIn("reconvergent_diamond", topology(fixed)["tags"])
        fixed["nodes"] = [{"id": "base", "target": "True", "depends_on": []},
                          {"id": "middle", "target": "True", "depends_on": ["base"]},
                          {"id": "root", "target": "True", "depends_on": ["base", "middle"]}]
        self.assertIn("shared_prerequisite", topology(fixed)["tags"])
        self.assertNotIn("reconvergent_diamond", topology(fixed)["tags"])

    def test_filtered_stage_lists_omitted_prerequisites_without_injecting_answers(self):
        plan, views, catalog, graph = fixture()
        plan["entries"][1]["difficulty"]["construction_band"] = "D3"
        exported = export_course(plan, views, catalog, graph, band="D3")
        self.assertEqual(exported["tasks"][0]["prerequisites_outside_selection"], ["fixture-z"])
        self.assertEqual(len(exported["tasks"]), 1)
        self.assertNotIn("reference", str(exported["tasks"][0]["input"]))
        with self.assertRaises(ValueError):
            export_course(plan, views, catalog, graph, split="dev")


if __name__ == "__main__":
    unittest.main()
