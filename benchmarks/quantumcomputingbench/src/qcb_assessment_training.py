"""Explicit whole-core training profiles; no dataset split relabeling.

An export boundary describes supplied supervision, not unknown pretraining,
an authenticated training run or the mathematical independence of examples.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re

from qcb_core import digest, read_json

B = Path(__file__).resolve().parents[1]
PROFILES = B / 'tracks/lean/assessment-v3/training-profiles.json'


def training_fingerprint(package):
    """Bind all mathematical/model records without a mutable outer producer ID."""
    if package.get('split') != 'train':
        raise ValueError('train-only baseline required')
    return digest({k: package[k] for k in ('split', 'counts', 'nl_and_semantic_examples', 'lean_examples')})


def core_bindings(registry):
    rows = {}
    for task in registry['tasks']:
        if task['split'] != 'train':
            continue
        if task['task_id'] in rows or not task['core_ids']:
            raise ValueError('unique nonempty training identities required')
        rows[task['task_id']] = {'task_hash': task['task_hash'], 'core_ids': sorted(task['core_ids']),
                                 'track': task['track']}
    return rows


def exclusion_closure(requested, bindings):
    """All views of every core joined by a multi-core training task move together."""
    excluded = set(requested)
    changed = True
    while changed:
        changed = False
        for task in bindings.values():
            ids = set(task['core_ids'])
            if ids & excluded and not ids <= excluded:
                excluded |= ids
                changed = True
    return sorted(excluded)


def apply_profile(package, bindings, profile):
    """Pure checked selection, keeping exact example contents and original splits."""
    required = {'profile_id', 'baseline_training_fingerprint', 'train_task_bindings_digest',
                'excluded_core_ids', 'retained_core_ids', 'counts', 'exposure_scope',
                'review_digest', 'source_group', 'canonical_splits_changed'}
    if not isinstance(profile, dict) or set(profile) != required:
        raise ValueError('unexpected training profile fields')
    if (profile['profile_id'] != 'promise_register_family_holdout'
            or profile['source_group'] != 'promise_register_protocols'
            or profile['exposure_scope'] != 'family_template_withholding_relative_to_this_export; allowed_generic_foundations; public_source_and_pretraining_not_sealed'
            or not isinstance(profile['review_digest'], str)
            or re.fullmatch('[0-9a-f]{64}', profile['review_digest']) is None):
        raise ValueError('reviewed profile scope required; no absolute unseen-source claim')
    if (profile['canonical_splits_changed'] is not False
            or profile['baseline_training_fingerprint'] != training_fingerprint(package)
            or profile['train_task_bindings_digest'] != digest(bindings)):
        raise ValueError('training profile does not match the exact baseline export')
    language, lean = package['nl_and_semantic_examples'], package['lean_examples']
    train_ids = {c for row in bindings.values() for c in row['core_ids']}
    excluded, retained = profile['excluded_core_ids'], profile['retained_core_ids']
    if (not isinstance(excluded, list) or excluded != sorted(set(excluded))
            or not isinstance(retained, list) or retained != sorted(set(retained))
            or not retained or set(excluded) & set(retained) or set(excluded) | set(retained) != train_ids
            or exclusion_closure(excluded, bindings) != excluded):
        raise ValueError('a training profile must omit complete core/view alias groups')
    expected_language = {k for k, t in bindings.items() if t['track'] != 'lean'}
    if package['counts'] != {'nl_and_semantic_views': len(language), 'lean_views': len(lean),
                             'distinct_existing_cores': len(train_ids)}:
        raise ValueError('baseline counts do not describe its supplied records')
    if {r['task_id'] for r in language} != expected_language or len(language) != len(expected_language):
        raise ValueError('baseline language training records are incomplete or duplicated')
    for row in language:
        t = bindings[row['task_id']]
        if row['split'] != 'train' or row['task_hash'] != t['task_hash']:
            raise ValueError('language split or task identity changed')
    if any(r['split'] != 'train' or r['core_id'] not in train_ids for r in lean):
        raise ValueError('Lean supervision imported a nontrain core')
    keep_language = [deepcopy(r) for r in language
                     if not set(bindings[r['task_id']]['core_ids']) & set(excluded)]
    keep_lean = [deepcopy(r) for r in lean if r['core_id'] not in excluded]
    represented = {c for r in keep_language for c in bindings[r['task_id']]['core_ids']}
    represented |= {r['core_id'] for r in keep_lean}
    counts = {'nl_and_semantic_views': len(keep_language), 'lean_views': len(keep_lean),
              'distinct_existing_cores': len(represented)}
    if counts != profile['counts'] or represented != set(retained):
        raise ValueError('profile coverage/counts do not describe actual retained examples')
    result = deepcopy(package)
    result.update(schema_version='qcb.study_training_export.v3', counts=counts,
                  nl_and_semantic_examples=keep_language, lean_examples=keep_lean,
                  study_training_profile=deepcopy(profile), profile_digest=digest(profile),
                  baseline_training_fingerprint=training_fingerprint(package),
                  canonical_splits_changed=False, training_exposure_authenticated=False,
                  pretraining_exposure='unknown', training_launched=False,
                  understanding_established=False)
    return result


def export_profile(profile_id='baseline'):
    # Reuse the original export implementation and leave its API/hash intact.
    import sys
    sys.path.insert(0, str(B / 'scripts'))
    from assessment import _training
    from qcb_bench_runtime import build_registry
    from qcb_integrity import text_sha
    package = _training()
    if profile_id == 'baseline':
        package['study_training_profile'] = {
            'profile_id': 'baseline', 'exposure_scope': 'held_out_target_compositions_with_seen_subproof_and_witness_templates',
            'family_holdout_claim': False}
        package['training_exposure_authenticated'] = False
    elif profile_id == 'promise_register_family_holdout':
        record = read_json(PROFILES)
        if set(record) != {'schema_version', 'profile', 'baseline_counts', 'exclusion_rationale'}:
            raise ValueError('unexpected public training profile registry')
        if (record['schema_version'] != 'qcb.study_training_profiles.v1'
                or record['baseline_counts'] != package['counts']):
            raise ValueError('profile baseline changed')
        package = apply_profile(package, core_bindings(build_registry()), record['profile'])
    else:
        raise ValueError('unknown study training profile')
    package['profile_producer_sources_sha256_lf'] = {
        p.relative_to(B.parents[1]).as_posix(): text_sha(p)
        for p in (Path(__file__), B / 'scripts/assessment.py')}
    return package
