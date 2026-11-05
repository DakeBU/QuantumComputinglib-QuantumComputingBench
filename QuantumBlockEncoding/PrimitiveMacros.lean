import QuantumBlockEncoding.ReversibleClassical
import Mathlib.Tactic

/-!
# Exact primitive macro compiler

The public programs in this file contain only `X`, `RY`, `RZ`, and `CX`.
Logical names such as H, T, and CCX occur only in specifications and proofs.
-/

namespace QuantumBlockEncoding

open QuantumBlockEncoding.Robin.ComplexLCU

noncomputable def hadamardMatrix : _root_.Matrix (Fin 2) (Fin 2) ℂ :=
  Complex.I •
    (standardRyMatrix (Real.pi / 2) * standardRzMatrix Real.pi)

noncomputable def phaseMatrix (theta : Real) :
    _root_.Matrix (Fin 2) (Fin 2) ℂ :=
  Complex.exp (((theta / 2 : Real) : ℂ) * Complex.I) •
    standardRzMatrix theta

theorem hadamardMatrix_apply (row column : Fin 2) :
    hadamardMatrix row column =
      let scale : ℂ := (Real.sqrt 2 / 2 : Real)
      match row.val, column.val with
      | 0, 0 | 0, 1 | 1, 0 => scale
      | _, _ => -scale := by
  have half : (Real.pi / 2) / 2 = Real.pi / 4 := by ring
  fin_cases row <;> fin_cases column <;>
    simp [hadamardMatrix, standardRyMatrix, standardRzMatrix,
      realRotation, realOrthogonalRotation, _root_.Matrix.mul_apply,
      Fin.sum_univ_two, half, Real.cos_pi_div_four,
      Real.sin_pi_div_four, Real.cos_pi_div_two,
      Real.sin_pi_div_two] <;>
    rw [← mul_assoc,
      mul_comm Complex.I ((Real.sqrt 2 : ℂ) / 2),
      mul_assoc, Complex.I_mul_I] <;> ring

theorem phaseMatrix_apply (theta : Real) (row column : Fin 2) :
    phaseMatrix theta row column =
      if row = column then
        if row = 0 then 1 else Complex.exp ((theta : ℂ) * Complex.I)
      else 0 := by
  have expPos :
      Complex.exp (((theta / 2 : Real) : ℂ) * Complex.I) =
        Complex.cos ((theta / 2 : Real) : ℂ) +
          Complex.sin ((theta / 2 : Real) : ℂ) * Complex.I :=
    Complex.exp_mul_I (((theta / 2 : Real) : ℂ))
  have expNeg :
      Complex.exp (((-(theta / 2) : Real) : ℂ) * Complex.I) =
        Complex.cos ((theta / 2 : Real) : ℂ) -
          Complex.sin ((theta / 2 : Real) : ℂ) * Complex.I := by
    rw [Complex.exp_mul_I]
    rw [show (((-(theta / 2) : Real) : ℂ)) =
      -(((theta / 2 : Real) : ℂ)) by push_cast; rfl]
    rw [Complex.cos_neg, Complex.sin_neg]
    ring
  have castHalf : (((theta / 2 : Real) : ℂ)) = (theta : ℂ) / 2 := by
    push_cast
    rfl
  rw [castHalf] at expPos expNeg
  fin_cases row <;> fin_cases column <;> simp [phaseMatrix,
    standardRzMatrix]
  · rw [← expNeg, ← Complex.exp_add]
    congr 2
    push_cast
    ring
    simp
  · rw [← expPos, ← Complex.exp_add]
    congr 2
    push_cast
    ring

def primitiveHProgram {qubits : Nat} (target : Fin qubits) :
    PrimitiveProgram qubits where
  globalPhase := .piRational (1 / 2)
  circuit :=
    [.rz target (.piRational 1), .ry target (.piRational (1 / 2))]

def primitiveTProgram {qubits : Nat} (target : Fin qubits) :
    PrimitiveProgram qubits where
  globalPhase := .piRational (1 / 8)
  circuit := [.rz target (.piRational (1 / 4))]

def primitiveTdgProgram {qubits : Nat} (target : Fin qubits) :
    PrimitiveProgram qubits where
  globalPhase := .piRational (-1 / 8)
  circuit := [.rz target (.piRational (-1 / 4))]

