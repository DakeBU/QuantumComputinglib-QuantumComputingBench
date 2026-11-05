"""Course selection keeps the original execution and evidence boundaries."""
import asyncio
import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(B / "src"), str(B / "scripts")]
import qcb_course_registry as registry
from qcb_core import digest
from qcb_evaluation_registry import export_views
from qcb_model_loop import run_episode
from test_proof_session import task

spec = importlib.util.spec_from_file_location("qcb_course_evaluate_cli", B / "scripts/evaluate_agentic.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


def software_course():
    t = task()
    entry = {"view_id": "software-course-view", "task_hash": digest(t),
             "allowed_modes": ["root_only", "proof_dag"],
             "allowed_exposures": ["closed_book", "approved_interface"],
             **{k: t[k] for k in ("core_id", "contract_hash", "family", "split", "snapshot_id")}}
    view = {"entry": entry, "task": t, "registry_digest": "f" * 64,
            "reference_lineage": {"software_mock_only": True}}
    plan = {"course_id": "software-mock-course", "entries": [
        {"view_id": entry["view_id"], "difficulty": {"construction_band": "D2"}}]}
    report = {"course_digest": digest(plan), "distinct_shared_cores": 1,
              "reference_qualification": {"software_mock_only": True}}
    return plan, {entry["view_id"]: view}, {"catalog_hash": "software-mock"}, {}, report


class CourseRegistryTests(unittest.TestCase):
    def registered(self, source=None):
        source = software_course() if source is None else source
        with patch.object(registry, "_load_current_course", return_value=source), \
                patch.object(registry, "validate_course"):
            return registry.load_course_registry()

    def test_registration_preserves_tasks_lineage_and_separates_execution(self):
        source = software_course()
        before = deepcopy(source)
        views, qualification = self.registered(source)
        self.assertEqual(source, before)
        view = views["software-course-view"]
        self.assertEqual(view["task"], source[1]["software-course-view"]["task"])
        self.assertEqual(view["reference_lineage"], source[1]["software-course-view"]["reference_lineage"])
        self.assertEqual(view["registry_digest"], qualification["registry_digest"])
        self.assertEqual(view["entry"]["construction_band"], "D2")
        self.assertFalse(qualification["validation_performed_lean_replay"])
        self.assertFalse(qualification["model_performance_measured"])
        self.assertEqual(qualification["isolated_model_evaluation"], "ENV_BLOCKED")
        self.assertEqual(qualification["new_mathematical_cores"], 0)

    def test_incomplete_qualification_or_replaced_task_hash_cannot_keep_identity(self):
        source = software_course()
        source[4]["course_digest"] = "stale"
        with self.assertRaises(ValueError):
            self.registered(source)
        source = software_course()
        views, original = self.registered(source)
        source[1]["software-course-view"]["entry"]["task_hash"] = "e" * 64
        _, changed = self.registered(source)
        self.assertNotEqual(original["registry_digest"], changed["registry_digest"])

    def test_export_remains_answer_free_and_fixed_split(self):
        views, qualification = self.registered()
        export = export_views(views, qualification)
        self.assertFalse(export["reference_answers_projected"])
        self.assertEqual(export["tasks"][0]["input"]["task"]["split"], task()["split"])
        self.assertFalse(export["blind_test"])
        self.assertNotIn("reference_lineage", export["tasks"][0]["input"])
        with self.assertRaises(ValueError):
            export_views(views, qualification, view_ids=["unknown"])

    def invoke(self, *arguments):
        out, err = io.StringIO(), io.StringIO()
        with patch.object(sys, "argv", ["evaluate_agentic.py", *map(str, arguments)]), \
                redirect_stdout(out), redirect_stderr(err):
            status = cli.main()
        return status, out.getvalue(), err.getvalue()

    def test_cli_default_preserves_pilot_and_explicit_course_uses_qualified_selection(self):
        views, qualification = self.registered()
        with patch.object(cli, "load_registry", return_value=(views, qualification)) as pilot, \
                patch.object(cli, "load_course_registry", return_value=(views, qualification)) as course:
            self.assertEqual(self.invoke("list")[0], 0)
            pilot.assert_called_once()
            course.assert_not_called()
            self.assertEqual(self.invoke("list", "--suite", "course-v4")[0], 0)
            course.assert_called_once()

    def test_offline_profile_does_not_read_course_or_pilot_registry(self):
        with patch.object(cli, "load_registry") as pilot, patch.object(cli, "load_course_registry") as course:
            self.assertEqual(self.invoke("schema")[0], 0)
            self.assertEqual(self.invoke("schema", "--suite", "course-v4")[0], 1)
            pilot.assert_not_called()
            course.assert_not_called()

    def test_real_formal_mode_still_blocks_before_adapter_or_episode_creation(self):
        from test_operator_profile import completed_profile
        views, _ = self.registered()
        constructed = []
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "not-created"
            result = asyncio.run(run_episode(views["software-course-view"], completed_profile(), path,
                authorized=True, provider_factory=lambda: constructed.append(True)))
            self.assertEqual(result["status"], "ENV_BLOCKED")
            self.assertFalse(path.exists())
            self.assertEqual(constructed, [])


if __name__ == "__main__":
    unittest.main()
