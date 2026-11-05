"""Content-bound historical review and fixed authored replay for the v3 extension.

Backend implementation is author-gold-aware. Earlier reviewers decoded the old
spelling only; the four new transport checks establish definitional equivalence.
Nothing here executes student proofs or authenticates real-world identities.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import math
from pathlib import Path
import re
import subprocess
from time import monotonic
from types import SimpleNamespace

import qcb_assessment_bank as base
from qcb_core import digest, read_json
from qcb_integrity import text_sha
from qcb_learning_reference import (REFERENCE_PROFILE, REPLAY_FIELDS, EVIDENCE_FIELDS,
                                    _RecordedAuthoredVerifier, _compact_evidence,
                                    validate_reference_results)
from qcb_learning_validity import challenge_task
from qcb_lean import APPROVED_AXIOMS
from qcb_proof_session import ProofSession, SessionLimits, validate_task

ROLES = frozenset({'candidates', 'authored_references', 'neutral_input', 'neutral_decoder',
    'neutral_mapping', 'source_input', 'source_comparison', 'answer_input', 'answer_review',
    'curation', 'normalization_seal', 'normalized_probes', 'normalized_references',
    'exposure_audit', 'statement_seal', 'prior_reference_replay'})
TRANSPORT_PROOF = 'by exact Iff.rfl'
HELPER_CANDIDATE = '92acaaa3-64b1-4778-bfc6-1e8a6c3cd34d'
HELPER_CONTEXT = ('namespace QCBCandidate001\n\ndef controlOnFirstTrue {α : Type*}\n'
    '    (F : Equiv.Perm (Bool × α)) (z : Bool × α) : Bool × α :=\n'
    '  if z.1 then F z else z\n\nend QCBCandidate001')
TRANSPORT_POLICY = {'kind': 'definitional_equivalence_not_new_semantic_review',
                    'proof': TRANSPORT_PROOF}
COUNTS = {'positive': 8, 'fresh_final_roots': 4, 'transport_roots': 4,
          'expected_rejections': 2, 'total': 14}


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _shape(value, fields, label):
    _require(isinstance(value, dict) and set(value) == set(fields), 'unexpected fields: ' + label)


def _sha_text(value):
    return hashlib.sha256(value.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def _rows(document, field, key, ids):
    rows = document.get(field)
    _require(isinstance(rows, list) and len(rows) == len(ids)
             and all(isinstance(r, dict) and isinstance(r.get(key), str) for r in rows)
             and {r[key] for r in rows} == set(ids), 'complete unique provenance rows required: ' + field)
    return {r[key]: r for r in rows}


def _substantive(value):
    if isinstance(value, dict):
        value = ' '.join(str(v) for v in value.values())
    _require(isinstance(value, str) and len(value.strip()) >= 40, 'substantive historical review required')


def _load_provenance(directory):
    directory = Path(directory).resolve()
    provenance = read_json(directory / 'provenance.json')
    _shape(provenance, {'schema_version', 'files', 'mappings', 'normalization_transport',
                        'author_gold_seen_by_backend'}, 'private v3 provenance')
    _require(provenance['schema_version'] == 'qcb.assessment_provenance.v3'
             and provenance['normalization_transport'] == TRANSPORT_POLICY
             and provenance['author_gold_seen_by_backend'] is True,
             'explicit old-spelling review/normalization boundary required')
    files = provenance['files']
    _require(isinstance(files, dict) and set(files) == ROLES, 'exact copied provenance files required')
    docs, hashes, paths = {}, {}, set()
    for role, entry in files.items():
        _shape(entry, {'path', 'sha256_raw'}, 'provenance file')
        _require(isinstance(entry['path'], str) and not Path(entry['path']).is_absolute()
                 and '..' not in Path(entry['path']).parts, 'unsafe provenance path')
        path = (directory / entry['path']).resolve()
        _require(path.is_relative_to(directory) and path not in paths, 'unsafe or repeated provenance path')
        _require(path.stat().st_size <= 32_000_000, 'bounded provenance file required')
        raw = path.read_bytes()
        _require(isinstance(entry['sha256_raw'], str)
                 and hashlib.sha256(raw).hexdigest() == entry['sha256_raw'], 'raw provenance file changed: ' + role)
        paths.add(path)
        hashes[role] = entry['sha256_raw']
        docs[role] = read_json(path)
    return provenance, docs, hashes


def _extension(packet, directory):
    old = read_json(Path(directory) / 'base-v2/cohort.json')
    _require(digest(old) == base.load_seal()['cohort_digest'], 'frozen base cohort changed')
    old_probes = old.get('probes')
    _require(isinstance(old_probes, list) and len(old_probes) == 14, 'exact fourteen-probe base required')
    probes = packet.get('probes')
    _require(isinstance(probes, list) and len(probes) == 18 and probes[:14] == old_probes,
             'frozen base propositions changed, removed or reordered')
    extension = probes[14:]
    _require(len({p['probe_id'] for p in probes}) == 18
             and all(p['split'] == 'test_public' and p['cluster_id'] == 'promise_register_protocols'
                     for p in extension), 'four distinct test-only Promise probes required')
    return extension


def _helper(candidate):
    context = candidate['formal_context']['required_minimal_context_lean']
    if context:
        _require(candidate['candidate_id'] == HELPER_CANDIDATE and context == HELPER_CONTEXT,
                 'only the exact reviewed local helper is allowed for transport')
    return context


def _check_semantics(packet, directory):
    """Verify historical raw bindings, not the truth of textual AI judgments."""
    provenance, d, h = _load_provenance(directory)
    extension = _extension(packet, directory)
    ids = {p['probe_id'] for p in extension}
    candidates = _rows(d['candidates'], 'items', 'candidate_id', ids)
    _require(d['normalized_probes']['probes'] == extension, 'normalized packet changed')
    mappings = provenance['mappings']
    _require(isinstance(mappings, list) and len(mappings) == 4, 'four explicit identity mappings required')
    by_probe = {}
    for row in mappings:
        _shape(row, {'probe_id', 'candidate_id', 'review_task_id'}, 'review mapping')
        _require(row['probe_id'] == row['candidate_id'] and row['probe_id'] in ids
                 and row['probe_id'] not in by_probe, 'candidate mapping drift')
        by_probe[row['probe_id']] = row['review_task_id']
    tids = set(by_probe.values())
    _require(len(tids) == 4 and d['neutral_mapping'] == [
        {'task_id': row['review_task_id'], 'author_candidate_id': row['candidate_id']}
        for row in mappings], 'original neutral mapping changed')
    neutral = d['neutral_input']
    _shape(neutral, {'schema_version', 'status', 'standard_definitional_conventions',
                     'literal_definition_excerpts', 'definition_evidence_scope', 'tasks'}, 'no-gold neutral input')
    neutral_rows = _rows(neutral, 'tasks', 'task_id', tids)
    decoder = d['neutral_decoder']
    _require(decoder['input_bytes_sha256'] == h['neutral_input'], 'decoder raw input binding changed')
    decoded = _rows(decoder, 'items', 'task_id', tids)
    source = d['source_input']
    _shape(source, {'schema_version', 'neutral_input', 'neutral_decoder', 'questions',
                    'statement_elaboration', 'boundary', 'neutral_input_raw_sha256',
                    'decoder_raw_sha256'}, 'no-gold source input')
    _require(source['neutral_input'] == neutral and source['neutral_decoder'] == decoder
             and source['neutral_input_raw_sha256'] == h['neutral_input']
             and source['decoder_raw_sha256'] == h['neutral_decoder'], 'source input substituted its neutral evidence')
    questions = _rows(source, 'questions', 'task_id', tids)
    comparison = d['source_comparison']
    _require(comparison['input_binding']['raw_bytes_sha256'] == h['source_input']
             and comparison['review_scope']['no_gold_seen_before_first_verdict'] is True,
             'first source verdict must bind the sole no-gold input')
    verdicts = _rows(comparison, 'items', 'task_id', tids)
    answer_input = d['answer_input']
    _require(answer_input['earlier_first_source_verdict_sha256_raw'] == h['source_comparison']
             and answer_input['earlier_source_verdict'] == comparison
             and answer_input['decision_encoding_adapter_only'] == {'P holds': 'holds', 'P fails': 'refuted'},
             'after-gold input replaced the frozen first verdict')
    answers = _rows(answer_input, 'items', 'task_id', tids)
    review = d['answer_review']
    _require(review['input_binding']['raw_bytes_sha256'] == h['answer_input']
             and review['input_binding']['frozen_first_source_verdict_raw_sha256'] == h['source_comparison']
             and review['scope']['gold_seen_in_this_phase'] is True
             and review['scope']['first_verdict_preserved'] is True
             and review['overall']['decisions_match_frozen_verdict'] is True
             and review['overall']['mandatory_rubric_repairs'] == [], 'answer review lacks the preserved first verdict')
    reviewed = _rows(review, 'items', 'task_id', tids)
    curated = d['curation']
    _require(curated['candidate_packet_sha256_raw'] == h['candidates']
             and curated['answer_review_sha256_raw'] == h['answer_review']
             and curated['source_comparison_sha256_raw'] == h['source_comparison']
             and curated['reference_replay_sha256_raw'] == h['prior_reference_replay']
             and curated['original_candidate_packet_unchanged'] is True
             and curated['questions_P_assumptions_contexts_unchanged'] is True
             and curated['rubric_mathematical_repairs'] == 0
             and curated['worked_expansions_root_reviewed'] is True, 'curation provenance or mathematical repair boundary changed')
    curation = _rows(curated, 'items', 'author_candidate_id', ids)
    original_refs = d['authored_references']
    _require(original_refs['candidate_packet_sha256_raw'] == h['candidates']
             and original_refs['statement_seal_sha256_raw'] == h['statement_seal'], 'original reference/seal binding changed')
    refs = _rows(original_refs, 'items', 'candidate_id', ids)
    statement = d['statement_seal']
    _require(statement['candidate_packet_sha256_raw'] == h['candidates']
             and statement['neutral_input_sha256_raw'] == h['neutral_input'], 'historical statement seal changed')
    sealed = _rows(statement, 'items', 'candidate_id', ids)
    prior = d['prior_reference_replay']
    _require(prior['candidate_packet_sha256_raw'] == h['candidates']
             and prior['statement_seal_sha256_raw'] == h['statement_seal']
             and prior['authored_reference_sha256_raw'] == h['authored_references']
             and prior['passed'] is True and prior['model_calls'] == 0,
             'historical curation replay provenance changed')
    normalized = _rows(d['normalized_references'], 'items', 'candidate_id', ids)
    normalization = d['normalization_seal']
    normalized_rows = _rows(normalization, 'items', 'probe_id', ids)
    transports = _rows(normalization, 'transport', 'candidate_id', ids)
    known_bindings = {Path(provenance['files'][role]['path']).name: value for role, value in h.items()}
    _require(len(known_bindings) == len(h), 'ambiguous copied provenance basenames')
    normalization_roles = {'candidates', 'curation', 'authored_references', 'statement_seal',
                           'prior_reference_replay', 'neutral_input', 'neutral_decoder',
                           'source_comparison', 'answer_review'}
    expected_bindings = {Path(provenance['files'][role]['path']).name: h[role]
                         for role in normalization_roles}
    for document in (normalization, d['normalized_probes']):
        bindings = document['input_bindings']
        _require(isinstance(bindings, list) and len(bindings) == len(expected_bindings)
                 and {Path(e['path'].replace('\\', '/')).name: e['sha256_raw'] for e in bindings}
                 == expected_bindings, 'normalization input has missing/stale raw provenance')
        for entry in bindings:
            _require(known_bindings.get(Path(entry['path'].replace('\\', '/')).name) == entry['sha256_raw'],
                     'normalization input has missing/stale raw provenance')
    _require(d['normalized_probes']['normalization_transport'] == normalization['transport'],
             'normalization transport records differ')
    role_ids = {'author': d['candidates']['author_identity'], 'decoder': decoder['reviewer_identity'],
                'source_reviewer': comparison['reviewer_identity'],
                'exposure_reviewer': d['exposure_audit']['auditor_identity']}
    _require(all(isinstance(v, str) and v.strip() for v in role_ids.values())
             and len(set(role_ids.values())) == 4 and review['reviewer_identity'] == role_ids['source_reviewer'],
             'distinct author/decoder/source/exposure identities required')
    current_sources = packet['source_bindings']
    _require(isinstance(current_sources, list) and current_sources,
             'current packet source union required')
    current_by_path = {}
    for binding in current_sources:
        _shape(binding, {'path', 'sha256_lf'}, 'current packet source binding')
        _require(isinstance(binding['path'], str) and binding['path'] not in current_by_path,
                 'unique current source paths required')
        current_by_path[binding['path']] = binding['sha256_lf']
    for p in extension:
        cid = p['probe_id']; tid = by_probe[cid]; candidate = candidates[cid]
        ctx = candidate['formal_context']; helper = _helper(candidate)
        _shape(neutral_rows[tid], {'task_id', 'imports', 'local_context', 'proposition'}, 'neutral task')
        _require(neutral_rows[tid] == {'task_id': tid, 'imports': ctx['imports'],
                    'local_context': helper, 'proposition': ctx['proposition']}, 'reviewed old P/context changed')
        _substantive(decoded[tid]['decoded_mathematics']); _substantive(decoded[tid]['semantic_slots'])
        _shape(questions[tid], {'task_id', 'question', 'assumptions', 'conventions'}, 'no-gold question')
        for field in ('question', 'assumptions', 'conventions'):
            _require(p[field] == candidate[field] == questions[tid][field] == answers[tid][field],
                     'normalization changed the reviewed question/premises/conventions')
        polarity = {'P holds': 'holds', 'P fails': 'refuted'}.get(verdicts[tid]['decision'])
        _require(polarity == p['gold']['decision'] == candidate['private_gold']['decision']
                 == reviewed[tid]['frozen_decision_adapted'] == reviewed[tid]['gold_decision'],
                 'gold disagrees with independently derived first polarity')
        _substantive(verdicts[tid]['derivation'])
        _require(verdicts[tid]['decoder_correspondence']['verdict'] == 'faithful to fixed P'
                 and verdicts[tid]['nl_correspondence']['verdict'] == 'equivalent to fixed P'
                 and verdicts[tid]['nl_correspondence']['repair_needed'] is False
                 and not verdicts[tid]['ambiguities'] and not verdicts[tid]['exact_repair_needs'],
                 'unresolved historical semantic correspondence')
        _require(answers[tid]['neutral_proposition'] == ctx['proposition']
                 and answers[tid]['author_gold'] == candidate['private_gold']
                 and answers[tid]['rubric'] == candidate['rubric'] == p['gold']['rubric']
                 == curation[cid]['rubric_unchanged'], 'gold/rubric input drift')
        _require(reviewed[tid]['gold_mathematical_verdict'] == 'correct and sufficient'
                 and reviewed[tid]['training_answer_assessment']['mathematical_repair_needed'] is False,
                 'unresolved author argument review')
        rubric = reviewed[tid]['rubric_review']
        _require(len(rubric) == len(p['gold']['rubric'])
                 and [c['id'] for c in rubric] == [c['id'] for c in p['gold']['rubric']]
                 and all(c['verdict'] in {'fair', 'fair with semantic grading'} and c['repair'] is None for c in rubric),
                 'rubric judgment changed or remains unresolved')
        _require(curation[cid]['opaque_review_task_id'] == tid
                 and curation[cid]['curated_gold']['decision'] == polarity
                 and p['gold']['answer'] == '\n\n'.join(curation[cid]['standalone_worked_solution']),
                 'curated worked answer or identity changed')
        original = refs[cid]; new = normalized[cid]
        _require(original['neutral_P'] == ctx['proposition'] and original['imports'] == ctx['imports']
                 and original['required_minimal_context_lean'] == helper
                 and original['neutral_P_sha256_lf'] == sealed[cid]['neutral_P_sha256_lf'] == _sha_text(ctx['proposition'])
                 and sealed[cid]['minimal_context_sha256_lf'] == _sha_text(helper)
                 and original['fixed_proof_sha256_lf'] == _sha_text(original['fixed_proof']),
                 'old proposition/reference content binding changed')
        _require(original['source_bindings'] == sealed[cid]['source_bindings'] == candidate['source_bindings'],
                 'old source bindings changed')
        historical_sources = candidate['source_bindings']
        _require(isinstance(historical_sources, list) and historical_sources
                 and d['normalized_probes']['source_bindings'] == historical_sources,
                 'normalized source bindings changed')
        for binding in historical_sources:
            _shape(binding, {'path', 'sha256_lf'}, 'historical source binding')
            path = (base.R / binding['path']).resolve()
            _require(path.is_relative_to(base.R) and binding['path'].startswith('QuantumBlockEncoding/')
                     and current_by_path.get(binding['path']) == binding['sha256_lf']
                     and text_sha(path) == binding['sha256_lf'],
                     'historical source binding differs from current source union or bytes')
        proposition = p['formal_context']['proposition']
        _require(new['neutral_P'] == proposition and new['imports'] == p['formal_context']['imports'] == ctx['imports']
                 and new['fixed_proof'] == p['gold']['reference_proof']
                 and new['fixed_proof_sha256_lf'] == _sha_text(new['fixed_proof'])
                 and new['original_fixed_proof_sha256_lf'] == _sha_text(original['fixed_proof'])
                 and new['target_proposition'] == (proposition if polarity == 'holds' else '¬ (' + proposition + ')')
                 and new['required_minimal_context_lean'] == '', 'normalized reference binding changed')
        nr = normalized_rows[cid]; tr = transports[cid]
        _require(nr['formal_context'] == p['formal_context'] and nr['question_sha256_lf'] == _sha_text(p['question'])
                 and nr['assumptions_digest'] == digest(p['assumptions'])
                 and nr['conventions_digest'] == digest(p['conventions'])
                 and nr['study_contract_hash'] == p['parent_contracts']['candidate:' + cid]
                 and tr['old_proposition_sha256_lf'] == _sha_text(ctx['proposition'])
                 and tr['new_proposition_sha256_lf'] == _sha_text(proposition)
                 and all(tr[k] is True for k in ('question_unchanged', 'assumptions_unchanged',
                                                 'conventions_unchanged', 'rubric_unchanged')),
                 'explicit old-to-new normalization contract changed')
    exposure = _rows(d['exposure_audit'], 'candidate_assessments', 'candidate_id', ids)
    _require(d['exposure_audit']['verdict']['unseen_target_mechanism_or_source_family_holdout'] == 'NOT_SUPPORTED_FOR_BASELINE'
             and all(exposure[k]['canonical_admission'] is False
                     and exposure[k]['private_gold_polarity'] == candidates[k]['private_gold']['decision'] for k in ids),
             'baseline exposure review cannot grant an unseen-mechanism holdout')
    return {'neutral_decoder_digest': digest(decoder), 'source_comparison_digest': digest(comparison),
            'answer_review_digest': digest(review), 'curation_digest': digest(curated),
            'transport_digest': digest({'policy': TRANSPORT_POLICY, 'normalization': normalization}),
            'exposure_audit_digest': digest(d['exposure_audit']),
            'review_role_identities_sha256_utf8': {k: hashlib.sha256(v.encode('utf-8')).hexdigest()
                                                 for k, v in role_ids.items()},
            'AI_not_authenticated_human_approval': True}


def check_semantics(packet, directory):
    try:
        return _check_semantics(packet, directory)
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError('malformed historical provenance') from error


class _TransportVerifier(_RecordedAuthoredVerifier):
    """Authored-only exact helper; never used for student verification."""
    def __init__(self, task, build_root, helper_context):
        _require(helper_context in ('', HELPER_CONTEXT), 'uninspected transport prelude')
        self.helper_context = helper_context
        super().__init__(task, {'assessment_root': [TRANSPORT_PROOF]}, build_root)

    def _source(self, request, nonce):
        _require(self.helper_context in ('', HELPER_CONTEXT), 'uninspected transport prelude')
        source = _RecordedAuthoredVerifier._source(self, request, nonce)
        marker = 'open scoped BigOperators\n'
        _require(source.count(marker) == 1, 'transport source-template boundary changed')
        return source.replace(marker, marker + self.helper_context + '\n', 1)


def _transport_contracts(packet, directory):
    _, docs, _ = _load_provenance(directory)
    extension = _extension(packet, directory)
    candidates = {p['candidate_id']: p for p in docs['candidates']['items']}
    contracts = []
    for p in extension:
        old = candidates[p['probe_id']]
        # Whitespace-only flattening allows the unchanged task schema; the
        # original literal term and exact helper remain explicitly committed.
        original = ' '.join(old['formal_context']['proposition'].split())
        target = '(' + original + ') ↔ (' + p['formal_context']['proposition'] + ')'
        task = challenge_task(p, 'holds', snapshot_id=packet['snapshot_id'], library_revision=packet['library_revision'])
        task['nodes'][0]['target'] = target
        task['contract_hash'] = digest({'original_formal_context': old['formal_context'],
                                       'normalized_formal_context': p['formal_context'], 'proof': TRANSPORT_PROOF})
        task['alignment_status'] = 'authored_definitional_transport_only; not_a_new_neutral_decode'
        contracts.append({'probe_id': p['probe_id'], 'task': validate_task(task), 'helper_context': _helper(old),
                          'old_proposition_sha256_lf': _sha_text(old['formal_context']['proposition']),
                          'new_proposition_sha256_lf': _sha_text(p['formal_context']['proposition'])})
    return contracts


def validate_transport_results(packet, directory, results):
    """Reconstruct every fixed transport request/source and foundational check."""
    contracts = _transport_contracts(packet, directory)
    _require(isinstance(results, list) and len(results) == 4, 'four actual transport roots required')
    expected = {c['probe_id']: c for c in contracts}; seen = set(); executions = set()
    fields = {'probe_id', 'task_hash', 'old_proposition_sha256_lf', 'new_proposition_sha256_lf',
              'submitted_status', 'submission_evidence', 'replays'}
    for row in results:
        _shape(row, fields, 'transport result')
        key = row['probe_id']; _require(key in expected and key not in seen, 'duplicate or unknown transport root')
        seen.add(key); contract = expected[key]; task = contract['task']
        _require(row['task_hash'] == digest(task)
                 and all(row[k] == contract[k] for k in ('old_proposition_sha256_lf', 'new_proposition_sha256_lf'))
                 and row['submitted_status'] == 'verified' and isinstance(row['replays'], list)
                 and len(row['replays']) == 1, 'transport target/proof replay binding differs')
        replay = row['replays'][0]; reply = row['submission_evidence']
        _shape(replay, REPLAY_FIELDS, 'transport replay'); _shape(reply, EVIDENCE_FIELDS, 'transport evidence')
        _require(isinstance(replay['execution_id'], str) and re.fullmatch('[0-9a-f]{32}', replay['execution_id'])
                 and replay['execution_id'] not in executions, 'distinct actual transport execution required')
        executions.add(replay['execution_id'])
        _require(replay['status'] == 'verified' and replay['final_replay'] is False
                 and type(replay['exit_code']) is int and replay['exit_code'] == 0
                 and replay['failure'] is None and replay['node_id'] == 'assessment_root'
                 and isinstance(replay['axioms'], list) and all(isinstance(x, str) for x in replay['axioms'])
                 and not (set(replay['axioms']) - APPROVED_AXIOMS)
                 and replay['runtime_checkout_commit'] == packet['library_revision']
                 and replay['proof_inputs_sha256'] == packet['proof_inputs_sha256']
                 and 'version ' + packet['lean_toolchain'].split(':v')[-1] + ',' in replay['actual_lean_version']
                 and replay['execution_class'] == 'trusted_local_authored_reference' and replay['isolated'] is False,
                 'transport runtime/axiom/root scope differs')
        _require(type(replay['elapsed_seconds']) in (int, float) and math.isfinite(replay['elapsed_seconds'])
                 and replay['elapsed_seconds'] >= 0, 'bounded typed transport timing required')
        meta = replay['request_metadata']
        _shape(meta, {'request_id', 'timeout_seconds', 'deadline_monotonic'}, 'transport request metadata')
        _require(isinstance(meta['request_id'], str) and meta['request_id'].isdigit()
                 and all(type(meta[k]) in (int, float) and math.isfinite(meta[k]) and meta[k] > 0
                         for k in ('timeout_seconds', 'deadline_monotonic'))
                 and meta['timeout_seconds'] <= REFERENCE_PROFILE['check_seconds'], 'bounded transport request required')
        request = {'schema_version': 'qcb.obligation_check.v1', 'task_hash': digest(task), 'node_id': 'assessment_root',
                   'imports': task['imports'], 'target': task['nodes'][0]['target'], 'universe_parameters': [],
                   'library_revision': packet['library_revision'], 'proof': TRANSPORT_PROOF,
                   'dependency_order': [], 'dependencies': {}, 'final_replay': False, **meta}
        source = _TransportVerifier._source(SimpleNamespace(task=task, nodes={}, allowlist={},
                                            helper_context=contract['helper_context']), request, replay['execution_id'])
        authored = base.B / 'src/qcb_authored_session.py'
        pipeline = authored.read_bytes().replace(b'\r\n', b'\n')
        _require(replay['request_hash'] == digest(request)
                 and replay['proof_sha256'] == hashlib.sha256(TRANSPORT_PROOF.encode()).hexdigest()
                 and replay['source_sha256'] == hashlib.sha256(source.encode()).hexdigest()
                 and replay['pipeline_source_sha256_lf'] == text_sha(authored)
                 and replay['pipeline_sha256'] in {hashlib.sha256(pipeline).hexdigest(),
                                                    hashlib.sha256(pipeline.replace(b'\n', b'\r\n')).hexdigest()},
                 'transport exact proof/request/source binding differs')
        _require(all(reply[k] == replay[k] for k in ('request_hash', 'proof_sha256', 'execution_id', 'status',
                                                    'axioms', 'execution_class', 'isolated'))
                 and reply['kernel_checked'] is True and reply['failure_class'] is None,
                 'transport summary differs from its actual replay')
    return {'transport_roots': len(seen), 'execution_ids': sorted(executions)}


async def replay_references(directory, build_root, *, progress=None):
    from qcb_assessment_v3 import load_private_bank, source_identity, _committed
    packet, seal = load_private_bank(directory, require_qualified=False)
    semantics = check_semantics(packet, directory)
    probes = _extension(packet, directory)
    _require(len({tuple(p['formal_context']['imports']) for p in probes}) == 1,
             'the frozen fourteen-check profile requires one extension import group')
    identity = source_identity()
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=base.R, text=True).strip()
    _committed(identity, commit)
    _require(COUNTS['total'] <= REFERENCE_PROFILE['max_root_replays'], 'authored replay ceiling exceeded')
    started = monotonic(); rows = []; raw = []; transports = []

    def limits():
        remaining = REFERENCE_PROFILE['batch_wall_seconds'] - (monotonic() - started)
        if remaining <= 0:
            raise TimeoutError('bounded extension authored batch exhausted')
        return SessionLimits(wall_seconds=min(REFERENCE_PROFILE['session_wall_seconds'], remaining),
                             check_seconds=REFERENCE_PROFILE['check_seconds'])

    def emit(record):
        raw.append(deepcopy(record))
        if progress is not None:
            progress(deepcopy(record))

    for index, probe in enumerate(probes):
        task = challenge_task(probe, probe['gold']['decision'], snapshot_id=packet['snapshot_id'], library_revision=packet['library_revision'])
        proof = probe['gold']['reference_proof']; negatives = index == 0
        verifier = _RecordedAuthoredVerifier(task, {'assessment_root': [proof] +
                    (['by exact True.intro', 'by sorry'] if negatives else [])}, build_root)
        session = ProofSession(task, verifier, mode='root_only', limits=limits())
        submitted = await session.act({'kind': 'submit', 'state_id': session.state_id, 'node_id': 'assessment_root', 'proof': proof})
        emit({'phase': 'submission', 'probe_id': probe['probe_id'], 'reply': submitted, 'replays': verifier.replays})
        finished = await session.act({'kind': 'finish', 'state_id': session.state_id})
        emit({'phase': 'fresh_final', 'probe_id': probe['probe_id'], 'reply': finished, 'replays': verifier.replays})
        _require(session.report()['formal_root_checked'], 'fixed extension root failed; preserve private progress')
        row = {'probe_id': probe['probe_id'], 'probe_digest': digest(probe), 'task_hash': digest(task),
               'formal_target_sha256': digest(task['nodes'][0]['target']), 'gold_polarity': probe['gold']['decision'],
               'submitted_status': submitted['status'], 'finish_status': finished['status'],
               'submission_evidence': _compact_evidence(submitted.get('evidence')),
               'final_evidence': _compact_evidence(finished.get('final_replay')),
               'formal_root_checked': True, 'negative_controls': []}
        if negatives:
            for label, bad in [('wrong_target', 'by exact True.intro'), ('sorry_axiom', 'by sorry')]:
                negative = ProofSession(task, verifier, mode='root_only', limits=limits())
                reply = await negative.act({'kind': 'submit', 'state_id': negative.state_id, 'node_id': 'assessment_root', 'proof': bad})
                row['negative_controls'].append({'kind': label, 'status': reply['status'], 'evidence': _compact_evidence(reply.get('evidence'))})
                emit({'phase': label, 'probe_id': probe['probe_id'], 'reply': reply, 'replays': verifier.replays})
                _require(reply['status'] == 'compile_error', 'environment failure is not a rejected proof control')
        row['replays'] = deepcopy(verifier.replays); rows.append(row)
    validate_reference_results({**packet, 'probes': probes}, rows)
    for contract in _transport_contracts(packet, directory):
        task = contract['task']; verifier = _TransportVerifier(task, build_root, contract['helper_context'])
        session = ProofSession(task, verifier, mode='root_only', limits=limits())
        reply = await session.act({'kind': 'submit', 'state_id': session.state_id,
                                   'node_id': 'assessment_root', 'proof': TRANSPORT_PROOF})
        emit({'phase': 'definitional_transport', 'probe_id': contract['probe_id'], 'reply': reply, 'replays': verifier.replays})
        transports.append({k: contract[k] for k in ('probe_id', 'old_proposition_sha256_lf', 'new_proposition_sha256_lf')}
                          | {'task_hash': digest(task), 'submitted_status': reply['status'],
                             'submission_evidence': _compact_evidence(reply.get('evidence')), 'replays': deepcopy(verifier.replays)})
    checked = validate_transport_results(packet, directory, transports)
    ordinary_ids = {r['execution_id'] for row in rows for r in row['replays']}
    _require(not ordinary_ids.intersection(checked['execution_ids']) and len(ordinary_ids) + len(checked['execution_ids']) == 14,
             'fourteen distinct authored executions required')
    _require(source_identity() == identity and check_semantics(packet, directory) == semantics,
             'extension source or semantic provenance changed during replay')
    _committed(identity, commit)
    return {'schema_version': 'qcb.private_assessment_references.v3', 'seal_digest': digest(seal),
            'cohort_digest': digest(packet), 'source_commit': commit, 'tested_code_commit': commit,
            'pipeline_source_hashes_lf': identity, 'semantic_review': semantics,
            'profile': deepcopy(REFERENCE_PROFILE), 'passed': True, 'results': rows,
            'transport_results': transports, 'new_reference_checks': deepcopy(COUNTS),
            'elapsed_seconds': monotonic() - started, 'execution_class': 'trusted_local_authored_reference',
            'isolated': False, 'model_calls': 0, 'model_performance_measured': False}, raw
