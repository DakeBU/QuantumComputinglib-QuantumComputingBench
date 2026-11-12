"""Literal nondense rational local-core producer. No quantum/runtime certificate.

Only local bond addresses are traversed during production. Words are enumerated
only by the separate finite test. Core order is q0, q1, ... (least significant
first). A more significant unequal bit overwrites the comparison state.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from collections import Counter


class Arithmetic:
    """Extended unit-cost rational/word schedule; GCD/bit costs are excluded."""
    def __init__(self):
        self.cost = Counter()

    def read(self, x):
        self.cost['read'] += 1
        return x

    def write(self, x):
        self.cost['write'] += 1
        return x

    def add(self, x, y):
        self.cost['field'] += 1
        return x+y

    def mul(self, x, y):
        self.cost['field'] += 1
        return x*y

    def div(self, x, y):
        self.cost['field'] += 1
        return x/y

    def compare(self, x, y):
        self.cost['compare'] += 1
        return (x > y)-(x < y)

    def powers(self, x, d):
        out = [self.write(Q(1))]
        for _ in range(d):
            out.append(self.write(self.mul(self.read(out[-1]), x)))
        return out

    def choose(self, n, i):
        self.cost['integer'] += 1
        if i > n:
            return Q(0)
        out = Q(1)
        for r in range(i):
            self.cost['integer'] += 2
            out = self.div(self.mul(out, Q(n-r)), Q(r+1))
        return out


def cutoff(delta):
    if delta <= 0:
        raise ValueError('positive source tolerance required by this exporter')
    return (max(1, -(-delta.denominator//delta.numerator))-1).bit_length()


def coefficients(k, e, ar):
    """Expand exactly the accepted middleValueQ, not an interpolated fit."""
    a = []
    fact = Q(1)
    invfacts = [Q(1)]
    for i in range(1, k+1):
        fact = ar.mul(fact, Q(i))
        invfacts.append(ar.write(ar.div(Q(1), fact)))
    for i in range(k+1):
        s = Q(0)
        for h in range(i+1):
            s = ar.add(s, ar.mul(ar.choose(k+i-h, k), ar.read(invfacts[h])))
        a.append(ar.write(s))
    m = 2*k+1
    out = []
    for j in range(m+1):
        first, second = Q(0), Q(0)
        if j >= k+1:
            for i in range(j-k-1, k+1):
                first = ar.add(first, ar.mul(ar.read(a[i]), ar.choose(i, j-k-1)))
            first = ar.mul(ar.mul(e, Q((-1)**(k+1))), first)
        for i in range(min(k,j)+1):
            term = ar.mul(ar.read(a[i]), Q((-1)**i))
            second = ar.add(second, ar.mul(term, ar.choose(k+1, j-i)))
        out.append(ar.write(ar.add(first, second)))
    return tuple(out)


def cut_lt(s, R, step, N, ar):
    x = ar.div(ar.add(s,R),step)
    ar.cost['integer'] += 3  # exact ceil, clamp lower and upper
    return min(N,max(0,-(-x.numerator//x.denominator)))


def cut_le(s, R, step, N, ar):
    x = ar.div(ar.add(s,R),step)
    ar.cost['integer'] += 4  # exact floor, successor, clamp lower and upper
    return min(N,max(0,x.numerator//x.denominator+1))


def advance(state, bit, cutbit):
    # state0=less, state1=equal, state2=greater
    return 0 if bit < cutbit else 2 if bit > cutbit else state


def accept(state, cut, N, complement):
    base = Q(0) if cut == 0 else Q(1) if cut == N else Q(state == 0)
    return 1-base if complement else base


@dataclass(frozen=True)
class Component:
    degree: int
    cuts: tuple
    complements: tuple
    origin: Q
    sign: int
    coeffs: tuple


@dataclass(frozen=True)
class Produced:
    width: int
    dimension: int
    cutoff: int
    degree: int
    middle_degree: int
    cuts: tuple
    # Sparse STORED local tables (a,b)->rational; omitted entries are literal0.
    tables: tuple
    left: tuple
    right: tuple
    components: tuple
    cost: dict

    def amplitude(self, j):
        if not 0 <= j < 2**self.width:
            raise ValueError('word outside physical grid')
        v = dict((i,x) for i,x in enumerate(self.left) if x)
        for q, table in enumerate(self.tables):
            result = {}
            for (a,b),z in table[(j>>q)&1].items():
                x = v.get(a,0)
                if x:
                    result[b] = result.get(b,Q(0))+x*z
            v = result
        return sum((x*self.right[i] for i,x in v.items()),Q(0))


def produce(k, width, R, delta):
    """Return one exact local table/boundary object, never an amplitude table.

    This is the mathematical input layer, not a free source-value callback.
    Radius/tolerance allocation are separately supplied by the reviewed source
    package. Generation includes scalar and sparse-output read/write schedules;
    integer/GCD and language/container overhead are not finite-bit certified.
    """
    if width < 1 or R <= 0:
        raise ValueError('physical positive rational radius and width>=1 required')
    ar = Arithmetic()
    k,width,R,delta = (ar.read(x) for x in (k,width,R,delta))
    N = 2**width
    ar.cost['integer'] += width+1
    T = cutoff(delta)
    d, m = 4*T*T+2*T+1, 2*k+1
    ar.cost['integer'] += 8
    step = ar.div(ar.mul(Q(2),R),Q(N))
    A = cut_lt(Q(-1),R,step,N,ar)
    B = cut_le(Q(0),R,step,N,ar)
    C = cut_le(Q(-T),R,step,N,ar)
    E = cut_lt(Q(T),R,step,N,ar)  # D=not(j<E)
    fact, tail = Q(1), [ar.write(Q(1))]
    for i in range(1,d+1):
        fact = ar.mul(fact,Q(i))
        tail.append(ar.write(ar.div(Q(1),fact)))
    c = ar.div(Q(1),Q(2**(T+1)))
    # Actual expMidpoint(-1), with equality belonging to the clipped branch.
    e = c if T <= 1 else sum((z*((-1)**i) for i,z in enumerate(tail)),Q(0))
    if T > 1:
        ar.cost['read'] += d+1
        ar.cost['field'] += 2*(d+1)
    middle = coefficients(k,e,ar)
    # Copy the shared tail coefficient table into two explicit stored tuples.
    ar.cost['read'] += 2*(d+1)
    ar.cost['write'] += 2*(d+1)
    comps = (
        Component(0,(A,C),(False,False),Q(0),1,(c,)),
        Component(d,(A,C),(False,True),-R,1,tuple(tail)),
        Component(m,(A,B),(True,False),-R,1,middle),
        Component(0,(B,E),(True,True),Q(0),1,(c,)),
        Component(d,(B,E),(True,False),R,-1,tuple(tail)),
    )
    # Degree0 origins/signs do not affect constants.
    D = sum(9*(c.degree+1) for c in comps)
    assert D == 18*(d+1)+9*(m+1)+18
    left, right = [], []
    for component in comps:
        r = component.degree+1
        pows = ar.powers(component.origin,component.degree)
        for a in range(3):
            for b in range(3):
                h = accept(a,component.cuts[0],N,component.complements[0])*accept(b,component.cuts[1],N,component.complements[1])
                ar.cost['field'] += 3
                ar.cost['compare'] += 6
                for i in range(r):
                    left.append(ar.write(ar.read(pows[i]) if a == b == 1 else Q(0)))
                    right.append(ar.write(ar.mul(h,ar.read(component.coeffs[i]))))
    tables = []
    for q in range(width):
        pair = []
        w = ar.mul(step,Q(2**q))
        for bit in range(2):
            core, offset = {}, 0
            for component in comps:
                r = component.degree+1
                wpows = ar.powers(ar.mul(Q(component.sign*bit),w),component.degree)
                for a in range(3):
                    for b in range(3):
                        cbits = tuple((cut>>q)&1 for cut in component.cuts)
                        ar.cost['integer'] += 4
                        a2,b2 = advance(a,bit,cbits[0]),advance(b,bit,cbits[1])
                        ar.cost['compare'] += 4
                        for i in range(r):
                            for j in range(i,r):
                                z = ar.mul(ar.choose(j,i),ar.read(wpows[j-i]))
                                ar.cost['compare'] += 1
                                if z:
                                    key=(offset+(3*a+b)*r+i,offset+(3*a2+b2)*r+j)
                                    core[ar.write(key)] = ar.write(z)
                offset += 9*r
            pair.append(ar.write(core))
        tables.append(ar.write(tuple(pair)))
    # Final immutable boundary/table references and copies.
    ar.cost['read'] += 2*D+2*width
    ar.cost['write'] += 2*D+3*width
    return Produced(width,D,T,d,m,(A,B,C,E),tuple(tables),tuple(left),tuple(right),comps,dict(ar.cost))


@dataclass(frozen=True)
class StoredProduced:
    source: Produced
    # Dense local tables in the existing bit-major StoredCore layout.
    tables: tuple
    # Same boundary absorption as StoredMatrixProductChain.ofTable.
    chain: tuple
    cost: dict

    def amplitude(self,j):
        v=(Q(1),)
        for q,A in enumerate(self.chain):
            r=len(A[0])//2
            bit=(j>>q)&1
            v=tuple(sum((v[a]*A[a][bit*r+b] for a in range(len(v))),Q(0)) for b in range(r))
        return v[0]


def materialize_and_close(obj):
    """Actually materialize scalar tables, then close the SAME object.

    No amplitude enumeration. The dense local-table output may be large in
    d,m, but never in2**width. Index arithmetic/bit/GCD costs remain excluded
    from the extended field/read/write schedule, not silently called proved.
    """
    ar=Arithmetic()
    D=obj.dimension
    tables=[]
    for pair in obj.tables:
        rows=[]
        for a in range(D):
            row=[]
            for bit in range(2):
                table=ar.read(pair[bit])
                for b in range(D):
                    z=ar.read(table.get((a,b),Q(0)))
                    row.append(ar.write(z))
            ar.cost['read'] += 2*D
            ar.cost['write'] += 2*D
            rows.append(ar.write(tuple(row)))
        ar.cost['read'] += D
        ar.cost['write'] += D
        tables.append(ar.write(tuple(rows)))
    ar.cost['read'] += obj.width
    ar.cost['write'] += obj.width
    tables=tuple(tables)
    final=ar.read(tables[-1])
    terminal=[]
    for a in range(D):
        row=[]
        for bit in range(2):
            z=Q(0)
            for b in range(D):
                x=ar.read(ar.read(final[a])[bit*D+b])
                y=ar.read(obj.right[b])
                z=ar.add(z,ar.mul(x,y))
            row.append(ar.write(z))
        ar.cost['read'] += 2
        ar.cost['write'] += 2
        terminal.append(ar.write(tuple(row)))
    ar.cost['read'] += D
    ar.cost['write'] += D
    terminal=tuple(terminal)
    first=ar.read(tables[0]) if obj.width > 1 else terminal
    r=D if obj.width > 1 else 1
    initial=[]
    for j in range(2*r):
        z=Q(0)
        for a in range(D):
            x=ar.read(obj.left[a])
            y=ar.read(ar.read(first[a])[j])
            z=ar.add(z,ar.mul(x,y))
        initial.append(ar.write(z))
    ar.cost['read'] += 2*r
    ar.cost['write'] += 2*r+1
    initial=(tuple(initial),)
    chain=[ar.write(initial)]
    if obj.width > 1:
        for A in tables[1:-1]:
            chain.append(ar.write(ar.read(A)))
        chain.append(ar.write(terminal))
    ar.cost['read'] += len(chain)
    ar.cost['write'] += len(chain)
    chain=tuple(chain)
    cost=Counter(obj.cost)
    cost.update(ar.cost)
    return StoredProduced(obj,tables,chain,dict(cost))
