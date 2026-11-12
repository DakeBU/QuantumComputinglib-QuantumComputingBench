"""Python-only freeze with exact old/new partitions; no Lean or network."""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import entry

FILES=['entry.py','README.md','build_profile.py','profile.json','test_guard.py','verify_failure.py',
       'actual-first-failure.json','freeze.py','python-tests.json','bindings.json','seal.json']


def write(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as out: json.dump(value,out,indent=2); out.write('\n')


def freeze(base,previous,project,package):
    profile=entry.read(package/'profile.json')
    def recheck():
        entry.verify(base,profile['baseFiles']); entry.verify(previous,profile['priorGuardFiles'])
        entry.verify(project,{entry.SHARED_PATH:entry.SHARED_SHA})
    recheck()
    command=[sys.executable,'-B','-m','unittest','discover','-s',str(package),'-p','test_guard.py','-v']
    env=dict(os.environ,C31_KERNEL_V1_TEST_PACKAGE=str(base),C31_KERNEL_TEST_PROJECT=str(project))
    started=datetime.now(timezone.utc).isoformat()
    child=subprocess.Popen(command,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT); timeout=False
    try: raw,_=child.communicate(timeout=60)
    except subprocess.TimeoutExpired: timeout=True; child.kill(); raw,_=child.communicate()
    text=raw.decode('utf-8')
    for root,label in ((package,'$V3_PACKAGE'),(base,'$KERNEL_V1_PACKAGE'),(previous,'$KERNEL_V2_PACKAGE'),(project,'$PROJECT')):
        for spelling in (str(root),str(root).replace('\\','/')): text=text.replace(spelling,label)
    write(package/'python-tests.json',dict(kind='ACTUAL_PYTHON_V3_SHADOW_COPY_AND_ENTRY_TESTS_NO_LEAN',
        PID=child.pid,startedUTC=started,finishedUTC=datetime.now(timezone.utc).isoformat(),exitCode=child.returncode,
        timedOut=timeout,rawStdoutSHA256=hashlib.sha256(raw).hexdigest(),stdoutSanitized=text,
        providerBinarySeedingInFullPrepareTest='EXPLICIT_STUB',localLeanInvocationCount=0,**entry.NO_ACCEPT))
    print(text)
    if timeout or child.returncode!=0: raise ValueError('actual Python tests failed; receipt preserved')
    recheck()
    files={p.name:entry.sha(p) for p in package.iterdir() if p.is_file() and p.name not in ('bindings.json','seal.json')}
    if set(files)!=set(FILES)-{'bindings.json','seal.json'}: raise ValueError('package partition drift')
    if any(p.is_dir() for p in package.iterdir()): raise ValueError('unexpected package subdirectory')
    write(package/'bindings.json',dict(files=files))
    write(package/'seal.json',dict(state='PRIVATE_V3_SHADOW_HELPER_FIX_PROPOSAL_PYTHON_TESTED_NATIVE_UNRUN',
        UTC=datetime.now(timezone.utc).isoformat(),profileSHA256=entry.sha(package/'profile.json'),
        manifestSHA256=entry.sha(package/'bindings.json'),firstFailureZIP_SHA256=profile['firstFailureArtifactZIP_SHA256'],
        oldV1_19FilesUnchanged=True,oldV2_9FilesUnchanged=True,
        immutableV1ManifestSHA256=profile['baseManifestSHA256'],immutableV1SealSHA256=profile['baseSealSHA256'],
        immutableV2ManifestSHA256=profile['priorGuardManifestSHA256'],immutableV2SealSHA256=profile['priorGuardSealSHA256'],
        sharedHelperSHA256=entry.SHARED_SHA,publicSafeReviewAllowlist=FILES,
        sourceProofTokenDeltaFromV1=False,raw87ProfileDeltaFromV1=False,collectorDelta=False,
        resourceDelta=False,strictComparisonDelta=False,workflowRewritten=False,
        localLeanInvocationCount=0,actualCandidateCompilationObserved=False,
        installationPerformed=False,productionChanged=False,gitOperations=0,networkOperations=0,
        rollback='Reverse optional entry command only; all temporary hooks restore in finally',
        guardBoundary='Actual entry/main/argv0 and loaded-three-module source path/hash/object observations, not OS/code-object attestation',
        **entry.NO_ACCEPT))
    print(json.dumps(dict(profileSHA256=entry.sha(package/'profile.json'),manifestSHA256=entry.sha(package/'bindings.json'),
        sealSHA256=entry.sha(package/'seal.json'),entrySHA256=entry.sha(package/'entry.py'),files=len(FILES))))


if __name__=='__main__': freeze(*(Path(p).resolve() for p in sys.argv[1:4]),Path(__file__).parent.resolve())
