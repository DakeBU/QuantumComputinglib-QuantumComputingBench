"""Candidate diagnostic-output validator. Does not invoke Lean or grant acceptance.

Usage: python validate-output.py expected-roots.json stdout.raw exit-code
An exit-code argument must be the ACTUAL native subprocess exit, not inferred
from stdout. Preserve all raw inputs externally before running this parser.
"""
import json,sys
from pathlib import Path

def validate(expected,stdout,exit_code):
    if exit_code!=0:raise ValueError('native subprocess failed; partial data is not complete')
    tags=('C29_BINDING_JSON','C29_ROOT_JSON','C29_GENERATED_JSON','C29_SUMMARY_JSON')
    records={t:[] for t in tags}
    for line in stdout.splitlines():
        for tag in tags:
            if line.startswith(tag+' '):records[tag].append(json.loads(line[len(tag)+1:]))
    if len(records[tags[0]])!=1 or len(records[tags[3]])!=1:
        raise ValueError('need exactly one binding and one terminal summary')
    roots=records[tags[1]];gen=records[tags[2]]
    specs=expected['roots'];binding=records[tags[0]][0];summary=records[tags[3]][0]
    if len(specs)!=319 or len(roots)!=len(specs):raise ValueError('explicit root count mismatch')
    if sum(s['sourcePrivate'] for s in specs)!=50:raise ValueError('private input count mismatch')
    if sum(s['sourceKind']=='opaque' for s in specs)!=7:raise ValueError('opaque input count mismatch')
    if sum(s['sourceKind']=='structure' for s in specs)!=11:raise ValueError('structure input count mismatch')
    actual_names=[]
    for i,(spec,row) in enumerate(zip(specs,roots),1):
        for k in ('sourceUserName','sourcePrivate','sourceKind'):
            if row[k]!=spec[k]:raise ValueError(f'explicit source identity mismatch at {i}: {k}')
        if row['ordinal']!=i:raise ValueError('ordinal gap/reorder')
        if row['actualPrivate']!=spec['sourcePrivate']:raise ValueError('actual private flag mismatch')
        if row['kernelRootPresent'] is not True:raise ValueError('kernel root absent')
        if row['actualKind'] not in ('axiomInfo','defnInfo','thmInfo','opaqueInfo','quotInfo','inductInfo','ctorInfo','recInfo'):
            raise ValueError('unknown actual ConstantInfo kind')
        if not isinstance(row['typePrettyExplicit'],str) or not row['typePrettyExplicit']:
            raise ValueError('missing actual signature')
        if not isinstance(row['axioms'],list) or not all(isinstance(a,str) for a in row['axioms']):
            raise ValueError('invalid actual axiom array')
        if not isinstance(row['universeParameters'],list):raise ValueError('missing universe list')
        if spec['sourceKind']=='opaque' and not row['opaqueClassification'].startswith('SOURCE_OPAQUE_'):
            raise ValueError('missing opaque observation')
        if row['sourceAgreement'] is not None or row['nativeAccepted'] is not False:
            raise ValueError('diagnostic made forbidden acceptance claim')
        actual_names.append(row['actualName'])
    if len(set(actual_names))!=319:raise ValueError('duplicate actual explicit identity')
    generated_names=[r['actualName'] for r in gen]
    if len(set(generated_names))!=len(gen) or set(generated_names)&set(actual_names):
        raise ValueError('duplicate or conflated generated identities')
    for row in gen:
        if row['includedIn319ExplicitRootCount'] is not False:raise ValueError('generated conflated with lexical roots')
    if binding['freshOleanPathComparisonPassed'] is not True:raise ValueError('fresh artifact comparison failed')
    if binding['expectedNamedRoots']!=319 or len(binding['actualStructures'])!=11:raise ValueError('binding counts wrong')
    if summary['status']!='RUNTIME_DIAGNOSTIC_COMPLETE_NOT_SCIENTIFIC_ACCEPTANCE':raise ValueError('missing complete status')
    if summary['explicitRootsCompleted']!=319 or summary['explicitPrivateCompleted']!=50:
        raise ValueError('summary root counts wrong')
    if summary['actualStructureCount']!=11:raise ValueError('summary structure count wrong')
    if summary['generatedTargetOwnedConstants']!=len(gen):raise ValueError('generated count mismatch')
    if summary['observedTargetOwnedConstants']!=319+len(gen) or binding['observedTargetOwnedConstants']!=319+len(gen):
        raise ValueError('target-owned partition mismatch')
    if summary['allExplicitNamesResolvedUniquely'] is not True:raise ValueError('resolver not complete')
    for k in ('axiomPolicyPass','sourceAgreement','publicationBinding'):
        if summary[k] is not None:raise ValueError('unexpected scientific acceptance')
    if summary['nativeAccepted'] is not False:raise ValueError('unexpected native acceptance')
    return {'diagnosticOutputComplete':True,'explicitRoots':319,'privateRoots':50,
            'generatedObserved':len(gen),'sourceAgreement':None,'publicationBinding':None,
            'nativeAccepted':False,'axiomPolicyPass':None}

if __name__=='__main__':
    expected=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    stdout=Path(sys.argv[2]).read_text(encoding='utf-8',errors='strict')
    print(json.dumps(validate(expected,stdout,int(sys.argv[3])),ensure_ascii=False))
