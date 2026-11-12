# Shared-node reuse and definition audit

Retrieval order completed before adding internal semantic providers:

1. ASPBE `ConcreteSemantics`, `BlockEncoding`, `BlockEncodingClassics`,
   `CircuitSemantics`, `StatePreparation`, `Robin.ComplexLCUProjection`.
   Reuse `StateVector`, `FiniteMatrix`, `basisKet`, `applyVec`, `productIndex`,
   `signalSystemBlockProjection`, and standard `Matrix.unitaryGroup`.
   Existing `pointwiseProjection_iff_cleanBasisAction` covers individual basis
   inputs but does not supply arbitrary-superposition branch weight or normalized
   accepted output. The new consumer fills that precise gap.
   Generic `VerifiedBlockEncoding` and candidate proposition fields are not
   silently treated as concrete unitarity/block semantics.
2. Mathlib finite matrix-vector linearity, complex normSq, finite nonnegative
   sums, real square-root scaling/cancellation. No new norm or tensor system.
3. Attributed cards for Timeroot/Lean-QuantumInfo (MIT),
   Hayata-Yamasaki-Group/lean-quantum (Apache-2.0), and
   duckki/quantum-computing-lean (license boundary; reference-only).
   Their development checkouts are not present in this environment; source
   code is not copied, imports are not claimed. The recorded APIs concern
   general states/channels/projectors and do not replace this narrow existing
   ASPBE flattening adapter. The benchmark suites are not proof dependencies.
   No floating OpenAI Math upstream is used.

The only new definitions are literal internal coordinate bookkeeping:
`cleanInput = sum_j b_j * basisKet(productIndex a j)` and
`cleanOutput_i = applyVec U cleanInput (productIndex a i)`.
No choice, quotient, canonical dilation, normalized-state fallback, or second
BlockEncoding predicate. Complex relative phases in b are retained exactly.
The source root uses a=zeroBasisIndex m; provider a is a deliberate finite
generalization, not a source all-zero identification.

Purification candidates: the generalized linearity/action providers serve the
success and normalization roots; weight helpers are private. The source root
packages newly proved obligations, not a relabelled existing declaration.
Source normalization and unitarity remain explicit for physical interpretation;
the algebraic conclusion is stronger and holds without them. No probability
upper bound is claimed merely because those binders occur.
