import json
import os
import subprocess
from replay_middle_support import HERE,ROOT,REL,sha,sanitize

out=HERE/'stage-probe-results-v2.json'
assert not out.exists()
paths=['stage-discriminator-seal-v1.json','stage-discriminator-seal-v2-additive.json','StageDiscriminatorsV2.lean','stage-probe-results-v1.json','test_stage_surrogate.py','test_stage_discriminators.py','replay-stage-probes-v2.py']
before={REL+'/'+p:sha(REL+'/'+p) for p in paths}
env=os.environ.copy(); env['LEAN_PATH']=str(HERE/'.cache'/'stage-c16'); env['PYTHONDONTWRITEBYTECODE']='1'
commands=[['.venv/Scripts/python.exe',REL+'/test_stage_surrogate.py','-v'],['lake','env','lean',REL+'/StageDiscriminatorsV2.lean']]
gates=[]
for i,command in enumerate(commands):
    log=HERE/f'stage-probe-gate-v2-{i}.log'
    assert not log.exists()
    p=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
    log.write_text(sanitize(p.stdout),encoding='utf-8')
    gates.append({'command':command,'exit_code':p.returncode,'log':log.relative_to(ROOT).as_posix(),'log_sha256':sha(log.relative_to(ROOT))})
    print(f'corrected stage probe {i}: exit {p.returncode}',flush=True)
unchanged=all(sha(p)==h for p,h in before.items())
out.write_text(json.dumps({'bindings_sha256':before,'unchanged':unchanged,'gates':gates,'initial_v1_kernel_exit':1,'initial_v1_failed_and_recovery_sorryAx_excluded':True,'prior_four_exact_tests':'Passed unchanged in v1; not rerun here'},indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if unchanged and all(g['exit_code']==0 for g in gates) else 1)
