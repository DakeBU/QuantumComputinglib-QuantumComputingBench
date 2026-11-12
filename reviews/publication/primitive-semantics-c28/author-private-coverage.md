# Author-private whole-module coverage and ambient audit

Evidence class: retrospective local source recovery. Historical formalizer: UNKNOWN. This author packet is not independent review, external-paper reproduction, pre-proof provenance, novelty evidence, a build result, or publication acceptance. Only `source-only.md` is intended for a fresh source-first mathematical reader; this mapping and `source-freeze.md` are private audit inputs.

## Reading boundary and conventions for this table

The three assigned actual files were read completely, including comments, imports, proof bodies and end markers. No decoder, reviewer or older review output was read. Target files were not edited. All declarations below have disposition NODE and map to the indicated source section. Proof-body tactic steps are compressed into the accompanying mathematical derivation, not treated as additional mathematical hypotheses.

Notation: C means `QuantumBlockEncoding.ConcreteSemantics`; P means `QuantumBlockEncoding`; R also means `QuantumBlockEncoding`, in the third file. Unqualified names in the first table are under C except the explicitly nested certificate namespace. Natural dimensions and wire counts, scalar carriers and universes, matrix/vector arguments, finite indices, real/complex scalars, exact expression objects, lists, typeclass data and equality decisions are TYPING. A logical premise on their values is SOURCE when the source section explicitly states it. STANDING, RULED and EXCESS premises are not introduced by this reconstruction. Existing source normalization/semantic evidence is not silently supplied by the author.

All source definitions in the targets are literal; equivalences package explicit mutually inverse functions, not arbitrary quotient representatives. The exact-refinement and certificate structures are evidence-bearing records, not characterized-object choice constructions. Standard complex matrix `star` is conjugate transpose, while scalar star is complex conjugation. `Matrix` without `_root_` in the first file resolves to the project function-valued finite matrix carrier; the concrete Mathlib carrier is definitionally the same function type. Matrix multiplication used by primitive semantics is Mathlib multiplication, not the lightweight syntactic fold operator.

## Complete ambient, syntax and import disposition

| Region | Ambient/disposition |
| --- | --- |
| `ConcreteSemantics.lean:1–6` | Direct imports, all retained: `Mathlib.Data.Complex.Basic`, `Mathlib.Data.Matrix.Mul`, `Mathlib.LinearAlgebra.UnitaryGroup`, `QuantumBlockEncoding.BlockEncodingClassics`, `QuantumBlockEncoding.CircuitSemantics`, `QuantumBlockEncoding.StatePreparation`. |
| `ConcreteSemantics.lean:8–19` | Module explanation: bridge only, not automatic unitarity; covered source §§1–3,8. |
| `ConcreteSemantics.lean:21–22,296–297` | Namespaces `QuantumBlockEncoding`, `ConcreteSemantics`; no namespace-local variables, notation declarations, opens, sections, options or hidden hypotheses. |
| `ConcreteSemantics.lean:140,180` | Nested namespace `ComplexStatePreparationCertificate`; autoimplicit `qubits : Nat` in its three declarations, not a positivity assumption. |
| `PrimitiveSemantics.lean:1–3` | Direct imports: `QuantumBlockEncoding.PrimitiveCircuit`, `QuantumBlockEncoding.Robin.Hadamard8Verified`, `Mathlib.Tactic`. The Robin import supplies rotation, permutation and reindexing providers transitively. |
| `PrimitiveSemantics.lean:5–10` | Half-angle convention explanation: source §4. Reference to software conventions is not used here as an external citation or an executable interoperability test. |
| `PrimitiveSemantics.lean:12,493` | Namespace `QuantumBlockEncoding`; no local variable block, section, local notation, option or hidden premise. |
| `PrimitiveSemantics.lean:14–15` | `open QuantumBlockEncoding.Robin.ComplexLCU`; `open scoped Kronecker`. Necessary for rotation/permutation providers and tensor lift. Covered §§4–5. |
| `ReversibleClassical.lean:1–2` | Direct imports: `QuantumBlockEncoding.PrimitiveRefinement`, `Mathlib.Tactic`. The refinement import transitively imports the whole primitive semantics. |
| `ReversibleClassical.lean:4–10` | Proof IR versus final `{X,RY,RZ,CX}` boundary: source §§7–8. No compiler theorem is present here. |
| `ReversibleClassical.lean:12,83` | Namespace `QuantumBlockEncoding`; no opens, local notation, options, local variables or sections. |
| All target files | No explicit `private` declaration, `instance` declaration, `axiom`, `sorry` or `admit` appears. Standard imported instances and tactic infrastructure are ambient dependencies, not newly audited declarations. `[simp]` attributes only control simplification and do not strengthen statements. `noncomputable` marks exact-real/mathlib constructions, not an efficiency theorem. |
| Generated elaborator declarations | Structure constructors/projections and inductive constructors are explicitly accounted below. Automatically generated recursors, no-confusion/injectivity facts and equation-compiler auxiliaries have no separately authored source claim; disposition EXCLUDED (compiler infrastructure, not an omitted mathematical definition). No build/elaborator inventory was produced in this source-only task. |

