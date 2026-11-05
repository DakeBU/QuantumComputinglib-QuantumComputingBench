# Statement Seal v1 (pre-proof)

Source id `lin-wiebe-2026-qasc`; 29 April 2026 edition, 447 PDF pages;
SHA256 `56825000d53025dea4c2998dd6a061592b8fb2b9a446c3194c5f408183327599`.
Primary URL https://math.berkeley.edu/~linlin/qasc/live_notes_0429.pdf.
Full printed pages 141-143 (PDF pages 141-143, zero-based indices 140-142)
were rendered and visually read before proof search. Primary full-text browsing
also checked the date, page count, and numbered equations.

## Bounded mathematical endpoint

For any positive real alpha, exact clean block `A = alpha B`, and finite
complex input b, the clean output of applying U to the clean input is
`c = alpha^-1 A b`. Consequently its Born weight is
`sum_i normSq(c_i) = (sum_i normSq((A b)_i)) / alpha^2`, and the weight
is positive exactly when `A b != 0`. If that image is nonzero, dividing
c by the square root of its weight gives the same coordinates as dividing
A b by the square root of its weight. This is the exact consumer part of
(9.2), (9.9), (9.10), and the superposition principle after (9.12),
not a full block-encoding construction or a Chapter 9 completeness claim.

Source-facing root specializes to qubit dimensions `2^m`, `2^n`, clean
signal index zero, a standard unitary U, and input Born weight one.
Providers may generalize the clean index and finite dimensions; this does not
alter the source root. Alpha is real positive, not a complex scaling phase.
No alpha-zero fallback or normalized state definition on a zero branch.

## Planned exact Lean interface

`exactConsumer` takes m,n:Nat; alpha:Real; A:FiniteMatrix (gridSize n)
(gridSize n) Complex; U:FiniteMatrix (gridSize m * gridSize n)
(gridSize m * gridSize n) Complex; b:StateVector (gridSize n) Complex;
`hAlpha : 0 < alpha`; `hUnitary : U in Matrix.unitaryGroup ... Complex`;
`hInput : sum_i Complex.normSq (b i) = 1`; and
`hBlock : forall i j, A i j = (alpha:Complex) *
signalSystemBlockProjection (gridSize m) (gridSize n) (gridSize n)
U (zeroBasisIndex m) i j`.

The conclusion is the conjunction of the four endpoint statements above,
with normalization conditional inside the conclusion on `applyVec A b != 0`.
Exact signature bytes will be bound after elaboration; no change to logical
inputs or conclusion without a versioned successor seal.

Post-elaboration signature binding (same v1 logical interface): SHA256
`5dc1f10a7727f21feec727bbb3b30f12ff30477e7de15aa59fced87387cf37a4`.
Hash domain is the UTF-8 substring from `theorem exactConsumer` through and
including ` := by` in ExactConsumer.lean. The source-facing signature did not
change during proof search. File/hash bindings and actual checks are in result.md.

## Binder and definition audit

- m,n,A,U,b: TYPING, the source's finite qubit matrices/vectors.
- hAlpha: SOURCE, positive subnormalization factor in Definition 9.2.
- hUnitary: SOURCE, U is unitary in (9.7)-(9.9).
- hInput: STANDING, b denotes a normalized quantum state.
- hBlock: SOURCE, literal exact equation (9.9), not a construction obligation.
- Nonzero image: no public premise; a derived success boundary and condition
  on the normalized conclusion, where the source's formula is meaningful.
- Basis-action linearity, normSq scaling, and square-root cancellation:
  implementation dependencies, not added premises.
- EXCESS: none intended.

Internal `cleanInput` is literally a finite superposition of the existing
`basisKet` at existing `productIndex`; `cleanOutput` is literally existing
`applyVec` followed by reading those clean coordinates. No second BlockEncoding,
state, channel, measurement, or normalized-state foundational API is created.
These are literal internal providers, not characterized/choice definitions.

Register order is ancilla high-order, system low-order: a*N+i. Input ancillas
are zero; only the zero output sector is accepted. No phase quotient, hidden
workspace cleanup, coherent controlled access, or inverse oracle is assumed.
No approximation, amplification, probability lower bound uniform in b,
gate/query/finite-bit complexity, physical measurement implementation, or
readout-cost theorem is claimed. The squared vector norm in (9.10) is written
as the exact sum of complex normSq, not Frobenius or matrix action norm.
