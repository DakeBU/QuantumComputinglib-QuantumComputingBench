"""Exact finite comparisons with immutable saved_action.py; not formal refinement."""
from decimal import Decimal
from fractions import Fraction as F
from itertools import product
from math import floor, ceil, factorial
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'saved-action'))
import saved_action as actual


def rounded(p, bits):
    g = 2 ** bits
    return F(floor(p[0]*g), g), F(ceil(p[1]*g), g)


def mul(a, b):
    ps = [x*y for x,y in product(a,b)]
    return min(ps), max(ps)


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def neg(a):
    return -a[1], -a[0]


def trig(theta, degree, bits):
    x = theta/2
    s = sum(((-1)**((i-1)//2)*x**i/F(factorial(i)) for i in range(degree+1) if i%2), F())
    c = sum(((-1)**(i//2)*x**i/F(factorial(i)) for i in range(degree+1) if not i%2), F())
    r = abs(x)**(degree+1)/F(factorial(degree+1))
    return rounded((s-r,s+r),bits), rounded((c-r,c+r),bits),r


def row(theta, u, v, degree=96, bits=80):
    s,c,_ = trig(theta,degree,bits)
    return rounded(add(mul(c,u),neg(mul(s,v))),bits), rounded(add(mul(s,u),mul(c,v)),bits)


def pair(a):
    return a.lo,a.hi


class ExactSavedRoundingTests(unittest.TestCase):
    def test_signed_floor_ceil_grid(self):
        values = [F(Decimal('-0.86958955523179937')), F(-1,10),F(0),F(3,8),F(-3,8),F(5,7)]
        for bits in [0,1,3,80]:
            for lo,hi in product(values,repeat=2):
                if lo>hi:
                    continue
                with self.subTest(bits=bits,lo=str(lo),hi=str(hi)):
                    got = pair(actual.outward(actual.Interval(lo,hi),actual.MeasuredWork(),bits))
                    self.assertEqual(got,rounded((lo,hi),bits))
                    self.assertTrue(lo-F(1,2**bits)<got[0]<=lo<=hi<=got[1]<hi+F(1,2**bits))
        self.assertEqual(rounded((F(-1,10),F(1,5)),0),(F(-1),F(1)))

    def test_all_product_signs_and_cancellation(self):
        intervals = [(F(-4),F(-2)),(F(-2),F(3)),(F(0),F(0)),(F(1),F(5)),(F(-1,3),F(-1,3))]
        for a,b in product(intervals,repeat=2):
            w = actual.MeasuredWork()
            aa,bb = actual.Interval(*a),actual.Interval(*b)
            self.assertEqual(pair(actual.times(aa,bb,w)),mul(a,b))
            self.assertEqual(pair(actual.plus(aa,bb,w)),add(a,b))
            self.assertEqual(pair(actual.negative(aa)),neg(a))
            p = pair(actual.times(aa,bb,w))
            for x,y in product([a[0],sum(a)/2,a[1]],[b[0],sum(b)/2,b[1]]):
                self.assertTrue(p[0]<=x*y<=p[1])
        a = actual.Interval(F(-1,3),F(-1,3))
        self.assertEqual(pair(actual.plus(a,actual.negative(a),actual.MeasuredWork())),(F(),F()))

    def test_taylor_loop_and_real_row_schedule(self):
        angles = [F(0),F(1,7),F(-1,7),F(Decimal('-0.86958955523179937'))]
        for theta in angles:
            for degree in [0,1,4,96]:
                for bits in [0,80]:
                    s,c,r = actual.finite_trig(theta/2,actual.MeasuredWork(),degree,bits)
                    self.assertEqual((pair(s),pair(c),r),trig(theta,degree,bits))
        for theta,u,v in product(angles,[(F(-2),F(3)),(F(1),F(1))],[(F(-1),F(-1)),(F(),F())]):
            w = actual.MeasuredWork()
            s,c,_ = actual.finite_trig(theta/2,w)
            aa,bb = actual.Interval(*u),actual.Interval(*v)
            p = actual.outward(actual.plus(actual.times(c,aa,w),actual.negative(actual.times(s,bb,w)),w),w)
            q = actual.outward(actual.plus(actual.times(s,aa,w),actual.times(c,bb,w),w),w)
            self.assertEqual((pair(p),pair(q)),row(theta,u,v))

    def test_actual_stage_cx_and_end_only_midpoint(self):
        angles = [F(-1,7),F(2,9),F(Decimal('-0.86958955523179937'))]
        gates = [('ry',angles[0],1),('cx',1,0),('ry',angles[1],0),('ry',angles[2],1)]
        manifest = {'n':1,'ancillas':1,'stage_spans':[{'start':0,'count':len(gates),'data_wire':0}]}
        centers,reports,_ = actual.stage_surrogates(gates,manifest,actual.MeasuredWork())
        size = 4
        matrix = [[(F(i==j),F(i==j)) for j in range(size)] for i in range(size)]
        for op,angle_or_control,wire in gates:
            # Physical ancilla q1 maps to local low bit0, data q0 to local bit1.
            target = 0 if wire==1 else 1
            if op=='cx':
                control = 0 if angle_or_control==1 else 1
                matrix = [matrix[i^(1<<target)] if i&(1<<control) else matrix[i] for i in range(size)]
            else:
                for i in range(size):
                    if i&(1<<target):
                        continue
                    j = i|(1<<target)
                    rows = [row(angle_or_control,matrix[i][k],matrix[j][k]) for k in range(size)]
                    matrix[i] = [p for p,q in rows]
                    matrix[j] = [q for p,q in rows]
        expected = [[sum(p)/2 for p in r] for r in matrix]
        radius = max((hi-lo)/2 for r in matrix for lo,hi in r)
        self.assertEqual(centers,[expected])
        self.assertEqual(F(reports[0]['entry_radius']),radius)
        self.assertEqual(F(reports[0]['eta']),size*radius)
        self.assertFalse(reports[0]['surrogate_unitarity_assumed'])


if __name__=='__main__':
    unittest.main()
