# Independent formal reconstruction, c28

This is a FORMAL-ONLY decoding of three complete Lean modules and the formal provider definitions needed to interpret them. It was written before the first Lean command in this run. No paper, source title/claim packet, authored lesson, atlas, author map, graph, earlier mathematical reconstruction or review was supplied or read. `sourceAgreement = null`; `opaqueAuthorPacketBinding = null`. Compilation plumbing borrowed from a prior run has no mathematical evidentiary role. This text describes the formal contract, not its agreement with an external source.

## Ambient types and scalar conventions

The natural-number-indexed matrix alias is a function `Fin rows -> Fin cols -> α`; the finite matrix abbreviation in ConcreteSemantics uses Mathlib's matrix type with those same finite indices. State vectors are column-coordinate functions. `gridSize n = 2^n`, and the all-zero index is the element with value zero. Primitive basis states instead are functions `Fin n -> Fin 2`. There is no flattening equivalence between those two basis representations proved in these three modules. One must not infer a little-endian or big-endian integer encoding of primitive bit functions.

Matrix multiplication acts on column vectors, so a gate list is executed left to right while its matrix product is written in reverse order. Matrix `star` is conjugate transpose. Complex scalar conjugation is distinct from matrix transpose. All rotation parameters are exact reals; the angle syntax also admits arbitrary real leaves. These are ideal exact matrix semantics, not finite-bit angle synthesis.

All definitions below are literal on their entire typed carriers, or proof-carrying records. There is no choice of an external mathematically characterized representative. Numerical approximation, hardware noise and resource implementation are outside this contract.

## ConcreteSemantics: 25 named source roots

`FiniteMatrix`, `StateVector`, `basisKet`, `basisKet_apply`, `zeroKet`, `applyVec` establish the carriers and the Kronecker-delta vector: e_j(i)=1 when j=i and zero otherwise, and `(Av)(i)=sum_j A(i,j)v(j)`. The relevant algebra assumptions vary: the raw action uses a nonunital nonassociative semiring, whereas the single-one ket lemmas use a nonassociative semiring. `ComplexUnitaryGate` contains a square complex matrix of size 2^n and membership in Mathlib's two-sided unitary group.

`applyVec_basisKet` and `applyVec_zeroKet` say that applying a matrix to a basis ket selects its indexed column. `applyVec_twoBasisSuperposition` and its `_apply` version say

    A(a e_l + b e_r) = a A[:,l] + b A[:,r],
    [A(a e_l+b e_r)]_i = a A(i,l)+b A(i,r).

The indices need not be distinct. These identities follow by distributivity and linearity of finite summation. They do not require unitarity or vector normalization.

`firstColumnMatches_iff_applyVec_zeroKet` is the equivalence between a pointwise first-column equality and equality of the resulting vector. It is a change of interface, not an existence theorem for a preparing circuit.

`ComplexStatePreparationCertificate` packages a target, a complex unitary matrix, a proof of `target.normalization`, and an equality U e_0 = target.amplitudes. The inherited target's `normalization` field is an arbitrary proposition. Thus this field does not definitionally mean sum |v_i|²=1. Independently, the unitary action equation mathematically implies unit norm for v; that norm theorem is not asserted by these roots.

Its `candidate` copies an arbitrary supplied circuit, layered schedule, resource record and optional auxiliary-qubit count into a candidate, alongside the certificate matrix. Its `verified` fills the target-normalization and unitarity obligations and converts the vector equality to a first-column equality. `preparesVector` projects the supplied preparation proof. There is no hypothesis or theorem identifying the supplied circuit's denotation with the matrix, no schedule-validity check, and no proof that the resource record counts that circuit. Arbitrary metadata here must not be advertised as verified implementation or complexity.

`ProductRegisterMatrix`, `flatToProductRegister`, `productRegisterBlockProjection` use the literal flattening `(s,i) -> s*systemDim+i`, separately for row and column widths. Projection takes equal selected signal indices on both sides: B(i,j)=U((s,i),(s,j)). `productRegisterBlockProjection_flatToProductRegister` proves this is the inherited flat block projection. `productIndex_val_eq_signalSystemBlockRowIndex` checks the same flattening against the product-index provider. `signalSystemBlockProjection_eq_cleanBlockProduct` identifies the rational-valued clean product block pointwise with the projection. These identities are definitional; there is no tensor-factor reorder hidden in them.

