"""Scoped independent source agreement is not generated-native admission."""
import hashlib
import json
from pathlib import Path
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[3]
sha=lambda b:hashlib.sha256(b).hexdigest()

class FinalActualReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/'reports/lean-433-migration/c29-final-actual-review-transport.json').read_bytes())
        cls.bundles={}
        for key in ('review','late_opaque_bridge'):
            row=cls.r[key]
            with zipfile.ZipFile(ROOT/row['bundle']) as z:
                cls.bundles[key]={n:z.read(n) for n in z.namelist()}
        cls.review=cls.bundles['review'];cls.late=cls.bundles['late_opaque_bridge']
        cls.seal=json.loads(cls.review['final-actual-comparison-v1-seal.json'])

    def test_exact_two_bundles_and_original_seals(self):
        for key,expected in [('review',12),('late_opaque_bridge',7)]:
            row=self.r[key];files=self.bundles[key]
            self.assertEqual(sha((ROOT/row['bundle']).read_bytes()),row['bundle_sha256'])
            self.assertEqual(len(files),expected)
            self.assertEqual(set(files),{r['member'] for r in row['members']})
            for member in row['members']:
                self.assertEqual((sha(files[member['member']]),len(files[member['member']])),(member['sha256'],member['bytes']))
        self.assertEqual(sha(self.review['final-actual-comparison-v1-seal.json']),'167c822867163fc7f5679a6ee712f68afb9089072274788761c35eb81b9bcc11')
        for row in self.seal['artifacts']:
            self.assertEqual(sha(self.review[row['path'].removeprefix('$REVIEWER/')]),row['sha256'])

    def test_report_scoped_agreement_is_separate_from_native_blocker(self):
        s=self.seal
        self.assertTrue(s['sourceAgreement']['supported'])
        self.assertEqual(s['status'],'SCOPED_SOURCE_AGREEMENT_WITH_NATIVE_TRUST_ADMISSION_BLOCKER')
        self.assertEqual(s['checks']['actualGeneratedNativeAxioms'],9)
        self.assertTrue(s['trust']['nativeAdmissionBlocked'])
        self.assertFalse(s['trust']['existingSourceScannerCoversGeneratedNativeTCB'])
        self.assertEqual(s['trust']['nonDiagnosticNativeConsumerChain'],[189,196,203,'generated233'])
        self.assertIsNone(s['trust']['axiomPolicyPass'])
        self.assertFalse(s['nativeAccepted']);self.assertFalse(s['canonicalAdmission'])
        self.assertFalse(s['scientific_ROOT']);self.assertFalse(s['mainCompletion'])
        self.assertEqual(s['openSourceGaps'],['G'+str(i).zfill(2) for i in range(1,15)])

    def test_two_type_text_holes_closed_but_ordinary_values_and_source_binding_not_inflated(self):
        checks=self.seal['checks']
        self.assertEqual(checks['actualTypeOmissionRowsAfterSupplement'],0)
        self.assertEqual(checks['remainingGeneratedValueOmissionRows'],96)
        self.assertEqual(checks['otherGeneratedExpandedTypeValueStringsNotBlanketManualRead'],268)
        self.assertFalse(self.seal['inputBindings']['author202AmbientBindingActuallyReplayed'])
        late=json.loads(self.late['packet.json'])
        self.assertTrue(late['requestedOpaqueBindingAcknowledged'])
        self.assertIsNone(late['acceptedReconstructionConclusion'])
        self.assertIsNone(late['sourceAgreement']);self.assertFalse(late['nativeAccepted'])
        self.assertFalse(self.r['nativeAccepted']);self.assertIsNone(self.r['publicationBinding'])

    def test_only_new_allowlisted_safe_original_bytes(self):
        allow=json.loads(self.review['final-actual-comparison-v1-public-allowlist.json'])
        expected={r['relativePath'] for r in allow['files']}|{'final-actual-comparison-v1-public-allowlist.json'}
        self.assertEqual(set(self.review),expected)
        self.assertNotIn('source-only-notes.md',self.review)
        self.assertNotIn('phase1-seal.json',self.review)
        for files in self.bundles.values():
            for name,data in files.items():
                self.assertNotIn('/',name);self.assertNotIn('\\',name)
                for forbidden in (b'C:/Users/',b'C:\\Users\\',b'D:/Users/',b'D:\\Users\\',b'/home/runner/',b'github_pat_',b'ghp_'):
                    self.assertNotIn(forbidden,data)

if __name__=='__main__':unittest.main()
