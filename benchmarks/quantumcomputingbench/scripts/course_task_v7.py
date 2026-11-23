#!/usr/bin/env python3
"""Produce or verify a reproducible, answer-free single-task course v7 contract."""
import argparse
import json
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[1]
R = B.parents[1]
sys.path[:0] = [str(B / "src"), str(R)]
from qcb_core import digest, read_json, write_json
from qcb_course_registry_v7 import load_course_registry
from qcb_proof_session import ProofSession
from website.scripts.proof_inputs import proof_input_digest


def package(view_id, mode, exposure, *, registry=None):
    views, identity = load_course_registry() if registry is None else registry
    if view_id not in views:
        raise ValueError("unknown qualified v7 task")
    view = views[view_id]
    task, entry = view["task"], view["entry"]
    if mode not in entry["allowed_modes"] or exposure not in entry["allowed_exposures"]:
        raise ValueError("unsupported task condition")
    payload = ProofSession(task, mode=mode, exposure=exposure).agent_input()
    output = {
        "schema_version": "qcb.course_task_package.v1",
        "suite_id": identity["suite_id"], "registry_digest": identity["registry_digest"],
        "view_id": view_id, "core_id": task["core_id"], "split": task["split"], "family": task["family"],
        "task_hash": entry["task_hash"], "condition": {"mode": mode, "exposure": exposure,
            "obligation_visibility": "provided_in_both_submission_modes",
            "library_graph_slice": "not_explicitly_provided", "autonomous_plan_test": False},
        "environment": {"lean_toolchain": (R / "lean-toolchain").read_text(encoding="utf-8").strip(),
            "library_revision": task["library_revision"], "proof_inputs_sha256": proof_input_digest(R),
            "imports": payload["task"]["imports"],
            "isolation_required_for_model_generated_lean": True,
            "isolated_runtime_qualified_by_this_package": False},
        "input": payload,
        "grading_contract": {"exact_root_required": True, "fresh_final_kernel_replay_required": True,
            "transitive_axiom_policy_required": True, "explanation_separately_graded": True,
            "reference_proofs_included": False, "model_performance_measured": False,
            "public_test_is_hidden": False, "fixture_success_is_model_success": False},
        "runner": {"entrypoint": "benchmarks/quantumcomputingbench/scripts/evaluate_course_v7.py",
            "commands": ["plan", "run-fixture", "run"], "operator_profile_required_for_run": True,
            "authorization_and_isolation_required_for_run": True,
            "environment_kind": "pinned_task_specification_not_a_container_image"},
    }
    output["package_digest"] = digest(output)
    return output


def verify(record, *, registry=None):
    if not isinstance(record, dict):
        raise ValueError("task package must be an object")
    condition = record["condition"]
    expected = package(record["view_id"], condition["mode"], condition["exposure"], registry=registry)
    if record != expected:
        raise ValueError("task package differs from the selected qualified registry and condition")
    return {"passed": True, "package_digest": expected["package_digest"], "model_calls": 0,
            "model_generated_lean_executed": False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    create = sub.add_parser("package")
    create.add_argument("--view", required=True)
    create.add_argument("--mode", choices=("root_only", "proof_dag"), default="proof_dag")
    create.add_argument("--exposure", choices=("closed_book", "approved_interface"), default="approved_interface")
    create.add_argument("--output", type=Path, required=True)
    check = sub.add_parser("verify")
    check.add_argument("--input", type=Path, required=True)
    args = p.parse_args()
    try:
        if args.command == "package":
            if args.output.exists():
                raise FileExistsError("choose a new output path")
            record = package(args.view, args.mode, args.exposure)
            write_json(args.output, record, immutable=True)
            result = {"package_digest": record["package_digest"], "reference_proofs_included": False}
        else:
            if args.input.stat().st_size > 1024 * 1024:
                raise ValueError("task package exceeds 1 MiB")
            result = verify(read_json(args.input))
        print(json.dumps(result))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
