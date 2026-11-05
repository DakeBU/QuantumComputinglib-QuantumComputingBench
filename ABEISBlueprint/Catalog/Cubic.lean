import QuantumBlockEncoding
import Verso
import VersoManual
import VersoBlueprint

open Verso.Genre
open Verso.Genre.Manual
open Informal

set_option linter.hashCommand false
set_option linter.style.longLine false
set_option verso.blueprint.externalCode.strictResolve true

#doc (Manual) "Declaration catalog: Cubic" =>
%%%
file := "catalog-cubic"
%%%

This chapter is generated from the Lean source. Every node denotes one explicit public
declaration, and every Lean link is checked during the Blueprint build. Definitions appear
in source order before later results whenever the source module does so.

Reader orientation: State-preparation and exact rational Householder developments for the cubic benchmark family. Each card separates an accessible
reading cue from formal status, the source docstring, and the authoritative Lean panel.
The standalone Library Explorer adds full-text search and filters across every chapter.

# QuantumBlockEncoding/CubicAmplitudePrimitive.lean

25 explicit public declarations, in source order.

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ControlWires" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ControlWires")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic n 2 control wires”. The first two wires are system controls and wire two is the clean signal.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The first two wires are system controls and wire two is the clean signal.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:22](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2controlwires). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ControlWires_ne_signal" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ControlWires_ne_signal")
*Plain-English reading.* Lean checks the proposition indexed as “cubic n 2 control wires ne signal”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:26](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2controlwires-ne-signal). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ControlIndex" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ControlIndex")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic n 2 control index”. Decode the two little-endian system controls.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Decode the two little-endian system controls.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:31](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2controlindex). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2Amplitude_abs_le_one" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2Amplitude_abs_le_one")
*Plain-English reading.* Lean checks the proposition indexed as “cubic n 2 amplitude abs le one”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:34](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2amplitude-abs-le-one). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2Angle" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2Angle")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic n 2 angle”. Exact standard-RY angle for the selected cubic amplitude.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Exact standard-RY angle for the selected cubic amplitude.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:44](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2angle). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveCircuit" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveCircuit")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic n 2 primitive circuit”. Four-way uniformly controlled rotation, compiled to primitive gates.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Four-way uniformly controlled rotation, compiled to primitive gates.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:50](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitivecircuit). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveProgram" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveProgram")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic n 2 primitive program”.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:54](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitiveprogram). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveCircuit_eval" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveCircuit_eval")
*Plain-English reading.* Lean checks the proposition indexed as “cubic n 2 primitive circuit eval”; the hypotheses and conclusion in the code panel fix its exact scope. Exact matrix semantics of the emitted gate list.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Exact matrix semantics of the emitted gate list.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:59](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitivecircuit-eval). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveProgram_eval" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveProgram_eval")
*Plain-English reading.* Lean checks the proposition indexed as “cubic n 2 primitive program eval”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:66](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitiveprogram-eval). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2EncodeBits" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2EncodeBits")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic n 2 encode bits”. Encode a signal value and a two-qubit system index into three named wires.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Encode a signal value and a two-qubit system index into three named wires.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:77](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2encodebits). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2EncodeBits_signal" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2EncodeBits_signal")
*Plain-English reading.* Lean checks the proposition indexed as “cubic n 2 encode bits signal”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:82](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2encodebits-signal). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ControlIndex_encode" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ControlIndex_encode")
*Plain-English reading.* Lean checks the proposition indexed as “cubic n 2 control index encode”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:86](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2controlindex-encode). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2EncodeBits_context_eq_iff" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2EncodeBits_context_eq_iff")
*Plain-English reading.* Lean checks the proposition indexed as “cubic n 2 encode bits context eq iff”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:95](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2encodebits-context-eq-iff). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveProgram_cleanEntry" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveProgram_cleanEntry")
*Plain-English reading.* Lean checks the proposition indexed as “cubic n 2 primitive program clean entry”; the hypotheses and conclusion in the code panel fix its exact scope. The primitive program's clean signal block is exactly the cubic diagonal.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The primitive program's clean signal block is exactly the cubic diagonal.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:103](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitiveprogram-cleanentry). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveFlatUnitary" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveFlatUnitary")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic n 2 primitive flat unitary”. Flat little-endian unitary used by the operator-certificate interface.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Flat little-endian unitary used by the operator-certificate interface.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:145](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitiveflatunitary). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveFlatUnitary_unitary" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveFlatUnitary_unitary")
*Plain-English reading.* Lean checks the proposition indexed as “cubic n 2 primitive flat unitary unitary”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:150](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitiveflatunitary-unitary). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveCleanIndex" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveCleanIndex")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic n 2 primitive clean index”.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:156](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitivecleanindex). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveFlatUnitary_cleanBlock" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveFlatUnitary_cleanBlock")
*Plain-English reading.* Lean checks the proposition indexed as “cubic n 2 primitive flat unitary clean block”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:159](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitiveflatunitary-cleanblock). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ComplexTarget" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ComplexTarget")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic n 2 complex target”.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:170](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2complextarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitivePresentation" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitivePresentation")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic n 2 primitive presentation”.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:177](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitivepresentation). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveResource" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveResource")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic n 2 primitive resource”.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:185](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitiveresource). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveOperatorCandidate" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveOperatorCandidate")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic n 2 primitive operator candidate”.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:188](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitiveoperatorcandidate). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveVerifiedBlockEncoding" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveVerifiedBlockEncoding")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic n 2 primitive verified block encoding”. Exact unitarity and clean-block promotion for the finite cubic route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Exact unitarity and clean-block promotion for the finite cubic route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:211](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitiveverifiedblockencoding). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2Primitive_oracleCalls_eq_zero" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2Primitive_oracleCalls_eq_zero")
*Plain-English reading.* Lean checks the proposition indexed as “cubic n 2 primitive oracle calls eq zero”; the hypotheses and conclusion in the code panel fix its exact scope. No opaque oracle survives in the accepted primitive resource row.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* No opaque oracle survives in the accepted primitive resource row.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:221](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitive-oraclecalls-eq-zero). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2Primitive_resource_faithful" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicN2Primitive_resource_faithful")
*Plain-English reading.* Lean checks the proposition indexed as “cubic n 2 primitive resource faithful”; the hypotheses and conclusion in the code panel fix its exact scope. Resource ownership is definitional rather than a handwritten tuple.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Resource ownership is definitional rather than a handwritten tuple.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicAmplitudePrimitive.lean:226](../../../../library/modules/cubicamplitudeprimitive/#decl-quantumblockencoding-cubicdiagonaloracle-cubicn2primitive-resource-faithful). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

# QuantumBlockEncoding/CubicStatePreparation.lean

269 explicit public declarations, in source order.

:::definition "QuantumBlockEncoding.CubicStatePreparation.taskId" (lean := "QuantumBlockEncoding.CubicStatePreparation.taskId")
*Plain-English reading.* This definition gives the library's named construction or computation for “task id”. Task identifier used by the retrieval and verifier ledgers.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Task identifier used by the retrieval and verifier ledgers.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:25](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-taskid). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.requestedEpsilon" (lean := "QuantumBlockEncoding.CubicStatePreparation.requestedEpsilon")
*Plain-English reading.* This definition gives the library's named construction or computation for “requested epsilon”. User-requested error tolerance '1e-10'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* User-requested error tolerance '1e-10'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:28](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-requestedepsilon). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.gridPoint" (lean := "QuantumBlockEncoding.CubicStatePreparation.gridPoint")
*Plain-English reading.* This definition gives the library's named construction or computation for “grid point”. Grid point 'x\_j = j / 2^n'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Grid point 'x\_j = j / 2^n'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:31](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-gridpoint). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic amplitude”. Cubic amplitude 'f(x\_j) = x\_j^3'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Cubic amplitude 'f(x\_j) = x\_j^3'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:35](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicamplitude). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.cubicOperator" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicOperator")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic operator”. The rank-one operator 'O\_n = |v\_n><0^n|'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The rank-one operator 'O\_n = |v\_n><0^n|'. In column-vector convention this maps the input basis state '|0^n>' to the unnormalized vector with entries '(j / 2^n)^3', and maps every other input basis state to zero.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:43](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicoperator). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic norm sq”. Exact rational squared norm of the unnormalized target vector.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Exact rational squared norm of the unnormalized target vector. The analytic normalizer is its square root; this rational quantity is the cheap diagnostic used before any approximate rotation-synthesis route is accepted.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:51](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicnormsq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.conservativeNormalizer" (lean := "QuantumBlockEncoding.CubicStatePreparation.conservativeNormalizer")
*Plain-English reading.* This definition gives the library's named construction or computation for “conservative normalizer”. A conservative rational normalizer.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* A conservative rational normalizer. It is not intended to be optimal; it is a stable placeholder until the approximate synthesis backend proves a sharper normalizer and error bound.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:60](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-conservativenormalizer). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.cubicTarget" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicTarget")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic target”. Operator-first target record used by the ABEIS harness.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Operator-first target record used by the ABEIS harness.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:64](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubictarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.defaultRequiredCost" (lean := "QuantumBlockEncoding.CubicStatePreparation.defaultRequiredCost")
*Plain-English reading.* This definition gives the library's named construction or computation for “default required cost”. Resource floor used for the first Scenario 2 run.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Resource floor used for the first Scenario 2 run.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:77](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-defaultrequiredcost). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.defaultPolicy" (lean := "QuantumBlockEncoding.CubicStatePreparation.defaultPolicy")
*Plain-English reading.* This definition gives the library's named construction or computation for “default policy”. Adaptive search policy for the cubic benchmark.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Adaptive search policy for the cubic benchmark. The zero gate/depth fields in 'defaultRequiredCost' deliberately mean "discover a concrete candidate and then rank it"; the active search is expected to relax from exact to approximate construction after a small exact-search stall window.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:89](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-defaultpolicy). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicDefaultPrecision" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicDefaultPrecision")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic cubic default precision”. First arithmetic-route precision seed for Scenario 2.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* First arithmetic-route precision seed for Scenario 2.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:100](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticcubicdefaultprecision). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicLayout" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicLayout")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic cubic layout”. Register layout for the first arithmetic-transduction candidate route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Register layout for the first arithmetic-transduction candidate route. The single signal qubit is the clean block selector. The pure workspace keeps an address copy, reversible square/cube work registers, and fixed-point precision workspace. This is a candidate interface only; it does not certify the arithmetic or rotation subroutines.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:110](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticcubiclayout). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicCircuit" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicCircuit")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic cubic circuit”. Oracle-level transcript for the scalable cubic route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Oracle-level transcript for the scalable cubic route. The clean branch is intended to compute 'j / 2^n', reversibly form the cubic fixed-point amplitude, apply one amplitude-transduction rotation, and uncompute the arithmetic workspace. Each label remains a semantic proof obligation.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:122](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticcubiccircuit). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicResource" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicResource")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic cubic resource”. Local resource count for the unexpanded oracle-level transcript.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Local resource count for the unexpanded oracle-level transcript.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:133](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticcubicresource). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicNormalizer" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicNormalizer")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic cubic normalizer”. Normalizer used by the first arithmetic-transduction route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Normalizer used by the first arithmetic-transduction route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:137](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticcubicnormalizer). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicCost" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicCost")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic cubic cost”. Candidate score extracted from the arithmetic-route layout and transcript.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Candidate score extracted from the arithmetic-route layout and transcript.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:141](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticcubiccost). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicResourceTuple" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicResourceTuple")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic cubic resource tuple”. Resource tuple in QBE candidate-population order.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Resource tuple in QBE candidate-population order.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:147](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticcubicresourcetuple). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicResource_eq" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicResource_eq")
*Plain-English reading.* Lean checks the proposition indexed as “arithmetic cubic resource eq”; the hypotheses and conclusion in the code panel fix its exact scope. The oracle-level transcript has seven unresolved calls and depth seven.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The oracle-level transcript has seven unresolved calls and depth seven.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:155](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticcubicresource-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicLayout_auxiliaryQubits" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicLayout_auxiliaryQubits")
*Plain-English reading.* Lean checks the proposition indexed as “arithmetic cubic layout auxiliary qubits”; the hypotheses and conclusion in the code panel fix its exact scope. The first arithmetic route records one signal qubit plus pure workspace.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The first arithmetic route records one signal qubit plus pure workspace.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:161](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticcubiclayout-auxiliaryqubits). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicClaim" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicClaim")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic cubic claim”. Human-facing construction claim for the first scalable route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Human-facing construction claim for the first scalable route. This claim is an unproved candidate record, not a certified block encoding.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:170](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticcubicclaim). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicLayout" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicLayout")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic rank one cubic layout”. Rank-one wrapper layout for the arithmetic cubic route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Rank-one wrapper layout for the arithmetic cubic route. The extra pure workspace is reserved for a zero-input filter and row-generation wrapper. This is still an oracle-level interface: it repairs the register shape of the candidate transcript, but it does not certify the wrapper semantics.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:192](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticrankonecubiclayout). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCircuit" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCircuit")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic rank one cubic circuit”. Rank-one candidate transcript around the arithmetic middle block.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Rank-one candidate transcript around the arithmetic middle block. The first two calls are the missing wrapper from 'CUBIC-CAND-SHAPE-001': reject nonzero input columns from the clean branch, then generate the output row register on the zero-input branch. The final call is a placeholder cleanup for the zero-input filter. The row-generation step is intentionally not uncomputed, because the output row is the system output of the rank-one operator.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:206](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticrankonecubiccircuit). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResource" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResource")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic rank one cubic resource”. Oracle-level resource count for the rank-one wrapped transcript.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Oracle-level resource count for the rank-one wrapped transcript.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:214](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticrankonecubicresource). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicNormalizer" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicNormalizer")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic rank one cubic normalizer”. Normalizer used by the rank-one wrapped arithmetic route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Normalizer used by the rank-one wrapped arithmetic route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:218](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticrankonecubicnormalizer). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCost" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCost")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic rank one cubic cost”. Candidate score for the rank-one wrapped arithmetic route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Candidate score for the rank-one wrapped arithmetic route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:222](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticrankonecubiccost). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResourceTuple" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResourceTuple")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic rank one cubic resource tuple”. Resource tuple in QBE candidate-population order for the wrapped route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Resource tuple in QBE candidate-population order for the wrapped route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:228](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticrankonecubicresourcetuple). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResource_eq" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResource_eq")
*Plain-English reading.* Lean checks the proposition indexed as “arithmetic rank one cubic resource eq”; the hypotheses and conclusion in the code panel fix its exact scope. The rank-one wrapper adds three oracle-level calls to the middle block.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The rank-one wrapper adds three oracle-level calls to the middle block.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:237](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticrankonecubicresource-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicLayout_auxiliaryQubits" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicLayout_auxiliaryQubits")
*Plain-English reading.* Lean checks the proposition indexed as “arithmetic rank one cubic layout auxiliary qubits”; the hypotheses and conclusion in the code panel fix its exact scope. Auxiliary qubits for the wrapped route include the zero-test workspace.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Auxiliary qubits for the wrapped route include the zero-test workspace.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:243](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticrankonecubiclayout-auxiliaryqubits). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResourceTuple_n2_default" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResourceTuple_n2_default")
*Plain-English reading.* Lean checks the proposition indexed as “arithmetic rank one cubic resource tuple n 2 default”; the hypotheses and conclusion in the code panel fix its exact scope. Default small diagnostic score for the wrapped route at 'n = 2', 'p = 40'.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Default small diagnostic score for the wrapped route at 'n = 2', 'p = 40'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:249](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticrankonecubicresourcetuple-n2-default). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicClaim" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicClaim")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic rank one cubic claim”. Human-facing construction claim for the rank-one wrapped scalable route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Human-facing construction claim for the rank-one wrapped scalable route. This still records obligations, not a verified block-encoding certificate.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:258](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticrankonecubicclaim). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicWorkspace" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicWorkspace")
*Plain-English reading.* This definition gives the library's named construction or computation for “hadamard counting cubic workspace”. Workspace seed for the Hadamard-counting mutation.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Workspace seed for the Hadamard-counting mutation. This is an oracle-level interface budget for the reversible cube/comparator workspace. It is not a gate-level implementation of multiplication.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:280](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubicworkspace). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicLayout" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicLayout")
*Plain-English reading.* This definition gives the library's named construction or computation for “hadamard counting cubic layout”. Register layout for the exact Hadamard-counting candidate.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Register layout for the exact Hadamard-counting candidate. The signal qubit is the reject flag. Pure ancillas are the nonzero-input flag, the 'R,T' path registers of total width '4\*n', and the reversible cube/comparator workspace. Nonzero input columns set the reject signal before the 'nz' cleanup, so the clean projection cannot leak identity entries.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:291](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubiclayout). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCircuit" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCircuit")
*Plain-English reading.* This definition gives the library's named construction or computation for “hadamard counting cubic circuit”. Oracle-level transcript for the Hadamard-counting route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Oracle-level transcript for the Hadamard-counting route. The row XOR is not uncomputed, because it writes the output system row for the rank-one operator. The separate nonzero-column reject signal is applied before the 'nz' cleanup, so nonzero input columns keep a clean-projection rejection witness. The Hadamard layers and reversible arithmetic are still semantic obligations at this interface tier.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:305](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubiccircuit). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCircuit_rejectSignalRepair" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCircuit_rejectSignalRepair")
*Plain-English reading.* Lean checks the proposition indexed as “hadamard counting cubic circuit reject signal repair”; the hypotheses and conclusion in the code panel fix its exact scope. The repaired transcript records a separate nonzero-column reject signal before the final 'nz' cleanup.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The repaired transcript records a separate nonzero-column reject signal before the final 'nz' cleanup. This is the compiled surface for 'CUBIC-HCOUNT-REJECT-REPAIR-001'; semantic clean-block correctness remains a future proof leaf.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:322](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubiccircuit-rejectsignalrepair). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResource" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResource")
*Plain-English reading.* This definition gives the library's named construction or computation for “hadamard counting cubic resource”. Oracle-level resource count for the Hadamard-counting route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Oracle-level resource count for the Hadamard-counting route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:336](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubicresource). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicNormalizer" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicNormalizer")
*Plain-English reading.* This definition gives the library's named construction or computation for “hadamard counting cubic normalizer”. Normalizer used by the Hadamard-counting route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Normalizer used by the Hadamard-counting route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:340](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubicnormalizer). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCost" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCost")
*Plain-English reading.* This definition gives the library's named construction or computation for “hadamard counting cubic cost”. Candidate score for the Hadamard-counting route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Candidate score for the Hadamard-counting route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:344](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubiccost). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResourceTuple" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResourceTuple")
*Plain-English reading.* This definition gives the library's named construction or computation for “hadamard counting cubic resource tuple”. Resource tuple in QBE candidate-population order.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Resource tuple in QBE candidate-population order.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:350](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubicresourcetuple). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResource_eq" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResource_eq")
*Plain-English reading.* Lean checks the proposition indexed as “hadamard counting cubic resource eq”; the hypotheses and conclusion in the code panel fix its exact scope. The Hadamard-counting interface has eight unresolved oracle-level calls.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The Hadamard-counting interface has eight unresolved oracle-level calls.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:358](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubicresource-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicLayout_auxiliaryQubits" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicLayout_auxiliaryQubits")
*Plain-English reading.* Lean checks the proposition indexed as “hadamard counting cubic layout auxiliary qubits”; the hypotheses and conclusion in the code panel fix its exact scope. Auxiliary qubits for the counting route include reject, 'nz', path, and workspace registers.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Auxiliary qubits for the counting route include reject, 'nz', path, and workspace registers.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:364](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubiclayout-auxiliaryqubits). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResourceTuple_n2" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResourceTuple_n2")
*Plain-English reading.* Lean checks the proposition indexed as “hadamard counting cubic resource tuple n 2”; the hypotheses and conclusion in the code panel fix its exact scope. Default small diagnostic score for the counting route at 'n = 2'.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Default small diagnostic score for the counting route at 'n = 2'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:370](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubicresourcetuple-n2). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicClaim" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicClaim")
*Plain-English reading.* This definition gives the library's named construction or computation for “hadamard counting cubic claim”. Human-facing construction claim for the Hadamard-counting exact route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Human-facing construction claim for the Hadamard-counting exact route. This is an unproved candidate record, not a certified block encoding.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:378](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubicclaim). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hardModeUpperAgentSchedule" (lean := "QuantumBlockEncoding.CubicStatePreparation.hardModeUpperAgentSchedule")
*Plain-English reading.* This definition gives the library's named construction or computation for “hard mode upper agent schedule”. Hard Mode panel escalation schedule.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Hard Mode panel escalation schedule. The four entries are the planned parallel-agent counts for levels 0 through 3. Upper agents should only move to the next level after the active proof leaf has stalled and the reviewer has confirmed that the blocker is not just stale memory.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:401](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hardmodeupperagentschedule). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hardModeMiddleAgentSchedule" (lean := "QuantumBlockEncoding.CubicStatePreparation.hardModeMiddleAgentSchedule")
*Plain-English reading.* This definition gives the library's named construction or computation for “hard mode middle agent schedule”.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:403](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hardmodemiddleagentschedule). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hardModeLowerAgentSchedule" (lean := "QuantumBlockEncoding.CubicStatePreparation.hardModeLowerAgentSchedule")
*Plain-English reading.* This definition gives the library's named construction or computation for “hard mode lower agent schedule”.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:405](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hardmodeloweragentschedule). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hardModeExactStallWindow" (lean := "QuantumBlockEncoding.CubicStatePreparation.hardModeExactStallWindow")
*Plain-English reading.* This definition gives the library's named construction or computation for “hard mode exact stall window”. Number of consecutive cycles without a closed leaf before the first escalation.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Number of consecutive cycles without a closed leaf before the first escalation.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:408](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hardmodeexactstallwindow). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hardModeConstructionStallWindow" (lean := "QuantumBlockEncoding.CubicStatePreparation.hardModeConstructionStallWindow")
*Plain-English reading.* This definition gives the library's named construction or computation for “hard mode construction stall window”. Number of consecutive cycles without an improving certified or finite candidate before the next Hard Mode level is considered.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Number of consecutive cycles without an improving certified or finite candidate before the next Hard Mode level is considered.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:414](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hardmodeconstructionstallwindow). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hardModeLevelCycleBudget" (lean := "QuantumBlockEncoding.CubicStatePreparation.hardModeLevelCycleBudget")
*Plain-English reading.* This definition gives the library's named construction or computation for “hard mode level cycle budget”. Per-level cycle budgets before the upper panel must explicitly review progress.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Per-level cycle budgets before the upper panel must explicitly review progress.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:417](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hardmodelevelcyclebudget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.relaxedEpsilonLadder" (lean := "QuantumBlockEncoding.CubicStatePreparation.relaxedEpsilonLadder")
*Plain-English reading.* This definition gives the library's named construction or computation for “relaxed epsilon ladder”. Scenario 2 epsilon ladder.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Scenario 2 epsilon ladder. The first entry is the user-requested tolerance. Later entries are relaxed exploratory waypoints used only if the exact or requested-epsilon search stalls; a relaxed waypoint is not a substitute for a certificate at 'requestedEpsilon'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:425](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-relaxedepsilonladder). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.relaxedEpsilonLadder_startsWithRequested" (lean := "QuantumBlockEncoding.CubicStatePreparation.relaxedEpsilonLadder_startsWithRequested")
*Plain-English reading.* Lean checks the proposition indexed as “relaxed epsilon ladder starts with requested”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:428](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-relaxedepsilonladder-startswithrequested). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.hardModeSchedules_have_four_levels" (lean := "QuantumBlockEncoding.CubicStatePreparation.hardModeSchedules_have_four_levels")
*Plain-English reading.* Lean checks the proposition indexed as “hard mode schedules have four levels”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:432](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hardmodeschedules-have-four-levels). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.hardModeLowerAgentSchedule_final" (lean := "QuantumBlockEncoding.CubicStatePreparation.hardModeLowerAgentSchedule_final")
*Plain-English reading.* Lean checks the proposition indexed as “hard mode lower agent schedule final”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:439](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hardmodeloweragentschedule-final). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.initialExpectedPhase" (lean := "QuantumBlockEncoding.CubicStatePreparation.initialExpectedPhase")
*Plain-English reading.* This definition gives the library's named construction or computation for “initial expected phase”. Current expected phase.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Current expected phase. This is a planning declaration, not a proof of impossibility: it records that exact finite gate synthesis should not consume the full budget before approximate arithmetic/state-preparation search starts.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:448](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-initialexpectedphase). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.gridSize_pos" (lean := "QuantumBlockEncoding.CubicStatePreparation.gridSize_pos")
*Plain-English reading.* Lean checks the proposition indexed as “grid size pos”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:451](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-gridsize-pos). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.cubicOperator_first_column" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicOperator_first_column")
*Plain-English reading.* Lean checks the proposition indexed as “cubic operator first column”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:454](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicoperator-first-column). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.cubicOperator_only_first_column" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicOperator_only_first_column")
*Plain-English reading.* Lean checks the proposition indexed as “cubic operator only first column”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:458](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicoperator-only-first-column). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.rankOneCleanBlockContract" (lean := "QuantumBlockEncoding.CubicStatePreparation.rankOneCleanBlockContract")
*Plain-English reading.* This definition gives the library's named construction or computation for “rank one clean block contract”. Entrywise clean-block contract for a rank-one cubic candidate.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Entrywise clean-block contract for a rank-one cubic candidate. The first field states the scaled clean first column. The second field states that all other input columns vanish in the clean block. This is a semantic obligation for a future unitary/circuit proof, not a proof that the current oracle labels already realize the contract.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:471](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-rankonecleanblockcontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCleanBlockContract" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCleanBlockContract")
*Plain-English reading.* This definition gives the library's named construction or computation for “arithmetic rank one cubic clean block contract”. Candidate-specific clean-block contract for the repaired rank-one route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Candidate-specific clean-block contract for the repaired rank-one route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:478](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticrankonecubiccleanblockcontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.rankOneCleanBlockContract_pointwise_eq" (lean := "QuantumBlockEncoding.CubicStatePreparation.rankOneCleanBlockContract_pointwise_eq")
*Plain-English reading.* Lean checks the proposition indexed as “rank one clean block contract pointwise eq”; the hypotheses and conclusion in the code panel fix its exact scope. The rank-one clean-block contract is exactly the target matrix, entry by entry, after multiplying by its normalizer.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The rank-one clean-block contract is exactly the target matrix, entry by entry, after multiplying by its normalizer.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:486](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-rankonecleanblockcontract-pointwise-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCleanBlockContract_pointwise_eq" (lean := "QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCleanBlockContract_pointwise_eq")
*Plain-English reading.* Lean checks the proposition indexed as “arithmetic rank one cubic clean block contract pointwise eq”; the hypotheses and conclusion in the code panel fix its exact scope. Candidate-specific bridge from the repaired wrapper's clean-block contract to the fixed cubic target.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Candidate-specific bridge from the repaired wrapper's clean-block contract to the fixed cubic target.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:506](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-arithmeticrankonecubiccleanblockcontract-pointwise-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCleanBlockContract" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCleanBlockContract")
*Plain-English reading.* This definition gives the library's named construction or computation for “hadamard counting cubic clean block contract”. Candidate-specific clean-block contract for the Hadamard-counting route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Candidate-specific clean-block contract for the Hadamard-counting route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:515](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubiccleanblockcontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCleanBlockContract_pointwise_eq" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCleanBlockContract_pointwise_eq")
*Plain-English reading.* Lean checks the proposition indexed as “hadamard counting cubic clean block contract pointwise eq”; the hypotheses and conclusion in the code panel fix its exact scope. Candidate-specific bridge from the Hadamard-counting clean-block contract to the fixed cubic target.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Candidate-specific bridge from the Hadamard-counting clean-block contract to the fixed cubic target.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:523](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubiccleanblockcontract-pointwise-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.rat_cube_sq_eq_sixth" (lean := "QuantumBlockEncoding.CubicStatePreparation.rat_cube_sq_eq_sixth")
*Plain-English reading.* Lean checks the proposition indexed as “rat cube sq eq sixth”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:531](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-rat-cube-sq-eq-sixth). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude_sq_eq_gridPoint_sixth" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude_sq_eq_gridPoint_sixth")
*Plain-English reading.* Lean checks the proposition indexed as “cubic amplitude sq eq grid point sixth”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:538](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicamplitude-sq-eq-gridpoint-sixth). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_sixthPowerFold" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_sixthPowerFold")
*Plain-English reading.* Lean checks the proposition indexed as “cubic norm sq sixth power fold”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:543](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicnormsq-sixthpowerfold). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.gridSize_rat_ne_zero" (lean := "QuantumBlockEncoding.CubicStatePreparation.gridSize_rat_ne_zero")
*Plain-English reading.* Lean checks the proposition indexed as “grid size rat ne zero”; the hypotheses and conclusion in the code panel fix its exact scope. The rational grid dimension is nonzero, for denominator side conditions.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The rational grid dimension is nonzero, for denominator side conditions.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:550](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-gridsize-rat-ne-zero). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.gridSize_rat_pos" (lean := "QuantumBlockEncoding.CubicStatePreparation.gridSize_rat_pos")
*Plain-English reading.* Lean checks the proposition indexed as “grid size rat pos”; the hypotheses and conclusion in the code panel fix its exact scope. The rational grid dimension is positive.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The rational grid dimension is positive.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:555](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-gridsize-rat-pos). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.rat_div_cube_div_eq" (lean := "QuantumBlockEncoding.CubicStatePreparation.rat_div_cube_div_eq")
*Plain-English reading.* Lean checks the proposition indexed as “rat div cube div eq”; the hypotheses and conclusion in the code panel fix its exact scope. Core rational normalization for the Hadamard-counting path ratio.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Core rational normalization for the Hadamard-counting path ratio.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:560](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-rat-div-cube-div-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude_div_conservativeNormalizer_eq" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude_div_conservativeNormalizer_eq")
*Plain-English reading.* Lean checks the proposition indexed as “cubic amplitude div conservative normalizer eq”; the hypotheses and conclusion in the code panel fix its exact scope. Arithmetic bridge for the Hadamard-counting path formula.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Arithmetic bridge for the Hadamard-counting path formula. After scaling by 'alpha = conservativeNormalizer n = gridSize n', the candidate clean-block entry 'j^3 / gridSize^4' recovers the cubic target amplitude.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:571](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicamplitude-div-conservativenormalizer-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.gridSize_three_mul_eq_cube" (lean := "QuantumBlockEncoding.CubicStatePreparation.gridSize_three_mul_eq_cube")
*Plain-English reading.* Lean checks the proposition indexed as “grid size three mul eq cube”; the hypotheses and conclusion in the code panel fix its exact scope. Path-register capacity identity for the Hadamard-counting route.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Path-register capacity identity for the Hadamard-counting route.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:579](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-gridsize-three-mul-eq-cube). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.gridSize_four_mul_eq_fourth" (lean := "QuantumBlockEncoding.CubicStatePreparation.gridSize_four_mul_eq_fourth")
*Plain-English reading.* Lean checks the proposition indexed as “grid size four mul eq fourth”; the hypotheses and conclusion in the code panel fix its exact scope. Four-register path-space identity for the Hadamard-counting denominator.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Four-register path-space identity for the Hadamard-counting denominator.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:585](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-gridsize-four-mul-eq-fourth). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_thresholdCountP_finRange" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_thresholdCountP_finRange")
*Plain-English reading.* Lean checks the proposition indexed as “hadamard counting cubic threshold count p fin range”; the hypotheses and conclusion in the code panel fix its exact scope. Reusable threshold count over 'List.finRange'.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Reusable threshold count over 'List.finRange'. If the threshold 'k' fits in an 'm'-element register, exactly 'k' entries of 'List.finRange m' have value strictly below 'k'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:596](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubic-thresholdcountp-finrange). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_thresholdFilterLength" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_thresholdFilterLength")
*Plain-English reading.* Lean checks the proposition indexed as “hadamard counting cubic threshold filter length”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:625](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubic-thresholdfilterlength). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_threshold_le_pathCapacity" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_threshold_le_pathCapacity")
*Plain-English reading.* Lean checks the proposition indexed as “hadamard counting cubic threshold le path capacity”; the hypotheses and conclusion in the code panel fix its exact scope. The cubic threshold for row 'j' fits in the '3\*n'-qubit path register.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The cubic threshold for row 'j' fits in the '3\*n'-qubit path register.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:632](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubic-threshold-le-pathcapacity). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_thresholdPathCount" (lean := "QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_thresholdPathCount")
*Plain-English reading.* Lean checks the proposition indexed as “hadamard counting cubic threshold path count”; the hypotheses and conclusion in the code panel fix its exact scope. Symbolic accepted-path count for the Hadamard-counting threshold register.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Symbolic accepted-path count for the Hadamard-counting threshold register. For fixed output row 'j', the '3\*n'-qubit threshold register contributes exactly 'j.val ^ 3' accepted values.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:645](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-hadamardcountingcubic-thresholdpathcount). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.gridPoint_nonneg" (lean := "QuantumBlockEncoding.CubicStatePreparation.gridPoint_nonneg")
*Plain-English reading.* Lean checks the proposition indexed as “grid point nonneg”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:653](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-gridpoint-nonneg). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.gridPoint_lt_one" (lean := "QuantumBlockEncoding.CubicStatePreparation.gridPoint_lt_one")
*Plain-English reading.* Lean checks the proposition indexed as “grid point lt one”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:662](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-gridpoint-lt-one). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.gridPoint_le_one" (lean := "QuantumBlockEncoding.CubicStatePreparation.gridPoint_le_one")
*Plain-English reading.* Lean checks the proposition indexed as “grid point le one”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:669](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-gridpoint-le-one). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.rat_pow_le_one_of_nonneg_le_one" (lean := "QuantumBlockEncoding.CubicStatePreparation.rat_pow_le_one_of_nonneg_le_one")
*Plain-English reading.* Lean checks the proposition indexed as “rat pow le one of nonneg le one”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:673](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-rat-pow-le-one-of-nonneg-le-one). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude_sq_le_one" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude_sq_le_one")
*Plain-English reading.* Lean checks the proposition indexed as “cubic amplitude sq le one”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:687](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicamplitude-sq-le-one). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.foldl_add_le_add_length" (lean := "QuantumBlockEncoding.CubicStatePreparation.foldl_add_le_add_length")
*Plain-English reading.* Lean checks the proposition indexed as “foldl add le add length”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:693](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-foldl-add-le-add-length). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_gridSize" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_gridSize")
*Plain-English reading.* Lean checks the proposition indexed as “cubic norm sq le grid size”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:719](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicnormsq-le-gridsize). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.gridSize_rat_le_sq" (lean := "QuantumBlockEncoding.CubicStatePreparation.gridSize_rat_le_sq")
*Plain-English reading.* Lean checks the proposition indexed as “grid size rat le sq”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:731](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-gridsize-rat-le-sq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_conservativeNormalizer_sq" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_conservativeNormalizer_sq")
*Plain-English reading.* Lean checks the proposition indexed as “cubic norm sq le conservative normalizer sq”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:743](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicnormsq-le-conservativenormalizer-sq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_arithmeticCubicNormalizer_sq" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_arithmeticCubicNormalizer_sq")
*Plain-English reading.* Lean checks the proposition indexed as “cubic norm sq le arithmetic cubic normalizer sq”; the hypotheses and conclusion in the code panel fix its exact scope. Candidate-specific normalizer bridge for the first arithmetic route.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Candidate-specific normalizer bridge for the first arithmetic route. This does not certify the candidate unitary; it only records that the route's current choice 'alpha = arithmeticCubicNormalizer n' inherits the compiled conservative norm bound.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:754](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicnormsq-le-arithmeticcubicnormalizer-sq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_hadamardCountingCubicNormalizer_sq" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_hadamardCountingCubicNormalizer_sq")
*Plain-English reading.* Lean checks the proposition indexed as “cubic norm sq le hadamard counting cubic normalizer sq”; the hypotheses and conclusion in the code panel fix its exact scope. Candidate-specific normalizer bridge for the Hadamard-counting route.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Candidate-specific normalizer bridge for the Hadamard-counting route. This does not certify the Hadamard-sandwich semantics; it only records that the route's normalizer inherits the compiled conservative norm bound.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:764](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicnormsq-le-hadamardcountingcubicnormalizer-sq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_n1" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_n1")
*Plain-English reading.* Lean checks the proposition indexed as “cubic norm sq n 1”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:769](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicnormsq-n1). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_n2" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_n2")
*Plain-English reading.* Lean checks the proposition indexed as “cubic norm sq n 2”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:773](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicnormsq-n2). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_n3" (lean := "QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_n3")
*Plain-English reading.* Lean checks the proposition indexed as “cubic norm sq n 3”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:777](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicstatepreparation-cubicnormsq-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.taskId" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.taskId")
*Plain-English reading.* This definition gives the library's named construction or computation for “task id”. Task identifier used by the retrieval and verifier ledgers.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Task identifier used by the retrieval and verifier ledgers.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:786](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-taskid). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalOperator" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalOperator")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic diagonal operator”. The diagonal cubic oracle target 'D\_n\[row,col\] = (row/2^n)^3' if 'row=col', else zero.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The diagonal cubic oracle target 'D\_n\[row,col\] = (row/2^n)^3' if 'row=col', else zero.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:789](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicdiagonaloperator). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.exactNormalizer" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.exactNormalizer")
*Plain-English reading.* This definition gives the library's named construction or computation for “exact normalizer”. Exact normalizer for the diagonal target at the primitive amplitude-oracle tier.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Exact normalizer for the diagonal target at the primitive amplitude-oracle tier.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:795](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-exactnormalizer). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalTarget" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalTarget")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic diagonal target”. Operator-first target record for the diagonal cubic oracle.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Operator-first target record for the diagonal cubic oracle.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:798](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicdiagonaltarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalOperator" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalOperator")
*Plain-English reading.* This definition gives the library's named construction or computation for “linear diagonal operator”. Hinted linear diagonal target 'O\_0\[row,col\] = row/2^n' if 'row=col', else zero.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Hinted linear diagonal target 'O\_0\[row,col\] = row/2^n' if 'row=col', else zero. This is the input operator for the task-local QSVT consumer route. It is only the target matrix; a block-encoding circuit for this matrix is a separate proof obligation.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:819](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonaloperator). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalTarget" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalTarget")
*Plain-English reading.* This definition gives the library's named construction or computation for “linear diagonal target”. Operator-first target record for the hinted linear diagonal input 'O\_0'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Operator-first target record for the hinted linear diagonal input 'O\_0'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:825](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonaltarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCleanBlockContract" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCleanBlockContract")
*Plain-English reading.* This definition gives the library's named construction or computation for “linear diagonal clean block contract”. Clean-block contract for the hinted linear diagonal input target.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Clean-block contract for the hinted linear diagonal input target.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:840](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalcleanblockcontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCleanBlockContract_pointwise_eq" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCleanBlockContract_pointwise_eq")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal clean block contract pointwise eq”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:846](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalcleanblockcontract-pointwise-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCleanBlock_eq_target" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCleanBlock_eq_target")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal clean block eq target”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:853](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalcleanblock-eq-target). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalExactCleanBlockFromPointwise" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalExactCleanBlockFromPointwise")
*Plain-English reading.* This definition gives the library's named construction or computation for “linear diagonal exact clean block from pointwise”. Package a supplied clean-block equality for the hinted linear diagonal target as an 'ExactCleanBlock' payload.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Package a supplied clean-block equality for the hinted linear diagonal target as an 'ExactCleanBlock' payload. This is semantic glue only. The caller still owns the unitary proof, cleanup proof, concrete circuit, and resource tuple for the matrix 'U'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:867](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalexactcleanblockfrompointwise). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalExactCleanBlockFromPointwise_clean_eq_target" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalExactCleanBlockFromPointwise_clean_eq_target")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal exact clean block from pointwise clean eq target”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:881](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalexactcleanblockfrompointwise-clean-eq-target). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalInputBEContract" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalInputBEContract")
*Plain-English reading.* This record groups the data and proof fields needed for “linear diagonal input be contract”. A proposition-valued field is a requirement until a constructor supplies it. Interface for a concrete block encoding of the hinted linear diagonal input.

