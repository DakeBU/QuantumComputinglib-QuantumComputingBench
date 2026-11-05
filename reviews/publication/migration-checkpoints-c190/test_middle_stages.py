import hashlib,json,shutil,tempfile,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def validate(root):
    i=json.loads((root/'index.json').read_bytes())
    assert len(i['archives'])==2 and sum(len(r['members']) for r in i['archives'])==6
    data=[]
    for r in i['archives']:
        assert sha((root/r['archive']).read_bytes())==r['sha256']
        with ZipFile(root/r['archive']) as z:
            assert len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(r['members'])
            for n,m in r['members'].items():assert (len(z.read(n)),sha(z.read(n)))==(m['bytes'],m['sha256'])
            assert sha(z.read(r['original_seal']))==r['original_seal_sha256']
            data.append(json.loads(z.read(r['original_seal'])))
    return i,data
class MiddleStages(unittest.TestCase):
    def test_exact_originals_and_no_promotion(self):
        i,_=validate(HERE)
        for k in ['independent_rerun','printed_body_audit','clean_transitive_TCB','main_merged','scientific_ROOT','source_publication_or_ProofSeal']:
            self.assertFalse(i[k])
    def test_exposure_chronology_and_two_values(self):
        i,(s,r)=validate(HERE)
        self.assertFalse(s['actual_middle_compiler_or_axiom_output_exposure'])
        self.assertFalse(s['C174_runtime_C172_discriminator_C175_public_packet_opened'])
        self.assertEqual(r['prior_C178_static_seal_sha256'],i['archives'][0]['original_seal_sha256'])
        self.assertEqual(r['targets'],s['public_targets'])
        self.assertEqual(r['actual_axiom_rows_each_run'],2)
        self.assertEqual(set(r['each_actual_axiom_list']),{'propext','Classical.choice','Quot.sound'})
    def test_missing_original_cannot_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);shutil.copyfile(HERE/'index.json',p/'index.json')
            with self.assertRaises(FileNotFoundError):validate(p)
    def test_tampered_archive_cannot_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);shutil.copyfile(HERE/'index.json',p/'index.json')
            i=json.loads((p/'index.json').read_bytes());(p/i['archives'][0]['archive']).write_bytes(b'corrupt')
            with self.assertRaises(AssertionError):validate(p)
if __name__=='__main__':unittest.main()
