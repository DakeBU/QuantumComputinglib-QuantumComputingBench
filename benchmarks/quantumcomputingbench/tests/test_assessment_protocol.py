"""Adversarial CPU controls for the private assessment scoring boundary.

All propositions, answers and reviews below are invented software fixtures.
No live registry, model, Lean, network or domain-understanding result is used.
"""
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / 'src'))
from qcb_core import digest
from qcb_assessment_protocol import (
    prepare_evaluation, freeze_first_answers, review_template, grade_assessment, assessment_groups,
    model_messages, model_answer_row,
)


def cohort():
    probes = []
    for pair_number in range(2):
        pair_id = str(uuid4())
        for decision in ('holds', 'refuted'):
            probes.append({'probe_id': str(uuid4()), 'pair_id': pair_id,
                'cluster_id': 'mechanism-' + str(pair_number), 'parent_core_ids': ['parent-' + str(pair_number)],
                'parent_contracts': {'parent-' + str(pair_number): digest(pair_number)},
                'canonical_relation': 'diagnostic_contract_candidate', 'split': 'test_public',
                'question': 'SOFTWARE FIXTURE: assess a displayed mathematical proposition.',
                'assumptions': ['SOFTWARE FIXTURE only'], 'conventions': ['Exact arithmetic.'],
                'formal_context': {'imports': ['Mathlib'], 'proposition': 'True'},
                'gold': {'decision': decision, 'reference_proof': 'SECRET_PROOF', 'answer': 'SECRET_ANSWER',
                         'rubric': [{'id': 'argument', 'criterion': 'SECRET_RUBRIC: valid argument.', 'weight': 3},
                                    {'id': 'boundary', 'criterion': 'Preserve assumptions and boundary.', 'weight': 1}]},
                'source_nodes': ['SECRET_SOURCE_' + str(pair_number)], 'reasoning_kind': 'assumption_diagnosis',
                'difficulty': {'band': 'D2', 'rationale': 'Synthetic protocol test.',
                               'status': 'provisional_author_mathematical_assessment', 'measured_model_difficulty': None},
                'author_identity': 'fixture-author', 'formal_coverage': 'decision_polarity_only'})
    return {'probes': probes, 'operator_private_metadata': 'SECRET_METADATA'}


