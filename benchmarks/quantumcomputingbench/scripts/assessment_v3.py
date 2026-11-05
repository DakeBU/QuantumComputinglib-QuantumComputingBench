#!/usr/bin/env python3
"""V3 study-local extension: private preparation/scoring and fixed authored replay.

No model launch or student proof execution. Author gold is accessed only by the
private bank and explicit fixed-reference workflow, never by the student export.
"""
from __future__ import annotations

import argparse
import asyncio
from copy import deepcopy
import json
from pathlib import Path
import re
import subprocess
import sys

B = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(B / 'src'), str(B / 'scripts')]
from assessment import _layout, _write, _read, _training, _private, _separate
from qcb_assessment_v3 import load_private_bank, public_status, protocol_identity
from qcb_assessment_protocol import (prepare_evaluation, freeze_first_answers, review_template,
                                     grade_assessment, model_messages)
from qcb_core import digest
from qcb_learning_validity import challenge_task

PROFILES = ('baseline', 'promise_register_family_holdout')


def _export_profile(name):
    """Root-owned policy integration; no invented filtered-export counts."""
    if name not in PROFILES:
        raise ValueError('unknown training profile')
    try:
        from qcb_assessment_training import export_profile
    except ModuleNotFoundError as error:
        if error.name != 'qcb_assessment_training' or name != 'baseline':
            raise ValueError('requested training profile is not available') from error
        return {**_training(), 'training_profile': 'baseline',
                'actual_model_exposure_authenticated': False}
    return export_profile(name)


def _sealed(value, field):
    return {**value, field: digest(value)}


def _study_design(name):
    if name not in PROFILES:
        raise ValueError('unknown training profile')
    from qcb_assessment_training import PROFILES as profile_manifest
    manifest = _read(profile_manifest)
    profile = manifest.get('profile')
    if (manifest.get('schema_version') != 'qcb.study_training_profiles.v1'
            or not isinstance(profile, dict) or profile.get('profile_id') != PROFILES[1]):
        raise ValueError('invalid public training profile manifest')
    fingerprint = profile.get('baseline_training_fingerprint')
    if not isinstance(fingerprint, str) or re.fullmatch('[0-9a-f]{64}', fingerprint) is None:
        raise ValueError('invalid baseline training fingerprint')
    definition = ({'profile_id': name, 'baseline_training_fingerprint': fingerprint}
                  if name == 'baseline' else profile)
    return {'training_profile': name, 'profile_definition_digest': digest(definition),
            'declared_only': True,
            'actual_model_exposure_authenticated': False}


def _controller_envelope(common_controller, profile):
    return _sealed({'schema_version': 'qcb.assessment_controller.v3',
                    'common_controller': deepcopy(common_controller),
                    'study_design': _study_design(profile)}, 'controller_digest')


def _unwrap_controller(envelope):
    if (not isinstance(envelope, dict) or set(envelope) != {
            'schema_version', 'common_controller', 'study_design', 'controller_digest'}
            or envelope['schema_version'] != 'qcb.assessment_controller.v3'
            or not isinstance(envelope['common_controller'], dict)
            or envelope['controller_digest'] != digest({k: v for k, v in envelope.items() if k != 'controller_digest'})):
        raise ValueError('stale or malformed v3 controller envelope')
    design = envelope['study_design']
    if (not isinstance(design, dict) or not isinstance(design.get('training_profile'), str)
            or design.get('declared_only') is not True
            or design.get('actual_model_exposure_authenticated') is not False
            or design != _study_design(design['training_profile'])):
        raise ValueError('invalid declared study design')
    return envelope['common_controller'], design['training_profile']


def _first_answer_envelope(common_lock, controller_envelope):
    common_controller, _ = _unwrap_controller(controller_envelope)
    if common_lock['controller_digest'] != common_controller['controller_digest']:
        raise ValueError('common first-answer lock differs from its controller')
    return _sealed({'schema_version': 'qcb.assessment_first_answers.v3',
                    'controller_digest': controller_envelope['controller_digest'],
                    'common_lock': deepcopy(common_lock)}, 'lock_digest')


def _unwrap_first_answers(envelope, controller_envelope):
    common_controller, _ = _unwrap_controller(controller_envelope)
    if (not isinstance(envelope, dict) or set(envelope) != {
            'schema_version', 'controller_digest', 'common_lock', 'lock_digest'}
            or envelope['schema_version'] != 'qcb.assessment_first_answers.v3'
            or envelope['lock_digest'] != digest({k: v for k, v in envelope.items() if k != 'lock_digest'})
            or envelope['controller_digest'] != controller_envelope['controller_digest']
            or not isinstance(envelope['common_lock'], dict)
            or envelope['common_lock'].get('controller_digest') != common_controller['controller_digest']):
        raise ValueError('v3 first-answer lock differs from its frozen controller/study design')
    return envelope['common_lock']


