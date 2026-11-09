#!/usr/bin/env python3
"""Reproduce projections/proposals/manifest from authored, reviewed batch files.

This checks bindings, not mathematical correctness or admission. It never edits
authored QA, frozen questions, review records, source, registry or other tracks.
"""
from pathlib import Path
import json, hashlib, sys

P=Path(__file__).resolve().parent
R=P.parents[5]
B=R/'benchmarks/quantumcomputingbench'
sys.path.insert(0,str(B/'src'))
from qcb_core import digest
from qcb_textbook_policy import CONTRACT_FIELDS

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def relative(p):return str(p.relative_to(R))
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def display(x):
 if isinstance(x,str):return x
 if isinstance(x,list):return '; '.join(display(y) for y in x)
 if isinstance(x,dict):return ' '.join('**'+k.replace('_',' ')+':** '+display(v) for k,v in x.items())
 return str(x)
def band(q):
 d=q['difficulty']
 return d.get('construction_band') or d.get('D1_D4',{}).get('provisional_route_band') or d.get('provisional_route_band') or d.get('level')

baseline=read(P/'evidence/baseline.json')
snapshot=read(R/baseline['graph']['path']);nodes={x['id']:x for x in snapshot['nodes']}
payloads=[read(p) for p in sorted((P/'qa').glob('*.json'))]
assert len(payloads)==6 and {q['slot'] for q in payloads}=={'G1','G2','P1','P2','E1','E2'}
review_index=[];proposals=[];questions=[];references=[];source_files={};node_roles={}
question_md=['# Batch 2 — questions only','',
 'Six proposed mathematical targets. These public supplementary questions have unassigned splits and add no admitted cores.','']
reference_md=['# Batch 2 — reference solutions and rubrics','',
 'Read QUESTIONS.md separately when attempting the problems. References are public authored mathematics with the content-bound review status in review-index.json.','']
rows=[]
for q in payloads:
 slot=q['slot'];qp=P/'qa'/f'{slot}.json';frozen=read(P/'questions'/f'{slot}.json')
 for k in ['core_id','question','assumptions','conventions']:assert q[k]==frozen[k],(slot,k)
 for k in ['mathematical_target','reference_answer','rubric','reasoning_map','boundary_cases','common_errors','source_refs','unverified','overlap','family']:assert q.get(k),(slot,k)
 assert q['core_id']=='candidate:'+q['proposal_id']
 assert q['admission']=='candidate_not_counted' and q['dedup_review_required'] is True
 assert q['split']=='unassigned_pending_reconciliation'
 report_path=P/'reviews'/f'{slot[0]}-review.json';report=read(report_path)
 assert report['reviewer']!=q['author']
 matches=[x for x in report['items'] if x['core_id']==q['core_id']];assert len(matches)==1
 review=matches[0];assert review['item_digest']==digest(q),(slot,'stale review')
 assert review.get('payload_sha256_raw',sha(qp))==sha(qp)
 assert review.get('reasoning') and review.get('source_checks')
 rr={'slot':slot,'core_id':q['core_id'],'reviewer':report['reviewer'],'report_path':relative(report_path),'report_sha256':sha(report_path),'item_digest':digest(q),'payload_sha256':sha(qp),'verdict':review['verdict'],'semantic_core_verdict':review['semantic_core_verdict'],'human_approval':False,'admission':'candidate_not_counted'}
 review_index.append(rr)
 sources=q['target_nodes']+q['supporting_nodes']
 for role,key in [('target','target_nodes'),('support','supporting_nodes')]:
  for node in q[key]:
   assert node in nodes,(slot,node)
   node_roles.setdefault(node,{'node':nodes[node],'uses':[]})['uses'].append({'slot':slot,'role':role})
 for ref in q['source_refs']:
  path=ref['path'];f=R/path;assert f.is_file(),path
  raw=sha(f);lf=hashlib.sha256(f.read_text(encoding='utf-8').encode()).hexdigest()
  expected=ref.get('sha256') or ref.get('sha256_raw') or ref.get('raw_sha256') or ref.get('sha256_lf')
  assert expected in [raw,lf],(slot,path,'source hash mismatch')
  source_files.setdefault(path,{'path':path,'source_commit':baseline['base_commit'],'sha256_raw':raw,'sha256_lf':lf,'uses':[]})['uses'].append({'slot':slot,'source_ref':ref})
 contract={k:q[k] for k in CONTRACT_FIELDS}
 proposal={'proposal_id':q['proposal_id'],'track':'non-lean','author':q['author'],'core_id':q['core_id'],'admission':'candidate_not_counted','dedup_review_required':True,'source_nodes':list(dict.fromkeys(sources)),'view_kind':'derivation','family':q['family'],'split':q['split'],'snapshot_id':q['snapshot_id'],'contract_hash':digest(contract),'base_commit':baseline['base_commit'],'package_id':P.name,'slot':slot,'payload_path':relative(qp),'payload_sha256':sha(qp),'item_digest':digest(q),'title':q['title'],'mathematical_target':q['mathematical_target'],'review_records':[rr],'status':'authored_with_content_bound_AI_review_pending_maintainer_decision','count_effect':'zero_until_explicit_admission','usage':'public_supplementary_diagnostic_only; no training or independent-held-out clearance','proposed_contract':contract}
 pp=B/'tracks/non-lean/proposals'/f"{q['proposal_id']}.json";write(pp,proposal);proposals.append(pp)
 questions.append({k:q[k] for k in ['slot','core_id','title','question','assumptions','conventions']})
 references.append({'slot':slot,'core_id':q['core_id'],'item_digest':digest(q),'reference_answer':q['reference_answer'],'rubric':q['rubric'],'boundary_cases':q['boundary_cases'],'common_errors':q['common_errors'],'reasoning_map':q['reasoning_map']})
 question_md+=['## '+slot+' — '+q['title'],'','### Assumptions','']+['- '+x for x in q['assumptions']]+['','### Conventions','']+['- '+x for x in q['conventions']]+['','### Question','',q['question'],'']
 reference_md+=['## '+slot+' — '+q['title'],'','### Reference solution','',q['reference_answer'],'','### Partial credit','']
 for item in q['rubric']:reference_md+=['- **'+str(item['weight'])+' points:** '+item['criterion']]
 reference_md+=['','Equivalent valid mathematical arguments receive the same substantive credit. Evidence status and formal identifiers are in the complete QA packet, outside the question.','','### Boundary cases','']
 reference_md+=['- '+display(x) for x in q['boundary_cases']]
 reference_md+=['','### Common errors','']+['- '+display(x) for x in q['common_errors']]
 reference_md+=['','### Author-supplied reasoning map','','These are declared mathematical inputs and scoped claims, not extracted Lean proof-term dependencies.','','#### Inputs','']
 for entry in q['reasoning_map']['inputs']:
  reference_md+=['- **'+entry['id']+'** ('+entry.get('kind','input')+'): '+entry['statement']]
 reference_md+=['','#### Steps','']
 for step in q['reasoning_map']['steps']:
  reference_md+=['- **'+step['id']+': '+step['claim']+'** Inputs: '+', '.join(step.get('required_inputs',[]))+'. '+('Additional/scoped assumptions: '+display(step['assumptions'])+'. ' if step.get('assumptions') else '')+('Scope: '+step['scope']+'. ' if step.get('scope') else '')+'Conclusion: '+step['conclusion']+' '+('Justification: '+step['justification'] if step.get('justification') else '')]
 reference_md+=['','#### Reuse and route scopes','']
 for key in ['AND_join_policy','reused_results','reconvergent_branches','alternative_routes','case_scopes']:
  if q['reasoning_map'].get(key):reference_md+=['- **'+key.replace('_',' ')+':** '+display(q['reasoning_map'][key])]
 reference_md+=['','### Evidence limitations','']+['- '+display(x) for x in q['unverified']]
 reference_md+=['','Full source roles, review bindings and provisional difficulty: [complete packet](qa/'+slot+'.json).','']
 rows.append({'slot':slot,'core_id':q['core_id'],'title':q['title'],'construction_band':band(q),'target':q['mathematical_target'],'target_nodes':q['target_nodes'],'supporting_nodes':q['supporting_nodes'],'overlap':q['overlap'],'review':rr,'proposal_path':relative(pp),'payload_path':relative(qp),'payload_sha256':sha(qp)})
