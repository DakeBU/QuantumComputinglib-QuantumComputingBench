import hashlib,json,re,sys,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[3]))
from tools.proof_trust import strip_lean_comments_and_strings
sha=lambda b:hashlib.sha256(b).hexdigest()

def validate(root):
    b=json.loads((root/'source-binding.json').read_bytes())
    for name,key in [('CachedSameRunProof.lean','source_sha256'),('SameRunProofChecks.lean','consumer_sha256'),
                     ('proof-result.json','record_sha256'),('proof-feedback.txt','source_feedback_sha256'),
                     ('consumer-feedback.txt','consumer_feedback_sha256')]:
        if sha((root/name).read_bytes())!=b[key]:raise ValueError('evidence byte mismatch')
    a=b['archive']
    if sha((root/a['file']).read_bytes())!=a['sha256']:raise ValueError('archive byte mismatch')
    with ZipFile(root/a['file']) as z:
        if len(z.namelist())!=10 or set(z.namelist())!=set(a['members']):raise ValueError('archive inventory mismatch')
        for n,m in a['members'].items():
            if (len(z.read(n)),sha(z.read(n)))!=(m['bytes'],m['sha256']):raise ValueError('original byte mismatch')
    return b,json.loads((root/'proof-result.json').read_bytes())

class SameReturnedRun(unittest.TestCase):
    def test_exact_sources_and_no_holes(self):
        validate(HERE)
        for n in ['CachedSameRunProof.lean','SameRunProofChecks.lean']:
            self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b',
                strip_lean_comments_and_strings((HERE/n).read_text(encoding='utf-8'))))
    def test_own_output_consumed_at_exact_type(self):
        b,p=validate(HERE);a,c=p['records']
        self.assertEqual(p['status'],'PROVED_LOCALLY_FOCUSED');self.assertEqual(p['actual_proved_roots'],1)
        self.assertEqual(c['selected_direct_provider_hashes'],[a['own_output_sha256']])
        self.assertEqual(a['own_output_sha256'],'6ca8d334addc44e0ac928fa21498e9e21dcd799587a565f277195797d5d4a555')
        self.assertEqual(a['axiom_reports'],[])
        self.assertFalse(p['source_zero_rows_are_empty_axiom_proof'])
        self.assertEqual([r['name'] for r in c['axiom_reports']],b['public_roots'])
        self.assertEqual(set(c['axiom_reports'][0]['axioms']),{'propext','Classical.choice','Quot.sound'})
        for r in p['records']:
            self.assertEqual(r['exit_code'],0);self.assertFalse(r['timeout']);self.assertTrue(r['ordinary_axioms_only'])
        source=(HERE/'CachedSameRunProof.lean').read_text(encoding='utf-8')
        signature=source.split('theorem produceCachedStored_same_run :',1)[1].split(':= by',1)[0]
        self.assertIn('let result := produceCachedStored k n R delta',signature)
        self.assertIn('denoteChain result.value = actualChain k n R delta ∧',signature)
        self.assertIn('StoredRectangularGivens.total result.cost',signature)
        self.assertNotIn('→',signature)
    def test_timeout_failure_preserved_not_promoted(self):
        b,_=validate(HERE)
        with ZipFile(HERE/b['archive']['file']) as z:
            old=json.loads(z.read('hermite-c207-actual-same-run-proof/proof-result.json'))
            self.assertEqual(old['actual_proved_roots'],0);self.assertEqual(len(old['records']),1)
            self.assertEqual(old['records'][0]['exit_code'],1)
            self.assertIsNone(old['records'][0]['own_output_sha256'])
            self.assertIn(b'200000',z.read('hermite-c207-actual-same-run-proof/CachedSameRunProof-feedback.txt'))
    def test_partial_scope_not_full_resource_or_review(self):
        b,p=validate(HERE)
        for k in ['independent_review','full_native_bit_or_quantum_cost','scientific_ROOT','main_merged','PURIFIED']:
            self.assertFalse(b[k])
        self.assertFalse(p['clean_transitive_TCB']);self.assertFalse(p['physical_one_evaluation_or_sharing'])
        self.assertTrue(p['inherited_cache_consumer_and_accounted_traffic_not_fresh_rebuilt'])
        self.assertFalse(p['full_native_bit_GCD_or_quantum_resources'])
        self.assertIn('total (rightSetup n R delta).cost',(HERE/'consumer-feedback.txt').read_text(encoding='utf-8'))
    def test_missing_or_modified_evidence_fails_closed(self):
        import tempfile,shutil
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            for n in ['source-binding.json','CachedSameRunProof.lean','SameRunProofChecks.lean']:
                shutil.copyfile(HERE/n,root/n)
            with self.assertRaises(FileNotFoundError):validate(root)
            (root/'CachedSameRunProof.lean').write_bytes(b'changed')
            with self.assertRaises(ValueError):validate(root)

if __name__=='__main__':unittest.main()
