"""Actual installed proof epoch and genuine current roles, not scientific root success."""
import hashlib,importlib.util,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class InstalledProofEpochTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('unchanged_gate_epoch_tests',ROOT/'website/scripts/check_research_publications.py')
        cls.gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.gate)
        spec=importlib.util.spec_from_file_location('committed_epoch_source',BASE/'test_prospective_reconstruction.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        names=['website/research/publications.json','website/research/sources.json','QuantumBlockEncoding/CubicStatePreparation.lean','QuantumBlockEncoding/CubicAmplitudePrimitive.lean']
        cls.before=m.committed_batch('1a4d0522f1f76ba26bd7a1fa20b9fb2bb4cf6fe4',names)
        cls.old=json.loads(cls.before['website/research/publications.json'])['records']
        cls.current=json.loads((ROOT/'website/research/publications.json').read_bytes())['records']
        cls.inventory={x['fullName']:x for x in json.loads((ROOT/'web/library/declarations.json').read_bytes())['declarations']}
    def test_all39_actual_wholemodule_records_pass_original_unchanged_gate(self):
        self.assertEqual(len(self.current),39)
        for row in self.current:self.gate.validate_record(ROOT,row,self.inventory)
    def test_existing37_semantic_metadata_is_exactly_preserved(self):
        mutable={'binding_sha256','decoder_evidence','reviewer_evidence'}
        for before,after in zip(self.old,self.current[:37]):
            self.assertEqual({k:v for k,v in before.items() if k not in mutable},{k:v for k,v in after.items() if k not in mutable})
            self.assertNotEqual(before['binding_sha256'],after['binding_sha256'])
    def test_old_role_bytes_and_genuine_original_lineage_are_not_rewritten(self):
        for before,after in zip(self.old,self.current[:37]):
            old=json.loads((ROOT/before['decoder_evidence']).read_bytes());new=json.loads((ROOT/after['decoder_evidence']).read_bytes())
            self.assertFalse(new['fresh_source_blind_run']);self.assertFalse(new['new_full_semantic_read'])
            self.assertEqual(new['reconstruction']['original_identity'],old['identity'])
            self.assertEqual(new['reconstruction']['original_reconstruction'],old['reconstruction'])
            self.assertEqual(new['reconstruction']['original_evidence_sha256'],sha((ROOT/before['decoder_evidence']).read_bytes()))
            rev=json.loads((ROOT/after['reviewer_evidence']).read_bytes())
            self.assertFalse(rev['fresh_full_source_review'])
            self.assertEqual(rev['decoder_evidence_sha256'],sha((ROOT/after['decoder_evidence']).read_bytes()))
    def test_old_epoch_bindings_are_rejected_not_silently_fresh(self):
        for row in self.old:
            with self.assertRaisesRegex(ValueError,'binding is stale'):self.gate.validate_record(ROOT,row,self.inventory)
    def test_C29_schema_repair_is_original_owner_result_with_immutable_predecessor(self):
        row=next(x for x in self.current if x['module'].endswith('/CubicStatePreparation.lean'))
        raw=(ROOT/row['decoder_evidence']).read_bytes();dec=json.loads(raw)
        self.assertEqual(sha(raw),'877a19229092019d6085984f1091d769b2d25454170a7c47e75b4c8be0ed6217')
        self.assertEqual(dec['role'],'decoder');self.assertEqual(dec['identity'],'/root/cubic_blind_decoder_c29')
        self.assertIn('20ba0b475f01f008a0359f1ec91cecfcd0a6e37071e68d507e53ba9e98920c96',raw.decode())
        self.assertTrue(dec['reconstruction'])
    def test_installed_pair_is_exactly_the_reviewed_twelve_proof_sites(self):
        for name in ('CubicStatePreparation','CubicAmplitudePrimitive'):
            path='QuantumBlockEncoding/'+name+'.lean';old=self.before[path];new=(ROOT/path).read_bytes()
            if name=='CubicAmplitudePrimitive':self.assertEqual(old.replace(b'native_decide +revert',b'decide +kernel +revert'),new)
            else:self.assertEqual(old.replace(b'native_decide',b'decide +kernel').replace(b'have hzero : (0 : Rat) - 0 = 0 := by decide +kernel',b'have hzero : (0 : Rat) - 0 = 0 := by exact Rat.sub_self'),new)
    def test_actual_four_fresh_compiles_and_prior_failure_are_preserved_raw(self):
        with zipfile.ZipFile(BASE/'local-focused-compile-original4.zip') as z:
            good=z.read('reports/lean-433-migration/c46-local-frozen-pair-compile-v2.json')
            bad=z.read('reports/lean-433-migration/c46-local-frozen-pair-compile-v1-failure.json')
        self.assertEqual(sha(good),'f809c2bba80c2b00ba3bc48d95b9852bab860f3e5bd652e99f12792e646b7115')
        self.assertEqual(sha(bad),'5c5bc85ca9a0f43d17cb3c78fcb48d9e6bf7e887be041e1ac0c912bc3d4245ea')
        data=json.loads(good);self.assertTrue(data['all_four_fresh']);self.assertEqual(len(data['rows']),4)
        self.assertFalse(data['full_Lean_Tests_gate']);self.assertFalse(data['main_admitted'])
        self.assertFalse(json.loads(bad)['all_four_fresh'])
        for row in data['rows']:self.assertEqual(row['source_sha256'],sha((ROOT/row['module']).read_bytes()))
    def test_source_row_append_and_remaining_gate_boundaries_are_exact(self):
        old=json.loads(self.before['website/research/sources.json'])['sources'];new=json.loads((ROOT/'website/research/sources.json').read_bytes())['sources']
        self.assertEqual(new[:-1],old);self.assertEqual(len(new),42)
        receipt=json.loads((ROOT/'reports/lean-433-migration/c46-paired-kernel-adoption.json').read_bytes())
        self.assertEqual(receipt['remaining_count'],12);self.assertEqual(receipt['old207_unchanged'],205)
        self.assertFalse(receipt['inherited_old_full_Lean_input_equality'])
        self.assertFalse(receipt['main_admitted']);self.assertFalse(receipt['scientific_ROOT']);self.assertFalse(receipt['PURIFIED'])
if __name__=='__main__':unittest.main()
