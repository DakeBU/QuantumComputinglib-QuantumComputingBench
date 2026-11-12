"""Actual changed-mechanism regressions, separate from uniform certificates."""
from decimal import Decimal, localcontext
from fractions import Fraction
import json
import math
from pathlib import Path
import sys
import unittest

import numpy as np

from offset_source import (HERMITE, Interval, certified_polynomial_injection,
                           convex_interval, offset_hermite_tt, rational_text,
                           read_rational)
sys.path.insert(0, str(HERMITE / "mass"))
from analytic_mass import HermiteMass
from mps_core_probe import TT
from mps_stable_cores import stable_hermite_tt
from scaled_canonicalize import scaled_right_canonicalize
from mps_ry_compiler import compile_mps


def diagnostic_precision(n, length):
    # Independent diagnostic only; no constructed TT consumes this reference.
    return max(180, math.ceil(n * math.log10(2)) +
               math.ceil(length.denominator.bit_length() * math.log10(2)) + 80)


def independent_reference(n, k, length):
    if n > 10:
        raise ValueError("dense diagnostic limit n<=10")
    with localcontext() as context:
        context.prec = diagnostic_precision(n, length)
        model = HermiteMass(k, n, Decimal(length.numerator) / Decimal(length.denominator))
        vector = np.array([float(model.value(j)) for j in range(1 << n)])
    return vector / np.linalg.norm(vector)


