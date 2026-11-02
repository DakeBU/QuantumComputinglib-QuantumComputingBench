"""Bounded obligation interaction is distinct from kernel or model success."""
import asyncio
import sys
import unittest
from copy import deepcopy
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_proof_session import TASK_SCHEMA, ProofSession, SessionLimits, bound_reply


def task():
    return {"schema_version": TASK_SCHEMA, "core_id": "qcb-core-fixture", "contract_hash": "f" * 64,
            "family": "fixture", "split": "train", "snapshot_id": "fixture-snapshot",
            "library_revision": "a" * 40, "imports": ["Mathlib.Tactic"], "question": "Prove a conjunction.",
            "assumptions": [], "conventions": [], "alignment_status": "authored_protocol_fixture_only",
            "root_id": "root", "nodes": [
                {"id": "base", "target": "True", "depends_on": []},
                {"id": "middle", "target": "True ∧ True", "depends_on": ["base"]},
                {"id": "root", "target": "(True ∧ True) ∧ True", "depends_on": ["middle"]}],
            "interfaces": [{"name": "True.intro", "type": "True", "module": "Init",
                            "source_node_id": "fixture:True.intro"}]}


class FixtureVerifier:
    execution_class = "fixture"
    isolated = False

    def __init__(self):
        self.requests = []

    async def verify(self, request):
        self.requests.append(deepcopy(request))
        good = request["proof"] != "by exact missing_lemma"
        return bound_reply(request, status="verified" if good else "compile_error",
                           execution_id="execution-" + str(len(self.requests)),
                           diagnostics="" if good else "unknown identifier missing_lemma")


async def action(session, kind, **payload):
    return await session.act({"kind": kind, "state_id": session.state_id, **payload})


