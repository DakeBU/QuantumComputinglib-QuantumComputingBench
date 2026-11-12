"""Synthetic Linux resource fixtures and real Python children only. No Lean."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from types import SimpleNamespace

import resource_gate as gate
import runner_v2 as adapter

PACKAGE = Path(__file__).parent
PROJECT = Path(os.environ.get('C31_TEST_PROJECT', Path.cwd()))
CONTEXT = dict(platform='linux', CI='true', GITHUB_ACTIONS='true', RUNNER_OS='Linux',
               GITHUB_RUN_ID='123456', GITHUB_JOB='SYNTHETIC_RESOURCE_FIXTURE', GITHUB_SHA='a' * 40)
MOUNT = '/sys/fs/cgroup'


def resource_files(available_mib=12288, child_limit_mib=10240, child_used_mib=1024,
                   parent_limit='max', parent_used_mib=2048):
    values = {'/proc/meminfo': f'MemTotal: 16777216 kB\nMemAvailable: {available_mib * 1024} kB\n',
              '/proc/self/cgroup': '0::/job\n',
              '/proc/self/mountinfo': '31 20 0:27 / /sys/fs/cgroup rw - cgroup2 cgroup rw\n'}
    for path, maximum, used in ((MOUNT + '/job', child_limit_mib * gate.MIB, child_used_mib),
                                (MOUNT, parent_limit, parent_used_mib)):
        values[path + '/memory.max'] = str(maximum) + '\n'
        values[path + '/memory.current'] = str(used * gate.MIB) + '\n'
        values[path + '/memory.events'] = 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\n'
    return {name: value.encode('ascii') for name, value in values.items()}


def snapshot(files=None, context=None):
    data = resource_files() if files is None else files
    return gate.sample(context=CONTEXT if context is None else context,
                       read_bytes=lambda name: data[name])


def native_result(code=0, timeout=False):
    return dict(PID=123, exitCode=code, timedOut=timeout, startedUTC=gate.utc(),
                finishedUTC=gate.utc(), wallSeconds=.1, stdoutSHA256='a' * 64, stderrSHA256='b' * 64)


class ResourceGateTests(unittest.TestCase):
    def test_complete_measured_gate_and_hash_bindings(self):
        row = snapshot(); self.assertTrue(gate.validate_snapshot(row))
        self.assertEqual(row['effectiveHeadroomBytes'], 9216 * gate.MIB)
        self.assertEqual(row['requiredHeadroomBytes'], 7168 * gate.MIB)
        self.assertEqual(len(row['fileReads']), 9)
        self.assertTrue(all(len(r['sha256']) == 64 for r in row['fileReads']))

    def test_host_available_and_every_visible_parent_limit_constrain(self):
        for files in (resource_files(available_mib=7167),
                      resource_files(child_limit_mib=8192, child_used_mib=1025),
                      resource_files(parent_limit=8192 * gate.MIB, parent_used_mib=1025)):
            row = snapshot(files)
            self.assertTrue(row['observationComplete']); self.assertFalse(row['gatePassed'])
            with self.assertRaises(ValueError): gate.validate_snapshot(row)

    def test_exact_boundary_passes_but_one_byte_less_fails(self):
        files = resource_files(child_limit_mib=8192, child_used_mib=1024)
        self.assertTrue(gate.validate_snapshot(snapshot(files)))
        files[MOUNT + '/job/memory.current'] = str(1024 * gate.MIB + 1).encode()
        self.assertFalse(snapshot(files)['gatePassed'])

    def test_visible_unlimited_limits_still_require_actual_host_available(self):
        files = resource_files(); files[MOUNT + '/job/memory.max'] = b'max\n'
        row = snapshot(files); self.assertTrue(gate.validate_snapshot(row))
        self.assertEqual(row['effectiveHeadroomBytes'], 12288 * gate.MIB)

    def test_v1_unknown_mount_missing_and_malformed_fields_never_green(self):
        mutations = [('/proc/self/cgroup', b'3:memory:/job\n'),
                     ('/proc/self/cgroup', b''), ('/proc/self/cgroup', b'0::/a\n0::/b\n'),
                     ('/proc/self/cgroup', b'0::/../escape\n'), ('/proc/self/mountinfo', b''),
                     ('/proc/meminfo', b'MemFree: 999999999 kB\n'),
                     ('/proc/meminfo', b'MemAvailable: unknown kB\n'),
                     (MOUNT + '/job/memory.max', b'unknown'),
                     (MOUNT + '/job/memory.current', b'-1'),
                     (MOUNT + '/job/memory.events', b'oom 0\n'),
                     (MOUNT + '/memory.events', b'oom 0\noom_kill 0\noom_kill 1\n')]
        for name, value in mutations:
            files = resource_files(); files[name] = value
            with self.subTest(name=name, value=value):
                row = snapshot(files); self.assertFalse(row['gatePassed'])
                with self.assertRaises(ValueError): gate.validate_snapshot(row)
        for name in resource_files():
            files = resource_files(); files.pop(name)
            self.assertFalse(snapshot(files)['gatePassed'])

    def test_windows_nonci_and_missing_ci_identity_forbidden_before_os_reads(self):
        for key, value in [('platform', 'win32'), ('platform', 'darwin'), ('CI', None),
                           ('GITHUB_ACTIONS', 'false'), ('RUNNER_OS', 'Windows'),
                           ('GITHUB_RUN_ID', None), ('GITHUB_JOB', ''), ('GITHUB_SHA', None)]:
            context = dict(CONTEXT); context[key] = value
            row = snapshot(context=context)
            self.assertFalse(row['gatePassed']); self.assertEqual(row['fileReads'], [])

    def test_missing_or_forged_snapshot_fields_rejected(self):
        for field in snapshot():
            row = snapshot(); row.pop(field)
            with self.subTest(field=field), self.assertRaises((ValueError, KeyError, TypeError)):
                gate.validate_snapshot(row)
        for field in snapshot()['cgroups'][0]:
            row = snapshot(); row['cgroups'][0].pop(field)
            with self.assertRaises((ValueError, KeyError, TypeError)): gate.validate_snapshot(row)
        row = snapshot(resource_files(available_mib=100)); row['gatePassed'] = True
        with self.assertRaises(ValueError): gate.validate_snapshot(row)

    def test_delegated_mount_hidden_ancestors_refused_as_unknown(self):
        files = resource_files()
        files['/proc/self/cgroup'] = b'0::/delegated/job\n'
        files['/proc/self/mountinfo'] = b'31 20 0:27 /delegated /sys/fs/cgroup rw - cgroup2 cgroup rw\n'
        row = snapshot(files); self.assertFalse(row['gatePassed'])
        self.assertIn('unknown effective ceiling', row['failure'])
        # Ancestors above the exposed mount are unobservable: no green fallback.
        files['/proc/self/cgroup'] = b'0::/different/job\n'
        self.assertFalse(snapshot(files)['gatePassed'])


class ClassificationTests(unittest.TestCase):
    def test_actual_ci1_diagnostic_classification_not_parent_verdict(self):
        actual = json.loads((PACKAGE / 'actual-ci1-analysis.json').read_text())
        self.assertEqual(gate.classify(actual['firstTargetProcess'], actual['stderrObserved'], {}, {}),
                         'LEAN_INTERNAL_MEMORY_EXCEPTION_SIGABRT_NOT_OS_OOM_PROOF')

    def test_os_kill_requires_cgroup_event_correlation_not_guess(self):
        before = snapshot(); after = snapshot()
        self.assertEqual(gate.classify(native_result(-9), '', before, after),
                         'PROCESS_SIGKILL_UNATTRIBUTED_NOT_INTERNAL_CAP_CLASSIFIED')
        after['cgroups'][0]['memoryEvents']['oom_kill'] += 1
        self.assertEqual(gate.classify(native_result(-9), '', before, after),
                         'SIGKILL_WITH_CGROUP_OOM_EVENT_CORRELATION_NOT_PID_ATTRIBUTION_PROOF')

    def test_timeout_api_error_and_unknown_fields_distinct(self):
        self.assertEqual(gate.classify(native_result(-9, True), '', {}, {}),
                         'WRAPPER_TIMEOUT_KILLED_OWN_CHILD')
        self.assertEqual(gate.classify(native_result(1), 'Probe.lean:1:1: error: unknown identifier', {}, {}),
                         'LEAN_REPORTED_ERROR_API_OR_IMPLEMENTATION_UNRESOLVED')
        self.assertEqual(gate.classify(native_result(1), '', {}, {}, 'Probe.lean:1:1: error: unknown identifier'),
                         'LEAN_REPORTED_ERROR_API_OR_IMPLEMENTATION_UNRESOLVED')
        for field in native_result():
            row = native_result(); row.pop(field)
            self.assertEqual(gate.classify(row, '', {}, {}), 'NATIVE_STARTUP_OR_RESULT_METADATA_INCOMPLETE')
        self.assertEqual(gate.classify(native_result(), 'lean::memory_exception excessive memory consumption', {}, {}),
                         'CONTRADICTORY_ZERO_EXIT_MEMORY_EXCEPTION')


class AdapterPythonOnlyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = json.loads((PACKAGE / 'ci2-profile.json').read_text())
        cls.base, cls.base_package = adapter.load_base(PROJECT, cls.profile)
        base_profile = json.loads((cls.base_package / 'profile.json').read_text())
        previous = sys.dont_write_bytecode; sys.dont_write_bytecode = True
        try: cls.api = cls.base.load_shared(PROJECT, base_profile)
        finally: sys.dont_write_bytecode = previous

    def test_finite_rewrite_and_unchanged_thread_invariant(self):
        result = adapter.rewrite_argv(['lean', '--threads=1', '--memory=3072', 'A.lean'])
        self.assertIn('--memory=5120', result); self.assertIn('--threads=1', result)
        self.assertNotIn('--memory=3072', result)
        for argv in ([], ['lean', '--memory=0'], ['lean', '--memory=99999'],
                     ['lean', '--memory=3072', '--memory=3072'], ['lean', '--threads=2'],
                     ['lean', '--memory', '3072']):
            with self.assertRaises(ValueError): adapter.rewrite_argv(argv)

    def test_unknown_or_low_preflight_starts_zero_children(self):
        for sampler in (lambda: snapshot(resource_files(available_mib=100)), lambda: {'gatePassed': True}):
            called = []
            callback = adapter.BudgetCallback(self.api, lambda: None, {'SYNTHETIC': True}, sampler=sampler)
            callback.native = lambda *a, **k: called.append(True)
            with tempfile.TemporaryDirectory() as directory:
                private = Path(directory)
                with self.assertRaises(adapter.PreflightRefused):
                    callback(private, 'fixture-no-start', ['lean'], private, dict(os.environ))
                self.assertEqual(called, [])
                self.assertTrue((private / 'ci2-fixture-no-start.preflight.json').exists())

    def test_rechecks_each_call_and_rejects_concurrent_child(self):
        callback = adapter.BudgetCallback(self.api, lambda: None, {}, sampler=snapshot)
        callback.lock.acquire()
        try:
            with self.assertRaises(adapter.PreflightRefused):
                callback(Path('unused'), 'fixture-concurrent', ['lean'], Path.cwd(), dict(os.environ))
        finally: callback.lock.release()

    def test_actual_python_zero_nonzero_timeout_pid_exit_hash_receipts(self):
        for label, code, timeout, expected in (
                ('python-zero', 'print("SYNTHETIC_PYTHON_NOT_LEAN")', 10, 'PROCESS_EXIT_ZERO'),
                ('python-nonzero', 'raise SystemExit(7)', 10, 'PROCESS_NONZERO_UNCLASSIFIED'),
                ('python-timeout', 'import time; time.sleep(5)', .05, 'WRAPPER_TIMEOUT_KILLED_OWN_CHILD')):
            callbacks = []
            callback = adapter.BudgetCallback(self.api, lambda: callbacks.append('pins-checked'),
                                               {'testScope': 'SYNTHETIC_RESOURCES_REAL_PYTHON_CHILD'}, sampler=snapshot)
            with tempfile.TemporaryDirectory() as directory:
                private = Path(directory)
                # These flags are Python script arguments after -c, not Python memory controls.
                argv = [sys.executable, '-c', code, '--threads=1', '--memory=3072']
                if expected == 'PROCESS_EXIT_ZERO':
                    result = callback(private, label, argv, private, dict(os.environ), timeout)
                    self.assertEqual(result['exitCode'], 0)
                else:
                    with self.assertRaises(self.api.NativeFailure):
                        callback(private, label, argv, private, dict(os.environ), timeout)
                row = json.loads((private / ('ci2-' + label + '.observation.json')).read_text())
                self.assertEqual(row['classification'], expected)
                self.assertIsInstance(row['nativeResult']['PID'], int)
                self.assertIn('--memory=5120', row['actualArgv'])
                self.assertEqual(len(row['preflightSHA256']), 64)
                self.assertEqual(len(row['postflightSHA256']), 64)
                self.assertEqual(len(callbacks), 2)
                self.assertFalse(row['nativeAccepted']); self.assertIsNone(row['axiomPolicyPass'])

    def test_runtime_budget_description_only_one_narrow_write_hook(self):
        callback = adapter.BudgetCallback(self.api, lambda: None, {'SYNTHETIC': True})
        with tempfile.TemporaryDirectory() as directory:
            private = Path(directory) / 'private'; private.mkdir()
            callback.write_json(private / 'runtime-environment.json', dict(nativeMemoryMiB=3072, nativeThreads=1))
            row = json.loads((private / 'runtime-environment.json').read_text())
            self.assertEqual(row['nativeMemoryMiB'], 5120); self.assertEqual(row['baseReportedMemoryMiB'], 3072)
            callback.write_json(private / 'other.json', dict(value=3072))
            self.assertEqual(json.loads((private / 'other.json').read_text()), dict(value=3072))

    def test_pin_callback_failure_starts_zero_children(self):
        def drift(): raise ValueError('SYNTHETIC_PIN_DRIFT')
        callback = adapter.BudgetCallback(self.api, drift, {}, sampler=snapshot)
        calls = []
        callback.native = lambda *args, **kwargs: calls.append(True)
        with tempfile.TemporaryDirectory() as directory:
            private = Path(directory)
            with self.assertRaisesRegex(ValueError, 'PIN_DRIFT'):
                callback(private, 'fixture-pin-drift', ['lean'], private, dict(os.environ))
            self.assertEqual(calls, []); self.assertEqual(list(private.iterdir()), [])

    def test_minimal_callback_rollback_restores_every_hook_after_error(self):
        load = lambda *args: None
        native = lambda *args: None
        write = lambda *args: None
        fake_base = SimpleNamespace(load_shared=load)
        fake_api = SimpleNamespace(native_call=native, write_json=write)
        callback = SimpleNamespace(write_json=lambda *args: None)
        with self.assertRaises(RuntimeError):
            with adapter.temporary_callbacks(fake_base, fake_api, callback):
                self.assertIs(fake_api.native_call, callback)
                self.assertIs(fake_base.load_shared(None, None), fake_api)
                raise RuntimeError('SYNTHETIC_ROLLBACK_TEST')
        self.assertIs(fake_base.load_shared, load)
        self.assertIs(fake_api.native_call, native); self.assertIs(fake_api.write_json, write)

    def test_unknown_postflight_and_incomplete_native_zero_result_never_green(self):
        for bad_after, incomplete in ((True, False), (False, True)):
            with tempfile.TemporaryDirectory() as directory:
                private = Path(directory)
                samples = iter([snapshot(), {'gatePassed': True} if bad_after else snapshot()])
                callback = adapter.BudgetCallback(self.api, lambda: None, {'SYNTHETIC': True},
                                                   sampler=lambda: next(samples))
                if incomplete:
                    callback.native = lambda *args, **kwargs: native_result()
                argv = [sys.executable, '-c', 'print("SYNTHETIC_PYTHON_ONLY")', '--memory=3072', '--threads=1']
                with self.assertRaises((ValueError, RuntimeError)):
                    callback(private, 'python-partial-metadata', argv, private, dict(os.environ), 10)

    def test_base14_and_source87_not_duplicated_or_relaxed(self):
        self.assertEqual(len(self.profile['baseFiles']), 14)
        base_profile = json.loads((self.base_package / 'profile.json').read_text())
        self.assertEqual(len(base_profile['roots']), 87)
        self.assertEqual(sum(r['sourcePrivate'] for r in base_profile['roots']), 8)
        self.assertEqual(len(base_profile['modules']), 3)
        bad = copy.deepcopy(self.profile); bad['baseFiles']['runner.py'] = '0' * 64
        with self.assertRaises(ValueError): adapter.load_base(PROJECT, bad)


if __name__ == '__main__':
    unittest.main()
