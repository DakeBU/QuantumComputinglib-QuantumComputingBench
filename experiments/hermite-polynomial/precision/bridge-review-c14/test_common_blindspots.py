"""Exact small discriminators; not a quantum ROOT certificate."""
from fractions import Fraction as F
import unittest


def matvec(matrix, vector):
    return tuple(sum((entry * value for entry, value in zip(row, vector)), F())
                 for row in matrix)


def norm_sq(vector):
    return sum((value * value for value in vector), F())


class CommonBlindspots(unittest.TestCase):
    def test_scalar_width_is_not_global_euclidean_error(self):
        scalar_budget = F(1, 10)
        full_error_sq = norm_sq((scalar_budget,) * 4)
        self.assertEqual(full_error_sq, F(1, 25))
        self.assertGreater(full_error_sq, scalar_budget * scalar_budget)

    def test_stage_midpoint_not_product_of_midpoints(self):
        interval_midpoint = (F(0) + F(2)) / 2
        product_interval_midpoint = (F(0) + F(4)) / 2
        self.assertEqual(interval_midpoint * interval_midpoint, F(1))
        self.assertEqual(product_interval_midpoint, F(2))
        self.assertNotEqual(product_interval_midpoint, interval_midpoint * interval_midpoint)

    def test_textual_decimal_is_not_binary64_parser_value(self):
        self.assertNotEqual(F('0.1'), F.from_float(float('0.1')))

    def test_signed_surrogate_amplification(self):
        matrix = ((F(1), F(-1)), (F(1), F(1)))
        once = matvec(matrix, (F(1), F(0)))
        twice = matvec(matrix, once)
        self.assertEqual(norm_sq(once), F(2))
        self.assertEqual(norm_sq(twice), F(4))

    def test_projected_data_does_not_erase_garbage_error(self):
        target, full_output = (F(1), F(0)), (F(1), F(1))
        self.assertEqual(full_output[0] - target[0], F(0))
        self.assertEqual(norm_sq(tuple(y - x for x, y in zip(target, full_output))), F(1))


if __name__ == '__main__':
    unittest.main(verbosity=2)
