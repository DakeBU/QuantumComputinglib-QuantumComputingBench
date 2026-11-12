"""Small exact witness: literal midpoint surrogates need not be unitary."""
from fractions import Fraction as F
import unittest
from test_stage_discriminators import pair_interpreter

class StageSurrogateWitness(unittest.TestCase):
    def test_literal_midpoint_can_expand(self):
        _,a,r=pair_interpreter(1,[('ry',F(2),0)],1,3)
        self.assertEqual(a,[[F(1),F(-1)],[F(1),F(1)]])
        gram=[[sum((a[k][i]*a[k][j] for k in range(2)),F()) for j in range(2)] for i in range(2)]
        self.assertEqual(gram,[[F(2),F()],[F(),F(2)]])
        self.assertNotEqual(gram,[[F(1),F()],[F(),F(1)]])
        self.assertEqual(r,F(1,2))

if __name__=='__main__':
    unittest.main()
