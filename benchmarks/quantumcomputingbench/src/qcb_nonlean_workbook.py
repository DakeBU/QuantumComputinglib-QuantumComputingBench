"""Content-bound supplemental NL exercises; never allocate cores or splits."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath

from qcb_core import digest, read_json
from qcb_curriculum import core_contract, load_catalog, validate_proposals

B = Path(__file__).resolve().parents[1]
R = B.parents[1]
PACKAGE = B / 'tracks/non-lean/packages/99e830bd-e868-4c7c-947c-8187a63ce46a'
CONTINUATION = B / 'tracks/non-lean/packages/ba29cd0a-3472-4598-a541-9294da63f30e'
AUDIT = B / 'reports/nonlean-intake-20261104'
BATCH2 = B / 'tracks/non-lean/packages/3703ef46-1a1d-47ab-a991-dc9d94a0f386'
BATCH2_INTAKE = B / 'reports/nonlean-intake-20261109/intake.json'
FROZEN = '86b9e677566498da04faebcf4e5ed57f177c6bb1'
GROUPS = {'A': ('normalization', 'Normalization and accepted states'),
          'B': ('coherence', 'Coherent constructions and precision'),
          'C': ('tensor-polynomial', 'Tensor structure and polynomial samples'),
          'G': ('gram-contractions', 'Gram contractions and sequential isometries'),
          'P': ('phase-suppliers', 'Phase suppliers and coherent error'),
          'E': ('error-composition', 'Error bounds across preparation and projection')}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def question_sha(packet):
    return hashlib.sha256(packet['question'].encode()).hexdigest()


def repository_path(value):
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or '\\' in value or ':' in value:
        raise ValueError('non-relative contribution path')
    resolved = R.joinpath(*path.parts).resolve()
    if not resolved.is_relative_to(B.resolve()):
        raise ValueError('contribution path leaves benchmark')
    return resolved


def band(packet):
    d = packet['difficulty']
    value = d.get('construction_band') or d.get('provisional_route_band') or d.get('D1_D4', {}).get('provisional_route_band')
    if value not in {'D1', 'D2', 'D3', 'D4'}:
        raise ValueError('missing declared construction band')
    return value


def batch2_entries(catalog, graph):
    """Verify the shipped content and its reader intake before projection."""
    manifest_path = BATCH2 / 'manifest.json'
    manifest = read_json(manifest_path)
    intake = read_json(BATCH2_INTAKE)
    if (manifest['schema_version'] != 'qcb.nonlean_batch_manifest.v1'
            or intake['schema_version'] != 'qcb.nl_batch2_intake.v1'
            or manifest['package_id'] != BATCH2.name or intake['manifest_sha256'] != sha(manifest_path)
            or manifest['catalog_hash'] != catalog['catalog_hash']
            or manifest['snapshot']['snapshot_id'] != catalog['snapshot_id']
            or manifest['snapshot']['source_commit'] != FROZEN
            or manifest['snapshot']['sha256'] != sha(repository_path(manifest['snapshot']['path']))
            or manifest['new_candidates'] != 6 or manifest['new_cores_admitted'] != 0
            or any(manifest[k] is not False for k in ('human_approval', 'new_Lean_execution', 'model_responses_collected'))):
        raise ValueError('batch 2 identity, frozen snapshot or admission boundary changed')
    files = {}
    for row in manifest['files']:
        path = repository_path(row['path'])
        if path in files or path.stat().st_size != row['bytes'] or sha(path) != row['sha256']:
            raise ValueError('batch 2 original contribution bytes changed: ' + row['path'])
        files[path] = row['sha256']
    contributions = manifest['contributions']
    slots = {row['slot'] for row in contributions}
    if len(contributions) != 6 or slots != {'G1', 'G2', 'P1', 'P2', 'E1', 'E2'} or set(intake['items']) != slots:
        raise ValueError('batch 2 requires exactly six reviewed question identities')
    expected = {p for p in BATCH2.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    expected |= {repository_path(row['proposal_path']) for row in contributions}
    if set(files) != expected - {manifest_path}:
        raise ValueError('batch 2 original file inventory changed')

    def delivery_rows(name):
        rows = [json.loads(line) for line in (BATCH2 / name).read_text(encoding='utf-8').splitlines()]
        if len(rows) != 6 or {row['slot'] for row in rows} != slots:
            raise ValueError('batch 2 export identity mismatch: ' + name)
        return {row['slot']: row for row in rows}

    questions = delivery_rows('questions-only.jsonl')
    references = delivery_rows('references-rubrics.jsonl')
    review_index = read_json(BATCH2 / 'review-index.json')
    indexed = {row['slot']: row for row in review_index['items']}
    if len(review_index['items']) != 6 or set(indexed) != slots or review_index['AI_reviews_not_human_approval'] is not True:
        raise ValueError('batch 2 review index is incomplete')
    for group in ('G', 'P', 'E'):
        authorization = read_json(BATCH2 / 'evidence' / (group + '-phase2-authorization.json'))
        bindings = {name: value for name, value in authorization['bound_files'].items() if name.startswith('reviews/')}
        if (authorization['phase1_observed_before_phase2_authorization'] is not True or not bindings
                or any(files.get(BATCH2 / name) != value for name, value in bindings.items())):
            raise ValueError('batch 2 question-first evidence changed')

    source_blobs = {}

    def check_source(path, commit, expected_hash):
        if (commit not in {manifest['base_commit'], FROZEN} or not re.fullmatch(r'[0-9a-f]{40}', commit)
                or not re.fullmatch(r'QuantumBlockEncoding/(?:[\w]+/)*[\w]+\.lean', path)):
            raise ValueError('invalid batch 2 pinned source')
        key = (commit, path)
        if key not in source_blobs:
            source_blobs[key] = subprocess.check_output(['git', 'show', commit + ':' + path], cwd=R).replace(b'\r\n', b'\n')
        blob = source_blobs[key]
        if hashlib.sha256(blob).hexdigest() != expected_hash:
            raise ValueError('batch 2 pinned source changed: ' + path)
        return blob

    entries, proposals = [], []
    for row in contributions:
        slot = row['slot']
        path = BATCH2 / 'qa' / (slot + '.json')
        packet = read_json(path)
        frozen = read_json(BATCH2 / 'questions' / (slot + '.json'))
        qfields = {'slot', 'core_id', 'title', 'question', 'assumptions', 'conventions'}
        if (repository_path(row['payload_path']) != path or packet['slot'] != slot or row['core_id'] != packet['core_id']
                or row['payload_sha256'] != files[path]
                or packet['core_id'] != 'candidate:' + packet['proposal_id']
                or packet['snapshot_id'] != catalog['snapshot_id'] or packet['contribution_type'] != 'new_candidate'
                or packet['split'] != 'unassigned_pending_reconciliation' or packet['admission'] != 'candidate_not_counted'
                or packet['dedup_review_required'] is not True
                or questions[slot] != {k: packet[k] for k in qfields}
                or any(frozen[k] != packet[k] for k in qfields | {'source_refs', 'target_nodes', 'supporting_nodes'})):
            raise ValueError('batch 2 frozen question or candidate contract changed: ' + slot)
        reference = references[slot]
        if reference['item_digest'] != digest(packet) or any(reference[k] != packet[k] for k in (
                'reference_answer', 'rubric', 'boundary_cases', 'common_errors', 'reasoning_map')):
            raise ValueError('batch 2 reference projection differs: ' + slot)
        index = indexed[slot]
        report_path = BATCH2 / 'reviews' / (slot[0] + '-review.json')
        report = read_json(report_path)
        reviewed = [item for item in report['items'] if item['slot'] == slot]
        if (index != row['review'] or repository_path(index['report_path']) != report_path
                or index['report_sha256'] != files[report_path] or index['payload_sha256'] != files[path]
                or index['item_digest'] != digest(packet) or index['core_id'] != packet['core_id']
                or index['human_approval'] is not False or index['admission'] != 'candidate_not_counted'
                or report['reviewer'] != index['reviewer'] or report['reviewer'] == packet['author']
                or len(reviewed) != 1 or reviewed[0]['verdict'] != 'accept' or index['verdict'] != 'accept'
                or reviewed[0]['payload_sha256_raw'] != files[path] or reviewed[0]['item_digest'] != digest(packet)
                or not reviewed[0]['reasoning'] or not reviewed[0]['source_checks']):
            raise ValueError('batch 2 exact final content review differs: ' + slot)
        for ref in packet['source_refs']:
            blob = check_source(ref['path'], ref['source_commit'], ref['sha256'])
            for span in ref.get('declaration_spans', []):
                lines = blob.splitlines(keepends=True)
                if not 1 <= span['line_start'] <= span['line_end'] <= len(lines) or hashlib.sha256(
                        b''.join(lines[span['line_start']-1:span['line_end']])).hexdigest() != span['sha256_lf']:
                    raise ValueError('batch 2 declaration span changed: ' + span['name'])
        for ref in reviewed[0]['source_checks']:
            check_source(ref.get('file', ref.get('path')), ref['source_commit'], ref['sha256_lf'])
        if not packet['target_nodes'] or not set(packet['target_nodes'] + packet['supporting_nodes']) <= graph.keys():
            raise ValueError('batch 2 anchor is absent from the frozen graph: ' + slot)
        if (abs(sum(r['weight'] for r in packet['rubric']) - 10) > 1e-12
                or any(r['weight'] <= 0 or not r['criterion'] for r in packet['rubric'])):
            raise ValueError('invalid batch 2 grading scale: ' + slot)
        annotation = intake['items'][slot]
        if (annotation['payload_sha256'] != files[path] or annotation['question_sha256'] != question_sha(packet)
                or annotation['verdict'] != 'public_study_only'):
            raise ValueError('batch 2 reader disposition is stale: ' + slot)
        reasoning = annotation.get('display_reasoning_map', packet['reasoning_map'])
        seen = {n['id'] for n in reasoning['inputs']}
        if len(seen) != len(reasoning['inputs']):
            raise ValueError('duplicate batch 2 reasoning input')
        for step in reasoning['steps']:
            if step['id'] in seen or not set(step['required_inputs']) <= seen:
                raise ValueError('invalid batch 2 reasoning topology: ' + slot)
            seen.add(step['id'])
        proposal = read_json(repository_path(row['proposal_path']))
        if (proposal['proposed_contract'] != core_contract(packet)
                or proposal['contract_hash'] != digest(core_contract(packet))
                or proposal['item_digest'] != digest(packet) or proposal['payload_sha256'] != files[path]
                or proposal['core_id'] != packet['core_id'] or proposal['split'] != packet['split']):
            raise ValueError('batch 2 proposed core differs from the reviewed contract: ' + slot)
        proposals.append(proposal)
        entries.append({'slot': slot, 'view_id': 'qcb-supplementary-' + slot.lower() + '-3703ef46',
                        'band': band(packet), 'packet': packet, 'payload_path': row['payload_path'],
                        'payload_sha256': files[path], 'question_sha256': question_sha(packet),
                        'review': {'report_path': index['report_path'], 'limitations': annotation['limitations']},
                        'notation': {'equations': []}, 'clarifications': annotation,
                        'display_reasoning_map': reasoning, 'display_rubric': packet['rubric']})
    return entries, proposals


def load_workbook():
    """Validate originals, current contracts and actual intake reviews."""
    catalog, originals, graph = load_catalog()
    manifest = read_json(PACKAGE / 'manifest.json')
    continuation = read_json(CONTINUATION / 'manifest.json')
    if manifest['catalog_hash'] != catalog['catalog_hash']:
        raise ValueError('cohort requires current-contract reconciliation')
    if continuation['original_manifest_sha256'] != sha(PACKAGE / 'manifest.json'):
        raise ValueError('continuation no longer binds the original cohort')
    for record in (manifest, continuation):
        for row in record['files']:
            path = repository_path(row['path'])
            if sha(path) != row['sha256'] or path.stat().st_size != row['bytes']:
                raise ValueError('original contribution bytes changed: ' + row['path'])
    intake = read_json(AUDIT / 'intake.json')
    if (intake['distinct_qa_packets'] != 12 or intake['byte_identical_shared_contribution_files'] != 104
            or intake['canonical_admissions_changed'] is not False):
        raise ValueError('archive overlap or admission accounting changed')
    reviews, notation = {}, {}
    comparison = read_json(AUDIT / 'reader-comparison.json')
    if (comparison['schema_version'] != 'qcb.nl_reader_comparison.v1'
            or comparison['verdict'] != 'accept_with_limitations'
            or comparison['human_expert_approval'] is not False):
        raise ValueError('reader notation/scope comparison is not accepted')
    expected_bindings = {(AUDIT / filename).relative_to(R).as_posix() for filename in (
        'A-notation.json', 'B-notation.json', 'C-notation.json', 'A-reader-addendum.json',
        'B-rubric-addendum.json', 'C-reader-addendum.json', 'reader-clarifications.json')}
    if set(comparison['reviewed_file_sha256']) != expected_bindings:
        raise ValueError('reader comparison must bind every notation and clarification input')
    for path, expected in comparison['reviewed_file_sha256'].items():
        if sha(repository_path(path)) != expected:
            raise ValueError('notation or scope clarification changed after comparison')
    clarifications = read_json(AUDIT / 'reader-clarifications.json')['items']
    for group in ('A', 'B', 'C'):
        report = read_json(AUDIT / (group + '-review.json'))
        if report['schema_version'] != 'qcb.nl_intake_review.v1':
            raise ValueError('unsupported intake review')
        phase = repository_path(report['phase1_path'])
        if sha(phase) != report['phase1_sha256']:
            raise ValueError('question-first derivation changed')
        for item in report['items']:
            if item['slot'] in reviews:
                raise ValueError('duplicate intake review')
            reviews[item['slot']] = {**item, 'reviewer': report['reviewer'],
                'report_path': (AUDIT / (group + '-review.json')).relative_to(R).as_posix()}
        annotations = read_json(AUDIT / (group + '-notation.json'))
        for item in annotations['items']:
            if item['slot'] in notation:
                raise ValueError('duplicate question notation')
            notation[item['slot']] = item
    entries, proposals, source_blobs = [], [], {}
    for row in manifest['contributions']:
        path = repository_path(row['payload_path'])
        packet = read_json(path)
        slot = packet['slot']
        review = reviews[slot]
        if (digest(packet) != row['item_digest'] or review['payload_sha256'] != sha(path)
                or review['question_sha256'] != question_sha(packet)
                or review['verdict'] != 'accept_with_limitations'
                or not review['reasoning'] or not review['source_checks']):
            raise ValueError('missing, rejected or stale intake review: ' + slot)
        if review['reviewer'] == packet['author']:
            raise ValueError('intake review cannot be authorship')
        if sum(r['weight'] for r in packet['rubric']) != 10:
            raise ValueError('rubric weights must sum to ten')
        if packet['contribution_type'] == 'existing_core_view':
            if core_contract(packet) != core_contract(originals[packet['core_id']]):
                raise ValueError('supplementary exposition changed the canonical contract')
        elif (packet['contribution_type'] != 'new_candidate'
              or packet['split'] != 'unassigned_pending_reconciliation'
              or packet['admission'] != 'candidate_not_counted'):
            raise ValueError('candidate silently received a scored split or admission')
        for node in packet['target_nodes'] + packet['supporting_nodes']:
            if node not in graph:
                raise ValueError('unknown frozen anchor: ' + node)
        for ref in packet['source_refs']:
            source = ref['path']
            if source not in source_blobs:
                rel = PurePosixPath(source)
                if source == 'benchmarks/quantumcomputingbench/manifests/release-v3/snapshot.json':
                    source_blobs[source] = repository_path(source).read_bytes()
                elif (rel.is_absolute() or '..' in rel.parts or ':' in source or '\\' in source
                        or not source.endswith('.lean')):
                    raise ValueError('invalid source path')
                else:
                    source_blobs[source] = subprocess.check_output(['git', 'show', FROZEN + ':' + source], cwd=R)
            if hashlib.sha256(source_blobs[source].replace(b'\r\n', b'\n')).hexdigest() != ref['sha256']:
                raise ValueError('frozen source binding changed: ' + source)
        given = notation[slot]
        if given['question_sha256'] != question_sha(packet):
            raise ValueError('stale given-question notation')
        for equation in given['equations']:
            if (equation['purpose'] != 'given_question_notation' or not equation['source_excerpt']
                    or equation['source_excerpt'] not in packet['question'] or not equation['tex']):
                raise ValueError('notation is not bound to a given question excerpt')
        clarification = clarifications.get(slot, {})
        if clarification and (clarification['payload_sha256'] != sha(path)
                              or clarification['question_sha256'] != question_sha(packet)):
            raise ValueError('stale reader scope clarification')
        display_map = clarification.get('display_reasoning_map', packet['reasoning_map'])
        overrides = clarification.get('rubric_overrides', {})
        if set(overrides) - {r['id'] for r in packet['rubric']}:
            raise ValueError('grading clarification names an unknown criterion')
        display_rubric = [{**r, 'criterion': overrides.get(r['id'], r['criterion'])} for r in packet['rubric']]
        seen = {n['id'] for n in display_map['inputs']}
        for step in display_map['steps']:
            if step['id'] in seen or any(n not in seen for n in step['required_inputs']):
                raise ValueError('invalid author-supplied reasoning route')
            seen.add(step['id'])
        proposal = read_json(repository_path(row['proposal_path']))
        proposals.append(proposal)
        entries.append({'slot': slot, 'view_id': 'qcb-supplementary-' + slot.lower() + '-99e830bd',
                        'band': band(packet), 'packet': packet, 'payload_path': row['payload_path'],
                        'payload_sha256': sha(path), 'question_sha256': question_sha(packet),
                        'review': review, 'notation': given, 'clarifications': clarification,
                        'display_reasoning_map': display_map, 'display_rubric': display_rubric})
    if len(entries) != 12 or set(reviews) != {e['slot'] for e in entries}:
        raise ValueError('incomplete or duplicated cohort')
    if Counter(e['packet']['contribution_type'] for e in entries) != {'existing_core_view': 4, 'new_candidate': 8}:
        raise ValueError('cohort view/candidate accounting changed')
    new_entries, new_proposals = batch2_entries(catalog, graph)
    entries.extend(new_entries)
    validate_proposals(catalog, proposals + new_proposals)
    dispositions = Counter(e['packet']['contribution_type'] for e in entries)
    result = {'schema_version': 'qcb.nonlean_workbook.v1', 'package_id': manifest['package_id'],
              'additional_package_ids': [BATCH2.name],
              'groups': GROUPS,
              'catalog_hash': catalog['catalog_hash'], 'snapshot_id': catalog['snapshot_id'],
              'source_commit': FROZEN, 'entries': entries,
              'counts': {'packets': len(entries), 'existing_core_expositions': dispositions['existing_core_view'],
                         'unassigned_candidates': dispositions['new_candidate'],
                         'by_band': dict(Counter(e['band'] for e in entries)), 'new_canonical_cores': 0,
                         'new_lean_admissions': 0, 'scored_training_or_evaluation_rows_added': 0},
              'human_expert_approval': False, 'model_performance_measured': False}
    result['workbook_digest'] = digest(result)
    return result


def download_payloads(workbook):
    """Separate supplemental questions, references and operator graph metadata."""
    questions, references, index, reverse = [], [], [], {}
    for entry in workbook['entries']:
        p = entry['packet']
        binding = {'view_id': entry['view_id'], 'question_sha256': entry['question_sha256']}
        questions.append({**binding, 'schema_version': 'qcb.supplementary_question.v1',
                          'input': {k: p[k] for k in ('question', 'assumptions', 'conventions')}})
        references.append({**binding, 'reference_answer': p['reference_answer'], 'rubric': entry['display_rubric'],
                           'grading_notes': entry['clarifications'].get('grading_notes', []),
                           'new_lean_verification': False})
        index.append({**binding, 'slot': entry['slot'], 'title': p['title'], 'band': entry['band'],
                      'core_id': p['core_id'], 'split': p['split'], 'contribution_type': p['contribution_type'],
                      'payload_sha256': entry['payload_sha256'], 'payload_path': entry['payload_path'],
                      'snapshot_id': p['snapshot_id'], 'target_nodes': p['target_nodes'],
                      'supporting_nodes': p['supporting_nodes'], 'review_path': entry['review']['report_path']})
        for key in ('target_nodes', 'supporting_nodes'):
            for node in p[key]:
                reverse.setdefault(node, []).append({**binding, 'role': key})
    def data(value):
        return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()
    def lines(value):
        return ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in value).encode()
    result = {'questions.jsonl': lines(questions), 'references.jsonl': lines(references),
              'index.json': data({'schema_version': 'qcb.supplementary_index.v1',
                  'workbook_digest': workbook['workbook_digest'], 'counts': workbook['counts'],
                  'canonical_training_evaluation_pool': False, 'items': index}),
              'source-node-index.json': data(reverse)}
    result['download-manifest.json'] = data({'schema_version': 'qcb.supplementary_downloads.v1',
        'workbook_digest': workbook['workbook_digest'],
        'files': {name: {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)} for name, raw in result.items()}})
    return result


def check_publication_sources(workbook, commit):
    """Public GitHub provenance must exist at the stated committed revision."""
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('supplementary provenance requires an exact commit')
    paths = {e['payload_path'] for e in workbook['entries']}
    paths.update(e['review']['report_path'] for e in workbook['entries'])
    paths.add((AUDIT / 'reader-comparison.json').relative_to(R).as_posix())
    paths.add(BATCH2_INTAKE.relative_to(R).as_posix())
    for path in sorted(paths):
        try:
            raw = subprocess.check_output(['git', 'show', commit + ':' + path], cwd=R, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as error:
            raise ValueError('supplementary provenance is not committed: ' + path) from error
        if hashlib.sha256(raw).hexdigest() != sha(repository_path(path)):
            raise ValueError('supplementary provenance differs from publication commit: ' + path)


def write_downloads(directory, workbook):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for name, raw in download_payloads(workbook).items():
        (directory / name).write_bytes(raw)


def verify_downloads(directory, workbook):
    directory = Path(directory)
    expected = download_payloads(workbook)
    if {p.name for p in directory.iterdir()} != set(expected):
        raise ValueError('supplemental download inventory differs')
    for name, raw in expected.items():
        if (directory / name).read_bytes() != raw:
            raise ValueError('supplemental download projection changed: ' + name)