*Formal status.* Data contract in the default import surface; proposition-valued fields are obligations, not automatically established facts.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Interface for a concrete block encoding of the hinted linear diagonal input. This names the fields a backend must supply before the exact clean-block payload can be used as a real input certificate. It is not itself a backend: the cleanup and resource propositions must describe the chosen circuit family.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:904](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalinputbecontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalInputBEContract.exactPayload" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalInputBEContract.exactPayload")
*Plain-English reading.* This definition gives the library's named construction or computation for “exact payload”. Extract the reusable exact clean-block payload from a concrete linear-diagonal input contract.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Extract the reusable exact clean-block payload from a concrete linear-diagonal input contract.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:926](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalinputbecontract-exactpayload). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalInputBEContract.clean_eq_target" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalInputBEContract.clean_eq_target")
*Plain-English reading.* Lean checks the proposition indexed as “clean eq target”; the hypotheses and conclusion in the code panel fix its exact scope. The extracted clean block equals the hinted linear diagonal target.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The extracted clean block equals the hinted linear diagonal target.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:932](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalinputbecontract-clean-eq-target). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.householderZero" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.householderZero")
*Plain-English reading.* This definition gives the library's named construction or computation for “householder zero”. Clean basis index for the 8-dimensional rational Householder signal block.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Clean basis index for the 8-dimensional rational Householder signal block.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:944](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-householderzero). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.dot8" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.dot8")
*Plain-English reading.* This definition gives the library's named construction or computation for “dot 8”. Explicit rational dot product for the 8-dimensional Householder support leaf.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Explicit rational dot product for the 8-dimensional Householder support leaf.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:947](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-dot8). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.householder8E0Minus" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.householder8E0Minus")
*Plain-English reading.* This definition gives the library's named construction or computation for “householder 8 e 0 minus”. Vector 'e\_0 - v' used in the rational Householder reflection.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Vector 'e\_0 - v' used in the rational Householder reflection.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:952](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-householder8e0minus). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.householder8" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.householder8")
*Plain-English reading.* This definition gives the library's named construction or computation for “householder 8”. Rational 8-by-8 Householder block used by the hinted 'O\_0' backend route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Rational 8-by-8 Householder block used by the hinted 'O\_0' backend route. The later backend still has to supply rational unit-vector completions for the grid values and prove orthogonality of this block family.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:961](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-householder8). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.householder8E0Minus_normSq" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.householder8E0Minus_normSq")
*Plain-English reading.* Lean checks the proposition indexed as “householder 8 e 0 minus norm sq”; the hypotheses and conclusion in the code panel fix its exact scope. Norm identity for 'e\_0 - v' under the rational unit-vector hypothesis.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Norm identity for 'e\_0 - v' under the rational unit-vector hypothesis.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:968](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-householder8e0minus-normsq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.householder8E0Minus_normSq_ne_zero" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.householder8E0Minus_normSq_ne_zero")
*Plain-English reading.* Lean checks the proposition indexed as “householder 8 e 0 minus norm sq ne zero”; the hypotheses and conclusion in the code panel fix its exact scope. The Householder denominator is nonzero when the clean coordinate is not one.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The Householder denominator is nonzero when the clean coordinate is not one.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:977](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-householder8e0minus-normsq-ne-zero). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.householder8_clean_entry" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.householder8_clean_entry")
*Plain-English reading.* Lean checks the proposition indexed as “householder 8 clean entry”; the hypotheses and conclusion in the code panel fix its exact scope. Active leaf 'HINT-HOUSEHOLDER8-CLEAN-ENTRY': the clean entry of the rational Householder block is the first coordinate of the supplied unit vector.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Active leaf 'HINT-HOUSEHOLDER8-CLEAN-ENTRY': the clean entry of the rational Householder block is the first coordinate of the supplied unit vector.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:989](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-householder8-clean-entry). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.householder8_isRationalOrthogonal" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.householder8_isRationalOrthogonal")
*Plain-English reading.* Lean checks the proposition indexed as “householder 8 is rational orthogonal”; the hypotheses and conclusion in the code panel fix its exact scope. Active leaf 'HINT-HOUSEHOLDER8-ORTHO': the rational 8-dimensional Householder block is orthogonal whenever the input vector has 'dot8 v v = 1' and does not equal the clean basis vector.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Active leaf 'HINT-HOUSEHOLDER8-ORTHO': the rational 8-dimensional Householder block is orthogonal whenever the input vector has 'dot8 v v = 1' and does not equal the clean basis vector.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:1132](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-householder8-isrationalorthogonal). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8SystemIndex" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8SystemIndex")
*Plain-English reading.* This definition gives the library's named construction or computation for “controlled householder 8 system index”. System component for the task-local 'ancilla × system' direct-sum matrix.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* System component for the task-local 'ancilla × system' direct-sum matrix.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:1146](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-controlledhouseholder8systemindex). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8AncillaIndex" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8AncillaIndex")
*Plain-English reading.* This definition gives the library's named construction or computation for “controlled householder 8 ancilla index”. Ancilla component for the task-local 'ancilla × system' direct-sum matrix.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Ancilla component for the task-local 'ancilla × system' direct-sum matrix.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:1151](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-controlledhouseholder8ancillaindex). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8Embed" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8Embed")
*Plain-English reading.* This definition gives the library's named construction or computation for “controlled householder 8 embed”. Clean embedding for the controlled Householder direct sum.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Clean embedding for the controlled Householder direct sum.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:1160](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-controlledhouseholder8embed). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum")
*Plain-English reading.* This definition gives the library's named construction or computation for “controlled householder 8 direct sum”. Task-local controlled direct sum of supplied Householder blocks over system branches.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Task-local controlled direct sum of supplied Householder blocks over system branches.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:1165](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-controlledhouseholder8directsum). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8_branchNontrivial_of_clean" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8_branchNontrivial_of_clean")
*Plain-English reading.* Lean checks the proposition indexed as “controlled householder 8 branch nontrivial of clean”; the hypotheses and conclusion in the code panel fix its exact scope. Grid branches for the linear diagonal input never have clean Householder coordinate equal to one.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Grid branches for the linear diagonal input never have clean Householder coordinate equal to one.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:1268](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-controlledhouseholder8-branchnontrivial-of-clean). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_clean_entry" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_clean_entry")
*Plain-English reading.* Lean checks the proposition indexed as “controlled householder 8 direct sum clean entry”; the hypotheses and conclusion in the code panel fix its exact scope. Active leaf 'HINT-CONTROLLED-DIRECT-SUM': the clean block of the controlled Householder direct sum is the hinted linear diagonal operator.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Active leaf 'HINT-CONTROLLED-DIRECT-SUM': the clean block of the controlled Householder direct sum is the hinted linear diagonal operator.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:1286](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-controlledhouseholder8directsum-clean-entry). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_columnInner_eq_identity_of_system_ne" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_columnInner_eq_identity_of_system_ne")
*Plain-English reading.* Lean checks the proposition indexed as “controlled householder 8 direct sum column inner eq identity of system ne”; the hypotheses and conclusion in the code panel fix its exact scope. Column-inner bridge for the controlled Householder direct sum in the cross-branch case.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Column-inner bridge for the controlled Householder direct sum in the cross-branch case. This is a support leaf for 'HINT-CONTROLLED-DIRECT-SUM-ORTHO': if two columns belong to different system branches, every path contribution through the block-diagonal direct sum vanishes, so the column inner product agrees with the off-diagonal identity entry.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:1360](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-controlledhouseholder8directsum-columninner-eq-identity-of-system-ne). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_columnInner_eq_branch" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_columnInner_eq_branch")
*Plain-English reading.* Lean checks the proposition indexed as “controlled householder 8 direct sum column inner eq branch”; the hypotheses and conclusion in the code panel fix its exact scope. Support leaf 'CDS-COL-FOLD': inside one decoded system branch, the column inner product of the controlled direct sum is the column inner product of that branch's Householder block.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Support leaf 'CDS-COL-FOLD': inside one decoded system branch, the column inner product of the controlled direct sum is the column inner product of that branch's Householder block.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:1799](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-controlledhouseholder8directsum-columninner-eq-branch). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_rowInner_eq_branch" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_rowInner_eq_branch")
*Plain-English reading.* Lean checks the proposition indexed as “controlled householder 8 direct sum row inner eq branch”; the hypotheses and conclusion in the code panel fix its exact scope. Support leaf 'CDS-ROW-FOLD': inside one decoded system branch, the row inner product of the controlled direct sum is the row inner product of that branch's Householder block.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Support leaf 'CDS-ROW-FOLD': inside one decoded system branch, the row inner product of the controlled direct sum is the row inner product of that branch's Householder block.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:1918](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-controlledhouseholder8directsum-rowinner-eq-branch). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_rowInner_eq_identity_of_system_ne" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_rowInner_eq_identity_of_system_ne")
*Plain-English reading.* Lean checks the proposition indexed as “controlled householder 8 direct sum row inner eq identity of system ne”; the hypotheses and conclusion in the code panel fix its exact scope. Row-inner bridge for the controlled Householder direct sum in the cross-branch case.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Row-inner bridge for the controlled Householder direct sum in the cross-branch case. This completes the branch split needed by 'controlledHouseholder8DirectSum\_isRationalOrthogonal': if two rows belong to different decoded system branches, no summation path can hit both blocks.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:1972](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-controlledhouseholder8directsum-rowinner-eq-identity-of-system-ne). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_isRationalOrthogonal" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_isRationalOrthogonal")
*Plain-English reading.* Lean checks the proposition indexed as “controlled householder 8 direct sum is rational orthogonal”; the hypotheses and conclusion in the code panel fix its exact scope. Active leaf 'HINT-CONTROLLED-DIRECT-SUM-ORTHO': branchwise rational orthogonality for the controlled direct sum of supplied 8-dimensional Householder blocks.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Active leaf 'HINT-CONTROLLED-DIRECT-SUM-ORTHO': branchwise rational orthogonality for the controlled direct sum of supplied 8-dimensional Householder blocks.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2012](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-controlledhouseholder8directsum-isrationalorthogonal). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalRationalCompletion" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalRationalCompletion")
*Plain-English reading.* This definition gives the library's named construction or computation for “linear diagonal rational completion”. Branch-vector completion contract for the rational Householder backend of the hinted linear diagonal input 'O\_0'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Branch-vector completion contract for the rational Householder backend of the hinted linear diagonal input 'O\_0'. This predicate records only the supplied vector family needed by the compiled Householder direct-sum support. Existence for every grid point remains blocked on the cited four-squares obligation.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2061](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalrationalcompletion). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalFourSquareBranchVector" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalFourSquareBranchVector")
*Plain-English reading.* This definition gives the library's named construction or computation for “linear diagonal four square branch vector”. Branch vector obtained from a four-square completion of the residual '(2^n)^2 - j^2'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Branch vector obtained from a four-square completion of the residual '(2^n)^2 - j^2'. The first coordinate is the grid value 'j / 2^n'; the next four coordinates carry the rationalized square witnesses.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2074](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalfoursquarebranchvector). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalFourSquareBranchVector_clean" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalFourSquareBranchVector_clean")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal four square branch vector clean”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2084](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalfoursquarebranchvector-clean). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalFourSquareBranchVector_unit" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalFourSquareBranchVector_unit")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal four square branch vector unit”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2091](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalfoursquarebranchvector-unit). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_of_fourSquareWitnesses" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_of_fourSquareWitnesses")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal rational completion of four square witnesses”; the hypotheses and conclusion in the code panel fix its exact scope. Adapter from explicit four-square witnesses to the rational-completion predicate.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Adapter from explicit four-square witnesses to the rational-completion predicate. This is the local consumer of the still-external 'Nat.sum\_four\_squares' dependency; it does not prove that the witnesses exist.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2114](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalrationalcompletion-of-foursquarewitnesses). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_exists" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_exists")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal rational completion exists”; the hypotheses and conclusion in the code panel fix its exact scope. Every dyadic grid value has an unconditional rational unit-vector completion.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Every dyadic grid value has an unconditional rational unit-vector completion. The only number-theoretic ingredient is Lagrange's four-square theorem applied to 'gridSize n ^ 2 - j.val ^ 2'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2134](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalrationalcompletion-exists). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_branchData" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_branchData")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal rational completion branch data”; the hypotheses and conclusion in the code panel fix its exact scope. Adapter leaf for 'HINT-O0-RATIONAL-COMPLETION': a rational-completion witness also supplies the nontrivial clean-coordinate side condition needed by the Householder block.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Adapter leaf for 'HINT-O0-RATIONAL-COMPLETION': a rational-completion witness also supplies the nontrivial clean-coordinate side condition needed by the Householder block.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2156](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalrationalcompletion-branchdata). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_backendSupport" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_backendSupport")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal rational completion backend support”; the hypotheses and conclusion in the code panel fix its exact scope. A rational-completion witness supplies the clean-block equality and rational orthogonality facts for the controlled Householder direct sum.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* A rational-completion witness supplies the clean-block equality and rational orthogonality facts for the controlled Householder direct sum. This still does not package a complete 'LinearDiagonalInputBEContract': cleanup integration, normalizer/resource fields, and a concrete existence theorem are separate proof obligations.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2176](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalrationalcompletion-backendsupport). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderCircuit" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderCircuit")
*Plain-English reading.* This definition gives the library's named construction or computation for “linear diagonal householder circuit”. Oracle-label circuit for the proved rational Householder realization of 'O\_0'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Oracle-label circuit for the proved rational Householder realization of 'O\_0'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2198](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalhouseholdercircuit). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderResource" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderResource")
*Plain-English reading.* This definition gives the library's named construction or computation for “linear diagonal householder resource”.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2201](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalhouseholderresource). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderResource_eq" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderResource_eq")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal householder resource eq”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2204](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalhouseholderresource-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderInputBEContract" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderInputBEContract")
*Plain-English reading.* This definition gives the library's named construction or computation for “linear diagonal householder input be contract”. Unconditional exact matrix-level block encoding of the hinted input 'O\_0'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Unconditional exact matrix-level block encoding of the hinted input 'O\_0'. Unlike the earlier interface-only payload, this certificate contains the concrete controlled Householder matrix, its rational orthogonality theorem, the clean-block theorem, the exact normalizer, and an auditable oracle-label resource equality.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2217](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalhouseholderinputbecontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderInputBEContract_clean_eq_target" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderInputBEContract_clean_eq_target")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal householder input be contract clean eq target”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2248](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalhouseholderinputbecontract-clean-eq-target). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderInputBEContract_complete" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderInputBEContract_complete")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal householder input be contract complete”; the hypotheses and conclusion in the code panel fix its exact scope. Root certificate for the hinted input operator 'O\_0'.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Root certificate for the hinted input operator 'O\_0'. This theorem exposes all matrix-level facts needed by a downstream polynomial consumer in one place, so the harness does not reopen the four-square, Householder, cleanup, normalizer, or resource leaves after they have compiled.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2261](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalhouseholderinputbecontract-complete). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator")
*Plain-English reading.* This definition gives the library's named construction or computation for “approx diagonal operator”. Supplied diagonal matrix for the first Scenario 2 approximate route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Supplied diagonal matrix for the first Scenario 2 approximate route. The function 'q' is only a proposed rational diagonal value. Approximation to the cubic target and the operator-norm bridge remain separate obligations.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2284](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-approxdiagonaloperator). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.ratAbs" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.ratAbs")
*Plain-English reading.* This definition gives the library's named construction or computation for “rat abs”. Task-local rational absolute value used before a project norm API exists.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Task-local rational absolute value used before a project norm API exists.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2289](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-ratabs). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.IsDiagonalRatMatrix" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.IsDiagonalRatMatrix")
*Plain-English reading.* This definition gives the library's named construction or computation for “is diagonal rat matrix”. Project-local rational matrices whose off-diagonal entries are zero.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Project-local rational matrices whose off-diagonal entries are zero.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2292](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-isdiagonalratmatrix). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.DiagonalRatOperatorNormBridge" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.DiagonalRatOperatorNormBridge")
*Plain-English reading.* This record groups the data and proof fields needed for “diagonal rat operator norm bridge”. A proposition-valued field is a requirement until a constructor supplies it. Typed contract for the missing rational-matrix operator-norm bridge.

