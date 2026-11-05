"""Verify only the authorized sanitized artifact; no raw metadata access."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
import entry

ZIP_SHA='7c395ab385ffb36a60b569b8688085155c54e50f3a7acc474e80c24b98ecf732'


def observe(path):
    before=entry.sha(path)
    if before!=ZIP_SHA: raise ValueError('first failure ZIP pin drift')
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if len(names)!=26 or len(set(names))!=26 or any('/' in n or '\\' in n for n in names):
            raise ValueError('first failure artifact partition')
        parse=lambda n:json.loads(z.read(n))
        receipts=parse('raw-derivation-receipts.json')['files']
        if len(receipts)!=25 or {r['publicRelativePath'] for r in receipts}!=set(names)-{'raw-derivation-receipts.json'}:
            raise ValueError('sanitized receipt partition')
        for row in receipts:
            if hashlib.sha256(z.read(row['publicRelativePath'])).hexdigest()!=row['publicSHA256']:
                raise ValueError('sanitized member digest mismatch')
        failure=parse('result.json'); outer=parse('kernel-successor-result.json')
        expected="[Errno 2] No such file or directory: '$CANDIDATE_WORKSPACE/tools/cubic_c29_diagnostic/runner.py'"
        if failure.get('failureType')!='FileNotFoundError' or failure.get('failure')!=expected:
            raise ValueError('unexpected first failure')
        processes={label:parse(label+'.result.json') for label in ('01-help','02-prefix')}
        for label,row in processes.items():
            started=parse(label+'.started.json')
            if row.get('exitCode')!=0 or row.get('timedOut') is not False or row.get('PID')!=started.get('PID'):
                raise ValueError('first failure child receipt disagreement')
        if any(n.startswith(('11-','12-','13-','30-')) for n in names): raise ValueError('unexpected target/collector receipt')
        result=dict(kind='INDEPENDENT_SANITIZED_FIRST_FAILURE_INSPECTION',artifactZIP_SHA256=before,
            members=len(names),verifiedPublicDerivativeReceipts=len(receipts),
            memberSHA256={n:hashlib.sha256(z.read(n)).hexdigest() for n in sorted(names)},
            failure=failure,outerStatus=outer,observedProcesses=processes,
            actualTargetCompilationObserved=False,actualCollectorObservation=False,
            absenceClaimBoundary='No target or collector receipts in these 26 sanitized members; not a claim about unuploaded filesystem state',
            scopeGap='load_shared callback fixes executing API origin, not unchanged base.run shadow sharedInstrumentation pin verification',
            sourceReadingBoundary='Sanitized technical artifact only; no raw job/artifact metadata, author natural source, reviewer or registry',
            **entry.NO_ACCEPT)
    if entry.sha(path)!=before: raise ValueError('ZIP changed during observation')
    return result


if __name__=='__main__':
    result=observe(Path(sys.argv[1]))
    with (Path(__file__).parent/'actual-first-failure.json').open('x',encoding='utf-8',newline='\n') as out:
        json.dump(result,out,indent=2); out.write('\n')
