"""Immutable erratum: audit all450 table flags against the actual CI stream."""
import hashlib
import json
from pathlib import Path
import unittest
import zipfile
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest()

class OmissionCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt=json.loads((ROOT/'reports/lean-433-migration/c29-ci3-omission-correction-transport.json').read_bytes())
        with zipfile.ZipFile(ROOT/cls.receipt['bundle']) as z:cls.new={n:z.read(n) for n in z.namelist()}
        with zipfile.ZipFile(ROOT/cls.receipt['historical_bundle']) as z:cls.old={n:z.read(n) for n in z.namelist()}
        cls.rows=json.loads(cls.old['actual-450-generated-full-fields.json'])
        cls.table=json.loads(cls.new['all-generated-audit-table-reviewed.json'])

    def test_exact_corrected_bundle_and_four_original_members(self):
        self.assertEqual(sha((ROOT/self.receipt['bundle']).read_bytes()),self.receipt['bundle_sha256'])
        self.assertEqual(len(self.new),4)
        for row in self.receipt['members']:
            self.assertEqual(sha(self.new[row['member']]),row['sha256'])
            self.assertEqual(len(self.new[row['member']]),row['bytes'])

    def test_old_erroneous_pre_review_field_preserved_not_rewritten(self):
        old=self.old['all-generated-audit-table.json']
        self.assertEqual(sha(old),self.receipt['prior_table_sha256'])
        original=json.loads(old)
        self.assertEqual(len(original),450)
        self.assertNotEqual(original,self.table)
        packet=json.loads(self.new['omission-correction-packet.json'])
        self.assertEqual(packet['supersededPreReviewTableSHA256'],sha(old))
        self.assertFalse(packet['originalRuntimeFilesChanged'])
        self.assertIn('only U+2026',packet['reason'])

    def test_all450_corrected_flags_recomputed_from_actual_strings(self):
        self.assertEqual(len(self.rows),450);self.assertEqual(len(self.table),450)
        for row,audit in zip(self.rows,self.table):
            self.assertEqual(row['actualName'],audit['actualName'])
            t=row['typePrettyExplicit'];v=row['valuePrettyExplicitAllowOpaque'] or ''
            self.assertEqual(audit['actualTypePrettyOmissionGlyph'],'⋯' in t)
            self.assertEqual(audit['actualValuePrettyOmissionGlyph'],'⋯' in v)
            self.assertEqual(audit['typeU22EFOmissionCount'],t.count('⋯'))
            self.assertEqual(audit['valueU22EFOmissionCount'],v.count('⋯'))
            self.assertEqual(audit['actualPrettyEllipsis'],any(g in t+v for g in ('⋯','…')))
        self.assertEqual(sum(x['actualTypePrettyOmissionGlyph'] for x in self.table),2)
        self.assertEqual(sum(x['actualValuePrettyOmissionGlyph'] for x in self.table),96)

    def test_current_selection_exact14_old_plus_two_new_not_planned_loose_files(self):
        allow=json.loads(self.new['publicsafe-allowlist-reviewed.json'])
        self.assertEqual(len(allow['files']),16)
        old_count=0
        for row in allow['files']:
            name=Path(row['relativePath']).name
            raw=self.new[name] if name in self.new else self.old[name]
            old_count+=name not in self.new
            self.assertEqual(sha(raw),row['sha256'])
        self.assertEqual(old_count,14)
        self.assertIn('all-generated-audit-table.json',allow['excludedPriorTable'])

    def test_old_final_boundary_already_had_true_two_and96_counts(self):
        boundary=json.loads(self.old['two-signature-real-omission-audit.json'])
        self.assertEqual(len(boundary['rows']),2)
        self.assertEqual(boundary['generatedValueRowsWithOmission'],96)
        self.assertEqual(boundary['generatedValueOmissionGlyphCount'],1004)

    def test_correction_not_new_native_or_acceptance_evidence(self):
        packet=json.loads(self.new['omission-correction-packet.json'])
        self.assertEqual(packet['newLeanRuns'],0);self.assertFalse(packet['newMathematics'])
        for obj in (packet,self.receipt,json.loads(self.new['seal.json'])):
            self.assertIsNone(obj['sourceAgreement']);self.assertIsNone(obj['axiomPolicyPass'])
            self.assertFalse(obj['nativeAccepted']);self.assertFalse(obj['scientific_ROOT'])

if __name__=='__main__':unittest.main()
