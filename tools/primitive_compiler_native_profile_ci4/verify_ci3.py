"""Authorized sanitized CI3 artifact verifier; never opens raw capture metadata/logs."""
import hashlib
import json
from pathlib import PurePosixPath
import zipfile

ZIP_SHA='84aa925f945f807d5eaedbd4dfc158d6c4dffc95a65885d159974cb77722adf9'
EXPECTED={'ci2-01-help.preflight.json','input-bindings.json','raw-derivation-receipts.json','result.json'}


def sha(data): return hashlib.sha256(data).hexdigest()


def verify(public,artifact):
    if sha(artifact.read_bytes())!=ZIP_SHA: raise ValueError('actual ZIP drift')
    members=[]
    with zipfile.ZipFile(artifact) as archive:
        names=[i.filename for i in archive.infolist() if not i.is_dir()]
        if set(names)!=EXPECTED or len(names)!=4: raise ValueError('four-member partition drift')
        for name in sorted(names):
            p=PurePosixPath(name)
            if p.is_absolute() or len(p.parts)!=1: raise ValueError('unsafe member')
            data=archive.read(name)
            if (public/name).read_bytes()!=data: raise ValueError('ZIP/extracted mismatch')
            members.append(dict(name=name,bytes=len(data),sha256=sha(data)))
    if {p.name for p in public.iterdir() if p.is_file()}!=EXPECTED: raise ValueError('unexpected member')
    def read(name): return json.loads((public/name).read_text(encoding='utf-8'))
    receipts=read('raw-derivation-receipts.json')['files']
    if len(receipts)!=3 or {r['publicRelativePath'] for r in receipts}!=EXPECTED-{'raw-derivation-receipts.json'}:
        raise ValueError('derivative partition drift')
    for r in receipts:
        if sha((public/r['publicRelativePath']).read_bytes())!=r['publicSHA256']: raise ValueError('derivative hash mismatch')
    pre,result,inputs=read('ci2-01-help.preflight.json'),read('result.json'),read('input-bindings.json')
    failed=pre['readAttempts'][-1]
    expected_self=('cgroup:[4026531835]').encode('utf-8')
    ns=pre['namespaceReads']
    if len(ns)!=1 or ns[0]['logicalPath']!='$PROC/self/ns/cgroup' or ns[0]['bytes']!=len(expected_self) or \
        ns[0]['sha256']!=sha(expected_self) or ns[0]['hashScope']!='READLINK_TARGET_UTF8':
        raise ValueError('actual self namespace fingerprint not verified')
    if failed['logicalPath']!='$PROC/pid1/ns/cgroup' or failed['exceptionType']!='PermissionError' or \
        failed['errno']!=13 or failed['status']!='READ_ERROR' or pre['failedReadLogicalPath']!=failed['logicalPath'] or \
        pre['observationComplete'] is not False or pre['gatePassed'] is not False or \
        'NO_CHILD_STARTED' not in result['failure'] or pre['cgroups']!=[] or pre['rootObservation'] is not None:
        raise ValueError('actual no-child permission failure changed')
    if inputs['profileSHA256']!=pre['binding']['baseRaw87ProfileSHA256'] or len(inputs['projectInputs'])!=31:
        raise ValueError('source binding incomplete')
    return dict(evidenceLayer='ACTUAL_CI3_PREFLIGHT_PERMISSION_FAILURE_NO_NATIVE_NOT_MATHEMATICAL_EVIDENCE',
        authorizedZIP_SHA256=ZIP_SHA,memberCount=4,publicMemberHashes=members,derivativeReceiptCount=3,
        derivativeReceiptsVerified=True,wrapperPID=pre['wrapperPID'],startedUTC=pre['startedUTC'],finishedUTC=pre['finishedUTC'],
        actualContext=pre['context'],contextSHAIsActualArtifactValueNotTaskHeadAssumption=True,
        parentReportedOfficialJobAPIHeadPrefix='d9ab49566fc7',
        jobHeadEvidenceSource='Parent separately reports official job API; this worker did not read raw metadata or independently query that API',
        executedCheckoutSHA=None,checkoutBoundary='Artifact GITHUB_SHA and parent-reported API head are distinct observations; neither is asserted here as exact executed checkout. The independent 31 source/config content hashes remain separately verified.',
        selfReadlinkBytes=ns[0]['bytes'],selfReadlinkSHA256=ns[0]['sha256'],
        selfReservedInitFingerprintVerified=True,PID1Observed=False,PID1ReadAttempted=True,
        failedLogicalPath=pre['failedReadLogicalPath'],failureType='PermissionError',errno=13,
        nativeChildrenStarted=0,nonrootAncestorReadingsCompleted=0,rootApplicabilityObserved=False,
        effectiveHeadroomEstablished=False,memAvailableBytes=pre['memAvailableBytes'],
        policyChange='New contract may use the sufficient self implementation fingerprint; this does not repair or rewrite the failed CI3 observation.',
        profileBinding=pre['binding'],noCompletedTargetOrCollectorEvidence=True,oldFailurePreserved=True,
        sourceAgreement=None,axiomPolicyPass=None,publicationBinding=None,scientificAcceptance=False,nativeAccepted=False,trustClosure=False)
