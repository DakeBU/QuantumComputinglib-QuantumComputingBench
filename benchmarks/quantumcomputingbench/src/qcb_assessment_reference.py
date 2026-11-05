"""Neutral semantic review and frozen authored replay for sealed assessment.

The question/reference bundle stays private. Public commitments bind exact
artifacts; they do not authenticate arbitrary imported execution claims.
"""
from __future__ import annotations

import asyncio
from copy import deepcopy
import hashlib
from pathlib import Path
import subprocess
from time import monotonic

from qcb_assessment_bank import B, R, SEAL, load_private_bank
from qcb_core import digest, read_json
from qcb_integrity import text_sha
from qcb_learning_reference import (REFERENCE_PROFILE, _RecordedAuthoredVerifier,
                                    _compact_evidence, validate_reference_results)
from qcb_learning_validity import challenge_task
from qcb_proof_session import ProofSession, SessionLimits


def decoder_payload(packet):
    return {'schema_version': 'qcb.neutral_assessment_decoder_input.v2',
            'lean_toolchain': packet['lean_toolchain'], 'source_bindings': packet['source_bindings'],
            'formal_items': [{'probe_id': p['probe_id'], 'imports': p['formal_context']['imports'],
                              'proposition': p['formal_context']['proposition']} for p in packet['probes']]}


def source_payload(packet, decoder):
    return {'schema_version': 'qcb.neutral_assessment_source_input.v2',
            'decoder_record_digest': digest(decoder), 'items': [
                {'probe_id': p['probe_id'], 'question': p['question'], 'assumptions': p['assumptions'],
                 'conventions': p['conventions'], 'formal_context': p['formal_context']}
                for p in packet['probes']], 'decoded_formal_mathematics': decoder['items'],
            'source_bindings': packet['source_bindings']}


def answer_payload(packet, comparison):
    return {'schema_version': 'qcb.assessment_answer_review_input.v2',
            'source_comparison_digest': digest(comparison), 'items': [
                {'probe_id': p['probe_id'], 'question': p['question'], 'assumptions': p['assumptions'],
                 'conventions': p['conventions'], 'reference_answer': p['gold']['answer'],
                 'rubric': p['gold']['rubric'], 'formal_coverage': p['formal_coverage']}
                for p in packet['probes']]}


def _rows(record, ids):
    rows = record.get('items')
    if (not isinstance(rows, list) or len(rows) != len(ids)
            or {r.get('probe_id') for r in rows} != ids):
        raise ValueError('every sealed proposition needs exactly one semantic review')
    return rows


def _substantive(row, field):
    value = row.get(field)
    if field == 'semantic_slots' and isinstance(value, dict):
        if (len(value) < 3 or any(not isinstance(k, str) or not k for k in value)
                or any(not ((isinstance(v, str) and v.strip())
                            or (isinstance(v, list) and all(isinstance(x, str) and x.strip() for x in v)))
                       for v in value.values())):
            raise ValueError('explicit nonempty semantic-slot descriptions required')
        value = __import__('json').dumps(value, ensure_ascii=False)
    if not isinstance(value, str) or not 40 <= len(value.strip()) <= 64000:
        raise ValueError('substantive mathematical review required: ' + field)


def check_semantics(packet, directory):
    directory = Path(directory)
    ids = {p['probe_id'] for p in packet['probes']}
    authors = {p['author_identity'] for p in packet['probes']}
    decoder_input = read_json(directory / 'decoder-input.json')
    decoder = read_json(directory / 'decoder.json')
    if decoder_input != decoder_payload(packet) or decoder.get('input_digest') != digest(decoder_input):
        raise ValueError('neutral decoder input changed')
    decoder_id = decoder.get('reviewer_identity')
    if not isinstance(decoder_id, str) or not decoder_id or decoder_id in authors:
        raise ValueError('decoder must be distinct from authors')
    for row in _rows(decoder, ids):
        _substantive(row, 'decoded_mathematics')
        _substantive(row, 'semantic_slots')
    source_input = read_json(directory / 'source-input.json')
    comparison = read_json(directory / 'source-comparison.json')
    if source_input != source_payload(packet, decoder) or comparison.get('input_digest') != digest(source_input):
        raise ValueError('neutral source comparison changed')
    comparer = comparison.get('reviewer_identity')
    if not isinstance(comparer, str) or not comparer or comparer in authors | {decoder_id}:
        raise ValueError('source comparer must be distinct from authors and decoder')
    by_id = {p['probe_id']: p for p in packet['probes']}
    for row in _rows(comparison, ids):
        _substantive(row, 'reasoning')
        _substantive(row, 'premise_audit')
        if (row.get('correspondence') != 'accept'
                or row.get('derived_decision') != by_id[row['probe_id']]['gold']['decision']):
            raise ValueError('independently derived polarity or correspondence disagrees')
    if comparison.get('gold_and_author_answers_seen_before_verdict') is not False:
        raise ValueError('source polarity must be derived before author gold is seen')
    answer_input = read_json(directory / 'answer-input.json')
    review = read_json(directory / 'answer-review.json')
    if (answer_input != answer_payload(packet, comparison)
            or review.get('input_digest') != digest(answer_input)
            or review.get('source_comparison_digest') != digest(comparison)):
        raise ValueError('answer review must retain the earlier independent polarity verdict')
    if review.get('reviewer_identity') != comparer:
        raise ValueError('answer review must follow the same recorded source comparer')
    for row in _rows(review, ids):
        _substantive(row, 'reasoning')
        if row.get('answer_verdict') != 'accept' or row.get('rubric_verdict') != 'accept':
            raise ValueError('unresolved answer/rubric review')
    return {'neutral_proposition_decoder': True, 'independent_polarity_before_gold': True,
            'complete_question_and_answer_review': True, 'decoder_identity': decoder_id,
            'source_comparer_identity': comparer, 'decoder_digest': digest(decoder),
            'source_comparison_digest': digest(comparison), 'answer_review_digest': digest(review),
            'review_is_AI_not_authenticated_human_approval': True}


