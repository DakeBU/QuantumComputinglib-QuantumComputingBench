"""Inspect only the explicitly authorized sanitized CI1 directory and ZIP."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

ZIP_SHA = 'a2edbb904f6be270e3b1c7dabc1090808390667ecf95f8dee323dbbe9de70dd6'


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def verify(public, artifact):
    if sha_bytes(artifact.read_bytes()) != ZIP_SHA:
        raise ValueError('authorized artifact ZIP hash mismatch')
    members = []
    with zipfile.ZipFile(artifact) as archive:
        names = [i.filename for i in archive.infolist() if not i.is_dir()]
        if len(names) != 21 or len(set(names)) != 21:
            raise ValueError('ZIP exact member count/uniqueness mismatch')
        for name in names:
            path = PurePosixPath(name)
            if path.is_absolute() or '..' in path.parts or len(path.parts) != 1:
                raise ValueError('unexpected public artifact layout')
            data = archive.read(name)
            if (public / name).read_bytes() != data:
                raise ValueError('ZIP/extracted public member bytes differ')
            members.append(dict(name=name, bytes=len(data), sha256=sha_bytes(data)))
    if {p.name for p in public.iterdir() if p.is_file()} != set(names):
        raise ValueError('public directory differs from exact ZIP members')
    def read(name):
        return json.loads((public / name).read_text(encoding='utf-8'))
    receipts = read('raw-derivation-receipts.json')['files']
    if len(receipts) != 20 or len({r['publicRelativePath'] for r in receipts}) != 20:
        raise ValueError('invalid derivative receipt partition')
    for receipt in receipts:
        if sha_bytes((public / receipt['publicRelativePath']).read_bytes()) != receipt['publicSHA256']:
            raise ValueError('sanitized derivative hash mismatch')
    if {r['publicRelativePath'] for r in receipts} != set(names) - {'raw-derivation-receipts.json'}:
        raise ValueError('incomplete derivative receipts')
    setup = read('11-target.setup.json'); result = read('11-target.result.json')
    started = read('11-target.started.json'); stderr = (public / '11-target.stderr.raw.sanitized.txt').read_text()
    stdout = (public / '11-target.stdout.raw.sanitized.txt').read_bytes()
    if started['PID'] != result['PID'] or result['PID'] != 13289:
        raise ValueError('first target PID binding mismatch')
    if result['exitCode'] != -6 or result['timedOut'] is not False or stdout != b'':
        raise ValueError('first target process observations changed')
    if '--memory=3072' not in setup['argv'] or '--threads=1' not in setup['argv']:
        raise ValueError('first target budget/threads not bound')
    if 'lean::memory_exception' not in stderr or 'excessive memory consumption' not in stderr:
        raise ValueError('actual memory exception text absent')
    if result['stdoutSHA256'] != sha_bytes(stdout) or result['stderrSHA256'] != \
            sha_bytes((public / '11-target.stderr.raw.sanitized.txt').read_bytes()):
        raise ValueError('raw/sanitized first-process stream hashes differ unexpectedly')
    for label in ('01-help', '02-prefix'):
        if read(label + '.result.json')['exitCode'] != 0:
            raise ValueError('bootstrap not a success')
    inputs = read('input-bindings.json'); environment = read('runtime-environment.json')
    if inputs['profileSHA256'] != '72c0931c4c62906835d831742a3b797b381e947fbb8e3ecb58c4ad62aaa64473' \
            or environment['profileSHA256'] != inputs['profileSHA256']:
        raise ValueError('C31 raw profile binding mismatch')
    return dict(evidenceLayer='ACTUAL_SANITIZED_CI1_PROCESS_FAILURE_NOT_LEAN_MATHEMATICAL_EVIDENCE',
        authorizedZIP_SHA256=ZIP_SHA, memberCount=21, publicMemberHashes=members,
        derivativeReceiptCount=20, derivativeReceiptsVerified=True,
        bootstrapExitCodes=[read(t + '.result.json')['exitCode'] for t in ('01-help', '02-prefix')],
        target='QuantumBlockEncoding.PrimitiveMacros', nativeBudgetMiB=3072, nativeThreads=1,
        firstTargetProcess=result, targetStartedPID=started['PID'], emptyTargetStdout=True,
        stderrObserved=stderr.strip(),
        classification='LEAN_INTERNAL_MEMORY_EXCEPTION_SIGABRT_NOT_OS_OOM_PROOF',
        missingResourceEvidence=['No CI1 MemAvailable/cgroup headroom measurements in this bundle',
                                 'No peak native RSS measurement establishes a sufficient replacement cap'],
        completedFreshTargetReceiptPresent='fresh-target-cohort.json' in names,
        collectorOrSignatureReceiptPresent=any('30-observe' in n or 'completeness' in n for n in names),
        absenceBoundary='No completed target/collector evidence is present. This ZIP cannot prove absence of unuploaded partial filesystem artifacts.',
        baseProfileSHA256=inputs['profileSHA256'], baseManifestSHA256=inputs['packageManifestSHA256'],
        sourceAgreement=None, axiomPolicyPass=None, publicationBinding=None,
        scientificAcceptance=False, nativeAccepted=False, trustClosure=False)


if __name__ == '__main__':
    import sys
    public, artifact, output = map(Path, sys.argv[1:4])
    value = verify(public, artifact)
    with output.open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    print(json.dumps({k:v for k,v in value.items() if k not in ('publicMemberHashes', 'stderrObserved')}))
