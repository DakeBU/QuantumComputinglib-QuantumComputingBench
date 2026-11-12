import QuantumBlockEncoding.PrimitiveCircuit
import QuantumBlockEncoding.Robin.Hadamard8Verified
import Mathlib.Tactic

/-!
# Exact matrix semantics for the primitive basis

The standard `RY` convention uses a half angle.  The bridge theorem below is
the convention check needed by every Robin coefficient loader.
-/

namespace QuantumBlockEncoding

open QuantumBlockEncoding.Robin.ComplexLCU
open scoped Kronecker

/-- Standard `RY(theta)` in the convention used by Qiskit and OpenQASM 3. -/
noncomputable def standardRyMatrix (theta : Real) :
    _root_.Matrix (Fin 2) (Fin 2) ℂ :=
  realRotation (theta / 2)

@[simp] theorem standardRyMatrix_zero : standardRyMatrix 0 = 1 := by
  ext row column
  fin_cases row <;> fin_cases column <;>
    simp [standardRyMatrix, realRotation, realOrthogonalRotation]

/-- Standard rotations compose by adding their physical angles. -/
theorem standardRyMatrix_add (left right : Real) :
    standardRyMatrix (left + right) =
      standardRyMatrix right * standardRyMatrix left := by
  have halfAdd : (left + right) / 2 = left / 2 + right / 2 := by ring
  rw [standardRyMatrix, halfAdd]
  ext row column
  fin_cases row <;> fin_cases column <;>
    simp [standardRyMatrix, realRotation, realOrthogonalRotation,
      _root_.Matrix.mul_apply, Fin.sum_univ_two,
      Real.sin_add, Real.cos_add] <;> ring

@[simp] theorem star_complex_cos_ofReal (theta : Real) :
    star (Complex.cos (theta : ℂ)) = Complex.cos (theta : ℂ) := by
  rw [← Complex.ofReal_cos, Complex.star_def, Complex.conj_ofReal]

@[simp] theorem conj_complex_cos_ofReal (theta : Real) :
    (starRingEnd ℂ) (Complex.cos (theta : ℂ)) =
      Complex.cos (theta : ℂ) := by
  rw [← Complex.ofReal_cos, Complex.conj_ofReal]

@[simp] theorem star_complex_sin_ofReal (theta : Real) :
    star (Complex.sin (theta : ℂ)) = Complex.sin (theta : ℂ) := by
  rw [← Complex.ofReal_sin, Complex.star_def, Complex.conj_ofReal]

@[simp] theorem conj_complex_sin_ofReal (theta : Real) :
    (starRingEnd ℂ) (Complex.sin (theta : ℂ)) =
      Complex.sin (theta : ℂ) := by
  rw [← Complex.ofReal_sin, Complex.conj_ofReal]

theorem complex_ofReal_div_two (theta : Real) :
    (theta : ℂ) / 2 = ((theta / 2 : Real) : ℂ) := by
  norm_num

@[simp] theorem conj_complex_cos_ofReal_div_two (theta : Real) :
    (starRingEnd ℂ) (Complex.cos ((theta : ℂ) / 2)) =
      Complex.cos ((theta : ℂ) / 2) := by
  rw [complex_ofReal_div_two, ← Complex.ofReal_cos, Complex.conj_ofReal]

@[simp] theorem conj_complex_sin_ofReal_div_two (theta : Real) :
    (starRingEnd ℂ) (Complex.sin ((theta : ℂ) / 2)) =
      Complex.sin ((theta : ℂ) / 2) := by
  rw [complex_ofReal_div_two, ← Complex.ofReal_sin, Complex.conj_ofReal]

@[simp] theorem standardRyMatrix_neg (theta : Real) :
    standardRyMatrix (-theta) = star (standardRyMatrix theta) := by
  change realRotation (-theta / 2) = star (realRotation (theta / 2))
  rw [show -theta / 2 = -(theta / 2) by ring]
  ext row column
  fin_cases row <;> fin_cases column <;>
    simp [realRotation, realOrthogonalRotation]

/-- Pauli X in the same two-dimensional basis as `standardRyMatrix`. -/
def xMatrix : _root_.Matrix (Fin 2) (Fin 2) ℂ := fun row column =>
  if row = column then 0 else 1

