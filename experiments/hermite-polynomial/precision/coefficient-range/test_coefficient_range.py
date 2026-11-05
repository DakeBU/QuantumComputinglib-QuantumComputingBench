"""Exact finite discrimination of literal frozen coefficient suppliers.

These Fraction checks do not replace the all-k Lean providers, scalar analytic
membership, executable refinement, or a runtime certificate.
"""
from fractions import Fraction
import json
import math
from pathlib import Path
import sys
import unittest

PRECISION = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PRECISION / "offset-source"))
from offset_source import (source_base_weights, source_coefficient_intervals,
                           exp_minus_one_interval)

CASES = tuple(range(33)) + (48, 64, 96, 128)


def source_numerator(k, i):
    # Integer common-denominator reconstruction, independent of Fraction sums.
    factorial = math.factorial(k)
    return sum(math.comb(k + i - m, k) * (factorial // math.factorial(m))
               for m in range(i + 1))


def numerator_row(k):
    degree = 2 * k + 1
    source = [source_numerator(k, i) for i in range(k + 1)]
    return [sum(source[i] * math.comb(k - i, r - i)
                for i in range(k + 1) if i <= r <= k)
            for r in range(degree + 1)]


def denominator_row(k):
    return [math.factorial(k) * math.comb(2 * k + 1, r)
            for r in range(2 * k + 2)]


def exponent_denominator(k):
    return k * (k + 1) + 2 * k + 1


def exponent_numerator(k):
    return (k + 2) * (k + 1) + k * (k + 1) + 5 * k + 1


def exponent_scalar_numerator(k):
    return (k + 2) * (k + 1) + 2 * k * (k + 1) + 7 * k + 2


class LiteralCoefficientTests(unittest.TestCase):
    def test_all_tested_rows_literal_integer_representation(self):
        for k in CASES:
            base, nums, dens = source_base_weights(k), numerator_row(k), denominator_row(k)
            for r, (value, numerator, denominator) in enumerate(zip(base, nums, dens)):
                self.assertGreater(denominator, 0)
                self.assertEqual(value, Fraction(numerator, denominator), (k, r))
                self.assertEqual(denominator % value.denominator, 0)
                self.assertLessEqual(value.numerator, numerator)

    def test_coarse_range_and_binary_output_bounds(self):
        for k in CASES:
            bound = (k + 1)**2 * 2**(3 * k)
            nums, dens = numerator_row(k), denominator_row(k)
            for value, numerator, denominator in zip(source_base_weights(k), nums, dens):
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, bound)
                self.assertLessEqual(numerator, bound * denominator)
                self.assertLessEqual(denominator, 2**exponent_denominator(k))
                self.assertLessEqual(numerator, 2**exponent_numerator(k))
                self.assertLessEqual(value.denominator.bit_length(), exponent_denominator(k) + 1)
                self.assertLessEqual(value.numerator.bit_length(), exponent_numerator(k) + 1)

    def test_k_zero_is_not_degenerate(self):
        self.assertEqual(source_base_weights(0), [Fraction(1), Fraction(0)])
        self.assertEqual(numerator_row(0), [1, 0])
        self.assertEqual(denominator_row(0), [1, 1])

    def test_actual_rational_exp_endpoint_rows(self):
        for k in (0, 1, 8, 32, 64, 128):
            base, nums, dens = source_base_weights(k), numerator_row(k), denominator_row(k)
            for terms in (2, 16, 32, 64):
                interval = exp_minus_one_interval(terms)
                self.assertTrue(0 <= interval.lo <= interval.hi <= 1)
                actual = source_coefficient_intervals(base, interval)
                for endpoint_name in ("lo", "hi"):
                    scalar = getattr(interval, endpoint_name)
                    p, q = scalar.numerator, scalar.denominator
                    for r, coefficient in enumerate(actual):
                        reflected = 2 * k + 1 - r
                        numerator = p * nums[r] * dens[reflected] + q * nums[reflected] * dens[r]
                        denominator = q * dens[r] * dens[reflected]
                        value = getattr(coefficient, endpoint_name)
                        self.assertEqual(value, Fraction(numerator, denominator))
                        self.assertTrue(0 <= value <= 2 * (k + 1)**2 * 2**(3 * k))
                        self.assertLessEqual(denominator, q * 2**(2 * exponent_denominator(k)))
                        self.assertLessEqual(numerator, (p + q) * 2**exponent_scalar_numerator(k))
                        self.assertEqual(denominator % value.denominator, 0)

    def test_rational_scalar_input_size_not_assumed_constant(self):
        k = 8
        nums, dens = numerator_row(k), denominator_row(k)
        scalar = Fraction(2**2000 + 1, 2**4096 + 3)
        for r in range(2 * k + 2):
            reflected = 2 * k + 1 - r
            numerator = scalar.numerator * nums[r] * dens[reflected] + scalar.denominator * nums[reflected] * dens[r]
            denominator = scalar.denominator * dens[r] * dens[reflected]
            output = Fraction(numerator, denominator)
            self.assertLessEqual(output.numerator.bit_length(), (scalar.numerator + scalar.denominator).bit_length() + exponent_scalar_numerator(k))
            self.assertLessEqual(output.denominator.bit_length(), scalar.denominator.bit_length() + 2 * exponent_denominator(k))


def witnesses():
    records = []
    for k in (0, 8, 32, 64, 128):
        base = source_base_weights(k)
        intervals = source_coefficient_intervals(base, exp_minus_one_interval(32))
        records.append({
            "k": k, "degree": 2 * k + 1, "row_length": len(base),
            "max_reduced_base_numerator_bits": max(x.numerator.bit_length() for x in base),
            "max_reduced_base_denominator_bits": max(x.denominator.bit_length() for x in base),
            "max_reduced_exp_endpoint_numerator_bits": max(q.numerator.bit_length() for x in intervals for q in (x.lo, x.hi)),
            "max_reduced_exp_endpoint_denominator_bits": max(q.denominator.bit_length() for x in intervals for q in (x.lo, x.hi)),
            "proved_base_numerator_bit_envelope": exponent_numerator(k) + 1,
            "proved_base_denominator_bit_envelope": exponent_denominator(k) + 1,
            "max_base_float_diagnostic": float(max(base)),
            "scope": "finite exact Fraction representation check; not Lean/Python whole-program refinement"
        })
    return {"task": "SP-HERMITE-POLY-002", "cases": list(CASES), "records": records,
            "all_k_lean_evidence": "CoefficientRange.lean", "global_epsilon_certificate": False}


if __name__ == "__main__":
    if "--witness" in sys.argv:
        print(json.dumps(witnesses(), indent=2, allow_nan=False))
    else:
        unittest.main()