*Formal status.* Data contract in the default import surface; proposition-valued fields are obligations, not automatically established facts.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Typed contract for the missing rational-matrix operator-norm bridge. This structure is deliberately conditional: it does not assert that the bridge is already available in this repository. A future Mathlib-backed proof or a human-accepted external contract must supply this record before an approximate block-encoding certificate may consume the norm bound.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2303](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-diagonalratoperatornormbridge). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.ratSquaredEuclideanNorm" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.ratSquaredEuclideanNorm")
*Plain-English reading.* This definition gives the library's named construction or computation for “rat squared euclidean norm”. Squared Euclidean norm on project-local finite rational vectors.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Squared Euclidean norm on project-local finite rational vectors.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2314](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-ratsquaredeuclideannorm). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.ratMatrixErrorAction" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.ratMatrixErrorAction")
*Plain-English reading.* This definition gives the library's named construction or computation for “rat matrix error action”. Action of the matrix error 'A - B' on a finite rational vector.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Action of the matrix error 'A - B' on a finite rational vector.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2318](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-ratmatrixerroraction). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.ratEuclideanOperatorNormErrorAtMost" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.ratEuclideanOperatorNormErrorAtMost")
*Plain-English reading.* This definition gives the library's named construction or computation for “rat euclidean operator norm error at most”. Non-vacuous squared Euclidean induced operator-norm error semantics.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Non-vacuous squared Euclidean induced operator-norm error semantics. For nonnegative 'epsilon', this states '||(A-B)v||₂² ≤ ||epsilon v||₂²' for every rational vector 'v'. Squared norms avoid introducing square roots while retaining the finite-dimensional Euclidean operator-norm statement.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2331](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-rateuclideanoperatornormerroratmost). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.ratMatrixErrorAction_eq_diagonal" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.ratMatrixErrorAction_eq_diagonal")
*Plain-English reading.* Lean checks the proposition indexed as “rat matrix error action eq diagonal”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2453](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-ratmatrixerroraction-eq-diagonal). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.ratAbs_nonneg" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.ratAbs_nonneg")
*Plain-English reading.* Lean checks the proposition indexed as “rat abs nonneg”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2468](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-ratabs-nonneg). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_eq_ratAbs_mul_self" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_eq_ratAbs_mul_self")
*Plain-English reading.* Lean checks the proposition indexed as “rat mul self eq rat abs mul self”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2472](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-rat-mul-self-eq-ratabs-mul-self). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_nonneg" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_nonneg")
*Plain-English reading.* Lean checks the proposition indexed as “rat mul self nonneg”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2477](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-rat-mul-self-nonneg). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_le_of_abs_le" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_le_of_abs_le")
*Plain-English reading.* Lean checks the proposition indexed as “rat mul self le of abs le”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2481](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-rat-mul-self-le-of-abs-le). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_vector_le_of_abs_le" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_vector_le_of_abs_le")
*Plain-English reading.* Lean checks the proposition indexed as “rat mul self vector le of abs le”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2499](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-rat-mul-self-vector-le-of-abs-le). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.ratEuclideanDiagonalOperatorNormBridge" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.ratEuclideanDiagonalOperatorNormBridge")
*Plain-English reading.* This definition gives the library's named construction or computation for “rat euclidean diagonal operator norm bridge”. Concrete proof that diagonal entrywise bounds imply the squared Euclidean bound.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Concrete proof that diagonal entrywise bounds imply the squared Euclidean bound.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2509](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-rateuclideandiagonaloperatornormbridge). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.ratEuclideanOperatorNormErrorAtMost_not_vacuous" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.ratEuclideanOperatorNormErrorAtMost_not_vacuous")
*Plain-English reading.* Lean checks the proposition indexed as “rat euclidean operator norm error at most not vacuous”; the hypotheses and conclusion in the code panel fix its exact scope. The local Euclidean error predicate is observably non-vacuous.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The local Euclidean error predicate is observably non-vacuous.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2525](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-rateuclideanoperatornormerroratmost-not-vacuous). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_isDiagonal" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_isDiagonal")
*Plain-English reading.* Lean checks the proposition indexed as “approx diagonal operator is diagonal”; the hypotheses and conclusion in the code panel fix its exact scope. The supplied approximate diagonal matrix has zero off-diagonal entries.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The supplied approximate diagonal matrix has zero off-diagonal entries.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2539](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-approxdiagonaloperator-isdiagonal). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalOperator_isDiagonal" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalOperator_isDiagonal")
*Plain-English reading.* Lean checks the proposition indexed as “cubic diagonal operator is diagonal”; the hypotheses and conclusion in the code panel fix its exact scope. The exact cubic diagonal target has zero off-diagonal entries.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The exact cubic diagonal target has zero off-diagonal entries.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2546](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicdiagonaloperator-isdiagonal). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalEntrywiseErrorAtMost" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalEntrywiseErrorAtMost")
*Plain-English reading.* This definition gives the library's named construction or computation for “approx diagonal entrywise error at most”. Entrywise scalar-error predicate for the Scenario 2 approximate diagonal route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Entrywise scalar-error predicate for the Scenario 2 approximate diagonal route. This is strictly weaker than the open operator-norm bridge: it says only that each supplied diagonal value 'q j' is close to the target cubic amplitude.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2558](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-approxdiagonalentrywiseerroratmost). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_entrywise_error" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_entrywise_error")
*Plain-English reading.* Lean checks the proposition indexed as “approx diagonal operator entrywise error”; the hypotheses and conclusion in the code panel fix its exact scope. Local entrywise bridge for 'APPROX-DIAG-NORM': diagonal scalar errors transfer to every matrix entry of the supplied diagonal operator.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Local entrywise bridge for 'APPROX-DIAG-NORM': diagonal scalar errors transfer to every matrix entry of the supplied diagonal operator. This does not prove an operator-norm bound; it is the reusable finite-matrix side of the still-open diagonal norm obligation.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2570](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-approxdiagonaloperator-entrywise-error). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_operatorNorm_error_of_contract" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_operatorNorm_error_of_contract")
*Plain-English reading.* Lean checks the proposition indexed as “approx diagonal operator operator norm error of contract”; the hypotheses and conclusion in the code panel fix its exact scope. Conditional adapter from the compiled diagonal entrywise theorem to the task-local operator-norm contract.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Conditional adapter from the compiled diagonal entrywise theorem to the task-local operator-norm contract. This theorem is the narrow QBE-side consumer promised by the proof DAG. It does not close 'DIAGONAL-ENTRYWISE-ERROR-OPNORM' unconditionally; the supplied 'bridge' remains the explicit external/classical obligation.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2597](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-approxdiagonaloperator-operatornorm-error-of-contract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_operatorNorm_error" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_operatorNorm_error")
*Plain-English reading.* Lean checks the proposition indexed as “approx diagonal operator operator norm error”; the hypotheses and conclusion in the code panel fix its exact scope. Unconditional local Euclidean operator-norm bound for the supplied diagonal approximation.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Unconditional local Euclidean operator-norm bound for the supplied diagonal approximation. This closes the former external bridge gap using the concrete finite rational semantics above.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2619](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-approxdiagonaloperator-operatornorm-error). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.rationalCircleBranchVector" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.rationalCircleBranchVector")
*Plain-English reading.* This definition gives the library's named construction or computation for “rational circle branch vector”. Two-coordinate rational unit-circle branch vector for the approximate controlled-Householder route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Two-coordinate rational unit-circle branch vector for the approximate controlled-Householder route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2635](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-rationalcirclebranchvector). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.rationalCircleBranchVector_clean" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.rationalCircleBranchVector_clean")
*Plain-English reading.* Lean checks the proposition indexed as “rational circle branch vector clean”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2641](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-rationalcirclebranchvector-clean). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.rationalCircleBranchVector_unit" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.rationalCircleBranchVector_unit")
*Plain-English reading.* Lean checks the proposition indexed as “rational circle branch vector unit”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2645](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-rationalcirclebranchvector-unit). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_clean_entry_of_branchValue" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_clean_entry_of_branchValue")
*Plain-English reading.* Lean checks the proposition indexed as “controlled householder 8 direct sum clean entry of branch value”; the hypotheses and conclusion in the code panel fix its exact scope. Approximate-route support leaf 'APPROX-CDS-CLEAN': if each controlled Householder branch has clean coordinate 'q j', then the clean block is the supplied diagonal matrix 'diag(q)'.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Approximate-route support leaf 'APPROX-CDS-CLEAN': if each controlled Householder branch has clean coordinate 'q j', then the clean block is the supplied diagonal matrix 'diag(q)'. This is not an approximate certificate. It proves only the local clean-block shape for supplied branch vectors.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2661](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-controlledhouseholder8directsum-clean-entry-of-branchvalue). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalFourSquareBranchVector" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalFourSquareBranchVector")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic diagonal four square branch vector”. Rational branch vector whose clean coordinate is '(j / 2^n)^3'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Rational branch vector whose clean coordinate is '(j / 2^n)^3'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2709](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicdiagonalfoursquarebranchvector). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalFourSquareBranchVector_clean" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalFourSquareBranchVector_clean")
*Plain-English reading.* Lean checks the proposition indexed as “cubic diagonal four square branch vector clean”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2719](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicdiagonalfoursquarebranchvector-clean). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalFourSquareBranchVector_unit" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalFourSquareBranchVector_unit")
*Plain-English reading.* Lean checks the proposition indexed as “cubic diagonal four square branch vector unit”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2728](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicdiagonalfoursquarebranchvector-unit). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.CubicDiagonalRationalCompletion" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.CubicDiagonalRationalCompletion")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic diagonal rational completion”.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2746](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicdiagonalrationalcompletion). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalRationalCompletion_of_fourSquareWitnesses" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalRationalCompletion_of_fourSquareWitnesses")
*Plain-English reading.* Lean checks the proposition indexed as “cubic diagonal rational completion of four square witnesses”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2752](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicdiagonalrationalcompletion-of-foursquarewitnesses). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalRationalCompletion_exists" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalRationalCompletion_exists")
*Plain-English reading.* Lean checks the proposition indexed as “cubic diagonal rational completion exists”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2767](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicdiagonalrationalcompletion-exists). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicAmplitude_lt_one" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicAmplitude_lt_one")
*Plain-English reading.* Lean checks the proposition indexed as “cubic amplitude lt one”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2784](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicamplitude-lt-one). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalRationalCompletion_backendSupport" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalRationalCompletion_backendSupport")
*Plain-English reading.* Lean checks the proposition indexed as “cubic diagonal rational completion backend support”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2800](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicdiagonalrationalcompletion-backendsupport). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.CubicDiagonalExactBEContract" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.CubicDiagonalExactBEContract")
*Plain-English reading.* This record groups the data and proof fields needed for “cubic diagonal exact be contract”. A proposition-valued field is a requirement until a constructor supplies it. Strong exact certificate for the cubic target, including orthogonality.

