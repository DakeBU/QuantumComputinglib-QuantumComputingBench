"""Exact same-cap diagnostic transport and current workflow guards."""
import hashlib,json,tempfile,unittest,zipfile
from pathlib import Path
import launch
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
class SerialTransportTests(unittest.TestCase):
    def test_exact24_members_and_single_runtime_expression(self):
        with zipfile.ZipFile(HERE/'public-runtime-package.zip') as z:new={n:z.read(n) for n in z.namelist()}
        with zipfile.ZipFile(ROOT/'tools/real_preparation_native_c34_ci3/public-runtime-package.zip') as z:old={n:z.read(n) for n in z.namelist()}
        self.assertEqual(len(new),24)
        self.assertEqual(set(new)-set(old),{'compile-policy.json','test_serial_policy.py'})
        self.assertEqual({n for n in old if old[n]!=new[n]},{'runner.py','package-bindings.json','packet-seal.json'})
        a=b"flags + ['-o', str(output), relative + '.lean']"
        b=b"flags + ['-DElab.async=false', '-o', str(output), relative + '.lean']"
        self.assertEqual(old['runner.py'].count(a),1);self.assertEqual(old['runner.py'].replace(a,b),new['runner.py'])
        for row in json.loads(new['packet-seal.json'])['files']:
            self.assertEqual(hashlib.sha256(new[row['path']]).hexdigest(),row['sha256'])
    def test_prepare_detects_runtime_tamper(self):
        with tempfile.TemporaryDirectory() as directory:
            project=Path(directory);package,out=launch.prepare(project)
            self.assertEqual(out.name,'c34-native-ci4')
            (package/'runner.py').write_bytes(b'FIXTURE_TAMPER')
            with self.assertRaises(ValueError):launch.prepare(project)
    def test_current_optional_workflow_keeps_same_boundary(self):
        w=(ROOT/'tools/real_preparation_native_c34_ci5/workflow-before-ci5.yml.txt').read_text()
        self.assertIn('real_preparation_native_c34_ci4/launch.py --ci',w)
        self.assertIn('real_preparation_native_c34_ci4/launch.py --python-tests',w)
        self.assertIn('timeout-minutes: 35',w);self.assertIn('contents: read',w)
        self.assertNotIn('continue-on-error',w);self.assertNotIn('pull_request_target',w)
        self.assertIn('_out/c34-native-ci4/public/',w)
        self.assertTrue(all(r.startswith('        run: ') for r in w.splitlines() if r.lstrip().startswith('run:')))
if __name__=='__main__':unittest.main()
