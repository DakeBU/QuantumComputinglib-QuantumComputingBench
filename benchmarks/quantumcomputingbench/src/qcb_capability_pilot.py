"""Current canonical knowledge rubrics and reviewed scoped retrieval targets."""
from __future__ import annotations

import hashlib
from copy import deepcopy

from qcb_capabilities import validate_rubric
from qcb_core import digest, read_json
from qcb_curriculum import load_catalog
from qcb_obligation_pilot import FIXTURE, B, load_pilot

DESIGN = B / "tracks/lean/evaluation/capability-design-v1.json"


def validate_engineered_examples(examples, canonical_rubric):
    """Bind fixed expectations to their inspected text, never relabel new prose."""
    if not isinstance(examples, list) or len(examples) != 2:
        raise ValueError("expected one fixed positive/negative explanation pair")
    ids = set()
    expected = {c["id"] for c in canonical_rubric}
    for example in examples:
        fields = {"id", "answer", "canonical_criteria", "assumption_audit", "answer_hash",
                  "adjudication_class", "model_answer", "source_blind"}
        if (not isinstance(example, dict) or set(example) != fields
                or not isinstance(example["id"], str) or not example["id"].strip() or example["id"] in ids
                or not isinstance(example["answer"], str) or not 0 < len(example["answer"]) <= 16000
                or example["answer_hash"] != digest(example["answer"])
                or example["adjudication_class"] != "engineered_expected_fixture_labels_by_same_source_aware_author"
                or example["model_answer"] is not False or example["source_blind"] is not False):
            raise ValueError("engineered example text/provenance changed after its expected labels")
        ids.add(example["id"])
        marks = example["canonical_criteria"]
        if not isinstance(marks, dict) or set(marks) != expected:
            raise ValueError("fixed expectations must cover every canonical criterion")
        for mark in marks.values():
            if (not isinstance(mark, dict) or set(mark) != {"verdict", "reason"}
                    or mark["verdict"] not in {"met", "not_met", "contradicted"}
                    or not isinstance(mark["reason"], str) or not mark["reason"].strip()):
                raise ValueError("fixed expected verdict and substantive reason required")
        audit = example["assumption_audit"]
        if (not isinstance(audit, dict) or set(audit) != {"contract_preserved", "reasons"}
                or type(audit["contract_preserved"]) is not bool
                or not isinstance(audit["reasons"], list) or not audit["reasons"]
                or any(not isinstance(s, str) or not s.strip() for s in audit["reasons"])):
            raise ValueError("typed assumption audit and reasons required for authored expectations")
    return deepcopy(examples)


def load_capability_pilot():
    cases, identity = load_pilot()
    design = read_json(DESIGN)
    catalog, items, _ = load_catalog()
    if (design["catalog_hash"] != catalog["catalog_hash"]
            or design["fixture_sha256_lf"] != hashlib.sha256(FIXTURE.read_text(encoding="utf-8").encode()).hexdigest()
            or design["source_blind"] is not False or design["mathematical_admission_claimed"] is not False):
        raise ValueError("capability design is stale or its review class changed")
    reviews = {r["core_id"]: r for r in design["cases"]}
    if len(reviews) != len(design["cases"]) or set(reviews) != {c["task"]["core_id"] for c in cases}:
        raise ValueError("capability design must cover exactly the fixed pilot")
    for case in cases:
        task = case["task"]
        review, item = reviews[task["core_id"]], items[task["core_id"]]
        if (review["contract_hash"] != task["contract_hash"] or review["corpus_hash"] != digest(task["interfaces"])
                or review["canonical_rubric"] != item["rubric"]
                or review["canonical_rubric_hash"] != digest(item["rubric"])
                or review["canonical_assumptions"] != task["assumptions"]
                or review["canonical_conventions"] != task["conventions"]):
            raise ValueError("capability scope differs from the complete canonical question/rubric")
        eligible = [r for r in review["root_routes"] if r["eligible_in_curated_corpus"]]
        shortcuts = [n for r in review["root_routes"] if not r["eligible_in_curated_corpus"] for n in r["and_names"]]
        rubric = {"schema_version": "qcb.capability_rubric.v1", "task_hash": digest(task),
                  "core_id": task["core_id"], "contract_hash": task["contract_hash"],
                  "interface_policy_hash": digest(task["interfaces"]),
                  "reviewer": {"identity": design["author"], "kind": "ai", "method": design["review_class"]},
                  "source_bindings": [{k: s[k] for k in ("path", "sha256_lf")}
                                      for s in case["operator_metadata"]["source_bindings"]],
                  "routes": [{"id": r["route_id"], "required_names": r["and_names"],
                              "unscored_dependencies": ["Other imported foundation facts, tactics and provider helpers are not exhaustively enumerated."],
                              "scope_note": "Curated interfaces of the authored mechanism only; callable shortcuts outside this corpus: " + ", ".join(shortcuts)}
                             for r in eligible],
                  "obligation_groups": [{"obligation_id": g["obligation_id"], "required_names": g["and_names"],
                                         "provider_obligations": g["provider_obligations"]}
                                        for g in review["local_curated_interface_groups"]],
                  "knowledge_criteria": [{**deepcopy(c), "kind": "reasoning"} for c in item["rubric"]],
                  "knowledge_source": {"item_digest": digest(item), "rubric_digest": digest(item["rubric"]),
                                       "criterion_ids": [c["id"] for c in item["rubric"]],
                                       "scope": "whole_current_canonical_rubric"},
                  "limitations": ["Source-aware AI curation, not source-blind or human approval.",
                                  "Whole-root route-aligned return fraction is degenerate: all current interfaces support the authored route.",
                                  "Local obligation groups are not alternative whole-root routes; empty groups are unscored.",
                                  "Imported shortcuts remain callable; no retrieval can still accompany a correct proof.",
                                  "External semantic marks are supplied judgments, not Lean certificates or authenticated reviewer identities."]}
        case["capability_rubric"] = validate_rubric(task, rubric)
        case["engineered_explanations"] = validate_engineered_examples(review["engineered_explanation_fixture_pair"], item["rubric"])
    identity["capability_design_digest"] = digest(design)
    return cases, identity


def reports_from_record(record):
    if not isinstance(record, dict):
        raise TypeError("evaluator record must be an object")
    if record.get("schema_version") == "qcb.proof_session_report.v1":
        reports = [record]
    elif record.get("schema_version") == "qcb.authored_obligation_smoke.v1":
        reports = [r["session"] for r in record["results"]]
    else:
        raise ValueError("expected evaluator session report or authored-obligation smoke")
    if not 1 <= len(reports) <= 128 or len({digest(r) for r in reports}) != len(reports):
        raise ValueError("empty, oversized or duplicate session report set")
    return reports
