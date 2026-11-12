from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import entry

FILES=['entry.py','README.md','build_profile.py','profile.json','test_guard.py','freeze.py','python-tests.json','bindings.json','seal.json']


def write(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as out: json.dump(value,out,indent=2); out.write('\n')


def freeze(base,package):
    profile=entry.read(package/'profile.json'); entry.verify(base,profile['baseFiles'])
    command=[sys.executable,'-B','-m','unittest','discover','-s',str(package),'-p','test_guard.py','-v']
    env=dict(os.environ,C31_KERNEL_V1_TEST_PACKAGE=str(base)); started=datetime.now(timezone.utc).isoformat()
    child=subprocess.Popen(command,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT); timeout=False
    try: raw,_=child.communicate(timeout=60)
    except subprocess.TimeoutExpired: timeout=True; child.kill(); raw,_=child.communicate()
    text=raw.decode('utf-8').replace(str(package),'$GUARD_PACKAGE').replace(str(base),'$KERNEL_V1_PACKAGE')
    write(package/'python-tests.json',dict(kind='ACTUAL_PYTHON_GUARD_TESTS_SYNTHETIC_MAIN_METADATA_NO_LEAN',
        PID=child.pid,startedUTC=started,finishedUTC=datetime.now(timezone.utc).isoformat(),exitCode=child.returncode,
        timedOut=timeout,rawStdoutSHA256=hashlib.sha256(raw).hexdigest(),stdoutSanitized=text,**entry.NO_ACCEPT))
    print(text)
    if timeout or child.returncode!=0: raise ValueError('Python guard test failure')
    entry.verify(base,profile['baseFiles'])
    files={p.name:entry.sha(p) for p in package.iterdir() if p.is_file() and p.name not in ('bindings.json','seal.json')}
    if set(files)!=set(FILES)-{'bindings.json','seal.json'}: raise ValueError('package partition drift')
    write(package/'bindings.json',dict(files=files))
    seal=dict(state='PRIVATE_SMALL_KERNEL_V2_EXECUTION_GUARD_PROPOSAL_PYTHON_TESTED_NATIVE_UNRUN',
        UTC=datetime.now(timezone.utc).isoformat(),profileSHA256=entry.sha(package/'profile.json'),manifestSHA256=entry.sha(package/'bindings.json'),
        immutableBaseManifestSHA256=profile['baseManifestSHA256'],immutableBaseSealSHA256=profile['baseSealSHA256'],
        old19FilesUnchanged=True,mathematicalDelta=False,resourceDelta=False,workflowRewritten=False,
        observedRuntimeFileGuards=['runtime.py','compare.py','proof_patch.py'],executingEntryGuard='entry.py plus argv0 and __main__.__file__',
        publicRepoCandidateTransportAllowed=True,privateLabelWasBlindReviewScopeNotConfidential=True,
        publicSafeReviewAllowlist=FILES,localLeanInvocationCount=0,actualCandidateCompilationObserved=False,
        actualProductionEntryExecuted=False,guardBoundary='Source path/on-disk SHA/object identity observations, not OS/codeobject attestation',
        installationPerformed=False,productionChanged=False,gitOperations=0,networkOperations=0,**entry.NO_ACCEPT)
    write(package/'seal.json',seal)
    print(json.dumps(dict(profileSHA256=seal['profileSHA256'],manifestSHA256=seal['manifestSHA256'],sealSHA256=entry.sha(package/'seal.json'),files=len(FILES))))


if __name__=='__main__': freeze(Path(sys.argv[1]).resolve(),Path(__file__).parent.resolve())
