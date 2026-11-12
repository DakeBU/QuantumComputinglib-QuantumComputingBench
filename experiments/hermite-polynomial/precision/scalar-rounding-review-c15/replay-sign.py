import json
import os
import subprocess
from replay import HERE,ROOT,REL,sha,sanitize

env=os.environ.copy()
env['LEAN_PATH']=str(HERE/'.cache')
logpath=HERE/'sign-gate-v1.log'
record=HERE/'sign-result-v1.json'
assert not logpath.exists() and not record.exists()
source=REL+'/SignDiscriminator.lean'
before={p:sha(p) for p in [source,REL+'/replay-sign.py',REL+'/discriminator-seal-v1.json']}
command=['lake','env','lean',source]
p=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
logpath.write_text(sanitize(p.stdout),encoding='utf-8')
record.write_text(json.dumps({'command':command,'exit_code':p.returncode,'bindings_sha256':before,'unchanged':all(sha(p)==h for p,h in before.items()),'log':logpath.relative_to(ROOT).as_posix(),'log_sha256':sha(logpath.relative_to(ROOT))},indent=2)+'\n',encoding='utf-8')
print('sign probe exit',p.returncode)
raise SystemExit(p.returncode)
