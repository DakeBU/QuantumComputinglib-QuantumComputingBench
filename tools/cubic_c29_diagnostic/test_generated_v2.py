"""Synthetic parser/guard tests only; never native Lean evidence."""
import copy
import json
from pathlib import Path
import unittest

import runner
import test_runner as original_tests


class GeneratedV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = Path(__file__).parent
        cls.module = runner.load_generated_validator(cls.package)
        cls.expected = json.loads((cls.package / 'expected-roots.json').read_text(encoding='utf-8'))
        cls.generated_expected = json.loads((cls.package / 'expected-generated-ci2.json').read_text(encoding='utf-8'))
        original_tests.OriginalStrictValidatorTests.setUpClass()

    def fixture(self):
        base = original_tests.OriginalStrictValidatorTests()
        f = base.fixture()
        f['binding'].update(targetModule='QuantumBlockEncoding.CubicStatePreparation',
                            observedTargetOwnedConstants=769, sourceAgreement=None, nativeAccepted=False)
        rows = []
        for spec in self.generated_expected['generated']:
            name, kind = spec['actualName'], spec['actualKind']
            has_value = kind in ('defnInfo', 'thmInfo', 'opaqueInfo')
            rows.append(dict(actualName=name, actualKind=kind, actualPrivate=False,
                userNameViaActualAPI=name, classification='SYNTHETIC_PARSER_CONTEXT_NOT_LEAN_EVIDENCE',
                structureParents=[], includedIn319ExplicitRootCount=False, kernelRootPresent=True,
                universeParameters=[], typePrettyExplicit='SYNTHETIC_NOT_LEAN_TYPE',
                actualHasValueAllowOpaque=has_value,
                valuePrettyExplicitAllowOpaque='SYNTHETIC_NOT_LEAN_VALUE' if has_value else None,
                valueTextScope='ACTUAL_META_PPEXPR_NOT_LOSSLESS_EXPR_SERIALIZATION',
                isUnsafe=False, opaqueClassification=('GENERATED_ACTUAL_OPAQUE_INFO'
                    if kind == 'opaqueInfo' else 'GENERATED_NOT_OPAQUE_INFO'),
                axioms=[name] if kind == 'axiomInfo' else [],
                selfOccursInAxioms=(kind == 'axiomInfo'),
                typeAxiomAuditScope=self.module.SCOPE, **runner.NO_ACCEPT))
        f['generated'] = rows
        f['summary'].update(generatedTargetOwnedConstants=450, observedTargetOwnedConstants=769,
                            generatedTypeValueAxiomAuditCompleted=450, generatedAuditSchema='C29_GENERATED_AUDIT_V2')
        return f

    def stream(self, f):
        return original_tests.OriginalStrictValidatorTests().stream(f)

    def reject(self, mutation, native_exit=0):
        f = self.fixture(); mutation(f)
        with self.assertRaises((ValueError, KeyError, TypeError)):
            self.module.validate(self.expected, self.stream(f), native_exit)

    def test_complete_synthetic_fields_do_not_grant_policy_or_acceptance(self):
        result = self.module.validate(self.expected, self.stream(self.fixture()), 0)
        self.assertEqual(result['generatedActualFieldsCollected'], 450)
        self.assertEqual(result['explicitRoots'], 319)
        self.assertEqual(result['privateRoots'], 50)
        self.assertFalse(result['wholeTargetTrustClosed'])
        self.assertIsNone(result['axiomPolicyPass'])
        self.assertFalse(result['nativeAccepted'])
        self.assertEqual(result['generatedAxiomInfoCount'], 9)
        self.assertEqual(result['generatedSelfAxiomObserved'], 9)

    def test_generated_exact_set_negative_cases(self):
        for mutation in (
            lambda f: f['generated'].pop(),
            lambda f: f['generated'].append(copy.deepcopy(f['generated'][0])),
            lambda f: f['generated'][0].update(actualName='WRONG_GENERATED_NAME'),
            lambda f: f['generated'][0].update(actualName=f['roots'][0]['actualName']),
            lambda f: f['generated'][0].update(actualKind='inventedKind')):
            with self.subTest(mutation=repr(mutation)):
                self.reject(mutation)

    def test_each_required_field_missing_is_rejected(self):
        for key in ('typePrettyExplicit', 'axioms', 'isUnsafe', 'kernelRootPresent', 'universeParameters',
                    'actualHasValueAllowOpaque', 'valuePrettyExplicitAllowOpaque', 'opaqueClassification',
                    'selfOccursInAxioms', 'sourceAgreement', 'publicationBinding', 'axiomPolicyPass',
                    'nativeAccepted', 'valueTextScope', 'typeAxiomAuditScope', 'structureParents'):
            with self.subTest(key=key):
                self.reject(lambda f: f['generated'][0].pop(key))

    def test_wrong_field_types_and_claims_rejected(self):
        for key, value in [('typePrettyExplicit', ''), ('axioms', 'not-an-array'), ('axioms', [42]),
                           ('axioms', ['x', 'x']), ('universeParameters', [False]), ('isUnsafe', 0),
                           ('kernelRootPresent', False), ('actualPrivate', 'false'),
                           ('actualHasValueAllowOpaque', None), ('selfOccursInAxioms', 'false'),
                           ('opaqueClassification', 'SOURCE_GUESSED'), ('valueTextScope', 'LOSSLESS'),
                           ('includedIn319ExplicitRootCount', True), ('nativeAccepted', True),
                           ('publicationBinding', 'accepted'), ('axiomPolicyPass', True),
                           ('sourceAgreement', True), ('scientific_ROOT', True), ('authorBinding', 'bound')]:
            with self.subTest(key=key, value=value):
                self.reject(lambda f: f['generated'][0].update({key: value}))

    def test_self_axiom_not_whitelisted_or_discarded(self):
        f = self.fixture()
        row = next(r for r in f['generated'] if r['actualKind'] == 'axiomInfo')
        row['axioms'].append('ANY_OBSERVED_UNASSESSED_AXIOM')
        result = self.module.validate(self.expected, self.stream(f), 0)
        self.assertIn('ANY_OBSERVED_UNASSESSED_AXIOM', result['generatedAxiomUnion'])
        self.assertIsNone(result['axiomPolicyPass'])
        row['selfOccursInAxioms'] = False
        with self.assertRaises(ValueError):
            self.module.validate(self.expected, self.stream(f), 0)

    def test_value_kind_consistency(self):
        for has_value in (True, False):
            f = self.fixture()
            row = next(r for r in f['generated'] if r['actualHasValueAllowOpaque'] == has_value)
            row['valuePrettyExplicitAllowOpaque'] = None if has_value else 'FABRICATED'
            with self.assertRaises(ValueError):
                self.module.validate(self.expected, self.stream(f), 0)

    def test_fixture_count_field_cannot_override_cubic_root_partition(self):
        self.reject(lambda f: f['generated'][0].update(includedIn319ExplicitRootCount=True,
                                                      includedIn5ExplicitRootCount=False))

    def test_generated_completion_and_legacy_metadata_rejected(self):
        self.reject(lambda f: f['summary'].update(generatedTypeValueAxiomAuditCompleted=449))
        self.reject(lambda f: f['summary'].pop('generatedAuditSchema'))
        self.reject(lambda f: f['generated'][0].update(
            typeAxiomAuditScope='NOT_REQUESTED_FOR_GENERATED_RESIDUAL_METADATA_ONLY'))

    def test_nonzero_and_partial_output_rejected(self):
        self.reject(lambda f: None, 1)
        self.reject(lambda f: f.update(summary=None))

    def test_generated_input_source_and_toolchain_drift_rejected(self):
        for key, value in [('targetRawSHA256', '0'*64), ('leanVersion', '4.29.1')]:
            expected = copy.deepcopy(self.generated_expected); expected[key] = value
            with self.assertRaises(ValueError):
                self.module.validate(self.expected, self.stream(self.fixture()), 0, expected)

    def test_no_acceptance_claims_in_binding_or_explicit_extensions(self):
        self.reject(lambda f: f['binding'].update(nativeAccepted=True))
        self.reject(lambda f: f['binding'].update(publicationBinding='BOUND'))
        self.reject(lambda f: f['roots'][0].update(authorBinding='BOUND'))
        self.reject(lambda f: f['roots'][0].update(scientific_ROOT=True))

    def test_driver_explicit_root_loop_preserved_exactly(self):
        for old, new in [('Probe-v4.lean', 'Probe-v5.lean'), ('FixtureProbe-v5.lean', 'FixtureProbe-v6.lean')]:
            a = (self.package / old).read_text(encoding='utf-8')
            b = (self.package / new).read_text(encoding='utf-8')
            select = lambda s: s.split('    let mut ordinal := 0', 1)[1].split('    let mut generatedCount := 0', 1)[0]
            self.assertEqual(select(a), select(b))
            self.assertEqual(a.split('def expectedRoots',1)[1].split('def constantKind',1)[0],
                             b.split('def expectedRoots',1)[1].split('def constantKind',1)[0])

    def test_active_versioned_validator_pin_required(self):
        self.assertEqual(runner.load_validator(self.package, versioned=True).__name__, 'validate')
        self.assertEqual(len(self.generated_expected['fixtureGenerated']), 15)

    def test_shared_fixture_generated_field_schema_uses_actual_driver_key(self):
        source = (self.package / 'FixtureProbe-v6.lean').read_text(encoding='utf-8')
        self.assertIn('("includedIn319ExplicitRootCount", .bool false)', source)
        rows = []
        for spec in self.generated_expected['fixtureGenerated']:
            row = copy.deepcopy(self.fixture()['generated'][0])
            row.update(actualName=spec['actualName'], actualKind=spec['actualKind'],
                       actualHasValueAllowOpaque=spec['actualKind'] in ('defnInfo','thmInfo','opaqueInfo'))
            row.update(axioms=[], selfOccursInAxioms=False,
                       valuePrettyExplicitAllowOpaque='SYNTHETIC_FIXTURE_VALUE' if row['actualHasValueAllowOpaque'] else None,
                       opaqueClassification='GENERATED_ACTUAL_OPAQUE_INFO' if row['actualKind']=='opaqueInfo' else 'GENERATED_NOT_OPAQUE_INFO')
            rows.append(row)
        summary=dict(generatedAuditSchema='C29_GENERATED_AUDIT_V2',generatedTypeValueAxiomAuditCompleted=15,
                     sourceAgreement=None,publicationBinding=None,axiomPolicyPass=None,nativeAccepted=False)
        checked=self.module.validate_generated(rows,self.generated_expected['fixtureGenerated'],[],summary)
        self.assertEqual(checked['generatedActualFieldsCollected'],15)


if __name__ == '__main__':
    unittest.main()
