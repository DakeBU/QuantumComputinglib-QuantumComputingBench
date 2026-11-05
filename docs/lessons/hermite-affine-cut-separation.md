# Finite separation at affine Hermite sample cuts

Provenance: retrospective local mathematical exposition, prepared on 16 October
2026 for an independent whole-module migration review. This is not an external
paper attribution, a historical pre-proof seal, or a novelty claim. The historical
formalizer is not identified. The scope is exact real algebra, not a quantum
state-preparation algorithm or a complexity result.

## S1. What a finite separation certificate says

Let X and Y be arbitrary index sets and I a finite index set. A real matrix F on
X by Y has an I-separation if there exist real functions A(x,i) and B(i,y) such
that, for every x and y,

    F(x,y) = sum over i in I of A(x,i) B(i,y).

Both factors are mathematical witnesses, not promised executable tables. I may
be empty; then F is zero. Neither X nor Y is assumed finite in this definition.

## S2. Separation bounds matrix rank

When Y is finite, an I-separation implies rank(F) <= |I|. Indeed, the entrywise
identity is the matrix product F=AB and rank(AB)<=rank(A)<=|I|. This is a rank
bound, not an assertion of exact rank or an optimal decomposition.

## S3-S5. Polynomial and Hermite factors

For a real polynomial p of degree at most d and arbitrary real functions u(x)
and v(y), expand p(u(x)+z) in powers of z. Its coefficients give d+1 separated
terms for p(u(x)+v(y)): the left factors are the Taylor polynomial coefficients
at u(x), and the right factors are v(y)^i for 0<=i<=d. Zero polynomial and
d=0 are included. If Y is finite, the corresponding rank is at most d+1.

For specificity, the Hermite bridge used here is the following fixed polynomial,
not an unspecified degree-bounded oracle. For k a natural number, let

    A_k(t) = sum(r=0..k) [sum(m=0..r) choose(k+r-m,k)/m!] t^r,
    t = p+1,
    P_k(p) = exp(-1)(1-t)^(k+1) A_k(t)
             + t^(k+1) A_k(1-t).

The existing polynomial interface supplies degree(P_k)<=2k+1 and P_k(0)=1.
Consequently the rank of P_k(u(x)+v(y)) is at most 2k+2 when Y is finite.
Those polynomial prerequisites are reused; their production cost is not free.

## S6-S10. A small algebra of witnesses

A product u(x)v(y) has a one-element separation (S6). Since exp(a+b)=exp(a)exp(b),
exp(u(x)+v(y)) has the same width (S7). Given witnesses of widths I and J:

- Adding the two matrices concatenates their factors on the disjoint union
  I+J (S8).
- Negating the left factor preserves width I (S9).
- Multiplying entries, not multiplying matrices, pairs the two index sets and
  has width I times J: left A(x,i)C(x,j), right B(i,y)D(j,y) (S10).

These are symbolic witness transformations. No memory layout, operation count,
efficient access, isometry or physical circuit follows from them alone.

## S11-S13. Integer cuts need two separated terms

For natural numbers M,x,y,T with y<M,

    M*x+y<T  iff  x<T div M or (x=T div M and y<T mod M).       (S11)

The quotient/remainder identity and y<M justify the single boundary row.
In particular, for arbitrary natural-valued u on X and v on Y with v(y)<M
for every y, the indicator H_T(x,y)=1[M*u(x)+v(y)<T] equals

    1[u(x)<T div M] * 1
    + 1[u(x)=T div M] * 1[v(y)<T mod M].                       (S12)

Thus its width is two. Its complement also has width two, using the left
factors 1-1[u(x)<T div M] and -1[u(x)=T div M] with the same right factors (S13).
There is no required positivity hypothesis on M beyond the stated suffix bound:
an actual column with v(y)<M implies M>0. Empty Y is allowed and makes that
condition vacuous. T=0 and a cut at a row boundary are included.

## S14. Exact real cut to natural cut

For real a,h,t with h>0 and natural j,

    a+h*j<t  iff  j<ceil_N((t-a)/h).

Here ceil_N is the least nonnegative integer at least its real argument; it is
clamped at zero for a negative argument. No computability or finite-bit cost of
this real ceiling is asserted. Strictness is essential at exact grid junctions.

## S15. The same piecewise function at both junctions

Define f_k(p) as exp(p) for p<-1, P_k(p) for -1<=p<=0, and exp(-p) for p>0.
Since P_k(0)=1=exp(0), this same function can instead use the strict middle
condition p<0 and the right exponential at p=0. At p=-1 the polynomial branch
is still used. No endpoint sample is discarded or approximated.

## S16-S19. Literal affine samples and the width bound

The witness index set is the following tagged disjoint union (S16):

    ((two times singleton) + ((two + two) times {0,...,2k+1}))
        + (two times singleton).

Its cardinality is 2 + 4(2k+2) + 2 = 8k+12 (S17). These tags record witness
composition and are not physical qubits, ranks of minimal factors or ancillas.

For natural k,M, real a,h with h>0, and arbitrary natural-valued u,v with
v(y)<M, consider the exact sample matrix

    F(x,y)=f_k(a+h*(M*u(x)+v(y))).

Set T_left=ceil_N((-1-a)/h) and T_right=ceil_N((0-a)/h).
Write row(x)=a+h*M*u(x) and col(y)=h*v(y). Then F is exactly

    H_left * exp(row+col)
    + (H_right-H_left) * P_k(row+col)
    + (1-H_right) * exp(-(row+col)),

where all displayed multiplications with H are entrywise. S12, S13, S7, S3 and
S8-S10 produce respectively 2, 4(2k+2), and 2 witness components (S18).
The strict-cut conventions in S14-S15 handle both junctions. When Y is finite,
S2 and S17 give rank(F)<=8k+12 (S19). X,Y need not encode complete bitstrings,
and u,v are not required to be injective, surjective or mutually independent.

## S20. Constant scaling

Multiplying all entries by any real constant c preserves the witness width by
scaling A. This includes zero and negative c. It does not prove c is a valid
normalization or compute a normalization constant.

## Boundary for a state-preparation consumer

This exact-real separation is a reusable prerequisite, not a complete tensor
train or a preparation circuit. It proves no coherent entry oracle, bond-isometry
completion, physical bit order or embedding, terminal/ancilla cleanup, postselection
success, amplitude error, finite-bit stability, precision synthesis, classical
preprocessing/storage cost, total gates/depth, or poly(n_p) certificate. A rank
bound depending on k is not a poly(n_p) claim without parameter and cost bounds.
There is no epsilon, L, or n_p parameter in these statements. Substitution of a
particular scientific grid, its normalization and the full executable/root
acceptance chain remains a separate obligation.
