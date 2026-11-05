"""Parent replay of the frozen distinct complex-stage review, not ROOT admission."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'experiments/hermite-polynomial/precision/'
PACKET = PREFIX + 'complex-stage-review-c21/'
AUTHOR = PREFIX + 'complex-stage-transport-c20/'
OUTPUT = PREFIX + 'cycle21-review-parent-checkpoint.json'
PATH = re.compile(r'(?<![A-Za-z0-9_])[A-Za-z]:[\\/]')


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def scan(value):
    if isinstance(value, dict):
        for key, item in value.items():
            scan(key)
            scan(item)
    elif isinstance(value, list):
        for item in value:
            scan(item)
    elif isinstance(value, str):
        if PATH.search(value) or re.search(r'github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]+', value):
            raise ValueError('Public path/credential policy violation')


def main():
    logs = [PREFIX + 'cycle21-review-parent-checkpoint-' + str(i) + '.log' for i in range(4)]
    if any((ROOT / path).exists() for path in [OUTPUT] + logs):
        raise SystemExit('Immutable checkpoint already exists')
    references = {
        PACKET + 'review-result-v1.json': '31cc4669c707332642ad1076eef7e1b91fb3282bb094396dacffee9dbb2cfa34',
        PACKET + 'review-handoff-v1.json': '8f433261333258ced910ba8f3785349d88198999d5bcaded66953d4bc2fc245b',
        PREFIX + 'cycle21-review-parent-checkpoint.py': sha(PREFIX + 'cycle21-review-parent-checkpoint.py'),
    }
    result = read(PACKET + 'review-result-v1.json')
    for row in result['evidence']:
        references[row['path']] = row['sha256']
    for path, digest in result['author_frozen_sha256'].items():
        references[AUTHOR + path] = digest
    gate = read(PACKET + 'gate-review-v1.json')
    assert gate['exit_code'] == 0 and gate['exact_before_after_equal']
    before = read(PACKET + gate['before_pins'])
    assert before == gate['after_sha256'] and len(before) == 7097
    assert len(gate['execution']) == 16 and all(row['exit_code'] == 0 for row in gate['execution'])
    pins = dict(before)
    for row in gate['execution']:
        command = row['command']
        assert command[:4] == ['lake', 'env', 'lean', '-o']
        pins[command[4]] = row['output_sha256']
    pins.update(references)
    for path, digest in pins.items():
        assert not Path(path).is_absolute() and ':' not in path and '..' not in Path(path).parts
        assert sha(path) == digest, 'Changed pin: ' + path
    public_files = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard', '--', PACKET],
                                  cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    for path in public_files + [PREFIX + 'cycle21-review-parent-checkpoint.py']:
        text = (ROOT / path).read_text(encoding='utf-8-sig')
        scan(json.loads(text) if path.endswith('.json') else text)
    # The independent finite script is replayed with an isolated output destination.
    # This leaves every frozen reviewer receipt untouched.
    finite_code = (
        "import importlib.util,tempfile; from pathlib import Path; "
        "p=Path('" + PACKET + "independent_discriminators.py'); "
        "s=importlib.util.spec_from_file_location('review_finite',p); "
        "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
        "t=tempfile.TemporaryDirectory(prefix='abeis-c21-parent-'); "
        "m.HERE=Path(t.name); m.main(); t.cleanup()"
    )
    commands = [(['lake', 'env', 'lean', AUTHOR + 'ComplexStageTransport.lean'], 6),
                (['lake', 'env', 'lean', AUTHOR + 'ConsumerChecksC20.lean'], 10),
                (['lake', 'env', 'lean', PACKET + 'ReviewChecksC21.lean'], 2),
                (['.venv/Scripts/python.exe', '-c', finite_code], 0)]
    rows, unexpected = [], []
    for index, (command, expected) in enumerate(commands):
        env = os.environ.copy()
        env['LEAN_PATH'] = str(ROOT / PACKET / '.cache')
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        start = time.perf_counter()
        run = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        text = run.stdout.replace(str(ROOT), '<repo>').replace(ROOT.as_posix(), '<repo>')
        text = re.sub(r'(?<![A-Za-z0-9_])[A-Za-z]:[\\/][^\r\n\'"<>]*', '<private-path>', text)
        scan(text)
        (ROOT / logs[index]).write_text(text, encoding='utf-8')
        hits = list(re.finditer(r'depends on axioms: \[(.*?)\]', text, re.S))
        reports = len(hits) + len(re.findall(r'does not depend on any axioms', text))
        for hit in hits:
            names = [re.sub(r'\.\{[^}]*\}$', '', name.strip()) for name in hit[1].split(',')]
            unexpected.extend(name for name in names if name and name not in {'propext', 'Classical.choice', 'Quot.sound'})
        passed = run.returncode == 0 and reports == expected
        if index == 3:
            finite = json.loads(text)
            passed = passed and finite['passed'] and finite['cases'] == 35
        rows.append({'command': command, 'exit_code': run.returncode, 'passed': passed,
                     'seconds': time.perf_counter() - start, 'axiom_reports': reports,
                     'log': logs[index], 'log_sha256': sha(logs[index])})
        print(json.dumps(rows[-1]), flush=True)
        if not passed:
            break
    unchanged = all(sha(path) == digest for path, digest in pins.items())
    passed = len(rows) == 4 and all(row['passed'] for row in rows) and unchanged and not unexpected
    receipt = {
        'task': 'SP-HERMITE-POLY-002', 'passed': passed,
        'review_status': result['status'], 'references_sha256': references,
        'resolved_pin_count': len(pins), 'all_bound_inputs_and_private_caches_unchanged': unchanged,
        'execution': rows, 'axiom_reports': sum(row['axiom_reports'] for row in rows),
        'unexpected_axioms': sorted(set(unexpected)), 'finite_cases': 35 if passed else None,
        'public_files_scanned': len(public_files) + 1, 'public_path_scan_passed': True,
        'distinct_review': 'accepted only at the internal actual-complex-stage interface',
        'cache_provenance': 'Fresh selected reviewer cache; 3404 inherited caches have explicitly unknown source correspondence; not full clean source closure',
        'scientific_ROOT': False, 'main_admission': False, 'public_source_blind_review': False,
        'PURIFIED': False,
        'remaining': ['uniform whole-family error allocation', 'actual full piecewise stored producer',
                      'QR and finite-bit runtime refinement', 'physical local/global support',
                      'finite gate synthesis and independent family executable acceptance',
                      'whole-module publication debt and main Lean4.33 migration'],
    }
    (ROOT / OUTPUT).write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': passed, 'receipt': OUTPUT, 'sha256': sha(OUTPUT)}), flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
