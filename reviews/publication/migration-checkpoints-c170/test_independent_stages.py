import hashlib,json,shutil,tempfile,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()

def validate(root):
    i=json.loads((root/'index.json').read_bytes());assert len(i['archives'])==4
    assert sum(len(r['members']) for r in i['archives'])==13
    data={}
    for r in i['archives']:
        assert sha((root/r['archive']).read_bytes())==r['sha256']
        with ZipFile(root/r['archive']) as z:
            assert set(z.namelist())==set(r['members']) and len(z.namelist())==len(set(z.namelist()))
            for n,m in r['members'].items():assert (len(z.read(n)),sha(z.read(n)))==(m['bytes'],m['sha256'])
            assert sha(z.read(r['original_seal']))==r['original_seal_sha256']
            data[r['archive']]=json.loads(z.read(r['original_seal']))
    return i,data

class IndependentStages(unittest.TestCase):
    def test_exact13_original_members_required(self):
        i,_=validate(HERE);self.assertFalse(i['scientific_ROOT']);self.assertFalse(i['main_merged'])
        self.assertFalse(i['source_publication_or_ProofSeal']);self.assertFalse(i['clean_transitive_TCB'])
    def test_distinct_static_runtime_seals_and_limits(self):
        _,d=validate(HERE)
        p=d['hermite-c161-primitive-internal-review-original.zip']
        r=d['hermite-c164-primitive-runtime-review-original.zip']
        s=d['hermite-c169-setup-internal-review-original.zip']
        t=d['hermite-c173-setup-runtime-review-original.zip']
        self.assertFalse(p['target_actual_compiler_or_axiom_output_exposure'])
        self.assertEqual(r['prior_C161_static_seal_sha256'],'d3ca8f0e1fe3dfa197f2b75c59b0024bae8662dabaf904f12ea68d877a15068c')
        self.assertEqual(p['actual_five_rightEntry_branch_upper_bounds'],[8,10,10,10,10])
        self.assertFalse(s['setup_runtime_or_axiom_output_exposure'])
        self.assertEqual(t['C169_static_seal_sha256'],'7e3d83332fb37e36f11302f5a25512bc8538352c92834017507bdaa6e11394d4')
        self.assertFalse(t['SourceAnchor_ProofSeal_scientific_ROOT'])
    def test_missing_archive_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);shutil.copyfile(HERE/'index.json',p/'index.json')
            with self.assertRaises(FileNotFoundError):validate(p)

if __name__=='__main__':unittest.main()
