"""Protocol mocks measure control/usage boundaries, never model accuracy."""
import asyncio
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_core import read_json
from qcb_model_loop import (
    ScriptedFixtureProvider,
    fixture_config,
    response_envelope,
    run_episode,
    validate_config,
)
from qcb_obligation_pilot import R
from test_evaluation_registry import context


class ModelLoopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.view = context()[3]["qcb-agentic-sp-007-v1"]

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="qcb-loop-test-")
        self.addCleanup(self.temp.cleanup)
        self.destination = Path(self.temp.name).resolve() / "episode"

    def execute(self, config=None, **kwargs):
        return asyncio.run(run_episode(self.view, config or fixture_config(), self.destination, **kwargs))

    def real_config(self, *, purpose="formal_proof"):
        config = fixture_config(purpose=purpose)
        config.update(provider_kind="operator_adapter")
        config["model"].update(id="unit-test/mock-endpoint", revision="a" * 40)
        config["adapter"] = {"id": "unit-test:provider", "revision_sha256": "b" * 64}
        return config

    def test_dry_run_and_blocked_formal_mode_never_construct_provider(self):
        calls = []

        def forbidden():
            calls.append("constructed")
            raise AssertionError("must not initialize a model")

        plan = self.execute(self.real_config(), authorized=False, provider_factory=forbidden)
        blocked = self.execute(self.real_config(), authorized=True, provider_factory=forbidden)
        self.assertEqual(plan["status"], "dry_run")
        self.assertEqual(blocked["status"], "ENV_BLOCKED")
        self.assertFalse(plan["episode_directory_created"])
        self.assertFalse(blocked["provider_constructed"])
        self.assertEqual(blocked["provider_calls"], 0)
        self.assertEqual(calls, [])
        self.assertFalse(self.destination.exists())

    def test_fixture_exercises_failure_repair_finish_and_no_formal_or_model_credit(self):
        result = self.execute(fixture=True)
        self.assertEqual(result["status"], "fixture_protocol_complete")
        self.assertTrue(result["session_report"]["protocol_complete"])
        self.assertFalse(result["session_report"]["formal_root_checked"])
        self.assertFalse(result["formal_proof_success"])
        self.assertFalse(result["model_generation_observed"])
        self.assertEqual(result["model_calls_confirmed"], 0)
        self.assertEqual(result["usage_kind"], "synthetic_fixture_values")
        self.assertEqual(result["session_report"]["metrics"]["repair_attempts"], 1)
        persisted = read_json(self.destination / "episode.json")
        self.assertEqual(persisted["status"], result["status"])
        self.assertEqual(len(persisted["calls"]), result["provider_calls"])

    def test_first_provider_input_contains_no_reference_controls_or_gold(self):
        seen = []

        class Capture(ScriptedFixtureProvider):
            async def respond(self, request):
                seen.append(deepcopy(request))
                return await super().respond(request)

        self.execute(fixture=True, provider_factory=Capture)
        encoded = json.dumps(seen[0])
        self.assertNotIn("reference_checkpoint", encoded)
        for cases, _ in context()[1].values():
            for case in cases:
                for proof in [*case["references"].values(), *case["controls"].values()]:
                    self.assertNotIn(json.dumps(proof)[1:-1], encoded)

    def test_explanation_only_never_executes_proof_actions_or_exposes_lean_context(self):
        seen = []

        class MockEndpoint:
            is_fixture = False
            implementation_sha256 = "b" * 64

            async def respond(self, request):
                seen.append(deepcopy(request))
                state = request["input"]["observation"]["state_id"]
                action = ({"kind": "submit", "state_id": state, "node_id": "root", "proof": "model-owned-data",
                           "receipt": {"kernel_checked": True}} if len(seen) == 1 else
                          {"kind": "explain", "state_id": state, "answer": "A mock mathematical response, not a real model result."})
                return response_envelope(request, action, fixture=False,
                                         usage={"input_tokens": 2, "output_tokens": 2, "endpoint_cost_usd": 0, "source": "endpoint_reported"})

        result = self.execute(self.real_config(purpose="explanation_only"), authorized=True, provider_factory=MockEndpoint)
        self.assertEqual(result["status"], "explanation_recorded")
        self.assertEqual(result["session_report"]["metrics"]["verifier_calls"], 0)
        self.assertFalse(result["formal_proof_success"])
        self.assertIsNone(result["knowledge_semantic_score"])
        for request in seen:
            self.assertNotIn("task", request["input"])
            self.assertNotIn("nodes", request["input"]["observation"])
            self.assertNotIn("QuantumBlockEncoding", json.dumps(request["messages"]))

    def test_unknown_usage_timeout_freezes_reservation_and_does_not_retry(self):
        class Slow(ScriptedFixtureProvider):
            async def respond(self, request):
                await asyncio.sleep(1)

        config = fixture_config()
        config["limits"]["max_call_seconds"] = 0.01
        result = self.execute(config, fixture=True, provider_factory=Slow)
        self.assertEqual(result["status"], "ENV_BLOCKED")
        self.assertEqual(result["provider_calls"], 1)
        self.assertTrue(result["endpoint_usage_unreconciled"])
        self.assertIsNone(result["calls"][0]["usage"])
        self.assertGreater(result["calls"][0]["reservation"]["output_tokens"], 0)
        with self.assertRaises(FileExistsError):
            self.execute(config, fixture=True, provider_factory=Slow)

    def test_reservation_precedes_generation_and_nl_error_feedback_stays_blinded(self):
        destination, seen = self.destination, []

        class InvalidThenExplain:
            is_fixture = False
            implementation_sha256 = "b" * 64

            async def respond(self, request):
                recorded = read_json(destination / "episode.json")
                call = recorded["calls"][-1]
                self_assert = (recorded["endpoint_usage_unreconciled"] is True
                               and call["status"] == "in_flight" and call["usage"] is None
                               and call["reservation"]["output_tokens"] == request["max_output_tokens"])
                if not self_assert:
                    raise AssertionError("pre-call reservation must already be durable")
                seen.append(deepcopy(request))
                action = {"kind": "explain", "state_id": request["input"]["observation"]["state_id"],
                          "answer": "" if len(seen) == 1 else "Mock explanation for protocol testing."}
                return response_envelope(request, action, fixture=False,
                                         usage={"input_tokens": 2, "output_tokens": 2,
                                                "endpoint_cost_usd": 0, "source": "endpoint_reported"})

        result = self.execute(self.real_config(purpose="explanation_only"), authorized=True, provider_factory=InvalidThenExplain)
        self.assertEqual(result["status"], "explanation_recorded")
        self.assertEqual(len(seen), 2)
        first_feedback = seen[1]["history"][0]["tool_response"]
        self.assertNotIn("observation", first_feedback)
        self.assertEqual(result["session_report"]["metrics"]["verifier_calls"], 0)
        self.assertNotIn("QuantumBlockEncoding", json.dumps(seen[1]["messages"]))

    def test_unknown_or_unbound_receipt_and_missing_telemetry_fail_closed(self):
        class Forged(ScriptedFixtureProvider):
            async def respond(self, request):
                response = await super().respond(request)
                response.update(kernel_checked=True)
                return response

        result = self.execute(fixture=True, provider_factory=Forged)
        self.assertEqual(result["status"], "API_BLOCKED")
        self.assertTrue(result["endpoint_usage_unreconciled"])
        self.assertEqual(result["session_report"]["metrics"]["verifier_calls"], 0)

    def test_falsy_real_telemetry_is_never_replaced_with_invented_counts(self):
        for index, invalid in enumerate(({}, [], False, 0)):
            self.destination = Path(self.temp.name) / ("bad-usage-" + str(index))

            class EmptyTelemetry:
                is_fixture = False
                implementation_sha256 = "b" * 64

                async def respond(self, request, payload=invalid):
                    action = {"kind": "explain", "state_id": request["input"]["observation"]["state_id"],
                              "answer": "Mock answer with missing telemetry."}
                    return response_envelope(request, action, fixture=False, usage=payload)

            result = self.execute(self.real_config(purpose="explanation_only"), authorized=True, provider_factory=EmptyTelemetry)
            self.assertEqual(result["status"], "API_BLOCKED")
            self.assertTrue(result["endpoint_usage_unreconciled"])
            self.assertEqual(result["totals"]["input_tokens"], 0)
            self.assertEqual(result["model_calls_confirmed"], 0)

    def test_cost_violation_is_recorded_not_clamped_to_the_limit(self):
        class Overspend(ScriptedFixtureProvider):
            async def respond(self, request):
                response = await super().respond(request)
                response["usage"]["endpoint_cost_usd"] = 1
                return response

        result = self.execute(fixture=True, provider_factory=Overspend)
        self.assertEqual(result["status"], "ADAPTER_LIMIT_VIOLATION")
        self.assertEqual(result["totals"]["endpoint_cost_usd"], 1)
        self.assertEqual(result["provider_calls"], 1)

    def test_token_call_and_byte_ceilings_stop_without_silent_history_truncation(self):
        config = fixture_config()
        config["limits"]["max_total_input_tokens"] = 1
        result = self.execute(config, fixture=True)
        self.assertEqual(result["status"], "BUDGET_EXHAUSTED")
        self.assertEqual(result["provider_calls"], 1)
        self.destination = self.destination.parent / "byte-limit"
        config = fixture_config()
        config["limits"]["max_request_bytes"] = 100
        result = self.execute(config, fixture=True)
        self.assertEqual(result["provider_calls"], 0)
        self.assertEqual(result["status"], "BUDGET_EXHAUSTED")

    def test_exhausted_tool_budget_prevents_more_provider_calls(self):
        config = fixture_config()
        config["session_limits"]["max_actions"] = 1
        result = self.execute(config, fixture=True)
        self.assertEqual(result["status"], "BUDGET_EXHAUSTED")
        self.assertEqual(result["provider_calls"], 1)
        self.assertEqual(result["actions_attempted"], 1)
        self.destination = self.destination.parent / "verifier-budget"
        config = fixture_config()
        config["session_limits"]["max_verifier_calls"] = 1
        result = self.execute(config, fixture=True)
        self.assertEqual(result["status"], "BUDGET_EXHAUSTED")
        self.assertEqual(result["provider_calls"], 3)  # explain, search, expected fixture error
        self.assertEqual(result["session_report"]["metrics"]["verifier_calls"], 1)

    def test_sync_or_wrong_revision_adapters_cannot_generate(self):
        generated = []

        class Sync:
            is_fixture = True
            implementation_sha256 = fixture_config()["adapter"]["revision_sha256"]

            def respond(self, request):
                generated.append(True)

        result = self.execute(fixture=True, provider_factory=Sync)
        self.assertEqual(result["status"], "API_BLOCKED")
        self.assertEqual(generated, [])
        self.assertEqual(result["provider_calls"], 0)

    def test_invalid_profiles_and_public_raw_destinations_are_rejected(self):
        config = self.real_config()
        config["model"]["revision"] = "main"
        with self.assertRaises(ValueError):
            validate_config(config)
        config = fixture_config()
        config["limits"]["max_calls"] = 80
        with self.assertRaises(ValueError):
            validate_config(config)
        with self.assertRaises(ValueError):
            asyncio.run(run_episode(self.view, fixture_config(), R / "_out/forbidden-model-raw", fixture=True))
        with self.assertRaises(ValueError):
            response_envelope({}, {}, fixture=False)


if __name__ == "__main__":
    unittest.main()
