import json
from pathlib import Path
import sys
import entry


def build(base,package):
    if entry.sha(base/'bindings.json')!='6a3bfa246013397e867d4c3427748abcb1faa17aa5b90ecd9889969640886057' or \
        entry.sha(base/'seal.json')!='5ed9c0c9d9dcb5ce75bd79748e42efc504a631b5c61c326d5e8f6e66cd6ccf80':
        raise ValueError('immutable kernel v1 seal drift')
    files=entry.read(base/'bindings.json')['files']; entry.verify(base,files)
    files=dict(files,**{'bindings.json':entry.sha(base/'bindings.json'),'seal.json':entry.sha(base/'seal.json')})
    profile=dict(schema='C31_KERNEL_EXECUTING_FILE_GUARD_V2',basePackage='tools/c31_kernel_proof_v1',baseFiles=files,
        baseManifestSHA256=entry.sha(base/'bindings.json'),baseSealSHA256=entry.sha(base/'seal.json'),
        sourceBlindReviewExclusionNotConfidential=True,publicRepoCandidateTransportAllowed=True,
        candidateTransport='Install all immutable v1 files including the SHA-sealed raw candidate; no new secret bytes beyond the public original plus three proof tokens',
        noMathematicalOrResourceDelta=True,**entry.NO_ACCEPT)
    with (package/'profile.json').open('x',encoding='utf-8',newline='\n') as out: json.dump(profile,out,indent=2); out.write('\n')
    print(json.dumps(dict(profileSHA256=entry.sha(package/'profile.json'),immutableBaseFiles=len(files))))


if __name__=='__main__': build(Path(sys.argv[1]).resolve(),Path(__file__).parent.resolve())