## Concrete finite action: every authored declaration

Every line number refers to the frozen full actual file, not a selected excerpt. Binder details in this table supplement the shared ambient above; absent extra premises, the row is unconditional on the typed arguments.

| Line | Declaration | Full mathematical carrier/input and premise disposition | Source coverage / argument |
| --- | --- | --- | --- |
| 25 | `FiniteMatrix` | `rows cols : Nat`, `α : Type u`; TYPING. | §1: finite function-valued matrix, Mathlib alias. |
| 29 | `StateVector` | `dimension : Nat`, `α : Type u`; TYPING. | §1: finite function-valued column. |
| 33 | `basisKet` | `dimension`, `α`, `[Zero α] [One α]`, `index : Fin dimension`; TYPING, no dimension positivity binder. | §2: delta column on every row. |
| 40 | `basisKet_apply` | Same scalar data, `index row : Fin dimension`; no extra SOURCE premise. | §2 delta formula; equality and inequality cases. |
| 50 | `zeroKet` | `qubits : Nat`, scalar zero/one instances; TYPING. | §§1–2: basis index zero in dimension `2^qubits`, including zero qubits. |
| 55 | `applyVec` | Arbitrary `rows cols`, `α`, `[NonUnitalNonAssocSemiring α]`, operator and vector; TYPING algebraic setting. | §1 finite sum action. |
| 64 | `ComplexUnitaryGate` | `qubits`; record of matrix and standard unitarity evidence. | §§1–2 explicit unitary gate record. |
| 70 | `applyVec_basisKet` | Arbitrary `rows cols`, `α`, `[NonAssocSemiring α]`, operator and `index : Fin cols`; TYPING. | §2 finite sum selects column. |
| 79 | `applyVec_twoBasisSuperposition` | Complex arbitrary rectangular operator, `a b : ℂ`, `left right : Fin cols`; no distinctness/normalization hypothesis. | §2 two-term linearity, coincident indices allowed. |
| 93 | `applyVec_twoBasisSuperposition_apply` | Previous inputs plus `row : Fin rows`; TYPING. | §2 coordinate version of same equality. |
| 103 | `applyVec_zeroKet` | Arbitrary `α`, `[NonAssocSemiring α]`, `qubits`, square register-sized operator; TYPING. | §2 column-zero identity. |
| 114 | `firstColumnMatches_iff_applyVec_zeroKet` | Same algebraic setting, operator, target record. Its target proposition is data, not a premise proved here. | §2 equivalence of all first-column entries and vector action; function extensionality. |
| 133 | `ComplexStatePreparationCertificate` | `qubits`, target, unitary-gate record, target-normalization evidence and preparation equation. Both evidence fields are SOURCE requirements of this record, not global assumptions. | §2 certificate and exact limits of normalization field. |
| 143 | `ComplexStatePreparationCertificate.candidate` | Certificate; arbitrary `Circuit`, `LayeredCircuit`, `Resource`, `auxiliaryQubits : Nat := 0`. | §2 repackaging, no circuit/schedule/resource linkage theorem. |
| 162 | `ComplexStatePreparationCertificate.verified` | Same supplied data. Uses certificate evidence internally. | §2 verified packaging, including first-column/action bridge. |
| 175 | `ComplexStatePreparationCertificate.preparesVector` | Certificate alone. | §2 read stored preparation equation, not a new construction. |
| 183 | `ProductRegisterMatrix` | Arbitrary `signalDim rows cols`, scalar `α`; TYPING. | §3 rectangular product indices. |
| 190 | `flatToProductRegister` | Arbitrary same dimensions/carrier and flat matrix; TYPING. | §3 high-signal/low-system formula. Bounds come from finite indices, not new positivity binders. |
| 201 | `productRegisterBlockProjection` | Product matrix and `signalIndex : Fin signalDim`; TYPING. | §3 restriction to identical selected input/output branch. |
| 210 | `productRegisterBlockProjection_flatToProductRegister` | Arbitrary dimensions/carrier, `[OfNat α 0]`, flat matrix and selected index. Zero numeral is an inherited API/TYPING requirement unused in entry formula. | §3 equality of the two projections by formula substitution. |
| 220 | `productIndex_val_eq_signalSystemBlockRowIndex` | `signalDim systemDim`, selected signal and system finite indices; TYPING. | §3 embedding value is `a*d+i`. |
| 232 | `signalSystemBlockProjection_eq_cleanBlockProduct` | Arbitrary square product dimensions, rational operator and signal index. | §3 rational pointwise equality; no orthogonality premise. |
| 249 | `cleanBasisActionAmplitude` | Arbitrary dimensions/carrier with `[NonAssocSemiring α]`, square product operator, selected branch, output/input indices. | §3 definition by basis input and clean output coordinate. |
| 259 | `cleanBasisActionAmplitude_eq_signalSystemBlockProjection` | Same typed arguments, no unitarity premise. | §3 basis-column identity and equal flattening. |
| 277 | `pointwiseProjection_iff_cleanBasisAction` | Same algebraic setting and operator/branch plus arbitrary target square matrix. | §3 pointwise block/action iff, all input/output coordinates; both directions substitute amplitude identity. |

