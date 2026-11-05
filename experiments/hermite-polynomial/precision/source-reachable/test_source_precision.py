"""Actual frozen Hermite producer diagnostics; no generic-TT substitution.

The expected-failure test passing means a producer failure was reproduced,
not that the producer satisfies the scientific contract. Dense references are
four-entry diagnostic outputs only and never construction inputs.
"""
from decimal import Decimal, localcontext
from fractions import Fraction
import json
import math
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

HERMITE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HERMITE / "mps"))
sys.path.insert(0, str(HERMITE / "mass"))

import numpy as np
import mps_stable_cores as producer
from mps_core_probe import left_cutoff, pi_interval
from scaled_canonicalize import scaled_right_canonicalize
from analytic_mass import HermiteMass


def cancellation_witness():
    n, k, length = 2, 0, Fraction(1, 10**100)
    digits = math.ceil(n * math.log10(2)) + 90
    low, high = pi_interval(8)
    assert Fraction(3) < low < high < Fraction(4)
    # Below1, adjacent p-digit Decimal numbers are separated by10^(-p).
    half_spacing = Fraction(1, 2 * 10**digits)
    assert 0 < low * length < high * length < half_spacing
    assert left_cutoff(n, length)[0] == 0
    coordinates = []
    restrict = producer.restrict_bernstein

    def record(coeff, lower, upper):
        coordinates.append((lower, upper))
        return restrict(coeff, lower, upper)

    try:
        with patch.object(producer, "restrict_bernstein", side_effect=record):
            producer.stable_hermite_tt(n, k, length)
    except ArithmeticError as error:
        assert str(error) == "source polynomial restriction outside [0,1]"
        assert coordinates == [(Decimal(1), Decimal(1))]
    else:
        raise AssertionError("Frozen actual producer unexpectedly succeeded")

    # Independent factored source evaluation at more than input-scale digits.
    # This is a diagnostic, not an arbitrary-width/theoretical certificate.
    with localcontext() as context:
        context.prec = 160
        model = HermiteMass(k, n, Decimal(1) / Decimal(10)**100)
        reference = [model.value(j) for j in range(1 << n)]
        assert all(Decimal(0) < x <= Decimal(1) for x in reference)
        assert reference[2] == 1
        assert reference[0] < reference[1] < reference[2]
        assert all(abs(x - 1) < Decimal(4) * Decimal('1e-100') for x in reference)
    return {
        "kind": "source_reachable_actual_supplier_failure",
        "failure_class": "IMPLEMENTATION_FAILED",
        "n": n, "k": k, "L": "1/10^100",
        "L_numerator_bits": length.numerator.bit_length(),
        "L_denominator_bits": length.denominator.bit_length(),
        "working_decimal_digits": digits,
        "exact_interval": "[1-pi/10^100,1] with strictly positive width",
        "rounded_interval": [str(x) for x in coordinates[0]],
        "exact_rational_enclosure_below_half_decimal_spacing": True,
        "failure": "ArithmeticError: source polynomial restriction outside [0,1]",
        "failure_stage": "coefficient injection, before QR and normalization",
        "source_center_amplitude": "1",
        "independent_source_values_positive": True,
        "dense_constructor_input": False,
        "uniform_numerical_certificate": False,
    }


def underflow_witness():
    # Actual-source underflow does occur, but this instance's omitted tails
    # have a rigorous tiny error budget. It is NOT a normalization falsifier.
    raw, metadata = producer.stable_hermite_tt(2, 0, Fraction(1000))
    normalized, normalizer = scaled_right_canonicalize(raw)
    actual = normalized.small_dense_diagnostic()
    np.testing.assert_array_equal(actual, np.array([0., 0., 1., 0.]))
    assert normalizer.to_float() == 1
    low, high = pi_interval(8)
    assert low > 3
    # Exact source amplitudes: exp(-1000*pi),exp(-500*pi),1,exp(-500*pi).
    # Euclidean raw error<=sqrt3*exp(-1500); normalization <=2 times it.
    # exp(1500)>1500^300/300! proves the displayed rational upper bound.
    rational_error_upper = 4 * Fraction(math.factorial(300), 1500**300)
    assert rational_error_upper < Fraction(1, 10**300)
    with localcontext() as context:
        context.prec = 100
        model = HermiteMass(0, 2, Decimal(1000))
        reference = [model.value(j) for j in range(4)]
        assert all(x > 0 for x in reference)
        assert reference[2] == 1
        assert reference[1] < Decimal('1e-650')
    return {
        "kind": "source_reachable_underflow_with_small_tail_budget",
        "n": 2, "k": 0, "L": "1000", "cutoff": metadata["left_cutoff"],
        "exact_source": "[exp(-1000*pi),exp(-500*pi),1,exp(-500*pi)]",
        "stored_normalized_state": [float(x) for x in actual],
        "normalizer": normalizer.to_float(),
        "rigorous_normalized_error_upper": "4*300!/1500^300 < 10^-300",
        "proof": "pi>3; monotone exp; normalization_stability; exp Taylor term300",
        "source_math_scope": "finite n2 input; exact source error derivation, not IEEE library certification",
        "dense_constructor_input": False,
        "is_normalization_failure": False,
    }


class SourcePrecisionTests(unittest.TestCase):
    def test_exact_source_coefficient_collapse_identity(self):
        # Finite exact rational discriminator for the general algebraic
        # derivation in result.json; not promotion to an all-k theorem.
        for k in range(25):
            d = 2 * k + 1
            a = [sum((Fraction(math.comb(k + i - m, k), math.factorial(m))
                      for m in range(i + 1)), Fraction()) for i in range(k + 1)]
            for r in range(k + 1):
                original = sum((a[i] * Fraction(math.comb(k - i, r - i), math.comb(d, r))
                                for i in range(r + 1)), Fraction())
                collapsed = sum((Fraction(math.comb(d - m, r - m),
                                          math.comb(d, r) * math.factorial(m))
                                 for m in range(r + 1)), Fraction())
                self.assertEqual(original, collapsed)
                self.assertGreaterEqual(collapsed, 1)
                self.assertLess(collapsed, 2)

    def test_actual_rational_input_coordinate_collapse(self):
        self.assertEqual(cancellation_witness()["failure_class"], "IMPLEMENTATION_FAILED")

    def test_actual_source_underflow_is_not_generic_tt_failure(self):
        self.assertFalse(underflow_witness()["is_normalization_failure"])

    def test_ordinary_neighbor_has_source_action(self):
        raw, _ = producer.stable_hermite_tt(2, 0, Fraction(1, 100))
        normalized, _ = scaled_right_canonicalize(raw)
        with localcontext() as context:
            context.prec = 100
            model = HermiteMass(0, 2, Decimal('0.01'))
            reference = np.array([float(model.value(j)) for j in range(4)])
        reference /= np.linalg.norm(reference)
        self.assertLess(np.linalg.norm(normalized.small_dense_diagnostic() - reference), 1e-14)


if __name__ == "__main__":
    if "--witness" in sys.argv:
        print(json.dumps({"cancellation": cancellation_witness(),
                          "underflow": underflow_witness()}, indent=2, allow_nan=False))
    else:
        unittest.main()
