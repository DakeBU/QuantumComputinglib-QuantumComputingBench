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

class ScopedReview(unittest.TestCase):
    def test_verified_scope_not_broad_acceptance(self):
        r=json.loads((ROOT/'parent-intake-receipt.json').read_bytes())
        self.assertTrue(r['parent_whole_three_files_read']);self.assertTrue(r['all_current_bytes_match'])
        self.assertEqual(r['private_ZIP_members'],10);self.assertEqual(r['payloads'],2)
        for n in ['independent_rerun','clean_transitive_TCB','source_publication','scientific_ROOT']:self.assertFalse(r[n])
    def test_nine_original_phase_files_and_exact_seal(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes());self.assertEqual(len(b['original_members']),9)
        r=json.loads((ROOT/'parent-intake-receipt.json').read_bytes())
        self.assertIn(r['review_seal_sha256'],{v['sha256'] for v in b['original_members'].values()})
