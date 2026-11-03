"""Synthetic receipt structures are never Lean evidence or stored as gold."""
import sys
import unittest
from copy import deepcopy
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_core import digest
from qcb_proof_session import proof_sha
from qcb_reference_receipt import validate_course_receipt
from test_proof_session import task


def synthetic():
    fixed = task()
    fixed["nodes"] = [{"id": "root", "target": "True", "depends_on": []}]
    case = {"task": fixed, "references": {"root": "by trivial"}, "controls": {"library_control": "by trivial"},
            "negative_controls": {"wrong_target": "by exact False.elim", "sorry_axiom": "by sorry"}}
    serial = 0

    def record(proof, *, positive, sorry=False):
        nonlocal serial
        serial += 1
        return {"status": "verified" if positive else "compile_error", "failure_class": None if positive else "IMPLEMENTATION_FAILED",
                "request_hash": f"{serial:064x}", "execution_id": f"{serial:032x}", "proof_sha256": proof_sha(proof),
                "kernel_checked": positive, "axioms": ["sorryAx"] if sorry else []}

    row = {"core_id": fixed["core_id"], "task_hash": digest(fixed), "passed": True,
           "positive_obligations": [{"node_id": "root", **record("by trivial", positive=True)}],
           "controls": {"library_control": record("by trivial", positive=True)},
           "negative_controls": {k: record(p, positive=False, sorry=k == "sorry_axiom") for k, p in case["negative_controls"].items()},
           "final_replay": record("by trivial", positive=True)}
    report = {"schema_version": "qcb.graph_course_reference_replay.v1", "passed": True,
              "execution_class": "trusted_local_authored_reference", "isolated": False, "model_performance_measured": False,
              "blind_test": False, "standalone_controls_are_completed_protocol_sessions": False,
              "model_calls": 0, "new_mathematical_cores": 0, "new_canonical_formal_admissions": 0,
              "tested_code_commit": "f"*40, "pipeline_source_hashes_lf": {"first": "a"*64, "second": "b"*64}, "results": [row]}
    report["receipt_digest"] = digest(report)
    return report, [case], {}, {"first", "second"}


class ReferenceReceiptTests(unittest.TestCase):
    def checked(self, mutate=None):
        report, cases, identity, paths = synthetic()
        if mutate:
            mutate(report)
            report.pop("receipt_digest")
            report["receipt_digest"] = digest(report)
        return validate_course_receipt(report, cases, identity, paths)

    def test_complete_synthetic_structure_is_only_metadata_validation(self):
        result = self.checked()
        self.assertFalse(result["model_performance_measured"])
        # An invented source SHA can pass structural validation. The real reader
        # must additionally check the pinned Git blobs and actual external run.
        self.assertEqual(result["tested_code_commit"], "f"*40)

    def test_contradictory_or_wrong_typed_header_cannot_be_overwritten(self):
        for key, value in (("model_performance_measured", True), ("model_calls", False), ("new_mathematical_cores", 999),
                           ("new_canonical_formal_admissions", 999), ("blind_test", True), ("isolated", 0)):
            with self.assertRaises(ValueError):
                self.checked(lambda r, k=key, v=value: r.update({k: v}))

    def test_axiom_type_and_negative_kernel_claim_are_rejected(self):
        for change in (lambda r: r["results"][0]["final_replay"].update(axioms=""),
                       lambda r: r["results"][0]["final_replay"].update(axioms=["sorryAx"]),
                       lambda r: r["results"][0]["negative_controls"]["wrong_target"].update(kernel_checked=True)):
            with self.assertRaises(ValueError):
                self.checked(change)

    def test_copied_positive_root_is_not_a_fresh_final_replay(self):
        def copy_root(report):
            positive = deepcopy(report["results"][0]["positive_obligations"][0])
            positive.pop("node_id")
            report["results"][0]["final_replay"] = positive
        with self.assertRaisesRegex(ValueError, "distinct"):
            self.checked(copy_root)

    def test_malformed_request_identity_and_truncated_pipeline_are_rejected(self):
        for change in (lambda r: r["results"][0]["final_replay"].update(request_hash="not-a-hash"),
                       lambda r: r["results"][0]["final_replay"].update(execution_id=""),
                       lambda r: r["pipeline_source_hashes_lf"].pop("second")):
            with self.assertRaises(ValueError):
                self.checked(change)


if __name__ == "__main__":
    unittest.main()
