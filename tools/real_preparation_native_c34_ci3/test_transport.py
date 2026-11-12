"""Canonical blob binding stays strict; fixtures never count as Lean acceptance."""
import hashlib,json,tempfile,unittest,zipfile
from pathlib import Path
import launch
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
class CanonicalCandidateTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with zipfile.ZipFile(HERE/'public-runtime-package.zip') as z:cls.new={n:z.read(n) for n in z.namelist()}
        with zipfile.ZipFile(ROOT/'tools/real_preparation_native_c34_ci1/public-runtime-package.zip') as z:cls.old={n:z.read(n) for n in z.namelist()}
    def test_exact22_partition_and_only_candidate_manifest_seal_changes(self):
        self.assertEqual(len(self.new),22);self.assertEqual(set(self.new)-set(self.old),{'source-byte-delta.json'})
        self.assertEqual({n for n in self.old if self.old[n]!=self.new[n]},{'candidate-sources.json','package-bindings.json','packet-seal.json'})
        self.assertEqual(hashlib.sha256(self.new['packet-seal.json']).hexdigest(),launch.APPROVED_SEAL_SHA256)
        for row in json.loads(self.new['packet-seal.json'])['files']:
            self.assertEqual(hashlib.sha256(self.new[row['path']]).hexdigest(),row['sha256'])
    def test_ten_committed_blob_changes_no_runtime_normalization(self):
        delta=json.loads(self.new['source-byte-delta.json']);candidate=json.loads(self.new['candidate-sources.json'])
        self.assertEqual((delta['changedRows'],delta['unchangedRows']),(10,210))
        self.assertFalse(delta['runtimeNormalization']);self.assertFalse(delta['alternateByteAcceptance'])
        by={r['path']:r for r in delta['comparisons']};self.assertEqual(len(by),220)
        for row in candidate['files']:
            self.assertEqual(row['sha256'],by[row['relativePath']]['committedBlobSHA256'])
            self.assertEqual(row['bytes'],by[row['relativePath']]['committedBlobBytes'])
    def test_prepare_exact22_rejects_runtime_tamper(self):
        with tempfile.TemporaryDirectory() as directory:
            project=Path(directory);package,_=launch.prepare(project)
            self.assertEqual(len(list(package.rglob('*.lean'))),4)
            (package/'candidate-sources.json').write_bytes(b'TAMPERED_FIXTURE')
            with self.assertRaises(ValueError):launch.prepare(project)
    def test_actual_failure_chain_and_current_workflow_steps(self):
        with zipfile.ZipFile(ROOT/'reviews/publication/real-preparation-c32/c34-ci2-actual-python-byte-failure-public.zip') as z:
            receipt=json.loads(z.read('c34-native-ci1/public/ci2-python-result.json'))
            self.assertEqual(receipt['exitCode'],1)
            for row in receipt['failedPythonDerivatives']:
                raw=z.read('c34-native-ci1/public/'+row['path'])
                self.assertEqual(hashlib.sha256(raw).hexdigest(),row['publicSHA256'])
            stderr=z.read('c34-native-ci1/public/ci2-python-failure.stderr.sanitized.txt')
            self.assertIn(b'candidate source byte binding changed',stderr);self.assertIn(b'FAILED (errors=1)',stderr)
        w=(ROOT/'.github/workflows/c34-real-preparation-native.yml').read_text()
        self.assertIn('        run: lake env python3 -B tools/real_preparation_native_c34_ci5/launch.py --ci',w)
        self.assertTrue(all(s.startswith('        run: ') for s in w.splitlines() if s.lstrip().startswith('run:')))
        self.assertNotIn('continue-on-error',w)
if __name__=='__main__':unittest.main()
