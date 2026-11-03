#!/usr/bin/env python3
"""Offline capability diagnostics and evaluator-only semantic review templates."""
import argparse
import asyncio
import hashlib
import json
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[1]
R = B.parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_capabilities import assess
from qcb_capability_pilot import load_capability_pilot, reports_from_record
from qcb_core import digest, read_json, write_json
from qcb_proof_session import ProofSession


def _read(path):
    if path.stat().st_size > 10 * 1024 * 1024:
        raise ValueError("evaluator input exceeds the 10 MiB record limit")
    return read_json(path)


def pipeline_identity():
    paths = [Path(__file__), B / "tracks/lean/evaluation/capability-design-v1.json",
             B / "tracks/lean/fixtures/obligation-pilot-v1.json"]
    paths.extend(B / "src" / name for name in ("qcb_capabilities.py", "qcb_capability_pilot.py",
                                               "qcb_proof_session.py", "qcb_core.py", "qcb_curriculum.py"))
    return {p.relative_to(R).as_posix(): hashlib.sha256(p.read_text(encoding="utf-8").encode()).hexdigest() for p in paths}


def templates(cases, reports):
    by_hash = {digest(c["task"]): c for c in cases}
    result = []
    for report in reports:
        case = by_hash[report["task_hash"]]
        # Validate the report before projecting any explanation to a judge.
        assess(case["task"], report, case["capability_rubric"])
        for index, answer in enumerate(report["explanations"]):
            result.append({"schema_version": "qcb.explanation_adjudication_template.v1",
                           "task_hash": digest(case["task"]), "report_digest": digest(report),
                           "rubric_digest": digest(case["capability_rubric"]),
                           "answer_index": index, "answer_digest": digest(answer),
                           "reviewer": {"identity": "", "kind": None, "method": ""},
                           "respondent_identity": "", "criteria": [
                               {"id": c["id"], "score": None, "reasoning": ""}
                               for c in case["capability_rubric"]["knowledge_criteria"]],
                           "semantic_fidelity": "uncertain", "reasoning": "",
                           "judge_context": {"question": case["task"]["question"],
                                             "assumptions": case["task"]["assumptions"],
                                             "conventions": case["task"]["conventions"], "answer": answer,
                                             "rubric": case["capability_rubric"]["knowledge_criteria"]},
                           "instructions": "Evaluator-only template, not an accepted grade. Review every criterion and assumptions; then remove judge_context/instructions and explicitly use schema qcb.explanation_adjudication.v1. Do not infer semantic truth or reviewer authenticity from schema acceptance."})
    return result


async def fixture_reports(cases):
    """Replay fixed authored examples/expected marks; no new semantic judging."""
    reports, marks = [], []
    for case in cases:
        for example in case["engineered_explanations"]:
            session = ProofSession(case["task"])
            # Exact names exercise the real scoped search surface, with a
            # second query for any names omitted by the six-result cap.
            missing = [e["name"] for e in case["task"]["interfaces"]]
            for _ in range(2):
                response = await session.act({"kind": "search", "state_id": session.state_id,
                                              "query": " ".join(missing)[:512]})
                returned = {e["name"] for e in response.get("entries", [])}
                missing = [n for n in missing if n not in returned]
                if not missing:
                    break
            await session.act({"kind": "explain", "state_id": session.state_id, "answer": example["answer"]})
            report = session.report()
            reports.append(report)
            marks.append({"schema_version": "qcb.explanation_adjudication.v1",
                          "task_hash": digest(case["task"]), "report_digest": digest(report),
                          "rubric_digest": digest(case["capability_rubric"]), "answer_index": 0,
                          "answer_digest": digest(example["answer"]),
                          "reviewer": {"identity": "/root", "kind": "ai",
                                       "method": "Replay of fixed source-aware AI fixture expectations inspected by /root; not a new judge call or a human/blind review."},
                          "respondent_identity": case["capability_rubric"]["reviewer"]["identity"],
                          "criteria": [{"id": key, "score": 1 if value["verdict"] == "met" else 0,
                                        "reasoning": value["reason"]} for key, value in example["canonical_criteria"].items()],
                          "semantic_fidelity": "faithful" if example["assumption_audit"]["contract_preserved"] else "unfaithful",
                          "reasoning": "Authored fixture only. " + " ".join(example["assumption_audit"]["reasons"])})
    return reports, marks


def evaluate(cases, identity, reports, marks):
    by_hash = {digest(c["task"]): c for c in cases}
    annotations = {}
    report_hashes = {digest(r) for r in reports}
    for mark in marks:
        key = mark["report_digest"]
        if key not in report_hashes or key in annotations:
            raise ValueError("unknown/duplicate report adjudication; select one explanation explicitly")
        annotations[key] = mark
    results = []
    for report in reports:
        case = by_hash[report["task_hash"]]
        results.append(assess(case["task"], report, case["capability_rubric"], annotations.get(digest(report))))
    return {"schema_version": "qcb.capability_batch_assessment.v1", **identity, "results": results,
            "distinct_mathematical_cores": len({r["core_id"] for r in results}),
            "new_mathematical_cores": 0, "model_performance_measured": False,
            "joint_capability_score": None, "formal_certificates_issued": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("assess-pilot", "review-templates", "fixture-smoke"))
    parser.add_argument("--input", type=Path)
    parser.add_argument("--adjudications", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise FileExistsError("choose a fresh output; prior evidence is preserved")
        if args.command == "fixture-smoke" and (args.input or args.adjudications):
            raise ValueError("fixture-smoke uses only fixed authored examples")
        if args.command != "fixture-smoke" and not args.input:
            raise ValueError("evaluator-owned --input required")
        if args.command == "review-templates" and (args.adjudications or args.output.resolve().is_relative_to(R)):
            raise ValueError("raw judge packets must stay outside the public repository; this command does not accept grades")
        sources = pipeline_identity()
        cases, identity = load_capability_pilot()
        if args.command == "fixture-smoke":
            reports, marks = asyncio.run(fixture_reports(cases))
        else:
            reports = reports_from_record(_read(args.input))
            marks = _read(args.adjudications) if args.adjudications else []
        result = ({"schema_version": "qcb.adjudication_templates.v1", "templates": templates(cases, reports),
                   "accepted_grades": 0, "model_performance_measured": False}
                  if args.command == "review-templates" else evaluate(cases, identity, reports, marks))
        result["engineered_fixture_smoke"] = args.command == "fixture-smoke"
        result["model_calls"] = 0
        if sources != pipeline_identity():
            raise ValueError("capability pipeline changed during assessment; preserve draft separately")
        result["pipeline_sha256_lf"] = sources
        result["assessment_digest"] = digest(result)
        write_json(args.output, result, immutable=True)
        print(json.dumps({"output": str(args.output), "results": len(result.get("results", [])),
                          "engineered_fixture_smoke": result["engineered_fixture_smoke"], "model_calls": 0}))
        return 0
    except (ValueError, KeyError, OSError, TypeError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