### Concrete record members (including their generated field projections)

| Owner/member | Complete field meaning / disposition |
| --- | --- |
| `ComplexUnitaryGate.mk`, `.matrix` | Constructor; matrix of size `2^n × 2^n` over `ℂ`; §2. |
| `ComplexUnitaryGate.unitary` | SOURCE evidence `matrix ∈ Matrix.unitaryGroup (Fin (2^n)) ℂ`; expands to actual complex unitarity, not an arbitrary Prop. §§1–2. |
| `ComplexStatePreparationCertificate.mk`, `.target` | Constructor; `StatePreparationTarget ℂ n`, expanded below; §2. |
| `ComplexStatePreparationCertificate.gate` | The preceding concrete gate record, including actual unitarity. §2. |
| `ComplexStatePreparationCertificate.normalizationProof` | SOURCE evidence of the target's arbitrary stored `normalization : Prop`. No fixed analytic norm is inferred. §2. |
| `ComplexStatePreparationCertificate.preparationProof` | SOURCE evidence `applyVec gate.matrix (zeroKet n) = target.amplitudes`. §2. |

Expanded imported bundles actually used: `StatePreparationTarget` contains amplitudes, arbitrary normalization proposition, source string (default empty); `StatePreparationCandidate` contains that target, a function-valued unitary matrix, arbitrary presentation circuit, schedule (default empty), resource, auxiliary qubits (default zero), and arbitrary `isUnitary : Prop`; `VerifiedStatePreparation` contains a candidate and evidence of its normalization proposition, its unitarity proposition and `FirstColumnMatches`. The adapter instantiates `isUnitary` with standard complex matrix unitarity and discharges these fields from the certificate. It does not constrain the supplied circuit/schedule/resource. These expansions are necessary SOURCE semantics of the certificate interface; imported definitions are context, not newly included whole-module audit scope.

