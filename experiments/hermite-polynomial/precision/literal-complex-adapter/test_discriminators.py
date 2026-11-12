"""Finite screening only; canonical-basis compatibility is proved symbolically in Lean."""
import cmath
import math
import unittest

def encode(bits):
    return 0 if not bits else bits[0] + 2 * encode(bits[1:])

def named_bits(w):
    return [tuple((i >> q) & 1 for q in range(w)) for i in range(2**w)]

def identity(n):
    return [[complex(i == j) for j in range(n)] for i in range(n)]

def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b))] for i in range(len(a))]

def literal(w,word,a=None):
    a=identity(2**w) if a is None else a
    for g in word:
        out=[]
        for i in range(2**w):
            if g[0]=='cx':
                out.append(a[i ^ (1<<g[2]) if (i>>g[1])&1 else i][:])
            else:
                _,theta,q=g
                lo=i & ~(1<<q)
                hi=i | (1<<q)
                c,s=math.cos(theta/2),math.sin(theta/2)
                out.append([s*u+c*v if (i>>q)&1 else c*u-s*v for u,v in zip(a[lo],a[hi])])
        a=out
    return a

def primitive(w,word):
    bits=named_bits(w)
    a=identity(2**w)
    for g in word:
        gate=[[0j]*len(bits) for _ in bits]
        for b in bits:
            col=encode(b)
            if g[0]=='cx':
                r=list(b)
                r[g[2]] ^= b[g[1]]
                gate[encode(r)][col]=1
            else:
                _,theta,q=g
                for v in (0,1):
                    r=list(b)
                    r[q]=v
                    c,s=math.cos(theta/2),math.sin(theta/2)
                    gate[encode(r)][col]=((c,-s),(s,c))[v][b[q]]
        a=mul(gate,a)
    return a

class Discriminators(unittest.TestCase):
    def close(self,a,b):
        self.assertLess(max(abs(x-y) for ra,rb in zip(a,b) for x,y in zip(ra,rb)),1e-12)

    def test_width0(self):
        self.close(literal(0,[]),primitive(0,[]))

    def test_signed_halfangle(self):
        for theta in (-1.25,0,0.75):
            a=literal(1,[('ry',theta,0)])
            self.assertAlmostEqual(a[0][1].real,-math.sin(theta/2))
            self.assertAlmostEqual(a[1][0].real,math.sin(theta/2))
            self.close(a,primitive(1,[('ry',theta,0)]))

    def test_all_spectators_and_cx_directions(self):
        for w in range(1,6):
            for q in range(w):
                words=[[('ry',-0.7,q)]]
                words += [[('ry',0.4,q),('cx',q,t),('ry',-0.9,t)] for t in range(w) if t!=q]
                for word in words:
                    self.close(literal(w,word),primitive(w,word))

    def test_order_discriminator(self):
        word=[('ry',0.9,0),('cx',0,1),('ry',-0.4,1)]
        a=literal(2,word)
        self.close(a,primitive(2,word))
        wrong=primitive(2,list(reversed(word)))
        self.assertGreater(max(abs(x-y) for ra,rb in zip(a,wrong) for x,y in zip(ra,rb)),0.1)

    def test_complex_input(self):
        word=[('ry',-0.3,2),('cx',2,0),('ry',0.7,1)]
        a=[[complex(i-j,(i+2*j)%5) for j in range(8)] for i in range(8)]
        self.close(literal(3,word,a),mul(primitive(3,word),a))

if __name__=='__main__':
    unittest.main()
