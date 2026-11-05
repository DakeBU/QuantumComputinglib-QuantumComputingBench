"""Original source-first review: narrow sparse result, never native admission."""
import hashlib
import json
from pathlib import Path
import unittest
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())

class OriginalV4ReviewTests(unittest.TestCase):
    def test_exact_three_review_artifacts(self):
        receipt=load(HERE/'parent-v4-review-transport-c31.json')
        root=HERE.parents[2]
        self.assertEqual(len(receipt['files']),3)
        for row in receipt['files']:
            raw=(root/row['path']).read_bytes()
            self.assertEqual(sha(raw),row['sha256']);self.assertEqual(len(raw),row['bytes'])

    def test_same_original_identity_and_phase1_derivation(self):
        seal=load(HERE/'reviewer-c31/phase2-v4-static-seal.json')
        self.assertEqual(seal['reviewer_identity'],'/root/primitive_compiler_source_first_c31')
        self.assertTrue(seal['original_firsthand_natural_derivation_retained'])
        self.assertEqual(len(seal['immutable_old_review_artifacts']),8)
        for row in seal['immutable_old_review_artifacts']:
            self.assertEqual(sha((HERE/'reviewer-c31'/Path(row['path']).name).read_bytes()),row['sha256'])

    def test_one_producer_edge_not_whole_topology_or_seven_gap_closure(self):
        seal=load(HERE/'reviewer-c31/phase2-v4-static-seal.json')
        c=seal['comparison']
        self.assertEqual(c['graph_change_count'],1)
        self.assertEqual(c['sole_graph_change']['path'],'/views/source-construction-graph/AND_hyperedges/20/tails/4')
        self.assertEqual(c['sole_graph_change']['value'],'claim:compiler-definition')
        self.assertTrue(c['all_seven_open_gaps_identical']);self.assertFalse(c['new_cycle_created'])
        self.assertEqual(seal['narrow_verdicts']['full_F3_or_whole_topology_closure'],'NOT_REDETERMINED')

    def test_exact_bound_v4_author_graph_and_concrete_call(self):
        seal=load(HERE/'reviewer-c31/phase2-v4-static-seal.json')
        self.assertEqual(sha((HERE/'metadata-v4/author-graph-views.json').read_bytes()),seal['authorized_v4_input_hashes']['author-graph-views.json'])
        self.assertIn('compileUniformlyControlledRy 2',seal['actual_source_and_preserved_context']['observed_constructor'])
        self.assertEqual(seal['actual_source_and_preserved_context']['lines'],[44,58])

    def test_no_native_source_agreement_main_or_purification_claim(self):
        seal=load(HERE/'reviewer-c31/phase2-v4-static-seal.json')
        self.assertIsNone(seal['source_agreement_verdict'])
        for key in ('formal_acceptance_claimed','native_acceptance_claimed','root_closure_claimed','main_admission_claimed','purification_claimed'):
            self.assertFalse(seal[key])

if __name__=='__main__':unittest.main()
