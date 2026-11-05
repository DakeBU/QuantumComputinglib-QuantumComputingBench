#!/usr/bin/env python3
"""Train-only exports and sealed quantum-semantic evaluation; no model launch."""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
import sys

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / 'src'))
from qcb_assessment_bank import R, load_private_bank, public_status, protocol_identity
from qcb_assessment_protocol import (prepare_evaluation, freeze_first_answers,
                                     review_template, grade_assessment, model_messages)
from qcb_core import digest, read_json


def _read(path):
    p = Path(path)
    if p.stat().st_size > 32_000_000:
        raise ValueError('assessment input exceeds the 32 MB ceiling')
    return read_json(p)


def _private(path):
    path = Path(path).resolve()
    if path.is_relative_to(R):
        raise ValueError('assessment questions, answers and ledgers stay outside the public checkout')
    return path


def _write(path, value, *, private=True):
    path = _private(path) if private else Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def _separate(a, b):
    return not (a == b or a.is_relative_to(b) or b.is_relative_to(a))


def _layout(bank, student, controller):
    bank, student, controller = _private(bank), _private(student), _private(controller)
    if not _separate(student.parent, controller.parent) or not _separate(student.parent, bank):
        raise ValueError('student mount, controller and private bank must occupy disjoint directories')
    return bank, student, controller


