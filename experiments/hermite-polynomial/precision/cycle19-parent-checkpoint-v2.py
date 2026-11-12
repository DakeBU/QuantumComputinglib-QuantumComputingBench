"""Versioned successor counting axiom-free declarations and printed universe suffixes.
The v1 failed validation remains immutable; all five underlying commands exited 0.
This successor reruns commands and never edits historical evidence.
No scientific ROOT or publication admission.
"""
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
SELF = PREFIX + 'cycle19-parent-checkpoint-v2.py'
OUTPUT = PREFIX + 'cycle19-parent-checkpoint-v2.json'
PRODUCER = PREFIX + 'piecewise-kernel-producer/'
REVIEW = PREFIX + 'literal-complex-review-c18/'
DECODER = 'reviews/publication/stored-tensor-train/'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def main():
    logs = [PREFIX + 'cycle19-parent-checkpoint-v2-' + str(i) + '.log' for i in range(5)]
    if any((ROOT / path).exists() for path in [OUTPUT] + logs):
        raise SystemExit('Immutable checkpoint already exists; use a new version')
    pins = {}
    references = {}

    def bind(path, expected):
        p = Path(path)
        if p.is_absolute() or ':' in path or '..' in p.parts:
            raise ValueError('Nonrelative binding')
        full = ROOT / p
        if digest(full) != expected:
            raise ValueError('Changed frozen input: ' + path)
        if full in pins and pins[full] != expected:
            raise ValueError('Conflicting binding: ' + path)
        pins[full] = expected

    def reference(path, expected):
        bind(path, expected)
        references[path] = expected

    reference(SELF, digest(ROOT / SELF))
    reference(PRODUCER + 'final-binding-manifest.json',
              '28a2e5d5b76b3c4a436ce70e9559be0b073f123c453357b4c7e8a8c6eb373ade')
    manifest = load(PRODUCER + 'final-binding-manifest.json')
    for path, sha in manifest['artifact_hashes'].items():
        bind(PRODUCER + path, sha)
    for path, sha in manifest['source_bindings'].items():
        bind(path, sha)
    for path, sha in manifest['ignored_cache_hashes'].items():
        bind(PRODUCER + path, sha)
    assert (ROOT / (PRODUCER + 'stored-object-v1.json')).is_file()
    reference(REVIEW + 'review-verdict-v1.json',
              '3231d6e11adcabb3ba8b739c362bd54f65d640cc1ef347e7b0c8b31967db8397')
    verdict = load(REVIEW + 'review-verdict-v1.json')
    for key in ['author_result', 'author_handoff', 'pre_verdict_reconstruction',
                'review_evidence', 'independent_consumer']:
        row = verdict[key]
        reference(row['path'], row['sha256'])
    for row in verdict['author_sources']:
        bind(row['path'], row['sha256'])
    evidence = load(verdict['review_evidence']['path'])
    assert evidence['final_input_count'] == len(evidence['final_input_pins_sha256']) == 17616
    for path, sha in evidence['final_input_pins_sha256'].items():
        bind(path, sha)
    for axioms in evidence['actual_axiom_roots'].values():
        assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
    for folder in [PRODUCER, REVIEW]:
        for path in sorted((ROOT / folder / '.cache').rglob('*.olean')):
            bind(path.relative_to(ROOT).as_posix(), digest(path))
    reference(DECODER + 'decoder-evidence.json',
              '3ca55e068130f105ff0e15219ea2b862aeee5d2b10ae23fad074ad18ff2dbe39')
    decoded = load(DECODER + 'decoder-evidence.json')
    reference(decoded['artifact'], decoded['artifact_sha256'])
    reference(decoded['whole_source_elaboration_receipt'],
              decoded['whole_source_elaboration_receipt_sha256'])
    receipt = load(decoded['whole_source_elaboration_receipt'])
    assert receipt['returncode'] == 0 and receipt['provider_pins_unchanged']
    assert not receipt['target_cache_used'] and not receipt['production_cache_outputs_requested']
    assert receipt['provider_pins_before'] == receipt['provider_pins_after']
    bind('QuantumBlockEncoding/StoredTensorTrain.lean', decoded['module_sha256'])
    bind(DECODER + 'decoder-packet.json', decoded['packet_sha256'])
    bind(DECODER + 'decoder-probe-c19-v3.lean', receipt['probe_sha256'])
    for row in receipt['context_files']:
        bind(row['path'], row['sha256'])
    prefix = subprocess.run(['lake', 'env', 'lean', '--print-prefix'], cwd=ROOT,
                            check=True, capture_output=True, text=True).stdout.strip().splitlines()[-1]

    def resolve(locator):
        for token, base in [('<repository>', ROOT), ('<lean-toolchain>', Path(prefix))]:
            if locator.startswith(token):
                suffix = locator[len(token):].lstrip('/\\')
                path = base / suffix
                if not path.resolve().is_relative_to(base.resolve()):
                    raise ValueError('Provider path escapes its prefix')
                return path
        raise ValueError('Unrecognized provider locator')

    for row in receipt['provider_pins_before']:
        pairs = [(row['source'], row['source_sha256'])]
        pairs += [(p['path'], p['sha256']) for p in row['artifacts']]
        for locator, sha in pairs:
            path = resolve(locator)
            if digest(path) != sha:
                raise ValueError('Changed imported provider: ' + row['module'])
            pins[path] = sha
    source = (ROOT / 'QuantumBlockEncoding/StoredTensorTrain.lean').read_text(encoding='utf-8-sig')
    names = receipt['declarations']
    assert len(names) == len(set(names)) == 30
    checks = '\nset_option pp.all true\n'
    for name in names:
        checks += '\n#check QuantumBlockEncoding.StoredTensorTrain.' + name
        checks += '\n#print axioms QuantumBlockEncoding.StoredTensorTrain.' + name + '\n'
    checks += (ROOT / (DECODER + 'decoder-probe-c19-v3.lean')).read_text(encoding='utf-8-sig')
    for op in ['field', 'sqrt', 'angle', 'trig', 'compare', 'read', 'write', 'emit']:
        checks += f'\nexample {{l m r : ℕ}} (A : QuantumBlockEncoding.StoredTensorTrain.StoredCore l m) (R : QuantumBlockEncoding.StoredGivens.StoredMatrix m r) : (QuantumBlockEncoding.StoredTensorTrain.absorption A R).cost .{op} ≤ QuantumBlockEncoding.StoredTensorTrain.absorptionBudget l m r .{op} := QuantumBlockEncoding.StoredTensorTrain.absorption_cost_le A R .{op}\n'
    commands = [
        (['lake', 'env', 'lean', PRODUCER + 'ActualDecomposition.lean'], PRODUCER + '.cache', None),
        (['lake', 'env', 'lean', REVIEW + 'ReviewConsumers.lean'], REVIEW + '.cache', None),
        (['.venv/Scripts/python.exe', '-m', 'unittest', 'discover', '-s', PRODUCER,
          '-p', 'test_producer.py', '-v'], None, None),
        (['.venv/Scripts/python.exe', '-m', 'unittest', 'discover', '-s', REVIEW,
          '-p', 'finite_checks.py', '-v'], None, None),
        (['lake', 'env', 'lean', '--stdin'], None, source + checks),
    ]
    rows, roots, forbidden = [], 0, []
    expected_roots = [3, 11, 0, 0, 30]
    for i, (command, cache, payload) in enumerate(commands):
        env = os.environ.copy()
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        if cache:
            env['LEAN_PATH'] = str(ROOT / cache)
        start = time.perf_counter()
        run = subprocess.run(command, cwd=ROOT, env=env, input=payload, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        text = run.stdout.replace(str(ROOT), '<repo>').replace(ROOT.as_posix(), '<repo>')
        text = text.replace(prefix, '<lean-toolchain>')
        text = re.sub(r'(?<![A-Za-z0-9_])[A-Za-z]:[\\/][^\r\n\'"<>]*', '<private-path>', text)
        (ROOT / logs[i]).write_text(text, encoding='utf-8')
        local = 0
        for hit in re.finditer(r'depends on axioms: \[(.*?)\]', text, re.S):
            local += 1
            forbidden.extend(x.strip() for x in [re.sub(r'\.\{[^}]*\}$', '', a.strip()) for a in hit[1].split(',')]
                             if x and x not in {'propext', 'Classical.choice', 'Quot.sound'})
        local += len(re.findall(r'does not depend on any axioms', text))
        roots += local
        okay = run.returncode == 0 and local == expected_roots[i]
        if i in [2, 3]:
            okay = okay and 'skipped' not in text.lower() and ('Ran 6 tests' if i == 2 else 'Ran 7 tests') in text
        rows.append({'command': command, 'exit_code': run.returncode, 'passed': okay,
                     'seconds': time.perf_counter() - start, 'axiom_roots': local,
                     'log': logs[i], 'log_sha256': digest(ROOT / logs[i]), 'private_cache': cache,
                     'stdin_sha256': hashlib.sha256(payload.encode()).hexdigest() if payload else None})
        print(json.dumps(rows[-1]), flush=True)
        if not okay:
            break
    unchanged = all(digest(path) == sha for path, sha in pins.items())
    passed = len(rows) == 5 and all(row['passed'] for row in rows) and unchanged and not forbidden
    out = {'schema_version': 1, 'task': 'SP-HERMITE-POLY-002', 'passed': passed,
           'supersedes_validation_only': PREFIX + 'cycle19-parent-checkpoint.json',
           'prior_failure_class': 'PARENT_PARSER_FAILED_NOT_LEAN_OR_MATHEMATICS',
           'references_sha256': references, 'resolved_binding_count': len(pins),
           'pin_maps': [PRODUCER + 'final-binding-manifest.json', verdict['review_evidence']['path'],
                        decoded['whole_source_elaboration_receipt']],
           'inputs_and_caches_unchanged': unchanged, 'execution': rows,
           'printed_axiom_roots': roots, 'unexpected_axioms': sorted(set(forbidden)),
           'finite_test_methods': 13 if passed else None,
           'cache_provenance': 'Pinned inherited repository/package/toolchain and private author/reviewer caches. Fresh parent consumer and whole StoredTensorTrain source checks, not a clean transitive repository build.',
           'literal_complex_review': 'Independent review accepted INTERNAL exact full-carrier bridge only',
           'piecewise_producer': 'Actual rational source five-component identity and finite same-stored-object diagnostics; uniform producer refinement remains open',
           'stored_tensor_train': 'Whole-module source-blind reconstruction passed; distinct source review and publication gates remain open',
           'scientific_ROOT': False, 'main_admission': False, 'public_PURIFIED': False,
           'remaining': ['uniform same-returned producer refinement', 'complex operator error transport',
                         'finite-bit QR/GCD/runtime cost', 'physical global synthesis and full terminal error',
                         'independent scientific-family executable acceptance', 'publication audit debt',
                         'clean integration and Lean 4.33 main migration']}
    (ROOT / OUTPUT).write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': passed, 'receipt': OUTPUT, 'sha256': digest(ROOT / OUTPUT)}), flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())

