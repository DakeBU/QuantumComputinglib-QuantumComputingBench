#!/usr/bin/env python3
"""Audit/export the Lean curriculum or check its inspected authored references."""
import argparse
import asyncio
import json
import subprocess
import sys
import time
from copy import deepcopy
from pathlib import Path

B = Path(__file__).resolve().parents[1]
R = B.parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_authored_session import AuthoredReferenceVerifier
from qcb_core import digest, read_json, write_json
from qcb_evaluation_registry import _source_lineage, load_registry
from qcb_graph_course_pilot import EVIDENCE, FIXTURE, load_candidates, load_qualified
from qcb_integrity import text_sha
from qcb_lean_course import coverage, export_course
from qcb_model_loop import fixture_config, run_episode
from qcb_proof_session import ProofSession, SessionLimits

PLAN = B / "tracks/lean/curriculum/course-v1.json"


def pipeline_identity():
    paths = [Path(__file__), FIXTURE, PLAN]
    paths.extend(B / "src" / n for n in ("qcb_graph_course_pilot.py", "qcb_lean_course.py", "qcb_proof_session.py",
                                        "qcb_authored_session.py", "qcb_core.py", "qcb_curriculum.py", "qcb_lean.py", "qcb_integrity.py"))
    # Explicit semantic inputs avoid a self-referential receipt-directory glob.
    paths.extend(EVIDENCE / n for n in ("comparison.json", "be-decoder-input.json", "rank-decoder-input.json",
                                       "be-decoder.json", "rank-decoder.json", "context-extensions.json"))
    return {p.relative_to(R).as_posix(): text_sha(p) for p in paths}


def load_course():
    existing, base_status = load_registry()
    additional, new_status, catalog, graph = load_qualified()
    if existing.keys() & additional.keys():
        raise ValueError("course views must not overwrite an existing experimental registry view")
    views = {**existing, **additional}
    plan = read_json(PLAN)
    report = coverage(plan, views, catalog, graph)
    report["reference_qualification"] = {"original_pilot": base_status, "new_companions": new_status}
    return plan, views, catalog, graph, report


def compact(reply):
    return {k: deepcopy(reply[k]) for k in ("status", "failure_class", "request_hash", "proof_sha256",
                                            "execution_id", "kernel_checked", "axioms") if k in reply}


async def act(session, kind, **kwargs):
    result = await session.act({"kind": kind, "state_id": session.state_id, **kwargs})
    return result


