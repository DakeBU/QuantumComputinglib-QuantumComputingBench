"""Versioned, sealed study cores extending the unchanged v2 assessment.

New study contracts do not grant canonical public-catalog admission. Exact
provenance commits to the reviewed data; hashes do not authenticate reviewers.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import hashlib
import math
import re
import subprocess
from uuid import UUID

import qcb_assessment_bank as base
from qcb_assessment_protocol import _index
from qcb_core import digest, read_json
from qcb_integrity import text_sha
from qcb_learning_validity import challenge_task, validate_probe

B, R = base.B, base.R
SEAL = B / 'tracks/lean/assessment-v3/seal.json'
QUALIFICATION = B / 'reports/assessment-v3/qualification.json'
SOFTWARE = B / 'reports/assessment-v3/software-checks.json'
PRIVATE_FILES = {'cohort.json', 'provenance.json'}
CORE_FIELDS = {'core_id', 'probe_id', 'contract_hash', 'mechanism_id',
               'exposure_group', 'canonical_alias', 'canonical_admission', 'source_nodes'}
PROVENANCE_NAMES = {'candidates-001.json', 'authored-references-001.json', 'neutral-input-001.json',
    'neutral-decode-001.json', 'neutral-mapping-001.json', 'source-input-001.json',
    'source-comparison-001.json', 'answer-review-input-001.json', 'answer-review-001.json',
    'curated-answers-001.json', 'normalization-seal-001.json', 'normalized-probes-001.json',
    'normalized-authored-references-001.json', 'exposure-independent-001.json',
    'statement-seal-001.json', 'reference-replay-001.json'}


def _shape(record, fields, label):
    if not isinstance(record, dict) or set(record) != set(fields):
        raise ValueError('unexpected fields: ' + label)


def _hash(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def _uuid4(value):
    try:
        return isinstance(value, str) and str(UUID(value)) == value and UUID(value).version == 4
    except (ValueError, TypeError, AttributeError):
        return False


def _pair_uuid(value):
    try:
        return isinstance(value, str) and str(UUID(value)) == value and UUID(value).version in (4, 5)
    except (ValueError, TypeError, AttributeError):
        return False


def study_contract(probe, source_bindings):
    """One immutable question contract shared by its NL and Lean stages."""
    return {'question': probe['question'], 'assumptions': probe['assumptions'],
            'conventions': probe['conventions'], 'formal_context': probe['formal_context'],
            'source_bindings': source_bindings}


def validate_seal(record, *, base_seal=None):
    fields = {'schema_version', 'release_id', 'base_v2_seal_digest', 'base_cohort_digest',
              'cohort_digest', 'private_files_sha256_lf', 'provenance_files_sha256_lf',
              'probe_index', 'study_core_index', 'source_bindings', 'proof_inputs_sha256',
              'catalog_hash', 'snapshot_id', 'library_revision', 'lean_toolchain',
              'exposure_audit_digest', 'exposure_scope', 'canonical_admissions_changed',
              'model_performance_measured'}
    _shape(record, fields, 'v3 seal')
    if (not isinstance(record['release_id'], str)
            or re.fullmatch(r'qcb-sealed-assessment-v3-[0-9]{8}', record['release_id']) is None):
        raise ValueError('bounded neutral release identifier required')
    old = base.load_seal() if base_seal is None else base_seal
    if (record['schema_version'] != 'qcb.sealed_assessment_extension.v3'
            or record['base_v2_seal_digest'] != digest(old)
            or record['base_cohort_digest'] != old['cohort_digest']
            or record['canonical_admissions_changed'] is not False
            or record['model_performance_measured'] is not False
            or record['exposure_scope'] != 'held_out_target_compositions_relative_to_frozen_train_export; shared_subproofs_and_witness_templates; public_library_exposed; pretraining_unknown'):
        raise ValueError('v3 must extend the exact frozen v2 without promoting model claims')
    for key in ('proof_inputs_sha256', 'catalog_hash', 'snapshot_id', 'library_revision', 'lean_toolchain'):
        if record[key] != old[key]:
            raise ValueError('extension changed its inherited source epoch')
    if not _hash(record['cohort_digest']) or not _hash(record['exposure_audit_digest']):
        raise ValueError('unbound extension or exposure audit')
    if set(record['private_files_sha256_lf']) != PRIVATE_FILES:
        raise ValueError('exact extension-private files required')
    if set(record['provenance_files_sha256_lf']) != {'provenance/' + n for n in PROVENANCE_NAMES}:
        raise ValueError('only neutral fixed provenance filenames may be public')
    for files in (record['private_files_sha256_lf'], record['provenance_files_sha256_lf']):
        if not isinstance(files, dict) or not files:
            raise ValueError('nonempty content-bound provenance required')
        for name, value in files.items():
            p = Path(name)
            if p.is_absolute() or '..' in p.parts or not _hash(value):
                raise ValueError('unsafe or unbound private provenance')
    rows = record['probe_index']
    if (not isinstance(rows, list) or len(rows) != 4
            or any(not isinstance(p, dict) or set(p) != base.META_FIELDS
                   or not _uuid4(p['probe_id']) or not _pair_uuid(p['pair_id']) for p in rows)
            or len({p['probe_id'] for p in rows}) != 4):
        raise ValueError('four exact, metadata-only extension propositions required')
    cores = record['study_core_index']
    if (not isinstance(cores, list) or len(cores) != 4
            or any(not isinstance(c, dict) or set(c) != CORE_FIELDS for c in cores)
            or {c['probe_id'] for c in cores} != {p['probe_id'] for p in rows}):
        raise ValueError('one new study core per question, not per response modality')
    known_base = {p['probe_id'] for p in old['probe_index']}
    if known_base & {p['probe_id'] for p in rows}:
        raise ValueError('new assessment identities overlap the frozen bank')
    by_id = {c['probe_id']: c for c in cores}
    pairs = {}
    for p in rows:
        c = by_id[p['probe_id']]
        if (c['core_id'] != 'candidate:' + p['probe_id'] or not _hash(c['contract_hash'])
                or c['canonical_alias'] is not None or c['canonical_admission'] is not False
                or p['parent_core_ids'] != [c['core_id']]
                or p['parent_contracts'] != {c['core_id']: c['contract_hash']}
                or c['source_nodes'] != p['source_nodes']
                or p['split'] != 'test_public' or p['cluster_id'] != 'promise_register_protocols'
                or p['difficulty_band'] not in {'D2', 'D3'}
                or c['exposure_group'] != 'promise_register_protocols'
                or c['mechanism_id'] not in {'dirty_flag_involution', 'target_only_control_hoisting'}):
            raise ValueError('study cores cannot borrow or relabel canonical train parents')
        pairs.setdefault(p['pair_id'], []).append(c)
    if (len(pairs) != 2 or {c['mechanism_id'] for c in cores} != {
            'dirty_flag_involution', 'target_only_control_hoisting'}
            or any(len(group) != 2 or len({c['mechanism_id'] for c in group}) != 1
                               for group in pairs.values())):
        raise ValueError('two complete contrasts share one exposure/split group')
    from qcb_curriculum import load_catalog
    _, _, graph = load_catalog()
    source_paths = {s['path'] for s in record['source_bindings']}
    if not source_paths or len(source_paths) != len(record['source_bindings']):
        raise ValueError('unique nonempty bound source files required')
    for p in rows:
        if not p['source_nodes']:
            raise ValueError('compiled source evidence required')
        for node in p['source_nodes']:
            if (node not in graph or graph[node].get('inventory_status') != 'Compiled'
                    or graph[node].get('open_obligation') is not False
                    or graph[node].get('source') not in source_paths):
                raise ValueError('study anchors must be compiled closed declarations')
    for binding in record['source_bindings']:
        _shape(binding, {'path', 'sha256_lf'}, 'source binding')
        p = (R / binding['path']).resolve()
        if (not p.is_relative_to(R) or not binding['path'].startswith('QuantumBlockEncoding/')
                or not _hash(binding['sha256_lf']) or text_sha(p) != binding['sha256_lf']):
            raise ValueError('extension source binding changed')
    return record


def load_seal():
    return validate_seal(read_json(SEAL))


def _bound_files(directory, files):
    for name, value in files.items():
        p = (directory / name).resolve()
        if not p.is_relative_to(directory) or text_sha(p) != value:
            raise ValueError('extension private evidence changed: ' + name)


def load_private_bank(directory, *, require_qualified=True):
    directory = Path(directory).resolve()
    if directory.is_relative_to(R):
        raise ValueError('private questions and gold must stay outside the public checkout')
    seal = load_seal()
    _bound_files(directory, seal['private_files_sha256_lf'])
    _bound_files(directory, seal['provenance_files_sha256_lf'])
    packet = read_json(directory / 'cohort.json')
    expected = {'schema_version', 'cohort_id', 'base_commit', 'library_revision',
                'proof_inputs_sha256', 'lean_toolchain', 'catalog_hash', 'snapshot_id',
                'source_bindings', 'probes', 'study_cores', 'base_v2_seal_digest',
                'admission', 'new_canonical_formal_admissions', 'model_performance_measured', 'blind_test'}
    _shape(packet, expected, 'v3 cohort')
    if (packet['schema_version'] != 'qcb.assessment_cohort.v3' or digest(packet) != seal['cohort_digest']
            or packet['admission'] != 'sealed_study_not_public_catalog_admission'
            or type(packet['new_canonical_formal_admissions']) is not int
            or packet['new_canonical_formal_admissions'] != 0 or not _uuid4(packet['cohort_id'])
            or packet['model_performance_measured'] is not False or packet['blind_test'] is not False):
        raise ValueError('unexpected extension cohort or promoted claim')
    old, old_seal = base.load_private_bank(directory / 'base-v2')
    if packet['base_v2_seal_digest'] != digest(old_seal):
        raise ValueError('base bank lineage changed')
    for key in ('library_revision', 'proof_inputs_sha256', 'lean_toolchain', 'catalog_hash', 'snapshot_id'):
        if packet[key] != old[key]:
            raise ValueError('cohort epoch drift')
    source_map = {s['path']: s for s in old['source_bindings']}
    for s in seal['source_bindings']:
        if s['path'] in source_map and source_map[s['path']] != s:
            raise ValueError('source bindings conflict with frozen base')
        source_map[s['path']] = s
    if packet['source_bindings'] != [source_map[k] for k in sorted(source_map)]:
        raise ValueError('cohort source union differs from inherited and new sources')
    # Assembly origin is distinct from author/reviewer identity and from the
    # actual pinned runtime. It must nevertheless name a real unchanged tree.
    _committed({s['path']: s['sha256_lf'] for s in packet['source_bindings']}, packet['base_commit'])
    ids = _index(packet)
    old_by = {p['probe_id']: p for p in old['probes']}
    if len(ids) != len(old_by) + 4 or any(ids.get(k) != v for k, v in old_by.items()):
        raise ValueError('frozen v2 propositions were changed, removed or duplicated')
    extension = [p for p in packet['probes'] if p['probe_id'] not in old_by]
    if [base.probe_metadata(p) for p in extension] != seal['probe_index']:
        raise ValueError('private extension differs from its public commitment')
    if packet['study_cores'] != seal['study_core_index']:
        raise ValueError('study core index drift')
    for p in extension:
        contract_hash = digest(study_contract(p, seal['source_bindings']))
        if p['parent_contracts'] != {'candidate:' + p['probe_id']: contract_hash}:
            raise ValueError('new study core does not bind its actual mathematical task')
        for decision in ('holds', 'refuted'):
            challenge_task(p, decision, snapshot_id=packet['snapshot_id'], library_revision=packet['library_revision'])
    from qcb_assessment_v3_reference import check_semantics
    semantics = check_semantics(packet, directory)
    if require_qualified:
        q = validate_qualification(seal)
        receipt = read_json(directory / 'reference-checks.json')
        if digest(receipt) != q['private_receipt_digest']:
            raise ValueError('extension execution receipt changed')
        validate_receipt_header(packet, seal, q, receipt)
        from qcb_learning_reference import validate_reference_results
        validate_reference_results({**packet, 'probes': extension}, receipt['results'])
        from qcb_assessment_v3_reference import validate_transport_results
        validate_transport_results(packet, directory, receipt['transport_results'])
        if (receipt['semantic_review'] != semantics or semantics != q['review']
                or receipt['source_commit'] != receipt['tested_code_commit']
                or receipt['source_commit'] != q['source_commit']
                or receipt['pipeline_source_hashes_lf'] != source_identity()
                or receipt['new_reference_checks'] != q['new_reference_checks']):
            raise ValueError('private v3 receipt does not match qualified semantics/source/checks')
        execution_ids = [r['execution_id'] for row in receipt['results'] + receipt['transport_results']
                         for r in row['replays']]
        if len(execution_ids) != 14 or len(set(execution_ids)) != len(execution_ids):
            raise ValueError('ordinary and transport executions must be distinct')
        validate_software()
    return packet, seal


def validate_receipt_header(packet, seal, qualification, receipt):
    from qcb_learning_reference import REFERENCE_PROFILE
    fields = {'schema_version', 'seal_digest', 'cohort_digest', 'source_commit', 'tested_code_commit',
              'pipeline_source_hashes_lf', 'semantic_review', 'profile', 'passed', 'results',
              'transport_results', 'new_reference_checks', 'elapsed_seconds', 'execution_class',
              'isolated', 'model_calls', 'model_performance_measured'}
    _shape(receipt, fields, 'private reference receipt')
    elapsed = receipt['elapsed_seconds']
    if (receipt['schema_version'] != 'qcb.private_assessment_references.v3'
            or receipt['seal_digest'] != digest(seal) or receipt['cohort_digest'] != digest(packet)
            or receipt['passed'] is not True or receipt['profile'] != REFERENCE_PROFILE
            or receipt['execution_class'] != 'trusted_local_authored_reference'
            or receipt['isolated'] is not False or type(receipt['model_calls']) is not int
            or receipt['model_calls'] != 0 or receipt['model_performance_measured'] is not False
            or type(elapsed) not in (int, float) or not math.isfinite(elapsed)
            or not 0 <= elapsed <= REFERENCE_PROFILE['batch_wall_seconds']
            or receipt['source_commit'] != receipt['tested_code_commit']
            or receipt['source_commit'] != qualification['source_commit']):
        raise ValueError('private receipt envelope contradicts qualified execution scope')


def source_identity():
    from qcb_assessment_reference import pipeline_identity
    paths = [B / 'src/qcb_assessment_v3.py', B / 'src/qcb_assessment_v3_reference.py', SEAL]
    return {**pipeline_identity(), **{p.relative_to(R).as_posix(): text_sha(p) for p in paths}}


def _committed(identity, commit):
    if (not isinstance(commit, str) or re.fullmatch('[0-9a-f]{40}', commit) is None
            or subprocess.run(['git', 'merge-base', '--is-ancestor', commit, 'HEAD'], cwd=R,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode):
        raise ValueError('actual tested source commit must be retained in history')
    for path, expected in identity.items():
        raw = subprocess.check_output(['git', 'show', commit + ':' + path], cwd=R)
        if hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest() != expected:
            raise ValueError('tested source and current extension pipeline differ')


def validate_qualification(seal=None):
    seal = load_seal() if seal is None else seal
    q = read_json(QUALIFICATION)
    fields = {'schema_version', 'seal_digest', 'base_qualification_digest', 'passed',
              'private_receipt_digest', 'source_commit', 'pipeline_source_hashes_lf',
              'new_reference_checks', 'review', 'execution_class', 'isolated',
              'model_performance_measured'}
    _shape(q, fields, 'extension qualification')
    if (q['schema_version'] != 'qcb.assessment_extension_qualification.v3'
            or q['seal_digest'] != digest(seal)
            or q['base_qualification_digest'] != digest(base.validate_qualification())
            or q['passed'] is not True or not _hash(q['private_receipt_digest'])
            or q['execution_class'] != 'trusted_local_authored_reference'
            or q['isolated'] is not False or q['model_performance_measured'] is not False):
        raise ValueError('extension mathematical qualification is missing or stale')
    if q['new_reference_checks'] != {'positive': 8, 'fresh_final_roots': 4,
                                    'transport_roots': 4, 'expected_rejections': 2, 'total': 14}:
        raise ValueError('all four new roots and both rejection controls must be checked')
    review_fields = {'neutral_decoder_digest', 'source_comparison_digest', 'answer_review_digest',
                     'curation_digest', 'transport_digest', 'exposure_audit_digest',
                     'review_role_identities_sha256_utf8', 'AI_not_authenticated_human_approval'}
    _shape(q['review'], review_fields, 'public extension review')
    if (q['review']['AI_not_authenticated_human_approval'] is not True
            or q['review']['exposure_audit_digest'] != seal['exposure_audit_digest']
            or not all(_hash(q['review'][k]) for k in review_fields - {
                'review_role_identities_sha256_utf8', 'AI_not_authenticated_human_approval'})):
        raise ValueError('extension review not bound')
    roles = q['review']['review_role_identities_sha256_utf8']
    if (not isinstance(roles, dict) or set(roles) != {'author', 'decoder', 'source_reviewer', 'exposure_reviewer'}
            or not all(_hash(v) for v in roles.values()) or len(set(roles.values())) != len(roles)):
        raise ValueError('distinct review role commitments required')
    if q['pipeline_source_hashes_lf'] != source_identity():
        raise ValueError('extension mathematical pipeline changed')
    _committed(q['pipeline_source_hashes_lf'], q['source_commit'])
    return q


def protocol_identity():
    paths = [B / 'scripts/assessment_v3.py', B / 'src/qcb_assessment_v3.py',
             B / 'src/qcb_assessment_training.py', B / 'tests/test_assessment_v3.py',
             B / 'tests/test_assessment_v3_reference.py', B / 'tests/test_assessment_training.py',
             B / 'tracks/lean/assessment-v3/training-profiles.json']
    return {**base.protocol_identity(), **{p.relative_to(R).as_posix(): text_sha(p) for p in paths}}


def validate_software():
    r = read_json(SOFTWARE)
    _shape(r, {'schema_version', 'passed', 'source_hashes_lf', 'integration_digest',
               'controls', 'training_export_counts', 'model_calls', 'training_launched'}, 'v3 software receipt')
    if (r['schema_version'] != 'qcb.assessment_software_checks.v3' or r['passed'] is not True
            or r['source_hashes_lf'] != protocol_identity() or not _hash(r['integration_digest'])
            or r['model_calls'] != 0 or r['training_launched'] is not False
            or type(r['controls']) is not int or r['controls'] < 12
            or r['training_export_counts'] != {'nl_and_semantic_views': 86, 'lean_views': 12,
                                              'distinct_existing_cores': 74}):
        raise ValueError('v3 software controls incomplete or stale')
    return r


def public_status():
    old = base.public_status()
    seal = load_seal()
    q = validate_qualification(seal)
    combined = {'schema_version': 'qcb.assessment_display_index.v3',
                'probe_index': deepcopy(old['seal']['probe_index']) + deepcopy(seal['probe_index']),
                'base_v2_seal_digest': digest(old['seal']), 'extension_seal_digest': digest(seal)}
    coverage = base.coverage_record(combined)
    coverage['existing_catalog_parent_core_count'] = old['coverage']['sealed_parent_core_count']
    coverage['study_core_count'] = len(seal['study_core_index'])
    return {**old, 'schema_version': 'qcb.assessment_status.v3', 'seal': combined,
            'coverage': coverage, 'base_v2_seal_digest': digest(old['seal']),
            'extension_seal': seal, 'extension_qualification': q,
            'study_core_index': seal['study_core_index'],
            'extension_protocol_validation': validate_software(),
            'reference_inheritance': '14 roots from unchanged qualified v2; 4 additional roots checked by v3',
            'canonical_admissions_changed': False}
