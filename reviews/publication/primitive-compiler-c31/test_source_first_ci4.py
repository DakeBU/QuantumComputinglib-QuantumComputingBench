"""Original CI4 reviewer confirms native blockers without total admission."""
import hashlib,json,re,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
class SourceFirstCI4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/'reports/lean-433-migration/c31-ci4-source-first-review-transport.json').read_bytes())
        cls.raw=(ROOT/cls.r['bundle']).read_bytes()
        with zipfile.ZipFile(ROOT/cls.r['bundle']) as z:cls.files={n:z.read(n) for n in z.namelist()}
        cls.seal=json.loads(cls.files['phase3-ci4-evidence-seal.json'])
    def test_exact_six_files_and_safe_scope(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(),self.r['bundle_sha256']);self.assertEqual(len(self.files),6)
        for m in self.r['members']:
            raw=self.files[m['name']];self.assertEqual(hashlib.sha256(raw).hexdigest(),m['sha256']);self.assertEqual(len(raw),m['bytes'])
            self.assertIsNone(re.search(rb'(?:[A-Za-z]:[\\/](?:Users|qb261009)|/home/runner/|github_pat_|ghp_)',raw))
    def test_actual_200_partition_and_native_consumer_blockers(self):
        s=self.seal;self.assertEqual((s['checks']['roots'],s['checks']['generated'],s['checks']['owned']),(87,113,200))
        self.assertEqual(len(s['selfAxioms']),3);self.assertEqual([r['consumerCountIncludingSelf'] for r in s['selfAxioms']],[19,6,7])
        self.assertTrue(s['checks']['externalInventoryNotConflatedWithProjectCopies'])
        self.assertEqual(s['checks']['values']['NOT_REQUESTED_VALUE_AVAILABLE'],194)
        self.assertFalse(self.r['all_fields_directly_from_kernel']);self.assertTrue(self.r['ordinary_kernel_native_blockers_open'])
    def test_no_total_promotion_or_provenance_conflation(self):
        for obj in (self.seal,self.r):
            self.assertIsNone(obj['sourceAgreement']);self.assertIsNone(obj['publicationBinding']);self.assertFalse(obj['nativeAccepted']);self.assertFalse(obj['scientific_ROOT'])
        self.assertFalse(self.seal['executionIdentity']['exactExecutedCheckoutIndependentlyAttested'])
        self.assertTrue(self.seal['executionIdentity']['APIHeadAndContextNotConflated'])
        self.assertEqual(len(self.seal['immutablePriorArtifacts']),11)
if __name__=='__main__':unittest.main()
