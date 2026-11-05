"""Record actual local repository gates without touching executable exports."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'experiments/hermite-polynomial/precision/'
OUTPUT = PREFIX + 'cycle20-integration-gate.json'


def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def main():
    logs = [PREFIX + 'cycle20-integration-gate-' + str(i) + '.log' for i in range(2)]
    if any((ROOT / p).exists() for p in [OUTPUT] + logs):
        raise SystemExit('Immutable integration receipt already exists')
    files = subprocess.run(['git', 'ls-files', '--', 'QuantumBlockEncoding', 'ABEISTests',
                            'QuantumBlockEncoding.lean', 'ABEISTests.lean',
                            'lean-toolchain', 'lakefile.lean', 'lake-manifest.json'],
                           cwd=ROOT, check=True, capture_output=True, text=True).stdout.splitlines()
    before = {p: sha(p) for p in files}
    rows = []
    for i, command in enumerate([['lake', 'build'], ['lake', 'build', 'Tests']]):
        start = time.perf_counter()
        run = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             encoding='utf-8', errors='replace')
        text = run.stdout.replace(str(ROOT), '<repo>').replace(ROOT.as_posix(), '<repo>')
        text = re.sub(r'(?<![A-Za-z0-9_])[A-Za-z]:[\\/][^\r\n\'"<>]*', '<private-path>', text)
        (ROOT / logs[i]).write_text(text, encoding='utf-8')
        jobs = re.findall(r'Build completed successfully \((\d+) jobs\)', text)
        rows.append({'command': command, 'exit_code': run.returncode,
                     'seconds': time.perf_counter() - start, 'log': logs[i],
                     'log_sha256': sha(logs[i]), 'jobs': int(jobs[-1]) if jobs else None})
        print(json.dumps(rows[-1]), flush=True)
        if run.returncode:
            break
    inherited = json.loads((ROOT / (PREFIX + 'complex-stage-transport-c20/gate-publication-seal-v1.json')).read_text())['after_sha256']
    inherited_changes = [p for p, h in inherited.items() if sha(p) != h]
    unchanged = before == {p: sha(p) for p in before}
    passed = len(rows) == 2 and all(r['exit_code'] == 0 for r in rows) and unchanged and not inherited_changes
    out = {'passed': passed, 'execution': rows, 'proof_input_files': len(before),
           'proof_inputs_unchanged': unchanged,
           'post_build_author_sealed_pin_count': len(inherited),
           'post_build_author_sealed_changes': inherited_changes,
           'environment': 'Incremental local Lean4.33 build with inherited caches and existing local Verso edits, not clean CI or fresh transitive compilation',
           'executable_exports_run': False, 'reader_gate': 'NOT_RUN_FOR_INTERNAL_WIP',
           'scientific_ROOT': False, 'main_admission': False, 'public_PURIFIED': False}
    (ROOT / OUTPUT).write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': passed, 'receipt': OUTPUT, 'sha256': sha(OUTPUT)}), flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
