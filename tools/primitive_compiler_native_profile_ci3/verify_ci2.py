"""Verify only the four authorized sanitized CI2 artifact members, never raw captures."""
import hashlib
import json
from pathlib import PurePosixPath
import zipfile

ZIP_SHA = '88cf00aa01965456ffd2c37ec61c7abcf0a84bdd3f0e79ff9aef55522b9e1a88'
EXPECTED = {'ci2-01-help.preflight.json','input-bindings.json','raw-derivation-receipts.json','result.json'}


def sha(data): return hashlib.sha256(data).hexdigest()


def verify(public, artifact):
    if sha(artifact.read_bytes()) != ZIP_SHA: raise ValueError('actual CI2 ZIP drift')
    members = []
    with zipfile.ZipFile(artifact) as archive:
        names = [i.filename for i in archive.infolist() if not i.is_dir()]
        if set(names) != EXPECTED or len(names) != 4: raise ValueError('exact four-member partition drift')
        for name in sorted(names):
            p = PurePosixPath(name)
            if p.is_absolute() or len(p.parts) != 1: raise ValueError('unsafe member')
            raw = archive.read(name)
            if (public / name).read_bytes() != raw: raise ValueError('extracted bytes differ')
            members.append(dict(name=name,bytes=len(raw),sha256=sha(raw)))
    if {p.name for p in public.iterdir() if p.is_file()} != EXPECTED: raise ValueError('unexpected public member')
    def read(name): return json.loads((public/name).read_text(encoding='utf-8'))
    receipts = read('raw-derivation-receipts.json')['files']
    if len(receipts) != 3 or {r['publicRelativePath'] for r in receipts} != EXPECTED-{'raw-derivation-receipts.json'}:
        raise ValueError('derivative partition mismatch')
    for r in receipts:
        if sha((public/r['publicRelativePath']).read_bytes()) != r['publicSHA256']:
            raise ValueError('public derivative SHA mismatch')
    pre, result = read('ci2-01-help.preflight.json'), read('result.json')
    inputs=read('input-bindings.json')
    if inputs['profileSHA256'] != pre['binding']['baseRaw87ProfileSHA256'] or \
            inputs['packageManifestSHA256'] != pre['binding']['base14FileManifestSHA256'] or \
            len(inputs['projectInputs']) != 31 or len({p['relativePath'] for p in inputs['projectInputs']}) != 31:
        raise ValueError('actual source/profile input binding incomplete')
    if pre['observationComplete'] is not False or pre['gatePassed'] is not False or \
            pre['failureType'] != 'FileNotFoundError' or 'NO_CHILD_STARTED' not in result['failure']:
        raise ValueError('actual failure contract changed')
    if pre['budgetMiB'] != 5120 or pre['reserveMiB'] != 2048 or pre['requiredHeadroomBytes'] != 7516192768:
        raise ValueError('old finite gate drift')
    if len(pre['cgroups']) != 2 or len(pre['fileReads']) != 9 or \
            any(g['memoryMaxRaw'] != 'max' for g in pre['cgroups']):
        raise ValueError('actual partial resource observations changed')
    return dict(evidenceLayer='ACTUAL_CI2_PREFLIGHT_FAILURE_NO_NATIVE_CHILD_NOT_MATHEMATICAL_EVIDENCE',
        authorizedZIP_SHA256=ZIP_SHA, memberCount=4, publicMemberHashes=members,
        derivativeReceiptCount=3, derivativeReceiptsVerified=True,
        failedLabel='01-help', wrapperPID=pre['wrapperPID'], startedUTC=pre['startedUTC'], finishedUTC=pre['finishedUTC'],
        nativeChildrenStarted=0, nativeChildEvidencePresent=False,
        memAvailableBytes=pre['memAvailableBytes'], requiredHeadroomBytes=pre['requiredHeadroomBytes'],
        completeNonrootRows=2, successfulFileReads=9, completeResourceObservation=False,
        finiteEffectiveHeadroomEstablished=False, failureType=pre['failureType'],
        failureLogicalPathRecorded='failedReadLogicalPath' in pre,
        rootFailureLocationProven=False,
        failureAnalysis='A file read failed after two nonroot observations. The sanitized old snapshot has no failed logical coordinate; it does not identify the missing file as a root interface. The documented root-only API mismatch is an independently identified implementation defect, not a certified location of this actual exception.',
        noCompletedTargetOrCollectorEvidence=True, profileBinding=pre['binding'],
        oldFailurePreserved=True, sourceAgreement=None, axiomPolicyPass=None, publicationBinding=None,
        scientificAcceptance=False, nativeAccepted=False, trustClosure=False)
