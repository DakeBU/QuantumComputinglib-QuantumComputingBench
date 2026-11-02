"""Separate retrieval observations, supplied semantic marks and formal evidence.

All inputs are evaluator-owned records. Digests detect stale content; they do
not authenticate a reviewer, establish mathematical truth, or create a live
formal certificate. No model, compiler, or automatic semantic judge runs here.
"""
from __future__ import annotations

import math
from copy import deepcopy

from qcb_core import digest
from qcb_curriculum import core_contract, load_catalog
from qcb_proof_session import validate_task
from qcb_textbook_policy import check_source_bindings


def _identity(record):
    if (not isinstance(record, dict) or set(record) != {"identity", "kind", "method"}
            or any(not isinstance(record[k], str) or not record[k].strip() for k in record)
            or record["kind"] not in {"human", "ai"}):
        raise ValueError("actual reviewer identity, human/AI kind and method required")


def validate_rubric(task, rubric):
    task = validate_task(task)
    required = {"schema_version", "task_hash", "core_id", "contract_hash", "interface_policy_hash",
                "reviewer", "source_bindings", "routes", "obligation_groups", "knowledge_source",
                "knowledge_criteria", "limitations"}
    if (not isinstance(rubric, dict) or set(rubric) != required
            or rubric["schema_version"] != "qcb.capability_rubric.v1"
            or rubric["task_hash"] != digest(task)
            or rubric["core_id"] != task["core_id"] or rubric["contract_hash"] != task["contract_hash"]
            or rubric["interface_policy_hash"] != digest(task["interfaces"])):
        raise ValueError("rubric must bind the exact task, core contract and interface corpus")
    _identity(rubric["reviewer"])
    if not isinstance(rubric["source_bindings"], list) or not rubric["source_bindings"]:
        raise ValueError("source-aware rubric requires inspected source bindings")
    check_source_bindings(rubric["source_bindings"])
    interfaces = {entry["name"] for entry in task["interfaces"]}
    routes = rubric["routes"]
    if not isinstance(routes, list) or not 1 <= len(routes) <= 32:
        raise ValueError("expected bounded operator-curated routes")
    seen = set()
    for route in routes:
        if not isinstance(route, dict) or set(route) != {"id", "required_names", "unscored_dependencies", "scope_note"}:
            raise ValueError("curated routes must disclose unscored dependencies and scope")
        if not isinstance(route["id"], str) or not route["id"].strip() or route["id"] in seen:
            raise ValueError("invalid/duplicate route identity")
        seen.add(route["id"])
        names = route["required_names"]
        if (not isinstance(names, list) or not names or any(not isinstance(n, str) for n in names)
                or len(set(names)) != len(names) or not set(names) <= interfaces):
            raise ValueError("each AND-route needs unique names inside the curated interface corpus")
        if (not isinstance(route["unscored_dependencies"], list)
                or any(not isinstance(s, str) or not s.strip() for s in route["unscored_dependencies"])
                or not isinstance(route["scope_note"], str) or not route["scope_note"].strip()):
            raise ValueError("route scope must distinguish interface coverage from proof completeness")
    criteria = rubric["knowledge_criteria"]
    if not isinstance(criteria, list) or not 1 <= len(criteria) <= 64:
        raise ValueError("expected bounded semantic criteria")
    seen = set()
    for criterion in criteria:
        if (not isinstance(criterion, dict) or set(criterion) != {"id", "criterion", "weight", "kind"}
                or not isinstance(criterion["id"], str) or not criterion["id"].strip() or criterion["id"] in seen
                or not isinstance(criterion["criterion"], str) or not criterion["criterion"].strip()
                or criterion["kind"] not in {"knowledge", "assumption", "reasoning"}
                or type(criterion["weight"]) not in (int, float)
                or not math.isfinite(criterion["weight"]) or not 0 < criterion["weight"] <= 1000):
            raise ValueError("invalid semantic criterion")
        seen.add(criterion["id"])
    source = rubric["knowledge_source"]
    if (not isinstance(source, dict) or set(source) != {"item_digest", "rubric_digest", "criterion_ids", "scope"}
            or source["scope"] != "whole_current_canonical_rubric"
            or not isinstance(source["item_digest"], str) or len(source["item_digest"]) != 64
            or source["criterion_ids"] != [c["id"] for c in criteria]
            or source["rubric_digest"] != digest([{k: c[k] for k in ("id", "criterion", "weight")} for c in criteria])):
        raise ValueError("whole canonical rubric content and criterion coverage must be bound")
    _, items, _ = load_catalog()
    item = items.get(task["core_id"])
    if (item is None or source["item_digest"] != digest(item) or source["rubric_digest"] != digest(item["rubric"])
            or task["contract_hash"] != digest(core_contract(item))
            or any(task[k] != item[k] for k in ("question", "assumptions", "conventions"))):
        raise ValueError("knowledge grading must use the current complete canonical question and rubric")
    groups = rubric["obligation_groups"]
    nodes = {n["id"]: n for n in task["nodes"]}
    if not isinstance(groups, list) or len(groups) != len(nodes):
        raise ValueError("each provided obligation needs one separately scoped group")
    covered = set()
    for group in groups:
        if (not isinstance(group, dict) or set(group) != {"obligation_id", "required_names", "provider_obligations"}
                or not isinstance(group["obligation_id"], str) or group["obligation_id"] not in nodes
                or group["obligation_id"] in covered):
            raise ValueError("unknown/duplicate obligation group")
        covered.add(group["obligation_id"])
        names = group["required_names"]
        if (not isinstance(names, list) or any(not isinstance(n, str) for n in names)
                or len(set(names)) != len(names) or not set(names) <= interfaces
                or group["provider_obligations"] != nodes[group["obligation_id"]]["depends_on"]):
            raise ValueError("local groups must preserve curated scope and all provider obligations")
    if (not isinstance(rubric["limitations"], list) or not rubric["limitations"]
            or any(not isinstance(s, str) or not s.strip() for s in rubric["limitations"])):
        raise ValueError("explicit rubric limitations required")
    return deepcopy(rubric)


