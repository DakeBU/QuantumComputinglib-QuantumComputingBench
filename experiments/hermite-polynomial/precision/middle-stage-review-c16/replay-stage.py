"""Fresh whole-source stage review, preserving middle cache and frozen task binding."""
import json
import os
import subprocess
import time
from replay_middle_support import HERE,ROOT,REL,sha,sanitize

AUTHOR='experiments/hermite-polynomial/precision/saved-stage-interpreter/'
PREC='experiments/hermite-polynomial/precision/'

def bindings():
    bound={AUTHOR+'result-v1.json':'b2ee44272c1a5a9e95d05a41af7eef2a28a968af60faf751c8f97976edf25074',AUTHOR+'gate-full-v1.json':'db9dd30a4335c0586d0f2added2af77aecc862396cc41842b9aa697e8c7d7ee3'}
    r=json.loads((ROOT/(AUTHOR+'result-v1.json')).read_text(encoding='utf-8'))
    bound.update(r['bindings_sha256'])
    for gate in r['execution']:
        bound[gate['log']]=gate['log_sha256']
    for p,h in bound.items():
        assert sha(p)==h,p
    # Historical search receipts bind earlier source versions, not current source.
    # Verify their immutable log hashes, retain their old source maps as history.
    for p in r['failure_receipts']:
        old=json.loads((ROOT/p).read_text(encoding='utf-8'))
        bound[p]=sha(p)
        for g in old['execution']:
            assert sha(g['log'])==g['log_sha256'],g['log']
            bound[g['log']]=g['log_sha256']
    for p in [REL+'/stage-discriminator-seal-v1.json',REL+'/replay-stage.py']:
        bound[p]=sha(p)
    return bound

def main():
    out=HERE/'stage-full-replay-v1.json'
    assert not out.exists()
    before=bindings()
    cache=HERE/'.cache'/'stage-c16'
    cache.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    env['LEAN_PATH']=str(cache)
    env['PYTHONDONTWRITEBYTECODE']='1'
    sources=[('FiniteTrig',PREC+'finite-trig/FiniteTrig.lean'),('SavedRounding',PREC+'saved-rounding/SavedRounding.lean'),('SavedStageInterpreter',AUTHOR+'SavedStageInterpreter.lean'),('StageOperatorBound',AUTHOR+'StageOperatorBound.lean')]
    commands=[['lake','env','lean','-o',REL+'/.cache/stage-c16/'+name+'.olean',src] for name,src in sources]
    commands += [['lake','env','lean',AUTHOR+'ConsumerChecks.lean'],['.venv/Scripts/python.exe',AUTHOR+'test_saved_stage.py','-v']]
    gates=[]
    for i,command in enumerate(commands):
        log=HERE/f'stage-full-gate-v1-{i}.log'
        assert not log.exists()
        start=time.perf_counter()
        p=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
        log.write_text(sanitize(p.stdout),encoding='utf-8')
        gates.append({'command':command,'exit_code':p.returncode,'seconds':time.perf_counter()-start,'log':log.relative_to(ROOT).as_posix(),'log_sha256':sha(log.relative_to(ROOT))})
        print(f'stage full gate {i}: exit {p.returncode}',flush=True)
        if p.returncode:
            break
    after={p:sha(p) for p in before}
    caches={p.relative_to(ROOT).as_posix():sha(p.relative_to(ROOT)) for p in cache.glob('*.olean')}
    out.write_text(json.dumps({'bindings_sha256':before,'unchanged':before==after,'gates':gates,'cache_sha256':caches,'cache_provenance':'Own new .cache/stage-c16 complete-source rebuild; author cache and earlier middle cache absent from LEAN_PATH','historical_receipts':'All old search logs matched; old source bindings not misrepresented as final versions','scope':'Focused internal mathematics only; no efficient dense runtime/root/publication'},indent=2)+'\n',encoding='utf-8')
    return 0 if before==after and len(gates)==6 and all(g['exit_code']==0 for g in gates) else 1

if __name__=='__main__':
    raise SystemExit(main())
