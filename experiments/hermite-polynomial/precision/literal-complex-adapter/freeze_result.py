"""Freeze the actual focused-gate evidence; no scientific-root promotion."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
REL=HERE.relative_to(ROOT).as_posix()

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def bind(p):
    return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}

def save(p,x):
    if p.exists():
        raise SystemExit('Refusing to replace frozen result')
    p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def main():
    gate=HERE/'gate-full-v1.json'
    evidence=json.loads(gate.read_text(encoding='utf-8'))
    if evidence['exit_code'] or not evidence['full_sources'] or not evidence['bound_inputs_unchanged']:
        raise SystemExit('Full source gate not accepted')
    for p,v in evidence['bindings_sha256'].items():
        if sha(ROOT/p)!=v:
            raise SystemExit('Gate input changed: '+p)
    sources=[HERE/(n+'.lean') for n in ['BasisCompatibility','LiteralComplexAdapter','ConsumerChecks']]
    for p in sources:
        if 'sorry' in p.read_text(encoding='utf-8') or '\naxiom ' in p.read_text(encoding='utf-8'):
            raise SystemExit('Proof-placeholder audit failed')
    result={
      'schema_version':1,'cycle':18,'evidence_class':'C_INTERNAL_PROVIDER',
      'status':'proved_locally_pending_distinct_review',
      'objective':'Exact full-matrix literal saved-stage real word to existing complex primitive evaluator through canonical primitiveBasisLEEquiv',
      'roots':['HermiteLiteralComplexAdapter.realWord_eq_primitive',
               'HermiteLiteralComplexAdapter.realWord_input_eq_primitive'],
      'internal_dependencies':['encode_testBit','decode_bit','decode_flip','decode_cxRow','decode_low','decode_high','lift_mul_apply','namedCast_step','namedCast_word'],
      'consumers':['primitive_entry_enclosure','primitive_entry_midpoint_error','primitive_has_exact_real_entries',
                   'chronological_consumer','arbitrary_complex_input_consumer','width_zero_word_empty'],
      'full_source_gate':bind(gate),'sources':[bind(p) for p in sources],
      'statement_seal':bind(HERE/'statement-seal-v1.json'),
      'replay':bind(HERE/'replay.py'),'finite_screen':bind(HERE/'test_discriminators.py'),
      'failure_receipts':[dict(bind(p),failure_class='IMPLEMENTATION_FAILED',
           mathematical_route_retired=False) for p in sorted(HERE.glob('gate-search-*.json'))],
      'assumptions':{'public_bridge_hypotheses':[],
        'CX_distinct':'inherited literal instruction constructor',
        'axioms':'propext, Classical.choice, Quot.sound only; final ConsumerChecks prints actual roots',
        'gridSize_elaboration':'local definition unfolding gridSize n = 2^n; no equality axiom or carrier replacement'},
      'source_graph':{'literal_row':'SavedRounding.realRyRow',
        'literal_word':'SavedStageInterpreter.realWord',
        'canonical_basis':'QuantumBlockEncoding.primitiveBasisLEEquiv',
        'target_evaluator':'QuantumBlockEncoding.evalPrimitiveCircuit',
        'independent_topology_review':'pending'},
      'mathematical_argument':[
        'Induct on width in the EXISTING recursive basis equivalence: encode b = b0 + 2 encode tail. Nat.bit and testBit_bit_succ give testBit(encode b,q)=decide(b q=1).',
        'Invert that identity. Frozen XOR flip complements exactly the target test bit and preserves all other bits. Thus inverse canonical indexing carries literal flip to xBasisAction, low/high to the splitPrimitiveWire inverse at bit0/bit1, and cxRow to existing cxBasisAction.',
        'Reindex a real matrix cast to named primitive coordinates. For RY, reindex the summation by splitPrimitiveWire and collapse the spectator-context identity; the two remaining terms are exactly the signed realRyRow half-angle. For CX, the existing involutive permutation multiplication theorem gives the actual frozen row action.',
        'Induct over chronological foldl. The existing evaluator is eval(rest)*eval(first), so later gates remain on the left. Reindex back by primitiveBasisLEEquiv and specialize the cast identity matrix.',
        'Substitute whole-matrix equality into frozen interval enclosure/midpoint theorems and into arbitrary complex-vector multiplication. Imaginary entries are identically zero.'
      ],
      'finite_diagnostics':{'tests':5,'widths':'0 through5 as applicable','scope':'screening only',
        'checks':['width0','signed halfangle','all spectator wires and CX directions','noncommuting chronological-order discriminator','complex input']},
      'scientific_ROOT':False,'full_family_acceptance':False,'public_PURIFIED':False,
      'stageEta_complex_operator_transport':'OPEN','uniform_error_budget':'OPEN',
      'local_support_lift':'OPEN','classical_runtime_resources':'OPEN',
      'repository_build_Tests_site_gates':'parent-owned integration gates; not claimed by focused receipt',
      'independent_review':'pending distinct reviewer',
      'failure_class':'NONE','salvage':'arbitrary-width canonical basis and full gate/word bridges locally compiled',
      'token_usage':None,'process_memory_ids':['QBE-PM-DENSE-CHECK-SMALL-INSTANCE'],
      'direction_fingerprint':'canonical-recursive-LE-testBit;named-wire-sparse-sum;chronological-full-matrix-cast',
      'expected_information_gain':'Close evaluator identification frontier without inventing a circuit or assuming compatibility',
      'parallel_admission':'single assigned worker, no child agents',
      'common_blind_spot_review':'pending distinct review of register/order/phase and full-carrier claims',
      'purification':'local duplicate-semantics and placeholder audit passed; public purification pending integration/review',
      'scope':'all writes confined to '+REL,
      'writes_stopped_after_handoff':True}
    save(HERE/'result-v1.json',result)
    handoff={'schema_version':1,'result':bind(HERE/'result-v1.json'),
      'objective_frontier_node':'literal-real saved-stage evaluator identification',
      'mathematical_delta':'Exact symbolic arbitrary-width full-operator bridge to existing primitive semantics; no phase or garbage quotient',
      'effect_on_root_frontier':'Evaluator identification closed locally; precision/scientific/runtime/root acceptance remains open',
      'named_evidence':result['roots']+result['consumers'],
      'files_changed':[p.relative_to(ROOT).as_posix() for p in sorted(HERE.iterdir()) if p.is_file()],
      'reuse_insight':'The two-entry RY row formula follows by splitting the existing primitive wire, not introducing a second circuit matrix semantics',
      'failure_class':'NONE','salvage_audit':'compiled basis compatibility and whole-matrix step/word supplied; failed receipts preserved',
      'residual_risk':'distinct source/semantic review pending; integration gates parent-owned',
      'recommended_next_fork':'Use exact matrix equality to transport stageEta real operator error into the existing complex operator model; separately prove local-support lift',
      'context_digest':'Canonical primitiveBasisLEEquiv, signed theta/2, CX direction and distinct, later-left order; width0 and all spectators included',
      'source_Lean_expansion_nodes':result['source_graph'],
      'boundaries':{'scientific_ROOT':False,'public_PURIFIED':False,'uniform_runtime_resources':False},
      'token_usage':None,'ALL_WRITES_STOPPED':True}
    save(HERE/'handoff-v1.json',handoff)
    print('result-v1.json SHA256:',sha(HERE/'result-v1.json'))
    print('handoff-v1.json SHA256:',sha(HERE/'handoff-v1.json'))

if __name__=='__main__':
    main()