def _report(task, report):
    if (not isinstance(report, dict) or report.get("schema_version") != "qcb.proof_session_report.v1"
            or report.get("task_hash") != digest(task)
            or any(report.get(k) != task[k] for k in ("core_id", "contract_hash", "family", "split"))
            or report.get("exposure") not in {"closed_book", "approved_interface"}
            or not isinstance(report.get("events"), list) or len(report["events"]) > 100000):
        raise ValueError("session report does not bind this evaluator-owned task")
    recorded = []
    for event in report["events"]:
        if (not isinstance(event, dict) or not isinstance(event.get("action"), dict)
                or not isinstance(event.get("response"), dict)):
            raise TypeError("malformed session event")
        if event["action"].get("kind") == "explain" and event["response"].get("status") == "recorded":
            answer = event["action"].get("answer")
            if not isinstance(answer, str):
                raise ValueError("malformed recorded explanation")
            recorded.append(answer)
    if report.get("explanations") != recorded:
        raise ValueError("explanation list differs from recorded actions")
    return report


def retrieval_metrics(task, report, rubric):
    """Measure only the returned curated interfaces, not hidden proof premises."""
    interfaces = {e["name"]: e for e in task["interfaces"]}
    returned = []
    calls = 0
    for event in report["events"]:
        action, response = event["action"], event["response"]
        if action.get("kind") != "search" or response.get("status") != "returned":
            continue
        calls += 1
        if report["exposure"] != "approved_interface" or not isinstance(response.get("entries"), list):
            raise ValueError("retrieval output conflicts with exposure or protocol")
        if len(response["entries"]) > 6:
            raise ValueError("retrieval output exceeds the protocol result cap")
        names = set()
        for entry in response["entries"]:
            if (not isinstance(entry, dict) or entry.get("name") not in interfaces
                    or entry != interfaces[entry["name"]] or entry["name"] in names):
                raise ValueError("retrieval response contains a changed/unknown/duplicate declaration")
            names.add(entry["name"])
            if entry["name"] not in returned:
                returned.append(entry["name"])
    if report["exposure"] == "closed_book":
        return {"status": "not_available_in_this_exposure", "curated_target_coverage": None,
                "curated_route_complete": None, "successful_search_calls": 0}
    targets = {n for route in rubric["routes"] for n in route["required_names"]}
    found = set(returned)
    routes = [{"id": route["id"], "matched": sorted(found & set(route["required_names"])),
               "missing": sorted(set(route["required_names"]) - found),
               "curated_interface_coverage": len(found & set(route["required_names"])) / len(route["required_names"]),
               "curated_route_complete": set(route["required_names"]) <= found,
               "unscored_dependencies": deepcopy(route["unscored_dependencies"])} for route in rubric["routes"]]
    groups = [{"obligation_id": g["obligation_id"],
               "local_interface_coverage": len(found & set(g["required_names"])) / len(g["required_names"]) if g["required_names"] else None,
               "local_interface_group_complete": set(g["required_names"]) <= found if g["required_names"] else None,
               "provider_obligations_not_scored_as_retrieval": deepcopy(g["provider_obligations"])}
              for g in rubric["obligation_groups"]]
    return {"status": "observed_curated_interfaces", "successful_search_calls": calls,
            "unique_returned": returned, "target_names": sorted(targets),
            "curated_target_coverage": len(found & targets) / len(targets),
            "route_aligned_return_fraction": len(found & targets) / len(found) if found else None,
            "curated_route_complete": any(r["curated_route_complete"] for r in routes), "routes": routes,
            "obligation_groups": groups,
            "local_groups_are_root_alternatives": False,
            "scope": "AND within each supplied route, OR across routes; not exhaustive proof-premise recall, usefulness or proof success"}


