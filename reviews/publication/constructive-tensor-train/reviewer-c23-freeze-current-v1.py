"""Freeze only reviewer-owned current public evidence, with no acceptance promotion."""
import hashlib
import json
import re
from pathlib import Path
root = Path.cwd()
base = root / 'reviews/publication/constructive-tensor-train'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
expected = {
    'reviewer-c23-source-inventory.json':'052a7b305bf35f673981fc403af194a6cccbc7f5426977e6149f95a62485c98b',
    'reviewer-c23-source-topology.json':'db55e56355da9b7e6c6acf1ef5ac3a5536ca076fe3434487c81161da848c0cdf',
    'reviewer-c23-phase1-seal.md':'aa7c43748d415916f10a0a34fd33a249b73b0c14dbfb61192fb5e18dff6e3ca1',
    'decoder-c23-freeze.json':'675716ee027edce38182f115612301369fdf0b5ff619ddb182f625ebcfdd5a1c',
    'decoder-c23-reconstruction.txt':'a9da979284f404c68b9000b35e610e1b5fa2db55fd915d7cacbf89ce0880346a',
    'parent-graph-views-v2.json':'ae78af6906d8d9d504a1a35e6a72559c24fab861092753d58396cdff9ce6b05c',
    'parent-source-coverage-v2.json':'a77f4dc57e2c993628ab73a2ebcce07488c405caf599a929904d4bd91fcedefc',
}
for name, expected_sha in expected.items():
    assert sha(base/name) == expected_sha, name
receipt = json.loads((base/'reviewer-c23-checks-v3.json').read_text(encoding='utf-8-sig'))
assert len(receipt['checks']) >= 8 and all(item['exit_code'] == 0 for item in receipt['checks'][:8])
consumer = json.loads((base/'reviewer-c23-consumer-check-v3.json').read_text(encoding='utf-8-sig'))
assert consumer['consumer_exit_code'] == 0
assert sha(base/'reviewer-c23-consumer.lean') == consumer['consumer_source_sha256']
public = []
for path in sorted(base.glob('reviewer-c23-*')):
    if not path.is_file() or path.name == 'reviewer-c23-current-freeze.json':
        continue
    text = path.read_text(encoding='utf-8-sig')
    assert not re.search(r'[A-Za-z]:\\|/Users/|/home/',text),path.name
    public.append({'path':path.relative_to(root).as_posix(),'sha256':sha(path),'bytes':path.stat().st_size})
record = {
    'reviewer_identity':'ctt_source_first_reviewer_c23',
    'run_identity':'ctt-source-first-c23-20261010-v1',
    'direction_fingerprint':'CTT_SOURCE_TOPOLOGY_AND_FIDELITY',
    'status':'CHANGES_REQUIRED_PENDING_DECODER_WORDING_CLARIFICATION_HUMAN_PRIORITY_PAUSE',
    'binding_sha256':'9be3c975b10363ad36778d6dc9da4c7a941857f6571f3e2f6072c73d65a51c09',
    'historical_formalizer':'unknown; retrospective packet author not presumed formalizer',
    'source_class':'retrospective-local-author-mathematical-exposition',
    'source_only_seal_unchanged':True,
    'source_formal_contract':'MATCH_ALL15',
    'successor_source_topology':'ACCEPTED_BOUNDED; original graph CHANGES_REQUIRED retained',
    'exposition':'ACCEPTED_BOUNDED_MATHEMATICS_NOT_INTEGRATED_PURIFICATION',
    'fresh_eight_bound_source_module_compiles':True,
    'independent_consumer_exit_code':0,
    'frozen_external_comparison_inputs':expected,
    'public_artifacts':public,
    'public_artifact_count':len(public),
    'public_local_machine_path_scan':'PASS',
    'private_caches_excluded_from_public_artifacts':True,
    'final_publication_acceptance':False,
    'full_repository_gate':'PENDING',
    'site_gate':'PENDING',
    'PURIFIED':False,
    'scientific_ROOT_closed':False,
    'main_admission':False,
    'production_registry_or_Git_edits':False,
    'frozen_decoder_mutated':False,
    'next_step':'After human resumption, decoder-owned versioned zero-pair wording clarification from existing formal context, followed by exact frozen-hash source/formal comparison; no final acceptance before that.',
}
out=base/'reviewer-c23-current-freeze.json'
assert not out.exists(),'Refuse to overwrite an existing freeze'
out.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'freeze_path':out.relative_to(root).as_posix(),'freeze_sha256':sha(out),'public_artifact_count':len(public)},ensure_ascii=False))
