"""Independent small-width screening, never symbolic certification."""
from fractions import Fraction
from pathlib import Path
import hashlib, io, json, math, sys, unittest
HERE=Path(__file__).resolve().parent
comparisons=0
def mm(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def identity(w): return [[complex(i==j) for j in range(1<<w)] for i in range(1<<w)]
def literal(w,word,m):
    for tag,x,y in word:
        result=[]
        for row in range(1<<w):
            if tag=='cx': result.append(m[row ^ (1<<y) if (row>>x)&1 else row][:]); continue
            c,s=math.cos(float(x)/2),math.sin(float(x)/2)
            lo=row & ~(1<<y); hi=row | (1<<y)
            result.append([s*u+c*v if (row>>y)&1 else c*u-s*v for u,v in zip(m[lo],m[hi])])
        m=result
    return m
def canonical(w,word):
    states=[tuple((index>>q)&1 for q in range(w)) for index in range(1<<w)]
    index={b:sum(v*(2**q) for q,v in enumerate(b)) for b in states}
    total=identity(w)
    for tag,x,y in word:
        gate=[[0j]*(1<<w) for _ in states]
        for b in states:
            if tag=='cx':
                r=list(b); r[y]=(r[y]+b[x])%2; gate[index[tuple(r)]][index[b]]=1
            else:
                c,s=math.cos(float(x)/2),math.sin(float(x)/2)
                for v in [0,1]:
                    r=list(b); r[y]=v; gate[index[tuple(r)]][index[b]]=((c,-s),(s,c))[v][b[y]]
        total=mm(gate,total)
    return total
def distance(a,b): return max(abs(x-y) for row,other in zip(a,b) for x,y in zip(row,other))
class Checks(unittest.TestCase):
    def close(self,a,b):
        global comparisons
        comparisons+=len(a)*len(a[0]); self.assertLess(distance(a,b),2e-12)
    def test_nonidentity_real_matrix(self):
        for w in range(1,5):
            m=[[float(i-3*j+2) for j in range(1<<w)] for i in range(1<<w)]
            word=[('ry',Fraction(-7,5),w-1)]+([('cx',w-1,0)] if w>1 else [])
            self.close(literal(w,word,m),mm(canonical(w,word),m))
    def test_all_spectator_sectors(self):
        for w in range(1,6):
            for q in range(w):
                word=[('ry',Fraction(-2,3),q)]
                self.close(literal(w,word,identity(w)),canonical(w,word))
                a=canonical(w,word)
                for i in range(1<<w):
                    for j in range(1<<w):
                        if (i & ~(1<<q))!=(j & ~(1<<q)): self.assertEqual(a[i][j],0)
    def test_cx_inverse_and_swapped_direction(self):
        for w in range(2,5):
            for c in range(w):
                for t in range(w):
                    if c==t: continue
                    a=canonical(w,[('cx',c,t)])
                    self.close(mm(a,a),identity(w))
                    self.close(literal(w,[('cx',c,t)],identity(w)),a)
                    self.assertGreater(distance(a,canonical(w,[('cx',t,c)])),0.5)
    def test_negative_rational_half_angle(self):
        theta=Fraction(-3,2); a=canonical(1,[('ry',theta,0)])
        self.assertAlmostEqual(a[0][1].real,math.sin(0.75))
        self.assertAlmostEqual(a[1][0].real,-math.sin(0.75))
        self.assertGreater(abs(a[0][1].real+math.sin(0.75)),1)
        self.assertGreater(abs(a[0][1].real-math.sin(1.5)),0.2)
    def test_chronological_order(self):
        word=[('ry',Fraction(4,5),0),('cx',0,1),('ry',Fraction(-1,3),1)]
        self.close(literal(2,word,identity(2)),canonical(2,word))
        self.assertGreater(distance(canonical(2,word),canonical(2,word[::-1])),0.2)
    def test_arbitrary_complex_vector(self):
        for w in range(1,5):
            v=[[complex(2*i-1,(3*i)%7-2)] for i in range(1<<w)]
            word=[('ry',Fraction(-3,2),w-1)]+([('cx',0,w-1)] if w>1 else [])
            self.close(mm(literal(w,word,identity(w)),v),mm(canonical(w,word),v))
    def test_width_zero_scalar_space(self):
        self.close(literal(0,[],[[7.0]]),[[7.0]])
        self.close(canonical(0,[]),[[1]])
if __name__=='__main__':
    receipt=HERE/'finite-checks-v1.json'; log=HERE/'finite-checks-v1.log'
    if receipt.exists() or log.exists(): raise SystemExit('Immutable evidence exists')
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    before=sha(Path(__file__)); stream=io.StringIO()
    run=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks))
    log.write_text(stream.getvalue(),encoding='utf-8')
    result={'command':[sys.executable,str(Path(__file__))],'test_count':run.testsRun,'entry_comparisons':comparisons,'failures':len(run.failures),'errors':len(run.errors),'passed':run.wasSuccessful(),'source_before_sha256':before,'source_after_sha256':sha(Path(__file__)),'log_sha256':sha(log),'symbolic_certification':False}
    receipt.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8'); print(stream.getvalue()); print(json.dumps(result)); print('RECEIPT',sha(receipt)); sys.exit(not run.wasSuccessful())
