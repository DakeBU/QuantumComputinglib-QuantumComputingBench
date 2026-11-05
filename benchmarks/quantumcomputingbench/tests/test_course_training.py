"""Formal supervision must not leak dev/test references or change the root."""
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(B / "src"), str(B / "scripts")]
from qcb_core import digest
import qcb_course_training as training
from qcb_course_training import export_training
from test_proof_session import task


def context():
    views, records = {}, {}
    for i, split in enumerate(("train", "dev", "test_public")):
        t = task()
        t.update(core_id="software-core-" + str(i), split=split)
        key = "software-view-" + str(i)
        views[key] = {"entry": {"task_hash": digest(t)}, "task": t,
                      "reference_lineage": {"software_mock_only": True}}
        records[t["core_id"]] = {"proof": "by exact " + split.upper() + "_PROOF_SENTINEL",
            "target": next(n["target"] for n in t["nodes"] if n["id"] == t["root_id"]),
            "imports": t["imports"], "task_digest": digest(t), "route": "constructed_whole_root",
            "source": "software_mock", "source_digest": "a" * 64}
    return views, {"registry_digest": "e" * 64, "suite_id": "software-mock-course"}, records


def source_corpus():
    """Both source shapes, with sentinel text instead of mathematical proofs."""
    packets, bound = {}, {}
    for index, name in enumerate(training.FIXTURES):
        t = task()
        t["core_id"] = "software-version-" + str(index)
        controls = {"library_control": "by exact LIBRARY_VERSION_" + str(index)}
        if index % 2 == 0:
            controls["constructed_whole_root"] = "by exact NORMALIZED_VERSION_" + str(index)
        case = {"task": t, "controls": controls}
        if index < 2:
            # These names are authoring syntax; only the bound loader outputs
            # have the exact tasks and proof bodies checked by qualification.
            raw = {"core_id": t["core_id"], "independent_root_reference": "by exact Authored.helper_" + str(index),
                   "root_id": t["root_id"], "imports": t["imports"], "nodes": t["nodes"]}
            packets[name] = {"cases": [raw]}
            bound[name] = ([case], {"fixture_digest": digest(packets[name])})
        else:
            packets[name] = {"cases": [case]}
    return packets, bound


class CourseTrainingTests(unittest.TestCase):
    def read_corpus(self, packets, bound):
        with patch.object(training, "read_json", side_effect=lambda path: packets[path.name]) as reader, \
                patch.object(training, "load_pilot", return_value=bound[training.FIXTURES[0]]) as pilot, \
                patch.object(training, "load_sequential_pilot", return_value=bound[training.FIXTURES[1]]) as sequential:
            result = training.reference_records()
        return result, reader, pilot, sequential

    def test_every_source_version_uses_exact_bound_task_and_normalized_controls(self):
        packets, bound = source_corpus()
        before = deepcopy((packets, bound))
        records, reader, pilot, sequential = self.read_corpus(packets, bound)
        self.assertEqual((packets, bound), before)
        self.assertEqual(len(records), len(training.FIXTURES))
        self.assertEqual([c.args[0].name for c in reader.call_args_list], list(training.FIXTURES))
        pilot.assert_called_once_with()
        sequential.assert_called_once_with()
        self.assertNotIn("Authored.helper_", str(records))
        for index, name in enumerate(training.FIXTURES):
            case = bound[name][0][0] if index < 2 else packets[name]["cases"][0]
            record = records[case["task"]["core_id"]]
            constructed = case["controls"].get("constructed_whole_root")
            expected_proof = constructed if constructed is not None else case["controls"]["library_control"]
            self.assertEqual(record["proof"], expected_proof)
            self.assertEqual(record["task_digest"], digest(case["task"]))
            self.assertEqual(record["source_digest"], digest(packets[name]["cases"][0]))
            self.assertEqual(record["route"], "constructed_whole_root" if constructed is not None else "library_application")

    def test_legacy_source_drift_or_different_bound_coverage_is_rejected(self):
        for mutation in ("source_digest", "coverage"):
            packets, bound = source_corpus()
            if mutation == "source_digest":
                bound[training.FIXTURES[0]][1]["fixture_digest"] = "stale"
            else:
                bound[training.FIXTURES[0]][0][0]["task"]["core_id"] = "different-core"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.read_corpus(packets, bound)

    def test_raw_legacy_proof_cannot_bypass_failed_bound_loader(self):
        packets, _ = source_corpus()
        with patch.object(training, "read_json", side_effect=lambda path: packets[path.name]), \
                patch.object(training, "load_pilot", side_effect=ValueError("unqualified legacy source")), \
                self.assertRaises(ValueError):
            training.reference_records()

    def test_only_train_whole_root_reference_is_projected_and_input_has_no_proof(self):
        views, qualification, records = context()
        before = deepcopy((views, qualification, records))
        result = export_training(views, qualification, records)
        self.assertEqual((views, qualification, records), before)
        self.assertEqual(result["distinct_shared_cores"], 1)
        self.assertNotIn("DEV_PROOF_SENTINEL", str(result))
        self.assertNotIn("TEST_PUBLIC_PROOF_SENTINEL", str(result))
        example = result["examples"][0]
        self.assertIn("TRAIN_PROOF_SENTINEL", example["target"]["proof"])
        self.assertNotIn("TRAIN_PROOF_SENTINEL", str(example["input"]))
        self.assertIsNone(example["process_reward_labels"])
        self.assertFalse(result["training_launched"])

    def test_wrong_target_import_or_task_cannot_reuse_reference(self):
        for key, value in (("target", "False"), ("imports", ["WrongModule"]),
                           ("task_digest", "stale"), ("task_digest", None)):
            views, qualification, records = context()
            records["software-core-0"][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                export_training(views, qualification, records)

    def test_relabelled_task_without_new_binding_is_rejected(self):
        views, qualification, records = context()
        views["software-view-0"]["task"]["question"] = "Replacement question."
        views["software-view-0"]["entry"]["task_hash"] = digest(views["software-view-0"]["task"])
        with self.assertRaises(ValueError):
            export_training(views, qualification, records)

    def test_empty_train_or_duplicate_core_is_not_a_valid_training_export(self):
        views, qualification, records = context()
        del views["software-view-0"]
        with self.assertRaises(ValueError):
            export_training(views, qualification, records)
        views, qualification, records = context()
        views["second-train-view"] = deepcopy(views["software-view-0"])
        with self.assertRaises(ValueError):
            export_training(views, qualification, records)


if __name__ == "__main__":
    unittest.main()
