"""Bounded provider-neutral action loop; no model or compiler imported here.

Providers are trusted operator adapters with an async respond(request) method.
They must enforce request token/cost/transport limits at the endpoint and report
real usage. Cooperative cancellation is not a remote-job or resource sandbox.
Formal model execution stays blocked before provider construction. Fixture
execution uses a simulation verifier, never the authored-reference executor.
"""
from __future__ import annotations

import asyncio
import inspect
import json
import math
import re
import secrets
import time
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

from qcb_core import digest, write_json
from qcb_integrity import text_sha
from qcb_obligation_pilot import R
from qcb_proof_session import ProofSession, SessionLimits, bound_reply, validate_task

_LIMITS = {"max_calls", "max_call_input_tokens", "max_call_output_tokens", "max_total_input_tokens",
           "max_total_output_tokens", "max_request_bytes", "max_response_bytes", "max_call_seconds",
           "max_wall_seconds", "max_total_endpoint_cost_usd", "max_call_endpoint_cost_usd"}


def _harness_sources():
    base = Path(__file__).resolve().parent
    names = ("qcb_model_loop.py", "qcb_evaluation_registry.py", "qcb_proof_session.py", "qcb_core.py", "qcb_operator_profile.py")
    paths = [base / name for name in names]
    paths.extend((base.parent / "scripts/evaluate_agentic.py", base.parent / "schemas/operator-run-config-v1.schema.json"))
    return {str(path.relative_to(R)).replace("\\", "/"): text_sha(path) for path in paths}


