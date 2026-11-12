import hashlib,json,re,sys,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[3]))
from tools.proof_trust import strip_lean_comments_and_strings
sha=lambda b:hashlib.sha256(b).hexdigest()
class ChainValues(unittest.TestCase):
    def binding(self):return json.loads((HERE/'source-binding.json').read_bytes())
    def test_actual_sources_no_holes(self):
        b=self.binding()
        for n,k in [('CachedChainValueProof.lean','source_sha256'),('ChainValueProofChecks.lean','consumer_sha256')]:
            raw=(HERE/n).read_bytes();self.assertEqual(sha(raw),b[k])
            self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b',strip_lean_comments_and_strings(raw.decode())))
    def test_exact_own_output_five_roots_and_types(self):
        b=self.binding();raw=(HERE/'proof-result.json').read_bytes();self.assertEqual(sha(raw),b['record_sha256'])
        p=json.loads(raw);a,c=p['records'];self.assertEqual(p['actual_proved_roots'],5)
        self.assertEqual(c['selected_direct_provider_hashes'],[a['own_output_sha256']])
        self.assertTrue(p['five_exact_typed_consumers_checked']);self.assertTrue(p['actual_loaded_definition_prints_in_consumer'])
        extra={'HermiteCachedPiecewiseStored.rightSetup_values','HermiteCachedPiecewiseStored.actual_cache_middle'}
        self.assertEqual({r['name'] for r in c['axiom_reports']},set(b['public_roots'])|extra)
        self.assertEqual(len(c['axiom_reports']),7)
        for r in c['axiom_reports']:self.assertEqual(set(r['axioms']),{'propext','Classical.choice','Quot.sound'})
        for r in [a,c]:self.assertEqual(r['exit_code'],0);self.assertFalse(r['timeout'])
    def test_original19_and_distinct_failure_classes(self):
        r=self.binding()['archive'];self.assertEqual(sha((HERE/r['file']).read_bytes()),r['sha256'])
        with ZipFile(HERE/r['file']) as z:
            self.assertEqual(len(z.namelist()),19);self.assertEqual(set(z.namelist()),set(r['members']))
            for n,m in r['members'].items():self.assertEqual((len(z.read(n)),sha(z.read(n))),(m['bytes'],m['sha256']))
            d=json.loads(z.read('hermite-c185-repaired-chain-value-proof/proof-result.json'))
            self.assertEqual(d['records'][0]['state'],'ENV_DEFERRED');self.assertNotIn('exit_code',d['records'][0])
            for packet in ['hermite-c180-same-chain-value-proof','hermite-c186-low-memory-chain-value-proof','hermite-c191-fin-index-chain-value-proof']:
                p=json.loads(z.read(packet+'/proof-result.json'));self.assertEqual(p['actual_proved_roots'],0)
                self.assertEqual(len(p['records']),1);self.assertEqual(p['records'][0]['exit_code'],1)
            self.assertIn(b'excessive memory consumption',z.read('hermite-c191-fin-index-chain-value-proof/CachedChainValueProof-feedback.txt'))
    def test_no_cost_root_or_main_promotion(self):
        b=self.binding()
        for k in ['independent_review','full_native_bit_or_quantum_cost','scientific_ROOT','main_merged','PURIFIED']:self.assertFalse(b[k])
        p=json.loads((HERE/'proof-result.json').read_bytes())
        self.assertFalse(p['full_resource_accounting_or_finitebit_ROOT']);self.assertFalse(p['clean_transitive_TCB'])
if __name__=='__main__':unittest.main()
