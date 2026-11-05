# Phase 1: independent source-only derivation

Source: *Exact rectangular row elimination and reversible recovery*, SHA-256
`fe6357c4a8714ba463b00a0d575a28b2387bff7a1cfd9478f063a0bd6ddd12bb`.

This is a review of a RETROSPECTIVE_IMPLEMENTATION_INFORMED local source.
The implementation predates the source. This review does not establish
historical-paper fidelity, novelty, a pre-proof statement seal, or an
implementation-independent origin for the source. The reviewer has not read
the implementation, formal decoder packet, earlier lessons, registry, or
other reviews. All derivations below were made from this source and ordinary
finite-dimensional real algebra. No Lean or numerical validation was run.

## 1. Frozen mathematical contract and binders

Let N,M be arbitrary natural numbers. Let A have entries A[i,c] in the real
numbers, with 0 <= i < N and 0 <= c < M. For intermediate calls let k,r be
natural with k+r <= M. Thus r>0 implies k<M and the active column exists.
The first guard k<N additionally supplies the pivot row and the valid
interval k,...,N-1. There is no condition N<=M or M<=N.

The intended complete output is the specific recursively computed pair
(T(A),R(A)), with T(A)=T(A,0,M) and R(A)=B(A,0,M), and the square N-by-N
matrix U(A) obtained from T(A). The conclusions are simultaneously:

    action(T(A), A) = R(A),
    U(A) A = R(A),
    for all i<N, c<M, c<i: R(A)[i,c]=0,
    length(T(A)) <= N M,
    U(A)^T U(A)=I_N,
    det(U(A))=1,
    U(A)^T R(A)=A.

N,M and index membership are TYPING data; the real scalar convention,
zero-based order, rotation convention, and chronological convention are
STANDING source conventions. A is an unrestricted SOURCE input. The
intermediate inequality k+r<=M is a SOURCE domain restriction. The premise
Prefix(A,k) belongs only to the auxiliary preservation theorem, not to the
complete output theorem. Supplier action, zeroing, preservation, length,
orthogonality, determinant, and product/action compatibility are dependency
obligations, never extra assumptions on A. No RULED correction has been
authorized and no additional rank, nonzero, isometry, positivity, or
normalization binder may be added.

Definitions are literal recurrences and explicit finite products, not a
characterized choice of an arbitrary orthogonal certificate. Prefix is a
literal predicate. There is no quotient by phase or by basis permutation.
The signed-angle subroutine is an externally supplied literal interface;
its exact representative requires the clarification in section 8.

## 2. One rotation and its sign

For distinct i,j the affected block is

    G(theta) = [[a,-b],[b,a]],
    a=cos(theta/2), b=sin(theta/2).

Direct multiplication gives G(theta)^T G(theta)=I_2, since a^2+b^2=1
and the cross terms cancel. Its determinant is a^2+b^2=1. All other rows
form an identity block; simultaneously reordering rows and columns to expose
the two-dimensional block changes neither determinant nor orthogonality.
Hence the embedded matrix has determinant +1 on all N rows.

For rho=sqrt(x^2+y^2)>0, a signed preparation angle alpha must satisfy

    cos(alpha/2)=x/rho, sin(alpha/2)=y/rho.

Using theta=-alpha therefore gives

    G(-alpha) [x;y]
      = [(x/rho)x+(y/rho)y; -(y/rho)x+(x/rho)y]
      = [rho;0].

The last equality uses rho^2=x^2+y^2 and rho>0. If rho=0 then x=y=0,
and theta=0 fixes the zero pair. This derives the supplier's required sign;
it does not simply assume that the word "elimination" supplies the result.
One possible independent realization is alpha=2 atan2(y,x) off the origin,
with zero at the origin. This is an illustrative realization, NOT a claim
that the source selected this exact branch or the implementation uses it.

For the discriminating pair (x,y)=(0,1), alpha=pi and theta=-pi sends
(0,1) to (1,0); theta=+pi instead sends it to (-1,0). For (-1,0), a
nontrivial two-row rotation can change the first component to +1. This does
not imply every terminal diagonal entry in the complete algorithm is
nonnegative: a one-row terminal interval has no rotation.

## 3. Adjacent sweep: independent reconstruction of supplier obligations

Fix 0<=c<M, lo,t natural, and lo+t<N. Starting at the current matrix,
for q=t,t-1,...,1 rotate rows lo+q-1 and lo+q using their CURRENT entries
in column c. Each step zeros row lo+q of that column. Later steps use only
rows <=lo+q-1, so they cannot recreate that already eliminated entry.
Induction over these t steps therefore zeros exactly the interval

    lo < i <= lo+t.

