"""Full-source focused replay. Additive immutable receipts; private cache only."""
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

def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def sanitize(text):
    for p in (str(ROOT), str(ROOT).replace('\\', '/')):
        text = text.replace(p, '<repo>')
    return re.sub(r'[A-Za-z]:[\\/][^\r\n\'"<>]*', '<private-path>', text)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--record', required=True)
    p.add_argument('--reuse-private-suppliers', action='store_true')
    args = p.parse_args()
    receipt = HERE / f'gate-{args.record}.json'
    if receipt.exists() or list(HERE.glob(f'gate-{args.record}-*.log')):
        raise SystemExit('Refusing to replace immutable records')
    (HERE / '.cache').mkdir(exist_ok=True)
    inputs = [str(x.relative_to(ROOT).as_posix()) for x in HERE.iterdir()
              if x.is_file() and x.suffix in ('.lean', '.py')]
    inputs += [f'{REL}/statement-seal-v1.json', f'{REL}/operator-seal-v1.json', 'lean-toolchain', 'lake-manifest.json',
               'experiments/hermite-polynomial/precision/finite-trig/FiniteTrig.lean',
               'experiments/hermite-polynomial/precision/saved-rounding/SavedRounding.lean',
               'experiments/hermite-polynomial/precision/saved-action/saved_action.py',
               'experiments/hermite-polynomial/precision/saved-rounding/result-v1.json',
               'experiments/hermite-polynomial/precision/saved-rounding/independent-audit.json',
               'experiments/hermite-polynomial/precision/next-source-stage-design-c15.json',
               'experiments/hermite-polynomial/precision/nonunitary-transport/NonunitaryTransport.lean',
               'tasks/SP-HERMITE-POLY-002.md', f'{REL}/.gitignore',
               '.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/Matrix.lean',
               '.lake/packages/mathlib/Mathlib/Algebra/Order/BigOperators/Ring/Finset.lean']
    before = {s: digest(s) for s in sorted(inputs)}
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['LEAN_PATH'] = str(HERE / '.cache') + os.pathsep + env.get('LEAN_PATH', '')
    modules = [
        ('FiniteTrig', 'experiments/hermite-polynomial/precision/finite-trig/FiniteTrig.lean'),
        ('SavedRounding', 'experiments/hermite-polynomial/precision/saved-rounding/SavedRounding.lean'),
        ('SavedStageInterpreter', f'{REL}/SavedStageInterpreter.lean'),
        ('StageOperatorBound', f'{REL}/StageOperatorBound.lean')]
    if args.reuse_private_suppliers:
        modules = modules[2:]
    commands = [['lake', 'env', 'lean', '-o', f'{REL}/.cache/{name}.olean', src]
                for name, src in modules]
    if (HERE / 'ConsumerChecks.lean').exists():
        commands += [['lake', 'env', 'lean', f'{REL}/ConsumerChecks.lean']]
    if (HERE / 'test_saved_stage.py').exists():
        commands += [['.venv/Scripts/python.exe', f'{REL}/test_saved_stage.py', '-v']]
    rows = []
    status = 0
    for i, command in enumerate(commands):
        start = time.perf_counter()
        run = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        log = HERE / f'gate-{args.record}-{i}.log'
        log.write_text(sanitize(run.stdout), encoding='utf-8')
        print(sanitize(run.stdout), end='', flush=True)
        rows.append({'command': command, 'exit_code': run.returncode,
                     'seconds': time.perf_counter() - start,
                     'log': log.relative_to(ROOT).as_posix(), 'log_sha256': digest(log.relative_to(ROOT).as_posix())})
        status = run.returncode
        if status:
            break
    after = {s: digest(s) for s in before}
    result = {'schema_version': 1, 'evidence_class': 'C_INTERNAL_PROVIDER',
              'exit_code': status, 'full_sources': not args.reuse_private_suppliers,
              'execution': rows, 'bindings_sha256': before,
              'bound_inputs_unchanged': before == after,
              'scientific_root': False, 'source_anchor': False,
              'uniform_finite_bit_certificate': False}
    receipt.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Receipt SHA256:', digest(receipt.relative_to(ROOT).as_posix()), flush=True)
    return status

if __name__ == '__main__':
    raise SystemExit(main())
