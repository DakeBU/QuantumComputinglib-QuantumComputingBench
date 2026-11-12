"""Synthetic Python guard tests only. No Lean execution or signature claim."""
import copy
import json
from pathlib import Path
import unittest
import supplemental_types_v1 as subject


class SupplementalTests(unittest.TestCase):
    def fixture(self):
        no = dict(sourceAgreement=None, publicationBinding=None, axiomPolicyPass=None, nativeAccepted=False)
        binding = dict(schema='C29_TWO_SIGNATURES_V1', targetModule='QuantumBlockEncoding.CubicStatePreparation',
            actualResolvedOleanPath=str(Path('SYNTHETIC_FRESH.olean').resolve()), freshOleanPathComparisonPassed=True,
            expectedNames=subject.NAMES, ppDeepTerms=True, ppMaxSteps=2000000, maxRecDepth=10000, **no)
        types = [dict(ordinal=i, actualName=name, actualKind='thmInfo', kernelRootPresent=True,
            typePrettyExplicit='SYNTHETIC_PARSER_TYPE_NOT_LEAN_EVIDENCE', universeParameters=[],
            axioms=['SYNTHETIC_UNASSESSED_AXIOM'], isUnsafe=False, selfOccursInAxioms=False,
            valuesPrinted=False, **no) for i, name in enumerate(subject.NAMES, 1)]
        summary = dict(schema='C29_TWO_SIGNATURES_V1', completed=2, valuesPrinted=False,
            scope='TWO_PRETTY_SIGNATURES_ONLY_NOT_AXIOM_POLICY', **no)
        return [binding, types, summary]

    def stream(self, f):
        return '\n'.join([subject.TAGS[0]+' '+json.dumps(f[0])] +
            [subject.TAGS[1]+' '+json.dumps(r) for r in f[1]] +
            ([subject.TAGS[2]+' '+json.dumps(f[2])] if f[2] is not None else []))

    def rejected(self, mutate, exit_code=0):
        f=self.fixture(); mutate(f)
        with self.assertRaises((ValueError, KeyError, TypeError)):
            subject.validate_supplement(self.stream(f), exit_code, 'SYNTHETIC_FRESH.olean')

    def test_synthetic_complete_only_tests_parser_not_native(self):
        row=subject.validate_supplement(self.stream(self.fixture()),0,'SYNTHETIC_FRESH.olean')
        self.assertEqual(len(row['signatures']),2)
        self.assertFalse(row['nativeAccepted']);self.assertIsNone(row['axiomPolicyPass'])

    def test_both_unicode_and_ascii_omission_glyphs_rejected(self):
        for glyph in ('⋯','…','...'):
            with self.subTest(glyph=glyph):self.rejected(lambda f:f[1][0].update(typePrettyExplicit='∀ n : '+glyph+', True'))

    def test_nonzero_even_with_complete_stream_rejected(self):self.rejected(lambda f:None,1)
    def test_partial_stream_rejected(self):self.rejected(lambda f:f.__setitem__(2,None))
    def test_missing_signature_rejected(self):self.rejected(lambda f:f[1].pop())
    def test_duplicate_signature_rejected(self):self.rejected(lambda f:f[1].__setitem__(1,copy.deepcopy(f[1][0])))
    def test_extra_signature_rejected(self):self.rejected(lambda f:f[1].append(copy.deepcopy(f[1][0])))
    def test_wrong_exact_name_rejected(self):self.rejected(lambda f:f[1][0].update(actualName='invented'))
    def test_wrong_fresh_path_rejected(self):self.rejected(lambda f:f[0].update(actualResolvedOleanPath='OTHER.olean'))
    def test_failed_lean_fresh_comparison_rejected(self):self.rejected(lambda f:f[0].update(freshOleanPathComparisonPassed=False))
    def test_wrong_kind_or_kernel_presence_rejected(self):
        self.rejected(lambda f:f[1][0].update(actualKind='axiomInfo'))
        self.rejected(lambda f:f[1][0].update(kernelRootPresent=False))
    def test_missing_type_and_bad_axiom_universe_fields_rejected(self):
        for key,value in [('typePrettyExplicit',''),('axioms','bad'),('universeParameters',[3]),('isUnsafe',0),('selfOccursInAxioms',True)]:
            with self.subTest(key=key):self.rejected(lambda f:f[1][0].update({key:value}))
    def test_no_policy_or_acceptance_at_any_record_level(self):
        for i in (0,2):
            for key,value in [('sourceAgreement',True),('publicationBinding','BOUND'),('axiomPolicyPass',True),('nativeAccepted',True),('scientific_ROOT',True)]:
                with self.subTest(i=i,key=key):self.rejected(lambda f:f[i].update({key:value}))
        self.rejected(lambda f:f[1][0].update(authorBinding='BOUND'))
    def test_value_output_scope_rejected(self):
        self.rejected(lambda f:f[1][0].update(valuePrettyExplicitAllowOpaque='NOT_ALLOWED'))
        self.rejected(lambda f:f[2].update(valuesPrinted=True))
    def test_option_and_expected_name_binding_required(self):
        self.rejected(lambda f:f[0].update(ppDeepTerms=False))
        self.rejected(lambda f:f[0].update(ppMaxSteps=5000))
        self.rejected(lambda f:f[0].update(maxRecDepth=1000))
        self.rejected(lambda f:f[0].update(expectedNames=list(reversed(subject.NAMES))))
    def test_missing_terminal_count_rejected(self):self.rejected(lambda f:f[2].update(completed=1))
    def test_malformed_json_rejected(self):
        with self.assertRaises(ValueError):subject.validate_supplement('C29_TWO_TYPE_JSON {',0,'SYNTHETIC_FRESH.olean')


if __name__=='__main__':unittest.main()