## Primitive semantics: every authored declaration

Unless separately stated, all angles in these rows are arbitrary `Real`; there are no bound, nonzero or positivity assumptions on them. Every implicit `qubits` is `Nat`, every wire belongs to `Fin qubits`, every assignment is `Fin qubits → Fin 2`, and every full-register matrix is a complex matrix on those assignments. These TYPING data are shared, not omitted premises.

| Line | Declaration | Inputs / actual logical prerequisites | Source coverage / argument |
| --- | --- | --- | --- |
| 18 | `standardRyMatrix` | Real angle; literal definition. | §4 `R(θ/2)`. |
| 22 | `standardRyMatrix_zero` | No arguments or premises. | §4 zero-angle identity, scalar sin/cos at zero. |
| 28 | `standardRyMatrix_add` | Real `left right`; no assumptions. | §4 physical-angle addition, product order right then left. |
| 39 | `star_complex_cos_ofReal` | Real theta. | §4 scalar conjugation fixes cosine of embedded real. |
| 43 | `conj_complex_cos_ofReal` | Real theta. | §4 same identity using conjugation endomorphism notation. |
| 48 | `star_complex_sin_ofReal` | Real theta. | §4 scalar conjugation fixes sine of embedded real. |
| 52 | `conj_complex_sin_ofReal` | Real theta. | §4 same sine identity in endomorphism notation. |
| 57 | `complex_ofReal_div_two` | Real theta. | §4 embedding commutes with division by two. |
| 61 | `conj_complex_cos_ofReal_div_two` | Real theta. | §4 half-argument conjugation identity from preceding cast equality. |
| 66 | `conj_complex_sin_ofReal_div_two` | Real theta. | §4 corresponding sine identity. |
| 71 | `standardRyMatrix_neg` | Real theta. | §4 negative-angle dagger, transpose plus sine sign. |
| 80 | `xMatrix` | No inputs, two-dimensional complex matrix. | §4 explicit Pauli flip. |
| 83 | `xMatrix_conjugates_standardRy` | Real theta. | §4 exact `X Y(θ) X = Y(-θ)`. |
| 91 | `standardRyMatrix_unitary` | Real theta, no coefficient domain premise. | §4 trig normalization. |
| 96 | `standardRyMatrix_two_arccos_eq_amplitudeRotation` | Real coefficient, `_lower : -1 ≤ coefficient`, `_upper : coefficient ≤ 1`; SOURCE interval, retained though unused in this equality proof. | §4 half-angle cancellation; bounds not represented as proof necessities for this equality. |
| 106 | `standardRyMatrix_pi_div_two_eq_warmRobinUniformBitPrepare` | No arguments/premises. | §4 full signed uniform preparation matrix; not Hadamard. |
| 116 | `PrimitiveBasis` | Natural qubits. | §5 named-wire binary functions; no endian integer identification. |
| 118 | `flipBit` | `bit : Fin 2`; literal total function. | §5 all two bit cases. |
| 120 | `flipBit_flipBit` | `bit : Fin 2`. | §5 involution by the two cases. |
| 123 | `xBasisAction` | Target, assignment. | §5 update only named target. |
| 127 | `xBasisAction_involutive` | Target; no extra premise. | §5 double flip; target/non-target coordinates. |
| 136 | `xBasisEquiv` | Target. | §5 equivalence with same action as inverse. |
| 143 | `cxBasisAction` | Control, target, assignment; no distinctness binder. | §5 raw total conditional action, including coincident wires. |
| 147 | `cxBasisAction_involutive` | Control, target, `distinct : control ≠ target` SOURCE. | §5 preservation of control; active/inactive cases. |
| 158 | `cxBasisEquiv` | Control, target, same SOURCE distinctness. | §5 self-inverse equivalence. |
| 166 | `cxBasisEquiv_apply` | Control, target, SOURCE distinctness and assignment. | §5 equivalence agrees with raw action. |
| 172 | `OtherPrimitiveWires` | Target; subtype `{wire // wire ≠ target}`. Subtype exclusion is TYPING, not separate circuit hypothesis. | §5 non-target wire set. |
| 175 | `splitPrimitiveWire` | Target. | §5 split/reconstruct bijection, complete target and other coordinate cases. |
| 194 | `splitPrimitiveWire_other_apply` | Target, assignment, non-target subtype wire. | §5 restriction at an explicitly non-target wire. |
| 200 | `liftPrimitiveOneQubit` | Target, arbitrary complex `2×2` gate. | §5 transport `gate ⊗ I` along split bijection. |
| 208 | `liftPrimitiveOneQubit_apply` | Previous inputs plus full-register row and column assignments. | §5 equality of other-wire restrictions decides zero versus gate entry. |
| 226 | `liftPrimitiveOneQubit_unitary` | Target, arbitrary gate, `unitary : gate ∈ Matrix.unitaryGroup (Fin 2) ℂ` SOURCE. | §5 conditional tensor/reindex unitarity, not automatic for input matrix. |
| 238 | `standardRzMatrix` | Real theta. | §4 exact diagonal phases with negative phase at bit zero. |
| 247 | `standardRzMatrix_unitary` | Real theta. | §4 both diagonal conjugate norms one; off-diagonal zero. |
| 269 | `standardRzMatrix_neg` | Real theta. | §4 dagger/negation, both signs and off-diagonal cases. |
| 292 | `star_equivPermutationMatrix` | Arbitrary `index : Type*`, `[Fintype index] [DecidableEq index]`, `equiv : index ≃ index`; TYPING. | §5 permutation adjoint is inverse permutation. |
| 312 | `star_liftPrimitiveOneQubit` | Target, arbitrary gate; no unitarity premise. | §5 entrywise dagger/lift identity, other-wire equal/unequal cases. |
| 329 | `evalPrimitiveGate` | Typed gate instruction, including constructor-held distinctness for CX and exact angle expression for rotations. | §5 all four instruction cases. |
| 337 | `evalPrimitiveGate_unitary` | Any typed gate. Constructor evidence is expanded below. | §5 permutation or lifted rotation unitarity; all four cases. |
| 348 | `xBasisEquiv_symm` | Target. | §5 same equivalence as its inverse. |
| 352 | `cxBasisEquiv_symm` | Control/target with SOURCE distinctness. | §5 self-inverse controlled permutation. |
| 358 | `evalPrimitiveGate_dagger` | Any typed gate. | §5 all four cases, angle negation for rotations. |
| 380 | `evalPrimitiveCircuit` | Arbitrary typed list. | §6 identity or tail-matrix times head-matrix. |
| 385 | `evalPrimitiveCircuit_unitary` | Arbitrary typed list; no unitary binder. | §6 induction using derived gate unitarity. |
| 395 | `evalPrimitiveCircuit_append` | Arbitrary left/right typed lists. | §6 reverse multiplication order under chronological concatenation. |
| 406 | `evalPrimitiveCircuit_dagger` | Arbitrary typed list. | §6 reverse-list map dagger; induction and append identity. |
| 419 | `evalGlobalPhase` | Exact angle object. | §6 `exp(i·eval(angle))`. |
| 422 | `evalGlobalPhase_unitary` | Exact angle object. | §6 scalar unitary predicate; both conjugate products one. |
| 436 | `evalGlobalPhase_neg` | Exact angle object. | §6 negative phase is conjugate. |
| 445 | `evalPrimitiveProgram` | Program containing list and phase angle. | §6 scalar multiplication of circuit matrix, no phase quotient. |
| 450 | `evalPrimitiveProgram_identity` | Natural qubits. | §6 empty list/zero phase identity. |
| 455 | `evalPrimitiveProgram_seq` | Left/right programs on same wire count. | §6 add phases, concatenate instructions, multiply later program on left. |
| 469 | `evalPrimitiveProgram_unitary` | Any program; no unitary or bounded-angle hypothesis. | §6 scalar unitary times circuit unitary. |
| 476 | `evalPrimitiveProgram_dagger` | Any program. | §6 reverse/dagger list and negative phase; exact matrix adjoint. |
| 488 | `PrimitiveRefinement` | Natural qubits; circuit, target full-register complex matrix, exact equality evidence. | §6 literal matrix equality, not phase equivalence. |

