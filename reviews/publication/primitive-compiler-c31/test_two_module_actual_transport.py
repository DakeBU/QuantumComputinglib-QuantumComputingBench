"""Recheck actual two-module and original-review transport without claiming acceptance."""
import hashlib,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
class TwoModuleTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/'reports/lean-433-migration/c31-two-module-actual-review-transport.json').read_bytes())
        cls.data=[]
        for row in cls.r['bundles']:
            with zipfile.ZipFile(ROOT/row['path']) as z:cls.data.append({n:z.read(n) for n in z.namelist()})
    def test_both_exact_partitions_and_all_payloads(self):
        self.assertEqual([len(f) for f in self.data],[11,8])
        for row,files in zip(self.r['bundles'],self.data):
            self.assertEqual(hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest(),row['sha256'])
            for m in row['members']:
                self.assertEqual(len(files[m['path']]),m['bytes'])
                self.assertEqual(hashlib.sha256(files[m['path']]).hexdigest(),m['sha256'])
    def test_all_156_actual_records_not_count_only(self):
        roots=json.loads(self.data[0]['root-contract-comparisons.json'])['roots']
        generated=json.loads(self.data[0]['generated-observations.json'])['rows']
        self.assertEqual((len(roots),len(generated)),(62,94))
        with zipfile.ZipFile(ROOT/'reviews/publication/primitive-compiler-c31/ci4-success-native-blockers-public.zip') as z:
            text=z.read('30-observe.stdout.raw.sanitized.txt').decode()
        actual={}
        for line in text.splitlines():
            tag,sep,payload=line.partition(' ')
            if tag in ('C31_ROOT_JSON','C31_GENERATED_JSON'):
                r=json.loads(payload);actual[r['actualName']]=r
        for row in [r['actualObservation'] for r in roots]+generated:
            self.assertEqual(row,actual[row['actualName']]);self.assertFalse(row['selfOccursInAxioms']);self.assertFalse(row['isUnsafe'])
        report=json.loads(self.data[0]['report.json'])
        self.assertEqual([m['owned'] for m in report['modules']],[98,58])
        self.assertEqual([r['name'] for r in report['oldCatalogDefects']],['QuantumBlockEncoding.hadamardMatrix_apply'])
    def test_late_binding_pending_and_parent_pointer_error_preserved(self):
        self.assertEqual(len(self.r['prospective_bindings']),2)
        self.assertIn(b"parent's first Phase4 directory pointer",self.data[1]['phase4-metadata-alignment-review.md'])
        self.assertFalse(self.r['registry_changed']);self.assertFalse(self.r['source_catalog_changed'])
        for key in ('nativeAccepted','scientific_ROOT','main_admission','PURIFIED'):self.assertFalse(self.r[key])
        self.assertIsNone(self.r['sourceAgreement']);self.assertIsNone(self.r['publicationBinding'])
if __name__=='__main__':unittest.main()
