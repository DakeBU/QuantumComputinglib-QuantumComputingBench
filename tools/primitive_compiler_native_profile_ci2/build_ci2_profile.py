"""One-time new proposal rendering; read-only on v1, sources and failure bundle."""
import hashlib
import json
from pathlib import Path
import sys


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(project, package):
    base = project / 'tools/primitive_compiler_native_profile_v1'
    manifest = base / 'proposal-bindings.json'
    if sha(manifest) != '6aee79faeab6160e8203b288a30bb02f50f452a0add0c68fe51c59fa13c4eacb':
        raise ValueError('old 14-file manifest changed')
    files = json.loads(manifest.read_text(encoding='utf-8'))['files']
    if len(files) != 14 or any(sha(base / name) != digest for name, digest in files.items()):
        raise ValueError('old14 bytes changed')
    old_profile = json.loads((base / 'profile.json').read_text(encoding='utf-8'))
    if sha(base / 'profile.json') != '72c0931c4c62906835d831742a3b797b381e947fbb8e3ecb58c4ad62aaa64473':
        raise ValueError('own87 profile changed')
    for name, digest in old_profile['projectInputs'].items():
        if sha(project / name) != digest:
            raise ValueError('original31 source/config input changed')
    shared = old_profile['sharedInstrumentation']
    if sha(project / shared['path']) != shared['sha256']:
        raise ValueError('shared instrumentation changed')
    original = project / 'runs/hermite-curriculum-goal-20261008/scratch/primitive-compiler-decoder-c31'
    if sha(original / 'source-formal-seal.json') != old_profile['sourceSealSHA256'] or \
            sha(original / 'native-profile-v1/proposal-seal.json') != sha(base / 'proposal-seal.json'):
        raise ValueError('original immutable seals changed')
    analysis = json.loads((package / 'actual-ci1-analysis.json').read_text(encoding='utf-8'))
    profile = dict(schema='C31_CI_ONLY_MEMORY_SUCCESSOR_V1', budgetMiB=5120, reserveMiB=2048, threads=1,
        direction='actual-CI-fresh-target-internal-cap-evidence-to-finite-gated-CI-only-successor',
        expectedInformationGain='test whether a finite higher internal cap permits the first actual fresh target under measured headroom, without changing any mathematical input',
        budgetStatus='UNPROVEN_FINITE_CANDIDATE_NOT_MEASURED_SUFFICIENT',
        cgroupPolicy='V2_CURRENT_AND_ALL_VISIBLE_ANCESTORS_PLUS_MEMAVAILABLE_UNKNOWN_REFUSED',
        oldLocalGateChanged=False, WindowsHighBudgetForbidden=True,
        basePackage='tools/primitive_compiler_native_profile_v1', baseManifestSHA256=sha(manifest),
        baseFiles=files, baseProposalSealSHA256=sha(base / 'proposal-seal.json'),
        baseProfileSHA256=sha(base / 'profile.json'), originalSourceSealSHA256=old_profile['sourceSealSHA256'],
        sharedInstrumentation=shared, firstFailureZIP_SHA256=analysis['authorizedZIP_SHA256'],
        firstFailureAnalysisSHA256=sha(package / 'actual-ci1-analysis.json'),
        parentReportedCI=dict(commit='0993729ffc69629d186840dc9fd4e2345d41b3db',
                              runID=38979121261, jobID=117235547250, artifactID=12080930253),
        existingWorkflowSHA256=sha(project / '.github/workflows/c31-native-diagnostic.yml'),
        outputPathUnchanged='_out/primitive-compiler-native-profile-v1',
        outputReuseForbidden=True, sourceAgreement=None, axiomPolicyPass=None, publicationBinding=None,
        scientificAcceptance=False, nativeAccepted=False, trustClosure=False)
    with (package / 'ci2-profile.json').open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(profile, handle, indent=2, ensure_ascii=False); handle.write('\n')
    print(json.dumps(dict(state='NEW_CI_ONLY_PROFILE_RENDERED_NOT_RUN', base14Unchanged=True,
                         sourceInputs=31, roots=87, privateRoots=8, profileSHA256=sha(package / 'ci2-profile.json'))))


if __name__ == '__main__':
    build(Path(sys.argv[1]).resolve(), Path(__file__).parent.resolve())
