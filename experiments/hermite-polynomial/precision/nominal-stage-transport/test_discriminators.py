"""Independent small exact-rational screens; not arbitrary-width Lean evidence."""
from fractions import Fraction as F
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'saved-stage-interpreter'))
from test_saved_stage import interpret

def identity(width):
    return [[F(i == j) for j in range(2**width)] for i in range(2**width)]

def multiply(a, b):
    return [[sum((x*y for x,y in zip(row,col)), F())
             for col in zip(*b)] for row in a]

def transpose(a):
    return [list(row) for row in zip(*a)]

def independent_gate(width, gate):
    """Bits are tuples of named wires; enumerate pair updates, not output routing."""
    a = identity(width)
    if gate[0] == 'cx':
        _, c, t = gate
        for j in range(2**width):
            bits = [(j // 2**q) % 2 for q in range(width)]
            if bits[c]:
                bits[t] = 1 - bits[t]
            i = sum(b * 2**q for q,b in enumerate(bits))
            for row in range(2**width):
                a[row][j] = F(row == i)
        return a
    _, cosine, sine, target = gate
    for j in range(2**width):
        if (j // 2**target) % 2 == 0:
            k = j + 2**target
            a[j][j], a[j][k] = cosine, -sine
            a[k][j], a[k][k] = sine, cosine
    return a

def independent_word(width, word):
    a = identity(width)
    for g in word:
        a = multiply(independent_gate(width,g), a)
    return a

WORD = [('ry', F(3,5), F(-4,5), 0), ('cx',0,2),
        ('ry', F(5,13), F(12,13), 2), ('cx',2,1)]

class Discriminators(unittest.TestCase):
    def test_full_signed_norm_spectator(self):
        a = independent_word(4, WORD)
        self.assertEqual(multiply(transpose(a),a), identity(4))
        self.assertEqual(a[:8], [row[:8] + [F()]*8 for row in independent_word(3,WORD)])
        # A normalization/Gram screen alone would not protect relative signs.
        wrong = [('ry',g[1],-g[2],g[3]) if g[0]=='ry' else g for g in WORD]
        self.assertNotEqual(a, independent_word(4,wrong))

    def test_control_direction_and_chronology(self):
        a = independent_word(3,WORD)
        reverse = list(reversed(WORD))
        swapped = [('cx',g[2],g[1]) if g[0]=='cx' else g for g in WORD]
        self.assertNotEqual(a, independent_word(3,reverse))
        self.assertNotEqual(a, independent_word(3,swapped))
        self.assertEqual(independent_gate(3,('cx',0,2))[5][1], 1)
        self.assertEqual(independent_gate(3,('cx',2,0))[5][1], 0)

    def test_width_zero_and_identity(self):
        self.assertEqual(independent_word(0,[]), [[F(1)]])
        self.assertEqual(independent_word(3,[('cx',0,2)]*2), identity(3))

    def test_expanding_actual_interval_surrogate(self):
        _, center, radius = interpret(1,[('ry',F(2),0)],1,3)
        self.assertEqual(center, [[F(1),F(-1)],[F(1),F(1)]])
        self.assertEqual(multiply(transpose(center),center), [[F(2),F(0)],[F(0),F(2)]])
        self.assertGreater(2*radius,F())
        # Multiplicative growth genuinely exceeds the additive eta sum.
        eta = 2*radius
        self.assertGreater((1+eta)**2-1,2*eta)

    def test_actual_stage_end_chronological_composition(self):
        first = [('ry',F(-9,7),0),('cx',0,2)]
        second = [('ry',F(5,3),2),('cx',2,1)]
        _, a, _ = interpret(3,first,3,4)
        _, b, _ = interpret(3,second,3,4)
        self.assertNotEqual(multiply(b,a),multiply(a,b))
        _, full, _ = interpret(3,first+second,3,4)
        # Stage midpoint product differs from taking one final full-word midpoint.
        self.assertNotEqual(multiply(b,a),full)

if __name__ == '__main__':
    unittest.main()
