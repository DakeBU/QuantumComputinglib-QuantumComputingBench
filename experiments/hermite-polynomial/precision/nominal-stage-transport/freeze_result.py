"""Bind a successful final whole-source gate without overwriting earlier receipts."""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REL = HERE.relative_to(ROOT).as_posix()

def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def main():
    output = HERE / 'result-v1.json'
    if output.exists():
        raise SystemExit('Refusing to overwrite frozen result')
    gate_path = REL + '/gate-full-v1.json'
    gate = json.loads((ROOT / gate_path).read_text(encoding='utf-8'))
    if gate['exit_code'] != 0 or not gate['full_sources'] or not gate['bound_inputs_unchanged']:
        raise SystemExit('Final fresh whole-source gate is not accepted')
    for path, expected in gate['bindings_sha256'].items():
        if digest(path) != expected:
            raise SystemExit('Final gate binding mismatch: ' + path)
    axiom_union = set()
    for row in gate['execution']:
        log_text = (ROOT / row['log']).read_text(encoding='utf-8')
        if digest(row['log']) != row['log_sha256'] or 'sorryAx' in log_text:
            raise SystemExit('Successful gate log contains binding/axiom failure')
        for match in re.finditer(r'depends on axioms:\s*\[([^\]]*)\]', log_text):
            axiom_union.update(s.strip() for s in match.group(1).split(',') if s.strip())
    if axiom_union != {'propext', 'Classical.choice', 'Quot.sound'}:
        raise SystemExit('Unexpected final axiom union')
    paths = set(gate['bindings_sha256'])
    paths.update(p.relative_to(ROOT).as_posix() for p in HERE.iterdir()
                 if p.is_file() and p.name != output.name)
    paths.add('experiments/hermite-polynomial/precision/nonunitary-transport/ConsumerChecks.lean')
    paths.add('QuantumBlockEncoding/PrimitiveSemantics.lean')
    paths.add('QuantumBlockEncoding/PrimitiveBasisLE.lean')
    paths.add('QuantumBlockEncoding/StatePreparationPrimitiveRoutes.lean')
    result = {
        'schema_version': 1, 'task': 'SP-HERMITE-POLY-002', 'cycle': 17,
        'evidence_class': 'C_INTERNAL_PROVIDER', 'status': 'PROVED_LOCAL_FOCUSED',
        'objective': 'Unconditional literal full-carrier real nominal contraction and produced actual nonunitary-stage chronological transport',
        'namespace': 'HermiteNominalStageTransport',
        'mathematical_delta': 'Every frozen arbitrary-width real RY/CX word preserves the full real Euclidean norm, hence contracts. Frozen stageCenter and produced stageEta form actual CLM stages with all Valid conjuncts internally discharged. Their chronological product and vector application error are bounded by product(1+eta)-1 against the literal flattened exact word.',
        'effect_on_root_frontier': 'Closes nominal exact-stage contraction and actual stages Valid/product/apply prerequisite from c16. Does not close complex circuit adapter, saved parser, source-to-stored TT, readout, runtime/resources or scientific ROOT.',
        'roots': [
            'sum_involution', 'ry_pair_square', 'vectorStep_ry_pair', 'vectorStep_sum_square',
            'realStep_mulVec', 'realStep_norm_preservation', 'realWord_norm_preservation',
            'nominal_norm_preservation', 'nominal_contraction', 'stageEta_nonneg',
            'actual_stage_valid', 'actual_stages_valid', 'actual_product_error', 'actual_apply_error',
            'realIdentity_eq_one', 'realStep_right_mul', 'realWord_right_mul',
            'realWord_append_composition', 'nominalProduct_eq_flatten',
            'actual_flatten_product_error', 'actual_flatten_apply_error',
            'changing_full_norm', 'changing_full_valid', 'changing_full_apply',
            'empty_width_valid', 'literal_signed_high_column', 'literal_signed_low_column'],
        'assumptions': 'Roots take only width, valid literal instruction words, degree/grid data, and arbitrary real full-carrier vector. CX distinct is instruction syntax. No contraction/Valid/surrogate unitarity/phase quotient/normalization/initial membership/tolerance premise.',
        'conventions': 'Fin(2^width), width including 0, q0 LSB, physical bit flip, RY row0 c*u-s*v and row1 s*u+c*v at exact rational theta/2, literal CX control direction. Full Euclidean norm, not entrywise Matrix norm. Chronological list/foldl and latest factor on left. All spectators and garbage retained.',
        'literal_definition': 'actualStage nominal=toEuclideanCLM(realWord word realIdentity), surrogate=toEuclideanCLM(stageCenter word degree bits), error=cast stageEta; actualStages maps over chronological word list.',
        'proof_explanation': 'The exact signed RY pair preserves u^2+v^2 using sin^2+cos^2=1. Compare the output row at i and flip(i), then sum over the full carrier; involutive reindexing turns both pair sums into twice the global square sum. CX is an involutive permutation because distinct targets preserve the control bit. Matrix mulVec commutes with these literal row actions, so every exact step preserves the Euclidean norm of every transformed vector. Word induction from identity proves unconditional nominal norm preservation and opnorm<=1. Frozen interval enclosure supplies nonnegative maxRadius and eta, and the frozen CLM difference bound supplies the third Valid conjunct. Existing nonunitary product-error transport then applies without surrogate contraction. Right matrix multiplication commutes with linear row action; chronological append and CLM multiplicativity identify nominal products with realWord words.flatten. Substitution and le_opNorm give error on every vector.',
        'source_lean_expansion': 'Literal pair/permutation -> full square sum -> mulVec -> Euclidean CLM norm -> exact word contraction; frozen enclosure/radius/error -> produced Stage.Valid -> existing product growth -> chronological exact flatten identity -> full vector apply error.',
        'reuse': 'Frozen SavedStageInterpreter and StageOperatorBound, Mathlib Euclidean CLM and Real.sin_sq_add_cos_sq, existing ExperimentalNonunitaryTransport product_error_le. PrimitiveSemantics/PrimitiveBasisLE/StatePreparationPrimitiveRoutes searched but not imported as an unproved custom-real semantics adapter.',
        'finite_discriminators': 'Five independent exact-rational tests cover signed rotations/Gram, spectator full blocks, asymmetric CX/q0 LSB, chronology, width0 and exact CX involution, actual frozen expanding surrogate [[1,-1],[1,1]] with Gram2I, multiplicative-vs-additive growth, and separate stage-midpoint-product versus whole-word midpoint. Rational rotation test matrices are convention diagnostics, not exact evaluation of rational-theta trigonometry. Two compiled symbolic literal RY signed-column guards check actual vectorStep signs for every rational theta.',
        'gate': {'path': gate_path, 'sha256': digest(gate_path)},
        'execution': gate['execution'],
        'bindings_sha256': {p: digest(p) for p in sorted(paths)},
        'axioms_expected_union': ['propext', 'Classical.choice', 'Quot.sound'],
        'axioms_checked_union': sorted(axiom_union),
        'new_axioms': False, 'new_sorry': False, 'new_native_decide': False,
        'failure_class': 'NONE_FOR_FINAL_PROVIDER; IMPLEMENTATION_FAILED_FOR_RETAINED_SEARCH_RECEIPTS',
        'authoring_failures': [
            'search-v1: ambiguous flip_flip and underspecified sum reindex functions; cast through opaque actualStage not unfolded. No mathematical contradiction.',
            'search-v3/v4: chronology proof simplification did not expand the RHS matrix product underneath an unfolded row-action lambda. Scoped Matrix notation was made explicit; early Matrix.mul_apply rewrite repairs the proof route. Consumer changed during failed v3; bound_inputs_unchanged=false. Failed records excluded from final evidence.',
            'search-v5: chronology provider compiled with ordinary3, but two new sign guards had ambiguous flip simplifier names and emitted Lean recovery sorryAx. Failed source/log receipt retained and excluded; fully qualified literal flip fixes the implementation. Replay/freezer were edited during search-v5, so its binding check is also excluded.',
            'Pre-proof read-only path typo caused ENV_BLOCKED command creation; corrected immediately with no file mutation.'
        ],
        'failure_receipts': [REL + '/gate-search-v1.json', REL + '/gate-search-v3.json', REL + '/gate-search-v4.json', REL + '/gate-search-v5.json'],
        'salvage_audit': 'All final mathematical helpers reach roots or real consumers. search-v2 proved contraction/actual Valid/product/apply before additive flatten consumer. Failed search sources are content-hash recorded, logs retained, no false mathematical route retirement. Private cache is not final proof evidence.',
        'process_memory_ids': ['QBE-PM-LOW-TOKEN-CONTROL-PLANE', 'QBE-PM-DENSE-CHECK-SMALL-INSTANCE', 'QBE-PM-VERIFIER-SEMANTIC-LEVEL'],
        'direction_fingerprint': 'literal-real-pair-permutation-norm-to-produced-stage-valid',
        'expected_information_gain': 'Close c16 nominal contraction/Valid prerequisite and end-to-end chronological real-word error without assuming surrogate unitarity or complex adapter.',
        'parallel_admission': 'Parent-authorized substantive worker; no worker subagents.',
        'common_blind_spot_review': 'PENDING_PARENT_OWNED',
        'independent_review': 'PENDING_PARENT_OWNED',
        'default_verified_route': 'Direct literal real norm proof; complex circuit adapter remains a distinct open route, not a competing certified result.',
        'purification': 'Internal helper reachability checked; no public/source-anchor PURIFIED or Exposition Seal claimed.',
        'remaining': [
            'Actual real-to-complex PrimitiveSemantics arbitrary-width bit/order/entry adapter',
            'Saved parser/Python Fraction/Int/in-place/runtime and caps refinement',
            'Saved stage partitions, physical wire maps, data-first TT and full terminal readout',
            'Source-to-stored C/QR/source norm floor and all global error stages',
            'Degree/grid selection or checked requested eta and final epsilon',
            'Efficient small-support lifting or explicitly charged dense 4^width matrix work/storage',
            'Uniform input/intermediate integer denominator/GCD/runtime/storage and physical synthesis costs',
            'C2', 'C3', 'X2', 'ROOT'],
        'cost_boundary': 'The mathematical full-carrier theorem is symbolic. stageCenter/stageEta dense materialization requires 4^width entries; no polynomial resource theorem follows. Local support/rank lifting and all scalable costs remain open.',
        'scientific_root': False, 'source_anchor': False, 'public_purified': False,
        'uniform_finite_bit_certificate': False, 'surrogate_unitarity_assumed': False,
        'full_repository_gate': 'Parent-owned; focused fresh whole experimental provider/consumer gate only.',
        'scope': REL + '/', 'worker_git_mutations': False,
        'parent_owns_checkpoint': True, 'per_worker_tokens': 'unknown',
        'recommended_next': 'Independent exact-source/auditor replay, then parent checkpoint. Next independent mathematical bridge is arbitrary-width custom-real to existing complex PrimitiveSemantics, or full saved stage partition/TT/readout adapter.'
    }
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Frozen result SHA256:', digest(output.relative_to(ROOT).as_posix()))

if __name__ == '__main__':
    main()
