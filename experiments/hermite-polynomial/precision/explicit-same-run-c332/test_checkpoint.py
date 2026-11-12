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

class SameResult(unittest.TestCase):
    def test_exact_own_output_and_suppliers(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes());a,b=r['records']
        self.assertEqual(r['actual_own_consumed_roots'],1);self.assertTrue(r['C250_all_eight_local_interfaces_closed'])
        self.assertEqual(b['selected_provider_hashes'],[a['own_output_sha256']])
        self.assertEqual(len(a['axiom_reports']),1);self.assertEqual(len(b['axiom_reports']),4)
        for row in a['axiom_reports']+b['axiom_reports']:self.assertEqual(set(row['axioms']),{'propext','Classical.choice','Quot.sound'})
        self.assertFalse(r['native_bit_GCD_CPU_allocation_physical_sharing_or_quantum_scientific_ROOT'])
    def test_prior_import_failure_and_unchanged_source(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            failed=json.loads(z.read('hermite-c335-explicit-same-run-composition-gate/proof-result.json'))
            self.assertEqual(failed['actual_own_consumed_roots'],0);self.assertEqual(failed['records'][0]['exit_code'],1)
            self.assertEqual(failed['records'][0]['source_sha256'],sha((ROOT/'SameRunProof.lean').read_bytes()))
        c=json.loads((ROOT/'prior-import-failure.json').read_bytes());self.assertEqual(c['failure_class'],'ENV_BLOCKED')
        self.assertFalse(c['mathematical_refutation']);self.assertFalse(c['consumer_run'])
    def test_no_public_drive_path_in_sanitized_feedback(self):
        import re
        b=(ROOT/'prior-import-feedback-sanitized.txt').read_bytes()
        self.assertIsNone(re.search(rb'(?i)[a-z]:[\/]',b))
        c=json.loads((ROOT/'feedback-privacy-binding.json').read_bytes());self.assertEqual(sha(b),c['public_sanitized_sha256'])
