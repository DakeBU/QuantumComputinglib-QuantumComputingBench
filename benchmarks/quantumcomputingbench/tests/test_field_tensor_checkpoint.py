"""Exact editorial scope and review isolation, not mathematical proofs."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(B / 'src'), str(B / 'scripts')]
import release
from qcb_core import digest, read_json
from qcb_curriculum import core_contract
import qcb_textbook_policy as policy

QUESTION_ONLY = {106, 108, 112}
ANSWER_ONLY = {115, 209}
IDS = {f'qcb-core-plan-{n}' for n in QUESTION_ONLY | ANSWER_ONLY}


class FieldTensorCheckpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.originals = {i['core_id']: i for i in release.checked()[2]}
        cls.current, cls.decisions = policy.apply_current_reader_policy(list(cls.originals.values()))
        cls.by_id = {i['core_id']: i for i in cls.current}

    def test_five_targets_preserve_contract_scope_and_ordered_nodes(self):
        self.assertTrue(IDS <= self.by_id.keys())
        self.assertEqual(len(self.current), len(self.by_id))
        for core in IDS:
            with self.subTest(core=core):
                old, new = self.originals[core], self.by_id[core]
                changed = {'question'} if int(core.rsplit('-', 1)[1]) in QUESTION_ONLY else set()
                for field in set(policy.CONTRACT_FIELDS) - changed:
                    self.assertEqual(old[field], new[field])
                self.assertEqual([s['supporting_nodes'] for s in old['semantic_steps']],
                                 [s['supporting_nodes'] for s in new['semantic_steps']])
                self.assertEqual(len(new['semantic_steps']), old['semantic_step_count'])
                self.assertNotEqual(old['reference_answer'], new['reference_answer'])
                self.assertNotIn(old['reviews'][0], new['reviews'])
                self.assertNotEqual(new['reviews'][0]['reviewer'], new['author']['identity'])
                decision = next(d for d in self.decisions if d['core_id'] == core)
                self.assertEqual(decision['prior_withdrawal']['predecessor_item_digest'], digest(old))

    def test_three_explicit_versions_and_two_unchanged_question_repairs(self):
        for n in QUESTION_ONLY:
            old, new = self.originals[f'qcb-core-plan-{n}'], self.by_id[f'qcb-core-plan-{n}']
            lineage = new['question_successor']
            self.assertEqual(new['question_version'], 2)
            self.assertEqual(lineage['changed_contract_fields'], ['question'])
            self.assertEqual(lineage['predecessor_contract_hash'], digest(core_contract(old)))
            self.assertEqual(lineage['current_contract_hash'], digest(core_contract(new)))
            self.assertFalse(lineage['equivalence_to_predecessor_claimed'])
            self.assertEqual(lineage['additional_core_count'], 0)
            self.assertNotIn('task_hash', new)
            self.assertIn('task_hash', new['inherited_predecessor_hashes'])
        for n in ANSWER_ONLY:
            old, new = self.originals[f'qcb-core-plan-{n}'], self.by_id[f'qcb-core-plan-{n}']
            self.assertEqual(core_contract(old), core_contract(new))
            self.assertIn('textbook_successor', new)
            self.assertNotIn('question_successor', new)
        # A later, separately reviewed assumption migration restores this core;
        # this earlier five-target checkpoint did not authorize that migration.
        old208, new208 = self.originals['qcb-core-plan-208'], self.by_id['qcb-core-plan-208']
        self.assertEqual(new208['question_successor']['changed_contract_fields'],
                         ['question', 'assumptions'])
        self.assertNotEqual(old208['assumptions'][0], new208['assumptions'][0])
        self.assertEqual(old208['assumptions'][1], new208['assumptions'][1])
        self.assertEqual(new208['verification_receipts'], [])
        self.assertNotIn(old208['reviews'][0], new208['reviews'])

    def test_missing_exact_review_never_reuses_an_old_approval(self):
        current_policy = read_json(B / 'shared/current-policy.json')
        rows = current_policy['answer_successors'] + current_policy['question_successors']
        actual_is_file = Path.is_file
        for row in [r for r in rows if r['core_id'] in IDS]:
            missing = B / row['review']
            with self.subTest(core=row['core_id']), patch.object(Path, 'is_file',
                    lambda path: False if path == missing else actual_is_file(path)):
                current, decisions = policy.apply_current_reader_policy(list(self.originals.values()))
            self.assertNotIn(row['core_id'], {i['core_id'] for i in current})
            decision = next(d for d in decisions if d['core_id'] == row['core_id'])
            self.assertTrue(decision['status'].startswith('withheld_pending_distinct_'))


if __name__ == '__main__':
    unittest.main()
