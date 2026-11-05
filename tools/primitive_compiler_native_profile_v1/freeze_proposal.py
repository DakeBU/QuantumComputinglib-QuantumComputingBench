"""Generate pending drivers, run Python-only tests, bind this private proposal."""
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

import runner


def freeze(project, package):
    profile = json.loads((package / 'profile.json').read_text(encoding='utf-8'))
    api = runner.load_shared(project, profile)
    source_seal = project / 'runs/hermite-curriculum-goal-20261008/scratch/primitive-compiler-decoder-c31/source-formal-seal.json'
    if api.sha(source_seal) != profile['sourceSealSHA256']:
        raise ValueError('original source seal changed')
    api.verify_pins(project, profile['projectInputs'])
    pending = package / 'pending-drivers'; pending.mkdir(exist_ok=False)
    drivers = runner.render_driver(profile, api, pending)
    # This is Python subprocess execution, not runner.run() or any Lean command.
    command = [sys.executable, '-m', 'unittest', 'discover', '-s', str(package), '-p', 'test*.py', '-v']
    proc = subprocess.Popen(command, cwd=project, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = proc.communicate(timeout=60)
    output = api.redact(stdout.decode('utf-8'), {str(project): '$PROJECT', str(package): '$PROFILE_PACKAGE'})
    test_receipt = dict(kind='ACTUAL_LOCAL_PYTHON_ONLY_TEST_RUN_NOT_LEAN_EVIDENCE',
        executedUTC=datetime.now(timezone.utc).isoformat(), PID=proc.pid, exitCode=proc.returncode,
        command='python -m unittest discover -s $PROFILE_PACKAGE -p test*.py -v',
        stdoutSanitized=output, leanInvocationCount=0)
    api.write_json(package / 'python-only-tests.json', test_receipt)
    print(output)
    if proc.returncode != 0:
        raise ValueError('Python implementation tests failed')
    files = {p.relative_to(package).as_posix(): api.sha(p) for p in sorted(package.rglob('*'))
             if p.is_file() and '__pycache__' not in p.parts and p.name not in
             ('proposal-bindings.json', 'proposal-seal.json')}
    api.write_json(package / 'proposal-bindings.json', dict(files=files))
    allow = ['README.md', 'HANDOFF.md', 'profile.json', 'Collector.lean', 'runner.py', 'validator.py',
             'test_profile.py', 'build_profile.py', 'freeze_proposal.py', 'python-only-tests.json',
             'instrumentation-rebind-provenance.json',
             'pending-drivers/Profile.lean', 'pending-drivers/Probe.lean',
             'c31-native-diagnostic.workflow.PROPOSAL.yml', 'proposal-bindings.json', 'proposal-seal.json']
    for relative in files:
        if relative not in allow:
            raise ValueError('unexpected proposal file')
    api.write_json(package / 'proposal-seal.json', dict(
        state='PRIVATE_PROFILE_PROPOSAL_PYTHON_TESTED_NATIVE_NOT_RUN',
        sourceSealSHA256=profile['sourceSealSHA256'], profileSHA256=api.sha(package / 'profile.json'),
        manifestSHA256=api.sha(package / 'proposal-bindings.json'),
        pendingDriverSHA256=drivers, publicSafeReviewAllowlist=allow,
        actualParentHEADReported='6e679397530552237a399f7a4abcb9abe993b419',
        parentHEADIndependentlyChecked=False, gitOperations=0, networkOperations=0,
        leanInvocationCount=0, canonicalChanges=0, requiredChecksChanged=False,
        **runner.validator.NO_ACCEPT))
    print(json.dumps(dict(state='PRIVATE_PROPOSAL_FROZEN_NATIVE_NOT_RUN',
                         profileSHA256=api.sha(package / 'profile.json'),
                         manifestSHA256=api.sha(package / 'proposal-bindings.json'),
                         proposalSealSHA256=api.sha(package / 'proposal-seal.json'),
                         sourceSealUnchanged=api.sha(source_seal) == profile['sourceSealSHA256'])))


if __name__ == '__main__':
    freeze(Path(sys.argv[1]).resolve(), Path(__file__).parent.resolve())
