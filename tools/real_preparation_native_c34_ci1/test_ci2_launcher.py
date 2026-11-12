"""Synthetic logging/privacy guards do not turn Python or Lean failure green."""
import hashlib,json,tempfile,unittest,zipfile
from pathlib import Path
from types import SimpleNamespace
import launch_ci2 as l
class LauncherDiagnosticTests(unittest.TestCase):
    def test_parent_predecessor_pin_and_exact_runtime(self):
        base=l.load_base();self.assertEqual(base.ARCHIVE_SHA256,'655e22d32feef66de822b26f6638b3ba7f7404ad81564c02244ce486cae51513')
        self.assertEqual(base.APPROVED_SEAL_SHA256,'36670de77f450852de4617295abe7b372127f0d3a8bd68b825db52deb699cc3b')
    def test_failed_text_keeps_error_and_removes_paths_credentials(self):
        project=Path('/synthetic/project');package=project/'_out/runtime'
        raw=(str(package)+'/test.py ValueError: actual failure\n/synthetic/project/source.lean\n'+str(Path.home())+'/private\ngithub_pat_TEST\n').encode()
        safe=l.sanitized(raw,project,package)
        self.assertIn(b'ValueError: actual failure',safe);self.assertIn(b'$PACKAGE/test.py',safe)
        self.assertNotIn(str(project).encode(),safe);self.assertNotIn(str(Path.home()).encode(),safe)
        self.assertNotIn(b'github_pat_',safe)
    def test_failure_hash_chain_and_success_has_no_failure_text(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory);child=SimpleNamespace(returncode=1,stdout=b'',stderr=b'AssertionError: SYNTHETIC')
            rows=l.preserve_failed_python(p,child,p/'project',p/'package');self.assertEqual(len(rows),2)
            for row in rows:self.assertEqual(hashlib.sha256((p/row['path']).read_bytes()).hexdigest(),row['publicSHA256'])
            self.assertEqual(rows[1]['rawSHA256'],hashlib.sha256(child.stderr).hexdigest())
            self.assertEqual(child.returncode,1)
            self.assertEqual(l.preserve_failed_python(p,SimpleNamespace(returncode=0),p,p),[])
    def test_historical_ci1_failure_remains_not_run_Lean(self):
        root=Path(__file__).resolve().parents[2]
        r=json.loads((root/'reports/lean-433-migration/c34-actual-ci1-python-failure.json').read_bytes())
        self.assertEqual(r['python_receipt']['exitCode'],1);self.assertEqual(r['actual_Lean_calls'],0)
        self.assertEqual(r['parser'],'NOT_RUN');self.assertFalse(r['nativeAccepted'])
if __name__=='__main__':unittest.main()