theorem evalGlobalPhase_pi_div_two :
    evalGlobalPhase (.piRational (1 / 2)) = Complex.I := by
  simp only [evalGlobalPhase, ExactAngle.eval]
  norm_num
  convert Complex.exp_pi_div_two_mul_I using 1 <;> push_cast <;> ring

theorem liftPrimitiveOneQubit_mul {qubits : Nat} (target : Fin qubits)
    (left right : _root_.Matrix (Fin 2) (Fin 2) ℂ) :
    liftPrimitiveOneQubit target (left * right) =
      liftPrimitiveOneQubit target left * liftPrimitiveOneQubit target right := by
  unfold liftPrimitiveOneQubit
  rw [← _root_.Matrix.reindexAlgEquiv_mul]
  congr 1
  rw [← _root_.Matrix.mul_kronecker_mul]
  simp

theorem smul_liftPrimitiveOneQubit {qubits : Nat} (target : Fin qubits)
    (scalar : ℂ) (gate : _root_.Matrix (Fin 2) (Fin 2) ℂ) :
    scalar • liftPrimitiveOneQubit target gate =
      liftPrimitiveOneQubit target (scalar • gate) := by
  ext row column
  simp only [_root_.Matrix.smul_apply, liftPrimitiveOneQubit_apply]
  by_cases context : (splitPrimitiveWire target row).2 =
      (splitPrimitiveWire target column).2 <;> simp [context]

theorem primitiveHProgram_eval {qubits : Nat} (target : Fin qubits) :
    evalPrimitiveProgram (primitiveHProgram target) =
      liftPrimitiveOneQubit target hadamardMatrix := by
  change evalGlobalPhase (.piRational (1 / 2)) •
      evalPrimitiveCircuit
        [.rz target (.piRational 1), .ry target (.piRational (1 / 2))] = _
  rw [evalGlobalPhase_pi_div_two]
  simp only [evalPrimitiveCircuit, _root_.Matrix.one_mul, evalPrimitiveGate,
    ExactAngle.eval]
  norm_num
  rw [← liftPrimitiveOneQubit_mul, smul_liftPrimitiveOneQubit]
  congr 2
  congr 2
  ring

theorem primitiveTProgram_eval {qubits : Nat} (target : Fin qubits) :
    evalPrimitiveProgram (primitiveTProgram target) =
      liftPrimitiveOneQubit target (phaseMatrix (Real.pi / 4)) := by
  change evalGlobalPhase (.piRational (1 / 8)) •
      evalPrimitiveCircuit [.rz target (.piRational (1 / 4))] = _
  have phaseEval : evalGlobalPhase (.piRational (1 / 8)) =
      Complex.exp ((((Real.pi / 4) / 2 : Real) : ℂ) * Complex.I) := by
    apply congrArg Complex.exp
    simp [evalGlobalPhase, ExactAngle.eval]
    push_cast
    ring
  rw [phaseEval]
  simp only [evalPrimitiveCircuit, _root_.Matrix.one_mul, evalPrimitiveGate]
  rw [smul_liftPrimitiveOneQubit]
  congr 2
  apply congrArg standardRzMatrix
  simp only [ExactAngle.eval]
  norm_num
  ring

theorem primitiveTdgProgram_eval {qubits : Nat} (target : Fin qubits) :
    evalPrimitiveProgram (primitiveTdgProgram target) =
      liftPrimitiveOneQubit target (phaseMatrix (-Real.pi / 4)) := by
  change evalGlobalPhase (.piRational (-1 / 8)) •
      evalPrimitiveCircuit [.rz target (.piRational (-1 / 4))] = _
  have phaseEval : evalGlobalPhase (.piRational (-1 / 8)) =
      Complex.exp ((((-Real.pi / 4) / 2 : Real) : ℂ) * Complex.I) := by
    apply congrArg Complex.exp
    simp [evalGlobalPhase, ExactAngle.eval]
    push_cast
    ring
  rw [phaseEval]
  simp only [evalPrimitiveCircuit, _root_.Matrix.one_mul, evalPrimitiveGate]
  rw [smul_liftPrimitiveOneQubit]
  congr 2
  apply congrArg standardRzMatrix
  simp only [ExactAngle.eval]
  norm_num
  ring

/-! ## Monomial semantics for the classical phase network -/

noncomputable def phasePermutationMatrix {index : Type*}
    [Fintype index] [DecidableEq index]
    (phase : index → ℂ) (permutation : index ≃ index) :
    _root_.Matrix index index ℂ := fun row column =>
  if row = permutation column then phase column else 0

