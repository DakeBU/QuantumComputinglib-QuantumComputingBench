#!/usr/bin/env python3
"""Prepare and score the fixed sparse-address study using offline records."""
import argparse
import asyncio
import json
import subprocess
import sys
from pathlib import Path

from assessment import _layout, _private, _read, _separate, _write
from assessment_v3 import _preflight_outputs
from lean_qa_training import PROFILE
from qcb_assessment_protocol import (
    freeze_first_answers, grade_assessment, model_messages, prepare_evaluation, review_template,
)
from qcb_core import digest, read_json
from qcb_learning_validity import challenge_task
from qcb_sparse_study import load_private_bank, load_seal, validate_qualification


def _sealed(payload, name):
    return {**payload, name: digest(payload)}


def controller_envelope(controller):
    return _sealed({"schema_version": "qcb.sparse_assessment_controller.v1",
                    "common_controller": controller, "training_profile_digest": digest(read_json(PROFILE)),
                    "actual_model_exposure_authenticated": False}, "controller_digest")


def lock_envelope(lock, envelope):
    return _sealed({"schema_version": "qcb.sparse_assessment_lock.v1",
                    "common_lock": lock, "controller_digest": envelope["controller_digest"]}, "lock_digest")


def formal_tasks(packet, controller, lock):
    probes = {p["probe_id"]: p for p in packet["probes"]}
    assignments = {row["task_id"]: row["probe_id"] for row in controller["assignments"]}
    return [
        {"task_id": row["task_id"], "first_response_hash": row["response_hash"],
         "task": challenge_task(probes[assignments[row["task_id"]]], row["answer"]["decision"],
                                snapshot_id=packet["snapshot_id"], library_revision=packet["library_revision"])}
        for row in lock["responses"] if row["status"] == "answered"
    ]


def _replay(args):
    if not args.trusted_local_reference:
        raise ValueError("explicit trusted authored-reference flag required")
    bank, output, transcript = (_private(p) for p in (args.bank, args.output, args.raw_output))
    if any(p == bank or not p.is_relative_to(bank) for p in (output, transcript)):
        raise ValueError("authored receipts and transcripts belong inside the private bank")
    _preflight_outputs(output, transcript)
    from qcb_sparse_study_reference import replay
    with transcript.open("x", encoding="utf-8") as handle:
        def progress(row):
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()
        receipt = asyncio.run(replay(bank, args.build_root, progress=progress))
    _write(output, receipt)
    return {"passed": True, "private_receipt_digest": digest(receipt), "model_calls": 0}


def run(args):
    if args.command == "check-references":
        return _replay(args)
    if args.command == "audit":
        seal = load_seal()
        qualified = validate_qualification(seal)
        if args.bank:
            load_private_bank(args.bank)
        return {"owner_only_probes": seal["probe_count"], "reference_checks": qualified["checks"],
                "private_bank_validated": args.bank is not None, "model_calls": 0}
    bank, student_path, controller_path = _layout(args.bank, args.student, args.controller)
    if not _separate(bank, controller_path.parent):
        raise ValueError("private bank and grader must occupy disjoint directories")
    packet, _ = load_private_bank(bank)
    if args.command == "prepare":
        student, controller = prepare_evaluation(packet, split="test_public")
        files = [(student_path, student), (controller_path, controller_envelope(controller))]
        for row in student:
            leaf = student_path.parent / row["task_id"]
            files.extend([(leaf / "task.json", row), (leaf / "messages.json", model_messages(row))])
        _preflight_outputs(*(path for path, _ in files), bank=bank)
        for path, value in files:
            _write(path, value)
        return {"prepared_tasks": len(student), "model_calls": 0}

    output = _private(args.output)
    inputs = (student_path, controller_path, getattr(args, "responses", None),
              getattr(args, "locked", None), getattr(args, "reviews", None))
    _preflight_outputs(output, inputs=(p for p in inputs if p is not None), bank=bank)
    if args.command == "formal-challenges":
        if any(not _separate(output.parent, p) for p in (bank, student_path.parent, controller_path.parent)):
            raise ValueError("formal challenges require a separate second-stage student directory")
    elif not output.is_relative_to(controller_path.parent):
        raise ValueError("locks, rubric reviews and scores belong in the private grader directory")

    student, envelope = _read(student_path), _read(controller_path)
    controller = envelope["common_controller"]
    if envelope != controller_envelope(controller):
        raise ValueError("controller is stale or belongs to a different training profile")
    if args.command == "freeze":
        record = lock_envelope(freeze_first_answers(packet, student, controller, _read(args.responses)), envelope)
    else:
        wrapped = _read(args.locked)
        lock = wrapped["common_lock"]
        if wrapped != lock_envelope(lock, envelope):
            raise ValueError("first answers differ from their frozen controller")
        if args.command == "review-template":
            record = review_template(packet, student, controller, lock)
        elif args.command == "score":
            record = grade_assessment(packet, student, controller, lock, _read(args.reviews) if args.reviews else [],
                                      evidence_kind=args.evidence_kind)
            record["study_training_profile_digest"] = envelope["training_profile_digest"]
        else:
            grade_assessment(packet, student, controller, lock)
            record = {"schema_version": "qcb.sparse_formal_challenges.v1",
                      "tasks": formal_tasks(packet, controller, lock),
                      "controller_digest": envelope["controller_digest"], "lock_digest": wrapped["lock_digest"],
                      "root_selection": "locked_student_belief", "candidate_execution": "ENV_BLOCKED"}
    _write(output, record)
    return {"artifact_written": True, "model_calls": 0}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("audit").add_argument("--bank", type=Path)
    a = sub.add_parser("check-references")
    for option in ("bank", "build-root", "output", "raw-output"):
        a.add_argument("--" + option, type=Path, required=True)
    a.add_argument("--trusted-local-reference", action="store_true")
    for command in ("prepare", "freeze", "review-template", "score", "formal-challenges"):
        a = sub.add_parser(command)
        for option in ("bank", "student", "controller"):
            a.add_argument("--" + option, type=Path, required=True)
        if command != "prepare":
            a.add_argument("--output", required=True, type=Path)
            a.add_argument("--responses" if command == "freeze" else "--locked", required=True, type=Path)
        if command == "score":
            a.add_argument("--reviews", type=Path)
            a.add_argument("--evidence-kind", required=True, choices=("synthetic_fixture", "operator_supplied"))
    args = parser.parse_args(argv)
    try:
        print(json.dumps(run(args)))
        return 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError, RuntimeError, subprocess.SubprocessError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
