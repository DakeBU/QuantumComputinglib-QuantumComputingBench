"""Freeze this C-only proposal with actual Python receipts; no native Lean or installation."""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import runner_v4
import verify_ci3

ALLOW=['README.md','HANDOFF.md','POLICY-RATIONALE.md','actual-ci3-analysis.json',
    'verify_ci3.py','development-test-provenance.json','build_profile.py','ci4-profile.json',
    'resource-contract.delta.patch','resource_gate_v4.py','runner_v4.py','test_ci4.py',
    'freeze_ci4.py','python-only-tests.json','ci4-bindings.json','ci4-seal.json']


def freeze(project,package,public,artifact):
    profile=runner_v4.read(package/'ci4-profile.json')
    ci3,p3=runner_v4.load_ci3(project,profile); profile3=runner_v4.read(p3/'ci3-profile.json')
    ci2,p2=ci3.load_ci2(project,profile3); profile2=runner_v4.read(p2/'ci2-profile.json')
    base,p1=ci2.load_base(project,profile2); profile1=runner_v4.read(p1/'profile.json')
    old=sys.dont_write_bytecode; sys.dont_write_bytecode=True
    try: api=base.load_shared(project,profile1)
    finally: sys.dont_write_bytecode=old
    original=project/'runs/hermite-curriculum-goal-20261008/scratch/primitive-compiler-decoder-c31'
    def unchanged():
        runner_v4.pins(p3,profile['priorFiles'])
        if api.sha(p3/'ci3-bindings.json')!=profile['priorManifestSHA256'] or api.sha(p3/'ci3-seal.json')!=profile['priorSealSHA256']:
            raise ValueError('CI3 immutable seal drift')
        ci3.pins(p2,profile3['priorFiles'])
        if api.sha(p2/'ci2-bindings.json')!=profile3['priorManifestSHA256'] or api.sha(p2/'ci2-seal.json')!=profile3['priorSealSHA256']:
            raise ValueError('CI2 immutable seal drift')
        api.verify_pins(p1,profile2['baseFiles'])
        if api.sha(p1/'proposal-bindings.json')!=profile2['baseManifestSHA256'] or \
            api.sha(p1/'proposal-seal.json')!=profile2['baseProposalSealSHA256'] or \
            api.sha(original/'source-formal-seal.json')!=profile2['originalSourceSealSHA256']:
            raise ValueError('V1/source immutable seal drift')
        api.verify_pins(project,profile1['projectInputs'])
        api.verify_pins(project,{profile1['sharedInstrumentation']['path']:profile1['sharedInstrumentation']['sha256']})
        actual=runner_v4.read(public/'input-bindings.json')['projectInputs']
        if len(actual)!=31 or {p['relativePath']:p['sha256'] for p in actual}!=profile1['projectInputs']:
            raise ValueError('actual independent content pins differ')
        if api.sha(project/'.github/workflows/c31-native-diagnostic.yml')!=profile['existingWorkflowSHA256']:
            raise ValueError('existing workflow changed')
        if verify_ci3.verify(public,artifact)!=runner_v4.read(package/'actual-ci3-analysis.json') or \
            api.sha(package/'actual-ci3-analysis.json')!=profile['priorFailureAnalysisSHA256']:
            raise ValueError('actual CI3 boundary drift')
    unchanged(); receipts=[]
    # Old CI3 tests create temporary directories inside their installed package.
    # This task is C-staging-write-only: test the new successor here and verify
    # every immutable prior byte, rather than mutating or relocating old tests.
    for label,location,pattern in [('new-ci4',package,'test_ci4.py')]:
        env=dict(os.environ,C31_TEST_PROJECT=str(project),TMP=str(package),TEMP=str(package))
        cmd=[sys.executable,'-B','-m','unittest','discover','-s',str(location),'-p',pattern,'-v']
        started=datetime.now(timezone.utc).isoformat()
        child=subprocess.Popen(cmd,cwd=project,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        timeout=False
        try: raw,_=child.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            timeout=True; child.kill(); raw,_=child.communicate()
        sanitized=api.redact(raw.decode('utf-8'),{str(project):'$PROJECT',str(package):'$CI4_PACKAGE'})
        receipts.append(dict(suite=label,PID=child.pid,exitCode=child.returncode,timedOut=timeout,
            startedUTC=started,finishedUTC=datetime.now(timezone.utc).isoformat(),
            command='python -B -m unittest discover -s $'+label.upper().replace('-','_')+' -p '+pattern+' -v',
            rawStdoutSHA256=hashlib.sha256(raw).hexdigest(),stdoutSanitized=sanitized))
        print(sanitized)
        if timeout or child.returncode!=0: raise ValueError('actual Python test failure: '+label)
    unchanged()
    api.write_json(package/'python-only-tests.json',dict(
        kind='ACTUAL_PYTHON_TESTS_SYNTHETIC_RESOURCES_REAL_PYTHON_CHILDREN_NO_LEAN',
        UTC=datetime.now(timezone.utc).isoformat(),suites=receipts,
        sourceRuntimeHashes={n:api.sha(package/n) for n in ('runner_v4.py','resource_gate_v4.py','test_ci4.py','freeze_ci4.py')},
        localLeanInvocationCount=0,actualLinuxResourceGateObserved=False,**runner_v4.NO_ACCEPT))
    files={p.relative_to(package).as_posix():api.sha(p) for p in sorted(package.rglob('*'))
        if p.is_file() and '__pycache__' not in p.parts and p.name not in ('ci4-bindings.json','ci4-seal.json')}
    if set(files)!=set(ALLOW)-{'ci4-bindings.json','ci4-seal.json'}: raise ValueError('package file partition drift')
    api.write_json(package/'ci4-bindings.json',dict(files=files))
    analysis=runner_v4.read(package/'actual-ci3-analysis.json')
    seal=dict(state='PRIVATE_C_ONLY_CI4_SELF_ONLY_CONTRACT_PROPOSAL_PYTHON_TESTED_NATIVE_UNRUN',
        UTC=datetime.now(timezone.utc).isoformat(),direction=profile['direction'],
        profileSHA256=api.sha(package/'ci4-profile.json'),manifestSHA256=api.sha(package/'ci4-bindings.json'),
        priorActualZIP_SHA256=verify_ci3.ZIP_SHA,priorActualMembers=4,priorDerivationReceipts=3,
        priorActualSelfFingerprintVerified=True,priorActualPID1FailurePreserved=True,priorActualNativeChildren=0,
        artifactContextSHA=analysis['actualContext']['GITHUB_SHA'],
        parentReportedOfficialJobAPIHeadPrefix=analysis['parentReportedOfficialJobAPIHeadPrefix'],
        jobHeadEvidenceSource=analysis['jobHeadEvidenceSource'],exactExecutedCheckoutSHA=None,
        priorCI3SealSHA256=profile['priorSealSHA256'],priorCI3ManifestSHA256=profile['priorManifestSHA256'],
        priorCI2SealSHA256=profile3['priorSealSHA256'],baseRaw87ProfileSHA256=profile2['baseProfileSHA256'],
        base14ManifestSHA256=profile2['baseManifestSHA256'],originalSourceSealSHA256=profile2['originalSourceSealSHA256'],
        sharedRunnerSHA256=profile1['sharedInstrumentation']['sha256'],sourceConfigPinsVerified=31,
        oldPackagesAndSealsUnchanged=True,oldWorkflowChanged=False,oldWorkflowSHA256=profile['existingWorkflowSHA256'],
        namespaceSchema='C31_CI4_RESOURCE_SELF_NAMESPACE_V1',namespacePolicy='SELF_ONLY_RESERVED_INIT_V1',
        mandatoryNamespaceReadlink='self only',PID1ReadRequested=False,PID1ObservedValue=None,
        namespaceResidual='Upstream implementation fingerprint under trusted OS/procfs assumption, not actual kernel binary attestation; unknown/dynamic refused',
        budgetMiB=5120,reserveMiB=2048,threads=1,requiredHeadroomBytes=7516192768,
        publicSafeReviewAllowlist=ALLOW,
        runtimePublicAllowlist='Only existing sanitized exporter derivatives with separate raw/public SHA receipts; no raw hierarchy/private/source/provider/log upload',
        localLeanInvocationCount=0,actualLinuxResourceGateObserved=False,scientificCollectorSuccessObserved=False,
        installationPerformed=False,workflowEditPerformed=False,gitOperations=0,canonicalChanges=0,
        networkBoundary='Only permitted primary Linux API and necessary upstream kernel source browsing',
        **runner_v4.NO_ACCEPT)
    api.write_json(package/'ci4-seal.json',seal)
    print(json.dumps(dict(state=seal['state'],profileSHA256=seal['profileSHA256'],
        manifestSHA256=seal['manifestSHA256'],sealSHA256=api.sha(package/'ci4-seal.json'),files=len(ALLOW))))


if __name__=='__main__':
    project,public,artifact=map(Path,sys.argv[1:4])
    freeze(project.resolve(),Path(__file__).parent.resolve(),public.resolve(),artifact.resolve())
