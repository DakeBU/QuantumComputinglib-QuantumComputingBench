"""Immutable public sanitized derivatives, exact raw provenance and scoped verdict."""
import hashlib, json, re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
REL=HERE.relative_to(ROOT).as_posix()
AUTHOR=ROOT/'experiments/hermite-polynomial/precision/literal-complex-adapter'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p): return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def save(path,data):
    if path.exists(): raise SystemExit('Immutable artifact exists: '+path.name)
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
def sanitize(text):
    text=text.replace(str(ROOT),'<repo>').replace(ROOT.as_posix(),'<repo>')
    return re.sub(r'[A-Za-z]:[\\/][^\r\n\'"<>]*','<private-path>',text)
def transform(data):
    if isinstance(data,str): return sanitize(data)
    if isinstance(data,list): return [transform(x) for x in data]
    if isinstance(data,dict):
        out={k:transform(v) for k,v in data.items()}
        if 'command' in data:
            cmd=data['command']; out['command']=[('lake' if str(cmd[0]).lower().endswith('lake.exe') else '.venv/Scripts/python.exe')]+[sanitize(str(x)).replace('<repo>\\','').replace('<repo>/','') for x in cmd[1:]]
        return out
    return data
def main():
    names=['pre-verdict-seal-v1','dependency-seal-v3','full-source-v1','consumers-v1','consumers-v2','consumers-v3','consumers-v4','finite-checks-v1']
    raw={n:json.loads((HERE/(n+'.json')).read_text(encoding='utf-8')) for n in names}
    if raw['full-source-v1']['exit_code'] or raw['consumers-v4']['exit_code']: raise SystemExit('Successful focused gates required')
    if not all(raw[n]['exact_before_after_equal'] for n in names if n!='finite-checks-v1'): raise SystemExit('Input drift')
    pins=raw['consumers-v4']['after_sha256']
    if any(sha(ROOT/p)!=h for p,h in pins.items()): raise SystemExit('Final input drift')
    successful=(HERE/'consumers-v4-0.log').read_text(encoding='utf-8')
    axiomrows=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]+)\]",successful,re.S)
    if len(axiomrows)!=11: raise SystemExit('Expected 11 actual axiom roots')
    allow={'propext','Classical.choice','Quot.sound'}
    if any(set(x.strip() for x in row.split(','))-allow for _,row in axiomrows): raise SystemExit('Unexpected axiom')
    if re.search(r'\bsorryAx\b|error:',successful): raise SystemExit('Failed consumer or placeholder')
    sourcefiles=[AUTHOR/(n+'.lean') for n in ['BasisCompatibility','LiteralComplexAdapter','ConsumerChecks']]+[HERE/'ReviewConsumers.lean']
    def code_text(p):
        text=re.sub(r'/\-.*?\-/', '', p.read_text(encoding='utf-8'),flags=re.S)
        return re.sub(r'--[^\n]*','',text)
    if any(re.search(r'\b(sorry|admit|axiom)\b',code_text(p)) for p in sourcefiles): raise SystemExit('Source placeholder audit')
    result=json.loads((AUTHOR/'result-v1.json').read_text(encoding='utf-8'))
    for b in result['sources']+[result['full_source_gate'],result['statement_seal'],result['replay'],result['finite_screen']]:
        if sha(ROOT/b['path'])!=b['sha256']: raise SystemExit('Author binding drift')
    exports=[]
    for name in names:
        path=HERE/(name+'.json'); normalized=transform(raw[name])
        entry={'raw_receipt':bind(path),'raw_retained_privately':True,'sanitization':'Absolute local path strings normalized; displayed commands are sanitized historical commands, not a claim of a different execution.','receipt':normalized}
        for row in normalized.get('execution',[]):
            old=ROOT/row['log']; out=HERE/('public-'+old.name)
            if out.exists(): raise SystemExit('Immutable log exists')
            out.write_text(sanitize(old.read_text(encoding='utf-8')),encoding='utf-8')
            row['raw_log_sha256']=sha(old); row['log']=out.relative_to(ROOT).as_posix(); row['log_sha256']=sha(out)
        exports.append(entry)
    evidence={'schema_version':1,'reviewer':'/root/literal_complex_review_c18','historical_raw_records':exports,'final_input_pins_sha256':pins,'final_input_count':len(pins),'actual_axiom_roots':{n:[x.strip() for x in row.split(',')] for n,row in axiomrows},'sanitized_publication_only':True}
    # Detect decoded Windows paths, not raw JSON escapes or Lean binders.
    def scan(x):
        if isinstance(x,str) and re.search(r'[A-Za-z]:[\\/]',x): raise SystemExit('Local path leak')
        if isinstance(x,list):
            for y in x: scan(y)
        if isinstance(x,dict):
            for k,y in x.items(): scan(k); scan(y)
    scan(evidence)
    save(HERE/'review-evidence-public-v1.json',evidence)
    verdict={'schema_version':1,'cycle':18,'reviewer':'/root/literal_complex_review_c18','status':'ACCEPT_INTERNAL_EXACT_OPERATOR_BRIDGE','evidence_class':'C_INTERNAL_PROVIDER','author_result':bind(AUTHOR/'result-v1.json'),'author_handoff':bind(AUTHOR/'handoff-v1.json'),'author_sources':[bind(p) for p in sourcefiles[:3]],'pre_verdict_reconstruction':bind(HERE/'pre-verdict-reconstruction.md'),'review_evidence':bind(HERE/'review-evidence-public-v1.json'),'independent_consumer':bind(HERE/'ReviewConsumers.lean'),'counts':{'whole_source_modules':9,'symbolic_consumer_roots':9,'printed_axiom_roots':11,'finite_tests':7,'finite_entry_comparisons':raw['finite-checks-v1']['entry_comparisons'],'sealed_input_count':len(pins)},'semantic_findings':['Canonical q0LSB basis proved coordinatewise.','Signed rational theta/2 RY with all spectators fixed; no phase quotient.','CX first control second target with inherited distinctness; inverse row action correct because CX is involutive.','Arbitrary real matrix input, all rows/columns and complete terminal carrier; arbitrary complex vectors are valid consumers.','Chronological foldl equals later-left matrix composition.','Width0 has one scalar basis and only an empty instruction word.'],'independent_comparison':'Pre-verdict reconstruction agrees with frozen author signatures and actual proof bodies. No excess bridge hypothesis, replacement semantic carrier or restricted terminal sector. Exact scalar inclusion and canonical reindexing are sufficient.','allowUnsafeReducibility_audit':'Read installed Lean.ReducibilityAttrs implementation: option bypasses reducibility-attribute validation for elaborator indexing, not kernel proof checking. gridSize has existing body 2^n. Successful independent consumer uses explicit matrix typing and no such option; actual roots contain only propext/Classical.choice/Quot.sound.','failure_history':{'author_search_receipts':6,'author_class':'IMPLEMENTATION_FAILED','own_consumers_v1':'IMPLEMENTATION_FAILED: HMul type inference did not unfold gridSize; exact failed source and raw log retained privately.','own_consumers_v2':'IMPLEMENTATION_FAILED: broad simp unfolded algebra equivalence before map_mul; failed chronology root printed sorryAx and is rejected. Source/log retained privately.','own_consumers_v3':'IMPLEMENTATION_FAILED: simp-only left carrier-definitional reflexivity; failed chronology root printed sorryAx and is rejected. Source/log retained privately.','resolution':'Explicit flat result typing, simp-only composition and kernel rfl compile successfully in consumers-v4. No failed receipt or source overwritten.'},'open_boundaries':['complex stageEta/operator norm transport','local-to-global/support lifts','QR','uniform error budget','finite-bit complexity','classical runtime refinement','scientific X2 acceptance','scientific ROOT acceptance','lake build and Tests integration','site/publication admission','main admission','purification/Exposition Seal'],'process_memory_ids':[],'direction_fingerprint':'independent-full-carrier-inverse-row-and-spectator-review','expected_information_gain':'Detect convention drift and kernel-placeholder contamination without authoring adapter code','parallel_review':'Distinct reviewer; no child agents; common register/order/phase blind-spot audit completed only for this internal bridge.','installed_Lean_source_audit':{'relative_to_toolchain':'src/lean/Lean/ReducibilityAttrs.lean','sha256':'7fa5b42ddae7219a582c6d64aad75f0751c41b011eef15313beff61fb45b3e0e','lean_executable_sha256':'dd86e9b24990b1da425ea4af910f016e4db8f9a25c9ddad27bc6bee3690e677f','lake_executable_sha256':'a1aebb13fc502ae9190745c6b3bd2101d0fec39f030cfc07b1993799c2374644'},'scientific_ROOT':False,'production_admission':False,'public_PURIFIED':False,'ALL_WRITES_STOPPED':True}
    save(HERE/'review-verdict-v1.json',verdict)
    handoff={'verdict':bind(HERE/'review-verdict-v1.json'),'status':verdict['status'],'failure_class':'NONE_ON_ACCEPTED_FINAL_GATE','initial_failures_preserved':True,'scope':REL,'all_writes_stopped':True,'parent_owned':['Git commit/push','canonical integration/admission','repository/site gates'],'scientific_ROOT':False,'public_PURIFIED':False}
    save(HERE/'review-handoff-v1.json',handoff)
    for name in ['review-evidence-public-v1.json','review-verdict-v1.json','review-handoff-v1.json']: print(name,sha(HERE/name))
if __name__=='__main__': main()
