"""Thin root-API sampler adapter; immutable CI2/V1 process and formal collectors reused."""
import argparse
from contextlib import contextmanager
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import resource_gate_v3 as gate3

NO_ACCEPT = dict(sourceAgreement=None, axiomPolicyPass=None, publicationBinding=None,
                 scientificAcceptance=False, nativeAccepted=False, trustClosure=False)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def pins(root, files):
    if not isinstance(files, dict) or not files:
        raise ValueError('empty pin vector')
    for name, expected in files.items():
        p = Path(name)
        if p.is_absolute() or '..' in p.parts or sha(root / p) != expected:
            raise ValueError('runtime byte pin drift: ' + name)


def load_ci2(project, profile):
    if profile['priorPackage'] != 'tools/primitive_compiler_native_profile_ci2':
        raise ValueError('unexpected immutable prior package')
    package = project / profile['priorPackage']
    pins(package, profile['priorFiles'])
    if sha(package / 'ci2-bindings.json') != profile['priorManifestSHA256'] or \
            sha(package / 'ci2-seal.json') != profile['priorSealSHA256'] or \
            read(package / 'ci2-bindings.json')['files'] != profile['priorFiles']:
        raise ValueError('immutable CI2 package manifest/seal drift')
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(package))
    try:
        if 'resource_gate' in sys.modules and Path(sys.modules['resource_gate'].__file__).resolve() != \
                (package / 'resource_gate.py').resolve():
            raise ValueError('unexpected old resource gate module')
        spec = importlib.util.spec_from_file_location('c31_immutable_ci2_runner_ci3', package / 'runner_v2.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
        sys.dont_write_bytecode = old
    gate3.bind_common(module.gate)
    return module, package


@contextmanager
def root_callbacks(prior, revalidate, binding, sampler=None):
    old_gate, old_callback = prior.gate, prior.BudgetCallback
    def factory(api, prior_revalidate, prior_binding):
        def both():
            revalidate()
            prior_revalidate()
        return old_callback(api, both, dict(prior_binding, ci3Binding=binding),
                            sampler=gate3.sample if sampler is None else sampler)
    prior.gate, prior.BudgetCallback = gate3, factory
    try:
        yield
    finally:
        prior.gate, prior.BudgetCallback = old_gate, old_callback


def run(project, package):
    profile_path, manifest_path = package / 'ci3-profile.json', package / 'ci3-bindings.json'
    profile, manifest = read(profile_path), read(manifest_path)
    if profile.get('schema') != 'C31_CI3_ROOT_API_CORRECTION_V1' or profile.get('budgetMiB') != 5120 \
            or profile.get('reserveMiB') != 2048 or profile.get('threads') != 1 \
            or profile.get('WindowsHighBudgetForbidden') is not True \
            or profile.get('oldLocalGateChanged') is not False \
            or profile.get('requiredInitCgroupNamespaceInode') != gate3.INIT_CGROUP_INODE:
        raise ValueError('unsupported CI3 contract')
    if any(k not in profile or profile[k] is not v for k,v in NO_ACCEPT.items()):
        raise ValueError('forbidden acceptance claim')
    profile_sha, manifest_sha = sha(profile_path), sha(manifest_path)
    pins(package, manifest['files'])
    prior, prior_package = load_ci2(project, profile)
    def revalidate():
        if sha(profile_path) != profile_sha or sha(manifest_path) != manifest_sha:
            raise ValueError('CI3 raw profile/manifest changed')
        pins(package, manifest['files'])
        pins(prior_package, profile['priorFiles'])
        if sha(prior_package / 'ci2-bindings.json') != profile['priorManifestSHA256'] or \
                sha(prior_package / 'ci2-seal.json') != profile['priorSealSHA256']:
            raise ValueError('CI2 boundary drift')
    revalidate()
    binding = dict(profileSHA256=profile_sha, manifestSHA256=manifest_sha,
        rootAPIContract=gate3.ROOT_NA, namespaceImplementationFingerprint=gate3.INIT_CGROUP_INODE,
        actualCI2FailureZIP_SHA256=profile['priorFailureZIP_SHA256'], mathematicalAcceptance=False)
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        with root_callbacks(prior, revalidate, binding):
            return prior.run(project, prior_package)
    finally:
        sys.dont_write_bytecode = old


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        code = run(args.project.resolve(), Path(__file__).parent.resolve())
    except Exception as error:
        print(json.dumps(dict(status='CI3_WRAPPER_FAILED_CLOSED', failureType=type(error).__name__, **NO_ACCEPT)))
        code = 1
    sys.exit(code)