for name,data in [('questions-only.jsonl',questions),('references-rubrics.jsonl',references)]:
 (P/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in data),encoding='utf-8')
(P/'QUESTIONS.md').write_text('\n'.join(question_md),encoding='utf-8')
(P/'REFERENCES.md').write_text('\n'.join(reference_md),encoding='utf-8')
write(P/'review-index.json',{'schema_version':'qcb.batch_review_index.v1','AI_reviews_not_human_approval':True,'items':review_index})
write(P/'coverage-overlap.json',{'schema_version':'qcb.batch_coverage_overlap.v1','base_commit':baseline['base_commit'],'prior_packets_recounted':0,'new_candidate_packets':6,'new_cores_admitted':0,'items':rows,'global_deduplication':'pending','sealed_assessment_comparison':'Only published seal/exposure/source metadata available; full private question comparison remains unresolved.'})
write(P/'source-index.json',{'schema_version':'qcb.batch_sources.v1','base_commit':baseline['base_commit'],'frozen_graph':baseline['graph'],'new_formal_execution':False,'source_files':list(source_files.values()),'graph_node_roles':list(node_roles.values()),'scope':'Exact source identities/bytes, with actor-specific mathematical reading recorded in authorship/review reports. No theorem-proof dependency extraction or source-paper-wide verification.'})
files=sorted([x for x in P.rglob('*') if x.is_file() and x.name!='manifest.json' and '__pycache__' not in x.parts]+proposals)
manifest={'schema_version':'qcb.nonlean_batch_manifest.v1','package_id':P.name,'base_commit':baseline['base_commit'],'base_tree':baseline['base_tree'],'branch':baseline['dedicated_branch'],'snapshot':baseline['graph'],'catalog_hash':baseline['registry']['catalog_hash'],'new_candidates':6,'existing_core_refinements_this_batch':0,'earlier_cohort_packets_preserved_not_recounted':12,'new_cores_admitted':0,'new_Lean_execution':False,'human_approval':False,'model_responses_collected':False,'contributions':rows,'pending_decisions':['Whole-target deduplication and shared assessed-subproof reconciliation','Split assignment and admission by maintainers','Comparison with unavailable owner-sealed assessment questions','Any new finite-bit supplier/compiler or formal certification is outside this batch'],'file_hash_policy':'SHA-256 of raw bytes. Manifest excludes itself; delivery SHA256SUMS binds the manifest. Source and baseline paths are pinned references, not copied repositories.','files':[{'path':relative(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in files]}
write(P/'manifest.json',manifest)
print(json.dumps({'candidate_packets':6,'existing_refinements':0,'admissions':0,'manifest_files':len(files),'reviews':[{'slot':x['slot'],'verdict':x['verdict']} for x in review_index]},indent=2))
