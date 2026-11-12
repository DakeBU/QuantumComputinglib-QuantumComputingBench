import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class ExactBindings(unittest.TestCase):
    def test_payloads_and_exact_originals(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes())
        for n,h in b['payloads'].items():self.assertEqual(sha((ROOT/n).read_bytes()),h,n)
        with ZipFile(ROOT/'original-freezes.zip') as z:
            self.assertEqual(set(z.namelist()),set(b['original_members']))
            for n,r in b['original_members'].items():
                raw=z.read(n);self.assertEqual(len(raw),r['bytes']);self.assertEqual(sha(raw),r['sha256'])
        self.assertFalse(b['scientific_ROOT']);self.assertFalse(b['main_merged'])

class HeightReview(unittest.TestCase):
    def test_parent_scope(self):
        r=json.loads((ROOT/'parent-intake-receipt.json').read_bytes())
        self.assertEqual((r['raw_input_pins'],r['private_archive_members']),(31,10))
        self.assertTrue(r['raw_and_payload_lengths_hashes_match'])
        self.assertFalse(r['independent_compiler_rerun'])
        self.assertFalse(r['source_publication_or_scientific_ROOT'])
    def test_separate_freezes_and_unchanged_one_root(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            r=json.loads(z.read('hermite-c291-height-bound-runtime-association/INPUT_MANIFEST.json'))
            self.assertEqual(r['actual_binding']['focused_roots'],1)
            self.assertFalse(r['actual_binding']['consumer_alias_is_second_scientific_root'])
            self.assertFalse(r['actual_binding']['zero_source_rows_are_empty_axiom_proof'])
            self.assertFalse(r['provider_boundary']['MinMax']['fresh_source_binary_audit'])
