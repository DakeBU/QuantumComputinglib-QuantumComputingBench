"""Independent whole-source elaboration using a private pinned provider cache."""
from pathlib import Path
import hashlib, json, os, re, shutil, subprocess, sys, time

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
TARGET = ROOT / 'QuantumBlockEncoding/StoredTensorTrain.lean'
PARENT = OUT.parent
version = sys.argv[1]
receipt_path = OUT / f'receipt-{version}.json'
assert not receipt_path.exists(), 'Immutable receipt exists'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run(cmd, **kw):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                          encoding='utf-8', errors='replace', **kw)

prefix = Path(run(['lake', 'env', 'lean', '--print-prefix']).stdout.strip().splitlines()[-1])
packages = sorted(p for p in (ROOT / '.lake/packages').iterdir() if p.is_dir())
source_roots = [ROOT] + packages + [prefix / 'src/lean', prefix / 'src/lean/lake']
cache_roots = [ROOT / '.lake/build/lib/lean'] + [p / '.lake/build/lib/lean' for p in packages] + [prefix / 'lib/lean']
private = OUT / 'private-cache'
private.mkdir(exist_ok=True)
project_cache = private / 'project'
project_cache.mkdir(exist_ok=True)
original_artifacts = []
source_pins = []

def label(p):
    for base, tag in [(ROOT, '<repository>'), (prefix, '<lean-toolchain>')]:
        try: return tag + '/' + p.relative_to(base).as_posix()
        except ValueError: pass
    raise RuntimeError('Unclassified path')

def strip_comments(content):
    depth, i, out, string = 0, 0, [], False
    while i < len(content):
        if string:
            if content[i] == '\\': i += 2; continue
            if content[i] == '"': string = False
            if content[i] == '\n': out.append('\n')
            i += 1
            continue
        if not depth and content[i] == '"': string = True; i += 1; continue
        pair = content[i:i+2]
        if pair == '/-': depth += 1; i += 2; continue
        if pair == '-/' and depth: depth -= 1; i += 2; continue
        if pair == '--' and not depth:
            end = content.find('\n', i)
            i = len(content) if end < 0 else end
            continue
        if not depth or content[i] == '\n': out.append(content[i])
        i += 1
    return ''.join(out)

queue = ['Init', 'QuantumBlockEncoding.StoredThinLQ', 'QuantumBlockEncoding.ConstructiveTensorTrain']
seen, providers = set(), []
while queue:
    mod = queue.pop()
    if mod in seen: continue
    assert mod != 'QuantumBlockEncoding.StoredTensorTrain'
    seen.add(mod)
    rel = Path(*mod.split('.'))
    source = next((p / rel.with_suffix('.lean') for p in source_roots if (p / rel.with_suffix('.lean')).is_file()), None)
    cache = next((p / rel.with_suffix('.olean') for p in cache_roots if (p / rel.with_suffix('.olean')).is_file()), None)
    assert source and cache, f'Provider unresolved: {mod}'
    source_pins.append((source, sha(source)))
    for line in strip_comments(source.read_text(encoding='utf-8-sig')).splitlines():
        match = re.match(r'^\s*(?:(?:public|private|meta)\s+)*import\s+(.+)', line)
        if match:
            queue.extend(t for t in match[1].split() if t != 'all' and re.fullmatch(r'[A-Za-z_][\w.]*', t))
    artifacts = [cache] + sorted(p for p in cache.parent.glob(cache.name + '.*') if p.is_file())
    artifacts += [cache.with_suffix(s) for s in ['.ir', '.ilean'] if cache.with_suffix(s).is_file()]
    records = []
    for original in artifacts:
        toolchain_artifact = original.is_relative_to(prefix)
        dest = (private / 'toolchain-snapshot' if toolchain_artifact else project_cache) / rel.parent / original.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            try: os.link(original, dest)
            except OSError: shutil.copy2(original, dest)
        assert sha(original) == sha(dest), f'Private snapshot differs: {mod}'
        records.append({'path': label(original), 'private_path': dest.relative_to(OUT).as_posix(), 'sha256': sha(dest)})
        original_artifacts.append((original, sha(dest)))
    providers.append({'module': mod, 'source': label(source), 'source_sha256': sha(source), 'artifacts': records})
providers.sort(key=lambda p: p['module'])
inputs = ['QuantumBlockEncoding/StoredTensorTrain.lean', 'docs/lessons/stored-tensor-train-canonicalization.md',
          'lean-toolchain', 'lake-manifest.json', 'lakefile.lean',
          'reviews/publication/stored-tensor-train/decoder-packet.json',
          'reviews/publication/stored-tensor-train/source-review-c20/source-first-seal.json']
before = {p: sha(ROOT / p) for p in inputs}
assert before[inputs[0]] == 'a9e5b0c2b00261d6f100a431fa95725c1bead82a4b87c41d54b59f0b084feae4'
source = TARGET.read_text(encoding='utf-8-sig')
names = re.findall(r'^(?:noncomputable\s+)?(?:abbrev|def|inductive|structure|theorem)\s+([\w.]+)', source, re.M)
assert len(names) == 30
checks = '\nset_option pp.all true\n'
for name in names:
    checks += f'\n#check QuantumBlockEncoding.StoredTensorTrain.{name}\n#print axioms QuantumBlockEncoding.StoredTensorTrain.{name}\n'
