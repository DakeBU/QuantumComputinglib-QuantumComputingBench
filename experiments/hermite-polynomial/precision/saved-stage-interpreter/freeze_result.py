"""Create one immutable structured C-provider handoff from exact passing gates."""
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REL = HERE.relative_to(ROOT).as_posix()

def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def main():
    out = HERE / 'result-v1.json'
    if out.exists():
        raise SystemExit('Refusing to replace immutable result')
    gate_path = f'{REL}/gate-full-v1.json'
    gate = json.loads((ROOT / gate_path).read_text(encoding='utf-8'))
    if gate['exit_code'] or not gate['full_sources'] or not gate['bound_inputs_unchanged']:
        raise SystemExit('Full-source passing gate required')
    for path, sha in gate['bindings_sha256'].items():
        if digest(path) != sha:
            raise SystemExit('Exact gate binding changed: ' + path)
    for path in HERE.glob('*.lean'):
        if re.search(r'\b(?:sorry|admit|axiom|native_decide|unsafe)\b', path.read_text(encoding='utf-8')):
            raise SystemExit('Forbidden Lean token: ' + path.name)
    result = {
        'schema_version': 1,
        'task': 'SP-HERMITE-POLY-002', 'cycle': 16,
        'evidence_class': 'C_INTERNAL_PROVIDER', 'status': 'PROVED_LOCAL_FOCUSED',
        'objective': 'Literal changing-target RY/CX full-matrix interval interpreter and stage-end Euclidean eta supplier',
        'mathematical_delta': 'Unconditional full matrix entry enclosure from exact identity through arbitrary chronological physical RY/CX word; stage-end-only midpoint entry error; finite all-entry max radius, nonnegativity and explicit Euclidean CLM operator error <= 2^width*maxradius. No fixed-pair-only restriction.',
        'effect_on_root_frontier': 'Closes c15 saved_stage_next full interval matrix and dimension-aware eta provider. Nominal contraction, primitive circuit adapter, stage partitions/TT/readout and ROOT remain open.',
        'namespace': 'HermiteSavedStageInterpreter',
        'roots': ['flip_flip', 'bit_flip', 'bit_flip_other', 'cxRow_involutive',
                  'identity_encloses', 'step_encloses', 'word_encloses',
                  'stage_enclosure', 'stage_midpoint_error',
                  'entryRadius_le_maxRadius', 'maxRadius_nonneg_of_encloses',
                  'stage_maxRadius_nonneg', 'stage_max_entry_error',
                  'real_entry_bound_euclidean_opnorm', 'stage_euclidean_operator_error',
                  'changing_target_CX_full_matrix', 'changing_target_CX_end_error',
                  'actual_first_saved_angle_full_matrix', 'changing_target_CX_eta'],
        'assumptions': 'Stage roots have only width, valid literal instruction word, degree and bits data. Initial membership discharged by singleton identity; trigonometric enclosure produced by FiniteTrig/SavedRounding. CX distinct is instruction syntax. No Valid, nominal contraction, surrogate unitarity, phase quotient or normalization premise.',
        'conventions': 'Basis Fin(2^width), q0 least significant via Nat.testBit/xor 2^q; row0 c*u-s*v and row1 s*u+c*v at exact rational theta/2. Full square matrices, every row/column and garbage coordinate. All RY output intervals outward-rounded; CX permutation exact; midpoint only after full word. Explicit real Euclidean induced CLM norm.',
        'source_lean_expansion': 'Identity -> produced Taylor/outward row bounds -> physical pair selection and exact CX permutation -> chronological full matrix induction -> final midpoint entries -> finite sup -> per-row Cauchy-Schwarz -> dimension-squared vector norm estimate -> explicit Euclidean opnorm eta.',
        'literal_runtime_link': '5 exact finite tests compare independent functional output-row matrix routing/Taylor formulas against immutable saved_action.py actual in-place row-pair implementation and eta. This is finite exact refinement evidence, not formal Python runtime or parser correctness.',
        'finite_discriminators': ['q0-LSB mask and asymmetric CX direction',
                                  'actual changing-target/CX all 4x4 center entries/radius/eta',
                                  'empty word and exact CX involution',
                                  'chronological reversal changes result',
                                  'early-midpoint changes result',
                                  'forcing same RY target changes result'],
        'proof_explanation': 'Entry enclosure follows induction on the actual instruction list. RY applies the previously certified signed rounded pair to the two physical predecessor rows; CX selects its exact predecessor row. Identity intervals enclose real identity. A final interval midpoint differs by at most halfwidth. The maximum halfwidth is nonnegative because enclosure supplies ordered endpoints. For error matrix A with entry abs<=r, Cauchy-Schwarz bounds each output row square by size*r^2*||x||^2. Summing size rows gives ||Ax||^2<=size^2*r^2*||x||^2, hence Euclidean operator norm<=size*r.',
        'direction_fingerprint': 'variable-target-CX-full-matrix-interval-refinement',
        'expected_information_gain': 'Remove c15 same-pair/CX and scalar-to-operator gaps independently of finite-middle-source work.',
        'process_memory_ids': ['QBE-PM-LOW-TOKEN-CONTROL-PLANE',
                               'QBE-PM-DENSE-CHECK-SMALL-INSTANCE',
                               'QBE-PM-VERIFIER-SEMANTIC-LEVEL'],
        'parallel_admission': 'Human-authorized parent fork; independent full-stage uncertainty; no worker subagents.',
        'common_blind_spot_review': 'PENDING_PARENT_OWNED',
        'independent_review': 'PENDING',
        'default_verified_route': 'Literal matrix interpreter; no alternative norm or circuit route selected.',
        'failure_class': 'NONE_FOR_FINAL_FOCUSED_PROVIDER',
        'authoring_failures': ['search-v1 IMPLEMENTATION_FAILED: root pow lemma was incorrectly namespaced; corrected without contract change.',
                              'search-v4 IMPLEMENTATION_FAILED: Matrix notation scope and nonexistent simplifier name, plus maxradius elaboration timeout.',
                              'search-v5/v6 IMPLEMENTATION_FAILED: finite-supremum le_sup type inference timed out. Generic nonnegativity isolation alone did not fix it; explicitly unfolding maxRadius and annotating the supremum carrier/function in v7 resolved elaboration.'],
        'failure_receipts': sorted(f'{REL}/{p.name}' for p in HERE.glob('gate-search-*.json')),
        'salvage_audit': 'All final Lean definitions and lemmas reach full-matrix entry or operator roots/consumers. Failed gates retained; no mathematics retired due to implementation errors. Private cache/probes not proof evidence.',
        'purification': 'Internal helper reachability checked. Production/source-blind/reader purification and Exposition Seal not claimed.',
        'remaining': ['Formal Python Fraction/Int/parser/in-place-loop refinement including caps',
                      'Adapter of realWord to existing complex PrimitiveSemantics circuit evaluation',
                      'Nominal exact-stage Euclidean contraction and actual NonunitaryTransport.Valid/product integration',
                      'Saved stage partitions, wire maps, data-first TT and full terminal readout refinement',
                      'Source-to-stored C, QR error and source norm floor',
                      'Uniform Hermite family finite-bit/runtime/storage/GCD/physical synthesis and scientific ROOT'],
        'recommended_next': 'Prove exact realStep norm preservation (RY orthogonal pair and CX involutive row permutation), derive nominal contraction, then supply actual NonunitaryTransport stages; separately bridge physical stage partition and all-garbage TT action.',
        'gate': {'path': gate_path, 'sha256': digest(gate_path)},
        'execution': gate['execution'],
        'bindings_sha256': gate['bindings_sha256'],
        'axioms_expected_union': ['propext', 'Classical.choice', 'Quot.sound'],
        'new_axioms': False, 'new_sorry': False, 'new_native_decide': False,
        'scientific_root': False, 'source_anchor': False,
        'uniform_finite_bit_certificate': False, 'surrogate_unitarity_assumed': False,
        'full_repository_gate': 'Parent-owned; focused independent experimental sources only, not production import graph.',
        'worker_git_mutations': False, 'parent_owns_checkpoint': True,
        'scope': REL + '/ only', 'per_worker_tokens': 'unknown'
    }
    out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('result-v1 SHA256:', digest(out.relative_to(ROOT).as_posix()))

if __name__ == '__main__':
    main()
