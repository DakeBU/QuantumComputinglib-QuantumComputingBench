"""Exact finite matrix discrimination, not uniform runtime refinement."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parent / 'saved-action'))
import saved_action as actual

def outward(a, bits):
    grid = 2 ** bits
    return (F(a[0].numerator * grid // a[0].denominator, grid),
            F(-((-a[1].numerator * grid) // a[1].denominator), grid))

def add(a, b):
    return a[0] + b[0], a[1] + b[1]

def neg(a):
    return -a[1], -a[0]

def mul(a, b):
    corners = [x * y for x in a for y in b]
    return min(corners), max(corners)

def trig(theta, degree, bits):
    q = theta / 2
    radius = abs(q) ** (degree + 1) / factorial(degree + 1)
    sine = sum(((-1) ** ((i-1)//2) * q**i / factorial(i)
                for i in range(1, degree+1, 2)), F())
    cosine = sum(((-1) ** (i//2) * q**i / factorial(i)
                  for i in range(0, degree+1, 2)), F())
    return outward((sine-radius, sine+radius), bits), outward((cosine-radius, cosine+radius), bits)

def step(a, g, degree, bits):
    size = len(a)
    if g[0] == 'cx':
        _, control, target = g
        return [list(a[i ^ (1 << target)] if i & (1 << control) else a[i])
                for i in range(size)]
    _, theta, target = g
    sine, cosine = trig(theta, degree, bits)
    # Functional output-row routing differs from producer's in-place pair loop.
    b = []
    mask = 1 << target
    for i in range(size):
        low = i ^ mask if i & mask else i
        high = i if i & mask else i ^ mask
        row = []
        for j in range(size):
            u, v = a[low][j], a[high][j]
            value = add(mul(sine, u), mul(cosine, v)) if i & mask else add(mul(cosine, u), neg(mul(sine, v)))
            row.append(outward(value, bits))
        b.append(row)
    return b

def interpret(width, word, degree=96, bits=80, early=False):
    a = [[(F(i == j), F(i == j)) for j in range(2**width)] for i in range(2**width)]
    for g in word:
        a = step(a, g, degree, bits)
        if early:
            a = [[((lo+hi)/2, (lo+hi)/2) for lo, hi in row] for row in a]
    center = [[(lo+hi)/2 for lo, hi in row] for row in a]
    radius = max((hi-lo)/2 for row in a for lo, hi in row)
    return a, center, radius

WORD = [('ry', F(-9,7), 0), ('cx', 0, 1), ('ry', F(5,3), 1),
        ('cx', 1, 0), ('ry', F(-1,2), 0)]

class FullMatrixTests(unittest.TestCase):
    def test_q0_LSB_changing_targets(self):
        eye = [[(F(i == j),F(i == j)) for j in range(4)] for i in range(4)]
        self.assertEqual(step(eye, ('cx',0,1), 0,0)[1], eye[3])
        self.assertEqual(step(eye, ('cx',1,0), 0,0)[1], eye[1])
        self.assertNotEqual(interpret(2,WORD)[1], interpret(2,[(g[0],g[1],0) if g[0]=='ry' else g for g in WORD])[1])

    def test_actual_fraction_stage_all_entries_and_eta(self):
        physical = [(g[0],g[1],2 if g[2]==0 else 1) if g[0]=='ry'
                    else ('cx',2 if g[1]==0 else 1,2 if g[2]==0 else 1) for g in WORD]
        manifest = {'n':2,'ancillas':1,'stage_spans':[
            {'start':0,'count':len(physical),'data_wire':1},
            {'start':len(physical),'count':0,'data_wire':0}]}
        centers, reports, sigma = actual.stage_surrogates(physical,manifest,actual.MeasuredWork())
        _, expected, radius = interpret(2,WORD)
        self.assertEqual(centers[0], expected)
        self.assertEqual(F(reports[0]['entry_radius']), radius)
        self.assertEqual(F(reports[0]['eta']), 4*radius)
        self.assertEqual(sigma, 4*radius)
        self.assertGreater(radius,F())

    def test_empty_and_exact_CX_involution(self):
        a, center, radius = interpret(2,[])
        b, _, r = interpret(2,[('cx',0,1),('cx',0,1)])
        self.assertEqual(a,b)
        self.assertEqual(radius,F())
        self.assertEqual(r,F())

    def test_chronology_reversal(self):
        self.assertNotEqual(interpret(2,WORD,2,3)[1], interpret(2,list(reversed(WORD)),2,3)[1])

    def test_no_intermediate_midpoint(self):
        word = [('ry',F(-9,7),0),('cx',0,1),('ry',F(-1),1)]
        self.assertNotEqual(interpret(2,word,0,1)[1], interpret(2,word,0,1,True)[1])

if __name__ == '__main__':
    unittest.main()
