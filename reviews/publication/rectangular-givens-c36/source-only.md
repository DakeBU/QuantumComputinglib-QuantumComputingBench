# Exact rectangular row elimination and reversible recovery

## Provenance and scope

This is a retrospective, implementation-informed local mathematical source,
authored by `/root` for independent comparison. It is not a historical paper,
a novelty claim, or a pre-proof Statement Seal. The implementation predates this
document. Independent reviewers must preserve that timing rather than claiming
that this prose independently predicted the code. The object is a reusable
exact-real linear-algebra construction, not a finite-bit quantum compiler.

## S1. Carrier, rotation convention, and chronological lists

Let N and M be arbitrary natural numbers, including zero, and let A be an
N-by-M real matrix. Rows and columns are numbered starting at zero. A plane
rotation on distinct rows i,j left-multiplies A, changing those two rows by

    new row i = cos(theta/2) row i - sin(theta/2) row j,
    new row j = sin(theta/2) row i + cos(theta/2) row j.

It fixes all other rows. Each rotation is orthogonal with determinant +1.
If a rotation list is [G1,...,Gs], its chronological action applies G1 first;
its accumulated matrix is U=Gs ... G1, not G1 ... Gs. The empty list acts by
the identity, including the empty-dimensional identity.

The required single-column supplier is a deterministic adjacent-row sweep.
For a column c and rows lo through lo+t<N, it visits adjacent pairs
(lo+t-1,lo+t), ..., (lo,lo+1), always evaluating the elimination angle from
the CURRENT matrix. For a pair of column entries x,y it uses the negative of
the exact signed preparation angle. This sends (x,y) to (sqrt(x*x+y*y),0).
The pair (0,0) uses angle zero. The sweep emits t rotation records, including
zero-angle records; it does not silently prune them.

We use the supplier's mathematical facts as dependencies: the emitted list
has exactly that chronological matrix action, zeros the processed column below
lo, and preserves an older column whenever that older column vanishes on the
whole rotated row interval. These are not assumptions on the final input A.
Proofs of the supplier itself are outside this source; the interface and use
sites are explicit so that a missing supplier cannot be hidden by a diagram.

## S2. Two synchronized recurrences

For k,r natural with k+r<=M, define a residual sweep B(A,k,r) and a list
T(A,k,r). For r=0 they return A and the empty list. For r>0:

- if k<N, run the single-column supplier on column k, rows k through N-1;
  let A' be its result and Q its emitted chronological list. Return
  B(A',k+1,r-1) and Q followed by T(A',k+1,r-1);
- if k>=N, there is no pivot row. Return B(A,k+1,r-1) and T(A,k+1,r-1)
  without a rotation or any change to A.

The current-matrix dependence is essential: the next column is NOT eliminated
using the original unmodified A, and a fixed arbitrary orthogonal certificate
is not substituted for this actual computed list.

Claim S2a: applying T(A,k,r) chronologically to A gives B(A,k,r).
Proof: induction on r. The nonempty branch composes the actual first-column
list action with the inductive next-column action. In the skip branch both
recurrences proceed with the same unchanged matrix. Empty r is immediate.

## S3. Prefix invariant and strict-below-diagonal zeros

Define Prefix(A,k) to mean: for every column c<M with c<k, and every row i<N
with c<i, the entry A[i,c] is zero. It does not assert diagonal positivity,
full rank, normalization or any factorization of A.

Claim S3a: if k<N and Prefix(A,k), the single-column sweep on column k
establishes Prefix(A',k+1). For the new column use its zeroing fact. For an
older column c<k, every row touched by the sweep is >=k>c; all its entries
were zero there. Each row rotation preserves that zero column segment.

Claim S3b: if Prefix(A,k), then Prefix(B(A,k,r),k+r).
Induct on r, using S3a when k<N. If k>=N, the next prefix condition adds no
possible below-diagonal entry at column k: an i<N with k<i cannot exist.
Thus the unchanged matrix satisfies Prefix(A,k+1), and induction applies.
This handles tall/wide/empty shapes without a full-rank or nonzero-pivot premise.

## S4. List-length bound

Claim S4: length(T(A,k,r)) <= N*r. Again induct on r. A non-skipped column
emits N-1-k records, at most N; concatenate it with the inductive bound for
r-1. A skipped column emits none. All subtraction on the natural row indices
is truncated; the non-skipped guard supplies k<N. This is a bound on the
actual list, not arithmetic runtime, storage, numerical precision, or gates.

## S5. Accumulated rotation matrix

For EVERY valid adjacent-rotation list T on N rows, write U(T) for its
chronological product. Claim S5a: transpose(U(T))*U(T)=I. Induct on the list:
for a first rotation G and remainder product V, U=V*G, so
U^T U = G^T V^T V G = G^T G = I. Claim S5b: det(U(T))=1, since the
determinant of the empty identity and each plane factor is one. These claims
do not require A to be orthogonal, and do not assert that the residual is I.

## S6. Complete computed outputs and final theorem chain

Define T(A)=T(A,0,M), R(A)=B(A,0,M), and U(A)=U(T(A)). Then:

1. chronological application of T(A) to A equals R(A) (S2a);
2. U(A)*A=R(A), by the chronological product/action identity;
3. R(A)[i,c]=0 whenever c<i, using the vacuous initial Prefix(A,0) and S3b;
4. length(T(A))<=N*M (S4);
5. U(A)^T U(A)=I and det(U(A))=1 (S5);
6. U(A)^T R(A)=A, by multiplying the equality in item 2 on the left by U(A)^T.

These statements quantify over all real rectangular A with no rank, isometry,
unit-vector, positive-diagonal, or SO premise on A. Recovery is of the original
matrix from the actual computed residual, not a supplied identity residual.
The construction is a source for reusable thin-factorization/isometry routines;
those downstream constructions require their own statements and certificates.

## S7. Evidence and resource boundaries

All matrices, angles, comparisons and trigonometric functions are exact-real
mathematics. No finite-bit representation, rational/irrational evaluation
algorithm, charged scalar operations, matrix-entry oracle, vector copying,
read/write count, numerical stability, gate set, ancilla cleanup, postselection,
or approximation tolerance is certified here. A symbolic list-length theorem
must not be relabeled a runtime theorem. If N is an exponentially sized
Hilbert-space dimension, a bound polynomial in N is not polynomial in its
qubit count. Row indices here are matrix indices, not a promised physical
qubit/wire layout. The rotation sign and chronological product convention
remain exact; global/relative phases or basis permutations are not quotiented
away by this real-matrix interface. Quantum compilation is a separate adapter.

## Source proof graph

S1's primitive action/zeroing/preservation/orthogonality/determinant interfaces
are separate supplier tails. S2 defines the paired residual/list and proves
action. S3 defines Prefix and proves its one-column and recursive preservation.
S4 proves list length independently of S3. S5 proves orthogonality and determinant
for arbitrary lists. S6 uses the appropriate AND tails: action plus product
semantics for U*A=R; prefix preservation for triangularity; list length for
the count; plane orthogonality for U^T*U=I; and both U*A=R and U^T*U=I for
recovery. These are source/construction dependencies, not claims that every
imported Lean declaration depends on every other one. S7 is an explicit
excluded-boundary node. No alternative numerical routine is silently included.
