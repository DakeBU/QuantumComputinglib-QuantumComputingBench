"""Independent full-source gate with reviewer-owned cache and immutable logs."""
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
PREC = 'experiments/hermite-polynomial/precision/'

def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()

def sanitize(s):
    for p in [str(ROOT), str(ROOT).replace('\\','/'), str(ROOT).replace('/','\\')]:
        s = s.replace(p, '<repo>')
    return re.sub(r'[A-Za-z]:[\\/][^\r\n\'\"<>]*', '<private-path>', s)

def bindings():
    bound = {}
    for rel, expected in [('finite-exp-degree/result.json','a3a0bf796ab229e65a5bc85acc58a5f92c505793a318162bc278df010d9c1f54'), ('saved-rounding/result-v1.json','96980fbe0707c80c463bf5a0b9c3649a1edc46ec190500e7a9e036a49e7eabbb')]:
        path = PREC + rel
        assert sha(path) == expected, path
        bound[path] = expected
        record = json.loads((ROOT/path).read_text(encoding='utf-8'))
        entries = record.get('bindings', [])
        entries += [{'path':p,'sha256':h} for p,h in record.get('bindings_sha256',{}).items()]
        entries += [{'path':g['log'],'sha256':g['log_sha256']} for g in record.get('execution',[])]
        for entry in entries:
            assert sha(entry['path']) == entry['sha256'], entry['path']
            bound[entry['path']] = entry['sha256']
    for p in [PREC+'finite-exp/FiniteExp.lean', 'lean-toolchain','lake-manifest.json', 'QuantumBlockEncoding/HermitePolynomial.lean', REL+'/discriminator-seal-v1.json', REL+'/replay.py']:
        bound[p] = sha(p)
    return bound

def main():
    out = HERE/'full-replay-v1.json'
    assert not out.exists(), 'Immutable reviewer replay already exists'
    before = bindings()
    (HERE/'.cache').mkdir(exist_ok=True)
    env = os.environ.copy()
    env['LEAN_PATH'] = str(HERE/'.cache')
    commands = []
    for folder, source in [('finite-exp','FiniteExp'),('finite-exp-degree','FiniteExpDegree')]:
        commands.append(['lake','env','lean','-o',f'{REL}/.cache/{source}.olean',PREC+folder+'/'+source+'.lean'])
    commands += [['lake','env','lean',PREC+'finite-exp-degree/ConsumerChecks.lean']]
    for folder, source in [('finite-trig','FiniteTrig'),('saved-rounding','SavedRounding')]:
        commands.append(['lake','env','lean','-o',f'{REL}/.cache/{source}.olean',PREC+folder+'/'+source+'.lean'])
    commands += [['lake','env','lean',PREC+'saved-rounding/ConsumerChecks.lean'], ['.venv/Scripts/python.exe',PREC+'saved-rounding/test_saved_rounding.py','-v']]
    gates = []
    for i, command in enumerate(commands):
        logpath = HERE/f'full-gate-v1-{i}.log'
        assert not logpath.exists()
        started = time.perf_counter()
        p = subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
        log = sanitize(p.stdout)
        logpath.write_text(log,encoding='utf-8')
        gates.append({'command':command,'exit_code':p.returncode,'seconds':time.perf_counter()-started,'log':logpath.relative_to(ROOT).as_posix(),'log_sha256':sha(logpath.relative_to(ROOT))})
        print(f'gate {i} exit {p.returncode}',flush=True)
        if p.returncode:
            break
    after = {p:sha(p) for p in before}
    caches = {p.relative_to(ROOT).as_posix():sha(p.relative_to(ROOT)) for p in (HERE/'.cache').glob('*.olean')}
    record = {'bindings_sha256':before,'unchanged':before==after,'gates':gates,'cache_sha256':caches,'cache_provenance':'Recompiled entire sources in this reviewer run; no author cache in LEAN_PATH','scope':'Focused experimental gates; no full project gate or runtime comparison'}
    out.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    return 0 if before==after and len(gates)==7 and all(g['exit_code']==0 for g in gates) else 1

if __name__ == '__main__':
    raise SystemExit(main())
