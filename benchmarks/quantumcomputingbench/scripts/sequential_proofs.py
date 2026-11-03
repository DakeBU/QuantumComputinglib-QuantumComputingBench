#!/usr/bin/env python3
"""Export or replay inspected sequential State Preparation proof companions."""
import argparse
import asyncio
import hashlib
import json
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[1]
R = B.parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_authored_session import AuthoredReferenceVerifier
from qcb_core import digest, write_json
from qcb_proof_session import ProofSession, SessionLimits
from qcb_sequential_pilot import (
    EVIDENCE,
    EXPECTED_CORES,
    FIXTURE,
    export_sequential,
    load_sequential_pilot,
)


def pipeline_identity():
    paths = [Path(__file__), FIXTURE, *EVIDENCE.glob("*.json")]
    paths.extend(B / "src" / name for name in ("qcb_sequential_pilot.py", "qcb_proof_session.py",
                                               "qcb_authored_session.py", "qcb_core.py", "qcb_curriculum.py", "qcb_lean.py"))
    return {p.relative_to(R).as_posix(): hashlib.sha256(p.read_text(encoding="utf-8").encode()).hexdigest() for p in paths}


async def _act(session, kind, **payload):
    return await session.act({"kind": kind, "state_id": session.state_id, **payload})


async def check_references(cases, identity, build_root):
    if {c["task"]["core_id"] for c in cases} != EXPECTED_CORES or len(cases) != len(EXPECTED_CORES):
        raise ValueError("refuse empty or incomplete sequential cohort")
    results = []
    for case in cases:
        task = case["task"]
        for condition in ("library_control", "constructed_whole_root", "provided_dag_repair"):
            verifier = AuthoredReferenceVerifier(task, case["allowed_proofs"], build_root)
            session = ProofSession(task, verifier, mode="proof_dag" if condition == "provided_dag_repair" else "root_only",
                                   limits=SessionLimits(wall_seconds=300))
            checks = []
            if condition == "provided_dag_repair":
                result = await _act(session, "search", query="Matrix")
                checks.append(result["status"] == "returned")
                pending = {n["id"]: n for n in task["nodes"]}
                done = set()
                while pending:
                    ready = [n for n in pending.values() if set(n["depends_on"]) <= done]
                    for node in ready:
                        if node["id"] == case["wrong_reference"]["node_id"]:
                            rejected = await _act(session, "submit", node_id=node["id"], proof=case["wrong_reference"]["proof"])
                            checks.append(rejected["status"] == "compile_error" and rejected["failure_class"] == "IMPLEMENTATION_FAILED")
                        result = await _act(session, "submit", node_id=node["id"], proof=case["references"][node["id"]])
                        checks.append(result["status"] == "verified")
                        done.add(node["id"])
                        del pending[node["id"]]
            else:
                result = await _act(session, "submit", node_id=task["root_id"], proof=case["controls"][condition])
                checks.append(result["status"] == "verified")
            final = await _act(session, "finish")
            checks.append(final["status"] == "verified")
            report = session.report()
            results.append({"condition": condition, "checks_passed": all(checks), "checks": checks,
                            "library_control_one_call": case["library_control_one_call"],
                            "semantic_coverage": case["semantic_coverage"], "session": report, "replays": verifier.replays})
            print(json.dumps({"core_id": task["core_id"], "condition": condition,
                              "checks_passed": all(checks), "verifier_calls": report["metrics"]["verifier_calls"]}), flush=True)
    result = {"schema_version": "qcb.sequential_authored_replay.v1", **identity, "results": results,
              "passed": all(r["checks_passed"] for r in results), "distinct_mathematical_cores": len(cases),
              "new_mathematical_cores": 0, "new_canonical_formal_admissions": 0,
              "execution_class": "trusted_local_authored_reference", "isolated": False,
              "model_calls": 0, "model_performance_measured": False, "blind_test": False,
              "knowledge_semantic_score": None, "matched_realized_compute_established": False}
    result["receipt_digest"] = digest(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("export", "check-references"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--build-root", type=Path)
    parser.add_argument("--trusted-local-reference", action="store_true")
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise FileExistsError("choose a fresh output; preserve prior evidence")
        if args.command == "check-references" and (not args.trusted_local_reference or not args.build_root):
            raise ValueError("reference replay requires explicit --trusted-local-reference and an already-built --build-root")
        if args.command == "export" and (args.trusted_local_reference or args.build_root):
            raise ValueError("export never executes Lean or accepts runtime options")
        sources = pipeline_identity()
        cases, identity = load_sequential_pilot()
        identity["pipeline_source_hashes_lf"] = sources
        result = (export_sequential(cases, identity) if args.command == "export"
                  else asyncio.run(check_references(cases, identity, args.build_root)))
        if sources != pipeline_identity():
            raise ValueError("pipeline changed during this run; do not promote this draft")
        write_json(args.output, result, immutable=True)
        print(json.dumps({"output": str(args.output), "passed": result.get("passed"), "model_calls": 0}))
        return 0 if result.get("passed", True) else 1
    except (ValueError, OSError, KeyError, TypeError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
