"""WIP independent formal diagnostic; never an admission/ROOT/axiom-policy gate."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PureWindowsPath
import re
import shutil
import subprocess
import sys
import time

MODULES = ('Core', 'Resources', 'Circuit', 'BlockEncoding', 'BlockEncodingClassics')
SIDECARS = ('.olean', '.olean.private', '.olean.server', '.ir')
OUT_REL = '_out/cubic-c29-diagnostic'
NO_ACCEPT = dict(sourceAgreement=None, publicationBinding=None, authorBinding=None,
                 axiomPolicyPass=None, scientific_ROOT=False, nativeAccepted=False)


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(path: Path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def safe_child(root: Path, relative: str):
    root = root.resolve()
    normalized = relative.replace('\\', '/')
    if not normalized or normalized.startswith('/') or PureWindowsPath(relative).is_absolute():
        raise ValueError('absolute/empty child path forbidden')
    if any(p in ('', '..') for p in normalized.split('/')) or ':' in normalized:
        raise ValueError('path escape/nonportable child path forbidden')
    path = root.joinpath(*normalized.split('/'))
    if not path.resolve().is_relative_to(root):
        raise ValueError('resolved child escapes root')
    return path


def write_json(path: Path, value):
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write('\n')


def verify_pins(root: Path, pins: dict):
    rows = []
    for relative, expected in pins.items():
        path = safe_child(root, relative)
        actual = sha(path)
        if actual != expected:
            raise ValueError('RESEAL hash mismatch: ' + relative)
        rows.append(dict(relativePath=relative, sha256=actual, bytes=path.stat().st_size))
    return rows


def verify_lean_help(text):
    if re.search(r'Lean \(version 4\.33\.0,', text) is None:
        raise ValueError('actual Lean binary is not the pinned 4.33.0 release')
    if not all(option in text for option in ('--threads', '--memory', '--print-prefix')):
        raise ValueError('actual Lean help lacks requested options')


def copy_local_providers(project: Path, fresh: Path):
    destination = safe_child(fresh, 'QuantumBlockEncoding')
    destination.mkdir()
    rows = []
    for module in MODULES:
        stem = '.lake/build/lib/lean/QuantumBlockEncoding/' + module
        required = safe_child(project, stem + '.olean')
        if not required.is_file():
            raise FileNotFoundError('missing inherited provider: ' + module)
        for suffix in SIDECARS:
            source = safe_child(project, stem + suffix)
            if source.is_file():
                dest = safe_child(destination, module + suffix)
                if dest.exists():
                    raise FileExistsError('provider destination already exists')
                before = sha(source)
                shutil.copyfile(source, dest)
                if sha(source) != before or sha(dest) != before:
                    raise ValueError('provider copy/source changed')
                rows.append(dict(module='QuantumBlockEncoding.' + module,
                                 source=str(source.resolve()), destination=str(dest.resolve()),
                                 sha256=before, bytes=dest.stat().st_size))
    return rows


class NativeFailure(RuntimeError):
    def __init__(self, label, result):
        super().__init__(f'{label}: native exit={result["exitCode"]}, timedOut={result["timedOut"]}')
        self.result = result


def native_call(private: Path, label: str, argv, cwd: Path, env: dict, timeout=600):
    if re.fullmatch(r'[a-z0-9-]+', label) is None:
        raise ValueError('unsafe native label')
    setup = dict(argv=list(map(str, argv)), cwd=str(cwd.resolve()), startedUTC=utc(),
                 wrapperPID=os.getpid(), timeoutSeconds=timeout,
                 selectedEnvironment={k: env.get(k) for k in ('LEAN_PATH', 'QBE_EXPECT_FRESH_OLEAN')})
    write_json(safe_child(private, label + '.setup.json'), setup)
    start = time.monotonic()
    result = dict(PID=None, startedUTC=setup['startedUTC'], exitCode=None,
                  timedOut=False, stdoutSHA256=None, stderrSHA256=None)
    stdout_path = safe_child(private, label + '.stdout.raw')
    stderr_path = safe_child(private, label + '.stderr.raw')
    try:
        with stdout_path.open('xb') as stdout, stderr_path.open('xb') as stderr:
            proc = subprocess.Popen(argv, cwd=cwd, env=env, stdout=stdout, stderr=stderr)
            result['PID'] = proc.pid
            write_json(safe_child(private, label + '.started.json'), dict(PID=proc.pid, startedUTC=utc()))
            print(json.dumps(dict(stage=label, PID=proc.pid, startedUTC=utc())), flush=True)
            try:
                result['exitCode'] = proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                result['timedOut'] = True
                proc.kill()  # Only this wrapper's own diagnostic child, never other jobs/processes.
                result['exitCode'] = proc.wait()
    finally:
        result.update(finishedUTC=utc(), wallSeconds=time.monotonic() - start)
        for key, path in [('stdoutSHA256', stdout_path), ('stderrSHA256', stderr_path)]:
            if path.exists():
                result[key] = sha(path)
        write_json(safe_child(private, label + '.result.json'), result)
    if result['exitCode'] != 0 or result['timedOut']:
        raise NativeFailure(label, result)
    return result


def artifact_file(path: Path):
    return (path.name.endswith(('.olean', '.olean.private', '.olean.server', '.ir')) or
            path.suffix.lower() in ('.so', '.dll', '.dylib', '.a', '.lib', '.o', '.bc', '.c') or
            '.so.' in path.name)


def inventory_providers(roots, excluded: Path):
    excluded = excluded.resolve()
    seen = set()
    rows = []
    for root in roots:
        root = root.resolve()
        if not root.is_dir():
            raise FileNotFoundError('configured provider root absent')
        for path in sorted(root.rglob('*')):
            if not path.is_file() or not artifact_file(path):
                continue
            real = path.resolve()
            if real.is_relative_to(excluded) or real in seen:
                continue
            # A symlink artifact must remain inside its explicitly inventoried search root.
            if not real.is_relative_to(root):
                raise ValueError('provider inventory symlink escapes configured root')
            seen.add(real)
            rows.append(dict(path=str(real), sha256=sha(real), bytes=real.stat().st_size))
    return rows


def partition_search_roots(roots):
    """Absent optional search roots cannot supply imports; preserve that state."""
    present, absent = [], []
    for root in roots:
        root = root.resolve()
        if root.is_dir():
            present.append(root)
        elif root.exists():
            raise ValueError('configured search root exists but is not a directory')
        else:
            absent.append(root)
    return present, absent


SECRET = re.compile(r'(?i)(?:Bearer\s+[A-Za-z0-9._~+/-]+|(?:ghp_|github_pat_|sk-)[A-Za-z0-9_-]+|'
                    r'(?:TOKEN|PASSWORD|SECRET|API_KEY)\s*=\s*[^\s"\']+|https?://[^\s/@:]+:[^\s/@]+@)')
ABSOLUTE = re.compile(r'(?<![\w$])(?:[A-Za-z]:[\\/][^\s"\'<>]*|/(?:[^\s"\'<>]+))')


def redact(text: str, logical_roots: dict):
    for actual, logical in sorted(logical_roots.items(), key=lambda p: len(p[0]), reverse=True):
        for variant in {actual, actual.replace('\\', '/'), actual.replace('\\', '\\\\')}:
            text = text.replace(variant, logical)
    text = SECRET.sub('[REDACTED_CREDENTIAL]', text)
    text = ABSOLUTE.sub('$ABSOLUTE_PATH_REDACTED', text)
    return text


def redact_tree(value, logical_roots):
    if isinstance(value, str):
        return redact(value, logical_roots)
    if isinstance(value, list):
        return [redact_tree(v, logical_roots) for v in value]
    if isinstance(value, dict):
        return {k: redact_tree(v, logical_roots) for k, v in value.items()}
    return value


def export_public(private: Path, public: Path, logical_roots: dict):
    receipts = []
    for raw in sorted(private.iterdir()):
        if not raw.is_file() or raw.suffix not in ('.raw', '.json'):
            continue
        if raw.is_symlink():
            raise ValueError('private log symlink forbidden')
        derived = raw.name + '.sanitized.txt' if raw.suffix == '.raw' else raw.name
        dest = safe_child(public, derived)
        text = raw.read_text(encoding='utf-8', errors='replace')
        if raw.suffix == '.json':
            value = redact_tree(json.loads(text), logical_roots)
            sanitized = json.dumps(value, indent=2, ensure_ascii=False) + '\n'
        else:
            sanitized = redact(text, logical_roots)
        if SECRET.search(sanitized) or ABSOLUTE.search(sanitized):
            raise ValueError('public sanitizer failed closed')
        for actual in logical_roots:
            if actual in sanitized:
                raise ValueError('unredacted configured absolute root')
        with dest.open('x', encoding='utf-8', newline='\n') as handle:
            handle.write(sanitized)
        receipts.append(dict(publicRelativePath=dest.name, rawSHA256=sha(raw),
                             publicSHA256=sha(dest), rawBytes=raw.stat().st_size))
    write_json(safe_child(public, 'raw-derivation-receipts.json'), dict(files=receipts, **NO_ACCEPT))


def load_validator(package: Path, versioned=False):
    name = 'validate-output.py'
    if versioned:
        pins = json.loads((package / 'pins.json').read_text(encoding='utf-8'))
        name = pins.get('activeValidator')
        if not isinstance(name, str) or name not in pins.get('versionedAuditFiles', {}):
            raise ValueError('active generated validator absent or unpinned')
        verify_pins(package, pins['versionedAuditFiles'])
    spec = importlib.util.spec_from_file_location('c29_selected_validator', safe_child(package, name))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate


def load_generated_validator(package: Path):
    load_validator(package, versioned=True)  # Verify all audit files before loading shared API.
    pins = json.loads((package / 'pins.json').read_text(encoding='utf-8'))
    spec = importlib.util.spec_from_file_location('c29_generated_validator',
                                                safe_child(package, pins['activeValidator']))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_fixture(stdout: str, exit_code: int, generated_expected=None, audit_module=None):
    """Real legacy API fixture only; never a Cubic axiom-policy/admission result."""
    if exit_code != 0:
        raise ValueError('fixture native failure, not API success')
    records = {tag: [] for tag in ('C29_ROOT_JSON', 'C29_BINDING_JSON', 'C29_SUMMARY_JSON', 'C29_GENERATED_JSON')}
    for line in stdout.splitlines():
        for tag in records:
            if line.startswith(tag + ' '):
                records[tag].append(json.loads(line[len(tag) + 1:]))
    roots = records['C29_ROOT_JSON']
    if len(roots) != 5 or len(records['C29_SUMMARY_JSON']) != 1 or len(records['C29_BINDING_JSON']) != 1:
        raise ValueError('fixture stream incomplete')
    by_name = {row['sourceUserName']: row for row in roots}
    if set(by_name) != {'Fixture.supplied', 'Fixture.exposed', 'Fixture.hidden', 'Fixture.sealed', 'Fixture.Pair'}:
        raise ValueError('fixture root identities mismatch')
    if by_name['Fixture.supplied']['actualKind'] != 'axiomInfo' or 'Fixture.supplied' not in by_name['Fixture.supplied']['axioms']:
        raise ValueError('fixture genuine axiom was not observed')
    if not by_name['Fixture.hidden']['actualPrivate'] or 'Fixture.supplied' not in by_name['Fixture.hidden']['axioms']:
        raise ValueError('fixture private theorem/axiom propagation failed')
    if by_name['Fixture.sealed']['actualKind'] != 'opaqueInfo' or not by_name['Fixture.sealed']['actualHasValueAllowOpaque']:
        raise ValueError('fixture opaque-with-body classification failed')
    if by_name['Fixture.Pair']['actualKind'] != 'inductInfo':
        raise ValueError('fixture structure classification failed')
    binding = records['C29_BINDING_JSON'][0]; summary = records['C29_SUMMARY_JSON'][0]
    if binding['freshOleanPathComparisonPassed'] is not True or len(binding['actualStructures']) != 1:
        raise ValueError('fixture fresh binding/structure metadata failed')
    if summary['explicitRootsCompleted'] != 5 or summary['explicitPrivateCompleted'] != 1 or summary['actualStructureCount'] != 1:
        raise ValueError('fixture summary mismatch')
    if summary['nativeAccepted'] is not False or summary['sourceAgreement'] is not None:
        raise ValueError('fixture emitted forbidden acceptance')
    extra = {}
    if generated_expected is not None:
        if audit_module is None or len(generated_expected) != 15:
            raise ValueError('fixture generated validator/set unavailable')
        extra = audit_module.validate_generated(records['C29_GENERATED_JSON'], generated_expected,
                                               [r['actualName'] for r in roots], summary)
        if summary['generatedTargetOwnedConstants'] != 15 or summary['observedTargetOwnedConstants'] != 20:
            raise ValueError('fixture generated partition mismatch')
    return dict(status='LEGACY_API_FIXTURE_OBSERVED_NOT_CUBIC_EVIDENCE', roots=5,
                generatedAudit=extra, **NO_ACCEPT)


def verify_driver_import_target(path: Path, expected_module: str):
    """Check the frozen legacy driver's direct import and runtime target before Lean."""
    source = path.read_text(encoding='utf-8')
    imports = re.findall(r'(?m)^import[ \t]+([A-Za-z_][A-Za-z0-9_.]*)[ \t]*$', source)
    targets = re.findall(r'(?m)^[ \t]*let target := `([A-Za-z_][A-Za-z0-9_.]*)[ \t]*$', source)
    if imports != [expected_module, 'Lean']:
        raise ValueError('driver import-target mismatch: expected first import ' + expected_module)
    if targets != [expected_module]:
        raise ValueError('driver runtime target mismatch: ' + expected_module)
    return dict(expectedModule=expected_module, firstImport=imports[0],
                runtimeTarget=targets[0], driverSHA256=sha(path))


