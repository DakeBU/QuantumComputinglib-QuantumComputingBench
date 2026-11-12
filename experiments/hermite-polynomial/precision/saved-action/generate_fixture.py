"""Actual OffsetSource -> SAME certified D -> ONE frozen plan saved fixture."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import time
from unittest import mock

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from saved_action import CAPS, core_record, FILES
sys.path.insert(0, str(HERE.parent / 'offset-source'))
from offset_source import offset_hermite_tt
from qr_residual import certify_scaled_canonicalize
from mps_core_probe import TT
import mps_ry_compiler as compiler


def json_bytes(value):
    return (json.dumps(value, indent=2, allow_nan=False) + '\n').encode('utf-8')


def verify_frozen_inputs():
    design = HERE.parent / 'next-circuit-frontier-design.json'
    if hashlib.sha256(design.read_bytes()).hexdigest() != '664809e1fd69c2918e4575087a630fbb1589069715cb74cd94659ccd42b7be1c':
        raise ValueError('frozen design changed')
    root = HERE.parents[3]
    for row in json.loads(design.read_bytes())['bindings']:
        if hashlib.sha256((root / row['path']).read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('frozen input digest changed')


def generate(directory, n=3, k=1, length=Fraction(1)):
    if not 1 <= n <= CAPS['n_max'] or not 0 <= k <= CAPS['k_max']:
        raise ValueError('fixture cap')
    verify_frozen_inputs()
    if directory.exists() and any(directory.iterdir()):
        raise ValueError('refuse overwriting fixture')
    directory.mkdir(parents=True, exist_ok=True)
    calls, trace, durations = {}, [], {}
    original_qr = np.linalg.qr
    def observed_qr(array, *args, **kwargs):
        calls['numpy_qr'] = calls.get('numpy_qr', 0) + 1
        result = original_qr(array, *args, **kwargs)
        trace.append({'operation': 'numpy_qr', 'shape': list(array.shape), 'mode': kwargs.get('mode', 'reduced'),
                      'input_sha256': hashlib.sha256(array.tobytes()).hexdigest(),
                      'output_shapes': [list(x.shape) for x in result]})
        return result
    original_canonical = compiler.right_canonicalize
    def observed_canonical(tt):
        calls['compiler_repeated_right_canonicalize'] = calls.get('compiler_repeated_right_canonicalize', 0) + 1
        returned = original_canonical(tt)
        trace.append({'operation': 'compiler_repeated_right_canonicalize',
                      'output_cores': core_record(returned[0]), 'head_float_norm_hex': float(returned[1]).hex()})
        return returned
    original_complete = compiler.complete_isometry
    def observed_complete(core, bond):
        calls['complete_isometry'] = calls.get('complete_isometry', 0) + 1
        returned = original_complete(core, bond)
        trace.append({'operation': 'complete_isometry', 'input_shape': list(core.shape),
                      'output_shape': list(returned.shape),
                      'output_sha256': hashlib.sha256(returned.tobytes()).hexdigest()})
        return returned
    original_atan2 = compiler.math.atan2
    def observed_atan2(y, x):
        calls['atan2'] = calls.get('atan2', 0) + 1
        return original_atan2(y, x)
    with mock.patch.object(TT, 'small_dense_diagnostic', side_effect=AssertionError('dense constructor/checker forbidden')), \
         mock.patch.object(np.linalg, 'qr', side_effect=observed_qr), \
         mock.patch.object(compiler, 'right_canonicalize', side_effect=observed_canonical), \
         mock.patch.object(compiler, 'complete_isometry', side_effect=observed_complete), \
         mock.patch.object(compiler.math, 'atan2', side_effect=observed_atan2):
        start = time.perf_counter()
        raw, source_metadata = offset_hermite_tt(n, k, length)
        durations['offset_source_seconds'] = time.perf_counter()-start
        raw_bytes = json_bytes(core_record(raw))
        start = time.perf_counter()
        returned, normalizer, qr_packet = certify_scaled_canonicalize(raw)
        durations['certified_scaled_return_seconds'] = time.perf_counter()-start
        returned_bytes = json_bytes(core_record(returned))
        if raw.max_bond > CAPS['bond_max'] or returned.max_bond > CAPS['bond_max']:
            raise ValueError('actual core bond cap')
        start = time.perf_counter()
        plan = compiler.compile_mps(returned)
        durations['compile_seconds'] = time.perf_counter()-start
        # Capture the SAME plan's actual iterator; writer regenerates that iterator.
        gates = list(plan.gates())
        if len(gates) > CAPS['saved_primitives_max']:
            raise ValueError('actual saved primitive cap')
        plan.write_qasm2(directory / 'saved.qasm')
        if json_bytes(core_record(returned)) != returned_bytes or json_bytes(core_record(raw)) != raw_bytes:
            raise AssertionError('frozen compile mutated C/D')
    spans, start = [], 0
    for i, planes in enumerate(plan.planes):
        count = sum(sum(1 for _ in compiler.expand_edge_rotation(plan.ancillas+1, first, second, angle)) for first, second, angle in planes)
        spans.append({'start': start, 'count': count, 'data_wire': n-1-i})
        start += count
    if start != len(gates):
        raise AssertionError('actual plan chronology count')
    manifest = {'schema_version': 1, 'n': n, 'ancillas': plan.ancillas, 'k': k, 'L': str(length),
                'qasm_sha256': hashlib.sha256((directory / 'saved.qasm').read_bytes()).hexdigest(),
                'raw_sha256': hashlib.sha256(raw_bytes).hexdigest(),
                'returned_sha256': hashlib.sha256(returned_bytes).hexdigest(),
                'stage_spans': spans,
                'gates': [[g[0], g[1].hex(), g[2]] if g[0] == 'ry' else list(g) for g in gates],
                'active_bonds_diagnostic_only': plan.active_bonds,
                'full_terminal_B': 1 << plan.ancillas,
                'resource_counts': plan.resource_counts,
                'primary_angle_semantics': 'literal saved decimal', 'actual_plan_binary64_reference_only': True}
    producer = {'schema_version': 1, 'same_returned_object_compiler_input': True,
                'compile_mps_calls': 1, 'certified_scaled_return_calls': 1,
                'source_producer': 'frozen OffsetSource', 'canonicalizer': 'frozen certify_scaled_canonicalize',
                'source_metadata': source_metadata, 'qr_residual_packet': qr_packet,
                'normalizer': {'mantissa_hex': normalizer.mantissa.hex(), 'exponent': normalizer.exponent},
                'observed_calls': calls, 'compiler_trace_diagnostic_only': trace,
                'C_D_unchanged_by_compiler_byte_check': True,
                'dense_constructor_forbidden': True, 'numpy_version': np.__version__,
                'frozen_backend_operations': 'QR/rescale/absorb/norm/copy; repeated prune/QR/norm; completion QR/determinant; hypot/atan2/Gray expansion. Call/shape counts retained; integer/BLAS runtime not proved.',
                'formal_refinement': False, 'scientific_root_closed': False}
    outputs = {'raw.json': raw_bytes, 'returned.json': returned_bytes,
               'manifest.json': json_bytes(manifest), 'producer.json': json_bytes(producer)}
    for name, payload in outputs.items():
        (directory / name).write_bytes(payload)
    inventory = {'schema_version': 1, 'sha256': {name: hashlib.sha256((directory/name).read_bytes()).hexdigest() for name in sorted(FILES-{'inventory.json'})}}
    (directory / 'inventory.json').write_bytes(json_bytes(inventory))
    return {'status': 'ACTUAL_SAME_RETURN_ONE_PLAN_FIXTURE_GENERATED', 'durations': durations,
            'instructions': len(gates), 'n': n, 'k': k, 'L': str(length),
            'fixture_sha256': {name: hashlib.sha256((directory/name).read_bytes()).hexdigest() for name in sorted(FILES)},
            'scientific_root_closed': False}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(generate(args.directory), indent=2))
    except (OSError, ValueError, ArithmeticError) as error:
        print(json.dumps({'status': 'FAIL_CLOSED', 'reason_class': type(error).__name__, 'scientific_root_closed': False}))
        raise SystemExit(1)
