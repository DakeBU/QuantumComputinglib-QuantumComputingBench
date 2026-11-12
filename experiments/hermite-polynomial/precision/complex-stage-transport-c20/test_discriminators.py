"""Finite supplements for the literal Lean interval definitions, not runtime refinement."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib, io, json, math, unittest
import numpy as np
HERE=Path(__file__).resolve().parent
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def negative(a): return (-a[1],-a[0])
def times(a,b):
    values=[x*y for x in a for y in b]; return (min(values),max(values))
def outward(a,bits):
    g=2**bits
    return (Q((a[0]*g).__floor__(),g),Q((a[1]*g).__ceil__(),g))
def trig(theta,degree,bits,sine):
    q=theta/2
    coeff=lambda i: ((1 if i%4==1 else -1 if i%4==3 else 0) if sine else
      (1 if i%4==0 else -1 if i%4==2 else 0))
    p=sum((Q(coeff(i))*q**i/math.factorial(i) for i in range(degree+1)),Q(0))
    radius=abs(q)**(degree+1)/math.factorial(degree+1)
    return outward((p-radius,p+radius),bits)
def interval(w,word,degree,bits):
    n=2**w; a=[[(Q(i==j),Q(i==j)) for j in range(n)] for i in range(n)]
    for tag,v,q in word:
        result=[]
        for i in range(n):
            if tag=='cx': result.append(a[i^(1<<q) if (i>>v)&1 else i][:]); continue
            c,s=trig(v,degree,bits,False),trig(v,degree,bits,True)
            lo=i & ~(1<<q); hi=i | (1<<q); row=[]
            for j in range(n):
                u,t=a[lo][j],a[hi][j]
                pair=(outward(add(times(c,u),negative(times(s,t))),bits),
                  outward(add(times(s,u),times(c,t)),bits))
                row.append(pair[(i>>q)&1])
            result.append(row)
        a=result
    center=np.array([[float((lo+hi)/2) for lo,hi in row] for row in a],dtype=complex)
    eta=n*max(float((hi-lo)/2) for row in a for lo,hi in row)
    return center,eta
def primitive(w,word):
    n=2**w; states=[tuple((i>>q)&1 for q in range(w)) for i in range(n)]
    enc=lambda b:sum(bit*2**q for q,bit in enumerate(b))
    total=np.eye(n,dtype=complex)
    for tag,v,q in word:
        g=np.zeros((n,n),dtype=complex)
        for b in states:
            if tag=='cx':
                r=list(b); r[q]^=b[v]; g[enc(r),enc(b)]=1
            else:
                c,s=math.cos(float(v)/2),math.sin(float(v)/2)
                for value in [0,1]:
                    r=list(b); r[q]=value; g[enc(r),enc(b)]=((c,-s),(s,c))[value][b[q]]
        total=g@total
    return total
class Discriminators(unittest.TestCase):
    def stage(self,w,word):
        s,e=interval(w,word,12,16); u=primitive(w,word)
        self.assertLessEqual(np.linalg.norm(s-u,2),e+2e-12)
        return s,e,u
    def test_complex_induced_operator(self):
        for w in range(1,5):
            word=[('ry',Q(-3,2),w-1)]+([('cx',w-1,0)] if w>1 else [])
            s,e,u=self.stage(w,word)
            x=np.array([complex(2*i-1,(3*i)%7-2) for i in range(2**w)])
            self.assertLessEqual(np.linalg.norm((s-u)@x),e*np.linalg.norm(x)+2e-12)
            self.assertAlmostEqual(np.linalg.norm(u@x),np.linalg.norm(x))
    def test_imaginary_input(self):
        s,e,u=self.stage(3,[('ry',Q(-2,3),2),('cx',2,0),('ry',Q(4,5),1)])
        x=1j*np.arange(1,9)
        self.assertLessEqual(np.linalg.norm((s-u)@x),e*np.linalg.norm(x)+2e-12)
    def test_all_spectators_and_terminal_sectors(self):
        for q in range(4):
            s,e,u=self.stage(4,[('ry',Q(-7,5),q)])
            for i in range(16):
                for j in range(16):
                    if i & ~(1<<q)!=j & ~(1<<q):
                        self.assertEqual(u[i,j],0); self.assertEqual(s[i,j],0)
    def test_cx_inverse_direction(self):
        for c,t in [(0,2),(2,0),(1,2),(2,1)]:
            s,e,u=self.stage(3,[('cx',c,t)])
            self.assertEqual(e,0); np.testing.assert_array_equal(s,u)
            np.testing.assert_array_equal(u@u,np.eye(8))
            self.assertGreater(np.linalg.norm(u-primitive(3,[('cx',t,c)]),2),1)
    def test_signed_halfangle(self):
        _,_,u=self.stage(1,[('ry',Q(-3,2),0)])
        self.assertAlmostEqual(u[0,1].real,math.sin(0.75))
        self.assertAlmostEqual(u[1,0].real,-math.sin(0.75))
    def test_chronological_growth_and_order(self):
        words=[[('ry',Q(-3,2),0)],[('cx',0,1),('ry',Q(2,3),1)]]
        approx=np.eye(4,dtype=complex); exact=np.eye(4,dtype=complex); growth=1.0
        for word in words:
            s,e,u=self.stage(2,word); approx=s@approx; exact=u@exact; growth*=1+e
        flat=primitive(2,sum(words,[])); np.testing.assert_allclose(exact,flat,atol=1e-14)
        self.assertLessEqual(np.linalg.norm(approx-flat,2),growth-1+2e-12)
        wrong=primitive(2,sum(words[::-1],[])); self.assertGreater(np.linalg.norm(approx-wrong,2),0.5)
        x=np.array([1+2j,-3j,2-1j,-2+4j])
        self.assertLessEqual(np.linalg.norm((approx-flat)@x),(growth-1)*np.linalg.norm(x)+2e-12)
    def test_width_zero_full_scalar_space(self):
        s,e,u=self.stage(0,[]); self.assertEqual(e,0)
        np.testing.assert_array_equal(s,[[1]]); np.testing.assert_array_equal(u,[[1]])
        self.assertEqual((s@np.array([2+3j]))[0],2+3j)
if __name__=='__main__':
    receipt=HERE/'finite-v1.json'; log=HERE/'finite-v1.log'
    if receipt.exists() or log.exists(): raise SystemExit('Immutable evidence exists')
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    before=sha(Path(__file__)); stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Discriminators))
    log.write_text(stream.getvalue(),encoding='utf-8')
    receipt.write_text(json.dumps({'command':['.venv/Scripts/python.exe',str(Path(__file__).relative_to(HERE.parents[3]))],'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'passed':result.wasSuccessful(),'source_before_sha256':before,'source_after_sha256':sha(Path(__file__)),'log_sha256':sha(log),'uniform_or_symbolic_certificate':False},indent=2)+'\n',encoding='utf-8')
    print(stream.getvalue()); print('RECEIPT',sha(receipt)); raise SystemExit(not result.wasSuccessful())
