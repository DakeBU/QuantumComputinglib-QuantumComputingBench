"""Small executing-file guard successor; immutable kernel v1 remains unchanged."""
import argparse
from contextlib import contextmanager
from datetime import datetime,timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

NO_ACCEPT=dict(sourceAgreement=None,axiomPolicyPass=None,publicationBinding=None,
    scientificAcceptance=False,nativeAccepted=False,trustClosure=False)
MODULE_FILES={'runtime':'runtime.py','compare':'compare.py','proof_patch':'proof_patch.py'}


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def verify(root,files):
    if not files: raise ValueError('empty pins')
    for name,value in files.items():
        p=Path(name)
        if p.is_absolute() or '..' in p.parts or sha(root/p)!=value: raise ValueError('byte pin drift: '+name)


def module_file(module,expected,expected_sha):
    actual=getattr(module,'__file__',None)
    if type(actual) is not str or Path(actual).resolve()!=expected.resolve():
        raise ValueError('actual imported module __file__ mismatch')
    if sha(Path(actual))!=expected_sha: raise ValueError('actual imported module source SHA mismatch')
    return dict(actualModuleName=getattr(module,'__name__',None),actualFile=str(Path(actual).resolve()),
        expectedLogicalFile='$KERNEL_V1_PACKAGE/'+expected.name,sourceSHA256=expected_sha)


def load_code(base,files):
    verify(base,files)
    for name in ('compare','proof_patch'):
        if name in sys.modules: module_file(sys.modules[name],base/MODULE_FILES[name],files[MODULE_FILES[name]])
    old=sys.dont_write_bytecode; sys.dont_write_bytecode=True; sys.path.insert(0,str(base))
    try:
        spec=importlib.util.spec_from_file_location('c31_kernel_v1_guarded_runtime',base/'runtime.py')
        module=importlib.util.module_from_spec(spec); sys.modules[spec.name]=module
        try: spec.loader.exec_module(module)
        except BaseException:
            if sys.modules.get(spec.name) is module: sys.modules.pop(spec.name)
            raise
    finally: sys.path.pop(0); sys.dont_write_bytecode=old
    for name,obj in [('runtime',module),('compare',module.compare),('proof_patch',module.proof_patch)]:
        module_file(obj,base/MODULE_FILES[name],files[MODULE_FILES[name]])
    return module


def execution_record(package,base,files,runtime,entry_file,argv0,main_file,entry_sha):
    expected=(package/'entry.py').resolve()
    for observed in (entry_file,argv0,main_file):
        if type(observed) is not str or Path(observed).resolve()!=expected:
            raise ValueError('actual executing entry/main/argv0 mismatch')
    if sha(expected)!=entry_sha: raise ValueError('actual entry source SHA mismatch')
    modules=[module_file(obj,base/MODULE_FILES[name],files[MODULE_FILES[name]]) for name,obj in
        [('runtime',runtime),('compare',runtime.compare),('proof_patch',runtime.proof_patch)]]
    if sys.modules.get(runtime.__name__) is not runtime or runtime.compare is not sys.modules.get('compare') or runtime.proof_patch is not sys.modules.get('proof_patch'):
        raise ValueError('runtime import object identity mismatch')
    return dict(kind='ACTUAL_EXECUTING_ENTRY_AND_IMPORTED_SOURCE_FILE_BINDINGS',
        observedUTC=datetime.now(timezone.utc).isoformat(),entry=dict(actualFile=str(expected),
            actualArgv0Resolved=str(Path(argv0).resolve()),actualMainModuleFile=str(Path(main_file).resolve()),
            sourceSHA256=entry_sha,expectedLogicalFile='$KERNEL_V2_GUARD_PACKAGE/entry.py'),modules=modules,
        sourceFileObservationOnly=True,OSAttestation=False,codeObjectAttestation=False,
        boundary='Observed __file__/main/argv0 identity and current on-disk source hashes, not OS/kernel attestation or proof against malicious live module mutation',
        **NO_ACCEPT)


@contextmanager
def guarded_hooks(runtime,guard):
    original_verify,original_write=runtime.verify,runtime.write
    recorded=[]
    def checked_verify(root,files):
        guard(); return original_verify(root,files)
    def checked_write(path,value):
        observed=guard()
        if path.name=='candidate-preparation-resource.json' and path.parent.name=='private':
            if recorded: raise ValueError('duplicate executing-entry startup receipt')
            original_write(path.parent/'executing-code-bindings.json',observed); recorded.append(True)
        return original_write(path,value)
    runtime.verify,runtime.write=checked_verify,checked_write
    try: yield
    finally: runtime.verify,runtime.write=original_verify,original_write


def run(project,package):
    pp,mp=package/'profile.json',package/'bindings.json'; profile,manifest=read(pp),read(mp)
    if profile.get('schema')!='C31_KERNEL_EXECUTING_FILE_GUARD_V2' or profile.get('basePackage')!='tools/c31_kernel_proof_v1' or \
        profile.get('sourceBlindReviewExclusionNotConfidential') is not True or \
        profile.get('publicRepoCandidateTransportAllowed') is not True or \
        any(k not in profile or profile[k] is not v for k,v in NO_ACCEPT.items()): raise ValueError('guard/transport contract')
    verify(package,manifest['files']); ps,ms=sha(pp),sha(mp)
    if profile['baseFiles'].get('bindings.json')!=profile['baseManifestSHA256'] or \
        profile['baseFiles'].get('seal.json')!=profile['baseSealSHA256']: raise ValueError('base manifest/seal profile disagreement')
    base=project/profile['basePackage']; runtime=load_code(base,profile['baseFiles'])
    def guard():
        verify(package,manifest['files']); verify(base,profile['baseFiles'])
        if sha(pp)!=ps or sha(mp)!=ms: raise ValueError('v2 profile/manifest drift')
        result=execution_record(package,base,profile['baseFiles'],runtime,__file__,sys.argv[0],
            getattr(sys.modules.get('__main__'),'__file__',None),manifest['files']['entry.py'])
        result.update(guardProfileSHA256=ps,guardManifestSHA256=ms,
            immutableKernelV1ManifestSHA256=profile['baseManifestSHA256'],
            immutableKernelV1SealSHA256=profile['baseSealSHA256'])
        return result
    guard()
    with guarded_hooks(runtime,guard): result=runtime.run(project,base)
    guard(); return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--project',type=Path,default=Path.cwd())
    args=parser.parse_args()
    try: result=run(args.project.resolve(),Path(__file__).parent.resolve())
    except Exception as error:
        print(json.dumps(dict(status='KERNEL_V2_EXECUTING_FILE_GUARD_FAILED_CLOSED',failureType=type(error).__name__,**NO_ACCEPT))); result=1
    sys.exit(result)
