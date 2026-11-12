"""Static parser/path tests only: no Lake, Lean, provisioning or theorem run."""
from copy import deepcopy
from contextlib import redirect_stdout
import io
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import tempfile
import unittest
from unittest.mock import patch
import replay


def axiom_output(names=None):
    return '\n'.join("'" + name + "' depends on axioms: [propext,\n Classical.choice, Quot.sound]"
                     for name in (replay.ROOTS if names is None else names)) + '\n'


def graph_fixture():
    helper = replay.ROOTS[1] + '._proof_11'
    def row(name, refs):
        return {'name': name, 'checked_type': 'fixed static test type',
                'generated_helper': name == helper,
                'type_references': [], 'value_references': sorted(refs)}
    return {'schema': 'measurement-coherent.bounded-helper-expression-slice.v2',
            'lean_version': '4.33.0', 'public_roots': replay.ROOTS[1:],
            'rows': [row(replay.ROOTS[3], [replay.ROOTS[1]]), row(replay.ROOTS[2], []),
                     row(replay.ROOTS[1], [helper]), row(helper, [replay.ROOTS[0]])]}


class ObservationTests(unittest.TestCase):
    def test_exact_multiline_roots(self):
        self.assertEqual(len(replay.check_positive(axiom_output())), 4)

    def test_missing_duplicate_reordered_roots(self):
        for names in [[], replay.ROOTS[:-1], replay.ROOTS + [replay.ROOTS[-1]],
                      list(reversed(replay.ROOTS)), [replay.ROOTS[1], *replay.ROOTS[1:]]]:
            with self.subTest(names=names), self.assertRaises(ValueError):
                replay.check_positive(axiom_output(names))

    def test_wrong_case_and_unparsed_text(self):
        for text in [axiom_output().replace(replay.ROOTS[0], replay.ROOTS[0].lower()),
                     'warning\n' + axiom_output(), axiom_output() + 'unparsed', '']:
            with self.subTest(text=text[:30]), self.assertRaises(ValueError):
                replay.check_positive(text)

    def test_reject_extra_sorry_native_and_missing_axioms(self):
        for replacement in ['propext, sorryAx', 'propext, Lean.ofReduceBool',
                            'propext, newAxiom', 'sorryAx', '', 'propext, propext']:
            with self.subTest(replacement=replacement), self.assertRaises(ValueError):
                replay.check_positive(axiom_output().replace('propext', replacement, 1))

    def test_exact_ordinary_set_required(self):
        with self.assertRaises(ValueError):
            replay.check_positive(axiom_output().replace(', Quot.sound', '', 1))


class PathTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='measurement-coherent-test-')
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)

    def test_new_relative_output(self):
        expected = self.repo / '_out' / 'fixed-run'
        self.assertEqual(replay.output_path(self.repo, '_out/fixed-run'), expected)
        self.assertEqual(replay.output_path(self.repo, '_out\\fixed-run'), expected)
        self.assertFalse(expected.exists())

    def test_invalid_output_paths(self):
        # Synthetic roots are assembled from explicit components, not host data.
        drive, win_root = 'C:', '\\'
        posix = PurePosixPath('/') / '_out' / 'run'
        windows = PureWindowsPath(drive, win_root) / '_out' / 'run'
        drive_relative = PureWindowsPath(drive) / 'run'
        unc = PureWindowsPath(win_root * 2 + win_root.join(('server', 'share'))) / 'run'
        self.assertTrue(posix.is_absolute())
        self.assertTrue(windows.is_absolute())
        self.assertTrue(unc.is_absolute())
        self.assertTrue(drive_relative.drive)
        self.assertFalse(drive_relative.is_absolute())
        values = ['', '_out', '_out/', 'out/run', '../_out/run', '_out/../run',
                  '_out/./run', '_out//run', *map(str, [posix, windows, drive_relative, unc]),
                  '_out/run:stream', '_out/run.', '_out/CON',
                  '_out/LPT1.txt', '_out/white space', '_out/~user']
        for value in values:
            with self.subTest(value=value), self.assertRaises(ValueError):
                replay.output_path(self.repo, value)

    def test_existing_output_not_overwritten(self):
        (self.repo / '_out/run').mkdir(parents=True)
        with self.assertRaises(ValueError):
            replay.output_path(self.repo, '_out/run')

    def test_output_symlink_rejected(self):
        (self.repo / 'other').mkdir()
        try:
            (self.repo / '_out').symlink_to(self.repo / 'other', target_is_directory=True)
        except OSError:
            with patch.object(Path, 'is_symlink', autospec=True,
                              side_effect=lambda path: path == self.repo / '_out'):
                with self.assertRaises(ValueError):
                    replay.output_path(self.repo, '_out/run')
            return
        with self.assertRaises(ValueError):
            replay.output_path(self.repo, '_out/run')

    def test_provider_exact_own_file(self):
        own = self.repo / 'own/MeasurementCoherent.olean'
        other = self.repo / 'Mathlib.olean'
        replay.check_providers(str(other) + '\n' + str(own) + '\n', [own])

    def test_repeated_non_owned_init_dependency_is_legitimate(self):
        own = self.repo / 'own/MeasurementProbability.olean'
        init = self.repo / 'toolchain/Init.olean'
        pil2 = self.repo / 'Mathlib/Analysis/InnerProductSpace/PiL2.olean'
        text = '\n'.join(map(str, [init, own, init, pil2])) + '\n'
        replay.check_providers(text, [own])
        with self.assertRaises(ValueError):
            replay.check_providers(text + str(own) + '\n', [own])

    def test_malformed_missing_foreign_duplicate_provider(self):
        own = self.repo / 'own/MeasurementCoherent.olean'
        foreign = self.repo / 'old/MeasurementCoherent.olean'
        values = ['', str(foreign), str(own) + '\n' + str(own),
                  str(own) + '\n' + str(foreign), 'relative/MeasurementCoherent.olean',
                  str(own) + '\nwarning', str(own.with_suffix('.lean'))]
        for text in values:
            with self.subTest(text=text), self.assertRaises(ValueError):
                replay.check_providers(text, [own])

    def test_environment_failure_is_nonzero_and_public_safe(self):
        (self.repo / 'lean-toolchain').write_text('leanprover/lean4:v4.33.0\n')
        (self.repo / 'lake-manifest.json').write_text('{}\n')
        predecessor = self.repo / replay.PREDECESSOR
        predecessor.parent.mkdir(parents=True)
        predecessor.write_text('static environment marker, not Lean evidence\n')
        args = ['replay.py', '--repo', str(self.repo), '--output', '_out/failure']
        with patch.object(replay.sys, 'argv', args), redirect_stdout(io.StringIO()), \
                patch.object(replay.subprocess, 'run', side_effect=AssertionError('no compiler allowed')):
            self.assertEqual(replay.main(), 1)
        text = (self.repo / '_out/failure/result.json').read_text()
        result = json.loads(text)
        self.assertFalse(result['success'])
        self.assertFalse(result['source_consumer_success'])
        self.assertFalse(result['main_admitted'])
        self.assertFalse(result['stable_QA_gold'])
        self.assertEqual(result['graph_status'], 'not_run')
        self.assertEqual(result['failure_class'], 'ENV_BLOCKED')
        self.assertEqual(result['failure_code'], 'wrong_manifest')
        self.assertNotIn(str(self.repo), text)


