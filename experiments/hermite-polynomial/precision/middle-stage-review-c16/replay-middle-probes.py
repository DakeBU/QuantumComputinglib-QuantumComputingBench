"""Whole own probes; keep any failure output immutable and typed."""
import json
import os
import subprocess
import time
from replay_middle_support import HERE,ROOT,REL,sha,sanitize

def main():
    output=HERE/'middle-probe-results-v1.json'
    assert not output.exists()
    paths=['middle-discriminator-seal-v1.json','MiddleDiscriminators.lean','test_middle_discriminators.py','replay-middle-probes.py','replay_middle_support.py']
    before={REL+'/'+p:sha(REL+'/'+p) for p in paths}
    env=os.environ.copy()
    env['LEAN_PATH']=str(HERE/'.cache')
    commands=[['.venv/Scripts/python.exe',REL+'/test_middle_discriminators.py','-v'],['lake','env','lean',REL+'/MiddleDiscriminators.lean']]
    gates=[]
    for i,command in enumerate(commands):
        logpath=HERE/f'middle-probe-gate-v1-{i}.log'
        assert not logpath.exists()
        start=time.perf_counter()
        p=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
        logpath.write_text(sanitize(p.stdout),encoding='utf-8')
        gates.append({'command':command,'exit_code':p.returncode,'seconds':time.perf_counter()-start,'log':logpath.relative_to(ROOT).as_posix(),'log_sha256':sha(logpath.relative_to(ROOT))})
        print(f'middle probe {i}: exit {p.returncode}',flush=True)
    unchanged=all(sha(p)==h for p,h in before.items())
    output.write_text(json.dumps({'bindings_sha256':before,'unchanged':unchanged,'gates':gates,'failure_policy':'Nonzero exits remain failed; additive repair only'},indent=2)+'\n',encoding='utf-8')
    return 0 if unchanged and all(g['exit_code']==0 for g in gates) else 1

if __name__=='__main__':
    raise SystemExit(main())
