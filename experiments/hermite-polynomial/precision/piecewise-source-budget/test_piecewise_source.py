"""Independent finite diagnostics; not a symbolic or runtime certificate."""
from fractions import Fraction as Q
from decimal import Decimal, localcontext
from math import comb, factorial
import unittest

PI = Decimal('3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679')

def dec(q):
    return Decimal(q.numerator)/Decimal(q.denominator)

def cutoff(delta):
    a = max(1, -(-delta.denominator//delta.numerator))
    return (a-1).bit_length()

def enclosure(q, delta):
    t = cutoff(delta)
    d = 4*t*t+2*t+1
    if q <= -t:
        return Q(0), Q(1, 2**t)
    term = Q(1)
    total = term
    for i in range(1, d+1):
        term *= q/i
        total += term
    radius = abs(term*q/(d+1))
    return total-radius, total+radius

def midpoint(q, delta):
    lo, hi = enclosure(q, delta)
    assert hi-lo <= delta
    return (lo+hi)/2

def coefficients(k):
    return [sum((Q(comb(k+i-m, k), factorial(m)) for m in range(i+1)), Q(0)) for i in range(k+1)]

def middle(k, e, p):
    t = p+1
    a = coefficients(k)
    return e*(1-t)**(k+1)*sum((c*t**i for i,c in enumerate(a)), Q(0)) + t**(k+1)*sum((c*(1-t)**i for i,c in enumerate(a)), Q(0))

def literal(k, delta, p):
    if p < -1:
        return midpoint(p, delta)
    if p <= 0:
        return middle(k, midpoint(Q(-1), delta), p)
    return midpoint(-p, delta)

def scientific(k, p):
    if p < -1:
        return p.exp()
    if p > 0:
        return (-p).exp()
    t = p+1
    a = [dec(x) for x in coefficients(k)]
    def power(x,i):
        return Decimal(1) if i == 0 else x**i
    return Decimal(-1).exp()*(1-t)**(k+1)*sum((c*power(t,i) for i,c in enumerate(a)), Decimal(0)) + t**(k+1)*sum((c*power(1-t,i) for i,c in enumerate(a)), Decimal(0))

def radius(k,n,L,eps):
    c = 2*(k+1)**2*2**(3*k)*(2*k+2)*(2*k+1)*2**(2*k+1)
    delta = eps/(8*2**(n+1)*c)
    m = cutoff(delta/(20*L))+1
    def atan(q):
        return sum((Q((-1)**i, (2*i+1)*q**(2*i+1)) for i in range(m)), Q(0))
    return (16*atan(5)-4*atan(239))*L

def normalized(v):
    norm = sum((x*x for x in v), Decimal(0)).sqrt()
    return [x/norm for x in v]

def distance(v,w):
    return sum(((x-y)**2 for x,y in zip(v,w)), Decimal(0)).sqrt()

class PiecewiseDiagnostics(unittest.TestCase):
    def test_owned_endpoints_and_clipped_tail(self):
        for k in (0,1,3,10):
            self.assertEqual(literal(k,Q(2),Q(-1)),Q(1,2))
            self.assertEqual(literal(k,Q(2),Q(0)),Q(1))
            self.assertEqual(literal(k,Q(2),Q(-2)),Q(1,2))
            self.assertEqual(literal(k,Q(2),Q(2)),Q(1,2))
        self.assertEqual(enclosure(Q(-10**100),Q(1,8)),(Q(0),Q(1,8)))
        self.assertEqual(literal(1,Q(1,8),Q(-10**100)),Q(1,16))
        self.assertNotEqual(literal(1,Q(1,8),Q(-10**100)),0)

    def test_asymmetric_middle_and_amplification(self):
        self.assertEqual(literal(1,Q(2),Q(-1,3)),Q(19,18))
        self.assertEqual(literal(1,Q(2),Q(-2,3)),Q(7,9))
        t=Q(1,10)
        factor=(1-t)**2*sum((c*t**i for i,c in enumerate(coefficients(1))),Q(0))
        self.assertEqual(factor,Q(1053,1000))
        self.assertGreater(factor,1)

    def test_full_physical_grid_original_normalized_target(self):
        with localcontext() as ctx:
            ctx.prec=90
            for k,n,L,eps in ((0,0,Q(1,5),Q(1)),(1,1,Q(1),Q(1)),(0,2,Q(4),Q(1,4))):
                N=2**(n+1)
                B=(k+1)**2*2**(2*k)
                delta=eps/(4*N*B)
                R=radius(k,n,L,eps)
                points=[-R+2*R*j/N for j in range(N)]
                self.assertEqual(points[N//2],0)
                self.assertEqual(points[0],-R)
                self.assertLess(points[-1],R)
                for j in range(N):
                    bits=[(j>>q)&1 for q in range(n+1)]
                    self.assertEqual(sum(b*2**q for q,b in enumerate(bits)),j)
                stored=[dec(literal(k,delta,p)) for p in points]
                reference=[scientific(k,dec(p)) for p in points]
                target=[scientific(k,-PI*dec(L)+2*PI*dec(L)*j/N) for j in range(N)]
                self.assertEqual(stored[N//2],1)
                self.assertGreaterEqual(sum((x*x for x in stored),Decimal(0)),1)
                self.assertGreaterEqual(sum((x*x for x in reference),Decimal(0)),1)
                scalar=max(abs(x-y) for x,y in zip(stored,reference))
                self.assertLessEqual(scalar,dec(delta)*B/2)
                self.assertLessEqual(distance(stored,reference),Decimal(N).sqrt()*dec(delta)*B/2)
                self.assertLessEqual(distance(normalized(stored),normalized(reference)),dec(eps)/4)
                self.assertLessEqual(distance(normalized(reference),normalized(target)),dec(eps)/4)
                self.assertLessEqual(distance(normalized(stored),normalized(target)),dec(eps)/2)
                self.assertNotEqual(normalized(reference),normalized(target))
                print(f'full grid k={k},width={n+1},N={N}: scalar={scalar:.3E}; original-state={distance(normalized(stored),normalized(target)):.3E}',flush=True)

    def test_scalar_budget_is_not_vector_budget(self):
        with localcontext() as ctx:
            ctx.prec=50
            self.assertEqual(distance([Decimal(1)]*4,[Decimal(0)]*4),2)
            self.assertEqual(Q(1,4)/(4*8*16),Q(1,2048))

if __name__ == '__main__':
    unittest.main()
