"""Portable scoped Lean checks, immutable receipts, private outputs only."""
import argparse, hashlib, json, os, re, shutil, subprocess, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
P='experiments/hermite-polynomial/precision/'
REL=HERE.relative_to(ROOT).as_posix()
MODULES=[(n,n+'.lean') for n in ['QuantumBlockEncoding/PrimitiveCircuit','QuantumBlockEncoding/PrimitiveSemantics','QuantumBlockEncoding/PrimitiveBasisLE']]
MODULES += [('FiniteTrig',P+'finite-trig/FiniteTrig.lean'),('SavedRounding',P+'saved-rounding/SavedRounding.lean'),('SavedStageInterpreter',P+'saved-stage-interpreter/SavedStageInterpreter.lean'),('StageOperatorBound',P+'saved-stage-interpreter/StageOperatorBound.lean'),('NonunitaryTransport',P+'nonunitary-transport/NonunitaryTransport.lean'),('NominalStageTransport',P+'nominal-stage-transport/NominalStageTransport.lean'),('ChronologicalTransport',P+'nominal-stage-transport/ChronologicalTransport.lean')]
MODULES += [(n,P+'literal-complex-adapter/'+n+'.lean') for n in ['BasisCompatibility','LiteralComplexAdapter','ConsumerChecks']]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(text):
    text=text.replace(str(ROOT),'<repo>').replace(ROOT.as_posix(),'<repo>')
    return re.sub(r'[A-Za-z]:[\\/][^\r\n\'"<>]*','<private-path>',text)
def inventory():
    paths={ROOT/p for _,p in MODULES}
    paths.update(ROOT/p for p in ['AGENTS.md','HARNESS.md','.agents/skills/qbe-substantive-worker/SKILL.md','docs/theorem-publication-protocol.md','docs/proof-digestion-protocol.md','docs/evidence-routed-memory-protocol.md','lean-toolchain','lakefile.lean','lake-manifest.json','QuantumBlockEncoding/PrimitiveRyPerturbation.lean','QuantumBlockEncoding/PrimitiveCircuitPerturbation.lean'])
    paths.update(ROOT/p for p in ['.agents/skills/qbe-frontier-master/SKILL.md','reports/process-memory.json',P+'saved-stage-interpreter/result-v1.json',P+'nominal-stage-transport/result-v1.json'])
    paths.add(HERE/'.gitignore')
    bases=[ROOT]+list((ROOT/'.lake/packages').iterdir())
    libs=[ROOT/'.lake/build/lib/lean']+[p/'.lake/build/lib/lean' for p in bases[1:]]
    queue=list(paths); seen=set()
    while queue:
        p=queue.pop()
        if p in seen or p.suffix!='.lean': continue
        seen.add(p)
        for mod in re.findall(r'^(?:(?:public|private|meta)\s+)*import\s+(\S+)',p.read_text(encoding='utf-8-sig'),re.M):
            module=mod.replace('.','/')
            for base in bases:
                source=base/(module+'.lean')
                if source.exists(): paths.add(source); queue.append(source); break
            for base in libs:
                cache=base/(module+'.olean')
                if cache.exists(): paths.add(cache); break
    # Old C18 package + caches and all production oleans are immutable sentinels.
    for d in ['literal-complex-adapter','literal-complex-review-c18']:
        paths.update(p for p in (ROOT/(P+d)).rglob('*') if p.is_file())
    paths.update((ROOT/'.lake/build/lib/lean/QuantumBlockEncoding').rglob('*.olean'))
    paths.update(p for p in HERE.iterdir() if p.is_file() and p.suffix in ['.lean','.md','.py'])
    paths.update((HERE/'.cache').rglob('*.olean'))
    return {p.relative_to(ROOT).as_posix():sha(p) for p in sorted(paths) if p.exists()}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--record',required=True); ap.add_argument('--seal-only',action='store_true'); ap.add_argument('--suppliers-only',action='store_true'); ap.add_argument('--reuse-suppliers',action='store_true'); args=ap.parse_args()
    receipt=HERE/('gate-'+args.record+'.json')
    if receipt.exists() or list(HERE.glob('gate-'+args.record+'-*.log')): raise SystemExit('Immutable evidence exists')
    if shutil.which('lake') is None: raise SystemExit('lake must be on PATH')
    before=inventory(); env=os.environ.copy(); env['LEAN_PATH']=str(HERE/'.cache'); env['PYTHONDONTWRITEBYTECODE']='1'
    modules=[] if args.seal_only else ([] if args.reuse_suppliers else MODULES)
    if not args.seal_only and not args.suppliers_only:
        modules += [(n,REL+'/'+n+'.lean') for n in ['ComplexStageTransport','ConsumerChecksC20'] if (HERE/(n+'.lean')).exists()]
    rows=[]; code=0
    for i,(name,source) in enumerate(modules):
        output=HERE/'.cache'/(name+'.olean'); output.parent.mkdir(parents=True,exist_ok=True)
        command=['lake','env','lean','-o',output.relative_to(ROOT).as_posix(),source]
        start=time.perf_counter(); run=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='utf-8',errors='replace')
        log=HERE/('gate-'+args.record+'-'+str(i)+'.log'); log.write_text(clean(run.stdout),encoding='utf-8')
        rows.append({'command':command,'exit_code':run.returncode,'seconds':time.perf_counter()-start,'log':log.relative_to(ROOT).as_posix(),'log_sha256':sha(log),'output_olean_sha256':sha(output) if output.exists() else None})
        print(json.dumps(rows[-1]),flush=True); print(clean(run.stdout),flush=True); code=run.returncode
        if code: break
    after={p:sha(ROOT/p) for p in before}
    data={'exit_code':code,'execution':rows,'before_sha256':before,'after_sha256':after,'input_count':len(before),'exact_before_after_equal':before==after,'private_outputs_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in (HERE/'.cache').rglob('*.olean')},'scientific_ROOT':False,'independent_review':'pending distinct C20 reviewer'}
    receipt.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8'); print('RECEIPT',sha(receipt),flush=True); return code
if __name__=='__main__': raise SystemExit(main())
