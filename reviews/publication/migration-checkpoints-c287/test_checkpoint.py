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

class ScopedReviews(unittest.TestCase):
    def test_static_then_separate_runtime_freeze(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            a=json.loads(z.read('hermite-c264-explicit-cost-independent-static-review/REVIEW_FREEZE_SEAL.json'))
            b=json.loads(z.read('hermite-c273-explicit-cost-runtime-association/REVIEW_FREEZE_SEAL.json'))
            raw=z.read('hermite-c264-explicit-cost-independent-static-review/REVIEW_FREEZE_SEAL.json')
            self.assertEqual(b['immutable_static_parent_seal']['sha256'],sha(raw))
            self.assertEqual(a['status'],'STATIC_FROZEN_STOP_BEFORE_RUNTIME')
            self.assertFalse(b['source_zero_axiom_rows_are_empty_axiom_proof'])
    def test_scope_and_parent_hash_verification(self):
        r=json.loads((ROOT/'parent-intake-receipt.json').read_bytes())
        self.assertEqual(r['direct_raw_bindings'],34);self.assertEqual(r['private_archive_members'],10)
        self.assertTrue(r['all_listed_lengths_and_hashes_match'])
        self.assertFalse(r['independent_compiler_rerun']);self.assertFalse(r['complete_loader_or_clean_transitive_TCB'])
        self.assertFalse(r['publication_or_main_admitted'])
