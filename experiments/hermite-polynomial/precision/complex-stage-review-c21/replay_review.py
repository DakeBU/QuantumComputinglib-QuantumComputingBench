"""Independent review replay; private cache, immutable receipts, robust import inventory."""
import hashlib,json,os,re,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
P='experiments/hermite-polynomial/precision/'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def sanitize(s):
    s=s.replace(str(ROOT),'<repo>').replace(ROOT.as_posix(),'<repo>')
    return re.sub(r'[A-Za-z]:[\\/][^\r\n\'"<>]*','<private-path>',s)
MODULES=[(n,n+'.lean') for n in ['QuantumBlockEncoding/PrimitiveCircuit','QuantumBlockEncoding/PrimitiveSemantics','QuantumBlockEncoding/PrimitiveBasisLE']]
MODULES += [('FiniteTrig',P+'finite-trig/FiniteTrig.lean'),('SavedRounding',P+'saved-rounding/SavedRounding.lean'),('SavedStageInterpreter',P+'saved-stage-interpreter/SavedStageInterpreter.lean'),('StageOperatorBound',P+'saved-stage-interpreter/StageOperatorBound.lean'),('NonunitaryTransport',P+'nonunitary-transport/NonunitaryTransport.lean'),('NominalStageTransport',P+'nominal-stage-transport/NominalStageTransport.lean'),('ChronologicalTransport',P+'nominal-stage-transport/ChronologicalTransport.lean')]
MODULES += [(n,P+'literal-complex-adapter/'+n+'.lean') for n in ['BasisCompatibility','LiteralComplexAdapter','ConsumerChecks']]
MODULES += [(n,P+'complex-stage-transport-c20/'+n+'.lean') for n in ['ComplexStageTransport','ConsumerChecksC20']]
MODULES += [('ReviewChecksC21',HERE.relative_to(ROOT).as_posix()+'/ReviewChecksC21.lean')]
def imports(s):
    s=re.sub(r'/\-.*?\-/',' ',s,flags=re.S)
    s=re.sub(r'--[^\n]*','',s)
    result=[]
    for line in s.splitlines():
        m=re.match(r'^\s*(?:(?:public|private|meta)\s+)*import\s+(.+)$',line)
        if m: result.extend(re.findall(r'[A-Za-z_][A-Za-z0-9_.]*',m.group(1)))
    return result
assert imports('public meta import A.B C.D\nmeta import E.F')==['A.B','C.D','E.F']
def inventory():
    paths={ROOT/p for _,p in MODULES}
    paths.update(ROOT/p for p in ['AGENTS.md','HARNESS.md','docs/proof-digestion-protocol.md','docs/theorem-publication-protocol.md','docs/evidence-routed-memory-protocol.md','reports/process-memory.json','tasks/SP-HERMITE-POLY-002.md','lean-toolchain','lakefile.lean','lake-manifest.json'])
    for name in ['complex-stage-transport-c20','literal-complex-adapter','literal-complex-review-c18','saved-stage-interpreter','nominal-stage-transport']:
        paths.update(p for p in (ROOT/(P+name)).rglob('*') if p.is_file())
    bases=[ROOT]+list((ROOT/'.lake/packages').iterdir())
    libs=[ROOT/'.lake/build/lib/lean']+[p/'.lake/build/lib/lean' for p in bases[1:]]
    selected={n.replace('/','.') for n,_ in MODULES}
    inherited={};missing=[];queue=list(paths);seen=set()
    while queue:
        p=queue.pop()
        if p in seen or p.suffix!='.lean': continue
        seen.add(p)
        for mod in imports(p.read_text(encoding='utf-8-sig')):
            rel=mod.replace('.','/')
            source=next((b/(rel+'.lean') for b in bases if (b/(rel+'.lean')).exists()),None)
            if source: paths.add(source);queue.append(source)
            if mod not in selected:
                cache=next((b/(rel+'.olean') for b in libs if (b/(rel+'.olean')).exists()),None)
                if cache:
                    paths.add(cache);inherited[mod]={'source':source.relative_to(ROOT).as_posix() if source and source.is_relative_to(ROOT) else None,'cache':cache.relative_to(ROOT).as_posix(),'provenance':'byte-pinned inherited cache; source-to-cache equality NOT independently established'}
                else: missing.append(mod)
    return {p.relative_to(ROOT).as_posix():sha(p) for p in sorted(paths) if p.exists()},inherited,sorted(set(missing))
def main():
    receipt=HERE/'gate-review-v1.json'
    if receipt.exists(): raise SystemExit('Immutable receipt exists')
    before,inherited,missing=inventory()
    (HERE/'pins-before-v1.json').write_text(json.dumps(before,indent=2)+'\n',encoding='utf-8')
    env=os.environ.copy();env['LEAN_PATH']=str(HERE/'.cache');env['PYTHONDONTWRITEBYTECODE']='1'
    rows=[];code=0
    for i,(name,source) in enumerate(MODULES):
        output=HERE/'.cache'/(name+'.olean');output.parent.mkdir(parents=True,exist_ok=True)
        command=['lake','env','lean','-o',output.relative_to(ROOT).as_posix(),source]
        t=time.perf_counter();r=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='utf-8',errors='replace')
        log=HERE/('gate-review-v1-'+str(i)+'.log');log.write_text(sanitize(r.stdout),encoding='utf-8')
        rows.append({'command':command,'exit_code':r.returncode,'seconds':time.perf_counter()-t,'source_sha256':sha(ROOT/source),'log':log.relative_to(ROOT).as_posix(),'log_sha256':sha(log),'output_sha256':sha(output) if output.exists() else None})
        print(json.dumps(rows[-1]),flush=True);print(sanitize(r.stdout),flush=True)
        code=r.returncode
        if code: break
    after={p:sha(ROOT/p) for p in before}
    data={'exit_code':code,'execution':rows,'before_pins':'pins-before-v1.json','before_pins_sha256':sha(HERE/'pins-before-v1.json'),'after_sha256':after,'exact_before_after_equal':before==after,'inherited_cache_provenance':inherited,'unresolved_import_caches':missing,'import_parser':'combined public/private/meta and multiple module names; comments stripped','trust_boundary':'Selected source modules freshly compiled; transitive inherited cache source correspondence remains partial closure, NOT full clean source build.','scientific_ROOT':False,'public_source_blind_review':False}
    receipt.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');print('RECEIPT',sha(receipt),flush=True)
    return code
if __name__=='__main__': raise SystemExit(main())
