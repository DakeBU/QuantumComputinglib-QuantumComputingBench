"""Read-only focused acceptance with immutable receipts, not root admission."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'experiments/hermite-polynomial/precision/'
OUTPUT = PREFIX + 'cycle18-parent-checkpoint.json'
SCRIPT = PREFIX + 'cycle18-parent-checkpoint.py'


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def main():
    if (ROOT / OUTPUT).exists():
        raise SystemExit('Immutable parent receipt already exists')
    bound = {SCRIPT: sha(SCRIPT)}

    def check(pins):
        for path, expected in pins.items():
            if Path(path).is_absolute() or ':' in path or '..' in Path(path).parts:
                raise ValueError('Nonrelative artifact binding')
            if sha(path) != expected:
                raise ValueError('Changed frozen artifact: ' + path)
            if path in bound and bound[path] != expected:
                raise ValueError('Incompatible artifact pin: ' + path)
            bound[path] = expected

    review = PREFIX + 'source-stage-review-c17/'
    adapter = PREFIX + 'literal-complex-adapter/'
    audit = read(review + 'independent-audit.json')
    check(audit['artifact_sha256'])
    check({review + 'independent-audit.json':
           '1d0beaa767c5d1a4c275068b96f46b418fda26967905fbe0ea4851c2dcce4d99',
           review + 'handoff.json':
           'b54499c7fd8bbddc8c6b60138ef5f58540025127d102b6a643fc17264a8625a0'})
    for name in ('source', 'stage'):
        receipt = read(review + name + '-replay-v3.json')
        assert receipt['exit_code'] == 0 and receipt['bound_inputs_unchanged']
        check(receipt['bindings_sha256'])
        check(receipt['private_olean_sha256'])
    author = read(adapter + 'gate-full-v1.json')
    assert author['exit_code'] == 0 and author['bound_inputs_unchanged']
    check(author['bindings_sha256'])
    check({adapter + 'gate-full-v1.json':
           '0db5dfc70a7822fad9c225b32c53a9d201af37c6fbdeb0cd71114f4716ecac2c'})
    caches = [review + '.cache/source-v3', review + '.cache/stage-v3', adapter + '.cache']
    for cache in caches:
        for file in sorted((ROOT / cache).rglob('*.olean')):
            relative = file.relative_to(ROOT).as_posix()
            check({relative: sha(relative)})
    commands = [
        (['lake', 'env', 'lean', review + 'SourceDiscriminatorsV1.lean'], caches[0]),
        (['lake', 'env', 'lean', review + 'StageDiscriminatorsV1.lean'], caches[1]),
        (['lake', 'env', 'lean', adapter + 'ConsumerChecks.lean'], caches[2]),
        (['.venv/Scripts/python.exe', review + 'test_actual_local_v1.py', '-v'], None),
        (['.venv/Scripts/python.exe', adapter + 'test_discriminators.py', '-v'], None),
    ]
    logs = [PREFIX + 'cycle18-parent-checkpoint-' + str(i) + '.log'
            for i in range(len(commands))]
    if any((ROOT / log).exists() for log in logs):
        raise SystemExit('Immutable parent log already exists')
    executions = []
    roots = 0
    forbidden = []
    for i, (command, cache) in enumerate(commands):
        env = os.environ.copy()
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        if cache:
            env['LEAN_PATH'] = str(ROOT / cache)
        start = time.perf_counter()
        run = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        text = run.stdout.replace(str(ROOT), '<repo>').replace(ROOT.as_posix(), '<repo>')
        text = re.sub(r'[A-Za-z]:[\\/][^\r\n\'"<>]*', '<private-path>', text)
        (ROOT / logs[i]).write_text(text, encoding='utf-8')
        for printed in re.finditer(r'depends on axioms: \[(.*?)\]', text, re.S):
            roots += 1
            axioms = [x.strip() for x in printed.group(1).split(',') if x.strip()]
            forbidden.extend(x for x in axioms
                             if x not in {'propext', 'Classical.choice', 'Quot.sound'})
        executions.append({'command': command, 'exit_code': run.returncode,
                           'seconds': time.perf_counter() - start,
                           'log': logs[i], 'log_sha256': sha(logs[i]),
                           'private_cache': cache})
        print(json.dumps(executions[-1]), flush=True)
        if run.returncode:
            break
    unchanged = all(sha(p) == digest for p, digest in bound.items())
    passed = (len(executions) == len(commands) and
              all(row['exit_code'] == 0 for row in executions) and
              unchanged and not forbidden and roots >= 23)
    receipt = {
        'schema_version': 1, 'task': 'SP-HERMITE-POLY-002', 'passed': passed,
        'source_stage_review': 'Accepted internal provider scope only',
        'literal_complex_adapter': 'PROVED_LOCAL_PENDING_DISTINCT_REVIEW',
        'bindings_sha256': bound, 'inputs_and_caches_unchanged': unchanged,
        'execution': executions, 'printed_axiom_roots': roots,
        'unexpected_axioms': sorted(set(forbidden)),
        'cache_provenance': 'Parent consumers reuse pinned reviewer/author private caches; '
                            'fresh whole-source author/reviewer gates are separate receipts. '
                            'This is not a clean transitive build.',
        'finite_tests': '1 actual local-carrier method and 5 adapter diagnostics; '
                        'neither is scientific-family acceptance',
        'scientific_ROOT': False, 'main_admission': False, 'public_PURIFIED': False,
        'remaining': ['precision-aware stored cores and same-run cost', 'QR and bit/GCD cost',
                      'complex operator-error and physical local-to-global lifting',
                      'full terminal readout', 'finite synthesis',
                      'independent scientific-family acceptance', 'whole publication debt']}
    (ROOT / OUTPUT).write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': passed, 'receipt': OUTPUT, 'sha256': sha(OUTPUT),
                      'binding_count': len(bound), 'printed_axiom_roots': roots}), flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
