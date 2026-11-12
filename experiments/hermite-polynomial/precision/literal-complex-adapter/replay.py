"""Versioned focused checks with private supplier oleans and frozen bindings."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REL = HERE.relative_to(ROOT).as_posix()
P = 'experiments/hermite-polynomial/precision/'
SUPPLIERS = [('FiniteTrig', P+'finite-trig/FiniteTrig.lean'),
 ('SavedRounding', P+'saved-rounding/SavedRounding.lean'),
 ('SavedStageInterpreter', P+'saved-stage-interpreter/SavedStageInterpreter.lean')]
PRODUCTION = [(n, n+'.lean') for n in ['QuantumBlockEncoding/PrimitiveCircuit',
 'QuantumBlockEncoding/PrimitiveSemantics', 'QuantumBlockEncoding/PrimitiveBasisLE']]
OWN = ['BasisCompatibility', 'LiteralComplexAdapter', 'ConsumerChecks']

def sha(p):
    return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

def main():
    a = argparse.ArgumentParser()
    a.add_argument('--record', required=True)
    a.add_argument('--reuse-private-suppliers', action='store_true')
    args = a.parse_args()
    receipt = HERE / ('gate-'+args.record+'.json')
    if receipt.exists() or list(HERE.glob('gate-'+args.record+'-*.log')):
        raise SystemExit('Immutable receipt already exists')
    (HERE/'.cache').mkdir(exist_ok=True)
    files = [p for _,p in SUPPLIERS] + [REL+'/'+p.name for p in HERE.iterdir() if p.is_file()]
    files += ['lean-toolchain','lake-manifest.json', 'QuantumBlockEncoding/PrimitiveBasisLE.lean',
      'QuantumBlockEncoding/PrimitiveSemantics.lean','QuantumBlockEncoding/PrimitiveCircuit.lean',
      'QuantumBlockEncoding/StatePreparationPrimitiveRoutes.lean',
      P+'nominal-stage-transport/result-v1.json', P+'saved-stage-interpreter/StageOperatorBound.lean']
    before = {p:sha(p) for p in sorted(set(files))}
    expected = {P+'saved-stage-interpreter/SavedStageInterpreter.lean':'9b6c52730dbb686908b7d98eff368bf7d87ed89b309ad162437372bca5e83d7d',
      P+'saved-stage-interpreter/StageOperatorBound.lean':'d763f631af61c598a5cac6ae7cbaa37138d120a9801c1fa53969ffdbcc4d09f4',
      P+'nominal-stage-transport/result-v1.json':'8e0d6feca6631c0eb1586901917e209095233c29e32b97bf8b2044130bd3d743'}
    if any(before[p] != v for p,v in expected.items()):
        raise SystemExit('Frozen inputs changed')
    env = os.environ.copy()
    env['LEAN_PATH'] = str(HERE/'.cache')
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    modules = [] if args.reuse_private_suppliers else PRODUCTION + SUPPLIERS
    modules += [(n,REL+'/'+n+'.lean') for n in OWN if (HERE/(n+'.lean')).exists()]
    for n,_ in modules:
        (HERE/'.cache'/n).parent.mkdir(parents=True,exist_ok=True)
    commands = [['lake','env','lean','-o',REL+'/.cache/'+n+'.olean',p] for n,p in modules]
    if (HERE/'test_discriminators.py').exists():
        commands.append(['.venv/Scripts/python.exe',REL+'/test_discriminators.py','-v'])
    rows=[]
    code=0
    for i,command in enumerate(commands):
        start=time.perf_counter()
        run=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='utf-8',errors='replace')
        output=run.stdout.replace(str(ROOT),'<repo>').replace(str(ROOT).replace('\\','/'),'<repo>')
        output=re.sub(r'[A-Za-z]:[\\/][^\r\n\'"<>]*','<private-path>',output)
        log=HERE/('gate-'+args.record+'-'+str(i)+'.log')
        log.write_text(output,encoding='utf-8')
        print(output,end='',flush=True)
        rows.append({'command':command,'exit_code':run.returncode,'seconds':time.perf_counter()-start,
          'log':log.relative_to(ROOT).as_posix(),'log_sha256':sha(log.relative_to(ROOT).as_posix())})
        code=run.returncode
        if code: break
    receipt.write_text(json.dumps({'schema_version':1,'exit_code':code,'full_sources':not args.reuse_private_suppliers,
      'execution':rows,'bindings_sha256':before,'bound_inputs_unchanged':before=={p:sha(p) for p in before},
      'scientific_root':False,'public_purified':False},indent=2)+'\n',encoding='utf-8')
    print('Receipt SHA256:',sha(receipt.relative_to(ROOT).as_posix()),flush=True)
    return code

if __name__=='__main__':
    raise SystemExit(main())