`PrimitiveRefinement.mk`, `.circuit`, `.target`, `.exact` are its constructor and all field projections. The `exact` field is SOURCE evidence `evalPrimitiveCircuit circuit = target`; it does not contain a program phase, implementation cost or norm approximation. All fields appear in source §6.

### Imported primitive interfaces expanded, not credited as new audited targets

`ExactAngle` has eight constructor forms: `rational(q)`, `piRational(q)`, `twiceArccosRational(q, |(q:Real)| ≤ 1)`, `twiceArccosSqrtRational(q, 0 ≤ (q:Real) ∧ (q:Real) ≤ 1)`, `real(value)`, `add(left,right)`, `neg(value)`, `scale(q,value)`. Rational/real values and expressions are TYPING; both domain proofs are SOURCE restrictions on that syntax. Their evaluation formulas are stated in §4. Addition and negation interpretation are dependencies of program and gate adjoint statements, not new public premises. The provider additionally defines subtraction and half-sum/half-difference and counts/resources; these are not called in the target semantics and are not promoted into new source claims.

`PrimitiveGate` has four forms only: `x(target)`, `ry(target,angle)`, `rz(target,angle)`, `cx(control,target,distinct)`. `distinct : control ≠ target` is SOURCE valid-wire evidence, not pure finite-index typing. `PrimitiveCircuit` is a list of these. `PrimitiveProgram` has `.circuit` and `.globalPhase`; identity is empty circuit/rational zero, sequence appends circuits and adds phase expressions, dagger reverses/maps gate dagger and negates phase. Gate dagger leaves X/CX and negates RY/RZ angles. These are §§5–6 ambient definitions. Imported resource counts are not hypotheses of any target theorem.

