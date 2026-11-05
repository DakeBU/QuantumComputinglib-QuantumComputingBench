"""Entry-contract regressions, not family state-preparation acceptance."""
from fractions import Fraction
import unittest
from unittest.mock import patch

import numpy as np

from checked_entry import offset_hermite_tt_checked
from offset_source import offset_hermite_tt


class CheckedEntryTests(unittest.TestCase):
    def test_invalid_budgets_never_call_delegate(self):
        budgets = [Fraction(0), Fraction(-1), 0.0, 1.0, True, False,
                   float("inf"), float("nan"), "1/100", None]
        for length in (Fraction(1, 10), Fraction(1000)):
            for budget in budgets:
                with self.subTest(L=length, budget=repr(budget)):
                    with patch("checked_entry._frozen_constructor") as delegate:
                        with self.assertRaisesRegex(ValueError, "local tolerance"):
                            offset_hermite_tt_checked(4, 0, length, budget)
                        delegate.assert_not_called()

    def test_invalid_dimensions_never_call_delegate(self):
        for n, k in [(0, 0), (-1, 0), (True, 0), (2.0, 0), (2, -1),
                     (2, False), (2, 0.0), ("2", 0), (2, None)]:
            with self.subTest(n=n, k=k):
                with patch("checked_entry._frozen_constructor") as delegate:
                    with self.assertRaises(ValueError):
                        offset_hermite_tt_checked(n, k, Fraction(1))
                    delegate.assert_not_called()

    def test_invalid_lengths_never_call_delegate(self):
        for length in (Fraction(0), Fraction(-1), 1.0, 1, True, None):
            with self.subTest(L=length):
                with patch("checked_entry._frozen_constructor") as delegate:
                    with self.assertRaisesRegex(ValueError, "rational L"):
                        offset_hermite_tt_checked(2, 0, length)
                    delegate.assert_not_called()

    def test_valid_delegate_called_once_and_identity_preserved(self):
        original_return = (object(), {"global_epsilon_certificate": False})
        budget = Fraction(1, 10**10000)
        with patch("checked_entry._frozen_constructor", return_value=original_return) as delegate:
            returned = offset_hermite_tt_checked(64, 8, Fraction(1, 7), budget)
        self.assertIs(returned, original_return)
        delegate.assert_called_once_with(64, 8, Fraction(1, 7), budget)

    def test_frozen_zero_injection_bypass_retained_and_checked_entry_rejects(self):
        for invalid in (Fraction(0), Fraction(-1), 0.0):
            _, metadata = offset_hermite_tt(4, 0, Fraction(1000), invalid)
            self.assertEqual(metadata["polynomial_certificates"], [])
            self.assertIs(metadata["global_epsilon_certificate"], False)
            with self.assertRaises(ValueError):
                offset_hermite_tt_checked(4, 0, Fraction(1000), invalid)

    def test_actual_valid_core_bytes_and_metadata_unchanged(self):
        for n, k, length in [(2, 0, Fraction(1, 10**100)), (3, 1, Fraction(1)),
                             (4, 0, Fraction(1000))]:
            with self.subTest(n=n, k=k, L=length):
                old, old_metadata = offset_hermite_tt(n, k, length)
                new, new_metadata = offset_hermite_tt_checked(n, k, length)
                self.assertEqual(len(old.cores), len(new.cores))
                for a, b in zip(old.cores, new.cores):
                    self.assertEqual(a.dtype, b.dtype)
                    self.assertEqual(a.shape, b.shape)
                    self.assertEqual(a.tobytes(), b.tobytes())
                    self.assertTrue(np.array_equal(a, b))
                self.assertEqual(old_metadata, new_metadata)

    def test_actual_unattainable_positive_tolerance_failure_propagates(self):
        for constructor in (offset_hermite_tt, offset_hermite_tt_checked):
            with self.assertRaisesRegex(ArithmeticError, "local coefficient tolerance not met"):
                constructor(2, 0, Fraction(1, 10), Fraction(1, 10**40))

    def test_exception_identity_preserved(self):
        failure = ArithmeticError("frozen supplier failed")
        with patch("checked_entry._frozen_constructor", side_effect=failure) as delegate:
            with self.assertRaises(ArithmeticError) as observed:
                offset_hermite_tt_checked(2, 0, Fraction(1))
        self.assertIs(observed.exception, failure)
        delegate.assert_called_once()


if __name__ == "__main__":
    unittest.main()