def pipeline_identity():
    names = ['qcb_assessment_bank.py', 'qcb_assessment_reference.py', 'qcb_learning_reference.py',
             'qcb_learning_validity.py', 'qcb_authored_session.py', 'qcb_proof_session.py',
             'qcb_lean.py', 'qcb_core.py', 'qcb_integrity.py', 'qcb_curriculum.py',
             'qcb_textbook_policy.py', 'qcb_formal_views.py']
    paths = [B / 'src' / n for n in names] + [SEAL, R / 'website/scripts/proof_inputs.py']
    return {p.relative_to(R).as_posix(): text_sha(p) for p in paths}


async def replay_references(directory, build_root, *, progress=None):
    packet, seal = load_private_bank(directory, require_qualified=False)
    semantics = check_semantics(packet, directory)
    planned = 2 * len(packet['probes']) + 2 * len({tuple(p['formal_context']['imports']) for p in packet['probes']})
    if planned > REFERENCE_PROFILE['max_root_replays']:
        raise ValueError('sealed replay exceeds bounded authored profile')
    identity = pipeline_identity()
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R, text=True).strip()
    for path, value in identity.items():
        raw = subprocess.check_output(['git', 'show', commit + ':' + path], cwd=R)
        if hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest() != value:
            raise ValueError('commit the entire reviewed reference pipeline and public seal first')
    started = monotonic()
    rows, raw, negative_imports = [], [], set()
    for probe in packet['probes']:
        remaining = REFERENCE_PROFILE['batch_wall_seconds'] - (monotonic() - started)
        if remaining <= 0:
            raise TimeoutError('bounded authored batch exhausted')
        task = challenge_task(probe, probe['gold']['decision'], snapshot_id=packet['snapshot_id'],
                              library_revision=packet['library_revision'])
        proof = probe['gold']['reference_proof']
        negatives = tuple(task['imports']) not in negative_imports
        verifier = _RecordedAuthoredVerifier(task, {'assessment_root': [proof] +
            (['by exact True.intro', 'by sorry'] if negatives else [])}, build_root)
        session = ProofSession(task, verifier, mode='root_only', limits=SessionLimits(
            wall_seconds=min(REFERENCE_PROFILE['session_wall_seconds'], remaining), check_seconds=120))
        submitted = await session.act({'kind': 'submit', 'state_id': session.state_id,
                                       'node_id': 'assessment_root', 'proof': proof})
        finished = await session.act({'kind': 'finish', 'state_id': session.state_id})
        if progress:
            progress({'probe_id': probe['probe_id'], 'submitted': submitted, 'finished': finished,
                      'session': session.report(), 'replays': verifier.replays})
        row = {'probe_id': probe['probe_id'], 'probe_digest': digest(probe), 'task_hash': digest(task),
               'formal_target_sha256': digest(task['nodes'][0]['target']), 'gold_polarity': probe['gold']['decision'],
               'submitted_status': submitted['status'], 'finish_status': finished['status'],
               'submission_evidence': _compact_evidence(submitted['evidence']) if 'evidence' in submitted else None,
               'final_evidence': _compact_evidence(finished['final_replay']) if 'final_replay' in finished else None,
               'formal_root_checked': session.report()['formal_root_checked'], 'negative_controls': []}
        if not row['formal_root_checked']:
            raise RuntimeError('authored sealed root failed; preserve private progress')
        if negatives:
            negative_imports.add(tuple(task['imports']))
            for label, bad in [('wrong_target', 'by exact True.intro'), ('sorry_axiom', 'by sorry')]:
                remaining = REFERENCE_PROFILE['batch_wall_seconds'] - (monotonic() - started)
                if remaining <= 0:
                    raise TimeoutError('bounded authored batch exhausted')
                s = ProofSession(task, verifier, mode='root_only', limits=SessionLimits(
                    wall_seconds=min(180, remaining), check_seconds=120))
                reply = await s.act({'kind': 'submit', 'state_id': s.state_id,
                                     'node_id': 'assessment_root', 'proof': bad})
                row['negative_controls'].append({'kind': label, 'status': reply['status'],
                    'evidence': _compact_evidence(reply['evidence']) if 'evidence' in reply else None})
                if progress:
                    progress({'probe_id': probe['probe_id'], 'negative': label, 'reply': reply,
                              'replays': verifier.replays})
        row['replays'] = deepcopy(verifier.replays)
        raw.append({'probe_id': probe['probe_id'], 'submitted': submitted, 'finished': finished,
                    'session': session.report(), 'replays': verifier.replays})
        if any(n['status'] != 'compile_error' for n in row['negative_controls']):
            raise RuntimeError('a rejected control is missing; environment failures are not negative gold')
        rows.append(row)
        print(__import__('json').dumps({'completed_authored_probes': len(rows), 'planned': len(packet['probes'])}), flush=True)
    validate_reference_results(packet, rows)
    if pipeline_identity() != identity:
        raise ValueError('reference source changed during batch')
    return {'schema_version': 'qcb.private_assessment_references.v2', 'seal_digest': digest(seal),
            'cohort_digest': digest(packet), 'tested_code_commit': commit,
            'pipeline_source_hashes_lf': identity, 'semantic_review': semantics,
            'profile': deepcopy(REFERENCE_PROFILE), 'passed': True, 'results': rows,
            'elapsed_seconds': monotonic() - started, 'execution_class': 'trusted_local_authored_reference',
            'isolated': False, 'model_calls': 0, 'model_performance_measured': False}, raw