theorem phasePermutationMatrix_mul {index : Type*}
    [Fintype index] [DecidableEq index]
    (leftPhase rightPhase : index → ℂ)
    (leftPerm rightPerm : index ≃ index) :
    phasePermutationMatrix rightPhase rightPerm *
        phasePermutationMatrix leftPhase leftPerm =
      phasePermutationMatrix
        (fun state => leftPhase state * rightPhase (leftPerm state))
        (leftPerm.trans rightPerm) := by
  ext row column
  rw [_root_.Matrix.mul_apply]
  classical
  rw [Finset.sum_eq_single (leftPerm column)]
  · by_cases h : row = rightPerm (leftPerm column) <;>
      simp [phasePermutationMatrix, h, mul_comm]
  · intro middle _ different
    simp [phasePermutationMatrix, different]
  · simp

theorem evalPrimitiveCx_eq_phasePermutationMatrix {qubits : Nat}
    (control target : Fin qubits) (distinct : control ≠ target) :
    evalPrimitiveGate (.cx control target distinct) =
      phasePermutationMatrix (fun _ => 1)
        (cxBasisEquiv control target distinct) := by
  ext row column
  rfl

theorem liftPhaseMatrix_eq_phasePermutationMatrix {qubits : Nat}
    (target : Fin qubits) (theta : Real) :
    liftPrimitiveOneQubit target (phaseMatrix theta) =
      phasePermutationMatrix
        (fun state => if state target = 0 then 1
          else Complex.exp ((theta : ℂ) * Complex.I))
        (Equiv.refl _) := by
  ext row column
  rw [liftPrimitiveOneQubit_apply]
  simp only [phasePermutationMatrix, Equiv.refl_apply]
  by_cases equal : row = column
  · subst row
    simp [phaseMatrix_apply]
  ·
    by_cases context : (splitPrimitiveWire target row).2 =
        (splitPrimitiveWire target column).2
    · have targetNe : row target ≠ column target := by
        intro targetEqual
        apply equal
        apply (splitPrimitiveWire target).injective
        exact Prod.ext targetEqual context
      simp [equal, context, phaseMatrix_apply, targetNe]
    · simp [equal, context]

def primitiveCxProgram {qubits : Nat} (control target : Fin qubits)
    (distinct : control ≠ target) : PrimitiveProgram qubits where
  circuit := [.cx control target distinct]
  globalPhase := .rational 0

theorem primitiveCxProgram_eval {qubits : Nat}
    (control target : Fin qubits) (distinct : control ≠ target) :
    evalPrimitiveProgram (primitiveCxProgram control target distinct) =
      phasePermutationMatrix (fun _ => 1)
        (cxBasisEquiv control target distinct) := by
  change evalGlobalPhase (.rational 0) •
      evalPrimitiveCircuit [.cx control target distinct] = _
  have zeroPhase : evalGlobalPhase (.rational 0) = 1 := by
    simp [evalGlobalPhase, ExactAngle.eval]
  rw [zeroPhase, one_smul]
  simp [evalPrimitiveCircuit, evalPrimitiveCx_eq_phasePermutationMatrix]

theorem primitiveTProgram_eval_monomial {qubits : Nat}
    (target : Fin qubits) :
    evalPrimitiveProgram (primitiveTProgram target) =
      phasePermutationMatrix
        (fun state => if state target = 0 then 1
          else Complex.exp (((Real.pi / 4 : Real) : ℂ) * Complex.I))
        (Equiv.refl _) := by
  rw [primitiveTProgram_eval, liftPhaseMatrix_eq_phasePermutationMatrix]

theorem primitiveTdgProgram_eval_monomial {qubits : Nat}
    (target : Fin qubits) :
    evalPrimitiveProgram (primitiveTdgProgram target) =
      phasePermutationMatrix
        (fun state => if state target = 0 then 1
          else Complex.exp (((-Real.pi / 4 : Real) : ℂ) * Complex.I))
        (Equiv.refl _) := by
  rw [primitiveTdgProgram_eval, liftPhaseMatrix_eq_phasePermutationMatrix]

structure MonomialProgram (qubits : Nat) where
  program : PrimitiveProgram qubits
  phase : PrimitiveBasis qubits → ℂ
  permutation : PrimitiveBasis qubits ≃ PrimitiveBasis qubits
  exact : evalPrimitiveProgram program =
    phasePermutationMatrix phase permutation

