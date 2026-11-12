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

class PolynomialLedger(unittest.TestCase):
    def test_two_actual_roots_and_same_own_output(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes());a,b=r['records']
        self.assertEqual(r['actual_own_consumed_roots'],2)
        self.assertEqual([a['exit_code'],b['exit_code']],[0,0])
        self.assertEqual(b['selected_direct_provider_hashes'],[a['own_output_sha256']])
        self.assertEqual(len(a['axiom_reports']),2);self.assertEqual(len(b['axiom_reports']),5)
        for row in a['axiom_reports']+b['axiom_reports']:self.assertEqual(set(row['axioms']),{'propext','Classical.choice','Quot.sound'})
    def test_not_a_native_or_quantum_certificate(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes())
        self.assertFalse(r['actual_producer_height_native_GCD_evaluator_allocation_or_scientific_ROOT'])
        self.assertFalse(r['independent_review']);self.assertFalse(r['clean_transitive_TCB'])
        s=(ROOT/'AllocatedPolynomialLedgerOwnChecks.lean').read_text()
        self.assertIn('result.quotientCalls',s);self.assertIn('result.remainderCalls',s)
