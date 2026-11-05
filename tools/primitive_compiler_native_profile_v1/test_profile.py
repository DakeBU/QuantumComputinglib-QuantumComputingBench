"""Real Python tests; every observation fixture is SYNTHETIC, never Lean evidence."""
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

import runner
import validator

PACKAGE = Path(__file__).parent
PROFILE = json.loads((PACKAGE / 'profile.json').read_text(encoding='utf-8'))
PROJECT = Path(os.environ.get('C31_TEST_PROJECT', Path.cwd()))


def obs(module, name, kind='defnInfo', private=False, user=None):
    available = kind in ('defnInfo', 'thmInfo', 'opaqueInfo')
    return dict(module=module, actualName=name, userNameViaActualAPI=user or name,
        actualPrivate=private, actualKind=kind, kernelRootPresent=True, kernelKind=kind,
        kernelTypeAndUniversesAgree=True, universeParameters=[], typePrettyExplicit='SYNTHETIC_NOT_LEAN_TYPE',
        isUnsafe=False, actualHasValueAllowOpaque=available, valueTextRequested=False,
        valuePrettyExplicitAllowOpaque=None,
        valueObservation='NOT_REQUESTED_VALUE_AVAILABLE' if available else 'NOT_REQUESTED_NO_VALUE_AVAILABLE',
        actualOpaqueInfo=kind == 'opaqueInfo', actualAxiomInfo=kind == 'axiomInfo', sourceOpaque=False,
        axioms=[name] if kind == 'axiomInfo' else [], selfOccursInAxioms=kind == 'axiomInfo',
        axiomCollection='ACTUAL_LEAN_COLLECT_AXIOMS_IMPORTED_EXTENSION_AND_LOCAL_BODIES',
        typeTextScope='ACTUAL_META_PPEXPR_NOT_LOSSLESS_EXPR_SERIALIZATION', **validator.NO_ACCEPT)


def fixture():
    bindings, roots, generated = [], [], []
    paths = {}
    for module in PROFILE['modules']:
        target = module['module']; local = []; extras = []; structures = []
        specs = [r for r in PROFILE['roots'] if r['module'] == target]
        for i, spec in enumerate(specs, 1):
            actual = ('_private.SYNTHETIC.' + str(i) + '.' + spec['sourceUserName']
                      if spec['sourcePrivate'] else spec['sourceUserName'])
            kind = next(iter(validator.SOURCE_KINDS[spec['sourceKind']]))
            row = obs(target, actual, kind, spec['sourcePrivate'], spec['sourceUserName'])
            row.update(moduleOrdinal=i, **{k: spec[k] for k in ('sourceUserName', 'sourcePrivate', 'sourceKind')})
            local.append(row)
            if spec['sourceKind'] == 'structure':
                fields = []
                for ordinal, name in enumerate(spec['structureFields']):
                    projection = 'SYNTHETIC.field.' + str(ordinal)
                    extra = obs(target, projection)
                    extra['includedInExplicitRootCount'] = False; extras.append(extra)
                    fields.append(dict(fieldName=name, projection=projection, actualKind='defnInfo'))
                ctor = 'SYNTHETIC.constructor'
                extra = obs(target, ctor, 'ctorInfo')
                extra['includedInExplicitRootCount'] = False; extras.append(extra)
                structures.append(dict(actualName=actual, constructors=[ctor],
                                       fieldNames=list(spec['structureFields']), fields=fields))
        # Unknown generated identity set is deliberately allowed, while partition completeness is mandatory.
        for kind in ('axiomInfo', 'opaqueInfo'):
            name = 'SYNTHETIC.' + target + '.' + kind
            extra = obs(target, name, kind)
            extra['includedInExplicitRootCount'] = False; extras.append(extra)
        owned = [r['actualName'] for r in local + extras]
        paths[target] = '$SYNTHETIC_COHORT/' + target + '.olean'
        bindings.append(dict(module=target, profileSHA256='SYNTHETIC_SHA', cohortID='SYNTHETIC_COHORT',
            resolvedOleanPath=paths[target], freshOleanPathComparisonPassed=True,
            ownershipMethod='ENVIRONMENT_MODULE_INDEX_NOT_NAME_PREFIX', ownedNames=owned,
            ownedCount=len(owned), expectedRoots=len(local), structures=structures,
            ppDeepTerms=True, ppMaxSteps=2000000, maxRecDepth=10000, **validator.NO_ACCEPT))
        roots += local; generated += extras
    summary = dict(status='FORMAL_DIAGNOSTIC_COMPLETE_NOT_ACCEPTANCE', profileSHA256='SYNTHETIC_SHA',
        cohortID='SYNTHETIC_COHORT', modulesCompleted=3, rootsCompleted=87, privateCompleted=8,
        generatedCompleted=len(generated), ownedCompleted=len(roots) + len(generated),
        allNamesResolvedUniquely=True, **validator.NO_ACCEPT)
    return dict(bindings=bindings, roots=roots, generated=generated, summary=summary, paths=paths)


