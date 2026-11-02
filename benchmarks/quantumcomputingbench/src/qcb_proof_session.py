"""Bounded proof-obligation interactions; no compiler or model is started here.

An obligation frontier is not a Lean tactic state or measured proof-term DAG.
Only a trusted, explicitly supplied verifier can return checked evidence. The
default verifier is blocked; JSON submitted by an agent is never a receipt.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import math
import re
import subprocess
import time
from copy import deepcopy
from dataclasses import asdict, dataclass

from qcb_core import digest
from qcb_lean import APPROVED_AXIOMS, _trusted_target

TASK_SCHEMA = "qcb.proof_obligation_task.v1"
UNIVERSE_TASK_SCHEMA = "qcb.proof_obligation_task.v2"
_ID = re.compile(r"[A-Za-z][A-Za-z0-9_]*\Z")
_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*\Z")
_FAILURES = {"compile_error": "IMPLEMENTATION_FAILED", "timeout": "ENV_BLOCKED",
             "verifier_error": "ENV_BLOCKED", "api_error": "API_BLOCKED"}


@dataclass(frozen=True)
class SessionLimits:
    max_actions: int = 32
    max_verifier_calls: int = 12
    max_searches: int = 8
    max_proof_chars: int = 16000
    max_query_chars: int = 512
    max_observation_chars: int = 24000
    wall_seconds: float = 180
    check_seconds: float = 45

    def __post_init__(self):
        for field in ("max_actions", "max_verifier_calls", "max_searches", "max_proof_chars",
                      "max_query_chars", "max_observation_chars"):
            value = getattr(self, field)
            if type(value) is not int or not 1 <= value <= 100000:
                raise ValueError("session count/character limits must be bounded positive integers")
        for field in ("wall_seconds", "check_seconds"):
            value = getattr(self, field)
            if type(value) not in (int, float) or not math.isfinite(value) or not 0 < value <= 600:
                raise ValueError("session deadlines must be finite and in (0,600]")
        if self.max_observation_chars < 8192:
            raise ValueError("observation envelope requires at least 8192 characters")


def validate_task(task):
    required = {"schema_version", "core_id", "contract_hash", "family", "split", "snapshot_id",
                "library_revision", "imports", "question", "assumptions", "conventions",
                "root_id", "nodes", "interfaces", "alignment_status"}
    if not isinstance(task, dict):
        raise TypeError("task must be an evaluator-owned object")
    version = task.get("schema_version")
    if version == UNIVERSE_TASK_SCHEMA:
        required.add("universe_parameters")
    if set(task) != required or version not in {TASK_SCHEMA, UNIVERSE_TASK_SCHEMA}:
        raise ValueError("unexpected task fields or schema; evaluator data must exclude gold")
    if version == UNIVERSE_TASK_SCHEMA:
        parameters = task["universe_parameters"]
        reserved = {"by", "in", "where", "theorem", "def", "axiom", "import", "Type", "Prop", "Sort", "universe"}
        if (not isinstance(parameters, list) or not 1 <= len(parameters) <= 8
                or any(not isinstance(p, str) or len(p) > 32 or not _ID.fullmatch(p) or p in reserved for p in parameters)
                or len(set(parameters)) != len(parameters)):
            raise ValueError("universe parameters must be fixed unique bounded identifiers, not a source preamble")
    for key in ("core_id", "contract_hash", "family", "snapshot_id", "library_revision", "question", "alignment_status"):
        if not isinstance(task[key], str) or not task[key].strip():
            raise ValueError("missing task identity/context: " + key)
    if task["split"] not in {"train", "dev", "test_public"}:
        raise ValueError("unknown or unadmitted split")
    for key in ("assumptions", "conventions"):
        if not isinstance(task[key], list) or any(not isinstance(s, str) for s in task[key]):
            raise ValueError("task premises must be evaluator-owned text lists")
    if (not isinstance(task["imports"], list) or not task["imports"]
            or any(not isinstance(s, str) or not _NAME.fullmatch(s) for s in task["imports"])):
        raise ValueError("invalid frozen imports")
    nodes = task["nodes"]
    if not isinstance(nodes, list) or not 1 <= len(nodes) <= 32:
        raise ValueError("expected a bounded evaluator-owned obligation DAG")
    by_id = {}
    for node in nodes:
        if not isinstance(node, dict) or set(node) != {"id", "target", "depends_on"}:
            raise ValueError("unexpected obligation fields")
        if not isinstance(node["id"], str) or len(node["id"]) > 64 or not _ID.fullmatch(node["id"]) or node["id"] in by_id:
            raise ValueError("invalid/duplicate obligation identity")
        _trusted_target(node["target"])
        deps = node["depends_on"]
        if not isinstance(deps, list) or any(not isinstance(d, str) for d in deps) or len(set(deps)) != len(deps):
            raise ValueError("invalid obligation dependencies")
        by_id[node["id"]] = node
    if task["root_id"] not in by_id:
        raise ValueError("missing fixed root")
    active, done = set(), set()

    def visit(key):
        if key not in by_id or key in active:
            raise ValueError("unknown dependency or cyclic obligation DAG")
        if key in done:
            return
        active.add(key)
        for dependency in by_id[key]["depends_on"]:
            visit(dependency)
        active.remove(key)
        done.add(key)

    visit(task["root_id"])
    if done != set(by_id):
        raise ValueError("disconnected obligations cannot inflate assessed depth")
    if not isinstance(task["interfaces"], list) or len(task["interfaces"]) > 128:
        raise ValueError("admitted retrieval interfaces must be bounded")
    names = set()
    for entry in task["interfaces"]:
        if not isinstance(entry, dict) or set(entry) != {"name", "type", "module", "source_node_id"}:
            raise ValueError("interfaces may contain declarations, never proofs or answers")
        for key in ("name", "module"):
            if not isinstance(entry[key], str) or not _NAME.fullmatch(entry[key]):
                raise ValueError("invalid interface identity")
        _trusted_target(entry["type"])
        if not isinstance(entry["source_node_id"], str) or not entry["source_node_id"].strip():
            raise ValueError("interface source identity missing")
        if entry["name"] in names:
            raise ValueError("duplicate interface declaration")
        names.add(entry["name"])
    if len(json.dumps(task, ensure_ascii=False)) > 128000:
        raise ValueError("task context too large")
    return deepcopy(task)


def proof_sha(proof):
    return hashlib.sha256(proof.encode()).hexdigest()


def bound_reply(request, *, status, execution_id, kernel_checked=False, axioms=(), diagnostics=""):
    """For trusted verifier implementations, not an agent-facing acceptance API."""
    return {"request_hash": digest(request), "proof_sha256": proof_sha(request["proof"]),
            "status": status, "execution_id": execution_id, "kernel_checked": kernel_checked,
            "axioms": list(axioms), "diagnostics": diagnostics}


class BlockedVerifier:
    execution_class = "blocked"
    isolated = False

    async def verify(self, request):
        return bound_reply(request, status="verifier_error", execution_id=request["request_id"],
                           diagnostics="An accepted isolated candidate verifier has not been connected.")


class ProofSession:
    """One task, immutable statements, bounded retrieval/check/repair/final replay.

    The task is operator/evaluator-owned. The verifier is an in-process trusted
    dependency, never an object or JSON supplied by the proving agent. Existing
    production candidate execution gates are not enabled by this protocol.
    """

    def __init__(self, task, verifier=None, *, mode="proof_dag", exposure="approved_interface", limits=None):
        self._task = validate_task(task)
        self.task_hash = digest(self._task)
        if mode not in {"root_only", "proof_dag"} or exposure not in {"closed_book", "approved_interface"}:
            raise ValueError("unsupported interaction mode or exposure")
        self.mode, self.exposure = mode, exposure
        self.limits = limits or SessionLimits()
        self.verifier = verifier or BlockedVerifier()
        if (self.verifier.execution_class not in {"blocked", "fixture", "trusted_local_authored_reference"}
                or self.verifier.isolated is not False):
            raise ValueError("candidate isolation integration is not enabled by this milestone")
        self._nodes = {n["id"]: n for n in self._task["nodes"]}
        self._accepted, self._proofs, self._attempts = {}, {}, {n: [] for n in self._nodes}
        self._execution_ids = set()
        self._serial = self._actions = self._checks = self._searches = 0
        self._started = time.monotonic()
        self._finished = False
        self._final = None
        self._lock = asyncio.Lock()
        self.events = []
        self.explanations = []

    @property
    def state_id(self):
        return digest({"task_hash": self.task_hash, "serial": self._serial,
                       "accepted": {k: v["proof_sha256"] for k, v in self._accepted.items()}})

    def observation(self):
        observation = {"task_hash": self.task_hash, "state_id": self.state_id,
                "state_kind": "evaluator_provided_obligation_frontier_not_tactic_state",
                "nodes": [{"id": n, "status": "evidence_accepted" if n in self._accepted else "pending",
                           "attempts": len(self._attempts[n]),
                           "last_feedback": deepcopy(self._attempts[n][-1]) if self._attempts[n] else None}
                          for n in self._nodes],
                "remaining_actions": max(0, self.limits.max_actions - self._actions),
                "remaining_verifier_calls": max(0, self.limits.max_verifier_calls - self._checks),
                "finished": self._finished}
        if len(json.dumps(observation, ensure_ascii=False)) > self.limits.max_observation_chars - 4000:
            observation["feedback_truncated"] = True
            for node in observation["nodes"]:
                feedback = node["last_feedback"]
                if feedback:
                    node["last_feedback"] = {k: feedback.get(k) for k in ("status", "failure_class")}
        return observation

    def agent_input(self):
        task = {k: deepcopy(v) for k, v in self._task.items() if k != "interfaces"}
        task["interface_policy_hash"] = digest(self._task["interfaces"])
        for node in task["nodes"]:
            node["helper_name"] = "qcb_step_" + node["id"]
        return {"schema_version": "qcb.proof_session_input.v1", "task": task,
                "task_hash": self.task_hash, "mode": self.mode, "exposure": self.exposure,
                "limits": asdict(self.limits), "observation": self.observation(),
                "capability_boundary": "Obligation checks, not incremental tactic execution; public fixture cohort."}

    def _result(self, status, failure_class=None, **details):
        return {"status": status, "failure_class": failure_class, **details, "observation": self.observation()}

    def _bounded_response(self, response):
        """Bound the complete tool reply; full attempts remain evaluator evidence."""
        def size():
            return len(json.dumps(response, ensure_ascii=False))

        limit = self.limits.max_observation_chars
        if size() <= limit:
            return response
        response["feedback_truncated"] = True
        for node in response["observation"]["nodes"]:
            feedback = node["last_feedback"]
            if feedback:
                node["last_feedback"] = {k: feedback.get(k) for k in ("status", "failure_class")}
                node["last_feedback"]["receipt_hash"] = digest(feedback)
        for key in ("evidence", "final_replay"):
            if key in response:
                full = response[key]
                response[key] = {k: full.get(k) for k in ("status", "failure_class", "proof_sha256", "kernel_checked")}
                response[key].update(receipt_hash=digest(full), diagnostics=full.get("diagnostics", "")[-1000:])
        while size() > limit and response.get("entries"):
            response["entries"].pop()
        if size() > limit:
            for node in response["observation"]["nodes"]:
                if node["last_feedback"]:
                    node["last_feedback"].pop("receipt_hash", None)
        if size() > limit:
            for node in response["observation"]["nodes"]:
                node["last_feedback"] = None
            for key in ("evidence", "final_replay"):
                if key in response:
                    response[key].pop("diagnostics", None)
        if size() > limit:
            raise RuntimeError("bounded observation envelope exceeded")
        return response

    def _search(self, query):
        if self.exposure != "approved_interface":
            return self._result("blocked", "API_BLOCKED", diagnostics="Retrieval is unavailable in closed_book.")
        if not isinstance(query, str) or not 0 < len(query) <= self.limits.max_query_chars:
            return self._result("rejected", "API_BLOCKED", diagnostics="Invalid bounded query.")
        if self._searches >= self.limits.max_searches:
            return self._result("blocked", "BUDGET_EXHAUSTED")
        self._searches += 1
        words = set(re.findall(r"[A-Za-z0-9_]+", query.lower()))
        ranked = []
        for entry in self._task["interfaces"]:
            overlap = len(words & set(re.findall(r"[A-Za-z0-9_]+", json.dumps(entry).lower())))
            if overlap:
                ranked.append((-overlap, entry["name"], entry))
        entries = []
        for _, _, entry in sorted(ranked):
            if len(json.dumps([*entries, entry])) <= self.limits.max_observation_chars:
                entries.append(deepcopy(entry))
            if len(entries) == 6:
                break
        return self._result("returned", entries=entries, mathematical_credit=False)

    async def _check(self, node_id, proof, *, final_replay=False):
        remaining = self.limits.wall_seconds - (time.monotonic() - self._started)
        if remaining <= 0 or self._checks >= self.limits.max_verifier_calls:
            return {"status": "blocked", "failure_class": "BUDGET_EXHAUSTED"}
        self._checks += 1
        order = []

        def ancestors(key):
            for dependency in self._nodes[key]["depends_on"]:
                if dependency in self._accepted and dependency not in order:
                    ancestors(dependency)
                    order.append(dependency)

        ancestors(node_id)
        request = {"schema_version": "qcb.obligation_check.v1", "task_hash": self.task_hash,
                   "request_id": str(self._checks), "node_id": node_id,
                   "imports": self._task["imports"], "target": self._nodes[node_id]["target"],
                   "universe_parameters": self._task.get("universe_parameters", []),
                   "library_revision": self._task["library_revision"], "proof": proof,
                   "dependency_order": order,
                   "dependencies": {k: {"target": self._nodes[k]["target"],
                                        "proof": self._proofs[k],
                                        "receipt_hash": digest(self._accepted[k]),
                                        "proof_sha256": proof_sha(self._proofs[k])}
                                    for k in order},
                   "final_replay": final_replay, "timeout_seconds": min(remaining, self.limits.check_seconds)}
        request["deadline_monotonic"] = time.monotonic() + request["timeout_seconds"]
        started = time.monotonic()
        try:
            reply = await asyncio.wait_for(self.verifier.verify(deepcopy(request)), timeout=request["timeout_seconds"])
            if (not isinstance(reply, dict) or reply.get("request_hash") != digest(request)
                    or reply.get("proof_sha256") != proof_sha(proof)):
                raise ValueError("Verifier returned stale/unbound evidence.")
            execution_id = reply.get("execution_id")
            if not isinstance(execution_id, str) or not 0 < len(execution_id) <= 128 or execution_id in self._execution_ids:
                raise ValueError("Verifier execution identity absent or reused.")
            self._execution_ids.add(execution_id)
            status = reply.get("status")
            if status not in {"verified", *_FAILURES}:
                raise ValueError("Unknown verifier status.")
            axioms = reply.get("axioms")
            if (not isinstance(axioms, list) or len(axioms) > 64 or any(not isinstance(a, str) for a in axioms)
                    or (status == "verified" and set(axioms) - APPROVED_AXIOMS)):
                raise ValueError("Unexpected axiom evidence.")
            if status == "verified" and self.verifier.execution_class != "fixture" and reply.get("kernel_checked") is not True:
                raise ValueError("Successful replay lacks actual kernel evidence.")
            diagnostic = reply.get("diagnostics", "")
            if not isinstance(diagnostic, str):
                raise TypeError("Malformed verifier diagnostics.")
            result = {k: deepcopy(reply[k]) for k in ("request_hash", "proof_sha256", "execution_id", "status", "axioms")}
            result.update(kernel_checked=reply.get("kernel_checked") is True,
                          diagnostics=diagnostic[-4000:], failure_class=_FAILURES.get(status),
                          execution_class=self.verifier.execution_class, isolated=False)
        except asyncio.TimeoutError:
            result = {"status": "timeout", "failure_class": "ENV_BLOCKED", "diagnostics": "Verification timed out."}
        except (ValueError, TypeError, KeyError) as error:
            result = {"status": "api_error", "failure_class": "API_BLOCKED", "diagnostics": str(error)}
        except (OSError, RuntimeError, subprocess.SubprocessError) as error:
            result = {"status": "verifier_error", "failure_class": "ENV_BLOCKED", "diagnostics": str(error)[-4000:]}
        result["seconds"] = time.monotonic() - started
        return result

    async def act(self, action):
        # Freeze JSON input before yielding; concurrent calls cannot race a
        # final replay or smuggle a changed proof into a recorded attempt.
        try:
            encoded = json.dumps(action, ensure_ascii=False, allow_nan=False)
            if len(encoded) > self.limits.max_proof_chars + 8000:
                action = {"invalid_action_hash": proof_sha(encoded)}
            else:
                action = json.loads(encoded)
        except (ValueError, TypeError):
            action = {"invalid_action": "not_json"}
        async with self._lock:
            response = self._bounded_response(await self._act(action))
            if len(self.events) < self.limits.max_actions:
                self.events.append({"action": deepcopy(action), "response": deepcopy(response),
                                    "observation_is_math_assumption": False})
            return response

    async def _act(self, action):
        if self._actions >= self.limits.max_actions or time.monotonic() - self._started >= self.limits.wall_seconds:
            return self._result("blocked", "BUDGET_EXHAUSTED")
        self._actions += 1
        if self._finished:
            return self._result("blocked", "API_BLOCKED", diagnostics="Session already finished.")
        fields = {"search": {"kind", "state_id", "query"}, "submit": {"kind", "state_id", "node_id", "proof"},
                  "explain": {"kind", "state_id", "answer"}, "finish": {"kind", "state_id"}}
        if not isinstance(action, dict) or not isinstance(action.get("kind"), str) or action["kind"] not in fields:
            return self._result("rejected", "API_BLOCKED", diagnostics="Unknown action.")
        kind = action["kind"]
        if set(action) != fields[kind] or action["state_id"] != self.state_id:
            return self._result("rejected", "API_BLOCKED", diagnostics="Action fields or frontier identity mismatch.")
        # One in-flight action per session; no candidate can mutate the fixed task.
        self._serial += 1
        if kind == "search":
            response = self._search(action["query"])
        elif kind == "explain":
            answer = action["answer"]
            if not isinstance(answer, str) or not 0 < len(answer) <= self.limits.max_proof_chars:
                response = self._result("rejected", "API_BLOCKED")
            else:
                self.explanations.append(answer)
                response = self._result("recorded", semantic_score=None, review="independent_rubric_required")
        elif kind == "submit":
            node, proof = action["node_id"], action["proof"]
            if not isinstance(node, str) or node not in self._nodes or not isinstance(proof, str) or not 0 < len(proof) <= self.limits.max_proof_chars:
                response = self._result("rejected", "API_BLOCKED", diagnostics="Invalid obligation or proof size.")
            elif node in self._accepted:
                response = self._result("rejected", "API_BLOCKED", diagnostics="Accepted obligations are immutable.")
            elif self.mode == "root_only" and node != self._task["root_id"]:
                response = self._result("rejected", "API_BLOCKED", diagnostics="This control accepts whole-root proofs only.")
            elif self.mode == "proof_dag" and any(d not in self._accepted for d in self._nodes[node]["depends_on"]):
                response = self._result("blocked", "API_BLOCKED", diagnostics="Declared predecessor obligations remain unchecked.")
            else:
                receipt = await self._check(node, proof)
                self._attempts[node].append(deepcopy(receipt))
                if receipt["status"] == "verified":
                    self._accepted[node], self._proofs[node] = receipt, proof
                response = self._result(receipt["status"], receipt.get("failure_class"), evidence=deepcopy(receipt))
        else:
            root = self._task["root_id"]
            if root not in self._accepted:
                response = self._result("blocked", "API_BLOCKED", diagnostics="No accepted root proof to replay.")
            else:
                self._final = await self._check(root, self._proofs[root], final_replay=True)
                self._finished = self._final["status"] == "verified"
                response = self._result(self._final["status"], self._final.get("failure_class"), final_replay=deepcopy(self._final))
        return response

    def report(self):
        final = self._final or {}
        return {"schema_version": "qcb.proof_session_report.v1", "task_hash": self.task_hash,
                "core_id": self._task["core_id"], "contract_hash": self._task["contract_hash"],
                "family": self._task["family"], "split": self._task["split"],
                "mode": self.mode, "exposure": self.exposure, "limits": asdict(self.limits),
                "execution_class": self.verifier.execution_class, "isolated": False,
                "protocol_complete": self._finished,
                "formal_root_checked": self._finished and final.get("kernel_checked") is True
                    and self.verifier.execution_class == "trusted_local_authored_reference",
                "isolated_prediction_success": False, "model_performance_measured": False,
                "model_usage": None, "matched_realized_compute_established": False,
                "knowledge_semantic_score": None, "explanation_review": "independent_rubric_required",
                "metrics": {"actions": self._actions, "verifier_calls": self._checks,
                            "retrieval_calls": self._searches,
                            "accepted_obligations": len(self._accepted),
                            "repair_attempts": sum(max(0, len(v)-1) for v in self._attempts.values()),
                            "wall_seconds": time.monotonic() - self._started},
                "planning_scope": "evaluator-provided obligation DAG; actual proof-term dependency depth unmeasured",
                "new_mathematical_cores": 0, "final_replay": deepcopy(self._final),
                "observation": self.observation(), "events": deepcopy(self.events),
                "attempt_evidence": deepcopy(self._attempts),
                "explanations": list(self.explanations)}