*Formal status.* Data contract in the default import surface; proposition-valued fields are obligations, not automatically established facts.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Strong exact certificate for the cubic target, including orthogonality.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2828](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicdiagonalexactbecontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalHouseholderExactBEContract" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalHouseholderExactBEContract")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic diagonal householder exact be contract”.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2838](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicdiagonalhouseholderexactbecontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalHouseholderExactBEContract_clean_eq_target" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalHouseholderExactBEContract_clean_eq_target")
*Plain-English reading.* Lean checks the proposition indexed as “cubic diagonal householder exact be contract clean eq target”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2867](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicdiagonalhouseholderexactbecontract-clean-eq-target). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalHouseholderExactBEContract_complete" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalHouseholderExactBEContract_complete")
*Plain-English reading.* Lean checks the proposition indexed as “cubic diagonal householder exact be contract complete”; the hypotheses and conclusion in the code panel fix its exact scope. Unconditional exact root certificate for the cubic diagonal operator.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Unconditional exact root certificate for the cubic diagonal operator. The conjunction deliberately includes the unitary predicate, clean-block target, normalizer, and resource equality; a clean-block-only arithmetic wrapper is not sufficient to close an operator block-encoding task.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:2879](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicdiagonalhouseholderexactbecontract-complete). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_cube_eq_cubicDiagonalOperator" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_cube_eq_cubicDiagonalOperator")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal cube eq cubic diagonal operator”; the hypotheses and conclusion in the code panel fix its exact scope. Target-identification leaf for the hinted route: the project-local matrix cube of 'O\_0' is the cubic diagonal target 'D\_n'.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Target-identification leaf for the hinted route: the project-local matrix cube of 'O\_0' is the cubic diagonal target 'D\_n'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3001](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonal-cube-eq-cubicdiagonaloperator). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCubicProductCertificate" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCubicProductCertificate")
*Plain-English reading.* This definition gives the library's named construction or computation for “linear diagonal cubic product certificate”. The compiled non-QSVT polynomial consumer for the human hint.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The compiled non-QSVT polynomial consumer for the human hint. It reuses the exact 'O\_0' clean-block payload three times through the library's product card.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3022](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalcubicproductcertificate). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCubicProductCertificate_target_eq" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCubicProductCertificate_target_eq")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal cubic product certificate target eq”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3030](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalcubicproductcertificate-target-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCubicProductCertificate_clean_eq_target" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCubicProductCertificate_clean_eq_target")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal cubic product certificate clean eq target”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3040](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalcubicproductcertificate-clean-eq-target). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicQSVTPolynomial" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicQSVTPolynomial")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic qsvt polynomial”. The polynomial selected by the human-hinted QSVT route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The polynomial selected by the human-hinted QSVT route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3050](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicqsvtpolynomial). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicQSVTPolynomial_gridPoint_abs_le_one" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicQSVTPolynomial_gridPoint_abs_le_one")
*Plain-English reading.* Lean checks the proposition indexed as “cubic qsvt polynomial grid point abs le one”; the hypotheses and conclusion in the code panel fix its exact scope. The cubic QSVT polynomial is bounded on every spectral value used by 'O\_0'.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The cubic QSVT polynomial is bounded on every spectral value used by 'O\_0'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3053](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicqsvtpolynomial-gridpoint-abs-le-one). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTLocalSideConditions" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTLocalSideConditions")
*Plain-English reading.* This record groups the data and proof fields needed for “cubic qsvt local side conditions”. A proposition-valued field is a requirement until a constructor supplies it. Locally checkable side conditions for the cubic polynomial on the 'O\_0' spectrum.

