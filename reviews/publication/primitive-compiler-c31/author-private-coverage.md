# C31 private author coverage — whole source, not compiler inventory

Author: parent /root. Historical formalizer UNKNOWN. All three complete production targets were actually read before this freeze. This is retrospective local recovery, not independent evidence or a pre-proof seal.

The following exact headers and source spans are lexical records; actual elaborated signatures, generated declarations and axiom dependencies remain to be obtained by the independent formal-only decoder.

Logical wire-distinctness is a SOURCE guard. Dimensions, finite wire/index carriers and finite enumeration instances are TYPING. Matrix equalities in proof-carrying internal program records are explicitly dependency evidence, never an invented premise of a final scientific state-preparation claim. ExactAngle evaluation/half-angle/global-phase conventions are SOURCE semantics, not merely typing.

## QuantumBlockEncoding.hadamardMatrix

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 15–18; public def; natural region S2–S4.

```lean
noncomputable def hadamardMatrix : _root_.Matrix (Fin 2) (Fin 2) ℂ
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.phaseMatrix

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 19–23; public def; natural region S2–S4.

```lean
noncomputable def phaseMatrix (theta : Real) :
    _root_.Matrix (Fin 2) (Fin 2) ℂ
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.hadamardMatrix_apply

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 24–40; public theorem; natural region S2–S4.

```lean
theorem hadamardMatrix_apply (row column : Fin 2) :
    hadamardMatrix row column =
      let scale : ℂ
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.phaseMatrix_apply

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 41–75; public theorem; natural region S2–S4.

```lean
theorem phaseMatrix_apply (theta : Real) (row column : Fin 2) :
    phaseMatrix theta row column =
      if row = column then
        if row = 0 then 1 else Complex.exp ((theta : ℂ) * Complex.I)
      else 0
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveHProgram

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 76–81; public def; natural region S2–S4.

```lean
def primitiveHProgram {qubits : Nat} (target : Fin qubits) :
    PrimitiveProgram qubits
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveTProgram

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 82–86; public def; natural region S2–S4.

```lean
def primitiveTProgram {qubits : Nat} (target : Fin qubits) :
    PrimitiveProgram qubits
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveTdgProgram

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 87–91; public def; natural region S2–S4.

```lean
def primitiveTdgProgram {qubits : Nat} (target : Fin qubits) :
    PrimitiveProgram qubits
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.evalGlobalPhase_pi_div_two

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 92–97; public theorem; natural region S2–S4.

```lean
theorem evalGlobalPhase_pi_div_two :
    evalGlobalPhase (.piRational (1 / 2)) = Complex.I
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.liftPrimitiveOneQubit_mul

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 98–107; public theorem; natural region S2–S4.

```lean
theorem liftPrimitiveOneQubit_mul {qubits : Nat} (target : Fin qubits)
    (left right : _root_.Matrix (Fin 2) (Fin 2) ℂ) :
    liftPrimitiveOneQubit target (left * right) =
      liftPrimitiveOneQubit target left * liftPrimitiveOneQubit target right
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.smul_liftPrimitiveOneQubit

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 108–116; public theorem; natural region S2–S4.

```lean
theorem smul_liftPrimitiveOneQubit {qubits : Nat} (target : Fin qubits)
    (scalar : ℂ) (gate : _root_.Matrix (Fin 2) (Fin 2) ℂ) :
    scalar • liftPrimitiveOneQubit target gate =
      liftPrimitiveOneQubit target (scalar • gate)
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveHProgram_eval

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 117–131; public theorem; natural region S2–S4.

```lean
theorem primitiveHProgram_eval {qubits : Nat} (target : Fin qubits) :
    evalPrimitiveProgram (primitiveHProgram target) =
      liftPrimitiveOneQubit target hadamardMatrix
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveTProgram_eval

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 132–151; public theorem; natural region S2–S4.

```lean
theorem primitiveTProgram_eval {qubits : Nat} (target : Fin qubits) :
    evalPrimitiveProgram (primitiveTProgram target) =
      liftPrimitiveOneQubit target (phaseMatrix (Real.pi / 4))
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveTdgProgram_eval

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 152–173; public theorem; natural region S2–S4.

