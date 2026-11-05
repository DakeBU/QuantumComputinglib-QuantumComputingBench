"""Transport and honest phase boundaries, not mathematical equivalence tests."""
import hashlib,json,re,unittest
from pathlib import Path
from zipfile import ZipFile

BASE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class FrozenReviewTests(unittest.TestCase):
    def test_exact_members_and_original_seals(self):
        o=json.loads((BASE/'index.json').read_bytes())
        self.assertEqual((o['archive_count'],o['member_count']),(2,51))
        for a in o['archives']:
            self.assertEqual(sha((BASE/a['archive']).read_bytes()),a['sha256'])
            with ZipFile(BASE/a['archive']) as z:
                self.assertEqual(set(z.namelist()),set(a['members']))
                for n,r in a['members'].items():
                    self.assertEqual((sha(z.read(n)),len(z.read(n))),(r['sha256'],r['bytes']))
                self.assertEqual(sha(z.read(a['seal'])),a['seal_sha256'])
                self.assertEqual(sha(z.read(a['manifest'])),a['manifest_sha256'])
    def test_no_public_host_paths_or_credentials(self):
        for p in BASE.glob('*.zip'):
            with ZipFile(p) as z:
                for n in z.namelist():
                    s=z.read(n).decode('utf-8-sig')
                    for _ in range(2):s=s.replace('\\\\','\\')
                    self.assertIsNone(re.search(r'(?<![A-Za-z0-9])[A-Za-z]:[/\\]',s),n)
                    self.assertNotIn('/'+'home/runner/',s)
                    self.assertIsNone(re.search(r'(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]{20,}',s))
    def test_robin_whole_freeze_is_before_actual_decoder(self):
        with ZipFile(BASE/'robin-c104-own-formal-first-original.zip') as z:
            o=json.loads(z.read('own-formal-first-seal.json'))
            self.assertEqual(o['phase'],'OWN_WHOLE_FORMAL_FIRST_FROZEN_BEFORE_ACTUAL_DECODER')
            self.assertEqual(len(o['public_safe_membership']),40)
    def test_no_integration_or_scientific_admission(self):
        o=json.loads((BASE/'index.json').read_bytes())
        for k in ('publication_admission','production_changed','scientific_ROOT','PURIFIED'):
            self.assertFalse(o[k])
        with ZipFile(BASE/'temporary-and-c110-decoder-comparison-original.zip') as z:
            o=json.loads(z.read('manifest.json'))
            self.assertEqual(o['state'],'THREE_WAY_TEXT_ONLY')
            self.assertEqual(len(o['payload_files']),9)

if __name__=='__main__':unittest.main()
