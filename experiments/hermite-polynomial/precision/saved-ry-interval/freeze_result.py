"""Build exact internal provider/consumer and record reproducible bounded evidence."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CACHE = ROOT / '.lake' / 'saved-ry-interval-cache'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env['LEAN_PATH'] = os.pathsep.join((str(CACHE), str(ROOT / '.lake' / 'finite-trig-cache'), env.get('LEAN_PATH', '')))
    bound_paths = sorted(p for p in HERE.iterdir() if p.suffix in ('.lean', '.py', '.ps1', '.md') or p.name.endswith('seal-v1.json'))
    dependencies = [
        ROOT / 'lean-toolchain', ROOT / 'lake-manifest.json',
        ROOT / 'QuantumBlockEncoding' / 'PrimitiveSemantics.lean',
        ROOT / 'QuantumBlockEncoding' / 'PrimitiveRyPerturbation.lean',
        ROOT / 'QuantumBlockEncoding' / 'PrimitiveBasisLE.lean',
        HERE.parent / 'finite-trig' / 'FiniteTrig.lean',
        HERE.parent / 'finite-trig' / 'finite_trig.py',
        HERE.parent / 'saved-action' / 'saved_action.py',
        HERE.parent / 'saved-action' / 'result-v1.json',
        HERE.parent / 'saved-action' / 'fixture-n3-k1-L1' / 'saved.qasm',
        HERE.parent / 'saved-action' / 'fixture-n3-k1-L1' / 'manifest.json',
    ]
    before = {str(p.relative_to(ROOT)).replace('\\', '/'): digest(p) for p in bound_paths + dependencies}
    rel_here = HERE.relative_to(ROOT).as_posix()
    commands = [
        ['lake', 'env', 'lean', '-o', '.lake/saved-ry-interval-cache/SavedRyInterval.olean', f'{rel_here}/SavedRyInterval.lean'],
        ['lake', 'env', 'lean', f'{rel_here}/ConsumerChecks.lean'],
        ['.venv/Scripts/python.exe', f'{rel_here}/test_saved_ry_interval.py', '-v'],
    ]
    execution = []
    for i, cmd in enumerate(commands):
        start = time.perf_counter()
        done = subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True, timeout=300)
        log = HERE / f'gate-v2-{i + 1}.log'
        captured = done.stdout + '\n' + done.stderr
        for prefix in (str(ROOT), ROOT.as_posix(), str(ROOT).replace('\\', '/'), str(ROOT).replace('/', '\\')):
            captured = captured.replace(prefix, '<repo>')
        # Other ambient toolchain paths, if any, are private too.
        import re
        captured = re.sub(r'[A-Za-z]:[\\/][^\r\n\"\']*', '<private-runtime-path>', captured)
        log.write_text(captured, encoding='utf-8')
        execution.append({'command': cmd, 'exit_code': done.returncode, 'measured_seconds': time.perf_counter() - start,
                          'log': str(log.relative_to(ROOT)).replace('\\', '/'), 'log_sha256': digest(log)})
        print(f'gate {i + 1}: exit {done.returncode}', flush=True)
        if done.returncode:
            print(captured, flush=True)
            break
    stable = all(digest(ROOT / name) == value for name, value in before.items())
    consumer_log = (HERE / 'gate-v2-2.log').read_text('utf-8') if (HERE / 'gate-v2-2.log').exists() else ''
    clean = 'sorryAx' not in consumer_log and 'Lean.ofReduceBool' not in consumer_log
    passed = len(execution) == 3 and all(x['exit_code'] == 0 for x in execution) and stable and clean
    result = {
        'schema_version': 2, 'evidence_class': 'C_INTERNAL_PROVIDER',
        'safe_successor_chronology': 'Unpublished v1 result/logs completed before privacy correction; retained only in ignored local .private/run-v1. Version2 reruns corrected relative commands and sanitizes logs; no prior frozen source packet changed.',
        'status': 'PROVED_LOCAL_FOCUSED' if passed else 'NOT_ACCEPTED',
        'head_readonly': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'toolchain': (ROOT / 'lean-toolchain').read_text().strip(),
        'mathematical_delta': 'Literal rational half-angle Taylor RY midpoint entries, 2delta Euclidean operator bound, arbitrary named spectator lift, CLM and vector bound; no desired operator bound assumed.',
        'proof_mechanism': 'Error = cosine_error*RY(0) + sine_error*RY(pi); actual signed matrices and lifted matrices, fixed unitary norms, triangle bound; unconditional FiniteTrig Taylor supplier.',
        'roots': ['entry_error', 'difference_decomposition', 'local_operator_error', 'lifted_operator_error', 'lifted_clm_error', 'lifted_vector_error', 'lifted_entry_error'],
        'cx_classification': 'Existing exact cxBasisAction reused in kernel basis discriminator; not a new CX semantic bridge or independent mathematical advance. Tautological cx_error_zero helper removed.',
        'namespace': 'HermiteSavedRyInterval',
        'kernel_discriminators': ['zero_angle forall n', 'signed_half_angle', 'physical_wire_discriminators q0/q1/q2', 'spectator_discriminator', 'cx_basis_discriminator'],
        'actual_saved_consumer': 'Exact rational first ASCII decimal -0.86958955523179937, theorem instantiated at saved default Taylor degree 96.',
        'axioms': {'consumer_prints_checked': clean, 'expected': ['propext', 'Classical.choice', 'Quot.sound'], 'new_axioms': False, 'new_native_decide': False},
        'execution': execution, 'bindings_sha256': before, 'bound_inputs_unchanged_during_gate': stable,
        'failure_class': 'NONE' if passed else 'IMPLEMENTATION_FAILED',
        'authoring_obstructions': ['IMPLEMENTATION_FAILED: Complex.cast simp normalization; fixed using literal typed real-cast differences.', 'IMPLEMENTATION_FAILED: Fin numeral contextual discriminator simplification; fixed with kernel cases. No mathematical refutation.'],
        'still_open': ['Python-to-Lean decoder/parser refinement', 'actual outward interval arithmetic and its rounded primitive midpoint', 'saved stage midpoint after ordered gate chronology', 'whole saved-plan full-tensor/readout refinement', 'uniform Hermite family', 'finite-bit and operation costs'],
        'phase_quotient': False, 'surrogate_unitarity_assumed': False,
        'source_anchor_admission': False, 'scientific_root_closed': False, 'independent_review': 'NOT_PERFORMED',
        'purification': 'Internal helpers serve compiled roots/consumer; no public PURIFIED or exposition seal claim',
        'full_repository_gate': 'Parent-owned integration obligation; not run by worker',
        'worker_git_mutations': False, 'parent_owns_checkpoint_push': True,
        'per_worker_tokens': 'unknown'
    }
    (HERE / 'result-v2.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
