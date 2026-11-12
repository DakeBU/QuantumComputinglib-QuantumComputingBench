import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class Review(unittest.TestCase):
    def test_exact_originals(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes())
        self.assertEqual(sha((ROOT/'original-freezes.zip').read_bytes()),b['archive_sha256'])
        with ZipFile(ROOT/'original-freezes.zip') as z:
            self.assertEqual(set(z.namelist()),set(b['original_members']))
            for n,r in b['original_members'].items():
                raw=z.read(n);self.assertEqual((len(raw),sha(raw)),(r['bytes'],r['sha256']))
    def test_parent_scope(self):
        r=json.loads((ROOT/'parent-intake-receipt.json').read_bytes())
        self.assertEqual((r['source_first_input_pins'],r['static_input_pins'],r['recorded_runtime_input_pins'],r['private_runtime_members']),(23,24,43,10))
        self.assertTrue(r['all_listed_lengths_hashes_match']);self.assertFalse(r['independent_compiler_rerun'])
        self.assertFalse(r['source_publication_or_scientific_ROOT'])
    def test_association_is_not_clean_loader_or_native_certificate(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            r=json.loads(z.read('hermite-c308-common-denominator-runtime-association/INPUT_MANIFEST.json'))
            self.assertTrue(r['association']['unresolved_lexical_Init_vs_prefix_provenance_limit'])
            self.assertFalse(r['association']['source_zero_rows_are_empty_axiom_proof'])
