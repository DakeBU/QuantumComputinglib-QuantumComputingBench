import hashlib,json,shutil,tempfile,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def validate(root):
    i=json.loads((root/'index.json').read_bytes());assert len(i['archives'])==6
    assert sum(len(r['members']) for r in i['archives'])==18
    data={}
    for r in i['archives']:
        assert sha((root/r['archive']).read_bytes())==r['sha256']
        with ZipFile(root/r['archive']) as z:
            assert len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(r['members'])
            for n,m in r['members'].items():assert (len(z.read(n)),sha(z.read(n)))==(m['bytes'],m['sha256'])
            assert sha(z.read(r['original_seal']))==r['original_seal_sha256']
            data[r['packet']]=json.loads(z.read(r['original_seal']))
    return i,data
class ReviewStages(unittest.TestCase):
    def test_exact18_no_admission_promotion(self):
        i,_=validate(HERE)
        for k in ['main_merged','independent_rerun','source_publication_or_ProofSeal','scientific_ROOT','clean_transitive_TCB']:self.assertFalse(i[k])
    def test_separate_chain_exposure_and_actual_own_output(self):
        _,d=validate(HERE);s=d['hermite-c196-chain-static-comparison'];r=d['hermite-c201-chain-runtime-association']
        self.assertFalse(s['samechain_runtime_compiler_or_actual_axiom_outputs_opened'])
        self.assertEqual(r['prior_C196_seal_sha256'],'e6c5ce412b7a79290772f989f0d8c2fb14f322013956ef001e78835127e11460')
        self.assertTrue(r['all_seven_loaded_definition_bodies_inspected']);self.assertEqual(r['actual_public_axiom_rows'],5)
        self.assertTrue(r['C191_same_source_memory_failure_not_accepted'])
    def test_cost_static_not_runtime_and_exact_formula_unproved(self):
        _,d=validate(HERE);s=d['hermite-c200-middle-cost-static-comparison'];r=d['hermite-c203-middle-cost-runtime-association']
        self.assertFalse(s['compiler_actual_output_or_axiom_gate_inspected'])
        self.assertFalse(s['exact_C194_count_certified_by_Lean']);self.assertFalse(r['C194_exact_formula_Lean_certified'])
        self.assertFalse(r['independent_rerun_or_full_TCB']);self.assertFalse(r['printed_proof_or_loaded_definition_bodies_audited'])
    def test_missing_archive_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);shutil.copyfile(HERE/'index.json',p/'index.json')
            with self.assertRaises(FileNotFoundError):validate(p)
    def test_tampered_archive_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);shutil.copyfile(HERE/'index.json',p/'index.json');i=json.loads((p/'index.json').read_bytes())
            (p/i['archives'][0]['archive']).write_bytes(b'invalid')
            with self.assertRaises(AssertionError):validate(p)
if __name__=='__main__':unittest.main()
