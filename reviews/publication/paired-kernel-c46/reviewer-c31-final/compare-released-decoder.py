"""Read-only comparison of a released decoder to independently sealed Stage1.

No decoder algorithm/tests, compiler, admission checker, subprocess or writes.
Private roots are CLI arguments; stdout uses logical-relative paths only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ap = argparse.ArgumentParser()
ap.add_argument('--project', type=Path, required=True)
ap.add_argument('--work', type=Path, required=True)
a = ap.parse_args()
R, W = a.project, a.work
S = W / 'paired-kernel-c46-source-first-stage1'
D = W / 'paired-kernel-c46-decoder-c31-current'
O = W / 'paired-kernel-c46-prospective/overlay'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def pin(p):
    raw = p.read_bytes()
    return dict(sha256=sha(raw), bytes=len(raw))

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def same(x, y):
    return x == y

def ensure(ok, label):
    if not ok:
        raise ValueError(label)

def relfile(root, name):
    ensure(not Path(name).is_absolute() and '..' not in Path(name).parts and '\\' not in name, 'unsafe path')
    p = root / name
    ensure(p.resolve().is_relative_to(root.resolve()), 'outside root')
    return p

ensure(pin(S / 'seal.json')['sha256'] == '9ec38c87dd40da2364010d1737b3262933af2dab959dafcb266bda2d6b040d41', 'own Stage1 changed')
stage_seal = read(S / 'seal.json')
for row in stage_seal['payload']:
    ensure(pin(S / row['path']) == {k: row[k] for k in ('sha256', 'bytes')}, 'Stage1 payload changed')
ensure(pin(S / 'public-allowlist.json')['sha256'] == stage_seal['public_allowlist_sha256'], 'Stage1 allowlist changed')
s = read(S / 'independent-index.json')
ensure(pin(D / 'seal.json')['sha256'] == '56914987c0744286129ebedeeef7fb6e9e8b066a427717835003010097693a5c', 'decoder seal')
ensure(pin(D / 'bindings.json')['sha256'] == '2b220462ac5312f4f6e7b04dbe006be3f7c768c3426774baadf2febb3c20a57e', 'decoder manifest')
seal, manifest, allow = (read(D / n) for n in ('seal.json', 'bindings.json', 'allowlist.json'))
ensure(pin(D / 'allowlist.json')['sha256'] == seal['allowlistSHA256'], 'decoder allowlist')
ensure(len(allow['members']) == len(set(allow['members'])) == 48, 'exact public48')
ensure(set(allow['members']) == set(manifest['files']) | {'bindings.json', 'seal.json'}, 'manifest membership')
transport = []
for name in allow['members']:
    observed = pin(relfile(D, name))
    if name in manifest['files']:
        ensure(observed['sha256'] == manifest['files'][name], 'decoder member changed: ' + name)
    target = ('reviews/publication/paired-kernel-c46/' + name if name.startswith('final-decoders/')
              else 'reviews/publication/paired-kernel-c46/decoder-c31-current/' + name)
    ensure(pin(relfile(R, target)) == observed, 'repository transport: ' + name)
    transport.append(dict(path=name, **observed, repository_path=target, exact_transport=True))
delta, lineage = (read(D / n) for n in ('delta-assessment.json', 'lineage.json'))
ensure(pin(D / 'delta-assessment.json')['sha256'] == 'a2bfba978667c4d85af16190f6a540324542e0f87d6218360084b0ba96ea4170', 'delta hash')
entries = {x['path']: x for x in s['overlay']['files']}
for rel, row in entries.items():
    ensure(pin(relfile(R, rel)) == row['current'] and pin(relfile(O, rel)) == row['overlay'], 'actual current/overlay drift: ' + rel)
ensure(pin(R / 'website/research/publications.json') == s['registry']['pin'], 'registry drift')
formal_checks = []
for rel, observed in delta['formalInputVector'].items():
    old = entries[rel]['current']; new = entries[rel]['overlay']
    ensure(observed == dict(originalSHA256=old['sha256'], overlaySHA256=new['sha256'], bytes=new['bytes']), 'formal vector: ' + rel)
    formal_checks.append(rel)
ensure(len(formal_checks) == 206, 'formal input206')
headers = {x['path']: x['imports'] for x in s['imports']['overlay_headers']}
for rel, names in headers.items():
    local = [n.replace('.', '/') + '.lean' for n in names if n.startswith('QuantumBlockEncoding.')]
    external = [n for n in names if not n.startswith('QuantumBlockEncoding.')]
    ensure(delta['completeGraph'][rel] == local, 'production graph: ' + rel)
    ensure(delta['externalImports'][rel] == external, 'production external imports: ' + rel)
pair_checks = []
for pair in s['pair']:
    rel = pair['module']; raw = (R / rel).read_bytes()
    sites = delta['proofOnlySites'][rel]
    ensure([x['line'] for x in sites] == [x['old_lines'][0] for x in pair['changes']], 'proof site lines')
    result = raw
    for site in reversed(sites):
        ensure(raw[site['start']:site['end']] == site['oldToken'].encode(), 'actual proof token coordinates')
        ensure(raw[:site['start']].count(b'\n') + 1 == site['line'], 'proof line coordinate')
        result = result[:site['start']] + site['newToken'].encode() + result[site['end']:]
    ensure(result == (O / rel).read_bytes(), 'full candidate reconstruction')
    pair_checks.append(dict(module=rel, count=len(sites), complete_candidate_equal=True))
own_prior = W.parent / '.c29-c31-joint-actual-decoder-c38'
ensure(delta['retainedActualSummary'] == read(own_prior / 'summary.json'), 'prior whole actual summary')
ensure(delta['retainedActualCohort'] == read(own_prior / 'technical-chain.json')['cohort'], 'prior exact cohort')
records = {x['module']: x for x in s['records']}
ensure(set(records) == set(delta['noImportCarryforward']) == set(lineage), 'exact37 partition')
checks = []
reviewers = []
for module, old in records.items():
    cl = delta['noImportCarryforward'][module]
    ensure(cl['importClosure'] == old['import_closure'], 'own closure equality')
    ensure(cl['formalClosureSHA256'] == {n: entries[n]['overlay']['sha256'] for n in old['import_closure']}, 'closure full pins')
    ex = sorted({n for p in old['import_closure'] for n in headers[p] if not n.startswith('QuantumBlockEncoding.')})
    ensure(cl['externalImports'] == ex, 'closure external imports')
    dpath = old['role_lineage'][0]['path']
    old_decoder = read(R / dpath)
    ensure(lineage[module]['originalEvidence'] == old_decoder, 'entire retained original evidence')
    ensure(lineage[module]['evidenceSHA256'] == old['role_lineage'][0]['pin']['sha256'], 'lineage original hash')
    name = Path(module).stem + '.json'
    wrapper = read(D / 'final-decoders' / name)
    reconstruction = wrapper['reconstruction']
    ensure(reconstruction['original_reconstruction'] == old_decoder['reconstruction'], 'exact old reconstruction')
    ensure(reconstruction['original_identity'] == old_decoder['identity'] and reconstruction['original_run_id'] == old_decoder['run_id'], 'old identity/run')
    ensure(reconstruction['original_evidence_path'] == dpath and reconstruction['original_evidence_sha256'] == old['role_lineage'][0]['pin']['sha256'], 'old decoder link')
    ensure(reconstruction['original_binding_sha256'] == old['computed_current_binding'], 'old binding link')
    ensure(wrapper['binding_sha256'] == old['computed_prospective_binding'], 'actual new binding')
    ensure(wrapper['explicit_import_closure'] == cl, 'wrapper closure')
    ensure(wrapper['original_lineage_sha256'] == pin(D / 'lineage.json')['sha256'], 'lineage artifact')
    checks.append(dict(module=module, file='final-decoders/' + name, decoder_sha256=pin(D / 'final-decoders' / name)['sha256'],
                       prospective_binding=wrapper['binding_sha256'], complete_original_lineage_equal=True,
                       complete_original_reconstruction_equal=True, own_stage1_closure_equal=True,
                       old_identity=old_decoder['identity'], old_run=old_decoder['run_id']))
    rpath = old['role_lineage'][1]['path']
    rev = read(R / rpath)
    ensure(pin(R / rpath) == old['role_lineage'][1]['pin'], 'original reviewer changed')
    reviewers.append(dict(module=module, original_reviewer_path=rpath,
                          original_reviewer_sha256=old['role_lineage'][1]['pin']['sha256'],
                          original_identity=rev['identity'], original_run_id=rev['run_id'],
                          original_packet_path=rev['packet_path'], original_packet_sha256=rev['packet_sha256'],
                          original_artifact_path=rev['artifact_path'], original_artifact_sha256=rev['artifact_sha256'],
                          original_semantic_slots=rev['semantic_slots']))
cubic = read(D / 'final-decoders/CubicAmplitudePrimitive.json')
candidate = next(x for x in s['candidates'] if x['module'] == cubic['module'])
ensure(cubic['binding_sha256'] == candidate['computed_binding'], 'whole Cubic opaque binding')
ensure(cubic['actualCandidateSourceSHA256'] == entries[cubic['module']]['overlay']['sha256'], 'whole Cubic source')
ensure(cubic['actualProviderCandidateSHA256'] == entries['QuantumBlockEncoding/CubicStatePreparation.lean']['overlay']['sha256'], 'Cubic actual provider')
ensure(cubic['actualOldJointCohort'] == delta['retainedActualCohort']['cohortID'], 'Cubic actual cohort')
wrappers = list((D / 'final-decoders').glob('*.json'))
ensure(len(wrappers) == 38 and not (D / 'final-decoders/CubicStatePreparation.json').exists(), 'no CSP wrapper')
for p in wrappers:
    w = read(p)
    ensure(w['role'] == 'decoder' and w['identity'] == '/root/primitive_compiler_formal_decoder_c31' and w['run_id'] == seal['run_id'], 'actual decoder role/identity/run')
    ensure(w['source_blind'] is True and w['fresh_source_blind_run'] is False and w['new_full_semantic_read'] is False, 'scope flags')
    ensure(w['artifact_sha256'] == pin(R / w['artifact_path'])['sha256'], 'actual artifact pointer')
    ensure(w['packet_sha256'] == pin(R / w['packet_path'])['sha256'], 'actual packet pointer')
    ensure(w['finalInstalledBuildPending'] is True and w['nativeAccepted'] is False, 'pending installed boundary')
ensure(pin(R / 'reviews/publication/primitive-compiler-c31/source-only.md')['sha256'] == '5907262565b6202fec61b189c42d942cb84d6215223a0da4211d63b92d3ad168', 'actual natural packet entry')
print(json.dumps(dict(schema='C46_ACTUAL_RELEASE_COMPARISON_TO_SEALED_OWN_STAGE1',
    identity='/root/primitive_compiler_source_first_c31', stage1_seal_sha256=pin(S / 'seal.json')['sha256'],
    decoder_seal=pin(D / 'seal.json'), decoder_manifest=pin(D / 'bindings.json'),
    decoder_allowlist=pin(D / 'allowlist.json'), decoder_delta=pin(D / 'delta-assessment.json'),
    exact_transport48=transport, formal_vector206_equal=True, own_production_import_graph142_equal=True,
    proof_token_coordinates_and_whole_candidates=pair_checks, prior_actual_summary_and_cohort_exact=True,
    current229_stage1_inputs_unchanged=True, full_original37_lineage_equal=True,
    compared37=checks, retained37_original_reviewer_scopes=reviewers,
    Cubic_decoder_sha256=pin(D / 'final-decoders/CubicAmplitudePrimitive.json')['sha256'],
    Cubic_whole25_candidate_binding_equal=True, no_CSP_wrapper=True,
    compiler_or_tests_or_admission_run=False), ensure_ascii=False, indent=2))
