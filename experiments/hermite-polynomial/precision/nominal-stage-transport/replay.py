"""Immutable, sanitized focused gates using only a worker-owned private cache."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REL = HERE.relative_to(ROOT).as_posix()
PREFIX = 'experiments/hermite-polynomial/precision/'
MODULES = [
    ('FiniteTrig', PREFIX + 'finite-trig/FiniteTrig.lean'),
    ('SavedRounding', PREFIX + 'saved-rounding/SavedRounding.lean'),
    ('SavedStageInterpreter', PREFIX + 'saved-stage-interpreter/SavedStageInterpreter.lean'),
    ('StageOperatorBound', PREFIX + 'saved-stage-interpreter/StageOperatorBound.lean'),
    ('NonunitaryTransport', PREFIX + 'nonunitary-transport/NonunitaryTransport.lean'),
    ('NominalStageTransport', REL + '/NominalStageTransport.lean'),
    ('ChronologicalTransport', REL + '/ChronologicalTransport.lean'),
]

def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def sanitize(text):
    for value in (str(ROOT), str(ROOT).replace('\\', '/')):
        text = text.replace(value, '<repo>')
    return re.sub(r'[A-Za-z]:[\\/][^\r\n\'"<>]*', '<private-path>', text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', required=True)
    parser.add_argument('--reuse-private-suppliers', action='store_true')
    args = parser.parse_args()
    receipt = HERE / ('gate-' + args.record + '.json')
    if receipt.exists() or list(HERE.glob('gate-' + args.record + '-*.log')):
        raise SystemExit('Refusing to overwrite immutable gate evidence')
    (HERE / '.cache').mkdir(exist_ok=True)
    inputs = [p for _, p in MODULES]
    inputs += [str(p.relative_to(ROOT).as_posix()) for p in HERE.iterdir()
               if p.is_file() and p.suffix in ('.py', '.lean')]
    inputs += [REL + '/statement-seal-v1.json', REL + '/chronology-seal-v2-additive.json', REL + '/.gitignore', 'lean-toolchain',
               'lake-manifest.json', 'tasks/SP-HERMITE-POLY-002.md',
               PREFIX + 'saved-stage-interpreter/result-v1.json',
               PREFIX + 'saved-stage-interpreter/independent-audit.json',
               '.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/Matrix.lean']
    before = {p: digest(p) for p in sorted(set(inputs))}
    expected = {
        PREFIX + 'saved-stage-interpreter/result-v1.json': 'b2ee44272c1a5a9e95d05a41af7eef2a28a968af60faf751c8f97976edf25074',
        PREFIX + 'saved-stage-interpreter/SavedStageInterpreter.lean': '9b6c52730dbb686908b7d98eff368bf7d87ed89b309ad162437372bca5e83d7d',
        PREFIX + 'saved-stage-interpreter/StageOperatorBound.lean': 'd763f631af61c598a5cac6ae7cbaa37138d120a9801c1fa53969ffdbcc4d09f4',
        'tasks/SP-HERMITE-POLY-002.md': '99bd13431c2e49de7a67658e489935b8fd5c965ab473285e3fbaf0a78b5b1ce9',
    }
    if any(before[p] != value for p, value in expected.items()):
        raise SystemExit('Frozen dependency/task binding changed; no gate run')
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['LEAN_PATH'] = str(HERE / '.cache')
    modules = MODULES[-2:] if args.reuse_private_suppliers else MODULES
    commands = [['lake', 'env', 'lean', '-o', REL + '/.cache/' + name + '.olean', path]
                for name, path in modules]
    if (HERE / 'ConsumerChecks.lean').exists():
        commands += [['lake', 'env', 'lean', REL + '/ConsumerChecks.lean']]
    if (HERE / 'test_discriminators.py').exists():
        commands += [['.venv/Scripts/python.exe', REL + '/test_discriminators.py', '-v']]
    rows = []
    code = 0
    for i, command in enumerate(commands):
        start = time.perf_counter()
        run = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        output = sanitize(run.stdout)
        log = HERE / ('gate-' + args.record + '-' + str(i) + '.log')
        log.write_text(output, encoding='utf-8')
        print(output, end='', flush=True)
        rows.append({'command': command, 'exit_code': run.returncode,
                     'seconds': time.perf_counter() - start,
                     'log': log.relative_to(ROOT).as_posix(),
                     'log_sha256': digest(log.relative_to(ROOT).as_posix())})
        code = run.returncode
        if code:
            break
    result = {'schema_version': 1, 'evidence_class': 'C_INTERNAL_PROVIDER',
              'exit_code': code, 'full_sources': not args.reuse_private_suppliers,
              'execution': rows, 'bindings_sha256': before,
              'bound_inputs_unchanged': before == {p: digest(p) for p in before},
              'scientific_root': False, 'source_anchor': False,
              'uniform_finite_bit_certificate': False}
    receipt.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Receipt SHA256:', digest(receipt.relative_to(ROOT).as_posix()), flush=True)
    return code

if __name__ == '__main__':
    raise SystemExit(main())
