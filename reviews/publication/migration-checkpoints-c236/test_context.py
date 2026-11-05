import hashlib,io,json,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class SuccessorContext(unittest.TestCase):
    def test_exact_originals_and_no_relabel(self):
        i=json.loads((HERE/'index.json').read_bytes());a=i['archive']
        self.assertEqual(sha((HERE/a['file']).read_bytes()),a['sha256'])
        with ZipFile(HERE/a['file']) as z:
            self.assertEqual(len(z.namelist()),7);self.assertEqual(set(z.namelist()),set(a['members']))
            for n,m in a['members'].items():self.assertEqual((len(z.read(n)),sha(z.read(n))),(m['bytes'],m['sha256']))
            c=json.loads(z.read('hermite-c222-successor-governance-context/successor-source-context.json'))
            s=json.loads(z.read('hermite-c224-successor-context-review/GOVERNANCE_REVIEW_SEAL.json'))
            old,new=c['previous_source_context_pins'],c['successor_source_context_pins']
            self.assertEqual(set(old),set(new));self.assertEqual(len(old),35)
            self.assertEqual([p for p in old if old[p]!=new[p]],['HARNESS.md'])
            self.assertTrue(s['removing_raw_insertion_exactly_recovers_original_mixed_bytes'])
            self.assertTrue(s['supplemental_linked_policy']['not_in_35_vector'])
            self.assertFalse(s['C217_proof_compiler_consumer_or_runtime_outputs_opened'])
            with ZipFile(io.BytesIO(z.read('hermite-c222-successor-governance-context/original-and-successor-governance.zip'))) as inner:
                b=inner.read('original-HARNESS.md');n=inner.read('successor-HARNESS.md')
                self.assertEqual(sha(b),old['HARNESS.md']);self.assertEqual(sha(n),new['HARNESS.md'])
                start=n.index(b'## 8a.');end=n.index(b'## 9.',start)
                self.assertEqual(n[:start]+n[end:],b)
        self.assertFalse(i['scientific_or_policy_approval']);self.assertFalse(i['main_merged'])
if __name__=='__main__':unittest.main()
