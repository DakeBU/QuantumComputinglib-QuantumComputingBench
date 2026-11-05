"""Synthetic CPU-only controls; no private artifacts, Lean or model evidence."""
from copy import deepcopy
import asyncio
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from uuid import uuid4

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / 'src'))
import qcb_assessment_v3_reference as ref
from qcb_core import digest
from qcb_integrity import text_sha
from qcb_learning_reference import EVIDENCE_FIELDS
from test_assessment_protocol import cohort

spec = importlib.util.spec_from_file_location('assessment_v3_cli_fixture', B / 'scripts/assessment_v3.py')
cli = importlib.util.module_from_spec(spec); spec.loader.exec_module(cli)


def fixture():
    extension = cohort()['probes']
    old = {'probes': [{'probe_id': str(uuid4())} for _ in range(14)]}
    for p in extension:
        p['cluster_id'] = 'promise_register_protocols'
        p['parent_core_ids'] = ['candidate:' + p['probe_id']]
        p['parent_contracts'] = {p['parent_core_ids'][0]: digest(p['probe_id'])}
        p['gold']['answer'] = 'SOFTWARE FIXTURE: an invented worked answer.'
    source_bindings = [{'path': 'QuantumBlockEncoding/SyntheticFixture.lean', 'sha256_lf': 'd' * 64}]
    packet = {'probes': old['probes'] + extension, 'snapshot_id': 'synthetic-snapshot', 'source_bindings': source_bindings,
              'library_revision': 'a' * 40, 'proof_inputs_sha256': 'b' * 64,
              'lean_toolchain': 'leanprover/lean4:v4.29.1'}
    tids = {p['probe_id']: str(uuid4()) for p in extension}
    mappings = [{'probe_id': k, 'candidate_id': k, 'review_task_id': v} for k, v in tids.items()]
    files = {k: {'path': 'evidence/' + k + '.json', 'sha256_raw': ''} for k in ref.ROLES}
    provenance = {'schema_version': 'qcb.assessment_provenance.v3', 'files': files, 'mappings': mappings,
                  'normalization_transport': deepcopy(ref.TRANSPORT_POLICY), 'author_gold_seen_by_backend': True}
    docs = {}; hashes = {}
    def add(role, value):
        docs[role] = value
        hashes[role] = hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()
        files[role]['sha256_raw'] = hashes[role]
    add('candidates', {'author_identity': 'fixture-author', 'items': [
        {'candidate_id': p['probe_id'], **{k: deepcopy(p[k]) for k in ('question', 'assumptions', 'conventions', 'rubric') if k in p},
         'rubric': deepcopy(p['gold']['rubric']), 'private_gold': {'decision': p['gold']['decision']},
         'formal_context': {**p['formal_context'], 'required_minimal_context_lean': ''}, 'source_bindings': source_bindings}
        for p in extension]})
    add('neutral_mapping', [{'task_id': r['review_task_id'], 'author_candidate_id': r['candidate_id']} for r in mappings])
    add('neutral_input', {'schema_version': 'fixture', 'status': 'fixture', 'standard_definitional_conventions': [],
        'literal_definition_excerpts': '', 'definition_evidence_scope': 'fixture',
        'tasks': [{'task_id': tids[p['probe_id']], 'imports': p['formal_context']['imports'], 'local_context': '',
                   'proposition': p['formal_context']['proposition']} for p in extension]})
    add('neutral_decoder', {'reviewer_identity': 'fixture-decoder', 'input_bytes_sha256': hashes['neutral_input'],
        'items': [{'task_id': tid, 'decoded_mathematics': 'SOFTWARE FIXTURE reviewed text. ' * 3,
                   'semantic_slots': {'one': 'SOFTWARE FIXTURE', 'two': 'semantics only', 'three': 'no actual theorem result'}} for tid in tids.values()]})
    add('source_input', {'schema_version': 'fixture', 'neutral_input': docs['neutral_input'], 'neutral_decoder': docs['neutral_decoder'],
        'neutral_input_raw_sha256': hashes['neutral_input'], 'decoder_raw_sha256': hashes['neutral_decoder'],
        'statement_elaboration': {}, 'boundary': 'no gold',
        'questions': [{'task_id': tids[p['probe_id']], **{k: p[k] for k in ('question', 'assumptions', 'conventions')}} for p in extension]})
    add('source_comparison', {'reviewer_identity': 'fixture-source', 'input_binding': {'raw_bytes_sha256': hashes['source_input']},
        'review_scope': {'no_gold_seen_before_first_verdict': True}, 'items': [
        {'task_id': tids[p['probe_id']], 'decision': 'P holds' if p['gold']['decision'] == 'holds' else 'P fails',
         'derivation': 'SOFTWARE FIXTURE manual derivation placeholder. ' * 3,
         'decoder_correspondence': {'verdict': 'faithful to fixed P'},
         'nl_correspondence': {'verdict': 'equivalent to fixed P', 'repair_needed': False}, 'ambiguities': [], 'exact_repair_needs': []}
        for p in extension]})
    add('answer_input', {'earlier_first_source_verdict_sha256_raw': hashes['source_comparison'],
        'earlier_source_verdict': docs['source_comparison'], 'decision_encoding_adapter_only': {'P holds': 'holds', 'P fails': 'refuted'},
        'items': [{'task_id': tids[p['probe_id']], **{k: p[k] for k in ('question', 'assumptions', 'conventions')},
                   'neutral_proposition': p['formal_context']['proposition'], 'author_gold': {'decision': p['gold']['decision']},
                   'rubric': p['gold']['rubric']} for p in extension]})
    add('answer_review', {'reviewer_identity': 'fixture-source', 'input_binding': {'raw_bytes_sha256': hashes['answer_input'],
        'frozen_first_source_verdict_raw_sha256': hashes['source_comparison']}, 'scope': {'gold_seen_in_this_phase': True, 'first_verdict_preserved': True},
        'overall': {'decisions_match_frozen_verdict': True, 'mandatory_rubric_repairs': []},
        'items': [{'task_id': tids[p['probe_id']], 'frozen_decision_adapted': p['gold']['decision'], 'gold_decision': p['gold']['decision'],
                   'gold_mathematical_verdict': 'correct and sufficient', 'training_answer_assessment': {'mathematical_repair_needed': False},
                   'rubric_review': [{'id': r['id'], 'verdict': 'fair', 'repair': None} for r in p['gold']['rubric']]} for p in extension]})
    add('statement_seal', {'candidate_packet_sha256_raw': hashes['candidates'], 'neutral_input_sha256_raw': hashes['neutral_input'],
        'items': [{'candidate_id': p['probe_id'], 'neutral_P_sha256_lf': ref._sha_text(p['formal_context']['proposition']),
                   'minimal_context_sha256_lf': ref._sha_text(''), 'source_bindings': source_bindings} for p in extension]})
    add('authored_references', {'candidate_packet_sha256_raw': hashes['candidates'], 'statement_seal_sha256_raw': hashes['statement_seal'],
        'items': [{'candidate_id': p['probe_id'], 'neutral_P': p['formal_context']['proposition'],
                   'imports': p['formal_context']['imports'], 'required_minimal_context_lean': '',
                   'neutral_P_sha256_lf': ref._sha_text(p['formal_context']['proposition']),
                   'fixed_proof': p['gold']['reference_proof'], 'fixed_proof_sha256_lf': ref._sha_text(p['gold']['reference_proof']),
                   'source_bindings': source_bindings} for p in extension]})
    add('prior_reference_replay', {'candidate_packet_sha256_raw': hashes['candidates'], 'statement_seal_sha256_raw': hashes['statement_seal'],
        'authored_reference_sha256_raw': hashes['authored_references'], 'passed': True, 'model_calls': 0})
    add('curation', {'candidate_packet_sha256_raw': hashes['candidates'], 'answer_review_sha256_raw': hashes['answer_review'],
        'source_comparison_sha256_raw': hashes['source_comparison'], 'reference_replay_sha256_raw': hashes['prior_reference_replay'],
        'original_candidate_packet_unchanged': True, 'questions_P_assumptions_contexts_unchanged': True, 'rubric_mathematical_repairs': 0,
        'worked_expansions_root_reviewed': True, 'items': [{'author_candidate_id': p['probe_id'], 'opaque_review_task_id': tids[p['probe_id']],
        'curated_gold': {'decision': p['gold']['decision']}, 'rubric_unchanged': p['gold']['rubric'],
        'standalone_worked_solution': [p['gold']['answer']]} for p in extension]})
    add('normalized_references', {'items': [{'candidate_id': p['probe_id'], 'neutral_P': p['formal_context']['proposition'],
        'imports': p['formal_context']['imports'], 'fixed_proof': p['gold']['reference_proof'],
        'original_fixed_proof_sha256_lf': ref._sha_text(p['gold']['reference_proof']), 'fixed_proof_sha256_lf': ref._sha_text(p['gold']['reference_proof']),
        'target_proposition': p['formal_context']['proposition'] if p['gold']['decision'] == 'holds' else '¬ (' + p['formal_context']['proposition'] + ')',
        'required_minimal_context_lean': ''} for p in extension]})
    input_roles = ['candidates', 'curation', 'authored_references', 'statement_seal', 'prior_reference_replay',
                   'neutral_input', 'neutral_decoder', 'source_comparison', 'answer_review']
    input_bindings = [{'path': files[k]['path'], 'sha256_raw': hashes[k]} for k in input_roles]
    add('normalization_seal', {'input_bindings': input_bindings, 'transport': [{'candidate_id': p['probe_id'],
        'old_proposition_sha256_lf': ref._sha_text(p['formal_context']['proposition']), 'new_proposition_sha256_lf': ref._sha_text(p['formal_context']['proposition']),
        **{k: True for k in ('question_unchanged', 'assumptions_unchanged', 'conventions_unchanged', 'rubric_unchanged')}} for p in extension],
        'items': [{'probe_id': p['probe_id'], 'formal_context': p['formal_context'], 'question_sha256_lf': ref._sha_text(p['question']),
                   'assumptions_digest': digest(p['assumptions']), 'conventions_digest': digest(p['conventions']),
                   'study_contract_hash': p['parent_contracts']['candidate:' + p['probe_id']]} for p in extension]})
    add('normalized_probes', {'probes': extension, 'input_bindings': input_bindings, 'source_bindings': source_bindings,
                             'normalization_transport': docs['normalization_seal']['transport']})
    add('exposure_audit', {'auditor_identity': 'fixture-exposure', 'candidate_assessments': [
        {'candidate_id': p['probe_id'], 'canonical_admission': False, 'private_gold_polarity': p['gold']['decision']} for p in extension],
        'verdict': {'unseen_target_mechanism_or_source_family_holdout': 'NOT_SUPPORTED_FOR_BASELINE'}})
    return packet, old, provenance, docs, hashes


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.packet, self.old, self.provenance, self.docs, self.hashes = fixture()

    def semantics(self):
        with patch.object(ref, '_load_provenance', return_value=(self.provenance, self.docs, self.hashes)), \
             patch.object(ref, '_extension', return_value=self.packet['probes'][14:]), \
             patch.object(ref, 'text_sha', return_value='d' * 64):
            return ref.check_semantics(self.packet, 'synthetic-unused')

    def test_complete_chain_returns_only_aggregate_hashes_and_role_hashes(self):
        result = self.semantics()
        self.assertEqual(set(result['review_role_identities_sha256_utf8']), {'author', 'decoder', 'source_reviewer', 'exposure_reviewer'})
        for value in result['review_role_identities_sha256_utf8'].values():
            self.assertRegex(value, '^[0-9a-f]{64}$')
        self.assertNotIn('SECRET_', json.dumps(result))
        self.assertNotIn('fixture-source', json.dumps(result))

    def test_stale_missing_and_reanchored_reviews_fail(self):
        original = deepcopy(self.docs)
        changes = [lambda d: d['neutral_decoder'].update(input_bytes_sha256='0' * 64),
                   lambda d: d['source_comparison']['review_scope'].update(no_gold_seen_before_first_verdict=False),
                   lambda d: d['answer_input'].update(earlier_first_source_verdict_sha256_raw='0' * 64),
                   lambda d: d['answer_review']['input_binding'].pop('frozen_first_source_verdict_raw_sha256'),
                   lambda d: d['curation'].update(rubric_mathematical_repairs=1),
                   lambda d: d['normalization_seal']['transport'][0].update(question_unchanged=False),
                   lambda d: d['normalization_seal']['input_bindings'].pop(),
                   lambda d: d['exposure_audit'].update(auditor_identity='fixture-author'),
                   lambda d: d['neutral_input'].update(gold='LEAK')]
        for change in changes:
            self.docs = deepcopy(original); change(self.docs)
            with self.subTest(change=change), self.assertRaises((ValueError, KeyError)):
                self.semantics()

    def test_normalized_question_or_rubric_cannot_be_silently_replaced(self):
        self.packet['probes'][14]['question'] = 'changed question'
        with self.assertRaises(ValueError): self.semantics()

    def test_agreeing_stale_historical_bindings_cannot_replace_current_source_union(self):
        for role in ('candidates', 'authored_references', 'statement_seal'):
            for row in self.docs[role]['items']:
                row['source_bindings'] = [{'path': 'QuantumBlockEncoding/SyntheticFixture.lean', 'sha256_lf': 'e' * 64}]
        self.docs['normalized_probes']['source_bindings'] = deepcopy(self.docs['candidates']['items'][0]['source_bindings'])
        with self.assertRaisesRegex(ValueError, 'current source union'):
            self.semantics()

    def test_current_source_bytes_must_match_even_when_every_claimed_binding_agrees(self):
        with patch.object(ref, '_load_provenance', return_value=(self.provenance, self.docs, self.hashes)), \
             patch.object(ref, '_extension', return_value=self.packet['probes'][14:]), \
             patch.object(ref, 'text_sha', return_value='e' * 64):
            with self.assertRaisesRegex(ValueError, 'current source union or bytes'):
                ref.check_semantics(self.packet, 'synthetic-unused')

    def test_frozen_base_mutation_rejected(self):
        with patch.object(ref, 'read_json', return_value=self.old), \
             patch.object(ref.base, 'load_seal', return_value={'cohort_digest': digest(self.old)}):
            self.assertEqual(len(ref._extension(self.packet, 'unused')), 4)
            self.packet['probes'][0] = {'probe_id': 'changed'}
            with self.assertRaisesRegex(ValueError, 'frozen base'):
                ref._extension(self.packet, 'unused')

    def test_exact_helper_only_no_arbitrary_commands(self):
        with self.assertRaisesRegex(ValueError, 'exact reviewed'):
            ref._helper({'candidate_id': ref.HELPER_CANDIDATE, 'formal_context': {'required_minimal_context_lean': ref.HELPER_CONTEXT + '\n#eval IO.println 1'}})

    def test_raw_file_and_missing_role_rejection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'provenance.json').write_text(json.dumps({**self.provenance, 'files': {}}))
            with self.assertRaisesRegex(ValueError, 'exact copied'):
                ref._load_provenance(root)
            for role, entry in self.provenance['files'].items():
                path = root / entry['path']; path.parent.mkdir(exist_ok=True)
                path.write_text(json.dumps(self.docs[role], sort_keys=True))
            (root / 'provenance.json').write_text(json.dumps(self.provenance))
            self.assertEqual(set(ref._load_provenance(root)[1]), ref.ROLES)
            (root / self.provenance['files']['source_comparison']['path']).write_text('{}')
            with self.assertRaisesRegex(ValueError, 'raw provenance'):
                ref._load_provenance(root)


