"""Evaluator-owned public pilot views with exact recorded-reference lineage.

Registration qualifies reference tasks, not live model predictions. Historical
kernel observations retain their source revisions. Nothing in this module runs
Lean, accepts an agent-supplied receipt, or changes the shared core catalog.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
from copy import deepcopy
from pathlib import PurePosixPath

from qcb_core import digest, read_json
from qcb_integrity import text_sha
from qcb_lean import APPROVED_AXIOMS
from qcb_obligation_pilot import B, R, load_pilot
from qcb_proof_session import ProofSession, SessionLimits, proof_sha
from qcb_sequential_pilot import load_sequential_pilot

MANIFEST = B / "tracks/lean/evaluation/agentic-registry-v1.json"
SOURCES = {
    "obligation-v1": {
        "loader": load_pilot,
        "checkpoint": "reports/lean-agentic-v1/execution-summary.json",
        "checkpoint_schema": "qcb.authored_obligation_checkpoint.v1",
        "code_revision": "1e073e02bfdee4bb0412959277f112aff7417f2b",
        "conditions": ("library_application", "constructed_whole_root", "provided_dag_repair"),
        "verified_checks": 20,
        "fresh_field": "successful_root_fresh_replays",
    },
    "sequential-v1": {
        "loader": load_sequential_pilot,
        "checkpoint": "reports/lean-agentic-capabilities-v1/sequential-execution.json",
        "checkpoint_schema": "qcb.sequential_authored_checkpoint.v1",
        "code_revision": "c3a01b8a8becd49a9290f64f261a3be17021d791",
        "conditions": ("library_control", "constructed_whole_root", "provided_dag_repair"),
        "verified_checks": 16,
        "fresh_field": "fresh_root_replays",
    },
}
EXPECTED_CORES = {"qcb-core-la-102", "qcb-core-sp-005", "qcb-core-sp-007", "qcb-core-sp-008"}


def _source_lineage(revision, hashes):
    if not re.fullmatch(r"[0-9a-f]{40}", revision) or not isinstance(hashes, dict) or not hashes:
        raise ValueError("recorded source revision and pipeline hashes required")
    current_matches = True
    for path, expected in hashes.items():
        if not isinstance(path, str):
            raise TypeError("pipeline locator must be text")
        parts = PurePosixPath(path).parts
        if (".." in parts or "\\" in path or ":" in path or PurePosixPath(path).is_absolute()
                or not path.startswith(("benchmarks/quantumcomputingbench/", "website/scripts/"))
                or not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected)):
            raise ValueError("invalid recorded pipeline source identity")
        # Read immutable Git blobs only, never import/execute historical code.
        source = subprocess.check_output(["git", "show", revision + ":" + path], cwd=R, timeout=10)
        if hashlib.sha256(source.replace(b"\r\n", b"\n")).hexdigest() != expected:
            raise ValueError("recorded pipeline hash differs from its pinned Git revision")
        current_path = R / path
        current_matches = (current_matches and current_path.is_file()
                           and current_path.resolve().is_relative_to(R.resolve()) and text_sha(current_path) == expected)
    return {"recorded_code_revision": revision, "recorded_pipeline_matches_current_sources": current_matches,
            "reference_replayed_during_registry_validation": False}


def _check_checkpoint(record, source, cases, entries, source_checker=_source_lineage):
    copy = deepcopy(record)
    claimed = copy.pop("checkpoint_digest", None)
    if (record.get("schema_version") != source["checkpoint_schema"] or digest(copy) != claimed
            or record.get("passed") is not True or record.get("isolated") is not False
            or record.get("execution_class") != "trusted_local_authored_reference"
            or record.get("model_performance_measured") is not False
            or type(record.get("model_calls")) is not int or record["model_calls"] != 0
            or type(record.get("new_mathematical_cores")) is not int or record["new_mathematical_cores"] != 0):
        raise ValueError("reference checkpoint is stale or has an unsupported evidence class")
    if any(e["checkpoint_digest"] != claimed for e in entries):
        raise ValueError("reference checkpoint differs from the registered pinned content")
    if (record.get("actual_replay_status_counts") != {"verified": source["verified_checks"], "compile_error": 2}
            or type(record.get(source["fresh_field"])) is not int or record[source["fresh_field"]] != 6
            or type(record.get("distinct_mathematical_cores")) is not int or record["distinct_mathematical_cores"] != len(cases)):
        raise ValueError("reference checkpoint lacks complete positive/negative/fresh-root evidence")
    rows = record.get("conditions")
    expected = {(c["task"]["core_id"], condition) for c in cases for condition in source["conditions"]}
    if (not isinstance(rows, list) or len(rows) != len(expected)
            or {(r.get("core_id"), r.get("condition")) for r in rows} != expected):
        raise ValueError("reference checkpoint must cover the exact core/condition Cartesian set")
    by_core = {c["task"]["core_id"]: c for c in cases}
    for row in rows:
        case = by_core[row["core_id"]]
        task = case["task"]
        proof = (case["references"][task["root_id"]] if row["condition"] == "provided_dag_repair"
                 else case["controls"][row["condition"]])
        final = row.get("final_replay", {})
        status = row.get("passed", row.get("checks_passed"))
        if (status is not True or row.get("formal_root_checked") is not True
                or row.get("task_hash") != digest(task) or final.get("status") != "verified"
                or final.get("kernel_checked") is not True or final.get("proof_sha256") != proof_sha(proof)
                or not isinstance(final.get("axioms"), list)
                or any(not isinstance(a, str) for a in final["axioms"])
                or set(final["axioms"]) - APPROVED_AXIOMS
                or not isinstance(final.get("request_hash"), str) or not re.fullmatch(r"[0-9a-f]{64}", final["request_hash"])
                or not isinstance(final.get("execution_id"), str) or not final["execution_id"]):
            raise ValueError("reference condition lacks exact bound fresh-root/axiom evidence")
    if record.get("tested_code_commit", source["code_revision"]) != source["code_revision"]:
        raise ValueError("reference checkpoint was relabelled with another source revision")
    return source_checker(source["code_revision"], record["pipeline_source_hashes_lf"])


def qualify(manifest, cohorts, checkpoints, source_checker=_source_lineage):
    """Inspect fixed evaluator artifacts; never called with proving-agent data."""
    if (manifest.get("schema_version") != "qcb.agentic_evaluation_registry.v1"
            or manifest.get("suite_id") != "qcb-agentic-public-pilot-v1"
            or manifest.get("suite_status") != "reference_qualified_public_pilot_not_stable_release"
            or manifest.get("blind_test") is not False or manifest.get("isolated_model_evaluation") != "ENV_BLOCKED"
            or set(cohorts) != set(SOURCES) or set(checkpoints) != set(SOURCES)):
        raise ValueError("unexpected pilot registry or source scope")
    entries = manifest.get("entries")
    if (not isinstance(entries, list) or len(entries) != len(EXPECTED_CORES)
            or {e.get("core_id") for e in entries} != EXPECTED_CORES
            or len({e.get("view_id") for e in entries}) != len(entries)):
        raise ValueError("registry must preserve all four unique shared-core task views")
    admitted, lineages = {}, {}
    for name, source in SOURCES.items():
        cases, identity = cohorts[name]
        selected = [e for e in entries if e.get("cohort") == name]
        if len(selected) != len(cases) or {e["core_id"] for e in selected} != {c["task"]["core_id"] for c in cases}:
            raise ValueError("registry provider/task coverage changed")
        record = checkpoints[name]
        for key in ("catalog_hash", "library_revision", "lean_toolchain", "proof_inputs_sha256"):
            if manifest[key] != identity[key] or record[key] != identity[key]:
                raise ValueError("registry/checkpoint library or catalog identity drift: " + key)
        if record["fixture_digest"] != identity["fixture_digest"] or record["fixture_sha256_lf"] != identity["fixture_sha256_lf"]:
            raise ValueError("reference evidence belongs to another fixed fixture")
        lineages[name] = _check_checkpoint(record, source, cases, selected, source_checker)
        by_core = {c["task"]["core_id"]: c for c in cases}
        for entry in selected:
            task = by_core[entry["core_id"]]["task"]
            root = next(n for n in task["nodes"] if n["id"] == task["root_id"])
            if (entry["view_id"] != "qcb-agentic-" + task["core_id"].removeprefix("qcb-core-") + "-v1"
                    or any(entry[k] != task[k] for k in ("core_id", "contract_hash", "family", "split", "snapshot_id"))
                    or entry["task_hash"] != digest(task) or entry["root_target_digest"] != digest(root["target"])
                    or entry["reference_checkpoint"] != source["checkpoint"]
                    or entry["pipeline_code_revision"] != source["code_revision"]
                    or entry["allowed_modes"] != ["root_only", "proof_dag"]
                    or entry["allowed_exposures"] != ["closed_book", "approved_interface"]
                    or entry["registration_scope"] != "reference_qualified_public_pilot_root; supplied_plan; explanations_separately_graded"
                    or entry["new_mathematical_cores"] != 0):
                raise ValueError("registered view differs from its current immutable task")
            admitted[entry["view_id"]] = {"entry": deepcopy(entry), "task": deepcopy(task),
                                          "registry_digest": digest(manifest),
                                          "reference_lineage": deepcopy(lineages[name])}
    return admitted, {"schema_version": "qcb.agentic_registry_qualification.v1", "suite_id": manifest["suite_id"],
                      "registry_digest": digest(manifest), "catalog_hash": manifest["catalog_hash"],
                      "qualified_views": len(admitted), "distinct_shared_core_ids": len(EXPECTED_CORES),
                      "new_mathematical_cores": 0, "new_canonical_formal_admissions": 0,
                      "source_lineages": lineages, "live_formal_certificates_issued": 0,
                      "validation_performed_lean_replay": False, "model_performance_measured": False,
                      "blind_test": False, "isolated_model_evaluation": "ENV_BLOCKED",
                      "qualification_scope": "Recorded reference evidence and exact root alignment; not live model success or stable release"}


def load_registry():
    manifest = read_json(MANIFEST)
    cohorts = {name: source["loader"]() for name, source in SOURCES.items()}
    checkpoints = {name: read_json(B / source["checkpoint"]) for name, source in SOURCES.items()}
    return qualify(manifest, cohorts, checkpoints)


def export_views(views, qualification, *, mode="proof_dag", exposure="approved_interface", split=None, view_ids=None):
    if mode not in {"root_only", "proof_dag"} or exposure not in {"closed_book", "approved_interface"}:
        raise ValueError("unsupported evaluation condition")
    if split not in {None, "train", "dev", "test_public"}:
        raise ValueError("unknown split")
    selected = set(views) if view_ids is None else set(view_ids)
    if not selected or selected - views.keys() or view_ids is not None and len(selected) != len(view_ids):
        raise ValueError("unknown, empty or duplicate view selection")
    tasks = []
    for key in sorted(selected):
        view = views[key]
        if split is not None and view["task"]["split"] != split:
            continue
        session = ProofSession(view["task"], mode=mode, exposure=exposure, limits=SessionLimits(wall_seconds=300))
        tasks.append({"view_id": key, "input": session.agent_input()})
    if not tasks:
        raise ValueError("selection contains no task in the requested split")
    return {"schema_version": "qcb.agentic_evaluation_export.v1", "suite_id": qualification["suite_id"],
            "registry_digest": qualification["registry_digest"], "tasks": tasks,
            "selected_views": len(tasks), "distinct_shared_core_ids": len({t["input"]["task"]["core_id"] for t in tasks}),
            "new_mathematical_cores": 0, "blind_test": False, "model_performance_measured": False,
            "candidate_execution": "disabled; accepted isolation required", "reference_answers_projected": False}
