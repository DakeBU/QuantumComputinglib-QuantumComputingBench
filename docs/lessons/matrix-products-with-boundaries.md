# Matrix products with explicit boundary vectors

A finite product of small real matrices can be represented exactly by a
tensor train with scalar boundaries. The boundary vectors belong inside the
first and last cores. This construction preserves every signed coefficient;
it does not prepare a normalized quantum state by itself.

## Matrices and coefficient order

Let `D` and `s` be natural numbers, and let `N=n+1` be a positive number of
emitted bits. For each position `t` and bit `b` in `{0,1}`, let
`K(t,b)` be a real `D` by `D` matrix. Let `l,r` be real vectors of length `D`.
For the word `x=(x_0,...,x_(N-1))`, the desired scalar is

\[
 a(x)=l^T K(s,x_0)K(s+1,x_1)\cdots K(s+N-1,x_{N-1})r.
\]

The first emitted bit is the first factor, not the last factor. More precisely,
define the right-boundary readout by

\[
 R(s,\varnothing)=r,\qquad
 R(s,(b,y))=K(s,b)R(s+1,y).
\]

Then `a(x)=sum_j l_j R(s,x)_j`. All entries are arbitrary signed reals. No
normalization, invertibility, full rank, positivity or nonzero-vector premise
is required. `D=0` is permitted: the scalar sum is empty and equals zero.

## Absorbing the boundaries

A core with left dimension `u` and right dimension `v` has entries
`A(i,(b,j))` and slices `A_b` of shape `u` by `v`. A chain contracts its
slices from the first bit to the last; the empty terminal chain contracts to
the identity matrix on its terminal bond.

For the final position, replace `K(t,b)` by the `D` by `1` slice
`K(t,b)r`. For each earlier position, keep the `D` by `D` slice `K(t,b)`.
Call this positive-length chain `T`. An induction on its length gives

\[
 \operatorname{contract}(T,x)_{j,0}=R(s,x)_j.
\]

The one-bit case is the matrix-vector product at the terminal core. In the
inductive step, summing over the next bond is exactly the next readout
recursion; the same word and position order are preserved.

Next, replace only the first core by

\[
 B(0,(b,j))=\sum_i l_i A(i,(b,j)).
\]

Finite-sum distributivity and exchange of the two bond sums prove
`contract(closeLeft(l,T),x)_(0,0)=sum_i l_i contract(T,x)_(i,0)`.
Thus the constructed scalar-boundary chain `C` satisfies

\[
 \operatorname{contract}(C,x)_{0,0}=a(x)
\]

for every word. When `N=1`, both boundaries are absorbed into the same core,
so its slice is the scalar `l^T K(s,b)r`; it is not a two-core construction.
When `D=0`, this single scalar core still has its two stored scalar addresses,
whose values are zero.

## Bond dimensions and local scalar addresses

Let `maxBond` include both boundaries of a dependent chain, and let
`storedScalars` count `2*u*v` scalar addresses in each core. The terminal
empty chain contributes no core addresses. The constructed chain obeys

\[
 \operatorname{maxBond}(C)\le\max(D,1),\qquad
 \operatorname{storedScalars}(C)\le2N\max(D,1)^2.
\]

More generally, for any `N`-core chain with all actual bonds bounded by `B`,
`storedScalars <= 2*N*B^2`. Inductively the first core contributes at most
`2*B^2`, since its two adjacent bond dimensions are at most `B`; apply the
same bound to the tail. This is an address-count theorem, not an arithmetic
runtime or allocation theorem. Evaluating matrix entries, computing boundary
products, copying/materializing arrays and their bit sizes remain outside it.

## Exact Lean correspondence

The whole module is `QuantumBlockEncoding.MatrixProductChain`.

| Mathematical object or step | Public Lean declarations |
| --- | --- |
| Matrix family and ordered readout | `Kernel`, `readout` |
| Absorb right boundary and prove readout | `tailChain`, `tailChain_contract` |
| Absorb left boundary and prove coefficient sum | `closeLeft`, `closeLeft_contract` |
| Scalar-boundary construction and exact coefficients | `ofKernel`, `ofKernel_contract` |
| Actual bond bounds | `tailChain_maxBond`, `ofKernel_maxBond` |
| Core address count and general/construction bounds | `storedScalars`, `storedScalars_le`, `ofKernel_storedScalars` |

The `maxBond<=B` premise belongs only to the general size theorem. The
construction supplies its own bond bound before using that theorem; no
caller-supplied amplitude equality or desired output property is assumed.
The mathematical operations are noncomputable real definitions, not an
executable stored array producer. The imported canonicalization/circuit
theorems are separate downstream results, not conclusions of this module.

## Reuse and the four graph views

The source construction graph is right-boundary absorption, then left-boundary
absorption, followed by coefficient preservation and the independent address
bound. The Lean graph records actual module ownership and imports; an import
does not establish a dependency on every theorem in that module. The compressed
spine is a single boundary-absorption move with these formulas as its lossless
expansion. A transport from matrix-product descriptions to physical state
preparation must additionally supply normalization, canonicalization, register
embedding, cleanup, circuit synthesis and resource costs. That conceptual
transport is not a certified functor or a consequence of address counting.

This is a retrospective local mathematical contract for an existing module,
not a historical pre-proof seal, external-paper assimilation or novelty claim.
It contains no physical bit/endian adapter, clean-ancilla claim, phase quotient,
error/success theorem, oracle implementation or finite-bit complexity theorem.