namespace MonomialProgram

def seq {qubits : Nat} (left right : MonomialProgram qubits) :
    MonomialProgram qubits where
  program := left.program.seq right.program
  phase := fun state => left.phase state * right.phase (left.permutation state)
  permutation := left.permutation.trans right.permutation
  exact := by
    rw [evalPrimitiveProgram_seq, left.exact, right.exact,
      phasePermutationMatrix_mul]

def cx {qubits : Nat} (control target : Fin qubits)
    (distinct : control ≠ target) : MonomialProgram qubits where
  program := primitiveCxProgram control target distinct
  phase := fun _ => 1
  permutation := cxBasisEquiv control target distinct
  exact := primitiveCxProgram_eval control target distinct

noncomputable def t {qubits : Nat} (target : Fin qubits) : MonomialProgram qubits where
  program := primitiveTProgram target
  phase := fun state => if state target = 0 then 1
    else Complex.exp (((Real.pi / 4 : Real) : ℂ) * Complex.I)
  permutation := Equiv.refl _
  exact := primitiveTProgram_eval_monomial target

noncomputable def tdg {qubits : Nat} (target : Fin qubits) : MonomialProgram qubits where
  program := primitiveTdgProgram target
  phase := fun state => if state target = 0 then 1
    else Complex.exp (((-Real.pi / 4 : Real) : ℂ) * Complex.I)
  permutation := Equiv.refl _
  exact := primitiveTdgProgram_eval_monomial target

end MonomialProgram

/-- The phase-only middle of the standard exact Toffoli decomposition. -/
noncomputable def primitiveCCXMiddle {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_b : a ≠ b) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target) : MonomialProgram qubits :=
  let cxBT := MonomialProgram.cx b target b_ne_target
  let cxAT := MonomialProgram.cx a target a_ne_target
  let cxAB := MonomialProgram.cx a b a_ne_b
  cxBT |>.seq (MonomialProgram.tdg target)
    |>.seq cxAT
    |>.seq (MonomialProgram.t target)
    |>.seq cxBT
    |>.seq (MonomialProgram.tdg target)
    |>.seq cxAT
    |>.seq (MonomialProgram.t b)
    |>.seq (MonomialProgram.t target)
    |>.seq cxAB
    |>.seq (MonomialProgram.t a)
    |>.seq (MonomialProgram.tdg b)
    |>.seq cxAB

/-- The exact primitive program uses the requested H/T/Tdg/CX chronology. -/
noncomputable def primitiveCCXProgram {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_b : a ≠ b) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target) : PrimitiveProgram qubits :=
  (primitiveHProgram target).seq
    ((primitiveCCXMiddle a b target a_ne_b a_ne_target b_ne_target).program.seq
      (primitiveHProgram target))

set_option maxHeartbeats 2000000 in
theorem primitiveCCXMiddle_permutation_eq_refl {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_b : a ≠ b) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target) :
    (primitiveCCXMiddle a b target a_ne_b a_ne_target b_ne_target).permutation =
      Equiv.refl _ := by
  apply Equiv.ext
  intro state
  have bitCases (bit : Fin 2) : bit = 0 ∨ bit = 1 := by
    fin_cases bit <;> simp
  rcases bitCases (state a) with ha | ha <;>
    rcases bitCases (state b) with hb | hb <;>
    rcases bitCases (state target) with ht | ht
  all_goals
    funext wire
    by_cases wa : wire = a <;> by_cases wb : wire = b <;>
      by_cases wt : wire = target <;>
      simp [primitiveCCXMiddle, MonomialProgram.seq, MonomialProgram.cx,
        MonomialProgram.t, MonomialProgram.tdg, cxBasisEquiv_apply,
        cxBasisAction,
        xBasisAction, flipBit, ha, hb, ht, wa, wb, wt,
        a_ne_b, a_ne_target, b_ne_target, Ne.symm a_ne_b,
        Ne.symm a_ne_target, Ne.symm b_ne_target]

