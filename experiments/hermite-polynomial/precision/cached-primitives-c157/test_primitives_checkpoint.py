import hashlib,json,re,sys,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[3]))
from tools.proof_trust import strip_lean_comments_and_strings
sha=lambda b:hashlib.sha256(b).hexdigest()

class Primitives(unittest.TestCase):
    def binding(self):return json.loads((HERE/'source-binding.json').read_bytes())

    def test_all_exact_source_files_required(self):
        b=self.binding();self.assertEqual(len(b['sources']),6)
        for name,h in b['sources'].items():self.assertEqual(sha((HERE/name).read_bytes()),h)
        self.assertEqual(b['sources']['CachedPrimitivesProof.lean'],'f267071f622a45f3ed68f15cd93d5483e70bae903135ba9edb3bd86926eb737b')
        self.assertEqual(b['sources']['PrimitiveProofChecks.lean'],'1326bb9dcba2b84ce406968f5d77f631866b6c0aead979dbcc61b779f8d18c48')

    def test_actual_seven_roots_and_fresh_output_consumer(self):
        b=self.binding();raw=(HERE/'proof-result.json').read_bytes();self.assertEqual(sha(raw),b['actual_gate_record_sha256'])
        p=json.loads(raw);self.assertEqual(p['status'],'PROVED_LOCALLY_FOCUSED');self.assertEqual(p['actual_proved_roots'],7)
        self.assertEqual(len(p['records']),2)
        a,c=p['records'];self.assertEqual(c['selected_direct_provider_sha256'],a['own_output_sha256'])
        self.assertEqual(c['direct_provider'],'OWN/CachedPrimitivesProof.olean')
        for r in p['records']:
            self.assertEqual(r['exit_code'],0);self.assertFalse(r['timeout'])
            self.assertEqual(len(r['axiom_reports']),7)
            self.assertEqual({x['name'] for x in r['axiom_reports']},set(b['actual_root_names']))
            for x in r['axiom_reports']:self.assertEqual(set(x['axioms']),{'propext','Classical.choice','Quot.sound'})

    def test_no_hidden_full_root_or_runtime_promotion(self):
        b=self.binding();p=json.loads((HERE/'proof-result.json').read_bytes())
        self.assertFalse(b['scientific_ROOT']);self.assertFalse(b['main_merged']);self.assertFalse(b['independent_review'])
        self.assertFalse(p['full_middle_or_cached_chain_refinement'])
        self.assertFalse(p['full_bit_or_GCD_or_evaluator_cost']);self.assertFalse(p['clean_transitive_TCB'])
        self.assertEqual(p['statement_seal_sha256'],b['exact_preproof_seal'])

    def test_original_author_freeze_exact_and_not_rewritten(self):
        row=self.binding()['author_archive'];self.assertEqual(sha((HERE/row['file']).read_bytes()),row['sha256'])
        with ZipFile(HERE/row['file']) as z:
            self.assertEqual(set(z.namelist()),set(row['members']));self.assertEqual(len(z.namelist()),5)
            for n,m in row['members'].items():self.assertEqual((len(z.read(n)),sha(z.read(n))),(m['bytes'],m['sha256']))
            m=json.loads(z.read('input-manifest.json'));self.assertFalse(m['execution']['compiler'])
            self.assertFalse(m['actual_roots_proved'])

    def test_no_new_trust_shortcuts_in_sources(self):
        pattern=r'\b(sorry|admit|unsafe|native_decide|axiom)\b'
        for name in self.binding()['sources']:
            source=strip_lean_comments_and_strings((HERE/name).read_text(encoding='utf-8'))
            self.assertIsNone(re.search(pattern,source))
        self.assertIsNone(re.search(pattern,strip_lean_comments_and_strings('/- axiom in prose -/')))
        self.assertIsNotNone(re.search(pattern,strip_lean_comments_and_strings('/- harmless -/\naxiom bad : True')))

if __name__=='__main__':unittest.main()
