"""Actual-return regressions; dense vectors appear only in small diagnostics."""
from decimal import Decimal, localcontext
from fractions import Fraction
import json
import math
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch

import numpy as np

from qr_residual import (MPS, ScaledNorm, Work, certify_pair,
                         certify_scaled_canonicalize, read_rational,
                         sqrt_upper, stored_cores, cross_gram, rational_text)
from mps_core_probe import TT

OFFSET = Path(__file__).resolve().parents[1] / "offset-source"
sys.path.insert(0, str(OFFSET))
from offset_source import offset_hermite_tt


def exact_amplitude(tt, j):
    """Independent slow amplitude specification, diagnostic only."""
    current = [Fraction(1)]
    for offset, core in enumerate(tt.cores):
        bit = (j >> (tt.n - 1 - offset)) & 1
        current = [sum((a * Fraction.from_float(float(core[i, bit, b]))
                        for i, a in enumerate(current)), Fraction())
                   for b in range(core.shape[2])]
    return current[0]


def check_dense_exact_identity(raw, output, cert):
    if raw.n > 8:
        raise AssertionError("dense diagnostic width cap")
    a = [exact_amplitude(raw, j) for j in range(1 << raw.n)]
    b = [exact_amplitude(output, j) for j in range(1 << output.n)]
    s = read_rational(cert["actual_normalizer"])
    assert sum((x*x for x in a), Fraction()) == read_rational(cert["raw_gram"])
    assert sum((x*x for x in b), Fraction()) == read_rational(cert["output_gram"])
    assert sum((x*y for x,y in zip(a,b)), Fraction()) == read_rational(cert["cross_gram"])
    assert sum(((y-x/s)**2 for x,y in zip(a,b)), Fraction()) == read_rational(cert["residual_squared"])
    # Literal signed normalized error. Decimal here is an independent finite
    # diagnostic, not what makes the rational certificate rigorous.
    with localcontext() as context:
        context.prec = 120
        dec = lambda x: Decimal(x.numerator)/Decimal(x.denominator)
        norm = dec(read_rational(cert["raw_gram"])).sqrt()
        error_sq = sum(((dec(y)-dec(x)/norm)**2 for x,y in zip(a,b)), Decimal())
        bound = dec(read_rational(cert["normalized_stored_TT_error_upper"]))
        assert error_sq.sqrt() <= bound + Decimal('1e-110')
        return float(error_sq.sqrt())


def case_record(n,k,L):
    raw,_ = offset_hermite_tt(n,k,L)
    output, norm, cert = certify_scaled_canonicalize(raw)
    if n <= 8:
        diagnostic = check_dense_exact_identity(raw,output,cert)
    else:
        diagnostic = None
    return {"n":n,"k":k,"L":str(L),"stored_normalized_error_bound":
            cert['normalized_stored_TT_error_upper'],
            "stored_normalized_error_bound_float_diagnostic":
            float(read_rational(cert['normalized_stored_TT_error_upper'])),
            "exact_residual_positive":read_rational(cert['residual_squared'])>0,
            "normalizer_ratio_error_bound":cert['normalizer_ratio_error_upper'],
            "normalizer_ratio_error_positive":read_rational(cert['normalizer_ratio_error_upper'])>0,
            "normalizer_ratio_error_float_diagnostic":float(read_rational(cert['normalizer_ratio_error_upper'])),
            "dense_error_diagnostic":diagnostic,"work":cert['work'],
            "global_source_epsilon_certificate":False}