def validate_config(config):
    if (not isinstance(config, dict) or set(config) != {"schema_version", "provider_kind", "adapter", "model", "sampling", "condition", "limits", "session_limits"}
            or config["schema_version"] != "qcb.agentic_run_config.v1"
            or config["provider_kind"] not in {"fixture", "operator_adapter"}):
        raise ValueError("unexpected model-loop configuration")
    adapter = config["adapter"]
    if (not isinstance(adapter, dict) or set(adapter) != {"id", "revision_sha256"}
            or not isinstance(adapter["id"], str) or not adapter["id"].strip()
            or not isinstance(adapter["revision_sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", adapter["revision_sha256"])):
        raise ValueError("operator adapter identity and implementation digest required")
    model = config["model"]
    if (not isinstance(model, dict) or set(model) != {"id", "revision", "chat_template_sha256"}
            or any(not isinstance(v, str) or not v.strip() for v in model.values())
            or not re.fullmatch(r"[0-9a-f]{64}", model["chat_template_sha256"])):
        raise ValueError("explicit model, checkpoint revision and actual template digest required")
    if (model["id"].startswith("fixture:") != (config["provider_kind"] == "fixture")
            or config["provider_kind"] == "fixture" and model["revision"] != "fixture"):
        raise ValueError("fixture accounting cannot be labelled as an actual model checkpoint")
    if config["provider_kind"] != "fixture" and not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", model["revision"]):
        raise ValueError("operator model revision must identify a pinned snapshot/artifact, not a floating tag")
    sampling = config["sampling"]
    if (not isinstance(sampling, dict) or set(sampling) != {"seed", "temperature", "top_p", "thinking_mode"}
            or type(sampling["seed"]) is not int or not 0 <= sampling["seed"] <= 2**32-1
            or type(sampling["temperature"]) not in (int, float) or not math.isfinite(sampling["temperature"])
            or not 0 <= sampling["temperature"] <= 2
            or type(sampling["top_p"]) not in (int, float) or not math.isfinite(sampling["top_p"])
            or not 0 < sampling["top_p"] <= 1 or sampling["thinking_mode"] not in {"enabled", "disabled", "unspecified"}):
        raise ValueError("bounded explicit sampling settings required")
    condition = config["condition"]
    if (not isinstance(condition, dict) or set(condition) != {"purpose", "mode", "exposure"}
            or condition["purpose"] not in {"formal_proof", "explanation_only"}
            or condition["mode"] not in {"root_only", "proof_dag"}
            or condition["exposure"] not in {"closed_book", "approved_interface"}
            or condition["purpose"] == "explanation_only" and condition["exposure"] != "closed_book"):
        raise ValueError("unsupported frozen evaluation condition")
    limits = config["limits"]
    if not isinstance(limits, dict) or set(limits) != _LIMITS:
        raise ValueError("all call, token, byte, time and endpoint-spend ceilings required")
    for key in _LIMITS:
        value = limits[key]
        is_cost = key.endswith("cost_usd")
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0 or not is_cost and value == 0:
            raise ValueError("limits must be finite; only endpoint cost ceilings may be zero")
        if key not in {"max_call_seconds", "max_wall_seconds"} and not is_cost and type(value) is not int:
            raise ValueError("call/token/byte limits must be integers")
    if (limits["max_calls"] > 32 or limits["max_wall_seconds"] > 600
            or limits["max_call_seconds"] > limits["max_wall_seconds"]
            or limits["max_request_bytes"] > 2_000_000 or limits["max_response_bytes"] > 1_000_000
            or limits["max_call_endpoint_cost_usd"] > limits["max_total_endpoint_cost_usd"]):
        raise ValueError("pilot ceilings exceed the supported bounded profile")
    if (not isinstance(config["session_limits"], dict)
            or set(config["session_limits"]) != set(asdict(SessionLimits()))):
        raise ValueError("explicit complete tool-session ceilings required")
    session_limits = SessionLimits(**config["session_limits"])
    if session_limits.wall_seconds > limits["max_wall_seconds"]:
        raise ValueError("tool session cannot outlive the model-loop ceiling")
    return deepcopy(config)


def fixture_config(*, purpose="formal_proof", mode="proof_dag", exposure="approved_interface"):
    return {"schema_version": "qcb.agentic_run_config.v1", "provider_kind": "fixture",
            "adapter": {"id": "fixture:scripted-provider-v1", "revision_sha256": text_sha(Path(__file__))},
            "model": {"id": "fixture:qcb-action-protocol-v1", "revision": "fixture",
                      "chat_template_sha256": digest("fixture-protocol; no model chat template")},
            "sampling": {"seed": 0, "temperature": 0, "top_p": 1, "thinking_mode": "disabled"},
            "condition": {"purpose": purpose, "mode": mode,
                          "exposure": "closed_book" if purpose == "explanation_only" else exposure},
            "limits": {"max_calls": 24, "max_call_input_tokens": 32768, "max_call_output_tokens": 2048,
                       "max_total_input_tokens": 262144, "max_total_output_tokens": 32768,
                       "max_request_bytes": 500000, "max_response_bytes": 32000,
                       "max_call_seconds": 30, "max_wall_seconds": 300,
                       "max_total_endpoint_cost_usd": 0, "max_call_endpoint_cost_usd": 0},
            "session_limits": asdict(SessionLimits(wall_seconds=300))}


def response_envelope(request, action, *, fixture, usage=None):
    """Helper for trusted adapters; model text cannot initialize verifier state."""
    if usage is None:
        if not fixture:
            raise ValueError("real adapters must supply endpoint usage; never invent token or cost values")
        usage = {"input_tokens": 1, "output_tokens": 1, "endpoint_cost_usd": 0, "source": "fixture"}
    return {"schema_version": "qcb.agent_action_response.v1", "request_digest": digest(request),
            "adapter_digest": digest(request["adapter"]), "prompt_digest": digest(request["messages"]),
            "model": deepcopy(request["model"]), "sampling_digest": digest(request["sampling"]),
            "stop_reason": "end_turn", "action": deepcopy(action),
            "usage": deepcopy(usage)}


class _FixtureVerifier:
    execution_class = "fixture"
    isolated = False

    async def verify(self, request):
        good = request["proof"] == "by exact fixture_placeholder"
        return bound_reply(request, status="verified" if good else "compile_error",
                           execution_id=secrets.token_hex(16), kernel_checked=False,
                           diagnostics="" if good else "Deliberate protocol-fixture error; not a Lean diagnostic.")


class ScriptedFixtureProvider:
    """Synthetic scheduling only. No correct reference proof is consulted."""
    is_fixture = True

    @property
    def implementation_sha256(self):
        return text_sha(Path(__file__))

    async def respond(self, request):
        public = request["input"]
        state_id = public["observation"]["state_id"]
        history = request["history"]
        if request["purpose"] == "explanation_only" or not any(t["action"].get("kind") == "explain" for t in history):
            action = {"kind": "explain", "state_id": state_id,
                      "answer": "Protocol fixture only; this is not a mathematical answer."}
        elif public["exposure"] == "approved_interface" and not any(t["action"].get("kind") == "search" for t in history):
            action = {"kind": "search", "state_id": state_id, "query": "Matrix"}
        else:
            task = public["task"]
            accepted = {n["id"] for n in public["observation"]["nodes"] if n["status"] == "evidence_accepted"}
            if task["root_id"] in accepted:
                action = {"kind": "finish", "state_id": state_id}
            else:
                ready = [n for n in task["nodes"] if n["id"] not in accepted and set(n["depends_on"]) <= accepted]
                node = task["root_id"] if public["mode"] == "root_only" else ready[0]["id"]
                first = not any(t["action"].get("kind") == "submit" for t in history)
                action = {"kind": "submit", "state_id": state_id, "node_id": node,
                          "proof": "by exact missing_fixture_lemma" if first else "by exact fixture_placeholder"}
        return response_envelope(request, action, fixture=True)


def _response(request, response, *, fixture, cap):
    encoded = json.dumps(response, ensure_ascii=False, allow_nan=False).encode()
    fields = {"schema_version", "request_digest", "adapter_digest", "prompt_digest", "model", "sampling_digest", "stop_reason", "action", "usage"}
    if (len(encoded) > cap or not isinstance(response, dict) or set(response) != fields
            or response["schema_version"] != "qcb.agent_action_response.v1"
            or response["request_digest"] != digest(request) or response["model"] != request["model"]
            or response["adapter_digest"] != digest(request["adapter"]) or response["prompt_digest"] != digest(request["messages"])
            or response["sampling_digest"] != digest(request["sampling"])
            or response["stop_reason"] != "end_turn" or not isinstance(response["action"], dict)):
        raise ValueError("malformed, oversized, incomplete or unbound provider response")
    usage = response["usage"]
    if (not isinstance(usage, dict) or set(usage) != {"input_tokens", "output_tokens", "endpoint_cost_usd", "source"}
            or any(type(usage[k]) is not int or usage[k] < 0 for k in ("input_tokens", "output_tokens"))
            or type(usage["endpoint_cost_usd"]) not in (int, float)
            or not math.isfinite(usage["endpoint_cost_usd"]) or usage["endpoint_cost_usd"] < 0
            or usage["source"] != ("fixture" if fixture else "endpoint_reported")):
        raise ValueError("complete endpoint telemetry or explicitly synthetic fixture values required")
    return deepcopy(response)


async def run_episode(view, config, destination, *, authorized=False, fixture=False, provider_factory=None):
    """Run one registered-view episode; raw records stay outside the repository.

    Full proof mode has no real-model verifier integration in this version.
    Explanation-only mode can use an explicitly authorized operator adapter;
    its model actions can never call Lean or receive a formal success label.
    """
    config = validate_config(config)
    task = validate_task(view["task"])
    if (view["entry"]["task_hash"] != digest(task) or not re.fullmatch(r"[0-9a-f]{64}", view["registry_digest"])
            or config["condition"]["mode"] not in view["entry"]["allowed_modes"]
            or config["condition"]["exposure"] not in view["entry"]["allowed_exposures"]):
        raise ValueError("view/task identity mismatch")
    if type(fixture) is not bool or type(authorized) is not bool or fixture != (config["provider_kind"] == "fixture"):
        raise ValueError("explicit provider/fixture execution class mismatch")
    destination = Path(destination).resolve()
    if destination.is_relative_to(R.resolve()):
        raise ValueError("raw model episodes must remain outside the public repository")
    if destination.exists():
        raise FileExistsError("choose a fresh episode directory; automatic resume/rebilling is disabled")
    header = {"schema_version": "qcb.agentic_episode.v1", "view_id": view["entry"]["view_id"],
              "registry_digest": view["registry_digest"], "reference_lineage": deepcopy(view["reference_lineage"]),
              "task_hash": digest(task), "core_id": task["core_id"], "contract_hash": task["contract_hash"],
              "family": task["family"], "split": task["split"], "snapshot_id": task["snapshot_id"],
              "library_revision": task["library_revision"], "config_digest": digest(config),
              "model": deepcopy(config["model"]), "sampling": deepcopy(config["sampling"]),
              "adapter": deepcopy(config["adapter"]),
              "harness_sources_sha256_lf": _harness_sources(),
              "condition": deepcopy(config["condition"]), "fixture": fixture,
              "provider_calls": 0, "model_calls_confirmed": 0, "model_generation_observed": False,
              "model_performance_measured": False, "formal_proof_success": False,
              "knowledge_semantic_score": None, "new_mathematical_cores": 0,
              "provider_constructed": False, "limits": deepcopy(config["limits"]),
              "usage_kind": "synthetic_fixture_values" if fixture else "endpoint_reported_not_independently_authenticated",
              "endpoint_usage_unreconciled": False, "calls": [], "turns": [],
              "actions_attempted": 0,
              "totals": {"input_tokens": 0, "output_tokens": 0, "endpoint_cost_usd": 0}}
    if not fixture and not authorized:
        return {**header, "status": "dry_run", "failure_class": None, "episode_directory_created": False}
    # Deliberately before provider_factory, discovery, initialization or calls.
    if not fixture and config["condition"]["purpose"] == "formal_proof":
        return {**header, "status": "ENV_BLOCKED", "failure_class": "ENV_BLOCKED",
                "reason": "No accepted isolated candidate verifier is connected. Authored-reference execution is never a model fallback.",
                "episode_directory_created": False}
    if provider_factory is None:
        if not fixture:
            return {**header, "status": "ENV_BLOCKED", "failure_class": "ENV_BLOCKED",
                    "reason": "Explicit trusted operator provider adapter required.", "episode_directory_created": False}
        provider_factory = ScriptedFixtureProvider
    destination.mkdir(parents=True, exist_ok=False)
    path = destination / "episode.json"
    state = {**header, "status": "initializing", "run_id": secrets.token_hex(16), "episode_directory_created": True}
    tool_started = time.monotonic()
    session = ProofSession(task, _FixtureVerifier() if fixture else None,
                           mode=config["condition"]["mode"], exposure=config["condition"]["exposure"],
                           limits=SessionLimits(**config["session_limits"]))
    started = time.monotonic()

    def persist():
        state["elapsed_seconds"] = time.monotonic() - started
        state["session_report"] = session.report()
        write_json(path, state)

    persist()
    try:
        provider = provider_factory()
        state["provider_constructed"] = True
        if getattr(provider, "is_fixture", None) is not fixture or not inspect.iscoroutinefunction(getattr(provider, "respond", None)):
            raise ValueError("operator provider class does not match the declared execution class")
        if getattr(provider, "implementation_sha256", None) != config["adapter"]["revision_sha256"]:
            raise ValueError("provider implementation identity differs from the pinned configuration")
        limits = config["limits"]
        for index in range(limits["max_calls"]):
            remaining_time = limits["max_wall_seconds"] - (time.monotonic() - started)
            remaining_tool_time = session.limits.wall_seconds - (time.monotonic() - tool_started)
            frontier = session.observation()
            available_in = limits["max_total_input_tokens"] - state["totals"]["input_tokens"]
            available_out = limits["max_total_output_tokens"] - state["totals"]["output_tokens"]
            available_cost = limits["max_total_endpoint_cost_usd"] - state["totals"]["endpoint_cost_usd"]
            if (remaining_time <= 0 or remaining_tool_time <= 0 or frontier["remaining_actions"] <= 0
                    or state["actions_attempted"] >= session.limits.max_actions
                    or config["condition"]["purpose"] == "formal_proof" and frontier["remaining_verifier_calls"] <= 0
                    or available_in <= 0 or available_out <= 0 or available_cost < 0
                    or limits["max_call_endpoint_cost_usd"] > 0 and available_cost == 0):
                state.update(status="BUDGET_EXHAUSTED", failure_class="BUDGET_EXHAUSTED")
                break
            if config["condition"]["purpose"] == "explanation_only":
                public = {"question_context": {k: deepcopy(task[k]) for k in ("core_id", "question", "assumptions", "conventions")},
                          "observation": {"state_id": session.state_id}, "allowed_actions": ["explain"]}
            else:
                public = session.agent_input()
            instructions = ("Return one JSON action with kind=explain, current state_id, and answer containing the mathematical explanation requested. Preserve the supplied assumptions and conventions."
                            if config["condition"]["purpose"] == "explanation_only" else
                            "Complete the fixed proof task using one JSON action per response: search(query), submit(node_id,proof), explain(answer), or finish. Include current state_id. Submit complete proof blocks of unchanged node targets; imports and hypotheses are fixed. The supplied obligation frontier is not an incremental Lean tactic state. Explanations are graded separately.")
            messages = [{"role": "system", "content": instructions},
                        {"role": "user", "content": json.dumps({"input": public, "history": state["turns"]}, ensure_ascii=False, allow_nan=False)}]
            request = {"schema_version": "qcb.agent_action_request.v1", "run_id": state["run_id"], "call_index": index,
                       "view_id": view["entry"]["view_id"], "purpose": config["condition"]["purpose"],
                       "task_hash": digest(task), "adapter": config["adapter"], "model": config["model"], "sampling": config["sampling"],
                       "messages": messages,
                       "input": public, "history": deepcopy(state["turns"]),
                       "max_input_tokens": min(limits["max_call_input_tokens"], available_in),
                       "max_output_tokens": min(limits["max_call_output_tokens"], available_out),
                       "cost_ceiling_usd": min(limits["max_call_endpoint_cost_usd"],
                                               available_cost),
                       "timeout_seconds": min(remaining_time, remaining_tool_time, limits["max_call_seconds"])}
            if len(json.dumps(request, ensure_ascii=False, allow_nan=False).encode()) > limits["max_request_bytes"]:
                state.update(status="BUDGET_EXHAUSTED", failure_class="BUDGET_EXHAUSTED", reason="Request byte ceiling reached; history was not silently truncated.")
                break
            call = {"request_digest": digest(request), "request": deepcopy(request), "status": "in_flight",
                    "reservation": {"input_tokens": request["max_input_tokens"], "output_tokens": request["max_output_tokens"],
                                    "endpoint_cost_usd": request["cost_ceiling_usd"]}, "usage": None}
            state["calls"].append(call)
            state["provider_calls"] += 1
            state.update(status="usage_unreconciled", endpoint_usage_unreconciled=True)
            persist()  # Record worst-case reservation before any provider generation.
            call_started = time.monotonic()
            try:
                raw = await asyncio.wait_for(provider.respond(deepcopy(request)), timeout=request["timeout_seconds"])
                response = _response(request, raw, fixture=fixture, cap=limits["max_response_bytes"])
            except (asyncio.TimeoutError, OSError, RuntimeError) as error:
                call.update(status="usage_unreconciled", error_type=type(error).__name__)
                state.update(status="ENV_BLOCKED", failure_class="ENV_BLOCKED")
                break
            except (ValueError, TypeError, KeyError, RecursionError) as error:
                call.update(status="usage_unreconciled", error_type=type(error).__name__)
                state.update(status="API_BLOCKED", failure_class="API_BLOCKED")
                break
            except Exception as error:  # noqa: BLE001 - SDK boundary: preserve unknown usage and stop, never accept success.
                call.update(status="usage_unreconciled", error_type=type(error).__name__)
                state.update(status="ENV_BLOCKED", failure_class="ENV_BLOCKED")
                break
            finally:
                call["seconds"] = time.monotonic() - call_started
            usage = response["usage"]
            call.update(status="fixture" if fixture else "completed", response=response, usage=usage)
            for key in state["totals"]:
                state["totals"][key] += usage[key]
            state["endpoint_usage_unreconciled"] = False
            state.update(status="running", failure_class=None)
            if not fixture:
                state["model_calls_confirmed"] += 1
                state["model_generation_observed"] = True
            if (usage["input_tokens"] > request["max_input_tokens"] or usage["output_tokens"] > request["max_output_tokens"]
                    or usage["endpoint_cost_usd"] > request["cost_ceiling_usd"]):
                state.update(status="ADAPTER_LIMIT_VIOLATION", failure_class="API_BLOCKED")
                break  # Preserve reported overspend; never cap it to manufacture compliance.
            if call["seconds"] > request["timeout_seconds"] + 0.01:
                state.update(status="ADAPTER_DEADLINE_VIOLATION", failure_class="ENV_BLOCKED")
                break  # Cancellation-resistant adapters do not get a late action executed.
            action = response["action"]
            if config["condition"]["purpose"] == "explanation_only" and action.get("kind") != "explain":
                tool = {"status": "rejected", "failure_class": "API_BLOCKED", "state_id": session.state_id,
                        "diagnostics": "Only a natural-language explanation is accepted in this condition."}
            else:
                tool = await session.act(action)
                if config["condition"]["purpose"] == "explanation_only":
                    tool = {k: v for k, v in tool.items() if k != "observation"}
                    tool["state_id"] = session.state_id
            state["turns"].append({"action": deepcopy(action), "tool_response": deepcopy(tool)})
            state["actions_attempted"] += 1
            if tool.get("failure_class") == "BUDGET_EXHAUSTED":
                state.update(status="BUDGET_EXHAUSTED", failure_class="BUDGET_EXHAUSTED")
                break
            if config["condition"]["purpose"] == "explanation_only" and tool["status"] == "recorded":
                state.update(status="explanation_recorded", failure_class=None)
                break
            if session.report()["protocol_complete"]:
                state.update(status="fixture_protocol_complete", failure_class=None)
                break
            persist()
        else:
            state.update(status="BUDGET_EXHAUSTED", failure_class="BUDGET_EXHAUSTED")
    except asyncio.CancelledError:
        state.update(status="cancelled", failure_class="ENV_BLOCKED")
        raise
    except Exception as error:  # noqa: BLE001 - Operator factories may raise SDK-specific exceptions; persist a typed failed run.
        failure = "ENV_BLOCKED" if isinstance(error, (ImportError, OSError)) else "API_BLOCKED"
        state.update(status=failure, failure_class=failure, error_type=type(error).__name__)
    finally:
        if _harness_sources() != state["harness_sources_sha256_lf"]:
            state.update(status="PIPELINE_DRIFT", failure_class="API_BLOCKED")
        persist()
    return deepcopy(state)
