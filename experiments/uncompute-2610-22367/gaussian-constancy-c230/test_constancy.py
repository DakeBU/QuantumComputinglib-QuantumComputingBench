import hashlib,json,re,sys,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[2]))
from tools.proof_trust import strip_lean_comments_and_strings
sha=lambda b:hashlib.sha256(b).hexdigest()
def validate(root):
    b=json.loads((root/'source-binding.json').read_bytes())
    for n,h in b['payloads'].items():
        if sha((root/n).read_bytes())!=h:raise ValueError('payload mismatch')
    a=b['archive']
    if sha((root/a['file']).read_bytes())!=a['sha256']:raise ValueError('archive mismatch')
    with ZipFile(root/a['file']) as z:
        if len(z.namelist())!=5 or set(z.namelist())!=set(a['members']):raise ValueError('inventory mismatch')
        for n,m in a['members'].items():
            if (len(z.read(n)),sha(z.read(n)))!=(m['bytes'],m['sha256']):raise ValueError('original mismatch')
    return b,json.loads((root/'proof-result.json').read_bytes())
class Constancy(unittest.TestCase):
    def test_exact_sources_and_preproof_seal(self):
        _,r=validate(HERE)
        for n in ['GaussianConstancyProof.lean','ConstancyProofChecks.lean']:
            self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b',strip_lean_comments_and_strings((HERE/n).read_text(encoding='utf-8'))))
        self.assertEqual(r['preproof_seal_sha256'],'f6badc2547806f2886fb15200e5444f40d03a182a204e8337274b637d28f5eb6')
        s=(HERE/'GaussianConstancyProof.lean').read_text(encoding='utf-8')
        self.assertNotIn('slopeUnbounded',s);self.assertNotIn('frozenWord',s.split('namespace UncomputeGaussian206',1)[1])
    def test_actual_own_consumer_and_ordinary_root(self):
        _,r=validate(HERE);a,c=r['records']
        self.assertEqual(r['status'],'PROVED_LOCALLY_FOCUSED');self.assertEqual(r['actual_proved_roots'],1)
        self.assertEqual(c['selected_own_provider_sha256'],a['own_output_sha256'])
        self.assertEqual(a['axiom_reports'],[]);self.assertFalse(r['source_zero_axiom_rows_are_empty_axiom_proof'])
        self.assertEqual(c['axiom_reports'][0]['name'],'UncomputeGaussian206.localIncrement_block128_constancy')
        self.assertTrue(set(c['axiom_reports'][0]['axioms'])<={'propext','Classical.choice','Quot.sound'})
        for record in [a,c]:self.assertEqual(record['exit_code'],0);self.assertFalse(record['timeout'])
        out=(HERE/'consumer-feedback.txt').read_text(encoding='utf-8')
        self.assertIn('j < 1024 → D < 2 ^ 25 →',out);self.assertIn('128 * (D / 128)',out)
    def test_not_error_circuit_or_resource_certificate(self):
        b,r=validate(HERE);self.assertTrue(r['exact_integer_model_constancy_only'])
        self.assertFalse(r['full_Gaussian_error_circuit_phase_cleanup_resources_or_SPBE_ROOT'])
        for key in ['independent_proof_review','source_publication_admitted','main_merged','scientific_ROOT','PURIFIED']:self.assertFalse(b[key])
    def test_missing_or_modified_evidence_rejected(self):
        import tempfile,shutil
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);shutil.copyfile(HERE/'source-binding.json',p/'source-binding.json')
            with self.assertRaises(FileNotFoundError):validate(p)
            n=next(iter(validate(HERE)[0]['payloads']));(p/n).write_bytes(b'changed')
            with self.assertRaises(ValueError):validate(p)
if __name__=='__main__':unittest.main()
