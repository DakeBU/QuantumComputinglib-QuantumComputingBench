import Mathlib.LinearAlgebra.Matrix.Swap
import Mathlib.Tactic.FinCases
import QuantumBlockEncoding.ConcreteSemantics

/-!
# Textbook state-preparation certificates

This module closes two one-qubit examples all the way from the familiar gate
equation to a `ComplexStatePreparationCertificate`.  The proofs use Mathlib's
unitary-group predicate and concrete matrix-vector action; no Boolean proxy or
unproved oracle contract is involved.
-/

open scoped ComplexConjugate

namespace QuantumBlockEncoding.TextbookStatePreparation

open ConcreteSemantics

def zeroIndex : Fin (gridSize 1) := ⟨0, Nat.pow_pos (by decide)⟩

def oneIndex : Fin (gridSize 1) := ⟨1, by native_decide⟩

def pauliX : FiniteMatrix (gridSize 1) (gridSize 1) ℂ :=
  _root_.Matrix.swap ℂ zeroIndex oneIndex

/-- The Pauli X matrix is unitary in Mathlib's standard unitary group. -/
theorem pauliX_unitary :
    pauliX ∈ _root_.Matrix.unitaryGroup (Fin (gridSize 1)) ℂ := by
  rw [_root_.Matrix.mem_unitaryGroup_iff]
  rw [show star pauliX = pauliX by
    exact _root_.Matrix.conjTranspose_swap zeroIndex oneIndex]
  exact _root_.Matrix.swap_mul_self zeroIndex oneIndex

def oneState : StateVector (gridSize 1) ℂ :=
  basisKet (gridSize 1) oneIndex

def oneTarget : StatePreparationTarget ℂ 1 where
  amplitudes := oneState
  normalization := ∑ index, Complex.normSq (oneState index) = 1
  source := "Pauli X textbook example"

theorem oneTarget_normalized : oneTarget.normalization := by
  change ∑ index, Complex.normSq (oneState index) = 1
  rw [Fintype.sum_eq_single oneIndex]
  · simp [oneState, basisKet]
  · simp_all [oneState, basisKet]

theorem pauliX_prepares_one :
    applyVec pauliX (zeroKet 1) = oneTarget.amplitudes := by
  change (_root_.Matrix.swap ℂ zeroIndex oneIndex).mulVec (zeroKet 1) = oneState
  rw [_root_.Matrix.swap_mulVec]
  funext row
  simp only [Function.comp_apply]
  by_cases hzero : row = zeroIndex
  · subst row
    rw [Equiv.swap_apply_left]
    have h10 : oneIndex ≠ zeroBasisIndex 1 := by
      intro h
      have hval := congrArg Fin.val h
      norm_num [oneIndex, zeroBasisIndex] at hval
    have h01 : zeroIndex ≠ oneIndex := by
      intro h
      have hval := congrArg Fin.val h
      norm_num [zeroIndex, oneIndex] at hval
    simp [zeroKet, oneState, basisKet, Pi.single_apply, h10, h01]
  · have hone : row = oneIndex := by
      apply Fin.ext
      change row.val = 1
      have hlt := row.isLt
      change row.val < 2 at hlt
      have hne : row.val ≠ 0 := by
        intro hz
        apply hzero
        apply Fin.ext
        simpa [zeroIndex] using hz
      omega
    subst row
    rw [Equiv.swap_apply_right]
    simp [zeroKet, oneState, basisKet, Pi.single_apply,
      zeroBasisIndex, zeroIndex, oneIndex, Fin.mk.injEq]

def pauliXGate : ComplexUnitaryGate 1 where
  matrix := pauliX
  unitary := pauliX_unitary

def pauliXCertificate : ComplexStatePreparationCertificate 1 where
  target := oneTarget
  gate := pauliXGate
  normalizationProof := oneTarget_normalized
  preparationProof := pauliX_prepares_one

def pauliXCircuit : Circuit := [Gate.oneQubit "X" 0]

def pauliXVerified : VerifiedStatePreparation ℂ 1 :=
  pauliXCertificate.verified pauliXCircuit [[Gate.oneQubit "X" 0]]
    pauliXCircuit.resource

theorem pauliXVerified_cost :
    pauliXVerified.candidate.cost =
      { auxiliaryQubits := 0, gateCount := 1, depth := 1, oracleCalls := 0 } := by
  rfl

