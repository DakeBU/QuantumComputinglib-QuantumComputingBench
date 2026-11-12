"""Derive only a new technical entry profile; never rewrite sealed predecessors."""
import json
from pathlib import Path
import sys
import entry


def build(base,previous,package):
    if entry.sha(previous/'bindings.json')!='d219474c6acc278d186ca74b2c7d8880f74e464731fe78e68e9919aad4f6af58' or \
        entry.sha(previous/'seal.json')!='fdffd9e2c1d6f5940fc4f96ca870d8bcd3c6d8ee69c9b6180b40e235ed36814f':
        raise ValueError('immutable v2 seal drift')
    entry.verify(previous,entry.read(previous/'bindings.json')['files'])
    profile=entry.read(previous/'profile.json'); entry.verify(base,profile['baseFiles'])
    if entry.read(base/'profile.json')['sharedInstrumentation']!=dict(path=entry.SHARED_PATH,sha256=entry.SHARED_SHA):
        raise ValueError('original shared instrumentation pin disagreement')
    profile.update(schema='C31_KERNEL_SHADOW_HELPER_GUARD_V3',
        shadowSharedHelper=dict(path=entry.SHARED_PATH,sha256=entry.SHARED_SHA),
        priorGuardProfileSHA256=entry.sha(previous/'profile.json'),
        priorGuardManifestSHA256=entry.sha(previous/'bindings.json'),priorGuardSealSHA256=entry.sha(previous/'seal.json'),
        priorGuardFiles=dict(entry.read(previous/'bindings.json')['files'],
            **{'bindings.json':entry.sha(previous/'bindings.json'),'seal.json':entry.sha(previous/'seal.json')}),
        firstFailureArtifactZIP_SHA256='7c395ab385ffb36a60b569b8688085155c54e50f3a7acc474e80c24b98ecf732',
        technicalDelta='Exclusive data-only shared helper copy plus existing continuous source/destination pin checks')
    with (package/'profile.json').open('x',encoding='utf-8',newline='\n') as out: json.dump(profile,out,indent=2); out.write('\n')
    print(entry.sha(package/'profile.json'))


if __name__=='__main__': build(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve(),Path(__file__).parent.resolve())
