# C21 internal complex-stage semantic audit

Independent reviewer: /root/complex_transport_review_c21. Author role: /root/literal_complex_review_c18 acting as C20 author, not reviewer. This is a distinct internal provider review, not a public source-blind decoder or Source Anchor admission.

## Frozen scope and reconstruction

The pre-proof reconstruction is reconstruction-before-proof-v1.md. The C20 result digest is 964aa2cce737273aa6e4b2d2f15f9721bcef066aecafe35b564bada7c6d8f9fe; handoff digest is faa255364e402730ec86978cabb7ba346fdbf45c0fd9e9c38d5f0237a24369d0. Both matched on initial inspection. The complete ComplexStageTransport.lean and ConsumerChecksC20.lean were read, alongside SavedStageInterpreter, StageOperatorBound, SavedRounding, NonunitaryTransport, NominalStageTransport, ChronologicalTransport, BasisCompatibility and LiteralComplexAdapter.

## Mathematical comparison

The definition actualStage has literal nominal evalPrimitiveCircuit(compileWord word), literal surrogate namedCast(stageCenter word degree bits), and literal real cast of stageEta. It is not correctness by definition: stage_entry_error independently uses namedCast_nominal and the actual saved interval supplier stage_max_entry_error. The midpoint is computed at stage end, not at each primitive step. Each complex difference entry is the real inclusion of the actual midpoint-minus-nominal real entry; its imaginary part is zero. ReviewChecksC21 independently checks this identity symbolically.

The generic complex_entry_bound_euclidean_opnorm theorem is sound. Triangle inequality gives the row sum of products of complex norms. Finite Cauchy-Schwarz bounds its square by the product of two sums of squares. EuclideanSpace.norm_sq_eq identifies the second sum with the full complex input norm, not merely the norm of its real part. Summing every row gives card(ι)^2*r^2*||x||^2. Both sides are nonnegative, allowing square-root removal. For PrimitiveBasis width, the existing q0LSB equivalence proves card=2^width. stage_operator_error therefore uses exactly N*actualMaxRadius=actualStageEta. No hidden missing square root or dimension factor is present.

nominal_contraction uses the existing evaluator's unitary certificate and the L2-operator-to-Euclidean-CLM identity. Surrogates are NOT assumed unitary. actual_stage_valid obtains eta nonnegativity from the actual interval enclosure, contraction from the literal primitive evaluator, and error from the new complex operator bound. actual_stages_valid discharges Valid internally for every mapped word. The generic NonunitaryTransport.product_error_le still requires Valid, appropriately; the actual roots supply it rather than exposing it as a caller premise.

The flatten proof inducts over chronological stage words. Its cons step is restProduct*headProduct and uses literal compileWord map-append and evalPrimitiveCircuit_append. This is later-left chronology. Matrix.toEuclideanCLM preserves multiplication, subtraction and identity. The final growth bound is product(1+eta)-1; replacing it by sum(eta) would be invalid for nonunitary midpoint products. The application bound multiplies by the arbitrary complex input norm.

## Binder classification and definition audit

At the six actual roots, width is TYPING; word/words, degree, bits and arbitrary complex x are original internal-contract data. The CX distinctness proof is part of the frozen literal Instruction constructor, not an additional theorem premise. There are NO supplied Valid, contraction, operator equality, midpoint bounds, normalization, success-sector, real-vector, clean-ancilla, source-correctness or resource assumptions. EXCESS=none. The generic library lemma's Fintype/DecidableEq and entry/nonnegative-radius inputs are an honest internal interface; these are discharged at the actual roots.

All stage, reindexing, cast, interval, word and product definitions are literal. No phase quotient, classical representative choice, invented zero/default extension or swapped target is introduced. Complete rows, columns, spectator patterns and terminal garbage sectors are retained. Width zero has a one-dimensional complex carrier and no inhabitable instruction. The imported adapter's local allowUnsafeReducibility only exposes gridSize's definition for elaboration; this is not a new axiom. Transitive axiom output is checked separately by fresh selected-source replay.

## Scope against the original scientific target

SP-HERMITE-POLY-002 fixes the normalized sampled piecewise Hermite/exponential target, little-endian order, exact-real gate contract and separately charged classical/finite-bit costs. The reviewed operator theorem does not substitute the midpoint output for that target and does not claim it approximates the target without the missing upstream/downstream bridges. The bound scales with full local dimension and actual interval widths; it does not by itself give polynomial preprocessing, a uniform family epsilon budget or physical-local/global assembly. Full QR, saved runtime refinement, coherent family construction, angle/source production, normalization stability, total finite-bit resources, repository build/Tests/site gates, canonical admission and purification remain open or inherited from separate evidence. No ROOT, main admission, certified population winner or PURIFIED claim follows from this review.

## Independent diagnostics

independent_discriminators.py imports no author executable. It uses tensor-product primitive RY matrices and explicit bit-column CX action, compared against independent rational interval row updates. The 35 finite cases cover non-real inputs, negative signed theta/2, all RY target wires/spectators and all ordered distinct CX pairs at widths 2 through 4, CX involutions versus reversed control/target, a noncommuting later-left stage sequence with reversed-order rejection, and width-zero complex identity. finite-review-v1.json is finite supporting evidence only, not a symbolic or runtime refinement certificate.

## Trust and acceptance boundary

The reviewer replay compiles selected source modules and both author modules into only the new C21 cache, plus reviewer-owned full-signature and imaginary-zero checks. It inventories combined public/meta imports and multiple import names, pins the frozen author/history artifacts, toolchain, manifest, available transitive sources and inherited caches before/after, and records inherited caches as unknown source-correspondence provenance. This is selected-source partial closure, NOT a fully fresh repository source build. Original author failed searches and publication-scanner failure remain unchanged. The final review receipt controls whether the scoped replay passes; this audit text alone does not assert compilation success.