def explanation_score(task, report, rubric, adjudication=None):
    """Validate supplied content-bound marks; do not judge prose automatically."""
    if adjudication is None:
        return {"status": "needs_external_adjudication", "weighted_supplied_mark": None,
                "semantic_fidelity": None, "kernel_certified": False}
    required = {"schema_version", "task_hash", "report_digest", "rubric_digest", "answer_index",
                "answer_digest", "reviewer", "respondent_identity", "criteria", "semantic_fidelity", "reasoning"}
    if (not isinstance(adjudication, dict) or set(adjudication) != required
            or adjudication["schema_version"] != "qcb.explanation_adjudication.v1"
            or adjudication["task_hash"] != digest(task) or adjudication["report_digest"] != digest(report)
            or adjudication["rubric_digest"] != digest(rubric)):
        raise ValueError("adjudication must bind exact task, full report and rubric")
    _identity(adjudication["reviewer"])
    respondent = adjudication["respondent_identity"]
    if (not isinstance(respondent, str) or not respondent.strip()
            or respondent == adjudication["reviewer"]["identity"]):
        raise ValueError("record an actual distinct respondent and reviewer; identity metadata is not authentication")
    index = adjudication["answer_index"]
    if type(index) is not int or not 0 <= index < len(report["explanations"]):
        raise ValueError("adjudication must select one recorded explanation explicitly")
    if adjudication["answer_digest"] != digest(report["explanations"][index]):
        raise ValueError("explanation changed after adjudication")
    if (adjudication["semantic_fidelity"] not in {"faithful", "unfaithful", "uncertain"}
            or not isinstance(adjudication["reasoning"], str) or not adjudication["reasoning"].strip()):
        raise ValueError("semantic fidelity and substantive external reasoning required")
    marks = adjudication["criteria"]
    expected = {c["id"] for c in rubric["knowledge_criteria"]}
    if not isinstance(marks, list) or len(marks) != len(expected):
        raise ValueError("every semantic criterion needs a supplied mark")
    by_id = {}
    for mark in marks:
        if (not isinstance(mark, dict) or set(mark) != {"id", "score", "reasoning"}
                or not isinstance(mark["id"], str) or mark["id"] in by_id
                or type(mark["score"]) not in (int, float) or not math.isfinite(mark["score"])
                or not 0 <= mark["score"] <= 1 or not isinstance(mark["reasoning"], str) or not mark["reasoning"].strip()):
            raise ValueError("invalid/duplicate criterion mark or missing reasoning")
        by_id[mark["id"]] = mark["score"]
    if set(by_id) != expected:
        raise ValueError("criterion identities differ from the bound rubric")
    value = sum(c["weight"] * by_id[c["id"]] for c in rubric["knowledge_criteria"]) / sum(c["weight"] for c in rubric["knowledge_criteria"])
    return {"status": "external_marks_recorded", "answer_index": index,
            "weighted_supplied_mark": None if adjudication["semantic_fidelity"] == "uncertain" else value,
            "semantic_fidelity": adjudication["semantic_fidelity"], "reviewer": deepcopy(adjudication["reviewer"]),
            "adjudication_digest": digest(adjudication), "kernel_certified": False,
            "reviewer_authenticity_or_independence_verified_by_schema": False,
            "scope": "Content-bound external semantic marks, not an automated mathematical truth verdict"}


def assess(task, report, rubric, adjudication=None):
    task = validate_task(task)
    rubric = validate_rubric(task, rubric)
    _report(task, report)
    return {"schema_version": "qcb.capability_assessment.v1", "task_hash": digest(task),
            "core_id": task["core_id"], "contract_hash": task["contract_hash"],
            "family": task["family"], "split": task["split"],
            "session_report_digest": digest(report), "rubric_digest": digest(rubric),
            "knowledge_source": deepcopy(rubric["knowledge_source"]),
            "retrieval": retrieval_metrics(task, report, rubric),
            "explanation": explanation_score(task, report, rubric, adjudication),
            "formal_root_status_from_evaluator_record": report.get("formal_root_checked"),
            "formal_certificate_issued_by_this_assessment": False,
            "joint_capability_score": None, "model_performance_measured": False,
            "mathematical_core_count_increment": 0,
            "trust_boundary": "Evaluator-owned artifacts only; JSON/digests do not authenticate execution or certify semantic judgments",
            "limitations": deepcopy(rubric["limitations"])}
