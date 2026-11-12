# Hermite bridges, exact cuts, and stored local blocks

Provenance: retrospective local mathematical exposition, 17 October 2026.
Historical formalizer: UNKNOWN. This document is not an external paper, a
historical pre-proof contract, an independent review, or a novelty claim.
All arithmetic below is exact unless explicitly described as integer-word
accounting. There is no approximation parameter or finite-bit theorem here.

## S1. The polynomial and the literal function

Let k be any natural number, including zero. For 0≤r≤k define

    a(k,r) = Σ(m=0..r) binom(k+r-m,k)/m!,
    A_k(t) = Σ(r=0..k) a(k,r)t^r,
    B_k(t) = (1-t)^(k+1) A_k(t),
    P_k(p) = exp(-1)B_k(p+1) + B_k(-p).

Thus, writing t=p+1, the second summand is t^(k+1)A_k(1-t).
The degree is at most 2k+1. For every integer j with 0≤j≤k,

    P_k^(j)(-1)=exp(-1),       P_k^(j)(0)=(-1)^j.

These are properties of the displayed polynomial, not data supplied to its
definition. One way to derive them is to take the first k+1 coefficients of
the formal series exp(X)/(1-X)^(k+1). Multiplication by (1-X)^(k+1)
recovers the coefficients 1/j! through degree k. Hence B_k^(j)(0)=1;
the factor (1-t)^(k+1) gives B_k^(j)(1)=0. Reflection gives (-1)^j.
No analytic convergence assumption is used. The same degree bound and jets
characterize P_k uniquely: a difference would be divisible by
p^(k+1)(p+1)^(k+1), of degree 2k+2.

The literal function is

    f_k(p) = exp(p)       if p<-1,
             P_k(p)     if -1≤p≤0,
             exp(-p)    if 0<p.

The polynomial, not the left exponential, supplies the value at -1; the
polynomial supplies the value at 0. Both values agree with the adjacent
exponential. A_k(t)>0 for t≥0, because its coefficients are nonnegative and
its constant coefficient is one. It follows that P_k>0 on [-1,0] and f_k>0
everywhere. These polynomial facts are prerequisites reused below, not cost
certificates for evaluating coefficients or samples.

## S2. A selector and one-junction differentiation

For real c and real functions f,g, put

    J_c(f,g)(x) = f(x) if x<c, and g(x) otherwise.

More generally, let E be any decidable pointwise predicate on the real line;
E need not be continuous or locally constant. If f and g have the same
derivative d at x and f(x)=g(x), then the function selecting f(y) on E(y)
and g(y) otherwise also has derivative d at x. Indeed its difference
quotient is, at each y, one of the two difference quotients based at the
common value. Both tend to d, so their arbitrary selection does too.

Suppose now that f,g are differentiable everywhere, f(c)=g(c), and
f'(c)=g'(c). Away from c the selected branch is constant on a neighborhood.
At c use the preceding common-slope argument. Thus for every x,

    (J_c(f,g))'(x) = J_c(f',g')(x).

This includes the derivative at c, where the right derivative value is used.

## S3. Finite-order gluing, including both endpoints

For any natural k, globally C^k functions f,g satisfying
f^(j)(c)=g^(j)(c) for every 0≤j≤k have globally C^k splice J_c(f,g).
For k=0, equality of values gives continuity at the only frontier point c.
For the induction step, the order-zero and order-one identities supply the
previous differentiation formula, and the remaining identities are matching
jets through order k for f' and g'. Apply induction to their splice.

For every j≥0, the j-th derivative of exp(p) is exp(p), and that of
exp(-p) is (-1)^j exp(-p). The jets in S1 therefore first glue P_k to
exp(-p) at zero. This right splice equals P_k on a neighborhood of -1
(all sufficiently nearby points are negative), so all of its derivatives
at -1 are those of P_k. Gluing exp(p) to this splice at -1 gives a
globally C^k function. It equals f_k everywhere: only p=0 changes branch
selection, and P_k(0)=1=exp(0). Consequently f_k is globally C^k on R.
The statement fixes the same k in the polynomial and in the regularity
order; it does not make a fixed f_k infinitely differentiable or C^(k+1).

