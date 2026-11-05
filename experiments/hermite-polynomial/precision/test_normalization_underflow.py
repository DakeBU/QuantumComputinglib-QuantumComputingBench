"""Minimal generic-TT falsifier, NOT Hermite producer/family refutation.

Binary64 input values are interpreted as their exact dyadic Fractions.
No source polynomial, dense constructor, rank truncation, or SVD is involved.
Two cores are necessary for terminal support to hide a max-scaled component.
The only physical action uses the small second internal position.
"""
from fractions import Fraction
import json
from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "mps"))
from mps_core_probe import TT
from scaled_canonicalize import scaled_right_canonicalize


def witness():
    large, small = float("1e308"), float("1e-308")
    first = np.array([large, small, large, small]).reshape(1, 2, 2)
    last = np.array([0.0, 0.0, 1.0, 1.0]).reshape(2, 2, 1)
    raw = TT([first, last])
    # Exact rational contraction of the STORED binary64 inputs.
    exact = [sum((Fraction.from_float(float(first[0, bit0, a]))
                  * Fraction.from_float(float(last[a, bit1, 0]))
                  for a in range(2)), Fraction())
             for bit0 in range(2) for bit1 in range(2)]
    assert all(value == Fraction.from_float(small) > 0 for value in exact)
    assert all(np.isfinite(core).all() for core in raw.cores)
    assert small / large == 0.0
    try:
        scaled_right_canonicalize(raw)
    except ArithmeticError as error:
        assert str(error) == "stored-zero tensor has no normalized state"
        return {
            "scope": "generic two-core nonzero TT; not proved reachable by Hermite producer",
            "failure_class": "REFUTED",
            "retired_claim": "finite nonzero represented TT implies scaled_right_canonicalize success",
            "core_shapes": [[1, 2, 2], [2, 2, 1]],
            "stored_large_hex": large.hex(),
            "stored_small_hex": small.hex(),
            "exact_amplitude": str(exact[0]),
            "exact_squared_norm": str(sum(value * value for value in exact)),
            "exact_normalized_amplitudes": ["1/2"] * 4,
            "initial_scaled_supported_entry": small / large,
            "actual_exception": str(error),
            "minimality": "minimal chain length for this terminal-support mechanism; not minimal dynamic range or bond dimension",
            "next_action": "supply a reachable-core dynamic-range/underflow error bound, or change the representation/scaling mechanism; positivity and finite norm alone are insufficient"
        }
    raise AssertionError("Expected scaled candidate to reject this nonzero exact action")


class UnderflowWitnessTests(unittest.TestCase):
    def test_supported_branch_lost_under_initial_max_scale(self):
        result = witness()
        self.assertEqual(result["initial_scaled_supported_entry"], 0.0)

    def test_one_core_finite_nonzero_has_a_retained_max_entry(self):
        canonical, _ = scaled_right_canonicalize(
            TT([np.array([1e308, 1e-308]).reshape(1, 2, 1)]))
        self.assertGreater(float(np.max(np.abs(canonical.cores[0]))), 0)


if __name__ == "__main__":
    if "--witness" in sys.argv:
        print(json.dumps(witness(), indent=2))
    else:
        unittest.main()
