"""Verify immutable scoped receipts and publish the C20 author handoff."""
import ast, hashlib, json, re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
REL=HERE.relative_to(ROOT).as_posix()
ALLOWED={'propext','Classical.choice','Quot.sound'}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def strings(value):
    if isinstance(value,str): yield value
    elif isinstance(value,dict):
        for k,v in value.items(): yield str(k); yield from strings(v)
    elif isinstance(value,list):
        for v in value: yield from strings(v)
def forbidden(value):
    return bool(re.search(r'(?:(?<![A-Za-z0-9_])[A-Za-z]:[\\/]|file://(?:[A-Za-z]:|/|localhost/)|(?:^|[\s\"\'])/(?:Users|home|tmp)/)',value))
def load(name): return json.loads((HERE/name).read_text(encoding='utf-8'))
def gate(name,expected):
    data=load(name)
    assert data['exit_code']==0 and data['exact_before_after_equal']
    assert len(data['execution'])==expected
    assert all(row['exit_code']==0 for row in data['execution'])
    for row in data['execution']:
        assert sha(ROOT/row['log'])==row['log_sha256']
        assert sha(ROOT/row['command'][4])==row['output_olean_sha256']
    return data
def main():
    out=HERE/'result-v1.json'; hand=HERE/'handoff-v1.json'
    assert not out.exists() and not hand.exists(),'Frozen outputs already exist'
    suppliers=gate('gate-suppliers-v1.json',13)
    final=gate('gate-full-v2.json',2)
    assert all(sha(ROOT/p)==h for p,h in final['after_sha256'].items())
    publication=gate('gate-publication-seal-v1.json',0)
    assert all(sha(ROOT/p)==h for p,h in publication['after_sha256'].items())
    # Bind every supplier source/cache against the final current inventory.
    supplier_sources=[r['command'][5] for r in suppliers['execution']]
    for p in supplier_sources:
        assert suppliers['before_sha256'][p]==final['before_sha256'][p]==sha(ROOT/p)
    for p,h in suppliers['private_outputs_sha256'].items(): assert sha(ROOT/p)==h
    roots={}
    for row in final['execution']:
        log=(ROOT/row['log']).read_text(encoding='utf-8')
        assert 'sorryAx' not in log
        for name,values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",log):
            axioms=set(v.strip() for v in values.split(',') if v.strip())
            assert axioms<=ALLOWED,(name,axioms)
            roots[name]=sorted(axioms)
    assert len(roots)==16,roots
    main_src=(HERE/'ComplexStageTransport.lean').read_text(encoding='utf-8')
    consumers=(HERE/'ConsumerChecksC20.lean').read_text(encoding='utf-8')
    for src in [main_src,consumers]:
        stripped=re.sub(r'/-.*?-/|--[^\n]*','',src,flags=re.S)
        assert not re.search(r'\b(?:sorry|admit|axiom|native_decide|unsafe|implemented_by)\b',stripped)
    finite=load('finite-v1.json')
    assert finite['passed'] and finite['tests']==7
    assert finite['source_before_sha256']==finite['source_after_sha256']==sha(HERE/'test_discriminators.py')
    assert finite['log_sha256']==sha(HERE/'finite-v1.log')
    path_hits=[]
    public=list(HERE.glob('*.json'))+list(HERE.glob('*.log'))+list(HERE.glob('*.py'))
    for p in public:
        content=p.read_text(encoding='utf-8')
        vals=list(strings(json.loads(content))) if p.suffix=='.json' else [content]
        if p.suffix=='.py':
            vals=[node.value for node in ast.walk(ast.parse(content)) if isinstance(node,ast.Constant) and isinstance(node.value,str)]
        path_hits += [p.name for value in vals if forbidden(value)]
    assert not path_hits,path_hits
    failures=[]
    for name,archive in [('gate-search-v1.json','search-v1.failed.lean'),('gate-search-v2.json','search-v2-consumers.failed.lean')]:
        raw=load(name); assert raw['exit_code']!=0
        failures.append({'classification':'IMPLEMENTATION_FAILED','receipt':ref(HERE/name),'source_archive':ref(HERE/archive),'unexpected_axiom_in_failed_diagnostic':'sorryAx; rejected, never accepted as proof'})
    failures.append({'classification':'IMPLEMENTATION_FAILED','layer':'publication scanner only','receipt':ref(HERE/'publication-scan-failure-v1.json'),'private_original_script':ref(HERE/'.cache/freeze-v1.py'),'finalizer_failure_not_mathematical_counterexample':True})
    evidence=[ref(HERE/n) for n in ['gate-statement-seal-v1.json','gate-suppliers-v1.json','gate-search-v3.json','gate-full-v1.json','gate-full-v2.json','gate-publication-seal-v1.json','finite-v1.json','finite-v1.log','statement-seal-v1.md']]
    evidence += [ref(HERE/n) for n in ['ComplexStageTransport.lean','ConsumerChecksC20.lean','replay.py','test_discriminators.py','freeze.py','freeze_v3.py','publication-scan-refinement-v2.json','.gitignore']]
    result={
      'schema_version':1,'status':'PROVED_LOCAL_PENDING_DISTINCT_REVIEW','author':'/root/literal_complex_review_c18 (C20 author only)',
      'frontier':'SP-HERMITE-POLY-002 C_INTERNAL_PROVIDER: actual complex saved-stage precision and chronological transport',
      'scientific_ROOT':False,'independent_review':'pending distinct C20 reviewer; old C18 review credit does not apply',
      'mathematical_delta':'Actual saved interval midpoint/error transported to complex Euclidean induced operator norm on the full canonical physical carrier; contraction and Valid derived internally; actual flatten evaluator identified and chronological product/apply growth bounded.',
      'actual_definitions':{'carrier':'EuclideanSpace Complex (PrimitiveBasis width)','nominal':'toEuclideanCLM (evalPrimitiveCircuit (compileWord word))','surrogate':'toEuclideanCLM (namedCast (stageCenter word degree bits))','error':'stageEta word degree bits cast to Real'},
      'kernel_axioms':roots,'root_count':6,'consumer_count':10,
      'gates':{'fresh_supplier_source_modules':13,'fresh_final_author_source_modules':2,'final_input_pin_count':final['input_count'],'exact_final_before_after':True,'supplier_sources_and_outputs_still_match':True,'private_outputs_only':True,'finite_tests':7,'finite_tests_symbolic_or_uniform_certificate':False},
      'commands':[['lake','env','lean','-o',r['command'][4],r['command'][5]] for r in suppliers['execution']+final['execution']],
      'portable_replay':['python',REL+'/replay.py','--record','NEW_RECORD'],'authoritative_finalizer_command':['python',REL+'/freeze_v3.py'],'finalizer_scope':'Frozen original finalizer and failed scanner diagnostic retained unchanged; refined publication copy freeze_v3.py is authoritative and separately pinned by publication seal.', 'publication_pin_count':publication['input_count'],'publication_path_scan':{'decoded_json_keys_and_values':True,'python_ast_literal_paths':True,'logs':True,'absolute_local_path_hits':0},
      'statement_seal':'gate-statement-seal-v1.json predates all C20 proof source; exact final public roots match sealed contract',
      'binder_audit':{'TYPING':['width'],'CONTRACT_DATA':['word/words','degree','bits','arbitrary complex x'],'EXCESS':[],'public_Valid_or_error_or_operator_equality_premise':False},
      'conventions':['canonical primitiveBasisLEEquiv q0LSB','signed theta/2 RY','CX control/target and instruction distinctness','all spectator assignments and terminal garbage','no real-vector restriction, clean sector or phase quotient','width zero has one complex coordinate','chronological later-left products'],
      'source_construction_graph':[
        {'node':'actual stage midpoint enclosure','requires':['literal saved interval semantics','signed RY/CX row semantics'],'evidence':'StageOperatorBound.stage_max_entry_error'},
        {'node':'actual complex entry enclosure','requires':['actual stage midpoint enclosure','C18 namedCast_word canonical exact evaluator'],'evidence':'stage_entry_error'},
        {'node':'complex Euclidean induced operator error','requires':['complex triangle inequality','finite Cauchy-Schwarz','complex norm-square identity','card PrimitiveBasis = 2^width','actual complex entry enclosure'],'evidence':'stage_operator_error'},
        {'node':'nominal contraction','requires':['canonical primitive circuit unitarity','L2 matrix norm = Euclidean CLM norm'],'evidence':'nominal_contraction'},
        {'node':'internal Valid','requires':['actual eta nonnegative','complex Euclidean induced operator error','nominal contraction'],'evidence':'actual_stages_valid'},
        {'node':'actual flatten and error','requires':['later-left append evaluator law','internal Valid','existing nonunitary growth theorem'],'evidence':'nominalProduct_eq_flatten; actual_flatten_product_error; actual_flatten_apply_error'}],
      'lean_dependency_graph':{'imports':['LiteralComplexAdapter','ChronologicalTransport','QuantumBlockEncoding.PrimitiveRyPerturbation'],'precision_supplier':'HermiteSavedStageInterpreter.stage_max_entry_error','nonneg_supplier':'HermiteNominalStageTransport.stageEta_nonneg','product_supplier':'ExperimentalNonunitaryTransport.product_error_le'},
      'compressed_quantum_spine':'literal saved interval midpoint/error -> canonical complex evaluator/full Euclidean norm -> internally valid stages -> chronological actual flatten bound',
      'functor_hypergraph':['actual real-to-complex inclusion AND canonical basis reindexing preserve the whole matrix','toEuclideanCLM preserves subtraction AND multiplication AND identity','growth recursion composes stage error without assuming surrogate unitarity'],
      'definition_audit':'All actual stage fields literal; no new quantum foundations or semantic carrier. Generic entry bound is an internal lemma whose premise is discharged from actual intervals.',
      'unsafe_reducibility_audit':'C20 has no unsafe/reducibility option. Imported frozen C18 local allowUnsafeReducibility exposes gridSize only for elaboration; all six transitive roots print only ordinary axioms.',
      'failure_class':'NONE (final gate); historical attempts separately IMPLEMENTATION_FAILED','historical_failures':failures,
      'salvage_audit':{'promoted':['generic arbitrary-complex induced-operator lemma','actual complex entry bridge','internally derived Valid','chronological flatten product/apply interface'],'discarded':[],'preserved_private':['two failed source snapshots'],'pending':['distinct review','canonical production admission','purification']},
      'process_memory_ids':['QBE-PM-LOW-TOKEN-CONTROL-PLANE','QBE-PM-DENSE-CHECK-SMALL-INSTANCE','QBE-PM-VERIFIER-SEMANTIC-LEVEL'],
      'direction_fingerprint':'actual-complex-entry-enclosure; arbitrary-complex-CS; canonical-unitary-nominal; chronological-nonunitary-growth',
      'expected_information_gain':'Close the previously missing actual complex-stage precision interface without a supplied validity premise.',
      'parallel_admission':'No subagents; one bounded author task. Distinct parent-assigned review is next, not self-review.',
      'common_blind_spot_audit':'Own symbolic and finite convention checks are author evidence; independent review pending.',
      'default_route':'Direct complex enclosure/Frobenius-style Cauchy-Schwarz bound selected: preserves exactly N*maxRadius=stageEta without introducing a real-vector reduction or opnorm-extension theorem. No competing verified C20 route claimed.',
      'purification_exposition_seal':'NOT_PURIFIED; author source-construction/Lean graph and compressed explanation supplied, independent Exposition Seal and production integration pending.',
      'reusable_insight':'Complex induced norm can be bounded directly from the actual real-valued interval entry radius using complex coefficient magnitudes and real Cauchy-Schwarz; no restriction on vector phases is needed.',
      'open_obligations':['full QR','finite-bit implementation and runtime refinement','physical-local/global support lift','uniform family error/resource budget','scientific X2/ROOT','distinct C20 review','repository build/Tests/site gates at parent integration','canonical admission and purification'],
      'integration_boundary':'No production/task/registry/history/Git or old C18 artifact writes. Full repository/site gates deliberately not run because they write outside the assigned subtree; parent must run before admission.',
      'residual_risk':'High confidence in scoped kernel statement; author-only semantic/source reconstruction is not independent admission. Finite Python model is supplementary and not runtime refinement.',
      'recommended_next':'Distinct fresh-context reviewer derives sealed actual complex-stage bridge and checks all before/after source/cache pins; parent integrates only after review plus repository/publication gates.',
      'evidence':evidence,'all_writes_stopped_after_handoff':True}
    assert not any(forbidden(s) for s in strings(result))
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    handoff={'status':result['status'],'result':ref(out),'source':[ref(HERE/'ComplexStageTransport.lean'),ref(HERE/'ConsumerChecksC20.lean')],'final_gate':ref(HERE/'gate-full-v2.json'),'supplier_gate':ref(HERE/'gate-suppliers-v1.json'),'seal':ref(HERE/'gate-statement-seal-v1.json'),'publication_seal':ref(HERE/'gate-publication-seal-v1.json'),'root_count':6,'consumer_count':10,'fresh_supplier_count':13,'finite_test_count':7,'pin_count':final['input_count'],'publication_pin_count':publication['input_count'],'all_pins_unchanged':True,'absolute_local_path_hits':0,'scientific_ROOT':False,'independent_review':'pending distinct C20 reviewer','ALL_WRITES_STOPPED':True}
    assert not any(forbidden(s) for s in strings(handoff))
    hand.write_text(json.dumps(handoff,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'result':ref(out),'handoff':ref(hand),'pin_count':final['input_count'],'ALL_WRITES_STOPPED':True},indent=2))
if __name__=='__main__': main()
