import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class BindingTests(unittest.TestCase):
    def test_bound_payloads(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes())
        for n,h in b['payloads'].items(): self.assertEqual(sha((ROOT/n).read_bytes()),h,n)
        self.assertFalse(b['scientific_ROOT']);self.assertFalse(b['main_merged'])
    def test_original_archive_members(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes())
        a=b['archive'];raw=(ROOT/a['file']).read_bytes();self.assertEqual(sha(raw),a['sha256'])
        with ZipFile(ROOT/a['file']) as z:
            self.assertEqual(set(z.namelist()),set(a['members']))
            for n,r in a['members'].items():
                x=z.read(n);self.assertEqual(len(x),r['bytes']);self.assertEqual(sha(x),r['sha256'])
