"""Whole-module author WIP and actual resource failure must fail closed."""
import hashlib,importlib.util,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('c36_original_gate',ROOT/'website/scripts/check_research_publications.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
class C36CheckpointTests(unittest.TestCase):
    def test_whole19_inventory_and_prospective_binding(self):
        c=json.loads((HERE/'publication-candidate.json').read_bytes())
        inventory={r['fullName']:r for r in json.loads((ROOT/'web/library/declarations.json').read_bytes())['declarations']}
        actual={n for n,r in inventory.items() if r['source']==c['module']}
        self.assertEqual(len(actual),19);self.assertEqual(set(c['declarations']),actual)
        self.assertEqual(c['binding_sha256'],gate.binding_digest(ROOT,c))
        with self.assertRaisesRegex(ValueError,'missing evidence file'):
            gate.validate_record(ROOT,c,inventory)
        self.assertFalse(c['main_admission']);self.assertFalse(c['scientific_ROOT'])
    def test_source_seal_and_all_formal_payloads_preserved(self):
        s=json.loads((HERE/'source-seal.json').read_bytes())
        raw=(HERE/'source-only.md').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),s['source_sha256'])
        self.assertEqual((ROOT/'docs/lessons/rectangular-row-elimination.md').read_bytes(),raw)
        self.assertEqual(s['timing'],'RETROSPECTIVE_IMPLEMENTATION_INFORMED_NOT_PREPROOF')
        with zipfile.ZipFile(HERE/'formal-only-packet-public.zip') as z:
            self.assertEqual(len(z.namelist()),10)
            m=json.loads(z.read('bindings.json'))
            for n,h in m['files'].items():self.assertEqual(hashlib.sha256(z.read(n)).hexdigest(),h)
            self.assertNotIn('source-only.md',z.namelist())
    def test_actual_same_cap_serial_failure_not_a_57_root_certificate(self):
        r=json.loads((ROOT/'reports/lean-433-migration/c36-c34-ci4-actual-memory-failure.json').read_bytes())
        p=ROOT/r['archive'];self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),r['archive_sha256'])
        with zipfile.ZipFile(p) as z:
            self.assertEqual(len(z.namelist()),41)
            for row in r['members']:self.assertEqual(hashlib.sha256(z.read(row['name'])).hexdigest(),row['sha256'])
            prefix='real-preparation-native-c34-implement-v2/public/'
            rows=json.loads(z.read(prefix+'raw-derivation-receipts.json'))['files']
            for row in rows:self.assertEqual(hashlib.sha256(z.read(prefix+row['publicRelativePath'])).hexdigest(),row['publicSHA256'])
            a=json.loads(z.read(prefix+'11-target.setup.json'))['argv']
            self.assertIn('-DElab.async=false',a);self.assertIn('--memory=3072',a)
            self.assertEqual(json.loads(z.read(prefix+'11-target.result.json'))['exitCode'],-6)
            self.assertIn(b'lean::memory_exception',z.read(prefix+'11-target.stderr.raw.sanitized.txt'))
            self.assertNotIn(prefix+'12-target.result.json',z.namelist())
            self.assertNotIn(prefix+'30-observe.result.json',z.namelist())
        self.assertEqual(r['actual_root_observations'],0)
        self.assertFalse(r['main_admission']);self.assertFalse(r['scientific_ROOT'])
if __name__=='__main__':unittest.main()
