"""Circuit-course identity and answer-boundary regression; no model execution."""
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(B / "src"), str(B / "scripts")]
from qcb_core import digest, read_json
from qcb_course_circuit_basics import EXPECTED_SPLITS, FIXTURE, PLAN, _validate_cases, reference_records
import qcb_course_registry_v7 as registry
from qcb_lean_course import export_course, topology
from qcb_proof_session import validate_task


class CircuitCourseTests(unittest.TestCase):
    def test_frozen_prior_course_and_original_splits(self):
        before, after = read_json(B / "tracks/lean/curriculum/course-v6.json"), read_json(PLAN)
        self.assertEqual(before["entries"], after["entries"][:len(before["entries"])])
        self.assertEqual(after["course_id"], registry.SUITE_ID)
        self.assertEqual(len(after["entries"]), registry.CORE_COUNT)
        self.assertEqual({e["core_id"]: e["split"] for e in after["entries"][-4:]}, EXPECTED_SPLITS)
        cases = read_json(FIXTURE)["cases"]
        _validate_cases(cases)
        for case in cases:
            task = validate_task(case["task"])
            entry = next(e for e in after["entries"] if e["view_id"] == case["view_id"])
            self.assertEqual(entry["task_hash"], digest(task))
            self.assertEqual(entry["topology"], topology(task))

    def test_train_export_has_only_two_train_companions(self):
        records = reference_records()
        self.assertEqual(set(records), {c for c, split in EXPECTED_SPLITS.items() if split == "train"})
        cases = read_json(FIXTURE)["cases"]
        for case in cases:
            core = case["task"]["core_id"]
            if core in records:
                self.assertEqual(records[core]["proof"], case["controls"]["constructed_whole_root"])
                self.assertEqual(records[core]["source_digest"], digest(case))
        for key in ("author_identity", "split", "group"):
            bad = deepcopy(cases)
            if key == "split":
                bad[0]["task"][key] = "train"
            elif key == "group":
                bad[0]["semantic_evidence"][key] = "reversible"
            else:
                bad[0][key] = "wrong-author"
            with self.subTest(field=key), self.assertRaises(ValueError):
                _validate_cases(bad)

    def test_answer_free_environments_under_both_modes(self):
        # The exact source input is authored public data, never a private gold
        # bundle. Session construction must still keep proof bodies out of all
        # input modes, including the supplied DAG condition.
        from qcb_proof_session import ProofSession
        for case in read_json(FIXTURE)["cases"]:
            task = validate_task(case["task"])
            for mode in ("root_only", "proof_dag"):
                for exposure in ("closed_book", "approved_interface"):
                    payload = ProofSession(task, mode=mode, exposure=exposure).agent_input()
                    serialized = repr(payload)
                    self.assertNotIn("constructed_whole_root", serialized)
                    self.assertNotIn("negative_controls", serialized)
                    self.assertNotIn("worked_derivation", serialized)
                    self.assertNotIn("reference_answer", serialized)
                    for proof in case["controls"].values():
                        self.assertNotIn(proof, serialized)

    def test_registry_rejects_truncated_or_wrong_version(self):
        source = ({"course_id": "qcb-lean-graph-course-v6", "entries": []}, {}, {}, {}, {})
        with patch.object(registry, "_load_current_course", return_value=source), \
                patch.object(registry, "validate_course"), self.assertRaises(ValueError):
            registry.load_course_registry()

    def test_single_task_contract_rejects_tampering(self):
        import course_task_v7 as bundle
        case = read_json(FIXTURE)["cases"][0]
        task = validate_task(case["task"])
        key = case["view_id"]
        synthetic_registry = ({key: {"task": task, "entry": {"task_hash": digest(task),
            "allowed_modes": ["root_only", "proof_dag"], "allowed_exposures": ["closed_book", "approved_interface"]}}},
            {"suite_id": registry.SUITE_ID, "registry_digest": "software-test"})
        with patch.object(bundle, "proof_input_digest", return_value="software-proof-digest"):
            record = bundle.package(key, "root_only", "approved_interface", registry=synthetic_registry)
            self.assertFalse(record["grading_contract"]["reference_proofs_included"])
            self.assertTrue(record["environment"]["isolation_required_for_model_generated_lean"])
            self.assertTrue(bundle.verify(record, registry=synthetic_registry)["passed"])
            bad = deepcopy(record)
            bad["environment"]["isolation_required_for_model_generated_lean"] = False
            with self.assertRaisesRegex(ValueError, "differs"):
                bundle.verify(bad, registry=synthetic_registry)
            bad = deepcopy(record)
            bad["input"]["task"]["question"] = "Altered target"
            # Even a recomputed checksum cannot replace the registered task.
            del bad["package_digest"]
            bad["package_digest"] = digest(bad)
            with self.assertRaisesRegex(ValueError, "differs"):
                bundle.verify(bad, registry=synthetic_registry)


if __name__ == "__main__":
    unittest.main()