def transport_fixture():
    packet, _, _, _, _ = fixture()
    contracts, rows = [], []
    for i, probe in enumerate(packet['probes'][14:]):
        task = ref.challenge_task(probe, 'holds', snapshot_id=packet['snapshot_id'], library_revision=packet['library_revision'])
        task['nodes'][0]['target'] = '(True) ↔ (True)'
        contract = {'probe_id': probe['probe_id'], 'task': task, 'helper_context': '',
                    'old_proposition_sha256_lf': ref._sha_text('True'), 'new_proposition_sha256_lf': ref._sha_text('True')}
        contracts.append(contract)
        meta = {'request_id': '1', 'timeout_seconds': 120, 'deadline_monotonic': 12345.0}
        request = {'schema_version': 'qcb.obligation_check.v1', 'task_hash': digest(task), 'node_id': 'assessment_root',
            'imports': task['imports'], 'target': task['nodes'][0]['target'], 'universe_parameters': [],
            'library_revision': packet['library_revision'], 'proof': ref.TRANSPORT_PROOF,
            'dependency_order': [], 'dependencies': {}, 'final_replay': False, **meta}
        nonce = f'{i+1:032x}'
        source = ref._TransportVerifier._source(SimpleNamespace(task=task, nodes={}, allowlist={}, helper_context=''), request, nonce)
        authored = B / 'src/qcb_authored_session.py'
        replay = {'node_id': 'assessment_root', 'request_hash': digest(request), 'execution_id': nonce,
            'final_replay': False, 'proof_sha256': hashlib.sha256(ref.TRANSPORT_PROOF.encode()).hexdigest(),
            'source_sha256': hashlib.sha256(source.encode()).hexdigest(), 'runtime_checkout_commit': packet['library_revision'],
            'proof_inputs_sha256': packet['proof_inputs_sha256'], 'actual_lean_version': 'Lean (version 4.29.1, synthetic)',
            'pipeline_sha256': hashlib.sha256(authored.read_bytes()).hexdigest(), 'pipeline_source_sha256_lf': text_sha(authored),
            'exit_code': 0, 'status': 'verified', 'axioms': [], 'failure': None, 'elapsed_seconds': .1,
            'execution_class': 'trusted_local_authored_reference', 'isolated': False, 'request_metadata': meta}
        reply = {k: deepcopy(replay[k]) for k in EVIDENCE_FIELDS if k in replay}
        reply.update(kernel_checked=True, failure_class=None)
        rows.append({k: contract[k] for k in ('probe_id', 'old_proposition_sha256_lf', 'new_proposition_sha256_lf')}
                    | {'task_hash': digest(task), 'submitted_status': 'verified', 'submission_evidence': reply, 'replays': [replay]})
    return packet, contracts, rows


