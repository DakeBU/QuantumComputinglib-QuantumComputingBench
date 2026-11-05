"""Build a small joint profile from fixed public technical packages, no Lean."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import zipfile

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f: json.dump(v,f,indent=2); f.write('\n')

def build(project,package):
    base=project/'tools/c31_kernel_proof_v1'; guard=project/'tools/c31_kernel_proof_v3'
    profile=read(base/'profile.json'); original=read(base/'original-profile.json')
    if sha(base/'profile.json')!='e3e46b04819500acc83eaadfd34ad5185ea79b3d778f26e7b5624d84377850e7': raise ValueError('C31 candidate raw profile')
    csp_archive='tools/cubic_c29_kernel_ci1/public-runtime-package.zip'
    with zipfile.ZipFile(project/csp_archive) as z:
        names=z.namelist(); pins=json.loads(z.read('proposal-pins.json'))
        if len(names)!=10 or len(set(names))!=10 or set(names)!=set(pins['packageFiles'])|{'proposal-pins.json'}: raise ValueError('CSP archive exact partition')
        members={n:hashlib.sha256(z.read(n)).hexdigest() for n in names}
        if any(members[n]!=v for n,v in pins['packageFiles'].items()): raise ValueError('CSP archive member pin')
        if members['candidate/CubicStatePreparation.lean']!='6ee53311b5d6e18c46afb3e068341689acb86f1bdbc425e774705e81c9142f44': raise ValueError('CSP candidate bytes')
    profile['projectInputs']['QuantumBlockEncoding/CubicStatePreparation.lean']=members['candidate/CubicStatePreparation.lean']
    profile['providers'].remove('QuantumBlockEncoding.CubicStatePreparation')
    write(package/'c31-profile.json',profile)
    external={}
    for prefix,manifest in (('tools/c31_kernel_proof_v1','bindings.json'),('tools/c31_kernel_proof_v3','bindings.json')):
        folder=project/prefix; files=read(folder/manifest)['files']
        for name,value in files.items():
            if sha(folder/name)!=value: raise ValueError('prior package byte drift')
            external[prefix+'/'+name]=value
        external[prefix+'/'+manifest]=sha(folder/manifest); external[prefix+'/seal.json']=sha(folder/'seal.json')
    kernel_config=read(base/'kernel-profile.json')
    for prefix,files in kernel_config['runtimePackages'].items():
        for name,value in files.items(): external[prefix+'/'+name]=value
    for name in ('KernelTwoTypes.lean','validate_two_types.py','package-bindings.json'):
        rel='tools/cubic_c29_kernel_types_v2/'+name; external[rel]=sha(project/rel)
    external['tools/cubic_c29_diagnostic/runner.py']='61733fc92f5e99672e0ce0260ff397e07c94a349e98e12c48dd6a3171d5a75d9'
    archives={csp_archive:'dd55fbd7a9e9ad8dd9168109271433c71ec4c26687a196e42584e3aceeb5d54e',
        'reviews/publication/cubic-source-c29/kernel-two-types-v2-actual-public.zip':'c1ed298ad9736c4ec3b4ab71b4324fa407a1415d7cf1c45350e0b12ef74f149d',
        'reviews/publication/primitive-compiler-c31/kernel-v3-actual-success-public.zip':'3e69139f0a9e1d275bc2eb0b89a0bb36206501f2def3510ba4876ac20a6a7267'}
    for rel,value in dict(external,**archives).items():
        if sha(project/rel)!=value: raise ValueError('external byte pin: '+rel)
    from joint_compare import FLAGS
    result=dict(schema='C29_C31_JOINT_FRESH_KERNEL_V1',budgetMiB=5120,reserveMiB=2048,threads=1,wholeSeconds=2100,
        compileOrder=['QuantumBlockEncoding.CubicStatePreparation']+[m['module'] for m in profile['modules']],
        originalProjectInputs=original['projectInputs'],derivedC31ProfileSHA256=sha(package/'c31-profile.json'),
        cspArchive=csp_archive,cspArchiveMembers=members,externalFiles=external,archives=archives,
        cspBaselineArchive='reviews/publication/cubic-source-c29/kernel-two-types-v2-actual-public.zip',
        c31BaselineArchive='reviews/publication/primitive-compiler-c31/kernel-v3-actual-success-public.zip',
        candidateCSP_SHA256=members['candidate/CubicStatePreparation.lean'],
        candidateCubic_SHA256='952e2b359796ef695a1b1c1a376d40a80affbc679f503f94227ea0c775a6cd48',
        expectedCSPSourceRoots=319,expectedC31SourceRoots=87,expectedJointGeneratedCount=None,
        direction='joint-fresh-provider-then-consumer/single-cohort/formal-only',**FLAGS)
    write(package/'profile.json',result)
    print('PROFILE',sha(package/'profile.json'))

if __name__=='__main__': build(Path(sys.argv[1]).resolve(),Path(__file__).parent.resolve())
