#!/usr/bin/env python3
"""Inspect pilot tasks, prepare offline operator profiles or run bounded episodes."""
import argparse
import asyncio
import importlib
import json
import re
import subprocess
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_core import write_json
from qcb_evaluation_registry import export_views, load_registry
from qcb_model_loop import fixture_config, run_episode
from qcb_operator_profile import (
    profile_schema,
    profile_template,
    read_operator_profile,
    validation_summary,
)


def _adapter_factory(reference):
    if not re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*:[A-Za-z_]\w*", reference):
        raise ValueError("operator adapter must be a trusted module:factory reference")
    module, name = reference.split(":")

    def construct():
        # No import/discovery until the model loop has passed its execution gate.
        return getattr(importlib.import_module(module), name)()

    return construct


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "list", "export", "plan", "run", "run-fixture",
                                           "schema", "profile-template", "validate-config"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--mode", choices=("root_only", "proof_dag"))
    parser.add_argument("--exposure", choices=("closed_book", "approved_interface"))
    parser.add_argument("--purpose", choices=("formal_proof", "explanation_only"))
    parser.add_argument("--split", choices=("train", "dev", "test_public"))
    parser.add_argument("--view", action="append")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--episode-dir", type=Path)
    parser.add_argument("--adapter")
    parser.add_argument("--authorize-model", action="store_true")
    args = parser.parse_args()
    try:
        if args.output and args.output.exists():
            raise FileExistsError("choose a fresh output; previous evidence is preserved")
        if args.command in {"export", "profile-template"} and not args.output:
            raise ValueError(args.command + " requires --output")
        if args.command in {"schema", "profile-template", "validate-config"}:
            if args.view or args.split or args.episode_dir or args.adapter or args.authorize_model:
                raise ValueError("offline profile commands accept no task, adapter or generation options")
            if args.command != "profile-template" and (args.mode or args.exposure or args.purpose):
                raise ValueError("profile condition flags apply only to profile-template")
            if args.command == "validate-config":
                if not args.config:
                    raise ValueError("validate-config requires --config")
                result = validation_summary(read_operator_profile(args.config))
            else:
                if args.config:
                    raise ValueError("schema/profile-template do not read a run config")
                result = (profile_schema() if args.command == "schema" else
                          profile_template(purpose=args.purpose or "formal_proof", mode=args.mode or "proof_dag",
                                           exposure=args.exposure))
            if args.output:
                write_json(args.output, result, immutable=True)
                print(json.dumps({"output": str(args.output), "model_calls": 0,
                                  "profile_ready_to_run": False if args.command == "profile-template" else None}))
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        episode = args.command in {"plan", "run", "run-fixture"}
        if args.command not in {"export", "run-fixture"} and (args.mode or args.exposure or args.purpose):
            raise ValueError("condition flags apply to export/run-fixture; actual plans/runs use their frozen config")
        if not episode and (args.config or args.episode_dir or args.adapter or args.authorize_model):
            raise ValueError("model options apply only to episode commands")
        if args.authorize_model and args.command != "run":
            raise ValueError("--authorize-model applies only to run")
        if args.command not in {"export", "plan", "run", "run-fixture"} and (args.split or args.view):
            raise ValueError("selection filters apply only to export")
        views, qualification = load_registry()
        if episode:
            if args.output or args.split or not args.episode_dir or not args.view or len(args.view) != 1:
                raise ValueError("episodes require exactly one --view and a fresh private --episode-dir; no --output/--split")
            if args.command == "run-fixture":
                if args.config or args.adapter or args.authorize_model:
                    raise ValueError("run-fixture uses only the builtin synthetic provider")
                if args.purpose == "explanation_only" and args.exposure == "approved_interface":
                    raise ValueError("explanation-only fixtures require closed-book exposure")
                config = fixture_config(purpose=args.purpose or "formal_proof", mode=args.mode or "proof_dag",
                                        exposure=args.exposure or "approved_interface")
            else:
                if not args.config:
                    raise ValueError("plan/run requires an explicit frozen model --config")
                config = read_operator_profile(args.config)
            if args.adapter and config["adapter"]["id"] != args.adapter:
                raise ValueError("adapter import reference differs from the pinned config identity")
            factory = _adapter_factory(args.adapter) if args.adapter else None
            result = asyncio.run(run_episode(views[args.view[0]], config, args.episode_dir,
                                             authorized=args.authorize_model and args.command == "run",
                                             fixture=args.command == "run-fixture", provider_factory=factory))
            print(json.dumps({k: result.get(k) for k in ("status", "failure_class", "reason", "view_id", "provider_calls",
                                                        "provider_constructed", "episode_directory_created", "model_calls_confirmed",
                                                        "model_generation_observed", "model_performance_measured", "formal_proof_success")}))
            return 0 if result["status"] in {"dry_run", "fixture_protocol_complete", "explanation_recorded"} else 2
        if args.command == "export":
            if args.purpose:
                raise ValueError("export chooses proof task mode/exposure only")
            result = export_views(views, qualification, mode=args.mode or "proof_dag", exposure=args.exposure or "approved_interface",
                                  split=args.split, view_ids=args.view)
        elif args.command == "list":
            result = {"qualification": qualification,
                      "views": [{k: v["entry"][k] for k in ("view_id", "core_id", "family", "split", "registration_scope")}
                                for v in views.values()]}
        else:
            result = qualification
        if args.output:
            write_json(args.output, result, immutable=True)
            print(json.dumps({"output": str(args.output), "model_calls": 0}))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
