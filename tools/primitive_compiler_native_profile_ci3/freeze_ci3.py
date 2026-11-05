"""Seal only the new private root-API proposal after actual Python-only tests."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import runner_v3
import verify_ci2

ALLOW = ['README.md','HANDOFF.md','PRIMARY-SOURCES.md','actual-ci2-analysis.json','verify_ci2.py',
    'build_profile.py','ci3-profile.json','resource_gate_v3.py','runner_v3.py','test_ci3.py',
    'workflow-one-line.PROPOSAL.patch','freeze_ci3.py','python-only-tests.json',
    'ci3-bindings.json','ci3-seal.json']


def freeze(project, package, public, artifact):
    profile=runner_v3.read(package/'ci3-profile.json')
    prior, prior_package=runner_v3.load_ci2(project,profile)
    ci2_profile=runner_v3.read(prior_package/'ci2-profile.json')
    base,base_package=prior.load_base(project,ci2_profile)
    base_profile=runner_v3.read(base_package/'profile.json')
    old=sys.dont_write_bytecode; sys.dont_write_bytecode=True
    try: api=base.load_shared(project,base_profile)
    finally: sys.dont_write_bytecode=old
    original=project/'runs/hermite-curriculum-goal-20261008/scratch/primitive-compiler-decoder-c31'
    def unchanged():
        runner_v3.pins(prior_package,profile['priorFiles'])
        if api.sha(prior_package/'ci2-bindings.json') != profile['priorManifestSHA256'] or \
                api.sha(prior_package/'ci2-seal.json') != profile['priorSealSHA256']:
            raise ValueError('old CI2 seal/manifest drift')
        api.verify_pins(base_package,ci2_profile['baseFiles'])
        if api.sha(base_package/'proposal-bindings.json') != ci2_profile['baseManifestSHA256'] or \
                api.sha(base_package/'proposal-seal.json') != ci2_profile['baseProposalSealSHA256'] or \
                api.sha(original/'source-formal-seal.json') != ci2_profile['originalSourceSealSHA256'] or \
                api.sha(original/'native-profile-v1/proposal-seal.json') != ci2_profile['baseProposalSealSHA256']:
            raise ValueError('original seals drift')
        api.verify_pins(project,base_profile['projectInputs'])
        actual_inputs=runner_v3.read(public/'input-bindings.json')['projectInputs']
        if {p['relativePath']:p['sha256'] for p in actual_inputs} != base_profile['projectInputs']:
            raise ValueError('actual CI2 source/config vector does not match immutable raw87 profile')
        api.verify_pins(project,{base_profile['sharedInstrumentation']['path']:base_profile['sharedInstrumentation']['sha256']})
        if api.sha(project/'.github/workflows/c31-native-diagnostic.yml') != profile['existingWorkflowSHA256']:
            raise ValueError('existing workflow changed')
        if verify_ci2.verify(public,artifact) != runner_v3.read(package/'actual-ci2-analysis.json') or \
                api.sha(package/'actual-ci2-analysis.json') != profile['priorFailureAnalysisSHA256']:
            raise ValueError('actual failure boundary drift')
    unchanged()
    receipts=[]
    for label,location,pattern in [('new-ci3',package,'test_ci3.py'),('unchanged-ci2',prior_package,'test_ci2.py')]:
        env=dict(os.environ,C31_TEST_PROJECT=str(project),TMP=str(package),TEMP=str(package))
        cmd=[sys.executable,'-B','-m','unittest','discover','-s',str(location),'-p',pattern,'-v']
        started=datetime.now(timezone.utc).isoformat()
        proc=subprocess.Popen(cmd,cwd=project,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        timed_out=False
        try: raw,_=proc.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            timed_out=True; proc.kill(); raw,_=proc.communicate()
        text=api.redact(raw.decode('utf-8'),{str(project):'$PROJECT',str(package):'$CI3_PACKAGE'})
        receipts.append(dict(suite=label,PID=proc.pid,exitCode=proc.returncode,timedOut=timed_out,
            startedUTC=started,finishedUTC=datetime.now(timezone.utc).isoformat(),
            command='python -B -m unittest discover -s $'+label.upper().replace('-','_')+' -p '+pattern+' -v',
            rawStdoutSHA256=hashlib.sha256(raw).hexdigest(),stdoutSanitized=text))
        print(text)
        if timed_out or proc.returncode != 0: raise ValueError('actual Python tests failed: '+label)
    unchanged()
    api.write_json(package/'python-only-tests.json',dict(
        kind='ACTUAL_PYTHON_TESTS_SYNTHETIC_RESOURCE_FIXTURES_REAL_PYTHON_CHILDREN_NO_LEAN',
        UTC=datetime.now(timezone.utc).isoformat(), suites=receipts,
        sourceRuntimeHashes={name:api.sha(package/name) for name in
            ('resource_gate_v3.py','runner_v3.py','test_ci3.py','freeze_ci3.py')},
        localLeanInvocationCount=0, actualLinuxResourceGateObserved=False, **runner_v3.NO_ACCEPT))
    files={p.relative_to(package).as_posix():api.sha(p) for p in sorted(package.rglob('*'))
        if p.is_file() and '__pycache__' not in p.parts and p.name not in ('ci3-bindings.json','ci3-seal.json')}
    if set(files) != set(ALLOW)-{'ci3-bindings.json','ci3-seal.json'}:
        raise ValueError('unexpected/missing proposal file')
    api.write_json(package/'ci3-bindings.json',dict(files=files))
    seal=dict(state='PRIVATE_CI3_ROOT_API_CORRECTION_PROPOSAL_PYTHON_TESTED_NATIVE_UNRUN',
        UTC=datetime.now(timezone.utc).isoformat(),direction=profile['direction'],
        profileSHA256=api.sha(package/'ci3-profile.json'),manifestSHA256=api.sha(package/'ci3-bindings.json'),
        actualCI2FailureZIP_SHA256=verify_ci2.ZIP_SHA,actualCI2Members=4,actualCI2DerivativesVerified=3,
        actualCI2NativeChildren=0,actualCI2MissingFileRootLocationProven=False,
        priorSealSHA256=profile['priorSealSHA256'],priorManifestSHA256=profile['priorManifestSHA256'],
        baseRaw87ProfileSHA256=ci2_profile['baseProfileSHA256'],base14ManifestSHA256=ci2_profile['baseManifestSHA256'],
        originalSourceSealSHA256=ci2_profile['originalSourceSealSHA256'],sourceConfigPinsVerified=31,
        sharedInstrumentationSHA256=base_profile['sharedInstrumentation']['sha256'],
        immutableCI2PackageUnchanged=True,immutableV1PackageUnchanged=True,originalSourceSealUnchanged=True,
        oldWorkflowSHA256=profile['existingWorkflowSHA256'],oldWorkflowChanged=False,
        rootObservation='DOCUMENTED_TRUE_ROOT_NOT_APPLICABLE_NOT_UNLIMITED',
        namespaceRecognition='Reserved initial inode implementation fingerprint; not kernel binary attestation; unknown refused',
        finiteBudgetMiB=5120,reserveMiB=2048,requiredHeadroomBytes=7516192768,threads=1,
        publicSafeReviewAllowlist=ALLOW,
        runtimePublicAllowlist='Only inherited sanitized exporter derivatives with independent raw/public SHA receipts. No raw paths/logs/binaries/source/provider upload.',
        publicPathBoundary='Logical resource coordinates retained; hierarchy paths redacted. OS-byte digests and explicit readlink-target digests unchanged; derivative digest is separate.',
        localLeanInvocationCount=0,actualLinuxResourceGateObserved=False,scientificCollectorSuccessObserved=False,
        installationPerformed=False,canonicalChanges=0,gitOperations=0,
        networkBoundary='Only authorized official Linux documentation and necessary upstream kernel source browsing',
        **runner_v3.NO_ACCEPT)
    api.write_json(package/'ci3-seal.json',seal)
    print(json.dumps(dict(state=seal['state'],profileSHA256=seal['profileSHA256'],
        manifestSHA256=seal['manifestSHA256'],sealSHA256=api.sha(package/'ci3-seal.json'),files=len(ALLOW))))


if __name__=='__main__':
    project,public,artifact=map(Path,sys.argv[1:4])
    freeze(project.resolve(),Path(__file__).parent.resolve(),public.resolve(),artifact.resolve())
