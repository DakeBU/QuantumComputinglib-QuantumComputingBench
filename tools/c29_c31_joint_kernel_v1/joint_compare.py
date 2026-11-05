"""Relational actual-observation checks; no whitelist or admission authority."""
import hashlib
import json

FLAGS=dict(sourceAgreement=None,publicationBinding=None,axiomPolicyPass=None,
    nativeAccepted=False,scientificAcceptance=False,trustClosure=False)
CSP='QuantumBlockEncoding.CubicStatePreparation'
CSP_FULL='cubic-c29-kernel-only-v1/public/04-full-kernel-candidate-probe.stdout.raw.sanitized.txt'
CSP_TWO='cubic-c29-kernel-types-v2/public/05-two-kernel-types.stdout.raw.sanitized.txt'
C31_STREAM='30-observe.stdout.raw.sanitized.txt'
CSP_TAGS=('C29_BINDING_JSON','C29_ROOT_JSON','C29_GENERATED_JSON','C29_SUMMARY_JSON')
TWO_TAGS=('C29_TWO_BINDING_JSON','C29_TWO_TYPE_JSON','C29_TWO_SUMMARY_JSON')
C31_TAGS=('C31_BINDING_JSON','C31_ROOT_JSON','C31_GENERATED_JSON','C31_SUMMARY_JSON')
TYPE_FIELDS=('actualName','actualPrivate','actualKind','kernelRootPresent','universeParameters',
    'typePrettyExplicit','actualHasValueAllowOpaque','isUnsafe','selfOccursInAxioms')


def require(value,message):
    if not value: raise ValueError(message)
def sha(data): return hashlib.sha256(data).hexdigest()
def pairs(values):
    out={}
    for k,v in values: require(k not in out,'duplicate JSON key'); out[k]=v
    return out
def parse(data): return json.loads(data,object_pairs_hook=pairs)
def stable(value): return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def strict(text,tags):
    result={t:[] for t in tags}; terminal=False
    for line in text.splitlines():
        require(line.strip() and not terminal,'blank/post-terminal output')
        tag,sep,payload=line.partition(' '); require(sep and tag in result,'unknown/truncated output')
        row=parse(payload); require(type(row) is dict,'non-object output'); result[tag].append(row)
        terminal=tag==tags[-1]
    require(terminal and len(result[tags[-1]])==1,'missing/duplicate terminal summary'); return result


def receipt_partition(files,prefix):
    manifest=parse(files[prefix+'raw-derivation-receipts.json'])['files']; names=[r['publicRelativePath'] for r in manifest]
    actual={n[len(prefix):] for n in files if n.startswith(prefix)}
    require(len(names)==len(set(names)) and set(names)==actual-{'raw-derivation-receipts.json'},'baseline receipt partition')
    for row in manifest:
        require(sha(files[prefix+row['publicRelativePath']])==row['publicSHA256'],'baseline public bytes hash')
    return dict(files=len(actual),receiptRows=len(manifest),rawBytesAbsentForRedactedDerivatives=True)


def common_rows(parsed,root_tag,gen_tag):
    roots=parsed[root_tag]; generated=parsed[gen_tag]; rows=roots+generated
    names=[r['actualName'] for r in rows]
    require(names and len(names)==len(set(names)),'zero/duplicate/colliding actual names')
    for row in rows:
        require(row['kernelRootPresent'] is True and row['isUnsafe'] is False and row['selfOccursInAxioms'] is False,'kernel/unsafe/self observation')
        require(row['actualKind']!='axiomInfo','new target-owned axiom')
        axes=row['axioms']; require(type(axes) is list and len(axes)==len(set(axes)),'axiom vector')
        require(not any('native_decide' in a or 'sorry' in a.lower() for a in axes),'native/sorry dependency')
        require(row.get('sourceAgreement') is None and row.get('nativeAccepted') is False,'acceptance claim')
    return {r['actualName']:r for r in roots},{r['actualName']:r for r in generated}


def overlay_two(csp,two):
    require([len(two[t]) for t in TWO_TAGS]==[1,2,1],'two full types partition')
    binding=two[TWO_TAGS[0]][0]; summary=two[TWO_TAGS[-1]][0]
    require(binding['targetModule']==CSP and binding['freshOleanPathComparisonPassed'] is True,'two fresh binding')
    require(binding['ppDeepTerms'] is True and binding['ppMaxSteps']==2000000 and binding['maxRecDepth']==10000,'two pp bounds')
    require(summary['completed']==2 and summary['valuesPrinted'] is False,'two type summary')
    allrows={r['actualName']:dict(r) for r in csp[CSP_TAGS[1]]+csp[CSP_TAGS[2]]}
    require([r['actualName'] for r in two[TWO_TAGS[1]]]==binding['expectedNames'],'two name order')
    for ordinal,row in enumerate(two[TWO_TAGS[1]],1):
        require(row['ordinal']==ordinal and row['actualName'] in allrows,'two membership/ordinal')
        require(row['valuesPrinted'] is False and row['actualKind']=='thmInfo','two scope/kind')
        for k in ('actualKind','kernelRootPresent','universeParameters','isUnsafe','axioms','selfOccursInAxioms'):
            require(row[k]==allrows[row['actualName']][k],'two/full actual field disagreement')
        text=row['typePrettyExplicit']; require(text and not any(x in text for x in ('⋯','…','...')),'two type still omitted')
        allrows[row['actualName']]['typePrettyExplicit']=text
    require(all(r['typePrettyExplicit'] and not any(x in r['typePrettyExplicit'] for x in ('⋯','…')) for r in allrows.values()),'uncovered complete type gap')
    return allrows


