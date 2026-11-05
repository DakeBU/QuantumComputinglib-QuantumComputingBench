# Ordered reuse audit (before implementation)

1. Local ASPBE: searched `QuantumBlockEncoding` for density, pure state,
   outer product, positivity and state/matrix carriers. Reuse
   `QuantumBlockEncoding.ConcreteSemantics.StateVector` and `FiniteMatrix`,
   already definitionally compatible with Mathlib finite matrices. There is
   no local density/partial-trace/channel structure that this slice needs.
   The existing `ComplexUnitaryGate` is the future gate boundary, not replaced
   or duplicated here. Local state-preparation normalization fields are
   generic propositions, not silently used as mathematical unit-vector facts.
2. Mathlib at the repository's manifest-pinned Lean4.33 dependency: found
   `Matrix.posSemidef_vecMulVec_self_star`, `Matrix.trace_vecMulVec`,
   `dotProduct_comm`, and `Matrix.vecMulVec_mul_vecMulVec`. These directly
   discharge the required algebra; a density wrapper or copied quantum
   foundation would add no semantic value. Reuse the existing predicates and
   operators directly, expose only the source-facing theorem pair.
3. Attributed external audit: read the repository cards for Lean-QuantumInfo
   (MIT), lean-quantum (Apache-2.0), quantum-computing-lean (license boundary
   recorded in the existing card), then inspected primary upstream index and
   state surfaces. No external library is imported or copied.

   - [Lean-QuantumInfo index](https://github.com/Timeroot/Lean-QuantumInfo/blob/master/QuantumInfo.lean):
     finite `Braket`, `MState`, `Unitary`, channels/entropy APIs. Higher-level
     finite state wrappers are adapter candidates for a later reviewed node.
   - [lean-quantum index](https://github.com/Hayata-Yamasaki-Group/lean-quantum/blob/main/Quantum.lean):
     operator-oriented quantum state/channel and trace-inequality modules.
     No reason to import the larger foundation for this coordinate identity.
   - [quantum-computing-lean State](https://github.com/duckki/quantum-computing-lean/blob/main/QuantumComputing/State.lean):
     analogous pure/density evolution interface with its own vector wrappers.
     Semantic design reference only; local direct Mathlib proof avoids copying
     under the card's unresolved top-level-license boundary.
   - [Lean-QIT-Bench](https://github.com/QuAIR/Lean-QIT-Bench): benchmark modules
     and goals are target references, not evidence of admitted proofs.
   - Lean-QuantumAlg-Bench/QAlg benchmark attribution inspected through local
     roadmap and technical-lemma references; no algorithm/gate theorem needed
     by this projector interface, no benchmark proof imported.

These upstream checks were read-only retrieval on 2026-10-08, not pinned
dependency intake or a claim to have built their current heads. The checked
proof depends solely on local ASPBE and pinned Mathlib. OpenAI/math is neither
used nor imported. Tensor/register APIs need no new adapter because this slice
has one unsplit finite system. No public absolute working paths are recorded.

Route: direct Mathlib algebra through existing carriers. New reusable node is
the exact source-facing adapter pair, not a new PSD/trace/vector definition.
Prospective consumer is the peer QIT textbook's pure-state layer; production
promotion/canonicalization requires distinct review and actual consumers.
