#!/usr/bin/env python3
"""Inspect staged diagnostics, replay fixed references, or plan matched learning."""
import argparse
import asyncio
import json
import random
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_core import digest, read_json, write_json
from qcb_learning_reference import (
    EVIDENCE,
    answer_payload,
    decoder_payload,
    qualify,
    replay_references,
    source_payload,
)
from qcb_learning_validity import (
    DecisionSession,
    R,
    decision_report,
    load_cohort,
    stage_a_input,
)


def fresh(path):
    if path is None:
        raise ValueError("an explicit fresh output path is required")
    if path.exists():
        raise FileExistsError("preserve prior evidence; choose a fresh output")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def fixture_smoke(packet):
    reports = []
    for behavior in ("always_holds", "always_refuted", "gold_oracle_fixture", "abstain", "env_blocked"):
        records = []
        for probe in packet["probes"]:
            session = DecisionSession(probe, snapshot_id=packet["snapshot_id"], library_revision=packet["library_revision"])
            if behavior == "env_blocked":
                records.append({"probe_id": probe["probe_id"], "generation_status": "env_blocked", "answer": None, "answer_digest": None})
                continue
            decision = {"always_holds": "holds", "always_refuted": "refuted", "gold_oracle_fixture": probe["gold"]["decision"], "abstain": "abstain"}[behavior]
            answer = {"decision": decision, "explanation": "Synthetic fixture only; this text is not a mathematical explanation or a model response."}
            session.commit(answer, state_id=session.state_id)
            if decision != "abstain":
                challenged = session.challenge(state_id=session.state_id)
                expected = probe["formal_context"]["proposition"] if decision == "holds" else "¬ (" + probe["formal_context"]["proposition"] + ")"
                if challenged["task"]["nodes"][0]["target"] != expected:
                    raise ValueError("challenge did not follow the sealed belief")
            records.append(session.operator_record())
        reports.append({"behavior": behavior, "report": decision_report(packet, records, evidence_kind="synthetic_fixture")})
    for row in reports:
        if row["behavior"] in {"always_holds", "always_refuted"} and row["report"]["pair_joint_decision_accuracy_on_complete"] != 0:
            raise ValueError("an always-one-label baseline must not pass balanced contrasts")
    return {"schema_version": "qcb.learning_validity_fixture.v1", "cohort_digest": digest(packet), "passed": True,
            "reports": reports, "model_calls": 0, "lean_calls": 0, "model_performance_measured": False,
            "learning_gain": None, "understanding_established": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("audit", "export-stage-a", "prepare-review", "run-fixture", "check-references", "experiment-template", "analyze", "score-decisions"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--review-stage", choices=("decoder", "source", "answers"))
    parser.add_argument("--build-root", type=Path)
    parser.add_argument("--trusted-local-reference", action="store_true")
    parser.add_argument("--raw-output", type=Path)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--scope", choices=("public_retest", "fresh_instance_transfer", "family_transfer", "composition_transfer"), default="public_retest")
    parser.add_argument("--registration", type=Path)
    parser.add_argument("--records", type=Path)
    parser.add_argument("--evidence-kind", choices=("synthetic_fixture", "unattested_import", "operator_model_observation"), default="unattested_import")
    args = parser.parse_args()
    try:
        if args.draft and args.command not in {"audit", "prepare-review"}:
            raise ValueError("unqualified drafts cannot be exported as evaluation inputs")
        if args.command != "check-references" and (args.build_root or args.trusted_local_reference or args.raw_output):
            raise ValueError("runtime options apply only to fixed authored reference checking")
        if args.command != "prepare-review" and args.review_stage:
            raise ValueError("review-stage applies only to prepare-review")
        packet, summary = load_cohort()
        if args.command == "prepare-review":
            if not args.review_stage:
                raise ValueError("choose the next independently reviewed stage")
            if args.review_stage == "decoder":
                result = decoder_payload(packet)
            elif args.review_stage == "source":
                result = source_payload(packet, read_json(EVIDENCE / "decoder.json"))
            else:
                result = answer_payload(packet, read_json(EVIDENCE / "decoder.json"), read_json(EVIDENCE / "source-comparison.json"))
        elif args.command == "check-references":
            if not args.trusted_local_reference or not args.build_root or not args.raw_output or not args.output:
                raise ValueError("fixed replay requires explicit authored-reference flag, pinned build root, summary and separate raw output")
            fresh(args.output)
            raw_path = fresh(args.raw_output).resolve()
            if raw_path.is_relative_to(R.resolve()) or raw_path == args.output.resolve():
                raise ValueError("raw reference transcripts must remain separate and outside the repository")
            # Append-only per-probe progress survives a later failed/expired check.
            def progress(row):
                with raw_path.open("a", encoding="utf-8", newline="\n") as stream:
                    stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            result, _ = asyncio.run(replay_references(packet, args.build_root, progress=progress))
        elif args.command == "audit" and args.draft:
            result = {**summary, "status": "DRAFT_NOT_EVALUATION_GOLD", "qualification": "not checked by this command"}
        else:
            qualification = qualify(packet)
            if args.command == "audit":
                result = {**summary, "qualification": qualification}
            elif args.command == "export-stage-a":
                inputs = [stage_a_input(p) for p in packet["probes"]]
                random.Random(args.seed).shuffle(inputs)
                result = {"schema_version": "qcb.semantic_decision_export.v1", "agent_inputs": inputs}
            elif args.command == "run-fixture":
                result = fixture_smoke(packet)
            elif args.command == "score-decisions":
                if not args.records:
                    raise ValueError("a separate operator record list is required")
                result = decision_report(packet, read_json(args.records), evidence_kind=args.evidence_kind)
            else:
                from qcb_learning_design import analyze_experiment, experiment_template
                if args.command == "experiment-template":
                    result = experiment_template(packet, scope=args.scope)
                else:
                    if not args.registration or not args.records:
                        raise ValueError("analysis requires a frozen registration and observed measurement list")
                    # No external trust callback is accepted through CLI data.
                    result = analyze_experiment(read_json(args.registration), packet, read_json(args.records))
        if args.output:
            if args.command != "check-references":
                fresh(args.output)
            write_json(args.output, result, immutable=True)
            print(json.dumps({"output": str(args.output), "status": result.get("status"), "passed": result.get("passed"), "model_performance_measured": False}))
        else:
            print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError, RuntimeError, TimeoutError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
