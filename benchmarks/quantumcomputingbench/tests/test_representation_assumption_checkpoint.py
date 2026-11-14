"""Exact current-content integration, not automated mathematical certification."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(B / 'src'), str(B / 'scripts')]
import release
from qcb_core import digest, read_json
from qcb_curriculum import core_contract, load_catalog
from qcb_integrity import text_sha
import qcb_textbook_policy as policy

ANSWER_ONLY = {117, 118, 119}
IDS = {f'qcb-core-plan-{n}' for n in ANSWER_ONLY | {120, 208}}


class RepresentationAssumptionCheckpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.originals = {i['core_id']: i for i in release.checked()[2]}
        cls.current, cls.decisions = policy.apply_current_reader_policy(list(cls.originals.values()))
        cls.by_id = {i['core_id']: i for i in cls.current}

    def test_all_five_exact_contract_scopes_and_ordered_nodes(self):
        self.assertTrue(IDS <= self.by_id.keys())
        for core in IDS:
            old, new = self.originals[core], self.by_id[core]
            n = int(core.rsplit('-', 1)[1])
            changed = set() if n in ANSWER_ONLY else {'question'} if n == 120 else {'question', 'assumptions'}
            for field in policy.CONTRACT_FIELDS:
                with self.subTest(core=core, field=field):
                    self.assertEqual(old[field] == new[field], field not in changed)
            self.assertEqual([s['supporting_nodes'] for s in old['semantic_steps']],
                             [s['supporting_nodes'] for s in new['semantic_steps']])
            self.assertEqual(len(new['semantic_steps']), old['semantic_step_count'])
            self.assertNotEqual(old['reference_answer'], new['reference_answer'])
            self.assertNotIn(old['reviews'][0], new['reviews'])
            self.assertNotEqual(new['reviews'][0]['reviewer'], new['author']['identity'])

    def test_versions_do_not_add_cores_or_transfer_old_contracts(self):
        for n in (120, 208):
            old, new = self.originals[f'qcb-core-plan-{n}'], self.by_id[f'qcb-core-plan-{n}']
            lineage = new['question_successor']
            self.assertEqual(new['question_version'], 2)
            self.assertEqual(lineage['predecessor_contract_hash'], digest(core_contract(old)))
            self.assertEqual(lineage['current_contract_hash'], digest(core_contract(new)))
            self.assertFalse(lineage['equivalence_to_predecessor_claimed'])
            self.assertEqual(lineage['additional_core_count'], 0)
        for n in ANSWER_ONLY:
            old, new = self.originals[f'qcb-core-plan-{n}'], self.by_id[f'qcb-core-plan-{n}']
            self.assertEqual(core_contract(old), core_contract(new))
            self.assertNotIn('question_successor', new)

    def test_actual_208_premises_context_and_evidence_are_current(self):
        old, new = self.originals['qcb-core-plan-208'], self.by_id['qcb-core-plan-208']
        lineage = new['question_successor']
        self.assertEqual(lineage['changed_contract_fields'], ['question', 'assumptions'])
        self.assertEqual(lineage['current_contract_hash'],
                         '5ca74f53013c3bb488541a92fdfbf70dae71b49f3281eb45b5e9dea82da54441')
        self.assertEqual(lineage['original_assumptions'], old['assumptions'])
        self.assertEqual(lineage['current_assumptions'], new['assumptions'])
        self.assertNotEqual(old['assumptions'][0], new['assumptions'][0])
        self.assertEqual(old['assumptions'][1], new['assumptions'][1])
        self.assertEqual(new['context_hash'], digest({
            k: new[k] for k in ('assumptions', 'conventions', 'formal_context')}))
        self.assertEqual(new['task_hash'], digest({'question': new['question'], 'context': new['context_hash']}))
        self.assertNotEqual(new['context_hash'], old['context_hash'])
        self.assertNotEqual(new['task_hash'], old['task_hash'])
        self.assertEqual(new['inherited_predecessor_hashes']['task_hash'], old['task_hash'])
        self.assertEqual(new['verification_receipts'], [])
        self.assertEqual(new['reviews'][0]['method'], 'independent-assumption-successor-review')

    def test_exact_review_bindings_and_missing_review_fail_closed(self):
        current_policy = read_json(B / 'shared/current-policy.json')
        rows = current_policy['answer_successors'] + current_policy['question_successors']
        actual_is_file = Path.is_file
        for row in [r for r in rows if r['core_id'] in IDS]:
            candidate, review_path = B / row['repair'], B / row['review']
            review = read_json(review_path)
            self.assertEqual(review['repair_record_digest'], digest(read_json(candidate)))
            if 'repair_record_sha256_lf' in review:
                self.assertEqual(review['repair_record_sha256_lf'], text_sha(candidate))
            self.assertEqual(review['original_item_digest'], digest(self.originals[row['core_id']]))
            with self.subTest(core=row['core_id']), patch.object(Path, 'is_file',
                    lambda path: False if path == review_path else actual_is_file(path)):
                current, decisions = policy.apply_current_reader_policy(list(self.originals.values()))
            self.assertNotIn(row['core_id'], {i['core_id'] for i in current})
            decision = next(d for d in decisions if d['core_id'] == row['core_id'])
            self.assertTrue(decision['status'].startswith('withheld_pending_distinct_'))

    def test_original_scope_and_unresolved_global_gates_are_not_shrunk(self):
        catalog, items, _ = load_catalog()
        self.assertEqual(len(items), 203)
        self.assertEqual(len(catalog['withheld_cores']), 10)
        self.assertEqual(len(catalog['review_scope_core_ids']), 213)
        self.assertFalse(catalog['global_semantic_dedup_complete'])
        self.assertEqual(sum('lean' in core['views'] for core in catalog['cores']), 3)


if __name__ == '__main__':
    unittest.main()
