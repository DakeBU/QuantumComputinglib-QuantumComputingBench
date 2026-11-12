"""Template installed only after genuine independent final wrappers exist."""
import copy,hashlib,importlib.util,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('real_c41_final_gate',ROOT/'website/scripts/check_research_publications.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
sha=lambda b:hashlib.sha256(b).hexdigest()
class WholeRealFinalBindings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=gate.load(ROOT,'website/research/publications.json')['records']
        cls.inventory={x['fullName']:x for x in gate.load(ROOT,'web/library/declarations.json')['declarations']}
        cls.new=[x for x in cls.records if x['module'] in {
            'QuantumBlockEncoding/RealAmplitudePreparation.lean','QuantumBlockEncoding/RealIsometryCompletion.lean','QuantumBlockEncoding/ConstructiveIsometryLocal.lean'}]
    def test_all_current_records_and_original27_preserved(self):
        receipt=gate.load(ROOT,'reports/lean-433-migration/c41-real-local-registry-integration.json')
        self.assertGreaterEqual(len(self.records),30);self.assertEqual(len(self.new),3)
        by={x['module']:x for x in self.records}
        for m,h in receipt['old_27_record_sha256'].items():
            self.assertEqual(sha(json.dumps(by[m],sort_keys=True,ensure_ascii=False).encode()),h)
        for record in self.records:gate.validate_record(ROOT,record,self.inventory)
        self.assertFalse(receipt['main_merged']);self.assertFalse(receipt['scientific_ROOT']);self.assertFalse(receipt['PURIFIED'])
    def test_actual_original_independent_identities_and_exact_decoder_bytes(self):
        for r in self.new:
            d=gate.load(ROOT,r['decoder_evidence']);v=gate.load(ROOT,r['reviewer_evidence'])
            self.assertEqual(d['identity'],'real-preparation-decoder-c32-5d05b95f-26db-4691-ab3b-5aae22195a3f')
            self.assertEqual(v['identity'],'/root/real_preparation_source_first_c32')
            self.assertEqual(v['decoder_evidence_sha256'],sha((ROOT/r['decoder_evidence']).read_bytes()))
            self.assertTrue(d['source_blind']);self.assertTrue(v['anti_anchored']);self.assertEqual(v['verdict'],'accepted')
            self.assertEqual(len({r['formalizer'],d['identity'],v['identity']}),3)
    def test_whole_public_inventory_and_no_source_hypothesis_escape(self):
        self.assertEqual([len(x['declarations']) for x in self.new],[41,7,5])
        for r in self.new:
            actual={n for n,x in self.inventory.items() if x.get('source')==r['module']}
            self.assertEqual(set(r['declarations']),actual)
            self.assertTrue(all(x['classification']!='unresolved' for x in r['assumption_deltas']))
        p=HERE/'metadata-v3';inv=json.loads((p/'whole-module-inventory.json').read_bytes())
        roots=[x for m in inv['modules'] for x in m['declarations']]
        self.assertEqual(len(roots),57);self.assertEqual(sum(x['modifier']=='private' for x in roots),4)
    def test_exact_independent_repair_not_historical_source_rewrite(self):
        expected='2e5757956c688e25145f839224d6db0d6a81f817ebbf2ab8a0abc7753450fd0c'
        for r in self.new:
            review=gate.load(ROOT,r['repair']['independent_review'])
            self.assertEqual(sha((ROOT/r['repair']['proposal_path']).read_bytes()),expected)
            self.assertEqual(review['proposal_sha256'],expected);self.assertEqual(review['verdict'],'accepted')
            self.assertEqual(review['identity'],'/root/real_preparation_source_first_c32');self.assertTrue(review['minimality_evidence'])
        with zipfile.ZipFile(HERE/'metadata-v2-wip-public-bundle.zip') as z:
            self.assertEqual(sha(z.read('source-effective-v2.md')),'936020bf35582267a8149ed49addd9a9b106c23512205acaf49e9a3febaa6d80')
    def test_missing_whole_declaration_and_stale_binding_rejected(self):
        r=self.new[0];bad=copy.deepcopy(r);bad['declarations'].pop()
        with self.assertRaisesRegex(ValueError,'whole changed-module inventory'):gate.validate_record(ROOT,bad,self.inventory)
        bad=copy.deepcopy(r);bad['residual_boundary']+=' unreviewed alteration'
        with self.assertRaisesRegex(ValueError,'binding is stale'):gate.validate_record(ROOT,bad,self.inventory)
        with self.assertRaisesRegex(ValueError,'changed production modules lack reviewed publication records'):gate.check(ROOT,'origin/main')
if __name__=='__main__':unittest.main()