## S4. Formula-derived translation matrices

Let d≥0 be a degree bound, unrelated to any sample-register width. Index rows
and columns by 0,…,d and use row-vector multiplication. Set

    v_d(x)_i = x^i,
    T_d(w)_(i,j) = binom(j,i) w^(j-i).

Here j-i is nonnegative integer subtraction truncated at zero; binom(j,i)=0
when i>j, so all entries below the diagonal vanish, even for w=0. The binomial
theorem gives the exact update

    v_d(x) T_d(w) = v_d(x+w).

For a finite list w_1,…,w_m, successively multiply on the right by these
matrices, with the empty list acting as the identity. The result is
v_d(origin+Σw_s). For any real polynomial q of degree at most d,
contracting this row with (q_0,…,q_d), its monomial coefficients, returns
q(origin+Σw_s). The degree bound is essential; it is not an assumed value
equality. For q=P_k choose d=2k+1. The bond has exactly 2k+2 coordinates,
independent of the number of weights. This is forward algebraic amplitude
semantics, not orthogonalization, numerical stability, a gate compilation,
or a cost theorem. No enumeration of binary words is needed for the identity.

## S5. Grid conventions and the exact natural cut

Let n≥0 and L>0. The full sample word has N=n+1 binary digits and 2^(n+1)
points. Define

    h = 2πL/2^(n+1) = πL/2^n >0,
    p_j = -πL+h*j       (j any natural number),
    C = ceil_N((-1+πL)/h),       M=2^n.

The natural ceiling ceil_N(x) is the least natural number ≥x and is zero
when x≤0. Then p_M=0, 0≤C≤M, and

    p_j<-1  iff j<C,
    p_j<0   iff j<M,
    -1≤p_j<0 iff C≤j<M.

Strict comparison is intentional: an exact sample at -1 belongs to the middle
part. The sample at zero may use the right part without changing f_k. There
is no restriction k≤n, n≥1, or πL>1. In particular C=0 and C=M are allowed.
The n used here is not the degree d of S4, and the full word width is n+1.

## S6. Exact-comparison binary search and its invariant

A run returns both a value and an eight-component nonnegative counter vector.
The components are field arithmetic, square root, inverse cosine, trigonometric
evaluation, comparison, stored-word read, stored-word write, and emitted record.
Sequential composition adds counters while passing the actual returned value.
Let e_q be one unit in component q.

For an interval with 2^r cells, supplied natural start s, real lower endpoint a,
and real width b, the search is:

    if r=0: compare a<-1; return s+1 if true, s otherwise;
    if r>0: half=b/2; middle=a+half; compare middle<-1;
            if true search (r-1,s+2^(r-1),middle,half),
            otherwise search (r-1,s,a,half).

Every comparison above is one exact-real comparison. The first case still
compares, so the one-cell case costs one comparison, not zero. The exact
counter vector for any inputs, even inputs not satisfying a grid invariant, is

    2r e_field + (r+1)e_compare.

Under L>0, a=p_s, b=h*2^r, and s≤C≤s+2^r, its returned value is C.
For r=0 the invariant confines C to s or s+1, distinguished by p_s<-1.
For r>0 the computed midpoint is p_(s+2^(r-1)); S5 confines C to the
chosen half, preserving both endpoint inequalities. Equality with -1 takes
the non-strict-cut half, which preserves the desired index.

Initialize b=πL by one multiplication and a=0-b by one subtraction, and run
the search with (r,s)=(n,0). The identity h*2^n=πL and C≤2^n supply the
invariant. The very same returned run has value C and exact counter vector

    (2n+2)e_field + (n+1)e_compare.

All other six components are zero. Values require L>0; the counter formula
does not. This does not implement exact real comparison on finite input
encodings. Natural index addition, powers of two, loop control and counter
bookkeeping are excluded here; they have no charged integer bit complexity.
There is no read/write allocation bound for this search in the selected model.

## S7. Supplied cached parent and width

For natural C,r define the aligned schedule

    s_r = 2^r floor(C/2^r),
    j_b = s_(r+1) + b*2^r       (b=0 or 1).

