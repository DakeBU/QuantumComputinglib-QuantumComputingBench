"""Replay the exact full-source algebraic chain; no stored/runtime/ROOT shortcut."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'experiments/hermite-polynomial/precision/'
PACKET = PREFIX + 'piecewise-kernel-assembly-c21/'
OUTPUT = PREFIX + 'cycle21-assembly-parent-checkpoint.json'


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def main():
    logs = [PREFIX + 'cycle21-assembly-parent-checkpoint-' + str(index) + '.log' for index in range(4)]
    assert not any((ROOT / path).exists() for path in [OUTPUT] + logs), 'Immutable receipt exists'
    refs = {
        PACKET + 'result.json': '01b5c0f605c33d767979273753992a6ec0833170a9703510e90ee74336f9746f',
        PACKET + 'final-binding-manifest.json': '92b4d401a9547cd980c6d954185ee5d41deb0e0308730a67fcea31494e919f2d',
    }
    manifest = read(PACKET + 'final-binding-manifest.json')
    assert manifest['all_writes_stopped'] and manifest['bindings_unchanged']
    assert manifest['fresh_source_passes'] == 19
    pins = dict(refs)
    for key in ['artifact_hashes', 'ignored_cache_hashes']:
        pins.update({PACKET + path: digest for path, digest in manifest[key].items()})
    for key in ['sources', 'frozen_inherited']:
        pins.update(manifest['pre_gate_bindings'][key])
    pins.update(manifest['inherited_source_equality_to_frozen_receipts'])
    for path, digest in pins.items():
        assert ':' not in path and not Path(path).is_absolute() and '..' not in Path(path).parts
        assert sha(path) == digest, 'Changed sealed input: ' + path
    resolved = manifest['resolved_consumerchecks']
    assert resolved['source'] == PREFIX + 'finite-middle-source/ConsumerChecks.lean'
    assert resolved['c20_consumerchecks_not_selected'] is True
    assert sha(PACKET + '.cache/ConsumerChecks.olean') == resolved['cache_sha256']
    launch = read(PACKET + 'launcher-receipt-v1.json')
    assert launch['process_exit'] == 1 and launch['accepted_whole_launcher_process'] is False
    focused = (ROOT / PACKET / 'focused-v1.public-v1.log').read_text(encoding='utf-8-sig')
    assert len(re.findall(r'^PASS .*\.lean\s*$', focused, re.M)) == 19
    assert 'ALL PRE-GATE SOURCE/SEAL/FROZEN BINDINGS UNCHANGED' in focused
    assert 'sorryAx' not in focused and not re.search(r'\berror:', focused)
    spec = importlib.util.spec_from_file_location('privacy', ROOT / PREFIX / 'cycle21-review-parent-checkpoint.py')
    privacy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(privacy)
    files = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard', '--', PACKET],
                           cwd=ROOT, check=True, capture_output=True, text=True).stdout.splitlines()
    for path in files:
        text = (ROOT / path).read_text(encoding='utf-8-sig')
        privacy.scan(json.loads(text) if path.endswith('.json') else text)
    rows, unexpected = [], []
    for index, (file, expected) in enumerate([('IndexedKernel.lean', 3), ('ActualCoefficients.lean', 3),
                                             ('ActualAssembly.lean', 5), ('AssemblyConsumerChecks.lean', 2)]):
        command = ['lake', 'env', 'lean', PACKET + file]
        env = os.environ.copy()
        env['LEAN_PATH'] = os.pathsep.join(str(ROOT / PREFIX / name / '.cache') for name in
                                          ['piecewise-kernel-assembly-c21', 'piecewise-kernel-producer', 'piecewise-kernel-uniform-c20'])
        start = time.perf_counter()
        run = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        text = run.stdout.replace(str(ROOT), '<repository>').replace(ROOT.as_posix(), '<repository>')
        text = re.sub(r'(?<![A-Za-z0-9_])[A-Za-z]:[\\/][^\r\n\'"<>]*', '<private-path>', text)
        privacy.scan(text)
        (ROOT / logs[index]).write_text(text, encoding='utf-8')
        matches = list(re.finditer(r'depends on axioms: \[(.*?)\]', text, re.S))
        reports = len(matches) + len(re.findall(r'does not depend on any axioms', text))
        for match in matches:
            names = [re.sub(r'\.\{[^}]*\}$', '', item.strip()) for item in match[1].split(',')]
            unexpected.extend(name for name in names if name and name not in {'propext', 'Classical.choice', 'Quot.sound'})
        passed = run.returncode == 0 and reports == expected
        rows.append({'command': command, 'returncode': run.returncode, 'passed': passed,
                     'seconds': time.perf_counter() - start, 'ordinary_axiom_reports': reports,
                     'log': logs[index], 'log_sha256': sha(logs[index])})
        print(json.dumps(rows[-1]), flush=True)
        if not passed:
            break
    unchanged = all(sha(path) == digest for path, digest in pins.items())
    passed = len(rows) == 4 and all(row['passed'] for row in rows) and unchanged and not unexpected
    result = {
        'task': 'SP-HERMITE-POLY-002', 'passed': passed, 'references_sha256': refs,
        'binding_manifest': PACKET + 'final-binding-manifest.json', 'resolved_pin_count': len(pins),
        'all_bound_inputs_and_private_outputs_unchanged': unchanged, 'execution': rows,
        'ordinary_axiom_reports': sum(row['ordinary_axiom_reports'] for row in rows),
        'unexpected_axioms': sorted(set(unexpected)), 'public_files_scanned': len(files),
        'public_path_scan_passed': True, 'launcher_failure_retained': launch['type'],
        'scope': 'Actual rational source coefficients and five-way q0-LSB chain on actual rationalGrid, same-object bond/scalar address bounds, actual allocated positive radius',
        'cache_provenance': '19 fresh selected suppliers, exact ordered ConsumerChecks cache; other inherited source/cache correspondence not a full clean closure',
        'distinct_source_review': 'PENDING', 'scientific_ROOT': False, 'main_admission': False, 'PURIFIED': False,
        'remaining': ['actual computable full stored tables and unconditional Window',
                      'same returned stored producer refinement', 'fully charged generation/copy/assembly costs',
                      'finite-bit/GCD/representation/runtime and QR', 'original source normalization/error composition',
                      'physical synthesis, independent family executable acceptance and ROOT'],
    }
    (ROOT / OUTPUT).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': passed, 'receipt': OUTPUT, 'sha256': sha(OUTPUT)}), flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
