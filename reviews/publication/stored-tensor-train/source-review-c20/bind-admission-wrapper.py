"""Independently compare metadata-only successors, then bind new reviewer packaging."""
from pathlib import Path
import hashlib, importlib.util, json, re
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
PARENT=OUT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
old_candidate_path=PARENT/'publication-candidate.json'
new_candidate_path=PARENT/'publication-candidate-v2.json'
wrapper_path=PARENT/'decoder-admission-evidence-v1.json'
original_decoder_path=PARENT/'decoder-evidence-c19-v4.json'
frozen_evidence_path=OUT/'reviewer-evidence-v2.json'
frozen_artifact_path=OUT/'reviewer-artifact-v2.json'
dest=OUT/'reviewer-admission-evidence-v1.json'
packet_path=OUT/'admission-comparison-packet-v1.json'
artifact_path=OUT/'admission-comparison-artifact-v1.json'
assert all(not p.exists() for p in [dest,packet_path,artifact_path])
assert sha(new_candidate_path)=='b525b7398f40d046942841bed1251f87538b8cf82dd8ab99fa0114cfe6d77685'
assert sha(wrapper_path)=='a62cb24b49830d263ef9ca3ec030cc4cdb5479f93462a960a99b334c3fccc121'
old,new,wrapper,decoded=map(read,[old_candidate_path,new_candidate_path,wrapper_path,original_decoder_path])
changed={k:{'old':old.get(k),'new':new.get(k)} for k in old.keys()|new.keys() if old.get(k)!=new.get(k)}
assert set(changed)=={'residual_boundary','decoder_evidence','reviewer_evidence','status','binding_sha256'}
math_fields=['module','source_id','source_statement','source_anchor','lesson_path','declarations','obligation_map','assumption_deltas','graph_contribution','formalizer']
assert all(old[k]==new[k] for k in math_fields)
assert wrapper['original_context_binding_sha256']==old['binding_sha256']
assert wrapper['binding_sha256']==new['binding_sha256']=='20dbb523afbc95af7098d3fb50498946212dabbfab45a01e18544a9b27c99495'
assert all(wrapper[k]==v for k,v in decoded.items() if k!='binding_sha256')
assert wrapper['original_evidence_sha256']==sha(original_decoder_path)
assert wrapper['artifact_sha256']==sha(ROOT/wrapper['artifact_path'])
assert wrapper['packet_sha256']==sha(ROOT/wrapper['packet_path'])
assert wrapper['source_blind'] is True and wrapper['new_lean_execution'] is False
assert wrapper['format_packaging']['new_decoder_execution'] is False
assert wrapper['identity']=='/root/stored_tt_blind_decoder_c19'
assert wrapper['run_id']=='stored-tt-blind-decoder-c19-v4-repair'
spec=importlib.util.spec_from_file_location('publication_checker',ROOT/'website/scripts/check_research_publications.py')
checker=importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
old_actual=checker.binding_digest(ROOT,old)
new_actual=checker.binding_digest(ROOT,new)
assert old_actual==old['binding_sha256']
assert new_actual==new['binding_sha256']
frozen_artifact=read(frozen_artifact_path)
frozen_evidence=read(frozen_evidence_path)
assert frozen_evidence['verdict']=='accepted' and frozen_artifact['fresh_lean']['returncode']==0
assert frozen_evidence['binding_sha256']==old_actual
packet={'schema_version':1,'role':'anti-anchored-reviewer-metadata-comparison','identity':'/root/stored_tt_source_review_c20',
    'source_first_seal':(OUT/'source-first-seal.json').relative_to(ROOT).as_posix(),'source_first_seal_sha256':sha(OUT/'source-first-seal.json'),
    'frozen_source_review_artifact':frozen_artifact_path.relative_to(ROOT).as_posix(),'frozen_source_review_artifact_sha256':sha(frozen_artifact_path),
    'frozen_source_review_evidence':frozen_evidence_path.relative_to(ROOT).as_posix(),'frozen_source_review_evidence_sha256':sha(frozen_evidence_path),
    'original_candidate':old_candidate_path.relative_to(ROOT).as_posix(),'original_candidate_sha256':sha(old_candidate_path),
    'new_candidate':new_candidate_path.relative_to(ROOT).as_posix(),'new_candidate_sha256':sha(new_candidate_path),
    'decoder_wrapper':wrapper_path.relative_to(ROOT).as_posix(),'decoder_wrapper_sha256':sha(wrapper_path),
    'original_decoder_evidence':original_decoder_path.relative_to(ROOT).as_posix(),'original_decoder_evidence_sha256':sha(original_decoder_path),
    'actual_changed_keys':changed,'unchanged_mathematical_fields':math_fields,
    'old_actual_recomputed_binding_sha256':old_actual,'new_actual_recomputed_binding_sha256':new_actual,
    'new_lean_or_decoder_execution':False,'metadata_only':True,
    'anti_anchoring_provenance':'The frozen source-only reconstruction predates implementation/decoder/candidate viewing. This successor only rebinds faithfully compared packaging; it is not a fresh mathematical verdict or decoder execution.'}
