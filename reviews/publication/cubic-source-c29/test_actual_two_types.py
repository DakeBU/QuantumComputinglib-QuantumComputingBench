"""Actual two-type observations and independent reading, never scientific acceptance."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
import zipfile
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())

class ActualTwoTypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt=load(ROOT/'reports/lean-433-migration/c29-actual-two-signatures-runtime.json')
        with zipfile.ZipFile(ROOT/cls.receipt['archive']) as z:cls.files={n:z.read(n) for n in z.namelist()}
        cls.transport=load(ROOT/'reports/lean-433-migration/c29-two-types-independent-transport.json')
        with zipfile.ZipFile(ROOT/cls.transport['bundle']) as z:cls.reading={n:z.read(n) for n in z.namelist()}
        cls.stream=cls.files['06-probe-v5.stdout.raw.sanitized.txt'].decode()
        cls.two_stream=cls.files['07-supplemental-two-types-v1.stdout.raw.sanitized.txt'].decode()
        cls.two=[json.loads(s.split(' ',1)[1]) for s in cls.two_stream.splitlines() if s.startswith('C29_TWO_TYPE_JSON ')]

    def test_exact_actual_archive_and45_members(self):
        self.assertEqual(sha((ROOT/self.receipt['archive']).read_bytes()),self.receipt['archive_sha256'])
        self.assertEqual(len(self.files),45)
        for row in self.receipt['files']:
            self.assertEqual(sha(self.files[row['path']]),row['sha256'])
            self.assertEqual(len(self.files[row['path']]),row['bytes'])

    def test_actual_five_native_calls_and_same_fresh_olean(self):
        self.assertEqual(len(self.receipt['actual_calls']),5)
        for call in self.receipt['actual_calls']:
            self.assertGreater(call['PID'],0);self.assertEqual(call['exitCode'],0);self.assertFalse(call['timedOut'])
            observed=json.loads(self.files[call['label']+'.result.json'])
            self.assertEqual(observed,{k:v for k,v in call.items() if k!='label'})
        self.assertEqual(self.receipt['actual_calls'][-1]['PID'],9887)
        inp=json.loads(self.files['supplemental-two-types-input.json'])
        self.assertEqual(inp['targetFreshOleanSHA256'],self.receipt['fresh_target_olean_sha256'])
        self.assertEqual(self.receipt['fresh_target_olean_sha256'],'bf072be3d4df8ed32049b7f67db6e0223ebb7f48dd84035715683b983f18cf45')

    def test_actual_original319plus450_and_supplement_validators(self):
        package=ROOT/'tools/cubic_c29_diagnostic'
        def module(name):
            spec=importlib.util.spec_from_file_location('actual_'+name.replace('-','_'),package/name)
            result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result
        result=module('validate-output-v2.py').validate(load(package/'expected-roots.json'),self.stream,0)
        self.assertEqual((result['explicitRoots'],result['generatedActualFieldsCollected']),(319,450))
        expected=next(r['path'] for r in json.loads(self.files['target-output.json'])['artifacts'] if r['path'].endswith('.olean'))
        two=module('supplemental_types_v1.py').validate_supplement(self.two_stream,0,expected)
        self.assertEqual(len(two['signatures']),2);self.assertFalse(two['nativeAccepted'])

    def test_only_two_type_texts_replace_real_old_holes_with_same_observed_fields(self):
        generated={r['actualName']:r for r in (json.loads(s.split(' ',1)[1]) for s in self.stream.splitlines() if s.startswith('C29_GENERATED_JSON '))}
        self.assertEqual(len(self.two),2)
        for i,row in enumerate(self.two):
            old=generated[row['actualName']]
            self.assertIn('⋯',old['typePrettyExplicit'])
            self.assertFalse(any(g in row['typePrettyExplicit'] for g in ('⋯','…','...')))
            self.assertEqual(len(row['typePrettyExplicit']),self.receipt['observed_two_type_characters'][i])
            self.assertEqual(sha(row['typePrettyExplicit'].encode()),self.receipt['observed_two_type_sha256'][i])
            for k in ('actualName','actualKind','universeParameters','isUnsafe','axioms','selfOccursInAxioms','kernelRootPresent'):
                self.assertEqual(row[k],old[k])

    def test_exact_independent_bundle_members_and_packet_identity(self):
        self.assertEqual(sha((ROOT/self.transport['bundle']).read_bytes()),self.transport['bundle_sha256'])
        self.assertEqual(len(self.reading),11)
        for row in self.transport['members']:
            self.assertEqual(sha(self.reading[row['member']]),row['sha256'])
        self.assertEqual(sha(self.reading['packet.json']),self.transport['original_packet_sha256'])
        self.assertEqual(sha(self.reading['publicsafe-allowlist.json']),self.transport['inner_allowlist_sha256'])

    def test_independent_math_is_eight_coordinate_Rat_normalization_not_new_cost_claim(self):
        reading=json.loads(self.reading['mathematical-reading.json'])
        self.assertEqual(reading['linear']['vector'],['J/N','a/N','b/N','c/N','d/N','0','0','0'])
        self.assertEqual(reading['cubic']['vector'],['J^3/N^3','a/N^3','b/N^3','c/N^3','d/N^3','0','0','0'])
        self.assertFalse(reading['kernelExprLosslessSerialization']);self.assertFalse(reading['proofBodyPrinted'])

    def test_native_value_and_source_residuals_not_accepted(self):
        residual=json.loads(self.reading['residual-boundaries.json'])
        self.assertEqual(residual['ordinaryValuePrettyOmissionRows'],96)
        self.assertEqual(residual['nativeTrust']['compilerGeneratedAxiomCount'],9)
        self.assertFalse(residual['allOrdinaryValueTokensCognitivelyRead'])
        for row in (self.receipt,self.transport,json.loads(self.reading['packet.json'])):
            self.assertIsNone(row['sourceAgreement']);self.assertIsNone(row['axiomPolicyPass'])
            self.assertFalse(row['nativeAccepted']);self.assertFalse(row['scientific_ROOT'])

if __name__=='__main__':unittest.main()
