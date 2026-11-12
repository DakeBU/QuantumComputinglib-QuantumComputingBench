"""Preserve execution receipt bytes; emit an explicitly bound PUBLIC derivative."""
from pathlib import Path
import hashlib, json

OUT=Path(__file__).resolve().parent
raw=OUT/'decoder-c19-v3-receipt.json'
public=OUT/'decoder-c19-v3-public-receipt.json'
if public.exists(): raise RuntimeError('Immutable public derivative already exists')
original=raw.read_bytes()
raw_sha=hashlib.sha256(original).hexdigest()
receipt=json.loads(original)
assert receipt['returncode']==0 and receipt['provider_pins_unchanged']
receipt['public_derivative']={
    'version':'c19-v3-public',
    'raw_receipt':'reviews/publication/stored-tensor-train/decoder-c19-v3-receipt.json',
    'raw_receipt_sha256':raw_sha,
    'original_execution_receipt_preserved_private':True,
    'new_lean_execution':False,
    'run_scope_unchanged':True,
    'mathematical_messages_unchanged':True,
    'source_and_cache_hashes_unchanged':True,
    'path_policy':'The original execution receipt already records symbolic repository/toolchain prefixes with exact suffix locators. This PUBLIC derivative preserves that redaction and all mathematical messages and pins; it adds explicit original-receipt provenance only.'}
public.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert raw.read_bytes()==original
print(json.dumps({'public_receipt':public.name,'public_receipt_sha256':hashlib.sha256(public.read_bytes()).hexdigest(),
                  'raw_receipt_sha256':raw_sha,'raw_byte_identical':True}))
