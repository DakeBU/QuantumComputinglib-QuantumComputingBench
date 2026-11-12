"""Independent immutable middle full-source replay; reviewer-owned new cache."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
REL=HERE.relative_to(ROOT).as_posix()
PREC='experiments/hermite-polynomial/precision/'
AUTHOR=PREC+'finite-middle-source/'

def sha(p):
    return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

def sanitize(s):
    for p in [str(ROOT),str(ROOT).replace('\\','/'),str(ROOT).replace('/','\\')]:
        s=s.replace(p,'<repo>')
    return re.sub(r'[A-Za-z]:[\\/][^\r\n\'\"<>]*','<private-path>',s)

def bindings():
    bound={AUTHOR+'result.json':'a7354a475b420b29d03999f78ff7939eb5aceb0ec7ec61c442b597465d1fe20a',AUTHOR+'handoff.json':'751b227d0a26b464c22113436826f771375e2c2e5ebab6ace95e56a029e7446a'}
    r=json.loads((ROOT/(AUTHOR+'result.json')).read_text(encoding='utf-8'))
    bound.update({AUTHOR+p:h for p,h in r['artifact_hashes'].items()})
    bound.update(r['dependency_hashes'])
    for p,h in bound.items():
        assert sha(p)==h,p
    for p in [REL+'/middle-discriminator-seal-v1.json',REL+'/replay-middle.py','QuantumBlockEncoding/HermiteBernstein.lean','QuantumBlockEncoding/StoredHermiteCoefficients.lean']:
        bound[p]=sha(p)
    return bound

def main():
    output=HERE/'middle-full-replay-v1.json'
    assert not output.exists()
    before=bindings()
    (HERE/'.cache'/'QuantumBlockEncoding').mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    env['LEAN_PATH']=str(HERE/'.cache')
    sources=[('QuantumBlockEncoding/HermitePolynomial','QuantumBlockEncoding/HermitePolynomial.lean'),('CoefficientRange',PREC+'coefficient-range/CoefficientRange.lean'),('FiniteExp',PREC+'finite-exp/FiniteExp.lean'),('FiniteExpDegree',PREC+'finite-exp-degree/FiniteExpDegree.lean'),('FiniteMiddleSource',AUTHOR+'FiniteMiddleSource.lean'),('ConsumerChecks',AUTHOR+'ConsumerChecks.lean')]
    gates=[]
    for i,(module,source) in enumerate(sources):
        command=['lake','env','lean','-o',REL+'/.cache/'+module+'.olean',source]
        logpath=HERE/f'middle-full-gate-v1-{i}.log'
        assert not logpath.exists()
        start=time.perf_counter()
        p=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
        logpath.write_text(sanitize(p.stdout),encoding='utf-8')
        gates.append({'command':command,'exit_code':p.returncode,'seconds':time.perf_counter()-start,'log':logpath.relative_to(ROOT).as_posix(),'log_sha256':sha(logpath.relative_to(ROOT))})
        print(f'middle full gate {i}: exit {p.returncode}',flush=True)
        if p.returncode:
            break
    after={p:sha(p) for p in before}
    cache={p.relative_to(ROOT).as_posix():sha(p.relative_to(ROOT)) for p in (HERE/'.cache').rglob('*.olean')}
    record={'bindings_sha256':before,'unchanged':before==after,'gates':gates,'cache_sha256':cache,'cache_provenance':'Complete sources freshly recompiled in new own ignored cache; no author cache in LEAN_PATH','scope':'Focused experimental gate only, not global ROOT/publication/bit runtime/clean CI'}
    output.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    return 0 if before==after and len(gates)==6 and all(g['exit_code']==0 for g in gates) else 1

if __name__=='__main__':
    raise SystemExit(main())
