"""Opt-in joint fresh CSP -> C31 diagnostic. No local/admission authority."""
import argparse
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import zipfile
sys.dont_write_bytecode=True
import joint_compare as JC

sys.dont_write_bytecode=True
OUT='_out/c29-c31-joint-kernel-v1'
CSP='QuantumBlockEncoding/CubicStatePreparation.lean'
CUBIC='QuantumBlockEncoding/CubicAmplitudePrimitive.lean'
OLD_CSP='d125f8c239bca1c15e6e4fa6e788df6dd8984394630cb2dcc9be8946c4cbcb55'
NEW_CSP='6ee53311b5d6e18c46afb3e068341689acb86f1bdbc425e774705e81c9142f44'
NEW_CUBIC='952e2b359796ef695a1b1c1a376d40a80affbc679f503f94227ea0c775a6cd48'

def sha(path): return JC.sha(path.read_bytes())
def read(path): return JC.parse(path.read_bytes())
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    JC.require(Path(module.__file__).resolve()==path.resolve(),'actual loaded file path')
    return module
def archive(path,expected):
    JC.require(sha(path)==expected,'archive raw SHA')
    with zipfile.ZipFile(path) as z:
        names=z.namelist(); JC.require(len(names)==len(set(names)),'duplicate archive name')
        JC.require(all(not Path(n).is_absolute() and '..' not in Path(n).parts and '\\' not in n for n in names),'archive path escape')
        return {n:z.read(n) for n in names}
