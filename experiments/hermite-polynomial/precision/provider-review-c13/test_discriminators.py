"""Independent finite exact discriminators; not cross-language refinement proofs."""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "finite-trig"))
from finite_trig import at_degree, enclose, dyadic_outward, LimitReached


def ceil_q(q):
    return -((-q.numerator) // q.denominator)


def log_terms(length, eps):
    threshold = max(1, ceil_q(20 * length / eps))
    return (threshold - 1).bit_length() + 1


def machin(m):
    def partial(q):
        return sum((Q((-1)**i, (2*i+1)*q**(2*i+1))
                    for i in range(m)), Q(0))
    return 16 * partial(5) - 4 * partial(239)


class ReviewDiscriminators(unittest.TestCase):
    def test_signed_recurrence_exact_formula(self):
        for q in [Q(-1000), Q(-123,7), Q(-3), Q(-1,10**100), Q(0), Q(1,7), Q(1000)]:
            for n in [0,1,2,3,7,25,56]:
                r = at_degree(q,n)
                s = sum((Q(1 if i%4==1 else -1 if i%4==3 else 0)
                         *q**i/factorial(i) for i in range(n+1)), Q(0))
                c = sum((Q(1 if i%4==0 else -1 if i%4==2 else 0)
                         *q**i/factorial(i) for i in range(n+1)), Q(0))
                self.assertEqual((r.sin_center,r.cos_center,r.radius),
                                 (s,c,abs(q)**(n+1)/factorial(n+1)))
                self.assertLessEqual(r.sin_bounds[0],r.sin_bounds[1])
                self.assertLessEqual(r.cos_bounds[0],r.cos_bounds[1])

    def test_cap_is_not_uniform_success(self):
        with self.assertRaises(LimitReached):
            enclose(Q(1000),Q(1,2**80),max_degree=128)
        for eps in [Q(-1),Q(-1,10**100)]:
            with self.assertRaises(ValueError):
                enclose(Q(0),eps)

    def test_outward_radius_not_raw_radius(self):
        raw = at_degree(Q(1,3),2)
        lo,hi = dyadic_outward(raw.sin_bounds,3)
        self.assertGreater(hi-lo,raw.width)
        self.assertLessEqual(hi-lo,raw.width+Q(2,2**3))

    def test_machin_count_budgets_and_endpoint_order(self):
        for length in [Q(1,10**100),Q(1,7),Q(1),Q(10**100)]:
            for eps in [length*100,length*20,length*10,length*5,length/1000,length/Q(10**10)]:
                m=log_terms(length,eps)
                err=Q(20,2**m)*length
                r=machin(m)*length
                self.assertGreater(r,0)
                self.assertLessEqual(err,eps)
                self.assertLessEqual(r-err,r+err)
        self.assertEqual([log_terms(Q(1),Q(e)) for e in [100,20,10,5]], [1,1,2,3])
        self.assertEqual(machin(1),Q(3804,1195))
        self.assertEqual(log_terms(Q(10**100),Q(1,10**100)),670)

    def test_noncommuting_chronology_and_amplification(self):
        # Orthogonal nominal stages: swap then sign flip. Correct order is B*A.
        a=((Q(0),Q(1)),(Q(1),Q(0)))
        b=((Q(1),Q(0)),(Q(0),Q(-1)))
        def apply(m,v):
            return tuple(sum((m[i][j]*v[j] for j in range(2)),Q(0)) for i in range(2))
        x=(Q(1),Q(2))
        self.assertEqual(apply(b,apply(a,x)),(Q(2),Q(-1)))
        self.assertEqual(apply(a,apply(b,x)),(Q(-2),Q(1)))
        self.assertNotEqual(apply(b,apply(a,x)),apply(a,apply(b,x)))
        self.assertEqual(Q(11,10)**2-1,Q(21,100))
        self.assertGreater(Q(11,10)**2-1,2*Q(1,10))


if __name__ == "__main__":
    unittest.main()