*Formal status.* Data contract in the default import surface; proposition-valued fields are obligations, not automatically established facts.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Locally checkable side conditions for the cubic polynomial on the 'O\_0' spectrum.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3064](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicqsvtlocalsideconditions). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.cubicQSVTLocalSideConditions" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicQSVTLocalSideConditions")
*Plain-English reading.* This definition gives the library's named construction or computation for “cubic qsvt local side conditions”.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3073](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicqsvtlocalsideconditions). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTExternalSemantics" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTExternalSemantics")
*Plain-English reading.* This record groups the data and proof fields needed for “cubic qsvt external semantics”. A proposition-valued field is a requirement until a constructor supplies it. Single external boundary for the hinted route.

*Formal status.* Data contract in the default import surface; proposition-valued fields are obligations, not automatically established facts.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Single external boundary for the hinted route. The supplier must provide a certified 'O\_0' block encoding and the transformed clean block. This interface replaces unconstrained QSVT proof search: all project-local leaves are compiled, while phase synthesis and the QSVT semantic theorem remain one explicit dependency.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3091](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicqsvtexternalsemantics). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTExternalSemantics.output_eq_cubic_target" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTExternalSemantics.output_eq_cubic_target")
*Plain-English reading.* Lean checks the proposition indexed as “output eq cubic target”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3112](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicqsvtexternalsemantics-output-eq-cubic-target). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTExternalSemantics.consumerContract" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTExternalSemantics.consumerContract")
*Plain-English reading.* This definition gives the library's named construction or computation for “consumer contract”. Instantiate the generic consumer boundary without reopening QSVT search.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Instantiate the generic consumer boundary without reopening QSVT search.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3120](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicqsvtexternalsemantics-consumercontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleLayout" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleLayout")
*Plain-English reading.* This definition gives the library's named construction or computation for “amplitude oracle layout”. One signal qubit and no pure workspace at the oracle-label tier.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* One signal qubit and no pure workspace at the oracle-label tier.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3138](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-amplitudeoraclelayout). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleCircuit" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleCircuit")
*Plain-English reading.* This definition gives the library's named construction or computation for “amplitude oracle circuit”. Oracle-level exact diagonal amplitude transcript.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Oracle-level exact diagonal amplitude transcript.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3144](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-amplitudeoraclecircuit). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResource" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResource")
*Plain-English reading.* This definition gives the library's named construction or computation for “amplitude oracle resource”. Resource of the oracle-label diagonal candidate.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Resource of the oracle-label diagonal candidate.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3148](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-amplitudeoracleresource). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleCost" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleCost")
*Plain-English reading.* This definition gives the library's named construction or computation for “amplitude oracle cost”. Candidate score for the oracle-label diagonal candidate.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Candidate score for the oracle-label diagonal candidate.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3152](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-amplitudeoraclecost). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResourceTuple" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResourceTuple")
*Plain-English reading.* This definition gives the library's named construction or computation for “amplitude oracle resource tuple”. Tuple in the QBE score order '(gateCount, depth, auxiliaryQubits, oracleCalls)'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Tuple in the QBE score order '(gateCount, depth, auxiliaryQubits, oracleCalls)'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3157](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-amplitudeoracleresourcetuple). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResource_eq" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResource_eq")
*Plain-English reading.* Lean checks the proposition indexed as “amplitude oracle resource eq”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3164](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-amplitudeoracleresource-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResourceTuple_eq" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResourceTuple_eq")
*Plain-English reading.* Lean checks the proposition indexed as “amplitude oracle resource tuple eq”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3168](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-amplitudeoracleresourcetuple-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.diagonalCleanBlockContract" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.diagonalCleanBlockContract")
*Plain-English reading.* This definition gives the library's named construction or computation for “diagonal clean block contract”. Clean-block contract for the diagonal cubic candidate.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Clean-block contract for the diagonal cubic candidate.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3175](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-diagonalcleanblockcontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.diagonalCleanBlockContract_pointwise_eq" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.diagonalCleanBlockContract_pointwise_eq")
*Plain-English reading.* Lean checks the proposition indexed as “diagonal clean block contract pointwise eq”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3181](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-diagonalcleanblockcontract-pointwise-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.primitiveOracleCleanBlock_eq_target" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.primitiveOracleCleanBlock_eq_target")
*Plain-English reading.* Lean checks the proposition indexed as “primitive oracle clean block eq target”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3188](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-primitiveoraclecleanblock-eq-target). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicAmplitude_le_one" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicAmplitude_le_one")
*Plain-English reading.* Lean checks the proposition indexed as “cubic amplitude le one”; the hypotheses and conclusion in the code panel fix its exact scope. Amplitude range needed by the one-signal diagonal construction.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Amplitude range needed by the one-signal diagonal construction.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3196](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicamplitude-le-one). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.cubicAmplitude_nonneg" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.cubicAmplitude_nonneg")
*Plain-English reading.* Lean checks the proposition indexed as “cubic amplitude nonneg”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3203](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-cubicamplitude-nonneg). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleDimension" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleDimension")
*Plain-English reading.* This definition gives the library's named construction or computation for “primitive amplitude oracle dimension”. Full matrix dimension of the unexpanded one-signal primitive oracle.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Full matrix dimension of the unexpanded one-signal primitive oracle.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3210](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-primitiveamplitudeoracledimension). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleUnitary" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleUnitary")
*Plain-English reading.* This opaque declaration exposes the interface for “primitive amplitude oracle unitary” while keeping its implementation from unfolding automatically. External primitive matrix supplied by the oracle-label tier.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* External primitive matrix supplied by the oracle-label tier. This is only a named object for the semantic contract below. The current file does not prove that this opaque matrix is a gate-expanded unitary.

