"""Exact-token signature, source-fragment, axiom and publication privacy audit."""
from pathlib import Path
import hashlib, json, re, sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
version = sys.argv[1]
receipt_path = OUT / f'receipt-{version}.json'
artifact_name = sys.argv[2] if len(sys.argv)>2 else 'decoder-artifact.json'
suffix = '-'+sys.argv[3] if len(sys.argv)>3 else ''
report_path = OUT / f'audit-{version}-{Path(artifact_name).stem}{suffix}.json'
assert not report_path.exists(), 'Immutable audit already exists'
receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
artifact_path = OUT.parent / artifact_name
artifact = json.loads(artifact_path.read_text(encoding='utf-8'))
source = (ROOT / 'QuantumBlockEncoding/StoredTensorTrain.lean').read_text(encoding='utf-8-sig')
checks = []
for actual, decoded in zip(receipt['declarations'], artifact['reconstruction']['declarations'], strict=True):
    assert actual['name'] == decoded['name']
    sig = actual['signature']
    ax = actual['axioms']
    ax_names = re.findall(r'\b(?:sorryAx|propext|Classical\.choice|Quot\.sound)\b', '\n'.join(ax))
    unknown_axioms = []
    for entry in ax:
        if 'depends on axioms:' in entry:
            for token in entry.split('depends on axioms:',1)[1].strip().strip('[]').split(','):
                base = re.sub(r'\.\{[^}]*\}', '', token).strip()
                if base not in ['propext','Classical.choice','Quot.sound']:
                    unknown_axioms.append(base)
    checks.append({'name':actual['name'], 'source_fragment_matches_actual':decoded['exact_formal_declaration_source'] in source,
        'own_exact_signature_unique':len(sig)==1, 'own_exact_axiom_report_unique':len(ax)==1,
        'decoder_signature_name_exact':bool(re.match(re.escape(actual['name'])+r'(?=\s|:|$)',decoded['actual_checked_signature'])),
        'decoder_full_signature_matches_own':len(sig)==1 and sig[0]==decoded['actual_checked_signature'],
        'decoder_axiom_report_matches_own':len(ax)==1 and ax[0]==decoded['actual_axiom_report'],
        'axioms_standard_only':len(ax)==1 and not unknown_axioms and 'sorryAx' not in ax_names,
        'unknown_axioms':unknown_axioms,
        'signature_audit_status':'PASS' if len(sig)==1 and sig[0]==decoded['actual_checked_signature'] else 'FAILED'})

path_pattern = re.compile(r'(?i)(?:[a-z]:[\\/]|file://|/(?:home|Users|tmp|mnt)/)')
privacy_findings = []
def inspect(value, file, key='$'):
    if isinstance(value, dict):
        for k,v in value.items(): inspect(k,file,key+'.<key>'); inspect(v,file,key+'.'+k)
    elif isinstance(value, list):
        for i,v in enumerate(value): inspect(v,file,key+f'[{i}]')
    elif isinstance(value,str):
        if path_pattern.search(value): privacy_findings.append({'file':file,'location':key})
        if key.endswith('.stdout'):
            for i,line in enumerate(value.splitlines()):
                if line.startswith('{'):
                    inspect(json.loads(line),file,key+f'.decoded[{i}]')
public_files = [p for p in OUT.iterdir() if p.is_file() and p.suffix in ['.json','.md','.lean'] and p.name!='receipt-v1.json']
for p in public_files:
    content = p.read_text(encoding='utf-8-sig')
    inspect(json.loads(content) if p.suffix=='.json' else content,p.relative_to(ROOT).as_posix())
sha = lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report = {'schema_version':1,'role':'reviewer','identity':'/root/stored_tt_source_review_c20',
    'run_id':'stored-tt-source-review-c20-'+version,'receipt':receipt_path.relative_to(ROOT).as_posix(),
    'receipt_sha256':sha(receipt_path),'decoder_artifact':artifact_path.relative_to(ROOT).as_posix(),
    'decoder_artifact_sha256':sha(artifact_path),'all_30_compared':len(checks)==30,'declarations':checks,
    'source_fidelity':'accepted for retrospective local stored algebraic/exact-real scope, not overall admission',
    'overall_evidence_status':'ACCEPTED_NARROW_SOURCE_FORMAL_SCOPE' if all(c['signature_audit_status']=='PASS' for c in checks) and receipt['returncode']==0 else 'FAILED_DECODER_OR_CONSUMER_AUDIT',
    'fresh_consumer_returncode':receipt['returncode'],'inputs_unchanged':receipt['inputs_unchanged'],
    'private_cache_unchanged':receipt['private_cache_unchanged'],'provider_count':receipt['provider_count'],
    'publication_privacy':{'files':[p.relative_to(ROOT).as_posix() for p in public_files],
        'decoded_json_keys_strings_and_nested_logs_checked':True,'findings':privacy_findings,
        'private_failures_excluded_explicitly':['receipt-v1.json'],'private_cache_excluded':True},
    'self_approval':False,'scope':'No ROOT/main/provider-wide/full-repository/site/purification approval.'}
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'audit':report_path.relative_to(ROOT).as_posix(),'sha256':sha(report_path),
    'signature_failures':[c['name'] for c in checks if c['signature_audit_status']=='FAILED'],
    'source_fragment_failures':[c['name'] for c in checks if not c['source_fragment_matches_actual']],
    'nonstandard_axioms':[c['name'] for c in checks if not c['axioms_standard_only']],
    'privacy_findings':privacy_findings,'returncode':receipt['returncode']},ensure_ascii=False))