class TransportTests(unittest.TestCase):
    def test_replay_cannot_start_before_committed_source_gate(self):
        import qcb_assessment_v3 as v3
        packet, _, _, _, _ = fixture()
        with patch.object(v3, 'load_private_bank', return_value=(packet, {})), \
             patch.object(v3, 'source_identity', return_value={'fixture': '0' * 64}), \
             patch.object(v3, '_committed', side_effect=ValueError('commit gate')), \
             patch.object(ref, 'check_semantics', return_value={}), \
             patch.object(ref, '_extension', return_value=packet['probes'][14:]), \
             patch.object(ref.subprocess, 'check_output', return_value='a' * 40), \
             patch.object(ref, '_RecordedAuthoredVerifier', side_effect=AssertionError('must not execute')):
            with self.assertRaisesRegex(ValueError, 'commit gate'):
                asyncio.run(ref.replay_references('unused', 'unused'))

    def test_engineered_receipt_and_adversarial_binding_failures(self):
        packet, contracts, rows = transport_fixture()
        with patch.object(ref, '_transport_contracts', return_value=contracts):
            self.assertEqual(ref.validate_transport_results(packet, 'unused', rows)['transport_roots'], 4)
            for field, value in [('source_sha256', '0' * 64), ('proof_sha256', '0' * 64), ('request_hash', '0' * 64),
                                 ('axioms', ['sorryAx']), ('runtime_checkout_commit', '0' * 40), ('final_replay', True), ('exit_code', True)]:
                changed = deepcopy(rows); changed[0]['replays'][0][field] = value
                with self.subTest(field=field), self.assertRaises(ValueError):
                    ref.validate_transport_results(packet, 'unused', changed)
            changed = deepcopy(rows); changed[1] = deepcopy(changed[0])
            with self.assertRaises(ValueError): ref.validate_transport_results(packet, 'unused', changed)