Given real origin a and step g, write x(j)=a+g*j. A parent record stores
two words (first,lower), and a tail-level record stores two real words
(width,factor). A child supplier receives these records AND supplied naturals
span, cut, midpoint and a Boolean b. The factor field is not used by this
supplier. The supplier does not generate its parent, width, span, cut, or
midpoint. For the source grid one later substitutes a=-πL, g=h, cut=C,
midpoint=2^n, and at chronological stage t one uses r=n-t.

For arbitrary natural lower,upper,first,size, use the literal predicates

    Full(lower,upper,first,size) := lower≤first and first+size≤upper,
    Outside(lower,upper,first,size) := first+size≤lower or upper≤first,
    Partial := not Full and not Outside.

These formulas apply to every natural input, including size zero or reversed
target endpoints; no unstated nonemptiness premise is imposed. For legal
nonempty intervals they describe containment, disjointness and an unresolved
intersection with the half-open target [lower,upper).

## S8. Flags and one child, with the actual charges

A flag routine receives lower,upper,first,last, with last the excluded
endpoint. It performs the four comparisons

    lower≤first, last≤upper, last≤lower, upper≤first,

then stores two Boolean words: full=the conjunction of the first two;
partial=not full and neither of the last two. If last=first+size they are
exactly the truth values of Full and Partial above. Its counter vector is
4e_compare+2e_write.

The child routine reads parent.first, parent.lower, and level.width (3 reads).
It selects the pair (real offset,natural offset)=(1,span) for b=1 and (0,0)
for b=0 (1 charged comparison). It sets

    first = parent.first + natural offset,
    last = first + span,
    lower = parent.lower + real offset*level.width,
    upper = lower + level.width.

There are two separately counted natural additions, including when the offset
is zero. The real calculations use one multiplication and two additions.
It calls the flag routine for [0,cut) and [cut,midpoint), reads the four
returned flags, and stores seven payload words: first,lower,upper and the
four flags. Therefore its exact eight-counter vector is

    3e_field + 9e_compare + 7e_read + 11e_write,

and its separate natural-addition count is 2. The other four counter
components vanish. The returned first,lower,upper and four flags have exactly
the formulas above; no source correctness is required for these literal facts.

To interpret the child as the source-aligned dyadic child one must supply
all FIVE equalities

    parent.first=s_(r+1),
    parent.lower=x(parent.first),
    level.width=g*2^r,
    span=2^r,
    midpoint=2^n.

Under these conditions the same returned child has first=j_b, lower=x(j_b),
upper=x(j_b+2^r), and its flags are Full/Partial for [0,cut) and [cut,2^n)
at (first,size)=(j_b,2^r). These are conclusions, not supplier assumptions.
The equalities are mathematical cache-coherence promises, not merely types.
No positivity of g or bound r≤n is needed for this equality refinement.

## S9. Both children from one returned run

Compute the b=0 and b=1 children once each. Materialize the vector in that
order, selecting the right precomputed child exactly when its index is one.
For a vector of length m, materialization stores the m counted results once,
then reads them to project values and aggregate stored metadata; the selected
model charges 2m reads and 2m writes. Scalar callbacks are not rerun.
Here the two selections add 2 comparisons and vector materialization adds
4 reads and 4 writes. The two-child run consequently has exact vector

    6e_field + 20e_compare + 18e_read + 26e_write,

whose sum is 70, and separate integer-addition count 4. Its index b returns
the b child of S8. With the five cache equalities of S8, BOTH children satisfy
the source refinement, while this same run retains the stated counters and
integer additions. A predicate describing child refinement abbreviates all
seven value/flag equalities; it does not weaken or add a premise.

If, additionally, cut≤2^n and r≤n, the returned first+span is strictly below
2^(n+2), so an n+2-bit unsigned word suffices for the endpoint. To see this,
s_(r+1)≤cut≤2^n and span=2^r≤2^n; each endpoint is at most 3*2^n<4*2^n.
This last bound requires only the parent-first and span equalities and these
two inequalities, not coordinate or width coherence. It does not give the
cost of implementing arithmetic on that word.

