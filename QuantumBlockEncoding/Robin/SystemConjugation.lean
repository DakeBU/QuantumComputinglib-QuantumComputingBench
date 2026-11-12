import QuantumBlockEncoding.Robin.ComplexLCUProjection
import Mathlib.Tactic

/-!
# System-register basis conjugation for logical block encodings

This module lifts a finite system unitary through coefficient and selector
registers.  It proves that conjugating a logical LCU matrix by this lift
conjugates its clean system block by the original system unitary.  The result
is independent of the Robin benchmark and is reusable for other structured
basis reductions.
-/

namespace QuantumBlockEncoding.Robin.ComplexLCU

open scoped Kronecker

/-- Lift a system-register matrix through coefficient and selector identities. -/
def systemLift
    {coefficient selector system : Type*}
    [Fintype coefficient] [DecidableEq coefficient]
    [Fintype selector] [DecidableEq selector]
    [Fintype system] [DecidableEq system]
    (operator : _root_.Matrix system system ℂ) :
    _root_.Matrix
      (LCUIndex coefficient selector system)
      (LCUIndex coefficient selector system) ℂ :=
  (1 : _root_.Matrix coefficient coefficient ℂ) ⊗ₖ
    ((1 : _root_.Matrix selector selector ℂ) ⊗ₖ operator)

/-- A unitary system operation remains unitary after the identity lifts. -/
theorem systemLift_unitary
    {coefficient selector system : Type*}
    [Fintype coefficient] [DecidableEq coefficient]
    [Fintype selector] [DecidableEq selector]
    [Fintype system] [DecidableEq system]
    (operator : _root_.Matrix system system ℂ)
    (unitary : operator ∈ _root_.Matrix.unitaryGroup system ℂ) :
    systemLift (coefficient := coefficient) (selector := selector) operator ∈
      _root_.Matrix.unitaryGroup
        (LCUIndex coefficient selector system) ℂ := by
  apply _root_.Matrix.kronecker_mem_unitary
  · exact (_root_.Matrix.unitaryGroup coefficient ℂ).one_mem
  · apply _root_.Matrix.kronecker_mem_unitary
    · exact (_root_.Matrix.unitaryGroup selector ℂ).one_mem
    · exact unitary

/-- Entry formula: coefficient and selector are Kronecker deltas. -/
@[simp] theorem systemLift_apply
    {coefficient selector system : Type*}
    [Fintype coefficient] [DecidableEq coefficient]
    [Fintype selector] [DecidableEq selector]
    [Fintype system] [DecidableEq system]
    (operator : _root_.Matrix system system ℂ)
    (row column : LCUIndex coefficient selector system) :
    systemLift (coefficient := coefficient) (selector := selector) operator
        row column =
      if row.1 = column.1 ∧ row.2.1 = column.2.1 then
        operator row.2.2 column.2.2
      else 0 := by
  rcases row with ⟨coefficientRow, ⟨selectorRow, systemRow⟩⟩
  rcases column with ⟨coefficientColumn, ⟨selectorColumn, systemColumn⟩⟩
  by_cases coefficientMatch : coefficientRow = coefficientColumn <;>
    by_cases selectorMatch : selectorRow = selectorColumn <;>
    simp [systemLift, coefficientMatch, selectorMatch]

/-- Entry formula for the adjoint system lift. -/
@[simp] theorem star_systemLift_apply
    {coefficient selector system : Type*}
    [Fintype coefficient] [DecidableEq coefficient]
    [Fintype selector] [DecidableEq selector]
    [Fintype system] [DecidableEq system]
    (operator : _root_.Matrix system system ℂ)
    (row column : LCUIndex coefficient selector system) :
    star (systemLift (coefficient := coefficient) (selector := selector) operator)
        row column =
      if row.1 = column.1 ∧ row.2.1 = column.2.1 then
        star (operator column.2.2 row.2.2)
      else 0 := by
  change star
      (systemLift (coefficient := coefficient) (selector := selector) operator
        column row) = _
  rw [systemLift_apply]
  by_cases coefficientMatch : row.1 = column.1 <;>
    by_cases selectorMatch : row.2.1 = column.2.1 <;>
    simp [coefficientMatch, selectorMatch, eq_comm]

/-- Left multiplication by a lifted system matrix on a clean row. -/
theorem systemLift_mul_cleanRow
    {coefficient selector system columnType : Type*}
    [Fintype coefficient] [DecidableEq coefficient]
    [Fintype selector] [DecidableEq selector]
    [Fintype system] [DecidableEq system]
    [Fintype columnType]
    (systemOperator : _root_.Matrix system system ℂ)
    (operator : _root_.Matrix
      (LCUIndex coefficient selector system) columnType ℂ)
    (cleanCoefficient : coefficient) (cleanSelector : selector)
    (systemRow : system) (column : columnType) :
    (systemLift (coefficient := coefficient) (selector := selector)
        systemOperator * operator)
        (cleanCoefficient, (cleanSelector, systemRow)) column =
      ∑ intermediate : system,
        systemOperator systemRow intermediate *
          operator (cleanCoefficient, (cleanSelector, intermediate)) column := by
  classical
  rw [_root_.Matrix.mul_apply]
  simp_rw [Fintype.sum_prod_type]
  simp_rw [systemLift_apply]
  rw [Finset.sum_eq_single cleanCoefficient]
  · rw [Finset.sum_eq_single cleanSelector]
    · simp
    · intro candidate _ candidate_ne
      simp [Ne.symm candidate_ne]
    · simp
  · intro candidate _ candidate_ne
    simp [Ne.symm candidate_ne]
  · simp