set_option maxHeartbeats 2000000 in
theorem primitiveCCXMiddle_phase_eq_ccz {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_b : a ≠ b) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target) (state : PrimitiveBasis qubits) :
    (primitiveCCXMiddle a b target a_ne_b a_ne_target b_ne_target).phase state =
      if state a = 1 ∧ state b = 1 ∧ state target = 1 then -1 else 1 := by
  have bitCases (bit : Fin 2) : bit = 0 ∨ bit = 1 := by
    fin_cases bit <;> simp
  rcases bitCases (state a) with ha | ha <;>
    rcases bitCases (state b) with hb | hb <;>
    rcases bitCases (state target) with ht | ht
  all_goals
    simp [primitiveCCXMiddle, MonomialProgram.seq, MonomialProgram.cx,
      MonomialProgram.t, MonomialProgram.tdg, cxBasisEquiv_apply,
      cxBasisAction,
      xBasisAction, flipBit, ha, hb, ht, a_ne_b, a_ne_target, b_ne_target,
      Ne.symm a_ne_b, Ne.symm a_ne_target, Ne.symm b_ne_target,
      ← Complex.exp_add]
  all_goals
    ring_nf
    simp

noncomputable def cczMatrix {qubits : Nat}
    (a b target : Fin qubits) :
    _root_.Matrix (PrimitiveBasis qubits) (PrimitiveBasis qubits) ℂ :=
  phasePermutationMatrix
    (fun state => if state a = 1 ∧ state b = 1 ∧ state target = 1
      then -1 else 1)
    (Equiv.refl _)

theorem primitiveCCXMiddle_eval {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_b : a ≠ b) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target) :
    evalPrimitiveProgram
        (primitiveCCXMiddle a b target a_ne_b a_ne_target b_ne_target).program =
      cczMatrix a b target := by
  rw [(primitiveCCXMiddle a b target a_ne_b a_ne_target b_ne_target).exact]
  unfold cczMatrix
  rw [primitiveCCXMiddle_permutation_eq_refl]
  congr 2
  funext state
  exact primitiveCCXMiddle_phase_eq_ccz a b target a_ne_b a_ne_target
    b_ne_target state

def zMatrix : _root_.Matrix (Fin 2) (Fin 2) ℂ := fun row column =>
  if row = column then if row = 0 then 1 else -1 else 0

theorem hadamard_mul_hadamard : hadamardMatrix * hadamardMatrix = 1 := by
  ext row column
  fin_cases row <;> fin_cases column <;>
    simp [hadamardMatrix_apply, _root_.Matrix.mul_apply, Fin.sum_univ_two]
  all_goals
    have squareRoot : (Real.sqrt 2) ^ 2 = (2 : Real) :=
      Real.sq_sqrt (by norm_num)
    apply Complex.ext <;> simp <;> nlinarith

theorem hadamard_mul_z_mul_hadamard :
    hadamardMatrix * zMatrix * hadamardMatrix = xMatrix := by
  ext row column
  fin_cases row <;> fin_cases column <;>
    simp [hadamardMatrix_apply, zMatrix, xMatrix,
      _root_.Matrix.mul_apply, Fin.sum_univ_two]
  all_goals
    have squareRoot : (Real.sqrt 2) ^ 2 = (2 : Real) :=
      Real.sq_sqrt (by norm_num)
    apply Complex.ext <;> simp <;> nlinarith

theorem liftPrimitiveOneQubit_eq_blockDiagonal {qubits : Nat}
    (target : Fin qubits) (gate : _root_.Matrix (Fin 2) (Fin 2) ℂ) :
    liftPrimitiveOneQubit target gate =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ (splitPrimitiveWire target).symm
        (_root_.Matrix.blockDiagonal
          (fun _ : OtherPrimitiveWires target → Fin 2 => gate)) := by
  ext row column
  simp [liftPrimitiveOneQubit_apply, _root_.Matrix.blockDiagonal_apply,
    splitPrimitiveWire]

noncomputable def cczTargetBlock {qubits : Nat}
    (a b target : Fin qubits) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target)
    (context : OtherPrimitiveWires target → Fin 2) :
    _root_.Matrix (Fin 2) (Fin 2) ℂ :=
  if context ⟨a, a_ne_target⟩ = 1 ∧ context ⟨b, b_ne_target⟩ = 1
  then zMatrix else 1

