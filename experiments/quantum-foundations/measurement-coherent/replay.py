"""Replay fixed authored sources, not model output, a production verifier or a sandbox.

Requires an already provisioned, matching Lean 4.33 checkout. Never installs or
updates dependencies; only invokes `lake env` for environment discovery.
"""
from __future__ import annotations
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import re
import shutil
import subprocess
import sys
import time

PACKAGE = Path(__file__).resolve().parent
PREDECESSOR = 'experiments/quantum-foundations/measurement-completeness/QuantumBlockEncoding/MeasurementProbability.lean'
PREDECESSOR_SHA = '33c1a01b8f1e752f22acbc12ae47faa503e5dc7ae5f3f4d73dff39eeb9505775'
MANIFEST_SHA = '510171e8214a2ac5e00f16c1bf92ad474d2de42c4cd2dc2b3d411272f7b58763'
FILES = {
    'QuantumBlockEncoding/MeasurementCoherent.lean': '22ef9784a3fe636b9ea07cf622bce01572425e2706e540e547934ec078dba34c',
    'Canary.lean': '49bd69b2e2efa31d39f83d34a6a9394990a08666bb9abb1b9b760da05f4e6290',
    'CheckSignatures.lean': 'abffe7799bc4fac0d6de44b19354484238b0001031c515b9d79d31e72779609d',
    'controls/OutputCompleteness.lean': '17165384f19fe213ccb11e2ed9138c4b16db8c4d4e40ff16b7af2f272345634b',
    'ExportHelpers.lean': '51cdde5efef3359dc3be057e5a887675fcc3253158c84d3be5e42865c1c02880',
}
ROOTS = ['QuantumBlockEncoding.MeasurementProbability.sum_norm_sq_eq',
         'QuantumBlockEncoding.MeasurementCoherent.branchIsometry',
         'QuantumBlockEncoding.MeasurementCoherent.branchIsometry_apply',
         'QuantumBlockEncoding.MeasurementCoherent.sum_inner_eq']
ORDINARY = {'propext', 'Classical.choice', 'Quot.sound'}
sha = lambda data: hashlib.sha256(data).hexdigest()


class ReplayFailure(RuntimeError):
    def __init__(self, kind, code):
        self.kind, self.code = kind, code
        super().__init__(code)


def observations(text, expected):
    """Strict C401 observation parser, with exact ordered root coverage."""
    rows, cursor = [], 0
    for m in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text, re.DOTALL):
        if text[cursor:m.start()].strip():
            raise ValueError('unexpected observation prelude')
        names = [x.strip() for x in m[2].split(',')]
        if any(not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.]*', n) for n in names):
            raise ValueError('malformed axiom list')
        if len(names) != len(set(names)):
            raise ValueError('duplicate axiom')
        rows.append({'name': m[1], 'axioms': names})
        cursor = m.end()
    if text[cursor:].strip() or [r['name'] for r in rows] != list(expected):
        raise ValueError('missing, duplicate, reordered or unparsed observation')
    return rows


def check_positive(text):
    rows = observations(text, ROOTS)
    if any(set(row['axioms']) != ORDINARY for row in rows):
        raise ValueError('not exactly the ordinary three axioms')
    return rows


def output_path(repo, value):
    """Reject drive/UNC/POSIX escapes, aliases, links and existing outputs."""
    parts = value.replace('\\', '/').split('/')
    reserved = {'CON', 'PRN', 'AUX', 'NUL', *('COM' + str(i) for i in range(1, 10)),
                *('LPT' + str(i) for i in range(1, 10))}
    if (PureWindowsPath(value).drive or Path(value).is_absolute() or len(parts) < 2
            or parts[0] != '_out' or any(not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', p)
                or p in {'.', '..'} or p.endswith('.') or p.split('.')[0].upper() in reserved
                for p in parts[1:])):
        raise ValueError('output must be a new repo-relative _out/name directory')
    root = repo.resolve()
    target = root.joinpath(*parts)
    for path in [target, *target.parents]:
        if path == root:
            break
        if path.is_symlink() or getattr(path, 'is_junction', lambda: False)():
            raise ValueError('output link/junction is not allowed')
    if not target.resolve().is_relative_to(root) or os.path.lexists(target):
        raise ValueError('output escapes repo or already exists')
    return target


def check_providers(text, expected):
    lines = [s.strip() for s in text.splitlines() if s.strip()]
    if not lines or any(not Path(s).is_absolute() or Path(s).suffix != '.olean' for s in lines):
        raise ValueError('malformed dependency output')
    selected = [Path(s).resolve() for s in lines]
    # Lean may repeat shared imports such as Init.olean. Only own providers
    # require exact-one coverage; same-basename foreign providers still fail.
    for own in expected:
        if [p for p in selected if p.name == own.name] != [own.resolve()]:
            raise ValueError('missing, duplicate or foreign own provider')


