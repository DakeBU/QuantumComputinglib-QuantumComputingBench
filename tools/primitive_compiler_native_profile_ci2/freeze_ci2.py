"""Freeze the private proposal, actual authorized failure analysis and Python receipt."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import runner_v2
import verify_ci1


def freeze(project, package, public, artifact):
    profile = json.loads((package / 'ci2-profile.json').read_text(encoding='utf-8'))
    base, base_package = runner_v2.load_base(project, profile)
    base_profile = json.loads((base_package / 'profile.json').read_text(encoding='utf-8'))
    prior = sys.dont_write_bytecode; sys.dont_write_bytecode = True
    try:
        api = base.load_shared(project, base_profile)
    finally:
        sys.dont_write_bytecode = prior
    analysis = verify_ci1.verify(public, artifact)
    if analysis != json.loads((package / 'actual-ci1-analysis.json').read_text(encoding='utf-8')):
        raise ValueError('first failure analysis changed')
    if api.sha(package / 'actual-ci1-analysis.json') != profile['firstFailureAnalysisSHA256']:
        raise ValueError('first failure analysis binding changed')
    api.verify_pins(base_package, profile['baseFiles'])
    api.verify_pins(project, base_profile['projectInputs'])
    original = project / 'runs/hermite-curriculum-goal-20261008/scratch/primitive-compiler-decoder-c31'
    if api.sha(original / 'source-formal-seal.json') != profile['originalSourceSealSHA256'] or \
            api.sha(original / 'native-profile-v1/proposal-seal.json') != profile['baseProposalSealSHA256']:
        raise ValueError('original seals changed')
    workflow = project / '.github/workflows/c31-native-diagnostic.yml'
    if api.sha(workflow) != profile['existingWorkflowSHA256']:
        raise ValueError('original workflow changed')
    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', str(package), '-p', 'test*.py', '-v']
    child = subprocess.Popen(command, cwd=project, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        raw, _ = child.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        child.kill(); child.communicate()
        raise RuntimeError('Python-only tests timed out; killed own test child')
    sanitized = api.redact(raw.decode('utf-8'), {str(project): '$PROJECT', str(package): '$CI2_PACKAGE'})
    receipt = dict(kind='ACTUAL_LOCAL_PYTHON_TESTS_SYNTHETIC_RESOURCES_REAL_PYTHON_CHILDREN_NO_LEAN',
        UTC=datetime.now(timezone.utc).isoformat(), PID=child.pid, exitCode=child.returncode,
        command='python -B -m unittest discover -s $CI2_PACKAGE -p test*.py -v',
        rawStdoutSHA256=hashlib.sha256(raw).hexdigest(), stdoutSanitized=sanitized,
        localLeanInvocationCount=0, **runner_v2.NO_ACCEPT)
    api.write_json(package / 'python-only-tests.json', receipt)
    print(sanitized)
    if child.returncode != 0:
        raise ValueError('Python gate failed')
    api.verify_pins(base_package, profile['baseFiles'])
    api.verify_pins(project, base_profile['projectInputs'])
    allow = ['README.md', 'HANDOFF.md', 'actual-ci1-analysis.json', 'verify_ci1.py',
             'build_ci2_profile.py', 'ci2-profile.json', 'resource_gate.py', 'runner_v2.py',
             'test_ci2.py', 'workflow-one-line.PROPOSAL.patch', 'freeze_ci2.py',
             'python-only-tests.json', 'ci2-bindings.json', 'ci2-seal.json']
    files = {p.relative_to(package).as_posix(): api.sha(p) for p in sorted(package.rglob('*'))
             if p.is_file() and '__pycache__' not in p.parts and p.name not in ('ci2-bindings.json', 'ci2-seal.json')}
    if set(files) != set(allow) - {'ci2-bindings.json', 'ci2-seal.json'}:
        raise ValueError('unexpected/missing new proposal file')
    api.write_json(package / 'ci2-bindings.json', dict(files=files))
    seal = dict(state='PRIVATE_CI2_FINITE_GATED_LINUX_ONLY_PROPOSAL_PYTHON_TESTED_NATIVE_UNRUN',
        UTC=datetime.now(timezone.utc).isoformat(), ci2ProfileSHA256=api.sha(package / 'ci2-profile.json'),
        ci2ManifestSHA256=api.sha(package / 'ci2-bindings.json'),
        firstFailureZIP_SHA256=api.sha(artifact), firstFailureMembers=21,
        firstFailurePreserved=True, actualFailureAnalysisSHA256=api.sha(package / 'actual-ci1-analysis.json'),
        base14VerifiedUnchanged=True, baseManifestSHA256=profile['baseManifestSHA256'],
        baseRaw87ProfileSHA256=profile['baseProfileSHA256'], baseProposalSealSHA256=profile['baseProposalSealSHA256'],
        originalSourceSealSHA256=profile['originalSourceSealSHA256'], sourceConfigPinsVerified=31,
        oldWorkflowSHA256=profile['existingWorkflowSHA256'], oldWorkflowChanged=False,
        publicSafeReviewAllowlist=allow,
        runtimePublicAllowlist='Existing sanitized public derivatives only, including ci2 pre/post/observation JSON; no raw/binaries/provider/source/private upload',
        resourceGate='Linux GitHub CI, complete MemAvailable + cgroup v2 visible ancestor accounting; 5120MiB+2048MiB; unknown/v1/hidden/Windows refused',
        localLeanInvocationCount=0, localLinuxHardwareGateObserved=False,
        observedPriorCI1NativeProcesses=3, scientificCollectorSuccessObserved=False,
        installationPerformed=False, canonicalChanges=0, gitOperations=0, networkOperations=0,
        sourceAgreement=None, axiomPolicyPass=None, publicationBinding=None,
        scientificAcceptance=False, nativeAccepted=False, trustClosure=False)
    api.write_json(package / 'ci2-seal.json', seal)
    print(json.dumps(dict(state=seal['state'], profileSHA256=seal['ci2ProfileSHA256'],
        manifestSHA256=seal['ci2ManifestSHA256'], sealSHA256=api.sha(package / 'ci2-seal.json'),
        base14Unchanged=True, sourceOnlySealUnchanged=True, firstFailureZIPUnchanged=True)))


if __name__ == '__main__':
    project, public, artifact = map(Path, sys.argv[1:4])
    freeze(project.resolve(), Path(__file__).parent.resolve(), public.resolve(), artifact.resolve())