checks += '\n' + (OUT / f'consumer-{version}.lean').read_text(encoding='utf-8-sig')
for op in ['field', 'sqrt', 'angle', 'trig', 'compare', 'read', 'write', 'emit']:
    checks += f'''\nexample {{l m r : ℕ}} (A : QuantumBlockEncoding.StoredTensorTrain.StoredCore l m)
    (R : QuantumBlockEncoding.StoredGivens.StoredMatrix m r) :
    (QuantumBlockEncoding.StoredTensorTrain.absorption A R).cost .{op} ≤
      QuantumBlockEncoding.StoredTensorTrain.absorptionBudget l m r .{op} :=
  QuantumBlockEncoding.StoredTensorTrain.absorption_cost_le A R .{op}
'''
payload = source + checks
env = os.environ.copy()
env['LEAN_PATH'] = str(project_cache)
native_roots = [prefix / 'bin', prefix / 'lib/lean'] + [p / '.lake/build/lib' for p in packages]
native_paths = sorted(set(p for base in native_roots if base.is_dir() for p in base.rglob('*.dll')))
native_before = [{'path':label(p),'sha256':sha(p)} for p in native_paths]
started = time.time()
normal_inherited_layout = version in ['v5', 'v6', 'v7']
cmd = ['lake','env','lean','--stdin','--json'] if normal_inherited_layout else [str(prefix / 'bin/lean.exe'),'--stdin','--json']
result = run(cmd, input=payload, timeout=500, **({} if normal_inherited_layout else {'env':env}))

def scrub(s):
    for base, tag in [(str(private), '<private-cache>'), (str(ROOT), '<repository>'), (str(prefix), '<lean-toolchain>')]:
        pattern = '[\\\\/]'.join(re.escape(t) for t in re.split(r'[\\/]', base))
        s = re.sub(pattern, lambda _: tag, s, flags=re.I)
    return s

messages = [json.loads(line) for line in result.stdout.splitlines() if line.startswith('{')]
public_stdout = '\n'.join(json.dumps({k: scrub(v) if isinstance(v, str) else v for k, v in m.items()},ensure_ascii=False) for m in messages)
decls = []
for name in names:
    fq = 'QuantumBlockEncoding.StoredTensorTrain.' + name
    signatures = [m['data'] for m in messages if re.match(re.escape(fq) + r'(?=\s|:|$)', m.get('data', ''))]
    axioms = [m['data'] for m in messages if m.get('data', '').startswith("'" + fq + "'")]
    decls.append({'name': fq, 'signature': signatures, 'axioms': axioms})
after = {p: sha(ROOT / p) for p in inputs}
cache_unchanged = all(sha(OUT / a['private_path']) == a['sha256'] for p in providers for a in p['artifacts'])
original_cache_unchanged = all(sha(p)==digest for p,digest in original_artifacts)
provider_sources_unchanged = all(sha(p)==digest for p,digest in source_pins)
native_after = [{'path':label(p),'sha256':sha(p)} for p in native_paths]
receipt = {'schema_version':1, 'role':'reviewer', 'identity':'/root/stored_tt_source_review_c20',
    'run_id':'stored-tt-source-review-c20-' + version, 'returncode':result.returncode,
    'elapsed_seconds':time.time()-started, 'stdout':public_stdout, 'stderr':scrub(result.stderr),
    'toolchain':run([str(prefix / 'bin/lean.exe'), '--version']).stdout.strip(),
    'whole_target_source':True, 'target_cache_imported':False, 'production_outputs_requested':False,
    'command':['lake','env','lean','--stdin','--json'] if normal_inherited_layout else ['<lean-toolchain>/bin/lean.exe','--stdin','--json'],
    'lean_path':'Normal inherited lake-env provider/native layout' if normal_inherited_layout else ['<private-cache>/project'], 'input_sha256_before':before,'input_sha256_after':after,
    'inputs_unchanged':before==after, 'private_cache_unchanged':cache_unchanged,
    'original_provider_artifacts_unchanged':original_cache_unchanged,
    'provider_sources_unchanged':provider_sources_unchanged,
    'native_pins_before':native_before,'native_pins_after':native_after,'native_pins_unchanged':native_before==native_after,
    'cache_provenance':'v5 uses normal inherited lake-env source/cache/native layout, pinned before/after and additionally privately snapshotted; no boot/package shadowing or transitive rebuild. Earlier v1-v4 private layouts failed before target elaboration and remain unchanged. No provider freshness or source-cache semantic correspondence claimed. No target olean imported.' if normal_inherited_layout else 'Private hardlink-or-copy project/package provider cache; installed core normally resolved and privately snapshotted/pinned. No provider freshness or source-cache semantic correspondence claimed.',
    'provider_count':len(providers), 'providers':providers, 'declarations':decls,
    'consumer_sha256':sha(OUT / f'consumer-{version}.lean'), 'runner_sha256':sha(Path(__file__)),
    'payload_sha256':hashlib.sha256(payload.encode()).hexdigest(),
    'failure_class':'NONE' if result.returncode == 0 else 'IMPLEMENTATION_FAILED'}
receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'receipt':receipt_path.relative_to(ROOT).as_posix(),'sha256':sha(receipt_path),
    'returncode':result.returncode,'provider_count':len(providers),'inputs_unchanged':before==after,
    'private_cache_unchanged':cache_unchanged,'signature_counts':[len(d['signature']) for d in decls],
    'axiom_counts':[len(d['axioms']) for d in decls],
    'errors':[m for m in messages if m.get('severity')=='error']},ensure_ascii=False))
