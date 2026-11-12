"""Freeze the narrowly scoped review only after the complete consumer gate passes."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
PARENT=OUT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt_path=OUT/'receipt-v7.json'
audit_path=OUT/'audit-v7-decoder-artifact-c19-v4.json'
receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
audit=json.loads(audit_path.read_text(encoding='utf-8'))
assert receipt['returncode']==0
assert receipt['inputs_unchanged'] and receipt['private_cache_unchanged']
assert receipt['provider_sources_unchanged'] and receipt['original_provider_artifacts_unchanged'] and receipt['native_pins_unchanged']
assert audit['all_30_compared'] and not audit['publication_privacy']['findings']
assert all(c['source_fragment_matches_actual'] and c['own_exact_signature_unique'] and c['own_exact_axiom_report_unique'] and c['decoder_full_signature_matches_own'] and c['decoder_axiom_report_matches_own'] and c['axioms_standard_only'] for c in audit['declarations'])
artifact_path=OUT/'reviewer-artifact-v2.json'
evidence_path=OUT/'reviewer-evidence-v2.json'
assert not artifact_path.exists() and not evidence_path.exists()
common={'schema_version':1,'role':'reviewer','identity':'/root/stored_tt_source_review_c20',
    'run_id':'stored-tt-source-review-c20-v7-final',
    'packet_sha256':'b236f3265e3f1aa8bdb2ec83e018a02ae513149d7bf652c04e86a291a32e6b07',
    'binding_sha256':'fd9ab0393ac26ae3707c90ac6333822ddfa19d96b73d1b1c97ab03a5764afe68',
    'module':'QuantumBlockEncoding/StoredTensorTrain.lean',
    'module_sha256':'a9e5b0c2b00261d6f100a431fa95725c1bead82a4b87c41d54b59f0b084feae4',
    'source_id':'aspbe-local-stored-tensor-train-canonicalization',
    'source_path':'docs/lessons/stored-tensor-train-canonicalization.md',
    'source_sha256':'9d1dd65a177d485c37240cba0b269c530ec3fdb615be0d103f81e5ae14abd9c0'}
artifact={**common,'verdict':'accepted','status':'accepted',
    'acceptance_scope':'Independent whole-module source fidelity, corrected decoder round trip, full actual source fresh elaboration, all30 exact signatures/ordinary axioms and independent consumers. Retrospective local stored real algebraic/eight-counter exact-real scope only.',
    'source_first_precomparison_seal':{'path':(OUT/'source-first-seal.json').relative_to(ROOT).as_posix(),'sha256':sha(OUT/'source-first-seal.json'),
        'reconstruction':(OUT/'source-first-reconstruction.md').relative_to(ROOT).as_posix(),'reconstruction_sha256':sha(OUT/'source-first-reconstruction.md'),
        'before_implementation_decoder_candidate_view':True,'historical_preproof_seal':False,'self_approved_source_topology':False},
    'source_comparison':{'path':(OUT/'source-comparison.md').relative_to(ROOT).as_posix(),'sha256':sha(OUT/'source-comparison.md'),
        'all_30_declarations_and_private_helpers':True,'binder_excess':[],'definition_kinds':'Literal constructions and reindexing/forgetting; no false uniqueness or zero fallback.',
        'carriers':'All real words and all terminal labels; head-first word order; no endian/circuit identification.',
        'rank':'min dimension recurrence, not numerical rank','normalization':'SOURCE input only in boundary_normalized; not a producer premise'},
    'semantic_slots':{
        'target_and_normalization':'Exact real TT contraction at every word/terminal label. Mass-one is conditional only in normalized-boundary consumer.',
        'dimensions_scalars_basis_order':'Natural dimensions including zero; real scalars; column bit*r+j; head-first Word recursion; rank means min dimension recurrence, not numerical rank.',
        'oracle_access':'Already stored nested-vector tables; no coherent/classical oracle claim; stored reads/copies explicitly charged.',
        'ancilla_workspace_terminal':'No circuit/ancilla semantics asserted. All terminal Fin r labels remain, not projected to a clean sector.',
        'phase_and_sign':'Exact real matrix equality preserves real signs across words. No global-phase quotient or complex conjugate-transpose/phase semantics.',
        'error_success_probability':'Exact equality and full squared Euclidean mass. No approximate norm, postselection, success probability or amplification claim.',
        'resource_tier':'Eight-counter extended exact-real stored-operation model; same returned producer cost. Input generation, finite-bit/GCD/runtime/stability/memory/physical gates and cleanup excluded.'},
    'decoder_evidence':{'path':'reviews/publication/stored-tensor-train/decoder-evidence-c19-v4.json','sha256':sha(PARENT/'decoder-evidence-c19-v4.json'),
        'artifact':'reviews/publication/stored-tensor-train/decoder-artifact-c19-v4.json','artifact_sha256':sha(PARENT/'decoder-artifact-c19-v4.json'),
        'independent_correction_audit':(OUT/'decoder-successor-audit-v1.json').relative_to(ROOT).as_posix(),
        'full_own_fresh_signature_audit':audit_path.relative_to(ROOT).as_posix(),'full_own_fresh_signature_audit_sha256':sha(audit_path)},
    'fresh_lean':{'receipt':receipt_path.relative_to(ROOT).as_posix(),'receipt_sha256':sha(receipt_path),'returncode':0,
        'whole_actual_target_source':True,'all_30_exact_signatures_and_standard_axioms':True,'independent_consumers_passed':True,
        'target_cache_imported':False,'production_outputs_requested':False,'source_context_cache_and_native_pins_unchanged':True,
        'provider_count':receipt['provider_count'],'provider_provenance':receipt['cache_provenance']},
    'process_handoff':{'failure_class':'NONE at accepted v7; historical ENV_BLOCKED/IMPLEMENTATION_FAILED retained',
        'salvage':'Complete target/all30 checks from v5/v6 retained; v7 fixes only a closed terminal3 word-cardinality simplification goal, with corrected earlier failure attribution.',
        'process_memory_ids_consulted':[],'direction_fingerprint':'source-first-complete-terminal-stored-cost-produced-binders-c20',
        'expected_information_gain':'Independent source fidelity and detect decoder extraction, terminal projection, numerical-rank, hidden hypotheses or resource-tier drift.',
        'parallel_admission':'Distinct source-first uncertainty explicitly assigned by parent; no subagents spawned.',
        'common_blind_spot':'One mathematical construction, not multiple surviving OR-routes. Shared import-scanner deficiency found and disclosed.',
        'purification':'Pending parent integration/independent exposition acceptance; no self-approved PURIFIED label.'},
    'retained_failures':['preflight-failure-v1.json','failure-v1-public.json','preflight-failure-v2.json','failure-v2-explanation.json','failure-v3-explanation.json','failure-v4-explanation.json','failure-v5-explanation.json','failure-v6-explanation.json'],
    'historical_decoder_failure':'Original absorption signature collision remains FAILED and immutable; v4 independent correction accepted, no silent overwrite.',
    'review_version_note':'v2 fixes only the stale accepted-v6 process marker in reviewer-artifact-v1. Actual accepted run is v7. v1 files retained unchanged; all source, compiler, decoder, hash, mathematical verdict and scope fields are unchanged.',
    'exclusions':['provider-wide freshness/source-cache equivalence','all-repository build','main/publication registry admission','ROOT/scientific closure','finite-bit runtime','input-core generation','numerical stability','peak memory','quantum gate count','physical embedding','isometry completion circuit','finite-angle synthesis','terminal cleanup','website gates','novelty','source-topology self-approval','public purification'],
    'source_reconstruction_approval':'Parent/distinct reviewer must independently inspect the sealed source reconstruction; this author does not self-approve it.'}
artifact_path.write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
evidence={**common,'status':'accepted','verdict':'accepted','source_present':True,
    'artifact':artifact_path.relative_to(ROOT).as_posix(),'artifact_sha256':sha(artifact_path),
    'whole_source_elaboration_receipt':receipt_path.relative_to(ROOT).as_posix(),'whole_source_elaboration_receipt_sha256':sha(receipt_path),
    'decoder_evidence':'reviews/publication/stored-tensor-train/decoder-evidence-c19-v4.json',
    'failure_class':'NONE','source_review_self_approval':False,'scope':artifact['acceptance_scope'],
    'residual_boundary':'Normal inherited pinned provider/native context, not provider fresh rebuild or source/cache equivalence. Parent owns aggregate Lean/Tests/docs/publication/main/root/purification gates and independent source-topology approval.'}
evidence_path.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'artifact':artifact_path.relative_to(ROOT).as_posix(),'artifact_sha256':sha(artifact_path),
    'evidence':evidence_path.relative_to(ROOT).as_posix(),'evidence_sha256':sha(evidence_path),'status':'accepted narrow source/formal scope'},ensure_ascii=False))
