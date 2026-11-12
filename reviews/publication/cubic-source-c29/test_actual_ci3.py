"""Real complete generated observations, not source fidelity or trust acceptance."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()


class ActualCI3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt=load(ROOT/'reports/lean-433-migration/c29-actual-ci3-runtime.json')
        with zipfile.ZipFile(ROOT/cls.receipt['archive']) as z:
            cls.files={name:z.read(name) for name in z.namelist()}
        cls.stream=cls.files['06-probe-v5.stdout.raw.sanitized.txt'].decode()
        cls.records={}
        for line in cls.stream.splitlines():
            if line.startswith('C29_'):
                tag,body=line.split(' ',1)
                cls.records.setdefault(tag,[]).append(json.loads(body))
        spec=importlib.util.spec_from_file_location('actual_ci3_v2',ROOT/'tools/cubic_c29_diagnostic/validate-output-v2.py')
        cls.validator=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.validator)

    def test_exact_archive_all38_members(self):
        self.assertEqual(sha((ROOT/self.receipt['archive']).read_bytes()),self.receipt['archive_sha256'])
        self.assertEqual(len(self.files),38)
        self.assertEqual(set(self.files),{r['path'] for r in self.receipt['files']})
        for row in self.receipt['files']:
            self.assertEqual(sha(self.files[row['path']]),row['sha256'])
            self.assertEqual(len(self.files[row['path']]),row['bytes'])

    def test_actual_calls_and_checkout_not_inferred_from_branch(self):
        self.assertEqual(self.receipt['actual_checkout_merge_commit'],'84613488476803f84482d5ac74661f339326fe3b')
        self.assertEqual(self.receipt['job_conclusion'],'success')
        calls=self.receipt['actual_calls']
        self.assertEqual([r['PID'] for r in calls],[5640,5646,5652,5668])
        for row in calls:
            self.assertEqual(row['exitCode'],0)
            self.assertFalse(row['timedOut'])
            self.assertEqual(json.loads(self.files[row['label']+'.result.json']),{k:v for k,v in row.items() if k!='label'})

    def test_original_and_generated_validator_replay_real_stream(self):
        checked=self.validator.validate(load(ROOT/'tools/cubic_c29_diagnostic/expected-roots.json'),self.stream,0)
        self.assertEqual(checked,self.receipt['actual_completeness'])
        self.assertEqual((checked['explicitRoots'],checked['privateRoots'],checked['generatedActualFieldsCollected']),(319,50,450))
        self.assertFalse(checked['wholeTargetTrustClosed'])
        self.assertIsNone(checked['axiomPolicyPass'])

    def test_real_missing_generated_and_nonzero_exit_are_rejected(self):
        expected=load(ROOT/'tools/cubic_c29_diagnostic/expected-roots.json')
        lines=self.stream.splitlines()
        index=next(i for i,s in enumerate(lines) if s.startswith('C29_GENERATED_JSON '))
        with self.assertRaises(ValueError):
            self.validator.validate(expected,'\n'.join(lines[:index]+lines[index+1:]),0)
        with self.assertRaises(ValueError):
            self.validator.validate(expected,self.stream,1)

    def test_nine_actual_native_axiom_types_and_no_fabricated_values(self):
        rows=self.records['C29_GENERATED_JSON']
        self.assertEqual(len(rows),450)
        self.assertEqual(len({r['actualName'] for r in rows}),450)
        axioms=[r for r in rows if r['actualKind']=='axiomInfo']
        self.assertEqual(len(axioms),9)
        for row in axioms:
            self.assertIn('._native.native_decide.',row['actualName'])
            self.assertIn('@Eq.{1} Bool',row['typePrettyExplicit'])
            self.assertIn('Bool.true',row['typePrettyExplicit'])
            self.assertIsNone(row['valuePrettyExplicitAllowOpaque'])
            self.assertFalse(row['actualHasValueAllowOpaque'])
            self.assertTrue(row['selfOccursInAxioms'])
            self.assertIn(row['actualName'],row['axioms'])
            self.assertFalse(row['isUnsafe'])
            self.assertIsNone(row['axiomPolicyPass'])
        self.assertTrue(all(not row['isUnsafe'] for row in rows))

    def test_explicit319_matches_previous_actual_runtime(self):
        with zipfile.ZipFile(HERE/'ci2-formal-runtime-public.zip') as old:
            stream=old.read('06-probe-v4.stdout.raw.sanitized.txt').decode()
        old_roots=[json.loads(s.split(' ',1)[1]) for s in stream.splitlines() if s.startswith('C29_ROOT_JSON ')]
        self.assertEqual(old_roots,self.records['C29_ROOT_JSON'])

    def test_full_values_are_preserved_but_not_lossless_expr_or_human_read_claim(self):
        rows=self.records['C29_GENERATED_JSON']
        self.assertGreater(sum(len(row['valuePrettyExplicitAllowOpaque'] or '') for row in rows),9_000_000)
        for row in rows:
            self.assertEqual(row['valueTextScope'],'ACTUAL_META_PPEXPR_NOT_LOSSLESS_EXPR_SERIALIZATION')
            self.assertEqual(row['actualHasValueAllowOpaque'],row['actualKind'] in ('defnInfo','thmInfo','opaqueInfo'))
        self.assertEqual(self.receipt['independent_decoder_review'],'IN_PROGRESS; no result inferred from successful instrumentation')

    def test_no_acceptance_and_all_diagnostic_python_tests_selected_in_ci(self):
        for key in ('sourceAgreement','publicationBinding','axiomPolicyPass'):
            self.assertIsNone(self.receipt[key])
        for key in ('nativeAccepted','main_admission','scientific_ROOT','PURIFIED'):
            self.assertFalse(self.receipt[key])
        workflow=(ROOT/'.github/workflows/cubic-c29-diagnostic.yml').read_text()
        self.assertIn("-p 'test*.py'",workflow)
        self.assertIn('cancel-in-progress: false',workflow)
        self.assertIn('contents: read',workflow)


if __name__=='__main__':
    unittest.main()