```lean
theorem primitiveTdgProgram_eval {qubits : Nat} (target : Fin qubits) :
    evalPrimitiveProgram (primitiveTdgProgram target) =
      liftPrimitiveOneQubit target (phaseMatrix (-Real.pi / 4))
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.phasePermutationMatrix

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 174–179; public def; natural region S2–S4.

```lean
noncomputable def phasePermutationMatrix {index : Type*}
    [Fintype index] [DecidableEq index]
    (phase : index → ℂ) (permutation : index ≃ index) :
    _root_.Matrix index index ℂ
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.phasePermutationMatrix_mul

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 180–198; public theorem; natural region S2–S4.

```lean
theorem phasePermutationMatrix_mul {index : Type*}
    [Fintype index] [DecidableEq index]
    (leftPhase rightPhase : index → ℂ)
    (leftPerm rightPerm : index ≃ index) :
    phasePermutationMatrix rightPhase rightPerm *
        phasePermutationMatrix leftPhase leftPerm =
      phasePermutationMatrix
        (fun state => leftPhase state * rightPhase (leftPerm state))
        (leftPerm.trans rightPerm)
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.evalPrimitiveCx_eq_phasePermutationMatrix

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 199–206; public theorem; natural region S2–S4.

```lean
theorem evalPrimitiveCx_eq_phasePermutationMatrix {qubits : Nat}
    (control target : Fin qubits) (distinct : control ≠ target) :
    evalPrimitiveGate (.cx control target distinct) =
      phasePermutationMatrix (fun _ => 1)
        (cxBasisEquiv control target distinct)
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.liftPhaseMatrix_eq_phasePermutationMatrix

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 207–230; public theorem; natural region S2–S4.

```lean
theorem liftPhaseMatrix_eq_phasePermutationMatrix {qubits : Nat}
    (target : Fin qubits) (theta : Real) :
    liftPrimitiveOneQubit target (phaseMatrix theta) =
      phasePermutationMatrix
        (fun state => if state target = 0 then 1
          else Complex.exp ((theta : ℂ) * Complex.I))
        (Equiv.refl _)
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveCxProgram

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 231–235; public def; natural region S2–S4.

```lean
def primitiveCxProgram {qubits : Nat} (control target : Fin qubits)
    (distinct : control ≠ target) : PrimitiveProgram qubits
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveCxProgram_eval

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 236–247; public theorem; natural region S2–S4.

```lean
theorem primitiveCxProgram_eval {qubits : Nat}
    (control target : Fin qubits) (distinct : control ≠ target) :
    evalPrimitiveProgram (primitiveCxProgram control target distinct) =
      phasePermutationMatrix (fun _ => 1)
        (cxBasisEquiv control target distinct)
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveTProgram_eval_monomial

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 248–256; public theorem; natural region S2–S4.

```lean
theorem primitiveTProgram_eval_monomial {qubits : Nat}
    (target : Fin qubits) :
    evalPrimitiveProgram (primitiveTProgram target) =
      phasePermutationMatrix
        (fun state => if state target = 0 then 1
          else Complex.exp (((Real.pi / 4 : Real) : ℂ) * Complex.I))
        (Equiv.refl _)
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveTdgProgram_eval_monomial

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 257–265; public theorem; natural region S2–S4.

```lean
theorem primitiveTdgProgram_eval_monomial {qubits : Nat}
    (target : Fin qubits) :
    evalPrimitiveProgram (primitiveTdgProgram target) =
      phasePermutationMatrix
        (fun state => if state target = 0 then 1
          else Complex.exp (((-Real.pi / 4 : Real) : ℂ) * Complex.I))
        (Equiv.refl _)
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.MonomialProgram

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 266–274; public structure; natural region S2–S4.

```lean
structure MonomialProgram (qubits : Nat)
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.MonomialProgram.seq

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 275–283; public def; natural region S2–S4.

```lean
def seq {qubits : Nat} (left right : MonomialProgram qubits) :
    MonomialProgram qubits
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.MonomialProgram.cx

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 284–290; public def; natural region S2–S4.

```lean
def cx {qubits : Nat} (control target : Fin qubits)
    (distinct : control ≠ target) : MonomialProgram qubits
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.MonomialProgram.t

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 291–297; public def; natural region S2–S4.

