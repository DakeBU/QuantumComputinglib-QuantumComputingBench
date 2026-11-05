"""Prospective means reproducible input, never proof/integration acceptance."""
import hashlib,importlib.util,json,re,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def committed_batch(base,names):
    specs=[base+':'+n for n in names]
    raw=subprocess.check_output(['git','cat-file','--batch'],input=('\n'.join(specs)+'\n').encode(),cwd=ROOT)
    offset=0;out={}
    for name in names:
        end=raw.index(b'\n',offset);header=raw[offset:end].split();assert len(header)==3 and header[1]==b'blob'
        size=int(header[2]);offset=end+1;out[name]=raw[offset:offset+size];offset+=size
        assert raw[offset:offset+1]==b'\n';offset+=1
    assert offset==len(raw)
    return out
class ProspectiveEpochTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with zipfile.ZipFile(BASE/'prospective-epoch-successor11.zip') as z:cls.payload={n:z.read(n) for n in z.namelist()}
        cls.ctx=json.loads(cls.payload['context.json']);cls.files=json.loads(cls.payload['overlay-manifest.json'])['files']
        names=sorted({r['path'] for r in cls.files if 'overlay/'+r['path'] not in cls.payload}|{r['module'] for r in cls.ctx['pair']}|{'website/research/publications.json','website/research/sources.json'})
        cls.base=committed_batch(cls.ctx['parent'],names)
        cls.overlay={r['path']:cls.payload.get('overlay/'+r['path'],cls.base.get(r['path'])) for r in cls.files}
    def test_all_prospective_bytes_reconstruct_and_old37_metadata_remains(self):
        seal=json.loads(self.payload['seal.json'])
        for row in seal['payload']:
            self.assertEqual(sha(self.payload[row['path']]),row['sha256'])
        for row in self.files:
            self.assertEqual(sha(self.overlay[row['path']]),row['sha256'])
            self.assertEqual(len(self.overlay[row['path']]),row['bytes'])
        self.assertEqual(len(json.loads(self.base['website/research/publications.json'])['records']),37)
        old=json.loads(self.base['website/research/sources.json'])['sources'];new=json.loads(self.overlay['website/research/sources.json'])['sources']
        self.assertEqual(new[:-1],old);self.assertEqual(len(new),42)
        self.assertFalse(self.ctx['production_changed']);self.assertFalse(self.ctx['new_role_evidence_authored'])
    def test_exact_pair_is_twelve_proof_sites_only(self):
        for row in self.ctx['pair']:
            name=row['module'];old=self.base[name];new=self.overlay[name]
            self.assertEqual(sha(old),row['original_sha256']);self.assertEqual(sha(new),row['candidate_sha256'])
            if name.endswith('/CubicAmplitudePrimitive.lean'):
                self.assertEqual(old.count(b'native_decide +revert'),3)
                self.assertEqual(old.replace(b'native_decide +revert',b'decide +kernel +revert'),new)
            else:
                self.assertEqual(old.count(b'native_decide'),9)
                replaced=old.replace(b'native_decide',b'decide +kernel')
                self.assertEqual(replaced.replace(b'have hzero : (0 : Rat) - 0 = 0 := by decide +kernel',b'have hzero : (0 : Rat) - 0 = 0 := by exact Rat.sub_self'),new)
    def test_original_binding_recipe_reproduces_all39_prospective_digests(self):
        spec=importlib.util.spec_from_file_location('original_gate_c46_test',ROOT/'website/scripts/check_research_publications.py')
        gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
        old=json.loads(self.base['website/research/publications.json'])['records']
        expected={x['module']:x['prospective_binding'] for x in self.ctx['contexts']}
        new=[json.loads(v) for k,v in self.payload.items() if k.startswith('candidate-record-')]
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            for path,raw in self.overlay.items():
                target=root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
            for row in old:
                self.assertEqual(gate.binding_digest(root,row),expected[row['module']])
            for row in new:self.assertEqual(gate.binding_digest(root,row),row['binding_sha256'])
        self.assertEqual(len(expected),37);self.assertEqual(len(new),2)
    def test_independent_graph_acceptance_does_not_approve_source_gaps(self):
        with zipfile.ZipFile(ROOT/'reviews/publication/robin-fixed-routes-c45/topology-v2-independent-original6.zip') as z:
            seal=json.loads(z.read('seal.json'))
            self.assertEqual(seal['verdict'],'ACCEPTED_BOUNDED_LOCAL')
            self.assertEqual(len(seal['source_gaps_still_open']),6)
            self.assertIn('Whole-module source or compiler acceptance',seal['not_approved'])
            self.assertEqual(len(seal['original_findings_resolved_in_successor']),6)
            for row in seal['artifacts']:
                self.assertEqual(sha(z.read(row['path'].split('/')[-1])),row['sha256'])
if __name__=='__main__':unittest.main()