Rotation/permutation provider formulas read at their actual source regions: `realOrthogonalRotation`, `realRotation`, `amplitudeRotation`, `realRotation_unitary`, `reindex_unitary`, `equivPermutationMatrix`, `equivPermutationMatrix_unitary`; the uniform preparation provider is the signed real rotation with cosine=sine=`sqrt 2 / 2`. Their use is dependency evidence, not external reference admission. Relevant operator symbols and tensor reindexing have their concrete mathematical meaning in §§4–5.

## Reversible classical proof IR: every declaration and constructor

| Line | Declaration/member | Inputs and logical prerequisites | Source coverage / argument |
| --- | --- | --- | --- |
| 14 | `ReversibleGate` | Natural qubits; inductive typed language with the following three forms. | §7 explicit proof-only instruction set. |
| 15 | `ReversibleGate.x` | `target : Fin qubits`. | §§5,7 single flip. |
| 16 | `ReversibleGate.cx` | Control/target finite wires, SOURCE `control ≠ target`. | §§5,7 controlled flip. |
| 17–20 | `ReversibleGate.ccx` | Three finite wires; SOURCE `control0 ≠ control1`, `control0 ≠ target`, `control1 ≠ target`, all retained at syntax level. | §7 triple distinctness; no final-ISA claim. |
| 22 | `ReversibleProgram` | Natural qubits; list alias. | §7 chronological proof program. |
| 24 | `ccxBasisAction` | Three finite wires and basis assignment; no distinctness premises. | §7 raw total double-one conditional update. |
| 30 | `ccxBasisAction_involutive` | Three wires, SOURCE `control0 ≠ target`, `control1 ≠ target`; no control–control inequality. | §7 active/inactive proof, preserving both controls. |
| 52 | `ccxBasisEquiv` | Three wires, same two SOURCE inequalities. | §7 self-inverse equivalence. |
| 63 | `ccxBasisEquiv_apply` | Same two SOURCE inequalities plus assignment. | §7 equivalence evaluates by raw action. |
| 71 | `evalReversibleGate` | Any typed reversible instruction. | §7 all three constructor cases. CCX pattern discards only the control–control proof. |
| 78 | `evalReversibleProgram` | Any typed instruction list. | §7 identity equivalence or head-equivalence followed by tail-equivalence; order explicit. |

