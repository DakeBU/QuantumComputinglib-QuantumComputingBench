"""Independent exact finite middle witnesses, not global error or cost proofs."""
from fractions import Fraction as F
from itertools import product
from math import ceil, comb, factorial
import unittest

def a_direct(k,i):
    return sum((F(comb(k+i-m,k),factorial(m)) for m in range(i+1)),F())

def a_cleared(k,i):
    return F(sum(comb(k+i-m,k)*(factorial(k)//factorial(m)) for m in range(i+1)),factorial(k))

def A(k,t):
    return sum((a_direct(k,i)*t**i for i in range(k+1)),F())

def endpoint(k,t):
    return (1-t)**(k+1)*A(k,t)

def middle(k,e,p):
    return e*endpoint(k,p+1)+endpoint(k,-p)

def original_coordinate(k,e,p):
    t=p+1
    return e*(1-t)**(k+1)*sum((a_cleared(k,i)*t**i for i in range(k+1)),F())+t**(k+1)*sum((a_cleared(k,i)*(1-t)**i for i in range(k+1)),F())

def allocated_midpoint(delta):
    # Literal rational mathematical producer, independently reconstructed.
    inverse=F(1)/delta if delta else F()
    T=(max(1,ceil(inverse))-1).bit_length()
    n=4*T*T+2*T+1
    if F(-1)<=-T:
        lo,hi=F(),F(1,2**T)
    else:
        q=F(-1)
        p=sum((q**i/factorial(i) for i in range(n+1)),F())
        r=abs(q)**(n+1)/factorial(n+1)
        lo,hi=p-r,p+r
    return (lo+hi)/2,(lo,hi),T,n

class MiddleDiscriminators(unittest.TestCase):
    def test_valid_coefficients_and_invalid_index_cast(self):
        for k in list(range(13))+[20,32]:
            for i in range(k+1):
                self.assertEqual(a_direct(k,i),a_cleared(k,i))
                for m in range(i+1):
                    self.assertEqual(factorial(k)%factorial(m),0)
        self.assertEqual(a_cleared(0,2),F(2))
        self.assertEqual(a_direct(0,2),F(5,2))
        self.assertNotEqual(a_cleared(0,2),a_direct(0,2))
        self.assertEqual([a_direct(3,i) for i in range(4)],[F(1),F(5),F(29,2),F(193,6)])

    def test_original_coordinate_asymmetric_and_endpoints(self):
        values=[F(-1),F(-9,10),F(-2,3),F(-1,3),F()]
        for k,e,p in product([0,1,2,3,7,12],[F(-1,7),F(),F(1,2),F(1)],values):
            self.assertEqual(middle(k,e,p),original_coordinate(k,e,p))
        for k,e in product(list(range(13))+[20,32],[F(-1,7),F(),F(1,2),F(1)]):
            self.assertEqual(middle(k,e,F()),F(1))
            self.assertEqual(middle(k,e,F(-1)),e)
        e=F(1,2)
        self.assertEqual(middle(1,e,F(-1,3)),F(19,18))
        self.assertEqual(middle(1,e,F(-2,3)),F(7,9))
        self.assertNotEqual(middle(1,e,F(-1,3)),middle(1,e,F(-2,3)))
        for p in values:
            self.assertEqual(middle(0,e,p),e*(-p)+p+1)

    def test_actual_allocation_clipping_and_invalid_delta(self):
        e,I,T,n=allocated_midpoint(F(2))
        self.assertEqual((e,I,T,n),(F(1,2),(F(),F(1)),0,1))
        self.assertNotEqual(e,F())
        self.assertEqual(middle(0,e,F(-1,2)),F(3,4))
        e,I,T,n=allocated_midpoint(F(1,1000))
        self.assertEqual((T,n),(10,421))
        self.assertTrue(I[1]-I[0]<=F(1,1000))
        self.assertTrue(0<e<1)
        for delta in [F(),F(-1),F(2),F(1,1000)]:
            e,*_=allocated_midpoint(delta)
            for k in [0,1,3,10,20]:
                self.assertEqual(middle(k,e,F()),F(1))
        # Invalid delta retains algebraic central identity, not a valid error budget.
        self.assertFalse(F()>0)

    def test_amplification_and_global_metric(self):
        for k,t in product([0,1,2,3,7,12],[F(),F(1,100),F(1,10),F(1,3),F(2,3),F(1)]):
            B=F((k+1)**2*2**(2*k))
            self.assertTrue(0<=A(k,t)<=B)
            self.assertTrue(0<=endpoint(k,t)<=B)
            e1,e2=F(1,3),F(2,5)
            p=t-1
            self.assertEqual(middle(k,e1,p)-middle(k,e2,p),(e1-e2)*endpoint(k,t))
        self.assertEqual(endpoint(1,F(1,10)),F(1053,1000))
        self.assertGreater(endpoint(1,F(1,10)),1)
        e=F(1,10)
        self.assertGreater(sum([e*e]*4,F()),e*e)
        self.assertEqual(sum([e*e]*4,F()),(2*e)**2)

if __name__=='__main__':
    unittest.main()