There are t visited pairs and exactly t emitted records, even when an angle
is zero. The case t=0 emits the empty list and does not change the matrix.
Rows outside [lo,lo+t] are unchanged.

If another column is zero on this entire interval before the sweep, each
rotation takes a pair (0,0) in that OTHER column to (0,0), regardless of the
angle computed from column c. Thus the column remains unchanged everywhere:
it stays zero inside the interval and is untouched outside. This argument
does not need that other column to be globally zero.

These elementary arguments reconstruct the mathematical interface. The
source expressly places the supplier proofs outside its scope; a later
implementation comparison must bind actual supplier certificates rather
than treating this explanation as a compiled proof.

## 4. Chronology and the synchronized recurrences

Define action([],X)=X and action(G::L,X)=action(L,GX). Set U([])=I_N
and U(G::L)=U(L)G. By list induction,

    action(L,X)=U(L)X,
    action(Q ++ L,X)=action(L,action(Q,X)),
    U(Q ++ L)=U(L)U(Q).

These identities fix composition order before use. A concrete check is N=3:
take G1 to rotate rows (0,1) by theta=pi and G2 to rotate (1,2) by theta=pi.
Then chronological action on e0 is e0 -> e1 -> e2. The reversed product
G1 G2 instead sends e0 to e1. This distinguishes the two product conventions.