theorem xMatrix_conjugates_standardRy (theta : Real) :
    xMatrix * standardRyMatrix theta * xMatrix = standardRyMatrix (-theta) := by
  rw [standardRyMatrix_neg]
  ext row column
  fin_cases row <;> fin_cases column <;>
    simp [xMatrix, standardRyMatrix, realRotation, realOrthogonalRotation,
      _root_.Matrix.mul_apply, Fin.sum_univ_two]

theorem standardRyMatrix_unitary (theta : Real) :
    standardRyMatrix theta ∈ _root_.Matrix.unitaryGroup (Fin 2) ℂ :=
  realRotation_unitary _

/-- The exact half-angle correction from standard `RY` to the logical loader. -/
theorem standardRyMatrix_two_arccos_eq_amplitudeRotation
    (coefficient : Real) (_lower : -1 ≤ coefficient)
    (_upper : coefficient ≤ 1) :
    standardRyMatrix (2 * Real.arccos coefficient) =
      amplitudeRotation coefficient := by
  unfold standardRyMatrix amplitudeRotation
  congr 1
  ring

/-- The symmetry PREPARE is exactly a standard `RY(pi/2)`, not an opaque H. -/
theorem standardRyMatrix_pi_div_two_eq_warmRobinUniformBitPrepare :
    standardRyMatrix (Real.pi / 2) =
      QuantumBlockEncoding.Robin.warmRobinUniformBitPrepare := by
  have half : (Real.pi / 2) / 2 = Real.pi / 4 := by ring
  unfold standardRyMatrix
  rw [half]
  unfold realRotation QuantumBlockEncoding.Robin.warmRobinUniformBitPrepare
  rw [Real.cos_pi_div_four, Real.sin_pi_div_four]

/-- Computational-basis bit strings with one named coordinate per qubit. -/
abbrev PrimitiveBasis (qubits : Nat) := Fin qubits → Fin 2

def flipBit (bit : Fin 2) : Fin 2 := if bit = 0 then 1 else 0

@[simp] theorem flipBit_flipBit (bit : Fin 2) : flipBit (flipBit bit) = bit := by
  fin_cases bit <;> rfl

def xBasisAction {qubits : Nat} (target : Fin qubits)
    (state : PrimitiveBasis qubits) : PrimitiveBasis qubits :=
  Function.update state target (flipBit (state target))

theorem xBasisAction_involutive {qubits : Nat} (target : Fin qubits) :
    Function.Involutive (xBasisAction target) := by
  intro state
  funext wire
  by_cases same : wire = target
  · subst wire
    simp [xBasisAction]
  · simp [xBasisAction, same]

def xBasisEquiv {qubits : Nat} (target : Fin qubits) :
    PrimitiveBasis qubits ≃ PrimitiveBasis qubits where
  toFun := xBasisAction target
  invFun := xBasisAction target
  left_inv := xBasisAction_involutive target
  right_inv := xBasisAction_involutive target

def cxBasisAction {qubits : Nat} (control target : Fin qubits)
    (state : PrimitiveBasis qubits) : PrimitiveBasis qubits :=
  if state control = 0 then state else xBasisAction target state

theorem cxBasisAction_involutive {qubits : Nat}
    (control target : Fin qubits) (distinct : control ≠ target) :
    Function.Involutive (cxBasisAction control target) := by
  intro state
  by_cases controlZero : state control = 0
  · simp [cxBasisAction, controlZero]
  · have controlUnchanged : xBasisAction target state control = state control := by
      simp [xBasisAction, distinct]
    simp [cxBasisAction, controlZero, controlUnchanged,
      xBasisAction_involutive target state]

def cxBasisEquiv {qubits : Nat} (control target : Fin qubits)
    (distinct : control ≠ target) :
    PrimitiveBasis qubits ≃ PrimitiveBasis qubits where
  toFun := cxBasisAction control target
  invFun := cxBasisAction control target
  left_inv := cxBasisAction_involutive control target distinct
  right_inv := cxBasisAction_involutive control target distinct

@[simp] theorem cxBasisEquiv_apply {qubits : Nat}
    (control target : Fin qubits) (distinct : control ≠ target)
    (state : PrimitiveBasis qubits) :
    cxBasisEquiv control target distinct state =
      cxBasisAction control target state := rfl