async def check_references(cases, identity, build_root, raw, tested_code_commit):
    started = time.monotonic()
    rows = []
    for case in cases:
        task = case["task"]
        remaining = 1800 - (time.monotonic() - started)
        if remaining <= 0:
            raise TimeoutError("authored curriculum batch wall ceiling exhausted; preserve partial raw records")
        verifier = AuthoredReferenceVerifier(task, case["allowed_proofs"], build_root)
        session = ProofSession(task, verifier, limits=SessionLimits(wall_seconds=min(300, remaining)))
        row = {"core_id": task["core_id"], "task_hash": digest(task), "positive_obligations": [], "negative_controls": {}, "controls": {}}
        pending = {n["id"]: n for n in task["nodes"]}
        done = set()
        while pending:
            ready = [n for n in pending.values() if set(n["depends_on"]) <= done]
            for node in ready:
                if node["id"] == task["root_id"]:
                    for name, proof in case["negative_controls"].items():
                        reply = await act(session, "submit", node_id=node["id"], proof=proof)
                        row["negative_controls"][name] = compact(reply.get("evidence", reply))
                        print(json.dumps({"core": task["core_id"], "negative": name, "status": reply["status"]}), flush=True)
                reply = await act(session, "submit", node_id=node["id"], proof=case["references"][node["id"]])
                row["positive_obligations"].append({"node_id": node["id"], **compact(reply.get("evidence", reply))})
                print(json.dumps({"core": task["core_id"], "node": node["id"], "status": reply["status"]}), flush=True)
                if reply["status"] != "verified":
                    raw.append({"core_id": task["core_id"], "session": session.report(), "replays": verifier.replays})
                    raise RuntimeError("inspected authored obligation failed; no course qualification")
                done.add(node["id"]);del pending[node["id"]]
        final = await act(session, "finish")
        row["final_replay"] = compact(final.get("final_replay", final))
        raw.append({"core_id": task["core_id"], "condition": "provided_dag_repair", "session": session.report(), "replays": verifier.replays})
        row["metrics"] = session.report()["metrics"]
        for name, proof in case["controls"].items():
            remaining = 1800 - (time.monotonic() - started)
            if remaining <= 0:
                raise TimeoutError("authored batch wall ceiling exhausted")
            control = AuthoredReferenceVerifier(task, case["allowed_proofs"], build_root)
            root = ProofSession(task, control, mode="root_only", limits=SessionLimits(wall_seconds=min(180, remaining)))
            reply = await act(root, "submit", node_id=task["root_id"], proof=proof)
            row["controls"][name] = compact(reply.get("evidence", reply))
            # Standalone controls are checked once in fresh processes. They are
            # not relabelled as completed two-check protocol sessions.
            raw.append({"core_id": task["core_id"], "condition": name, "session": root.report(), "replays": control.replays})
            print(json.dumps({"core": task["core_id"], "control": name, "status": reply["status"]}), flush=True)
        row["passed"] = (session.report()["formal_root_checked"]
                         and all(v["status"] == "verified" and v.get("kernel_checked") is True for v in row["controls"].values())
                         and row["negative_controls"]["wrong_target"]["status"] == "compile_error"
                         and row["negative_controls"]["sorry_axiom"]["status"] == "compile_error"
                         and "sorryAx" in row["negative_controls"]["sorry_axiom"].get("axioms", []))
        rows.append(row)
        if not row["passed"]:
            raise RuntimeError("fresh-root/control/negative gate failed; preserve raw evidence")
    return {"schema_version": "qcb.graph_course_reference_replay.v1", **identity,
            "tested_code_commit": tested_code_commit,
            "results": rows, "passed": len(rows) == len(cases), "elapsed_seconds": time.monotonic()-started,
            "execution_class": "trusted_local_authored_reference", "isolated": False, "model_calls": 0,
            "model_performance_measured": False, "new_mathematical_cores": 0, "new_canonical_formal_admissions": 0,
            "blind_test": False, "standalone_controls_are_completed_protocol_sessions": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("audit", "export", "check-references", "run-fixture"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--split", choices=("train", "dev", "test_public"))
    parser.add_argument("--band", choices=("D1", "D2", "D3", "D4"))
    parser.add_argument("--mode", choices=("root_only", "proof_dag"))
    parser.add_argument("--exposure", choices=("closed_book", "approved_interface"))
    parser.add_argument("--build-root", type=Path)
    parser.add_argument("--trusted-local-reference", action="store_true")
    parser.add_argument("--raw-output", type=Path)
    parser.add_argument("--view")
    parser.add_argument("--episode-dir", type=Path)
    args = parser.parse_args()
    raw = []
    try:
        if args.command in {"audit", "check-references"} and (args.mode or args.exposure):
            raise ValueError("mode/exposure flags apply only to export or run-fixture")
        for path in (args.output, args.raw_output):
            if path and path.exists():
                raise FileExistsError("choose fresh outputs; prior receipts are preserved")
        if args.raw_output and args.raw_output.resolve().is_relative_to(R.resolve()):
            raise ValueError("raw reference trajectories must remain outside the public repository")
        if args.command == "check-references":
            if (not args.output or not args.build_root or not args.trusted_local_reference
                    or args.split or args.band or args.view or args.episode_dir):
                raise ValueError("reference replay requires output, matching build root and explicit authored-reference flag; no subset")
            sources = pipeline_identity()
            tested_code = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=R, text=True).strip()
            if not _source_lineage(tested_code, sources)["recorded_pipeline_matches_current_sources"]:
                raise ValueError("freeze and commit the exact reviewed reference pipeline before replay")
            cases, identity, _, _ = load_candidates()
            result = asyncio.run(check_references(cases, identity, args.build_root, raw, tested_code))
            if sources != pipeline_identity():
                raise ValueError("course pipeline changed during replay; do not promote this run")
            result["pipeline_source_hashes_lf"] = sources
            result["receipt_digest"] = digest(result)
        else:
            if args.build_root or args.trusted_local_reference or args.raw_output:
                raise ValueError("compiler options apply only to check-references")
            plan, views, catalog, graph, report = load_course()
            if args.command == "run-fixture":
                if not args.view or not args.episode_dir or args.split or args.band or args.output:
                    raise ValueError("fixture requires one view and a fresh private episode directory")
                result = asyncio.run(run_episode(views[args.view], fixture_config(mode=args.mode or "proof_dag", exposure=args.exposure or "approved_interface"), args.episode_dir, fixture=True))
                print(json.dumps({k: result[k] for k in ("status", "provider_calls", "model_calls_confirmed", "formal_proof_success")}))
                return 0 if result["status"] == "fixture_protocol_complete" else 2
            if args.view or args.episode_dir or args.command == "audit" and (args.split or args.band):
                raise ValueError("selection filters apply to export; episode options to run-fixture")
            result = (report if args.command == "audit" else
                      export_course(plan, views, catalog, graph, split=args.split, band=args.band, mode=args.mode or "proof_dag", exposure=args.exposure or "approved_interface"))
            if args.command == "export" and not args.output:
                raise ValueError("export requires a fresh --output")
        if args.output:
            write_json(args.output, result, immutable=True)
            print(json.dumps({"output": str(args.output), "passed": result.get("passed"), "model_calls": 0}))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1
    finally:
        if args.raw_output and raw:
            write_json(args.raw_output, {"execution_class": "trusted_local_authored_reference", "records": raw}, immutable=True)


if __name__ == "__main__":
    raise SystemExit(main())
