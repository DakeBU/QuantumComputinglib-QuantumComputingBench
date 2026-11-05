"""Exact source-review integration; all old records and soundness gates retained."""
import copy,hashlib,importlib.util,json,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('c31_test_integrated_gate',ROOT/'website/scripts/check_research_publications.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
class IntegratedModuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=gate.load(ROOT,'website/research/publications.json')['records']
        cls.by={r['module']:r for r in cls.records}
        cls.inventory={r['fullName']:r for r in gate.load(ROOT,'web/library/declarations.json')['declarations']}
        cls.receipt=gate.load(ROOT,'reports/lean-433-migration/c31-two-module-local-registry-integration.json')
    def test_all_current_records_strict_validate(self):
        self.assertGreaterEqual(len(self.records),25)
        for r in self.records:gate.validate_record(ROOT,r,self.inventory)
    def test_old23_bindings_unchanged_and_global26gap_remains(self):
        old=self.receipt['old_23_bindings'];self.assertEqual(len(old),23)
        for module,binding in old.items():self.assertEqual(self.by[module]['binding_sha256'],binding)
        with self.assertRaisesRegex(ValueError,'changed production modules lack reviewed publication records'):
            gate.check(ROOT,'origin/main')
        self.assertEqual(len(self.receipt['missing_changed_module_records']),26)
    def test_two_whole_public_sets_and_private_generated_review_scope(self):
        for label,count in [('PrimitiveMacros',43),('UniformlyControlledRy',11)]:
            r=self.by['QuantumBlockEncoding/'+label+'.lean'];self.assertEqual(len(r['declarations']),count)
            d=gate.load(ROOT,r['decoder_evidence']);v=gate.load(ROOT,r['reviewer_evidence'])
            self.assertEqual(v['decoder_evidence_sha256'],hashlib.sha256((ROOT/r['decoder_evidence']).read_bytes()).hexdigest())
            self.assertEqual(len({r['formalizer'],d['identity'],v['identity']}),3)
            self.assertFalse(v['main_admission']);self.assertFalse(v['scientific_ROOT']);self.assertFalse(v['PURIFIED'])
        self.assertEqual(self.receipt['private_helpers_in_whole_module_review'],8)
        self.assertEqual(self.receipt['actual_owned_records'],156)
    def test_original_v1_missing_anti_anchor_cannot_pass_unchanged_gate(self):
        r=self.by['QuantumBlockEncoding/PrimitiveMacros.lean'];load=gate.load
        def historical(root,name):
            if name==r['reviewer_evidence']:
                return load(root,'reviews/publication/primitive-compiler-c31/reviewer-final-v1/PrimitiveMacros.reviewer-evidence.json')
            return load(root,name)
        with patch.object(gate,'load',side_effect=historical):
            with self.assertRaisesRegex(ValueError,'accepted anti-anchored review'):gate.validate_record(ROOT,r,self.inventory)
if __name__=='__main__':unittest.main()
