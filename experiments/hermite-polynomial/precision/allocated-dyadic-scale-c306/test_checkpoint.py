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

class Scale(unittest.TestCase):
    def test_actual_first_scale_root_and_own_consumer(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes());a,b=r['records']
        self.assertEqual(r['actual_own_consumed_roots'],1)
        self.assertEqual(b['selected_direct_provider_hashes'],[a['own_output_sha256']])
        self.assertEqual({x['name'] for x in b['axiom_reports']},{'HermiteAllocatedPolynomialCost.scaleDyadicBound','C306ExactChecks.scaleDyadicExpandedCheck'})
        self.assertFalse(r['other_two_cost_roots_proved']);self.assertFalse(r['independent_review'])
    def test_warnings_retained_and_no_epsilon_upper_restriction(self):
        s=(ROOT/'ExactChecks.lean').read_text(encoding='utf-8')
        self.assertIn('0 < epsilon →',s);self.assertNotIn('epsilon ≤ 1',s)
        self.assertIn('Unused tactic', (ROOT/'AllocatedDyadicScaleProof-feedback.txt').read_text())
