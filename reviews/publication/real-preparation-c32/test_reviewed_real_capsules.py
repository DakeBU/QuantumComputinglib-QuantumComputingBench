"""Exact independent capsule integrity; no semantic or native acceptance."""
import hashlib,json,pathlib,unittest,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[3];HERE=pathlib.Path(__file__).resolve().parent
sha=lambda raw:hashlib.sha256(raw).hexdigest()
class ReviewedRealCapsules(unittest.TestCase):
    def test_original_phase3_4_exact_allowlist_and_seal(self):
        r=json.loads((ROOT/'reports/lean-433-migration/c41-real-repair-and-metadata-checkpoint.json').read_bytes())
        p=ROOT/r['review_archive']['path'];self.assertEqual(sha(p.read_bytes()),r['review_archive']['sha256'])
        with zipfile.ZipFile(p) as z:
            a=json.loads(z.read('publicsafe-allowlist.json'));s=json.loads(z.read('phase4-seal.json'))
            self.assertEqual(set(z.namelist()),set(a['allowed_payloads'])|set(a['control_files']))
            self.assertEqual(len(z.namelist()),7)
            for n,h in s['artifact_pins'].items():self.assertEqual(sha(z.read(n)),h)
            self.assertEqual(sha(z.read('phase4-seal.json')),'d8b546a987d2b4635ef98095f0d73796f0136821bed8d81f7f0f9d69c6cf3cb4')
            self.assertTrue(s['phase3_completed_before_new_actual_decoder_open'])
            self.assertIsNone(s['sourceAgreement']);self.assertFalse(s['final_accepted_publication_binding_emitted'])
    def test_metadata_original_22_files_and_all_207_current_raw_pins(self):
        p=HERE/'metadata-v3';f=json.loads((p/'freeze.json').read_bytes());m=json.loads((p/'manifest.json').read_bytes())
        self.assertEqual(sha((p/'freeze.json').read_bytes()),'a94627897de1653754e7f496d00a2b19536bc9243fad235b15ee7693e9605e09')
        self.assertEqual(sha((p/'manifest.json').read_bytes()),f['manifest_sha256'])
        self.assertEqual({x.name for x in p.iterdir() if x.is_file()},{x['path'] for x in m['files']}|{'manifest.json','freeze.json'})
        for x in m['files']:self.assertEqual(sha((p/x['path']).read_bytes()),x['sha256'])
        pins=json.loads((p/'current-pins.json').read_bytes())['files'];self.assertEqual(len(pins),207)
        for x in pins:self.assertEqual(sha((ROOT/x['path']).read_bytes()),x['sha256'])
        self.assertIsNone(f['sourceAgreement']);self.assertFalse(f['nativeAccepted'])
    def test_repair_is_literal_convention_only_and_all_old_and_tails_retained(self):
        p=HERE/'metadata-v3';new=(p/'source-effective-v3.md').read_bytes();change=json.loads((p/'source-change-record-v3.json').read_bytes())
        self.assertEqual(sha(new),'dba646110300c6a8e9f8b275eeb0dba2140add2a9f0096934f03a51e886da6cd')
        with zipfile.ZipFile(HERE/'metadata-v2-wip-public-bundle.zip') as z:
            old=z.read('source-effective-v2.md');g=json.loads(z.read('four-view-graph.json'))
        self.assertEqual(new.decode().replace(change['after'],change['before'],1).encode(),old)
        current=json.loads((p/'four-view-graph.json').read_bytes())
        self.assertEqual(current['source_view']['and_hyperedges'][:-1],g['source_view']['and_hyperedges'])
        self.assertEqual(current['functor_view'],g['functor_view'])
        self.assertEqual((ROOT/'docs/publication-c32-v3/source-effective-v3.md').read_bytes(),new)
if __name__=='__main__':unittest.main()
