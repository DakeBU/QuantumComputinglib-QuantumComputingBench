"""CI-only finite memory callback adapter over the byte-identical C31 v1 runner."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import threading
from contextlib import contextmanager

import resource_gate as gate

NO_ACCEPT = dict(sourceAgreement=None, axiomPolicyPass=None, publicationBinding=None,
                 scientificAcceptance=False, nativeAccepted=False, trustClosure=False)


class PreflightRefused(RuntimeError):
    pass


def rewrite_argv(argv):
    argv = list(map(str, argv))
    if not argv:
        raise ValueError('empty native command')
    memories = [i for i, value in enumerate(argv) if value.startswith('--memory=')]
    threads = [i for i, value in enumerate(argv) if value.startswith('--threads=')]
    if len(memories) > 1 or len(threads) > 1 or '--memory' in argv or '--threads' in argv:
        raise ValueError('ambiguous/unbounded native option form')
    if memories:
        if argv[memories[0]] != '--memory=3072':
            raise ValueError('base budget changed: require explicit successor review')
        argv[memories[0]] = '--memory=5120'
    else:
        argv.append('--memory=5120')
    if threads:
        if argv[threads[0]] != '--threads=1':
            raise ValueError('base thread count changed')
    else:
        argv.append('--threads=1')
    return argv


def load_base(project, profile):
    if profile['basePackage'] != 'tools/primitive_compiler_native_profile_v1':
        raise ValueError('unexpected base package path')
    package = project / profile['basePackage']
    import hashlib
    def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
    if digest(package / 'proposal-bindings.json') != profile['baseManifestSHA256']:
        raise ValueError('base v1 manifest changed')
    manifest = json.loads((package / 'proposal-bindings.json').read_text(encoding='utf-8'))['files']
    if len(manifest) != 14 or manifest != profile['baseFiles']:
        raise ValueError('base 14-file vector changed')
    for name, expected in manifest.items():
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or digest(package / relative) != expected:
            raise ValueError('base package byte drift')
    if digest(package / 'proposal-seal.json') != profile['baseProposalSealSHA256']:
        raise ValueError('base proposal seal changed')
    if digest(package / 'profile.json') != profile['baseProfileSHA256']:
        raise ValueError('base87 raw profile changed')
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(package))
    try:
        if 'validator' in sys.modules and Path(sys.modules['validator'].__file__).resolve() != (package / 'validator.py').resolve():
            raise ValueError('unexpected validator module already loaded')
        spec = importlib.util.spec_from_file_location('c31_immutable_base_runner_ci2', package / 'runner.py')
        base = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(base)
    finally:
        sys.path.pop(0)
        sys.dont_write_bytecode = previous
    return base, package


class BudgetCallback:
    """Only native_call and the one budget-description write are adapted."""
    def __init__(self, api, revalidate, binding, sampler=gate.sample):
        self.api = api
        self.native = api.native_call
        self.write = api.write_json
        self.revalidate = revalidate
        self.binding = binding
        self.sampler = sampler
        self.lock = threading.Lock()

    def write_json(self, path, value):
        if path.name == 'runtime-environment.json' and path.parent.name == 'private':
            if value.get('nativeMemoryMiB') != 3072 or value.get('nativeThreads') != 1:
                raise ValueError('base runtime budget description changed')
            value = dict(value, baseReportedMemoryMiB=3072, nativeMemoryMiB=5120,
                         ciOnlyBudgetAdapter='C31_CI2_FINITE_GATED_5120_MIB',
                         ci2Binding=self.binding)
        return self.write(path, value)

    def __call__(self, private, label, argv, cwd, env, timeout=600):
        if not re.fullmatch('[a-z0-9-]+', label) or not self.lock.acquire(blocking=False):
            raise PreflightRefused('invalid label or concurrent native invocation refused')
        try:
            self.revalidate()
            before = self.sampler()
            pre = self.api.safe_child(private, 'ci2-' + label + '.preflight.json')
            self.write(pre, dict(before, binding=self.binding, wrapperPID=os.getpid(), **NO_ACCEPT))
            try:
                gate.validate_snapshot(before)
                effective = rewrite_argv(argv)
            except Exception as error:
                raise PreflightRefused('NO_CHILD_STARTED: ' + str(error)) from error
            result, failure = None, None
            try:
                result = self.native(private, label, effective, cwd, env, timeout=timeout)
            except Exception as error:
                failure = error
                result = getattr(error, 'result', None)
                actual_result = private / (label + '.result.json')
                if result is None and actual_result.is_file():
                    result = json.loads(actual_result.read_text(encoding='utf-8'))
            after = self.sampler()
            post = self.api.safe_child(private, 'ci2-' + label + '.postflight.json')
            self.write(post, dict(after, binding=self.binding,
                                 childPID=result.get('PID') if isinstance(result, dict) else None,
                                 wrapperPID=os.getpid(), **NO_ACCEPT))
            stderr_file = private / (label + '.stderr.raw')
            stdout_file = private / (label + '.stdout.raw')
            stderr = stderr_file.read_text(encoding='utf-8', errors='replace') if stderr_file.is_file() else ''
            stdout = stdout_file.read_text(encoding='utf-8', errors='replace') if stdout_file.is_file() else ''
            classification = gate.classify(result, stderr, before, after, stdout)
            streams_match = isinstance(result, dict) and all(p.is_file() and self.api.sha(p) == result.get(k)
                for p, k in ((stdout_file, 'stdoutSHA256'), (stderr_file, 'stderrSHA256')))
            receipt = private / (label + '.started.json')
            result_file = private / (label + '.result.json')
            receipts_match = isinstance(result, dict) and receipt.is_file() and result_file.is_file() and \
                json.loads(receipt.read_text(encoding='utf-8')).get('PID') == result.get('PID') and \
                json.loads(result_file.read_text(encoding='utf-8')) == result
            if classification == 'PROCESS_EXIT_ZERO' and not (streams_match and receipts_match):
                classification = 'NATIVE_STREAM_OR_PID_RESULT_RECEIPTS_INCOMPLETE'
            observation = dict(binding=self.binding, requestedArgv=list(map(str, argv)), actualArgv=effective,
                preflightSHA256=self.api.sha(pre), postflightSHA256=self.api.sha(post),
                nativeResult=result, stderrRawSHA256=self.api.sha(stderr_file) if stderr_file.is_file() else None,
                stdoutRawSHA256=self.api.sha(stdout_file) if stdout_file.is_file() else None,
                actualStreamHashesMatch=streams_match, actualPIDResultReceiptsMatch=receipts_match,
                classification=classification, wrapperPID=os.getpid(), observedUTC=gate.utc(),
                exceptionType=type(failure).__name__ if failure else None, **NO_ACCEPT)
            self.write(self.api.safe_child(private, 'ci2-' + label + '.observation.json'), observation)
            self.revalidate()
            # Unknown postflight fields do not grant completeness; a lower measured
            # post-run headroom is recorded and re-gated before the next child.
            gate.validate_snapshot(after, require_pass=False)
            if failure is not None:
                raise failure
            if classification != 'PROCESS_EXIT_ZERO':
                raise RuntimeError('non-success actual process observation: ' + classification)
            return result
        finally:
            self.lock.release()


@contextmanager
def temporary_callbacks(base, api, callback):
    old_load, old_native, old_write = base.load_shared, api.native_call, api.write_json
    api.native_call, api.write_json = callback, callback.write_json
    base.load_shared = lambda _project, _profile: api
    try:
        yield
    finally:
        base.load_shared = old_load
        api.native_call, api.write_json = old_native, old_write


def run(project, package):
    profile_path = package / 'ci2-profile.json'
    profile = json.loads(profile_path.read_text(encoding='utf-8'))
    if profile.get('schema') != 'C31_CI_ONLY_MEMORY_SUCCESSOR_V1' or profile.get('budgetMiB') != 5120 \
            or profile.get('reserveMiB') != 2048 or profile.get('threads') != 1 \
            or profile.get('WindowsHighBudgetForbidden') is not True \
            or profile.get('oldLocalGateChanged') is not False:
        raise ValueError('unsupported finite CI2 profile')
    for field, value in NO_ACCEPT.items():
        if profile.get(field) is not value:
            raise ValueError('forbidden successor acceptance claim')
    previous_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        base, base_package = load_base(project, profile)
        old_load = base.load_shared
        base_profile = json.loads((base_package / 'profile.json').read_text(encoding='utf-8'))
        api = old_load(project, base_profile)
        raw_profile_sha = api.sha(profile_path)
        manifest_path = package / 'ci2-bindings.json'
        manifest_sha = api.sha(manifest_path)
        files = json.loads(manifest_path.read_text(encoding='utf-8'))['files']
        def revalidate():
            if api.sha(profile_path) != raw_profile_sha or api.sha(manifest_path) != manifest_sha:
                raise ValueError('CI2 raw profile/code manifest changed')
            api.verify_pins(package, files)
            api.verify_pins(base_package, profile['baseFiles'])
            if api.sha(base_package / 'proposal-bindings.json') != profile['baseManifestSHA256'] or \
                    api.sha(base_package / 'proposal-seal.json') != profile['baseProposalSealSHA256']:
                raise ValueError('immutable v1 base seal/manifest changed')
            api.verify_pins(project, base_profile['projectInputs'])
            api.verify_pins(project, {base_profile['sharedInstrumentation']['path']:
                                      base_profile['sharedInstrumentation']['sha256']})
        revalidate()
        binding = dict(ci2ProfileSHA256=raw_profile_sha, ci2CodeManifestSHA256=manifest_sha,
                       baseRaw87ProfileSHA256=profile['baseProfileSHA256'],
                       base14FileManifestSHA256=profile['baseManifestSHA256'],
                       candidateMemoryMiB=5120, measuredReserveMiB=2048,
                       priorFailureZIP_SHA256=profile['firstFailureZIP_SHA256'])
        callback = BudgetCallback(api, revalidate, binding)
        with temporary_callbacks(base, api, callback):
            # Base OUT_REL is retained solely to keep the existing always-upload
            # public path unchanged. Its exclusive mkdir still refuses all reuse.
            return base.run(project, base_package)
    finally:
        sys.dont_write_bytecode = previous_bytecode


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        code = run(args.project.resolve(), Path(__file__).parent.resolve())
    except Exception as error:
        print(json.dumps(dict(status='CI2_WRAPPER_FAILED_CLOSED', failureType=type(error).__name__, **NO_ACCEPT)))
        code = 1
    sys.exit(code)
