import hashlib,json,re,sys,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[3]))
from tools.proof_trust import strip_lean_comments_and_strings
sha=lambda b:hashlib.sha256(b).hexdigest()
class MiddleCost(unittest.TestCase):
    def binding(self):return json.loads((HERE/'source-binding.json').read_bytes())
    def test_exact_sources_no_holes(self):
        b=self.binding()
        for n,key in [('CachedMiddleCostProof.lean','source_sha256'),('MiddleCostProofChecks.lean','consumer_sha256')]:
            raw=(HERE/n).read_bytes();self.assertEqual(sha(raw),b[key])
            self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b',strip_lean_comments_and_strings(raw.decode())))
    def test_actual_own_output_root_ordinary_axioms(self):
        b=self.binding();raw=(HERE/'proof-result.json').read_bytes();self.assertEqual(sha(raw),b['record_sha256'])
        p=json.loads(raw);self.assertEqual(p['status'],'PROVED_LOCALLY_FOCUSED');self.assertEqual(p['actual_proved_roots'],1)
        a,c=p['records'];self.assertEqual(c['selected_direct_provider_sha256'],a['own_output_sha256'])
        self.assertEqual(c['direct_provider'],'OWN/CachedMiddleCostProof.olean')
        self.assertEqual(a['axiom_reports'],[])
        self.assertEqual([r['name'] for r in c['axiom_reports']],b['public_roots'])
        self.assertEqual(set(c['axiom_reports'][0]['axioms']),{'propext','Classical.choice','Quot.sound'})
        for r in [a,c]:self.assertEqual(r['exit_code'],0);self.assertFalse(r['timeout'])
    def test_failure_and_repair_originals(self):
        r=self.binding()['archive'];self.assertEqual(sha((HERE/r['file']).read_bytes()),r['sha256'])
        with ZipFile(HERE/r['file']) as z:
            self.assertEqual(len(z.namelist()),10);self.assertEqual(set(z.namelist()),set(r['members']))
            for n,m in r['members'].items():self.assertEqual((len(z.read(n)),sha(z.read(n))),(m['bytes'],m['sha256']))
            old=json.loads(z.read('hermite-c182-middle-cost-proof/proof-result.json'))
            self.assertEqual(old['actual_proved_roots'],0);self.assertEqual(old['records'][0]['exit_code'],1)
            self.assertIsNone(old['records'][0]['own_output_sha256']);self.assertEqual(len(old['records']),1)
    def test_no_resource_or_publication_promotion(self):
        b=self.binding()
        for k in ['independent_review','full_native_bit_or_quantum_cost','scientific_ROOT','main_merged','PURIFIED']:self.assertFalse(b[k])
        p=json.loads((HERE/'proof-result.json').read_bytes())
        self.assertFalse(p['full_bit_or_GCD_or_evaluator_cost']);self.assertFalse(p['clean_transitive_TCB'])
if __name__=='__main__':unittest.main()
