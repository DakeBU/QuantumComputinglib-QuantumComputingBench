"""Compact FULL saved-decimal action diagnostic; no scientific acceptance.

The mathematical Taylor supplier is separate from this Python interpreter.
Every terminal bond sector is retained. No target renormalization is performed.
"""
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import re
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
PRECISION = HERE.parent
sys.path.insert(0, str(PRECISION / "qr-residual"))
from qr_residual import Work, cross_gram, sqrt_upper, stored_cores, rational_text

CAPS = json.loads((HERE / "statement-seal-v1.json").read_text())['caps']
FILES = {"saved.qasm", "manifest.json", "raw.json", "returned.json", "producer.json", "inventory.json"}
NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
RY = re.compile(rf"ry\(({NUMBER})\) q\[(\d+)\];")
CX = re.compile(r"cx q\[(\d+)\],q\[(\d+)\];")


class LimitReached(ValueError):
    pass


class MeasuredWork(Work):
    def __init__(self):
        super().__init__()
        self.interval_row_output_entries = 0
        self.row_permutation_cell_copies = 0
        self.dyadic_outward_roundings = 0
        self.taylor_terms = 0
        self.taylor_cache_hits = 0
        self.taylor_unique_angles = 0
        self.rational_endpoint_comparisons = 0
        self.chain_scalar_copies = 0
        self.json_bytes_decoded = 0
        self.qasm_bytes_decoded = 0
        self.angle_decimal_decodes = 0
        self.float_hex_decodes = 0
        self.rational_chain_validation_cells = 0
        self.primitive_steps = 0
        self.peak_local_matrix_entries = 0
        self.dyadic_round_integer_operand_bits_max = 0
        self.integer_floor_ceil_operations = 0
        self.integer_grid_shifts = 0

    def note(self, value):
        if max(abs(value.numerator).bit_length(), value.denominator.bit_length()) > CAPS['rational_operand_bits_max']:
            raise LimitReached("rational operand cap")
        return super().note(value)


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F

    def __post_init__(self):
        if type(self.lo) is not F or type(self.hi) is not F or self.lo > self.hi:
            raise ValueError("ordered Fraction endpoints required")


def plus(a, b, w):
    return Interval(w.add(a.lo, b.lo), w.add(a.hi, b.hi))


def negative(a):
    return Interval(-a.hi, -a.lo)


def times(a, b, w):
    products = [w.mul(x, y) for x in (a.lo, a.hi) for y in (b.lo, b.hi)]
    w.rational_endpoint_comparisons += 6
    return Interval(min(products), max(products))


