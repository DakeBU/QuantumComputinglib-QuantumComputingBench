"""Exact envelope successor; no source, trust, capacity or acceptance shortcut."""
import hashlib,json,tempfile,unittest,zipfile
from pathlib import Path
import launch
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
class GatedTransportTests(unittest.TestCase):
    def test_exact31_source_unchanged_and_full_resource_chain(self):
        with zipfile.ZipFile(HERE/'public-runtime-package.zip') as z:new={n:z.read(n) for n in z.namelist()}
        with zipfile.ZipFile(ROOT/'tools/real_preparation_native_c34_ci4/public-runtime-package.zip') as z:old={n:z.read(n) for n in z.namelist()}
        self.assertEqual(len(new),31)
        p,q=json.loads(old['profile.json']),json.loads(new['profile.json'])
        self.assertEqual({k:v for k,v in p.items() if k!='envelope'},{k:v for k,v in q.items() if k!='envelope'})
        self.assertEqual((q['envelope']['memoryMiB'],q['envelope']['reserveMiB'],q['envelope']['requiredHeadroomMiB']),(5120,2048,7168))
        for n in ('Parser.lean','Collector.lean','validator.py','candidate-sources.json'):self.assertEqual(old[n],new[n])
        self.assertEqual(old['discovery.py'].replace(b'--memory=3072',b'--memory=5120'),new['discovery.py'])
        for n,row in json.loads(new['resource-chain.json'])['files'].items():
            self.assertEqual(new[n],(ROOT/row['source']).read_bytes());self.assertEqual(hashlib.sha256(new[n]).hexdigest(),row['sha256'])
        for row in json.loads(new['packet-seal.json'])['files']:self.assertEqual(hashlib.sha256(new[row['path']]).hexdigest(),row['sha256'])
    def test_prepare_rejects_runtime_tamper(self):
        with tempfile.TemporaryDirectory() as directory:
            package,out=launch.prepare(Path(directory));self.assertEqual(out.name,'c34-native-ci5')
            (package/'resource_adapter.py').write_bytes(b'SYNTHETIC_TAMPER')
            with self.assertRaises(ValueError):launch.prepare(Path(directory))
    def test_optional_workflow_and_exact_launcher_changes(self):
        b=json.loads((HERE/'transport-bindings.json').read_bytes());old=(ROOT/'tools/real_preparation_native_c34_ci4/launch.py').read_bytes()
        for row in b['launcher_exact5identity_replacements']:
            self.assertEqual(old.count(row['before'].encode()),1);old=old.replace(row['before'].encode(),row['after'].encode())
        self.assertEqual(old,(HERE/'launch.py').read_bytes())
        w=(HERE/'workflow-before-ci5.yml.txt').read_text()
        for row in b['workflow_changes']:
            self.assertEqual(w.count(row['before']),1);w=w.replace(row['before'],row['after'])
        self.assertEqual(w,(ROOT/'.github/workflows/c34-real-preparation-native.yml').read_text())
        self.assertIn('real_preparation_native_c34_ci5/launch.py --ci',w);self.assertIn('contents: read',w)
        self.assertIn('cancel-in-progress: false',w);self.assertIn('timeout-minutes: 35',w)
        self.assertNotIn('continue-on-error',w);self.assertNotIn('pull_request_target',w)
        self.assertTrue(all(r.startswith('        run: ') for r in w.splitlines() if r.lstrip().startswith('run:')))
if __name__=='__main__':unittest.main()
