"""Versioned format-only assembly; never fabricates a decoder or reviewer run."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIX = HERE.relative_to(ROOT).as_posix() + '/'


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def main():
    candidate_path = PREFIX + 'publication-candidate-v2.json'
    decoder_path = PREFIX + 'decoder-admission-evidence-v1.json'
    receipt_path = PREFIX + 'admission-preparation-v1.json'
    for path in [candidate_path, decoder_path, receipt_path]:
        assert not (ROOT / path).exists(), 'Immutable output exists'
    spec = importlib.util.spec_from_file_location('publication_check', ROOT / 'website/scripts/check_research_publications.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    old = read(PREFIX + 'publication-candidate.json')
    original_decoder_path = PREFIX + 'decoder-evidence-c19-v4.json'
    original_decoder = read(original_decoder_path)
    assert old['binding_sha256'] == original_decoder['binding_sha256'] == checker.binding_digest(ROOT, old)
    assert sha(original_decoder['artifact']) == original_decoder['artifact_sha256']
    assert sha(PREFIX + 'decoder-packet.json') == original_decoder['packet_sha256']
    candidate = copy.deepcopy(old)
    # Only the resolved pending label is replaced; the mathematical source,
    # declarations, assumptions and entire production/dependency context stay fixed.
    candidate['residual_boundary'] = (
        'Reviewed whole30-declaration exact-real stored canonicalization/refinement only; '
        'not provider-wide source/cache correspondence, main admission, input-core generation, '
        'finite-bit/runtime/stability/peak-memory, physical synthesis/cleanup or scientific ROOT.'
    )
    candidate['decoder_evidence'] = decoder_path
    candidate['reviewer_evidence'] = PREFIX + 'source-review-c20/reviewer-admission-evidence-v1.json'
    candidate['status'] = 'RETROSPECTIVE_WHOLE_MODULE_REVIEWED; final mechanical admission pending; reader/purification/main pending'
    candidate['binding_sha256'] = checker.binding_digest(ROOT, candidate)
    decoder = copy.deepcopy(original_decoder)
    decoder['binding_sha256'] = candidate['binding_sha256']
    decoder['packet_path'] = PREFIX + 'decoder-packet.json'
    decoder['artifact_path'] = original_decoder['artifact']
    decoder['original_evidence_path'] = original_decoder_path
    decoder['original_evidence_sha256'] = sha(original_decoder_path)
    decoder['original_context_binding_sha256'] = original_decoder['binding_sha256']
    decoder['format_packaging'] = {
        'packager': 'root parent metadata-only assembly, not a new decoder identity/run',
        'new_decoder_execution': False,
        'source_blind_reconstruction_and_original_run_unchanged': True,
        'candidate': candidate_path,
        'candidate_context_change': 'Resolved pending correspondence label only; mathematical source, assumptions, declarations, graph and all formal/context bytes unchanged',
        'admission_requires_distinct_reviewer_of_this_exact_wrapper': True,
    }
    for path, value in [(candidate_path, candidate), (decoder_path, decoder)]:
        (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    receipt = {
        'status': 'METADATA_PREPARED_NOT_ADMITTED',
        'candidate': candidate_path, 'candidate_sha256': sha(candidate_path),
        'decoder_wrapper': decoder_path, 'decoder_wrapper_sha256': sha(decoder_path),
        'original_candidate_sha256': sha(PREFIX + 'publication-candidate.json'),
        'original_decoder_evidence_sha256': sha(original_decoder_path),
        'old_binding': old['binding_sha256'], 'new_binding': candidate['binding_sha256'],
        'production_source_changed': False, 'new_Lean_execution': False,
        'new_independent_decoder_run': False, 'reviewer_wrapper': 'PENDING',
        'ROOT': False, 'main_admission': False, 'PURIFIED': False,
    }
    (ROOT / receipt_path).write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