def check_signatures(text):
    names = re.findall(r'^@([A-Za-z0-9_.]+)\.\{', text, re.MULTILINE)
    if names != ROOTS[1:]:
        raise ValueError('missing, duplicate or reordered checked signatures')


def check_orientation(code, text):
    required = ['Application type mismatch', 'has type', 'but is expected to have type',
                'ContinuousLinearMap.adjoint (M i)', ROOTS[1] + ' M hM']
    if code == 0 or any(s not in text for s in required):
        raise ValueError('expected completeness-orientation type mismatch absent')


def check_graph(text):
    if not text.strip().startswith('COHERENT_HELPERS|'):
        raise ValueError('missing helper-slice marker')
    data = json.loads(text.strip().removeprefix('COHERENT_HELPERS|'))
    if (not isinstance(data, dict)
            or data.get('schema') != 'measurement-coherent.bounded-helper-expression-slice.v2'
            or data.get('lean_version') != '4.33.0' or data.get('public_roots') != ROOTS[1:]):
        raise ValueError('wrong helper-slice context')
    rows = data.get('rows', [])
    if not 3 <= len(rows) <= 64:
        raise ValueError('wrong helper-slice size')
    table, prefix = {}, ROOTS[1] + '.'
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('name'), str):
            raise ValueError('malformed graph row')
        name = row.get('name', '')
        if name in table or (name not in ROOTS[1:] and not name.startswith(prefix)):
            raise ValueError('duplicate or out-of-scope graph row')
        if row.get('generated_helper') is not name.startswith(prefix) or not isinstance(row.get('checked_type'), str):
            raise ValueError('malformed helper row')
        for key in ['value_references', 'type_references']:
            refs = row.get(key)
            if not isinstance(refs, list) or any(not isinstance(x, str) for x in refs) or refs != sorted(set(refs)):
                raise ValueError('malformed references')
        table[name] = row
    if any(n not in table for n in ROOTS[1:]) or ROOTS[1] not in table[ROOTS[3]]['value_references']:
        raise ValueError('missing public roots or actual overlap consumer edge')
    pending, seen, found = [ROOTS[1]], set(), False
    while pending:
        name = pending.pop()
        if name in seen:
            continue
        seen.add(name)
        for child in table[name]['value_references']:
            found |= child == ROOTS[0]
            if child.startswith(prefix):
                if child not in table:
                    raise ValueError('missing outlined helper')
                pending.append(child)
    if not found or any(n.startswith(prefix) and n not in seen for n in table):
        raise ValueError('predecessor path absent or unrelated helper included')
    return data


