"""Optional proof candidate transport cannot masquerade as production acceptance."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[3]
PACKAGE=ROOT/'tools/cubic_c29_kernel_ci1'
spec=importlib.util.spec_from_file_location('kernel_ci1_launch_test',PACKAGE/'launch.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)

class KernelIntegrationTests(unittest.TestCase):
    def test_parent_transport_and_actual_python_not_lean(self):
        receipt=json.loads((ROOT/'reports/lean-433-migration/c29-kernel-ci1-integration.json').read_bytes())
        for row in receipt['files']:
            raw=(ROOT/row['path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])
        self.assertEqual(hashlib.sha256((ROOT/receipt['workflow_path']).read_bytes()).hexdigest(),receipt['workflow_sha256'])
        result=receipt['parent_python']['observed']
        self.assertTrue(result['passed']);self.assertEqual(result['tests'],31)
        self.assertEqual(result['LeanCalls'],0);self.assertFalse(result['nativeAccepted'])
        self.assertFalse(receipt['production_Lean_changed']);self.assertFalse(receipt['trusted_verifier_changed'])

    def test_exact_runtime_and_original_source_delta_pins(self):
        pins,runtime,tests=M.inputs()
        self.assertEqual(len(runtime),10);self.assertEqual(len(tests),2)
        self.assertEqual(hashlib.sha256((ROOT/'QuantumBlockEncoding/CubicStatePreparation.lean').read_bytes()).hexdigest(),
            'd125f8c239bca1c15e6e4fa6e788df6dd8984394630cb2dcc9be8946c4cbcb55')
        self.assertEqual(hashlib.sha256(runtime['candidate/CubicStatePreparation.lean']).hexdigest(),
            '6ee53311b5d6e18c46afb3e068341689acb86f1bdbc425e774705e81c9142f44')
        self.assertEqual(hashlib.sha256(tests['test_kernel_only.py']).hexdigest(),
            '2db9acf95c3da6e0e2e0158a2e8c1bc8aad1c35fff3ba342ed6fd4d031fd80a4')
        self.assertNotIn(b'native_decide',runtime['candidate/CubicStatePreparation.lean'])

    def test_changed_archive_or_wrong_member_set_rejected(self):
        pins,_,_=M.inputs();archive=PACKAGE/'public-runtime-package.zip'
        with self.assertRaisesRegex(ValueError,'sealed archive changed'):
            M.archive_bytes(archive,'0'*64,pins['runtime_files'])
        with self.assertRaisesRegex(ValueError,'exact archive member partition changed'):
            M.archive_bytes(archive,pins['runtime_archive_sha256'],{'missing':'0'*64})

    def test_path_escape_is_rejected_even_when_bytes_and_hash_match(self):
        with tempfile.TemporaryDirectory(prefix='kernel-ci-path-test-',dir=ROOT/'_out') as d:
            path=Path(d)/'bad.zip'
            with zipfile.ZipFile(path,'w') as z:z.writestr('../escape',b'x')
            with self.assertRaisesRegex(ValueError,'unsafe archive path'):
                M.archive_bytes(path,hashlib.sha256(path.read_bytes()).hexdigest(),
                    {'../escape':hashlib.sha256(b'x').hexdigest()})

    def test_optional_workflow_has_no_production_mutation_or_required_gate_change(self):
        workflow=(ROOT/'.github/workflows/c29-kernel-only-diagnostic.yml').read_text()
        self.assertIn('contents: read',workflow);self.assertIn('cancel-in-progress: false',workflow)
        self.assertIn('timeout-minutes: 35',workflow);self.assertIn('--python-tests',workflow)
        self.assertIn('--execute-reviewed-candidate',workflow)
        self.assertIn('_out/cubic-c29-kernel-only-v1/public/',workflow)
        self.assertNotIn('git push',workflow);self.assertNotIn('git commit',workflow)
        self.assertNotIn('continue-on-error',workflow)
        self.assertIn('tools/cubic_c29_kernel_ci1/** -text',(ROOT/'.gitattributes').read_text())

if __name__=='__main__':unittest.main()
