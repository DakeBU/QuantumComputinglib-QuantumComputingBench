"""Finite CI-only proof-token successor using immutable C31 runtime/collector APIs."""
import argparse
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import time

import compare
import proof_patch

NO_ACCEPT=dict(sourceAgreement=None,axiomPolicyPass=None,publicationBinding=None,
    scientificAcceptance=False,nativeAccepted=False,trustClosure=False)
OUT='_out/c31-kernel-proof-v1'


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def write(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as out: json.dump(value,out,indent=2,ensure_ascii=False); out.write('\n')


def verify(root,files):
    if not files: raise ValueError('empty pins')
    for name,expected in files.items():
        rel=Path(name)
        if rel.is_absolute() or '..' in rel.parts or sha(root/rel)!=expected: raise ValueError('pin drift: '+name)


def load_runtime(project,config):
    for path,files in config['runtimePackages'].items(): verify(project/path,files)
    package=project/'tools/primitive_compiler_native_profile_ci4'
    old=sys.dont_write_bytecode; sys.dont_write_bytecode=True; sys.path.insert(0,str(package))
    try:
        if 'resource_gate_v4' in sys.modules and Path(sys.modules['resource_gate_v4'].__file__).resolve()!=(package/'resource_gate_v4.py').resolve():
            raise ValueError('unexpected resource gate module')
        spec=importlib.util.spec_from_file_location('c31_kernel_ci4_api',package/'runner_v4.py')
        ci4=importlib.util.module_from_spec(spec); spec.loader.exec_module(ci4)
        ci3,p3=ci4.load_ci3(project,read(package/'ci4-profile.json'))
        ci2,p2=ci3.load_ci2(project,read(p3/'ci3-profile.json'))
        base,p1=ci2.load_base(project,read(p2/'ci2-profile.json'))
        original=read(p1/'profile.json'); api=base.load_shared(project,original)
        ci4.gate4.bind_common(ci2.gate)
    finally: sys.path.pop(0); sys.dont_write_bytecode=old
    return ci4,ci2,base,p1,original,api


class Deadline:
    def __init__(self,seconds=2100,clock=time.monotonic):
        if seconds!=2100: raise ValueError('whole budget must remain 35 minutes')
        self.clock=clock; self.end=clock()+seconds
    def remaining(self):
        value=self.end-self.clock()
        if value<=0: raise RuntimeError('WHOLE_35_MINUTE_BUDGET_EXHAUSTED')
        return value
    def native(self,original):
        def bounded(private,label,argv,cwd,env,timeout=600):
            return original(private,label,argv,cwd,env,timeout=min(timeout,self.remaining()))
        return bounded


def prepare(project,package,work,run_package,derived,base,api):
    work.mkdir(); run_package.mkdir()
    originals=read(package/'original-profile.json')
    expected,sites=proof_patch.candidate((project/proof_patch.RELATIVE).read_bytes())
    candidate=package/'candidate'/proof_patch.RELATIVE
    if candidate.read_bytes()!=expected: raise ValueError('candidate is not exact token successor')
    proof_patch.validate_derivation(originals,derived,sha(candidate))
    inputs=[]
    for relative,wanted in derived['projectInputs'].items():
        source=candidate if relative==proof_patch.RELATIVE else api.safe_child(project,relative)
        destination=api.safe_child(work,relative); destination.parent.mkdir(parents=True,exist_ok=True)
        before=sha(source); shutil.copyfile(source,destination)
        if before!=wanted or sha(source)!=before or sha(destination)!=wanted: raise ValueError('shadow source copy drift')
        inputs.append(dict(relativePath=relative,sha256=wanted,sourceSHA256Before=before,sourceSHA256After=sha(source)))
    provider_seed=api.safe_child(work,'.lake/build/lib/lean'); provider_seed.mkdir(parents=True)
    provider_rows=base.copy_providers(project,provider_seed,derived,api)
    # Only immutable collector/pending driver files are copied; the unchanged
    # base run orchestrator is loaded from its original pinned location.
    source_package=project/'tools/primitive_compiler_native_profile_v1'
    for relative in ('Collector.lean','pending-drivers/Profile.lean','pending-drivers/Probe.lean'):
        dest=api.safe_child(run_package,relative); dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source_package/relative,dest)
        if sha(dest)!=sha(source_package/relative): raise ValueError('immutable collector/driver copy drift')
    write(run_package/'profile.json',derived)
    files={p.relative_to(run_package).as_posix():sha(p) for p in run_package.rglob('*') if p.is_file()}
    write(run_package/'proposal-bindings.json',dict(files=files,
        provenance='NEW_RUNTIME_INPUT_VIEW_NOT_ORIGINAL_V1_14_FILE_SEAL',**NO_ACCEPT))
    return inputs,provider_rows,files


