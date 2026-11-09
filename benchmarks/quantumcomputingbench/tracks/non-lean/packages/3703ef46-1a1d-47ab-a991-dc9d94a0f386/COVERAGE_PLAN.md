# Batch 2 coverage plan — frozen before packet authoring

Base: `bb260f4e27360a0d3791b40cb22638af4b086fc9` (current main retrieved 6 November 2026).
Frozen benchmark graph: `qcb-snapshot-ffa644f0da3031a1ce754b9a`, source commit
`86b9e677566498da04faebcf4e5ed57f177c6bb1`. The resolved registry has 198 retained
cores and 15 reserved/withheld cores. No reserved target is available for reuse as
a new ID. The earlier two ZIPs contain ONE twelve-packet cohort; its four existing
core expositions and eight unassigned candidates are already present in this base.
They remain unchanged and are not part of the new packet count.

## Selection matrix

| Slot | Subject and mathematical target | Assessment type / provisional band | Existing coverage and bounded overlap | Frozen substrate anchors / evidence class |
|---|---|---|---|---|
| G1 | State preparation: finite-grid Gram contraction, local arithmetic error, dynamic range and normalizer margin | Prescribed numerical construction, bit budget and small-mass counterexample / D4 | Prior C3 supplies exact Gram algebra; A2 supplies normalization background; LA209/210 assess exact-real cost. New target charges rounding and range. Recurrence unrolling overlaps E1. | `TensorTrainNormEnvironment.gram`, `.gram_scalar`; `StoredTensorTrainNorm.update`, `.gram`, `.norm`. Original NL numerical analysis over exact-source substrate. |
| G2 | Sequential approximate isometries: multiplicative mass invariant, target-error growth and fidelity failure | Induction, sharpness, counterexample and conditional composition / D4 | SP007/008 and prior B1/C2 cover exact contraction, unitary mass and canonicality. Prior B3 supplies unitary telescoping; nonisometric amplification is a different obligation. | `SequentialBondPreparation.step_apply`, `.run`, `.amplitudeMass_run`. Original NL extension, not a new checked theorem. |
| P1 | Coherent finite-bit phase supplier by modular phase kickback with complete cleanup/resource ledger | Construction and precise assumption diagnosis / D3 | Prior B2 explicitly lacks a phase supplier; Plan207/209 cover angle/amplitude records; Plan519 Boolean kickback is a specialization. No repair or replacement of reserved Plan208. | Frozen coherent permutation/controlled-operation and phase substrate, exact IDs to be bound in payload. Elementary NL construction; catalyst and arithmetic suppliers are charged hypotheses, not free gates. |
| P2 | Sharp conversion from basis-column error to operator error, with unitary coherent failure witness | Norm derivation and counterexample / D2 | Plan010 diagnoses entrywise error; prior B2 controls distinct retained label blocks. The new target assesses the sharp square-root dimension loss under column promises and unitary witnesses. | Frozen `ConcreteSemantics.applyVec` and unitary/permutation interfaces; original finite-dimensional norm argument. |
| E1 | A posteriori Gram residuals certify a positive norm margin before data, circuit and projection error composition | Multi-interface reasoning with all premises / D4 | Prior A2/A3/B3 supply generic normalization, projection and telescoping. New assessed bridge is residual-to-certified-mass-to-end-to-end preparation. Unrolling shares an assessed subproof with G1. | `TensorTrainNormEnvironment.gram`, `.gram_eq_sum`, `.gram_scalar`; `PrimitiveCircuitPerturbation.aligned_eval_distance_le`. Exact identities plus original NL residual/error analysis. |
| E2 | Two-sided LCU with complex coefficients and approximate prepared columns | Construction and operator-error composition / D3 | BE004/006/112 cover exact same-P architecture and cleanup boundaries; prior B2 supplies phase diagnostics. New target is asymmetric left/right coefficients with column-only approximation, not full-P operator approximation. | `ComplexLCUProjection` clean column/row/entry and approximate block interface. Original NL perturbative extension of exact source semantics. |

Bands annotate the construction/reasoning route; they are neither measured model
difficulty nor graph distances. D0 records contract-reading facets inside packets
and adds no question. The six targets are advisory candidate scope, not a ruling
that six globally distinct canonical cores exist. A target that duplicates a full
existing contract will be dropped or converted to an existing-core view.

## Evidence and split boundaries

The source graph supplies compatible definitions and reusable interfaces. Module
imports/ownership only establish source organization. Conditional Functor
Hypergraph transports are distinct from the authored mathematical reasoning maps.
Each map must retain every premise at an AND join; alternative constructions and
excluded-domain diagnostics must not become false conjunctive theorem steps.
Nothing here is extracted Lean proof-term dependency evidence.

Existing test/dev/train contracts and withheld identities are frozen. Proposed
new targets receive fresh UUIDs, `candidate_not_counted`, mandatory semantic dedup
review and unassigned splits. Shared normalization, Gram propagation, phase,
projection and telescoping results preclude automatic independent-scoring claims.
Public solutions are not a hidden holdout. New live-only nodes, if needed, go to a
separate snapshot-refresh request and unadmitted appendix, never into the frozen
snapshot or validator-visible source-node list.

## Review and completion frontier

Freeze question, assumptions and conventions before a fresh-context reviewer
derives a solution using the pinned sources. Seal that derivation before exposing
the authored answer/rubric. The second phase compares exact payload hashes and
records substantive findings, source access, prior exposure and uncertainty.
AI review, self-review, structural validation, human approval and admission remain
separate. Retain all adverse findings and earlier frozen versions if revisions
are necessary. No Lean, model-response collection, inference or training is part
of this batch.
