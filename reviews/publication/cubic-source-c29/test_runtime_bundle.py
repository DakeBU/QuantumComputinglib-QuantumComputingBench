"""Exact public runtime audit bundle and explicit pretty-print gaps."""
import hashlib
import json
from pathlib import Path
import unittest
import zipfile
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()


class RuntimeBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt=load(ROOT/'reports/lean-433-migration/c29-ci3-independent-transport.json')
        with zipfile.ZipFile(ROOT/cls.receipt['bundle']) as z:
            cls.files={n:z.read(n) for n in z.namelist()}
        cls.rows=json.loads(cls.files['actual-450-generated-full-fields.json'])

    def test_exact_original_members_and_separate_packaging_identity(self):
        self.assertEqual(sha((ROOT/self.receipt['bundle']).read_bytes()),self.receipt['bundle_sha256'])
        self.assertEqual(len(self.files),16)
        self.assertEqual(len(self.receipt['members']),15)
        for row in self.receipt['members']:
            self.assertEqual(sha(self.files[row['member']]),row['sha256'])
            self.assertEqual(len(self.files[row['member']]),row['bytes'])
        self.assertEqual(sha(self.files['publicsafe-allowlist.json']),self.receipt['inner_allowlist_sha256'])
        self.assertEqual(sha(self.files['packet.json']),self.receipt['original_packet_sha256'])

    def test_full_generated_record_array_matches_actual_ci3_stream(self):
        with zipfile.ZipFile(HERE/'ci3-formal-runtime-public.zip') as z:
            stream=z.read('06-probe-v5.stdout.raw.sanitized.txt').decode()
        rows=[json.loads(s.split(' ',1)[1]) for s in stream.splitlines() if s.startswith('C29_GENERATED_JSON ')]
        self.assertEqual(rows,self.rows)
        self.assertEqual(len(self.rows),450)

    def test_two_real_type_gaps_are_not_just_omitted_proofs(self):
        gaps=json.loads(self.files['two-signature-real-omission-audit.json'])
        affected=[row for row in self.rows if '⋯' in row['typePrettyExplicit']]
        self.assertEqual(len(affected),2)
        self.assertEqual({r['actualName'] for r in affected},{r['exactName'] for r in gaps['rows']})
        self.assertEqual(gaps['generatedValueRowsWithOmission'],96)
        self.assertEqual(gaps['generatedValueOmissionGlyphCount'],1004)
        for row in gaps['rows']:
            self.assertTrue(row['omissionAffectsBinderDomains'])
            self.assertTrue(row['omissionAffectsDataTermsAndEqRHS'])
            self.assertFalse(row['onlyProofArguments'])
            self.assertFalse(row['completeMathematicalSignatureReconstructibleFromCapturedText'])
        explicit=json.loads(self.files['actual-319-explicit.json'])
        self.assertEqual(len(explicit),319)
        self.assertTrue(all('⋯' not in r['typePrettyExplicit'] for r in explicit))

    def test_machine_value_inspection_not_all_token_cognitive_or_trust_claim(self):
        packet=json.loads(self.files['packet.json'])
        self.assertFalse(packet['wholeTargetTrustClosed'])
        self.assertFalse(packet['losslessExpr'])
        self.assertIn('2_INCOMPLETE',packet['generatedFullMathematicalSignatureText'])
        self.assertIn('96_PRESENT_STRINGS_HAVE_PP_OMISSIONS',packet['generatedValues'])
        scope=json.loads(self.files['review-scope-and-delta.json'])
        self.assertEqual(scope['generated450']['rowsAllMachineTraversed'],450)
        self.assertEqual(scope['generated450']['ppSignatureResiduals'],2)
        self.assertFalse(scope['generated450']['rawKernelExprSerialized'])

    def test_native_and_source_decisions_remain_unassessed(self):
        for row in (self.receipt,json.loads(self.files['packet.json'])):
            for key in ('sourceAgreement','publicationBinding','axiomPolicyPass'):
                self.assertIsNone(row[key])
            self.assertFalse(row['nativeAccepted'])
            self.assertFalse(row['scientific_ROOT'])


if __name__=='__main__':
    unittest.main()
