"""Synthetic receipt-consistency tests; no Lean process or proof claim."""
import hashlib
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_authored_session import AuthoredReferenceVerifier
from qcb_core import digest
from qcb_integrity import text_sha
from qcb_learning_reference import (
    EVIDENCE_FIELDS,
    qualify,
    replay_references,
    validate_reference_results,
)
from qcb_learning_validity import challenge_task
from test_learning_validity import synthetic_probe


def engineered_receipt():
    probe = synthetic_probe()
    probe["gold"]["reference_proof"] = "by rfl"
    packet = {"probes": [probe], "snapshot_id": "software-fixture", "library_revision": "a" * 40,
              "proof_inputs_sha256": "b" * 64, "lean_toolchain": "leanprover/lean4:v4.29.1"}
    task = challenge_task(probe, "holds", snapshot_id=packet["snapshot_id"], library_revision=packet["library_revision"])
    replays, evidence = [], []
    cases = [(probe["gold"]["reference_proof"], False, "verified", 0, []),
             (probe["gold"]["reference_proof"], True, "verified", 0, []),
             ("by exact True.intro", False, "compile_error", 1, []),
             ("by sorry", False, "compile_error", 0, ["sorryAx"])]
    for i, (proof, final, status, code, axioms) in enumerate(cases):
        nonce = format(i+1, "032x")
        meta = {"request_id": "2" if final else "1", "timeout_seconds": 120, "deadline_monotonic": 12345.0 + i}
        request = {"schema_version": "qcb.obligation_check.v1", "task_hash": digest(task), "node_id": "assessment_root",
                   "imports": task["imports"], "target": task["nodes"][0]["target"], "universe_parameters": [],
                   "library_revision": packet["library_revision"], "proof": proof, "dependency_order": [], "dependencies": {},
                   "final_replay": final, **meta}
        source = AuthoredReferenceVerifier._source(SimpleNamespace(task=task, nodes={}, allowlist={}), request, nonce)
        replay = {"node_id": "assessment_root", "request_hash": digest(request), "execution_id": nonce,
                  "final_replay": final, "proof_sha256": hashlib.sha256(proof.encode()).hexdigest(),
                  "source_sha256": hashlib.sha256(source.encode()).hexdigest(), "runtime_checkout_commit": packet["library_revision"],
                  "proof_inputs_sha256": packet["proof_inputs_sha256"], "actual_lean_version": "Lean (version 4.29.1, synthetic software fixture)",
                  "pipeline_sha256": hashlib.sha256((B / "src/qcb_authored_session.py").read_bytes()).hexdigest(),
                  "pipeline_source_sha256_lf": text_sha(B / "src/qcb_authored_session.py"), "exit_code": code,
                  "status": status, "axioms": axioms, "failure": None, "elapsed_seconds": 0.1,
                  "execution_class": "trusted_local_authored_reference", "isolated": False, "request_metadata": meta}
        reply = {k: deepcopy(replay[k]) for k in EVIDENCE_FIELDS if k in replay}
        reply.update(kernel_checked=status == "verified", failure_class=None if status == "verified" else "IMPLEMENTATION_FAILED")
        replays.append(replay)
        evidence.append(reply)
    row = {"probe_id": probe["probe_id"], "probe_digest": digest(probe), "task_hash": digest(task),
           "formal_target_sha256": digest(task["nodes"][0]["target"]), "gold_polarity": "holds",
           "submitted_status": "verified", "finish_status": "verified", "formal_root_checked": True,
           "submission_evidence": evidence[0], "final_evidence": evidence[1], "replays": replays,
           "negative_controls": [{"kind": "wrong_target", "status": "compile_error", "evidence": evidence[2]},
                                 {"kind": "sorry_axiom", "status": "compile_error", "evidence": evidence[3]}]}
    return packet, [row]