def _preflight_outputs(*paths, inputs=(), bank=None):
    """Check the whole output layout without creating directories or files."""
    targets = tuple(path.resolve() for path in paths)
    input_paths = tuple(path.resolve() for path in inputs)
    for index, (path, target) in enumerate(zip(paths, targets)):
        if path.is_symlink() or target.exists():
            raise FileExistsError('preserve previous evidence; choose fresh output names')
        if any(not _separate(target, other) for other in targets[:index]):
            raise ValueError('output paths must be distinct and non-nested')
        if any(not _separate(target, other) for other in input_paths):
            raise ValueError('output paths cannot overlap input files')
        if bank is not None and bank.is_relative_to(target):
            raise ValueError('output paths cannot replace the private bank directory or its ancestors')
        ancestor = next((parent for parent in target.parents if parent.exists()), None)
        if ancestor is None or not ancestor.is_dir():
            raise NotADirectoryError('output ancestors must be directories')
    return targets


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    a = sub.add_parser('audit'); a.add_argument('--bank', type=Path); a.add_argument('--output', type=Path)
    a = sub.add_parser('export-training'); a.add_argument('--output', required=True, type=Path)
    a.add_argument('--training-profile', choices=PROFILES, default='baseline')
    for command in ('prepare', 'freeze', 'review-template', 'score', 'formal-challenges', 'check-references'):
        a = sub.add_parser(command); a.add_argument('--bank', required=True, type=Path)
        if command == 'check-references':
            a.add_argument('--build-root', required=True, type=Path)
            a.add_argument('--trusted-local-reference', action='store_true')
            a.add_argument('--output', required=True, type=Path); a.add_argument('--raw-output', required=True, type=Path)
            continue
        a.add_argument('--student', required=True, type=Path); a.add_argument('--controller', required=True, type=Path)
        if command == 'prepare':
            a.add_argument('--split', required=True, choices=('dev', 'test_public'))
            a.add_argument('--training-profile', choices=PROFILES, default='baseline')
        else:
            a.add_argument('--output', required=True, type=Path)
            a.add_argument('--responses' if command == 'freeze' else '--locked', required=True, type=Path)
            if command == 'score':
                a.add_argument('--reviews', type=Path)
                a.add_argument('--training-profile', choices=PROFILES)
                a.add_argument('--evidence-kind', required=True, choices=('synthetic_fixture', 'operator_supplied'))
    args = parser.parse_args(argv)
    try:
        if args.command == 'export-training':
            output, = _preflight_outputs(args.output)
            record = _export_profile(args.training_profile)
            _write(output, record, private=False)
            print(json.dumps({'training_counts': record['counts'], 'training_profile': args.training_profile,
                              'training_launched': False})); return 0
        if args.command == 'audit':
            bank = _private(args.bank) if args.bank else None
            output = _preflight_outputs(args.output, bank=bank)[0] if args.output else None
            record = public_status()
            if bank is not None:
                packet, _ = load_private_bank(bank)
                record['private_bundle_verified'] = True; record['private_probe_count'] = len(packet['probes'])
            if output is not None:
                _write(output, record, private=False)
            print(json.dumps({'qualified': True, 'understanding_established': False})); return 0
        if args.command == 'check-references':
            if not args.trusted_local_reference:
                raise ValueError('authored replay requires the explicit trusted-reference flag')
            bank = _private(args.bank)
            raw_output = _private(args.raw_output)
            progress_output = raw_output.with_suffix(raw_output.suffix + '.progress.jsonl')
            targets = (_private(args.output), raw_output, _private(progress_output))
            if any(not p.is_relative_to(bank) for p in targets):
                raise ValueError('authored receipts and raw transcripts stay inside the private bank')
            output, raw_output, progress_path = _preflight_outputs(args.output, args.raw_output, progress_output, bank=bank)
            from qcb_assessment_v3_reference import replay_references
            def progress(row):
                progress_path.parent.mkdir(parents=True, exist_ok=True)
                with progress_path.open('a', encoding='utf-8') as handle:
                    handle.write(json.dumps(row, ensure_ascii=False) + '\n')
            result, raw = asyncio.run(replay_references(bank, args.build_root, progress=progress))
            _write(output, result); _write(raw_output, raw)
            print(json.dumps({'passed': result['passed'], 'private_receipt_digest': digest(result)})); return 0
        # This is deliberately the normal qualified v3 path, with no global
        # substitution of v2 loaders or monkeypatching of common protocol code.
        bank, student_path, controller_path = _layout(args.bank, args.student, args.controller)
        if args.command == 'prepare':
            _preflight_outputs(args.student, args.controller, bank=bank)
            packet, _ = load_private_bank(bank)
            student, controller = prepare_evaluation(packet, split=args.split)
            controller_envelope = _controller_envelope(controller, args.training_profile)
            artifacts = [(student_path, student), (controller_path, controller_envelope)]
            for row in student:
                messages = model_messages(row)
                leaf = student_path.parent / row['task_id']
                if leaf.exists() or leaf.is_symlink():
                    raise FileExistsError('student task leaf already exists; choose a fresh student mount')
                artifacts.extend([(leaf / 'task.json', row), (leaf / 'messages.json', messages)])
            _preflight_outputs(*(path for path, _ in artifacts))
            for path, value in artifacts:
                _write(path, value)
            print(json.dumps({'prepared_tasks': len(student), 'model_calls': 0})); return 0
        output = _private(args.output)
        if args.command == 'formal-challenges':
            if any(not _separate(output.parent, p) for p in (bank, student_path.parent, controller_path.parent)):
                raise ValueError('formal challenges need a separate second-stage student mount')
        elif not output.is_relative_to(controller_path.parent):
            raise ValueError('first-answer locks, rubric reviews and scores stay inside the private grader directory')
        inputs = (student_path, controller_path, getattr(args, 'responses', None),
                  getattr(args, 'locked', None), getattr(args, 'reviews', None))
        _preflight_outputs(args.output, inputs=(path for path in inputs if path is not None), bank=bank)
        packet, _ = load_private_bank(bank)
        student, controller_envelope = _read(student_path), _read(controller_path)
        controller, declared = _unwrap_controller(controller_envelope)
        if args.command == 'freeze':
            common_lock = freeze_first_answers(packet, student, controller, _read(args.responses))
            record = _first_answer_envelope(common_lock, controller_envelope)
        else:
            locked_envelope = _read(args.locked)
            locked = _unwrap_first_answers(locked_envelope, controller_envelope)
            if args.command == 'review-template':
                record = review_template(packet, student, controller, locked)
            elif args.command == 'score':
                if args.training_profile is not None and args.training_profile != declared:
                    raise ValueError('declared training profile differs from its prepared controller')
                record = grade_assessment(packet, student, controller, locked,
                    _read(args.reviews) if args.reviews else [], evidence_kind=args.evidence_kind)
                record.update(schema_version='qcb.assessment_score.v3',
                              protocol_sources_sha256_lf=protocol_identity(),
                              v3_controller_digest=controller_envelope['controller_digest'],
                              v3_lock_digest=locked_envelope['lock_digest'],
                              study_design=deepcopy(controller_envelope['study_design']),
                              declared_training_profile=declared, actual_model_exposure_authenticated=False)
            else:
                grade_assessment(packet, student, controller, locked)
                probes = {p['probe_id']: p for p in packet['probes']}
                assignments = {a['task_id']: a['probe_id'] for a in controller['assignments']}
                tasks = []
                for response in locked['responses']:
                    if response['status'] == 'answered':
                        probe = probes[assignments[response['task_id']]]
                        task = challenge_task(probe, response['answer']['decision'],
                            snapshot_id=packet['snapshot_id'], library_revision=packet['library_revision'])
                        tasks.append({'task_id': response['task_id'], 'first_response_hash': response['response_hash'], 'task': task})
                record = {'schema_version': 'qcb.sealed_formal_challenges.v3', 'tasks': tasks,
                          'v3_controller_digest': controller_envelope['controller_digest'],
                          'v3_lock_digest': locked_envelope['lock_digest'],
                          'root_selection': 'locked_student_belief_not_gold',
                          'candidate_execution': 'ENV_BLOCKED until accepted isolated verifier',
                          'proofs_or_gold_projected': False, 'model_calls': 0}
        _write(output, record)
        print(json.dumps({'command': args.command, 'artifact_written': True, 'model_calls': 0})); return 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError, subprocess.SubprocessError) as error:
        print('ERROR: ' + str(error), file=sys.stderr); return 1


if __name__ == '__main__':
    raise SystemExit(main())
