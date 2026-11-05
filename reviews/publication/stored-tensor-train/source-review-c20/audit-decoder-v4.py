"""Independently validate the decoder successor against actual prior execution messages."""
from pathlib import Path
import hashlib, json, re
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
PARENT = OUT.parent
dest = OUT / 'decoder-successor-audit-v1.json'
assert not dest.exists()
artifact_path = PARENT / 'decoder-artifact-c19-v4.json'
receipt_path = PARENT / 'decoder-c19-v3-public-receipt.json'
artifact = json.loads(artifact_path.read_text(encoding='utf-8'))
receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
messages = [json.loads(s) for s in receipt['stdout'].splitlines() if s.startswith('{')]
source = (ROOT / 'QuantumBlockEncoding/StoredTensorTrain.lean').read_text(encoding='utf-8-sig')
old = json.loads((PARENT / 'decoder-artifact.json').read_text(encoding='utf-8'))
checks=[]
for item,previous in zip(artifact['reconstruction']['declarations'],old['reconstruction']['declarations'],strict=True):
    name=item['name']
    sigs=[m['data'] for m in messages if re.match(re.escape(name)+r'(?:\.\{[^}]*\})?(?=\s|:|$)',m.get('data',''))]
    axioms=[m['data'] for m in messages if m.get('data','').startswith("'"+name+"'")]
    unknown=[]
    for ax in axioms:
        if 'depends on axioms:' in ax:
            for token in ax.split('depends on axioms:',1)[1].strip().strip('[]').split(','):
                base=re.sub(r'\.\{[^}]*\}','',token).strip()
                if base not in ['propext','Classical.choice','Quot.sound']: unknown.append(base)
    checks.append({'name':name,'actual_receipt_exact_signature_unique':len(sigs)==1,
        'successor_signature_exact_match':sigs==[item['actual_checked_signature']],
        'successor_axioms_exact_match':axioms==[item['actual_axiom_report']],
        'source_fragment_matches_actual':item['exact_formal_declaration_source'] in source,
        'axioms_standard_only':len(axioms)==1 and not unknown,'unknown_axioms':unknown,
        'historical_signature_failure':previous['actual_checked_signature'] != item['actual_checked_signature'],
        'source_first_comparison':'Correspondence accepted in the mathematical group coverage of source-comparison.md'})
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
result={'schema_version':1,'role':'reviewer','identity':'/root/stored_tt_source_review_c20',
    'run_id':'stored-tt-source-review-c20-decoder-successor-audit-v1',
    'artifact':artifact_path.relative_to(ROOT).as_posix(),'artifact_sha256':sha(artifact_path),
    'receipt':receipt_path.relative_to(ROOT).as_posix(),'receipt_sha256':sha(receipt_path),
    'execution_provenance':'These are actual decoder v3 execution messages, independently selected with exact name-token boundaries. This audit is not a new Lean execution.',
    'all_30_compared':len(checks)==30,'checks':checks,
    'decoder_successor_signature_and_axiom_correction_accepted':all(c['successor_signature_exact_match'] and c['successor_axioms_exact_match'] and c['source_fragment_matches_actual'] and c['axioms_standard_only'] for c in checks),
    'historical_failure_preserved':'Original absorption signature collision remains FAILED in the immutable old artifact; successor corrects only that field and partial inherited-closure provenance.',
    'source_fidelity':'accepted only for retrospective local real stored-tensor-train algebraic and eight-counter exact-real contract',
    'own_fresh_consumer_gate':'ENV_BLOCKED: private native-library loading; no independent fresh target signatures/axioms obtained in v1-v4',
    'overall_publication_admission':False,'self_approval':False,
    'provider_boundary':'Decoder pins partial inherited closure; reviewer privately expanded combined import closure to4901 and preserved unresolved native-library loading boundary. Neither source-cache semantic equality nor provider-wide compilation is certified.'}
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'path':dest.relative_to(ROOT).as_posix(),'sha256':sha(dest),
    'accepted_correction':result['decoder_successor_signature_and_axiom_correction_accepted'],
    'historical_failures':[c['name'] for c in checks if c['historical_signature_failure']],
    'source_fragment_failures':[c['name'] for c in checks if not c['source_fragment_matches_actual']]},ensure_ascii=False))
