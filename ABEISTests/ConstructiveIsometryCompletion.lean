import QuantumBlockEncoding.ConstructiveIsometryLocal

open scoped BigOperators
open QuantumBlockEncoding
open QuantumBlockEncoding.ConstructiveIsometryCompletion
open QuantumBlockEncoding.ConstructiveIsometryLocal

namespace ConstructiveSOChecks

def noColumns (N : ℕ) : _root_.Matrix (Fin N) (Fin 0) ℝ := fun _ => Fin.elim0

def noPositions (N : ℕ) : Fin 0 ↪ Fin N where
  toFun := Fin.elim0
  inj' a := Fin.elim0 a

example {N : ℕ} (hN : 0 < N) : complete hN (noColumns N) (noPositions N) = 1 := by
  simp [complete, placeColumns, orientColumns, extendPrefix, prefixCompletion,
    RectangularGivens.transform, RectangularGivens.decompose, RectangularGivens.sweepSteps,
    AdjacentGivens.stepsMatrix, permuteColumns]

def negativeColumn : _root_.Matrix (Fin 2) (Fin 1) ℝ := !![-1; 0]

def highPosition : Fin 1 ↪ Fin 2 where
  toFun := fun _ => 1
  inj' := by intro a b _; exact Subsingleton.elim a b

theorem negativeColumn_isometry : negativeColumn.transpose * negativeColumn = 1 := by
  ext a b
  fin_cases a
  fin_cases b
  norm_num [negativeColumn, _root_.Matrix.mul_apply, Fin.sum_univ_two]

example : Equiv.Perm.sign (extendPrefix (by decide) highPosition 1 le_rfl) = -1 := by decide

example : unusedPosition (by decide : 1 < 2) highPosition = 0 := by decide

example : complete (by decide : 1 < 2) negativeColumn highPosition 0 1 = -1 := by
  have h := (complete_spec (by decide) negativeColumn highPosition negativeColumn_isometry).2.2 0 0
  change complete (by decide : 1 < 2) negativeColumn highPosition 0 1 = negativeColumn 0 0 at h
  simpa [negativeColumn] using h

example : (complete (by decide : 1 < 2) negativeColumn highPosition).det = 1 :=
  (complete_spec (by decide) negativeColumn highPosition negativeColumn_isometry).2.1

/-- Non-coordinate rational column, negative second column, and non-prefix labels. -/
noncomputable def twoColumns : _root_.Matrix (Fin 3) (Fin 2) ℝ := !![3 / 5, 0; 4 / 5, 0; 0, -1]

def mixedPositions : Fin 2 ↪ Fin 3 where
  toFun := ![2, 0]
  inj' := by decide

theorem twoColumns_isometry : twoColumns.transpose * twoColumns = 1 := by
  ext a b
  fin_cases a <;> fin_cases b <;>
    norm_num [twoColumns, _root_.Matrix.mul_apply, Fin.sum_univ_succ]

example : extendPrefix (by decide) mixedPositions 2 le_rfl 0 = 2 ∧
    extendPrefix (by decide) mixedPositions 2 le_rfl 1 = 0 ∧
    unusedPosition (by decide : 2 < 3) mixedPositions = 1 := by decide

example : complete (by decide : 2 < 3) twoColumns mixedPositions 1 2 = 4 / 5 := by
  simpa [twoColumns, mixedPositions] using
    (complete_spec (by decide) twoColumns mixedPositions twoColumns_isometry).2.2 1 0

example : complete (by decide : 2 < 3) twoColumns mixedPositions 2 0 = -1 := by
  simpa [twoColumns, mixedPositions] using
    (complete_spec (by decide) twoColumns mixedPositions twoColumns_isometry).2.2 2 1

example : (complete (by decide : 2 < 3) twoColumns mixedPositions).transpose *
    complete (by decide : 2 < 3) twoColumns mixedPositions = 1 ∧
    (complete (by decide : 2 < 3) twoColumns mixedPositions).det = 1 :=
  ⟨(complete_spec (by decide) twoColumns mixedPositions twoColumns_isometry).1,
    (complete_spec (by decide) twoColumns mixedPositions twoColumns_isometry).2.1⟩

/-- Actual local register convention, including the zero-control one-wire case. -/
def signedLocal : _root_.Matrix (PrimitiveBasis 1) (Fin 1) ℝ :=
  fun row _ => if row 0 = 0 then 0 else -1

theorem signedLocal_isometry : signedLocal.transpose * signedLocal = 1 := by
  ext a b
  fin_cases a
  fin_cases b
  change (∑ row, signedLocal row 0 * signedLocal row 0) = 1
  rw [← (Equiv.funUnique (Fin 1) (Fin 2)).symm.sum_comp
    (fun row : PrimitiveBasis 1 => signedLocal row 0 * signedLocal row 0)]
  norm_num [signedLocal, Fin.sum_univ_two, Equiv.funUnique, Equiv.piUnique]

example : localCompletion (q := 0) (by decide) signedLocal (fun _ => 1)
    (TensorTrainLocalCompiler.activePositions (q := 0) (l := 1) (by decide) 0) = -1 := by
  simpa [signedLocal] using
    (localCompletion_spec (q := 0) (by decide) signedLocal signedLocal_isometry).2.2
      (fun _ => 1) 0

#check complete
#check complete_spec
#check completeNamed_spec
#check completeStage_spec
#print axioms sweep_prefix
#print axioms prefixCompletion_columns
#print axioms extendPrefix_agrees
#print axioms complete_spec
#print axioms completeNamed_spec
#print axioms completeStage_spec

end ConstructiveSOChecks