```lean
noncomputable def t {qubits : Nat} (target : Fin qubits) : MonomialProgram qubits
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.MonomialProgram.tdg

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 298–307; public def; natural region S2–S4.

```lean
noncomputable def tdg {qubits : Nat} (target : Fin qubits) : MonomialProgram qubits
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveCCXMiddle

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 308–328; public def; natural region S2–S4.

```lean
noncomputable def primitiveCCXMiddle {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_b : a ≠ b) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target) : MonomialProgram qubits
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveCCXProgram

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 329–337; public def; natural region S2–S4.

```lean
noncomputable def primitiveCCXProgram {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_b : a ≠ b) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target) : PrimitiveProgram qubits
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveCCXMiddle_permutation_eq_refl

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 338–362; public theorem; natural region S2–S4.

```lean
theorem primitiveCCXMiddle_permutation_eq_refl {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_b : a ≠ b) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target) :
    (primitiveCCXMiddle a b target a_ne_b a_ne_target b_ne_target).permutation =
      Equiv.refl _
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveCCXMiddle_phase_eq_ccz

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 363–384; public theorem; natural region S2–S4.

```lean
theorem primitiveCCXMiddle_phase_eq_ccz {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_b : a ≠ b) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target) (state : PrimitiveBasis qubits) :
    (primitiveCCXMiddle a b target a_ne_b a_ne_target b_ne_target).phase state =
      if state a = 1 ∧ state b = 1 ∧ state target = 1 then -1 else 1
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.cczMatrix

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 385–392; public def; natural region S2–S4.

```lean
noncomputable def cczMatrix {qubits : Nat}
    (a b target : Fin qubits) :
    _root_.Matrix (PrimitiveBasis qubits) (PrimitiveBasis qubits) ℂ
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveCCXMiddle_eval

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 393–407; public theorem; natural region S2–S4.

```lean
theorem primitiveCCXMiddle_eval {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_b : a ≠ b) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target) :
    evalPrimitiveProgram
        (primitiveCCXMiddle a b target a_ne_b a_ne_target b_ne_target).program =
      cczMatrix a b target
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.zMatrix

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 408–410; public def; natural region S2–S4.

```lean
def zMatrix : _root_.Matrix (Fin 2) (Fin 2) ℂ
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.hadamard_mul_hadamard

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 411–419; public theorem; natural region S2–S4.

```lean
theorem hadamard_mul_hadamard : hadamardMatrix * hadamardMatrix = 1
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.hadamard_mul_z_mul_hadamard

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 420–430; public theorem; natural region S2–S4.

```lean
theorem hadamard_mul_z_mul_hadamard :
    hadamardMatrix * zMatrix * hadamardMatrix = xMatrix
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.liftPrimitiveOneQubit_eq_blockDiagonal

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 431–440; public theorem; natural region S2–S4.

```lean
theorem liftPrimitiveOneQubit_eq_blockDiagonal {qubits : Nat}
    (target : Fin qubits) (gate : _root_.Matrix (Fin 2) (Fin 2) ℂ) :
    liftPrimitiveOneQubit target gate =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ (splitPrimitiveWire target).symm
        (_root_.Matrix.blockDiagonal
          (fun _ : OtherPrimitiveWires target → Fin 2 => gate))
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.cczTargetBlock

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 441–448; public def; natural region S2–S4.

```lean
noncomputable def cczTargetBlock {qubits : Nat}
    (a b target : Fin qubits) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target)
    (context : OtherPrimitiveWires target → Fin 2) :
    _root_.Matrix (Fin 2) (Fin 2) ℂ
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.cczMatrix_eq_blockDiagonal

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 449–504; public theorem; natural region S2–S4.

```lean
theorem cczMatrix_eq_blockDiagonal {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_target : a ≠ target) (b_ne_target : b ≠ target) :
    cczMatrix a b target =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ (splitPrimitiveWire target).symm
        (_root_.Matrix.blockDiagonal
          (cczTargetBlock a b target a_ne_target b_ne_target))
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.ccxTargetBlock

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 505–512; public def; natural region S2–S4.