*Declaration kind.* opaque.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3219](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-primitiveamplitudeoracleunitary). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleIsUnitary" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleIsUnitary")
*Plain-English reading.* This opaque declaration exposes the interface for “primitive amplitude oracle is unitary” while keeping its implementation from unfolding automatically. Explicit unitarity obligation for the primitive oracle-label matrix.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Explicit unitarity obligation for the primitive oracle-label matrix.

*Declaration kind.* opaque.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3224](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-primitiveamplitudeoracleisunitary). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCleanBlockExtracts" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCleanBlockExtracts")
*Plain-English reading.* This opaque declaration exposes the interface for “primitive amplitude oracle clean block extracts” while keeping its implementation from unfolding automatically. Explicit clean-block extraction obligation for the primitive oracle-label matrix.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Explicit clean-block extraction obligation for the primitive oracle-label matrix.

*Declaration kind.* opaque.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3229](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-primitiveamplitudeoraclecleanblockextracts). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleSemanticContract" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleSemanticContract")
*Plain-English reading.* This definition gives the library's named construction or computation for “primitive amplitude oracle semantic contract”. Primitive one-signal amplitude-oracle semantic contract.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Primitive one-signal amplitude-oracle semantic contract. This contract keeps the unexpanded primitive tier honest: it requires both a unitarity obligation for the named oracle matrix and a clean-block extraction obligation whose extracted block satisfies the diagonal target contract.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3241](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-primitiveamplitudeoraclesemanticcontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleSemanticContract_unitary" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleSemanticContract_unitary")
*Plain-English reading.* Lean checks the proposition indexed as “primitive amplitude oracle semantic contract unitary”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3248](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-primitiveamplitudeoraclesemanticcontract-unitary). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleSemanticContract_cleanBlock_eq_target" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleSemanticContract_cleanBlock_eq_target")
*Plain-English reading.* Lean checks the proposition indexed as “primitive amplitude oracle semantic contract clean block eq target”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3253](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-primitiveamplitudeoraclesemanticcontract-cleanblock-eq-target). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleLayout" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleLayout")
*Plain-English reading.* This definition gives the library's named construction or computation for “expanded amplitude oracle layout”. Expanded arithmetic route layout.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Expanded arithmetic route layout. The workspace count is explicit because the reversible arithmetic, angle synthesis, and uncomputation proof are not yet fixed to one resource backend.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3268](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedamplitudeoraclelayout). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleLayout_auxiliaryQubits" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleLayout_auxiliaryQubits")
*Plain-English reading.* Lean checks the proposition indexed as “expanded amplitude oracle layout auxiliary qubits”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3273](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedamplitudeoraclelayout-auxiliaryqubits). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleNormalizer_eq" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleNormalizer_eq")
*Plain-English reading.* Lean checks the proposition indexed as “expanded amplitude oracle normalizer eq”; the hypotheses and conclusion in the code panel fix its exact scope. The expanded route targets the same exact normalizer 'alpha = 1'.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The expanded route targets the same exact normalizer 'alpha = 1'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3280](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedamplitudeoraclenormalizer-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.StandardRyCleanEntryScalarTier" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.StandardRyCleanEntryScalarTier")
*Plain-English reading.* This record groups the data and proof fields needed for “standard ry clean entry scalar tier”. A proposition-valued field is a requirement until a constructor supplies it. Scalar-tier contract for the standard 'R\_y' clean-entry identity.

*Formal status.* Data contract in the default import surface; proposition-valued fields are obligations, not automatically established facts.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Scalar-tier contract for the standard 'R\_y' clean-entry identity. The project-local matrix layer is still exact 'Rat', so 'arccos' and 'cos' are represented here by backend-supplied scalar functions. The contract keeps the standard convention explicit: for every rational amplitude 'a' in '\[0, 1\]', the clean signal entry of 'R\_y (2 \* arccos a)' is exactly 'a' after embedding into the backend scalar tier.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3293](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-standardrycleanentryscalartier). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedRyCleanEntryForCubicAmplitudes" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedRyCleanEntryForCubicAmplitudes")
*Plain-English reading.* This definition gives the library's named construction or computation for “expanded ry clean entry for cubic amplitudes”. Indexwise clean-entry obligation for the cubic diagonal amplitudes in a chosen standard-'R\_y' scalar tier.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Indexwise clean-entry obligation for the cubic diagonal amplitudes in a chosen standard-'R\_y' scalar tier.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3308](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedrycleanentryforcubicamplitudes). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.expandedRyCleanEntryForCubicAmplitudes_of_standardTier" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedRyCleanEntryForCubicAmplitudes_of_standardTier")
*Plain-English reading.* Lean checks the proposition indexed as “expanded ry clean entry for cubic amplitudes of standard tier”; the hypotheses and conclusion in the code panel fix its exact scope. 'DIAG-EXP-RY-001': the standard scalar-tier 'R\_y' clean-entry contract applies to every cubic grid amplitude because the existing Lean range lemmas prove '0 <= (j / 2^n)^3 <= 1'.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* 'DIAG-EXP-RY-001': the standard scalar-tier 'R\_y' clean-entry contract applies to every cubic grid amplitude because the existing Lean range lemmas prove '0 <= (j / 2^n)^3 <= 1'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3321](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedrycleanentryforcubicamplitudes-of-standardtier). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitude" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitude")
*Plain-English reading.* This opaque declaration exposes the interface for “expanded arithmetic computes cubic amplitude” while keeping its implementation from unfolding automatically. Semantic obligation that the expanded reversible arithmetic computes 'a\_j = (j / 2^n)^3' into the named workspace.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Semantic obligation that the expanded reversible arithmetic computes 'a\_j = (j / 2^n)^3' into the named workspace.

*Declaration kind.* opaque.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3334](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedarithmeticcomputescubicamplitude). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.ExpandedCubicArithmeticBackend" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.ExpandedCubicArithmeticBackend")
*Plain-English reading.* This record groups the data and proof fields needed for “expanded cubic arithmetic backend”. A proposition-valued field is a requirement until a constructor supplies it. Backend-level shape for the expanded reversible arithmetic compute phase.

