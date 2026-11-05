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

class SourceAnalysis(unittest.TestCase):
    def test_actual_source_not_global_certificate(self):
        r=json.loads((ROOT/'parent-intake.json').read_bytes())
        self.assertTrue(r['parent_whole_three_files_read']);self.assertTrue(r['all_hashes_match'])
        self.assertEqual((r['source_pins'],r['payloads']),(25,2))
        self.assertFalse(r['proposed_global_height_bound_proved'])
        self.assertFalse(r['actual_Sites_or_native_or_quantum_ROOT'])
