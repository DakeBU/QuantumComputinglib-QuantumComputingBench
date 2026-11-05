"""Read-only author assembly: emit patches as JSON; never run Lean or mutate caches.

The caller must apply outputs with apply_patch. Proposed source-row binding is
the repository publication algorithm with exactly the owned row substituted.
No decoder/reviewer evidence is produced by this author utility.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'reviews/publication/constructive-tensor-train/'
MODULE = 'QuantumBlockEncoding/ConstructiveTensorTrain.lean'
LESSON = 'docs/lessons/constructive-tensor-train-canonicalization.md'
NS = 'QuantumBlockEncoding.ConstructiveTensorTrain.'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def raw(path):
    return (ROOT / path).read_bytes()


def read_json(path):
    return json.loads(raw(path).decode('utf-8-sig'))


def emit(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def main():
    candidate = read_json(PREFIX + 'publication-candidate.json')
    source = read_json(PREFIX + 'author-source-row-candidate.json')['source']
    target = raw(MODULE).decode('utf-8')
    declarations = list(re.finditer(
        r'(?m)^(?:noncomputable )?(?:structure|def|theorem) ([A-Za-z0-9_.]+)\b', target))
    blocks = []
    for i, match in enumerate(declarations):
        end = declarations[i + 1].start() if i + 1 < len(declarations) else target.rfind('\nend ')
        block = target[match.start():end]
        next_doc = block.find('\n/--')
        if next_doc >= 0:
            block = block[:next_doc]
        block = block.rstrip()
        clause = re.search(r'(?m)^  \|', block)
        assignment = block.find(':=')
        if clause and (assignment < 0 or clause.start() < assignment):
            statement = block[:clause.start()].rstrip()
            body = block[clause.start():]
        else:
            parts = block.split(':=', 1)
            statement = parts[0].rstrip()
            body = ':=' + parts[1] if len(parts) == 2 else None
        blocks.append({'name': NS + match.group(1),
                       'line_start': target[:match.start()].count('\n') + 1,
                       'statement_source': statement,
                       'definition_or_proof_source': body,
                       'source_exact': block})
    assert [b['name'] for b in blocks] == candidate['declarations']
    inventory = read_json('web/library/declarations.json')['declarations']
    inventoried = [item['fullName'] for item in inventory if item['source'] == MODULE]
    assert set(inventoried) == set(candidate['declarations']) and len(inventoried) == 15
    lesson_old = raw(LESSON).decode('utf-8')
    lesson_base = re.sub(r'\n<!-- begin generated Lean disclosures -->.*?<!-- end generated Lean disclosures -->\n',
                         '', lesson_old, flags=re.S)
    by_short = {b['name'][len(NS):]: b for b in blocks}

    def disclose(match):
        sections = [match.group(0), '\n<!-- begin generated Lean disclosures -->']
        for name in match.group(1).split():
            b = by_short[name]
            sections.append('\n<details>\n<summary>Exact Lean statement: ' + name + '</summary>\n\n```lean\n'
                            + b['statement_source'] + '\n```\n\n</details>\n')
            if b['definition_or_proof_source']:
                sections.append('\n<details>\n<summary>Exact Lean definition or proof: ' + name + '</summary>\n\n```lean\n'
                                + b['definition_or_proof_source'] + '\n```\n\n</details>\n')
        sections.append('<!-- end generated Lean disclosures -->\n')
        return ''.join(sections)

    lesson = re.sub(r'<!-- lean-disclosures: ([A-Za-z0-9_ ]+) -->', disclose, lesson_base)
    lesson_bytes = lesson.encode('utf-8')
    keys = ('module', 'source_id', 'source_statement', 'source_anchor', 'lesson_path',
            'declarations', 'obligation_map', 'assumption_deltas', 'graph_contribution',
            'formalizer', 'residual_boundary')
    payload = {key: candidate.get(key) for key in keys}
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode())
    for name in (MODULE, LESSON, 'lean-toolchain', 'lake-manifest.json'):
        digest.update(name.encode())
        digest.update(lesson_bytes if name == LESSON else raw(name))
    global_digest = hashlib.sha256()
    raw_inputs = []
    for directory in ('QuantumBlockEncoding', 'ABEISTests'):
        for path in sorted((ROOT / directory).rglob('*.lean')):
            name = path.relative_to(ROOT).as_posix()
            data = path.read_bytes()
            digest.update(name.encode())
            digest.update(data)
            global_digest.update(name.encode())
            global_digest.update(data)
            raw_inputs.append({'path': name, 'sha256': sha(data), 'bytes': len(data)})
    digest.update(json.dumps(source, sort_keys=True, ensure_ascii=False).encode())
    binding = digest.hexdigest()
    candidate['binding_sha256'] = binding
    candidate['binding_mode'] = 'checker binding_digest with the owned proposed source row, not canonical registry insertion'
    candidate['owned_source_row_candidate'] = PREFIX + 'author-source-row-candidate.json'
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    providers = ['QuantumBlockEncoding/ConstructiveThinLQ.lean',
                 'QuantumBlockEncoding/TensorTrainCanonical.lean',
                 'QuantumBlockEncoding/RectangularGivens.lean',
                 'QuantumBlockEncoding/ThinLQ.lean',
                 'QuantumBlockEncoding/AdjacentGivens.lean',
                 'QuantumBlockEncoding/SequentialBondPreparation.lean',
                 'QuantumBlockEncoding/RealAmplitudePreparation.lean']
    context_files = []
    for name in [MODULE] + providers:
        data = raw(name)
        text = data.decode('utf-8')
        context_files.append({'path': name, 'sha256': sha(data),
                              'encoding': 'UTF-8; text retains source newline characters',
                              'imports': re.findall(r'(?m)^import ([^\r\n]+)', text),
                              'full_source_text': text})
    mathlib_path = '.lake/packages/mathlib/Mathlib/Logic/Equiv/Fin/Basic.lean'
    mathlib = raw(mathlib_path).decode('utf-8')
    e_start = mathlib.index('/-- Equivalence between `Fin m × Fin n`')
    e_end = mathlib.index('\n/--', e_start + 4)
    context = {'schema_version': 1, 'role': 'formal-context-snapshot-not-reconstruction',
               'target_module': MODULE, 'module_sha256': sha(raw(MODULE)),
               'declarations': blocks, 'source_lexical_not_elaborated_types': True,
               'files': context_files,
               'upstream_context': {'path': mathlib_path, 'file_sha256': sha(raw(mathlib_path)),
                                    'exact_finProdFinEquiv_source': mathlib[e_start:e_end]},
               'additional_transitive_imports': 'Available actual repository/formal library source; not all are duplicated in this bounded snapshot.',
               'fresh_Lean_execution': False, 'cached_olean_attestation': False}
    context_bytes = emit(context).encode('utf-8')
    packet = {'schema_version': 1, 'role': 'source-blind-formal-decoder',
              'binding_sha256': binding, 'binding_is_opaque_to_decoder': True,
              'module': MODULE, 'module_sha256': sha(raw(MODULE)),
              'toolchain': raw('lean-toolchain').decode().strip(),
              'toolchain_sha256': sha(raw('lean-toolchain')),
              'manifest_sha256': sha(raw('lake-manifest.json')),
              'lakefile_sha256': sha(raw('lakefile.lean')),
              'formal_context_path': PREFIX + 'author-formal-context.json',
              'formal_context_sha256': sha(context_bytes),
              'declarations': candidate['declarations'],
              'allowed_context': ['Whole actual target source and formal imports/providers/types/scopes',
                                  'Toolchain, manifest, lakefile and process protocols',
                                  'Exact source-derived declaration inventory; not an attestation of elaboration'],
              'withheld': ['Authored prose, proposed source metadata and publication data',
                           'Author classifications and graph proposals, other reviews and desired verdicts'],
              'questions': ['Independently reconstruct the exact mathematical content of every public declaration, expanding ambient project definitions and distinguishing output proof fields from input premises.',
                            'Record all context read and the source versus cached-provider boundary; source-visible signatures are not fresh elaborated #check types.',
                            'If Lean is run, bind actual source/toolchain/manifest scope, actual command, complete diagnostic outcome and axiom census; do not import the cached target as evidence of freshly checked target source.',
                            'Report mismatches or limitations in your own words; no acceptance conclusion is requested.'],
              'author_is_not_decoder': True, 'decoder_run_status': 'NOT_STARTED_BY_AUTHOR',
              'instructions': 'Do not inspect withheld author artifacts. Preserve the opaque binding; recomputation requires withheld metadata and is not part of blind reconstruction. Independent formal source reads are permitted. No lesson title, source row, author assumption delta, or desired verdict is supplied.'}
    publications = read_json('website/research/publications.json')['records']
    proof_paths = ['QuantumBlockEncoding.lean', 'Tests.lean', 'lakefile.lean',
                   'lake-manifest.json', 'lean-toolchain'] + [x['path'] for x in raw_inputs]
    normalized_records = {name: sha(raw(name).replace(b'\r\n', b'\n'))
                          for name in sorted(proof_paths)}
    normalized_proof_digest = sha(json.dumps(normalized_records, sort_keys=True,
                                            separators=(',', ':')).encode())
    freeze = {'schema_version': 1, 'status': 'AUTHOR_FROZEN_REVIEW_PENDING_NOT_ADMITTED',
              'author_revision': 'v2 equation-clause-aware source disclosure extraction',
              'superseded_pre_final_binding': 'e57f0d7ebcd8ea6eb9d2d17cdec5555a63d7dbda095f8f212dd88603694cb361',
              'author_extraction_fix': 'IMPLEMENTATION_FAILED: a first-assignment split cut canonicalize inside its nil record. Fixed by detecting leading equation clauses before record assignments. No mathematical refutation or production change.',
              'author_identity': 'constructive_tt_publication_packet; retrospective agent packet author',
              'historical_formalizer': 'unknown; not manufactured',
              'direction_fingerprint': 'CTT_WHOLE_MODULE_MATH_EXPOSITION_AND_BLIND_PACKET',
              'expected_information_gain': 'Remove one coherent next explanation/review bottleneck after deterministic ThinLQ and StoredTensorTrain without changing production proof or overstating the physical frontier.',
              'head_observed': head, 'module_sha256': sha(raw(MODULE)),
              'whole_module_public_inventory_count': len(blocks),
              'binding_sha256': binding,
              'binding_recipe': 'Exact canonical checker recipe, except source lookup is replaced by the owned proposed source row; on integration the row must match byte-equivalent canonical JSON semantics. Target/lesson/toolchain/manifest raw bytes plus sorted complete QuantumBlockEncoding/ABEISTests source bytes are bound.',
              'global_production_raw_sha256': global_digest.hexdigest(),
              'repository_normalized_proof_input_sha256': normalized_proof_digest,
              'global_raw_recipe': 'sha256 of sorted path UTF-8 then raw bytes, QuantumBlockEncoding followed by ABEISTests; toolchain/manifest separately bound in publication digest',
              'toolchain_sha256': sha(raw('lean-toolchain')),
              'manifest_sha256': sha(raw('lake-manifest.json')),
              'lakefile_sha256': sha(raw('lakefile.lean')),
              'lesson_sha256': sha(lesson_bytes),
              'owned_proposed_source_row_sha256': sha(raw(PREFIX + 'author-source-row-candidate.json')),
              'author_supporting_artifacts': {name: sha(raw(PREFIX + name)) for name in
                  ['author-source-coverage.json', 'author-binder-definition-audit.json',
                   'author-graph-views.json', 'author-freeze.py']},
              'formal_context_sha256': sha(context_bytes),
              'decoder_packet_sha256': sha(emit(packet).encode('utf-8')),
              'canonical_publications_sha256_observed': sha(raw('website/research/publications.json')),
              'canonical_sources_sha256_observed': sha(raw('website/research/sources.json')),
              'existing_records_observed': [{'module': r['module'], 'binding_sha256': r['binding_sha256']} for r in publications],
              'existing_records_modified_by_author': False,
              'production_modified_by_author': False, 'Git_modified_by_author': False,
              'fresh_Lean_execution': False, 'build_result': 'NOT_RUN; authoring/metadata checks only',
              'decoder': 'PENDING distinct run', 'source_first_reviewer': 'PENDING distinct run',
              'source_topology_independent_review': 'PENDING', 'PURIFIED': False,
              'Exposition_Seal': 'PENDING', 'main_admission': False,
              'raw_production_inputs': raw_inputs}
    outputs = {LESSON: lesson,
               PREFIX + 'publication-candidate.json': emit(candidate),
               PREFIX + 'author-formal-context.json': emit(context),
               PREFIX + 'author-decoder-packet.json': emit(packet),
               PREFIX + 'author-freeze.json': emit(freeze)}
    print(json.dumps({'outputs': outputs}, ensure_ascii=False))


if __name__ == '__main__':
    main()
