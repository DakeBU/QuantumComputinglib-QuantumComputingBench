"""Bind only the new private CI4 proposal and the authorized actual CI3 artifact."""
import difflib
import json
from pathlib import Path
import sys

import runner_v4
import verify_ci3


def write(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as out:
        json.dump(value,out,ensure_ascii=False,indent=2); out.write('\n')


def build(project,package,public,artifact):
    prior=project/'tools/primitive_compiler_native_profile_ci3'
    if runner_v4.sha(prior/'ci3-bindings.json')!='a14db08d1c1a9c5d236acb7acd30ed906c6c1c9fd00625286f4b0fb82fbdc738' or \
        runner_v4.sha(prior/'ci3-seal.json')!='674d09b0be9e9f776d36ec688984587e9e56707749e31772ab0741187c41b418':
        raise ValueError('immutable CI3 drift')
    files=runner_v4.read(prior/'ci3-bindings.json')['files']; runner_v4.pins(prior,files)
    analysis=verify_ci3.verify(public,artifact); write(package/'actual-ci3-analysis.json',analysis)
    profile=dict(schema='C31_CI4_SELF_ONLY_NAMESPACE_PROFILE_V1',
        direction='actual-PID1-permission-failure-to-sufficient-self-init-namespace-contract',
        namespacePolicy='SELF_ONLY_RESERVED_INIT_V1',PID1ReadRequested=False,
        budgetMiB=5120,reserveMiB=2048,threads=1,WindowsHighBudgetForbidden=True,oldLocalGateChanged=False,
        requiredInitCgroupNamespaceInode=0xEFFFFFFB,
        priorPackage='tools/primitive_compiler_native_profile_ci3',priorFiles=files,
        priorManifestSHA256=runner_v4.sha(prior/'ci3-bindings.json'),priorSealSHA256=runner_v4.sha(prior/'ci3-seal.json'),
        priorFailureZIP_SHA256=verify_ci3.ZIP_SHA,priorFailureAnalysisSHA256=runner_v4.sha(package/'actual-ci3-analysis.json'),
        existingWorkflowSHA256=runner_v4.sha(project/'.github/workflows/c31-native-diagnostic.yml'),
        retainedSourceRoots=87,retainedModules=3,retainedDynamicGeneratedPartition=True,
        scientificCollectorSuccessObserved=False,**runner_v4.NO_ACCEPT)
    write(package/'ci4-profile.json',profile)
    old=(prior/'resource_gate_v3.py').read_text(encoding='utf-8').splitlines(keepends=True)
    new=(package/'resource_gate_v4.py').read_text(encoding='utf-8').splitlines(keepends=True)
    # Generated exact review derivative, not an instruction to change the prior file.
    delta=''.join(difflib.unified_diff(old,new,fromfile='immutable-ci3/resource_gate_v3.py',tofile='new-ci4/resource_gate_v4.py'))
    with (package/'resource-contract.delta.patch').open('x',encoding='utf-8',newline='\n') as out: out.write(delta)
    runner_v4.load_ci3(project,profile)
    print(json.dumps(dict(profileSHA256=runner_v4.sha(package/'ci4-profile.json'),
        actualCI3ArtifactVerified=True,nativeChildrenStarted=0)))


if __name__=='__main__':
    project,public,artifact=map(Path,sys.argv[1:4])
    build(project.resolve(),Path(__file__).parent.resolve(),public.resolve(),artifact.resolve())
