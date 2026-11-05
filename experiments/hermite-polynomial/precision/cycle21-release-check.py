"""Select only the frozen C21 internal review and its parent replay for Git."""
import importlib.util
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'experiments/hermite-polynomial/precision/'
PACKET = PREFIX + 'complex-stage-review-c21/'
OUTPUT = PREFIX + 'cycle21-staging-result.json'


def main():
    if (ROOT / OUTPUT).exists():
        raise SystemExit('Immutable selection receipt exists')
    path = ROOT / PREFIX / 'cycle21-review-parent-checkpoint.py'
    spec = importlib.util.spec_from_file_location('parent_check', path)
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    gate = parent.read(PREFIX + 'cycle21-review-parent-checkpoint.json')
    assert gate['passed'] and gate['axiom_reports'] == 18 and gate['finite_cases'] == 35
    for file, digest in gate['references_sha256'].items():
        assert parent.sha(file) == digest
    for row in gate['execution']:
        assert row['passed'] and parent.sha(row['log']) == row['log_sha256']
    files = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard', '--', PACKET],
                           cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    assert files and not any('/.cache/' in file or '/__pycache__/' in file for file in files)
    files += [file.relative_to(ROOT).as_posix()
              for file in (ROOT / PREFIX).glob('cycle21-*') if file.is_file()]
    files += ['proof-obligations/SP-HERMITE-POLY-002.md', 'candidate-populations/SP-HERMITE-POLY-002.md']
    selected = {}
    for file in sorted(set(files)):
        text = (ROOT / file).read_text(encoding='utf-8-sig')
        parent.scan(json.loads(text) if file.endswith('.json') else text)
        selected[file] = parent.sha(file)
    result = {'passed': True, 'selected_sha256': selected,
              'scope': 'Frozen distinct internal complex review and successful parent replay only',
              'axiom_reports': 18, 'finite_cases': 35,
              'active_worker_files_selected': False, 'raw_private_receipts_selected': False,
              'user_files_selected': False, 'production_source_changed': False,
              'scientific_ROOT': False, 'main_admission': False, 'PURIFIED': False,
              'publication_debt': {'accepted': 7, 'missing': 44, 'total_changed': 51}}
    (ROOT / OUTPUT).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': True, 'selected_files': len(selected) + 1,
                      'receipt': OUTPUT, 'sha256': parent.sha(OUTPUT)}))


if __name__ == '__main__':
    main()
