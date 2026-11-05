"""Whole stored counter interface, exact independent chain and unchanged old bindings."""
import copy,hashlib,importlib.util,json,re,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('c39_stored_test_gate',ROOT/'website/scripts/check_research_publications.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
def zipjson(name,member):
    with zipfile.ZipFile(HERE/name) as z:return json.loads(z.read(member))
class StoredReviewedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=gate.load(ROOT,'website/research/publications.json')['records']
        cls.r=next(r for r in cls.records if r['module']=='QuantumBlockEncoding/StoredGivens.lean')
        cls.inventory={r['fullName']:r for r in gate.load(ROOT,'web/library/declarations.json')['declarations']}
    def test_all_current_records_and_old26_bindings_preserved(self):
        receipt=gate.load(ROOT,'reports/lean-433-migration/c39-stored-local-registry-integration.json');by={r['module']:r for r in self.records}
        self.assertGreaterEqual(len(self.records),27);self.assertEqual(len(receipt['old_26_bindings']),26)
        for m,b in receipt['old_26_bindings'].items():self.assertEqual(by[m]['binding_sha256'],b)
        for r in self.records:gate.validate_record(ROOT,r,self.inventory)
        for f in ('main_merged','scientific_ROOT','PURIFIED'):self.assertIs(receipt[f],False)
    def test_exact_actual_independent_identities_and_decoder_hash(self):
        r=self.r;d=gate.load(ROOT,r['decoder_evidence']);v=gate.load(ROOT,r['reviewer_evidence'])
        self.assertEqual(d['identity'],'/root/stored_givens_formal_decoder_c38');self.assertEqual(v['identity'],'/root/stored_givens_source_first_c38')
        self.assertEqual(v['decoder_evidence_sha256'],hashlib.sha256((ROOT/r['decoder_evidence']).read_bytes()).hexdigest())
        self.assertTrue(d['source_blind']);self.assertTrue(v['anti_anchored']);self.assertEqual(v['verdict'],'accepted')
        self.assertEqual(len({r['formalizer'],d['identity'],v['identity']}),3)
        with zipfile.ZipFile(ROOT/d['packet_path']) as z:self.assertEqual(set(z.namelist()),{'formal/Module'+str(i)+'.lean' for i in range(4)})
    def test_whole60_plus_anonymous_and_all_17_AND_tails(self):
        meta=zipjson('author-frozen-public.zip','metadata.json');cmp=zipjson('source-review-public-derivative.zip','phase2/declaration-comparison.json')
        cov=zipjson('source-review-public-derivative.zip','phase1/coverage.json')
        self.assertEqual(set(self.r['declarations']),{d['fullName'] for d in meta['inventory']['declarations']})
        self.assertEqual(len(self.r['declarations']),60);self.assertEqual(len(cmp['rows']),61)
        self.assertTrue(all(x['result']=='MATCH' and x['excess_binders']==[] and not x['repair_proposed'] for x in cmp['rows']))
        self.assertEqual(len(meta['inventory']['supplement']['anonymousInstances']),1)
        edges=self.r['graph_contribution']['source_AND_hyperedges'];self.assertEqual(len(edges),17)
        self.assertEqual([(e['tail_labels'],e['head_label']) for e in edges],[(e['tails'],e['head']) for e in cov['and_hyperedges']])
        for e in edges:self.assertTrue(e['all_tails_required']);self.assertTrue(set(e['tails']+[e['head']])<=set(self.r['graph_contribution']['node_ids']))
    def test_source_and_original_private_derivative_distinction(self):
        with zipfile.ZipFile(HERE/'author-frozen-public.zip') as z:source=z.read('source.md')
        self.assertEqual((ROOT/self.r['lesson_path']).read_bytes(),source)
        self.assertFalse(self.r['statement_seal']['preproof'])
        self.assertEqual(self.r['statement_seal']['evidence_class'],'RETROSPECTIVE_IMPLEMENTATION_INFORMED')
        ds=zipjson('formal-decoder-public-derivative.zip','derivative-seal.json')
        rs=zipjson('source-review-public-derivative.zip','derivative-seal.json')
        self.assertIn('posthoc',ds['creation_status'].lower())
        self.assertEqual(self.r['purification']['status'],'PENDING')
    def test_missing_declaration_and_false_AND_mutation_rejected(self):
        bad=copy.deepcopy(self.r);bad['declarations'].pop()
        with self.assertRaisesRegex(ValueError,'whole changed-module inventory'):gate.validate_record(ROOT,bad,self.inventory)
        bad=copy.deepcopy(self.r);bad['graph_contribution']['source_AND_hyperedges'][0]['tails'].pop()
        with self.assertRaisesRegex(ValueError,'binding is stale'):gate.validate_record(ROOT,bad,self.inventory)
        with self.assertRaisesRegex(ValueError,'changed production modules lack reviewed publication records'):gate.check(ROOT,'origin/main')
if __name__=='__main__':unittest.main()
