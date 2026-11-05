"""Small independent exact witnesses; no universal runtime/root certificate."""
from fractions import Fraction as F
from itertools import product
from math import ceil, factorial, floor
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'saved-action'))
import saved_action as actual

def round_i(a,bits):
    g=2**bits
    return F(floor(a[0]*g),g),F(ceil(a[1]*g),g)

def corners(a,b):
    values=[x*y for x,y in product(a,b)]
    return min(values),max(values)

def plus(a,b):
    return a[0]+b[0],a[1]+b[1]

def minus(a):
    return -a[1],-a[0]

def center(a):
    return (a[0]+a[1])/2

def trig(theta,n,bits):
    q=theta/2
    sp=sum((F((-1)**((k-1)//2))*q**k/factorial(k) for k in range(1,n+1,2)),F())
    cp=sum((F((-1)**(k//2))*q**k/factorial(k) for k in range(0,n+1,2)),F())
    r=abs(q)**(n+1)/factorial(n+1)
    return round_i((sp-r,sp+r),bits),round_i((cp-r,cp+r),bits)

def row(theta,u,v,n,bits):
    s,c=trig(theta,n,bits)
    return round_i(plus(corners(c,u),minus(corners(s,v))),bits),round_i(plus(corners(s,u),corners(c,v)),bits)

def trace(angles,u,v,n,bits,early_midpoint=False):
    for theta in angles:
        u,v=row(theta,u,v,n,bits)
        if early_midpoint:
            u,v=(center(u),center(u)),(center(v),center(v))
    return u,v

def cutoff(e):
    m=max(1,ceil(1/e)) if e else 1
    return (m-1).bit_length()

def checked(q,e,T,n):
    if q>0 or e<=0:
        return None
    if q<=-T:
        interval=(F(),F(1,2**T))
    else:
        p=sum((q**k/factorial(k) for k in range(n+1)),F())
        r=abs(q)**(n+1)/factorial(n+1)
        interval=p-r,p+r
    return interval if interval[1]-interval[0]<=e else None

class IndependentDiscriminators(unittest.TestCase):
    def test_clipping_precision_zero_and_allocation(self):
        self.assertEqual(checked(F(-20),F(1,8),3,43),(F(),F(1,8)))
        self.assertNotEqual(checked(F(-20),F(1,8),3,43),(F(),F()))
        for e in [F(),F(-1,8)]:
            self.assertIsNone(checked(F(-20),e,3,43))
        self.assertIsNone(checked(F(1),F(1,8),3,43))
        self.assertEqual((cutoff(F(2)),4*cutoff(F(2))**2+2*cutoff(F(2))+1),(0,1))
        self.assertEqual(checked(F(),F(2),0,1),(F(),F(1)))
        self.assertEqual(4*80**2+2*80+1,25761)
        self.assertEqual(checked(F(-10**1000),F(1,2**80),80,25761),(F(),F(1,2**80)))
        self.assertIsNone(checked(F(-1),F(1,1000),10,0))

    def test_signed_grid_and_product_center(self):
        for q,bits in product([F(-1,10),F(-5,7),F(0),F(3,8)], [0,1,7,80]):
            got=actual.outward(actual.Interval(q,q),actual.MeasuredWork(),bits)
            self.assertEqual((got.lo,got.hi),round_i((q,q),bits))
            self.assertTrue(q-F(1,2**bits)<got.lo<=q<=got.hi<q+F(1,2**bits))
        self.assertEqual(round_i((F(-1,10),F(-1,10)),0),(F(-1),F()))
        self.assertEqual(int(F(-1,10)),0)
        a,b=(F(-2),F(3)),(F(-4),F(5))
        got=actual.times(actual.Interval(*a),actual.Interval(*b),actual.MeasuredWork())
        self.assertEqual((got.lo,got.hi),(F(-12),F(15)))
        self.assertNotEqual(center((got.lo,got.hi)),center(a)*center(b))

    def test_half_angle_sign_and_chronological_rounding(self):
        theta=F(-1)
        s,c=trig(theta,1,3)
        self.assertEqual(s,(F(-5,8),F(-3,8)))
        self.assertEqual(row(theta,(F(1),F(1)),(F(),F()),1,3)[1],s)
        actual_s,actual_c,_=actual.finite_trig(theta/2,actual.MeasuredWork(),1,3)
        self.assertEqual(((actual_s.lo,actual_s.hi),(actual_c.lo,actual_c.hi)),(s,c))
        choices=[F(-1),F(-1,3),F(1,5),F(2,3),F(1)]
        found_reversal=found_early=False
        for a,b,n,bits in product(choices,choices,[1,2,4],[0,2,3]):
            uv=trace([a,b],(F(1),F(1)),(F(),F()),n,bits)
            if uv!=trace([b,a],(F(1),F(1)),(F(),F()),n,bits):
                found_reversal=True
            if tuple(map(center,uv))!=tuple(map(center,trace([a,b],(F(1),F(1)),(F(),F()),n,bits,True))):
                found_early=True
            if found_reversal and found_early:
                break
        self.assertTrue(found_reversal,'Rounded chronology must not be replaced by commuting exact RY claim')
        self.assertTrue(found_early,'End interval midpoint must not be replaced by products of intermediate centers')

    def test_scalar_not_global_norm(self):
        e=F(1,10)
        squared=sum((e*e for _ in range(4)),F())
        self.assertEqual(squared,(2*e)**2)
        self.assertGreater(squared,e**2)

if __name__=='__main__':
    unittest.main()
