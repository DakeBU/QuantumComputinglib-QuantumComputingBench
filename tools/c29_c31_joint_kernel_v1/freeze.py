"""Python-only joint proposal freeze; no native Lean invocation."""
from datetime import datetime,timezone
import os
from pathlib import Path
import re
import subprocess
import sys
import entry as E
import joint_compare as J

FILES=['entry.py','joint_compare.py','build_profile.py','test_joint.py','freeze.py','README.md',
    'profile.json','c31-profile.json','development-diagnostics.json','python-tests.json','bindings.json','seal.json']


def write(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as f:
        import json
        json.dump(value,f,indent=2); f.write('\n')


def freeze(project,package):
    setup=E.setup(project,package); profile=setup[0]; api=setup[8]
    allpins=dict(profile['originalProjectInputs'],**profile['externalFiles'],**profile['archives'])
    api.verify_pins(project,allpins)
    before={n:E.sha(project/n) for n in allpins}
    command=[sys.executable,'-B','-m','unittest','discover','-s',str(package),'-p','test_joint.py','-v']
    env=dict(os.environ,C31_JOINT_TEST_PROJECT=str(project)); begin=datetime.now(timezone.utc).isoformat()
    child=subprocess.Popen(command,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT); timeout=False
    try: raw,_=child.communicate(timeout=60)
    except subprocess.TimeoutExpired: timeout=True; child.kill(); raw,_=child.communicate()
    text=raw.decode('utf-8')
    for root,label in ((package,'$JOINT_PACKAGE'),(project,'$PROJECT')):
        text=text.replace(str(root),label).replace(str(root).replace('\\','/'),label)
    write(package/'python-tests.json',dict(kind='ACTUAL_PYTHON_JOINT_PROPOSAL_TESTS_NOT_JOINT_LEAN',
        PID=child.pid,startedUTC=begin,finishedUTC=datetime.now(timezone.utc).isoformat(),exitCode=child.returncode,
        timedOut=timeout,rawStdoutSHA256=J.sha(raw),stdoutSanitized=text,
        actualChildScope='One real Python child through unchanged native wrapper with synthetic CI/resource context; never a Lean child',
        syntheticOleanFixturesNotLeanArtifacts=True,actualJointCompilationObserved=False,localLeanInvocationCount=0,**J.FLAGS))
    print(text); J.require(not timeout and child.returncode==0,'actual Python tests failed; receipt preserved')
    api.verify_pins(project,allpins); J.require(before=={n:E.sha(project/n) for n in allpins},'old source/package/archive bytes changed')
    actual={p.name for p in package.iterdir() if p.is_file()}
    J.require(actual==set(FILES)-{'bindings.json','seal.json'} and not any(p.is_dir() for p in package.iterdir()),'package exact partition')
    for name in actual:
        J.require(re.search(r'[A-Za-z]:[\\/](?:Users|home|tmp)[\\/]',(package/name).read_text(encoding='utf-8')) is None,'host path leak')
    files={n:E.sha(package/n) for n in sorted(actual)}
    write(package/'bindings.json',dict(files=files,**J.FLAGS))
    write(package/'seal.json',dict(state='JOINT_CSP_C31_FRESH_KERNEL_PROPOSAL_PYTHON_TESTED_LEAN_UNRUN',
        UTC=datetime.now(timezone.utc).isoformat(),identity='/root/primitive_compiler_formal_decoder_c31',
        direction='joint-fresh-provider-then-consumer/single-cohort/formal-only',
        profileSHA256=E.sha(package/'profile.json'),c31ProfileSHA256=E.sha(package/'c31-profile.json'),
        manifestSHA256=E.sha(package/'bindings.json'),entrySHA256=E.sha(package/'entry.py'),
        fixedCSPCandidateSHA256=E.NEW_CSP,fixedCubicCandidateSHA256=E.NEW_CUBIC,
        originalInputsAndPackagesUnchanged=True,originalProjectInputs=len(profile['originalProjectInputs']),
        freshCompileOrder=profile['compileOrder'],CSPSourceRoots=319,C31SourceRoots=87,
        generatedExpectation=None,localLeanInvocationCount=0,actualJointCompilationObserved=False,
        separateSuccessesDoNotEstablishJointSuccess=True,publicSafeAllowlist=FILES,
        productionChanged=False,registryChanged=False,workflowChanged=False,installationPerformed=False,gitOperations=0,networkOperations=0,
        resourceContract='CI4 Linux self-namespace / MemAvailable and nonroot ancestor headroom >=5120+2048MiB / threads1 / whole2100s',
        ordinaryBodyOmissionsNotHiddenOrReclassified=True,
        rollback='Do not select/revert only the optional new entry command; all original packages and failed outputs remain intact',
        processSkill='qbe-substantive-worker: frozen objective, typed NOT_RUN integration boundary and handoff; no source/admission authority',
        **J.FLAGS))
    for name in ('profile.json','c31-profile.json','entry.py','joint_compare.py','python-tests.json','bindings.json','seal.json'):
        print(name,E.sha(package/name))


if __name__=='__main__': freeze(Path(sys.argv[1]).resolve(),Path(__file__).parent.resolve())
