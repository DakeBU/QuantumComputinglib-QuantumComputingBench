"""Additive corrected kernel replay; initial whole-source failure remains failed."""
import json
import os
import subprocess
from replay_middle_support import HERE,ROOT,REL,sha,sanitize

output=HERE/'middle-probe-results-v2.json'
logpath=HERE/'middle-probe-gate-v2.log'
assert not output.exists() and not logpath.exists()
paths=['middle-discriminator-seal-v1.json','middle-discriminator-seal-v2-additive.json','MiddleDiscriminatorsV2.lean','middle-probe-results-v1.json','replay-middle-probes-v2.py']
before={REL+'/'+p:sha(REL+'/'+p) for p in paths}
env=os.environ.copy()
env['LEAN_PATH']=str(HERE/'.cache')
command=['lake','env','lean',REL+'/MiddleDiscriminatorsV2.lean']
p=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
logpath.write_text(sanitize(p.stdout),encoding='utf-8')
unchanged=all(sha(p)==h for p,h in before.items())
output.write_text(json.dumps({'bindings_sha256':before,'unchanged':unchanged,'command':command,'exit_code':p.returncode,'log':logpath.relative_to(ROOT).as_posix(),'log_sha256':sha(logpath.relative_to(ROOT)),'v1_kernel_exit':1,'v1_kernel_failed_not_green':True,'finite_test_evidence':'Existing v1 four-method finite suite passed; unchanged and not rerun here'},indent=2)+'\n',encoding='utf-8')
print('middle corrected kernel probe: exit',p.returncode)
raise SystemExit(p.returncode if unchanged else 1)
