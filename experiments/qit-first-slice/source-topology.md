# Source-first topology and coverage

Reconstructed from the pinned PDF before implementation Lean was written.
Extractor is the formalizing worker; distinct review pending (not self-approved).

## Source Proof / Construction Graph

`S2.4 standard inner product` AND `S4 normalized vector` AND
`S4 outer-product formula` -> `S4 forward pure projector satisfies S2.1`.
The source asserts this without a detailed proof; quadratic positivity and
trace calculation are SOURCE_GAP explanatory bridges, discharged locally only
after Lean verification, not falsely represented as printed proof steps.

Exhaustive disposition of relevant complete pages:

| Region | Disposition |
| --- | --- |
| p.3 heading/physical examples | EXCLUDED: motivation, no mathematical acceptance target |
| Eqs. 2.1-2.3 | EXCLUDED: qubit examples and Born-rule probabilities outside interface |
| Definition 2.1 positivity and trace | NODE S2.1 |
| finite-dimensional restriction and Eq. 2.4 | NODE S2.4 |
| Definition 2.2/Eq. 2.5 | EXCLUDED: observable interface outside target |
| p.4 observable continuation/Eq. 2.6 | EXCLUDED: measurement expectation outside target |
| convexity/compactness paragraph | EXCLUDED: mixed-state convex geometry outside target |
| pure-state paragraph: extremality and rank 1 | EXCLUDED: converse/characterization needs separate spectral/rank proof |
| pure-state paragraph: outer product, unit norm, projector | NODE S4, selected forward contract |
| mixed-state terminology | EXCLUDED: vocabulary, no new formal predicate |
| Definition 2.3/Eq. 2.7 | EXCLUDED: ensembles outside target |
| ensemble infinity/Exercise 2.1 reference | EXCLUDED: decomposition nonuniqueness outside target |
| Eq. 2.8 and spectral/probability paragraph | EXCLUDED: spectral decomposition outside target |
| Section 2.2 physical introduction and Brun17 citation | EXCLUDED: measurement dynamics outside target |
| Definition 2.4/Eq. 2.9 and properties i-iii | EXCLUDED: projective measurement families outside target |

No OR-routes in the selected source assertion. Rank/extremal converse is not
silently collapsed into the forward theorem.

## Lean Dependency Graph (to be bound to compilation)

Shared `ConcreteSemantics.StateVector`/`FiniteMatrix` provide carriers;
Mathlib `posSemidef_vecMulVec_self_star` supplies positivity;
`trace_vecMulVec` and `dotProduct_comm` supply trace normalization;
`vecMulVec_mul_vecMulVec` and supplied source unit norm supply idempotence.
These are named implementation references, not a claimed elaborated proof-term
export. Actual module imports are separately recorded in FirstSlice.lean.

## Compressed Quantum Spine

Shared finite state vector -> literal rank-one outer product -> positive
trace-one projector. One matrix representation, no new density wrapper.
Lossless expansion: S2.1/S2.4/S4 and the two sealed Lean roots.

## Functor Hypergraph

Proposed conceptual bridge (not a certified categorical functor):
AND-tail {finite vector, source unit norm, standard complex inner product}
-> head {positive trace-one projector} via `ψψ†`.
Hypothesis map: coordinates retain conjugate-linear first argument.
Conclusion map: PSD and unit trace plus projector identity, no quotient/rank
characterization. Failure boundary: unnormalized vectors still give PSD but
not generally unit trace or idempotence. Source S2.1/S2.4/S4; candidate substrate
the two sealed roots; conceptual independent review pending. No SP/BE resource
transport, unitary/categorical composition, partial trace, channel or tensor
claim is implied.
