"""Validate the eighth scoped record and select only frozen, public-safe packets."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'experiments/hermite-polynomial/precision/'
REVIEW = 'reviews/publication/stored-tensor-train/'
PACKET = PREFIX + 'piecewise-kernel-assembly-c21/'
OUTPUT = PREFIX + 'cycle21-admission-staging-result.json'
TEST_LOG = PREFIX + 'cycle21-admission-regression-tests.log'


def main():
    assert not any((ROOT / path).exists() for path in [OUTPUT, TEST_LOG]), 'Immutable output exists'
    spec = importlib.util.spec_from_file_location('check', ROOT / 'website/scripts/check_research_publications.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    spec = importlib.util.spec_from_file_location('parent_privacy', ROOT / PREFIX / 'cycle21-review-parent-checkpoint.py')
    privacy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(privacy)
    inventory = {row['fullName']: row for row in privacy.read('web/library/declarations.json')['declarations']}
    records = privacy.read('website/research/publications.json')['records']
    assert len(records) == 8
    for record in records:
        checker.validate_record(ROOT, record, inventory)
    base = 'e71ed7555d03efc808978f9f52f34ac9a9b54589'
    changed = checker.changed_modules(ROOT, base)
    missing = sorted(set(changed) - {record['module'] for record in records})
    assert len(changed) == 51 and len(missing) == 43
    assert privacy.read(REVIEW + 'parent-admission-check-v1.json')['passed']
    assert privacy.read(PREFIX + 'cycle21-assembly-parent-checkpoint.json')['passed']
    command = ['.venv/Scripts/python.exe', '-m', 'unittest',
               'website.scripts.test_lean_publication_gate',
               'website.scripts.test_publication_byte_transport',
               'website.scripts.test_research_atlas', '-v']
    tests = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    text = tests.stdout + tests.stderr
    text = text.replace(str(ROOT), '<repository>').replace(ROOT.as_posix(), '<repository>')
    text = re.sub(r'(?<![A-Za-z0-9_])[A-Za-z]:[\\/][^\r\n\'"<>]*', '<private-path>', text)
    privacy.scan(text)
    (ROOT / TEST_LOG).write_text(text, encoding='utf-8')
    assert tests.returncode == 0 and 'Ran 45 tests' in text and 'skipped' not in text.lower()
    paths = [PACKET, REVIEW + 'source-review-c20/']
    files = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard', '--'] + paths,
                           cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    assert not any('/private-cache/' in path or '/.cache/' in path or path.endswith('.raw.log')
                   or path == REVIEW + 'source-review-c20/receipt-v1.json' for path in files)
    files += [REVIEW + name for name in ['prepare-admission-v1.py', 'publication-candidate-v2.json',
                                       'decoder-admission-evidence-v1.json', 'admission-preparation-v1.json',
                                       'source-topology-admission-v1.json', 'parent-admission-check-v1.py',
                                       'parent-admission-check-v1.json']]
    files += [REVIEW + 'parent-admission-check-v1-' + str(index) + '.log' for index in range(3)]
    files += [path.relative_to(ROOT).as_posix() for path in (ROOT / PREFIX).glob('cycle21-assembly-parent-checkpoint*') if path.is_file()]
    files += [PREFIX + 'cycle21-admission-release-check.py', TEST_LOG, 'website/research/publications.json',
              'proof-obligations/SP-HERMITE-POLY-002.md', 'candidate-populations/SP-HERMITE-POLY-002.md']
    selected = {}
    for path in sorted(set(files)):
        contents = (ROOT / path).read_text(encoding='utf-8-sig')
        privacy.scan(json.loads(contents) if path.endswith('.json') else contents)
        selected[path] = privacy.sha(path)
    result = {
        'passed': True, 'selected_sha256': selected,
        'whole_module_records_individually_valid': 8,
        'changed_production_modules': 51, 'missing_reviewed_records': missing,
        'full_diff_publication_gate': 'FAIL_CLOSED_43_MISSING_NOT_BYPASSED',
        'regression_command': command, 'regression_returncode': tests.returncode,
        'regression_tests': 45, 'regression_log': TEST_LOG, 'regression_log_sha256': privacy.sha(TEST_LOG),
        'assembly_ordinary_axiom_reports': 13, 'stored_tt_exact_types_and_axiom_reports': 30,
        'local_Lean_build_and_Tests': 'Actual parent commands exit0 under4.33; inherited caches/Verso boundary disclosed',
        'main_admission': False, 'scientific_ROOT': False, 'PURIFIED': False,
        'private_raw_or_user_files_selected': False, 'active_workers_selected': False,
        'production_source_changed': False,
        'scope': 'Actual full-source algebraic chain WIP and eighth whole-module retrospective stored exact-real publication record; no whole provider or finite-bit/scientific acceptance',
    }
    (ROOT / OUTPUT).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': True, 'selected_files': len(selected) + 1,
                      'reviewed': 8, 'missing': 43, 'tests': 45,
                      'receipt': OUTPUT, 'sha256': privacy.sha(OUTPUT)}))


if __name__ == '__main__':
    main()
