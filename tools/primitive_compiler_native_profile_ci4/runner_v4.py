"""Versioned self-only namespace adapter over unchanged CI3/CI2/V1 runtime code."""
import argparse
from contextlib import contextmanager
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import resource_gate_v4 as gate4

NO_ACCEPT=dict(sourceAgreement=None,axiomPolicyPass=None,publicationBinding=None,
    scientificAcceptance=False,nativeAccepted=False,trustClosure=False)


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text(encoding='utf-8'))


def pins(root,files):
    if not isinstance(files,dict) or not files: raise ValueError('empty pin vector')
    for name,value in files.items():
        p=Path(name)
        if p.is_absolute() or '..' in p.parts or sha(root/p)!=value: raise ValueError('byte pin drift: '+name)


def load_ci3(project,profile):
    if profile['priorPackage']!='tools/primitive_compiler_native_profile_ci3': raise ValueError('unexpected prior package')
    package=project/profile['priorPackage']
    pins(package,profile['priorFiles'])
    if sha(package/'ci3-bindings.json')!=profile['priorManifestSHA256'] or \
        sha(package/'ci3-seal.json')!=profile['priorSealSHA256'] or \
        read(package/'ci3-bindings.json')['files']!=profile['priorFiles']:
        raise ValueError('old CI3 manifest/seal drift')
    old=sys.dont_write_bytecode; sys.dont_write_bytecode=True; sys.path.insert(0,str(package))
    try:
        if 'resource_gate_v3' in sys.modules and Path(sys.modules['resource_gate_v3'].__file__).resolve()!= \
            (package/'resource_gate_v3.py').resolve(): raise ValueError('unexpected old resource module')
        spec=importlib.util.spec_from_file_location('c31_immutable_ci3_runner_ci4',package/'runner_v3.py')
        module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    finally:
        sys.path.pop(0); sys.dont_write_bytecode=old
    return module,package


@contextmanager
def self_callbacks(prior,revalidate,binding):
    old_gate,old_root=prior.gate3,prior.root_callbacks
    def root_factory(ci2,prior_revalidate,prior_binding,sampler=None):
        def both(): revalidate(); prior_revalidate()
        return old_root(ci2,both,dict(prior_binding,ci4Binding=binding),
            sampler=gate4.sample if sampler is None else sampler)
    prior.gate3,prior.root_callbacks=gate4,root_factory
    try: yield
    finally: prior.gate3,prior.root_callbacks=old_gate,old_root


def run(project,package):
    pp,mp=package/'ci4-profile.json',package/'ci4-bindings.json'
    profile,manifest=read(pp),read(mp)
    if profile.get('schema')!='C31_CI4_SELF_ONLY_NAMESPACE_PROFILE_V1' or \
        profile.get('namespacePolicy')!='SELF_ONLY_RESERVED_INIT_V1' or \
        profile.get('budgetMiB')!=5120 or profile.get('reserveMiB')!=2048 or profile.get('threads')!=1 or \
        profile.get('PID1ReadRequested') is not False or profile.get('WindowsHighBudgetForbidden') is not True or \
        profile.get('oldLocalGateChanged') is not False or profile.get('requiredInitCgroupNamespaceInode')!=0xEFFFFFFB:
        raise ValueError('unsupported CI4 contract')
    if any(k not in profile or profile[k] is not v for k,v in NO_ACCEPT.items()): raise ValueError('acceptance claim refused')
    ps,ms=sha(pp),sha(mp); pins(package,manifest['files'])
    prior,prior_package=load_ci3(project,profile)
    def revalidate():
        if sha(pp)!=ps or sha(mp)!=ms: raise ValueError('CI4 raw profile/manifest drift')
        pins(package,manifest['files']); pins(prior_package,profile['priorFiles'])
        if sha(prior_package/'ci3-bindings.json')!=profile['priorManifestSHA256'] or \
            sha(prior_package/'ci3-seal.json')!=profile['priorSealSHA256']: raise ValueError('immutable CI3 boundary drift')
    revalidate()
    binding=dict(profileSHA256=ps,manifestSHA256=ms,namespacePolicy='SELF_ONLY_RESERVED_INIT_V1',
        priorActualZIP_SHA256=profile['priorFailureZIP_SHA256'],PID1ReadRequested=False)
    old=sys.dont_write_bytecode; sys.dont_write_bytecode=True
    try:
        with self_callbacks(prior,revalidate,binding): return prior.run(project,prior_package)
    finally: sys.dont_write_bytecode=old


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--project',type=Path,default=Path.cwd())
    args=parser.parse_args()
    try: code=run(args.project.resolve(),Path(__file__).parent.resolve())
    except Exception as error:
        print(json.dumps(dict(status='CI4_WRAPPER_FAILED_CLOSED',failureType=type(error).__name__,**NO_ACCEPT))); code=1
    sys.exit(code)
