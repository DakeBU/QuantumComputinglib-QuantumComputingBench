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

class EnvironmentDeferred(unittest.TestCase):
    def test_no_compiler_or_proof_failure_in_either_attempt(self):
        for tag,cap in [('initial',3072),('lower',1536)]:
            r=json.loads((ROOT/(tag+'-memory-deferral.json')).read_bytes())
            p=json.loads((ROOT/(tag+'-memory-plan.json')).read_bytes())
            self.assertEqual(r['actual_own_consumed_roots'],0);self.assertEqual(len(r['records']),1)
            row=r['records'][0];self.assertEqual(row['state'],'ENV_DEFERRED_BEFORE_COMPILER')
            self.assertNotIn('exit_code',row)
            self.assertEqual(p['memory_cap_MiB'],cap);self.assertEqual(p['reserve_MiB'],2048)
            self.assertLess(row['available_MiB'],cap+2048)
            self.assertEqual(p['source_sha256'],sha((ROOT/'ReturnedSourceCacheProof.lean').read_bytes()))
            self.assertEqual(p['consumer_sha256'],sha((ROOT/'ExpandedChecks.lean').read_bytes()))
            self.assertFalse(r['all_three_C345_local_roots_proved'])
