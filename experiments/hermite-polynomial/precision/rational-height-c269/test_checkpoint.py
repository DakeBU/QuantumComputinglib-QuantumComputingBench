import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class Bindings(unittest.TestCase):
    def test_payloads(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes())
        for n,h in b['payloads'].items():self.assertEqual(sha((ROOT/n).read_bytes()),h,n)
        self.assertFalse(b['scientific_ROOT']);self.assertFalse(b['main_merged'])
    def test_original_members(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes());a=b['archive']
        self.assertEqual(sha((ROOT/a['file']).read_bytes()),a['sha256'])
        with ZipFile(ROOT/a['file']) as z:
            self.assertEqual(set(z.namelist()),set(a['members']))
            for n,r in a['members'].items():
                x=z.read(n);self.assertEqual(len(x),r['bytes']);self.assertEqual(sha(x),r['sha256'])

class HeightFrontier(unittest.TestCase):
    def test_type_formation_is_not_four_proofs(self):
        r=json.loads((ROOT/'type-probe-result.json').read_bytes())
        self.assertEqual(r['status'],'TYPECHECKED_DEFINITIONS_NOT_PROVED')
        self.assertEqual(r['proposition_formations'],4);self.assertEqual(r['proved_roots'],0)
    def test_actual_first_root_and_own_consumer(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes());a,b=r['records']
        self.assertEqual(r['status'],'PROVED_LOCALLY_FOCUSED');self.assertEqual(r['actual_own_consumed_roots'],1)
        self.assertEqual([a['exit_code'],b['exit_code']],[0,0])
        self.assertEqual(b['selected_direct_provider_hashes'],[a['own_output_sha256']])
        self.assertEqual({x['name'] for x in b['axiom_reports']},{'HermiteRationalHeight.heightBound','C282ExactChecks.heightBoundExpandedCheck'})
        for x in b['axiom_reports']:self.assertEqual(set(x['axioms']),{'propext','Classical.choice','Quot.sound'})
    def test_seal_precedes_author_and_expanded_signature(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            raw=z.read('hermite-c280-rational-height-preproof-seal/STATEMENT_SEAL.json')
            a=json.loads(z.read('hermite-c282-rational-height-bound-proof/AUTHOR_FREEZE.json'))
            self.assertEqual(a['preproof_seal_sha256'],sha(raw))
        s=(ROOT/'ExactChecks.lean').read_text(encoding='utf-8')
        self.assertIn('q.num.natAbs < 2^B',s);self.assertIn('q.den < 2^B',s);self.assertIn('1 ≤ B',s)
    def test_no_producer_or_native_credit(self):
        r=json.loads((ROOT/'proof-result.json').read_bytes())
        for key in ['other_three_roots_proved','actual_producer_height_native_GCD_evaluator_allocation_or_scientific_ROOT',
                    'independent_review','clean_transitive_TCB','main_merged']:
            self.assertFalse(r[key],key)