def external_environment(project,work,environment):
    original=environment.get('LEAN_PATH','').split(os.pathsep)
    if not original or any(not p for p in original): raise ValueError('requires actual lake env nonempty LEAN_PATH')
    roots=[(Path(p) if Path(p).is_absolute() else project/p).resolve() for p in original]
    forbidden={project.resolve(),(project/'.lake/build/lib/lean').resolve()}
    external=[p for p in roots if p not in forbidden]
    for p in external:
        if p.is_relative_to(project) and not p.is_relative_to(project/'.lake/packages'):
            raise ValueError('unexpected original-project fallback')
    env=dict(environment); env['LEAN_PATH']=os.pathsep.join(map(str,[work/'.lake/build/lib/lean']+external))
    return env


@contextmanager
def reused_callbacks(base,ci2,gate,api,callback,env):
    old_gate,old_out=ci2.gate,base.OUT_REL
    old_environment=dict(os.environ)
    ci2.gate=gate
    try:
        os.environ.clear(); os.environ.update(env)
        with ci2.temporary_callbacks(base,api,callback): yield
    finally:
        ci2.gate,base.OUT_REL=old_gate,old_out
        os.environ.clear(); os.environ.update(old_environment)


def run(project,package):
    deadline=Deadline(); config=read(package/'kernel-profile.json'); manifest=read(package/'bindings.json')
    if config.get('schema')!='C31_EXACT_PROOF_KERNEL_SUCCESSOR_V1' or config.get('wholeSeconds')!=2100 or \
        config.get('budgetMiB')!=5120 or config.get('reserveMiB')!=2048 or config.get('threads')!=1 or \
        config.get('baselineCandidateGeneratedCount') is not None:
        raise ValueError('successor profile contract')
    if any(k not in config or config[k] is not v for k,v in NO_ACCEPT.items()): raise ValueError('acceptance claim refused')
    verify(package,manifest['files']); config_sha=sha(package/'kernel-profile.json'); manifest_sha=sha(package/'bindings.json')
    ci4,ci2,base,p1,original,api=load_runtime(project,config)
    if original!=read(package/'original-profile.json'): raise ValueError('immutable raw87 profile drift')
    derived=read(package/'profile.json'); candidate=package/'candidate'/proof_patch.RELATIVE
    if sha(package/'original-profile.json')!=config['originalProfileSHA256'] or \
        sha(package/'profile.json')!=config['candidateProfileSHA256'] or sha(candidate)!=config['candidateTargetSHA256'] or \
        sha(package/'baseline.json')!=config['baselineSHA256'] or config['originalTargetSHA256']!=proof_patch.ORIGINAL_SHA:
        raise ValueError('exact source/profile/baseline binding disagreement')
    proof_patch.validate_derivation(original,derived,sha(candidate))
    ci4.gate4.context_check(ci4.gate4.actual_context())
    out=api.safe_child(project,OUT); out.mkdir(parents=True,exist_ok=False)
    private=out/'private'; public=out/'public'; private.mkdir(mode=0o700); public.mkdir()
    work=out/'workspace'; run_package=out/'runtime-input-view'
    status=dict(status='KERNEL_SUCCESSOR_NOT_RUN',**NO_ACCEPT); code=1; seed=[]; run_files={}
    logical={str(project):'$PROJECT',str(package):'$KERNEL_PACKAGE',str(work):'$CANDIDATE_WORKSPACE',str(out):'$KERNEL_RUN'}
    def revalidate():
        deadline.remaining(); verify(package,manifest['files'])
        if sha(package/'kernel-profile.json')!=config_sha or sha(package/'bindings.json')!=manifest_sha:
            raise ValueError('successor raw profile/manifest changed')
        for path,files in config['runtimePackages'].items(): verify(project/path,files)
        api.verify_pins(project,original['projectInputs'])
        api.verify_pins(project,{original['sharedInstrumentation']['path']:original['sharedInstrumentation']['sha256']})
        if work.exists(): api.verify_pins(work,derived['projectInputs'])
        if run_files: verify(run_package,run_files)
        base.recheck_rows(seed,api)
    try:
        revalidate()
        initial=ci4.gate4.sample(); write(private/'candidate-preparation-resource.json',dict(initial,**NO_ACCEPT))
        ci4.gate4.validate_snapshot(initial)
        inputs,seed,run_files=prepare(project,package,work,run_package,derived,base,api)
        write(private/'candidate-input-bindings.json',dict(originalRaw87ProfileSHA256=sha(package/'original-profile.json'),
            candidateRaw87ProfileSHA256=sha(package/'profile.json'),derivedOnlyTargetSHAChanges=True,
            inputCopies=inputs,providerSeedCopies=seed,wholeBudgetSeconds=2100,**NO_ACCEPT))
        callback=ci2.BudgetCallback(api,revalidate,dict(kernelProfileSHA256=config_sha,
            packageManifestSHA256=manifest_sha,sourceProofTokenSuccessor=True,
            resourceContract='CI4_SELF_ONLY_5120_PLUS_2048_THREADS1',wholeSeconds=2100),sampler=ci4.gate4.sample)
        callback.native=deadline.native(callback.native)
        env=external_environment(project,work,dict(os.environ))
        with reused_callbacks(base,ci2,ci4.gate4,api,callback,env): code=base.run(work,run_package)
        revalidate()
        if code==0:
            inner=work/base.OUT_REL/'private'
            records=base.validator.parse((inner/'30-observe.stdout.raw').read_text(encoding='utf-8'))
            result=compare.compare(read(package/'baseline.json'),records)
            write(private/'whole-owned-comparison.json',result)
            if result['issues']: raise ValueError('complete comparison requires review: '+str(len(result['issues'])))
            status.update(status=result['status'],roots=87,generated=result['candidateGeneratedObserved'],owned=result['newOwned'])
        else: status.update(status='CANDIDATE_NATIVE_OR_STREAM_FAILURE_NOT_MATHEMATICAL_REFUTATION')
    except Exception as error:
        code=1; status.update(status='KERNEL_SUCCESSOR_FAILED_CLOSED_NOT_REFUTATION',failureType=type(error).__name__,failure=str(error))
    finally:
        inner=work/base.OUT_REL/'private'
        if inner.is_dir():
            for source in sorted(inner.iterdir()):
                if source.is_file() and source.suffix in ('.json','.raw'):
                    dest=api.safe_child(private,source.name)
                    if dest.exists(): raise ValueError('raw receipt output collision')
                    before=sha(source); shutil.copyfile(source,dest)
                    if sha(source)!=before or sha(dest)!=before: raise ValueError('raw receipt export copy drift')
        write(private/'kernel-successor-result.json',dict(status,wholeRemainingSeconds=max(0,deadline.end-deadline.clock())))
        api.export_public(private,public,logical)
    print(json.dumps(api.redact_tree(status,logical))); return code


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--project',type=Path,default=Path.cwd())
    args=parser.parse_args()
    try: result=run(args.project.resolve(),Path(__file__).parent.resolve())
    except Exception as error:
        print(json.dumps(dict(status='KERNEL_WRAPPER_FAILED_CLOSED',failureType=type(error).__name__,**NO_ACCEPT))); result=1
    sys.exit(result)
