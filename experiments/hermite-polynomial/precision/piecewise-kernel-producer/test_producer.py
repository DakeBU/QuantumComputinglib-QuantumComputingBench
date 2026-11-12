"""Finite exact Fraction diagnostics, never an arbitrary-width certificate."""
import unittest
from fractions import Fraction as Q
from math import comb, factorial
import json
from pathlib import Path
from producer import produce, advance, accept, materialize_and_close

def actual(k,delta,p):
    T=(max(1,-(-delta.denominator//delta.numerator))-1).bit_length()
    d=4*T*T+2*T+1
    def midpoint(q):
        return Q(1,2**(T+1)) if q <= -T else sum((q**i/factorial(i) for i in range(d+1)),Q(0))
    if p < -1:
        return midpoint(p)
    if p > 0:
        return midpoint(-p)
    a=[sum((Q(comb(k+i-h,k),factorial(h)) for h in range(i+1)),Q(0)) for i in range(k+1)]
    return midpoint(Q(-1))*(-p)**(k+1)*sum((z*(p+1)**i for i,z in enumerate(a)),Q(0))+(p+1)**(k+1)*sum((z*(-p)**i for i,z in enumerate(a)),Q(0))

class ProducerTests(unittest.TestCase):
    def test_actual_allocated_radius_and_source_delta(self):
        # Independently reproduce the accepted Machin radius supplier and
        # sourceDelta, not arbitrary substitute data. Full grid only here.
        for width,L,epsilon in ((1,Q(1,5),Q(1)),(3,Q(4),Q(64))):
            k=0
            N=2**width
            radius_constant=Q(8)
            radius_delta=epsilon/(8*N*radius_constant)
            a=max(1,-(-(radius_delta/(20*L)).denominator//(radius_delta/(20*L)).numerator))
            terms=(a-1).bit_length()+1
            def atan(q):
                return sum((Q((-1)**i,(2*i+1)*q**(2*i+1)) for i in range(terms)),Q(0))
            R=(16*atan(5)-4*atan(239))*L
            delta=epsilon/(4*N)
            obj=produce(k,width,R,delta)
            for j in range(N):
                self.assertEqual(obj.amplitude(j),actual(k,delta,-R+2*R*j/N))
            print(f'PASS actual allocation k0,width={width},L={L},epsilon={epsilon},delta={delta},T={obj.cutoff},d={obj.degree},D={obj.dimension}',flush=True)

    def test_saved_stored_object_replay(self):
        path=Path(__file__).with_name('stored-object-v1.json')
        if not path.exists():
            self.skipTest('export_v1.py must run before saved-object replay')
        packet=json.loads(path.read_text(encoding='utf-8'))
        chain=tuple(tuple(tuple(Q(x) for x in row) for row in A) for A in packet['same_returned_closed_chain'])
        width=packet['inputs']['width']
        for j in range(2**width):
            v=(Q(1),)
            for q,A in enumerate(chain):
                r=len(A[0])//2
                bit=(j>>q)&1
                v=tuple(sum((v[a]*A[a][bit*r+b] for a in range(len(v))),Q(0)) for b in range(r))
            self.assertEqual(v,(actual(1,Q(2),-2+Q(4*j,2**width)),))
        print('PASS independently loaded saved stored chain exact signed source on all8 words',flush=True)

    def test_same_returned_stored_chain(self):
        for width in (1,3):
            obj=produce(1,width,Q(2),Q(2))
            stored=materialize_and_close(obj)
            self.assertIs(stored.source,obj)
            self.assertEqual(len(stored.tables),width)
            for table in stored.tables:
                self.assertEqual(len(table),obj.dimension)
                self.assertTrue(all(len(row)==2*obj.dimension for row in table))
            self.assertEqual(len(stored.chain),width)
            self.assertEqual(len(stored.chain[0]),1)
            self.assertEqual(len(stored.chain[-1][0]),2)
            for j in range(2**width):
                self.assertEqual(stored.amplitude(j),obj.amplitude(j))
                self.assertEqual(stored.amplitude(j),actual(1,Q(2),-2+Q(4*j,2**width)))
            for op in ('field','read','write'):
                self.assertGreater(stored.cost[op],obj.cost[op])
            scalars=sum(sum(len(row) for row in A) for A in stored.chain)
            self.assertLessEqual(scalars,2*width*obj.dimension**2)
            print(f'PASS same stored returned chain,width={width},D={obj.dimension},chain_scalars={scalars},charged={stored.cost}',flush=True)

    def test_all_words_actual_source(self):
        for k,width,R,delta in ((0,1,Q(1),Q(2)),(1,3,Q(2),Q(2)),(1,3,Q(2),Q(1,2)),(0,3,Q(3),Q(1,4)),(2,2,Q(2,3),Q(2))):
            obj=produce(k,width,R,delta)
            N=2**width
            self.assertEqual(obj.dimension,18*(obj.degree+1)+9*(2*k+2)+18)
            for j in range(N):
                p=-R+2*R*j/N
                self.assertEqual(obj.amplitude(j),actual(k,delta,p),(k,width,R,delta,j,p))
            self.assertEqual(obj.amplitude(N//2),1)
            print(f'PASS exact full grid k={k},width={width},R={R},delta={delta},T={obj.cutoff},d={obj.degree},D={obj.dimension},cuts={obj.cuts},nonzero_entries={sum(len(t[b]) for t in obj.tables for b in (0,1))}',flush=True)

    def test_threshold_zero_and_N_endpoints(self):
        for width in range(1,8):
            N=2**width
            for cut in range(N+1):
                for j in range(N):
                    state=1
                    for q in range(width):
                        state=advance(state,(j>>q)&1,(cut>>q)&1)
                    self.assertEqual(accept(state,cut,N,False),Q(j<cut))
                    self.assertEqual(accept(state,cut,N,True),Q(j>=cut))

    def test_large_width_nondense_generation(self):
        # Generation scales far beyond enumerable physical dimension at T0.
        obj=produce(1,64,Q(3),Q(2))
        self.assertEqual(len(obj.tables),64)
        self.assertLess(sum(len(t[b]) for t in obj.tables for b in (0,1)),200000)
        for j in (0,1,2**63-1,2**63,2**64-1):
            self.assertEqual(obj.amplitude(j),actual(1,Q(2),-3+Q(6*j,2**64)))
        print(f'PASS width64,D={obj.dimension},stored_nonzero={sum(len(t[b]) for t in obj.tables for b in (0,1))},charged={obj.cost}',flush=True)

if __name__ == '__main__':
    unittest.main()
