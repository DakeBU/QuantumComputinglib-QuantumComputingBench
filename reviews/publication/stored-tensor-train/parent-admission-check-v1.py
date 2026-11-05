"""Fresh whole-source parent check with inherited-provider pins and no target cache."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIX = HERE.relative_to(ROOT).as_posix() + '/'
REVIEW = PREFIX + 'source-review-c20/'
OUTPUT = PREFIX + 'parent-admission-check-v1.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def main():
    logs = [PREFIX + 'parent-admission-check-v1-' + str(i) + '.log' for i in range(3)]
    assert not any((ROOT / path).exists() for path in [OUTPUT] + logs), 'Immutable output exists'
    receipt_path = REVIEW + 'receipt-v7.json'
    assert sha(ROOT / receipt_path) == '16ff413a2afdf2828c780d9bb7032d71457512d00ddd1688be0ab91d0ff53abb'
    reviewed = read(receipt_path)
    assert reviewed['returncode'] == 0 and reviewed['whole_target_source']
    assert not reviewed['target_cache_imported'] and not reviewed['production_outputs_requested']
    for key in ['inputs_unchanged', 'private_cache_unchanged', 'provider_sources_unchanged',
                'original_provider_artifacts_unchanged', 'native_pins_unchanged']:
        assert reviewed[key]
    assert reviewed['provider_count'] == 4901
    prefix = Path(subprocess.run(['lake', 'env', 'lean', '--print-prefix'], cwd=ROOT,
                                capture_output=True, text=True, check=True).stdout.strip().splitlines()[-1])

    def resolve(locator):
        for token, base in [('<repository>', ROOT), ('<lean-toolchain>', prefix)]:
            if locator.startswith(token):
                path = base / locator[len(token):].lstrip('/\\')
                assert path.resolve().is_relative_to(base.resolve())
                return path
        raise ValueError('Unclassified provider locator')

    pins = {}
    for path, digest in reviewed['input_sha256_before'].items():
        pins[ROOT / path] = digest
    pins[ROOT / receipt_path] = sha(ROOT / receipt_path)
    for provider in reviewed['providers']:
        pins[resolve(provider['source'])] = provider['source_sha256']
        for artifact in provider['artifacts']:
            pins[resolve(artifact['path'])] = artifact['sha256']
            pins[ROOT / REVIEW / artifact['private_path']] = artifact['sha256']
    for row in reviewed['native_pins_before']:
        pins[resolve(row['path'])] = row['sha256']
    for path, digest in pins.items():
        assert sha(path) == digest, 'Frozen provider/input changed'
    candidate = read(PREFIX + 'publication-candidate-v2.json')
    names = candidate['declarations']
    assert len(names) == len(set(names)) == 30
    source = (ROOT / candidate['module']).read_text(encoding='utf-8-sig')
    checks = '\nset_option pp.all true\n'
    for name in names:
        checks += '\n#check ' + name + '\n#print axioms ' + name + '\n'
    checks += (ROOT / REVIEW / 'consumer-v7.lean').read_text(encoding='utf-8-sig')
    for op in ['field', 'sqrt', 'angle', 'trig', 'compare', 'read', 'write', 'emit']:
        checks += ('\nexample {l m r : ℕ} (A : QuantumBlockEncoding.StoredTensorTrain.StoredCore l m) '
                   '(R : QuantumBlockEncoding.StoredGivens.StoredMatrix m r) : '
                   '(QuantumBlockEncoding.StoredTensorTrain.absorption A R).cost .' + op +
                   ' ≤ QuantumBlockEncoding.StoredTensorTrain.absorptionBudget l m r .' + op +
                   ' := QuantumBlockEncoding.StoredTensorTrain.absorption_cost_le A R .' + op + '\n')
    payload = source + checks
    commands = [(['lake', 'env', 'lean', '--stdin', '--json'], payload),
                (['lake', 'build'], None), (['lake', 'build', 'Tests'], None)]
    rows, messages = [], []
    for index, (command, stdin) in enumerate(commands):
        started = time.perf_counter()
        run = subprocess.run(command, cwd=ROOT, input=stdin, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        text = run.stdout
        text = text.replace(str(ROOT), '<repository>').replace(ROOT.as_posix(), '<repository>')
        text = text.replace(str(prefix), '<lean-toolchain>').replace(prefix.as_posix(), '<lean-toolchain>')
        text = re.sub(r'(?<![A-Za-z0-9_])[A-Za-z]:[\\/][^\r\n\'"<>]*', '<private-path>', text)
        if index == 0:
            messages = [json.loads(line) for line in text.splitlines() if line.startswith('{')]
            assert not any(message.get('severity') == 'error' for message in messages)
            for name in names:
                exact = re.compile('^' + re.escape(name) + r'(?:\.\{[^}]*\})?(?=\s|:|$)')
                signatures = [message['data'] for message in messages if exact.search(message.get('data', ''))]
                axioms = [message['data'] for message in messages if message.get('data', '').startswith("'" + name + "' ")]
                assert len(signatures) == len(axioms) == 1
                if 'does not depend on any axioms' not in axioms[0]:
                    body = re.search(r'depends on axioms: \[(.*?)\]', axioms[0], re.S)
                    assert body
                    actual = {re.sub(r'\.\{[^}]*\}$', '', item.strip()) for item in body[1].split(',')}
                    assert actual <= {'propext', 'Classical.choice', 'Quot.sound'}
        (ROOT / logs[index]).write_text(text, encoding='utf-8')
        rows.append({'command': command, 'returncode': run.returncode,
                     'seconds': time.perf_counter() - started, 'log': logs[index],
                     'log_sha256': sha(ROOT / logs[index]),
                     'stdin_sha256': hashlib.sha256(stdin.encode()).hexdigest() if stdin else None})
        print(json.dumps(rows[-1]), flush=True)
        if run.returncode:
            break
    unchanged = all(sha(path) == digest for path, digest in pins.items())
    passed = len(rows) == 3 and all(row['returncode'] == 0 for row in rows) and unchanged
    result = {'passed': passed, 'module': candidate['module'],
              'candidate_binding_sha256': candidate['binding_sha256'],
              'reviewer_receipt': receipt_path, 'reviewer_receipt_sha256': sha(ROOT / receipt_path),
              'source_first_seal_sha256': sha(ROOT / REVIEW / 'source-first-seal.json'),
              'whole_source_fresh': True, 'target_cache_imported': False,
              'production_cache_outputs_requested_by_focused_check': False,
              'actual_exact_signature_and_ordinary_axiom_reports': 30,
              'independent_v7_consumers_replayed': True, 'eight_counter_consumers_replayed': True,
              'resolved_input_provider_native_and_private_pin_count': len(pins),
              'bound_input_provider_native_and_private_pins_unchanged': unchanged,
              'execution': rows,
              'cache_provenance': 'Normal pinned inherited provider/native layout, not a clean transitive source rebuild; local Verso edits disclosed by actual logs',
              'scientific_ROOT': False, 'main_admission': False, 'PURIFIED': False,
              'mechanical_publication_record': 'PENDING exact distinct reviewer wrapper and current inventory validation'}
    (ROOT / OUTPUT).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': passed, 'receipt': OUTPUT, 'sha256': sha(ROOT / OUTPUT)}), flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