`cleanBasisActionAmplitude` is the output amplitude at `(s,output)` after applying U to the basis input `(s,input)`. `cleanBasisActionAmplitude_eq_signalSystemBlockProjection` reduces it to U's selected matrix entry, using the basis-column identity. `pointwiseProjection_iff_cleanBasisAction` says equality of all those amplitudes is exactly pointwise equality of the projected block with an arbitrary target matrix. These are amplitude equalities, not probabilities. They do not state that the signal register remains clean with probability one, that off-sector amplitudes vanish, that the block is normalized, or that postselection succeeds with a given probability. The signal index is any typed element, not necessarily zero. Empty dimensions are allowed where indices are absent; requiring `Fin signalDim` excludes an empty signal carrier at a call site.

## PrimitiveSemantics: 55 named source roots

### Single-qubit and conjugation algebra

`standardRyMatrix(theta)` is

    [[cos(theta/2), -sin(theta/2)],
     [sin(theta/2),  cos(theta/2)]].

`standardRyMatrix_zero`, `_add`, `_neg`, `_unitary` give identity at zero, `Ry(l+r)=Ry(r)Ry(l)`, `Ry(-theta)=Ry(theta)*`, and unitarity. The sum formula follows by the sine/cosine addition formulas entrywise, the negative formula by parity, and unitarity by cos²+sin²=1. `xMatrix` has zero diagonal and one off diagonal; `xMatrix_conjugates_standardRy` gives X Ry(theta) X = Ry(-theta).

The seven scalar helper roots `star_complex_cos_ofReal`, `conj_complex_cos_ofReal`, `star_complex_sin_ofReal`, `conj_complex_sin_ofReal`, `complex_ofReal_div_two`, `conj_complex_cos_ofReal_div_two`, `conj_complex_sin_ofReal_div_two` state reality under conjugation and compatibility of the real-to-complex embedding with halving. These are ambient scalar identities, not additional quantum assumptions.

`standardRyMatrix_two_arccos_eq_amplitudeRotation` identifies Ry(2 arccos c) with the provider's literal rotation by arccos c. Its -1≤c≤1 binders are present in the theorem but unused in this definitional equality; a clean matrix entry equals c only after a separate bounded-arccos theorem. `standardRyMatrix_pi_div_two_eq_warmRobinUniformBitPrepare` identifies the pi/2 rotation with the literal matrix `[[sqrt(2)/2,-sqrt(2)/2],[sqrt(2)/2,sqrt(2)/2]]`. Despite the provider name, this matrix is not the usual full Hadamard matrix: the second column's signs differ.

`standardRzMatrix(theta)` is diagonal with entries cos(theta/2)-i sin(theta/2), cos(theta/2)+i sin(theta/2). `_unitary` uses the norm-one trigonometric identity on each diagonal entry; `_neg` gives its adjoint at the negative angle.

### Basis permutations and local lifting

`PrimitiveBasis`, `flipBit`, `flipBit_flipBit`, `xBasisAction`, `xBasisAction_involutive`, `xBasisEquiv` describe a bit flip at exactly the selected wire and show its involution. `cxBasisAction` leaves a state unchanged if its control bit is zero and otherwise flips the target. `cxBasisAction_involutive`, `cxBasisEquiv`, `cxBasisEquiv_apply` require control != target for invertibility. The action function exists also with equal control and target, but no such invertibility claim is made. The proof keeps the control unchanged while applying the target flip twice.

`OtherPrimitiveWires` is the subtype excluding the selected wire. `splitPrimitiveWire` bijectively decomposes a basis assignment into its selected bit and the remaining assignment. `splitPrimitiveWire_other_apply` verifies the latter component. `liftPrimitiveOneQubit` reindexes `gate tensor I` through this bijection. `_apply` states the entry is `gate(row(target),column(target))` exactly when the remaining assignments agree, and zero otherwise. `_unitary` transports unitarity of gate tensor identity through the reindexing. This is exact arbitrary-width lifting, not a finite simulation.

`star_equivPermutationMatrix` says the adjoint of the matrix P_e(row,col)=[row=e(col)] is P_(e inverse). `star_liftPrimitiveOneQubit` says lifting commutes with adjoint. The proof mechanisms are the transposed inverse relation for permutation entries and entrywise conjugation with an identity spectator factor.

### Gate lists, phases and refinement

