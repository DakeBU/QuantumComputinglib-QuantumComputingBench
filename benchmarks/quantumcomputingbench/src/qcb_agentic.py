"""Audit the Lean evaluation frontier and export existing warmups, never proofs.

This is not an interactive executor, model baseline, or new core admission.
The public reference cohort cannot become a blind test by hiding a JSON field.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy

from qcb_core import digest
from qcb_curriculum import core_contract

SCHEMA = "qcb.lean_agentic_frontier.v1"
TASK_SCHEMA = "qcb.lean_warmup_projection.v1"
MODES = {
    "knowledge_and_statement_understanding": {
        "role": "prerequisite and separate semantic/rubric assessment",
        "status": "existing_nl_views_not_kernel_certified_prose",
    },
    "single_shot_library_application": {
        "role": "honest formal API-application baseline",
        "status": "fixed_references_available_isolated_predictions_blocked",
    },
    "premise_retrieval": {
        "role": "retrieve admissible declarations without held-out solutions",
        "status": "needs_task_scoped_interfaces_and_retrieval_metrics",
    },
    "multi_node_proof_construction": {
        "role": "compose reviewed mathematical dependencies into a fixed root",
        "status": "needs_nontrivial_targets_and_a_broader_reviewed_proof_protocol",
    },
    "incremental_lean_feedback": {
        "role": "submit parseable tactic blocks with scoped state and final replay",
        "status": "needs_stateful_executor_and_independent_final_replay",
    },
    "diagnostic_driven_repair": {
        "role": "repair failed attempts without changing the target or assumptions",
        "status": "needs_version_bound_attempts_and_repair_evaluation",
    },
}


def _cores(catalog):
    cores = catalog["cores"]
    ids = [c["core_id"] for c in cores]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate shared core identity")
    if set(ids) & {c["core_id"] for c in catalog.get("withheld_cores", [])}:
        raise ValueError("withheld and admitted core scopes overlap")
    return cores


def _formal(core):
    view = core.get("views", {}).get("lean")
    if view is None:
        return None
    if (view.get("status") != "reference_and_alignment_checked"
            or view.get("task_kind") != "library_lemma_application"
            or view.get("execution_class") != "trusted_local_reference"
            or view.get("isolated") is not False):
        raise ValueError("unsupported formal evidence class; review before projecting")
    if view.get("nl_explanation_certified_by_kernel") is not False:
        raise ValueError("formal evidence cannot certify the entire explanation")
    return view


def audit_catalog(catalog):
    """Use the resolved canonical catalog, not counts copied into a new ledger."""
    cores = _cores(catalog)
    formal = [c for c in cores if _formal(c) is not None]
    return {
        "schema_version": SCHEMA,
        "catalog_hash": catalog["catalog_hash"],
        "snapshot_id": catalog["snapshot_id"],
        "graph_source_commit": catalog["graph_source_commit"],
        "counts": {
            "admitted_mathematical_cores": len(cores),
            "lean_warmup_views": len(formal),
            "distinct_lean_warmup_cores": len({c["core_id"] for c in formal}),
            "admitted_cores_without_formal_views": len(cores) - len(formal),
            "withheld_cores_not_current_gold": len(catalog.get("withheld_cores", [])),
        },
        "formal_core_ids": [c["core_id"] for c in formal],
        "formal_views_by_split": dict(sorted(Counter(c["split"] for c in formal).items())),
        "formal_views_by_part": dict(sorted(Counter(c["part"] for c in formal).items())),
        "without_formal_view": [c["core_id"] for c in cores if "lean" not in c.get("views", {})],
        "withheld_core_ids": [c["core_id"] for c in catalog.get("withheld_cores", [])],
        "capabilities": deepcopy(MODES),
        "evidence_boundaries": {
            "new_core_admissions": 0,
            "deep_proof_synthesis_established": False,
            "model_performance_measured": False,
            "isolated_prediction_evaluation": catalog["isolated_prediction_evaluation"],
            "global_semantic_dedup_complete": catalog["global_semantic_dedup_complete"],
            "graph_topology_is_proof_dependency_depth": False,
            "legal_tactic_implies_useful_progress": False,
            "public_reference_cohort_is_blind_test": False,
        },
    }


def export_warmups(catalog, items, *, split=None):
    """Closed-book input projection only; never execute a candidate or copy gold.

    Callers must obtain catalog/items from load_catalog(), which rechecks source,
    semantic and historical kernel bindings. No invented retrieval scope or new
    split is accepted here. Public reference exposure remains explicitly visible.
    """
    if split not in {None, "train", "dev", "test_public"}:
        raise ValueError("unknown split")
    tasks = []
    for core in _cores(catalog):
        formal = _formal(core)
        if formal is None or (split is not None and core["split"] != split):
            continue
        item = items[core["core_id"]]
        if (digest(item) != core["item_digest"]
                or digest(core_contract(item)) != core["contract_hash"]
                or any(item[k] != core[k] for k in ("core_id", "family", "split"))):
            raise ValueError("resolved question or split differs from canonical core")
        # Explicit allowlists: reference answers, proofs, rubrics, reviews, steps,
        # titles and arbitrary new metadata cannot silently enter model input.
        task = {
            "schema_version": TASK_SCHEMA,
            "task_id": formal["view_id"],
            "core_id": core["core_id"],
            "contract_hash": core["contract_hash"],
            "source_item_digest": core["item_digest"],
            "snapshot_id": core["snapshot_id"],
            "family": core["family"],
            "split": core["split"],
            "task_kind": "library_lemma_application",
            "exposure": "closed_book",
            "question": item["question"],
            "assumptions": deepcopy(item["assumptions"]),
            "conventions": deepcopy(item["conventions"]),
            "formal_context": {
                k: deepcopy(formal["formal_context"][k]) for k in ("imports", "target")
            },
            "answer_format": "restricted_lean_application",
            "proof_language": "existing qcb_lean application grammar; not general tactic blocks",
            "mathematical_scope": "formal conclusion only; NL explanation is separately assessed",
        }
        task["task_hash"] = digest(task)
        tasks.append(task)
    if len({t["task_id"] for t in tasks}) != len(tasks):
        raise ValueError("duplicate formal task identity")
    return {
        "schema_version": "qcb.lean_warmup_export.v1",
        "catalog_hash": catalog["catalog_hash"],
        "snapshot_id": catalog["snapshot_id"],
        "graph_source_commit": catalog["graph_source_commit"],
        "tasks": tasks,
        "distinct_mathematical_cores": len({t["core_id"] for t in tasks}),
        "new_core_admissions": 0,
        "candidate_execution": "disabled; this command only projects existing task inputs",
        "answer_exposure": "Reference answers and proofs already exist publicly; not blind or contamination-free.",
        "model_performance_measured": False,
        "limitations": [
            "This is a warmup input projection, not an agentic executor or grading release.",
            "The existing baseline runner does not consume this new schema automatically.",
            "No approved-interface or open-library policy is invented by this export.",
            "Hiding answer fields does not remove prior public exposure.",
        ],
    }
