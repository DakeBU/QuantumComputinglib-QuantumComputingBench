#!/usr/bin/env python3
"""Export fixed pilot inputs or replay inspected authored protocol fixtures."""
import argparse
import asyncio
import json
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_authored_session import AuthoredReferenceVerifier
from qcb_core import digest, write_json
from qcb_obligation_pilot import (
    EXPECTED_CORES,
    export_pilot,
    load_pilot,
    pipeline_identity,
)
from qcb_proof_session import ProofSession, SessionLimits


async def _act(session, kind, **payload):
    return await session.act({"kind": kind, "state_id": session.state_id, **payload})


async def smoke(cases, identity, build_root):
    if {c["task"]["core_id"] for c in cases} != EXPECTED_CORES or len(cases) != len(EXPECTED_CORES):
        raise ValueError("refuse vacuous or incomplete fixed-cohort smoke")
    results = []
    for case in cases:
        task = case["task"]
        # Each control gets the same declared ceilings/exposure and provided DAG.
        # Actual costs differ and are reported, not asserted to be compute-matched.
        for condition in ("library_application", "constructed_whole_root", "provided_dag_repair"):
            verifier = AuthoredReferenceVerifier(task, case["allowed_proofs"], build_root)
            session = ProofSession(task, verifier,
                                   mode="proof_dag" if condition == "provided_dag_repair" else "root_only",
                                   limits=SessionLimits(wall_seconds=300))
            checks = []
            if condition == "provided_dag_repair":
                query = "sqrt sum" if task["core_id"] == "qcb-core-sp-005" else "det updateRow"
                retrieved = await _act(session, "search", query=query)
                checks.append(retrieved["status"] == "returned" and bool(retrieved["entries"]))
                wrong = case["wrong_reference"]
                rejected = await _act(session, "submit", node_id=wrong["node_id"], proof=wrong["proof"])
                checks.append(rejected["status"] == "compile_error" and rejected["failure_class"] == "IMPLEMENTATION_FAILED")
                # This authored explanation marker is deliberately ungraded; no
                # fabricated model/rubric accuracy is inferred from a fixed script.
                explanation = await _act(session, "explain", answer="Authored smoke only; semantic response not evaluated.")
                checks.append(explanation.get("semantic_score") is None)
                pending = {n["id"]: n for n in task["nodes"]}
                done = set()
                while pending:
                    ready = [n for n in pending.values() if set(n["depends_on"]) <= done]
                    for node in ready:
                        response = await _act(session, "submit", node_id=node["id"], proof=case["references"][node["id"]])
                        checks.append(response["status"] == "verified")
                        done.add(node["id"])
                        del pending[node["id"]]
            else:
                response = await _act(session, "submit", node_id=task["root_id"], proof=case["controls"][condition])
                checks.append(response["status"] == "verified")
            final = await _act(session, "finish")
            checks.append(final["status"] == "verified")
            report = session.report()
            results.append({"condition": condition, "checks_passed": all(checks),
                            "checks": checks, "session": report, "replays": verifier.replays})
            print(json.dumps({"core_id": task["core_id"], "condition": condition,
                              "checks_passed": all(checks), "verifier_calls": report["metrics"]["verifier_calls"]}), flush=True)
    result = {"schema_version": "qcb.authored_obligation_smoke.v1", **identity,
              "passed": all(r["checks_passed"] for r in results), "results": results,
              "execution_class": "trusted_local_authored_reference", "isolated": False,
              "model_performance_measured": False, "model_calls": 0, "blind_test": False,
              "distinct_mathematical_cores": len(cases), "new_mathematical_cores": 0,
              "new_formal_view_admissions": 0,
              "comparison_scope": "Authored engineering controls; root-only permits repeated attempts; no causal strategy or model claim.",
              "knowledge_semantic_score": None, "matched_realized_compute_established": False}
    result["receipt_digest"] = digest(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("export-pilot", "smoke"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--build-root", type=Path)
    parser.add_argument("--trusted-local-reference", action="store_true")
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise FileExistsError("choose a fresh output; prior evidence is preserved")
        if args.command == "smoke" and (not args.trusted_local_reference or not args.build_root):
            raise ValueError("smoke requires explicit --trusted-local-reference and an already-built --build-root")
        if args.command == "export-pilot" and (args.trusted_local_reference or args.build_root):
            raise ValueError("export does not execute Lean or accept runtime options")
        cases, identity = load_pilot()
        identity["pipeline_source_hashes_lf"] = pipeline_identity()
        result = (export_pilot(cases, identity) if args.command == "export-pilot"
                  else asyncio.run(smoke(cases, identity, args.build_root)))
        if pipeline_identity() != identity["pipeline_source_hashes_lf"]:
            raise ValueError("pipeline/fixture changed during the run; preserve draft evidence separately and rerun")
        write_json(args.output, result, immutable=True)
        print(json.dumps({"output": str(args.output), "passed": result.get("passed"),
                          "tasks": len(cases), "model_performance_measured": False}))
        return 0 if result.get("passed", True) else 1
    except (ValueError, OSError, KeyError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
