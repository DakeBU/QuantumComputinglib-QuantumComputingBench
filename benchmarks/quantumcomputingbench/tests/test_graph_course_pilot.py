"""Reviewed data and replay-driver software mocks; these tests never run Lean."""
import asyncio
import importlib.util
import secrets
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_core import digest, read_json
from qcb_graph_course_pilot import FIXTURE, check_semantics, load_candidates
from qcb_proof_session import bound_reply, proof_sha

spec = importlib.util.spec_from_file_location("qcb_course_cli_test", B / "scripts/lean_course.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class GraphCoursePilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases, cls.identity, cls.catalog, cls.graph = load_candidates()

    def test_exact_five_shared_targets_and_complete_inspected_control_allowlists(self):
        self.assertEqual(len(self.cases), 5)
        self.assertEqual(sum(len(c["references"]) for c in self.cases), 13)
        self.assertEqual({c["task"]["split"] for c in self.cases}, {"train", "dev"})
        for case in self.cases:
            self.assertEqual(set(case["references"]), {n["id"] for n in case["task"]["nodes"]})
            for proof in [*case["controls"].values(), *case["negative_controls"].values()]:
                self.assertIn(proof, case["allowed_proofs"][case["task"]["root_id"]])

    def test_stale_target_rejects_even_with_updated_local_task_hash(self):
        packet = read_json(FIXTURE)
        cases = deepcopy(self.cases)
        case = next(c for c in cases if c["task"]["core_id"] == "qcb-core-be-105")
        next(n for n in case["task"]["nodes"] if n["id"] == case["task"]["root_id"])["target"] = "True"
        cores = {c["core_id"]: c for c in self.catalog["cores"]}
        with self.assertRaises(ValueError):
            check_semantics(packet, cases, cores)

    def test_typing_universes_cannot_silently_change_after_review(self):
        packet = read_json(FIXTURE); cases = deepcopy(self.cases)
        cases[0]["task"]["universe_parameters"] = ["u"]
        cores = {c["core_id"]: c for c in self.catalog["cores"]}
        with self.assertRaises(ValueError):
            check_semantics(packet, cases, cores)

    def test_mock_replay_driver_keeps_controls_and_rejected_axioms_distinct(self):
        wrong = {proof_sha(c["negative_controls"]["wrong_target"]) for c in self.cases}

        class SoftwareMockOnly:
            # This branch label exercises driver serialization. It is never
            # written as a reference receipt or claimed as kernel evidence.
            execution_class = "trusted_local_authored_reference"
            isolated = False

            def __init__(self, task, allowlist, build_root):
                self.replays = []

            async def verify(self, request):
                negative = request["proof"] == "by sorry" or proof_sha(request["proof"]) in wrong
                axioms = ["sorryAx"] if request["proof"] == "by sorry" else []
                return bound_reply(request, status="compile_error" if negative else "verified",
                                   execution_id=secrets.token_hex(16), kernel_checked=not negative, axioms=axioms)

        raw = []
        with patch.object(cli, "AuthoredReferenceVerifier", SoftwareMockOnly):
            result = asyncio.run(cli.check_references(self.cases, self.identity, "not-used-by-mock", raw, "f"*40))
        self.assertTrue(result["passed"])
        self.assertFalse(result["standalone_controls_are_completed_protocol_sessions"])
        self.assertEqual(result["model_calls"], 0)
        self.assertEqual(len(raw), 14)
        self.assertTrue(all("sorryAx" in r["negative_controls"]["sorry_axiom"]["axioms"] for r in result["results"]))
        self.assertTrue(all(r["final_replay"]["kernel_checked"] for r in result["results"]))
        # Prohibit treating fixture serialization output as actual stored gold.
        self.assertNotEqual(result.get("receipt_digest"), digest(result))


if __name__ == "__main__":
    unittest.main()
