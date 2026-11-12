"""Seal honest scoped acceptance after reviewer gates, retaining partial cache closure."""
import ast,hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
P='experiments/hermite-polynomial/precision/'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    target=HERE/'review-result-v1.json';handoff=HERE/'review-handoff-v1.json'
    if target.exists() or handoff.exists():raise SystemExit('Immutable review exists')
    gate=json.loads((HERE/'gate-review-v1.json').read_text(encoding='utf-8'))
    assert gate['exit_code']==0 and len(gate['execution'])==16
    assert gate['exact_before_after_equal']
    finite=json.loads((HERE/'finite-review-v1.json').read_text(encoding='utf-8'))
    assert finite['passed'] and len(finite['cases'])==35
    old={'result-v1.json':'964aa2cce737273aa6e4b2d2f15f9721bcef066aecafe35b564bada7c6d8f9fe','handoff-v1.json':'faa255364e402730ec86978cabb7ba346fdbf45c0fd9e9c38d5f0237a24369d0'}
    for p,h in old.items():assert sha(ROOT/(P+'complex-stage-transport-c20/'+p))==h
    axioms={}
    for row in gate['execution'][13:]:
        s=(ROOT/row['log']).read_text(encoding='utf-8')
        assert 'sorryAx' not in s
        axiom_pattern=r"'([^']+)' depends on axioms:"+r"\s*\[([^\]]*)\]"
        for name,body in re.findall(axiom_pattern,s,re.S):
            names=sorted(x.strip() for x in body.split(',') if x.strip())
            assert set(names)<={'propext','Classical.choice','Quot.sound'}
            axioms[name]=names
    assert len(axioms)==18
    signatures=(ROOT/gate['execution'][-1]['log']).read_text(encoding='utf-8')
    assert all('@'+x+' :' in signatures for x in ['stage_operator_error','nominal_contraction','actual_stages_valid','nominalProduct_eq_flatten','actual_flatten_product_error','actual_flatten_apply_error'])
    evidence=[];hits=[]
    for p in sorted(HERE.iterdir()):
        if not p.is_file():continue
        if p.suffix=='.json':
            data=json.loads(p.read_text(encoding='utf-8'))
            def strings(v):
                if isinstance(v,str):yield v
                elif isinstance(v,dict):
                    for k,x in v.items():yield k;yield from strings(x)
                elif isinstance(v,list):
                    for x in v:yield from strings(x)
            items=list(strings(data))
        elif p.suffix=='.py':
            items=[x.value for x in ast.walk(ast.parse(p.read_text(encoding='utf-8'))) if isinstance(x,ast.Constant) and isinstance(x.value,str)]
        else:items=[p.read_text(encoding='utf-8')]
        for s in items:
            pattern=r'[A-Za-z]:[\\/]'+'|'+'/'+'Users/'+'|'+'/'+'home/'+'|'+'/'+'mnt/'
            if re.search(pattern,s):hits.append(p.name)
        evidence.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
    assert not hits,hits
    data={'schema_version':1,'status':'INTERNAL_ACCEPT_WITH_EXPLICIT_PARTIAL_CACHE_CLOSURE','reviewer':'/root/complex_transport_review_c21','author':'/root/literal_complex_review_c18 acting as C20 author','author_frozen_sha256':old,'review_type':'distinct internal-provider review; NOT public source-blind admission','preproof_reconstruction':'reconstruction-before-proof-v1.md','semantic_audit':'mathematical-audit-v1.md','fresh_selected_modules':16,'fresh_author_modules':2,'reviewer_owned_symbolic_checks':['full_complex_signature','error_imaginary_part_zero'],'kernel_axioms':axioms,'finite_independent_cases':35,'all_pins_before_after_equal':True,'pin_count':len(gate['after_sha256']),'inherited_cache_count':len(gate['inherited_cache_provenance']),'unresolved_import_caches':gate['unresolved_import_caches'],'trust_boundary':gate['trust_boundary'],'import_parser':'combined public/private/meta + multiple names; available sources and caches recursively byte-pinned','binder_audit':{'TYPING':['width','CX constructor wire typing/distinctness'],'CONTRACT_DATA':['word/words','degree','bits','arbitrary complex x'],'EXCESS':[],'supplied_Valid_error_contraction_operator_equality':False},'preserved':['literal evalPrimitiveCircuit(compileWord word)','actual stageCenter and stageEta','signed theta/2','q0LSB','all terminal/spectator sectors','CX control-target direction','later-left flatten chronology','width-zero complex scalar','ordinary Euclidean induced operator norm'],'source_boundary':'SP-HERMITE-POLY-002 normalized sampled g_k target is unchanged; no substitute midpoint target','failure_class':'NONE in scoped gates; inherited cache provenance unknown is explicit trust debt, not mathematical refutation','salvage_audit':'C20 earlier failed searches/scanner artifacts preserved byte-identically; complex entry/opnorm/Valid/flatten interfaces reusable only at this internal boundary','process_memory_ids':['QBE-PM-LOW-TOKEN-CONTROL-PLANE','QBE-PM-DENSE-CHECK-SMALL-INSTANCE','QBE-PM-VERIFIER-SEMANTIC-LEVEL'],'direction_fingerprint':'independent actual-complex-stage reconstruction and direct Frobenius-bound audit; adverse full-carrier finite checks; fresh private selected-source replay','expected_information_gain':'independent accept/reject of newly authored transport without self-review credit','parallel_admission':'parent-assigned distinct uncertainty reviewer; no children','common_blind_spot_audit':'whole-carrier order/phase/CX/spectator/width-zero checked independently; no claim of complete multi-route Source Anchor audit','default_verified_route':'direct arbitrary-complex Cauchy-Schwarz bound preserves actual N*maxRadius; no competing route decision','purification_exposition_seal':'NOT_PURIFIED; internal audit only','scientific_ROOT':False,'main_admission':False,'public_source_blind_review':False,'absolute_local_path_hits':0,'open':['full clean transitive source/cache rebuild provenance','repository build/Tests/site integration gates','full QR','runtime and finite-bit refinement','physical-local/global support lift','uniform family epsilon and resources','canonical source-anchor admission and purification'],'evidence':evidence,'all_writes_stopped_after_handoff':True}
    target.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    summary={'status':data['status'],'result':{'path':target.relative_to(ROOT).as_posix(),'sha256':sha(target)},'gate':{'path':(HERE/'gate-review-v1.json').relative_to(ROOT).as_posix(),'sha256':sha(HERE/'gate-review-v1.json')},'finite_cases':35,'fresh_modules':16,'axiom_checked_roots':18,'pin_count':data['pin_count'],'before_after_equal':True,'inherited_cache_provenance':'partial closure explicitly retained','scientific_ROOT':False,'main_admission':False,'public_source_blind_review':False,'ALL_WRITES_STOPPED':True}
    handoff.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'result_sha256':sha(target),'handoff_sha256':sha(handoff),'status':data['status']}))
if __name__=='__main__':main()