packet_path.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
slots={
    'target':'Same already stored real TT; actual returned residual and right-canonical chain; exact all-word/all-terminal action and entire semantic returned-Result refinement.',
    'normalization':'Same full squared mass semantics. Only boundary_normalized assumes input mass one; canonicalize and boundary_mass do not.',
    'registers':'Natural finite bonds including zero; head-first recursive words; flattened bit*r+j; terminal Fin r unchanged; min-dimension recurrence, not numerical rank or physical endian basis.',
    'oracles':'Already stored nested-vector real tables, charged stored access/materialization; no coherent oracle or uncharged input generation premise/claim.',
    'ancillas_phases':'No quantum ancilla, physical embedding or cleanup theorem. Full terminal labels retained. Exact real signs preserved; no complex conjugate-transpose or global-phase quotient semantics.',
    'error_success':'Exact algebraic equalities and all-terminal mass; no approximation, projected garbage sector, postselection, success probability or amplification resource claim.',
    'resources':'Same eight-counter stored extended exact-real cost for the actual producer, including materialized absorption and node costs; no finite-bit/runtime/stability/peak-memory/input-generation/physical-gate/synthesis/cleanup claim.'}
artifact={'schema_version':1,'role':'reviewer','identity':'/root/stored_tt_source_review_c20','run_id':'stored-tt-source-review-c20-admission-metadata-v1',
    'verdict':'accepted','anti_anchored':True,'metadata_only':True,'new_lean_execution':False,
    'packet_path':packet_path.relative_to(ROOT).as_posix(),'packet_sha256':sha(packet_path),
    'binding_sha256':new_actual,'original_context_binding_sha256':old_actual,
    'source_fidelity_and_formal_verdict':'Inherited exactly from independently authored/frozen whole-source c20 v7 review; all30 exact-v4 signatures/ordinary axioms and independent consumers passed.',
    'metadata_comparison':'Independently compared actual objects, not parent assertion: only five candidate metadata keys differ; only residual_boundary is among binding-relevant fields. All mathematical fields/formal/source/toolchain contexts are equal. Original and successor bindings recomputed with the actual checker.',
    'decoder_wrapper_comparison':'Every original v4 decoder evidence field except binding preserved; exact identity/run/reconstruction/sourceblind status/artifact/receipts preserved. Parent packaging is not a new decoder run.',
    'semantic_slots':slots,'original_source_review_evidence':frozen_evidence_path.relative_to(ROOT).as_posix(),
    'original_source_review_evidence_sha256':sha(frozen_evidence_path),'original_source_review_artifact':frozen_artifact_path.relative_to(ROOT).as_posix(),
    'original_source_review_artifact_sha256':sha(frozen_artifact_path),
    'decoder_evidence_sha256':sha(wrapper_path),'self_approval_of_source_topology':False,
    'remaining_boundary':frozen_evidence['residual_boundary'],
    'no_production_git_task_registry_site_changes':True}
artifact_path.write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
evidence={**artifact,'artifact_path':artifact_path.relative_to(ROOT).as_posix(),'artifact_sha256':sha(artifact_path),
    'status':'accepted','decoder_evidence_path':wrapper_path.relative_to(ROOT).as_posix()}
dest.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path_pattern=re.compile(r'(?i)(?:[a-z]:[\\/]|file://|/(?:home|Users|tmp|mnt)/)')
assert not any(path_pattern.search(p.read_text(encoding='utf-8')) for p in [packet_path,artifact_path,dest])
print(json.dumps({'evidence':dest.relative_to(ROOT).as_posix(),'evidence_sha256':sha(dest),
    'artifact':artifact_path.relative_to(ROOT).as_posix(),'artifact_sha256':sha(artifact_path),
    'packet_sha256':sha(packet_path),'candidate_changed_keys':list(changed),
    'new_binding_recomputed':new_actual,'old_binding_recomputed':old_actual,
    'new_lean_execution':False,'privacy':'no literal local paths in new wrapper packet/artifact/evidence'},ensure_ascii=False))