def _training():
    from qcb_bench_runtime import build_registry, export_records
    from qcb_course_registry import load_course_registry
    from qcb_course_training import export_training, reference_records
    registry = build_registry()
    nl = export_records(registry, purpose='training')
    views, qualification = load_course_registry()
    lean = export_training(views, qualification, reference_records())
    ids = {c for t in registry['tasks'] if t['split'] == 'train' for c in t['core_ids']}
    if any(x['core_id'] not in ids for x in lean['examples']):
        raise ValueError('Lean supervision must retain existing train identity')
    import subprocess
    from qcb_integrity import text_sha
    return {'schema_version': 'qcb.complementary_training_export.v2',
            'source_commit': __import__('subprocess').check_output(
                ['git', 'rev-parse', 'HEAD'], cwd=R, text=True).strip(),
            'split': 'train', 'nl_and_semantic_examples': nl, 'lean_examples': lean['examples'],
            'source_dirty': bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=R, text=True).strip()),
            'producer_source_sha256_lf': text_sha(Path(__file__)),
            'counts': {'nl_and_semantic_views': len(nl), 'lean_views': len(lean['examples']),
                       'distinct_existing_cores': len(ids)},
            'registry_digest': registry.get('registry_hash', registry.get('registry_digest')),
            'source_exposure': 'public_authored_training_material; pretraining_exposure_unknown',
            'workbook_included': False, 'assessment_bank_included': False,
            'new_mathematical_core_count': 0, 'training_launched': False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    a = sub.add_parser('audit'); a.add_argument('--bank', type=Path)
    a.add_argument('--output', type=Path)
    a = sub.add_parser('export-training'); a.add_argument('--output', required=True, type=Path)
    for cmd in ('prepare', 'freeze', 'review-template', 'score', 'formal-challenges', 'check-references'):
        a = sub.add_parser(cmd); a.add_argument('--bank', required=True, type=Path)
        if cmd == 'prepare':
            a.add_argument('--split', required=True, choices=['dev', 'test_public'])
            a.add_argument('--student', required=True, type=Path)
            a.add_argument('--controller', required=True, type=Path)
        elif cmd == 'check-references':
            a.add_argument('--build-root', required=True, type=Path)
            a.add_argument('--trusted-local-reference', action='store_true')
            a.add_argument('--output', required=True, type=Path)
            a.add_argument('--raw-output', required=True, type=Path)
        else:
            a.add_argument('--student', required=True, type=Path)
            a.add_argument('--controller', required=True, type=Path)
            a.add_argument('--output', required=True, type=Path)
            if cmd == 'freeze':
                a.add_argument('--responses', required=True, type=Path)
            else:
                a.add_argument('--locked', required=True, type=Path)
            if cmd == 'score':
                a.add_argument('--reviews', type=Path)
                a.add_argument('--evidence-kind', required=True, choices=['synthetic_fixture', 'operator_supplied'])
    args = parser.parse_args(argv)
    try:
        if args.command == 'export-training':
            result = _training(); _write(args.output, result, private=False)
            print(json.dumps({'training_counts': result['counts'], 'training_launched': False})); return 0
        if args.command == 'audit':
            result = public_status()
            if args.bank:
                packet, _ = load_private_bank(args.bank)
                result['private_bundle_verified'] = True
                result['private_probe_count'] = len(packet['probes'])
            if args.output:
                _write(args.output, result, private=False)
            print(json.dumps({'qualified': True, 'coverage': {k: v for k, v in result['coverage'].items()
                                                            if k != 'all_modules'},
                              'understanding_established': False})); return 0
        if args.command == 'check-references':
            if not args.trusted_local_reference:
                raise ValueError('authored replay requires the explicit trusted-reference flag')
            bank = _private(args.bank)
            if any(not _private(p).is_relative_to(bank) for p in (args.output, args.raw_output)):
                raise ValueError('authored receipts and raw transcripts stay inside the private bank')
            progress_path = args.raw_output.with_suffix(args.raw_output.suffix + '.progress.jsonl')
            if args.output.exists() or args.raw_output.exists() or progress_path.exists():
                raise FileExistsError('preserve previous evidence; choose fresh output names')
            from qcb_assessment_reference import replay_references
            def progress(row):
                path = args.raw_output.with_suffix(args.raw_output.suffix + '.progress.jsonl')
                _private(path); path.parent.mkdir(parents=True, exist_ok=True)
                with path.open('a', encoding='utf-8') as f:
                    f.write(json.dumps(row, ensure_ascii=False) + '\n')
            result, raw = asyncio.run(replay_references(args.bank, args.build_root, progress=progress))
            _write(args.output, result); _write(args.raw_output, raw)
            print(json.dumps({'passed': result['passed'], 'private_receipt_digest': digest(result)})); return 0
        packet, _ = load_private_bank(args.bank)
        if args.command == 'prepare':
            bank, student_path, controller_path = _layout(args.bank, args.student, args.controller)
            if student_path.exists() or controller_path.exists():
                raise FileExistsError('preserve earlier runs; choose fresh artifact paths')
            student, controller = prepare_evaluation(packet, split=args.split)
            _write(student_path, student); _write(controller_path, controller)
            for row in student:
                _write(student_path.parent / row['task_id'] / 'task.json', row)
                _write(student_path.parent / row['task_id'] / 'messages.json', model_messages(row))
            print(json.dumps({'prepared_tasks': len(student), 'model_calls': 0})); return 0
        bank, student_path, controller_path = _layout(args.bank, args.student, args.controller)
        output = _private(args.output)
        if args.command == 'formal-challenges':
            if any(not _separate(output.parent, p) for p in (bank, student_path.parent, controller_path.parent)):
                raise ValueError('formal challenges need a separate second-stage student mount')
        elif not output.is_relative_to(controller_path.parent):
            raise ValueError('first-answer locks, rubric reviews and scores stay inside the private grader directory')
        student, controller = _read(student_path), _read(controller_path)
        if args.command == 'freeze':
            result = freeze_first_answers(packet, student, controller, _read(args.responses))
        else:
            locked = _read(args.locked)
            if args.command == 'review-template':
                result = review_template(packet, student, controller, locked)
            elif args.command == 'score':
                result = grade_assessment(packet, student, controller, locked,
                    _read(args.reviews) if args.reviews else [], evidence_kind=args.evidence_kind)
                result['protocol_sources_sha256_lf'] = protocol_identity()
            else:
                grade_assessment(packet, student, controller, locked)
                from qcb_learning_validity import challenge_task
                by_id = {p['probe_id']: p for p in packet['probes']}
                assignments = {a['task_id']: a['probe_id'] for a in controller['assignments']}
                tasks = []
                for response in locked['responses']:
                    if response['status'] != 'answered':
                        continue
                    probe = by_id[assignments[response['task_id']]]
                    task = challenge_task(probe, response['answer']['decision'],
                        snapshot_id=packet['snapshot_id'], library_revision=packet['library_revision'])
                    tasks.append({'task_id': response['task_id'], 'first_response_hash': response['response_hash'],
                                  'task': task})
                result = {'schema_version': 'qcb.sealed_formal_challenges.v2', 'tasks': tasks,
                          'root_selection': 'locked_student_belief_not_gold',
                          'candidate_execution': 'ENV_BLOCKED until accepted isolated verifier',
                          'proofs_or_gold_projected': False, 'model_calls': 0}
        _write(args.output, result)
        print(json.dumps({'command': args.command, 'artifact_written': True, 'model_calls': 0})); return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print('ERROR: ' + str(error), file=sys.stderr); return 1


if __name__ == '__main__':
    raise SystemExit(main())
