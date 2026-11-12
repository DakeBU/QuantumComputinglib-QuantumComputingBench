import hashlib,importlib.util,json,re,sys,unittest
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
    for a in b['archives']:
        if sha((root/a['file']).read_bytes())!=a['sha256']:raise ValueError('archive mismatch')
        with ZipFile(root/a['file']) as z:
            if len(z.namelist())!=len(set(z.namelist())) or set(z.namelist())!=set(a['members']):raise ValueError('inventory mismatch')
            for n,m in a['members'].items():
                if (len(z.read(n)),sha(z.read(n)))!=(m['bytes'],m['sha256']):raise ValueError('original mismatch')
    return b
class GaussianModel(unittest.TestCase):
    def test_bound_sources_definitions_not_proofs(self):
        validate(HERE)
        for n in ['GaussianFixedWords.lean','GaussianIntegerCore.lean']:
            s=strip_lean_comments_and_strings((HERE/n).read_text(encoding='utf-8'))
            self.assertIsNone(re.search(r'\b(theorem|lemma|axiom|sorry|admit|unsafe|noncomputable|native_decide)\b',s))
        core=(HERE/'GaussianIntegerCore.lean').read_text(encoding='utf-8')
        self.assertEqual(core.count('letI : Decidable (inDomain xs)'),1)
        self.assertNotIn('classical',core)
    def test_all_literal_words_and_zero_suffix(self):
        validate(HERE);c=json.loads((HERE/'fixed_constants.json').read_bytes());words=[int(x,16) for x in c['words']]
        source=(HERE/'GaussianFixedWords.lean').read_text(encoding='utf-8')
        arms={int(j):int(v) for j,v in re.findall(r'^  \| (\d+) => (\d+)$',source,re.M)}
        self.assertEqual(set(arms),set(range(514)));self.assertEqual(len(words),1024)
        self.assertTrue(all(arms[j]==words[j] for j in arms));self.assertEqual(words[514:],[0]*510)
        self.assertIn('  | _ => 0',source)
    def test_actual_own_outputs_and_thirty_one_named_types(self):
        validate(HERE);r=json.loads((HERE/'type-probe-result.json').read_bytes());a,c,d=r['records']
        self.assertEqual(r['status'],'TYPECHECKED_DEFINITIONS_NOT_PROVED');self.assertEqual(r['proof_roots'],0)
        self.assertEqual(c['selected_own_provider_sha256'],a['own_output_sha256'])
        self.assertEqual(d['selected_own_provider_sha256'],c['own_output_sha256'])
        for x in r['records']:self.assertEqual(x['exit_code'],0);self.assertFalse(x['timeout'])
        out=(HERE/'definition-type-feedback.txt').read_text(encoding='utf-8')
        self.assertEqual(len(re.findall(r'^UncomputeGaussian206\.',out,re.M)),31)
        self.assertIn('if inDomain xs ∧ k < 2 ^ 39',out)
    def test_exact_parent_finite_replay_not_uniform_acceptance(self):
        validate(HERE);spec=importlib.util.spec_from_file_location('gaussian_checkpoint_model',HERE/'integer_model.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        self.assertEqual(m.diagnostic(),json.loads((HERE/'finite-diagnostic.json').read_bytes()))
        self.assertEqual(m.middle_row(100,2**14,0),-4)
        self.assertEqual(m.local_increment(0,0),2**32-160)
        self.assertEqual(m.increment(-(514<<25)),768);self.assertEqual(m.increment(514<<25),0)
        self.assertFalse(m.diagnostic()['circuit_or_error_acceptance'])
    def test_independent_review_barriers_and_old_type_failure(self):
        b=validate(HERE)
        with ZipFile(HERE/b['archives'][0]['file']) as z:
            r=json.loads(z.read('uncompute-c225-gaussian-definition-type-probe/type-probe-result.json'))
            self.assertEqual(r['proof_roots'],0);self.assertEqual(r['records'][1]['exit_code'],1)
            self.assertIsNone(r['records'][1]['own_output_sha256'])
        with ZipFile(HERE/b['archives'][1]['file']) as z:
            s=json.loads(z.read('uncompute-c213-gaussian-integer-source-first/SOURCE_FIRST_SEAL.json'))
            v=json.loads(z.read('uncompute-c221-gaussian-integer-static-comparison/STATIC_VERDICT.json'))
            t=json.loads(z.read('uncompute-c231-gaussian-successor-static-review/STATIC_SUCCESSOR_SEAL.json'))
            self.assertFalse(s['author_C206_access']);self.assertFalse(v['exposure']['compiler_outputs'])
            self.assertTrue(t['no_runtime_or_diagnostic_exposure'])
        with ZipFile(HERE/b['archives'][2]['file']) as z:
            s=json.loads(z.read('STATEMENT_SEAL.json'));self.assertEqual(s['EXCESS'],[]);self.assertFalse(s['proof_started'])
            self.assertIn('localIncrement_block128_constancy',z.read('sealed-signature.txt').decode())
    def test_no_numeric_circuit_resource_or_source_admission(self):
        b=validate(HERE)
        for n in ['full_Gaussian_error','circuit_phase_cleanup','resource1583_139','SPBE_ROOT','source_publication_admitted','main_merged','PURIFIED']:self.assertFalse(b[n])
        self.assertIn('Apache',(HERE/'LICENSE').read_text(encoding='utf-8'))
        self.assertIn('64b5a13aa249f1360846657392e6c66817b26d0f',(HERE/'NOTICE').read_text(encoding='utf-8'))
    def test_missing_and_changed_payload_rejected(self):
        import shutil,tempfile
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);shutil.copyfile(HERE/'source-binding.json',p/'source-binding.json')
            with self.assertRaises(FileNotFoundError):validate(p)
            n=next(iter(validate(HERE)['payloads']));(p/n).write_bytes(b'changed')
            with self.assertRaises(ValueError):validate(p)
if __name__=='__main__':unittest.main()
