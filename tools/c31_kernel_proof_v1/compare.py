"""Complete observed row comparison, not an axiom policy/admission gate."""
import hashlib
import json

TAGS=('C31_ROOT_JSON','C31_GENERATED_JSON')
SIG=('module','actualName','userNameViaActualAPI','actualKind','kernelKind','actualPrivate',
     'kernelRootPresent','kernelTypeAndUniversesAgree','universeParameters','typePrettyExplicit',
     'typeTextScope','isUnsafe','actualHasValueAllowOpaque','actualOpaqueInfo','actualAxiomInfo',
     'sourceOpaque','valueTextRequested','valueObservation','valuePrettyExplicitAllowOpaque')


def digest(value): return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def normalized(records):
    return [dict(family=tag,identity=r.get('sourceUserName',r['actualName']),
        actualName=r['actualName'],module=r['module'],signatureSHA256=digest({k:r[k] for k in SIG}),
        axioms=sorted(r['axioms']),selfAxiom=r['selfOccursInAxioms'],unsafe=r['isUnsafe'],kind=r['actualKind'])
        for tag in TAGS for r in records[tag]]


def compare(baseline,records):
    old=baseline['rows']; new=normalized(records); removed=set(baseline['targetNativeAxioms'])
    def key(r): return r['family'],r['module'],r['identity']
    oldmap={key(r):r for r in old}; newmap={key(r):r for r in new}
    if len(oldmap)!=len(old) or len(newmap)!=len(new): raise ValueError('duplicate row comparison key')
    oldroots={k for k in oldmap if k[0]=='C31_ROOT_JSON'}
    newroots={k for k in newmap if k[0]=='C31_ROOT_JSON'}
    if len(oldroots)!=87 or oldroots!=newroots: raise ValueError('old/new 87-root vector drift')
    diffs=[]; issues=[]
    structures={b['module']:b['structures'] for b in records['C31_BINDING_JSON']}
    if structures!=baseline['structures']: issues.append('actual structure field/constructor/projection metadata drift')
    for k,a in oldmap.items():
        b=newmap.get(k)
        if b is None:
            diffs.append(dict(identity=list(k),state='REMOVED_GENERATED',old=a,new=None)); continue
        wanted=set(a['axioms'])-removed; got=set(b['axioms'])
        same=a['signatureSHA256']==b['signatureSHA256']
        row=dict(identity=list(k),state='SURVIVING',signatureUnchanged=same,
            oldSignatureSHA256=a['signatureSHA256'],newSignatureSHA256=b['signatureSHA256'],
            oldAxioms=a['axioms'],oldMinus3=sorted(wanted),newAxioms=b['axioms'],
            oldMinus3EqualsNew=wanted==got,removedAxioms=sorted(set(a['axioms'])-got),
            addedAxioms=sorted(got-set(a['axioms'])),extraRemovedBeyondNative3=sorted(wanted-got),
            additionsBeyondOldMinus3=sorted(got-wanted))
        diffs.append(row)
        if not same: issues.append('surviving signature drift: '+a['actualName'])
        if got-wanted: issues.append('axiom addition beyond old-minus3: '+a['actualName'])
    additions=[r for r in new if key(r) not in oldmap]
    old_union={a for r in old for a in r['axioms']}-removed
    if any(set(r['axioms'])-old_union for r in additions):
        issues.append('new generated row adds dependencies beyond the old observed union minus3')
    if any(r['actualName'] in removed or set(r['axioms'])&removed for r in new):
        issues.append('one of exact old native axioms or its dependency survives')
    if any(r['selfAxiom'] or r['kind']=='axiomInfo' or r['unsafe'] for r in new):
        issues.append('candidate has actual self-axiom/axiomInfo/unsafe declaration')
    # New generated identities/count are observations, never an invented baseline.
    return dict(status='EXACT_PROOF_SUCCESSOR_COMPARISON_COMPLETE_NOT_ACCEPTANCE' if not issues else
        'CANDIDATE_COMPARISON_DIFFERENCE_REQUIRES_REVIEW',issues=issues,
        oldRoots=len(oldroots),newRoots=len(newroots),oldOwned=len(old),newOwned=len(new),
        candidateGeneratedObserved=sum(r['family']=='C31_GENERATED_JSON' for r in new),
        oldRowsCompared=len(diffs),perOldRow=diffs,newGeneratedRows=additions,
        actualStructureMetadataUnchanged=structures==baseline['structures'],
        targetNativeAxioms=sorted(removed),signatureMethod='Exact SHA of complete actual explicit pretty-type/universe/kind/value-availability observations; not lossless Expr serialization or cross-environment definitional equality',
        axiomBoundary='Every surviving row compares actual recursive axioms with old minus the exact three. Extra removals are reported, not a whitelist; additions are refused. New generated rows are all reported, not guessed by count/name.',
        sourceAgreement=None,axiomPolicyPass=None,publicationBinding=None,
        scientificAcceptance=False,nativeAccepted=False,trustClosure=False)
