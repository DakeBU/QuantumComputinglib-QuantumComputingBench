"""Read-only finite actual local-carrier diagnostic; no filesystem output."""
import sys
from pathlib import Path
from fractions import Fraction
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'saved-action'))
from saved_action import MeasuredWork, stage_surrogates


class ActualLocalCarrier(unittest.TestCase):
    def test_actual_empty_stage_local_width(self):
        n, a = 12, 2
        manifest = {'n': n, 'ancillas': a,
                    'stage_spans': [{'start': 0, 'count': 0} for _ in range(n)]}
        work = MeasuredWork()
        matrices, stages, sigma = stage_surrogates([], manifest, work)
        self.assertEqual(len(matrices), n)
        self.assertEqual(work.peak_local_matrix_entries, 64)
        for matrix in matrices:
            self.assertEqual(len(matrix), 8)
            self.assertEqual(matrix, [[Fraction(i == j) for j in range(8)]
                                      for i in range(8)])
        self.assertTrue(all(Fraction(stage['eta']) == 0 for stage in stages))
        self.assertEqual(sigma, 0)
        self.assertNotEqual(work.peak_local_matrix_entries, 4**(n+a))
        print('actual stage_surrogates: n12,a2,12 local8x8 matrices,peak64,eta0; '
              'routine-only, not parser/full global circuit/runtime refinement')


if __name__ == '__main__':
    unittest.main()
