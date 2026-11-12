"""Actual whole-target source-read agreement preserves its signature-export failure."""
import hashlib,json,unittest,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
SHA=lambda b:hashlib.sha256(b).hexdigest()
class ActualWholeRobinReviewTests(unittest.TestCase):
    def test_exact16_originals_explicit_permission_and_all14_hashes(self):
        with zipfile.ZipFile(BASE/'source-formal-stage4-original16.zip') as z:
            prefix='W/robin-c47-source-formal-stage4/'
            self.assertEqual(len(z.namelist()),16)
            self.assertEqual(SHA(z.read('seal.json')),'4af475e99b1f4a5211c0a8fc9cb78ed90ea2c9710a8d726a11b1a6254997fc64')
            self.assertEqual(SHA(z.read('SHA256SUMS.json')),'a0aad2d58f314e1ca0abbdc9a9c26ed684238aed0185c417d23bac0107a78d86')
            manifest=json.loads(z.read('SHA256SUMS.json'))
            self.assertEqual(set(z.namelist()),{p.removeprefix(prefix) for p in manifest['exactPublicsafeSet']})
            self.assertEqual(set(z.namelist()),{p.removeprefix(prefix) for p in json.loads(z.read('publicsafe-allowlist.json'))['files']})
            self.assertEqual(len(manifest['files']),14)
            for row in manifest['files']:self.assertEqual(SHA(z.read(row['path'].removeprefix(prefix))),row['sha256'])
    def test_actual_semantic_verdict_full9_coverage_no_excess_at_source_read_tier(self):
        with zipfile.ZipFile(BASE/'source-formal-stage4-original16.zip') as z:
            findings=json.loads(z.read('typed-findings.json'))
            self.assertEqual(findings['mathematicalFidelityVerdict'],'SCOPED_SOURCE_FORMAL_AGREEMENT_AT_SOURCE_READ_LEVEL')
            self.assertEqual(findings['mathematicalFailureClass'],'NONE')
            self.assertEqual(findings['coverage']['wholeTargets'],9);self.assertEqual(findings['coverage']['explicitDeclarations'],215)
            self.assertEqual(findings['coverage']['ambientCommands'],53)
            self.assertEqual(findings['assumptionAudit']['explicitPrefixGroups'],247);self.assertEqual(findings['assumptionAudit']['EXCESS'],0)
            self.assertEqual(SHA(z.read('mathematical-fidelity-report.md')),'27970e37e2dead9dad31422f43923694a6deaa14a07b680c86a4ec4dec6144e8')
    def test_genuine18_signature_boundary_defects_remain_open(self):
        with zipfile.ZipFile(BASE/'source-formal-stage4-original16.zip') as z:
            issue=json.loads(z.read('signature-annex-findings.json'));typed=json.loads(z.read('typed-findings.json'))
            self.assertEqual(issue['count'],18);self.assertEqual(issue['whereCases'],12);self.assertEqual(issue['equationCases'],6)
            self.assertEqual(len(issue['differences']),18)
            self.assertEqual(typed['findings'][0]['status'],'OPEN_IN_PINNED_C49_ANNEX')
            self.assertEqual(typed['artifactFailureClass'],'IMPLEMENTATION_FAILED')
            self.assertIn('NOT_ACCEPTED',typed['signatureAnnexVerdict'])
    def test_no_final_metadata_binding_compile_or_scientific_root_was_fabricated(self):
        with zipfile.ZipFile(BASE/'source-formal-stage4-original16.zip') as z:
            typed=json.loads(z.read('typed-findings.json'))
            self.assertTrue(typed['publicationBindingVerdict'].startswith('NOT_PERFORMED'))
            boundaries=' '.join(typed['remainingUnresolved'])
            for key in ('Lean elaboration','wholeRobinMatrix','finitebit','metadata11fields','PURIFIED'):self.assertIn(key,boundaries)
if __name__=='__main__':unittest.main()
