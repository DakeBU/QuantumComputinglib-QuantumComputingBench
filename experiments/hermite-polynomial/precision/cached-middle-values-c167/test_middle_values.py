import hashlib,json,re,sys,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[3]))
from tools.proof_trust import strip_lean_comments_and_strings
sha=lambda b:hashlib.sha256(b).hexdigest()

class MiddleValues(unittest.TestCase):
    def binding(self):return json.loads((HERE/'source-binding.json').read_bytes())
    def test_exact_actual_sources(self):
        b=self.binding()
        self.assertEqual(sha((HERE/'CachedMiddleValueProof.lean').read_bytes()),b['source_sha256'])
        self.assertEqual(sha((HERE/'MiddleValueProofChecks.lean').read_bytes()),b['consumer_sha256'])
        for n in ['CachedMiddleValueProof.lean','MiddleValueProofChecks.lean']:
            self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b',strip_lean_comments_and_strings((HERE/n).read_text(encoding='utf-8'))))
    def test_actual_both_root_axioms_and_own_output(self):
        b=self.binding();raw=(HERE/'proof-result.json').read_bytes();self.assertEqual(sha(raw),b['record_sha256'])
        p=json.loads(raw);self.assertEqual(p['actual_proved_roots'],2);self.assertEqual(len(p['records']),2)
        a,c=p['records'];self.assertEqual(c['selected_direct_provider_sha256'],a['own_output_sha256'])
        self.assertEqual(c['direct_provider'],'OWN/CachedMiddleValueProof.olean')
        for r in p['records']:
            self.assertEqual(r['exit_code'],0);self.assertFalse(r['timeout'])
            self.assertEqual({x['name'] for x in r['axiom_reports']},set(b['public_roots']))
            self.assertEqual(len(r['axiom_reports']),2)
            for x in r['axiom_reports']:self.assertEqual(set(x['axioms']),{'propext','Classical.choice','Quot.sound'})
    def test_exact_precompile_author_freeze_preserved(self):
        row=self.binding()['archive'];self.assertEqual(sha((HERE/row['file']).read_bytes()),row['sha256'])
        with ZipFile(HERE/row['file']) as z:
            self.assertEqual(set(z.namelist()),set(row['members']));self.assertEqual(len(z.namelist()),4)
            for n,m in row['members'].items():self.assertEqual((len(z.read(n)),sha(z.read(n))),(m['bytes'],m['sha256']))
            self.assertFalse(json.loads(z.read('input-manifest.json'))['execution']['compiler'])
    def test_no_finite_or_full_root_promotion(self):
        b=self.binding();p=json.loads((HERE/'proof-result.json').read_bytes())
        for k in ['finite_screen_is_proof','full_cost_or_chain','scientific_ROOT','main_merged']:self.assertFalse(b[k])
        self.assertFalse(p['full_bit_or_GCD_or_evaluator_cost']);self.assertFalse(p['clean_transitive_TCB'])

if __name__=='__main__':unittest.main()