def outward(a, w, bits=80):
    grid = 1 << bits
    w.integer_grid_shifts += 1
    lo_n = a.lo.numerator * grid
    hi_n = a.hi.numerator * grid
    w.dyadic_round_integer_operand_bits_max = max(w.dyadic_round_integer_operand_bits_max,
        abs(lo_n).bit_length(), abs(hi_n).bit_length(), a.lo.denominator.bit_length(), a.hi.denominator.bit_length())
    w.integer_floor_ceil_operations += 2
    lo = w.note(F(lo_n // a.lo.denominator, grid))
    hi = w.note(F(-((-hi_n) // a.hi.denominator), grid))
    w.dyadic_outward_roundings += 2
    return Interval(lo, hi)


def finite_trig(x, w, degree=96, bits=80):
    """Explicit rational Taylor + Lagrange radius; no math.sin/cos used.

    Soundness in real mathematics is supplied separately by HermiteFiniteTrig;
    this loop/refinement is not a checked Lean program.
    """
    if type(x) is not F or abs(x) > CAPS['half_angle_abs_max']:
        raise LimitReached("half-angle cap")
    if type(degree) is not int or not 0 <= degree <= CAPS['taylor_degree_max']:
        raise LimitReached("Taylor degree cap")
    if type(bits) is not int or not 0 <= bits <= CAPS['interval_grid_bits']:
        raise LimitReached("interval grid cap")
    term, sine, cosine = F(1), F(), F()
    for i in range(degree + 1):
        if i % 4 == 1:
            sine = w.add(sine, term)
        elif i % 4 == 3:
            sine = w.add(sine, -term)
        elif i % 4 == 0:
            cosine = w.add(cosine, term)
        else:
            cosine = w.add(cosine, -term)
        term = w.div(w.mul(term, x), F(i + 1))
        w.taylor_terms += 1
    radius = abs(term)
    sin_raw = Interval(w.add(sine, -radius), w.add(sine, radius))
    cos_raw = Interval(w.add(cosine, -radius), w.add(cosine, radius))
    return outward(sin_raw, w, bits), outward(cos_raw, w, bits), radius


def core_record(tt):
    rows = []
    for c in tt.cores:
        if c.dtype != np.dtype('float64') or not np.all(np.isfinite(c)):
            raise ValueError("finite actual float64 cores required")
        rows.append({'shape': list(c.shape), 'values': [float(v).hex() for v in c.flat],
                     'bytes_sha256': hashlib.sha256(c.tobytes(order='C')).hexdigest()})
    return {'schema_version': 1, 'cores': rows}


def decode_tt(record, w):
    from mps_core_probe import TT
    if record.get('schema_version') != 1 or not isinstance(record.get('cores'), list):
        raise ValueError("core record schema")
    if not 1 <= len(record['cores']) <= CAPS['n_max']:
        raise LimitReached("core sites cap")
    cores = []
    for row in record['cores']:
        shape = row.get('shape')
        if (not isinstance(shape, list) or len(shape) != 3 or shape[1] != 2
                or any(type(x) is not int or not 1 <= x <= CAPS['bond_max'] for x in (shape[0], shape[2]))):
            raise ValueError("binary positive core shape required")
        values = row.get('values')
        if not isinstance(values, list) or len(values) != math.prod(shape):
            raise ValueError("core scalar count")
        decoded = []
        for token in values:
            if not isinstance(token, str) or len(token) > 32:
                raise ValueError("float hex token cap")
            value = float.fromhex(token)
            if not math.isfinite(value) or value.hex() != token:
                raise ValueError("canonical finite float hex required")
            decoded.append(value)
            w.float_hex_decodes += 1
        core = np.array(decoded, dtype=np.float64).reshape(shape)
        if hashlib.sha256(core.tobytes(order='C')).hexdigest() != row.get('bytes_sha256'):
            raise ValueError("stored core byte hash")
        cores.append(core)
    return TT(cores)


def validate_chain(chain, w):
    if not isinstance(chain, list) or not chain:
        raise ValueError("nonempty rational chain")
    if len(chain) > CAPS['n_max'] + 4:
        raise LimitReached("rational chain site cap")
    previous = 1
    for core in chain:
        if not isinstance(core, list) or len(core) != previous or not core:
            raise ValueError("rational chain left bond")
        right = None
        for row in core:
            if not isinstance(row, list) or len(row) != 2:
                raise ValueError("binary physical dimension")
            for slab in row:
                if not isinstance(slab, list) or not slab:
                    raise ValueError("nonempty right bond")
                if right is None:
                    right = len(slab)
                if len(slab) != right:
                    raise ValueError("ragged rational core")
                for value in slab:
                    if type(value) is not F:
                        raise TypeError("exact Fraction chain required")
                    w.note(value)
                    w.rational_chain_validation_cells += 1
        if right > CAPS['bond_max']:
            raise LimitReached("chain bond cap")
        previous = right
    if previous != 1:
        raise ValueError("scalar terminal boundary required")


def terminal_readout(a):
    """Emit MSB first, carry low remainder; every B terminal label survives."""
    tail = []
    for width in range(a, 0, -1):
        incoming, following = 1 << width, 1 << (width - 1)
        core = [[[F() for _ in range(following)] for _ in range(2)] for _ in range(incoming)]
        for label in range(incoming):
            core[label][label // following][label % following] = F(1)
        tail.append(core)
    return tail


def action_chain(centers, a, w):
    B = 1 << a
    chain = []
    for i, matrix in enumerate(centers):
        if len(matrix) != 2 * B or any(len(row) != 2 * B for row in matrix):
            raise ValueError("stage matrix shape")
        incoming = [0] if i == 0 else range(B)
        core = [[[matrix[bit * B + out][inc] for out in range(B)] for bit in range(2)] for inc in incoming]
        w.chain_scalar_copies += len(core) * 2 * B
        chain.append(core)
    chain += terminal_readout(a)
    validate_chain(chain, w)
    return chain


def literal_embedding(returned, a, w):
    chain = stored_cores(returned, w)
    chain += [[[[F(1)], [F()]]]] * a
    validate_chain(chain, w)
    return chain


def literal_residual(qchain, dchain, w, bits=80):
    if type(bits) is not int or not 0 <= bits <= CAPS['certificate_sqrt_bits']:
        raise LimitReached("directed sqrt grid cap")
    validate_chain(qchain, w)
    validate_chain(dchain, w)
    if len(qchain) != len(dchain):
        raise ValueError("same physical site count")
    before_add, before_mul = w.rational_additions, w.rational_multiplications
    gq, gd, cross = cross_gram(qchain, qchain, w), cross_gram(dchain, dchain, w), cross_gram(qchain, dchain, w)
    adds, muls = w.rational_additions - before_add, w.rational_multiplications - before_mul
    M = max(len(slab) for chain in (qchain, dchain) for core in chain for row in core for slab in row)
    budget = 27 * len(qchain) * M**3
    if adds + muls > budget:
        raise AssertionError("contraction cubic schedule budget")
    q = w.add(w.add(gq, gd), -w.mul(F(2), cross))
    if q < 0:
        raise AssertionError("negative literal squared residual")
    r, sqrt_work = sqrt_upper(q, bits, w)
    return {'action_gram': rational_text(gq), 'literal_D_gram': rational_text(gd),
            'cross_gram': rational_text(cross), 'residual_squared': rational_text(q),
            'residual_upper': rational_text(r), 'sqrt_work': sqrt_work,
            'contraction_additions': adds, 'contraction_multiplications': muls,
            'contraction_field_budget': budget, 'target_renormalized': False}


def decimal_angle(token, w):
    if len(token) > CAPS['angle_token_chars_max']:
        raise LimitReached("angle token cap")
    d = Decimal(token)
    if not d.is_finite() or abs(d.as_tuple().exponent) > CAPS['decimal_exponent_abs_max']:
        raise LimitReached("decimal exponent cap")
    w.angle_decimal_decodes += 1
    return w.note(F(d))


def parse_saved(qasm, manifest, w):
    if not isinstance(manifest, dict) or type(manifest.get('schema_version')) is not int or manifest['schema_version'] != 1:
        raise ValueError("saved manifest schema")
    n, a = manifest.get('n'), manifest.get('ancillas')
    if type(n) is not int or not 1 <= n <= CAPS['n_max'] or type(a) is not int or not 0 <= a <= 4:
        raise LimitReached("saved dimension cap")
    if 1 << a > CAPS['bond_max']:
        raise LimitReached("saved bond cap")
    if len(qasm) > CAPS['input_bytes_max']:
        raise LimitReached("QASM byte cap")
    if hashlib.sha256(qasm).hexdigest() != manifest.get('qasm_sha256'):
        raise ValueError("saved QASM byte binding")
    lines = qasm.decode('ascii').splitlines()
    if lines[:3] != ['OPENQASM 2.0;', 'include "qelib1.inc";', f'qreg q[{n+a}];']:
        raise ValueError("literal saved header")
    rows = manifest.get('gates')
    if not isinstance(rows, list) or len(rows) > CAPS['saved_primitives_max']:
        raise LimitReached("primitive list cap")
    if len(lines) - 3 != len(rows):
        raise ValueError("missing/extra saved instruction")
    gates, transport, parser_transport = [], F(), F()
    for line, ref in zip(lines[3:], rows):
        if not isinstance(ref, list) or len(ref) != 3:
            raise ValueError("manifest primitive schema")
        ry, cx = RY.fullmatch(line), CX.fullmatch(line)
        if ry:
            angle, target = decimal_angle(ry[1], w), int(ry[2])
            if ref[0] != 'ry' or not isinstance(ref[1], str) or len(ref[1]) > 32:
                raise ValueError("RY reference schema")
            binary = float.fromhex(ref[1])
            if not math.isfinite(binary) or binary.hex() != ref[1] or f'{binary:.17g}' != ry[1] or target != ref[2]:
                raise ValueError("actual plan angle/wire transport changed")
            w.float_hex_decodes += 1
            transport = w.add(transport, abs(w.add(angle, -F.from_float(binary))))
            parser_transport = w.add(parser_transport, abs(w.add(angle, -F.from_float(float(ry[1])))))
            gate = ('ry', angle, target)
        elif cx:
            gate = ('cx', int(cx[1]), int(cx[2]))
            if list(gate) != ref or gate[1] == gate[2]:
                raise ValueError("actual plan CX transport changed")
        else:
            raise ValueError("unsupported saved primitive")
        wires = [gate[2]] if gate[0] == 'ry' else [gate[1], gate[2]]
        if any(type(wire) is not int or not 0 <= wire < n+a for wire in wires):
            raise ValueError("physical wire range")
        gates.append(gate)
    spans = manifest.get('stage_spans')
    if not isinstance(spans, list) or len(spans) != n:
        raise ValueError("one span for every data stage")
    start = 0
    for i, span in enumerate(spans):
        if (not isinstance(span, dict) or type(span.get('start')) is not int
                or type(span.get('count')) is not int or span['start'] != start
                or span['count'] < 0 or span.get('data_wire') != n-1-i):
            raise ValueError("chronological stage partition")
        end = start + span['count']
        if end > len(gates):
            raise ValueError("span outside saved stream")
        allowed = set(range(n, n+a)) | {n-1-i}
        for gate in gates[start:end]:
            wires = [gate[2]] if gate[0] == 'ry' else [gate[1], gate[2]]
            if not set(wires) <= allowed:
                raise ValueError("cross-stage/reused-data wire")
        start = end
    if start != len(gates):
        raise ValueError("incomplete stage partition")
    w.qasm_bytes_decoded += len(qasm)
    return gates, {'decimal_vs_original_binary64_RY_bound': rational_text(transport/2),
                   'decimal_vs_parser_binary64_RY_bound': rational_text(parser_transport/2),
                   'primary_semantics': 'exact textual rational decimals',
                   'parser_semantics': 'separate actual Qiskit/binary64 diagnostic'}


def stage_surrogates(gates, manifest, w):
    n, a = manifest['n'], manifest['ancillas']
    B, centers, reports, cache = 1 << a, [], [], {}
    size = 2 * B
    zero, one = Interval(F(), F()), Interval(F(1), F(1))
    for offset, span in enumerate(manifest['stage_spans']):
        matrix = [[one if i == j else zero for j in range(size)] for i in range(size)]
        w.peak_local_matrix_entries = max(w.peak_local_matrix_entries, size*size)
        wires = {n + i: i for i in range(a)}
        wires[n-1-offset] = a
        max_radius = F()
        for gate in gates[span['start']:span['start']+span['count']]:
            w.primitive_steps += 1
            if gate[0] == 'cx':
                control, target = wires[gate[1]], wires[gate[2]]
                matrix = [matrix[i ^ (1 << target)] if (i >> control) & 1 else matrix[i] for i in range(size)]
                w.row_permutation_cell_copies += size*size
            elif gate[0] == 'ry':
                x, target = w.div(gate[1], F(2)), wires[gate[2]]
                if x not in cache:
                    cache[x] = finite_trig(x, w)
                    w.taylor_unique_angles += 1
                else:
                    w.taylor_cache_hits += 1
                sine, cosine, radius = cache[x]
                max_radius = max(max_radius, radius)
                mask = 1 << target
                for first in range(size):
                    if first & mask:
                        continue
                    second = first | mask
                    row0, row1 = matrix[first], matrix[second]
                    matrix[first] = [outward(plus(times(cosine, u, w), negative(times(sine, v, w)), w), w) for u, v in zip(row0, row1)]
                    matrix[second] = [outward(plus(times(sine, u, w), times(cosine, v, w), w), w) for u, v in zip(row0, row1)]
                    w.interval_row_output_entries += 2*size
            else:
                raise ValueError("unsupported primitive")
        center = [[w.div(w.add(x.lo, x.hi), F(2)) for x in row] for row in matrix]
        delta = max(w.div(w.add(x.hi, -x.lo), F(2)) for row in matrix for x in row)
        eta = w.mul(F(size), delta)
        reports.append({'stage': offset, 'start': span['start'], 'count': span['count'],
                        'entry_radius': rational_text(delta), 'eta': rational_text(eta),
                        'maximum_Taylor_remainder': rational_text(max_radius),
                        'surrogate_unitarity_assumed': False})
        centers.append(center)
    product = F(1)
    for report in reports:
        product = w.mul(product, w.add(F(1), F(report['eta'])))
    return centers, reports, w.add(product, F(-1))


def encode_chain(chain):
    return [[[[rational_text(x) for x in slab] for slab in row] for row in core] for core in chain]


def load_fixture(directory, w):
    actual = {p.name for p in directory.iterdir()}
    if actual != FILES or any(not (directory / name).is_file() for name in FILES):
        raise ValueError("missing/extra fixture files")
    data = {}
    for name in FILES:
        p = directory / name
        if p.stat().st_size > CAPS['input_bytes_max']:
            raise LimitReached("fixture file bytes cap")
        data[name] = p.read_bytes()
    inventory = json.loads(data['inventory.json'])
    hashes = inventory.get('sha256')
    if not isinstance(hashes, dict) or set(hashes) != FILES - {'inventory.json'}:
        raise ValueError("fixture inventory schema")
    for name, expected in hashes.items():
        if hashlib.sha256(data[name]).hexdigest() != expected:
            raise ValueError("fixture byte hash mismatch")
    parsed = {name: json.loads(raw) for name, raw in data.items() if name.endswith('.json')}
    w.json_bytes_decoded = sum(len(raw) for name, raw in data.items() if name.endswith('.json'))
    return data, parsed


def audit_fixture(directory):
    w = MeasuredWork()
    data, parsed = load_fixture(directory, w)
    manifest = parsed['manifest.json']
    gates, transport = parse_saved(data['saved.qasm'], manifest, w)
    returned = decode_tt(parsed['returned.json'], w)
    if returned.n != manifest['n'] or manifest.get('returned_sha256') != hashlib.sha256(data['returned.json']).hexdigest():
        raise ValueError("same returned D binding")
    if manifest.get('raw_sha256') != hashlib.sha256(data['raw.json']).hexdigest():
        raise ValueError("same stored C binding")
    producer = parsed['producer.json']
    if not producer.get('same_returned_object_compiler_input') or producer.get('compile_mps_calls') != 1 or producer.get('certified_scaled_return_calls') != 1:
        raise ValueError("same-return/one-plan provenance")
    centers, stages, sigma = stage_surrogates(gates, manifest, w)
    qchain = action_chain(centers, manifest['ancillas'], w)
    dchain = literal_embedding(returned, manifest['ancillas'], w)
    residual = literal_residual(qchain, dchain, w)
    r = F(residual['residual_upper'])
    result = {'status': 'FINITE_FULL_SAVED_ACTION_RESIDUAL_CANDIDATE',
              'n': manifest['n'], 'ancillas': manifest['ancillas'], 'B': 1 << manifest['ancillas'],
              'instructions': len(gates), 'stages': stages, 'transport': transport,
              'full_terminal_bond_labels': 1 << manifest['ancillas'],
              'readout_sites': manifest['ancillas'], 'physical_sites': len(qchain),
              'coordinate_map': 'data-first TT word -> physical j+2^n*b',
              'sigma_product_bound': rational_text(sigma), 'literal_residual': residual,
              'saved_decimal_to_literal_D_bound_candidate': rational_text(w.add(sigma, r)),
              'candidate_bound_float_diagnostic': float(sigma + r),
              'fixture_sha256': {name: hashlib.sha256(raw).hexdigest() for name, raw in sorted(data.items())},
              'rational_action_chain': encode_chain(qchain), 'rational_literal_D_chain': encode_chain(dchain),
              'work': {**vars(w), 'Fraction_GCD_internal_trace': 'NOT instrumented; field operation counts and conservative pre-GCD bit bounds recorded, not GCD runtime',
                       'integer_shifts_floor_ceil_abs_comparisons': 'performed separately from field count',
                       'input_and_output_text_conversion': 'exact serialization; byte totals measured, conversion runtime not certified'},
              'dense_constructor_or_checker_input': False, 'target_renormalized': False,
              'every_garbage_coordinate_retained': True, 'global_phase_alignment': False,
              'formalGate': 'OPEN', 'executableRoot': 'OPEN', 'scientific_root_closed': False,
              'uniform_finite_bit_certificate': False,
              'unproved_bridges': ['Python rational Taylor/arithmetic refinement', 'saved decimal parser and RY/CX primitive refinement',
                                  'local stage to data-first TT/readout refinement', 'source-to-stored C error and source norm floor',
                                  'total finite-bit cost including NumPy QR/completion/atan2 and Fraction GCD']}
    return result, qchain, dchain


def amplitude(chain, word):
    """Tiny diagnostic only, never consumed by primary crossGram certificate."""
    row = [F(1)]
    for bit, core in zip(word, chain):
        row = [sum((row[i] * core[i][bit][j] for i in range(len(row))), F()) for j in range(len(core[0][bit]))]
    return row[0]


def physical_word(index, n, a):
    j, b = index % (1 << n), index >> n
    return [(j >> q) & 1 for q in range(n-1, -1, -1)] + [(b >> q) & 1 for q in range(a-1, -1, -1)]


def independent_saved_replay(directory, qchain, dchain):
    """Small Qiskit saved-file replay; binary64 parser, not primary semantics."""
    from qiskit import qasm2
    from qiskit.quantum_info import Statevector
    manifest = json.loads((directory / 'manifest.json').read_text())
    n, a = manifest['n'], manifest['ancillas']
    if n > 3 or n+a > 7:
        raise LimitReached("independent dense diagnostic cap")
    circuit = qasm2.load(str(directory / 'saved.qasm'))
    state = np.asarray(Statevector.from_instruction(circuit).data)
    surrogate = np.array([float(amplitude(qchain, physical_word(i, n, a))) for i in range(1 << (n+a))])
    target = np.array([float(amplitude(dchain, physical_word(i, n, a))) for i in range(1 << (n+a))])
    return {'scope': 'independent tiny saved Qiskit binary64 parser replay, diagnostic only',
            'physical_dimension': len(state), 'saved_to_literal_D_euclidean_diagnostic': float(np.linalg.norm(state-target)),
            'saved_to_surrogate_euclidean_diagnostic': float(np.linalg.norm(state-surrogate)),
            'terminal_garbage_norm_diagnostic': float(np.linalg.norm(state[1 << n:])),
            'phase_alignment': False, 'primary_checker_consumed_dense_input': False}


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('fixture', type=Path)
    args = parser.parse_args()
    try:
        result, qchain, dchain = audit_fixture(args.fixture)
        result['independent_saved_replay'] = independent_saved_replay(args.fixture, qchain, dchain)
        print(json.dumps(result, indent=2, allow_nan=False))
    except (ValueError, ArithmeticError, OSError) as error:
        print(json.dumps({'status': 'LIMIT_REACHED' if isinstance(error, LimitReached) else 'FAIL_CLOSED',
                          'reason_class': type(error).__name__, 'scientific_root_closed': False}))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