theorem cczMatrix_eq_blockDiagonal {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_target : a ≠ target) (b_ne_target : b ≠ target) :
    cczMatrix a b target =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ (splitPrimitiveWire target).symm
        (_root_.Matrix.blockDiagonal
          (cczTargetBlock a b target a_ne_target b_ne_target)) := by
  ext row column
  simp only [cczMatrix, phasePermutationMatrix,
    _root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply,
    _root_.Matrix.submatrix_apply, Equiv.symm_symm,
    _root_.Matrix.blockDiagonal_apply]
  by_cases context : (splitPrimitiveWire target row).2 =
      (splitPrimitiveWire target column).2
  · rw [if_pos context]
    by_cases targetEqual : row target = column target
    · have equal : row = column := by
        apply (splitPrimitiveWire target).injective
        exact Prod.ext targetEqual context
      subst row
      rw [if_pos (show column = (Equiv.refl _) column by rfl)]
      by_cases active : column a = 1 ∧ column b = 1
      · have bitCases (bit : Fin 2) : bit = 0 ∨ bit = 1 := by
          fin_cases bit <;> simp
        rcases bitCases (column target) with htarget | htarget <;>
          simp [cczTargetBlock, active, zMatrix, htarget,
            splitPrimitiveWire]
      · have inactiveTriple :
            ¬(column a = 1 ∧ column b = 1 ∧ column target = 1) := by
          intro triple
          exact active ⟨triple.1, triple.2.1⟩
        simp [cczTargetBlock, active, inactiveTriple, splitPrimitiveWire]
    · have notEqual : row ≠ column := by
        intro equal
        exact targetEqual (congrFun equal target)
      have notEqualRefl : row ≠ (Equiv.refl _) column := by
        simpa using notEqual
      rw [if_neg notEqualRefl]
      have splitTargetNe :
          (splitPrimitiveWire target row).1 ≠
            (splitPrimitiveWire target column).1 := by
        simpa [splitPrimitiveWire] using targetEqual
      by_cases active :
          (splitPrimitiveWire target row).2 ⟨a, a_ne_target⟩ = 1 ∧
            (splitPrimitiveWire target row).2 ⟨b, b_ne_target⟩ = 1
      · simp [cczTargetBlock, active, zMatrix, splitTargetNe]
      · simp [cczTargetBlock, active, splitTargetNe,
          _root_.Matrix.one_apply]
  · have notEqual : row ≠ column := by
      intro equal
      exact context (congrArg (fun state =>
        (splitPrimitiveWire target state).2) equal)
    have notEqualRefl : row ≠ (Equiv.refl _) column := by
      simpa using notEqual
    rw [if_neg notEqualRefl, if_neg context]

noncomputable def ccxTargetBlock {qubits : Nat}
    (a b target : Fin qubits) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target)
    (context : OtherPrimitiveWires target → Fin 2) :
    _root_.Matrix (Fin 2) (Fin 2) ℂ :=
  if context ⟨a, a_ne_target⟩ = 1 ∧ context ⟨b, b_ne_target⟩ = 1
  then xMatrix else 1

theorem equivPermutationMatrix_ccx_eq_blockDiagonal {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_target : a ≠ target) (b_ne_target : b ≠ target) :
    Robin.ComplexLCU.equivPermutationMatrix
        (ccxBasisEquiv a b target a_ne_target b_ne_target) =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ (splitPrimitiveWire target).symm
        (_root_.Matrix.blockDiagonal
          (ccxTargetBlock a b target a_ne_target b_ne_target)) := by
  ext row column
  simp only [Robin.ComplexLCU.equivPermutationMatrix,
    _root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply,
    _root_.Matrix.submatrix_apply, Equiv.symm_symm,
    _root_.Matrix.blockDiagonal_apply, ccxBasisEquiv_apply]
  by_cases context : (splitPrimitiveWire target row).2 =
      (splitPrimitiveWire target column).2
  · rw [if_pos context]
    have aEqual : row a = column a := by
      simpa [splitPrimitiveWire, a_ne_target] using
        congrFun context ⟨a, a_ne_target⟩
    have bEqual : row b = column b := by
      simpa [splitPrimitiveWire, b_ne_target] using
        congrFun context ⟨b, b_ne_target⟩
    by_cases active : column a = 1 ∧ column b = 1
    · have rowActive : row a = 1 ∧ row b = 1 := by simpa [aEqual, bEqual]
      have actionIff :
          row = Function.update column target (flipBit (column target)) ↔
            row target = flipBit (column target) := by
        constructor
        · intro equality
          simpa [Function.update] using congrFun equality target
        · intro targetEqual
          apply (splitPrimitiveWire target).injective
          apply Prod.ext
          · simpa [splitPrimitiveWire, Function.update]
          · funext wire
            have contextWire := congrFun context wire
            simpa [splitPrimitiveWire, Function.update, wire.property] using
              contextWire
      have flipIff : row target = flipBit (column target) ↔
          row target ≠ column target := by
        have bitCases (bit : Fin 2) : bit = 0 ∨ bit = 1 := by
          fin_cases bit <;> simp
        rcases bitCases (row target) with hrow | hrow <;>
          rcases bitCases (column target) with hcolumn | hcolumn <;>
          simp [hrow, hcolumn, flipBit]
      simp [ccxTargetBlock, active, rowActive,
        ccxBasisAction, xMatrix, splitPrimitiveWire, xBasisAction,
        actionIff, flipIff]
    · have rowInactive : ¬(row a = 1 ∧ row b = 1) := by
        simpa [aEqual, bEqual] using active
      have rowEqIff : row = column ↔ row target = column target := by
        constructor
        · intro equality
          exact congrFun equality target
        · intro targetEqual
          apply (splitPrimitiveWire target).injective
          exact Prod.ext targetEqual context
      simp [ccxTargetBlock, active, rowInactive,
        ccxBasisAction, rowEqIff, splitPrimitiveWire,
        _root_.Matrix.one_apply]
  · have actionMiss : row ≠ ccxBasisAction a b target column := by
      intro action
      apply context
      funext wire
      have actionWire := congrFun action wire.1
      change row wire.1 = column wire.1
      by_cases active : column a = 1 ∧ column b = 1
      · simpa [ccxBasisAction, active, xBasisAction, wire.property] using
          actionWire
      · simpa [ccxBasisAction, active] using actionWire
    simp [ccxTargetBlock, context, actionMiss]

