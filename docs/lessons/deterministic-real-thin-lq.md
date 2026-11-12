# Deterministic real thin LQ factors

A real matrix can be reconstructed from a fixed number of orthonormal row
directions even when its rows are zero or dependent. Here the factors are
specified by a particular sequence of adjacent row rotations, rather than
selected from an existence theorem. The construction uses exact real
arithmetic; its equations alone do not certify numerical stability or running
time.

## Matrices and output equations

Let \(m,n\) be nonnegative integers, let
\(A\in\mathbb R^{m\times n}\), and set \(r=\min(m,n)\).
A factor record contains matrices
\[
 R\in\mathbb R^{m\times r},\qquad Q\in\mathbb R^{r\times n}
\]
and proofs of the two equations
\[
 A=RQ,\qquad QQ^{\mathsf T}=I_r.
\]
The second equation means that the rows of \(Q\) are orthonormal. A record
type describes these obligations; a constructor must still produce the factors
and prove the equations. The inner dimension is \(r\), not the rank of
\(A\). This contract does not require a triangular factor, unique factors,
full rank, positive entries, or nonzero rows.

The scalar field is real and \(\mathsf T\) is ordinary transpose. No quantum
register, oracle, ancilla, phase, success probability, or approximation
parameter is part of this matrix contract.

Lean object: `QuantumBlockEncoding.ConstructiveThinLQ.Factorization`.

## The fixed row elimination procedure

For real \(x,y\), put \(\rho=\sqrt{x^2+y^2}\). If \(\rho=0\), both
entries are zero and use angle zero. Otherwise define
\[
 \alpha(x,y)=
 \begin{cases}
 -\arccos(x/\rho),&y<0,\\
 \arccos(x/\rho),&y\ge0.
 \end{cases}
\]
The quotient lies in \([-1,1]\), and this signed choice satisfies
\(\cos\alpha=x/\rho\), \(\sin\alpha=y/\rho\). Apply the ordered plane
rotation with angle \(-2\alpha\), using the half-angle convention
\[
 \begin{pmatrix}
 \cos(\theta/2)&-\sin(\theta/2)\\
 \sin(\theta/2)&\cos(\theta/2)
 \end{pmatrix}.
\]
On the two selected rows this sends their entries in the current column to
\((\rho,0)\). All other rows are unchanged. Each plane matrix is orthogonal,
has determinant one, and acts on the entire row, not just the pivot entries.
The zero-pair branch is a valid identity operation on that pair, not division
by zero or a substitute matrix value.

For a matrix \(B\) with \(N\) rows and \(M\) columns, process columns
\(c=0,\ldots,M-1\) in order. When \(c<N\), use the adjacent row pairs
\((N-2,N-1),(N-3,N-2),\ldots,(c,c+1)\), recomputing each angle from the
current matrix. When \(c\ge N\), there are no entries below that pivot
position, so advance without a rotation. An empty range of pairs performs no
operation.

Write \(S(B)\) for the accumulated square transform and \(T(B)\) for the
resulting rectangular matrix. The chronological first rotation acts first:
if the list is \(G_1,\ldots,G_s\), then
\(S(B)=G_s\cdots G_1\). The exact procedure gives
\[
 S(B)B=T(B),\qquad S(B)^{\mathsf T}S(B)=I_N,
 \qquad T(B)_{ji}=0\quad(i<j).
\]
Indeed, a bottom-up pass zeroes the current column below its diagonal. For
each earlier column, both entries of every affected pair are already zero,
so the pass preserves all previous zeros. Induction over columns proves the
displayed residual property. Multiplying the individual orthogonal matrices
proves orthogonality of \(S(B)\), and applying the chronological list proves
the first equation. Consequently
\[
 S(B)^{\mathsf T}T(B)=B.
\]
Because \(S(B)\) is square, its orthogonality also gives
\(S(B)S(B)^{\mathsf T}=I_N\).

These are dependencies from `AdjacentGivens` and `RectangularGivens`, not extra
assumptions supplied by a factorization caller. They define the exact procedure
used below; no claim about evaluating square roots, inverse trigonometric
functions, comparisons, or matrix entries at finite precision follows here.

## Wide matrices

Assume \(m\le n\). Apply the fixed procedure to \(B=A^{\mathsf T}\),
which has \(n\) rows and \(m\) columns. Define the actual factors by
\[
 R_{ik}=T(A^{\mathsf T})_{ki}\quad(0\le i,k<m),
 \qquad
 Q_{kj}=S(A^{\mathsf T})_{kj}\quad(0\le k<m, 0\le j<n).
\]
These are the transpose of the leading \(m\) residual rows and the leading
\(m\) transform rows. They are literal extractions from this one specified
elimination procedure, not arbitrary factors with similar equations.

