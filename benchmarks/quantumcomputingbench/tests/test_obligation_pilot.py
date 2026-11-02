"""Canonical binding, answer projection and authored-only worker contracts."""
import asyncio
import json
import subprocess
import sys
import time
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_authored_session import AuthoredReferenceVerifier
from qcb_core import digest, read_json
from qcb_curriculum import load_catalog
from qcb_obligation_pilot import FIXTURE, bind_cases, export_pilot
from qcb_proof_session import ProofSession, SessionLimits, proof_sha
from test_proof_session import FixtureVerifier, action, task


class PilotBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = read_json(FIXTURE)
        cls.catalog, cls.items, _ = load_catalog()
        cls.cases = bind_cases(cls.packet, cls.catalog, cls.items)

    def test_two_existing_cores_and_exact_roots_with_no_new_admission(self):
        self.assertEqual(len(self.cases), 2)
        self.assertEqual(sum(len(c["task"]["nodes"]) for c in self.cases), 10)
        for case in self.cases:
            self.assertEqual(set(case["references"]), {n["id"] for n in case["task"]["nodes"]})
            self.assertTrue(all("QuantumComputingBench.PilotMath" not in p for p in case["references"].values()))
            self.assertIn("existing_root_reviewed", case["task"]["alignment_status"])

    def test_stale_catalog_contract_split_root_or_source_fails_closed(self):
        mutations = [lambda p: p.update(catalog_hash="stale"),
                     lambda p: p.update(proof_inputs_sha256="stale"),
                     lambda p: p.update(lean_toolchain="stale"),
                     lambda p: p.update(cases=[]),
                     lambda p: p["cases"].pop(),
                     lambda p: p["cases"][0]["binding"].update(contract_hash="stale"),
                     lambda p: p["cases"][0]["binding"].update(split="train"),
                     lambda p: p["cases"][0]["nodes"][-1].update(target="True"),
                     lambda p: p["cases"][0]["source_bindings"][0].update(sha256_lf="stale"),
                     lambda p: p["cases"].append(deepcopy(p["cases"][0]))]
        for mutate in mutations:
            packet = deepcopy(self.packet)
            mutate(packet)
            with self.assertRaises(ValueError):
                bind_cases(packet, self.catalog, self.items)

    def test_agent_projection_excludes_all_proofs_answers_rubrics_and_interfaces(self):
        exported = export_pilot(self.cases, {"fixture_digest": digest(self.packet)})
        text = json.dumps(exported)
        for case in self.cases:
            for proof in [*case["references"].values(), *case["controls"].values(), case["wrong_reference"]["proof"]]:
                self.assertNotIn(json.dumps(proof)[1:-1], text)
        for entry in exported["tasks"]:
            self.assertNotIn("interfaces", entry["task"])
            self.assertNotIn("knowledge_assumption_rubric", entry["task"])
            self.assertEqual(entry["exposure"], "approved_interface")
        self.assertFalse(exported["blind_test"])
        self.assertEqual(exported["new_mathematical_cores"], 0)


class AuthoredWorkerTests(unittest.TestCase):
    def test_non_allowlisted_proof_never_reaches_lean_or_filesystem(self):
        backend = AuthoredReferenceVerifier.__new__(AuthoredReferenceVerifier)
        backend.task = task()
        backend.task_hash = digest(backend.task)
        backend.nodes = {n["id"]: n for n in backend.task["nodes"]}
        backend.revision = backend.task["library_revision"]
        backend.allowlist = {k: {proof_sha("by trivial")} for k in backend.nodes}
        backend.replays = []
        session = ProofSession(backend.task, backend)
        with patch("qcb_authored_session._run_reference", side_effect=AssertionError("must never execute")):
            result = asyncio.run(action(session, "submit", node_id="base", proof="by exact model_supplied_code"))
        self.assertEqual(result["failure_class"], "API_BLOCKED")
        self.assertEqual(backend.replays, [])

    def test_caller_timeout_waits_for_native_worker_cleanup_before_next_action(self):
        backend = AuthoredReferenceVerifier.__new__(AuthoredReferenceVerifier)
        state = {"active": 0, "peak": 0}

        def native(request):
            state["active"] += 1
            state["peak"] = max(state["peak"], state["active"])
            try:
                time.sleep(0.06)
            finally:
                state["active"] -= 1

        backend._verify = native

        async def run():
            session = ProofSession(task(), backend, limits=SessionLimits(check_seconds=0.005))
            for _ in range(2):
                result = await action(session, "submit", node_id="base", proof="by trivial")
                self.assertEqual(result["failure_class"], "ENV_BLOCKED")
                self.assertEqual(state["active"], 0)
            self.assertEqual(state["peak"], 1)
        asyncio.run(run())

    def test_subprocess_runtime_errors_are_recorded_as_environment_not_refutation(self):
        for error in (subprocess.CalledProcessError(128, ["git"]), subprocess.TimeoutExpired(["git"], 10)):
            backend = FixtureVerifier()

            async def fail(request, failure=error):
                raise failure

            backend.verify = fail
            session = ProofSession(task(), backend)
            result = asyncio.run(action(session, "submit", node_id="base", proof="by trivial"))
            self.assertEqual(result["failure_class"], "ENV_BLOCKED")
            self.assertEqual(len(session.events), 1)
            self.assertEqual(len(session.report()["attempt_evidence"]["base"]), 1)

    def test_complete_observations_and_responses_respect_character_ceiling(self):
        sample = task()
        sample["nodes"] = [{"id": "leaf" + str(i), "target": "True", "depends_on": []} for i in range(31)]
        sample["nodes"].append({"id": "root", "target": "True", "depends_on": [n["id"] for n in sample["nodes"]]})

        class LongError(FixtureVerifier):
            async def verify(self, request):
                reply = await super().verify(request)
                reply.update(status="compile_error", diagnostics="large actual diagnostic " * 300)
                return reply

        async def run():
            session = ProofSession(sample, LongError(), limits=SessionLimits(max_actions=40, max_verifier_calls=40,
                                                                           max_observation_chars=8192))
            for i in range(31):
                response = await action(session, "submit", node_id="leaf" + str(i), proof="by trivial")
                self.assertLessEqual(len(json.dumps(response, ensure_ascii=False)), 8192)
                self.assertLessEqual(len(json.dumps(session.observation(), ensure_ascii=False)), 8192)
            self.assertEqual(len(session.report()["attempt_evidence"]["leaf0"][0]["diagnostics"]), 4000)
        asyncio.run(run())


if __name__ == "__main__":
    unittest.main()