class LearningReferenceTests(unittest.TestCase):
    def setUp(self):
        self.packet, self.rows = engineered_receipt()

    def test_consistent_engineered_metadata_is_not_a_lean_or_model_execution(self):
        result = validate_reference_results(self.packet, self.rows)
        self.assertEqual(result, {"checked_probes": 1, "checked_replays": 4})
        self.assertNotIn("qualified", result)

    def test_no_alternate_directory_can_escape_the_committed_evidence_binding(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaisesRegex(ValueError, "fixed committed"):
            qualify(self.packet, evidence_dir=Path(tmp))

    def test_all_actual_source_request_and_pipeline_fields_are_required(self):
        for field in ("source_sha256", "request_hash", "pipeline_sha256", "pipeline_source_sha256_lf", "request_metadata"):
            rows = deepcopy(self.rows)
            del rows[0]["replays"][0][field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_reference_results(self.packet, rows)

    def test_environmental_failure_cannot_be_disguised_as_negative_type_rejection(self):
        rows = deepcopy(self.rows)
        for replay in rows[0]["replays"][2:]:
            replay.update(status="timeout", failure="timeout")
        with self.assertRaises(ValueError):
            validate_reference_results(self.packet, rows)

    def test_control_summary_needs_the_actual_matching_execution(self):
        for mutation in ("empty", "status", "proof", "execution", "kernel"):
            rows = deepcopy(self.rows)
            reply = rows[0]["negative_controls"][0]["evidence"]
            if mutation == "empty":
                rows[0]["negative_controls"][0]["evidence"] = {}
            elif mutation == "status":
                reply["status"] = "verified"
            elif mutation == "proof":
                reply["proof_sha256"] = "c" * 64
            elif mutation == "execution":
                reply["execution_id"] = "f" * 32
            else:
                reply["kernel_checked"] = True
            with self.subTest(mutation=mutation), self.assertRaises((ValueError, KeyError)):
                validate_reference_results(self.packet, rows)

    def test_generated_source_and_actual_request_are_reconstructed(self):
        for mutation in ("source", "deadline", "pipeline", "proof", "target"):
            rows = deepcopy(self.rows)
            replay = rows[0]["replays"][0]
            if mutation == "source":
                replay["source_sha256"] = "c" * 64
            elif mutation == "deadline":
                replay["request_metadata"]["deadline_monotonic"] += 1
            elif mutation == "pipeline":
                replay["pipeline_sha256"] = "c" * 64
            elif mutation == "proof":
                replay["proof_sha256"] = "c" * 64
                rows[0]["submission_evidence"]["proof_sha256"] = "c" * 64
            else:
                rows[0]["formal_target_sha256"] = "c" * 64
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_reference_results(self.packet, rows)

    def test_bool_integer_flags_and_wrong_compiler_exit_are_not_equivalent(self):
        for mutation in ("flag", "exit", "kernel", "axiom", "sorry"):
            rows = deepcopy(self.rows)
            if mutation == "flag":
                rows[0]["replays"][1]["final_replay"] = 1
            elif mutation == "exit":
                rows[0]["replays"][2]["exit_code"] = 0
            elif mutation == "kernel":
                rows[0]["final_evidence"]["kernel_checked"] = 1
            elif mutation == "axiom":
                rows[0]["replays"][0]["axioms"] = ["native_decide_fake_axiom"]
                rows[0]["submission_evidence"]["axioms"] = ["native_decide_fake_axiom"]
            else:
                rows[0]["replays"][3]["axioms"] = []
                rows[0]["negative_controls"][1]["evidence"]["axioms"] = []
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_reference_results(self.packet, rows)

    def test_fresh_replays_cannot_reuse_nonce_or_swap_initial_final(self):
        rows = deepcopy(self.rows)
        rows[0]["final_evidence"], rows[0]["submission_evidence"] = rows[0]["submission_evidence"], rows[0]["final_evidence"]
        with self.assertRaises(ValueError):
            validate_reference_results(self.packet, rows)
        rows = deepcopy(self.rows)
        rows[0]["replays"][3]["execution_id"] = rows[0]["replays"][0]["execution_id"]
        with self.assertRaises(ValueError):
            validate_reference_results(self.packet, rows)

    def test_negative_controls_bind_the_actual_runtime_and_target_too(self):
        for field, value in (("runtime_checkout_commit", "f" * 40), ("proof_inputs_sha256", "f" * 64),
                             ("actual_lean_version", "NO LEAN WAS RUN"), ("node_id", "another_root")):
            rows = deepcopy(self.rows)
            for replay in rows[0]["replays"][2:]:
                replay[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_reference_results(self.packet, rows)


class LearningReferenceProgressTests(unittest.IsolatedAsyncioTestCase):
    async def test_mid_control_deadline_preserves_every_completed_check(self):
        packet, rows = engineered_receipt()
        engineered = rows[0]
        progress = []

        class FakeVerifier:
            def __init__(self, *_args, **_kwargs):
                self.replays = []

        class FakeSession:
            state_id = "software-test-state"

            def __init__(self, _task, verifier, **_kwargs):
                self.verifier = verifier

            async def act(self, action):
                final = action["kind"] == "finish"
                wrong = action.get("proof") == "by exact True.intro"
                index = 2 if wrong else 1 if final else 0
                self.verifier.replays.append(deepcopy(engineered["replays"][index]))
                evidence = deepcopy(engineered["negative_controls"][0]["evidence"] if wrong else
                                    engineered["final_evidence"] if final else engineered["submission_evidence"])
                return {"status": evidence["status"], "final_replay" if final else "evidence": evidence}

            def report(self):
                return {"formal_root_checked": True}

        with (patch("qcb_learning_reference.check_semantics", return_value={}),
              patch("qcb_learning_reference.pipeline_identity", return_value={}),
              patch("qcb_learning_reference.read_json", return_value=packet),
              patch("qcb_learning_reference.subprocess.check_output", return_value="f" * 40),
              patch("qcb_learning_reference._RecordedAuthoredVerifier", FakeVerifier),
              patch("qcb_learning_reference.ProofSession", FakeSession),
              patch("qcb_learning_reference.monotonic", side_effect=[0, 1, 2, 2401]),
              self.assertRaises(TimeoutError)):
            await replay_references(packet, "not-used-by-software-fixture", progress=lambda row: progress.append(deepcopy(row)))
        self.assertEqual([r["phase"] for r in progress], ["positive_checks", "negative_control"])
        self.assertEqual([len(r["replays"]) for r in progress], [2, 3])
        self.assertEqual(progress[-1]["control"], "wrong_target")


if __name__ == "__main__":
    unittest.main()