class DiagnosticTests(unittest.TestCase):
    def test_clean_package_path_setup_without_private_directory(self):
        with tempfile.TemporaryDirectory(prefix='measurement-coherent-clean-') as directory:
            clean = Path(directory)
            self.assertFalse((clean / 'PRIVATE').exists())
            case = PathTests('test_new_relative_output')
            with patch.object(replay, 'PACKAGE', clean):
                try:
                    case.setUp()
                    case.test_new_relative_output()
                    self.assertFalse((clean / 'PRIVATE').exists())
                finally:
                    case.doCleanups()

    def test_signatures_order(self):
        def output(names):
            return '\n'.join('@' + name + '.{u} : complete_type' for name in names)
        replay.check_signatures(output(replay.ROOTS[1:]))
        for names in [replay.ROOTS[1:2], list(reversed(replay.ROOTS[1:])),
                      replay.ROOTS[1:] + [replay.ROOTS[1]]]:
            with self.subTest(names=names), self.assertRaises(ValueError):
                replay.check_signatures(output(names))

    def test_orientation_requires_actual_typed_mismatch(self):
        text = ('Application type mismatch has type but is expected to have type '
                'ContinuousLinearMap.adjoint (M i) ' + replay.ROOTS[1] + ' M hM')
        replay.check_orientation(1, text)
        for code, output in [(0, text), (1, 'error: noncomputable'),
                             (1, text.replace('but is expected to have type', ''))]:
            with self.subTest(code=code), self.assertRaises(ValueError):
                replay.check_orientation(code, output)

    def test_memory_reserves_are_not_lowered(self):
        with patch.object(replay, 'available_memory_MiB', return_value=5119):
            with self.assertRaises(replay.ReplayFailure):
                replay.preflight(5120)
        with patch.object(replay, 'available_memory_MiB', return_value=6143):
            self.assertEqual(replay.preflight(5120), 6143)
            with self.assertRaises(replay.ReplayFailure):
                replay.preflight(6144)

    def test_authored_inputs_have_exact_fixed_hashes(self):
        for name, digest in replay.FILES.items():
            with self.subTest(name=name):
                self.assertEqual(replay.sha((replay.PACKAGE / name).read_bytes()), digest)


class GraphTests(unittest.TestCase):
    def check(self, data):
        return replay.check_graph('COHERENT_HELPERS|' + json.dumps(data))

    def test_outlined_predecessor_path(self):
        self.assertEqual(len(self.check(graph_fixture())['rows']), 4)

    def test_reject_wrong_public_roots_and_row_coverage(self):
        cases = []
        for roots in [replay.ROOTS[1:2], list(reversed(replay.ROOTS[1:])), replay.ROOTS[1:] * 2]:
            data = graph_fixture(); data['public_roots'] = roots; cases.append(data)
        data = graph_fixture(); data['rows'].append(deepcopy(data['rows'][0])); cases.append(data)
        data = graph_fixture(); data['rows'].pop(0); cases.append(data)
        data = graph_fixture(); data['rows'].pop(); cases.append(data)
        for data in cases:
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.check(data)

    def test_reject_false_edges_scope_and_malformed_graph(self):
        for change in ['overlap', 'predecessor', 'outside', 'references', 'flag']:
            data = graph_fixture()
            if change == 'overlap': data['rows'][0]['value_references'] = []
            if change == 'predecessor': data['rows'][-1]['value_references'] = []
            if change == 'outside': data['rows'][-1]['name'] = 'Unrelated.helper'
            if change == 'references': data['rows'][0]['value_references'] *= 2
            if change == 'flag': data['rows'][-1]['generated_helper'] = False
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.check(data)
        for text in ['', 'COHERENT_HELPERS|[]', 'COHERENT_HELPERS|not-json']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                replay.check_graph(text)


if __name__ == '__main__':
    unittest.main()
