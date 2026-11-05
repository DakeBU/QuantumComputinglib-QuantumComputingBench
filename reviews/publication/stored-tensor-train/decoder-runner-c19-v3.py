"""Source-blind whole-source stdin elaboration; no target import or compiler outputs."""
from pathlib import Path
import hashlib, json, re, subprocess, sys, time

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PREFIX = 'decoder-c19'
TOOLCHAIN_PREFIXES = set()
TARGET = ROOT / 'QuantumBlockEncoding/StoredTensorTrain.lean'
PACKET = OUT / 'decoder-packet.json'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(cmd, **kw):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                          encoding='utf-8', errors='replace', **kw)

def without_comments(text):
    out, depth, i, string = [], 0, 0, False
    while i < len(text):
        if string:
            if text[i] == '\\': i += 2; continue
            if text[i] == '"': string = False
            if text[i] == '\n': out.append('\n')
            i += 1
            continue
        if not depth and text[i] == '"': string = True; i += 1; continue
        if text[i:i+2] == '/-': depth += 1; i += 2; continue
        if depth and text[i:i+2] == '-/': depth -= 1; i += 2; continue
        if not depth and text[i:i+2] == '--':
            end = text.find('\n', i)
            i = len(text) if end < 0 else end
            continue
        if not depth or text[i] == '\n': out.append(text[i])
        i += 1
    return ''.join(out)

def pins():
    # Resolve the recursive source import closure, pinning each source and cached
    # compiler artifact. No target olean is opened, hashed, or imported.
    search = [ROOT, ROOT / '.lake/packages/mathlib']
    search += sorted((ROOT / '.lake/packages').iterdir())
    prefix = run(['lake', 'env', 'lean', '--print-prefix']).stdout.strip().splitlines()[-1]
    TOOLCHAIN_PREFIXES.add(prefix)
    lib = Path(prefix) / 'lib/lean'
    sources = search + [Path(prefix) / 'src/lean']
    caches = [ROOT / '.lake/build/lib/lean'] + [p / '.lake/build/lib/lean' for p in search[1:]] + [lib]
    queue = ['Init', 'QuantumBlockEncoding.StoredThinLQ', 'QuantumBlockEncoding.ConstructiveTensorTrain']
    seen, records, provenance = set(), [], {}
    while queue:
        mod = queue.pop()
        if mod in seen: continue
        seen.add(mod)
        if mod == 'QuantumBlockEncoding.StoredTensorTrain':
            raise RuntimeError('Forbidden target cache import')
        rel = Path(*mod.split('.'))
        source = next((p / rel.with_suffix('.lean') for p in sources if (p / rel.with_suffix('.lean')).is_file()), None)
        cache = next((p / rel.with_suffix('.olean') for p in caches if (p / rel.with_suffix('.olean')).is_file()), None)
        if source is None or cache is None:
            raise RuntimeError(f'Unresolved source/cache: {mod}: {source} {cache}; imported at {provenance.get(mod)}')
        content = source.read_text(encoding='utf-8-sig')
        for line in without_comments(content).splitlines():
            hit = re.match(r'^\s*(?:(?:public|private|meta)\s+)?import\s+(.*)', line)
            if hit:
                for token in hit[1].split('--')[0].split():
                    if token != 'all' and re.fullmatch(r'[A-Za-z_][\w.]*', token):
                        queue.append(token)
                        provenance[token] = (str(source), line)
        artifacts = [cache] + [p for p in cache.parent.glob(cache.name + '.*') if p.is_file()]
        for suffix in ['.ilean', '.ir', '.trace']:
            p = cache.with_suffix(suffix)
            if p.is_file(): artifacts.append(p)
        records.append({'module': mod, 'source': str(source), 'source_sha256': digest(source),
                        'artifacts': [{'path': str(p), 'sha256': digest(p), 'bytes': p.stat().st_size}
                                      for p in sorted(set(artifacts))]})
    return sorted(records, key=lambda x: x['module'])

version = sys.argv[1]
probe = OUT / f'decoder-probe-c19-{version}.lean'
receipt_path = OUT / f'{PREFIX}-{version}-receipt.json'
if receipt_path.exists(): raise RuntimeError('Immutable receipt already exists')
started = time.time()
source_sha_before = digest(TARGET)
packet_sha_before = digest(PACKET)
assert source_sha_before == 'a9e5b0c2b00261d6f100a431fa95725c1bead82a4b87c41d54b59f0b084feae4'
assert packet_sha_before == 'b236f3265e3f1aa8bdb2ec83e018a02ae513149d7bf652c04e86a291a32e6b07'
context_names = ['lean-toolchain', 'lake-manifest.json', 'lakefile.lean']
context_before = [{'path': f, 'sha256': digest(ROOT / f)} for f in context_names]
before = pins()
source = TARGET.read_text(encoding='utf-8-sig')
names = re.findall(r'^(?:noncomputable\s+)?(?:abbrev|def|inductive|structure|theorem)\s+([\w.]+)', source, re.M)
assert len(names) == 30, names
checks = '\nset_option pp.all true\n'
for name in names:
    fq = 'QuantumBlockEncoding.StoredTensorTrain.' + name
    checks += f'\n#check {fq}\n#print axioms {fq}\n'