def relational(old_roots,old_gen,new_roots,new_gen,old_rows=None,new_rows=None):
    require(set(old_roots)==set(new_roots),'explicit root identity changed')
    require(set(old_gen)<=set(new_gen),'candidate baseline generated declaration missing')
    a=old_rows or dict(old_roots,**old_gen); b=new_rows or dict(new_roots,**new_gen)
    old_union={x for r in a.values() for x in r['axioms']}; rows=[]
    for name in sorted(a):
        before,after=a[name],b[name]
        keys=list(TYPE_FIELDS)
        if name in old_roots: keys += ['sourceUserName','sourcePrivate','sourceKind']
        else: keys += ['userNameViaActualAPI']
        require(all(before[k]==after[k] for k in keys),'surviving signature/availability changed: '+name)
        require(set(after['axioms'])<=set(before['axioms']),'per-row recursive axiom increase: '+name)
        rows.append(dict(actualName=name,role='source-root' if name in old_roots else 'generated',
            signatureSHA256=sha(stable({k:after[k] for k in keys})),signatureUnchanged=True,
            oldAxioms=sorted(before['axioms']),newAxioms=sorted(after['axioms']),
            removedAxioms=sorted(set(before['axioms'])-set(after['axioms']))))
    additions=[]
    for name in sorted(set(b)-set(a)):
        row=b[name]; require(row['actualKind']=='thmInfo' and set(row['axioms'])<=old_union,'new generated is not a bounded ordinary theorem')
        require(not any(x in row['typePrettyExplicit'] for x in ('⋯','…')),'new helper type omitted')
        additions.append(dict(actualName=name,actualKind=row['actualKind'],universeParameters=row['universeParameters'],
            typePrettyExplicit=row['typePrettyExplicit'],axioms=row['axioms'],actualHasValueAllowOpaque=row['actualHasValueAllowOpaque']))
    return dict(explicitRoots=len(new_roots),generatedObserved=len(new_gen),ownedObserved=len(b),
        allBaselineSignaturesPreserved=True,perRowAxiomsOnlyDecrease=True,rows=rows,newGenerated=additions,
        newAxiomUnion=sorted({x for r in b.values() for x in r['axioms']}),
        generatedNamesAndCountObservedNotGuessed=True,axiomPolicyPass=None,**{k:v for k,v in FLAGS.items() if k!='axiomPolicyPass'})


def compare_c31(old_text,new_text):
    old,new=strict(old_text,C31_TAGS),strict(new_text,C31_TAGS)
    require(len(old[C31_TAGS[1]])==len(new[C31_TAGS[1]])==87,'C31 source87')
    a,ag=common_rows(old,C31_TAGS[1],C31_TAGS[2]); b,bg=common_rows(new,C31_TAGS[1],C31_TAGS[2])
    for parsed in (old,new):
        require(len(parsed[C31_TAGS[0]])==3,'C31 bindings')
        for binding in parsed[C31_TAGS[0]]:
            emitted={r['actualName'] for r in parsed[C31_TAGS[1]]+parsed[C31_TAGS[2]] if r['module']==binding['module']}
            require(len(binding['ownedNames'])==len(set(binding['ownedNames']))==binding['ownedCount'] and emitted==set(binding['ownedNames']),'C31 owned partition')
    require([r['structures'] for r in old[C31_TAGS[0]]]==[r['structures'] for r in new[C31_TAGS[0]]],'C31 structure metadata changed')
    result=relational(a,ag,b,bg)
    require(all(not any(x in r['typePrettyExplicit'] for x in ('⋯','…')) for r in list(b.values())+list(bg.values())),'C31 complete type gap')
    return result


def compare_csp(old_text,old_two,new_text,new_two,expected,original_validator,field_validator):
    old,new=strict(old_text,CSP_TAGS),strict(new_text,CSP_TAGS)
    for parsed,text in ((old,old_text),(new,new_text)):
        original_validator.validate(expected,text,0)
        roots=parsed[CSP_TAGS[1]]; generated=parsed[CSP_TAGS[2]]
        field_validator.validate_generated(generated,
            [dict(actualName=r['actualName'],actualKind=r['actualKind']) for r in generated],
            [r['actualName'] for r in roots],parsed[CSP_TAGS[-1]][0])
    a,ag=common_rows(old,CSP_TAGS[1],CSP_TAGS[2]); b,bg=common_rows(new,CSP_TAGS[1],CSP_TAGS[2])
    require(old[CSP_TAGS[0]][0]['actualStructures']==new[CSP_TAGS[0]][0]['actualStructures'],'CSP complete structure metadata changed')
    old_complete=overlay_two(old,strict(old_two,TWO_TAGS)); new_complete=overlay_two(new,strict(new_two,TWO_TAGS))
    result=relational(a,ag,b,bg,old_complete,new_complete)
    result.update(twoFullTypeSupplementsCompared=True,ordinaryDataSourceBytesUnchangedByExactProofOnlyDelta=True,
        generatedValueTextScope='Only actually available v5 fields observed; no all-body completeness requirement or claim',
        oldGeneratedValueTextOmissions=sum(any(x in (r.get('valuePrettyExplicitAllowOpaque') or '') for x in ('⋯','…')) for r in ag.values()),
        newGeneratedValueTextOmissions=sum(any(x in (r.get('valuePrettyExplicitAllowOpaque') or '') for x in ('⋯','…')) for r in bg.values()),
        actualGeneratedValueFieldsPresent=sum('valuePrettyExplicitAllowOpaque' in r for r in bg.values()))
    return result
