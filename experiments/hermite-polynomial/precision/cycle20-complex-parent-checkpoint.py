"""Read-only actual complex-stage consumer and finite-discriminator replay."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'experiments/hermite-polynomial/precision/'
PACKET = PREFIX + 'complex-stage-transport-c20/'
SELF = PREFIX + 'cycle20-complex-parent-checkpoint.py'
OUTPUT = PREFIX + 'cycle20-complex-parent-checkpoint.json'
PATH = re.compile(r'(?<![A-Za-z0-9_])[A-Za-z]:[\\/]')


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def scan(value):
    if isinstance(value, dict):
        for k, v in value.items():
            scan(k)
            scan(v)
    elif isinstance(value, list):
        for v in value:
            scan(v)
    elif isinstance(value, str):
        if PATH.search(value) or re.search(r'github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]+', value):
            raise ValueError('Public path/credential policy violation')


def main():
    logs = [PREFIX + 'cycle20-complex-parent-checkpoint-' + str(i) + '.log' for i in range(3)]
    if any((ROOT / p).exists() for p in [OUTPUT] + logs):
        raise SystemExit('Immutable checkpoint already exists')
    refs = {
        SELF: sha(SELF),
        PACKET + 'result-v1.json': '964aa2cce737273aa6e4b2d2f15f9721bcef066aecafe35b564bada7c6d8f9fe',
        PACKET + 'handoff-v1.json': 'faa255364e402730ec86978cabb7ba346fdbf45c0fd9e9c38d5f0237a24369d0'}
    result = read(PACKET + 'result-v1.json')
    for row in result['evidence']:
        refs[row['path']] = row['sha256']
    pins = dict(refs)
    for filename in ['gate-full-v2.json', 'gate-publication-seal-v1.json']:
        gate = read(PACKET + filename)
        assert gate['exit_code'] == 0 and gate['exact_before_after_equal']
        assert gate['before_sha256'] == gate['after_sha256']
        for p, h in gate['after_sha256'].items():
            if p in pins and pins[p] != h:
                raise ValueError('Conflicting frozen input pin: ' + p)
            pins[p] = h
        pins.update(gate['private_outputs_sha256'])
    for p, h in pins.items():
        if Path(p).is_absolute() or ':' in p or '..' in Path(p).parts:
            raise ValueError('Nonrelative binding')
        if sha(p) != h:
            raise ValueError('Changed frozen input: ' + p)
    files = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard', '--', PACKET],
                           cwd=ROOT, check=True, capture_output=True, text=True).stdout.splitlines()
    assert files
    for p in files + [SELF]:
        text = (ROOT / p).read_text(encoding='utf-8-sig')
        scan(json.loads(text) if p.endswith('.json') else text)
    commands = [(['lake', 'env', 'lean', PACKET + 'ComplexStageTransport.lean'], 6),
                (['lake', 'env', 'lean', PACKET + 'ConsumerChecksC20.lean'], 10),
                (['.venv/Scripts/python.exe', '-m', 'unittest', 'discover', '-s', PACKET,
                  '-p', 'test_discriminators.py', '-v'], 0)]
    rows, unexpected = [], []
    for i, (command, expected) in enumerate(commands):
        env = os.environ.copy()
        env['LEAN_PATH'] = str(ROOT / PACKET / '.cache')
        env['PYTHONDONTWRITEBYTECODE'] = '1'
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
        okay = run.returncode == 0 and reports == expected
        if i == 2:
            okay = okay and 'Ran 7 tests' in text and 'skipped' not in text.lower()
        rows.append({'command': command, 'exit_code': run.returncode, 'passed': okay,
                     'seconds': time.perf_counter() - start, 'axiom_reports': reports,
                     'log': logs[i], 'log_sha256': sha(logs[i])})
        print(json.dumps(rows[-1]), flush=True)
        if not okay:
            break
    unchanged = all(sha(p) == h for p, h in pins.items())
    passed = len(rows) == 3 and all(r['passed'] for r in rows) and unchanged and not unexpected
    out = {'task': 'SP-HERMITE-POLY-002', 'passed': passed,
           'references_sha256': refs, 'resolved_pin_count': len(pins),
           'pin_maps': [PACKET + 'gate-full-v2.json', PACKET + 'gate-publication-seal-v1.json'],
           'bound_inputs_and_private_caches_unchanged': unchanged,
           'execution': rows, 'axiom_reports': sum(r['axiom_reports'] for r in rows),
           'unexpected_axioms': sorted(set(unexpected)), 'finite_test_methods': 7 if passed else None,
           'public_files_scanned': len(files) + 1, 'public_path_scan_passed': True,
           'scope': 'Actual stageCenter/stageEta complex Euclidean induced-error, nominal contraction, internally supplied Valid and actual flattened evaluator chronology, arbitrary complex inputs/full terminal carrier',
           'cache_provenance': 'Pinned private author fresh selected suppliers and inherited transitive production/Mathlib caches, not clean provider-wide build',
           'distinct_review': 'PENDING separate complex-stage-review-c21',
           'scientific_ROOT': False, 'main_admission': False, 'public_PURIFIED': False,
           'remaining': ['physical local-to-global support', 'uniform allocated degree/bits and full error budget',
                         'actual QR and finite-bit runtime refinement', 'complete piecewise stored producer',
                         'finite gate synthesis and independent scientific-family acceptance',
                         'publication/integration/reader gates and main Lean4.33 migration']}
    (ROOT / OUTPUT).write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': passed, 'receipt': OUTPUT, 'sha256': sha(OUTPUT)}), flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