theorem hadamard_conjugates_ccz {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_target : a ≠ target) (b_ne_target : b ≠ target) :
    liftPrimitiveOneQubit target hadamardMatrix *
        cczMatrix a b target *
        liftPrimitiveOneQubit target hadamardMatrix =
      Robin.ComplexLCU.equivPermutationMatrix
        (ccxBasisEquiv a b target a_ne_target b_ne_target) := by
  rw [liftPrimitiveOneQubit_eq_blockDiagonal,
    cczMatrix_eq_blockDiagonal a b target a_ne_target b_ne_target,
    equivPermutationMatrix_ccx_eq_blockDiagonal a b target
      a_ne_target b_ne_target]
  rw [← _root_.Matrix.reindexAlgEquiv_mul,
    ← _root_.Matrix.reindexAlgEquiv_mul]
  apply_fun (_root_.Matrix.reindexAlgEquiv ℂ ℂ
    (splitPrimitiveWire target).symm).symm
  simp only [AlgEquiv.symm_apply_apply]
  rw [← _root_.Matrix.blockDiagonal_mul,
    ← _root_.Matrix.blockDiagonal_mul]
  congr 1
  funext context
  by_cases active :
      context ⟨a, a_ne_target⟩ = 1 ∧
        context ⟨b, b_ne_target⟩ = 1
  · simp [cczTargetBlock, ccxTargetBlock, active,
      hadamard_mul_z_mul_hadamard]
  · simp [cczTargetBlock, ccxTargetBlock, active,
      hadamard_mul_hadamard]

/-- The requested H/T/Tdg/CX decomposition is exactly Toffoli, including its
global phase. -/
theorem primitiveCCXProgram_eval {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_b : a ≠ b) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target) :
    evalPrimitiveProgram
        (primitiveCCXProgram a b target a_ne_b a_ne_target b_ne_target) =
      Robin.ComplexLCU.equivPermutationMatrix
        (ccxBasisEquiv a b target a_ne_target b_ne_target) := by
  rw [primitiveCCXProgram, evalPrimitiveProgram_seq,
    evalPrimitiveProgram_seq, primitiveHProgram_eval,
    primitiveCCXMiddle_eval]
  exact hadamard_conjugates_ccz a b target a_ne_target b_ne_target

noncomputable def primitiveCCXProgramRefinement {qubits : Nat}
    (a b target : Fin qubits)
    (a_ne_b : a ≠ b) (a_ne_target : a ≠ target)
    (b_ne_target : b ≠ target) : PrimitiveProgramRefinement qubits where
  program := primitiveCCXProgram a b target a_ne_b a_ne_target b_ne_target
  target := Robin.ComplexLCU.equivPermutationMatrix
    (ccxBasisEquiv a b target a_ne_target b_ne_target)
  exact := primitiveCCXProgram_eval a b target a_ne_b a_ne_target b_ne_target

end QuantumBlockEncoding
