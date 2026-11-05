"""C31 isolated fresh-cohort diagnostic proposal. No admission/axiom policy."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import sys
import uuid

import validator

OUT_REL = '_out/primitive-compiler-native-profile-v1'


def load_shared(project, profile):
    entry = profile['sharedInstrumentation']
    # Bootstrap path is fixed and read-only; no profile-supplied Python path execution.
    if entry['path'] != 'tools/cubic_c29_diagnostic/runner.py':
        raise ValueError('unexpected instrumentation module')
    path = project / entry['path']
    import hashlib
    if hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
        raise ValueError('shared instrumentation SHA drift')
    spec = importlib.util.spec_from_file_location('c31_reused_public_instrumentation', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render_driver(profile, shared, driver):
    targets = [m['module'] for m in profile['modules']]
    lines = ['import Collector', 'namespace C31Native',
             'def targets : Array Lean.Name := #[' + ', '.join('`' + m for m in targets) + ']',
             'def roots : Array RootSpec := #[']
    for root in profile['roots']:
        module, name, kind = root['module'], root['sourceUserName'], root['sourceKind']
        for ident in (module, name):
            if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.]*', ident):
                raise ValueError('nonliteral profile name')
        lines.append('  { targetModule := `' + module + ', userName := `' + name +
                     ', privateRoot := ' + str(root['sourcePrivate']).lower() +
                     ', sourceKind := ' + json.dumps(kind) + ' },')
    lines += [']', 'end C31Native']
    (driver / 'Profile.lean').write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    probe = ['import ' + m for m in targets] + ['import Profile']
    for option in ('pp.deepTerms', 'pp.proofs', 'pp.explicit', 'pp.universes', 'pp.fullNames',
                   'pp.privateNames', 'pp.funBinderTypes', 'pp.piBinderTypes'):
        probe.append('set_option ' + option + ' true')
    probe += ['set_option pp.notation false', 'set_option pp.maxSteps 2000000',
              'set_option maxRecDepth 10000', 'set_option maxHeartbeats 20000000',
              'run_cmd C31Native.collect C31Native.targets C31Native.roots']
    (driver / 'Probe.lean').write_text('\n'.join(probe) + '\n', encoding='utf-8', newline='\n')
    return dict(profileDriverSHA256=shared.sha(driver / 'Profile.lean'),
                probeSHA256=shared.sha(driver / 'Probe.lean'))


def copy_providers(project, fresh, profile, api):
    rows = []
    targets = {m['module'] for m in profile['modules']}
    for module in profile['providers']:
        if module in targets:
            raise ValueError('target cannot be inherited into fresh cohort')
        relative = module.replace('.', '/')
        for suffix in api.SIDECARS:
            source = api.safe_child(project, '.lake/build/lib/lean/' + relative + suffix)
            if suffix == '.olean' and not source.is_file():
                raise FileNotFoundError('missing inherited project provider ' + module)
            if not source.is_file():
                continue
            destination = api.safe_child(fresh, relative + suffix)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                raise FileExistsError('provider cohort collision')
            before = api.sha(source)
            shutil.copyfile(source, destination)
            if api.sha(source) != before or api.sha(destination) != before:
                raise ValueError('provider changed while copying')
            rows.append(dict(module=module, source=str(source.resolve()),
                             destination=str(destination.resolve()), sha256=before))
    return rows


def recheck_rows(rows, api):
    for row in rows:
        for key in ('source', 'destination', 'path'):
            if key in row and api.sha(Path(row[key])) != row['sha256']:
                raise ValueError('RESEAL source/provider/cohort artifact changed')


def run(project, package):
    project, package = project.resolve(), package.resolve()
    profile = json.loads((package / 'profile.json').read_text(encoding='utf-8'))
    validator.validate_profile(profile)
    api = load_shared(project, profile)
    out = api.safe_child(project, OUT_REL)
    out.mkdir(parents=True, exist_ok=False)
    private = out / 'private'; private.mkdir(mode=0o700)
    public = out / 'public'; public.mkdir()
    logical = {str(project): '$PROJECT', str(package): '$PROFILE_PACKAGE'}
    status = dict(status='NOT_RUN', cleanTransitive=False, actualLoadTrace=False, **validator.NO_ACCEPT)
    code = 1
    try:
        profile_sha = api.sha(package / 'profile.json')
        manifest_sha = api.sha(package / 'proposal-bindings.json')
        manifest = json.loads((package / 'proposal-bindings.json').read_text(encoding='utf-8'))
        api.verify_pins(package, manifest['files'])
        inputs = api.verify_pins(project, profile['projectInputs'])
        api.write_json(private / 'input-bindings.json', dict(
            profileSHA256=profile_sha, packageManifestSHA256=manifest_sha,
            projectInputs=inputs, sourceSealSHA256=profile['sourceSealSHA256'],
            sharedInstrumentation=profile['sharedInstrumentation'], **validator.NO_ACCEPT))
        env = dict(os.environ)
        bootstrap = shutil.which('lean', path=env.get('PATH'))
        if not bootstrap:
            raise FileNotFoundError('lake env lean absent')
        api.native_call(private, '01-help', [bootstrap, '--help'], project, env, timeout=30)
        api.verify_lean_help((private / '01-help.stdout.raw').read_text(encoding='utf-8'))
        api.native_call(private, '02-prefix', [bootstrap, '--print-prefix'], project, env, timeout=30)
        prefix = Path((private / '02-prefix.stdout.raw').read_text(encoding='utf-8').strip()).resolve()
        lean = prefix / 'bin' / ('lean.exe' if os.name == 'nt' else 'lean')
        if not lean.is_file():
            raise FileNotFoundError('actual Lean binary absent')
        lean_sha = api.sha(lean)
        logical[str(prefix)] = '$TOOLCHAIN'
        raw = env.get('LEAN_PATH', '').split(os.pathsep)
        if not raw or any(not p for p in raw):
            raise ValueError('lake env requires explicit nonempty LEAN_PATH')
        original = [(Path(p) if Path(p).is_absolute() else project / p).resolve() for p in raw]
        forbidden = {project, (project / '.lake/build/lib/lean').resolve()}
        external = list(dict.fromkeys([r for r in original if r not in forbidden] + [prefix / 'lib/lean']))
        # Reject alternate project-local fallback roots, except explicit package caches.
        for root in external:
            if root.is_relative_to(project) and not root.is_relative_to(project / '.lake/packages'):
                raise ValueError('unexpected project-local fallback search root')
        native_roots = list(dict.fromkeys(external + [prefix / 'lib']))
        present, absent = api.partition_search_roots(native_roots)
        providers = api.inventory_providers(present, out)
        for i, root in enumerate(native_roots):
            logical.setdefault(str(root), '$SEARCH_ROOT_' + str(i))
        api.write_json(private / 'provider-inventory.json', dict(
            mode='ACTUAL_OS_ARTIFACT_INVENTORY_NOT_LOAD_TRACE',
            actualExternalSearchRoots=list(map(str, external)),
            removedProjectFallbackRoots=list(map(str, forbidden)),
            inventoriedRoots=list(map(str, present)), absentConfiguredRoots=list(map(str, absent)),
            artifacts=providers, leanBinary=str(lean), leanBinarySHA256=lean_sha,
            boundary='Inherited provider artifacts, not clean-transitive; native loads outside inventoried roots untraced',
            **validator.NO_ACCEPT))
        fresh = out / 'cohort'; fresh.mkdir()
        sources = out / 'source'; sources.mkdir()
        driver = out / 'driver'; driver.mkdir()
        copies = copy_providers(project, fresh, profile, api)
        api.write_json(private / 'provider-copies.json', dict(files=copies, **validator.NO_ACCEPT))
        cohort = uuid.uuid4().hex
        env['LEAN_PATH'] = os.pathsep.join(map(str, [fresh, driver] + external))
        env['C31_FRESH_ROOT'] = str(fresh.resolve())
        env['C31_PROFILE_SHA256'] = profile_sha
        env['C31_COHORT_ID'] = cohort
        env.pop('QBE_EXPECT_FRESH_OLEAN', None)
        api.write_json(private / 'runtime-environment.json', dict(
            LEAN_PATH=env['LEAN_PATH'], C31_FRESH_ROOT=env['C31_FRESH_ROOT'],
            profileSHA256=profile_sha, cohortID=cohort, nativeMemoryMiB=3072,
            nativeThreads=1, processTimeoutSeconds=900, **validator.NO_ACCEPT))
        def revalidate_inputs():
            api.verify_pins(project, profile['projectInputs'])
            api.verify_pins(package, manifest['files'])
            api.verify_pins(project, {profile['sharedInstrumentation']['path']:
                                      profile['sharedInstrumentation']['sha256']})
            if api.sha(package / 'profile.json') != profile_sha or api.sha(package / 'proposal-bindings.json') != manifest_sha:
                raise ValueError('raw profile/package manifest changed')
        flags = [str(lean), '--threads=1', '--memory=3072']
        fresh_rows, expected_oleans = [], {}
        compile_receipts = []
        for ordinal, target in enumerate(profile['modules'], 1):
            revalidate_inputs()
            recheck_rows(fresh_rows + copies, api)
            relative = target['module'].replace('.', '/')
            source = api.safe_child(project, relative + '.lean')
            copied_source = api.safe_child(sources, relative + '.lean')
            copied_source.parent.mkdir(parents=True, exist_ok=True)
            if copied_source.exists():
                raise FileExistsError('source cohort collision')
            shutil.copyfile(source, copied_source)
            before = api.sha(source)
            if before != target['rawSHA256'] or api.sha(copied_source) != before:
                raise ValueError('copied target source hash mismatch')
            output = api.safe_child(fresh, relative + '.olean')
            output.parent.mkdir(parents=True, exist_ok=True)
            if any(api.safe_child(fresh, relative + s).exists() for s in api.SIDECARS):
                raise FileExistsError('target artifact inherited or reused')
            result = api.native_call(private, f'1{ordinal}-target', flags +
                ['-o', str(output), relative + '.lean'], sources, env, timeout=900)
            revalidate_inputs()
            if api.sha(copied_source) != before or not output.is_file():
                raise ValueError('target changed or successful exit without output')
            new_rows = [dict(path=str(api.safe_child(fresh, relative + s).resolve()),
                            sha256=api.sha(api.safe_child(fresh, relative + s)))
                        for s in api.SIDECARS if api.safe_child(fresh, relative + s).is_file()]
            fresh_rows += new_rows
            expected_oleans[target['module']] = str(output.resolve())
            compile_receipts.append(dict(module=target['module'], sourceSHA256Before=before,
                sourceSHA256After=api.sha(source), copiedSourceSHA256=api.sha(copied_source),
                cohortID=cohort, nativeResult=result, artifacts=new_rows))
        api.write_json(private / 'fresh-target-cohort.json', dict(
            compileOrder=[m['module'] for m in profile['modules']],
            cohortID=cohort, targets=compile_receipts, **validator.NO_ACCEPT))
        shutil.copyfile(package / 'Collector.lean', driver / 'Collector.lean')
        drivers = render_driver(profile, api, driver)
        for name in ('Profile.lean', 'Probe.lean'):
            if api.sha(driver / name) != api.sha(package / 'pending-drivers' / name):
                raise ValueError('rendered driver differs from frozen own-profile vector')
        drivers['collectorSHA256'] = api.sha(driver / 'Collector.lean')
        for ordinal, name in enumerate(('Collector', 'Profile'), 1):
            api.native_call(private, f'2{ordinal}-driver', flags +
                ['-o', str(driver / (name + '.olean')), name + '.lean'], driver, env, timeout=900)
        driver_rows = [dict(path=str(p.resolve()), sha256=api.sha(p)) for p in sorted(driver.iterdir())
                       if p.is_file()]
        api.write_json(private / 'driver-bindings.json', dict(
            generatedDrivers=drivers, artifacts=driver_rows, **validator.NO_ACCEPT))
        result = api.native_call(private, '30-observe', flags + ['Probe.lean'], driver, env, timeout=900)
        checked = validator.validate(profile, (private / '30-observe.stdout.raw').read_text(
            encoding='utf-8', errors='strict'), result['exitCode'], timed_out=result['timedOut'],
            profile_sha=profile_sha, cohort_id=cohort, expected_oleans=expected_oleans)
        revalidate_inputs()
        if api.sha(lean) != lean_sha or any(p.exists() for p in absent):
            raise ValueError('binary or absent-root state changed')
        recheck_rows(providers + copies + fresh_rows + driver_rows, api)
        api.write_json(private / 'completeness.json', checked)
        status.update(status=checked['status'], roots=87, privateRoots=8,
                      generated=checked['generated'], cohortID=cohort)
        code = 0
    except Exception as error:
        status.update(status='DIAGNOSTIC_FAILED_NOT_MATHEMATICAL_REFUTATION',
                      failureType=type(error).__name__, failure=str(error))
    finally:
        api.write_json(private / 'result.json', status)
        # Existing redaction exports raw-derived text/JSON only, not sources/oleans/providers.
        api.export_public(private, public, logical)
    print(json.dumps(api.redact_tree(status, logical)))
    return code


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        result = run(args.project, Path(__file__).parent)
    except Exception as error:
        print(json.dumps(dict(status='WRAPPER_FAILED_CLOSED', failureType=type(error).__name__,
                              **validator.NO_ACCEPT)))
        result = 1
    sys.exit(result)
