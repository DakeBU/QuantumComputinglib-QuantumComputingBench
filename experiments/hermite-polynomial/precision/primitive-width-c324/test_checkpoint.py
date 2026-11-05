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

class PrimitiveWidth(unittest.TestCase):
    def test_exact_own_output_and_ordinary_root(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes());a,b=r['records']
        self.assertEqual(r['actual_own_consumed_roots'],1);self.assertTrue(r['primitiveWidth_proved'])
        self.assertEqual(b['selected_direct_provider_hashes'],[a['own_output_sha256']])
        for row in b['axiom_reports']:self.assertEqual(set(row['axioms']),{'propext','Classical.choice','Quot.sound'})
        self.assertFalse(r['actual_producer_height_native_GCD_evaluator_allocation_or_scientific_ROOT'])
    def test_failures_and_stale_metadata_are_preserved(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            for n in ['hermite-c318-primitive-width-proof','hermite-c322-primitive-width-membership-successor']:
                r=json.loads(z.read(n+'/proof-result.json'));self.assertEqual(r['actual_own_consumed_roots'],0)
                self.assertEqual(r['records'][0]['exit_code'],1)
            a=json.loads(z.read('hermite-c321-width-empty-list-repair/input-manifest.json'))
            old=json.loads(z.read('hermite-c310-primitive-width-proof/input-manifest.json'))
            self.assertEqual(a['outputs'],old['outputs'])
            fresh=json.loads(z.read('hermite-c324-width-cap-unfolding-repair/input-manifest.json'))
            self.assertTrue(fresh['current_outputs_not_inherited_ancestor_metadata'])
            actual={row['path']:row['sha256'] for row in fresh['outputs']}
            self.assertEqual(actual['PrimitiveWidthProof.lean'],sha((ROOT/'PrimitiveWidthProof.lean').read_bytes()))
