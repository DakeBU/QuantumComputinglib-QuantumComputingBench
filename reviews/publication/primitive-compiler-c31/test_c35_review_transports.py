"""Independent sealed artifacts remain exact and do not self-admit."""
import hashlib,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
class IndependentKernelTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=json.loads((ROOT/'reports/lean-433-migration/c35-original-kernel-review-transport.json').read_bytes())
    def test_exact_two_allowlists_and_all_bytes(self):
        for packet,count in zip(self.r['packets'],[13,7]):
            path=ROOT/packet['archive'];self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),packet['archive_sha256'])
            with zipfile.ZipFile(path) as z:
                self.assertEqual(len(z.namelist()),count)
                self.assertEqual(set(z.namelist()),{r['name'] for r in packet['members']})
                for row in packet['members']:
                    raw=z.read(row['name']);self.assertEqual((len(raw),hashlib.sha256(raw).hexdigest()),(row['bytes'],row['sha256']))
    def test_exhaustive_independent_decoder_result_agrees_with_actual(self):
        with zipfile.ZipFile(ROOT/self.r['packets'][0]['archive']) as z:
            summary=json.loads(z.read('evidence-summary.json'));delta=json.loads(z.read('whole-owned-replay.json'))
            self.assertEqual((summary['sourceRoots'],summary['newGenerated'],summary['newOwned']),(87,113,200))
            self.assertEqual(summary['surviving'],197);self.assertEqual(summary['axiomClosuresChanged'],21)
            self.assertEqual(len(delta['removed']),3);self.assertEqual(len(delta['added']),3)
            self.assertEqual(delta['unexpectedDifferenceNames'],[])
            self.assertEqual(summary['newAxiomUnion'],['Classical.choice','Quot.sound','propext'])
            self.assertTrue(summary['originalSourceBlindScopePreserved'])
            self.assertFalse(summary['nativeAccepted']);self.assertIsNone(summary['sourceAgreement'])
    def test_source_first_review_and_joint_scope_are_not_final_wrappers(self):
        self.assertNotEqual(self.r['decoder_identity'],self.r['reviewer_identity'])
        with zipfile.ZipFile(ROOT/self.r['packets'][1]['archive']) as z:
            text=z.read('review.md').decode();carry=z.read('carryforward.md').decode()
            self.assertIn('PENDING_EXACT_FORMAL_METADATA_BRIDGE',text)
            self.assertIn('not a final registry',text)
            self.assertIn('not a joint-build observation',carry)
            self.assertIn('without reading this round',text)
        for key in ['production_changed','old_seals_changed','registry_changed','nativeAccepted','scientific_ROOT','main_admission']:
            self.assertFalse(self.r[key])
if __name__=='__main__':unittest.main()