abbrev OtherPrimitiveWires {qubits : Nat} (target : Fin qubits) :=
  {wire : Fin qubits // wire ≠ target}

def splitPrimitiveWire {qubits : Nat} (target : Fin qubits) :
    PrimitiveBasis qubits ≃
      Fin 2 × (OtherPrimitiveWires target → Fin 2) where
  toFun state := (state target, fun wire => state wire.1)
  invFun pair wire :=
    if same : wire = target then pair.1 else pair.2 ⟨wire, same⟩
  left_inv state := by
    funext wire
    by_cases same : wire = target
    · subst wire
      simp
    · simp [same]
  right_inv pair := by
    rcases pair with ⟨targetBit, otherBits⟩
    apply Prod.ext
    · simp
    · funext wire
      simp [wire.property]

theorem splitPrimitiveWire_other_apply {qubits : Nat}
    (target : Fin qubits) (state : PrimitiveBasis qubits)
    (wire : OtherPrimitiveWires target) :
    (splitPrimitiveWire target state).2 wire = state wire.1 := rfl

/-- Lift a one-qubit matrix to a named wire, leaving every other wire fixed. -/
noncomputable def liftPrimitiveOneQubit {qubits : Nat} (target : Fin qubits)
    (gate : _root_.Matrix (Fin 2) (Fin 2) ℂ) :
    _root_.Matrix (PrimitiveBasis qubits) (PrimitiveBasis qubits) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ (splitPrimitiveWire target).symm
    (gate ⊗ₖ (1 : _root_.Matrix
      (OtherPrimitiveWires target → Fin 2)
      (OtherPrimitiveWires target → Fin 2) ℂ))

@[simp] theorem liftPrimitiveOneQubit_apply {qubits : Nat}
    (target : Fin qubits) (gate : _root_.Matrix (Fin 2) (Fin 2) ℂ)
    (row column : PrimitiveBasis qubits) :
    liftPrimitiveOneQubit target gate row column =
      if (splitPrimitiveWire target row).2 =
          (splitPrimitiveWire target column).2 then
        gate (row target) (column target)
      else 0 := by
  simp only [liftPrimitiveOneQubit, _root_.Matrix.reindexAlgEquiv_apply,
    _root_.Matrix.reindex_apply, _root_.Matrix.submatrix_apply,
    _root_.Matrix.kroneckerMap_apply, _root_.Matrix.one_apply,
    Equiv.symm_symm]
  by_cases contextsEqual :
      (splitPrimitiveWire target row).2 =
        (splitPrimitiveWire target column).2
  · simp [contextsEqual, splitPrimitiveWire]
  · simp [contextsEqual, splitPrimitiveWire]

theorem liftPrimitiveOneQubit_unitary {qubits : Nat} (target : Fin qubits)
    (gate : _root_.Matrix (Fin 2) (Fin 2) ℂ)
    (unitary : gate ∈ _root_.Matrix.unitaryGroup (Fin 2) ℂ) :
    liftPrimitiveOneQubit target gate ∈
      _root_.Matrix.unitaryGroup (PrimitiveBasis qubits) ℂ := by
  apply reindex_unitary
  apply _root_.Matrix.kronecker_mem_unitary
  · exact unitary
  · exact (_root_.Matrix.unitaryGroup
      (OtherPrimitiveWires target → Fin 2) ℂ).one_mem

/-- Standard exact `RZ(theta)` matrix, including its phase convention. -/
noncomputable def standardRzMatrix (theta : Real) :
    _root_.Matrix (Fin 2) (Fin 2) ℂ := fun row column =>
  if row = column then
    if row = 0 then
      (Real.cos (theta / 2) : ℂ) - (Real.sin (theta / 2) : ℂ) * Complex.I
    else
      (Real.cos (theta / 2) : ℂ) + (Real.sin (theta / 2) : ℂ) * Complex.I
  else 0

theorem standardRzMatrix_unitary (theta : Real) :
    standardRzMatrix theta ∈ _root_.Matrix.unitaryGroup (Fin 2) ℂ := by
  let c := Real.cos (theta / 2)
  let s := Real.sin (theta / 2)
  have trig : s ^ 2 + c ^ 2 = 1 := by
    simp [c, s, Real.sin_sq_add_cos_sq]
  have minusNorm :
      star ((c : ℂ) - (s : ℂ) * Complex.I) *
          ((c : ℂ) - (s : ℂ) * Complex.I) = 1 := by
    apply Complex.ext <;> simp <;> nlinarith
  have plusNorm :
      star ((c : ℂ) + (s : ℂ) * Complex.I) *
          ((c : ℂ) + (s : ℂ) * Complex.I) = 1 := by
    apply Complex.ext <;> simp <;> nlinarith
  rw [_root_.Matrix.mem_unitaryGroup_iff']
  ext row column
  fin_cases row <;> fin_cases column
  · simpa [standardRzMatrix, _root_.Matrix.mul_apply, c, s] using minusNorm
  · simp [standardRzMatrix, _root_.Matrix.mul_apply]
  · simp [standardRzMatrix, _root_.Matrix.mul_apply]
  · simpa [standardRzMatrix, _root_.Matrix.mul_apply, c, s] using plusNorm

@[simp] theorem standardRzMatrix_neg (theta : Real) :
    standardRzMatrix (-theta) = star (standardRzMatrix theta) := by
  ext row column
  fin_cases row <;> fin_cases column
  · change
      (Real.cos (-theta / 2) : ℂ) -
          (Real.sin (-theta / 2) : ℂ) * Complex.I =
        star ((Real.cos (theta / 2) : ℂ) -
          (Real.sin (theta / 2) : ℂ) * Complex.I)
    rw [show -theta / 2 = -(theta / 2) by ring,
      Real.cos_neg, Real.sin_neg]
    simp
  · simp [standardRzMatrix, _root_.Matrix.star_apply]
  · simp [standardRzMatrix, _root_.Matrix.star_apply]
  · change
      (Real.cos (-theta / 2) : ℂ) +
          (Real.sin (-theta / 2) : ℂ) * Complex.I =
        star ((Real.cos (theta / 2) : ℂ) +
          (Real.sin (theta / 2) : ℂ) * Complex.I)
    rw [show -theta / 2 = -(theta / 2) by ring,
      Real.cos_neg, Real.sin_neg]
    simp

theorem star_equivPermutationMatrix
    {index : Type*} [Fintype index] [DecidableEq index]
    (equiv : index ≃ index) :
    star (equivPermutationMatrix equiv) =
      equivPermutationMatrix equiv.symm := by
  ext row column
  rw [_root_.Matrix.star_apply]
  simp only [equivPermutationMatrix]
  by_cases hit : column = equiv row
  · have reverseHit : row = equiv.symm column := by
      simpa using (congrArg equiv.symm hit).symm
    rw [if_pos hit, if_pos reverseHit]
    exact star_one ℂ
  · have reverseMiss : row ≠ equiv.symm column := by
      intro reverseHit
      apply hit
      simpa using (congrArg equiv reverseHit).symm
    rw [if_neg hit, if_neg reverseMiss]
    exact star_zero ℂ

theorem star_liftPrimitiveOneQubit {qubits : Nat} (target : Fin qubits)
    (gate : _root_.Matrix (Fin 2) (Fin 2) ℂ) :
    star (liftPrimitiveOneQubit target gate) =
      liftPrimitiveOneQubit target (star gate) := by
  ext row column
  simp only [liftPrimitiveOneQubit, _root_.Matrix.reindexAlgEquiv_apply,
    _root_.Matrix.reindex_apply, _root_.Matrix.submatrix_apply,
    _root_.Matrix.star_apply, _root_.Matrix.kroneckerMap_apply,
    _root_.Matrix.one_apply, Equiv.symm_symm]
  by_cases otherEqual :
      (splitPrimitiveWire target row).2 = (splitPrimitiveWire target column).2
  · rw [if_pos otherEqual.symm, if_pos otherEqual, StarMul.star_mul,
      star_one, one_mul, mul_one]
  · rw [if_neg (Ne.symm otherEqual), if_neg otherEqual, mul_zero,
      star_zero, mul_zero]

/-- Exact matrix denotation of one primitive instruction. -/
noncomputable def evalPrimitiveGate {qubits : Nat} : PrimitiveGate qubits →
    _root_.Matrix (PrimitiveBasis qubits) (PrimitiveBasis qubits) ℂ
  | .x target => equivPermutationMatrix (xBasisEquiv target)
  | .ry target angle => liftPrimitiveOneQubit target (standardRyMatrix angle.eval)
  | .rz target angle => liftPrimitiveOneQubit target (standardRzMatrix angle.eval)
  | .cx control target distinct =>
      equivPermutationMatrix (cxBasisEquiv control target distinct)

theorem evalPrimitiveGate_unitary {qubits : Nat} (gate : PrimitiveGate qubits) :
    evalPrimitiveGate gate ∈
      _root_.Matrix.unitaryGroup (PrimitiveBasis qubits) ℂ := by
  cases gate with
  | x target => exact equivPermutationMatrix_unitary _
  | ry target angle =>
      exact liftPrimitiveOneQubit_unitary target _ (standardRyMatrix_unitary _)
  | rz target angle =>
      exact liftPrimitiveOneQubit_unitary target _ (standardRzMatrix_unitary _)
  | cx control target distinct => exact equivPermutationMatrix_unitary _

theorem xBasisEquiv_symm {qubits : Nat} (target : Fin qubits) :
    (xBasisEquiv target).symm = xBasisEquiv target := by
  rfl

theorem cxBasisEquiv_symm {qubits : Nat} (control target : Fin qubits)
    (distinct : control ≠ target) :
    (cxBasisEquiv control target distinct).symm =
      cxBasisEquiv control target distinct := by
  rfl

theorem evalPrimitiveGate_dagger {qubits : Nat}
    (gate : PrimitiveGate qubits) :
    evalPrimitiveGate gate.dagger = star (evalPrimitiveGate gate) := by
  cases gate with
  | x target =>
      rw [evalPrimitiveGate, PrimitiveGate.dagger,
        star_equivPermutationMatrix, xBasisEquiv_symm]
      rfl
  | ry target angle =>
      simp only [PrimitiveGate.dagger, evalPrimitiveGate, ExactAngle.eval_neg,
        standardRyMatrix_neg]
      rw [star_liftPrimitiveOneQubit]
  | rz target angle =>
      simp only [PrimitiveGate.dagger, evalPrimitiveGate, ExactAngle.eval_neg,
        standardRzMatrix_neg]
      rw [star_liftPrimitiveOneQubit]
  | cx control target distinct =>
      rw [evalPrimitiveGate, PrimitiveGate.dagger,
        star_equivPermutationMatrix, cxBasisEquiv_symm]
      rfl

/-- Chronological circuit evaluation: later instructions multiply on the left. -/
noncomputable def evalPrimitiveCircuit {qubits : Nat} : PrimitiveCircuit qubits →
    _root_.Matrix (PrimitiveBasis qubits) (PrimitiveBasis qubits) ℂ
  | [] => 1
  | gate :: rest => evalPrimitiveCircuit rest * evalPrimitiveGate gate

theorem evalPrimitiveCircuit_unitary {qubits : Nat}
    (circuit : PrimitiveCircuit qubits) :
    evalPrimitiveCircuit circuit ∈
      _root_.Matrix.unitaryGroup (PrimitiveBasis qubits) ℂ := by
  induction circuit with
  | nil => exact (_root_.Matrix.unitaryGroup (PrimitiveBasis qubits) ℂ).one_mem
  | cons gate rest induction =>
      exact (_root_.Matrix.unitaryGroup (PrimitiveBasis qubits) ℂ).mul_mem
        induction (evalPrimitiveGate_unitary gate)

theorem evalPrimitiveCircuit_append {qubits : Nat}
    (left right : PrimitiveCircuit qubits) :
    evalPrimitiveCircuit (left ++ right) =
      evalPrimitiveCircuit right * evalPrimitiveCircuit left := by
  induction left with
  | nil => simp [evalPrimitiveCircuit]
  | cons gate rest induction =>
      simp only [List.cons_append, evalPrimitiveCircuit]
      rw [induction]
      simp [mul_assoc]

theorem evalPrimitiveCircuit_dagger {qubits : Nat}
    (circuit : PrimitiveCircuit qubits) :
    evalPrimitiveCircuit (circuit.reverse.map PrimitiveGate.dagger) =
      star (evalPrimitiveCircuit circuit) := by
  induction circuit with
  | nil => simp [evalPrimitiveCircuit]
  | cons gate rest induction =>
      simp only [List.reverse_cons, List.map_append, List.map_singleton,
        evalPrimitiveCircuit_append, evalPrimitiveCircuit]
      rw [induction, evalPrimitiveGate_dagger]
      simp

/-- Unit-modulus scalar represented by an exact global phase. -/
noncomputable def evalGlobalPhase (angle : ExactAngle) : ℂ :=
  Complex.exp ((angle.eval : ℂ) * Complex.I)

theorem evalGlobalPhase_unitary (angle : ExactAngle) :
    evalGlobalPhase angle ∈ unitary ℂ := by
  unfold evalGlobalPhase
  rw [Unitary.mem_iff]
  constructor
  · change (starRingEnd ℂ)
        (Complex.exp ((angle.eval : ℂ) * Complex.I)) * _ = 1
    rw [← Complex.exp_conj, ← Complex.exp_add]
    simp
  · change _ * (starRingEnd ℂ)
        (Complex.exp ((angle.eval : ℂ) * Complex.I)) = 1
    rw [← Complex.exp_conj, ← Complex.exp_add]
    simp

@[simp] theorem evalGlobalPhase_neg (angle : ExactAngle) :
    evalGlobalPhase (.neg angle) = star (evalGlobalPhase angle) := by
  unfold evalGlobalPhase
  rw [ExactAngle.eval_neg, Complex.star_def, ← Complex.exp_conj]
  congr 2
  simp

/-- Exact program semantics, with the same `exp(i phase)` convention used by
Qiskit and OpenQASM 3. -/
noncomputable def evalPrimitiveProgram {qubits : Nat}
    (program : PrimitiveProgram qubits) :
    _root_.Matrix (PrimitiveBasis qubits) (PrimitiveBasis qubits) ℂ :=
  evalGlobalPhase program.globalPhase • evalPrimitiveCircuit program.circuit

@[simp] theorem evalPrimitiveProgram_identity (qubits : Nat) :
    evalPrimitiveProgram (PrimitiveProgram.identity qubits) = 1 := by
  simp [evalPrimitiveProgram, evalGlobalPhase, PrimitiveProgram.identity,
    evalPrimitiveCircuit, ExactAngle.eval]

theorem evalPrimitiveProgram_seq {qubits : Nat}
    (left right : PrimitiveProgram qubits) :
    evalPrimitiveProgram (PrimitiveProgram.seq left right) =
      evalPrimitiveProgram right * evalPrimitiveProgram left := by
  simp only [evalPrimitiveProgram, PrimitiveProgram.seq,
    ExactAngle.eval_add, evalPrimitiveCircuit_append, evalGlobalPhase]
  rw [Complex.ofReal_add, add_mul, Complex.exp_add]
  ext row column
  simp only [_root_.Matrix.smul_apply, _root_.Matrix.mul_apply, smul_eq_mul]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro wire _
  ring

theorem evalPrimitiveProgram_unitary {qubits : Nat}
    (program : PrimitiveProgram qubits) :
    evalPrimitiveProgram program ∈
      _root_.Matrix.unitaryGroup (PrimitiveBasis qubits) ℂ := by
  exact Unitary.smul_mem_of_mem (evalGlobalPhase_unitary program.globalPhase)
    (evalPrimitiveCircuit_unitary program.circuit)

theorem evalPrimitiveProgram_dagger {qubits : Nat}
    (program : PrimitiveProgram qubits) :
    evalPrimitiveProgram program.dagger = star (evalPrimitiveProgram program) := by
  change evalGlobalPhase (.neg program.globalPhase) •
      evalPrimitiveCircuit
        (program.circuit.reverse.map PrimitiveGate.dagger) =
    star (evalGlobalPhase program.globalPhase •
      evalPrimitiveCircuit program.circuit)
  rw [evalGlobalPhase_neg, evalPrimitiveCircuit_dagger]
  simp

/-- A typed primitive refinement records exact equality, not equality up to phase. -/
structure PrimitiveRefinement (qubits : Nat) where
  circuit : PrimitiveCircuit qubits
  target : _root_.Matrix (PrimitiveBasis qubits) (PrimitiveBasis qubits) ℂ
  exact : evalPrimitiveCircuit circuit = target

end QuantumBlockEncoding
