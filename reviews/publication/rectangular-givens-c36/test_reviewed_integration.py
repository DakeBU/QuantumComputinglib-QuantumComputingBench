"""Exact independent bindings and complete AND tails, not a root/resource certificate."""
import copy,hashlib,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('c37_test_gate',ROOT/'website/scripts/check_research_publications.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
class ReviewedRectangularTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=gate.load(ROOT,'website/research/publications.json')['records']
        cls.record=next(r for r in cls.registry if r['module']=='QuantumBlockEncoding/RectangularGivens.lean')
        cls.inventory={r['fullName']:r for r in gate.load(ROOT,'web/library/declarations.json')['declarations']}
    def test_entire_registry_and_old25_bindings_preserved(self):
        receipt=gate.load(ROOT,'reports/lean-433-migration/c37-rectangular-local-registry-integration.json')
        by={r['module']:r for r in self.registry}
        self.assertGreaterEqual(len(self.registry),26)
        self.assertEqual(len(receipt['old_25_bindings']),25)
        for module,binding in receipt['old_25_bindings'].items():self.assertEqual(by[module]['binding_sha256'],binding)
        for r in self.registry:gate.validate_record(ROOT,r,self.inventory)
        self.assertFalse(receipt['main_merged']);self.assertFalse(receipt['scientific_ROOT']);self.assertFalse(receipt['PURIFIED'])
    def test_original_decoder_and_distinct_reviewer_exact_chain(self):
        r=self.record;d=gate.load(ROOT,r['decoder_evidence']);v=gate.load(ROOT,r['reviewer_evidence'])
        self.assertEqual(len(r['declarations']),19)
        self.assertEqual(d['identity'],'/root/rectangular_formal_decoder_c36')
        self.assertEqual(v['identity'],'/root/rectangular_source_first_c36')
        self.assertEqual(len({r['formalizer'],d['identity'],v['identity']}),3)
        self.assertEqual(v['decoder_evidence_sha256'],hashlib.sha256((ROOT/r['decoder_evidence']).read_bytes()).hexdigest())
        self.assertTrue(d['source_blind']);self.assertTrue(v['anti_anchored']);self.assertEqual(v['verdict'],'accepted')
        for e in (d,v):
            for label in ('packet','artifact'):
                self.assertEqual(hashlib.sha256((ROOT/e[label+'_path']).read_bytes()).hexdigest(),e[label+'_sha256'])
    def test_separate_determinant_skip_length_and_recovery_AND_tails(self):
        compare=gate.load(ROOT,self.record['source_proof_coverage']);g=self.record['graph_contribution'];p='concept:rectangular-elimination/'
        self.assertEqual(g['source_AND_hyperedges'],[dict(tails=[p+n for n in e['tails']],head=p+e['head']) for e in compare['reviewed_AND_hyperedges']])
        edges={e['head']:e['tails'] for e in compare['reviewed_AND_hyperedges']}
        self.assertEqual(len(edges),17);self.assertIn('PLANE_DET',edges['S5B'])
        self.assertIn('SKIP_PREFIX_FROM_ROW_LT_N_LE_K',edges['S3B']);self.assertIn('SWEEP_LENGTH',edges['S4'])
        self.assertEqual(edges['S6_6'],['S6_2','S6_5_ORTH','MATRIX_ASSOCIATIVITY_AND_IDENTITY'])
        self.assertEqual(len(compare['declaration_map']),19);self.assertEqual(compare['scope']['definitions'],6)
        self.assertFalse(self.record['statement_seal']['pre_proof_claim'])
    def test_source_clarification_exact_original_review_and_natural_seal(self):
        repair=self.record['repair'];v=gate.load(ROOT,repair['independent_review'])
        self.assertEqual(hashlib.sha256((ROOT/repair['proposal_path']).read_bytes()).hexdigest(),v['proposal_sha256'])
        self.assertEqual(v['verdict'],'accepted');self.assertNotEqual(v['identity'],self.record['formalizer'])
        for key in ('sealed_natural_derivation','sealed_original_independent_verdict'):
            p=(ROOT/repair['independent_review']).parent/v['minimality_evidence'][key]
            digest_key=key+'_sha256' if key=='sealed_natural_derivation' else 'sealed_original_verdict_sha256'
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),v['minimality_evidence'][digest_key])
    def test_missing_declaration_stale_binding_and_missing_global_records_rejected(self):
        r=copy.deepcopy(self.record);r['declarations'].pop()
        with self.assertRaisesRegex(ValueError,'whole changed-module inventory'):gate.validate_record(ROOT,r,self.inventory)
        r=copy.deepcopy(self.record);r['graph_contribution']['source_AND_hyperedges'][0]['tails'].pop()
        with self.assertRaisesRegex(ValueError,'binding is stale'):gate.validate_record(ROOT,r,self.inventory)
        with self.assertRaisesRegex(ValueError,'changed production modules lack reviewed publication records'):gate.check(ROOT,'origin/main')
if __name__=='__main__':unittest.main()