class ProofSessionTests(unittest.TestCase):
    def run_async(self, code):
        return asyncio.run(code)

    def test_default_verifier_is_blocked_and_does_not_call_lean(self):
        session = ProofSession(task())
        result = self.run_async(action(session, "submit", node_id="base", proof="by trivial"))
        self.assertEqual(result["failure_class"], "ENV_BLOCKED")
        self.assertFalse(session.report()["formal_root_checked"])

    def test_constructor_rejects_cycles_disconnected_nodes_gold_and_unknown_imports(self):
        changes = [lambda t: t["nodes"][0]["depends_on"].append("root"),
                   lambda t: t["nodes"].append({"id": "unrelated", "target": "True", "depends_on": []}),
                   lambda t: t.update(reference_proof="SECRET"),
                   lambda t: t["imports"].append("Mathlib\naxiom injected : False")]
        for change in changes:
            row = task()
            change(row)
            with self.assertRaises(ValueError):
                ProofSession(row)

    def test_task_and_observations_are_copied_and_closed_book_hides_interface(self):
        row = task()
        session = ProofSession(row, exposure="closed_book")
        row["nodes"][0]["target"] = "False"
        public = session.agent_input()
        self.assertEqual(public["task"]["nodes"][0]["target"], "True")
        self.assertNotIn("interfaces", public["task"])
        self.assertNotIn("True.intro", str(public))
        public["task"]["nodes"][0]["target"] = "False"
        self.assertEqual(session.agent_input()["task"]["nodes"][0]["target"], "True")
        result = self.run_async(action(session, "search", query="True"))
        self.assertEqual(result["failure_class"], "API_BLOCKED")

    def test_retrieval_returns_only_scoped_statements_and_no_mathematical_credit(self):
        session = ProofSession(task())
        result = self.run_async(action(session, "search", query="True"))
        self.assertEqual(result["entries"], task()["interfaces"])
        self.assertFalse(result["mathematical_credit"])
        result["entries"][0]["type"] = "False"
        self.assertEqual(self.run_async(action(session, "search", query="True"))["entries"][0]["type"], "True")

    def test_unknown_receipt_or_statement_fields_cannot_be_submitted(self):
        session = ProofSession(task(), FixtureVerifier())
        for extra in ({"target": "False"}, {"receipt": {"verified": True}}, {"imports": ["Bad"]}):
            request = {"kind": "submit", "state_id": session.state_id, "node_id": "base", "proof": "by trivial", **extra}
            result = self.run_async(session.act(request))
            self.assertEqual(result["failure_class"], "API_BLOCKED")
        self.assertEqual(session.report()["metrics"]["verifier_calls"], 0)

    def test_unchecked_dependencies_and_stale_state_are_rejected(self):
        session = ProofSession(task(), FixtureVerifier())
        old = session.state_id
        blocked = self.run_async(action(session, "submit", node_id="root", proof="by trivial"))
        self.assertEqual(blocked["failure_class"], "API_BLOCKED")
        stale = self.run_async(session.act({"kind": "search", "state_id": old, "query": "True"}))
        self.assertEqual(stale["failure_class"], "API_BLOCKED")

    def test_repair_and_fresh_final_replay_do_not_become_model_scores(self):
        async def run():
            backend = FixtureVerifier()
            session = ProofSession(task(), backend)
            wrong = await action(session, "submit", node_id="base", proof="by exact missing_lemma")
            self.assertEqual(wrong["failure_class"], "IMPLEMENTATION_FAILED")
            self.assertIn("missing_lemma", wrong["observation"]["nodes"][0]["last_feedback"]["diagnostics"])
            for node in ("base", "middle", "root"):
                self.assertEqual((await action(session, "submit", node_id=node, proof="by trivial"))["status"], "verified")
            self.assertFalse(session.report()["protocol_complete"])
            await action(session, "finish")
            report = session.report()
            self.assertTrue(report["protocol_complete"])
            self.assertFalse(report["formal_root_checked"])
            self.assertFalse(report["model_performance_measured"])
            self.assertIsNone(report["knowledge_semantic_score"])
            self.assertEqual(report["metrics"]["repair_attempts"], 1)
            self.assertEqual(report["metrics"]["verifier_calls"], 5)
            final = backend.requests[-1]
            self.assertTrue(final["final_replay"])
            self.assertEqual(final["dependency_order"], ["base", "middle"])
            self.assertIn("proof", final["dependencies"]["base"])
            self.assertNotIn("dependencies", session.agent_input())
        self.run_async(run())

    def test_root_only_control_does_not_require_artificial_subgoal_execution(self):
        async def run():
            session = ProofSession(task(), FixtureVerifier(), mode="root_only")
            self.assertEqual((await action(session, "submit", node_id="base", proof="by trivial"))["status"], "rejected")
            await action(session, "submit", node_id="root", proof="by trivial")
            await action(session, "finish")
            self.assertTrue(session.report()["protocol_complete"])
            self.assertEqual(session.report()["metrics"]["accepted_obligations"], 1)
        self.run_async(run())

    def test_axiom_stale_receipt_or_missing_kernel_evidence_fails_closed(self):
        for corruption in (lambda r: r.update(request_hash="old"), lambda r: r.update(axioms=["sorryAx"]),
                           lambda r: r.update(execution_id=""), lambda r: r.update(kernel_checked=False)):
            class Bad(FixtureVerifier):
                execution_class = "trusted_local_authored_reference"

                async def verify(self, request, change=corruption):
                    reply = await super().verify(request)
                    reply["kernel_checked"] = True
                    change(reply)
                    return reply

            session = ProofSession(task(), Bad())
            result = self.run_async(action(session, "submit", node_id="base", proof="by trivial"))
            self.assertEqual(result["failure_class"], "API_BLOCKED")
            self.assertEqual(session.report()["metrics"]["accepted_obligations"], 0)

    def test_trusted_reply_flags_are_not_isolated_model_evaluation(self):
        class KernelFixture(FixtureVerifier):
            execution_class = "trusted_local_authored_reference"

            async def verify(self, request):
                reply = await super().verify(request)
                reply["kernel_checked"] = True
                reply["axioms"] = ["propext"]
                return reply

        async def run():
            session = ProofSession(task(), KernelFixture(), mode="root_only")
            await action(session, "submit", node_id="root", proof="by trivial")
            await action(session, "finish")
            report = session.report()
            self.assertTrue(report["formal_root_checked"])
            self.assertFalse(report["isolated_prediction_success"])
            self.assertFalse(report["model_performance_measured"])
        self.run_async(run())

    def test_runtime_claim_cannot_enable_isolated_execution(self):
        backend = FixtureVerifier()
        backend.isolated = True
        with self.assertRaisesRegex(ValueError, "not enabled"):
            ProofSession(task(), backend)

    def test_deadlines_budgets_and_oversize_inputs_are_bounded(self):
        class Slow(FixtureVerifier):
            async def verify(self, request):
                await asyncio.sleep(1)

        session = ProofSession(task(), Slow(), limits=SessionLimits(check_seconds=0.01))
        self.assertEqual(self.run_async(action(session, "submit", node_id="base", proof="by trivial"))["failure_class"], "ENV_BLOCKED")
        session = ProofSession(task(), FixtureVerifier(), limits=SessionLimits(max_actions=1))
        self.run_async(action(session, "search", query="True"))
        for _ in range(5):
            self.assertEqual(self.run_async(action(session, "finish"))["failure_class"], "BUDGET_EXHAUSTED")
        self.assertEqual(len(session.events), 1)
        session = ProofSession(task(), FixtureVerifier(), limits=SessionLimits(max_proof_chars=8))
        result = self.run_async(action(session, "submit", node_id="base", proof="a" * 9000))
        self.assertEqual(result["failure_class"], "API_BLOCKED")
        self.assertLess(len(str(session.events)), 5000)

    def test_concurrent_stale_actions_do_not_race_evidence(self):
        async def run():
            session = ProofSession(task(), FixtureVerifier())
            request = {"kind": "submit", "state_id": session.state_id, "node_id": "base", "proof": "by trivial"}
            results = await asyncio.gather(session.act(request), session.act(request))
            self.assertEqual(sorted(r["status"] for r in results), ["rejected", "verified"])
            self.assertEqual(session.report()["metrics"]["verifier_calls"], 1)
        self.run_async(run())

    def test_knowledge_explanation_requires_independent_grading(self):
        session = ProofSession(task(), FixtureVerifier())
        result = self.run_async(action(session, "explain", answer="A proposed mathematical explanation."))
        self.assertIsNone(result["semantic_score"])
        self.assertEqual(session.report()["metrics"]["verifier_calls"], 0)


if __name__ == "__main__":
    unittest.main()
