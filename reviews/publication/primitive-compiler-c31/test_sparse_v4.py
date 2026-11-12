"""Sparse graph byte-delta checks, never full topology or native acceptance."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
V4=HERE/'metadata-v4'
load=lambda p:json.loads(p.read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


class SparseV4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('c31_v4_public_subset',V4/'verify-sparse-v4.py')
        cls.audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.audit)
        cls.old=load(HERE/'metadata-v3/author-graph-views.json')
        cls.new=load(V4/'author-graph-views.json')

    def test_exact_public_v4_and_original_v3_reviewer_transports(self):
        receipt=load(HERE/'parent-v3-review-and-v4-transport-c31.json')
        self.assertEqual((len(receipt['reviewer_files']),len(receipt['author_v4_files'])),(3,14))
        for row in receipt['reviewer_files']+receipt['author_v4_files']:
            self.assertEqual(sha(ROOT/row['path']),row['sha256'])
            self.assertEqual((ROOT/row['path']).stat().st_size,row['bytes'])

    def test_exact_one_json_tail_addition(self):
        got=self.audit.check_sparse(self.old,self.new)
        self.assertEqual(got,load(V4/'sparse-checks.json')['positive'])
        self.assertEqual(got['exact_path_diff'],[{'op':'add','path':'/views/source-construction-graph/AND_hyperedges/20/tails/4','value':'claim:compiler-definition'}])
        self.assertEqual(got['unchanged_other_AND_records'],31)
        self.assertEqual(got['OPEN_gaps_preserved'],7)
        self.assertFalse(got['construction_DAG_cycle'])

    def test_ten_mutations_still_rejected(self):
        got=self.audit.negative_tests(self.old,self.new)
        self.assertEqual(got,load(V4/'sparse-checks.json')['negative_tests'])
        self.assertEqual(len(got),10)
        self.assertTrue(all(row['result']=='REJECTED_EXPECTED' for row in got))

    def test_original_reviewer_v3_partial_finding_not_overwritten(self):
        seal=load(HERE/'reviewer-c31/phase2-v3-static-seal.json')
        self.assertEqual(seal['old_finding_status']['F1']['status'],'RESOLVED_STATIC')
        self.assertEqual(seal['old_finding_status']['F2']['status'],'RESOLVED_STATIC')
        gap=seal['old_finding_status']['F3']['remaining_open']
        self.assertEqual(gap['missing_explicit_producer_tail'],'claim:compiler-definition')
        self.assertFalse(gap['mathematical_refutation'])
        for row in seal['immutable_predecessor_artifacts']:
            self.assertEqual(sha(HERE/'reviewer-c31'/row['path'].removeprefix('$REVIEWER/')),row['sha256'])

    def test_author_binding_successors_preserve_original_mathematics(self):
        for name in ('PrimitiveMacros','UniformlyControlledRy','CubicAmplitudePrimitive'):
            old=load(HERE/'metadata-v3'/('publication-candidate-'+name+'.json'))
            new=load(V4/('publication-candidate-'+name+'.json'))
            self.assertEqual(new['v3_predecessor_binding_sha256'],old['binding_sha256'])
            for field in ('source_statement','source_anchor','declarations','assumption_deltas','binder_definition_audit','formal_context','source_proof_coverage'):
                self.assertEqual(new[field],old[field])
            self.assertFalse(new['independent_acceptance'])
            self.assertFalse(new['main_admission'])

    def test_public_subset_is_not_private_history_replay_or_admission(self):
        allow=load(V4/'public-allowlist.json')
        self.assertTrue(allow['private_original_handoff_not_exported'])
        self.assertFalse(allow['standalone_public_verification_of_private_history'])
        receipt=load(HERE/'parent-v3-review-and-v4-transport-c31.json')
        self.assertIsNone(receipt['sourceAgreement'])
        self.assertFalse(receipt['nativeAccepted'])
        self.assertFalse(receipt['main_admission'])


if __name__=='__main__':
    unittest.main()
