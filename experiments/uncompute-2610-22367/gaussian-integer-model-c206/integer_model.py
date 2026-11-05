# SPDX-License-Identifier: Apache-2.0
"""New exact-integer transcription of the frozen uncompute Gaussian witness.

Modified/derived from scalar formulas, not imported upstream code. See NOTICE
and LICENSE. No floats, numpy, upstream imports, fitting or circuit execution.
The default command is a bounded diagnostic, not a proof or error certificate.
"""
import argparse
import hashlib
import json
from pathlib import Path

DATA_SHA256 = 'eda0180c296ab1f45d05537ae6fffcbc036f68b055f501f6174978a1b41fddbe'
UPSTREAM_RAW_SHA256 = 'eac7b1a900fd3d8a407edfdcb74c2210d28bcb5a6b656d9e6b84dfa53452f379'
SCALARS = dict(Ncut=514, s0=455, NT=6, M=11, CAPW=18, A0SH=7,
               A0BITS=25, EQ=8, RB=6, I0=2, FLOW=2, FW=19, EWID=11)
MOD = 1 << 39


def load_fixed():
    raw = Path(__file__).with_name('fixed_constants.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == DATA_SHA256
    c = json.loads(raw)
    assert all(c[k] == v for k, v in SCALARS.items())
    assert all(len(c[k]) == 514 for k in ('A0p', 'B1p', 'E'))
    assert len(c['words']) == 1024
    return c, tuple(int(w, 16) for w in c['words'])


CFG, WORDS = load_fixed()


def bit(n, i):
    return (n >> i) & 1 if i >= 0 else 0


def digit(n, i):
    """Radix-4 controls; the lower overlap bit of row zero is zero."""
    b0, b1, b2 = bit(n, 2*i-1), bit(n, 2*i), bit(n, 2*i+1)
    one = b0 ^ b1
    two = (1-one) & (b1 ^ b2)
    return one, two, 1-2*b2


def fields(j):
    if not 0 <= j < 1024:
        raise ValueError('address is ten bits')
    w = WORDS[j]
    slope = w % (1 << 19)
    cp = (w >> 19) % (1 << 11)
    correction = cp if cp < (1 << 10) else cp-(1 << 11)
    a0 = (w >> 30) % (1 << 25)
    return a0, slope, correction


def truncate_signed(z, shift, keep):
    """Arithmetic right shift then low-column truncation; negative floors kept."""
    return (z // (1 << (shift+keep))) * (1 << keep)


def middle_row(j, D, t):
    assert 0 <= D < (1 << 25) and 0 <= t < 6
    U = D >> 14
    one, two, sign = digit(U, t)
    correction = fields(j)[2] * 256
    shift = 15-2*t
    low = max(2, 9-shift)
    return sign * (one * truncate_signed(correction, shift, low)
                   + two * truncate_signed(correction, shift-1, low))


def slope_trace(j, D):
    """Actual finite register model, in stored units of four full-slope units."""
    states = [fields(j)[1]]
    for t in range(6):
        row = middle_row(j, D, t)
        assert row % 4 == 0
        states.append((states[-1] + row//4) % (1 << 19))
    return states


def slope_unbounded(j, D):
    return 4*fields(j)[1] + sum(middle_row(j, D, t) for t in range(6))


def slope_word(j, D):
    return 4*slope_trace(j, D)[-1]


def final_row(F, D, i):
    assert 0 <= F < (1 << 21) and 0 <= D < (1 << 25) and 2 <= i <= 10
    one, two, sign = digit(F, i)
    shift = 21-2*i
    drop = max(6, 2*i+5-18)
    t1 = (D // (1 << (shift+drop))) * (1 << drop)
    t2 = (D // (1 << (shift-1+drop))) * (1 << drop)
    bias = (one | two) * (1 << (drop-1))
    return sign * (one*t1 + two*t2 + bias)


def local_increment(j, D):
    F = slope_word(j, D)
    P = sum(final_row(F, D, i) for i in range(2, 11))
    return 128*fields(j)[0]-P


def fold_signed(xs):
    return xs if xs >= 0 else -xs-1


def increment(xs):
    if not -(1 << 35) <= xs < (1 << 35):
        raise ValueError('outside original signed input promise')
    y = fold_signed(xs)
    return local_increment(y >> 25, y % (1 << 25))


def output(xpattern, k):
    if not 0 <= xpattern < MOD or not 0 <= k < MOD:
        raise ValueError('input patterns must be 39 bits')
    xs = xpattern if xpattern < (1 << 38) else xpattern-MOD
    return xpattern, (k+increment(xs)) % MOD


def diagnostic():
    # Finite structural checks of ALL final table entries, not numerical error.
    for j, w in enumerate(WORDS):
        assert 0 <= w < (1 << 55)
        if j < 514:
            a, b, q = fields(j)
            assert a == CFG['A0p'][j]
            assert 4*b == CFG['B1p'][j]
            assert 256*q == CFG['E'][j]-(1 << 18)
            rebuilt = (CFG['B1p'][j] >> 2) | (((CFG['E'][j] >> 8) ^ 1024) << 19) | (a << 30)
            assert rebuilt == w
        else:
            assert w == 0
        if 455 <= j < 514:
            assert fields(j)[1:] == (0, 0)
    assert CFG['A0p'][0] == (1 << 25)-1
    assert all(a < (1 << 25)-1 for a in CFG['A0p'][1:])
    ds = (0, 1, 63, 127, 128, 16383, 16384, (1 << 24)+127, (1 << 25)-1)
    js = (0, 1, 31, 127, 454, 455, 513, 514, 1023)
    mid_counterexample = None
    final_counterexample = None
    for j in js:
        for D in ds:
            F = slope_word(j, D)
            assert F == slope_unbounded(j, D) % (1 << 21)
            if 455 <= j:
                assert local_increment(j, D) == 128*fields(j)[0]
            P = sum(final_row(F, D, i) for i in range(2, 11))
            if final_counterexample is None and P != F*D//(1 << 21):
                final_counterexample = dict(j=j, D=D, F=F, row_sum=P, floor_full=F*D//(1 << 21))
            S = slope_unbounded(j, D)-4*fields(j)[1]
            naive = (D >> 14)*(256*fields(j)[2])//(1 << 15)
            if mid_counterexample is None and S != naive:
                mid_counterexample = dict(j=j, D=D, rows=S, floor_full=naive)
            start = D//128*128
            assert local_increment(j, start) == local_increment(j, start+127)
    assert final_counterexample is not None and mid_counterexample is not None
    xs_cases = (-(1 << 35), -(514 << 25), -1, 0, 1, (455 << 25), (514 << 25), (1 << 35)-1)
    samples = []
    for xs in xs_cases:
        inc = increment(xs)
        assert increment(xs) == increment(-xs-1)
        vals = []
        for k in (0, MOD-1):
            xpat = xs % MOD
            xp, ko = output(xpat, k)
            assert xp == xpat and (ko-k) % MOD == inc % MOD
            vals.append(ko)
        samples.append(dict(xs=xs, folded=fold_signed(xs), increment=inc, outputs_k0_kmax=vals))
    return dict(classification='FINITE_EXACT_INTEGER_DIAGNOSTIC_NOT_PROOF',
                source_raw_sha256=UPSTREAM_RAW_SHA256, copied_lf_sha256=DATA_SHA256,
                fixed_table_entries=1024, coefficient_rows=514,
                tested_local_pairs=len(js)*len(ds), tested_global_inputs=len(xs_cases),
                mid_shifts=[15-2*t for t in range(6)], mid_lows=[max(2, 9-(15-2*t)) for t in range(6)],
                final_drops=[max(6, 2*i+5-18) for i in range(2, 11)],
                final_constancy_exponents=[21-2*i-1+max(6, 2*i+5-18) for i in range(2, 11)],
                middle_full_product_counterexample=mid_counterexample,
                final_full_product_counterexample=final_counterexample,
                origin_increment=increment(0), origin_ideal_integer_gap=(1 << 32)-increment(0),
                samples=samples, float_or_exp_calls=False, circuit_or_error_acceptance=False)


def table_patch(destination):
    # Mechanical data transcription only; no search, table mutation or proof.
    lines = ['-- SPDX-License-Identifier: Apache-2.0',
             '-- Modified transcription of fixed uncompute constants; see NOTICE and LICENSE.',
             '-- All 1024 addresses represented: explicit nonzero prefix and zero suffix.',
             'import Init', '', 'namespace UncomputeGaussian206', '',
             'def frozenWord (j : Nat) : Nat :=', '  match j with']
    lines += [f'  | {j} => {w}' for j, w in enumerate(WORDS[:514])]
    lines += ['  | _ => 0', '', 'end UncomputeGaussian206', '']
    body = '\n'.join(lines)
    return '*** Begin Patch\n*** Add File: '+destination+'\n'+''.join('+'+s+'\n' for s in body.splitlines())+'*** End Patch\n'


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--table-patch')
    a = p.parse_args()
    if a.table_patch:
        print(table_patch(a.table_patch), end='')
    else:
        print(json.dumps(diagnostic(), indent=2))
