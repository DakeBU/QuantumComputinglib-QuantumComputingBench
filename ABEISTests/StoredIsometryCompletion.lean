import QuantumBlockEncoding.StoredIsometryCompletion

namespace StoredIsometryCompletionTests

open QuantumBlockEncoding StoredGivens StoredIsometryCompletion

def noPositions (N : ℕ) : Positions N 0 :=
  ⟨#v[], by intro a; exact Fin.elim0 a⟩

def noColumns (N : ℕ) : StoredMatrix N 0 := Vector.replicate N #v[]

example {N : ℕ} (hN : 0 < N) :
    denote (complete hN (noColumns N) (noPositions N)).value = 1 := by
  rw [complete_value]
  simp [ConstructiveIsometryCompletion.complete, ConstructiveIsometryCompletion.placeColumns,
    ConstructiveIsometryCompletion.orientColumns, ConstructiveIsometryCompletion.extendPrefix,
    ConstructiveIsometryCompletion.prefixCompletion, RectangularGivens.transform,
    RectangularGivens.decompose, RectangularGivens.sweepSteps, AdjacentGivens.stepsMatrix,
    ConstructiveIsometryCompletion.permuteColumns]

def highPosition : Positions 2 1 :=
  ⟨#v[1], by intro a b _; exact Subsingleton.elim a b⟩

example : (permutation (by decide) highPosition 1 le_rfl).value.forward[0] = 1 ∧
    (permutation (by decide) highPosition 1 le_rfl).value.inverse[1] = 0 := by
  rw [permutation_forward (by decide : 1 ≤ 2) highPosition 1 le_rfl ⟨0, by decide⟩,
    permutation_inverse (by decide : 1 ≤ 2) highPosition 1 le_rfl ⟨1, by decide⟩]
  decide

example : (permutation (by decide) highPosition 1 le_rfl).value.polarity = -1 := by
  rw [permutation_polarity]
  have h : Equiv.Perm.sign
      (ConstructiveIsometryCompletion.extendPrefix (by decide) highPosition.embedding 1 le_rfl) = -1 := by
    decide
  simp [realSign, h]

noncomputable def identity2 : StoredMatrix 2 2 := #v[#v[1, 0], #v[0, 1]]

/-- The odd physical permutation flips the unused column, not an active one. -/
example : denote (placeColumns (by decide : 1 < 2) highPosition identity2).value 1 0 = -1 := by
  rw [placeColumns_value]
  norm_num [ConstructiveIsometryCompletion.placeColumns,
    ConstructiveIsometryCompletion.orientColumns, ConstructiveIsometryCompletion.extendPrefix,
    ConstructiveIsometryCompletion.unusedPosition, ConstructiveIsometryCompletion.permuteColumns,
    highPosition, Positions.embedding, Equiv.Perm.sign_trans, Equiv.Perm.sign_swap',
    RealIsometryCompletion.signFlip, _root_.Matrix.mul_diagonal,
    _root_.Matrix.submatrix_apply, denote, identity2, Equiv.swap_apply_def]

noncomputable def negativeColumn : StoredMatrix 2 1 := #v[#v[-1], #v[0]]

theorem negativeColumn_isometry : (denote negativeColumn).transpose * denote negativeColumn = 1 := by
  ext a b
  fin_cases a
  fin_cases b
  norm_num [negativeColumn, denote, _root_.Matrix.mul_apply, Fin.sum_univ_two]

example : denote (complete (by decide : 1 < 2) negativeColumn highPosition).value 0 1 = -1 := by
  simpa [negativeColumn, denote, highPosition, Positions.embedding] using
    (complete_spec (by decide) negativeColumn highPosition negativeColumn_isometry).2.2 0 0

example : (denote (complete (by decide : 1 < 2) negativeColumn highPosition).value).det = 1 :=
  (complete_spec (by decide) negativeColumn highPosition negativeColumn_isometry).2.1

def mixedPositions : Positions 3 2 := ⟨#v[2, 0], by decide⟩

noncomputable def mixedColumns : StoredMatrix 3 2 := #v[#v[3 / 5, 0], #v[4 / 5, 0], #v[0, -1]]

theorem mixedColumns_isometry : (denote mixedColumns).transpose * denote mixedColumns = 1 := by
  have entries : denote mixedColumns = !![3 / 5, 0; 4 / 5, 0; 0, -1] := by
    ext i j
    fin_cases i <;> fin_cases j <;> rfl
  rw [entries]
  ext a b
  fin_cases a <;> fin_cases b <;>
    norm_num [_root_.Matrix.mul_apply, Fin.sum_univ_succ]

example : denote (complete (by decide : 2 < 3) mixedColumns mixedPositions).value 1 2 = 4 / 5 := by
  simpa [mixedColumns, denote, mixedPositions, Positions.embedding] using
    (complete_spec (by decide) mixedColumns mixedPositions mixedColumns_isometry).2.2 1 0

example : denote (complete (by decide : 2 < 3) mixedColumns mixedPositions).value 2 0 = -1 := by
  simpa [mixedColumns, denote, mixedPositions, Positions.embedding] using
    (complete_spec (by decide) mixedColumns mixedPositions mixedColumns_isometry).2.2 2 1

example : (permutation (by decide) mixedPositions 2 le_rfl).value.forward[2] = 1 := by
  rw [permutation_forward (by decide : 2 ≤ 3) mixedPositions 2 le_rfl ⟨2, by decide⟩]
  decide

example (U : StoredMatrix 3 3) : (signColumn U 2).cost .field = 3 ∧
    (signColumn U 2).cost .read = 21 ∧ (signColumn U 2).cost .write = 15 := by
  simp [signColumn_cost, signBudget, tick]

example (p : PermutationTable 3) :
    (swapPermutation p 1 1).value.polarity = p.polarity := by
  simp [swapPermutation_polarity]

example (V : StoredMatrix 3 2) :
    StoredRectangularGivens.total (complete (by decide) V mixedPositions).cost ≤ 1336 := by
  simpa using complete_total_cost_le (by decide) V mixedPositions

example (V : Run (StoredMatrix 3 2)) (e : Run (Positions 3 2)) (op : Op) :
    (completeFrom (by decide) V e).cost op ≤
      V.cost op + e.cost op + polynomialBudget 3 2 op := completeFrom_cost_le _ _ _ _

#print axioms QuantumBlockEncoding.StoredIsometryCompletion.permutation_forward
#print axioms QuantumBlockEncoding.StoredIsometryCompletion.permutation_inverse
#print axioms QuantumBlockEncoding.StoredIsometryCompletion.permutation_polarity
#print axioms QuantumBlockEncoding.StoredIsometryCompletion.placeColumns_value
#print axioms QuantumBlockEncoding.StoredIsometryCompletion.complete_value
#print axioms QuantumBlockEncoding.StoredIsometryCompletion.complete_spec
#print axioms QuantumBlockEncoding.StoredIsometryCompletion.complete_total_cost_le
#print axioms QuantumBlockEncoding.StoredIsometryCompletion.completeFrom_cost_le

end StoredIsometryCompletionTests