class AssessmentProtocolTests(unittest.TestCase):
    def setUp(self):
        self.packet = cohort()
        self.student, self.controller = prepare_evaluation(self.packet, split='test_public')
        self.index = {p['probe_id']: p for p in self.packet['probes']}
        self.by_alias = {a['task_id']: self.index[a['probe_id']] for a in self.controller['assignments']}

    def responses(self, *, always=None):
        return [{'task_id': row['task_id'], 'status': 'answered',
                 'answer': {'decision': always or self.by_alias[row['task_id']]['gold']['decision'],
                            'explanation': 'NONSENSE: every linear map is unitary and every vector has unit norm.'}}
                for row in self.student]

    def freeze(self, responses=None):
        return freeze_first_answers(self.packet, self.student, self.controller,
                                    self.responses() if responses is None else responses)

    def reviews(self, locked, *, met=True):
        reviews = review_template(self.packet, self.student, self.controller, locked)
        for review in reviews:
            review['reviewer'] = {'identity': 'fixture-reviewer', 'kind': 'human', 'method': 'Invented test marks only.'}
            for criterion in review['criteria']:
                criterion.update(met=met, reason='Synthetic judgment for arithmetic routing.')
        return reviews

    def grade(self, locked, reviews=(), **kwargs):
        return grade_assessment(self.packet, self.student, self.controller, locked, reviews, **kwargs)

    def test_student_projection_has_no_evaluator_ids_hashes_or_gold(self):
        for row in self.student:
            self.assertEqual(set(row), {'task_id', 'question', 'assumptions', 'conventions', 'response_format'})
        text = json.dumps(self.student)
        for secret in ['SECRET_', 'cohort_digest', 'probe_id', 'pair_id', 'cluster_id', 'source_nodes', 'parent_core_ids']:
            self.assertNotIn(secret, text)
        second, controller = prepare_evaluation(self.packet, split='test_public')
        self.assertNotEqual(self.controller['run_id'], controller['run_id'])
        self.assertFalse({r['task_id'] for r in self.student} & {r['task_id'] for r in second})
        self.student[0]['assumptions'].append('local mutation')
        self.assertFalse(any('local mutation' in p['assumptions'] for p in self.packet['probes']))


    def test_model_messages_are_deterministic_fresh_chat_without_transport_metadata(self):
        row = self.student[0]
        messages = model_messages(row)
        self.assertEqual(messages, model_messages(deepcopy(row)))
        self.assertEqual([m['role'] for m in messages], ['system', 'user'])
        payload = json.loads(messages[1]['content'])
        self.assertEqual(payload, {k: row[k] for k in ('question', 'assumptions', 'conventions', 'response_format')})
        self.assertEqual(payload['response_format']['decision'], 'holds | refuted | abstain')
        renamed = deepcopy(row); renamed['task_id'] = str(uuid4())
        self.assertEqual(messages, model_messages(renamed))
        text = json.dumps(messages)
        for forbidden in ['task_id', 'controller', 'probe_id', 'pair_id', 'cluster_id', 'digest', 'SECRET_', row['task_id']]:
            self.assertNotIn(forbidden, text)
        for probe in self.packet['probes']:
            self.assertNotIn(probe['probe_id'], text)
        messages[1]['content'] = 'local mutation'
        self.assertNotEqual(messages, model_messages(row))

    def test_model_messages_reject_enriched_or_changed_projection(self):
        for key in ('probe_id', 'controller_digest', 'gold', 'messages'):
            row = deepcopy(self.student[0]); row[key] = 'SECRET_INJECTED_METADATA'
            with self.subTest(key=key), self.assertRaises(ValueError): model_messages(row)
        row = deepcopy(self.student[0]); row['response_format']['gold'] = 'holds'
        with self.assertRaises(ValueError): model_messages(row)
        row = deepcopy(self.student[0]); row['assumptions'] = {'secret': 'not a list'}
        with self.assertRaises(ValueError): model_messages(row)

    def test_inner_answer_abstention_transport_and_existing_freeze_api(self):
        alias = self.student[0]['task_id']
        for decision in ('holds', 'refuted'):
            answer = {'decision': decision, 'explanation': 'Synthetic mathematical argument.'}
            row = model_answer_row(alias, answer)
            self.assertEqual(row, {'task_id': alias, 'status': 'answered', 'answer': answer})
            answer['explanation'] = 'changed original'
            self.assertNotEqual(row['answer']['explanation'], answer['explanation'])
        raw_abstention = {'decision': 'abstain', 'explanation': 'The needed mathematical boundary is unresolved.'}
        abstained = model_answer_row(alias, raw_abstention)
        self.assertEqual(abstained, {'task_id': alias, 'status': 'abstained', 'answer': None})
        self.assertTrue(raw_abstention['explanation'])
        responses = [model_answer_row(r['task_id'], raw_abstention) for r in self.student]
        report = self.grade(self.freeze(responses))
        self.assertEqual(report['outcomes'], {'abstained': 4})
        self.assertEqual(report['label_accuracy_over_planned'], 0)
        self.assertEqual(report['qualified_success_over_planned'], 0)

    def test_model_answer_normalization_rejects_malformed_answers_without_repair(self):
        alias = self.student[0]['task_id']
        bads = [None, '{}', [], {'decision': 'holds'},
                {'decision': 'holds', 'explanation': '', 'score': 1},
                {'decision': 'holds', 'explanation': 'ok', 'status': 'answered'},
                {'decision': 'abstained', 'explanation': 'ok'},
                {'decision': 'abstain', 'explanation': '   '},
                {'decision': [], 'explanation': 'ok'},
                {'decision': True, 'explanation': 'ok'},
                {'decision': 'refuted', 'explanation': 'x' * 16001}]
        for answer in bads:
            with self.subTest(answer=answer), self.assertRaises(ValueError): model_answer_row(alias, answer)
        for invalid_alias in (None, [], 'task-1', '00000000-0000-0000-0000-000000000000', alias.upper()):
            with self.subTest(alias=invalid_alias), self.assertRaises(ValueError):
                model_answer_row(invalid_alias, {'decision': 'holds', 'explanation': 'ok'})

    def test_correct_labels_and_nonsense_do_not_earn_argument_or_qualified_success(self):
        report = self.grade(self.freeze())
        self.assertEqual(report['label_accuracy_over_planned'], 1)
        self.assertEqual(report['pair_label_success_over_planned'], 1)
        self.assertIsNone(report['argument_score_over_planned'])
        self.assertIsNone(report['reviewed_argument_credit_over_planned'])
        self.assertTrue(all(r['argument_score'] is None for r in report['rows']))
        self.assertEqual(report['qualified_success_over_planned'], 0)
        self.assertEqual(report['pair_qualified_success_over_planned'], 0)
        self.assertFalse(report['all_planned_qualified'])
        self.assertIsNone(report['formal_proof_score'])
        self.assertFalse(report['understanding_established'])

    def test_always_holds_cannot_pass_any_balanced_pair(self):
        report = self.grade(self.freeze(self.responses(always='holds')))
        self.assertEqual(report['label_accuracy_over_planned'], .5)
        self.assertEqual(report['pair_label_success_over_planned'], 0)

    def test_one_correct_and_missing_keep_planned_denominators(self):
        locked = self.freeze(self.responses()[:1])
        report = self.grade(locked, self.reviews(locked))
        self.assertEqual(report['outcomes'], {'answered': 1, 'missing': 3})
        self.assertEqual(report['label_accuracy_over_planned'], .25)
        self.assertEqual(report['qualified_success_over_planned'], .25)
        self.assertEqual(report['reviewed_argument_credit_over_planned'], .25)
        self.assertIsNone(report['argument_score_over_planned'])
        self.assertEqual(report['pair_label_success_over_planned'], 0)
        self.assertFalse(report['all_planned_qualified'])

    def test_empty_abstained_and_wrong_are_distinct_and_never_fully_qualified(self):
        empty = self.grade(self.freeze([]))
        self.assertEqual(empty['label_accuracy_over_planned'], 0)
        self.assertEqual(empty['outcomes'], {'missing': 4})
        rows = [{'task_id': r['task_id'], 'status': s, 'answer': None}
                for r, s in zip(self.student, ['abstained', 'env_blocked', 'not_run', 'budget_exhausted'])]
        report = self.grade(self.freeze(rows))
        self.assertEqual(report['submitted_responses'], 4)
        self.assertEqual(report['answered_probes'], 0)
        self.assertEqual(report['qualified_success_over_planned'], 0)
        self.assertEqual(review_template(self.packet, self.student, self.controller, self.freeze(rows)), [])
        locked = self.freeze(self.responses(always='refuted'))
        self.assertEqual(self.grade(locked, self.reviews(locked))['qualified_success_over_planned'], .5)

    def test_every_criterion_is_required_even_when_weighted_score_is_high(self):
        locked = self.freeze()
        reviews = self.reviews(locked)
        for review in reviews:
            review['criteria'][1]['met'] = False
        report = self.grade(locked, reviews)
        self.assertEqual(report['argument_score_over_planned'], .75)
        self.assertEqual(report['qualified_success_over_planned'], 0)
        self.assertFalse(any(r['argument_pass'] for r in report['rows']))
        report = self.grade(locked, self.reviews(locked), evidence_kind='operator_supplied')
        self.assertEqual(report['qualified_success_over_planned'], 1)
        self.assertTrue(report['all_planned_qualified'])
        self.assertFalse(report['model_performance_measured'])
        self.assertFalse(report['model_identity_authenticated'])
        self.assertFalse(report['review_identity_authenticated'])
        self.assertFalse(report['understanding_established'])

    def test_seal_detects_mutation_and_does_not_alias_original_response(self):
        responses = self.responses(); locked = self.freeze(responses)
        responses[0]['answer']['decision'] = 'abstain'
        self.assertNotEqual(locked['responses'][0]['answer']['decision'], 'abstain')
        changed = deepcopy(locked); changed['responses'][0]['answer']['explanation'] = 'replacement'
        with self.assertRaises(ValueError): self.grade(changed)
        changed = deepcopy(locked); changed['lock_digest'] = '0' * 64
        with self.assertRaises(ValueError): self.grade(changed)

    def test_response_injection_duplicates_empty_and_unknown_aliases_rejected(self):
        good = self.responses()
        bads = []
        r = deepcopy(good); r[0]['answer']['score'] = 1; bads.append(r)
        r = deepcopy(good); r[0]['answer']['explanation'] = ''; bads.append(r)
        r = deepcopy(good); r[0]['answer']['decision'] = []; bads.append(r)
        r = deepcopy(good); r[0]['status'] = 'missing'; bads.append(r)
        r = deepcopy(good); r[0]['task_id'] = str(uuid4()); bads.append(r)
        r = deepcopy(good); r[1] = deepcopy(r[0]); bads.append(r)
        r = deepcopy(good); r[0]['score'] = 1; bads.append(r)
        r = deepcopy(good); r[0]['status'] = 'abstained'; bads.append(r)
        for bad in bads:
            with self.subTest(bad=bad), self.assertRaises(ValueError): self.freeze(bad)

    def test_stale_swapped_extra_and_unset_reviews_rejected(self):
        locked = self.freeze(); good = self.reviews(locked)
        bads = [review_template(self.packet, self.student, self.controller, locked)]
        r = deepcopy(good); r[0]['response_hash'] = r[1]['response_hash']; bads.append(r)
        r = deepcopy(good); r[0]['lock_digest'] = '0' * 64; bads.append(r)
        r = deepcopy(good); r[0]['rubric_digest'] = '0' * 64; bads.append(r)
        r = deepcopy(good); r[0]['criteria'][0]['criterion'] = 'easier criterion'; bads.append(r)
        r = deepcopy(good); r[0]['criteria'][0]['weight'] = 99; bads.append(r)
        r = deepcopy(good); r[0]['criteria'][0]['met'] = 1; bads.append(r)
        r = deepcopy(good); r[0]['criteria'][0]['reason'] = ''; bads.append(r)
        r = deepcopy(good); r[0]['criteria'].append(deepcopy(r[0]['criteria'][0])); bads.append(r)
        r = deepcopy(good); r[1] = deepcopy(r[0]); bads.append(r)
        r = deepcopy(good); r[0]['self_grade'] = True; bads.append(r)
        r = deepcopy(good); r[0]['reviewer']['identity'] = 'fixture-author'; bads.append(r)
        for bad in bads:
            with self.subTest(bad=bad), self.assertRaises(ValueError): self.grade(locked, bad)

    def test_controller_and_student_changes_cannot_substitute_tasks(self):
        locked = self.freeze()
        altered = deepcopy(self.student); altered[0]['question'] = 'easier problem'
        with self.assertRaises(ValueError): freeze_first_answers(self.packet, altered, self.controller, [])
        altered = deepcopy(self.controller); altered['assignments'][0]['probe_id'] = str(uuid4())
        with self.assertRaises(ValueError): freeze_first_answers(self.packet, self.student, altered, [])
        second, controller = prepare_evaluation(self.packet, split='test_public')
        with self.assertRaises(ValueError): grade_assessment(self.packet, second, controller, locked)

    def test_transitive_source_parent_mechanism_groups_do_not_use_family_names(self):
        self.assertEqual(len(assessment_groups(self.packet)), 2)
        merged = deepcopy(self.packet)
        for probe in merged['probes'][2:]: probe['source_nodes'].append('SECRET_SOURCE_0')
        groups = assessment_groups(merged)
        self.assertEqual(len(groups), 1)
        self.assertFalse(groups[0]['independence_established'])
        self.assertEqual(len(groups[0]['probe_ids']), 4)
        merged = deepcopy(self.packet)
        for probe in merged['probes'][2:]: probe['cluster_id'] = 'mechanism-0'
        self.assertEqual(len(assessment_groups(merged)), 1)

    def test_no_hidden_defaults_and_bad_provenance_or_split_fail_closed(self):
        for split in ['test_private', None, [], 'train']:
            with self.subTest(split=split), self.assertRaises(ValueError): prepare_evaluation(self.packet, split=split)
        for kind in ['model_verified', None, []]:
            with self.subTest(kind=kind), self.assertRaises(ValueError): self.grade(self.freeze(), evidence_kind=kind)
        changed = deepcopy(self.packet); changed['probes'][1]['gold']['decision'] = 'holds'
        with self.assertRaises(ValueError): prepare_evaluation(changed, split='test_public')


if __name__ == '__main__':
    unittest.main()
