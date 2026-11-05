"""Fresh consumer replay for the frozen uniform mask/translation supplier.

Does not overwrite worker caches or imply a complete piecewise producer/ROOT.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'experiments/hermite-polynomial/precision/'
PACKET = PREFIX + 'piecewise-kernel-uniform-c20/'
SELF = PREFIX + 'cycle20-uniform-parent-checkpoint.py'
OUTPUT = PREFIX + 'cycle20-uniform-parent-checkpoint.json'
FORBIDDEN_PATH = re.compile(r'(?<![A-Za-z0-9_])[A-Za-z]:[\\/]')


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def scan(value):
    if isinstance(value, str):
        if FORBIDDEN_PATH.search(value) or re.search(r'github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]+', value):
            raise ValueError('Public path/credential policy violation')
    elif isinstance(value, dict):
        for key, item in value.items():
            scan(key)
            scan(item)
    elif isinstance(value, list):
        for item in value:
            scan(item)


def main():
    logs = [PREFIX + 'cycle20-uniform-parent-checkpoint-' + str(i) + '.log' for i in range(4)]
    if any((ROOT / p).exists() for p in [OUTPUT] + logs):
        raise SystemExit('Immutable checkpoint already exists')
    manifest_path = PACKET + 'final-binding-manifest.json'
    assert sha(manifest_path) == '5cfd9c3f36bc56e0d888947988da341c7ee2747187b00e61a776b642e20dd0a9'
    manifest = json.loads((ROOT / manifest_path).read_text(encoding='utf-8-sig'))
    pins = {manifest_path: sha(manifest_path), SELF: sha(SELF)}
    for key in ['artifact_hashes', 'ignored_cache_hashes']:
        pins.update({PACKET + p: h for p, h in manifest[key].items()})
    pins.update(manifest['proof_source_inherited_bindings'])
    for path, expected in pins.items():
        if Path(path).is_absolute() or ':' in path or '..' in Path(path).parts:
            raise ValueError('Nonrelative binding')
        if sha(path) != expected:
            raise ValueError('Frozen binding changed: ' + path)
    # Public derivatives only; raw logs and own caches remain private.
    for path in [PACKET + p for p in manifest['artifact_hashes']] + [manifest_path, SELF]:
        text = (ROOT / path).read_text(encoding='utf-8-sig')
        scan(json.loads(text) if path.endswith('.json') else text)
    files = [('UniformComparison.lean', 9), ('UniformTranslation.lean', 3),
             ('UniformThresholds.lean', 4), ('ConsumerChecks.lean', 5)]
    rows, unexpected = [], []
    for i, (filename, expected_roots) in enumerate(files):
        command = ['lake', 'env', 'lean', PACKET + filename]
        env = os.environ.copy()
        env['LEAN_PATH'] = str(ROOT / PACKET / '.cache')
        start = time.perf_counter()
        run = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        text = run.stdout.replace(str(ROOT), '<repo>').replace(ROOT.as_posix(), '<repo>')
        text = re.sub(r'(?<![A-Za-z0-9_])[A-Za-z]:[\\/][^\r\n\'"<>]*', '<private-path>', text)
        scan(text)
        (ROOT / logs[i]).write_text(text, encoding='utf-8')
        hits = list(re.finditer(r'depends on axioms: \[(.*?)\]', text, re.S))
        reports = len(hits) + len(re.findall(r'does not depend on any axioms', text))
        for hit in hits:
            names = [re.sub(r'\.\{[^}]*\}$', '', a.strip()) for a in hit[1].split(',')]
            unexpected.extend(a for a in names if a and a not in {'propext', 'Classical.choice', 'Quot.sound'})
        rows.append({'command': command, 'exit_code': run.returncode,
                     'seconds': time.perf_counter() - start, 'axiom_reports': reports,
                     'expected_axiom_reports': expected_roots, 'log': logs[i],
                     'log_sha256': sha(logs[i]),
                     'passed': run.returncode == 0 and reports == expected_roots})
        print(json.dumps(rows[-1]), flush=True)
        if not rows[-1]['passed']:
            break
    unchanged = all(sha(p) == h for p, h in pins.items())
    passed = len(rows) == 4 and all(r['passed'] for r in rows) and unchanged and not unexpected
    result = {
        'task': 'SP-HERMITE-POLY-002', 'passed': passed,
        'bindings_sha256': pins, 'inputs_and_private_caches_unchanged': unchanged,
        'execution': rows, 'axiom_reports': sum(r['axiom_reports'] for r in rows),
        'unexpected_axioms': sorted(set(unexpected)), 'public_path_scan_passed': True,
        'same_returned_comparator': 'Arbitrary-width q0LSB3-state stored chain, actual rational-grid strict/inclusive masks, D<=3 and storedScalars<=18*width',
        'cost_tier': 'Charged exact-real/word operations <=5*n^2+149*n+479 plus18*width quotient and remainder calls separately; not finite-bit runtime',
        'polynomial_interface': 'Generic rational binomial contraction, actual Hermite middle/Taylor coefficients not yet instantiated',
        'cache_provenance': 'Pinned worker-private fresh selected-source outputs, inherited transitive production/Mathlib caches; not clean repository CI',
        'distinct_review': 'PENDING', 'scientific_ROOT': False, 'main_admission': False,
        'resource_winner': False, 'public_PURIFIED': False,
        'remaining': ['actual source coefficient generation and equality',
                      'mask-product and five-way directsum contraction',
                      'same returned full piecewise stored producer and total generation cost',
                      'finite-bit arithmetic/QR/normalization/synthesis/global support',
                      'independent scientific-family executable acceptance',
                      'publication/integration/reader gates and main Lean4.33 migration']}
    (ROOT / OUTPUT).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': passed, 'receipt': OUTPUT, 'sha256': sha(OUTPUT)}), flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