Natural additions here are single-word operations, not arbitrary-integer bit
complexity. The five supplied equalities do not charge generating powers,
casts, parent schedules or coordinates. Boolean conjunction/negation, finite
loop indexing, register-local tuple access, proofs and counter arithmetic are
outside the selected counters. Stored record payload and vector materialization
are charged as described; neither is silently a callback.

## S10. The local tagged bond and two stored field records

Set d=2k+1, P=d+1=2k+2 and D=2k+6. The bond is the tagged disjoint union

    {left boundary,left free}
      + {middle boundary,middle coefficient 0,…,middle coefficient d}
      + {right}.

There are D states, with integer layout left boundary 0, left free 1, middle
boundary 2, middle coefficient j at 3+j, and right at D-1. This is a fixed
explicit decoder using sums and an optional initial boundary tag, not a choice
based only on cardinality.

One supplied materialized record for each b∈{0,1} contains exactly:
a left-partial Boolean, a real left injection, a real left-free factor,
a middle-partial Boolean, a stored real vector of length P for middle injection,
a nested stored P-by-P real matrix for shared subdivision, and a real right
factor. Producing the two records and proving their source correctness are
separate supplier obligations. A matrix is rows of stored vectors; a record or
row reference counts as a word, not as a freshly evaluated scalar function.

## S11. Block meaning and stored entry reader

The record denotes the following D-by-D block diagonal matrix. The left block,
in boundary/free order, is

    [ 1[left partial]    left injection ]
    [       0               left free  ].

The middle block has boundary-boundary entry 1[middle partial], boundary-to-
coefficient row equal to the stored injection vector, coefficient-to-boundary
column zero, and coefficient-coefficient block the stored shared matrix.
The right block is the stored right factor. Every cross-block entry is zero.

An actual block reader uses eight conservative charged comparisons for the
two decoded tag dispatches. Beyond those eight: each boundary-boundary case
reads its Boolean (one read) and selects 1 or 0 (one comparison); each scalar
injection/free/right case reads one scalar; the middle injection case reads
the vector reference then its scalar (two reads); the shared case reads the
matrix reference, row reference, then scalar (three reads); a zero case returns
literal zero without numerical reads. Its value is exactly the block entry.

Decoding each integer bond index is charged eight comparisons. The explicit
sum thresholds and optional boundary decoder use at most six actual comparison
tests per index, including the equality-to-zero and failed-branch less-than-zero
tests; eight is a conservative charge. Index arithmetic and product-index
decoding are excluded word arithmetic, not a finite-bit runtime assertion.

A complete entry reader first reads the selected one of the two field records
(one read), decodes both bonds (16 charged comparisons), and runs the block
reader (eight dispatch comparisons plus the case-specific work). Its returned
value is the corresponding record's block entry, and its per-component counter
is at most 29; the block reader's per-component counter is at most 12.
These bounds hold for arbitrary records and all k≥0 without source promises.

## S12. Materialized two-slice table and its costs

Materialize all D rows and 2D columns, with output column indexed by the pair
(b,outgoing bond); integer flattening is b*D+outgoing. Thus each row contains
both bit slices. Each of the 2D^2 entry readers runs once. Nested vector
materialization adds exactly

    (2D^2+D)*(2e_read+2e_write)

to their summed counters. For every one of the eight components, the resulting
counter is at most 72D^2; summing all eight gives at most 576D^2. These are
conservative bounds, not equality claims. The returned table entry at
(a,(b,c)) is exactly the block meaning of record b at decoded states a,c.
Both the value identity and the cost bound concern this one materializing run.
There are no scalar field operations, square roots, angle or trigonometric
evaluations, or emitted rotations in the entry/assembly algorithm itself.

These costs exclude generation of the field records, source exponentials,
source coefficients, interval restriction/subdivision and coordinates. No
source-kernel callback is called during assembly. Counter/proof bookkeeping
and natural index arithmetic are excluded. In particular the sum over eight
counters does not include a hidden exponential or integer bit-cost counter.

## S13. Explicit source-supplier conditions

