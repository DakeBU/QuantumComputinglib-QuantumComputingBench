import hashlib,json,unittest
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class ExactCheckpoint(unittest.TestCase):
    def test_exact_archived_originals(self):
        b=json.loads((ROOT/'source-binding.json').read_bytes())
        for n,h in b['payloads'].items():self.assertEqual(sha((ROOT/n).read_bytes()),h,n)
        self.assertEqual(sha((ROOT/'original-freezes.zip').read_bytes()),b['archive_sha256'])
        with ZipFile(ROOT/'original-freezes.zip') as z:
            self.assertEqual(set(z.namelist()),set(b['original_members']))
            for n,r in b['original_members'].items():
                raw=z.read(n);self.assertEqual((len(raw),sha(raw)),(r['bytes'],r['sha256']))
        self.assertFalse(b['main_merged']);self.assertFalse(b['scientific_ROOT'])

class SuffixTypes(unittest.TestCase):
    def test_exact_type_formation_chain_not_proof(self):
        r=json.loads((ROOT/'type-probe-result.json').read_bytes());a,b=r['records']
        self.assertEqual(r['status'],'TYPECHECKED_DEFINITIONS_NOT_PROVED')
        self.assertEqual([a['exit_code'],b['exit_code']],[0,0]);self.assertEqual(r['proved_roots'],0)
        self.assertEqual(r['proposition_formations'],3)
        self.assertEqual(b['selected_direct_provider_hashes'],[a['own_output_sha256']])
        self.assertEqual(a['source_sha256'],sha((ROOT/'SourceSuffixDefinitions.lean').read_bytes()))
        self.assertEqual(b['source_sha256'],sha((ROOT/'ExactTypeChecks.lean').read_bytes()))
    def test_exact_preproof_seal_and_no_excess_binders(self):
        s=json.loads((ROOT/'STATEMENT_SEAL.json').read_bytes())
        self.assertEqual(s['definition_sha256'],sha((ROOT/'SourceSuffixDefinitions.lean').read_bytes()))
        self.assertEqual(s['signature_sha256'],sha((ROOT/'sealed-signatures.txt').read_bytes()))
        self.assertEqual(s['type_probe_result_sha256'],sha((ROOT/'type-probe-result.json').read_bytes()))
        self.assertEqual((ROOT/'sealed-definitions.lean').read_bytes(),(ROOT/'SourceSuffixDefinitions.lean').read_bytes())
        self.assertEqual(s['binder_audit']['EXCESS'],[]);self.assertEqual(len(s['closed_targets']),3)
        self.assertEqual(s['mathematical_proofs_accepted'],0)
        self.assertTrue(s['proof_search_authorized_only_after_this_seal']);self.assertFalse(s['main_merged'])
