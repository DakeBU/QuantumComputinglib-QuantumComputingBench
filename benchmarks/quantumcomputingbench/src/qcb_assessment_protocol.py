"""Private assessment projection, sealed responses and rubric-bound scoring.

Pure CPU/data functions: no default bank, filesystem, model or Lean execution.
Hashes detect stale/substituted artifacts, not a dishonest operator who rewrites
an entire transcript. The caller must preserve the first seal and keep the
controller, private bank and review artifacts outside every student mount.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import json
from uuid import UUID, uuid4
from random import SystemRandom

from qcb_core import digest
from qcb_learning_validity import validate_answer, validate_probe

SPLITS = {'train', 'dev', 'test_public'}
STATUSES = {'answered', 'abstained', 'not_run', 'env_blocked', 'budget_exhausted', 'protocol_error'}
RESPONSE_FORMAT = {'decision': 'holds | refuted | abstain',
                   'explanation': 'Give a mathematical argument or precise counterexample, preserving the stated boundaries; if abstaining, explain the uncertainty.'}
MODEL_SYSTEM_INSTRUCTION = (
    'Assess the mathematical proposition using the supplied question, assumptions and conventions. '
    'Return exactly one JSON object with decision (holds, refuted, or abstain) and a nonempty explanation '
    'containing your mathematical argument, precise counterexample, or reason for abstaining. '
    'Do not use tools or request formal-proof feedback.'
)


def _shape(value, fields, label):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ValueError('unexpected fields: ' + label)


def _text(value, label, limit=4096):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError('bounded nonempty text required: ' + label)


def _uuid(value):
    try:
        return isinstance(value, str) and str(UUID(value)) == value and UUID(value).version == 4
    except (ValueError, TypeError, AttributeError):
        return False


def _seal(value, field):
    return {**value, field: digest(value)}


def _index(packet):
    if not isinstance(packet, dict) or not isinstance(packet.get('probes'), list) or not 2 <= len(packet['probes']) <= 512:
        raise ValueError('a bounded normalized probe packet is required')
    probes, pairs, parents = {}, {}, {}
    for raw in packet['probes']:
        try:
            probe = validate_probe(raw)
        except (TypeError, KeyError, AttributeError) as error:
            raise ValueError('malformed normalized probe') from error
        key = probe['probe_id']
        if key in probes:
            raise ValueError('duplicate private probe identity')
        probes[key] = probe
        pairs.setdefault(probe['pair_id'], []).append(probe)
        for parent in probe['parent_core_ids']:
            identity = (probe['split'], probe['parent_contracts'][parent])
            if parent in parents and parents[parent] != identity:
                raise ValueError('shared parent aliases disagree about split or contract')
            parents[parent] = identity
    for group in pairs.values():
        if (len(group) != 2 or {p['gold']['decision'] for p in group} != {'holds', 'refuted'}
                or len({p['split'] for p in group}) != 1 or len({p['cluster_id'] for p in group}) != 1):
            raise ValueError('each contrast needs two balanced propositions in the same split and mechanism')
    return probes


def _student_row(probe, alias):
    return {'task_id': alias, 'question': probe['question'],
            'assumptions': deepcopy(probe['assumptions']), 'conventions': deepcopy(probe['conventions']),
            'response_format': deepcopy(RESPONSE_FORMAT)}


def model_messages(student_row):
    """Build one deterministic fresh-chat prompt, excluding controller metadata.

    The accepted row is the exact student projection. IDs stay in transport;
    the user-message JSON contains only the four mathematical input fields.
    """
    _shape(student_row, {'task_id', 'question', 'assumptions', 'conventions', 'response_format'}, 'student row')
    if not _uuid(student_row['task_id']):
        raise ValueError('canonical UUID4 task alias required')
    _text(student_row['question'], 'question', 64000)
    for field in ('assumptions', 'conventions'):
        values = student_row[field]
        if not isinstance(values, list):
            raise ValueError('ordered mathematical text list required: ' + field)
        for value in values:
            _text(value, field, 64000)
    if student_row['response_format'] != RESPONSE_FORMAT:
        raise ValueError('canonical inner decision/explanation response format required')
    assessment = {field: deepcopy(student_row[field])
                  for field in ('question', 'assumptions', 'conventions', 'response_format')}
    return [{'role': 'system', 'content': MODEL_SYSTEM_INSTRUCTION},
            {'role': 'user', 'content': json.dumps(assessment, sort_keys=True, ensure_ascii=False,
                                                 separators=(',', ':'), allow_nan=False)}]


def model_answer_row(task_id, answer):
    """Normalize an exact inner answer into transport without repairing it.

    The caller must preserve the raw reply separately, including an abstention's
    explanation. Abstention has no asserted mathematical answer in the outer
    response protocol, so its transport answer is null.
    """
    if not _uuid(task_id):
        raise ValueError('canonical UUID4 task alias required')
    try:
        normalized = validate_answer(answer)
    except (TypeError, KeyError, AttributeError) as error:
        raise ValueError('malformed inner decision and explanation') from error
    abstained = normalized['decision'] == 'abstain'
    return {'task_id': task_id, 'status': 'abstained' if abstained else 'answered',
            'answer': None if abstained else normalized}


def prepare_evaluation(packet, *, split):
    """Return answer-free student rows and a separate private controller seal."""
    probes = _index(packet)
    if not isinstance(split, str) or split not in SPLITS:
        raise ValueError('explicit known split required')
    selected = [p for p in probes.values() if p['split'] == split]
    if not selected:
        raise ValueError('empty assessment selection')
    SystemRandom().shuffle(selected)
    aliases = [{'task_id': str(uuid4()), 'probe_id': p['probe_id']} for p in selected]
    student = [_student_row(p, a['task_id']) for p, a in zip(selected, aliases)]
    controller = _seal({'schema_version': 'qcb.assessment_controller.v1', 'run_id': str(uuid4()),
                        'cohort_digest': digest(packet), 'student_digest': digest(student),
                        'split': split, 'assignments': aliases}, 'controller_digest')
    return student, controller


def _context(packet, student, controller):
    probes = _index(packet)
    _shape(controller, {'schema_version', 'run_id', 'cohort_digest', 'student_digest',
                        'split', 'assignments', 'controller_digest'}, 'controller')
    if (controller['schema_version'] != 'qcb.assessment_controller.v1' or not _uuid(controller['run_id'])
            or controller['cohort_digest'] != digest(packet) or not isinstance(controller['split'], str) or controller['split'] not in SPLITS
            or controller['controller_digest'] != digest({k: v for k, v in controller.items() if k != 'controller_digest'})
            or not isinstance(student, list) or not isinstance(controller['assignments'], list)
            or not student or len(student) != len(controller['assignments'])
            or controller['student_digest'] != digest(student)):
        raise ValueError('stale or malformed student/controller binding')
    by_alias, seen = {}, set()
    for row, assignment in zip(student, controller['assignments']):
        _shape(assignment, {'task_id', 'probe_id'}, 'private alias assignment')
        alias, key = assignment['task_id'], assignment['probe_id']
        if (not _uuid(alias) or alias in by_alias or not isinstance(key, str) or key not in probes
                or key in seen or probes[key]['split'] != controller['split']
                or row != _student_row(probes[key], alias)):
            raise ValueError('unknown/duplicate alias or changed student projection')
        by_alias[alias] = probes[key]
        seen.add(key)
    if seen != {k for k, p in probes.items() if p['split'] == controller['split']}:
        raise ValueError('controller omits planned probes from its frozen split')
    return by_alias


def _response(row, by_alias):
    _shape(row, {'task_id', 'status', 'answer'}, 'response')
    if (not isinstance(row['task_id'], str) or row['task_id'] not in by_alias
            or not isinstance(row['status'], str) or row['status'] not in STATUSES):
        raise ValueError('unknown alias or response status')
    if row['status'] == 'answered':
        try:
            answer = validate_answer(row['answer'])
        except (TypeError, KeyError, AttributeError) as error:
            raise ValueError('malformed decision and explanation') from error
        if answer['decision'] == 'abstain':
            raise ValueError('use abstained status and null answer')
    elif row['answer'] is not None:
        raise ValueError('unanswered statuses cannot carry answers')
    return deepcopy(row)


def freeze_first_answers(packet, student, controller, responses):
    """Hash-seal the first supplied batch; derive missing rows over all plans.

    Retaining this seal before review is an operator obligation. This pure
    function does not provide a persistent single-use store or authentication.
    """
    by_alias = _context(packet, student, controller)
    if not isinstance(responses, list) or len(responses) > len(by_alias):
        raise ValueError('bounded response list required')
    supplied = {}
    for raw in responses:
        row = _response(raw, by_alias)
        if row['task_id'] in supplied:
            raise ValueError('duplicate first response; replacement is forbidden')
        supplied[row['task_id']] = row
    rows = []
    for alias in by_alias:
        row = supplied.get(alias, {'task_id': alias, 'status': 'missing', 'answer': None})
        rows.append(_seal(row, 'response_hash'))
    return _seal({'schema_version': 'qcb.assessment_first_answers.v1', 'run_id': controller['run_id'],
                  'cohort_digest': digest(packet), 'student_digest': digest(student),
                  'controller_digest': controller['controller_digest'], 'responses': rows}, 'lock_digest')


def _locked(packet, student, controller, locked):
    _shape(locked, {'schema_version', 'run_id', 'cohort_digest', 'student_digest',
                    'controller_digest', 'responses', 'lock_digest'}, 'first-response seal')
    if not isinstance(locked['responses'], list):
        raise ValueError('sealed response list required')
    submitted = []
    for row in locked['responses']:
        _shape(row, {'task_id', 'status', 'answer', 'response_hash'}, 'sealed response')
        bare = {k: v for k, v in row.items() if k != 'response_hash'}
        if row['response_hash'] != digest(bare):
            raise ValueError('response hash differs from sealed first answer')
        if row['status'] != 'missing':
            submitted.append(bare)
        elif row['answer'] is not None:
            raise ValueError('missing response cannot have an answer')
    if locked != freeze_first_answers(packet, student, controller, submitted):
        raise ValueError('stale, replaced or malformed first-response seal')
    return {r['task_id']: r for r in locked['responses']}


def review_template(packet, student, controller, locked):
    """Private rubric-only review forms; untouched judgments cannot be scored."""
    by_alias = _context(packet, student, controller)
    rows = _locked(packet, student, controller, locked)
    reviews = []
    for alias, probe in by_alias.items():
        row = rows[alias]
        if row['status'] != 'answered':
            continue
        reviews.append({'schema_version': 'qcb.assessment_argument_review.v1', 'run_id': controller['run_id'],
                        'task_id': alias, 'cohort_digest': digest(packet), 'student_digest': digest(student),
                        'controller_digest': controller['controller_digest'], 'lock_digest': locked['lock_digest'],
                        'response_hash': row['response_hash'], 'rubric_digest': digest(probe['gold']['rubric']),
                        'reviewer': {'identity': None, 'kind': None, 'method': None},
                        'criteria': [{**deepcopy(c), 'met': None, 'reason': None} for c in probe['gold']['rubric']]})
    return reviews


def assessment_groups(packet, *, probe_ids=None):
    """Merge shared mechanisms, pairs, parents and source nodes conservatively.

    Different family strings never establish independence. Even disjoint
    resulting groups need substantive source/exposure review by the operator.
    """
    probes = _index(packet)
    selected = list(probes) if probe_ids is None else probe_ids
    if (not isinstance(selected, list) or not selected or any(not isinstance(k, str) or k not in probes for k in selected)
            or len(set(selected)) != len(selected)):
        raise ValueError('unique known probes required for grouping')
    groups = []
    for key in selected:
        p = probes[key]
        merged = {'probe_ids': {key}, 'mechanisms': {p['cluster_id']}, 'pair_ids': {p['pair_id']},
                  'parent_core_ids': set(p['parent_core_ids']), 'source_nodes': set(p['source_nodes'])}
        touched = [g for g in groups if any(g[k] & merged[k] for k in merged if k != 'probe_ids')]
        for group in touched:
            for field in merged:
                merged[field] |= group[field]
            groups.remove(group)
        groups.append(merged)
    return [{'group_id': digest(sorted(g['probe_ids'])), **{k: sorted(v) for k, v in g.items()},
             'independence_established': False} for g in sorted(groups, key=lambda g: sorted(g['probe_ids']))]


def grade_assessment(packet, student, controller, locked, reviews=(), *, evidence_kind='synthetic_fixture'):
    """Score labels and actually supplied argument reviews over planned tasks.

    A reviewer can make a mathematical mistake or falsely certify nonsense.
    Declared judgments are not authenticated evidence of a real model run.
    """
    if not isinstance(evidence_kind, str) or evidence_kind not in {'synthetic_fixture', 'operator_supplied'}:
        raise ValueError('explicit supported evidence kind required')
    by_alias = _context(packet, student, controller)
    responses = _locked(packet, student, controller, locked)
    expected = {r['task_id']: r for r in review_template(packet, student, controller, locked)}
    if not isinstance(reviews, (list, tuple)) or len(reviews) > len(expected):
        raise ValueError('bounded review list required')
    marks = {}
    for review in reviews:
        if not isinstance(review, dict) or not isinstance(review.get('task_id'), str):
            raise ValueError('review record required')
        alias = review['task_id']
        template = expected.get(alias)
        if template is None or alias in marks or set(review) != set(template):
            raise ValueError('unknown, duplicate or unexpected review')
        for field in template:
            if field not in {'reviewer', 'criteria'} and review[field] != template[field]:
                raise ValueError('stale, swapped or changed response/rubric review binding')
        _shape(review['reviewer'], {'identity', 'kind', 'method'}, 'reviewer')
        for field in ('identity', 'method'):
            _text(review['reviewer'][field], 'reviewer ' + field)
        if (not isinstance(review['reviewer']['kind'], str) or review['reviewer']['kind'] not in {'human', 'ai'}
                or review['reviewer']['identity'] == by_alias[alias]['author_identity']):
            raise ValueError('declared distinct mathematical reviewer required')
        criteria = review['criteria']
        originals = by_alias[alias]['gold']['rubric']
        if not isinstance(criteria, list) or len(criteria) != len(originals):
            raise ValueError('every exact rubric criterion needs a judgment')
        for criterion, original in zip(criteria, originals):
            _shape(criterion, {'id', 'criterion', 'weight', 'met', 'reason'}, 'criterion judgment')
            if ({k: criterion[k] for k in original} != original or type(criterion['weight']) is not int
                    or type(criterion['met']) is not bool):
                raise ValueError('changed rubric or unset/malformed criterion judgment')
            _text(criterion['reason'], 'criterion reason')
        weighted = sum(c['weight'] for c in criteria if c['met']) / sum(c['weight'] for c in criteria)
        marks[alias] = (weighted, all(c['met'] for c in criteria), digest(review))
    rows = []
    for alias, probe in by_alias.items():
        response = responses[alias]
        correct = response['answer']['decision'] == probe['gold']['decision'] if response['status'] == 'answered' else None
        mark = marks.get(alias)
        rows.append({'task_id': alias, 'probe_id': probe['probe_id'], 'pair_id': probe['pair_id'],
                     'status': response['status'], 'response_hash': response['response_hash'],
                     'decision_correct': correct, 'argument_score': mark[0] if mark else None,
                     'argument_pass': mark[1] if mark else None, 'review_hash': mark[2] if mark else None,
                     'qualified_pass': correct is True and mark is not None and mark[1],
                     'formal_proof_score': None})
    pairs = {}
    for row in rows:
        pairs.setdefault(row['pair_id'], []).append(row)
    planned, planned_pairs = len(rows), len(pairs)
    groups = assessment_groups(packet, probe_ids=[p['probe_id'] for p in by_alias.values()])
    reviewed_credit = sum(m[0] for m in marks.values()) / planned
    return {'schema_version': 'qcb.assessment_score.v1', 'run_id': controller['run_id'],
            'cohort_digest': digest(packet), 'student_digest': digest(student),
            'controller_digest': controller['controller_digest'], 'lock_digest': locked['lock_digest'],
            'evidence_kind': evidence_kind, 'planned_probes': planned, 'planned_contrast_pairs': planned_pairs,
            'submitted_responses': sum(r['status'] != 'missing' for r in rows),
            'outcomes': dict(Counter(r['status'] for r in rows)), 'answered_probes': sum(r['status'] == 'answered' for r in rows),
            'label_accuracy_over_planned': sum(r['decision_correct'] is True for r in rows) / planned,
            'pair_label_success_over_planned': sum(all(r['decision_correct'] is True for r in pair) for pair in pairs.values()) / planned_pairs,
            'argument_reviewed_probes': len(marks), 'argument_review_coverage': len(marks) / planned,
            'argument_score_over_planned': reviewed_credit if len(marks) == planned else None,
            'reviewed_argument_credit_over_planned': reviewed_credit if marks else None,
            'qualified_success_over_planned': sum(r['qualified_pass'] for r in rows) / planned,
            'pair_qualified_success_over_planned': sum(all(r['qualified_pass'] for r in pair) for pair in pairs.values()) / planned_pairs,
            'all_planned_qualified': all(r['qualified_pass'] for r in rows),
            'shared_exposure_groups': groups, 'group_count': len(groups), 'independence_established': False,
            'grouping_rules': ['shared_mechanism', 'shared_pair', 'shared_parent', 'shared_source_node'],
            'rows': rows, 'review_identity_authenticated': False, 'model_identity_authenticated': False,
            'model_performance_measured': False, 'operator_provenance_authenticated': False,
            'formal_proof_score': None, 'formal_execution': 'ENV_BLOCKED', 'learning_gain': None,
            'understanding_established': False,
            'scope': 'Behavioral item scoring from sealed records and declared rubric reviews; no authenticated model, formal-proof or general-understanding claim.'}