def check_local_certificates(metadata):
    for certificate in metadata["polynomial_certificates"]:
        budget = read_rational(certificate["maximum_coefficient_error_bound"])
        assert budget <= read_rational(certificate["tolerance"])
        actual_errors = []
        for endpoints, stored, error in zip(certificate["coefficient_intervals"],
                                            certificate["stored_dyadics"],
                                            certificate["coefficient_error_bounds"]):
            lo, hi = map(read_rational, endpoints)
            stored, error = read_rational(stored), read_rational(error)
            assert lo <= hi
            assert error == max(abs(stored - lo), abs(stored - hi))
            actual_errors.append(error)
        assert max(actual_errors) == budget
        ulo, uhi = map(read_rational, certificate["offset_lower_enclosure"])
        vlo, vhi = map(read_rational, certificate["offset_upper_enclosure"])
        zlo, zhi = map(read_rational, certificate["second_parameter_enclosure"])
        assert 0 <= ulo <= uhi < 1 and 0 < vlo <= vhi <= 1
        assert 0 < zlo <= zhi <= 1

        # Independent source values at three legal points in the injection.
        # This checks the orientation without using any dense constructor input.
        n, k, length = certificate["n"], certificate["k"], read_rational(certificate["L"])
        a, b, degree = certificate["a"], certificate["b"], 2 * k + 1
        with localcontext() as context:
            context.prec = diagnostic_precision(n, length)
            model = HermiteMass(k, n, Decimal(length.numerator) / Decimal(length.denominator))
            coeff = [read_rational(x) for x in certificate["stored_dyadics"]]
            delta = Decimal(budget.numerator) / Decimal(budget.denominator)
            for j in sorted({a, (a + b - 1) // 2, b - 1}):
                y = Decimal(j - a) / Decimal(b - a)
                value = sum((Decimal(c.numerator) / Decimal(c.denominator) * math.comb(degree, r) *
                             (y**r if r else Decimal(1)) *
                             ((1 - y)**(degree - r) if degree != r else Decimal(1))
                             for r, c in enumerate(coeff)), Decimal(0))
                # Diagnostic residual guard is separate from the exact rational
                # stored endpoint certificate and is not promoted to a theorem.
                guard = Decimal(10)**(-context.prec + 20)
                assert abs(value - model.value(j)) <= delta + guard


def actual_pipeline(n, k, length, circuit=False, sign=1):
    raw, metadata = offset_hermite_tt(n, k, length)
    check_local_certificates(metadata)
    if sign == -1:
        # Generic signed-library regression, not a substituted Hermite target.
        raw = TT([c.copy() for c in raw.cores])
        raw.cores[0] *= -1
    canonical, normalizer = scaled_right_canonicalize(raw)
    reference = sign * independent_reference(n, k, length)
    error = float(np.linalg.norm(canonical.small_dense_diagnostic() - reference))
    record = {"n": n, "k": k, "L": rational_text(length), "sign_diagnostic": sign,
              "scaled_state_error_diagnostic": error,
              "norm_float_diagnostic": normalizer.to_float(),
              "max_bond": raw.max_bond, "core_scalars": raw.scalar_count,
              "injections": metadata["middle_dyadic_injections"],
              "certificate_count": len(metadata["polynomial_certificates"]),
              "max_saved_coefficient_endpoint_bits": max((c["max_coefficient_endpoint_bits"]
                  for c in metadata["polynomial_certificates"]), default=0),
              "max_local_error_diagnostic_float": max((float(read_rational(c["maximum_coefficient_error_bound"]))
                  for c in metadata["polynomial_certificates"]), default=0.),
              "dense_constructor_input": False, "uniform_global_certificate": False}
    assert error < 1e-12
    if circuit:
        from qiskit.quantum_info import Statevector
        # Existing actual compiler consumes the scaled normalized TT. It repeats
        # QR; this is charged and not claimed as a proved compiler refinement.
        plan = compile_mps(canonical)
        state = np.asarray(Statevector.from_instruction(plan.qiskit_circuit()).data)
        expected = np.zeros_like(state)
        expected[:1 << n] = reference
        circuit_error = float(np.linalg.norm(state - expected))
        assert circuit_error < 1e-11  # Literal signed vector; no phase alignment.
        record["actual_ry_cx_circuit_error_diagnostic"] = circuit_error
        record["actual_primitive_resources"] = plan.resource_counts
        record["compiler_input"] = "actual scaled-normalized TT, not independent source vector"
    return record


class OffsetSourceTests(unittest.TestCase):
    def test_tiny_length_actual_pipeline_and_circuit(self):
        length = Fraction(1, 10**100)
        with self.assertRaisesRegex(ArithmeticError, "source polynomial restriction outside"):
            stable_hermite_tt(2, 0, length)
        record = actual_pipeline(2, 0, length, circuit=True)
        self.assertLess(record["max_local_error_diagnostic_float"], 3e-100)

    def test_ordinary_large_and_nonterminating_rational_lengths(self):
        for n, k, length in [(1, 0, Fraction(1, 10)), (3, 1, Fraction(1)),
                              (5, 2, Fraction(1, 2)), (8, 8, Fraction(10)),
                              (4, 0, Fraction(1000)), (5, 3, Fraction(1, 7))]:
            with self.subTest(n=n, k=k, L=length):
                actual_pipeline(n, k, length, circuit=(n == 3))

    def test_signed_basis_literal_not_phase_quotient(self):
        actual_pipeline(2, 0, Fraction(1, 10), circuit=True, sign=-1)

    def test_wide_tiny_length_no_dense_reference(self):
        n = 64
        raw, metadata = offset_hermite_tt(n, 2, Fraction(1, 10**100))
        check_local_certificates(metadata)
        canonical, norm = scaled_right_canonicalize(raw)
        self.assertFalse(metadata["dense_constructor_input"])
        self.assertLessEqual(raw.max_bond, 10)
        self.assertLess(abs(norm.log2_norm - n / 2), 1e-12)
        for j in (0, 1, (1 << (n - 1)) - 1, 1 << (n - 1), (1 << n) - 1):
            self.assertLess(abs(canonical.amplitude(j) / math.ldexp(1., -n // 2) - 1), 1e-12)

    def test_long_exact_certificates_do_not_print_underflow_as_zero(self):
        raw, metadata = offset_hermite_tt(2, 2, Fraction(1, 10**1000))
        check_local_certificates(metadata)
        certificates = metadata["polynomial_certificates"]
        self.assertTrue(any("0x" in endpoint for c in certificates
                            for pair in c["coefficient_intervals"] for endpoint in pair))
        self.assertGreater(read_rational(certificates[0]["maximum_coefficient_error_bound"]), 0)
        self.assertEqual(raw.amplitude(2), 1.)

    def test_impossible_local_tolerance_fails_closed(self):
        with self.assertRaisesRegex(ArithmeticError, "local coefficient tolerance not met"):
            certified_polynomial_injection(2, 0, Fraction(1, 10), 0, 2,
                                           Fraction(1, 10**40), max_refinements=2)

    def test_near_cutoff_coordinate_enclosure_is_refined(self):
        from mps_core_probe import pi_interval
        length = Fraction(2) / pi_interval(32)[1]
        values, certificate = certified_polynomial_injection(
            2, 0, length, 1, 2, Fraction(1, 10**14), initial_terms=16)
        self.assertGreater(certificate["counters"]["coordinate_refinements"], 0)
        self.assertGreaterEqual(certificate["terms"], 32)
        actual_pipeline(2, 0, length)
        # The same legal interval is not falsely declared certified if a
        # deliberately insufficient one-attempt cap is requested.
        with self.assertRaisesRegex(ArithmeticError, "source offset locus not certified after"):
            certified_polynomial_injection(2, 0, length, 1, 2,
                                           Fraction(1, 10**14), initial_terms=16,
                                           max_refinements=1)

    def test_signed_interval_convex_corners(self):
        a, b, t = Interval(Fraction(-2), Fraction(-1)), Interval(Fraction(1), Fraction(4)), Interval(Fraction(1, 4), Fraction(3, 4))
        result = convex_interval(a, b, t)
        for x in (a.lo, a.hi):
            for y in (b.lo, b.hi):
                for p in (t.lo, (t.lo + t.hi) / 2, t.hi):
                    self.assertTrue(result.contains((1 - p) * x + p * y))


def witnesses():
    try:
        stable_hermite_tt(2, 0, Fraction(1, 10**100))
    except ArithmeticError as error:
        assert str(error) == "source polynomial restriction outside [0,1]"
        old_failure = str(error)
    else:
        raise AssertionError("Frozen predecessor failure unexpectedly changed")
    records = [actual_pipeline(2, 0, Fraction(1, 10**100), circuit=True),
               actual_pipeline(3, 1, Fraction(1), circuit=True),
               actual_pipeline(8, 8, Fraction(10)),
               actual_pipeline(4, 0, Fraction(1000)),
               actual_pipeline(2, 0, Fraction(1, 10), circuit=True, sign=-1)]
    return {"task": "SP-HERMITE-POLY-002", "kind": "actual_offset_successor_diagnostics",
            "records": records, "old_fixed_digit_failure_preserved": True,
            "unpatched_old_failure": old_failure,
            "global_epsilon_certificate": False}


if __name__ == "__main__":
    if "--witness" in sys.argv:
        print(json.dumps(witnesses(), indent=2, allow_nan=False))
    else:
        unittest.main()
