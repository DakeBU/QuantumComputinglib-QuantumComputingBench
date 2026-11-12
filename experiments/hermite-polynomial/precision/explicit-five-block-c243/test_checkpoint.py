import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class BindingTests(unittest.TestCase):
    def test_bound_payloads(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes())
        for n,h in b['payloads'].items(): self.assertEqual(sha((ROOT/n).read_bytes()),h,n)
        self.assertFalse(b['scientific_ROOT']);self.assertFalse(b['main_merged'])
    def test_original_archive_members(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes())
        a=b['archive'];raw=(ROOT/a['file']).read_bytes();self.assertEqual(sha(raw),a['sha256'])
        with ZipFile(ROOT/a['file']) as z:
            self.assertEqual(set(z.namelist()),set(a['members']))
            for n,r in a['members'].items():
                x=z.read(n);self.assertEqual(len(x),r['bytes']);self.assertEqual(sha(x),r['sha256'])

class ProducerTests(unittest.TestCase):
    def test_actual_type_formation_is_not_proof(self):
        r=json.loads((ROOT/'type-probe-result.json').read_bytes())
        self.assertEqual(r['status'],'TYPECHECKED_DEFINITIONS_NOT_PROVED')
        self.assertEqual([x['exit_code'] for x in r['records']],[0,0])
        self.assertEqual(r['proposition_formations'],8);self.assertEqual(r['proof_roots'],0)
        self.assertFalse(r['full_SP_resource_or_scientific_ROOT'])
    def test_original_failure_is_preserved(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            r=json.loads(z.read('hermite-c246-explicit-five-block-type-probe/type-probe-result.redacted.json'))
            self.assertEqual(r['records'][0]['exit_code'],1)
            self.assertIsNone(r['records'][0]['own_output_sha256'])
            self.assertEqual(r['proof_roots'],0)
    def test_only_transport_changed(self):
        with ZipFile(ROOT/'original-freezes.zip') as z:
            a=z.read('hermite-c243-explicit-five-block-definitions/ExplicitFiveBlockDefinitions.lean').decode()
            b=z.read('hermite-c248-explicit-five-block-transport-repair/ExplicitFiveBlockDefinitions.lean').decode()
            old='  let original : FullIndex k delta := hd ▸ index.run.value'
            new='  let original : FullIndex k delta := Eq.mp (congrArg (fun e => FiveIndex e (2*k+1)) hd) index.run.value'
            self.assertEqual(a.count(old),1);self.assertEqual(a.replace(old,new),b)
    def test_explicit_scalar_body_and_preproof_boundary(self):
        s=(ROOT/'ExplicitFiveBlockDefinitions.lean').read_text(encoding='utf-8')
        for token in ['actualBlocksQ','actualEntryQ','actualLeftQ','actualRightQ','Nat.choose']:
            self.assertNotIn(token,s)
        q=json.loads((ROOT/'STATEMENT_SEAL.json').read_bytes())
        self.assertEqual(len(q['approved_declarations']),8)
        self.assertFalse(q['proof_search_preceded_seal'])
        self.assertTrue(q['budget_is_unproved_partial_annotation'])
