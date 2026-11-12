"""Fresh reviewer diagnostics. Never feeds the primary certificate or overwrites fixtures."""
import copy
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import shutil
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
import saved_action as sa
from generate_fixture import generate
from qr_residual import read_rational, stored_cores

FIXTURE = HERE / 'fixture-n3-k1-L1'
RESULT_SHA = 'c6ec9a792ceee64d17d8a419562aea473a8f1ec8c7f9a66511cedd53349c9e6a'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bound_checks():
    result = json.loads((HERE / 'result-v1.json').read_bytes())
    assert sha(HERE / 'result-v1.json') == RESULT_SHA
    rows = result['source_bindings']
    rows += json.loads((HERE / 'provider-binding-v1.json').read_bytes())['bindings']
    rows += json.loads((HERE.parent / 'next-circuit-frontier-design.json').read_bytes())['bindings']
    for row in rows:
        assert sha(ROOT / row['path']) == row['sha256'], row['path']
    for name, digest in result['fixture_sha256'].items():
        assert sha(FIXTURE / name) == digest, name
    return len(rows), len(result['fixture_sha256'])


def own_word_value(chain, bits):
    # Explicit sum over internal bond labels; no author amplitude helper.
    dimensions = [len(core[0][0]) for core in chain[:-1]]
    value = F()
    for bond_word in itertools.product(*(range(d) for d in dimensions)):
        labels = (0,) + bond_word + (0,)
        term = F(1)
        for site, bit in enumerate(bits):
            term *= chain[site][labels[site]][bit][labels[site+1]]
        value += term
    return value


def own_gram(a, b):
    return sum((own_word_value(a, word) * own_word_value(b, word)
                for word in itertools.product((0, 1), repeat=len(a))), F())


