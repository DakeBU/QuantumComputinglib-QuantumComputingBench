"""Portable producer transport integrity, not an actual Lean result."""
import hashlib,json,re,unittest,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
class PortableTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b=json.loads((HERE/'transport-bindings.json').read_bytes())
        with zipfile.ZipFile(HERE/'public-runtime-package.zip') as z:cls.f={n:z.read(n) for n in z.namelist()}
        cls.s=json.loads(cls.f['packet-seal.json'])
    def test_exact_package_partition_and_manifest(self):
        self.assertEqual(hashlib.sha256((HERE/'public-runtime-package.zip').read_bytes()).hexdigest(),self.b['archive_sha256'])
        self.assertEqual(len(self.f),21)
        self.assertEqual(hashlib.sha256(self.f['packet-seal.json']).hexdigest(),self.b['approved_seal_sha256'])
        self.assertEqual(set(self.f),{r['path'] for r in self.s['files']}|{'packet-seal.json'})
        for row in self.b['payloads']:
            self.assertEqual(hashlib.sha256(self.f[row['path']]).hexdigest(),row['sha256'])
            self.assertEqual(len(self.f[row['path']]),row['bytes'])
        for name,digest in json.loads(self.f['package-bindings.json'])['files'].items():
            self.assertEqual(hashlib.sha256(self.f[name]).hexdigest(),digest)
    def test_portability_delta_explicit_runtime_not_modified(self):
        d=self.s['parent_derivative'];self.assertEqual(d['exact_delta'],self.b['exact_portability_delta'])
        self.assertEqual({r['path'] for r in d['exact_delta']},{'package-bindings.json','preceding-packet-bindings.json','primary-parser-api-anchors.json','python-only-tests.json','test_adapter.py'})
        self.assertTrue(d['runtime_parser_collector_validator_profile_and_candidate_bytes_unchanged'])
        for raw in self.f.values():
            self.assertIsNone(re.search(rb'(?:[A-Za-z]:[\\/](?:Users|qb261009)|/home/runner/|github_pat_|ghp_)',raw))
    def test_no_stub_fifty_seven_roots_and_no_native_claim(self):
        self.assertNotIn(b'NotImplementedError',self.f['discovery.py'])
        self.assertIn(b'parseImports',self.f['Parser.lean'])
        p=json.loads(self.f['profile.json']);self.assertEqual(len(p['roots']),57)
        self.assertEqual([r['sourceRoots'] for r in p['modules']],[45,7,5])
        self.assertEqual(self.s['actualKernelObservations'],0);self.assertEqual(self.s['actualParserObservations'],0)
        self.assertFalse(self.s['nativeAccepted']);self.assertIsNone(self.s['sourceAgreement'])
    def test_optional_bounded_workflow_only_uploads_sanitized_paths(self):
        w=(ROOT/'.github/workflows/c34-real-preparation-native.yml').read_text()
        self.assertIn('pull_request:',w);self.assertIn('contents: read',w);self.assertIn('timeout-minutes: 35',w)
        self.assertIn('cancel-in-progress: false',w);self.assertIn('real_preparation_native_c34_ci5/launch.py --ci',w)
        self.assertNotIn('pull_request_target',w);self.assertNotIn('secrets.',w)
        self.assertIn('_out/real-preparation-native-c34-implement-v2/public/',w)
        self.assertNotIn('path: _out/',w)
if __name__=='__main__':unittest.main()
