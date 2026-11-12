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

class Forensics(unittest.TestCase):
    def test_parent_exact_scope(self):
        r=json.loads((ROOT/'parent-intake-receipt.json').read_bytes())
        self.assertEqual((r['source_input_pins'],r['private_members']),(31,6))
        self.assertTrue(r['all_lengths_hashes_match']);self.assertEqual(r['accepted_roots'],0)
    def test_diagnosis_does_not_certify_repair(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            r=json.loads(z.read('hermite-c315-chain-carrier-forensics/FORENSIC_FREEZE_SEAL.json'))
            self.assertTrue(r['interpretation']['no_mathematical_refutation_or_Lean_bug_claim'])
            for finding in r['two_findings']:self.assertFalse(finding['implemented_or_compiled'])
