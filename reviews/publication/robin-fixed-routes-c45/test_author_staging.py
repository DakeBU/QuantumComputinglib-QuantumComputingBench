"""Author packet integrity only; explicitly not independent semantic acceptance."""
import hashlib,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
class AuthorRecoveryTests(unittest.TestCase):
    def test_every_author_payload_is_present_and_exact(self):
        p=ROOT/'reviews/publication/robin-fixed-routes-c45/author-recovery-original152.zip'
        with zipfile.ZipFile(p) as z:
            self.assertEqual(len(z.namelist()),152)
            seal=json.loads(z.read('seal.json'))
            for row in seal['outputFileDigests']:
                raw=z.read(row['path'])
                self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])
                self.assertEqual(len(raw),row['bytes'])
            self.assertIn('whole-module semantic author audit incomplete',seal['scope']['robinMatrix'])
            self.assertIn('INDEPENDENTLY_REVIEWED',seal['notState'])
    def test_every_raw_author_input_still_matches(self):
        with zipfile.ZipFile(ROOT/'reviews/publication/robin-fixed-routes-c45/author-recovery-original152.zip') as z:
            before=json.loads(z.read('pins-before.json'));after=json.loads(z.read('pins-after.json'))
            pins=before['formalSources']+before['naturalAndProtocols']
            self.assertEqual(len(pins),63)
            self.assertEqual(after['files'],[{k:r[k] for k in ('path','sha256','bytes')} for r in pins])
            self.assertEqual(after['changed'],[])
            for row in pins:self.assertEqual(hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest(),row['sha256'])
if __name__=='__main__':unittest.main()
