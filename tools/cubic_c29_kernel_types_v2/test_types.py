"""Synthetic type-only stream guards, never a Lean certificate."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
HERE=Path(__file__).resolve().parent
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result
R=module('kernel_type_addon',HERE/'run.py');V=module('kernel_type_validator',HERE/'validate_two_types.py')
FRESH=HERE/'SYNTHETIC_NOT_REAL.olean'
def rows():
    flags=dict(sourceAgreement=None,publicationBinding=None,axiomPolicyPass=None,nativeAccepted=False)
    return [dict(schema='C29_TWO_SIGNATURES_V1',targetModule='QuantumBlockEncoding.CubicStatePreparation',
        freshOleanPathComparisonPassed=True,actualResolvedOleanPath=str(FRESH),expectedNames=V.NAMES,
        ppDeepTerms=True,ppMaxSteps=2000000,maxRecDepth=10000,**flags),
      [dict(ordinal=i,actualName=n,actualKind='thmInfo',kernelRootPresent=True,typePrettyExplicit='True',
         universeParameters=[],axioms=[],isUnsafe=False,selfOccursInAxioms=False,valuesPrinted=False,**flags)
       for i,n in enumerate(V.NAMES,1)],
      dict(schema='C29_TWO_SIGNATURES_V1',completed=2,valuesPrinted=False,scope='TWO_PRETTY_SIGNATURES_ONLY_NOT_AXIOM_POLICY',**flags)]
def stream(data):
    a,b,c=data
    return '\n'.join([V.TAGS[0]+' '+json.dumps(a)]+[V.TAGS[1]+' '+json.dumps(x) for x in b]+[V.TAGS[2]+' '+json.dumps(c)])
class TypeSupplementTests(unittest.TestCase):
    def test_complete_synthetic_fixture_not_proof(self):
        result=R.checked_stream(V,stream(rows()),0,FRESH)
        self.assertFalse(result['nativeAccepted']);self.assertFalse(result['wholeTargetTrustClosed'])
    def test_nonzero_partial_rejected(self):
        with self.assertRaisesRegex(ValueError,'nonzero native exit'):R.checked_stream(V,stream(rows()),1,FRESH)
    def test_missing_type_rejected(self):
        data=rows();data[1].pop()
        with self.assertRaisesRegex(ValueError,'exactly one fresh binding'):R.checked_stream(V,stream(data),0,FRESH)
    def test_omitted_type_rejected(self):
        data=rows();data[1][0]['typePrettyExplicit']='True ⋯'
        with self.assertRaisesRegex(ValueError,'still omitted'):R.checked_stream(V,stream(data),0,FRESH)
    def test_wrong_fresh_path_rejected(self):
        data=rows();data[0]['actualResolvedOleanPath']=str(HERE/'wrong.olean')
        with self.assertRaisesRegex(ValueError,'same fresh artifact'):R.checked_stream(V,stream(data),0,FRESH)
    def test_native_acceptance_rejected(self):
        data=rows();data[1][0]['nativeAccepted']=True
        with self.assertRaisesRegex(ValueError,'native acceptance'):R.checked_stream(V,stream(data),0,FRESH)
    def test_unsafe_signature_rejected(self):
        data=rows();data[1][0]['isUnsafe']=True
        with self.assertRaisesRegex(ValueError,'unsafe or self-axiom'):R.checked_stream(V,stream(data),0,FRESH)
    def test_unrecognized_diagnostic_rejected(self):
        with self.assertRaisesRegex(ValueError,'unknown two-type diagnostic'):R.checked_stream(V,stream(rows())+'\nC29_FAKE_JSON {}',0,FRESH)
if __name__=='__main__':unittest.main()
