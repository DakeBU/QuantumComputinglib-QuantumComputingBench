"""Fail closed for exact compatibility maintenance, NEVER source assimilation.

This validates evidence bindings, not natural-language truth or human honesty.
Official CI and complete publication/reader gates still govern main integration.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
from pathlib import Path, PurePosixPath, PureWindowsPath

APPROVED_CASE = {
    'module': 'QuantumBlockEncoding/RobinMatrix.lean',
    'base_commit': 'af585d9cbbb299c1c8c48647627a2cb820ef536a',
    'old_source_sha256': 'e957b6a5961ad2c22cfd154f17cbbec3e7668027b2f526d9f762798eb1c50038',
    'new_source_sha256': '1cca5119ac056fe041b25c529909b9fb6c3e4995e04ebde2f69e83fce47a0835',
    'old_toolchain': 'leanprover/lean4:v4.29.1',
    'new_toolchain': 'leanprover/lean4:v4.33.0',
    'old_manifest_sha256': '3f85247e74f75c3030bf538085e098d3f721b2837d21d22da0bdc96efcc0a466',
    'new_manifest_sha256': '510171e8214a2ac5e00f16c1bf92ad474d2de42c4cd2dc2b3d411272f7b58763',
    'diff_sha256': '9418ed5a4e1754b042d03084cab78ac171794cd35f71ed469ea94f0933df4bd2',
}
SCIENTIFIC_KEYS = {'source_assimilated', 'BE_root_closed', 'PDE_formalized',
                   'physical_operator_verified', 'resource_theorem_verified', 'PURIFIED'}
ROLES = {'whole-module-decoder', 'whole-module-review', 'raw-association',
         'compiled-runtime', 'compatibility-review', 'policy-review'}
ORIGINAL_INPUT_MANIFEST_SHA256 = '1e9753617607d960798a6161dcb5b3f0d338524fae3885d1a22d6200b8b7dbf5'
sha = lambda raw: hashlib.sha256(raw).hexdigest()

def local_file(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not name:
        raise ValueError('maintenance evidence path is missing')
    p = PurePosixPath(name)
    if p.is_absolute() or PureWindowsPath(name).drive or '..' in p.parts or '\\' in name or ':' in name:
        raise ValueError('non-portable maintenance evidence path')
    out = root / p
    if not out.resolve().is_relative_to(root.resolve()) or not out.is_file():
        raise ValueError('missing maintenance evidence file: ' + name)
    return out

def git_bytes(root: Path, *args: str) -> bytes:
    result = subprocess.run(['git', *args], cwd=root, capture_output=True)
    if result.returncode:
        raise ValueError('cannot verify exact maintenance Git baseline')
    return result.stdout

def proof_context(root: Path) -> dict[str, str]:
    names = {'QuantumBlockEncoding.lean', 'Tests.lean', 'lean-toolchain', 'lakefile.lean', 'lake-manifest.json'}
    for directory in ('QuantumBlockEncoding', 'ABEISTests'):
        folder = root / directory
        if not folder.is_dir():
            raise ValueError('missing complete maintenance source directory')
        names.update(p.relative_to(root).as_posix() for p in folder.rglob('*.lean'))
    return {n: sha(local_file(root, n).read_bytes()) for n in sorted(names)}

def binding_digest(root: Path, record: dict) -> str:
    keys = ('schema', 'kind', 'case', 'scope', 'declarations', 'coverage', 'maintainer',
            'historical_formalizer', 'scientific_claims', 'remaining_BE_obligations',
            'proof_context', 'lesson_path', 'diff_path')
    payload = {k: record.get(k) for k in keys}
    # Evidence receipt contents contain this digest, so bind their roles/paths
    # here and verify their actual bytes separately; no recursive digest claim.
    # Bind ALL receipt semantics before any wrapper is emitted. Only the
    # receipt's own root-binding and resulting file hash are excluded to avoid
    # recursion. A single actor cannot refresh identity, old seal, runtime
    # flags, result or provenance while leaving other reviews apparently fresh.
    payload['evidence_paths'] = {r: {k: e.get(k) for k in ('path', 'artifact_path', 'artifact_sha256', 'expected_fields')}
                                 for r, e in record.get('evidence', {}).items()}
    h = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode())
    for name in (record['lesson_path'], record['diff_path'],
                 'website/scripts/check_research_publications.py',
                 'website/scripts/check_toolchain_maintenance.py',
                 'docs/theorem-publication-protocol.md'):
        h.update(name.encode()); h.update(local_file(root, name).read_bytes())
    return h.hexdigest()

def validate_record(root: Path, record: dict, inventory: dict) -> None:
    if record.get('schema') != 1 or record.get('kind') != 'exact-toolchain-maintenance':
        raise ValueError('unknown maintenance record kind')
    case = record.get('case')
    if case != APPROVED_CASE:
        raise ValueError('not the independently approved exact maintenance case')
    if record.get('scope') != 'BE-only compatibility; no scientific promotion':
        raise ValueError('maintenance scientific scope changed')
    claims = record.get('scientific_claims', {})
    if set(claims) != SCIENTIFIC_KEYS or any(v is not False for v in claims.values()):
        raise ValueError('maintenance cannot claim scientific or publication success')
    if not record.get('maintainer') or record.get('historical_formalizer') != 'UNKNOWN':
        raise ValueError('maintainer or historical authorship disclosure missing')
    if not record.get('remaining_BE_obligations'):
        raise ValueError('remaining BE obligations must stay explicit')
    module = case['module']; base = case['base_commit']
    if sha(local_file(root, module).read_bytes()) != case['new_source_sha256']:
        raise ValueError('maintenance source changed')
    if sha(git_bytes(root, 'show', base + ':' + module)) != case['old_source_sha256']:
        raise ValueError('maintenance baseline source changed')
    if git_bytes(root, 'show', base + ':lean-toolchain').decode().strip() != case['old_toolchain']:
        raise ValueError('maintenance old toolchain changed')
    if local_file(root, 'lean-toolchain').read_text().strip() != case['new_toolchain']:
        raise ValueError('maintenance new toolchain changed')
    if sha(git_bytes(root, 'show', base + ':lake-manifest.json')) != case['old_manifest_sha256']:
        raise ValueError('maintenance old dependency context changed')
    if sha(local_file(root, 'lake-manifest.json').read_bytes()) != case['new_manifest_sha256']:
        raise ValueError('maintenance new dependency context changed')
    # Object-store-dependent default abbreviation is not a portable byte format.
    diff = git_bytes(root, 'diff', '--no-ext-diff', '--no-renames', '--abbrev=8', base, '--', module)
    if sha(diff) != case['diff_sha256'] or local_file(root, record['diff_path']).read_bytes() != diff:
        raise ValueError('maintenance compatibility diff changed')
    actual = {n for n, row in inventory.items() if row.get('source') == module}
    declared = record.get('declarations', [])
    if len(actual) != 395 or len(declared) != len(set(declared)) or set(declared) != actual:
        raise ValueError('maintenance must bind the exact whole public inventory')
    if any(inventory[n].get('experimental') is not True or inventory[n].get('openProof') for n in actual):
        raise ValueError('maintenance must preserve experimental flags and reject proof holes')
    if record.get('coverage') != {'raw_declarations': 677, 'structure_fields': 1950, 'public_exports': 395}:
        raise ValueError('maintenance whole-module coverage changed')
    current = proof_context(root)
    if record.get('proof_context') != current:
        raise ValueError('maintenance full source/config context is stale or incomplete')
    expected = binding_digest(root, record)
    if record.get('binding_sha256') != expected:
        raise ValueError('stale maintenance binding')
    evidence = record.get('evidence', {})
    if set(evidence) != ROLES:
        raise ValueError('maintenance requires complete independent and runtime evidence')
    identities = {}
    for role, ref in evidence.items():
        raw = local_file(root, ref['path']).read_bytes()
        if sha(raw) != ref.get('sha256'):
            raise ValueError('maintenance evidence bytes changed')
        e = json.loads(raw)
        stable_fields = {k: v for k, v in e.items() if k != 'binding_sha256'}
        # Python dict equality conflates JSON true/1 and 1/1.0. Compare
        # canonical JSON instead, including nested types; nonfinite JSON values
        # are rejected, not treated as another valid metadata representation.
        canonical = lambda value: json.dumps(value, sort_keys=True, ensure_ascii=False,
                                             separators=(',', ':'), allow_nan=False)
        if canonical(ref.get('expected_fields')) != canonical(stable_fields):
            raise ValueError('maintenance receipt semantics differ from the independently reviewed binding')
        if e.get('role') != role or not e.get('identity') or not e.get('run_id'):
            raise ValueError('maintenance evidence role/identity/run missing')
        if e.get('binding_sha256') != expected or e.get('purpose') != 'compatibility-only':
            raise ValueError('maintenance evidence scope/context mismatch')
        artifact = local_file(root, e.get('artifact_path', ''))
        if sha(artifact.read_bytes()) != e.get('artifact_sha256'):
            raise ValueError('maintenance actual artifact missing or changed')
        if any(e.get(k) != ref.get(k) for k in ('artifact_path', 'artifact_sha256')):
            raise ValueError('maintenance result artifact differs from the reviewed binding')
        identities[role] = e['identity']
        if role in {'whole-module-decoder', 'whole-module-review', 'raw-association'}:
            # This is a NEW mechanical association to OLD immutable work,
            # not a retroactively fabricated human verdict under a new policy.
            if e.get('receipt_kind') != 'exact-input-reuse' or e.get('new_review_performed') is not False:
                raise ValueError('historical review must be explicitly reused, not relabelled as a new review')
            if e.get('original_raw_module_sha256') != case['new_source_sha256']:
                raise ValueError('historical review cannot silently acquire changed source inputs')
            original_inputs = local_file(root, e.get('original_input_manifest_path', '')).read_bytes()
            if sha(original_inputs) != ORIGINAL_INPUT_MANIFEST_SHA256:
                raise ValueError('historical exact eleven-input formal manifest changed')
            # The old decoder read eleven scoped inputs, NOT the entire current
            # library. Preserve that boundary; full-library equality/build is
            # checked independently by proof_context and compiled-runtime.
            old_inputs = json.loads(original_inputs)['inputs']
            if len(old_inputs) != 11 or any(sha(local_file(root, i['path']).read_bytes()) != i['production_raw_sha256']
                                           for i in old_inputs):
                raise ValueError('historically reviewed input bytes no longer match')
            original_seal = local_file(root, e.get('original_seal_path', ''))
            if sha(original_seal.read_bytes()) != e.get('original_seal_sha256') or e.get('original_scope_preserved') is not True:
                raise ValueError('historical seal/scope association missing or changed')
        if role in {'compatibility-review', 'policy-review'}:
            if e.get('verdict') != 'accepted-for-compatibility-only' or e.get('anti_anchored') is not True:
                raise ValueError('maintenance needs actual accepted independent review')
        if role == 'whole-module-decoder' and e.get('source_blind') is not True:
            raise ValueError('maintenance whole-module decoder must remain source-blind')
        if role == 'compiled-runtime':
            if e.get('proof_context') != current or e.get('full_library_and_Tests') is not True or e.get('trust_gate') is not True:
                raise ValueError('maintenance requires source-bound actual full Lean/Tests/trust evidence')
            if not e.get('workflow_run_id') or not e.get('job_id') or not e.get('native_trust_disclosure'):
                raise ValueError('maintenance runtime provenance/native disclosure missing')
    separate = [record['maintainer'], identities['whole-module-decoder'], identities['whole-module-review'],
                identities['compatibility-review']]
    if len(set(separate)) != len(separate):
        raise ValueError('maintenance author, decoder and independent reviewers must differ')
    if identities['policy-review'] in separate[:3]:
        raise ValueError('maintenance policy reviewer cannot be the author or reused whole-module roles')

def partition_records(registry: dict) -> tuple[dict, dict]:
    ordinary = registry['records']
    maintenance = registry.get('maintenance_records', [])
    if not isinstance(ordinary, list) or not isinstance(maintenance, list):
        raise ValueError('publication record collections must be lists')
    by_module = {item['module']: item for item in ordinary}
    by_maintenance = {item['case']['module']: item for item in maintenance}
    if len(by_module) != len(ordinary) or len(by_maintenance) != len(maintenance):
        raise ValueError('duplicate publication or maintenance module')
    if by_module.keys() & by_maintenance.keys():
        raise ValueError('a module cannot mix source-assimilation and maintenance lanes')
    return by_module, by_maintenance
