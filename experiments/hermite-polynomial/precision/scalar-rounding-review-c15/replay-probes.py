"""Record all own probes including the known failed v1, sanitizing before writes."""
import json
import os
import subprocess
import time
from replay import HERE,ROOT,REL,sha,sanitize

def main():
    result=HERE/'probe-results-v1.json'
    assert not result.exists()
    inputs=['discriminator-seal-v1.json','discriminator-seal-v2-additive.json','Discriminators.lean','test_discriminators.py','test_discriminators_v2.py','replay-probes.py']
    before={REL+'/'+p:sha(REL+'/'+p) for p in inputs}
    env=os.environ.copy()
    env['LEAN_PATH']=str(HERE/'.cache')
    commands=[['.venv/Scripts/python.exe',REL+'/test_discriminators.py','-v'],['.venv/Scripts/python.exe',REL+'/test_discriminators_v2.py','-v'],['lake','env','lean',REL+'/Discriminators.lean']]
    gates=[]
    for i,command in enumerate(commands):
        logpath=HERE/f'probe-gate-v1-{i}.log'
        assert not logpath.exists()
        start=time.perf_counter()
        p=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
        logpath.write_text(sanitize(p.stdout),encoding='utf-8')
        gates.append({'command':command,'exit_code':p.returncode,'seconds':time.perf_counter()-start,'log':logpath.relative_to(ROOT).as_posix(),'log_sha256':sha(logpath.relative_to(ROOT))})
        print(f'probe {i} exit {p.returncode}',flush=True)
    unchanged=all(sha(p)==h for p,h in before.items())
    record={'bindings_sha256':before,'gates':gates,'unchanged':unchanged,'expected_exit_codes':[1,0,0],'v1_failure_class':'IMPLEMENTATION_FAILED reviewer symmetric test fixtures; not author mathematical failure','v1_failed_gate_not_green':True}
    result.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    return 0 if unchanged and [g['exit_code'] for g in gates]==[1,0,0] else 1

if __name__=='__main__':
    raise SystemExit(main())