def write_bytes(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f: f.write(data)


def verify_csp_delta(original,candidate):
    JC.require(JC.sha(original)==OLD_CSP and JC.sha(candidate)==NEW_CSP,'fixed CSP source bytes')
    lines=original.splitlines(keepends=True); locations=(252,372,437,441,771,775,779,2465,2535)
    JC.require(original.count(b'native_decide')==9,'CSP nine tokens')
    for line in locations:
        JC.require(lines[line-1].count(b'native_decide')==1,'CSP exact proof site')
        lines[line-1]=lines[line-1].replace(b'native_decide',b'exact Rat.sub_self' if line==2465 else b'decide +kernel')
    JC.require(b''.join(lines)==candidate,'CSP changed beyond nine proof tokens')
    return dict(proofTokenEdits=9,allOtherBytesIdentical=True,ordinaryDataDefinitionsUnchanged=True)


def reject_target_cache(roots,modules,api):
    for root in roots:
        for module in modules:
            relative=module.replace('.','/')
            for suffix in api.SIDECARS:
                JC.require(not api.safe_child(root,relative+suffix).exists(),'four-target cache/fallback present: '+module)


def joint_bindings(csp,three,full,two):
    JC.require(three['cohortID']==csp['cohortID'] and all(r['cohortID']==csp['cohortID'] for r in three['targets']),'CSP/consumer cohort identity')
    root=Path(three['targets'][0]['artifacts'][0]['path']).parent.parent
    JC.require(Path(csp['freshOlean'])==root/CSP.replace('.lean','.olean'),'CSP/consumer actual cohort root')
    JC.require(full[JC.CSP_TAGS[0]][0]['actualResolvedOleanPath']==csp['freshOlean'] and
        two[JC.TWO_TAGS[0]][0]['actualResolvedOleanPath']==csp['freshOlean'],'CSP probes loaded different artifact')


def setup(project,package):
    profile=read(package/'profile.json'); derived=read(package/'c31-profile.json')
    JC.require(profile['schema']=='C29_C31_JOINT_FRESH_KERNEL_V1' and
        (profile['budgetMiB'],profile['reserveMiB'],profile['threads'],profile['wholeSeconds'])==(5120,2048,1,2100) and
        profile['expectedJointGeneratedCount'] is None,'joint finite profile')
    JC.require(all(k in profile and profile[k] is v for k,v in JC.FLAGS.items()),'joint acceptance contract')
    # Only public technical APIs are executed, from exact pinned originals.
    for name,wanted in dict(profile['externalFiles'],**profile['archives']).items():
        JC.require(sha(project/name)==wanted,'external code/archive pin: '+name)
    guard_path=project/'tools/c31_kernel_proof_v3/entry.py'; guard=load('joint_reused_guard_v3',guard_path)
    base_package=project/'tools/c31_kernel_proof_v1'
    guard_profile=read(project/'tools/c31_kernel_proof_v3/profile.json')
    runtime=guard.load_code(base_package,guard_profile['baseFiles'])
    ci4,ci2,base,p1,original,api=runtime.load_runtime(project,read(base_package/'kernel-profile.json'))
    api.verify_pins(project,profile['originalProjectInputs'])
    wanted=read(base_package/'profile.json'); wanted['projectInputs'][CSP]=NEW_CSP
    wanted['providers'].remove(JC.CSP)
    JC.require(derived==wanted and sha(package/'c31-profile.json')==profile['derivedC31ProfileSHA256'],'exact joint C31 profile derivation')
    JC.require(len(derived['projectInputs'])==31 and len(derived['roots'])==87 and len(derived['providers'])==24,'joint vector dimensions')
    JC.require(profile['compileOrder']==[JC.CSP]+[r['module'] for r in derived['modules']],'CSP-first compile order')
    data=archive(project/profile['cspArchive'],profile['archives'][profile['cspArchive']])
    JC.require(len(data)==10 and {n:JC.sha(v) for n,v in data.items()}==profile['cspArchiveMembers'],'CSP member vector')
    delta=verify_csp_delta(data['original/CubicStatePreparation.lean'],data['candidate/CubicStatePreparation.lean'])
    JC.require((project/CSP).read_bytes()==data['original/CubicStatePreparation.lean'],'original CSP project binding')
    cubic=(base_package/'candidate'/CUBIC).read_bytes(); expected,sites=runtime.proof_patch.candidate((project/CUBIC).read_bytes())
    JC.require(cubic==expected and JC.sha(cubic)==NEW_CUBIC,'exact unchanged three-token Cubic candidate')
    return profile,derived,guard,runtime,ci4,ci2,base,p1,api,data,cubic,dict(CSP=delta,CubicProofTokenSites=sites)


def prepare(project,work,view,derived,p1,api,base,guard,csp_bytes,cubic_bytes):
    work.mkdir(); view.mkdir(); rows=[]
    for relative,wanted in derived['projectInputs'].items():
        if relative==CSP: data=csp_bytes
        elif relative==CUBIC: data=cubic_bytes
        else: data=api.safe_child(project,relative).read_bytes()
        JC.require(JC.sha(data)==wanted,'shadow input source pin')
        dest=api.safe_child(work,relative); write_bytes(dest,data)
        JC.require(sha(dest)==wanted,'shadow input destination pin')
        rows.append(dict(relativePath=relative,sha256=wanted,destination=str(dest)))
    helper=guard.copy_shared_helper(project,work,derived,api)
    seed=api.safe_child(work,'.lake/build/lib/lean'); seed.mkdir(parents=True)
    copies=base.copy_providers(project,seed,derived,api)
    reject_target_cache([seed], [JC.CSP]+[r['module'] for r in derived['modules']],api)
    for relative in ('Collector.lean','pending-drivers/Profile.lean','pending-drivers/Probe.lean'):
        data=(p1/relative).read_bytes(); destination=api.safe_child(view,relative); write_bytes(destination,data)
        JC.require(sha(destination)==sha(p1/relative),'unchanged C31 collector/driver')
    api.write_json(view/'profile.json',derived)
    files={p.relative_to(view).as_posix():sha(p) for p in view.rglob('*') if p.is_file()}
    api.write_json(view/'proposal-bindings.json',dict(files=files,provenance='NEW_JOINT_INPUT_VIEW_NOT_OLD_V1_SEAL',**JC.FLAGS))
    return rows,[*copies,helper],files,helper


class JointCSP:
    """Single insertion point: same base cohort exists, before any C31 target."""
    def __init__(self,work,base,api,callback,derived):
        self.work,self.base,self.api,self.callback,self.derived=work,base,api,callback,derived
        self.called=False; self.rows=[]; self.receipt=None; self.environment=None; self.absent=[]

    def compile(self,path,value):
        if path.name!='runtime-environment.json' or path.parent!=self.work/self.base.OUT_REL/'private': return
        JC.require(not self.called,'CSP insertion duplicate'); self.called=True
        api=self.api; inner=self.work/self.base.OUT_REL; fresh=inner/'cohort'; sources=inner/'source'
        recorded=read(path); profile_sha=recorded['profileSHA256']; cohort=recorded['cohortID']
        env=dict(os.environ,LEAN_PATH=recorded['LEAN_PATH'],C31_FRESH_ROOT=str(fresh.resolve()),
            C31_PROFILE_SHA256=profile_sha,C31_COHORT_ID=cohort)
        env.pop('QBE_EXPECT_FRESH_OLEAN',None)
        roots=[Path(p) for p in env['LEAN_PATH'].split(os.pathsep)]
        reject_target_cache(roots,self.derived_modules(),api)
        original=api.safe_child(self.work,CSP); source=api.safe_child(sources,CSP)
        before=sha(original); JC.require(before==NEW_CSP,'CSP shadow source pin')
        write_bytes(source,original.read_bytes()); output=api.safe_child(fresh,CSP.replace('.lean','.olean'))
        output.parent.mkdir(parents=True,exist_ok=True)
        inventory=read(inner/'private/provider-inventory.json'); lean=Path(inventory['leanBinary'])
        self.absent=[Path(p) for p in inventory.get('absentConfiguredRoots',[])]
        JC.require(sha(lean)==inventory['leanBinarySHA256'],'actual native binary source pin')
        result=self.callback(inner/'private','10-csp-target',[str(lean),'--threads=1','--memory=3072','-o',str(output),CSP],sources,env,timeout=900)
        JC.require(output.is_file() and sha(original)==before==sha(source),'CSP fresh compile/source before-after')
        artifacts=[
            dict(path=str(p),sha256=sha(p)) for suffix in api.SIDECARS
            for p in [api.safe_child(fresh,CSP.replace('.lean',suffix))] if p.is_file()]
        self.rows=[dict(path=str(source),sha256=NEW_CSP),dict(path=str(lean),sha256=inventory['leanBinarySHA256'])]+artifacts
        self.receipt=dict(module=JC.CSP,sourceSHA256Before=before,sourceSHA256After=sha(original),
            copiedSourceSHA256=sha(source),freshOlean=str(output.resolve()),freshOleanSHA256=sha(output),
            cohortID=cohort,nativeResult=result,artifacts=artifacts,sourceArtifactInherited=False,**JC.FLAGS)
        api.write_json(inner/'private/joint-csp-fresh.json',self.receipt); self.environment=env

    def derived_modules(self): return [JC.CSP]+[r['module'] for r in self.derived['modules']]


@contextmanager
def insertion(callback,joint):
    old=callback.write_json
    def wrapped(path,value):
        result=old(path,value); joint.compile(path,value); return result
    callback.write_json=wrapped
    try: yield
    finally: callback.write_json=old


def run(project,package):
    profile,derived,guard,runtime,ci4,ci2,base,p1,api,csp_zip,cubic,delta=setup(project,package)
    deadline=runtime.Deadline(); manifest=read(package/'bindings.json'); manifest_sha=sha(package/'bindings.json')
    profile_sha=sha(package/'profile.json'); base_package=project/'tools/c31_kernel_proof_v1'
    base_files=read(project/'tools/c31_kernel_proof_v3/profile.json')['baseFiles']
    def executing():
        api.verify_pins(package,manifest['files'])
        JC.require(sha(package/'profile.json')==profile_sha and sha(package/'bindings.json')==manifest_sha,'joint own profile/manifest drift')
        record=guard.execution_record(package,base_package,base_files,runtime,__file__,sys.argv[0],
            getattr(sys.modules.get('__main__'),'__file__',None),manifest['files']['entry.py'])
        record['entry']['expectedLogicalFile']='$JOINT_PACKAGE/entry.py'
        record['jointComparisonModule']=guard.module_file(JC,package/'joint_compare.py',manifest['files']['joint_compare.py'])
        record['jointComparisonModule']['expectedLogicalFile']='$JOINT_PACKAGE/joint_compare.py'
        record['reusedGuardAPI']=guard.module_file(guard,project/'tools/c31_kernel_proof_v3/entry.py',
            profile['externalFiles']['tools/c31_kernel_proof_v3/entry.py'])
        record['reusedGuardAPI']['expectedLogicalFile']='$PROJECT/tools/c31_kernel_proof_v3/entry.py'
        return record
    executing(); ci4.gate4.context_check(ci4.gate4.actual_context())
    out=api.safe_child(project,OUT); out.mkdir(parents=True,exist_ok=False)
    private=out/'private'; public=out/'public'; private.mkdir(mode=0o700); public.mkdir()
    work=out/'workspace'; view=out/'runtime-input-view'; csp_runtime=out/'csp-validator-view'
    state=dict(seed=[],viewFiles={},extra=[],joint=None); status=dict(status='JOINT_NOT_RUN',**JC.FLAGS); code=1
    logical={str(project):'$PROJECT',str(package):'$JOINT_PACKAGE',str(work):'$JOINT_WORKSPACE',str(out):'$JOINT_RUN'}
    def revalidate():
        deadline.remaining(); executing()
        api.verify_pins(project,dict(profile['externalFiles'],**profile['archives']))
        api.verify_pins(project,profile['originalProjectInputs'])
        if work.exists(): api.verify_pins(work,derived['projectInputs'])
        if state['viewFiles']: api.verify_pins(view,state['viewFiles'])
        base.recheck_rows(state['seed']+state['extra']+(state['joint'].rows if state['joint'] else []),api)
        if work.exists(): reject_target_cache([work/'.lake/build/lib/lean'],profile['compileOrder'],api)
        if state['joint']:
            JC.require(not any(p.exists() for p in state['joint'].absent),'absent provider root appeared')
            if state['joint'].environment:
                roots=[Path(p) for p in state['joint'].environment['LEAN_PATH'].split(os.pathsep)]
                reject_target_cache(roots[1:],profile['compileOrder'],api)
    try:
        revalidate(); api.write_json(private/'executing-code-bindings.json',executing())
        initial=ci4.gate4.sample(); api.write_json(private/'joint-preparation-resource.json',dict(initial,**JC.FLAGS)); ci4.gate4.validate_snapshot(initial)
        rows,state['seed'],state['viewFiles'],helper=prepare(project,work,view,derived,p1,api,base,guard,csp_zip['candidate/CubicStatePreparation.lean'],cubic)
        api.write_json(private/'joint-inputs.json',dict(originalProjectInputs=profile['originalProjectInputs'],
            shadowProjectInputs=derived['projectInputs'],inputCopies=rows,providerSeedCopies=state['seed'],
            sharedHelperCopy=helper,exactSourceDelta=delta,c31RawProfileSHA256=sha(view/'profile.json'),**JC.FLAGS))
        callback=ci2.BudgetCallback(api,revalidate,dict(jointProfileSHA256=profile_sha,jointManifestSHA256=manifest_sha,
            compileOrder=profile['compileOrder'],resourceContract='CI4_SELF_ONLY_5120_PLUS_2048_THREADS1',wholeSeconds=2100),sampler=ci4.gate4.sample)
        callback.native=deadline.native(callback.native)
        joint=JointCSP(work,base,api,callback,derived); state['joint']=joint
        env=runtime.external_environment(project,work,dict(os.environ))
        reject_target_cache([Path(p) for p in env['LEAN_PATH'].split(os.pathsep)],profile['compileOrder'],api)
        with insertion(callback,joint),runtime.reused_callbacks(base,ci2,ci4.gate4,api,callback,env):
            code=base.run(work,view)
            JC.require(code==0 and joint.called and joint.receipt is not None,'C31 compilation/observation or CSP insertion failed')
            inner=work/base.OUT_REL; native_private=inner/'private'; driver=inner/'driver'
            actual_env=dict(joint.environment); actual_env['QBE_EXPECT_FRESH_OLEAN']=joint.receipt['freshOlean']
            three=read(native_private/'fresh-target-cohort.json')
            JC.require(three['cohortID']==joint.receipt['cohortID'],'CSP/consumer cohort identity')
            for target in three['targets']: state['extra']+=target['artifacts']
            inventory=read(native_private/'provider-inventory.json'); state['extra']+=inventory['artifacts']
            state['extra']+=read(native_private/'driver-bindings.json')['artifacts']
            csp_runtime.mkdir()
            for name in ('validate-output.py','validate-output-v2.py','expected-roots.json'):
                destination=csp_runtime/name; write_bytes(destination,csp_zip['vendor/'+name]); state['extra'].append(dict(path=str(destination),sha256=sha(destination)))
            for name,data in [('CspProbe.lean',csp_zip['vendor/Probe-v5.lean']),('KernelTwoTypes.lean',(project/'tools/cubic_c29_kernel_types_v2/KernelTwoTypes.lean').read_bytes())]:
                destination=driver/name; write_bytes(destination,data); state['extra'].append(dict(path=str(destination),sha256=sha(destination)))
            lean=inventory['leanBinary']; flags=[lean,'--threads=1','--memory=3072']
            full=api.native_call(native_private,'40-csp-probe',flags+['CspProbe.lean'],driver,actual_env,timeout=900)
            types=api.native_call(native_private,'41-csp-two-types',flags+['KernelTwoTypes.lean'],driver,actual_env,timeout=900)
            full_text=(native_private/'40-csp-probe.stdout.raw').read_text(encoding='utf-8')
            two_text=(native_private/'41-csp-two-types.stdout.raw').read_text(encoding='utf-8')
            original_validator=load('joint_csp_original_validator',csp_runtime/'validate-output.py')
            fields=load('joint_csp_field_validator',csp_runtime/'validate-output-v2.py')
            two_validator=load('joint_csp_two_validator',project/'tools/cubic_c29_kernel_types_v2/validate_two_types.py')
            two_validator.validate_supplement(two_text,types['exitCode'],Path(joint.receipt['freshOlean']))
            parsed=JC.strict(full_text,JC.CSP_TAGS)
            joint_bindings(joint.receipt,three,parsed,JC.strict(two_text,JC.TWO_TAGS))
            baselines={name:archive(project/profile[name],profile['archives'][profile[name]]) for name in ('cspBaselineArchive','c31BaselineArchive')}
            JC.receipt_partition(baselines['cspBaselineArchive'],'cubic-c29-kernel-only-v1/public/')
            JC.receipt_partition(baselines['cspBaselineArchive'],'cubic-c29-kernel-types-v2/public/')
            JC.receipt_partition(baselines['c31BaselineArchive'],'')
            csp_baseline=baselines['cspBaselineArchive']; c31_baseline=baselines['c31BaselineArchive']
            csp_check=JC.compare_csp(csp_baseline[JC.CSP_FULL].decode(),csp_baseline[JC.CSP_TWO].decode(),full_text,two_text,
                read(csp_runtime/'expected-roots.json'),original_validator,fields)
            c31_check=JC.compare_c31(c31_baseline[JC.C31_STREAM].decode(),(native_private/'30-observe.stdout.raw').read_text(encoding='utf-8'))
            revalidate()
            api.write_json(private/'joint-comparison.json',dict(CSP=csp_check,C31=c31_check,**JC.FLAGS))
            api.write_json(private/'joint-four-target-cohort.json',dict(compileOrder=profile['compileOrder'],
                cohortID=three['cohortID'],targets=[joint.receipt]+three['targets'],
                bothCSPProbesSameFreshOlean=joint.receipt['freshOlean'],CSPProbeNativeResult=full,twoTypesNativeResult=types,**JC.FLAGS))
        revalidate(); status.update(status='JOINT_FRESH_PROVIDER_CONSUMER_DIAGNOSTIC_COMPLETE_NOT_ACCEPTANCE',
            CSPRoots=csp_check['explicitRoots'],CSPGenerated=csp_check['generatedObserved'],C31Roots=c31_check['explicitRoots'],
            C31Generated=c31_check['generatedObserved'],cohortID=joint.receipt['cohortID'],inheritedProviders=True,cleanTransitive=False,actualLoadTrace=False); code=0
    except Exception as error:
        code=1; status.update(status='JOINT_FAILED_CLOSED_NOT_MATHEMATICAL_REFUTATION',failureType=type(error).__name__,failure=str(error))
    finally:
        inner=work/base.OUT_REL/'private'
        if inner.is_dir():
            for source in sorted(inner.iterdir()):
                if source.is_file() and source.suffix in ('.json','.raw'):
                    data=source.read_bytes(); destination=private/source.name; write_bytes(destination,data)
                    JC.require(sha(source)==sha(destination),'actual receipt copy drift')
        api.write_json(private/'joint-result.json',dict(status,wholeRemainingSeconds=max(0,deadline.end-deadline.clock())))
        api.export_public(private,public,logical)
    print(json.dumps(api.redact_tree(status,logical))); return code


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--project',type=Path,default=Path.cwd())
    args=parser.parse_args()
    try: result=run(args.project.resolve(),Path(__file__).parent.resolve())
    except Exception as error:
        print(json.dumps(dict(status='JOINT_ENTRY_FAILED_CLOSED',failureType=type(error).__name__,**JC.FLAGS))); result=1
    sys.exit(result)
