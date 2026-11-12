"""C21 independent finite screening; no author executable imported."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math
import numpy as np
HERE=Path(__file__).resolve().parent
def mm(a,b):
    v=[x*y for x in a for y in b];return min(v),max(v)
def aa(a,b):return a[0]+b[0],a[1]+b[1]
def nn(a):return -a[1],-a[0]
def roundout(a,b):
    n=2**b;return F(math.floor(a[0]*n),n),F(math.ceil(a[1]*n),n)
def coeff(t,d,b,sine):
    x=t/2
    terms=[F((-1)**(i//2))*x**i/math.factorial(i) for i in range(d+1) if i%2==int(sine)]
    center=sum(terms,F(0));r=abs(x)**(d+1)/math.factorial(d+1)
    return roundout((center-r,center+r),b)
def interval(w,word,d=14,b=18):
    n=2**w;a=[[(F(int(i==j)),F(int(i==j))) for j in range(n)] for i in range(n)]
    for g in word:
        if g[0]=='CX':
            _,c,t=g;a=[a[i^(1<<t) if (i>>c)&1 else i][:] for i in range(n)]
        else:
            _,t,q=g;c,s=coeff(t,d,b,False),coeff(t,d,b,True);v=[[None]*n for _ in range(n)]
            for low in range(n):
                if (low>>q)&1:continue
                high=low+(1<<q)
                for j in range(n):
                    v[low][j]=roundout(aa(mm(c,a[low][j]),nn(mm(s,a[high][j]))),b)
                    v[high][j]=roundout(aa(mm(s,a[low][j]),mm(c,a[high][j])),b)
            a=v
    center=np.array([[float((l+h)/2) for l,h in row] for row in a],dtype=complex)
    eta=float(n*max((h-l)/2 for row in a for l,h in row))
    return center,eta
def gate(w,g):
    n=2**w
    if g[0]=='RY':
        _,theta,q=g;c=math.cos(float(theta)/2);s=math.sin(float(theta)/2)
        factors=[np.array([[c,-s],[s,c]]) if i==q else np.eye(2) for i in reversed(range(w))]
        result=np.array([[1.]])
        for a in factors:result=np.kron(result,a)
        return result.astype(complex)
    _,c,t=g
    out=np.zeros((n,n),dtype=complex)
    for j in range(n):
        bits=[(j//2**q)%2 for q in range(w)];bits[t]=(bits[t]+bits[c])%2
        i=sum(v*2**q for q,v in enumerate(bits));out[i,j]=1
    return out
def literal(w,word):
    a=np.eye(2**w,dtype=complex)
    for g in word:a=gate(w,g)@a
    return a
def main():
    target=HERE/'finite-review-v1.json'
    if target.exists():raise SystemExit('Immutable evidence exists')
    rows=[]
    def screen(name,w,word):
        a,e=interval(w,word);u=literal(w,word);n=2**w
        x=np.array([complex(2*j-3,5-3*j) for j in range(n)])
        op=float(np.linalg.norm(a-u,2));act=float(np.linalg.norm((a-u)@x));lim=e*float(np.linalg.norm(x))
        assert op<=e+2e-12 and act<=lim+2e-12
        assert np.linalg.norm(u@x)-np.linalg.norm(x)<2e-12
        rows.append({'case':name,'width':w,'operator_error':op,'actual_stage_eta':e,'complex_apply_error':act,'complex_apply_bound':lim})
        return a,e,u
    for w in range(1,5):
        for q in range(w):
            a,e,u=screen('negative-RY-all-spectators',w,[('RY',F(-7,3),q)])
            assert u[0,1<<q].real>0 and u[1<<q,0].real<0
            for i in range(2**w):
                for j in range(2**w):
                    if (i>>q<<q) != (j>>q<<q) and (i & ~(1<<q))!=(j & ~(1<<q)):
                        assert u[i,j]==0 and a[i,j]==0
            # All non-target bits agree for every nonzero matrix entry.
            for i,j in zip(*np.nonzero(u)):assert (i & ~(1<<q))==(j & ~(1<<q))
    for w in range(2,5):
        for c in range(w):
            for t in range(w):
                if c==t:continue
                a,e,u=screen('CX-every-ordered-wire-pair',w,[('CX',c,t)])
                assert e==0 and np.array_equal(a,u) and np.array_equal(u@u,np.eye(2**w))
                assert np.linalg.norm(u-gate(w,('CX',t,c)),2)>1
    words=[[('RY',F(-4,3),0)],[('CX',0,2),('RY',F(3,5),1)],[('RY',F(-2,7),2)]]
    a=np.eye(8,dtype=complex);u=a.copy();growth=1
    for word in words:
        s,e,v=screen('complex-stage-sequence',3,word);a=s@a;u=v@u;growth*=1+e
    flat=literal(3,[g for word in words for g in word]);wrong=literal(3,[g for word in reversed(words) for g in word])
    assert np.linalg.norm(u-flat,2)<2e-12
    assert np.linalg.norm(a-wrong,2)>0.5
    x=np.array([complex(j-1,2*j+3) for j in range(8)])
    assert np.linalg.norm((a-flat)@x)<=(growth-1)*np.linalg.norm(x)+2e-12
    rows.append({'case':'later-left-growth-and-reversal-discriminator','growth_minus_one':growth-1,'product_error':float(np.linalg.norm(a-flat,2)),'wrong_order_distance':float(np.linalg.norm(a-wrong,2))})
    a,e,u=screen('width-zero-full-complex-scalar',0,[])
    assert e==0 and np.array_equal(a,[[1]]) and np.array_equal(u,[[1]])
    assert (a@np.array([2+3j]))[0]==2+3j
    data={'reviewer':'/root/complex_transport_review_c21','passed':True,'cases':rows,'independent_from_author_executable':True,'evidence_level':'finite matrix/operator discriminators only; no uniform symbolic or runtime-refinement credit','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    target.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':True,'cases':len(rows),'receipt_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}))
if __name__=='__main__':main()
