"""Portable full-source reproduction; lake is resolved from PATH.

Start with repository dependencies already built. All new oleans are private.
Historical sanitized records retain raw hashes and do not assert these portable
commands were the historical commands.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
REL=HERE.relative_to(ROOT).as_posix()
P='experiments/hermite-polynomial/precision/'
MODULES=[(n,n+'.lean') for n in ['QuantumBlockEncoding/PrimitiveCircuit','QuantumBlockEncoding/PrimitiveSemantics','QuantumBlockEncoding/PrimitiveBasisLE']]
MODULES += [('FiniteTrig',P+'finite-trig/FiniteTrig.lean'),('SavedRounding',P+'saved-rounding/SavedRounding.lean'),('SavedStageInterpreter',P+'saved-stage-interpreter/SavedStageInterpreter.lean')]
MODULES += [(n,P+'literal-complex-adapter/'+n+'.lean') for n in ['BasisCompatibility','LiteralComplexAdapter','ConsumerChecks']]
MODULES += [('ReviewConsumers',REL+'/ReviewConsumers.lean')]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def clean(text):
    text=text.replace(str(ROOT),'<repo>').replace(ROOT.as_posix(),'<repo>')
    return re.sub(r'[A-Za-z]:[\\/][^\r\n\'"<>]*','<private-path>',text)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--record',required=True); args=ap.parse_args()
    receipt=HERE/('portable-'+args.record+'.json')
    if receipt.exists() or list(HERE.glob('portable-'+args.record+'-*.log')): raise SystemExit('Immutable evidence exists')
    if shutil.which('lake') is None: raise SystemExit('lake must be discoverable on PATH')
    evidence=json.loads((HERE/'review-evidence-public-v1.json').read_text(encoding='utf-8'))
    # Private historical failure files and scripts were not Lean proof inputs.
    pins={p:h for p,h in evidence['final_input_pins_sha256'].items() if not p.startswith(REL+'/') or p in [REL+'/ReviewConsumers.lean',REL+'/pre-verdict-reconstruction.md']}
    before={p:sha(ROOT/p) for p in pins}
    if before!=pins: raise SystemExit('Sealed proof dependencies changed')
    env=os.environ.copy(); env['LEAN_PATH']=str(HERE/'.cache'); env['PYTHONDONTWRITEBYTECODE']='1'
    rows=[]; code=0
    for i,(name,source) in enumerate(MODULES):
        output=HERE/'.cache'/(name+'.olean'); output.parent.mkdir(parents=True,exist_ok=True)
        command=['lake','env','lean','-o',output.relative_to(ROOT).as_posix(),source]
        start=time.perf_counter(); run=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='utf-8',errors='replace')
        log=HERE/('portable-'+args.record+'-'+str(i)+'.log'); log.write_text(clean(run.stdout),encoding='utf-8')
        rows.append({'command':command,'exit_code':run.returncode,'seconds':time.perf_counter()-start,'log':log.relative_to(ROOT).as_posix(),'log_sha256':sha(log),'output_sha256':sha(output) if output.exists() else None})
        code=run.returncode
        if code: break
    after={p:sha(ROOT/p) for p in pins}
    receipt.write_text(json.dumps({'execution':rows,'exit_code':code,'input_count':len(pins),'before_sha256':before,'after_sha256':after,'exact_before_after_equal':before==after,'production_olean_outputs':False,'scientific_ROOT':False},indent=2)+'\n',encoding='utf-8')
    print('RECEIPT',sha(receipt)); return code
if __name__=='__main__': raise SystemExit(main())