/-- Right multiplication by the adjoint lift on a clean column. -/
theorem mul_star_systemLift_cleanColumn
    {rowType coefficient selector system : Type*}
    [Fintype rowType]
    [Fintype coefficient] [DecidableEq coefficient]
    [Fintype selector] [DecidableEq selector]
    [Fintype system] [DecidableEq system]
    (operator : _root_.Matrix rowType
      (LCUIndex coefficient selector system) ℂ)
    (systemOperator : _root_.Matrix system system ℂ)
    (row : rowType)
    (cleanCoefficient : coefficient) (cleanSelector : selector)
    (systemColumn : system) :
    (operator * star (systemLift (coefficient := coefficient)
        (selector := selector) systemOperator))
        row (cleanCoefficient, (cleanSelector, systemColumn)) =
      ∑ intermediate : system,
        operator row (cleanCoefficient, (cleanSelector, intermediate)) *
          star (systemOperator systemColumn intermediate) := by
  classical
  rw [_root_.Matrix.mul_apply]
  simp_rw [Fintype.sum_prod_type]
  simp_rw [star_systemLift_apply]
  rw [Finset.sum_eq_single cleanCoefficient]
  · rw [Finset.sum_eq_single cleanSelector]
    · simp
    · intro candidate _ candidate_ne
      simp [candidate_ne]
    · simp
  · intro candidate _ candidate_ne
    simp [candidate_ne]
  · simp

/-- Extract the coefficient/selector clean block as a system matrix. -/
noncomputable def cleanSystemBlock
    {coefficient selector system : Type*}
    (operator : _root_.Matrix
      (LCUIndex coefficient selector system)
      (LCUIndex coefficient selector system) ℂ)
    (cleanCoefficient : coefficient) (cleanSelector : selector) :
    _root_.Matrix system system ℂ := fun row column =>
  operator (cleanCoefficient, (cleanSelector, row))
    (cleanCoefficient, (cleanSelector, column))

/-- Conjugate a full logical matrix only on its system register. -/
noncomputable def conjugateSystem
    {coefficient selector system : Type*}
    [Fintype coefficient] [DecidableEq coefficient]
    [Fintype selector] [DecidableEq selector]
    [Fintype system] [DecidableEq system]
    (systemOperator : _root_.Matrix system system ℂ)
    (operator : _root_.Matrix
      (LCUIndex coefficient selector system)
      (LCUIndex coefficient selector system) ℂ) :
    _root_.Matrix
      (LCUIndex coefficient selector system)
      (LCUIndex coefficient selector system) ℂ :=
  systemLift (coefficient := coefficient) (selector := selector) systemOperator *
    (operator * star (systemLift (coefficient := coefficient)
      (selector := selector) systemOperator))

/-- System conjugation preserves unitarity. -/
theorem conjugateSystem_unitary
    {coefficient selector system : Type*}
    [Fintype coefficient] [DecidableEq coefficient]
    [Fintype selector] [DecidableEq selector]
    [Fintype system] [DecidableEq system]
    (systemOperator : _root_.Matrix system system ℂ)
    (operator : _root_.Matrix
      (LCUIndex coefficient selector system)
      (LCUIndex coefficient selector system) ℂ)
    (systemUnitary : systemOperator ∈
      _root_.Matrix.unitaryGroup system ℂ)
    (operatorUnitary : operator ∈
      _root_.Matrix.unitaryGroup
        (LCUIndex coefficient selector system) ℂ) :
    conjugateSystem systemOperator operator ∈
      _root_.Matrix.unitaryGroup
        (LCUIndex coefficient selector system) ℂ := by
  apply (_root_.Matrix.unitaryGroup
    (LCUIndex coefficient selector system) ℂ).mul_mem
  · exact systemLift_unitary systemOperator systemUnitary
  · apply (_root_.Matrix.unitaryGroup
      (LCUIndex coefficient selector system) ℂ).mul_mem
    · exact operatorUnitary
    · exact Unitary.star_mem
        (systemLift_unitary systemOperator systemUnitary)

/-- Conjugating the full logical matrix conjugates exactly its clean system block. -/
theorem cleanSystemBlock_conjugateSystem
    {coefficient selector system : Type*}
    [Fintype coefficient] [DecidableEq coefficient]
    [Fintype selector] [DecidableEq selector]
    [Fintype system] [DecidableEq system]
    (systemOperator : _root_.Matrix system system ℂ)
    (operator : _root_.Matrix
      (LCUIndex coefficient selector system)
      (LCUIndex coefficient selector system) ℂ)
    (cleanCoefficient : coefficient) (cleanSelector : selector) :
    cleanSystemBlock (conjugateSystem systemOperator operator)
        cleanCoefficient cleanSelector =
      systemOperator *
        (cleanSystemBlock operator cleanCoefficient cleanSelector *
          star systemOperator) := by
  classical
  ext row column
  unfold cleanSystemBlock conjugateSystem
  rw [systemLift_mul_cleanRow]
  simp_rw [mul_star_systemLift_cleanColumn]
  rw [_root_.Matrix.mul_apply]
  apply Finset.sum_congr rfl
  intro intermediate _
  congr 1

end QuantumBlockEncoding.Robin.ComplexLCU
