import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class Bindings(unittest.TestCase):
    def test_payloads(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes())
        for n,h in b['payloads'].items():self.assertEqual(sha((ROOT/n).read_bytes()),h,n)
        self.assertFalse(b['scientific_ROOT']);self.assertFalse(b['main_merged'])
    def test_original_members(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes());a=b['archive']
        self.assertEqual(sha((ROOT/a['file']).read_bytes()),a['sha256'])
        with ZipFile(ROOT/a['file']) as z:
            self.assertEqual(set(z.namelist()),set(a['members']))
            for n,r in a['members'].items():
                x=z.read(n);self.assertEqual(len(x),r['bytes']);self.assertEqual(sha(x),r['sha256'])

class FailureFrontier(unittest.TestCase):
    def test_failed_probe_does_not_launch_value_lane(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes())
        self.assertEqual(len(r['records']),1);self.assertEqual(r['records'][0]['module'],'Probe')
        self.assertEqual(r['records'][0]['exit_code'],1);self.assertIsNone(r['records'][0]['own_output_sha256'])
        self.assertFalse(r['interface_probe_own_consumed']);self.assertEqual(r['actual_own_consumed_public_roots'],0)
    def test_frozen_scientific_scalar_unchanged_by_probe_repair(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            a=z.read('hermite-c275-constructor-iota-probe-and-successor/ExplicitScalarValueProof.lean')
            b=z.read('hermite-c281-probe-reflexivity-successor/ExplicitScalarValueProof.lean')
            self.assertEqual(a,b)
            r=json.loads(z.read('hermite-c265-explicit-five-block-value-successor-proof/preflight-failure.json'))
            self.assertEqual(r['compiler_invocations'],0);self.assertFalse(r['mathematical_refutation'])