```lean
noncomputable def ccxTargetBlock {qubits : Nat}
    (a b target : Fin qubits) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target)
    (context : OtherPrimitiveWires target → Fin 2) :
    _root_.Matrix (Fin 2) (Fin 2) ℂ
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.equivPermutationMatrix_ccx_eq_blockDiagonal

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 513–584; public theorem; natural region S2–S4.

```lean
theorem equivPermutationMatrix_ccx_eq_blockDiagonal {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_target : a ≠ target) (b_ne_target : b ≠ target) :
    Robin.ComplexLCU.equivPermutationMatrix
        (ccxBasisEquiv a b target a_ne_target b_ne_target) =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ (splitPrimitiveWire target).symm
        (_root_.Matrix.blockDiagonal
          (ccxTargetBlock a b target a_ne_target b_ne_target))
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.hadamard_conjugates_ccz

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 585–615; public theorem; natural region S2–S4.

```lean
theorem hadamard_conjugates_ccz {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_target : a ≠ target) (b_ne_target : b ≠ target) :
    liftPrimitiveOneQubit target hadamardMatrix *
        cczMatrix a b target *
        liftPrimitiveOneQubit target hadamardMatrix =
      Robin.ComplexLCU.equivPermutationMatrix
        (ccxBasisEquiv a b target a_ne_target b_ne_target)
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveCCXProgram_eval

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 616–628; public theorem; natural region S2–S4.

```lean
theorem primitiveCCXProgram_eval {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_b : a ≠ b) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target) :
    evalPrimitiveProgram
        (primitiveCCXProgram a b target a_ne_b a_ne_target b_ne_target) =
      Robin.ComplexLCU.equivPermutationMatrix
        (ccxBasisEquiv a b target a_ne_target b_ne_target)
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveCCXProgramRefinement

Module `QuantumBlockEncoding/PrimitiveMacros.lean`, source lines 629–638; public def; natural region S2–S4.

```lean
noncomputable def primitiveCCXProgramRefinement {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_b : a ≠ b) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target) : PrimitiveProgramRefinement qubits
```

Literal exact macro/monomial or block identity; expand MonomialProgram.exact as the evaluation equality. Phases are arbitrary only in the general monomial identity; final H/T/CCX matrices retain all exact global phases. Final network requires pairwise-distinct controls/target; intermediate block identities retain their actual weaker guards.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.prependControlBit

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 16–19; private def; natural region S5–S7.

```lean
private def prependControlBit {n : Nat} (bit : Fin 2)
    (tail : PrimitiveBasis n) : PrimitiveBasis (n + 1)
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.halfAddAngles

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 20–26; private def; natural region S5–S7.

```lean
private def halfAddAngles {n : Nat}
    (angles : PrimitiveBasis (n + 1) → ExactAngle) :
    PrimitiveBasis n → ExactAngle
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.halfSubAngles

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 27–33; private def; natural region S5–S7.