for name in ['StoredChain', 'CoreResult', 'Result']:
    checks += '\n#print QuantumBlockEncoding.StoredTensorTrain.' + name + '\n'
checks += '\n' + probe.read_text(encoding='utf-8-sig')
for op in ['field', 'sqrt', 'angle', 'trig', 'compare', 'read', 'write', 'emit']:
    checks += f'''\nexample {{l m r : ℕ}} (A : QuantumBlockEncoding.StoredTensorTrain.StoredCore l m)
    (R : QuantumBlockEncoding.StoredGivens.StoredMatrix m r) :
    (QuantumBlockEncoding.StoredTensorTrain.absorption A R).cost .{op} ≤
      QuantumBlockEncoding.StoredTensorTrain.absorptionBudget l m r .{op} :=
  QuantumBlockEncoding.StoredTensorTrain.absorption_cost_le A R .{op}
'''
payload = source + checks
result = run(['lake', 'env', 'lean', '--stdin', '--json'], input=payload, timeout=600)
after = pins()
receipt = {'schema_version': 1, 'role': 'decoder', 'identity': '/root/stored_tt_blind_decoder_c19',
           'run_id': f'stored-tt-blind-decoder-c19-{version}', 'source_blind': True,
           'binding_sha256': 'fd9ab0393ac26ae3707c90ac6333822ddfa19d96b73d1b1c97ab03a5764afe68',
           'packet_sha256': packet_sha_before, 'module_sha256_before': source_sha_before,
           'module_file_sha256_after': digest(TARGET), 'probe_sha256': digest(probe),
           'payload_sha256': hashlib.sha256(payload.encode()).hexdigest(), 'declarations': names,
           'command': ['lake', 'env', 'lean', '--stdin', '--json'], 'returncode': result.returncode,
           'stdout': result.stdout, 'stderr': result.stderr, 'elapsed_seconds': time.time() - started,
           'toolchain': run(['lake', 'env', 'lean', '--version']).stdout.strip(),
           'context_files': [{'path': f, 'sha256': digest(ROOT / f)} for f in context_names],
           'context_files_before': context_before,
           'packet_sha256_after': digest(PACKET),
           'runner_sha256': digest(Path(__file__)),
           'failure_class': 'NONE' if result.returncode == 0 else 'IMPLEMENTATION_FAILED',
           'provider_cache_provenance': 'Existing repository .lake build outputs, plus pinned package/toolchain libraries; imported providers were not freshly recompiled. Source and cache byte equality checked before/after, not a claim of fresh source-cache equivalence.',
           'provider_pins_before': before, 'provider_pins_after': after,
           'provider_pins_unchanged': before == after,
           'target_cache_used': False, 'production_cache_outputs_requested': False,
           'scope': 'Whole target source including its imports/private helpers plus independent consumers. No ROOT, main, site, full repository or provider-wide acceptance claim.'}
assert source_sha_before == receipt['module_file_sha256_after'], 'Target source changed during run'
assert packet_sha_before == receipt['packet_sha256_after'], 'Packet changed during run'
assert context_before == receipt['context_files'], 'Build context changed during run'

def scrub(value):
    if isinstance(value, dict): return {scrub(k): scrub(v) for k, v in value.items()}
    if isinstance(value, list): return [scrub(v) for v in value]
    if not isinstance(value, str): return value
    roots = [(str(ROOT), '<repository>')] + [(p, '<lean-toolchain>') for p in TOOLCHAIN_PREFIXES]
    for path, label in sorted(roots, key=lambda item: -len(item[0])):
        pattern = '[\\\\/]'.join(re.escape(part) for part in re.split(r'[\\/]', path))
        value = re.sub(pattern, lambda _: label, value, flags=re.I)
    return value

receipt = scrub(receipt)
receipt['privacy_path_notation'] = 'Repository and installed toolchain prefixes are replaced by <repository> and <lean-toolchain>; suffixes remain exact source/cache locators. SHA256 binds actual bytes at these resolved locations. This is path redaction, not source/cache replacement.'
receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'receipt': str(receipt_path.relative_to(ROOT)), 'sha256': digest(receipt_path),
                  'returncode': result.returncode, 'providers': len(before),
                  'unchanged': before == after, 'stdout': result.stdout[-16000:], 'stderr': result.stderr}, ensure_ascii=False))
