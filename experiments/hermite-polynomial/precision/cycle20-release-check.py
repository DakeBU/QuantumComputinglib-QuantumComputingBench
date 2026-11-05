"""Exact-name decoder correction check and scoped, path-clean WIP selection."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'experiments/hermite-polynomial/precision/'
DECODER = 'reviews/publication/stored-tensor-train/'
PACKETS = [PREFIX + 'piecewise-kernel-uniform-c20', PREFIX + 'complex-stage-transport-c20']
PATH = re.compile(r'(?<![A-Za-z0-9_])[A-Za-z]:[\\/]')


def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def read(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))


def main():
    provenance = read(DECODER + 'decoder-provenance-c19-v4.json')
    for row in provenance['old_files_preserved']:
        assert sha(row['path']) == row['sha256']
    for field in ['successor_artifact', 'successor_evidence']:
        assert sha(provenance[field]) == provenance[field + '_sha256']
    artifact = read(provenance['successor_artifact'])
    receipt = read(DECODER + 'decoder-c19-v3-public-receipt.json')
    messages = [json.loads(line) for line in receipt['stdout'].splitlines() if line.strip()]
    assert receipt['returncode'] == 0 and not any(m['severity'] == 'error' for m in messages)
    declarations = artifact['reconstruction']['declarations']
    assert len(declarations) == len({d['name'] for d in declarations}) == 30
    for row in declarations:
        name = re.escape(row['name'])
        exact = re.compile('^' + name + r'(?:\.\{[^}]*\})?(?=\s|:|$)')
        checked = [m['data'] for m in messages if exact.search(m['data'])]
        axioms = [m['data'] for m in messages if m['data'].startswith("'" + row['name'] + "' ")]
        assert len(checked) == len(axioms) == 1
        assert row['actual_checked_signature'] == checked[0]
        assert row['actual_axiom_report'] == axioms[0]
    assert provenance['provider_closure_exhaustive'] is False
    assert provenance['new_lean_execution'] is False
    files = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard', '--'] + PACKETS,
                           cwd=ROOT, check=True, capture_output=True, text=True).stdout.splitlines()
    files += [DECODER + p for p in ['decoder-artifact-c19-v4.json', 'decoder-evidence-c19-v4.json',
                                   'decoder-provenance-c19-v4.json', 'decoder-privacy-c19-v4.json']]
    files += [p.relative_to(ROOT).as_posix() for p in (ROOT / PREFIX).glob('cycle20-*') if p.is_file()]
    files += ['proof-obligations/SP-HERMITE-POLY-002.md', 'candidate-populations/SP-HERMITE-POLY-002.md']
    issues = []

    def scan(value, filename, key):
        if isinstance(value, dict):
            for k, v in value.items():
                scan(k, filename, key + '.<key>')
                scan(v, filename, key + '.' + str(k))
        elif isinstance(value, list):
            for i, v in enumerate(value):
                scan(v, filename, key + '.' + str(i))
        elif isinstance(value, str):
            if PATH.search(value) or re.search(r'github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]+', value):
                issues.append({'file': filename, 'field': key})

    selected = {}
    for p in sorted(set(files)):
        text = (ROOT / p).read_text(encoding='utf-8-sig')
        scan(json.loads(text) if p.endswith('.json') else text, p, '$')
        selected[p] = sha(p)
    print(json.dumps({'passed': not issues, 'selected_sha256': selected, 'issues': issues,
                      'exact_decoder_names_verified': 30,
                      'raw_receipts_or_active_workers_selected': False,
                      'scientific_ROOT': False, 'main_admission': False}, indent=2))
    return 0 if not issues else 1


if __name__ == '__main__':
    raise SystemExit(main())