def available_memory_MiB():
    if os.name == 'nt':
        class Memory(ctypes.Structure):
            _fields_ = [('length', ctypes.c_ulong), ('load', ctypes.c_ulong),
                        *[(n, ctypes.c_ulonglong) for n in
                          ('total', 'available', 'page', 'apage', 'virtual', 'avirtual', 'extended')]]
        m = Memory()
        m.length = ctypes.sizeof(m)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):
            raise ReplayFailure('ENV_BLOCKED', 'memory_measurement_failed')
        return m.available // 1048576
    if sys.platform.startswith('linux'):
        data = Path('/proc/meminfo').read_text()
        available = int(re.search(r'^MemAvailable:\s+(\d+)', data, re.MULTILINE)[1]) // 1024
        limit, current = Path('/sys/fs/cgroup/memory.max'), Path('/sys/fs/cgroup/memory.current')
        if limit.is_file() and current.is_file() and limit.read_text().strip() != 'max':
            available = min(available, (int(limit.read_text()) - int(current.read_text())) // 1048576)
        return available
    raise ReplayFailure('ENV_BLOCKED', 'memory_measurement_unsupported')


def preflight(required):
    free = available_memory_MiB()
    if free < required:
        error = ReplayFailure('ENV_BLOCKED', 'memory_reserve_not_met')
        error.free_MiB = free
        raise error
    return free


def discover_repo(value):
    candidates = [Path(value)] if value else list(PACKAGE.parents)
    for root in candidates:
        if all((root / name).is_file() for name in ['lean-toolchain', 'lake-manifest.json', PREDECESSOR]):
            return root.resolve()
    raise ValueError('matching provisioned repository not found; pass --repo')


def replay(repo, out):
    out.mkdir(parents=True, exist_ok=False)
    record = {'schema': 'measurement-coherent.fixed-replay.v1', 'success': False, 'status': 'started',
              'source_consumer_success': False, 'graph_status': 'not_run', 'stages': [],
              'full_repository_gate': False, 'main_admitted': False, 'stable_QA_gold': False}
    def save():
        (out / 'result.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    def require(ok, code, kind='IMPLEMENTATION_FAILED'):
        if not ok:
            raise ReplayFailure(kind, code)
    def run(label, command, env=None, graph=False):
        entry = {'label': label, 'status': 'started', 'required_free_MiB': 6144 if graph else 5120,
                 'cap_MiB': 2048 if graph else 1536, 'jobs': 1, 'timeout_seconds': 120}
        record['stages'].append(entry)
        save()
        start, stdout, stderr = time.monotonic(), b'', b''
        try:
            entry['free_MiB'] = preflight(entry['required_free_MiB'])
            result = subprocess.run(command, cwd=repo, env=env, capture_output=True, timeout=120)
            stdout, stderr = result.stdout, result.stderr
            entry.update(exit_code=result.returncode, status='observed')
            return result
        except subprocess.TimeoutExpired as error:
            stdout, stderr = error.stdout or b'', error.stderr or b''
            raise ReplayFailure('ENV_BLOCKED', 'stage_timeout') from None
        except ReplayFailure as error:
            if hasattr(error, 'free_MiB'):
                entry['free_MiB'] = error.free_MiB
            raise
        except OSError:
            raise ReplayFailure('ENV_BLOCKED', 'stage_launch_failed') from None
        finally:
            entry['seconds'] = round(time.monotonic() - start, 3)
            for key, data in [('stdout', stdout), ('stderr', stderr)]:
                name = label + '.' + key
                (out / name).write_bytes(data)
                entry[key] = {'path': name, 'sha256': sha(data)}
            save()
    def passed():
        record['stages'][-1]['status'] = 'passed'
        save()
    save()
    try:
        require((repo / 'lean-toolchain').read_text().strip() == 'leanprover/lean4:v4.33.0', 'wrong_toolchain', 'ENV_BLOCKED')
        require(sha((repo / 'lake-manifest.json').read_bytes()) == MANIFEST_SHA, 'wrong_manifest', 'ENV_BLOCKED')
        require((repo / '.lake/packages').is_dir(), 'dependencies_not_provisioned', 'ENV_BLOCKED')
        inputs = {n: PACKAGE / n for n in FILES}
        inputs['QuantumBlockEncoding/MeasurementProbability.lean'] = repo / PREDECESSOR
        pins = dict(FILES, **{'QuantumBlockEncoding/MeasurementProbability.lean': PREDECESSOR_SHA})
        record['input_pins'] = pins
        for name, source in inputs.items():
            require(source.is_file() and sha(source.read_bytes()) == pins[name], 'fixed_input_mismatch', 'ENV_BLOCKED')
            target = out / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        prefix = run('environment-prefix', ['lake', 'env', 'lean', '-M1536', '-j1', '--print-prefix'])
        require(prefix.returncode == 0, 'lake_environment_failed', 'ENV_BLOCKED'); passed()
        binary = Path(prefix.stdout.decode().strip()) / ('bin/lean.exe' if os.name == 'nt' else 'bin/lean')
        require(binary.is_file(), 'actual_binary_missing', 'ENV_BLOCKED')
        record['binary_sha256'] = sha(binary.read_bytes())
        base = run('environment-path', ['lake', 'env', sys.executable, '-B', '-c',
                                      'import os; print(os.environ.get("LEAN_PATH", ""))'])
        require(base.returncode == 0, 'lake_path_failed', 'ENV_BLOCKED'); passed()
        paths = [Path(p) if Path(p).is_absolute() else repo / p for p in base.stdout.decode().strip().split(os.pathsep) if p]
        paths = [p.resolve() for p in paths if p.resolve() != (repo / '.lake/build/lib/lean').resolve()]
        require(bool(paths), 'empty_dependency_path', 'ENV_BLOCKED')
        env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, [out, *paths])))
        version = run('version', [str(binary), '--version'], env)
        require(version.returncode == 0 and re.search(rb'\bversion 4\.33\.0(?:\s|,|\(|$)', version.stdout), 'wrong_actual_binary', 'ENV_BLOCKED'); passed()
        record['toolchain_sha256'] = sha((repo / 'lean-toolchain').read_bytes())
        record['manifest_sha256'] = MANIFEST_SHA
        options = ['-M1536', '-j1', '--root=' + str(out)]
        def lean(label, args, graph=False):
            return run(label, [str(binary), *args], env, graph)
        def positive(label, args):
            result = lean(label, [*options, *args])
            kind = 'ENV_BLOCKED' if b'memory_exception' in result.stderr else 'IMPLEMENTATION_FAILED'
            require(result.returncode == 0, label + '_failed', kind)
            passed()
            return result
        pred, source = [out / ('QuantumBlockEncoding/' + n + '.lean') for n in ['MeasurementProbability', 'MeasurementCoherent']]
        positive('predecessor', ['-o', str(pred.with_suffix('.olean')), str(pred)])
        require(pred.with_suffix('.olean').is_file(), 'own_predecessor_not_emitted')
        deps = positive('source-deps', ['--deps', str(source)])
        check_providers(deps.stdout.decode(), [pred.with_suffix('.olean')])
        positive('source', ['-o', str(source.with_suffix('.olean')), str(source)])
        require(source.with_suffix('.olean').is_file(), 'own_source_not_emitted')
        for name in ['Canary.lean', 'CheckSignatures.lean', 'controls/OutputCompleteness.lean']:
            deps = positive(name.split('/')[-1].removesuffix('.lean') + '-deps', ['--deps', str(out / name)])
            check_providers(deps.stdout.decode(), [source.with_suffix('.olean')])
        record['own_olean_pins'] = {p.with_suffix('.olean').relative_to(out).as_posix(): sha(p.with_suffix('.olean').read_bytes()) for p in [pred, source]}
        record['axioms'] = check_positive(positive('consumer', [str(out / 'Canary.lean')]).stdout.decode())
        check_signatures(positive('checked-signatures', [str(out / 'CheckSignatures.lean')]).stdout.decode())
        wrong = lean('orientation-control', [*options, str(out / 'controls/OutputCompleteness.lean')])
        check_orientation(wrong.returncode, wrong.stdout.decode()); passed()
        record.update(source_consumer_success=True, graph_status='started')
        save()
        graph_options = ['-M2048', '-j1', '--root=' + str(out)]
        graph_deps = lean('graph-deps', [*graph_options, '--deps', str(out / 'ExportHelpers.lean')], graph=True)
        require(graph_deps.returncode == 0, 'graph_dependency_query_failed', 'ENV_BLOCKED')
        check_providers(graph_deps.stdout.decode(), [source.with_suffix('.olean')]); passed()
        graph = lean('graph', [*graph_options, str(out / 'ExportHelpers.lean')], graph=True)
        require(graph.returncode == 0, 'graph_failed', 'ENV_BLOCKED' if b'memory_exception' in graph.stderr else 'IMPLEMENTATION_FAILED')
        data = check_graph(graph.stdout.decode()); passed()
        graph_file = out / 'bounded-helper-graph.json'
        graph_file.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        record.update(graph_status='passed', graph_sha256=sha(graph_file.read_bytes()))
        require(all(sha(p.read_bytes()) == pins[n] and sha((out / n).read_bytes()) == pins[n] for n, p in inputs.items()), 'input_changed')
        require(sha(binary.read_bytes()) == record['binary_sha256'] and sha((repo / 'lake-manifest.json').read_bytes()) == MANIFEST_SHA, 'environment_changed', 'ENV_BLOCKED')
        require(all(sha((out / n).read_bytes()) == h for n, h in record['own_olean_pins'].items()), 'own_provider_changed')
        record.update(success=True, status='fixed_preparatory_replay_passed', failure_class='NONE')
    except Exception as error:
        kind = error.kind if isinstance(error, ReplayFailure) else ('ENV_BLOCKED' if isinstance(error, OSError) else 'IMPLEMENTATION_FAILED')
        code = error.code if isinstance(error, ReplayFailure) else ('filesystem_failure' if isinstance(error, OSError) else 'observation_rejected')
        record.update(success=False, status='failed', failure_class=kind, failure_code=code)
        if record['stages']:
            record['stages'][-1].update(status='failed', failure_class=kind, failure_code=code)
        if record['graph_status'] == 'started':
            record['graph_status'] = 'failed'
    finally:
        save()
    return record['success']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', help='already provisioned matching checkout; otherwise search ancestors')
    parser.add_argument('--output', required=True, help='new repo-relative _out/name directory')
    args = parser.parse_args()
    try:
        repo = discover_repo(args.repo)
        out = output_path(repo, args.output)
    except ValueError as error:
        parser.error(str(error))
    success = replay(repo, out)
    print(json.dumps({'success': success, 'scope': 'fixed_preparatory_sources_only',
                      'full_repository_gate': False, 'main_admitted': False, 'stable_QA_gold': False}))
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
