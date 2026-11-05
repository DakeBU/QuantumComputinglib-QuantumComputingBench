"""Bounded diagnostics for the isolated scaled candidate, not family proof."""
from decimal import Decimal, localcontext
from fractions import Fraction
import math
from pathlib import Path
import sys
import unittest
from unittest import mock
import warnings

import numpy as np

from mps_core_probe import TT, right_canonicalize
from mps_ry_compiler import compile_mps
from mps_stable_cores import stable_hermite_tt
from scaled_canonicalize import ScaledNorm, scaled_right_canonicalize

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mass"))
from analytic_mass import HermiteMass


class ScaledCanonicalizationTests(unittest.TestCase):
    def test_independent_small_dense_source_and_sign_order(self):
        cases = ((1, 0, "1/10"), (5, 2, "1/2"), (8, 8, "10"), (8, 8, "300"))
        for n, k, length in cases:
            with self.subTest(n=n, k=k, L=length), localcontext() as context:
                context.prec = 120
                source = HermiteMass(k, n, Decimal(Fraction(length).numerator)
                                     / Decimal(Fraction(length).denominator))
                # Independently enumerate only these expressly small cases.
                expected = np.array([float(source.value(j)) for j in range(1 << n)])
                expected_norm = math.hypot(*expected)
                raw, _ = stable_hermite_tt(n, k, Fraction(length))
                original = [core.copy() for core in raw.cores]
                actual, norm = scaled_right_canonicalize(raw)
                np.testing.assert_allclose(actual.small_dense_diagnostic(),
                                           expected / expected_norm, atol=3e-13, rtol=3e-13)
                self.assertLess(np.linalg.norm(actual.small_dense_diagnostic()
                                               - expected / expected_norm), 3e-12)
                self.assertLess(abs(norm.to_float() / expected_norm - 1), 3e-13)
                for before, after in zip(original, raw.cores):
                    np.testing.assert_array_equal(before, after)
                self.assertLessEqual(actual.max_bond, raw.max_bond)

    def test_old_vs_new_overflow_boundary(self):
        for n in (1023, 1024, 1025, 1026):
            with self.subTest(n=n):
                raw, _ = stable_hermite_tt(n, 0, Fraction(1, 100))
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", RuntimeWarning)
                    if n <= 1024:
                        _, old_norm = right_canonicalize(raw)
                        self.assertTrue(math.isfinite(old_norm))
                    else:
                        with self.assertRaisesRegex(ArithmeticError, "no finite positive norm"):
                            compile_mps(raw)
                with mock.patch.object(TT, "small_dense_diagnostic",
                                       side_effect=AssertionError("dense forbidden")), \
                        mock.patch.object(np.linalg, "svd",
                                          side_effect=AssertionError("SVD forbidden")):
                    canonical, norm = scaled_right_canonicalize(raw)
                    self.assertTrue(math.isfinite(norm.log_norm))
                    self.assertLessEqual(canonical.max_bond, raw.max_bond)
                    self.assertAlmostEqual(canonical.squared_norm(), 1, delta=2e-11)
                    # Width-independent source has exp(-pi L) <= g <= 1.
                    self.assertGreaterEqual(norm.log2_norm, n / 2 - math.pi / (100 * math.log(2)) - 2e-11)
                    self.assertLessEqual(norm.log2_norm, n / 2 + 2e-11)
                    self.assertLessEqual(canonical.scalar_count, raw.scalar_count)
                    # This is a spot diagnostic, not all-amplitude acceptance.
                    central = canonical.amplitude(1 << (n - 1))
                    self.assertGreater(central, 0)
                    self.assertAlmostEqual(math.log(central) + norm.log_norm, 0, delta=2e-11)

    def test_larger_cache_only_widths_and_absorption_scaling(self):
        # Exactly represented rank-one product; norm is 2**(n/2), far outside
        # binary64 at these widths. No Hermite cutoff or dense sample table.
        with mock.patch.object(TT, "small_dense_diagnostic",
                               side_effect=AssertionError("dense forbidden")), \
                mock.patch.object(np.linalg, "svd", side_effect=AssertionError("SVD forbidden")):
            for n in (2048, 4096, 8192):
                with self.subTest(n=n):
                    raw = TT([np.ones((1, 2, 1)) for _ in range(n)])
                    canonical, norm = scaled_right_canonicalize(raw)
                    self.assertEqual(canonical.scalar_count, 2 * n)
                    self.assertEqual(canonical.max_bond, 1)
                    self.assertAlmostEqual(norm.log2_norm, n / 2, delta=2e-10)
                    self.assertAlmostEqual(canonical.squared_norm(), 1, delta=3e-11)
                    with self.assertRaises(ArithmeticError):
                        norm.to_float()

    def test_large_hermite_cache_only_beyond_norm_representability(self):
        with mock.patch.object(TT, "small_dense_diagnostic",
                               side_effect=AssertionError("dense forbidden")), \
                mock.patch.object(np.linalg, "svd", side_effect=AssertionError("SVD forbidden")):
            raw, _ = stable_hermite_tt(2049, 0, Fraction(1, 100))
            canonical, norm = scaled_right_canonicalize(raw)
            self.assertTrue(math.isfinite(norm.log_norm))
            self.assertAlmostEqual(canonical.squared_norm(), 1, delta=3e-11)
            self.assertLessEqual(canonical.max_bond, raw.max_bond)
            self.assertLessEqual(canonical.scalar_count, raw.scalar_count)
            central = canonical.amplitude(1 << 2048)
            self.assertGreater(central, 0)  # subnormal at this width, not zero
            self.assertAlmostEqual(math.log(central) + norm.log_norm, 0, delta=3e-11)
            with self.assertRaises(ArithmeticError):
                norm.to_float()

    def test_signed_rank_deficient_nonprefix_and_extreme_scales(self):
        # Only the second internal position carries action; repeated terminal
        # rows are rank deficient. Positive scaling must keep the minus sign.
        first = np.zeros((1, 2, 3))
        first[0, :, 1] = [-2, 3]
        last = np.array([[1., -1.], [1., -1.], [0., 0.]]).reshape(3, 2, 1)
        raw = TT([first, last])
        expected = raw.small_dense_diagnostic()
        actual, norm = scaled_right_canonicalize(raw)
        np.testing.assert_allclose(actual.small_dense_diagnostic(), expected / math.hypot(*expected),
                                   atol=2e-15, rtol=2e-15)
        self.assertAlmostEqual(norm.to_float(), math.hypot(*expected), places=13)
        self.assertEqual(actual.cores[0].shape[2], 2)  # reduced dimensions, not rank=1
        for factor in (1e300, 1e-300, -1e300, -1e-300):
            with self.subTest(factor=factor):
                extreme = TT([np.full((1, 2, 1), factor) for _ in range(3)])
                result, extreme_norm = scaled_right_canonicalize(extreme)
                expected_sign = -1 if factor < 0 else 1
                np.testing.assert_allclose(result.small_dense_diagnostic(),
                                           np.full(8, expected_sign / math.sqrt(8)), atol=2e-15)
                self.assertAlmostEqual(extreme_norm.log_norm,
                                       3 * math.log(abs(factor)) + 1.5 * math.log(2), delta=1e-11)
                with self.assertRaises(ArithmeticError):
                    extreme_norm.to_float()

    def test_zero_empty_bond_nonfinite_complex_and_normalizer_rejection(self):
        zero = TT([np.zeros((1, 2, 1))])
        with self.assertRaisesRegex(ArithmeticError, "stored-zero"):
            scaled_right_canonicalize(zero)
        cancellation = TT([np.array([1., -1., 1., -1.]).reshape(1, 2, 2),
                           np.array([1., 0., 1., 0.]).reshape(2, 2, 1)])
        np.testing.assert_array_equal(cancellation.small_dense_diagnostic(), np.zeros(4))
        with self.assertRaisesRegex(ArithmeticError, "stored-zero"):
            scaled_right_canonicalize(cancellation)
        empty = TT([np.empty((1, 2, 0)), np.empty((0, 2, 1))])
        with self.assertRaisesRegex(ArithmeticError, "zero-sized"):
            scaled_right_canonicalize(empty)
        for bad in (math.nan, math.inf, -math.inf):
            with self.subTest(bad=bad), self.assertRaisesRegex(ArithmeticError, "nonfinite"):
                scaled_right_canonicalize(TT([np.array([bad, 1]).reshape(1, 2, 1)]))
        with self.assertRaisesRegex(ValueError, "real cores"):
            scaled_right_canonicalize(TT([np.ones((1, 2, 1), dtype=complex)]))
        for mantissa in (0, 1, math.nan, math.inf):
            with self.subTest(mantissa=mantissa), self.assertRaises(ValueError):
                ScaledNorm(mantissa, 0)


if __name__ == "__main__":
    unittest.main()
