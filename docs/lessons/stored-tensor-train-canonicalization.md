# Right-canonicalization of an already stored real tensor train

This procedure rewrites small local tables, not a table of all amplitudes.
It preserves every emitted word and terminal bond label. For a stored real
train of length \(n\), with all bond dimensions at most \(D\), the specified
producer has extended exact-real word cost at most
\[
 n(176D^3+116D^2+29D+8)+5D^2+4D+6.
\]
This counts the stated stored operations, not finite-bit execution time,
input-core generation, quantum gates or numerical stability.

This is a retrospective local contract for
`QuantumBlockEncoding/StoredTensorTrain.lean`. It is not an external-paper
assimilation, a historical pre-proof seal or a novelty claim. Independent
source-blind reconstruction and source-first comparison remain required.

## Objects and complete word action

Let the bond dimensions be \(d_0,\ldots,d_n\), all natural numbers, including
zero. Core \(A_i\) is an already stored nested vector of shape
\(d_i\times(2d_{i+1})\). Its physical-bit/right-bond column address is
\(b d_{i+1}+j\), with \(b\in\{0,1\}\) and \(0\le j<d_{i+1}\).
Write \(A_i(b)\) for the corresponding \(d_i\times d_{i+1}\) slice.
An empty chain at bond \(r\) contracts to \(I_r\).
For a recursively ordered word \(x=(x_0,\ldots,x_{n-1})\), define
\[
 M_C(x)=A_0(x_0)\cdots A_{n-1}(x_{n-1}).
\]
The first core emits the first word bit. No physical integer-basis or
little-endian circuit identification is supplied by this word convention.

Right-canonical means, at every site, that the complete flattened core has
orthonormal rows: \(Q_iQ_i^{\mathsf T}=I\). This sums over both physical bit
values and every right-bond label, not a selected clean sector. The terminal
bond remains unchanged.

## Stored absorption and its cost

Given stored \(A\) of shape \(l\times(2m)\) and stored residual
\(S\) of shape \(m\times r\), construct a stored core \(B\) by
\[
 B(a,b,j)=\sum_{u=0}^{m-1} A(a,b,u)S(u,j).
\]
Each summand reads the two stored scalars through their row references,
multiplies them and contributes to the recursive sum. The sum has one charged
addition per summand, including addition to its zero base. Every output entry
is materialized through the stored two-pass collector before factorization.
Empty sums are zero; no full-rank or positivity premise appears.

The eight counters are field operations, square roots, angles, trigonometric
calls, exact comparisons, reads, writes and emitted records. For counter
\(o\), let \(t_p(o)\) be one when \(o=p\), and zero otherwise. The entry
cost is bounded by
\[
 m(4t_{\rm read}+2t_{\rm field}),
\]
and the entire absorption cost by
\[
 l(2r)m(4t_{\rm read}+2t_{\rm field})
 +(l(2r)+l)(2t_{\rm read}+2t_{\rm write}).
\]
The latter storage term counts entry and outer-row materialization. Summing
all eight counters gives
\[
 12lmr+8lr+4l.
\]
These formulas concern this actual stored producer, not an arbitrary
uncharged matrix-entry callback.

## Deterministic factorization supplier

Flatten \(B\) using the same physical-bit/right-bond equivalence and apply
the existing deterministic stored thin-LQ producer. If
\(s=\min(l,2r)\), its returned tables \(R,Q\) satisfy
\[
 B=RQ,\qquad QQ^{\mathsf T}=I_s.
\]
The row dimension is the dimension recurrence, not the numerical rank.
Zero pivots and rank-deficient inputs therefore do not imply a smaller
claimed rank. The exact returned \(R\) and \(Q\), not merely equivalent
witnesses, match the existing deterministic semantic factorization under
the same flattening. For \(l,r\le D\), its total stored-operation cost is
at most
\[
 164D^3+108D^2+25D+2.
\]
The thin-LQ supplier and its definition/order conventions are dependencies;
this lesson does not independently re-prove their internals or certify
finite-precision QR.

## Backward recursion and returned-value refinement

