"""Strict artifact checks only; never a mathematical acceptance substitute."""
import hashlib,json,re,shutil,tempfile,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
EXPECTED={'hermite-c151-degree-internal-review-original.zip',
 'hermite-c154-degree-runtime-review-original.zip','hermite-c150-c155-c156-original.zip'}

def validate(root):
    index=json.loads((root/'index.json').read_bytes())
    assert index['schema']=='C158_EXACT_SEPARATE_INTERNAL_REVIEWS_AND_TYPED_CACHE_SUPPLIER_V1'
    rows=index['archives'];assert len(rows)==3 and {r['archive'] for r in rows}==EXPECTED
    assert sum(len(r['members']) for r in rows)==25
    payloads={}
    for row in rows:
        path=root/row['archive'];assert path.name==row['archive']
        assert sha(path.read_bytes())==row['sha256']
        with ZipFile(path) as z:
            names=z.namelist();assert len(names)==len(set(names))
            assert set(names)==set(row['members'])
            for name,meta in row['members'].items():
                raw=z.read(name);assert (len(raw),sha(raw))==(meta['bytes'],meta['sha256'])
                text=raw.decode('utf-8')
                assert not re.search(r'[A-Za-z]:[/\\]|github_pat_|ghp_[A-Za-z0-9]',text)
                payloads[(row['archive'],name)]=raw
    return index,payloads

class Checkpoint(unittest.TestCase):
    def test_all25_exact_original_members(self):
        i,p=validate(HERE);self.assertEqual(len(p),25)
        self.assertFalse(i['scientific_ROOT']);self.assertFalse(i['main_merged'])
        self.assertFalse(i['source_publication_or_ProofSeal'])
        self.assertFalse(i['production_scheduler_changed'])
        self.assertIsNone(i['matched_efficiency_winner'])

    def test_separate_exposure_stages_are_not_relabelled(self):
        _,p=validate(HERE)
        s=p[('hermite-c151-degree-internal-review-original.zip','STATIC_REVIEW_SEAL.json')]
        r=p[('hermite-c154-degree-runtime-review-original.zip','RUNTIME_REVIEW_SEAL.json')]
        self.assertEqual(sha(s),'f2ba65a06427e5cda134cd418c5bab22fd1778d107759cffd7c7228ab1664286')
        self.assertEqual(sha(r),'595ae533b64770d9dd1e447855dd93db27b8478187fc9049a516e8eb3b2ecb92')
        a,b=json.loads(s),json.loads(r)
        self.assertFalse(a['actual_compiler_output_exposure'])
        self.assertEqual(b['prior_static_seal_sha256'],sha(s))
        self.assertFalse(b['reviewer_compiler_or_script_execution'])
        self.assertFalse(b['clean_transitive_TCB'])

    def test_actual_typing_is_not_proof_and_exact_scope_is_sealed(self):
        _,p=validate(HERE);name='hermite-c150-c155-c156-original.zip'
        c=json.loads(p[(name,'C155/type-probe-result.json')])
        self.assertEqual(c['status'],'TYPE_PROBE_PASS')
        self.assertEqual(c['proposition_formations_checked'],17)
        self.assertEqual([r['exit_code'] for r in c['records']],[0]*4)
        for r in c['records']:
            self.assertEqual(sha(p[(name,'C150/'+r['module']+'.lean')]),r['source_sha256'])
            self.assertFalse(r['timeout']);self.assertTrue(r['own_output_sha256'])
        self.assertFalse(c['proposition_formation_is_proof'])
        self.assertFalse(c['candidate_400_11_bounds_accepted'])
        sealraw=p[(name,'C156/STATEMENT_SEAL.json')];s=json.loads(sealraw)
        self.assertEqual(sha(sealraw),'e4be7acce67f288b8b70755da16c4f0c40bba589cd40454b45111547b2c5ee5a')
        self.assertEqual(sha(p[(name,'C156/sealed-signatures.txt')]),s['exact_signature_sha256'])
        self.assertFalse(s['actual_roots_proved']);self.assertFalse(s['scientific_ROOT'])
        self.assertIn('captured actualBlocksQ construction/setup remain UNACCOUNTED',s['precise_cost_boundary'])

    def test_missing_archive_cannot_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);shutil.copyfile(HERE/'index.json',root/'index.json')
            with self.assertRaises(FileNotFoundError):validate(root)

    def test_tampered_archive_cannot_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);shutil.copyfile(HERE/'index.json',root/'index.json')
            for name in EXPECTED:shutil.copyfile(HERE/name,root/name)
            victim=root/next(iter(sorted(EXPECTED)))
            with victim.open('ab') as f:f.write(b'counterfactual-test-fixture')
            with self.assertRaises(AssertionError):validate(root)

if __name__=='__main__':unittest.main()
