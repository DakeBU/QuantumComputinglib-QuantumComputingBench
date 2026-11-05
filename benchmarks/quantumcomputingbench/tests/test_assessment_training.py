"""Study-level withholding never changes original split or drops one modality only."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from qcb_assessment_training import apply_profile, exclusion_closure, training_fingerprint
from qcb_core import digest


def fixture():
    bindings = {k: {'task_hash': k, 'core_ids': [c], 'track': track}
                for k, c, track in [('a', 'A', 'nonlean'), ('b', 'B', 'nonlean'),
                                     ('c', 'C', 'nonlean'), ('a-sem', 'A', 'semantic'),
                                     ('a-lean', 'A', 'lean'), ('c-lean', 'C', 'lean')]}
    data = {'split': 'train', 'counts': {'nl_and_semantic_views': 4, 'lean_views': 2,
                                       'distinct_existing_cores': 3},
            'source_commit': 'old-commit', 'producer': 'original-producer',
            'nl_and_semantic_examples': [{'task_id': k, 'task_hash': k, 'split': 'train',
                                          'reference': {'answer': 'supervision for ' + c}}
                                         for k, c in [('a', 'A'), ('b', 'B'), ('c', 'C'), ('a-sem', 'A')]],
            'lean_examples': [{'core_id': c, 'view_id': k, 'split': 'train', 'reference': k}
                              for k, c in [('a-lean', 'A'), ('c-lean', 'C')]]}
    profile = {'profile_id': 'promise_register_family_holdout',
               'baseline_training_fingerprint': training_fingerprint(data),
               'train_task_bindings_digest': digest(bindings), 'excluded_core_ids': ['A'],
               'retained_core_ids': ['B', 'C'],
               'counts': {'nl_and_semantic_views': 2, 'lean_views': 1, 'distinct_existing_cores': 2},
               'exposure_scope': 'family_template_withholding_relative_to_this_export; allowed_generic_foundations; public_source_and_pretraining_not_sealed',
               'review_digest': 'a' * 64, 'source_group': 'promise_register_protocols',
               'canonical_splits_changed': False}
    return data, bindings, profile


class FamilyTrainingTests(unittest.TestCase):
    def test_all_views_of_excluded_core_are_removed_without_split_relabel(self):
        data, bindings, profile = fixture()
        result = apply_profile(data, bindings, profile)
        self.assertEqual([r['task_id'] for r in result['nl_and_semantic_examples']], ['b', 'c'])
        self.assertEqual([r['core_id'] for r in result['lean_examples']], ['C'])
        self.assertTrue(all(r['split'] == 'train' for r in result['nl_and_semantic_examples'] + result['lean_examples']))
        self.assertEqual(result['counts']['distinct_existing_cores'], 2)
        self.assertFalse(result['training_exposure_authenticated'])
        self.assertFalse(result['understanding_established'])

    def test_selection_preserves_retained_reference_values_and_original_package(self):
        data, bindings, profile = fixture(); original = deepcopy(data)
        result = apply_profile(data, bindings, profile)
        self.assertEqual(data, original)
        self.assertEqual(result['nl_and_semantic_examples'][0], data['nl_and_semantic_examples'][1])
        result['nl_and_semantic_examples'][0]['reference']['answer'] = 'mutation'
        self.assertEqual(data, original)

    def test_producer_commit_metadata_does_not_change_mathematical_fingerprint(self):
        data, _, _ = fixture(); changed = deepcopy(data)
        changed.update(source_commit='different-code-commit', producer='new-producer')
        self.assertEqual(training_fingerprint(data), training_fingerprint(changed))
        changed['nl_and_semantic_examples'][0]['reference']['answer'] = 'changed mathematics'
        self.assertNotEqual(training_fingerprint(data), training_fingerprint(changed))

    def test_changed_example_or_binding_cannot_reuse_frozen_profile(self):
        data, bindings, profile = fixture(); data['nl_and_semantic_examples'][0]['reference']['answer'] = 'changed'
        with self.assertRaisesRegex(ValueError, 'exact baseline'):
            apply_profile(data, bindings, profile)
        data, bindings, profile = fixture(); bindings['a']['core_ids'] = ['B']
        with self.assertRaisesRegex(ValueError, 'exact baseline'):
            apply_profile(data, bindings, profile)

    def test_multicore_aliases_require_transitive_whole_group_exclusion(self):
        data, bindings, profile = fixture()
        bindings['a-sem']['core_ids'] = ['A', 'B']
        self.assertEqual(exclusion_closure(['A'], bindings), ['A', 'B'])
        bindings['c']['core_ids'] = ['B', 'C']
        self.assertEqual(exclusion_closure(['A'], bindings), ['A', 'B', 'C'])
        profile['train_task_bindings_digest'] = digest(bindings)
        with self.assertRaisesRegex(ValueError, 'complete core/view'):
            apply_profile(data, bindings, profile)

    def test_forged_counts_and_empty_training_profile_are_rejected(self):
        data, bindings, profile = fixture(); profile['counts']['lean_views'] = 2
        with self.assertRaisesRegex(ValueError, 'coverage/counts'):
            apply_profile(data, bindings, profile)
        data, bindings, profile = fixture(); profile.update(excluded_core_ids=['A', 'B', 'C'], retained_core_ids=[])
        with self.assertRaisesRegex(ValueError, 'complete core/view'):
            apply_profile(data, bindings, profile)

    def test_unreviewed_or_absolute_exposure_claim_cannot_be_exported(self):
        for value in [None, 'not-content-bound']:
            data, bindings, profile = fixture(); profile['review_digest'] = value
            with self.assertRaisesRegex(ValueError, 'reviewed profile'):
                apply_profile(data, bindings, profile)
        data, bindings, profile = fixture(); profile['exposure_scope'] = 'guaranteed unseen by the model'
        with self.assertRaisesRegex(ValueError, 'unseen-source'):
            apply_profile(data, bindings, profile)

    def test_missing_or_duplicate_language_records_never_silently_shrink_denominator(self):
        for change in ('drop', 'duplicate'):
            data, bindings, profile = fixture()
            if change == 'drop': data['nl_and_semantic_examples'].pop()
            else: data['nl_and_semantic_examples'].append(deepcopy(data['nl_and_semantic_examples'][0]))
            profile['baseline_training_fingerprint'] = training_fingerprint(data)
            with self.assertRaises(ValueError):
                apply_profile(data, bindings, profile)

    def test_nontrain_rows_are_never_reclassified_as_train(self):
        for group in ('nl_and_semantic_examples', 'lean_examples'):
            data, bindings, profile = fixture(); data[group][0]['split'] = 'test_public'
            profile['baseline_training_fingerprint'] = training_fingerprint(data)
            with self.assertRaises(ValueError):
                apply_profile(data, bindings, profile)


if __name__ == '__main__':
    unittest.main()
