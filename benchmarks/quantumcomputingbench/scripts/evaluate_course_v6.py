#!/usr/bin/env python3
"""Plan or run one bounded episode from the fixed qualified v6 course."""
import argparse
import asyncio
import json
import subprocess
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from evaluate_agentic import _adapter_factory
from qcb_course_registry_v6 import load_course_registry
from qcb_model_loop import fixture_config, run_episode
from qcb_operator_profile import read_operator_profile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "run", "run-fixture"))
    parser.add_argument("--view", required=True)
    parser.add_argument("--episode-dir", required=True, type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--adapter")
    parser.add_argument("--authorize-model", action="store_true")
    parser.add_argument("--mode", choices=("root_only", "proof_dag"))
    parser.add_argument("--exposure", choices=("closed_book", "approved_interface"))
    parser.add_argument("--purpose", choices=("formal_proof", "explanation_only"))
    args = parser.parse_args()
    try:
        if args.command == "run-fixture":
            if args.config or args.adapter or args.authorize_model:
                raise ValueError("run-fixture uses only the builtin synthetic provider")
            purpose = args.purpose or "formal_proof"
            exposure = args.exposure or ("closed_book" if purpose == "explanation_only" else "approved_interface")
            if purpose == "explanation_only" and exposure != "closed_book":
                raise ValueError("explanation-only fixtures require closed-book exposure")
            config = fixture_config(purpose=purpose, mode=args.mode or "proof_dag", exposure=exposure)
        else:
            if args.mode or args.exposure or args.purpose:
                raise ValueError("plan/run conditions come from the frozen operator config")
            if args.authorize_model and args.command != "run":
                raise ValueError("--authorize-model applies only to run")
            if not args.config:
                raise ValueError("plan/run requires an explicit frozen model --config")
            config = read_operator_profile(args.config)
        if args.adapter and config["adapter"]["id"] != args.adapter:
            raise ValueError("adapter import reference differs from the pinned config identity")
        views, _ = load_course_registry()
        if args.view not in views:
            raise ValueError("unknown qualified v6 view")
        # This closure does not import the provider. run_episode checks task,
        # private destination, authorization and isolation before constructing it.
        factory = _adapter_factory(args.adapter) if args.adapter else None
        result = asyncio.run(run_episode(views[args.view], config, args.episode_dir,
                                         authorized=args.authorize_model and args.command == "run",
                                         fixture=args.command == "run-fixture", provider_factory=factory))
        print(json.dumps({key: result.get(key) for key in (
            "status", "failure_class", "reason", "view_id", "provider_calls", "provider_constructed",
            "episode_directory_created", "model_calls_confirmed", "model_generation_observed",
            "model_performance_measured", "formal_proof_success")}))
        return 0 if result["status"] in {"dry_run", "fixture_protocol_complete", "explanation_recorded"} else 2
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