There is no separately declared reversible unitarity, matrix denotation, adjoint compiler, CCX decomposition or resource theorem in this file. Reversibility of the evaluation result is packaged by its equivalence-valued type. The ambient `PrimitiveRefinement` import does not itself supply a CCX-to-final-ISA bridge. All zero-/one-/two-wire constraints are stated in §§6–7 without introducing global lower bounds on wire count.

## Mathematical topology and exclusions

Source §§1–2 give carriers → delta column → basis action → first-column/action equivalence → certificate repackaging. Section 3 uses the same column identity AND explicit flattening to give clean-basis amplitude = projected entry → pointwise iff. Section 4 gives literal rotation matrices → scalar/trig identities → unitarity, inverse, sign and angle bridges. Section 5 combines named-wire bijections AND tensor identity with one-qubit unitarity, and uses basis equivalences for permutation matrices; the four instruction cases are alternatives under their common evaluator, not four jointly required operands. Section 6 combines instruction denotation with chronological list recursion, then circuit unitarity AND scalar phase unitarity to derive program unitarity and exact adjoint. Section 7 independently composes basis equivalences for proof execution. This topology reconstructs the local formulas, not an elaborated Lean proof-term dependency graph or a novelty graph.

No displayed formula, declaration, constructor, substantive comment or ambient restriction in the three files was excluded from the mathematical contract merely because it was private, small, or inconvenient. Only generated compiler machinery is excluded as above. Comments advertising linear extension of a basis statement are explanatory mathematical consequences, not a claim that the target declares a separate arbitrary-input theorem. The source states the finite basis bridge and does not invent a new normalizer, failure-branch theorem, resource bound or CCX compiler. Section 8 preserves those boundaries.

## Author handoff state

Objective: recover the actual semantics of three whole historical modules for later fresh source-first reading. Delta: one self-contained mathematical contract, declaration-to-source coverage and exact byte/context bindings. Effect on root frontier: author evidence only; no semantic review or new theorem closure is claimed.

Failure class: NONE for source recovery. A read-only `git status` query reported that the supplied repository mirror was not a work tree; this did not block raw source/hash reading and is not mathematical failure evidence. No Git writes, cache writes, build or Lean invocation occurred. No process-memory item was used as mathematical authority. No failed proof fragments were generated; salvage not applicable. Direction fingerprint: whole-module retrospective finite-action/primitive/IR source author, with explicit phase/order/normalization/empty-carrier boundaries. No agents were spawned. Default verified route/comparator, independent topology review, decoder/reviewer acceptance, Proof Seal, purification and Exposition Seal: not performed; pending parent-coordinated distinct readers. The historical formalizer identity remains UNKNOWN.