def own_physical_word(i, n, a):
    # Extract separately from physical data and ancilla registers.
    return tuple(int(c) for c in format(i % (2**n), f'0{n}b')) + (
        tuple(int(c) for c in format(i // (2**n), f'0{a}b')) if a else ())


def own_stage(gates, n, a, offset):
    # Full dense *local* primitive matrices and generic multiplication at 90
    # decimal digits. Supporting numerical diagnostic, not an interval proof.
    size = 2**(a+1)
    with localcontext() as context:
        context.prec = 90
        zero, one = Decimal(0), Decimal(1)
        matrix = [[one if i == j else zero for j in range(size)] for i in range(size)]
        wiremap = {n+i:i for i in range(a)} | {n-1-offset:a}
        for gate in gates:
            primitive = [[zero for _ in range(size)] for _ in range(size)]
            if gate[0] == 'cx':
                c, t = wiremap[gate[1]], wiremap[gate[2]]
                for col in range(size):
                    row = col ^ (1 << t) if col & (1 << c) else col
                    primitive[row][col] = one
            else:
                x = Decimal(gate[1].numerator) / Decimal(gate[1].denominator) / 2
                # Separate literal factorial/power sums to degree 160.
                sine = sum((Decimal((-1)**j) * x**(2*j+1) / Decimal(math.factorial(2*j+1))
                            for j in range(80)), zero) if x else zero
                cosine = sum((Decimal((-1)**j) * x**(2*j) / Decimal(math.factorial(2*j))
                              for j in range(81)), zero) if x else one
                mask = 1 << wiremap[gate[2]]
                for col in range(size):
                    primitive[col][col] = cosine
                    primitive[col ^ mask][col] = -sine if col & mask else sine
            matrix = [[sum((primitive[i][k]*matrix[k][j] for k in range(size)), zero)
                       for j in range(size)] for i in range(size)]
        return [[F(value) for value in row] for row in matrix]


def exact_pair_regressions():
    rng = random.Random(731841)
    records = []
    for bonds_a, bonds_b in [([1,3,2,1],[1,2,4,1]), ([1,1],[1,1]),
                             ([1,4,1],[1,3,1]), ([1,2,2,2,1],[1,3,2,1,1])]:
        def chain(bonds):
            return [[[[F(rng.randint(-3,3), rng.randint(1,7)) for _ in range(right)]
                      for _ in range(2)] for _ in range(left)]
                    for left,right in zip(bonds[:-1],bonds[1:])]
        a, b = chain(bonds_a), chain(bonds_b)
        w = sa.MeasuredWork()
        got = sa.literal_residual(a,b,w)
        expected = own_gram(a,a) + own_gram(b,b) - 2*own_gram(a,b)
        assert read_rational(got['residual_squared']) == expected
        assert read_rational(got['residual_upper'])**2 >= expected
        assert expected >= 0
        records.append({'bonds_a':bonds_a, 'bonds_b':bonds_b, 'q_nonnegative':True,
                        'exact_word_sum_equality':True})
    return records


def rebound(directory, mode):
    manifest = json.loads((directory/'manifest.json').read_bytes())
    lines = (directory/'saved.qasm').read_text().splitlines()
    rows = manifest['gates']
    first = next(i for i,row in enumerate(rows) if row[0] == 'ry' and float.fromhex(row[1]))
    if mode in ('angle', 'sign'):
        angle = float.fromhex(rows[first][1])
        angle = angle + .25 if mode == 'angle' else -angle
        rows[first][1] = angle.hex()
        lines[3+first] = f'ry({angle:.17g}) q[{rows[first][2]}];'
    elif mode == 'reverse_stage':
        count = manifest['stage_spans'][0]['count']
        rows[:count] = reversed(rows[:count])
        lines[3:3+count] = reversed(lines[3:3+count])
    elif mode == 'terminal_excitation':
        angle = math.pi
        rows.append(['ry', angle.hex(), manifest['n']])
        lines.append(f'ry({angle:.17g}) q[{manifest["n"]}];')
        manifest['stage_spans'][-1]['count'] += 1
    data = ('\n'.join(lines)+'\n').encode('ascii')
    (directory/'saved.qasm').write_bytes(data)
    manifest['qasm_sha256'] = hashlib.sha256(data).hexdigest()
    (directory/'manifest.json').write_text(json.dumps(manifest))
    inventory = {'schema_version':1, 'sha256':{name:sha(directory/name)
                  for name in sa.FILES-{'inventory.json'}}}
    (directory/'inventory.json').write_text(json.dumps(inventory))


def run():
    report = {'binding_before':bound_checks(), 'diagnostic_only':True}
    result, qchain, dchain = sa.audit_fixture(FIXTURE)
    frozen = json.loads((HERE/'result-v1.json').read_bytes())
    assert all(result[key] == frozen[key] for key in result)
    report['all_primary_result_fields_reproduced'] = True
    manifest = json.loads((FIXTURE/'manifest.json').read_bytes())
    gates, _ = sa.parse_saved((FIXTURE/'saved.qasm').read_bytes(),manifest,sa.MeasuredWork())
    centers, stage_reports, sigma = sa.stage_surrogates(gates,manifest,sa.MeasuredWork())
    local = []
    for i, span in enumerate(manifest['stage_spans']):
        matrix = own_stage(gates[span['start']:span['start']+span['count']],3,2,i)
        delta = read_rational(stage_reports[i]['entry_radius'])
        maxerror = max(abs(matrix[r][c]-centers[i][r][c]) for r in range(8) for c in range(8))
        assert maxerror < delta
        local.append({'stage':i, 'max_center_error_decimal_diagnostic':float(maxerror),
                      'entry_radius':float(delta), 'every_entry_inside_reported_radius':True})
    report['independent_90_digit_local_full_matrix_diagnostics'] = local
    q = sum(((own_word_value(qchain,own_physical_word(i,3,2))-
              own_word_value(dchain,own_physical_word(i,3,2)))**2 for i in range(32)), F())
    assert q == read_rational(result['literal_residual']['residual_squared'])
    report['full_32_coordinate_exact_word_residual_equality'] = True
    producer = json.loads((FIXTURE/'producer.json').read_bytes())
    raw_tt = sa.decode_tt(json.loads((FIXTURE/'raw.json').read_bytes()),sa.MeasuredWork())
    raw_chain = stored_cores(raw_tt,sa.MeasuredWork())
    stored_d = dchain[:3]
    norm = producer['normalizer']
    exponent = norm['exponent']
    scale = F.from_float(float.fromhex(norm['mantissa_hex'])) * (
        F(2**exponent) if exponent >= 0 else F(1,2**(-exponent)))
    assert scale > 0
    qr = producer['qr_residual_packet']
    raw_g, d_g, raw_d = own_gram(raw_chain,raw_chain), own_gram(stored_d,stored_d), own_gram(raw_chain,stored_d)
    assert raw_g == read_rational(qr['raw_gram']) > 0
    assert d_g == read_rational(qr['output_gram'])
    assert raw_d == read_rational(qr['cross_gram'])
    assert d_g-2*raw_d/scale+raw_g/scale**2 == read_rational(qr['residual_squared'])
    assert abs(raw_g/scale**2-1) == read_rational(qr['normalizer_ratio_error_upper'])
    report['same_C_D_literal_normalizer_QR_exact_word_checks'] = True
    report['exact_pair_regressions'] = exact_pair_regressions()
    # General zero-ancilla readout and maximum a=4 routing, all B labels.
    checked = 0
    for a in range(5):
        tail = sa.terminal_readout(a)
        for label in range(2**a):
            head = [[ [F(int(j==label)) for j in range(2**a)], [F() for _ in range(2**a)] ]]
            chain = [head]+tail
            sa.validate_chain(chain,sa.MeasuredWork())
            for out in range(2**a):
                word = (0,) + (tuple(int(c) for c in format(out,f'0{a}b')) if a else ())
                assert own_word_value(chain,word) == F(int(label==out))
                checked += 1
    report['independent_all_readout_label_checks_a0_through_a4'] = checked
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        generated = generate(base/'regenerated')
        assert generated['fixture_sha256'] == result['fixture_sha256']
        report['independent_normal_producer_fixture_bytes_equal'] = True
        report['rebound_on_disk_mutants'] = []
        for mode in ('angle','sign','reverse_stage','terminal_excitation'):
            target = base/mode
            shutil.copytree(FIXTURE,target)
            rebound(target,mode)
            changed,c,d = sa.audit_fixture(target)
            r = read_rational(changed['literal_residual']['residual_upper'])
            assert r > F(1,100000)
            from qiskit import qasm2
            from qiskit.quantum_info import Statevector
            import numpy as np
            state = np.asarray(Statevector.from_instruction(qasm2.load(str(target/'saved.qasm'))).data)
            d_dense = np.array([float(own_word_value(d,own_physical_word(i,3,2))) for i in range(32)])
            error = float(np.linalg.norm(state-d_dense))
            garbage = float(np.linalg.norm(state[8:]))
            assert abs(error-float(r)) < 1e-11
            if mode == 'terminal_excitation':
                assert garbage > .99 and error > 1.4
            report['rebound_on_disk_mutants'].append({'mode':mode,'literal_residual_upper':float(r),
                'independent_qiskit_error':error, 'full_terminal_garbage_norm':garbage})
        report['new_normal_producer_supporting_cases'] = []
        for idx,(n,k,length) in enumerate([(1,0,F(1,10)),(2,2,F(1,2)),(3,3,F(2)),(3,8,F(10))]):
            target = base/f'case{idx}'
            generate(target,n,k,length)
            actual,c,d = sa.audit_fixture(target)
            diag = sa.independent_saved_replay(target,c,d)
            assert diag['saved_to_literal_D_euclidean_diagnostic'] < 1e-10
            report['new_normal_producer_supporting_cases'].append({'n':n,'k':k,'L':str(length),
                'instructions':actual['instructions'], 'B':actual['B'],
                'candidate_bound':actual['candidate_bound_float_diagnostic'], 'diagnostic':diag})
        for name in sa.FILES:
            target = base/f'missing_{name.replace(".","_")}'
            shutil.copytree(FIXTURE,target)
            (target/name).unlink()
            try:
                sa.audit_fixture(target)
            except ValueError:
                pass
            else:
                raise AssertionError('missing artifact accepted')
        report['every_required_artifact_missing_rejected'] = sorted(sa.FILES)
    # A low-degree independent radius check at negative arguments as well as ties.
    for x in (F(-8),F(-31,7),F(0),F(1,13),F(8)):
        for degree in (0,1,2,3,16,96):
            sine,cosine,radius = sa.finite_trig(x,sa.MeasuredWork(),degree,80)
            assert radius == abs(x)**(degree+1)/math.factorial(degree+1)
            for is_sine, interval in ((True,sine),(False,cosine)):
                poly = sum((F((-1)**((i-1)//2 if is_sine else i//2),math.factorial(i))*x**i
                            for i in range(degree+1) if i%2 == int(is_sine)), F())
                assert interval.lo <= poly-radius and interval.hi >= poly+radius
    report['fresh_30_taylor_degree_argument_pairs_exact_formula_outward_checks'] = True
    report['binding_after'] = bound_checks()
    report['frozen_files_unchanged'] = True
    return report


if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
