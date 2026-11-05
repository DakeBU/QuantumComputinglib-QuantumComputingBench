"""Public reader stays useful without exposing sealed questions or answers."""
import unittest
import hashlib
from copy import deepcopy
from urllib.parse import urljoin
from unittest.mock import patch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'benchmarks/quantumcomputingbench/src'))

from website.scripts.qcb_assessment_reader import BASE, publish_assessment, publication_record, training_package


def record():
    return {'seal': {'probe_index': [
        {'probe_id': str(i), 'pair_id': str(i // 2), 'cluster_id': 'quantum_mechanism',
         'parent_core_ids': ['qcb-core-sp-005'],
         'source_nodes': ['declaration:QuantumBlockEncoding.example']} for i in range(14)]},
        'coverage': {'sealed_parent_core_count': 6, 'declaration_inventory': 4524,
                     'compiled_inventory': 3548, 'course_anchors': 61,
                     'sealed_assessment_anchors': 12,
                     'compiled_not_anchored_by_these_formal_suites': 3480,
                     'all_modules': [{'source': 'QuantumBlockEncoding/Example.lean',
                                      'compiled_inventory_declarations': 10,
                                      'course_anchor_count': 2, 'sealed_assessment_anchor_count': 1}]},
        'secret_question': 'SECRET_QUESTION_DO_NOT_PUBLISH',
        'secret_answer': 'SECRET_ANSWER_DO_NOT_PUBLISH'}


class AssessmentReaderTests(unittest.TestCase):
    def test_role_identifier_projection_preserves_original_qualification_and_other_fields(self):
        from qcb_core import digest
        status = {'qualification': {'review': {
            'decoder_identity': '/root/decoder', 'source_comparer_identity': '/root/comparer',
            'decoder_digest': 'review-binding'}}, 'runtime_note': '/home/example/not-an-identity'}
        original = deepcopy(status)
        projected = publication_record(status, 'a' * 40)
        self.assertEqual(status, original)
        self.assertEqual(projected['qualification_unprojected_digest'], digest(original['qualification']))
        for field in ('decoder_identity', 'source_comparer_identity'):
            expected = 'sha256:' + hashlib.sha256(original['qualification']['review'][field].encode()).hexdigest()
            self.assertEqual(projected['qualification']['review'][field], expected)
        self.assertNotEqual(projected['qualification']['review']['decoder_identity'],
                            projected['qualification']['review']['source_comparer_identity'])
        self.assertEqual(projected['qualification']['review']['decoder_digest'], 'review-binding')
        self.assertEqual(projected['runtime_note'], original['runtime_note'])

    def setUp(self):
        self.pages = {}
        def write(route, title, body, description):
            self.pages[route] = body
        self.report = publish_assessment(write, lambda t, d: '<div class="qcb-reader"><h1>' + t
                                        + '</h1><p>' + d + '</p>', record(), 'a' * 40)

    def test_three_stage_route_and_three_page_hierarchy(self):
        self.assertEqual(set(self.pages), {BASE, BASE + 'coverage/', BASE + 'protocol/'})
        page = self.pages[BASE]
        for value in ('Study and train', 'Calibrate in public', 'Assess on a sealed set'):
            self.assertIn(value, page)
        self.assertEqual(self.report['sealed_probes'], 14)
        self.assertEqual(self.report['contrast_pairs'], 7)

    def test_secret_data_never_projected(self):
        output = '\n'.join(self.pages.values())
        self.assertNotIn('SECRET_QUESTION', output)
        self.assertNotIn('SECRET_ANSWER', output)
        self.assertFalse(self.report['hidden_questions_published'])

    def test_scope_and_first_answer_argument_formal_evidence_are_separate(self):
        self.assertIn('does not certify mastery', self.pages[BASE])
        protocol = self.pages[BASE + 'protocol/']
        for value in ('first-response seal', 'Missing answers', 'ENV_BLOCKED', 'not the reference label'):
            self.assertIn(value, '\n'.join(self.pages.values()))
        self.assertIn('public references', protocol.lower())

    def test_coverage_keeps_inventory_and_mastery_distinct_and_folds_details(self):
        page = self.pages[BASE + 'coverage/']
        self.assertIn('Question capacity and mastery coverage cannot be obtained by dividing', page)
        self.assertIn('<details', page)
        self.assertNotIn('<details open', page)
        self.assertIn('no independence claim', page)

    def test_graph_links_resolve_under_project_prefix(self):
        base = 'https://example.org/PROJECT/' + BASE + 'coverage/'
        self.assertEqual(urljoin(base, '../../../../lean-graph/index.html'),
                         'https://example.org/PROJECT/lean-graph/index.html')
        self.assertIn('../../../../lean-graph/index.html?focus=', self.pages[BASE + 'coverage/'])

    def test_training_download_counts_views_without_inflating_shared_cores(self):
        tasks = [{'task_id': k, 'task_hash': k + '-hash', 'split': 'train', 'track': track,
                  'core_ids': ['one-core'], 'reference': {'answer': 'public train'}}
                 for k, track in [('a', 'nonlean'), ('b', 'semantic')]]
        rows = [{k: t[k] for k in ('task_id', 'task_hash', 'split', 'reference')} for t in tasks]
        lean = {'split': 'train', 'dev_and_test_references_projected': False,
                'examples': [{'split': 'train', 'core_id': 'one-core'}]}
        with patch('qcb_bench_runtime.export_records', return_value=rows):
            package = training_package({'tasks': tasks}, lean, 'a' * 40)
        self.assertEqual(package['counts'], {'nl_and_semantic_views': 2, 'lean_views': 1,
                                             'distinct_existing_cores': 1})
        self.assertFalse(package['assessment_bank_included'])

    def test_training_download_rejects_mislabeled_evaluation_rows(self):
        tasks = [{'task_id': 'train', 'task_hash': 'hash', 'split': 'train', 'track': 'nonlean',
                  'core_ids': ['train-core'], 'reference': {'answer': 'public train'}}]
        leaked = [{'task_id': 'eval', 'task_hash': 'hash', 'split': 'train',
                   'reference': {'answer': 'should not be exported'}}]
        with patch('qcb_bench_runtime.export_records', return_value=leaked):
            with self.assertRaisesRegex(ValueError, 'leaked'):
                training_package({'tasks': tasks}, {}, 'a' * 40)

    def test_v3_study_core_links_and_training_profiles_do_not_inflate_public_catalog(self):
        from uuid import uuid4
        r = record(); r['study_core_index'] = []
        for i in range(4):
            probe = str(uuid4()); core = 'candidate:' + probe
            r['study_core_index'].append({'core_id': core, 'probe_id': probe, 'contract_hash': 'b' * 64})
            r['seal']['probe_index'].append({'probe_id': probe, 'pair_id': 'new-pair-' + str(i // 2),
                 'cluster_id': 'promise_register_protocols', 'parent_core_ids': [core],
                 'source_nodes': ['declaration:QuantumBlockEncoding.example']})
        r['coverage'].update(existing_catalog_parent_core_count=6, study_core_count=4, sealed_parent_core_count=10)
        pages={}
        summary=publish_assessment(lambda route,title,body,description: pages.__setitem__(route,body),
                                   lambda title,description: '<div>',r,'a'*40)
        self.assertEqual(len(pages),4)
        self.assertEqual(summary['sealed_probes'],18)
        self.assertEqual(summary['existing_catalog_parent_cores'],6)
        self.assertEqual(summary['additional_study_cores'],4)
        self.assertIn('61 cores · 77 views',pages[BASE+'training-profiles/'])
        self.assertIn('does not alter the public catalog',pages[BASE+'coverage/'].replace('do not alter','does not alter'))
        self.assertNotIn('/cores/candidate:',pages[BASE+'coverage/'])
        for c in r['study_core_index']:
            self.assertIn('#study-'+c['probe_id'],pages[BASE+'coverage/'])
        self.assertNotIn('SECRET', ''.join(pages.values()))

    def test_v3_conditions_keep_operator_declaration_separate_from_model_exposure(self):
        r=record();r['study_core_index']=[{'core_id':'candidate:x','probe_id':'x','contract_hash':'c'*64}]
        pages={}
        publish_assessment(lambda route,title,body,description: pages.__setitem__(route,body),
                           lambda title,description:'<div>',r,'a'*40)
        page=pages[BASE+'training-profiles/']
        self.assertIn('operator declaration',page)
        self.assertIn('excluded baseline examples',page)
        self.assertIn('Different package sizes',page)
        self.assertIn('Original split labels',page)


if __name__ == '__main__':
    unittest.main()