*Formal status.* Data contract in the default import surface; proposition-valued fields are obligations, not automatically established facts.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Backend-level shape for the expanded reversible arithmetic compute phase. The structure records only the compute half of the route: starting from a clean workspace, the backend returns the same system index together with a workspace whose distinguished amplitude register contains 'CubicStatePreparation.cubicAmplitude n j'. Clean uncompute remains the separate obligation 'expandedWorkspaceCleanUncomputed'.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3346](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedcubicarithmeticbackend). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.symbolicExpandedCubicArithmeticBackend" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.symbolicExpandedCubicArithmeticBackend")
*Plain-English reading.* This definition gives the library's named construction or computation for “symbolic expanded cubic arithmetic backend”. Symbolic compute-phase backend for 'DIAG-EXP-ARITH-BACKEND-001'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Symbolic compute-phase backend for 'DIAG-EXP-ARITH-BACKEND-001'. This witness records only the pointwise arithmetic value written by the compute phase. It does not certify a reversible gate implementation, clean uncompute, or the bridge to 'expandedArithmeticComputesCubicAmplitude'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3361](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-symbolicexpandedcubicarithmeticbackend). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticBackendComputesCubicAmplitude" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticBackendComputesCubicAmplitude")
*Plain-English reading.* This definition gives the library's named construction or computation for “expanded arithmetic backend computes cubic amplitude”. Pointwise arithmetic-backend semantics for 'DIAG-EXP-ARITH-001'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Pointwise arithmetic-backend semantics for 'DIAG-EXP-ARITH-001'. For each system index 'j', the compute phase preserves 'j' and writes exactly the cubic diagonal amplitude into its distinguished amplitude register.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3377](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedarithmeticbackendcomputescubicamplitude). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.symbolicExpandedCubicArithmeticBackend_computes" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.symbolicExpandedCubicArithmeticBackend_computes")
*Plain-English reading.* Lean checks the proposition indexed as “symbolic expanded cubic arithmetic backend computes”; the hypotheses and conclusion in the code panel fix its exact scope. The symbolic backend satisfies the pointwise compute contract for every system index.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The symbolic backend satisfies the pointwise compute contract for every system index. The opaque expanded-route predicate still requires a separate backend bridge witness.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3391](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-symbolicexpandedcubicarithmeticbackend-computes). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticBackendBridge" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticBackendBridge")
*Plain-English reading.* This definition gives the library's named construction or computation for “expanded arithmetic backend bridge”. Bridge obligation from a concrete arithmetic backend to the expanded route predicate.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Bridge obligation from a concrete arithmetic backend to the expanded route predicate. This is conditional for the same reason as the rotation bridge: the backend must still justify that its pointwise compute semantics are the semantics of the route predicate used by the block-encoding contract.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3406](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedarithmeticbackendbridge). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitude_of_backendBridge" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitude_of_backendBridge")
*Plain-English reading.* Lean checks the proposition indexed as “expanded arithmetic computes cubic amplitude of backend bridge”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3412](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedarithmeticcomputescubicamplitude-of-backendbridge). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticBackendBridge_iff_of_computes" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticBackendBridge_iff_of_computes")
*Plain-English reading.* Lean checks the proposition indexed as “expanded arithmetic backend bridge iff of computes”; the hypotheses and conclusion in the code panel fix its exact scope. General normal form for arithmetic backend bridge proof search.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* General normal form for arithmetic backend bridge proof search. Once a backend's pointwise compute contract is available, proving its bridge is equivalent to proving the opaque expanded-route predicate itself. This lemma is a proof-reduction aid; it does not supply the route semantics.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3427](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedarithmeticbackendbridge-iff-of-computes). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitude_of_symbolicBackendBridge" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitude_of_symbolicBackendBridge")
*Plain-English reading.* Lean checks the proposition indexed as “expanded arithmetic computes cubic amplitude of symbolic backend bridge”; the hypotheses and conclusion in the code panel fix its exact scope. Specialized conditional closure for the symbolic arithmetic backend.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Specialized conditional closure for the symbolic arithmetic backend. This does not prove the backend bridge witness; it only packages the already compiled pointwise compute proof with a future honest bridge witness for 'DIAG-ARITH-BACKEND-BRIDGE-001'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3448](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedarithmeticcomputescubicamplitude-of-symbolicbackendbridge). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.symbolicExpandedCubicArithmeticBackend_bridge_iff" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.symbolicExpandedCubicArithmeticBackend_bridge_iff")
*Plain-English reading.* Lean checks the proposition indexed as “symbolic expanded cubic arithmetic backend bridge iff”; the hypotheses and conclusion in the code panel fix its exact scope. Normal form for the symbolic arithmetic bridge obligation.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Normal form for the symbolic arithmetic bridge obligation. For the symbolic backend, the pointwise compute proof is already compiled, so the bridge obligation is logically equivalent to the opaque expanded-route predicate itself. This is a proof-reduction lemma, not a bridge witness: it keeps 'DIAG-ARITH-BACKEND-BRIDGE-001' blocked until a concrete route-semantics representation proves 'expandedArithmeticComputesCubicAmplitude'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3468](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-symbolicexpandedcubicarithmeticbackend-bridge-iff). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicPayload_lt_capacity" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicPayload_lt_capacity")
*Plain-English reading.* Lean checks the proposition indexed as “fixed denom cubic payload lt capacity”; the hypotheses and conclusion in the code panel fix its exact scope. 'DIAG-ARITH-FIXED-DENOM-CAP-001': the fixed-denominator cubic payload fits in the '3 \* n'-qubit workspace register.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* 'DIAG-ARITH-FIXED-DENOM-CAP-001': the fixed-denominator cubic payload fits in the '3 \* n'-qubit workspace register.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3481](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomcubicpayload-lt-capacity). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicAmplitude_eq" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicAmplitude_eq")
*Plain-English reading.* Lean checks the proposition indexed as “fixed denom cubic amplitude eq”; the hypotheses and conclusion in the code panel fix its exact scope. 'DIAG-ARITH-FIXED-DENOM-ALG-001': projecting the fixed-denominator payload 'j.val ^ 3' by the '3 \* n'-qubit denominator recovers the cubic grid amplitude.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* 'DIAG-ARITH-FIXED-DENOM-ALG-001': projecting the fixed-denominator payload 'j.val ^ 3' by the '3 \* n'-qubit denominator recovers the cubic grid amplitude.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3493](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomcubicamplitude-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticBackend" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticBackend")
*Plain-English reading.* This definition gives the library's named construction or computation for “fixed denom cubic arithmetic backend”. 'DIAG-ARITH-FIXED-DENOM-BACKEND-001': concrete compute-phase backend whose '3 \* n'-qubit workspace stores the fixed-denominator payload 'j.val ^ 3'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* 'DIAG-ARITH-FIXED-DENOM-BACKEND-001': concrete compute-phase backend whose '3 \* n'-qubit workspace stores the fixed-denominator payload 'j.val ^ 3'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3509](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomcubicarithmeticbackend). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticBackend_computes" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticBackend_computes")
*Plain-English reading.* Lean checks the proposition indexed as “fixed denom cubic arithmetic backend computes”; the hypotheses and conclusion in the code panel fix its exact scope. Pointwise compute contract for the fixed-denominator arithmetic backend.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Pointwise compute contract for the fixed-denominator arithmetic backend. This closes the backend leaf only; the bridge to 'expandedArithmeticComputesCubicAmplitude' remains a separate semantic obligation.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3527](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomcubicarithmeticbackend-computes). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitudeTransparent" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitudeTransparent")
*Plain-English reading.* This definition gives the library's named construction or computation for “expanded arithmetic computes cubic amplitude transparent”. Transparent arithmetic-route interface for 'DIAG-ARITH-ROUTE-TRANSPARENT-001'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Transparent arithmetic-route interface for 'DIAG-ARITH-ROUTE-TRANSPARENT-001'. This records that some explicit backend satisfies the pointwise compute contract. It is intentionally weaker than the opaque expanded-route predicate: using it as a route certificate still requires a later named bridge or contract refactor.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3546](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedarithmeticcomputescubicamplitudetransparent). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticRouteTransparent" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticRouteTransparent")
*Plain-English reading.* Lean checks the proposition indexed as “fixed denom cubic arithmetic route transparent”; the hypotheses and conclusion in the code panel fix its exact scope. Fixed-denominator witness for the transparent arithmetic route interface.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Fixed-denominator witness for the transparent arithmetic route interface. This packages the already compiled fixed-denominator backend and its pointwise compute theorem. It does not prove 'expandedArithmeticComputesCubicAmplitude n (3 \* n)'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3558](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomcubicarithmeticroutetransparent). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticBackend_bridge_iff" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticBackend_bridge_iff")
*Plain-English reading.* Lean checks the proposition indexed as “fixed denom cubic arithmetic backend bridge iff”; the hypotheses and conclusion in the code panel fix its exact scope. Fixed-denominator normal form for the arithmetic bridge obligation.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Fixed-denominator normal form for the arithmetic bridge obligation. The concrete backend's pointwise compute proof is available, so direct bridge search is equivalent to proving the opaque expanded-route predicate itself. This records the remaining route-semantics gap without supplying a bridge witness.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3572](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomcubicarithmeticbackend-bridge-iff). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyUsesCubicAngle" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyUsesCubicAngle")
*Plain-English reading.* This opaque declaration exposes the interface for “expanded controlled ry uses cubic angle” while keeping its implementation from unfolding automatically. Semantic obligation for the standard 'R\_y' convention on the signal qubit: for each basis index 'j', the route uses 'theta\_j = 2 \* arccos ((j / 2^n)^3)', so the clean entry is 'cos (theta\_j / 2) = (j / 2^n)^3'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Semantic obligation for the standard 'R\_y' convention on the signal qubit: for each basis index 'j', the route uses 'theta\_j = 2 \* arccos ((j / 2^n)^3)', so the clean entry is 'cos (theta\_j / 2) = (j / 2^n)^3'.

*Declaration kind.* opaque.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3586](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedcontrolledryusescubicangle). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyUsesCubicAngleTransparent" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyUsesCubicAngleTransparent")
*Plain-English reading.* This definition gives the library's named construction or computation for “expanded controlled ry uses cubic angle transparent”. Transparent controlled-'R\_y' angle-convention interface for 'DIAG-RY-TRANSPARENT-INTERFACE-001'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Transparent controlled-'R\_y' angle-convention interface for 'DIAG-RY-TRANSPARENT-INTERFACE-001'. This records only the already compiled scalar clean-entry fact for every standard tier. It does not prove the opaque route predicate 'expandedControlledRyUsesCubicAngle'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3597](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedcontrolledryusescubicangletransparent). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomControlledRyRouteTransparent" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomControlledRyRouteTransparent")
*Plain-English reading.* Lean checks the proposition indexed as “fixed denom controlled ry route transparent”; the hypotheses and conclusion in the code panel fix its exact scope. Fixed-denominator wrapper for the transparent controlled-'R\_y' route.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Fixed-denominator wrapper for the transparent controlled-'R\_y' route. This packages the scalar-tier theorem at workspace size '3 \* n'. It does not provide a backend witness for 'expandedControlledRyUsesCubicAngle'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3608](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomcontrolledryroutetransparent). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyBackendBridge" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyBackendBridge")
*Plain-English reading.* This definition gives the library's named construction or computation for “expanded controlled ry backend bridge”. Backend bridge obligation from the scalar-tier 'R\_y' clean-entry interface to the expanded route predicate.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Backend bridge obligation from the scalar-tier 'R\_y' clean-entry interface to the expanded route predicate. This is intentionally conditional: the file already proves the scalar clean-entry fact for cubic amplitudes, but a concrete backend must still justify that this fact is the semantics of the controlled rotation used by the route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3622](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedcontrolledrybackendbridge). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyUsesCubicAngle_of_backendBridge" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyUsesCubicAngle_of_backendBridge")
*Plain-English reading.* Lean checks the proposition indexed as “expanded controlled ry uses cubic angle of backend bridge”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3628](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedcontrolledryusescubicangle-of-backendbridge). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyBackendBridge_iff_of_standardTier" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyBackendBridge_iff_of_standardTier")
*Plain-English reading.* Lean checks the proposition indexed as “expanded controlled ry backend bridge iff of standard tier”; the hypotheses and conclusion in the code panel fix its exact scope. Normal form for controlled-rotation backend-bridge proof search.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Normal form for controlled-rotation backend-bridge proof search. The scalar-tier clean-entry theorem is already compiled, so proving a backend bridge for the controlled rotation is equivalent to proving the opaque route predicate itself. This is a proof-reduction lemma for 'DIAG-RY-BACKEND-WITNESS-001'; it does not supply the missing backend semantics.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3644](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedcontrolledrybackendbridge-iff-of-standardtier). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.ExpandedControlledRyWorkspaceReadonlyWitness" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.ExpandedControlledRyWorkspaceReadonlyWitness")
*Plain-English reading.* This record groups the data and proof fields needed for “expanded controlled ry workspace readonly witness”. A proposition-valued field is a requirement until a constructor supplies it. Transparent readonly-rotation interface for 'DIAG-RY-WORKSPACE-READONLY-001'.

*Formal status.* Data contract in the default import surface; proposition-valued fields are obligations, not automatically established facts.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Transparent readonly-rotation interface for 'DIAG-RY-WORKSPACE-READONLY-001'. This records that the controlled signal rotation may read the arithmetic workspace payload while preserving both the system index and workspace value. It does not prove 'expandedWorkspaceCleanUncomputed' or any opaque route predicate.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3666](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedcontrolledryworkspacereadonlywitness). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyWorkspaceReadonlyTransparent" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyWorkspaceReadonlyTransparent")
*Plain-English reading.* This definition gives the library's named construction or computation for “expanded controlled ry workspace readonly transparent”. Transparent predicate for a controlled-rotation step that preserves the arithmetic workspace.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Transparent predicate for a controlled-rotation step that preserves the arithmetic workspace. This is intentionally separate from route-level cleanup; a later packet must choose either a transparent cleanup contract refactor or a nontrivial bridge.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3686](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedcontrolledryworkspacereadonlytransparent). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedWorkspaceCleanUncomputed" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedWorkspaceCleanUncomputed")
*Plain-English reading.* This opaque declaration exposes the interface for “expanded workspace clean uncomputed” while keeping its implementation from unfolding automatically. Semantic obligation that the arithmetic workspace is returned clean.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Semantic obligation that the arithmetic workspace is returned clean.

*Declaration kind.* opaque.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3691](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedworkspacecleanuncomputed). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.ExpandedArithmeticCleanUncomputeWitness" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.ExpandedArithmeticCleanUncomputeWitness")
*Plain-English reading.* This record groups the data and proof fields needed for “expanded arithmetic clean uncompute witness”. A proposition-valued field is a requirement until a constructor supplies it. Transparent clean-uncompute interface for 'DIAG-EXP-UNCOMP-TRANSPARENT-INTERFACE-001'.

