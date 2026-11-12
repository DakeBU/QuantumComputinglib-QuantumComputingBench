from fractions import Fraction as Q
from math import factorial
import unittest
from finite_trig import at_degree, enclose, exact_decimal, dyadic_outward, LimitReached


class FiniteTrigTests(unittest.TestCase):
    def test_literal_finite_formulas(self):
        for q in [Q(0), Q(1, 3), Q(-1), Q(8), Q(-123, 7)]:
            for n in [0, 1, 2, 7, 32]:
                actual = at_degree(q, n)
                s = sum(((1 if i % 4 == 1 else -1 if i % 4 == 3 else 0)
                         * q**i / factorial(i) for i in range(n + 1)), Q(0))
                c = sum(((1 if i % 4 == 0 else -1 if i % 4 == 2 else 0)
                         * q**i / factorial(i) for i in range(n + 1)), Q(0))
                self.assertEqual((actual.sin_center, actual.cos_center, actual.radius),
                                 (s, c, abs(q)**(n + 1) / factorial(n + 1)))

    def test_zero_and_signed_symmetry(self):
        z = enclose(Q(0), Q(0), max_degree=0)
        self.assertEqual((z.sin_bounds, z.cos_bounds), ((Q(0), Q(0)), (Q(1), Q(1))))
        for n in [0, 1, 7, 24]:
            p, m = at_degree(Q(3, 7), n), at_degree(Q(-3, 7), n)
            self.assertEqual(p.sin_center, -m.sin_center)
            self.assertEqual(p.cos_center, m.cos_center)
            self.assertEqual(p.radius, m.radius)

    def test_minimal_degree_and_width(self):
        for q in [Q(0), Q(1, 3), Q(-1), Q(8), Q(-8)]:
            for bits in [8, 32, 80]:
                eps = Q(1, 2**bits)
                result = enclose(q, eps)
                self.assertLessEqual(result.width, eps)
                self.assertEqual(result, at_degree(q, result.degree))
                for n in range(result.degree):
                    self.assertGreater(at_degree(q, n).width, eps)

    def test_cap_failure_is_honest(self):
        with self.assertRaises(LimitReached):
            enclose(Q(1000), Q(1, 2**80), max_degree=128)
        with self.assertRaises(LimitReached):
            enclose(Q(1), Q(0), max_degree=128)

    def test_exact_text_not_float_relabel(self):
        for token in ["0", "-0", "3.1415926535897931", "-1.25e-03", ".5", "+2."]:
            self.assertEqual(exact_decimal(token), Q(token))
        self.assertNotEqual(exact_decimal("0.1"), Q.from_float(0.1))
        for token in ["nan", "inf", "1/3", " 1", "1 ", "", "0x1p0"]:
            with self.assertRaises(ValueError):
                exact_decimal(token)
        with self.assertRaises(LimitReached):
            exact_decimal("1e9999999")

    def test_float_rejected(self):
        with self.assertRaises(TypeError):
            enclose(0.1, Q(1, 1000))
        with self.assertRaises(TypeError):
            at_degree(0.1, 20)

    def test_dyadic_outward(self):
        for q in [Q(-8), Q(0), Q(1, 3), Q(8)]:
            p = enclose(q, Q(1, 2**80))
            for bounds in [p.sin_bounds, p.cos_bounds]:
                lo, hi = dyadic_outward(bounds, 80)
                self.assertLessEqual(lo, bounds[0])
                self.assertGreaterEqual(hi, bounds[1])
                self.assertLessEqual(hi - lo, p.width + Q(2, 2**80))


if __name__ == "__main__":
    unittest.main()
