"""A content-sealed assessment bank kept outside the public repository.

Public metadata describes scope and evidence, never the sealed questions/gold.
Hash agreement is not independent authentication of a model or a reviewer.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import hashlib
from pathlib import Path
import re
import subprocess

from qcb_core import digest, read_json
from qcb_integrity import text_sha

B = Path(__file__).resolve().parents[1]
R = B.parents[1]
PUBLIC = B / 'tracks/lean/assessment-v2'
SEAL = PUBLIC / 'seal.json'
QUALIFICATION = B / 'reports/assessment-v2/qualification.json'
PROTOCOL_CHECKS = B / 'reports/assessment-v2/software-checks.json'
META_FIELDS = {'probe_id', 'pair_id', 'cluster_id', 'parent_core_ids', 'parent_contracts',
               'split', 'source_nodes', 'difficulty_band'}
PRIVATE_FILES = {'cohort.json', 'decoder-input.json', 'decoder.json', 'source-input.json',
                 'source-comparison.json', 'answer-input.json', 'answer-review.json'}


def probe_metadata(probe):
    return {key: (probe['difficulty']['band'] if key == 'difficulty_band' else deepcopy(probe[key]))
            for key in sorted(META_FIELDS)}


def _hash(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def load_seal(path=SEAL):
    seal = read_json(path)
    fields = {'schema_version', 'release_id', 'base_commit', 'library_revision', 'snapshot_id',
              'catalog_hash', 'proof_inputs_sha256', 'lean_toolchain', 'cohort_digest',
              'private_files_sha256_lf', 'source_bindings', 'probe_index', 'exposure',
              'new_canonical_admissions', 'model_performance_measured'}
    if (set(seal) != fields or seal['schema_version'] != 'qcb.sealed_assessment.v2'
            or seal['exposure'] != 'sealed_local_questions; run_exposure_not_authenticated'
            or seal['new_canonical_admissions'] != 0 or seal['model_performance_measured'] is not False):
        raise ValueError('unexpected sealed assessment contract')
    for key in ('catalog_hash', 'proof_inputs_sha256', 'cohort_digest'):
        if not _hash(seal[key]):
            raise ValueError('invalid public content commitment')
    rows = seal['probe_index']
    if not isinstance(rows, list) or not rows or any(set(row) != META_FIELDS for row in rows):
        raise ValueError('public index may contain only approved assessment metadata')
    if len({row['probe_id'] for row in rows}) != len(rows):
        raise ValueError('duplicate sealed probe identity')
    if (not isinstance(seal['private_files_sha256_lf'], dict)
            or set(seal['private_files_sha256_lf']) != PRIVATE_FILES):
        raise ValueError('sealed private review files required')
    for name, value in seal['private_files_sha256_lf'].items():
        if Path(name).is_absolute() or '..' in Path(name).parts or not _hash(value):
            raise ValueError('unsafe or unbound private file')
    from qcb_curriculum import load_catalog
    from proof_inputs import proof_input_digest
    catalog, _, graph = load_catalog()
    if (seal['catalog_hash'] != catalog['catalog_hash'] or seal['snapshot_id'] != catalog['snapshot_id']
            or seal['proof_inputs_sha256'] != proof_input_digest(R)
            or seal['lean_toolchain'] != (R / 'lean-toolchain').read_text().strip()):
        raise ValueError('assessment source/snapshot changed')
    cores = {row['core_id']: row for row in catalog['cores']}
    pairs = {}
    for row in rows:
        if (row['difficulty_band'] not in {'D1', 'D2', 'D3', 'D4'}
                or not isinstance(row['cluster_id'], str)
                or re.fullmatch('[a-z0-9_]{3,100}', row['cluster_id']) is None):
            raise ValueError('bounded neutral mechanism and design band required')
        if (row['split'] not in {'dev', 'test_public'} or not row['parent_core_ids']
                or set(row['parent_contracts']) != set(row['parent_core_ids'])):
            raise ValueError('sealed evaluation must retain its inherited evaluation split')
        for core in row['parent_core_ids']:
            if (core not in cores or cores[core]['contract_hash'] != row['parent_contracts'][core]
                    or cores[core]['split'] != row['split']):
                raise ValueError('assessment parent contract/split drift')
        for node in row['source_nodes']:
            if (node not in graph or graph[node].get('inventory_status') != 'Compiled'
                    or graph[node].get('open_obligation') is not False):
                raise ValueError('uncompiled or planned assessment anchor')
        pairs.setdefault(row['pair_id'], []).append(row)
    if any(len(p) != 2 or len({r['cluster_id'] for r in p}) != 1
           or len({r['split'] for r in p}) != 1 for p in pairs.values()):
        raise ValueError('each sealed contrast is one complete pair in one split/mechanism')
    for source in seal['source_bindings']:
        p = (R / source['path']).resolve()
        if (set(source) != {'path', 'sha256_lf'} or not p.is_relative_to(R)
                or not source['path'].startswith('QuantumBlockEncoding/')
                or text_sha(p) != source['sha256_lf']):
            raise ValueError('sealed assessment source binding changed')
    return seal


def load_private_bank(directory, *, require_qualified=True):
    directory = Path(directory).resolve()
    if directory.is_relative_to(R):
        raise ValueError('sealed questions and gold must remain outside the public checkout')
    seal = load_seal()
    for name, value in seal['private_files_sha256_lf'].items():
        p = (directory / name).resolve()
        if not p.is_relative_to(directory) or text_sha(p) != value:
            raise ValueError('sealed private file changed: ' + name)
    from qcb_learning_validity import load_cohort
    packet, _ = load_cohort(directory / 'cohort.json')
    if (digest(packet) != seal['cohort_digest']
            or [probe_metadata(p) for p in packet['probes']] != seal['probe_index']):
        raise ValueError('private assessment differs from committed public seal')
    if require_qualified:
        qualification = validate_qualification(seal)
        receipt = read_json(directory / 'reference-checks.json')
        if digest(receipt) != qualification['private_receipt_digest']:
            raise ValueError('sealed private reference receipt changed')
        from qcb_learning_reference import validate_reference_results
        validate_reference_results(packet, receipt['results'])
        validate_protocol_checks()
    return packet, seal


def validate_qualification(seal=None):
    seal = load_seal() if seal is None else seal
    q = read_json(QUALIFICATION)
    public_fields = {'schema_version', 'seal_digest', 'passed', 'reference_checks', 'review',
                     'tested_code_commit', 'pipeline_source_hashes_lf', 'private_receipt_digest',
                     'execution_class', 'isolated', 'model_performance_measured', 'source_runtime'}
    if (set(q) != public_fields or q.get('schema_version') != 'qcb.sealed_assessment_qualification.v2'
            or q.get('seal_digest') != digest(seal) or q.get('passed') is not True
            or q.get('model_performance_measured') is not False
            or q.get('execution_class') != 'trusted_local_authored_reference'
            or q.get('isolated') is not False):
        raise ValueError('assessment qualification missing or stale')
    if set(q['reference_checks']) != {'positive', 'fresh_final_roots', 'expected_rejections', 'total'}:
        raise ValueError('only aggregate public reference counts may be published')
    if set(q['review']) != {'neutral_proposition_decoder', 'independent_polarity_before_gold',
        'complete_question_and_answer_review', 'decoder_identity', 'source_comparer_identity',
        'decoder_digest', 'source_comparison_digest', 'answer_review_digest',
        'review_is_AI_not_authenticated_human_approval'}:
        raise ValueError('only aggregate private review bindings may be published')
    if set(q['source_runtime']) != {'actual_commit', 'proof_inputs_sha256', 'lean_toolchain',
                                   'compiled_modules', 'fresh_gate_digest'}:
        raise ValueError('public runtime metadata must not contain local paths or secret transcripts')
    runtime = q['source_runtime']
    if (runtime['actual_commit'] != seal['library_revision']
            or runtime['proof_inputs_sha256'] != seal['proof_inputs_sha256']
            or runtime['lean_toolchain'] != seal['lean_toolchain']
            or not _hash(runtime['fresh_gate_digest'])):
        raise ValueError('runtime must match the sealed library and production proof inputs')
    from proof_inputs import lean_module_targets
    if runtime['compiled_modules'] != len(lean_module_targets(R)):
        raise ValueError('complete production module gate required')
    counts = q['reference_checks']
    if (any(type(v) is not int or v < 0 for v in counts.values())
            or counts['expected_rejections'] < 2 or counts['expected_rejections'] % 2
            or counts['total'] != counts['positive'] + counts['expected_rejections']):
        raise ValueError('invalid aggregate reference counts')
    if (q['reference_checks']['positive'] != 2 * len(seal['probe_index'])
            or q['reference_checks']['fresh_final_roots'] != len(seal['probe_index'])
            or not q['reference_checks']['expected_rejections']):
        raise ValueError('incomplete authored assessment checks')
    if (q['review']['neutral_proposition_decoder'] is not True
            or q['review']['independent_polarity_before_gold'] is not True
            or q['review']['complete_question_and_answer_review'] is not True):
        raise ValueError('assessment semantic review incomplete')
    if not _hash(q['private_receipt_digest']):
        raise ValueError('private execution receipt not content bound')
    from qcb_assessment_reference import pipeline_identity
    if (q['pipeline_source_hashes_lf'] != pipeline_identity()
            or not isinstance(q['tested_code_commit'], str)
            or re.fullmatch('[0-9a-f]{40}', q['tested_code_commit']) is None):
        raise ValueError('the complete fixed reference pipeline must be identified')
    if subprocess.run(['git', 'merge-base', '--is-ancestor', q['tested_code_commit'], 'HEAD'],
                      cwd=R, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
        raise ValueError('reference source commit is absent from this history')
    for path, expected in q['pipeline_source_hashes_lf'].items():
        p = (R / path).resolve()
        if not p.is_relative_to(R) or text_sha(p) != expected:
            raise ValueError('qualified reference pipeline changed')
        raw = subprocess.check_output(['git', 'show', q['tested_code_commit'] + ':' + path], cwd=R)
        if hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest() != expected:
            raise ValueError('recorded reference source commit differs')
    return q


def coverage_record(seal):
    from qcb_curriculum import load_catalog
    catalog, _, graph = load_catalog()
    course = read_json(B / 'tracks/lean/curriculum/course-v4.json')['entries']
    declarations = {k: n for k, n in graph.items() if n.get('kind') == 'declaration'}
    compiled = {k for k, n in declarations.items() if n.get('inventory_status') == 'Compiled'}
    course_nodes = {n for c in course for n in c['source_node_ids']}
    assessment_nodes = {n for p in seal['probe_index'] for n in p['source_nodes']}
    training = {c['core_id'] for c in catalog['cores'] if c['split'] == 'train'}
    parents = {c for p in seal['probe_index'] for c in p['parent_core_ids']}
    if training & parents:
        raise ValueError('sealed assessment reuses an inherited train core')
    training_nodes = {n for c in catalog['cores'] if c['core_id'] in training
                      for n in c['target_nodes'] + c['supporting_nodes']}
    by_source = []
    for path in sorted({n.get('source') for n in declarations.values()} - {None}):
        ids = {k for k, n in declarations.items() if n.get('source') == path}
        by_source.append({'source': path, 'inventoried_declarations': len(ids),
                          'compiled_inventory_declarations': len(ids & compiled),
                          'course_anchor_count': len(ids & course_nodes),
                          'sealed_assessment_anchor_count': len(ids & assessment_nodes)})
    return {'schema_version': 'qcb.assessment_coverage.v2', 'catalog_hash': catalog['catalog_hash'],
            'snapshot_id': catalog['snapshot_id'], 'declaration_inventory': len(declarations),
            'compiled_inventory': len(compiled), 'course_anchors': len(course_nodes),
            'sealed_assessment_anchors': len(assessment_nodes),
            'compiled_not_anchored_by_these_formal_suites': len(compiled - course_nodes - assessment_nodes),
            'sealed_probe_count': len(seal['probe_index']),
            'sealed_parent_core_count': len(parents), 'sealed_parent_core_ids': sorted(parents),
            'split_counts': dict(sorted(Counter(p['split'] for p in seal['probe_index']).items())),
            'mechanism_counts': dict(sorted(Counter(p['cluster_id'] for p in seal['probe_index']).items())),
            'difficulty_counts': dict(sorted(Counter(p['difficulty_band'] for p in seal['probe_index']).items())),
            'canonical_train_core_count': len(training), 'exact_train_parent_overlap': [],
            'training_shared_source_nodes': sorted(training_nodes & assessment_nodes),
            'all_modules': by_source, 'anchor_coverage_is_mastery_coverage': False,
            'family_disjointness_establishes_mechanism_independence': False,
            'full_graph_mastery_claim_supported': False}


def protocol_identity():
    paths = [B / 'src/qcb_assessment_protocol.py', B / 'scripts/assessment.py',
             B / 'tests/test_assessment_protocol.py', B / 'tests/test_assessment_bank.py']
    return {p.relative_to(R).as_posix(): text_sha(p) for p in paths}


def validate_protocol_checks():
    record = read_json(PROTOCOL_CHECKS)
    if (set(record) != {'schema_version', 'source_hashes_lf', 'protocol_tests', 'privacy_tests',
                        'integration_digest', 'training_export_counts', 'passed', 'model_calls',
                        'training_launched'}
            or record['schema_version'] != 'qcb.assessment_software_checks.v2'
            or record['source_hashes_lf'] != protocol_identity()
            or record['passed'] is not True or record['model_calls'] != 0
            or record['training_launched'] is not False or not _hash(record['integration_digest'])):
        raise ValueError('assessment software checks missing, stale or contain nonpublic fields')
    if (type(record['protocol_tests']) is not int or record['protocol_tests'] < 12
            or type(record['privacy_tests']) is not int or record['privacy_tests'] < 5
            or record['training_export_counts'] != {'nl_and_semantic_views': 86, 'lean_views': 12,
                                                   'distinct_existing_cores': 74}):
        raise ValueError('required software controls or train-only exports are unverified')
    return record


def public_status():
    seal = load_seal()
    qualification = validate_qualification(seal)
    return {'schema_version': 'qcb.assessment_status.v2', 'seal': seal,
            'qualification': qualification, 'coverage': coverage_record(seal),
            'protocol_validation': validate_protocol_checks(),
            'model_performance_measured': False, 'understanding_established': False,
            'candidate_formal_execution': 'ENV_BLOCKED until accepted isolated verifier',
            'private_evidence_publicly_replayable': False}
