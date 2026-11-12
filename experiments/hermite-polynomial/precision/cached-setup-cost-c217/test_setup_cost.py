import hashlib,json,re,sys,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[3]))
from tools.proof_trust import strip_lean_comments_and_strings
sha=lambda b:hashlib.sha256(b).hexdigest()
def validate(root):
    b=json.loads((root/'source-binding.json').read_bytes())
    for n,h in b['payloads'].items():
        if sha((root/n).read_bytes())!=h:raise ValueError('payload mismatch')
    a=b['archive']
    if sha((root/a['file']).read_bytes())!=a['sha256']:raise ValueError('archive mismatch')
    with ZipFile(root/a['file']) as z:
        if len(z.namelist())!=len(set(z.namelist())) or set(z.namelist())!=set(a['members']):raise ValueError('inventory mismatch')
        for n,m in a['members'].items():
            if (len(z.read(n)),sha(z.read(n)))!=(m['bytes'],m['sha256']):raise ValueError('original mismatch')
    return b,json.loads((root/'proof-result.json').read_bytes())
class SetupCost(unittest.TestCase):
    def test_sources_no_holes_and_exact_raw_binding(self):
        b,_=validate(HERE)
        for n in ['SetupCostProof.lean','SetupCostProofChecks.lean','SetupCostAudit.lean']:
            self.assertIsNone(re.search(r'\b(sorry|admit|unsafe|axiom|native_decide)\b',strip_lean_comments_and_strings((HERE/n).read_text(encoding='utf-8'))))
        self.assertTrue(b['parent_actual_loaded_definitions_read']);self.assertFalse(b['parent_all_expanded_proof_terms_read'])
    def test_actual_own_root_consumer_and_body_audit(self):
        _,p=validate(HERE);a,c,d=p['records']
        self.assertEqual(p['status'],'PROVED_LOCALLY_FOCUSED');self.assertEqual(p['actual_proved_roots'],1)
        for r in [a,c,d]:self.assertEqual(r['exit_code'],0);self.assertFalse(r['timeout'])
        self.assertEqual(a['axiom_reports'],[])
        for r in [c,d]:
            self.assertEqual(r['selected_direct_provider_sha256'],a['own_output_sha256'])
            self.assertEqual(r['direct_provider'],'OWN/SetupCostProof.olean')
            self.assertEqual([x['name'] for x in r['axiom_reports']],['HermiteCachedPiecewiseStored.rightSetup_total_le'])
            self.assertEqual(set(r['axiom_reports'][0]['axioms']),{'propext','Classical.choice','Quot.sound'})
        self.assertTrue(p['definition_print_audit_compiled'])
    def test_both_failed_sources_retained_without_outputs(self):
        b,_=validate(HERE)
        with ZipFile(HERE/b['archive']['file']) as z:
            self.assertEqual(len(z.namelist()),26)
            for packet in ['hermite-c210-actual-setup-cost-proof','hermite-c216-repaired-setup-cost-proof']:
                p=json.loads(z.read(packet+'/proof-result.json'))
                self.assertEqual(p['actual_proved_roots'],0);self.assertEqual(len(p['records']),1)
                self.assertEqual(p['records'][0]['exit_code'],1);self.assertIsNone(p['records'][0]['own_output_sha256'])
            s=json.loads(z.read('hermite-c202-setup-cost-contract/STATEMENT_SEAL.json'))
            self.assertEqual(s['binder_audit']['EXCESS'],[]);self.assertEqual(s['binder_audit']['logical_premises'],[])
    def test_reviewed_successor_context_not_relabelled_old(self):
        b,p=validate(HERE)
        self.assertFalse(p['original_frozen_context_rewritten'])
        self.assertEqual(p['successor_context_sha256'],'3d961e2d29ffa1b2f7f95bc1437b0fe87c7c1826afce675cafc59e037fcd1f88')
        self.assertEqual(p['linked_policy_sha256'],'27053a22f580d8785b54baa8f9d8fd7968ca1b1b2484496a555f8c3393c8c8cd')
        self.assertEqual(p['original_preproof_C202_seal_sha256'],'e8109bf4623955cc959f7dbbe9bba81def8de5add68f18714eaeee89f47b4be0')
        for key in ['independent_mathematical_review','full_native_bit_or_quantum_cost','scientific_ROOT','main_merged','PURIFIED']:self.assertFalse(b[key])
    def test_missing_and_changed_evidence_fail(self):
        import tempfile,shutil
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);shutil.copyfile(HERE/'source-binding.json',p/'source-binding.json')
            with self.assertRaises(FileNotFoundError):validate(p)
            b,_=validate(HERE);n=next(iter(b['payloads']));(p/n).write_bytes(b'changed')
            with self.assertRaises(ValueError):validate(p)
if __name__=='__main__':unittest.main()