class ResidualTests(unittest.TestCase):
    def test_actual_source_returns_and_exact_gram(self):
        for n,k,L in [(2,0,Fraction(1,10**100)),(3,1,Fraction(1)),
                      (5,3,Fraction(1,7)),(4,0,Fraction(1000))]:
            with self.subTest(n=n,k=k,L=L):
                record=case_record(n,k,L)
                self.assertLess(float(read_rational(record['stored_normalized_error_bound'])),1e-11)

    def test_same_return_source_once_no_dense(self):
        raw,_=offset_hermite_tt(3,1,Fraction(1))
        import qr_residual
        actual=qr_residual.scaled_right_canonicalize
        held=[]
        def traced(arg):
            pair=actual(arg); held.append(pair); return pair
        with (patch('qr_residual.scaled_right_canonicalize',side_effect=traced) as call,
             patch.object(TT,'amplitude',side_effect=AssertionError('dense production')),
             patch.object(TT,'small_dense_diagnostic',side_effect=AssertionError('dense production'))):
            output,norm,cert=certify_scaled_canonicalize(raw)
        self.assertEqual(call.call_count,1)
        self.assertIs(output,held[0][0]); self.assertIs(norm,held[0][1])
        self.assertFalse(cert['dense_constructor_or_checker_input'])

    def test_rank_deficient_and_tall_reduced_qr(self):
        # QR sees a 2 by5 matrix at the terminal core. Deficient rows/columns
        # remain; no claimed numerical/exact rank calculation is introduced.
        raw=TT([np.array([1.,-1.,2.,0.,3.,2.,0.,1.,1.,-2.]).reshape(1,2,5),
                np.array([1.,2.,2.,4.,0.,0.,-1.,-2.,3.,6.]).reshape(5,2,1)])
        output,_,cert=certify_scaled_canonicalize(raw)
        self.assertEqual(output.cores[1].shape,(2,2,1))
        self.assertLess(check_dense_exact_identity(raw,output,cert),1e-12)
        self.assertLess(float(read_rational(cert['normalized_stored_TT_error_upper'])),1e-12)

    def test_zero_and_stored_cancellation_are_honest_failures(self):
        zero=TT([np.zeros((1,2,1))])
        with self.assertRaisesRegex(ArithmeticError,'stored-zero'):
            certify_scaled_canonicalize(zero)
        cancellation=TT([np.array([1.,1.,1.,1.]).reshape(1,2,2),
                         np.array([1.,1.,-1.,-1.]).reshape(2,2,1)])
        nonzero=TT([np.ones((1,2,1)),np.ones((1,2,1))])
        with self.assertRaisesRegex(ArithmeticError,'stored raw TT is zero'):
            certify_pair(cancellation,nonzero,ScaledNorm(.5,1))
        with self.assertRaises(ArithmeticError):
            certify_scaled_canonicalize(cancellation)

    def test_tiny_huge_scales_signed_and_no_normalizer_expansion(self):
        for scale in (math.ldexp(1.,-1000),math.ldexp(1.,1000)):
            raw=TT([np.array([-scale,scale]).reshape(1,2,1) for _ in range(3)])
            output,norm,cert=certify_scaled_canonicalize(raw)
            with self.assertRaises(ArithmeticError): norm.to_float()
            self.assertLess(check_dense_exact_identity(raw,output,cert),1e-12)
            self.assertLess(float(read_rational(cert['normalized_stored_TT_error_upper'])),1e-12)

    def test_normalizer_drift_and_wrong_signed_return_detected(self):
        raw=TT([np.array([1.,0.]).reshape(1,2,1)])
        output=TT([np.array([1.,0.]).reshape(1,2,1)])
        cert=certify_pair(raw,output,ScaledNorm(.5,2)) # actual s=2, not true norm1
        self.assertEqual(read_rational(cert['residual_squared']),Fraction(1,4))
        self.assertEqual(read_rational(cert['normalizer_ratio_error_upper']),Fraction(3,4))
        self.assertGreaterEqual(read_rational(cert['normalized_stored_TT_error_upper']),1)
        wrong=TT([np.array([-1.,0.]).reshape(1,2,1)])
        cert=certify_pair(raw,wrong,ScaledNorm(.5,1))
        self.assertEqual(read_rational(cert['residual_squared']),4)
        self.assertEqual(read_rational(cert['normalized_stored_TT_error_upper']),2)

    def test_wide_no_amplitude_enumeration_and_cubic_counts(self):
        n=64
        product=TT([np.array([1.,-.5]).reshape(1,2,1) for _ in range(n)])
        actual,_=offset_hermite_tt(n,2,Fraction(1,10**100))
        for raw in (product,actual):
            with self.subTest(max_bond=raw.max_bond), patch.object(
                TT,'amplitude',side_effect=AssertionError('enumeration')):
                _,_,cert=certify_scaled_canonicalize(raw)
            self.assertEqual(cert['work']['visited_core_pairs'],3*n)
            self.assertLessEqual(cert['work']['contraction_additions']+
                                 cert['work']['contraction_multiplications'],
                                 27*n*max(cert['raw_max_bond'],cert['output_max_bond'])**3)
            self.assertLess(float(read_rational(cert['normalized_stored_TT_error_upper'])),1e-11)

    def test_directed_sqrt_and_invalid_stored_inputs(self):
        for q in (Fraction(0),Fraction(1,4),Fraction(2),Fraction(1,10**1000)):
            r,_=sqrt_upper(q,80,Work())
            self.assertGreaterEqual(r*r,q)
            if q==0:self.assertEqual(r,0)
        for array in (np.array([np.inf,1.]),np.array([np.nan,1.])):
            with self.assertRaises(ArithmeticError):
                certify_scaled_canonicalize(TT([array.reshape(1,2,1)]))
        with self.assertRaises(ValueError):
            certify_scaled_canonicalize(TT([np.ones((1,2,1),dtype=np.float32)]))
        with self.assertRaises(ValueError):
            certify_scaled_canonicalize(TT([np.ones((1,2,1))]),certificate_bits=-1)
        with self.assertRaises(ValueError):
            certify_scaled_canonicalize(TT([np.ones((1,2,0)),np.ones((0,2,1))]))
        with self.assertRaises(ValueError):
            certify_scaled_canonicalize(TT([np.ones((1,2,1),dtype=np.complex128)]))
        with self.assertRaisesRegex(ValueError,'same physical core count'):
            certify_pair(TT([np.ones((1,2,1))]),
                         TT([np.ones((1,2,1)),np.ones((1,2,1))]),ScaledNorm(.5,1))