class CliTests(unittest.TestCase):
    def test_prepare_keeps_profile_metadata_in_private_grader_and_projects_leaf_messages(self):
        external = B.parents[1].parent / 'synthetic-v3-never-created'
        with patch.object(cli, 'load_private_bank', return_value=(cohort(), {})), \
             patch.object(cli, '_write') as writes, redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(['prepare', '--bank', str(external / 'bank'),
                '--student', str(external / 'student/tasks.json'), '--controller', str(external / 'grader/controller.json'),
                '--split', 'test_public', '--training-profile', 'promise_register_family_holdout']), 0)
        student = writes.call_args_list[0].args[1]
        controller = writes.call_args_list[1]
        self.assertEqual(controller.args[0].parent, (external / 'grader').resolve())
        _, declared = cli._unwrap_controller(controller.args[1])
        self.assertEqual(declared, 'promise_register_family_holdout')
        self.assertFalse(controller.args[1]['study_design']['actual_model_exposure_authenticated'])
        for row in student:
            self.assertEqual(set(row), {'task_id', 'question', 'assumptions', 'conventions', 'response_format'})
        for call in writes.call_args_list[2:]:
            path, value = call.args
            self.assertIn(path.name, {'task.json', 'messages.json'})
            self.assertNotIn('training_profile', json.dumps(value))
            self.assertNotIn('SECRET_', json.dumps(value))

    def test_unknown_profile_is_not_fabricated_and_envelope_does_not_authenticate_exposure(self):
        with self.assertRaises(ValueError): cli._export_profile('not-a-profile')
        controller = {'run_id': 'fixture', 'controller_digest': '0' * 64}
        record = cli._controller_envelope(controller, 'promise_register_family_holdout')
        self.assertFalse(record['study_design']['actual_model_exposure_authenticated'])
        self.assertEqual(record['common_controller']['controller_digest'], controller['controller_digest'])

    def test_existing_first_answer_envelope_rejects_profile_change_even_with_rehashed_controller(self):
        packet = cohort()
        with tempfile.TemporaryDirectory() as directory, \
             patch.object(cli, 'load_private_bank', return_value=(packet, {})), \
             patch.object(cli, 'protocol_identity', return_value={}), \
             redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            root = Path(directory)
            student = root / 'student/tasks.json'; controller = root / 'grader/controller.json'
            locked = root / 'grader/first.json'; responses = root / 'grader/responses.json'
            common = ['--bank', str(root / 'bank'), '--student', str(student), '--controller', str(controller)]
            self.assertEqual(cli.main(['prepare', *common, '--split', 'test_public', '--training-profile', 'baseline']), 0)
            prepared = json.loads(controller.read_text())
            aliases = prepared['common_controller']['assignments']
            responses.write_text(json.dumps([{'task_id': a['task_id'], 'status': 'answered',
                'answer': {'decision': 'holds', 'explanation': 'SOFTWARE FIXTURE: an invented answer.'}} for a in aliases]))
            self.assertEqual(cli.main(['freeze', *common, '--responses', str(responses), '--output', str(locked)]), 0)
            first = json.loads(locked.read_text())
            self.assertEqual(first['controller_digest'], prepared['controller_digest'])
            score = root / 'grader/baseline-score.json'
            self.assertEqual(cli.main(['score', *common, '--locked', str(locked), '--output', str(score),
                                      '--evidence-kind', 'synthetic_fixture']), 0)
            result = json.loads(score.read_text())
            self.assertEqual(result['v3_lock_digest'], first['lock_digest'])
            self.assertEqual(result['declared_training_profile'], 'baseline')
            prepared['study_design']['training_profile'] = 'promise_register_family_holdout'
            prepared['controller_digest'] = digest({k: v for k, v in prepared.items() if k != 'controller_digest'})
            controller.write_text(json.dumps(prepared))
            refused = root / 'grader/MUST-NOT-EXIST-score.json'
            self.assertEqual(cli.main(['score', *common, '--locked', str(locked), '--output', str(refused),
                                      '--evidence-kind', 'synthetic_fixture']), 1)
            self.assertFalse(refused.exists())
            self.assertEqual(json.loads(locked.read_text()), first)

    def test_rubric_reviews_stay_bound_to_common_lock_with_v3_envelopes(self):
        packet = cohort()
        from qcb_assessment_protocol import prepare_evaluation, freeze_first_answers
        student, common = prepare_evaluation(packet, split='test_public')
        controller = cli._controller_envelope(common, 'baseline')
        responses = [{'task_id': r['task_id'], 'status': 'answered',
                      'answer': {'decision': 'holds', 'explanation': 'SOFTWARE FIXTURE only.'}} for r in student]
        common_lock = freeze_first_answers(packet, student, common, responses)
        first = cli._first_answer_envelope(common_lock, controller)
        returned = cli._unwrap_first_answers(first, controller)
        template = cli.review_template(packet, student, common, returned)
        self.assertTrue(all(r['lock_digest'] == common_lock['lock_digest'] for r in template))
        first['common_lock']['responses'][0]['answer']['explanation'] = 'replacement'
        with self.assertRaises(ValueError): cli._unwrap_first_answers(first, controller)

    def test_progress_collision_and_nested_reference_outputs_rejected_before_replay(self):
        external = B.parents[1].parent / 'synthetic-never-created'
        bank = external / 'bank'
        cases = [(bank / 'raw.json.progress.jsonl', bank / 'raw.json'),
                 (bank / 'receipt', bank / 'receipt/raw.json'),
                 (bank / 'raw.json/receipt.json', bank / 'raw.json')]
        with patch.object(cli, 'load_private_bank', side_effect=AssertionError('must not load')), \
             patch.object(ref, 'replay_references', side_effect=AssertionError('must not execute')) as replay, \
             redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
            for receipt, raw in cases:
                with self.subTest(receipt=receipt, raw=raw):
                    self.assertEqual(cli.main(['check-references', '--bank', str(bank), '--build-root', str(external / 'build'),
                        '--trusted-local-reference', '--output', str(receipt), '--raw-output', str(raw)]), 1)
            replay.assert_not_called()

    def test_reference_output_leak_rejected_before_replay_or_loader(self):
        external = B.parents[1].parent / 'synthetic-never-created'
        with patch.object(cli, 'load_private_bank', side_effect=AssertionError('must not load')), \
             patch.object(ref, 'replay_references', side_effect=AssertionError('must not execute')), \
             redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(['check-references', '--bank', str(external / 'bank'),
                '--build-root', str(external / 'build'), '--trusted-local-reference',
                '--output', str(external / 'bank/receipt.json'), '--raw-output', str(external / 'student/raw.json')]), 1)


if __name__ == '__main__':
    unittest.main()
