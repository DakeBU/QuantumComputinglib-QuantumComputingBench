"""One-time rendering from this decoder's own frozen source inventory only."""
import hashlib
import json
from pathlib import Path
import re
import sys


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(sealed, project, output):
    seal_sha = '0fd3e599c0532c6e308dbb87b26b420f939886d9d39de89c419692946f40cd68'
    if sha(sealed / 'source-formal-seal.json') != seal_sha:
        raise ValueError('original C31 seal changed')
    seal = json.loads((sealed / 'source-formal-seal.json').read_text(encoding='utf-8'))
    for name in ('declaration-contracts.json', 'import-source-pins.json', 'configuration-binding.json'):
        if sha(sealed / name) != seal['artifactBindings'][name]:
            raise ValueError('original C31 binding changed')
    declarations = json.loads((sealed / 'declaration-contracts.json').read_text(encoding='utf-8'))['declarations']
    closure = json.loads((sealed / 'import-source-pins.json').read_text(encoding='utf-8'))['modules']
    configuration = json.loads((sealed / 'configuration-binding.json').read_text(encoding='utf-8'))['configuration']
    roots = []
    for item in declarations:
        row = dict(module=item['module'], sourceUserName=item['sourceScopedName'],
                   sourcePrivate=item['private'], sourceKind=item['kind'])
        if item['kind'] == 'structure':
            row['structureFields'] = re.findall(r'(?m)^  ([A-Za-z_][A-Za-z0-9_]*)\s*:',
                                                item['completeFormalRegion'])
        roots.append(row)
    modules = []
    for module in seal['targetBindings']:
        modules.append(dict(module=module['module'], rawSHA256=module['rawSHA256'],
                            sourceRoots=module['declarationCount'], privateRoots=module['privateCount']))
    targets = {m['module'] for m in modules}
    providers = [m for m in closure if m.get('owner') == 'project' and m['module'] not in targets]
    pins = {m['module'].replace('.', '/') + '.lean': m['sourceSHA256']
            for m in closure if m.get('owner') == 'project'}
    pins.update({c['file']: c['sha256'] for c in configuration})
    for relative, digest in pins.items():
        if sha(project / relative) != digest:
            raise ValueError('input drift ' + relative)
    api = project / 'tools/cubic_c29_diagnostic/runner.py'
    profile = dict(schema='C31_NATIVE_PROFILE_V1', sourceSealSHA256=seal_sha,
        sourceRootInventorySHA256=sha(sealed / 'declaration-contracts.json'),
        direction='shared-API-runtime-completeness-for-C31-not-duplicate-source-mathematics',
        expectedInformationGain='reusable next-three-module fresh formal runtime evidence',
        modules=modules, roots=roots, providers=[m['module'] for m in providers],
        projectInputs=pins, valuesRequested=False, ppDeepTerms=True, ppMaxSteps=2000000,
        maxRecDepth=10000, generatedIdentityBaseline=None, generatedCountBaseline=None,
        sharedInstrumentation=dict(path='tools/cubic_c29_diagnostic/runner.py', sha256=sha(api)),
        scientificAcceptance=False, sourceAgreement=None, publicationBinding=None,
        axiomPolicyPass=None, nativeAccepted=False, trustClosure=False)
    if len(roots) != 87 or sum(r['sourcePrivate'] for r in roots) != 8:
        raise ValueError('original C31 vector incomplete')
    destination = output / 'profile.json'
    if destination.exists():
        raise FileExistsError('profile rendering is exclusive')
    destination.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(dict(status='PROFILE_RENDERED_FROM_OWN_C31_SEAL', roots=87, private=8,
                         providers=len(providers), profileSHA256=sha(destination))))


if __name__ == '__main__':
    build(*(Path(x) for x in sys.argv[1:4]))