def witness():
    return {"kind":"actual-stored-scaled-QR-a-posteriori-residual",
            "records":[case_record(2,0,Fraction(1,10**100)),case_record(3,1,Fraction(1)),
                       case_record(5,3,Fraction(1,7)),case_record(4,0,Fraction(1000))],
            "not_global_source_or_circuit_certificate":True}


def wide_witness():
    started=time.perf_counter()
    raw,_=offset_hermite_tt(64,2,Fraction(1,10**100))
    source_seconds=time.perf_counter()-started
    started=time.perf_counter()
    with (patch.object(TT,'amplitude',side_effect=AssertionError('enumeration')),
          patch.object(TT,'small_dense_diagnostic',side_effect=AssertionError('enumeration'))):
        output,_,cert=certify_scaled_canonicalize(raw)
    elapsed=time.perf_counter()-started
    q,r=read_rational(cert['residual_squared']),read_rational(cert['residual_upper'])
    assert q>=0 and r*r>=q
    assert cert['work']['scalar_assembly_additions']==4
    assert cert['work']['scalar_assembly_multiplications']==6
    assert cert['work']['scalar_assembly_divisions']==1
    return {"n":64,"k":2,"L":"1/10^100","raw_bond":raw.max_bond,
            "output_bond":output.max_bond,"source_seconds":source_seconds,
            "QR_and_certificate_seconds":elapsed,
            "bound_float_DIAGNOSTIC":float(read_rational(cert['normalized_stored_TT_error_upper'])),
            "residual_positive":q>0,
            "tau_positive":read_rational(cert['normalizer_ratio_error_upper'])>0,
            "exact_square_root_bound_checked":True,"work":cert['work'],
            "no_amplitudes_called":True,"stored_raw_not_ideal_source":True}


if __name__=='__main__':
    if '--wide-witness' in sys.argv: print(json.dumps(wide_witness(),indent=2,allow_nan=False))
    elif '--witness' in sys.argv: print(json.dumps(witness(),indent=2,allow_nan=False))
    else: unittest.main()
