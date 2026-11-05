"""Versioned LOCAL source and actual raw recovery integrity, not Lean admission."""
import hashlib,json,shutil,subprocess,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent
SHA=lambda b:hashlib.sha256(b).hexdigest()
class RobinNaturalSourceRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.author=zipfile.ZipFile(BASE/'natural-source-v2-author-original18.zip')
        cls.review=zipfile.ZipFile(BASE/'natural-source-v2-stage1-public6.zip')
        cls.addClassCleanup(cls.author.close);cls.addClassCleanup(cls.review.close)
    def test_exact_author_seal_and_all18_original_bytes(self):
        self.assertEqual(SHA(self.author.read('seal.json')),'be2e1d7d29b7de472ae1aa8f918b79db348f142f6687f042d9c95a785b2ee899')
        seal=json.loads(self.author.read('seal.json'))
        self.assertEqual(set(self.author.namelist()),{r['path'] for r in seal['files']}|{'seal.json'})
        for row in seal['files']:self.assertEqual(SHA(self.author.read(row['path'])),row['sha256'])
        self.assertEqual(self.author.read('natural-source-v2.md'),(BASE/'natural-source-v2.md').read_bytes())
        self.assertEqual(seal['independent_new_source_review'],'PENDING')
    def test_lossless_author_source_coverage_and_target_scope(self):
        source=self.author.read('natural-source-v2.md').decode()
        coverage=json.loads(self.author.read('source-proof-coverage-proposal.json'))
        self.assertEqual(''.join(row['text'] for row in coverage['lines']),source)
        self.assertEqual([row['line'] for row in coverage['lines']],list(range(1,415)))
        self.assertEqual(SHA(source.encode()),'10681db8c6f62818bcdd8d6eef787027983b010540e86c547afbaacc34031790')
        seal=json.loads(self.author.read('seal.json'))
        self.assertFalse(seal['scope']['whole_RobinMatrix']);self.assertFalse(seal['scope']['paper7_external_final_consumer'])
    def test_actual_reviewer_only_public_six_and_exact_report(self):
        self.assertEqual(set(self.review.namelist()),{'README.md','reconstruction.md','source-graph.json','source-coverage.json','diagnostics.js','diagnostics.json'})
        self.assertEqual(SHA(self.review.read('reconstruction.md')),'eb534283a7c658bf7604e4be3d258e07a61ba5a6d3d06277ec70cc21c7f02ee6')
        for private in ('scope-manifest.json','SHA256SUMS.json','SEAL.md'):self.assertNotIn(private,self.review.namelist())
    def test_independent_graph_and414line_dispositions_keep_matched_OR(self):
        graph=json.loads(self.review.read('source-graph.json'));coverage=json.loads(self.review.read('source-coverage.json'))
        self.assertEqual(len(graph['nodes']),61);self.assertEqual(len(graph['edges']),41)
        ordinary=[n for n in graph['nodes'] if n['id']!='ROOT-M224']
        self.assertEqual(len(ordinary),60)
        self.assertTrue(all(n['implementationInspected'] is False for n in ordinary))
        root=next(n for n in graph['nodes'] if n['id']=='ROOT-M224')
        self.assertEqual(root['status'],'DERIVED_SOURCE_ONLY')
        self.assertEqual([r['line'] for r in coverage['dispositions']],list(range(1,415)))
        nodes={n['id'] for n in graph['nodes']}
        for row in coverage['dispositions']:
            if row['disposition']=='NODE':self.assertIn(row['node'],nodes)
            else:self.assertTrue(row['reason'])
        alternatives=[e for e in graph['edges'] if e['kind']=='OR']
        self.assertEqual(len(alternatives),1);self.assertEqual(alternatives[0]['head'],'ROOT-M224')
        self.assertEqual(alternatives[0]['tail'],['R36','R45']);self.assertFalse(alternatives[0]['allTailInputsRequired'])
        self.assertTrue(all(e['allTailInputsRequired'] for e in graph['edges'] if e['kind']=='AND'))
    def test_real_exact_finite_diagnostic_replay_is_not_kernel_acceptance(self):
        node=shutil.which('node');self.assertIsNotNone(node,'Node required; missing diagnostic runtime is not green')
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'diagnostics.js';path.write_bytes(self.review.read('diagnostics.js'))
            run=subprocess.run([node,str(path)],capture_output=True,check=True,timeout=30)
        actual=json.loads(run.stdout);saved=json.loads(self.review.read('diagnostics.json'))
        self.assertEqual(actual,saved);self.assertEqual(actual['checks'],7120);self.assertEqual(actual['aliasCases'],5760)
        self.assertIn('not a Lean result',actual['evidenceClass'])
        self.assertEqual(actual['figure4']['total'],881);self.assertEqual(actual['xor']['total'],106)
    def test_actual_stage2_request_changes_is_preserved_not_parent_approval(self):
        with zipfile.ZipFile(BASE/'natural-source-v2-stage2-public6.zip') as z:
            self.assertEqual(set(z.namelist()),{'README.md','topology-review.md','typed-findings.json','crosswalk.json','source-coverage-comparison.json','publicsafe-envelope.json'})
            self.assertEqual(SHA(z.read('topology-review.md')),'ef0700add43527c3d97b5f1622ffc0d0bafd2982f0cc9bdea02142e988237e57')
            finding=json.loads(z.read('typed-findings.json'))
            self.assertEqual(finding['verdict'],'REQUEST_CHANGES_SOURCE_COVERAGE_ONLY')
            self.assertEqual(len(finding['findings']),1)
            self.assertEqual(finding['findings'][0]['status'],'OPEN')
            self.assertEqual(finding['findings'][0]['sourceLines'],[181,183])
    def test_publicsafe_successor_does_not_release_private_original_envelopes(self):
        with zipfile.ZipFile(BASE/'natural-source-v2-stage2-public6.zip') as z:
            envelope=json.loads(z.read('publicsafe-envelope.json'))
            for row in envelope['stage1OriginalHashes']:
                if row['file'] in self.review.namelist():self.assertEqual(SHA(self.review.read(row['file'])),row['sha256'])
            for private in ('scope-manifest.json','SHA256SUMS.json','SEAL.md'):
                self.assertNotIn(private,z.namelist());self.assertNotIn(private,envelope['stage1PublicsafeAllowlist'])
    def test_source_only_verdict_keeps_implementation_and_finitebit_gates_unassessed(self):
        with zipfile.ZipFile(BASE/'natural-source-v2-stage2-public6.zip') as z:
            finding=json.loads(z.read('typed-findings.json'))
            scope=' '.join(finding['unassessed'])
            for marker in ('Implementation/formal','compiler/axiom/kernel','complete target','finite-bit','publication/admission','PURIFIED'):
                self.assertIn(marker,scope)
if __name__=='__main__':unittest.main()
