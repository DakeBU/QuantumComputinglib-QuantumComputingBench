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

class ValueFrontier(unittest.TestCase):
    def test_accepted_scalar_is_reused(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes())
        self.assertEqual(r['prior_accepted_scalar_roots'],3)
        self.assertEqual(r['records'][0]['selected_provider_hashes'][0],'cab232830420ff84aae508599b0ecd2f8ad696ef681a3c1e8e365454164ffc60')
        if r['status']=='PROVED_LOCALLY_FOCUSED':
            self.assertEqual(r['actual_own_consumed_public_roots'],7)
            a,b=r['records'];self.assertEqual(b['selected_provider_hashes'],[a['own_output_sha256']])
            self.assertEqual(len(b['axiom_reports']),7)
        else:self.assertEqual(r['actual_own_consumed_public_roots'],0)
        self.assertFalse(r['same_run_cost_or_finitebit_or_scientific_ROOT'])
    def test_prior_failed_chain_is_not_accepted(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            r=json.loads(z.read('hermite-c301-common-discriminant-probe-first-value-proof/proof-result.json'))
            self.assertEqual(r['actual_own_consumed_public_roots'],3)
            self.assertIsNone(r['records'][-1]['own_output_sha256'])
            self.assertEqual(r['records'][-1]['exit_code'],1)