Canonicalization runs from the terminal bond toward the initial bond.
For an empty chain, return the materialized \(I_r\) as residual and retain
the empty chain. For a head \(A\) and tail \(C\), first compute the tail's
stored residual \(S\) and right-canonical chain \(E\). Materialize the
absorption \(B=A S\) without mixing the emitted bit. Factor that actual
stored \(B=RQ\), and return residual \(R\) with chain \(Q::E\).

Inductively the returned rank obeys
\[
 s_n=d_n,\qquad s_i=\min(d_i,2s_{i+1}).
\]
Its maximum bond never exceeds the input maximum bond. Associativity and
the slice-wise factorization give, for every full word,
\[
 M_C(x)=R M_E(x).
\]
There is no supplied source-action or factorization hypothesis at the public
producer: these fields are proved for the returned object. Forgetting storage
from the returned result yields exactly the existing deterministic
`ConstructiveTensorTrain.canonicalize` result, including its residual and
canonical cores. This is stronger than the existence of some suitable chain;
proof-field equality does not add a runtime claim.

## Whole-run cost

Each recursion node charges three reads and three writes. The empty identity
producer contributes \(5r^2+4r\); thus the empty-chain total is
\(5r^2+4r+6\). At each nonempty site the absorbed residual rank is bounded by
the old tail's initial bond, so the input maximum-bond bound controls both
absorption and factorization dimensions. Adding tail, absorption,
factorization and node costs gives
\[
 6+(12D^3+8D^2+4D)+(164D^3+108D^2+25D+2)
 =176D^3+116D^2+29D+8.
\]
Induction gives the total bound stated above, including \(n=0\) and \(D=0\).
It describes the same returned object as the action/refinement theorems.

## Boundary mass, without garbage projection

For a real row boundary \(v\in\mathbb R^{d_0}\), put \(w=vR\).
With \({\rm mass}(z)=\sum_j z_j^2\), define
\[
 {\rm chainMass}(C,v)=\sum_x\sum_{j=0}^{d_n-1}(vM_C(x))_j^2.
\]
The all-word factorization and the right-canonical row isometries imply
\[
 {\rm chainMass}(C,v)={\rm mass}(w).
\]
Only the conditional normalization consumer assumes input mass one; it then
concludes \({\rm mass}(w)=1\). That premise is not silently produced by
canonicalization. Terminal labels are all retained. This is not complex
conjugate-transpose semantics, a gate-level state-action theorem or cleanup.

## Public declaration map

| Mathematical step | Public Lean declarations |
| --- | --- |
| Stored carriers and semantic erasure | StoredCore, denoteCore, StoredChain, denoteChain |
| Counted sums | sumEntries, sumEntries_value, sumEntries_cost_le |
| Entry absorption | absorptionEntry, absorptionEntry_value, absorptionEntry_cost_le |
| Materialized absorption and bounds | absorption, absorption_value, absorptionBudget, absorption_cost_le, absorption_total_cost_le |
| Deterministic stored factorization | CoreResult, factorCore, factorCore_total_cost_le, factorCore_R, factorCore_Q |
| Same returned recursive result | Result, nodeBudget, canonicalize, canonicalize_maxBond_le, canonicalize_total_cost_le, Result.toSemantic, canonicalize_refines |
| Full boundary mass and conditional normalization | boundary, boundary_mass, boundary_normalized |

## Reuse and remaining boundary

The source construction graph keeps materialized absorption, deterministic
thin-LQ, backward recursion and returned-value transport distinct. Cost
accounting is a separate branch of that same construction. The Lean graph
records actual module imports and declarations, not inferred proof-term
dependencies. The compressed spine is stored right-canonicalization; a
conceptual transport to preparation still needs normalization, physical
embedding, isometry completion, finite-angle synthesis and full terminal
cleanup as a complete AND-tail.

Input storage is already given. Index/counter bookkeeping, integer/rational
bit lengths, GCD, numerical stability, machine allocation, peak memory and
finite-bit execution remain outside the exact-real model. No scientific
Hermite root, resource winner, independent executable family acceptance or
public purification is asserted by this retrospective contract.
