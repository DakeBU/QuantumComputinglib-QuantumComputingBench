import json
import os
import subprocess
from replay_middle_support import HERE,ROOT,REL,sha,sanitize

def main():
    output=HERE/'stage-probe-results-v1.json'
    assert not output.exists()
    paths=['stage-discriminator-seal-v1.json','StageDiscriminators.lean','test_stage_discriminators.py','replay-stage-probes.py']
    before={REL+'/'+p:sha(REL+'/'+p) for p in paths}
    env=os.environ.copy()
    env['LEAN_PATH']=str(HERE/'.cache'/'stage-c16')
    env['PYTHONDONTWRITEBYTECODE']='1'
    commands=[['.venv/Scripts/python.exe',REL+'/test_stage_discriminators.py','-v'],['lake','env','lean',REL+'/StageDiscriminators.lean']]
    gates=[]
    for i,command in enumerate(commands):
        log=HERE/f'stage-probe-gate-v1-{i}.log'
        assert not log.exists()
        p=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
        log.write_text(sanitize(p.stdout),encoding='utf-8')
        gates.append({'command':command,'exit_code':p.returncode,'log':log.relative_to(ROOT).as_posix(),'log_sha256':sha(log.relative_to(ROOT))})
        print(f'stage probe {i}: exit {p.returncode}',flush=True)
    unchanged=all(sha(p)==h for p,h in before.items())
    output.write_text(json.dumps({'bindings_sha256':before,'unchanged':unchanged,'gates':gates,'failure_policy':'Nonzero exits retained failed, additive corrections only'},indent=2)+'\n',encoding='utf-8')
    return 0 if unchanged and all(g['exit_code']==0 for g in gates) else 1

if __name__=='__main__':
    raise SystemExit(main())
