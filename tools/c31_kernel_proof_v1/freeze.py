"""Seal the new candidate/proposal only after exact source and whole-baseline checks."""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import compare
import proof_patch
import runtime

FILES=['README.md','HANDOFF.md','proof_patch.py','compare.py','runtime.py','build_package.py',
    'test_kernel.py','freeze.py','original-profile.json','profile.json','kernel-profile.json',
    'baseline.json','proof-sites.json','proof-token.PROPOSAL.patch','workflow.PROPOSAL.yml',
    'candidate/QuantumBlockEncoding/CubicAmplitudePrimitive.lean','python-tests.json','bindings.json','seal.json']


def freeze(project,package,public):
    config=runtime.read(package/'kernel-profile.json')
    ci4,ci2,base,p1,original,api=runtime.load_runtime(project,config)
    baseline=runtime.read(package/'baseline.json')
    source_root=project/'runs/hermite-curriculum-goal-20261008/scratch/primitive-compiler-decoder-c31'
    def unchanged():
        for root,files in config['runtimePackages'].items(): runtime.verify(project/root,files)
        api.verify_pins(project,original['projectInputs'])
        api.verify_pins(project,{original['sharedInstrumentation']['path']:original['sharedInstrumentation']['sha256']})
        if runtime.sha(source_root/'source-formal-seal.json')!=original['sourceSealSHA256']:
            raise ValueError('original source seal drift')
        if runtime.sha(package/'original-profile.json')!=config['originalProfileSHA256'] or \
            runtime.sha(package/'profile.json')!=config['candidateProfileSHA256'] or \
            runtime.sha(package/'baseline.json')!=config['baselineSHA256']:
            raise ValueError('new exact profile/baseline hash binding drift')
        new,sites=proof_patch.candidate((project/proof_patch.RELATIVE).read_bytes())
        if new!=(package/'candidate'/proof_patch.RELATIVE).read_bytes(): raise ValueError('candidate byte drift')
        proof_patch.validate_derivation(original,runtime.read(package/'profile.json'),proof_patch.sha(new))
        runtime.verify(public,baseline['actualPublicMemberSHA256'])
        text=(public/'30-observe.stdout.raw.sanitized.txt').read_text(encoding='utf-8'); records=base.validator.parse(text)
        terminal=records['C31_SUMMARY_JSON'][0]; bindings=records['C31_BINDING_JSON']
        checked=base.validator.validate(original,text,0,timed_out=False,profile_sha=config['originalProfileSHA256'],
            cohort_id=terminal['cohortID'],expected_oleans={b['module']:b['resolvedOleanPath'] for b in bindings})
        if compare.normalized(records)!=baseline['rows'] or checked!=runtime.read(public/'completeness.json'):
            raise ValueError('complete actual baseline drift')
    unchanged()
    cmd=[sys.executable,'-B','-m','unittest','discover','-s',str(package),'-p','test_kernel.py','-v']
    env=dict(os.environ,C31_TEST_PROJECT=str(project),TMP=str(package),TEMP=str(package))
    started=datetime.now(timezone.utc).isoformat(); child=subprocess.Popen(cmd,cwd=project,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    timeout=False
    try: raw,_=child.communicate(timeout=60)
    except subprocess.TimeoutExpired: timeout=True; child.kill(); raw,_=child.communicate()
    sanitized=api.redact(raw.decode('utf-8'),{str(project):'$PROJECT',str(package):'$KERNEL_PACKAGE'})
    runtime.write(package/'python-tests.json',dict(kind='ACTUAL_PYTHON_TESTS_SYNTHETIC_COMPARISONS_REAL_PYTHON_CHILDREN_NO_LEAN',
        PID=child.pid,startedUTC=started,finishedUTC=datetime.now(timezone.utc).isoformat(),exitCode=child.returncode,
        timedOut=timeout,rawStdoutSHA256=hashlib.sha256(raw).hexdigest(),stdoutSanitized=sanitized,
        command='python -B -m unittest discover -s $KERNEL_PACKAGE -p test_kernel.py -v',
        localLeanInvocationCount=0,actualCandidateCompilationObserved=False,**runtime.NO_ACCEPT))
    print(sanitized)
    if timeout or child.returncode!=0: raise ValueError('Python tests failed')
    unchanged()
    files={p.relative_to(package).as_posix():runtime.sha(p) for p in sorted(package.rglob('*'))
        if p.is_file() and '__pycache__' not in p.parts and p.name not in ('bindings.json','seal.json')}
    if set(files)!=set(FILES)-{'bindings.json','seal.json'}: raise ValueError('exact package partition drift')
    runtime.write(package/'bindings.json',dict(files=files))
    seal=dict(state='PRIVATE_EXACT_PROOF_KERNEL_SUCCESSOR_PROPOSAL_PYTHON_TESTED_NATIVE_UNRUN',
        UTC=datetime.now(timezone.utc).isoformat(),profileSHA256=runtime.sha(package/'kernel-profile.json'),
        raw87ProfileSHA256=config['candidateProfileSHA256'],manifestSHA256=runtime.sha(package/'bindings.json'),
        originalTargetSHA256=proof_patch.ORIGINAL_SHA,candidateTargetSHA256=config['candidateTargetSHA256'],
        exactProofTokenChanges=3,originalBytesInvertiblyPreserved=True,
        actualBaselineRoots=87,actualBaselineGenerated=baseline['observedGenerated'],actualBaselineOwned=baseline['observedOwned'],
        actualBaselineSelfNativeAxioms=baseline['targetNativeAxioms'],candidateGeneratedExpectation=None,
        originalRuntimeAndSourcePinsUnchanged=True,originalSourceSealSHA256=original['sourceSealSHA256'],
        publicSafeReviewAllowlist=[p for p in FILES if not p.startswith('candidate/')],
        privateRequiredCandidateFiles=['candidate/QuantumBlockEncoding/CubicAmplitudePrimitive.lean'],
        runtimePublicAllowlist='Only existing sanitized log/JSON derivatives including complete owned-row comparison, never source/provider/private/raw hierarchy data',
        wholeSeconds=2100,budgetMiB=5120,reserveMiB=2048,threads=1,
        localLeanInvocationCount=0,actualCandidateCompilationObserved=False,installationPerformed=False,
        workflowChanged=False,productionChanged=False,gitOperations=0,networkOperations=0,
        **runtime.NO_ACCEPT)
    runtime.write(package/'seal.json',seal)
    print(json.dumps(dict(state=seal['state'],profileSHA256=seal['profileSHA256'],
        manifestSHA256=seal['manifestSHA256'],sealSHA256=runtime.sha(package/'seal.json'),files=len(FILES))))


if __name__=='__main__':
    project,public=map(Path,sys.argv[1:3]); freeze(project.resolve(),Path(__file__).parent.resolve(),public.resolve())