def verify_active_drivers(package: Path, pins: dict):
    bindings = {}
    for key, expected in [('activeFixtureProbe', 'Fixture'),
                          ('activeProbe', 'QuantumBlockEncoding.CubicStatePreparation')]:
        name = pins.get(key)
        if not isinstance(name, str) or name not in pins['versionedDriverFiles']:
            raise ValueError('missing or unpinned active driver: ' + key)
        verify_pins(package, {name: pins['versionedDriverFiles'][name]})
        bindings[key] = verify_driver_import_target(safe_child(package, name), expected)
    return bindings


def run(project: Path, package: Path):
    project = project.resolve()
    package = package.resolve()
    out = safe_child(project, OUT_REL)
    out.mkdir(parents=True, exist_ok=False)  # Exclusive: never clean/reuse past diagnostic outputs.
    private = safe_child(out, 'private'); private.mkdir(mode=0o700)
    public = safe_child(out, 'public'); public.mkdir()
    logical = {str(project): '$PROJECT'}
    status = dict(status='WIP_NOT_RUN', cleanTransitive=False, **NO_ACCEPT)
    try:
        pins = json.loads((package / 'pins.json').read_text(encoding='utf-8'))
        input_rows = verify_pins(project, pins['projectInputs'])
        package_rows = verify_pins(package, pins['immutableCandidate3Files'])
        driver_rows = verify_pins(package, pins['versionedDriverFiles'])
        audit_rows = verify_pins(package, pins['versionedAuditFiles'])
        if pins.get('expectedGeneratedFile') != 'expected-generated-ci2.json':
            raise ValueError('active generated expected-set binding absent')
        audit_module = load_generated_validator(package)
        generated_expected = json.loads(safe_child(package, pins['expectedGeneratedFile']).read_text(encoding='utf-8'))
        driver_bindings = verify_active_drivers(package, pins)
        write_json(private / 'inputs.json', dict(projectInputs=input_rows, candidate3Files=package_rows,
                                                versionedDriverFiles=driver_rows, activeProbe=pins['activeProbe'],
                                                activeFixtureProbe=pins['activeFixtureProbe'], driverBindings=driver_bindings,
                                                activeValidator=pins['activeValidator'], versionedAuditFiles=audit_rows))
        env = dict(os.environ)
        bootstrap = shutil.which('lean', path=env.get('PATH'))
        if not bootstrap:
            raise FileNotFoundError('lean executable absent from lake env PATH')
        native_call(private, '01-help', [bootstrap, '--help'], project, env, timeout=30)
        help_text = (private / '01-help.stdout.raw').read_text(encoding='utf-8', errors='strict')
        verify_lean_help(help_text)
        native_call(private, '02-prefix', [bootstrap, '--print-prefix'], project, env, timeout=30)
        prefix = Path((private / '02-prefix.stdout.raw').read_text(encoding='utf-8').strip()).resolve()
        logical[str(prefix)] = '$TOOLCHAIN'
        lean = prefix / 'bin' / ('lean.exe' if os.name == 'nt' else 'lean')
        if not lean.is_file():
            raise FileNotFoundError('resolved actual toolchain binary absent')
        raw_roots = env.get('LEAN_PATH', '').split(os.pathsep)
        if not raw_roots or any(not p for p in raw_roots):
            raise ValueError('lake env must supply nonempty explicit LEAN_PATH entries')
        roots = [(Path(p) if Path(p).is_absolute() else project / p).resolve() for p in raw_roots]
        roots.append(prefix / 'lib' / 'lean')
        for i, root in enumerate(roots):
            if not str(root).startswith(str(project)) and not str(root).startswith(str(prefix)):
                logical[str(root)] = '$SEARCH_ROOT_' + str(i)
        native_roots = list(dict.fromkeys(roots + [prefix / 'lib']))
        present_roots, absent_roots = partition_search_roots(native_roots)
        providers = inventory_providers(present_roots, out)
        write_json(private / 'providers.json', dict(
            inventoryMode='POTENTIAL_PROVIDER_FILES_UNDER_ACTUAL_SEARCH_ROOTS_NOT_ACTUAL_LOAD_TRACER',
            roots=list(map(str, native_roots)), inventoriedRoots=list(map(str, present_roots)),
            absentConfiguredSearchRoots=list(map(str, absent_roots)),
            artifacts=providers, actualLeanBinary=str(lean),
            actualLeanBinarySHA256=sha(lean),
            boundary='Inherited providers, not cleantransitive; native libraries outside inventoried roots remain untraced'))
        # This genuine legacy API fixture is separate from every Cubic result.
        fixture = safe_child(out, 'fixture'); fixture.mkdir()
        shutil.copyfile(package / 'Fixture.lean', fixture / 'Fixture.lean')
        shutil.copyfile(safe_child(package, pins['activeFixtureProbe']), fixture / 'Probe.lean')
        fixture_env = dict(env)
        fixture_env['LEAN_PATH'] = os.pathsep.join(map(str, [fixture] + roots))
        fixture_olean = fixture / 'Fixture.olean'
        native_call(private, '03-fixture-compile', [str(lean), '--threads=1', '--memory=3072', '-o',
                    str(fixture_olean), 'Fixture.lean'], fixture, fixture_env)
        fixture_hash = sha(fixture_olean)
        fixture_env['QBE_EXPECT_FRESH_OLEAN'] = str(fixture_olean)
        fixture_result = native_call(private, '04-fixture-probe', [str(lean), '--threads=1', '--memory=3072',
                                     'Probe.lean'], fixture, fixture_env)
        checked_fixture = validate_fixture((private / '04-fixture-probe.stdout.raw').read_text(encoding='utf-8'),
                                           fixture_result['exitCode'], generated_expected['fixtureGenerated'], audit_module)
        if sha(fixture_olean) != fixture_hash:
            raise ValueError('fixture artifact changed during probe')
        write_json(private / 'fixture-result.json', dict(fixtureOleanSHA256=fixture_hash, diagnostic=checked_fixture))
        fresh = safe_child(out, 'fresh'); fresh.mkdir()
        copies = copy_local_providers(project, fresh)
        write_json(private / 'fresh-provider-copies.json', dict(files=copies))
        driver = safe_child(out, 'driver'); driver.mkdir()
        shutil.copyfile(safe_child(package, pins['activeProbe']), safe_child(driver, 'Probe.lean'))
        for name in ('expected-roots.json', 'validate-output.py', pins['activeValidator'],
                     pins['expectedGeneratedFile'], 'pins.json'):
            shutil.copyfile(safe_child(package, name), safe_child(driver, name))
        env['LEAN_PATH'] = os.pathsep.join(map(str, [fresh] + roots))
        target_rel = 'QuantumBlockEncoding/CubicStatePreparation.lean'
        target = safe_child(project, target_rel)
        output = safe_child(fresh, 'QuantumBlockEncoding/CubicStatePreparation.olean')
        if output.exists():
            raise FileExistsError('fresh target artifact already exists')
        verify_pins(project, pins['projectInputs'])
        native_call(private, '05-target', [str(lean), '--threads=1', '--memory=3072', '-o', str(output), target_rel], project, env)
        verify_pins(project, pins['projectInputs'])
        if not output.is_file():
            raise FileNotFoundError('native target success without fresh olean')
        fresh_outputs = [p for p in output.parent.glob('CubicStatePreparation.*') if p.is_file()]
        fresh_rows = [dict(path=str(p), sha256=sha(p), bytes=p.stat().st_size) for p in fresh_outputs]
        write_json(private / 'target-output.json', dict(artifacts=fresh_rows, targetRawSHA256=sha(target)))
        env['QBE_EXPECT_FRESH_OLEAN'] = str(output)
        result = native_call(private, '06-probe-v5', [str(lean), '--threads=1', '--memory=3072', 'Probe.lean'], driver, env)
        checked = load_validator(driver, versioned=True)(
            json.loads((driver / 'expected-roots.json').read_text(encoding='utf-8')),
            (private / '06-probe-v5.stdout.raw').read_text(encoding='utf-8', errors='strict'), result['exitCode'])
        verify_pins(project, pins['projectInputs'])
        if any(path.exists() for path in absent_roots):
            raise ValueError('RESEAL previously absent search root appeared during diagnostic')
        for row in providers + fresh_rows:
            if sha(Path(row['path'])) != row['sha256']:
                raise ValueError('RESEAL provider/fresh artifact changed during diagnostic')
        for row in copies:
            if sha(Path(row['source'])) != row['sha256'] or sha(Path(row['destination'])) != row['sha256']:
                raise ValueError('RESEAL copied local provider changed')
        write_json(private / 'output-completeness.json', checked)
        status.update(status='FORMAL_RUNTIME_DIAGNOSTIC_COMPLETE_NOT_ACCEPTANCE',
                      explicitRoots=319, explicitPrivateRoots=50,
                      generatedActualFields=checked['generatedActualFieldsCollected'],
                      generatedTrust='ACTUAL_TYPE_VALUE_AXIOMS_COLLECTED_POLICY_UNASSESSED_NOT_TRUST_CLOSURE')
        return_code = 0
    except Exception as error:
        status.update(status='DIAGNOSTIC_FAILED_NOT_MATHEMATICAL_REFUTATION',
                      failureType=type(error).__name__, failure=str(error))
        return_code = 1
    finally:
        write_json(private / 'result.json', status)
        export_public(private, public, logical)
    print(json.dumps(redact_tree(status, logical), ensure_ascii=False))
    return return_code


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        code = run(args.project, Path(__file__).parent)
    except Exception as error:
        # No traceback/local-path leak if output is pre-existing or sanitization fails.
        print(json.dumps(dict(status='WRAPPER_FAILED_CLOSED', failureType=type(error).__name__, **NO_ACCEPT)))
        code = 1
    sys.exit(code)