The following specifies exactly what the supplied fields must contain for
identification with the source local kernel. For any natural k,n,t and real L,
put r=n-t using truncated natural subtraction, g=2πL/2^(n+1), a=-πL,
C=ceil_N((-1-a)/g), M=2^n, first=s_(r+1)+b*2^r, and size=2^r.
Division by zero, if encountered outside the legal L>0 grid, has the total
real-field convention x/0=0. Thus these are all-carrier formulas; to interpret
t as an actual stage of the positive source grid one uses L>0 and 0≤t≤n.

For 0≤i,j≤d, define the two shared row-update matrices by

    S_0(i,j) = binom(j,i)/2^j                     if i≤j, else 0,
    S_1(i,j) = binom(d-j,i-j)/2^(d-j)             if j≤i, else 0.

To specify the source injection vector without a scalar-evaluation oracle,
let β_j be the unique degree-d Bernstein coordinates of P_k(t-1):

    Σ(j=0..d) β_j binom(d,j)t^j(1-t)^(d-j) = P_k(t-1).

Equivalently, put

    ℓ_j = Σ(i=0..k) Σ(v=0..k-i)
            1[j=i+v] a(k,i) binom(k-i,v)/binom(d,i+v),
    β_j = exp(-1)ℓ_j + ℓ_(d-j).

For a coefficient row c define D_z c(i)=(1-z)c_i+zc_(i+1),
L_z(c)_i=(D_z^i c)_0, and R_u(c)_i=L_(1-u)(j↦c_(d-j))_(d-i).
The literal interval-restriction row is

    Restrict(u,v,c) = L_((v-u)/(1-u))(R_u(c)).

Only indices 0,…,d affect the indicated entries; arbitrary extensions beyond d
do not matter. This literal formula is defined even when u=1 by total division;
the affine polynomial restriction interpretation requires u≠1. A fully included
middle child on a legal positive grid has u=1+x(first)<1, so this condition
is supplied by that geometric fact, not imposed as an extra kernel-output
assumption. Set u=1+x(first), v=1+x(first+size), with x(j)=a+g*j.

The seven supplier clauses, all required together for each bit b, are:

1. Left-partial flag equals Partial(0,C,first,size).
2. Left injection equals exp(x(first)+g*(2^r-1)) when
   Full(0,C,first,size), and equals zero otherwise.
3. Left-free factor equals 1 for b=1, and exp(-g*2^r) for b=0.
4. Middle-partial flag equals Partial(C,M,first,size).
5. Every entry j of the middle injection is Restrict(u,v,β)_j when
   Full(C,M,first,size), and zero otherwise.
6. Every shared matrix entry (i,j) equals S_b(i,j).
7. Right factor equals b (as the real number 0 or 1) if r=n;
   otherwise it equals exp(-g*2^r) for b=1 and 1 for b=0.

The injection zeros on disabled children are part of the supplied numerical
data. A bare unguarded injection row does not satisfy these conditions merely
because a later flag happens to be false. These clauses are mathematical
equalities about stored fields, not typing premises and not a procedure that
produces the records. No clause assumes equality of the assembled table with
the source kernel.

## S14. What conditional assembly actually identifies

Define a source local kernel by the block form of S11 with entries given by
the seven formulas in S13. Direct case analysis on the two tagged bonds proves
that a record satisfying all seven clauses has precisely this block meaning.
Apply this to both supplied records and the entry identity in S12: the table
returned by the very same assembly run has, for every integer incoming bond,
bit and outgoing bond, exactly this source kernel entry in the explicit layout
at stage t. The uniform cost bounds of S12 still apply to that run.

This is local table refinement, not production of all raw-source-chain data.
The translation matrices of S4 are monomial translation; S13 uses a distinct
Bernstein restriction/subdivision representation. The two interfaces must not
be silently identified just because both have P coordinates. The results here
alone assert no complete normalized quantum state, PREPARE/SELECT oracle,
unitarity, isometry, clean ancillas, postselection probability, numerical error,
finite-bit stability, gate/depth bound, or efficient whole-source producer.
They are exact classical/algebraic prerequisites with explicitly conditional
stored suppliers and explicitly limited operation accounting.