noncomputable def invSqrtTwo : ℂ :=
  (Real.sqrt 2 / 2 : ℝ)

theorem invSqrtTwo_mul_self : invSqrtTwo * invSqrtTwo = (1 : ℂ) / 2 := by
  rw [show invSqrtTwo * invSqrtTwo =
      ((Real.sqrt 2 / 2 * (Real.sqrt 2 / 2) : ℝ) : ℂ) by
    simp [invSqrtTwo]]
  rw [show Real.sqrt 2 / 2 * (Real.sqrt 2 / 2) = (1 : ℝ) / 2 by
    nlinarith [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]]
  norm_num

noncomputable def hadamard :
    FiniteMatrix (gridSize 1) (gridSize 1) ℂ :=
  fun row column =>
    if row.val = 1 ∧ column.val = 1 then -invSqrtTwo else invSqrtTwo

theorem star_hadamard : star hadamard = hadamard := by
  ext row column
  fin_cases row <;> fin_cases column <;>
    simp [hadamard, invSqrtTwo]

theorem hadamard_unitary :
    hadamard ∈ _root_.Matrix.unitaryGroup (Fin (gridSize 1)) ℂ := by
  rw [_root_.Matrix.mem_unitaryGroup_iff, star_hadamard]
  ext row column
  fin_cases row <;> fin_cases column <;>
    rw [_root_.Matrix.mul_apply, Finset.sum_fin_eq_sum_range] <;>
    simp [gridSize, hadamard, invSqrtTwo_mul_self,
      _root_.Matrix.one_apply] <;>
    norm_num [Finset.sum_range_succ]

noncomputable def plusState : StateVector (gridSize 1) ℂ :=
  fun _ => invSqrtTwo

noncomputable def plusTarget : StatePreparationTarget ℂ 1 where
  amplitudes := plusState
  normalization := ∑ index, Complex.normSq (plusState index) = 1
  source := "Hadamard textbook example"

theorem plusTarget_normalized : plusTarget.normalization := by
  change ∑ _index : Fin 2, Complex.normSq invSqrtTwo = 1
  rw [Fin.sum_univ_two]
  rw [show Complex.normSq invSqrtTwo = (1 : ℝ) / 2 by
    simp [invSqrtTwo, Complex.normSq_apply]]
  norm_num

theorem hadamard_prepares_plus :
    applyVec hadamard (zeroKet 1) = plusTarget.amplitudes := by
  have hcolumn :
      applyVec hadamard (zeroKet 1) =
        hadamard.col (zeroBasisIndex 1) :=
    applyVec_zeroKet hadamard
  rw [hcolumn]
  change hadamard.col (0 : Fin 2) = plusState
  funext row
  change hadamard row (zeroBasisIndex 1) = invSqrtTwo
  fin_cases row <;> simp [hadamard, zeroBasisIndex, gridSize]

noncomputable def hadamardGate : ComplexUnitaryGate 1 where
  matrix := hadamard
  unitary := hadamard_unitary

noncomputable def hadamardCertificate :
    ComplexStatePreparationCertificate 1 where
  target := plusTarget
  gate := hadamardGate
  normalizationProof := plusTarget_normalized
  preparationProof := hadamard_prepares_plus

def hadamardCircuit : Circuit := [Gate.oneQubit "H" 0]

noncomputable def hadamardVerified : VerifiedStatePreparation ℂ 1 :=
  hadamardCertificate.verified hadamardCircuit [[Gate.oneQubit "H" 0]]
    hadamardCircuit.resource

theorem hadamardVerified_cost :
    hadamardVerified.candidate.cost =
      { auxiliaryQubits := 0, gateCount := 1, depth := 1, oracleCalls := 0 } := by
  rfl

/-- The certified Pauli X example states the familiar textbook equation. -/
theorem pauliXCertificate_prepares_one :
    applyVec pauliXCertificate.gate.matrix (zeroKet 1) =
      pauliXCertificate.target.amplitudes :=
  pauliXCertificate.preparesVector

/-- The certified Hadamard example prepares the equal superposition. -/
theorem hadamardCertificate_prepares_plus :
    applyVec hadamardCertificate.gate.matrix (zeroKet 1) =
      hadamardCertificate.target.amplitudes :=
  hadamardCertificate.preparesVector

end QuantumBlockEncoding.TextbookStatePreparation
