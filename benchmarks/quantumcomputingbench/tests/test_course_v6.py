"""Software-only v6 selection/export tests; sentinel proofs certify no mathematics."""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(B / "src"), str(B / "scripts")]
import evaluate_course_v6 as cli
import lean_course_v6 as course
import lean_training_v6 as training
import qcb_course_linear_circuit as cohort
import qcb_course_registry_v6 as registry
from qcb_core import digest, write_json
from qcb_evaluation_registry import export_views
from qcb_lean_course import coverage, topology
from qcb_operator_profile import profile_template
from test_proof_session import task


def software_course():
    """Complete synthetic catalog/tasks, independently checked by validate_course."""
    plan = {"schema_version": "qcb.lean_course.v1", "course_id": registry.SUITE_ID,
            "catalog_hash": "software-catalog", "snapshot_id": "fixture-snapshot",
            "difficulty_status": "provisional_author_mathematical_assessment",
            "measured_model_difficulty": None, "blind_test": False,
            "prerequisite_edge_kind": "pedagogical_not_theorem_dependency",
            "new_mathematical_cores": 0, "canonical_formal_admissions_changed": False, "entries": []}
    catalog = {"catalog_hash": plan["catalog_hash"], "snapshot_id": plan["snapshot_id"], "cores": []}
    views, graph, records = {}, {}, {}
    core_ids = ["software-core-" + str(i) for i in range(21)]
    core_ids += ["qcb-core-be-011", "qcb-core-la-019", "qcb-core-la-006", "qcb-core-la-013"]
    for i, core_id in enumerate(core_ids):
        t = task()
        t.update(core_id=core_id, split="dev" if i == 0 else "test_public" if i == 1 else "train")
        key, anchor = "software-view-" + str(i), "software-anchor-" + str(i)
        fields = {k: t[k] for k in ("core_id", "contract_hash", "family", "split", "snapshot_id")}
        entry = {"view_id": key, "task_hash": digest(t), **fields}
        views[key] = {"task": t, "entry": {**entry, "allowed_modes": ["root_only", "proof_dag"],
            "allowed_exposures": ["closed_book", "approved_interface"]},
            "reference_lineage": {"software_mock_only": True}}
        plan["entries"].append({**entry, "source_item_digest": "f" * 64, "source_node_ids": [anchor],
            "prerequisite_core_ids": [], "skills": ["statement_understanding"], "topology": topology(t),
            "difficulty": {"construction_band": "D2", "rationale": "Software fixture only.",
                           "imported_shortcut": "No mathematical evidence.", "measured_model_difficulty": None}})
        catalog["cores"].append({**fields, "item_digest": "f" * 64, "target_nodes": [anchor],
                                 "supporting_nodes": [], "part": "software"})
        graph[anchor] = {"kind": "declaration", "open_obligation": False,
                         "inventory_status": "Compiled", "source": "software-fixture"}
        records[core_id] = {"proof": "by exact " + t["split"].upper() + "_SENTINEL_" + str(i),
            "target": t["nodes"][-1]["target"], "imports": t["imports"], "task_digest": digest(t),
            "route": "constructed_whole_root", "method_disclosure": "Software fixture only.",
            "source": "software-sentinel", "source_digest": "e" * 64}
    report = coverage(plan, views, catalog, graph)
    report["reference_qualification"] = {"software_mock_only": True}
    return (plan, views, catalog, graph, report), records


def software_cases():
    cases = []
    for core_id in sorted(cohort.EXPECTED):
        t = task()
        t["core_id"] = core_id
        cases.append({"task": t, "controls": {"constructed_whole_root": "by exact SOFTWARE_SENTINEL"},
                      "shortcut_disclosure": "Software fixture only."})
    return cases


def operator_config():
    config = profile_template()
    config["adapter"] = {"id": "qcb_nonexistent_adapter:create", "revision_sha256": "a" * 64}
    config["model"] = {"id": "unit-test/no-endpoint", "revision": "b" * 40, "chat_template_sha256": "c" * 64}
    return config