def stream(data):
    lines = []
    for group, tag in [('bindings', 'C31_BINDING_JSON'), ('roots', 'C31_ROOT_JSON'),
                       ('generated', 'C31_GENERATED_JSON')]:
        lines += [tag + ' ' + json.dumps(r) for r in data[group]]
    if data['summary'] is not None:
        lines.append('C31_SUMMARY_JSON ' + json.dumps(data['summary']))
    return '\n'.join(lines)


def validate(data, exit_code=0, timeout=False):
    return validator.validate(PROFILE, stream(data), exit_code, timed_out=timeout,
        profile_sha='SYNTHETIC_SHA', cohort_id='SYNTHETIC_COHORT', expected_oleans=data['paths'])


class StreamTests(unittest.TestCase):
    def reject(self, mutation, exit_code=0, timeout=False):
        data = fixture(); mutation(data)
        with self.assertRaises((ValueError, KeyError, TypeError)):
            validate(data, exit_code, timeout)

    def test_complete_synthetic_not_acceptance(self):
        result = validate(fixture())
        self.assertEqual(result['roots'], 87); self.assertEqual(result['private'], 8)
        self.assertFalse(result['nativeAccepted']); self.assertIsNone(result['axiomPolicyPass'])

    def test_unknown_generated_identity_can_change_but_must_be_fully_partitioned(self):
        data = fixture(); row = data['generated'][-1]; old = row['actualName']
        new = 'SYNTHETIC_NEW_UNPREDICTED_GENERATED_NAME'
        row['actualName'] = row['userNameViaActualAPI'] = new
        binding = next(b for b in data['bindings'] if b['module'] == row['module'])
        binding['ownedNames'][binding['ownedNames'].index(old)] = new
        self.assertGreater(validate(data)['generated'], 0)

    def test_nonzero_missing_and_timedout_exit_fail_even_with_complete_output(self):
        for exit_code, timeout in [(1, False), (-9, False), (None, False), (True, False), (0, True)]:
            self.reject(lambda f: None, exit_code, timeout)

    def test_zero_exit_partial_empty_duplicate_and_colliding_records_fail(self):
        for mutation in (
            lambda f: f['roots'].pop(), lambda f: f['generated'].pop(),
            lambda f: f['bindings'].pop(), lambda f: f.update(summary=None),
            lambda f: f['roots'].append(copy.deepcopy(f['roots'][0])),
            lambda f: f['generated'].append(copy.deepcopy(f['generated'][0])),
            lambda f: f['generated'][0].update(actualName=f['roots'][0]['actualName']),
            lambda f: f['bindings'][0].update(ownedNames=[], ownedCount=0)):
            self.reject(mutation)

    def test_every_actual_observation_field_required_on_explicit_and_generated(self):
        for family in ('roots', 'generated'):
            for key in obs('SYNTHETIC_MODULE', 'SYNTHETIC_NAME'):
                with self.subTest(family=family, key=key):
                    self.reject(lambda f: f[family][0].pop(key))

    def test_kind_kernel_universe_value_and_axiom_corruption(self):
        for key, value in [('actualKind', 'invented'), ('kernelRootPresent', False),
                           ('kernelKind', 'axiomInfo'), ('kernelTypeAndUniversesAgree', False),
                           ('universeParameters', ['u', 'u']), ('universeParameters', [False]),
                           ('axioms', 'not-an-array'), ('axioms', ['a', 'a']),
                           ('selfOccursInAxioms', True), ('actualOpaqueInfo', True),
                           ('actualPrivate', 0), ('isUnsafe', 0), ('valueTextRequested', True),
                           ('actualHasValueAllowOpaque', False),
                           ('valuePrettyExplicitAllowOpaque', 'FABRICATED'), ('typePrettyExplicit', ''),
                           ('typePrettyExplicit', 'forall x, ⋯'), ('typePrettyExplicit', 'forall x, …')]:
            self.reject(lambda f: f['generated'][0].update({key: value}))

    def test_no_whitelist_unknown_axioms_preserved_not_approved(self):
        data = fixture(); row = next(r for r in data['generated'] if r['actualKind'] == 'axiomInfo')
        row['axioms'].append('SYNTHETIC_UNASSESSED_AXIOM')
        result = validate(data)
        self.assertIn('SYNTHETIC_UNASSESSED_AXIOM', result['observedAxiomUnion'])
        self.assertIsNone(result['axiomPolicyPass'])
        self.assertIsNone(row['valuePrettyExplicitAllowOpaque'])

    def test_binding_profile_cohort_private_source_order_and_pp_drift(self):
        for mutation in (
            lambda f: f['bindings'][0].update(profileSHA256='wrong'),
            lambda f: f['bindings'][0].update(cohortID='wrong'),
            lambda f: f['bindings'][0].update(resolvedOleanPath='wrong'),
            lambda f: f['bindings'][0].update(freshOleanPathComparisonPassed=False),
            lambda f: f['bindings'][0].update(ownershipMethod='NAME_PREFIX_GUESS'),
            lambda f: f['bindings'][0].update(ppDeepTerms=False),
            lambda f: f['bindings'][0].update(ppMaxSteps=0),
            lambda f: f['bindings'][0].update(maxRecDepth=0),
            lambda f: f['roots'].reverse(),
            lambda f: f['roots'][0].update(sourceUserName='wrong'),
            lambda f: next(r for r in f['roots'] if r['sourcePrivate']).update(actualPrivate=False),
            lambda f: f['generated'][0].update(includedInExplicitRootCount=True),
            lambda f: f['summary'].update(ownedCompleted=0)):
            self.reject(mutation)

    def test_structure_field_and_constructor_completeness(self):
        for mutation in (
            lambda f: f['bindings'][0].update(structures=[]),
            lambda f: f['bindings'][0]['structures'][0]['fields'].pop(),
            lambda f: f['bindings'][0]['structures'][0]['fieldNames'].reverse(),
            lambda f: f['bindings'][0]['structures'][0]['fields'][0].update(projection='MISSING'),
            lambda f: f['bindings'][0]['structures'][0].update(constructors=['MISSING'])):
            self.reject(mutation)

    def test_forbidden_claims_rejected_in_every_record_family(self):
        for family in ('bindings', 'roots', 'generated', 'summary'):
            for key, value in [('nativeAccepted', True), ('sourceAgreement', True),
                               ('axiomPolicyPass', True), ('publicationBinding', 'BOUND'),
                               ('scientificAcceptance', True), ('trustClosure', True),
                               ('scientific_ROOT', True), ('authorBinding', 'BOUND')]:
                def mutate(f):
                    (f[family] if family == 'summary' else f[family][0])[key] = value
                self.reject(mutate)

    def test_malformed_unexpected_and_postterminal_output(self):
        for text in ('', 'C31_ROOT_JSON {', stream(fixture()) + '\nC31_ROOT_JSON {}',
                     'C31_ROOT_JSON {"actualName":"a","actualName":"b"}',
                     'warning: partial output\n' + stream(fixture())):
            with self.assertRaises(ValueError):
                validator.validate(PROFILE, text, 0, timed_out=False, profile_sha='SYNTHETIC_SHA',
                    cohort_id='SYNTHETIC_COHORT', expected_oleans=fixture()['paths'])

    def test_native_axiom_info_cannot_have_a_fabricated_body_or_omit_self(self):
        for changes in (dict(actualHasValueAllowOpaque=True),
                        dict(axioms=[], selfOccursInAxioms=False),
                        dict(valuePrettyExplicitAllowOpaque='GUESSED_NATIVE_BODY')):
            data = fixture()
            next(r for r in data['generated'] if r['actualKind'] == 'axiomInfo').update(changes)
            with self.assertRaises(ValueError): validate(data)

    def test_profile_zeros_duplicates_wrong_private_or_root_count_fail(self):
        for mutate in (lambda p: p['roots'].pop(), lambda p: p.update(modules=[]),
                       lambda p: p['roots'].__setitem__(1, copy.deepcopy(p['roots'][0])),
                       lambda p: p['modules'][0].update(rawSHA256='x'),
                       lambda p: p.update(ppMaxSteps=0)):
            profile = copy.deepcopy(PROFILE); mutate(profile)
            with self.assertRaises(ValueError): validator.validate_profile(profile)


class PythonRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = runner.load_shared(PROJECT, PROFILE)

    def test_reused_safe_paths_sha_os_inventory_and_redaction(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('../outside', '/absolute', r'C:\outside', 'a//b'):
                with self.assertRaises(ValueError): self.api.safe_child(root, name)
            (root / 'a.olean').write_bytes(b'SYNTHETIC_PROVIDER')
            self.assertEqual(len(self.api.inventory_providers([root], root / 'excluded')), 1)
            with self.assertRaises(ValueError): self.api.verify_pins(root, {'a.olean': '0' * 64})
            value = self.api.redact(str(root) + '/file TOKEN=secret', {str(root): '$SYNTHETIC'})
            self.assertNotIn(str(root), value); self.assertNotIn('TOKEN=secret', value)

    def test_actual_python_child_nonzero_and_timeout_never_success(self):
        for label, source, timeout in [('python-nonzero', 'raise SystemExit(7)', 10),
                                       ('python-timeout', 'import time; time.sleep(5)', .05)]:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                with self.assertRaises(self.api.NativeFailure) as caught:
                    self.api.native_call(root, label, [sys.executable, '-c', source],
                                         root, dict(os.environ), timeout=timeout)
                self.assertIsInstance(caught.exception.result['PID'], int)
                self.assertNotEqual(caught.exception.result['exitCode'], 0)

    def test_provider_target_inheritance_and_duplicate_collisions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); fresh = root / 'fresh'; fresh.mkdir()
            bad = copy.deepcopy(PROFILE); bad['providers'] = [bad['modules'][0]['module']]
            with self.assertRaises(ValueError): runner.copy_providers(root, fresh, bad, self.api)
            good = copy.deepcopy(PROFILE); good['providers'] = ['Synthetic.Provider', 'Synthetic.Provider']
            source = root / '.lake/build/lib/lean/Synthetic/Provider.olean'
            source.parent.mkdir(parents=True); source.write_bytes(b'SYNTHETIC_PROVIDER')
            with self.assertRaises(FileExistsError): runner.copy_providers(root, fresh, good, self.api)

    def test_actual_87_driver_vector_has_deep_terms_and_bounded_limits(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); runner.render_driver(PROFILE, self.api, root)
            source = (root / 'Profile.lean').read_text()
            self.assertEqual(source.count('targetModule :='), 87)
            self.assertEqual(source.count('privateRoot := true'), 8)
            probe = (root / 'Probe.lean').read_text()
            self.assertIn('pp.deepTerms true', probe)
            self.assertIn('pp.maxSteps 2000000', probe)
            self.assertIn('maxRecDepth 10000', probe)

    def test_exclusive_output_and_shared_code_pin(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / runner.OUT_REL).mkdir(parents=True)
            # Test exclusive path rule directly without invoking Lean.
            with self.assertRaises(FileExistsError):
                self.api.safe_child(root, runner.OUT_REL).mkdir(parents=True, exist_ok=False)
        bad = copy.deepcopy(PROFILE); bad['sharedInstrumentation']['sha256'] = '0' * 64
        with self.assertRaises(ValueError): runner.load_shared(PROJECT, bad)


if __name__ == '__main__':
    unittest.main()
