"""Same-fresh kernel-candidate two-type supplement; no production/admission change."""
from datetime import datetime,timezone
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
FLAGS=dict(sourceAgreement=None,publicationBinding=None,axiomPolicyPass=None,
           nativeAccepted=False,scientific_ROOT=False)

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    if Path(module.__file__).resolve()!=path.resolve():raise ValueError('executed module path mismatch')
    return module

def read(path):return json.loads(path.read_bytes())

def digest(path):
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()

def checked_stream(validator,text,code,fresh):
    allowed={'C29_TWO_BINDING_JSON','C29_TWO_TYPE_JSON','C29_TWO_SUMMARY_JSON'}
    for line in text.splitlines():
        if line.startswith('C29_') and line.split(' ',1)[0] not in allowed:
            raise ValueError('unknown two-type diagnostic tag')
    result=validator.validate_supplement(text,code,fresh)
    if any(r['isUnsafe'] or r['selfOccursInAxioms'] for r in result['signatures']):
        raise ValueError('unsafe or self-axiom signature')
    return result

def run(project):
    if not sys.platform.startswith('linux') or os.environ.get('GITHUB_ACTIONS')!='true' or os.environ.get('RUNNER_OS')!='Linux':
        raise ValueError('finite supplement is GitHub Linux CI only')
    project=project.resolve();profile=read(HERE/'profile.json');manifest=read(HERE/'package-bindings.json')
    if profile['schema']!='C29_KERNEL_TWO_TYPES_SAME_FRESH_V2' or profile['entrySHA256']!=digest(Path(__file__)):
        raise ValueError('unsupported entry/profile')
    package=project/'tools/cubic_c29_kernel_ci1'
    def recheck():
        for name,expected in manifest['files'].items():
            if digest(HERE/name)!=expected:raise ValueError('supplement package drift: '+name)
        for name,expected in profile['priorPackageFiles'].items():
            if digest(package/name)!=expected:raise ValueError('CI1 package drift: '+name)
    recheck()
    prior=load('c29_kernel_ci1_exact_launcher_for_types_v2',package/'launch.py')
    code=prior.execute()
    if code!=0:return code
    runtime=project/'_out/cubic-c29-kernel-ci1/runtime'
    driver_package=read(runtime/'proposal-pins.json')
    for name,expected in driver_package['packageFiles'].items():
        if digest(runtime/name)!=expected:raise ValueError('prepared runtime changed')
    api=load('c29_kernel_exact_vendor_for_types_v2',runtime/'vendor/runner.py')
    api.verify_pins(project,driver_package['originalProjectInputs'])
    validator=load('c29_kernel_two_types_validator_v1',HERE/'validate_two_types.py')
    old_private=project/'_out/cubic-c29-kernel-only-v1/private'
    old_final=read(old_private/'result.json')
    if old_final['status']!='KERNEL_SUBSTITUTION_RUNTIME_DIAGNOSTIC_COMPLETE_NOT_ACCEPTANCE':
        raise ValueError('preceding actual candidate diagnostic absent')
    fresh=project/'_out/cubic-c29-kernel-only-v1/fresh/QuantumBlockEncoding/CubicStatePreparation.olean'
    old_artifacts=read(old_private/'fresh-candidate-artifacts.json')
    before=digest(fresh)
    if old_artifacts['candidateSourceSHA256']!=profile['candidateRawSHA256'] or old_artifacts['files'][0]['sha256']!=before:
        raise ValueError('same-candidate fresh artifact binding failed')
    env=dict(os.environ)
    env.update(read(old_private/'04-full-kernel-candidate-probe.setup.json')['selectedEnvironment'])
    env['QBE_EXPECT_FRESH_OLEAN']=str(fresh)
    prefix=Path((old_private/'02-prefix.stdout.raw').read_text().strip()).resolve()
    lean=prefix/'bin/lean'
    if digest(lean)!=read(old_private/'providers.json')['actualLeanBinarySHA256']:
        raise ValueError('actual Lean binary changed')
    out=api.safe_child(project,'_out/cubic-c29-kernel-types-v2');out.mkdir(exist_ok=False)
    private=out/'private';private.mkdir();public=out/'public';public.mkdir();driver=out/'driver';driver.mkdir()
    logical={str(project):'$PROJECT',str(prefix):'$TOOLCHAIN',str(HERE):'$KERNEL_TYPES_PACKAGE'}
    result=dict(status='TWO_KERNEL_CANDIDATE_TYPES_NOT_RUN',**FLAGS);exit_code=1
    try:
        source=HERE/'KernelTwoTypes.lean';destination=driver/'KernelTwoTypes.lean'
        shutil.copyfile(source,destination)
        if digest(source)!=digest(destination):raise ValueError('collector source/destination changed')
        api.write_json(private/'input-bindings.json',dict(schema=profile['schema'],actualEntrySHA256=digest(Path(__file__)),
            actualEntryPath=str(Path(__file__).resolve()),actualPriorLauncherSHA256=digest(package/'launch.py'),
            actualVendorSHA256=digest(runtime/'vendor/runner.py'),collectorSourceSHA256=digest(source),
            collectorDestinationSHA256=digest(destination),validatorSHA256=digest(HERE/'validate_two_types.py'),
            targetFreshOleanSHA256=before,candidateSourceSHA256=profile['candidateRawSHA256'],
            manifestSHA256=digest(HERE/'package-bindings.json'),sameFreshFromPrecedingFullProbe=True,**FLAGS))
        recheck()
        actual=api.native_call(private,'05-two-kernel-types',
            [str(lean),'--threads=1','--memory=3072','KernelTwoTypes.lean'],driver,env,timeout=300)
        validated=checked_stream(validator,(private/'05-two-kernel-types.stdout.raw').read_text(),actual['exitCode'],fresh)
        recheck()
        api.verify_pins(project,driver_package['originalProjectInputs'])
        for name,expected in driver_package['packageFiles'].items():
            if digest(runtime/name)!=expected:raise ValueError('prepared executing runtime changed')
        if digest(lean)!=read(old_private/'providers.json')['actualLeanBinarySHA256']:
            raise ValueError('actual Lean binary changed after supplement')
        if any(Path(p).exists() for p in read(old_private/'providers.json')['absentSearchRoots']):
            raise ValueError('previously absent search root appeared')
        if digest(fresh)!=before or digest(source)!=digest(destination):raise ValueError('fresh/collector drift after observation')
        for row in read(old_private/'copied-five-local-providers.json')['files']:
            if digest(Path(row['source']))!=row['sha256'] or digest(Path(row['destination']))!=row['sha256']:
                raise ValueError('copied provider changed')
        for row in read(old_private/'providers.json')['files']:
            if digest(Path(row['path']))!=row['sha256']:raise ValueError('inherited provider changed')
        validated.update(targetFreshOleanSHA256=before,nativePID=actual['PID'],nativeExitCode=actual['exitCode'])
        api.write_json(private/'two-kernel-types.json',validated)
        result.update(status='TWO_KERNEL_CANDIDATE_TYPES_OBSERVED_NOT_ACCEPTANCE',
            targetFreshOleanSHA256=before,candidateSourceSHA256=profile['candidateRawSHA256'],
            types=2,valuesPrinted=False,independentReview='PENDING',inheritedProviders=True,cleanTransitive=False,actualLoadTrace=False)
        exit_code=0
    except Exception as error:
        result.update(status='SUPPLEMENT_FAILED_NOT_MATHEMATICAL_REFUTATION',failureType=type(error).__name__,failure=str(error))
    finally:
        api.write_json(private/'result.json',result);api.export_public(private,public,logical)
    print(json.dumps(api.redact_tree(result,logical)),flush=True)
    return exit_code

if __name__=='__main__':
    try:code=run(Path.cwd())
    except Exception as error:
        print(json.dumps(dict(status='SUPPLEMENT_ENTRY_FAILED_CLOSED',failureType=type(error).__name__,**FLAGS)));code=1
    sys.exit(code)