class CourseV6Tests(unittest.TestCase):
    def registered(self, source=None):
        source = software_course()[0] if source is None else source
        with patch.object(registry, "_load_current_course", return_value=source):
            return registry.load_course_registry()

    def test_cumulative_loader_preserves_previous_views_and_qualification(self):
        source, _ = software_course()
        plan, views, catalog, graph, report = source
        old = {key: value for key, value in views.items() if key not in {"software-view-23", "software-view-24"}}
        new = {key: value for key, value in views.items() if key not in old}
        before = deepcopy(source)
        status = {"software_mock_only": "new"}
        with patch.object(course.previous, "load_course", return_value=({}, old, catalog, graph, report)), \
                patch.object(course, "qualified", return_value=(new, status, catalog, graph)), \
                patch.object(course, "read_json", return_value=plan):
            merged = course.load_course()
        self.assertEqual(source, before)
        self.assertEqual(merged[1], views)
        self.assertEqual(merged[4]["distinct_shared_cores"], 25)
        self.assertEqual(merged[4]["reference_qualification"], {
            "previous_course": report["reference_qualification"], "linear_circuit": status})

    def test_cumulative_loader_rejects_overlap_or_unqualified_addition(self):
        source, _ = software_course()
        with patch.object(course.previous, "load_course", return_value=source), \
                patch.object(course, "qualified", return_value=(source[1], {}, source[2], source[3])), \
                self.assertRaisesRegex(ValueError, "replace"):
            course.load_course()
        with patch.object(course.previous, "load_course", return_value=source), \
                patch.object(course, "qualified", side_effect=ValueError("unqualified")), \
                self.assertRaisesRegex(ValueError, "unqualified"):
            course.load_course()

    def test_registry_preserves_tasks_and_binds_only_fixed_v6_selector(self):
        source, _ = software_course()
        before = deepcopy(source)
        views, qualification = self.registered(source)
        self.assertEqual(source, before)
        self.assertEqual(qualification["suite_id"], registry.SUITE_ID)
        self.assertEqual(qualification["distinct_shared_core_ids"], 25)
        self.assertEqual(qualification["isolated_model_evaluation"], "ENV_BLOCKED")
        self.assertFalse(qualification["model_performance_measured"])
        self.assertFalse(qualification["validation_performed_lean_replay"])
        for key, view in views.items():
            self.assertEqual(view["task"], source[1][key]["task"])
            self.assertEqual(view["reference_lineage"], source[1][key]["reference_lineage"])
            self.assertEqual(view["registry_digest"], qualification["registry_digest"])
        self.assertTrue(all("v6.py" in name for name in qualification["selection_sources_sha256_lf"]))

    def test_registry_rejects_wrong_version_partial_course_split_and_identity_drift(self):
        for mutation in ("version", "partial", "split", "task_hash", "entry_split", "report"):
            source, _ = software_course()
            plan, views, catalog, graph, report = source
            if mutation == "version":
                plan["course_id"] = "qcb-lean-graph-course-v5"
                report["course_digest"] = digest(plan)
            elif mutation == "partial":
                removed = plan["entries"].pop()
                del views[removed["view_id"]]
                source = (plan, views, catalog, graph, {**coverage(plan, views, catalog, graph),
                                                      "reference_qualification": {}})
            elif mutation == "split":
                views["software-view-0"]["task"]["split"] = "train"
            elif mutation == "task_hash":
                views["software-view-0"]["entry"]["task_hash"] = "a" * 64
            elif mutation == "entry_split":
                views["software-view-0"]["entry"]["split"] = "train"
            else:
                report["course_digest"] = "stale"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.registered(source)

    def test_answer_free_task_exports_keep_frozen_splits(self):
        views, qualification = self.registered()
        for split in ("train", "dev", "test_public"):
            result = export_views(views, qualification, split=split)
            self.assertFalse(result["reference_answers_projected"])
            self.assertEqual({row["input"]["task"]["split"] for row in result["tasks"]}, {split})
            self.assertNotIn("SENTINEL", str(result))

    def test_cohort_projection_binds_exact_train_roots_without_fallback(self):
        cases = software_cases()
        with patch.object(cohort, "read_json", return_value={"cases": cases}) as reader:
            records = cohort.reference_records()
        reader.assert_called_once_with(cohort.FIXTURE)
        self.assertEqual(set(records), cohort.EXPECTED)
        for case in cases:
            record = records[case["task"]["core_id"]]
            self.assertEqual(record["source_digest"], digest(case))
            self.assertEqual(record["task_digest"], digest(case["task"]))
            self.assertEqual(record["proof"], case["controls"]["constructed_whole_root"])
        for mutation in ("dev", "test_public", "extra", "duplicate", "wrong_core", "proof"):
            changed = deepcopy(cases)
            if mutation in {"dev", "test_public"}:
                changed[0]["task"]["split"] = mutation
            elif mutation == "extra":
                changed.append(deepcopy(changed[0]))
            elif mutation == "duplicate":
                changed[1] = deepcopy(changed[0])
            elif mutation == "wrong_core":
                changed[0]["task"]["core_id"] = "different-core"
            else:
                changed[0]["controls"]["constructed_whole_root"] = None
            with self.subTest(mutation=mutation), \
                    patch.object(cohort, "read_json", return_value={"cases": changed}), self.assertRaises(ValueError):
                cohort.reference_records()

    def test_candidates_require_fixed_source_and_sanitized_review(self):
        result = (software_cases(), {"software_only": True}, {}, {})
        with patch.object(cohort, "load_candidates", return_value=result) as loader, \
                patch.object(cohort, "bind_review_input") as bind:
            self.assertEqual(cohort.candidates(), result)
        loader.assert_called_once_with(fixture=cohort.FIXTURE, evidence_dir=cohort.EVIDENCE,
                                       expected_cores=cohort.EXPECTED)
        bind.assert_called_once_with(cohort.FIXTURE, cohort.EVIDENCE, result[0], require_sanitized=True)
        with patch.object(cohort, "load_candidates", return_value=result), \
                patch.object(cohort, "bind_review_input", side_effect=ValueError("stale review")), \
                self.assertRaisesRegex(ValueError, "stale review"):
            cohort.candidates()

    def export_training(self, records=None):
        source, original = software_course()
        records = original if records is None else records
        views, qualification = self.registered(source)
        old = {key: val for key, val in records.items() if key.startswith("software-core-")}
        ham = {key: records[key] for key in ("qcb-core-be-011", "qcb-core-la-019")}
        new = {key: records[key] for key in cohort.EXPECTED}
        with patch.object(training, "load_course_registry", return_value=(views, qualification)), \
                patch.object(training, "previous_records", return_value=old), \
                patch.object(training, "hamiltonian_records", return_value=ham), \
                patch.object(training, "linear_circuit_records", return_value=new):
            return training.export()

    def test_training_is_cumulative_train_only_with_no_answer_in_input(self):
        result = self.export_training()
        self.assertEqual(result["suite_id"], registry.SUITE_ID)
        self.assertEqual(result["distinct_shared_cores"], 23)
        self.assertFalse(result["dev_and_test_references_projected"])
        self.assertFalse(result["training_launched"])
        self.assertNotIn("DEV_SENTINEL", str(result))
        self.assertNotIn("TEST_PUBLIC_SENTINEL", str(result))
        self.assertTrue(cohort.EXPECTED <= {row["core_id"] for row in result["examples"]})
        self.assertIn("qcb-core-be-011", {row["core_id"] for row in result["examples"]})
        for row in result["examples"]:
            self.assertEqual(row["split"], "train")
            self.assertNotIn("SENTINEL", str(row["input"]))
            self.assertIn("TRAIN_SENTINEL", row["target"]["proof"])

    def test_training_rejects_mismatched_target_imports_task_and_duplicate_sources(self):
        for field, value in (("target", "False"), ("imports", ["Wrong"]), ("task_digest", "stale")):
            _, records = software_course()
            records["qcb-core-la-006"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.export_training(records)
        views, qualification = self.registered()
        with patch.object(training, "load_course_registry", return_value=(views, qualification)), \
                patch.object(training, "previous_records", return_value={"duplicate": {}}), \
                patch.object(training, "hamiltonian_records", return_value={"duplicate": {}}), \
                patch.object(training, "linear_circuit_records") as later, self.assertRaises(ValueError):
            training.export()
        later.assert_not_called()

    def test_unqualified_course_never_opens_training_references(self):
        with patch.object(training, "load_course_registry", side_effect=ValueError("unqualified")), \
                patch.object(training, "previous_records") as old, \
                patch.object(training, "hamiltonian_records") as ham, \
                patch.object(training, "linear_circuit_records") as new, self.assertRaises(ValueError):
            training.export()
        for loader in (old, ham, new):
            loader.assert_not_called()


class CourseV6CliTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="qcb-v6-software-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        source, _ = software_course()
        with patch.object(registry, "_load_current_course", return_value=source):
            self.registered = registry.load_course_registry()
        self.config = self.directory / "operator.json"
        write_json(self.config, operator_config())

    def invoke(self, *arguments):
        output, errors = io.StringIO(), io.StringIO()
        with patch.object(sys, "argv", ["evaluate_course_v6.py", *map(str, arguments)]), \
                patch.object(cli, "load_course_registry", return_value=self.registered), \
                redirect_stdout(output), redirect_stderr(errors):
            status = cli.main()
        return status, output.getvalue(), errors.getvalue()

    def arguments(self, command, *extra):
        return (command, "--view", "software-view-23", "--episode-dir", self.directory / "episode", *extra)

    def test_plan_and_unauthorized_run_never_import_adapter_or_create_directory(self):
        for command in ("plan", "run"):
            with patch("evaluate_agentic.importlib.import_module", side_effect=AssertionError("provider import")) as discover:
                status, output, _ = self.invoke(*self.arguments(command, "--config", self.config,
                    "--adapter", "qcb_nonexistent_adapter:create"))
            self.assertEqual(status, 0)
            self.assertEqual(json.loads(output)["status"], "dry_run")
            self.assertFalse((self.directory / "episode").exists())
            discover.assert_not_called()

    def test_authorized_formal_run_still_blocks_before_provider_and_directory(self):
        with patch("evaluate_agentic.importlib.import_module", side_effect=AssertionError("provider import")) as discover:
            status, output, _ = self.invoke(*self.arguments("run", "--config", self.config,
                "--adapter", "qcb_nonexistent_adapter:create", "--authorize-model"))
        self.assertEqual(status, 2)
        result = json.loads(output)
        self.assertEqual(result["status"], "ENV_BLOCKED")
        self.assertFalse(result["provider_constructed"])
        self.assertFalse(result["formal_proof_success"])
        self.assertFalse((self.directory / "episode").exists())
        discover.assert_not_called()

    def test_fixture_is_explicit_synthetic_protocol_with_no_formal_success(self):
        status, output, _ = self.invoke(*self.arguments("run-fixture"))
        self.assertEqual(status, 0)
        result = json.loads(output)
        self.assertEqual(result["status"], "fixture_protocol_complete")
        self.assertEqual(result["model_calls_confirmed"], 0)
        self.assertFalse(result["formal_proof_success"])
        self.assertTrue((self.directory / "episode/episode.json").exists())

    def test_invalid_options_and_profile_cannot_start_episode(self):
        cases = [self.arguments("plan"), self.arguments("plan", "--config", self.config, "--authorize-model"),
                 self.arguments("run-fixture", "--adapter", "unexpected:create"),
                 self.arguments("run", "--config", self.config, "--adapter", "wrong:create"),
                 self.arguments("run", "--config", self.config, "--mode", "root_only"),
                 ("run-fixture", "--view", "not-in-v6", "--episode-dir", self.directory / "episode"),
                 ("run-fixture", "--view", "software-view-23", "--episode-dir", B / "forbidden-private-episode")]
        with patch.object(cli, "run_episode", side_effect=AssertionError("episode invoked")):
            for arguments in cases[:-1]:
                with self.subTest(arguments=arguments):
                    self.assertEqual(self.invoke(*arguments)[0], 1)
        self.assertEqual(self.invoke(*cases[-1])[0], 1)
        invalid = self.directory / "invalid.json"
        write_json(invalid, profile_template())
        self.assertEqual(self.invoke(*self.arguments("run", "--config", invalid))[0], 1)
        self.assertFalse((self.directory / "episode").exists())


if __name__ == "__main__":
    unittest.main()
