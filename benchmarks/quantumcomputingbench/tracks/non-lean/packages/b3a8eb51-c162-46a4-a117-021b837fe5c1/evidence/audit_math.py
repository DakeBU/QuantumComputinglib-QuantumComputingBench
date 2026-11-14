"""Finite matrix checks for additional public relation witnesses in the reviewed packets."""
from itertools import permutations
import json
import numpy as np

def monomial(perm,phase):
    result=np.zeros((len(perm),len(perm)),complex)
    for j,i in enumerate(perm):result[i,j]=phase[j]
    return result

def cycle_sets(perm):
    seen=set();result=[]
    for i in range(len(perm)):
        if i in seen:continue
        group=[];j=i
        while j not in seen:
            seen.add(j);group.append(j);j=perm[j]
        result.append(group)
    return result

def check_cycles():
    rng=np.random.default_rng(582171);cases=0
    for n in range(1,6):
        for perm in permutations(range(n)):
            p=np.exp(1j*rng.uniform(-np.pi,np.pi,n));u=monomial(perm,p)
            diag=np.exp(1j*rng.uniform(-np.pi,np.pi,n));d=np.diag(diag);v=d@u@d.conj().T
            transformed=np.array([v[i,j] for j,i in enumerate(perm)])
            assert np.allclose(u.conj().T@u,np.eye(n))
            cycles=cycle_sets(perm)
            for cyc in cycles:assert np.allclose(np.prod(p[cyc]),np.prod(transformed[cyc]))
            for k in range(1,2*n+1):
                expected=sum(len(c)*np.prod(p[c])**(k//len(c)) for c in cycles if k%len(c)==0)
                assert np.allclose(np.trace(np.linalg.matrix_power(u,k)),expected)
            cases+=1
    return {'permutations_of_labeled_sets':cases,'largest_dimension':5,'tested':'Diagonal rephasing preserves each oriented cycle product. Traces of powers count closed cycles with their accumulated weight. Random phases have a fixed seed.'}

def check_line():
    rng=np.random.default_rng(23704);cases=0;negative_basis=0
    for n in range(2,9):
        for src in range(n):
            for _ in range(9):
                vec=rng.normal(size=n);vec[rng.random(n)<.35]=0
                if not np.any(vec):vec[src]=1
                vec/=np.linalg.norm(vec);work=vec.copy();start=min(src,np.nonzero(vec)[0].min());end=max(src,np.nonzero(vec)[0].max());count=0
                operations=[]
                pairs=[(i,i+1,True) for i in range(start,src)]+[(i-1,i,False) for i in range(end,src,-1)]
                for i,j,zero_left in pairs:
                    v,w=work[i],work[j];length=np.hypot(v,w)
                    if length:
                        c,s=(w/length,v/length) if zero_left else (v/length,-w/length)
                    else:
                        c,s=1.,0.
                    work[i],work[j]=c*v-s*w,s*v+c*w
                    operations.append((i,j,c,s))
                sign_only=start==end and work[src]<0
                if sign_only:
                    i=max(0,src-1);j=i+1
                    work[i],work[j]=-work[i],-work[j]
                    operations.append((i,j,-1.,0.))
                    negative_basis+=1
                basis=np.eye(n)[src]
                assert np.allclose(work,basis) and len(operations)==end-start+int(sign_only)
                rebuilt=basis.copy()
                for i,j,c,s in reversed(operations):
                    v,w=rebuilt[i],rebuilt[j]
                    rebuilt[i],rebuilt[j]=c*v+s*w,-s*v+c*w
                assert np.allclose(rebuilt,vec)
                cases+=1
    return {'sampled_vectors':cases,'negative_basis_examples':negative_basis,'largest_dimension':8,'tested':'Apply signed eliminations on increasingly ordered adjacent pairs, gather at the positive basis input and reverse to the exact target. Negative single-site targets use one sign-flip gate. The general lower bound is proved in the packet.'}

if __name__=='__main__':print(json.dumps({'cycle_checks':check_cycles(),'state_preparation_checks':check_line(),'scope':'Finite auxiliary diagnostics for public mechanisms. Correctness, necessity and tightness are assessed in the question-first proofs.'},indent=2))
