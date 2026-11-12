"""Finite exact-rational diagnostics, not a Python/Lean refinement theorem."""
from fractions import Fraction as F
from pathlib import Path
import re
import sys
import unittest

HERE = Path(__file__).resolve().parent
PRECISION = HERE.parent
sys.path.insert(0, str(PRECISION / 'finite-trig'))
sys.path.insert(0, str(PRECISION / 'saved-action'))
from finite_trig import at_degree, exact_decimal, dyadic_outward
from saved_action import finite_trig, MeasuredWork


def midpoint(theta, degree):
    e = at_degree(theta / 2, degree)
    return ((e.cos_center, -e.sin_center), (e.sin_center, e.cos_center))


def lifted_entry(theta, degree, target, row, col):
    if row & ~(1 << target) != col & ~(1 << target):
        return F()
    return midpoint(theta, degree)[(row >> target) & 1][(col >> target) & 1]


class SavedRyIntervalTests(unittest.TestCase):
    def test_half_angle_and_signed_entries(self):
        self.assertEqual(midpoint(F(1), 1), ((F(1), F(-1, 2)), (F(1, 2), F(1))))
        self.assertEqual(midpoint(F(-1), 1), ((F(1), F(1, 2)), (F(-1, 2), F(1))))
        self.assertNotEqual(midpoint(F(1), 1)[1][0], F(1))

    def test_zero_all_sampled_degrees(self):
        for n in range(33):
            self.assertEqual(midpoint(F(), n), ((F(1), F()), (F(), F(1))))
            self.assertEqual(at_degree(F(), n).radius, F())

    def test_physical_q0_q1_q2(self):
        for target in range(3):
            for source in range(8):
                destination = source ^ (1 << target)
                sign = -1 if source & (1 << target) else 1
                self.assertEqual(lifted_entry(F(1), 1, target, destination, source), F(sign, 2))
        self.assertEqual(lifted_entry(F(1), 1, 0, 2, 0), F())

    def test_cx_exact_permutation(self):
        perm = [i ^ 2 if i & 1 else i for i in range(4)]
        self.assertEqual(perm, [0, 3, 2, 1])
        self.assertEqual([perm[perm[i]] for i in range(4)], list(range(4)))

    def test_actual_fixture_exact_tokens_and_finite_supplier(self):
        qasm = (PRECISION / 'saved-action' / 'fixture-n3-k1-L1' / 'saved.qasm').read_text('ascii')
        tokens = re.findall(r'ry\(([^)]*)\)', qasm)
        self.assertTrue(tokens)
        self.assertEqual(exact_decimal(tokens[0]), F(-86958955523179937, 100000000000000000))
        for token in sorted(set(tokens)):
            theta = exact_decimal(token)
            e = at_degree(theta / 2, 96)
            sine, cosine, radius = finite_trig(theta / 2, MeasuredWork())
            self.assertEqual(radius, e.radius)
            self.assertEqual((sine.lo, sine.hi), dyadic_outward(e.sin_bounds))
            self.assertEqual((cosine.lo, cosine.hi), dyadic_outward(e.cos_bounds))
            # Saved action's outward-rounded primitive center is not silently
            # identified with the exact Taylor-polynomial midpoint.
            self.assertLessEqual(sine.lo, e.sin_center)
            self.assertLessEqual(e.sin_center, sine.hi)


if __name__ == '__main__':
    unittest.main()
