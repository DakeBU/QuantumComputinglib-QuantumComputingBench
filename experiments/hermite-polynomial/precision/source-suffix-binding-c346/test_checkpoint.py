import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class ExactCheckpoint(unittest.TestCase):
    def test_exact_archived_originals(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes())
        for n,h in b['payloads'].items():self.assertEqual(sha((ROOT/n).read_bytes()),h,n)
        self.assertEqual(sha((ROOT/'original-freezes.zip').read_bytes()),b['archive_sha256'])
        with ZipFile(ROOT/'original-freezes.zip') as z:
            self.assertEqual(set(z.namelist()),set(b['original_members']))
            for n,r in b['original_members'].items():
                raw=z.read(n);self.assertEqual((len(raw),sha(raw)),(r['bytes'],r['sha256']))
        self.assertFalse(b['main_merged']);self.assertFalse(b['scientific_ROOT'])

class ExactInternalProof(unittest.TestCase):
    def test_exact_new_own_output_and_ordinary_axioms(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes());a,b=r['records']
        self.assertEqual(r['status'],'PROVED_LOCALLY_FOCUSED');self.assertEqual(r['actual_own_consumed_roots'],1)
        self.assertEqual([a['exit_code'],b['exit_code']],[0,0])
        self.assertEqual(b['selected_direct_provider_hashes'],[a['own_output_sha256']])
        self.assertEqual([len(a['axiom_reports']),len(b['axiom_reports'])],[1,2])
        for row in a['axiom_reports']+b['axiom_reports']:self.assertEqual(set(row['axioms']),{'propext','Classical.choice','Quot.sound'})
        self.assertFalse(r['producer_Sites_or_native_or_quantum_scientific_ROOT']);self.assertFalse(r['independent_review'])
    def test_exact_source_and_consumer_bytes(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes())
        for row in r['records']:self.assertEqual(row['source_sha256'],sha((ROOT/(row['module']+'.lean')).read_bytes()))

    def test_original_failure_never_imported_and_not_hidden(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            r=json.loads(z.read('hermite-c346-source-suffix-binding-proof/attempt-01/result.json'))
            self.assertEqual(r['exit_code'],1);self.assertIsNone(r['own_sha256']);self.assertEqual(r['accepted_roots'],0)
            self.assertEqual(z.read('hermite-c346-source-suffix-binding-proof/attempt-02/SourceSuffixBindingProof.lean'),(ROOT/'SourceSuffixBindingProof.lean').read_bytes())
        p=json.loads((ROOT/'failure-privacy-binding.json').read_bytes())
        self.assertEqual(p['public_sanitized_sha256'],sha((ROOT/'prior-failed-feedback-sanitized.txt').read_bytes()))
        self.assertFalse(p['prior_failed_own_output_imported'])
