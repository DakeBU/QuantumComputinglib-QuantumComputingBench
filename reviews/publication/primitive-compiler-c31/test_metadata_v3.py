"""Public visible-subset checks, not replay of withheld private predecessor history."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
V3=HERE/'metadata-v3'
load=lambda p:json.loads(p.read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


class MetadataV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('c31_v3_subset',V3/'audit-metadata-v3.py')
        cls.audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.audit)
        cls.coverage=load(V3/'author-source-coverage.json')
        cls.binders=load(V3/'author-binder-definition-audit.json')
        cls.graph=load(V3/'author-graph-views.json')

    def test_exact16_transports_and_five_visible_predecessor_references(self):
        receipt=load(HERE/'parent-v3-transport-c31.json')
        self.assertEqual(len(receipt['files']),16)
        for row in receipt['files']:
            self.assertEqual(sha(ROOT/row['path']),row['sha256'])
            self.assertEqual((ROOT/row['path']).stat().st_size,row['bytes'])
        allow=load(V3/'public-allowlist.json')
        self.assertEqual(len(allow['exact_original_references']),5)
        for row in allow['exact_original_references']:
            self.assertEqual(sha(V3/row['path']),row['sha256'])

    def test_visible_static_metadata_and_lossless_source(self):
        result=self.audit.audit_metadata(self.coverage,self.binders,self.graph,(HERE/'source-only.md').read_bytes())
        self.assertEqual(result,load(V3/'author-static-tests.json')['positive'])
        self.assertEqual((result['source_roots'],result['exact_source_atoms'],result['lossless_paragraphs']),(87,60,34))

    def test_thirteen_rejected_mutations_and_three_finite_screens(self):
        rows=self.audit.negative_tests(self.coverage,self.binders,self.graph,(HERE/'source-only.md').read_bytes())
        self.assertEqual(rows,load(V3/'author-static-tests.json')['negative_mutation_tests'])
        self.assertEqual(len(rows),16)
        self.assertEqual(sum(row['result']=='REJECTED_EXPECTED' for row in rows),13)
        self.assertEqual(sum(row['result'].startswith('FINITE_') for row in rows),3)

    def test_corrected_pi_guards_and_no_injective_control_hypothesis(self):
        roots={r['id']:r for r in self.coverage['whole_module_inventory']}
        for key in ('C31-055','C31-056'):
            row=roots[key]
            self.assertEqual(len(row['binder_audit']),6)
            self.assertEqual(row['binder_audit'][4]['classification'],'SOURCE')
            self.assertEqual(row['binder_audit'][4]['exact_lexical_binder'],'(∀ control, wires control ≠ target)')
            self.assertFalse(row['standing_semantics_not_extra_parameter']['computational_access_assumed'])

    def test_distinct_complete_paths_and_local_proof_or(self):
        graph=self.graph['views']['source-construction-graph']
        self.assertEqual(len(graph['AND_hyperedges']),32)
        edges={e['id']:e for e in graph['AND_hyperedges']}
        self.assertNotIn('claim:recursive-evaluation',edges['and:semantic-compiler-direct']['tails'])
        self.assertNotIn('claim:named-wire-clean-entries',edges['and:flat-unitarity']['tails'])
        self.assertNotIn('claim:Ry-count',edges['and:verified-wrapper-correctness']['tails'])
        self.assertEqual(len(graph['local_alternative_proofs']),1)
        self.assertFalse(graph['local_alternative_proofs'][0]['compiled_alternative_construction'])
        self.assertEqual(len(graph['open_source_gap_ids']),7)

    def test_formal_context_and_original_natural_source_unchanged(self):
        self.assertEqual(sha(HERE/'author-formal-context.json'),'a0b798f1e74b084274a44061514f7944ea6b694c13af2b8f718a27ea7b0ac408')
        self.assertEqual(sha(HERE/'source-only.md'),'5907262565b6202fec61b189c42d942cb84d6215223a0da4211d63b92d3ad168')
        self.assertEqual(sha(HERE/'reviewer-c31/phase2-static-seal.json'),'88227580b575d7952bb1ba0b7817a05374d9194d98c4f8166db3046b0dea0f64')

    def test_prospective_bindings_are_not_admitted_records(self):
        for name in ('PrimitiveMacros','UniformlyControlledRy','CubicAmplitudePrimitive'):
            row=load(V3/('publication-candidate-'+name+'.json'))
            self.assertFalse(row['independent_acceptance'])
            self.assertFalse(row['main_admission'])
            self.assertFalse(row['scientific_ROOT'])
        receipt=load(HERE/'parent-v3-transport-c31.json')
        self.assertIsNone(receipt['sourceAgreement'])
        self.assertFalse(receipt['nativeAccepted'])

    def test_visible_subset_is_not_private_historical_replay(self):
        allow=load(V3/'public-allowlist.json')
        self.assertTrue(allow['private_original_handoff_not_referenced'])
        self.assertTrue(allow['not_standalone_verification_of_all_historical_private_artifacts'])
        self.assertFalse((HERE/'handoff.txt').exists())
        # Deliberately do NOT invoke audit.verify_package on this projection:
        # it needs the withheld original private predecessor handoff pin.
        self.assertIn('withholds private original handoff',load(HERE/'parent-v3-transport-c31.json')['historical_private_boundary'])


if __name__=='__main__':
    unittest.main()
