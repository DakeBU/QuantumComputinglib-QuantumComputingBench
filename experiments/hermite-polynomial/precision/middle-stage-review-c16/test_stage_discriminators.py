"""Independent tuple-wire pair loop and exact norm/size discriminators."""
from fractions import Fraction as F
from itertools import product
from math import ceil, factorial, floor
from pathlib import Path
import sys
import unittest

HERE=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(HERE.parent/'saved-action'))
import saved_action as actual

def tuple_bits(index,width):
    return tuple((index//(2**q))%2 for q in range(width))

def tuple_index(bits):
    return sum(b*2**q for q,b in enumerate(bits))

def toggle(index,q,width):
    bits=list(tuple_bits(index,width)); bits[q]=1-bits[q]
    return tuple_index(bits)

def rnd(a,bits):
    g=2**bits
    return F(floor(a[0]*g),g),F(ceil(a[1]*g),g)

def plus(a,b): return a[0]+b[0],a[1]+b[1]
def neg(a): return -a[1],-a[0]
def times(a,b):
    p=[x*y for x,y in product(a,b)]
    return min(p),max(p)

def trig(theta,n,bits):
    x=theta/2
    s=sum((F((-1)**((i-1)//2))*x**i/factorial(i) for i in range(1,n+1,2)),F())
    c=sum((F((-1)**(i//2))*x**i/factorial(i) for i in range(0,n+1,2)),F())
    r=abs(x)**(n+1)/factorial(n+1)
    return rnd((s-r,s+r),bits),rnd((c-r,c+r),bits)

def pair_interpreter(width,word,n=96,bits=80,early=False):
    size=2**width
    a=[[(F(i==j),F(i==j)) for j in range(size)] for i in range(size)]
    for op,payload,q in word:
        if op=='cx':
            for i in range(size):
                if tuple_bits(i,width)[payload] and not tuple_bits(i,width)[q]:
                    j=toggle(i,q,width)
                    a[i],a[j]=a[j],a[i]
        else:
            s,c=trig(payload,n,bits)
            for i in range(size):
                if tuple_bits(i,width)[q]: continue
                j=toggle(i,q,width)
                u,v=a[i],a[j]
                a[i]=[rnd(plus(times(c,x),neg(times(s,y))),bits) for x,y in zip(u,v)]
                a[j]=[rnd(plus(times(s,x),times(c,y)),bits) for x,y in zip(u,v)]
        if early:
            a=[[((lo+hi)/2,(lo+hi)/2) for lo,hi in row] for row in a]
    centers=[[(lo+hi)/2 for lo,hi in row] for row in a]
    r=max((hi-lo)/2 for row in a for lo,hi in row)
    return a,centers,r

WORD=[('ry',F(-4,5),2),('cx',2,0),('ry',F(2,7),0),('cx',0,1),('ry',F(-3,2),1)]

class StageDiscriminators(unittest.TestCase):
    def test_tuple_routing_and_actual_eight_by_eight_stage(self):
        self.assertEqual(toggle(3,0,3),2)
        self.assertEqual(toggle(1,2,3),5)
        physical_map={0:1,1:2,2:0} # q1,q2 ancillas become local bits0,1; dataq0 bit2
        physical=[('ry',v,physical_map[q]) if op=='ry' else ('cx',physical_map[v],physical_map[q]) for op,v,q in WORD]
        manifest={'n':1,'ancillas':2,'stage_spans':[{'start':0,'count':len(WORD),'data_wire':0}]}
        centers,reports,sigma=actual.stage_surrogates(physical,manifest,actual.MeasuredWork())
        _,expected,r=pair_interpreter(3,WORD)
        self.assertEqual(centers,[expected])
        self.assertEqual(F(reports[0]['entry_radius']),r)
        self.assertEqual(F(reports[0]['eta']),8*r)
        self.assertEqual(sigma,8*r)
        self.assertGreater(r,0)

    def test_spectator_garbage_and_empty_carrier(self):
        word=[('ry',F(-2,3),0),('cx',0,1),('ry',F(1,5),1)]
        a,_,_=pair_interpreter(3,word,4,7)
        small,_,_=pair_interpreter(2,word,4,7)
        for i,j in product(range(8),repeat=2):
            expected=small[i%4][j%4] if i//4==j//4 else (F(),F())
            self.assertEqual(a[i][j],expected)
        a,c,r=pair_interpreter(0,[])
        self.assertEqual((a,c,r),([[(F(1),F(1))]],[[F(1)]],F()))

    def test_chronology_target_direction_and_end_midpoint(self):
        base=pair_interpreter(3,WORD,2,3)[1]
        self.assertNotEqual(base,pair_interpreter(3,list(reversed(WORD)),2,3)[1])
        forced=[(op,v,0) if op=='ry' else (op,v,q) for op,v,q in WORD]
        self.assertNotEqual(base,pair_interpreter(3,forced,2,3)[1])
        reversed_cx=[('cx',q,v) if op=='cx' else (op,v,q) for op,v,q in WORD]
        self.assertNotEqual(base,pair_interpreter(3,reversed_cx,2,3)[1])
        early_word=[('ry',F(-9,7),0),('cx',0,1),('ry',F(-1),1)]
        self.assertNotEqual(pair_interpreter(2,early_word,0,1)[1],pair_interpreter(2,early_word,0,1,True)[1])

    def test_entry_vs_operator_radius_and_dense_scaling(self):
        r=F(1,10); n=4
        A=[[r]*n for _ in range(n)]
        x=[F(1)]*n
        Ax=[sum((a*y for a,y in zip(row,x)),F()) for row in A]
        xnorm2=sum((y*y for y in x),F())
        ynorm2=sum((y*y for y in Ax),F())
        self.assertEqual(ynorm2/xnorm2,(n*r)**2)
        self.assertGreater(ynorm2,r*r*xnorm2)
        # Counting only, no dense large allocation or runtime benchmark.
        for width in [0,1,2,3,8,16]:
            self.assertEqual((2**width)**2,4**width)
        self.assertEqual(4**16,4294967296)

if __name__=='__main__':
    unittest.main()