`evalPrimitiveGate` interprets X and distinct-wire CX as permutation matrices and Ry/Rz as the lifted rotations evaluated at exact angles. `_unitary` follows by its four constructor cases. `xBasisEquiv_symm` and `cxBasisEquiv_symm` identify each inverse with itself. `evalPrimitiveGate_dagger` consequently interprets the syntactic dagger as matrix adjoint.

`evalPrimitiveCircuit` assigns the empty list identity and a nonempty list `gate::rest` the product E(rest)E(gate). `_unitary` is closure under products. `_append` is E(left++right)=E(right)E(left); it follows by induction and associativity. `_dagger` says reversing the list and daggering each gate gives E(circuit)*; it follows by the append identity and star reversing multiplication. No gate commutation is assumed.

`evalGlobalPhase(angle)=exp(i eval(angle))`. `_unitary` says this complex scalar has norm one (via conjugate multiplication), and `_neg` says negative angle conjugates it. `evalPrimitiveProgram` multiplies the circuit matrix by this phase. `_identity`, `_seq`, `_unitary`, `_dagger` show identity, temporal composition, unitarity and adjoint compatibility for programs, with exact global phase retained. The sequence proof uses exp(i(a+b))=exp(ia)exp(ib) and scalar centrality. There is no quotient by global phase and no loss of relative phase if such programs later become controlled branches; no theorem here constructs such a controlled-program operation.

`PrimitiveRefinement` is a record containing a circuit, arbitrary target matrix and equality E(circuit)=target. It does not generate the circuit or provide a synthesis-complexity bound. The inherited PrimitiveRefinement provider extends this with a phase-aware program record and metadata-only resource accessors; its proof of zero oracle calls concerns the literal circuit resource accounting, not an implementation of an external oracle.

## ReversibleClassical: 8 named source roots

`ReversibleGate` has X, CX with distinct wires, and CCX with three pairwise distinct wires. `ReversibleProgram` is its gate list. `ccxBasisAction` flips the target iff both controls equal one. `ccxBasisAction_involutive` needs only each control distinct from the target, not controls distinct from one another. This is sufficient since both control values are unchanged by the target operation; an active condition remains active, and two flips cancel. If inactive, both applications are the identity. `ccxBasisEquiv` packages the action and inverse as the same function, and `_apply` exposes its action.

`evalReversibleGate` returns those basis equivalences by constructor. The CCX gate's control-control distinctness proof is not used by its semantic equivalence, though the syntax still requires it. `evalReversibleProgram` is identity on an empty list and `E(gate).trans E(rest)` otherwise. Since equivalence trans applies the first function followed by the second, this executes the gate list from head to tail. These are arbitrary-width classical reversible permutations, not a Toffoli decomposition into the primitive Ry/Rz/CX language, not a complex-matrix embedding theorem, and not resource bounds.

## Whole-module coverage and retained boundaries

The 25+55+8 named declarations above include aliases, structures and the inductive type, and all attribute-prefixed lemmas. None of these three modules contains a source-declared private root or instance. Generated constructors/projections/recursors are not confused with source-declared roots; their existence is elaboration evidence, not extra mathematical advances. All roots have a disposition above; no source-facing theorem is asserted.

The formal provider closure has 23 project modules sealed, with complete comment-stripped text and an ambient/declaration inventory. Only the semantic definitions needed above were interpreted mathematically; sealing a provider is not a claim to reconstruct all its mathematics. PrimitiveSemantics reaches ConcreteSemantics through inherited Robin providers. ReversibleClassical reaches PrimitiveSemantics through inherited PrimitiveRefinement. The intended fresh compilation explicitly overrides already-fresh cohort modules in ModuleSetup.importArts, including transitive imports, but does not rebuild all intermediate or other provider modules. Therefore the verification is never a clean transitive rebuild. The same provider sources and inherited project oleans must be rehashed at completion.

An initial inventory scan missed inline attributes. Both its original seal and a version-two corrected inventory seal are retained. Version two was made before any Lean command and changes no source/toolchain/provider bytes. Setups and execution metadata created after sealing receive late attestations, never retroactive initial-seal status.

No paper fidelity, author-approved binder classification, publication acceptance, source topology, full repository/test/site closure, complete producer, finite-bit complexity or hardware-cost certificate follows from this packet. Full repository gates are outside the assigned focused scope. Remaining publication and independent-source-review decisions belong to a distinct source-present reviewer.
