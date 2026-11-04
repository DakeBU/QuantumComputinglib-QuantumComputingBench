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
FROZEN = '86b9e677566498da04faebcf4e5ed57f177c6bb1'
GROUPS = {'A': ('normalization', 'Normalization and accepted states'),
          'B': ('coherence', 'Coherent constructions and precision'),
          'C': ('tensor-polynomial', 'Tensor structure and polynomial samples')}


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
    for group in GROUPS:
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
    validate_proposals(catalog, proposals)
    if len(entries) != 12 or set(reviews) != {e['slot'] for e in entries}:
        raise ValueError('incomplete or duplicated cohort')
    if Counter(e['packet']['contribution_type'] for e in entries) != {'existing_core_view': 4, 'new_candidate': 8}:
        raise ValueError('cohort view/candidate accounting changed')
    result = {'schema_version': 'qcb.nonlean_workbook.v1', 'package_id': manifest['package_id'],
              'groups': GROUPS,
              'catalog_hash': catalog['catalog_hash'], 'snapshot_id': catalog['snapshot_id'],
              'source_commit': FROZEN, 'entries': entries,
              'counts': {'packets': 12, 'existing_core_expositions': 4, 'unassigned_candidates': 8,
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