Transposing the recovery equation gives
\[
 T(A^{\mathsf T})^{\mathsf T}S(A^{\mathsf T})=A.
\]
For each entry, its sum over all \(n\) indices therefore satisfies
\[
 A_{ij}=\sum_{\ell=0}^{n-1}T(A^{\mathsf T})_{\ell i}
                            S(A^{\mathsf T})_{\ell j}.
\]
If \(\ell\ge m\), then \(i<m\le\ell\), so the residual entry is zero.
Removing these zero terms leaves
\[
 A_{ij}=\sum_{k=0}^{m-1}R_{ik}Q_{kj}=(RQ)_{ij}.
\]
The prefix-sum identity is the shared `ThinLQ.sum_prefix_of_zero` prerequisite.
There is no full-rank premise hidden in this truncation.

The rows of the full square transform are orthonormal. Taking the leading
\(m\) rows preserves their pairwise inner products:
\[
 (QQ^{\mathsf T})_{ab}
   =\sum_{j=0}^{n-1}S(A^{\mathsf T})_{aj}S(A^{\mathsf T})_{bj}
   =\delta_{ab}\quad(0\le a,b<m).
\]
Thus the actual wide factors have both required equations, including when the
input has repeated or zero rows.

Lean definitions: `QuantumBlockEncoding.ConstructiveThinLQ.wideR` and
`QuantumBlockEncoding.ConstructiveThinLQ.wideQ`. The two proofs are
`wide_factorization` and `wide_orthogonal` in the same namespace.
`factorOfLE` packages these factors and proofs into a factor record of inner
dimension \(m\).

## Tall and empty matrices

For all shapes, compare the dimensions. When \(m\le n\), use the wide
constructor and \(r=m\). When \(m>n\), choose the specified factors
\(R=A\) and \(Q=I_n\). Then \(r=n\), \(A=AI_n\), and
\(I_nI_n^{\mathsf T}=I_n\). This branch satisfies the two equations; it does
not promise an additional triangularity property of \(A\).

This prescription includes empty dimensions. For \(m=0\), the wide factors
have zero inner dimension; no pivot is required and the reconstruction has no
row entries to check. For \(n=0<m\), the tall branch uses the empty identity.
For \(m=n=0\), the wide branch also gives the empty equations. In each case,
the identity of the zero-dimensional space is an empty matrix, not an
unjustified nonzero scalar.

Lean definition: `QuantumBlockEncoding.ConstructiveThinLQ.factor`. The theorem
`QuantumBlockEncoding.ConstructiveThinLQ.factor_correct` states the two
equations for that actual returned factor record. Neither output correctness
nor dimension comparison uses the earlier existence theorem to select factors.

## Reuse and the four graph views

The source construction consists of the signed plane rule, bottom-up pass,
preserved-zero invariant, chronological transform, wide extraction and
dimension cases. The wide and tall cases jointly cover all shapes; neither
unguarded case is a sufficient route for every matrix.

The Lean graph has actual imports of `RectangularGivens` and `ThinLQ` and named
calls to recovery, below-diagonal zeros, transform orthogonality and prefix-sum
removal. Imports alone do not describe every theorem dependency, and this
description is not an exported elaborated proof-term graph.

The compressed mathematical move is “eliminate the transpose, discard the
provably zero residual tail, retain an orthonormal row frame.” Its expansion is
the procedure and entrywise proofs above. The stored-factor supplier and
tensor-train consumers reuse this interface, but their storage, contraction,
quantum action and cost claims require their own proofs.

The Functor Hypergraph may represent a conceptual transport from rectangular
matrix coordinates to an orthonormal row-frame representation, conditional on
the reconstructed equations and exact-real conventions. It is not a certified
categorical functor, a quantum circuit, or a complexity transport.

The authoritative formal source is
[ConstructiveThinLQ.lean](../../QuantumBlockEncoding/ConstructiveThinLQ.lean).
Its exact current source supplies Lean disclosures rather than a copied proof.
This is a retrospective local explanation of an existing constructor, not a new
algorithm or an external-paper assimilation claim. Whole-module local review
is tracked in `website/research/publications.json`; it is distinct from full
migration, numerical certification and the Hermite scientific root.
