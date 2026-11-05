"""Exact real independent joint addenda; no production or scientific acceptance."""
import hashlib,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
class JointReviewTransportTests(unittest.TestCase):
    def test_exact_three_archives_and_original_allowlists(self):
        r=json.loads((ROOT/'reports/lean-433-migration/c39-joint-independent-review-transport.json').read_bytes())
        self.assertEqual([x['members'] for x in r['archives']],[23,7,6])
        for x in r['archives']:
            self.assertEqual(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest(),x['sha256'])
            with zipfile.ZipFile(ROOT/x['path']) as z:
                a=json.loads(z.read(x['allowlist']));names=a.get('members',a.get('public_files'))
                self.assertEqual(set(z.namelist()),set(names));self.assertEqual(len(names),x['members'])
                self.assertEqual(hashlib.sha256(z.read(x['seal'])).hexdigest(),x['seal_sha256'])
                self.assertEqual(hashlib.sha256(z.read(x['allowlist'])).hexdigest(),x['allowlist_sha256'])
                if x['members']==23:
                    pins=json.loads(z.read('final-bindings-v2.json'))['files']
                    self.assertEqual(set(pins),set(names)-{'final-bindings-v2.json','final-seal-v2.json'})
                    for n,d in pins.items():self.assertEqual(hashlib.sha256(z.read(n)).hexdigest(),d)
                else:
                    for p in a['payload']:self.assertEqual(hashlib.sha256(z.read(p['name'])).hexdigest(),p['sha256'])
    def test_distinct_actual_roles_and_explicit_nonacceptance(self):
        r=json.loads((ROOT/'reports/lean-433-migration/c39-joint-independent-review-transport.json').read_bytes())
        self.assertNotEqual(r['decoder_identity'],r['reviewer_identity'])
        for k in ('nativeAccepted','production_candidates_installed','main_merged','scientific_ROOT','PURIFIED'):self.assertIs(r[k],False)
        self.assertIsNone(r['sourceAgreement']);self.assertEqual(r['actual_observations']['owned'],968)
        self.assertEqual(r['actual_observations']['exact_removed_native_axioms'],{'CSP':9,'Cubic':3})
        self.assertEqual(r['actual_observations']['CSP_value_text_omissions'],96)
if __name__=='__main__':unittest.main()
