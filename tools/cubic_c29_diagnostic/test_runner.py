"""Python-only implementation tests. Synthetic streams are NEVER Lean evidence."""
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

import runner


class FilesystemAndNativeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def providers(self):
        directory = self.root / '.lake/build/lib/lean/QuantumBlockEncoding'
        directory.mkdir(parents=True)
        for name in runner.MODULES:
            (directory / (name + '.olean')).write_bytes(('PYTHON_FIXTURE_ONLY_' + name).encode())
        return directory

    def test_expected_hash_accept_and_reject(self):
        path = self.root / 'input.txt'; path.write_bytes(b'fixture input')
        self.assertEqual(runner.verify_pins(self.root, {'input.txt': runner.sha(path)})[0]['bytes'], 13)
        with self.assertRaisesRegex(ValueError, 'RESEAL'):
            runner.verify_pins(self.root, {'input.txt': '0' * 64})

    def test_actual_lean_help_version_and_flags_are_required(self):
        valid = 'Lean (version 4.33.0, platform, commit fixture) --threads --memory --print-prefix'
        runner.verify_lean_help(valid)
        for bad in (valid.replace('4.33.0', '4.29.1'), valid.replace('--memory', '')):
            with self.assertRaises(ValueError):
                runner.verify_lean_help(bad)

    def test_fresh_provider_copy_and_sidecar_pins(self):
        source = self.providers()
        for suffix in ('.olean.private', '.olean.server', '.ir'):
            (source / ('Core' + suffix)).write_bytes(('FIXTURE' + suffix).encode())
        fresh = self.root / 'fresh'; fresh.mkdir()
        rows = runner.copy_local_providers(self.root, fresh)
        self.assertEqual(len(rows), 8)
        for row in rows:
            self.assertEqual(runner.sha(Path(row['source'])), row['sha256'])
            self.assertEqual(runner.sha(Path(row['destination'])), row['sha256'])

    def test_missing_provider_rejected(self):
        directory = self.providers(); (directory / 'Circuit.olean').unlink()
        fresh = self.root / 'fresh'; fresh.mkdir()
        with self.assertRaisesRegex(FileNotFoundError, 'missing inherited provider'):
            runner.copy_local_providers(self.root, fresh)

    def test_nonexclusive_provider_destination_rejected(self):
        self.providers()
        fresh = self.root / 'fresh'; fresh.mkdir()
        (fresh / 'QuantumBlockEncoding').mkdir()
        with self.assertRaises(FileExistsError):
            runner.copy_local_providers(self.root, fresh)

    def test_path_escape_rejected(self):
        for relative in ('../outside', '/tmp/outside', r'C:\outside', 'fresh/../../outside', r'..\outside', 'a//b'):
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                runner.safe_child(self.root, relative)

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as external:
            try:
                (self.root / 'link').symlink_to(external, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest('host does not permit test symlinks')
            with self.assertRaises(ValueError):
                runner.safe_child(self.root, 'link/file.txt')

    def test_actual_python_nonzero_preserves_partial_stream(self):
        private = self.root / 'private'; private.mkdir()
        with self.assertRaises(runner.NativeFailure) as raised:
            runner.native_call(private, 'fixture-python-failure', [sys.executable, '-c',
                "print('FIXTURE_PARTIAL_NOT_LEAN_EVIDENCE', flush=True); raise SystemExit(7)"],
                self.root, dict(os.environ), timeout=10)
        self.assertEqual(raised.exception.result['exitCode'], 7)
        self.assertIsInstance(raised.exception.result['PID'], int)
        self.assertIn(b'FIXTURE_PARTIAL_NOT_LEAN_EVIDENCE', (private / 'fixture-python-failure.stdout.raw').read_bytes())
        self.assertEqual(json.loads((private / 'fixture-python-failure.result.json').read_text())['exitCode'], 7)

    def test_actual_python_timeout_is_failure(self):
        private = self.root / 'private'; private.mkdir()
        with self.assertRaises(runner.NativeFailure) as raised:
            runner.native_call(private, 'fixture-python-timeout', [sys.executable, '-c',
                'import time; time.sleep(5)'], self.root, dict(os.environ), timeout=0.05)
        self.assertTrue(raised.exception.result['timedOut'])
        self.assertNotEqual(raised.exception.result['exitCode'], 0)

    def test_native_label_escape_rejected(self):
        with self.assertRaises(ValueError):
            runner.native_call(self.root, '../escape', [sys.executable], self.root, dict(os.environ))

    def test_redaction_of_roots_unknown_paths_and_credentials(self):
        text = '/home/runner/work/project/file /private/unmapped/file C:\\Users\\Alice\\x '
        text += 'Bearer secretvalue ghp_abcdef TOKEN=credential https://user:pass@example.test/path'
        result = runner.redact(text, {'/home/runner/work/project': '$PROJECT'})
        self.assertIn('$PROJECT/file', result)
        for secret in ('/home/runner', '/private/unmapped', 'Alice', 'secretvalue', 'ghp_', 'credential', 'user:pass'):
            self.assertNotIn(secret, result)
        self.assertIsNone(runner.ABSOLUTE.search(result))

    def test_public_derivation_has_raw_hash_without_private_bytes(self):
        private = self.root / 'private'; private.mkdir()
        public = self.root / 'public'; public.mkdir()
        raw = private / 'fixture.stdout.raw'; raw.write_text(str(self.root) + '/source TOKEN=secret', encoding='utf-8')
        runner.write_json(private / 'result.json', dict(path=str(self.root), **runner.NO_ACCEPT))
        runner.export_public(private, public, {str(self.root): '$PROJECT'})
        receipt = json.loads((public / 'raw-derivation-receipts.json').read_text())
        row = next(r for r in receipt['files'] if r['publicRelativePath'].startswith('fixture'))
        self.assertEqual(row['rawSHA256'], runner.sha(raw))
        for p in public.iterdir():
            self.assertNotIn(str(self.root), p.read_text())
            self.assertNotIn('TOKEN=secret', p.read_text())
        self.assertFalse((public / raw.name).exists())

    def test_inventory_includes_only_provider_types_and_excludes_output(self):
        providers = self.root / 'providers'; providers.mkdir()
        for name in ('a.olean', 'a.olean.private', 'a.olean.server', 'a.ir', 'libx.so', 'libx.so.1', 'x.dll', 'x.a'):
            (providers / name).write_bytes(b'PROVIDER_FIXTURE')
        (providers / 'secret.txt').write_text('not inventoried')
        excluded = providers / 'out'; excluded.mkdir(); (excluded / 'never.olean').write_bytes(b'EXCLUDED')
        rows = runner.inventory_providers([providers], excluded)
        self.assertEqual(len(rows), 8)
        self.assertFalse(any('secret' in row['path'] or 'never' in row['path'] for row in rows))

    def test_absent_optional_search_root_is_explicit_not_a_missing_module(self):
        present = self.root / 'existing'; present.mkdir()
        absent = self.root / 'not-built-optional-package'
        actual, missing = runner.partition_search_roots([present, absent])
        self.assertEqual(actual, [present.resolve()])
        self.assertEqual(missing, [absent.resolve()])
        self.assertFalse(absent.exists())

    def test_nondirectory_search_root_is_rejected(self):
        file = self.root / 'not-a-search-directory'; file.write_bytes(b'fixture')
        with self.assertRaisesRegex(ValueError, 'not a directory'):
            runner.partition_search_roots([file])

    def test_exclusive_output_is_not_overwritten(self):
        output = self.root / runner.OUT_REL; output.mkdir(parents=True)
        marker = output / 'keep'; marker.write_text('keep')
        with self.assertRaises(FileExistsError):
            runner.run(self.root, Path(__file__).parent)
        self.assertEqual(marker.read_text(), 'keep')


class DriverImportTargetTests(unittest.TestCase):
    def setUp(self):
        self.package = Path(__file__).parent
        self.pins = json.loads((self.package / 'pins.json').read_text(encoding='utf-8'))

    def test_actual_v4_wrong_fixture_import_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'import-target mismatch'):
            runner.verify_driver_import_target(self.package / 'FixtureProbe-v4.lean', 'Fixture')

    def test_v5_import_and_runtime_target_are_actual_fixture(self):
        observed = runner.verify_driver_import_target(self.package / 'FixtureProbe-v5.lean', 'Fixture')
        self.assertEqual(observed['firstImport'], 'Fixture')
        self.assertEqual(observed['runtimeTarget'], 'Fixture')
        old = (self.package / 'FixtureProbe-v4.lean').read_bytes()
        new = (self.package / 'FixtureProbe-v5.lean').read_bytes()
        self.assertEqual(old.split(b'\n', 1)[1], new.split(b'\n', 1)[1])

    def test_cubic_v4_keeps_its_own_target_import(self):
        observed = runner.verify_driver_import_target(self.package / 'Probe-v4.lean',
                                                       'QuantumBlockEncoding.CubicStatePreparation')
        self.assertEqual(observed['driverSHA256'],
                         '396452a5704adbe78941eba817257fc07d3f5294771d8fdb4ce0fd282f59411c')

    def test_runtime_target_drift_rejected_even_with_correct_import(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'Probe.lean'
            source = (self.package / 'FixtureProbe-v5.lean').read_text(encoding='utf-8')
            source = source.replace('let target := `Fixture', 'let target := `Other', 1)
            path.write_text(source, encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'runtime target mismatch'):
                runner.verify_driver_import_target(path, 'Fixture')

    def test_active_fixture_driver_key_and_pin_required(self):
        self.assertEqual(runner.verify_active_drivers(self.package, self.pins)['activeFixtureProbe']['runtimeTarget'],
                         'Fixture')
        for mutate in (lambda p: p.pop('activeFixtureProbe'),
                       lambda p: p.update(activeFixtureProbe='unpinned.lean'),
                       lambda p: p.update(activeFixtureProbe='FixtureProbe-v4.lean')):
            pins = copy.deepcopy(self.pins); mutate(pins)
            with self.assertRaises(ValueError):
                runner.verify_active_drivers(self.package, pins)


class OriginalStrictValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        package = Path(__file__).parent
        cls.validator = staticmethod(runner.load_validator(package))
        cls.expected = json.loads((package / 'expected-roots.json').read_text(encoding='utf-8'))

    def fixture(self):
        # Entirely synthetic in-memory parser fixture. It is not written as a run artifact.
        roots = []
        for i, spec in enumerate(self.expected['roots'], 1):
            roots.append(dict(ordinal=i, sourceUserName=spec['sourceUserName'],
                sourcePrivate=spec['sourcePrivate'], sourceKind=spec['sourceKind'],
                actualName='PARSER_FIXTURE_ONLY_' + str(i), actualPrivate=spec['sourcePrivate'],
                actualKind='axiomInfo' if spec['sourceKind'] == 'opaque' else 'defnInfo',
                kernelRootPresent=True, typePrettyExplicit='PARSER_FIXTURE_NOT_LEAN_TYPE',
                axioms=[], universeParameters=[], opaqueClassification='SOURCE_OPAQUE_PARSER_FIXTURE',
                sourceAgreement=None, nativeAccepted=False))
        generated = [dict(actualName='GENERATED_PARSER_FIXTURE', includedIn319ExplicitRootCount=False)]
        binding = dict(freshOleanPathComparisonPassed=True, expectedNamedRoots=319,
                       actualStructures=[{} for _ in range(11)], observedTargetOwnedConstants=320)
        summary = dict(status='RUNTIME_DIAGNOSTIC_COMPLETE_NOT_SCIENTIFIC_ACCEPTANCE',
            explicitRootsCompleted=319, explicitPrivateCompleted=50, actualStructureCount=11,
            generatedTargetOwnedConstants=1, observedTargetOwnedConstants=320,
            allExplicitNamesResolvedUniquely=True, axiomPolicyPass=None, sourceAgreement=None,
            publicationBinding=None, nativeAccepted=False)
        return dict(binding=binding, roots=roots, generated=generated, summary=summary)

    def stream(self, f):
        rows = ['C29_BINDING_JSON ' + json.dumps(f['binding'])]
        rows += ['C29_ROOT_JSON ' + json.dumps(r) for r in f['roots']]
        rows += ['C29_GENERATED_JSON ' + json.dumps(r) for r in f['generated']]
        if f['summary'] is not None:
            rows.append('C29_SUMMARY_JSON ' + json.dumps(f['summary']))
        return '\n'.join(rows)

    def rejected(self, mutate, native_exit=0):
        fixture = self.fixture(); mutate(fixture)
        with self.assertRaises((ValueError, KeyError, TypeError)):
            self.validator(self.expected, self.stream(fixture), native_exit)

    def test_synthetic_complete_fixture_tests_parser_only(self):
        value = self.validator(self.expected, self.stream(self.fixture()), 0)
        self.assertTrue(value['diagnosticOutputComplete'])
        self.assertFalse(value['nativeAccepted'])
        self.assertIsNone(value['axiomPolicyPass'])

    def test_nonzero_native_rejects_even_complete_synthetic_stream(self):
        self.rejected(lambda f: None, native_exit=7)

    def test_missing_root(self):
        self.rejected(lambda f: f['roots'].pop())

    def test_reordered_root(self):
        self.rejected(lambda f: f['roots'].reverse())

    def test_duplicate_actual_root(self):
        self.rejected(lambda f: f['roots'][1].update(actualName=f['roots'][0]['actualName']))

    def test_wrong_private_flag(self):
        self.rejected(lambda f: f['roots'][0].update(actualPrivate=not f['roots'][0]['sourcePrivate']))

    def test_missing_type(self):
        self.rejected(lambda f: f['roots'][0].update(typePrettyExplicit=''))

    def test_invalid_axiom_array(self):
        self.rejected(lambda f: f['roots'][0].update(axioms='not an array'))

    def test_missing_terminal_summary(self):
        self.rejected(lambda f: f.update(summary=None))

    def test_generated_conflated_with_explicit(self):
        self.rejected(lambda f: f['generated'][0].update(actualName=f['roots'][0]['actualName']))

    def test_generated_marked_explicit(self):
        self.rejected(lambda f: f['generated'][0].update(includedIn319ExplicitRootCount=True))

    def test_forbidden_acceptance(self):
        self.rejected(lambda f: f['summary'].update(nativeAccepted=True))

    def test_fresh_comparison_false(self):
        self.rejected(lambda f: f['binding'].update(freshOleanPathComparisonPassed=False))

    def test_structure_count_wrong(self):
        self.rejected(lambda f: f['binding'].update(actualStructures=[]))

    def test_owned_partition_wrong(self):
        self.rejected(lambda f: f['summary'].update(observedTargetOwnedConstants=321))

    def test_truncated_json(self):
        with self.assertRaises(ValueError):
            self.validator(self.expected, 'C29_BINDING_JSON {', 0)


if __name__ == '__main__':
    unittest.main()
