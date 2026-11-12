import hashlib,json,re,sys,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[3]))
from tools.proof_trust import strip_lean_comments_and_strings
sha=lambda b:hashlib.sha256(b).hexdigest()

class Setup(unittest.TestCase):
    def binding(self):return json.loads((HERE/'source-binding.json').read_bytes())
    def test_exact_sources_and_no_trust_shortcuts(self):
        b=self.binding()
        self.assertEqual(sha((HERE/'CachedSetupProof.lean').read_bytes()),b['source_sha256'])
        self.assertEqual(sha((HERE/'SetupProofChecks.lean').read_bytes()),b['exact_type_consumer_sha256'])
        for name in ['CachedSetupProof.lean','SetupProofChecks.lean']:
            code=strip_lean_comments_and_strings((HERE/name).read_text(encoding='utf-8'))
            self.assertIsNone(re.search(r'\b(sorry|admit|unsafe|native_decide|axiom)\b',code))
    def test_actual_root_and_own_output_consumer(self):
        b=self.binding();raw=(HERE/'proof-result.json').read_bytes();self.assertEqual(sha(raw),b['actual_gate_record_sha256'])
        p=json.loads(raw);self.assertEqual(p['actual_proved_roots'],1);self.assertEqual(len(p['records']),2)
        a,c=p['records'];self.assertEqual(c['selected_direct_provider_sha256'],a['own_output_sha256'])
        self.assertEqual(c['direct_provider'],'OWN/CachedSetupProof.olean')
        for r in p['records']:
            self.assertEqual(r['exit_code'],0);self.assertFalse(r['timeout'])
            self.assertEqual(len(r['axiom_reports']),1)
            self.assertEqual(r['axiom_reports'][0]['name'],b['root'])
            self.assertEqual(set(r['axiom_reports'][0]['axioms']),{'propext','Classical.choice','Quot.sound'})
    def test_actual_failure_and_exact_proof_only_successor_preserved(self):
        b=self.binding()['archive'];self.assertEqual(sha((HERE/b['file']).read_bytes()),b['sha256'])
        with ZipFile(HERE/b['file']) as z:
            self.assertEqual(set(z.namelist()),set(b['members']));self.assertEqual(len(z.namelist()),10)
            for n,m in b['members'].items():self.assertEqual((len(z.read(n)),sha(z.read(n))),(m['bytes'],m['sha256']))
            p=json.loads(z.read('C165/proof-result.json'));self.assertEqual(p['records'][0]['exit_code'],1)
            self.assertEqual(p['actual_proved_roots'],0)
            self.assertIn(b'sorryAx',z.read('C165/CachedSetupProof-feedback.txt'))
            self.assertEqual(z.read('C162/SetupProofChecks.lean'),z.read('C166/SetupProofChecks.lean'))
            m=json.loads(z.read('C166/input-manifest.json'))
            self.assertFalse(m['predecessor']['executable_bodies_or_root_type_changed'])
            source=z.read('C162/CachedSetupProof.lean').decode()
            for old,new in m['predecessor']['proof_only_replacements']:
                self.assertEqual(source.count(old),1);source=source.replace(old,new)
            self.assertEqual(source.encode(),(HERE/'CachedSetupProof.lean').read_bytes())
    def test_not_full_cost_or_scientific_root(self):
        b=self.binding();p=json.loads((HERE/'proof-result.json').read_bytes())
        for k in ['full_resource_cost','full_construction_refinement','scientific_ROOT','main_merged']:self.assertFalse(b[k])
        for k in ['full_middle_or_cached_chain_refinement','full_bit_or_GCD_or_evaluator_cost','clean_transitive_TCB']:self.assertFalse(p[k])

if __name__=='__main__':unittest.main()
