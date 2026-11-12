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

class Representation(unittest.TestCase):
    def test_new_own_output_exact_consumer(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes());a,b=r['records']
        self.assertEqual(r['actual_own_consumed_roots'],1)
        self.assertEqual([a['exit_code'],b['exit_code']],[0,0])
        self.assertEqual(b['selected_direct_provider_hashes'],[a['own_output_sha256']])
        for row in b['axiom_reports']:self.assertEqual(set(row['axioms']),{'propext','Classical.choice','Quot.sound'})
        self.assertFalse(r['primitiveWidth_proved']);self.assertFalse(r['independent_review'])
    def test_only_notation_repaired_after_preserved_failure(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            old=z.read('hermite-c298-primitive-representation-proof/PrimitiveRepresentationProof.lean')
            new=z.read('hermite-c305-primitive-representation-notation-repair/PrimitiveRepresentationProof.lean')
            self.assertEqual(old.replace('w.numerator /. (w.denominator : ℤ)'.encode(),'Rat.divInt w.numerator (w.denominator : ℤ)'.encode()),new)
            r=json.loads(z.read('hermite-c303-primitive-representation-proof/proof-result.json'))
            self.assertEqual(r['actual_own_consumed_roots'],0);self.assertEqual(len(r['records']),1)
