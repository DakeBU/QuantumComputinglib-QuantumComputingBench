#!/usr/bin/env python3
"""QuantumComputingBench task, dataset, offline-run and review entry point."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from qcb_bench_runtime import (
    _manifest_tasks,
    _write,
    build_registry,
    bundle,
    doctor,
    export_records,
    prepare_run,
    public_index,
    read_jsonl,
    review_template,
    score,
    select_tasks,
    smoke,
    write_downloads,
    write_jsonl,
)
from qcb_core import read_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "list", "show", "export", "prepare-run", "score", "review-template", "smoke", "doctor", "bundle", "downloads"))
    parser.add_argument("--split", choices=("train", "dev", "test_public"))
    parser.add_argument("--track", choices=("nonlean", "semantic", "lean"))
    parser.add_argument("--task", action="append")
    parser.add_argument("--purpose", choices=("evaluation", "training", "reference"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--responses", type=Path)
    parser.add_argument("--reviews", type=Path)
    parser.add_argument("--exposure", choices=("closed_book", "open_library"))
    args = parser.parse_args()
    try:
        for field, commands in {
            "purpose": {"show", "export"}, "exposure": {"prepare-run"},
            "split": {"list", "show", "export", "prepare-run", "bundle"},
            "track": {"list", "show", "export", "prepare-run", "bundle"},
            "task": {"list", "show", "export", "prepare-run", "bundle"},
            "manifest": {"score", "review-template"}, "responses": {"score", "review-template"},
            "reviews": {"score"},
        }.items():
            if getattr(args, field) is not None and args.command not in commands:
                raise ValueError("--" + field + " does not apply to " + args.command)
        if args.command == "doctor":
            result = doctor()
        else:
            registry = build_registry()
            if args.command == "validate":
                result = {"passed": True, "registry_hash": registry["registry_hash"], **registry["summary"]}
            elif args.command in {"list", "show"}:
                index = public_index(registry)
                selected = select_tasks(registry, split=args.split, track=args.track, task_ids=args.task)
                if args.command == "show" and len(selected) != 1:
                    raise ValueError("show requires exactly one selected --task")
                index["tasks"] = [t for t in index["tasks"] if t["task_id"] in {v["task_id"] for v in selected}]
                result = index if args.command == "list" else export_records(registry, purpose=args.purpose or "evaluation", task_ids=[t["task_id"] for t in selected])
            elif args.command in {"export", "prepare-run", "bundle", "smoke", "downloads"}:
                if args.output is None:
                    raise ValueError("this command requires a fresh --output path")
                if args.command == "export":
                    records = export_records(registry, purpose=args.purpose or "evaluation", split=args.split, track=args.track, task_ids=args.task)
                    write_jsonl(args.output, records)
                    result = {"records": len(records), "purpose": args.purpose}
                elif args.command in {"prepare-run", "bundle"}:
                    fn = prepare_run if args.command == "prepare-run" else bundle
                    kw = {"split": args.split or "test_public", "track": args.track or "semantic", "task_ids": args.task}
                    if args.command == "prepare-run":
                        kw["exposure"] = args.exposure or "closed_book"
                    result = fn(registry, args.output, **kw)
                else:
                    result = smoke(registry, args.output) if args.command == "smoke" else write_downloads(args.output, registry)
            else:
                if not args.manifest or not args.responses:
                    raise ValueError("scoring/review preparation requires --manifest and --responses")
                manifest, responses = read_json(args.manifest), read_jsonl(args.responses)
                if args.command == "review-template":
                    score(registry, manifest, responses)
                    tasks = _manifest_tasks(registry, manifest)
                    answered = {r["task_id"] for r in responses if r["status"] == "answered"}
                    rows = review_template([t for t in tasks if t["task_id"] in answered], responses)
                    if not args.output:
                        raise ValueError("review-template requires a fresh --output")
                    write_jsonl(args.output, rows)
                    result = {"review_records": len(rows), "ready_to_score": False}
                else:
                    result = score(registry, manifest, responses, read_jsonl(args.reviews) if args.reviews else [])
                    if args.output:
                        _write(args.output, result)
        if args.command in {"doctor", "validate", "list", "show"} and args.output:
            _write(args.output, result)
        if args.command == "smoke":
            result = {k: result[k] for k in ("passed", "synthetic_fixture", "model_calls", "lean_calls", "container_calls")}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError, RuntimeError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