*Formal status.* Data contract in the default import surface; proposition-valued fields are obligations, not automatically established facts.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Transparent clean-uncompute interface for 'DIAG-EXP-UNCOMP-TRANSPARENT-INTERFACE-001'. This records the data needed to state honest reversible cleanup: a compute step matching the backend on clean workspace, an uncompute step that preserves the system index, and a two-sided cleanup condition after compute. It does not prove the opaque route predicate 'expandedWorkspaceCleanUncomputed'.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3703](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedarithmeticcleanuncomputewitness). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedWorkspaceCleanUncomputedTransparent" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedWorkspaceCleanUncomputedTransparent")
*Plain-English reading.* This definition gives the library's named construction or computation for “expanded workspace clean uncomputed transparent”. Transparent cleanup predicate backed by an explicit reversible witness.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Transparent cleanup predicate backed by an explicit reversible witness. This is intentionally separate from 'expandedWorkspaceCleanUncomputed'; a later route must either instantiate this interface and refactor a contract to consume it, or supply a nontrivial bridge to the opaque predicate.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3731](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedworkspacecleanuncomputedtransparent). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.expandedWorkspaceCleanUncomputedTransparent_of_witness" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedWorkspaceCleanUncomputedTransparent_of_witness")
*Plain-English reading.* Lean checks the proposition indexed as “expanded workspace clean uncomputed transparent of witness”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3735](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedworkspacecleanuncomputedtransparent-of-witness). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicComputeStep" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicComputeStep")
*Plain-English reading.* This definition gives the library's named construction or computation for “fixed denom cubic compute step”. Fixed-denominator reversible compute lift for 'DIAG-EXP-UNCOMP-FIXED-DENOM-WITNESS-001'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Fixed-denominator reversible compute lift for 'DIAG-EXP-UNCOMP-FIXED-DENOM-WITNESS-001'. This modular-add step agrees with 'fixedDenomCubicArithmeticBackend' on clean workspace, but unlike the backend's overwrite-style compute field it is invertible on every workspace value.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3783](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomcubiccomputestep). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicUncomputeStep" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicUncomputeStep")
*Plain-English reading.* This definition gives the library's named construction or computation for “fixed denom cubic uncompute step”. Modular-subtract inverse for 'fixedDenomCubicComputeStep'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Modular-subtract inverse for 'fixedDenomCubicComputeStep'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3791](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomcubicuncomputestep). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicComputeStep_matches_backend_on_clean" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicComputeStep_matches_backend_on_clean")
*Plain-English reading.* Lean checks the proposition indexed as “fixed denom cubic compute step matches backend on clean”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3798](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomcubiccomputestep-matches-backend-on-clean). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicUncomputeStep_after_compute" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicUncomputeStep_after_compute")
*Plain-English reading.* Lean checks the proposition indexed as “fixed denom cubic uncompute step after compute”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3807](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomcubicuncomputestep-after-compute). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomExpandedArithmeticCleanUncomputeWitness" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomExpandedArithmeticCleanUncomputeWitness")
*Plain-English reading.* This definition gives the library's named construction or computation for “fixed denom expanded arithmetic clean uncompute witness”. Fixed-denominator witness for the transparent clean-uncompute interface.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Fixed-denominator witness for the transparent clean-uncompute interface. This packages modular add/sub cleanup only. It does not prove the opaque predicate 'expandedWorkspaceCleanUncomputed', does not state controlled-rotation workspace-readonly semantics, and does not close extraction or unitarity.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3827](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomexpandedarithmeticcleanuncomputewitness). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomWorkspaceCleanUncomputedTransparent" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomWorkspaceCleanUncomputedTransparent")
*Plain-English reading.* Lean checks the proposition indexed as “fixed denom workspace clean uncomputed transparent”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3846](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomworkspacecleanuncomputedtransparent). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalValueBackend" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalValueBackend")
*Plain-English reading.* This record groups the data and proof fields needed for “linear diagonal value backend”. A proposition-valued field is a requirement until a constructor supplies it. Backend-level shape for computing the hinted linear diagonal value 'x\_j = j / 2^n'.

*Formal status.* Data contract in the default import surface; proposition-valued fields are obligations, not automatically established facts.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Backend-level shape for computing the hinted linear diagonal value 'x\_j = j / 2^n'. This is a transparent value-computation support interface for 'HINT-O0-BACKEND'. It does not provide the signal rotation, rational orthogonal matrix, or clean-block equality required by 'LinearDiagonalInputBEContract'.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3860](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalvaluebackend). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalValueBackendComputesGridPoint" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalValueBackendComputesGridPoint")
*Plain-English reading.* This definition gives the library's named construction or computation for “linear diagonal value backend computes grid point”. Pointwise value-computation contract for a linear diagonal backend.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Pointwise value-computation contract for a linear diagonal backend. On clean workspace the backend preserves the system index and writes exactly 'CubicStatePreparation.gridPoint n j' into its distinguished value register.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3874](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalvaluebackendcomputesgridpoint). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalValueBackend" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalValueBackend")
*Plain-English reading.* This definition gives the library's named construction or computation for “fixed denom linear diagonal value backend”. Fixed-denominator value backend for 'O\_0'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Fixed-denominator value backend for 'O\_0'. The workspace stores the numerator 'j' in an 'n'-qubit register and interprets it as the rational value 'j / 2^n'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3889](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomlineardiagonalvaluebackend). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalValueBackend_computes" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalValueBackend_computes")
*Plain-English reading.* Lean checks the proposition indexed as “fixed denom linear diagonal value backend computes”; the hypotheses and conclusion in the code panel fix its exact scope. The fixed-denominator linear backend computes 'x\_j = j / 2^n' on clean workspace.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The fixed-denominator linear backend computes 'x\_j = j / 2^n' on clean workspace.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3901](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomlineardiagonalvaluebackend-computes). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalValueCleanUncomputeWitness" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalValueCleanUncomputeWitness")
*Plain-English reading.* This record groups the data and proof fields needed for “linear diagonal value clean uncompute witness”. A proposition-valued field is a requirement until a constructor supplies it. Transparent cleanup witness for a linear value backend.

*Formal status.* Data contract in the default import surface; proposition-valued fields are obligations, not automatically established facts.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Transparent cleanup witness for a linear value backend. The witness uses an invertible compute/uncompute pair around the backend's clean-workspace value contract. It is intentionally separate from the missing controlled-rotation and full clean-block obligations.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3919](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalvaluecleanuncomputewitness). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalWorkspaceCleanUncomputedTransparent" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalWorkspaceCleanUncomputedTransparent")
*Plain-English reading.* This definition gives the library's named construction or computation for “linear diagonal workspace clean uncomputed transparent”. Transparent predicate for honest compute/uncompute cleanup of an 'O\_0' value backend.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Transparent predicate for honest compute/uncompute cleanup of an 'O\_0' value backend.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3941](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalworkspacecleanuncomputedtransparent). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalWorkspaceCleanUncomputedTransparent_of_witness" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalWorkspaceCleanUncomputedTransparent_of_witness")
*Plain-English reading.* Lean checks the proposition indexed as “linear diagonal workspace clean uncomputed transparent of witness”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3945](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-lineardiagonalworkspacecleanuncomputedtransparent-of-witness). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalComputeStep" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalComputeStep")
*Plain-English reading.* This definition gives the library's named construction or computation for “fixed denom linear diagonal compute step”. Modular-add compute step for the fixed-denominator linear backend.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Modular-add compute step for the fixed-denominator linear backend.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3952](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomlineardiagonalcomputestep). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalUncomputeStep" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalUncomputeStep")
*Plain-English reading.* This definition gives the library's named construction or computation for “fixed denom linear diagonal uncompute step”. Modular-subtract inverse for 'fixedDenomLinearDiagonalComputeStep'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Modular-subtract inverse for 'fixedDenomLinearDiagonalComputeStep'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3960](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomlineardiagonaluncomputestep). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalComputeStep_matches_backend_on_clean" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalComputeStep_matches_backend_on_clean")
*Plain-English reading.* Lean checks the proposition indexed as “fixed denom linear diagonal compute step matches backend on clean”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3967](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomlineardiagonalcomputestep-matches-backend-on-clean). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalUncomputeStep_after_compute" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalUncomputeStep_after_compute")
*Plain-English reading.* Lean checks the proposition indexed as “fixed denom linear diagonal uncompute step after compute”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3976](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomlineardiagonaluncomputestep-after-compute). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalCleanUncomputeWitness" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalCleanUncomputeWitness")
*Plain-English reading.* This definition gives the library's named construction or computation for “fixed denom linear diagonal clean uncompute witness”. Fixed-denominator cleanup witness for the hinted 'O\_0' value backend.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Fixed-denominator cleanup witness for the hinted 'O\_0' value backend. This closes only the transparent value-compute/cleanup support leaf for 'HINT-O0-BACKEND'; a full 'LinearDiagonalInputBEContract' instance still needs a signal-amplitude matrix with 'IsRationalOrthogonal', clean-block equality, and resource accounting.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:3997](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomlineardiagonalcleanuncomputewitness). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalWorkspaceCleanUncomputedTransparent" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalWorkspaceCleanUncomputedTransparent")
*Plain-English reading.* Lean checks the proposition indexed as “fixed denom linear diagonal workspace clean uncomputed transparent”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:4016](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-fixeddenomlineardiagonalworkspacecleanuncomputedtransparent). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockExtracts" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockExtracts")
*Plain-English reading.* This opaque declaration exposes the interface for “expanded amplitude oracle clean block extracts” while keeping its implementation from unfolding automatically. Clean-block extraction obligation for the expanded arithmetic/rotation route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Clean-block extraction obligation for the expanded arithmetic/rotation route.

*Declaration kind.* opaque.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:4023](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedamplitudeoraclecleanblockextracts). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockContract" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockContract")
*Plain-English reading.* This definition gives the library's named construction or computation for “expanded amplitude oracle clean block contract”. Expanded-route clean-block contract for 'DIAG-EXPANDED-CONTRACT-001'.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Expanded-route clean-block contract for 'DIAG-EXPANDED-CONTRACT-001'. This is an interface, not a proof of the expanded circuit. It keeps the transparent arithmetic witness, transparent controlled-rotation witness, and clean-uncompute obligations explicit and requires the extracted clean block to satisfy the existing diagonal contract.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:4035](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedamplitudeoraclecleanblockcontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockContract_diagonal" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockContract_diagonal")
*Plain-English reading.* Lean checks the proposition indexed as “expanded amplitude oracle clean block contract diagonal”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:4044](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedamplitudeoraclecleanblockcontract-diagonal). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockContract_eq_target" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockContract_eq_target")
*Plain-English reading.* Lean checks the proposition indexed as “expanded amplitude oracle clean block contract eq target”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:4051](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedamplitudeoraclecleanblockcontract-eq-target). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleSemanticContract" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleSemanticContract")
*Plain-English reading.* This definition gives the library's named construction or computation for “expanded amplitude oracle semantic contract”. Conditional semantic interface for an expanded arithmetic/rotation route with an explicit workspace size.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Conditional semantic interface for an expanded arithmetic/rotation route with an explicit workspace size.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:4063](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedamplitudeoraclesemanticcontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleSemanticContract_cleanBlock_eq_target" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleSemanticContract_cleanBlock_eq_target")
*Plain-English reading.* Lean checks the proposition indexed as “expanded amplitude oracle semantic contract clean block eq target”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:4068](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-expandedamplitudeoraclesemanticcontract-cleanblock-eq-target). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate")
*Plain-English reading.* This definition gives the library's named construction or computation for “primitive amplitude oracle candidate”. Conditional candidate at the primitive oracle-label tier.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Conditional candidate at the primitive oracle-label tier.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:4080](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-primitiveamplitudeoraclecandidate). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate_costTuple_eq" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate_costTuple_eq")
*Plain-English reading.* Lean checks the proposition indexed as “primitive amplitude oracle candidate cost tuple eq”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:4097](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-primitiveamplitudeoraclecandidate-costtuple-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate_unitary_from_contract" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate_unitary_from_contract")
*Plain-English reading.* Lean checks the proposition indexed as “primitive amplitude oracle candidate unitary from contract”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:4108](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-primitiveamplitudeoraclecandidate-unitary-from-contract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate_block_from_contract" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate_block_from_contract")
*Plain-English reading.* Lean checks the proposition indexed as “primitive amplitude oracle candidate block from contract”; the hypotheses and conclusion in the code panel fix its exact scope.

*Formal status.* Compiled theorem in the default ASPBE import surface; the displayed Lean signature is the authoritative claim.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:4114](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-primitiveamplitudeoraclecandidate-block-from-contract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleVerified" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleVerified")
*Plain-English reading.* This definition gives the library's named construction or computation for “primitive amplitude oracle verified”. Conditional exact certificate for the primitive oracle-label tier.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Conditional exact certificate for the primitive oracle-label tier. This packages a verified block encoding only from an explicit proof of 'primitiveAmplitudeOracleSemanticContract n'; the contract itself remains an open primitive-oracle obligation until such a proof or accepted primitive axiom is supplied.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:4128](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-primitiveamplitudeoracleverified). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleClaim" (lean := "QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleClaim")
*Plain-English reading.* This definition gives the library's named construction or computation for “amplitude oracle claim”. Human-facing construction claim for the first exact diagonal route.

*Formal status.* Compiled declaration in the default ASPBE import surface; its kind and displayed Lean type determine how it may be used.

*Why it is in this chapter.* State-preparation and exact rational Householder developments for the cubic benchmark family.

*Technical source note.* Human-facing construction claim for the first exact diagonal route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/CubicStatePreparation.lean:4136](../../../../library/modules/cubicstatepreparation/#decl-quantumblockencoding-cubicdiagonaloracle-amplitudeoracleclaim). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::
