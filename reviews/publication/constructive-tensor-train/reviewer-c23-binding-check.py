"""Independent content checks; owned candidate is not canonical admission."""
import hashlib
import importlib.util
import json
from pathlib import Path

root = Path.cwd()
base = root / 'reviews/publication/constructive-tensor-train'
def read(name):
    return json.loads((base / name).read_text(encoding='utf-8-sig'))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

candidate = read('publication-candidate.json')
source = read('author-source-row-candidate.json')
spec = importlib.util.spec_from_file_location('ctt_review_checker', root / 'website/scripts/check_research_publications.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
load_original = checker.load
def proposed_source_lookup(repo, name):
    if name == 'website/research/sources.json':
        return {'sources': [source]}
    return load_original(repo, name)
checker.load = proposed_source_lookup
computed = checker.binding_digest(root, candidate)
assert computed == '121c0c8603b75ccde304783e94fa61abd82159768b0007da675da201f7501c24'
assert computed == candidate['binding_sha256']
context = read('author-formal-context.json')
for item in context['files']:
    assert sha(root / item['path']) == item['sha256'], item['path']
    assert (root / item['path']).read_text(encoding='utf-8') == item['full_source_text'], item['path']
assert context['upstream_context']['file_sha256'] == sha(root / context['upstream_context']['path'])
module_text = (root / candidate['module']).read_text(encoding='utf-8')
for decl in context['declarations']:
    assert decl['source_exact'] in module_text, decl['name']
assert set(candidate['declarations']) == {d['name'] for d in context['declarations']}
receipt = {
    'reviewer_identity': 'ctt_source_first_reviewer_c23',
    'run_identity': 'ctt-source-first-c23-20261010-v1',
    'binding_sha256': computed,
    'recipe': 'actual checker.binding_digest; source lookup substituted with owned proposed row, no canonical registry write',
    'canonical_admission_claimed': False,
    'all_eight_context_sources_match_raw_hash_and_normalized_text': True,
    'all_fifteen_public_declarations_match_actual_source': True,
    'upstream_product_equivalence_hash_matches': True,
    'hashes': {name:sha(base / name) for name in ['publication-candidate.json','author-formal-context.json','author-graph-views.json','author-source-coverage.json','reviewer-c23-source-inventory.json','reviewer-c23-source-topology.json','reviewer-c23-phase1-seal.md']},
}
(base / 'reviewer-c23-binding-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