For S2a induct on r, with the statement generalized over the current A,k.
At r=0, both recurrences return A and []. At r>0, write r=s+1.
If k<N, the supplier gives Q,A' with action(Q,A)=A'. The next call is
legal because (k+1)+s=k+r<=M. By induction on that actual A',

    action(Q ++ T(A',k+1,s),A)
      = action(T(A',k+1,s),A')
      = B(A',k+1,s).

This is exactly the residual recurrence. If k>=N, both recurrences skip
the column with the same unchanged A and invoke the same legal next call.
No supplier is called in that branch. This proves synchronization for all
legal k,r, not just k=0.

The current-matrix requirement is substantive. For example start with rows
(1,0), (1,1), (0,1). Eliminating column 0 gives rows
(sqrt(2),1/sqrt(2)), (0,1/sqrt(2)), (0,1). The second-column pair is now
(1/sqrt(2),1), not its original pair (1,1). Reusing the angle for (1,1)
would leave the last entry 1/sqrt(2)-1/2, which is nonzero.

## 5. Prefix and the skip branch

Prefix(A,k) means that for every c<M with c<k and every i<N with c<i,
A[i,c]=0. At k=0 it is vacuous. It says nothing about diagonal signs or rank.

Assume k<N, k<M and Prefix(A,k). In the full supplier interval k,...,N-1,
every entry of every older column c<k is zero because its row index is
>=k>c. Section 3 therefore preserves those columns. Rows outside the interval
are untouched. The supplier zeros the new column k at every i>k. For a
column c<k+1, natural-number order gives c<k or c=k. These two cases prove
Prefix(A',k+1).

If instead k>=N, the only newly admitted column c=k has no below-diagonal
row: i<N<=k contradicts k<i. Older columns are unchanged. Thus
Prefix(A,k+1) already follows from Prefix(A,k), with no rotation.

Induction on r now proves Prefix(B(A,k,r),k+r), using the updated A' in the
active branch and unchanged A in the skip branch. For the complete call,
k+r=M, so every c<M is covered, and the strict-below-diagonal conclusion
follows. This does not assert a full QR/LQ factorization, a thin factor,
a canonical isometry completion, or an identity residual.

## 6. Count, orthogonality, determinant, and recovery

Let ell(A,k,r)=length(T(A,k,r)). In an active branch the exact number
of emitted records is t=N-1-k (natural subtraction under k<N), giving

    ell(A,k,s+1) = (N-1-k) + ell(A',k+1,s)
                 <= N + N s = N(s+1).

A skipped branch emits zero and has ell(A,k,s+1)<=Ns<=N(s+1).
The base case is zero. The proof uses no Prefix result and does not remove
zero-angle rotations. Independently, the recurrence yields the sharper
reviewer consequence

    ell(A,k,r) = sum over 0<=q<r of
                  (if k+q<N then N-1-(k+q) else 0).

This extra formula is not a source claim. It shows the count is shape-based,
not rank-dependent. For p=min(M,N), the complete count is
p(N-1)-p(p-1)/2 when N>0, and zero when N=0. Only the weaker N M bound
is required for comparison to S4.

For every valid rotation list, independently of A, induct on its head G.
If V=U(tail), then U=VG and

    U^T U = G^T V^T V G = G^T G = I_N,
    det(U)=det(V)det(G)=1.

The empty-list identity supplies both bases. The determinant conclusion
requires the +1 determinant of the factors; orthogonality alone would allow
determinant -1. Adjacency is sufficient but not mathematically needed for
these two identities; distinct valid row indices and the rotation block are.

Finally synchronization AND product/action semantics give U(A)A=R(A).
With the separate orthogonality result,

    U(A)^T R(A) = U(A)^T(U(A)A)
                = (U(A)^T U(A))A = A.

Neither determinant one, triangularity, nor the count is needed for this
recovery step. Conversely, orthogonality by itself does not connect U to the
computed R. There is no basis for replacing R(A) by I.

## 7. Edge-case audit

- N=0: every column step skips; T=[]; all 0-by-M entries and triangularity
  are vacuous. U is the unique 0-by-0 identity and its determinant is 1.
  The action and recovery equalities remain well-typed.
- M=0: r=0 immediately; A and R are N-by-0; U=I_N and T=[].
- N=1: every active interval has t=0, so every A is left unchanged. In
  particular A=[-1] has negative diagonal and R is not I. No below-diagonal
  entry exists.
- k=N-1: the final pivot interval has one row and emits no rotation.
- k>=N, r>0: all remaining calls skip without changing A; the prefix
  extension is vacuous for new columns, not a zero-pivot assumption.
- Tall A: the full interval below each available column is swept. Wide A:
  later columns have no below-diagonal rows and may retain arbitrary entries.
- All-zero or rank-deficient A: zero pairs use the specified zero angle and
  still emit records. For N=2,M=1,A=0, there is one record, not zero records.
- Negative data, zero pivot above a nonzero lower entry, and negative final
  diagonal are admitted. No division by a zero norm is needed if the
  supplied angle follows the explicit zero branch.

## 8. Source clarifications and exact failure boundaries

F1 — local-zeroing scope (S1, lines 27-39). Read literally over all rows,
"zeros ... below lo" is false for a partial interval. Take N=3,M=1,
A=(0,0,1)^T, lo=0,t=1. The sole pair is (0,0), so the emitted zero-angle
rotation leaves row 2 equal to 1 although 2>lo. The true supplier conclusion
is lo<i<=lo+t, with rows outside the interval unchanged. Every S2 use has
lo=k and t=N-1-k, so this local reading already covers every needed i>k.
This is a source-contract wording ambiguity, with an explicit counterexample
to its unbounded reading; it is not a counterexample to S2-S6. The proposed
interval qualification is a proposed clarification, not an authorized rewrite
of the pinned source. A later reviewer must check the actual formal scope.

F2 — exact angle-record representative (S1, lines 29-31). The source does
not define the signed preparation angle's range/branch. The needed matrix
action follows from the two trigonometric equations in section 2. Those
equations do not distinguish alpha from alpha+4pi, and hence do not uniquely
specify the stored real-angle record off the origin. For example alpha=0
and alpha=4pi both prepare (1,0), giving different exact elimination-angle
records but identical rotation matrices. The source explicitly fixes the
origin angle to zero, but does not fix every other representative. If exact
record equality to the implementation is required, supply a pinned definition
of the deterministic angle function. If only action, zeros, count,
orthogonality, determinant, and recovery are compared, representative freedom
does not invalidate those claims. This is an external-interface precision
obligation, not permission to select a different algorithm silently.

No rank or nonzero-pivot repair is necessary. No counterexample to the
complete matrix-level theorem chain was found under the stated full-sweep
supplier interface. This qualified mathematical assessment is not a formal
equivalence verdict and not a publication acceptance.

## 9. Resource and publication boundary

All operations are exact-real mathematics. A list length is not a charged
operation count or total runtime. It omits entry evaluation, matrix updates,
angle evaluation, storage, copying, and memory access. It gives neither a
finite-bit algorithm nor numerical error/stability guarantees. If N=2^n,
N M is not thereby polynomial in n. Row adjacency is adjacency of matrix
indices, not nearest-neighbor physical qubits. No gate set, clean ancillas,
postselection, success probability, bit order adapter, or relative-phase
quotient is certified. Thin factorization and isometry consumers remain
separate obligations.

Phase 1 is now ready for a content seal. Implementation and decoder
comparison, binder expansion against actual formal definitions, supplier
certificate binding, compilation, publication, and purification remain
pending. The source's own graph paragraph was audited against the independent
derivations above, not used as self-certification.
