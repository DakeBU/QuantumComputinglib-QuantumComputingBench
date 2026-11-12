"""Generate only this exclusive proposal's bindings from immutable own packages."""
import json
from pathlib import Path
import sys

import runner_v3
import verify_ci2


def write(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as out:
        json.dump(value, out, ensure_ascii=False, indent=2); out.write('\n')


def build(project, package, public, artifact):
    prior = project / 'tools/primitive_compiler_native_profile_ci2'
    if runner_v3.sha(prior/'ci2-bindings.json') != '8f89167d4515631989099ad689f858c4b69f1003872ca69a52a67903ac775ef3' or \
            runner_v3.sha(prior/'ci2-seal.json') != '373c06cc36e7f043cad97b323f8f6eea15e170f310cf8aa3a17dd9b57a6d430c':
        raise ValueError('old CI2 seal drift')
    files = runner_v3.read(prior/'ci2-bindings.json')['files']
    runner_v3.pins(prior, files)
    analysis = verify_ci2.verify(public, artifact)
    write(package/'actual-ci2-analysis.json', analysis)
    profile = dict(schema='C31_CI3_ROOT_API_CORRECTION_V1',
        direction='Linux-cgroup-v2-root-interface-API-correction-not-memory-threshold-relaxation',
        budgetMiB=5120, reserveMiB=2048, threads=1, WindowsHighBudgetForbidden=True, oldLocalGateChanged=False,
        requiredInitCgroupNamespaceInode=0xEFFFFFFB,
        priorPackage='tools/primitive_compiler_native_profile_ci2', priorFiles=files,
        priorManifestSHA256=runner_v3.sha(prior/'ci2-bindings.json'),
        priorSealSHA256=runner_v3.sha(prior/'ci2-seal.json'),
        priorProfileSHA256=runner_v3.sha(prior/'ci2-profile.json'),
        priorFailureZIP_SHA256=verify_ci2.ZIP_SHA,
        priorFailureAnalysisSHA256=runner_v3.sha(package/'actual-ci2-analysis.json'),
        existingWorkflowSHA256=runner_v3.sha(project/'.github/workflows/c31-native-diagnostic.yml'),
        retainedSourceRoots=87, retainedModules=3, retainedDynamicGeneratedPartition=True,
        scientificCollectorSuccessObserved=False, **runner_v3.NO_ACCEPT)
    write(package/'ci3-profile.json', profile)
    runner_v3.load_ci2(project, profile)
    print(json.dumps(dict(profileSHA256=runner_v3.sha(package/'ci3-profile.json'),
        actualCI2ArtifactVerified=True, nativeChildrenStarted=analysis['nativeChildrenStarted'])))


if __name__ == '__main__':
    project, public, artifact = map(Path,sys.argv[1:4])
    build(project.resolve(),Path(__file__).parent.resolve(),public.resolve(),artifact.resolve())