```lean
private def halfSubAngles {n : Nat}
    (angles : PrimitiveBasis (n + 1) → ExactAngle) :
    PrimitiveBasis n → ExactAngle
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.primitiveControlAssignment

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 34–41; public def; natural region S5–S7.

```lean
def primitiveControlAssignment {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (context : OtherPrimitiveWires target → Fin 2) : PrimitiveBasis controls
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.controlledRyBlockMatrix

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 42–50; public def; natural region S5–S7.

```lean
noncomputable def controlledRyBlockMatrix {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle) :
    _root_.Matrix (PrimitiveBasis qubits) (PrimitiveBasis qubits) ℂ
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.controlledRyBlockMatrix_apply

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 51–66; public theorem; natural region S5–S7.

```lean
@[simp] theorem controlledRyBlockMatrix_apply {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle)
    (row column : PrimitiveBasis qubits) :
    controlledRyBlockMatrix wires target distinct angles row column =
      if (splitPrimitiveWire target row).2 =
          (splitPrimitiveWire target column).2 then
        standardRyMatrix
          (angles (primitiveControlAssignment wires target distinct
            (splitPrimitiveWire target row).2)).eval
          (row target) (column target)
      else 0
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.kronecker_one_eq_blockDiagonal

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 67–77; private theorem; natural region S5–S7.

```lean
private theorem kronecker_one_eq_blockDiagonal
    {context : Type*} [Fintype context] [DecidableEq context]
    (gate : _root_.Matrix (Fin 2) (Fin 2) ℂ) :
    gate ⊗ₖ (1 : _root_.Matrix context context ℂ) =
      _root_.Matrix.blockDiagonal (fun _ : context => gate)
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.evalPrimitiveRy_eq_controlledRyBlockMatrix_zero

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 78–91; private theorem; natural region S5–S7.

```lean
private theorem evalPrimitiveRy_eq_controlledRyBlockMatrix_zero
    {qubits : Nat} (target : Fin qubits) (angle : ExactAngle) :
    evalPrimitiveGate (.ry target angle) =
      controlledRyBlockMatrix (fun index : Fin 0 => Fin.elim0 index)
        target (fun index => Fin.elim0 index) (fun _ => angle)
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.controlledXBlock

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 92–96; private def; natural region S5–S7.

```lean
private def controlledXBlock {qubits : Nat} (control target : Fin qubits)
    (distinct : control ≠ target) (context : OtherPrimitiveWires target → Fin 2) :
    _root_.Matrix (Fin 2) (Fin 2) ℂ
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.xMatrix_flipBit

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 97–100; private theorem; natural region S5–S7.

```lean
private theorem xMatrix_flipBit (bit : Fin 2) :
    xMatrix (flipBit bit) bit = 1
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.evalPrimitiveCx_eq_controlledXBlock

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 101–192; private theorem; natural region S5–S7.

```lean
private theorem evalPrimitiveCx_eq_controlledXBlock
    {qubits : Nat} (control target : Fin qubits)
    (distinct : control ≠ target) :
    evalPrimitiveGate (.cx control target distinct) =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ (splitPrimitiveWire target).symm
        (_root_.Matrix.blockDiagonal
          (controlledXBlock control target distinct))
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.compileUniformlyControlledRy

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 193–217; public def; natural region S5–S7.

```lean
def compileUniformlyControlledRy {qubits : Nat} :
    (controls : Nat) →
    (wires : Fin controls → Fin qubits) →
    (target : Fin qubits) →
    (∀ control, wires control ≠ target) →
    (PrimitiveBasis controls → ExactAngle) →
    PrimitiveCircuit qubits
  | 0, _, target, _, angles =>
      [.ry target (angles fun index => Fin.elim0 index)]
  | controls + 1, wires, target, distinct, angles =>
      let head
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.uniformlyControlledRyMatrix

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 218–240; public def; natural region S5–S7.

```lean
noncomputable def uniformlyControlledRyMatrix {qubits : Nat} :
    (controls : Nat) →
    (wires : Fin controls → Fin qubits) →
    (target : Fin qubits) →
    (∀ control, wires control ≠ target) →
    (PrimitiveBasis controls → ExactAngle) →
    _root_.Matrix (PrimitiveBasis qubits) (PrimitiveBasis qubits) ℂ
  | 0, _, target, _, angles =>
      evalPrimitiveGate (.ry target (angles fun index => Fin.elim0 index))
  | controls + 1, wires, target, distinct, angles =>
      let head
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.compileUniformlyControlledRy_eval

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 241–259; public theorem; natural region S5–S7.

```lean
theorem compileUniformlyControlledRy_eval {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle) :
    evalPrimitiveCircuit
        (compileUniformlyControlledRy controls wires target distinct angles) =
      uniformlyControlledRyMatrix controls wires target distinct angles
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.compileUniformlyControlledRy_eval_controlledRyBlockMatrix

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 260–370; public theorem; natural region S5–S7.

```lean
theorem compileUniformlyControlledRy_eval_controlledRyBlockMatrix
    {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle) :
    evalPrimitiveCircuit
        (compileUniformlyControlledRy controls wires target distinct angles) =
      controlledRyBlockMatrix wires target distinct angles
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.compileUniformlyControlledRy_ryCount

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 371–386; public theorem; natural region S5–S7.

```lean
theorem compileUniformlyControlledRy_ryCount {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle) :
    (compileUniformlyControlledRy controls wires target distinct angles).ryCount =
      2 ^ controls
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.compileUniformlyControlledRy_cxCount

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 387–403; public theorem; natural region S5–S7.

```lean
theorem compileUniformlyControlledRy_cxCount {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle) :
    (compileUniformlyControlledRy controls wires target distinct angles).cxCount =
      2 * (2 ^ controls - 1)
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.compileUniformlyControlledRy_oracleCalls_eq_zero

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 404–411; public theorem; natural region S5–S7.

```lean
theorem compileUniformlyControlledRy_oracleCalls_eq_zero
    {qubits controls : Nat} (wires : Fin controls → Fin qubits)
    (target : Fin qubits) (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle) :
    (compileUniformlyControlledRy controls wires target distinct angles).resource.oracleCalls = 0
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.compileUniformlyControlledRy_five_control_counts

Module `QuantumBlockEncoding/UniformlyControlledRy.lean`, source lines 412–422; public theorem; natural region S5–S7.

```lean
theorem compileUniformlyControlledRy_five_control_counts
    {qubits : Nat} (wires : Fin 5 → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis 5 → ExactAngle) :
    (compileUniformlyControlledRy 5 wires target distinct angles).ryCount = 32 ∧
    (compileUniformlyControlledRy 5 wires target distinct angles).cxCount = 62
```

Literal target/context block or recursive angle compiler/count; control-target inequality is SOURCE, control-control injectivity is NOT assumed. HalfAdd/HalfSub evaluate to actual half-sum/half-difference. Count conclusions are exponential exact-real primitive counts, not preprocessing or finite-bit cost.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ControlWires

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 22–25; public def; natural region S8–S9.

```lean
def cubicN2ControlWires : Fin 2 → Fin 3
  | 0 => 0
  | _ => 1
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ControlWires_ne_signal

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 26–30; public theorem; natural region S8–S9.

```lean
theorem cubicN2ControlWires_ne_signal (wire : Fin 2) :
    cubicN2ControlWires wire ≠ (2 : Fin 3)
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ControlIndex

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 31–33; public def; natural region S8–S9.

```lean
def cubicN2ControlIndex (bits : PrimitiveBasis 2) : Fin 4
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2Amplitude_abs_le_one

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 34–43; public theorem; natural region S8–S9.

```lean
theorem cubicN2Amplitude_abs_le_one (bits : PrimitiveBasis 2) :
    |((CubicStatePreparation.cubicAmplitude 2
      (cubicN2ControlIndex bits) : Rat) : Real)| ≤ 1
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2Angle

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 44–49; public def; natural region S8–S9.

```lean
noncomputable def cubicN2Angle (bits : PrimitiveBasis 2) : ExactAngle
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveCircuit

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 50–53; public def; natural region S8–S9.

```lean
noncomputable def cubicN2PrimitiveCircuit : PrimitiveCircuit 3
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveProgram

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 54–58; public def; natural region S8–S9.

```lean
noncomputable def cubicN2PrimitiveProgram : PrimitiveProgram 3
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveCircuit_eval

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 59–65; public theorem; natural region S8–S9.

```lean
theorem cubicN2PrimitiveCircuit_eval :
    evalPrimitiveCircuit cubicN2PrimitiveCircuit =
      controlledRyBlockMatrix cubicN2ControlWires 2
        cubicN2ControlWires_ne_signal cubicN2Angle
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveProgram_eval

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 66–76; public theorem; natural region S8–S9.

```lean
theorem cubicN2PrimitiveProgram_eval :
    evalPrimitiveProgram cubicN2PrimitiveProgram =
      controlledRyBlockMatrix cubicN2ControlWires 2
        cubicN2ControlWires_ne_signal cubicN2Angle
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2EncodeBits

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 77–81; public def; natural region S8–S9.

```lean
def cubicN2EncodeBits (signal : Fin 2) (system : Fin 4) : PrimitiveBasis 3
  | 0 => ⟨system.val % 2, by omega⟩
  | 1 => ⟨(system.val / 2) % 2, by omega⟩
  | _ => signal
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2EncodeBits_signal

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 82–85; public theorem; natural region S8–S9.

```lean
@[simp] theorem cubicN2EncodeBits_signal (signal : Fin 2) (system : Fin 4) :
    cubicN2EncodeBits signal system 2 = signal
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ControlIndex_encode

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 86–94; public theorem; natural region S8–S9.

```lean
@[simp] theorem cubicN2ControlIndex_encode
    (signal : Fin 2) (system : Fin 4) :
    cubicN2ControlIndex
        (primitiveControlAssignment cubicN2ControlWires 2
          cubicN2ControlWires_ne_signal
          (splitPrimitiveWire 2 (cubicN2EncodeBits signal system)).2) =
      system
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2EncodeBits_context_eq_iff

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 95–102; public theorem; natural region S8–S9.

```lean
@[simp] theorem cubicN2EncodeBits_context_eq_iff
    (leftSignal rightSignal : Fin 2) (left right : Fin 4) :
    (splitPrimitiveWire 2 (cubicN2EncodeBits leftSignal left)).2 =
        (splitPrimitiveWire 2 (cubicN2EncodeBits rightSignal right)).2 ↔
      left = right
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveProgram_cleanEntry

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 103–144; public theorem; natural region S8–S9.

```lean
theorem cubicN2PrimitiveProgram_cleanEntry (row column : Fin 4) :
    evalPrimitiveProgram cubicN2PrimitiveProgram
        (cubicN2EncodeBits 0 row) (cubicN2EncodeBits 0 column) =
      ((cubicDiagonalOperator 2 row column : Rat) : ℂ)
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveFlatUnitary

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 145–149; public def; natural region S8–S9.

```lean
noncomputable def cubicN2PrimitiveFlatUnitary :
    _root_.Matrix (Fin (gridSize 3)) (Fin (gridSize 3)) ℂ
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveFlatUnitary_unitary

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 150–155; public theorem; natural region S8–S9.

```lean
theorem cubicN2PrimitiveFlatUnitary_unitary :
    cubicN2PrimitiveFlatUnitary ∈
      _root_.Matrix.unitaryGroup (Fin (gridSize 3)) ℂ
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveCleanIndex

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 156–158; public def; natural region S8–S9.

```lean
noncomputable def cubicN2PrimitiveCleanIndex (system : Fin 4) : Fin (gridSize 3)
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveFlatUnitary_cleanBlock

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 159–169; public theorem; natural region S8–S9.

```lean
theorem cubicN2PrimitiveFlatUnitary_cleanBlock (row column : Fin 4) :
    cubicN2PrimitiveFlatUnitary
        (cubicN2PrimitiveCleanIndex row)
        (cubicN2PrimitiveCleanIndex column) =
      ((cubicDiagonalOperator 2 row column : Rat) : ℂ)
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2ComplexTarget

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 170–176; public def; natural region S8–S9.

```lean
noncomputable def cubicN2ComplexTarget :
    QueryOperatorTarget ℂ (gridSize 2) (gridSize 2)
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitivePresentation

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 177–184; public def; natural region S8–S9.

```lean
noncomputable def cubicN2PrimitivePresentation : Circuit
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveResource

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 185–187; public def; natural region S8–S9.

```lean
noncomputable def cubicN2PrimitiveResource : Resource
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveOperatorCandidate

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 188–210; public def; natural region S8–S9.

```lean
noncomputable def cubicN2PrimitiveOperatorCandidate :
    OperatorBlockEncodingCandidate ℂ 2
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveVerifiedBlockEncoding

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 211–220; public def; natural region S8–S9.

```lean
noncomputable def cubicN2PrimitiveVerifiedBlockEncoding :
    VerifiedOperatorBlockEncoding ℂ 2
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2Primitive_oracleCalls_eq_zero

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 221–225; public theorem; natural region S8–S9.

```lean
theorem cubicN2Primitive_oracleCalls_eq_zero :
    cubicN2PrimitiveResource.oracleCalls = 0
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.

## QuantumBlockEncoding.CubicDiagonalOracle.cubicN2Primitive_resource_faithful

Module `QuantumBlockEncoding/CubicAmplitudePrimitive.lean`, source lines 226–230; public theorem; natural region S8–S9.

```lean
theorem cubicN2Primitive_resource_faithful :
    cubicN2PrimitiveResource = cubicN2PrimitiveCircuit.resource
```

Literal finite n=2 construction or exact encoding/candidate/refinement; no arbitrary-n generalization. Arccos bound is supplied by the finite rational dependency, not a new public premise. Candidate unitary/block Props are instantiated by the actual unitary membership/entry equation and the verified wrapper supplies their proofs. Presentation exact-angle strings are not numeric export data.

Definition classification: literal (or internal proof-carrying record constructor); no unique-choice or quotient claim. No altered production binder or target is proposed. Exact full source is retained by the input digest, including ambient namespace/options and all proof bodies.
