"""Exact local admission, including fail-closed missing evidence checks."""
import copy,hashlib,importlib.util,json,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[3];HERE=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(path):return json.loads(path.read_bytes())
class FoundationsFinalAdmission(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('foundations_final_gate',ROOT/'website/scripts/check_research_publications.py')
        cls.gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.gate)
        cls.inv={x['fullName']:x for x in load(ROOT/'web/library/declarations.json')['declarations']}
        cls.records=load(ROOT/'website/research/publications.json')['records']
        cls.context=load(HERE/'final-context-c43-v3.json')
    def test_actual_registry_and_old30_records_preserved(self):
        self.assertGreaterEqual(len(self.records),33)
        receipt=load(ROOT/'reports/lean-433-migration/c43-foundations-local-registry-integration.json')
        for r in self.records:self.gate.validate_record(ROOT,r,self.inv)
        for r in self.records[:30]:self.assertEqual(sha(json.dumps(r,sort_keys=True,ensure_ascii=False).encode()),receipt['old30_record_sha256'][r['module']])
    def test_all_three_roles_bind_exact_real_results_and_repair(self):
        for r in self.context['records']:
            d=load(ROOT/r['decoder_evidence']);v=load(ROOT/r['reviewer_evidence'])
            self.assertEqual(d['identity'],'/root/sp_foundations_formal_decoder_c41')
            self.assertEqual(v['identity'],'/root/sp_foundations_source_first_c41')
            self.assertEqual(v['decoder_evidence_sha256'],sha((ROOT/r['decoder_evidence']).read_bytes()))
            self.assertEqual(v['binding_sha256'],d['binding_sha256']);self.assertTrue(d['source_blind'])
            self.assertEqual(v['verdict'],'accepted');self.assertTrue(v['anti_anchored'])
            self.assertEqual(set(v['semantic_slots']),{'target','normalization','registers','oracles','ancillas_phases','error_success','resources'})
            self.assertTrue(all(v['semantic_slots'].values()))
            repair=load(ROOT/r['repair']['independent_review'])
            self.assertEqual(repair['verdict'],'accepted')
            self.assertEqual(repair['proposal_sha256'],sha((ROOT/r['repair']['proposal_path']).read_bytes()))
    def test_missing_decoder_and_reviewer_cannot_pass(self):
        missing='reviews/publication/sp-foundations-c42/no-such-independent-evidence-c43.json'
        self.assertFalse((ROOT/missing).exists())
        for r in self.context['records']:
            for key in ('decoder_evidence','reviewer_evidence'):
                bad=copy.deepcopy(r);bad[key]=missing
                with self.assertRaisesRegex(ValueError,'missing evidence file'):self.gate.validate_record(ROOT,bad,self.inv)
    def test_missing_exact_repair_review_cannot_pass(self):
        for r in self.context['records']:
            bad=copy.deepcopy(r);bad['repair']['independent_review']='reviews/publication/sp-foundations-c42/no-such-minimality-review-c43.json'
            with self.assertRaisesRegex(ValueError,'missing evidence file'):self.gate.validate_record(ROOT,bad,self.inv)
    def test_changed_source_statement_cannot_reuse_old_review(self):
        for r in self.context['records']:
            bad=copy.deepcopy(r);bad['source_statement']+=' unauthorized stronger conclusion'
            with self.assertRaisesRegex(ValueError,'publication binding is stale'):self.gate.validate_record(ROOT,bad,self.inv)
if __name__=='__main__':unittest.main()
