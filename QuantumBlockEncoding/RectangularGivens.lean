import QuantumBlockEncoding.AdjacentGivens

/-!
# Deterministic rectangular adjacent-row elimination

The recurrence processes each column in order, with a bottom-up adjacent
Givens sweep when the pivot row exists. It returns its actual rotation list
and an upper-trapezoidal residual, with an exact orthogonal recovery map.
This is exact-real semantics, not an arithmetic evaluation cost theorem.
-/

namespace QuantumBlockEncoding.RectangularGivens

open AdjacentGivens

noncomputable def sweep {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ)
    (k : ℕ) : (remaining : ℕ) → k + remaining ≤ M →
      _root_.Matrix (Fin N) (Fin M) ℝ
  | 0, _ => A
  | remaining + 1, columns =>
      if h : k < N then
        sweep (columnSweep A ⟨k, by omega⟩ k (N - 1 - k) (by omega))
          (k + 1) remaining (by omega)
      else sweep A (k + 1) remaining (by omega)

noncomputable def sweepSteps {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ)
    (k : ℕ) : (remaining : ℕ) → k + remaining ≤ M → List (Step N)
  | 0, _ => []
  | remaining + 1, columns =>
      if h : k < N then
        columnSweepSteps A ⟨k, by omega⟩ k (N - 1 - k) (by omega) ++
          sweepSteps (columnSweep A ⟨k, by omega⟩ k (N - 1 - k) (by omega))
            (k + 1) remaining (by omega)
      else sweepSteps A (k + 1) remaining (by omega)

theorem sweepSteps_action {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ)
    (k remaining : ℕ) (columns : k + remaining ≤ M) :
    applySteps (sweepSteps A k remaining columns) A = sweep A k remaining columns := by
  induction remaining generalizing A k with
  | zero => rfl
  | succ remaining ih =>
      by_cases h : k < N
      · simp only [sweepSteps, sweep, dif_pos h, applySteps_append, columnSweepSteps_action]
        exact ih _ _ _
      · simp only [sweepSteps, sweep, dif_neg h]
        exact ih _ _ _

/-- Previously eliminated columns vanish strictly below their diagonal. -/
def UpperPrefix {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ) (k : ℕ) : Prop :=
  ∀ col : Fin M, col.val < k → ∀ row : Fin N, col.val < row.val → A row col = 0

theorem columnSweep_upperPrefix {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ)
    (col : Fin M) (h : col.val < N) (fixedPrefix : UpperPrefix A col.val) :
    UpperPrefix (columnSweep A col col.val (N - 1 - col.val) (by omega)) (col.val + 1) := by
  intro old oldLt row below
  by_cases same : old = col
  · subst old
    exact columnSweep_zeroed A col col.val _ _ row below (by omega)
  · have oldEarlier : old.val < col.val := by
      have unequal : old.val ≠ col.val := fun eq => same (Fin.ext eq)
      omega
    rw [columnSweep_preserves_zero_column]
    · exact fixedPrefix old oldEarlier row below
    · intro r lower upper
      exact fixedPrefix old oldEarlier r (by omega)

theorem sweep_upperPrefix {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ)
    (k remaining : ℕ) (columns : k + remaining ≤ M) (fixedPrefix : UpperPrefix A k) :
    UpperPrefix (sweep A k remaining columns) (k + remaining) := by
  induction remaining generalizing A k with
  | zero => simpa [sweep] using fixedPrefix
  | succ remaining ih =>
      by_cases h : k < N
      · rw [sweep, dif_pos h]
        have result := ih _ (k + 1) (by omega)
          (columnSweep_upperPrefix A ⟨k, by omega⟩ h fixedPrefix)
        simpa only [Nat.add_assoc, Nat.add_left_comm, Nat.add_comm] using result
      · rw [sweep, dif_neg h]
        have next : UpperPrefix A (k + 1) := by
          intro col oldLt row below
          exact fixedPrefix col (by omega) row below
        have result := ih A (k + 1) (by omega) next
        simpa only [Nat.add_assoc, Nat.add_left_comm, Nat.add_comm] using result

theorem sweepSteps_length_le {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ)
    (k remaining : ℕ) (columns : k + remaining ≤ M) :
    (sweepSteps A k remaining columns).length ≤ N * remaining := by
  induction remaining generalizing A k with
  | zero => simp [sweepSteps]
  | succ remaining ih =>
      by_cases h : k < N
      · simp only [sweepSteps, dif_pos h, List.length_append, columnSweepSteps_length]
        have next := ih (columnSweep A ⟨k, by omega⟩ k (N - 1 - k) (by omega))
          (k + 1) (by omega)
        rw [Nat.mul_succ]
        omega
      · simp only [sweepSteps, dif_neg h]
        exact (ih A (k + 1) (by omega)).trans (Nat.mul_le_mul_left N (by omega))

theorem stepsMatrix_orthogonal {N : ℕ} (steps : List (Step N)) :
    (stepsMatrix steps).transpose * stepsMatrix steps = 1 := by
  induction steps with
  | nil => simp [stepsMatrix]
  | cons step rest ih =>
      simp only [stepsMatrix, _root_.Matrix.transpose_mul, _root_.Matrix.mul_assoc]
      rw [← _root_.Matrix.mul_assoc (stepsMatrix rest).transpose, ih,
        _root_.Matrix.one_mul]
      exact planeMatrix_orthogonal _ _ step.distinct _

theorem stepsMatrix_det {N : ℕ} (steps : List (Step N)) :
    (stepsMatrix steps).det = 1 := by
  induction steps with
  | nil => simp [stepsMatrix]
  | cons step rest ih =>
      rw [stepsMatrix, _root_.Matrix.det_mul, ih]
      rw [one_mul]
      change (planeMatrix step.first step.second step.angle).det = 1
      exact planeMatrix_det _ _ step.distinct step.angle

noncomputable def decompose {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ) :
    List (Step N) := sweepSteps A 0 M (by omega)

noncomputable def reduced {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ) :
    _root_.Matrix (Fin N) (Fin M) ℝ := sweep A 0 M (by omega)

noncomputable def transform {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ) :
    _root_.Matrix (Fin N) (Fin N) ℝ := stepsMatrix (decompose A)

theorem decompose_action {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ) :
    applySteps (decompose A) A = reduced A := sweepSteps_action A 0 M _

theorem transform_mul {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ) :
    transform A * A = reduced A := by
  rw [← decompose_action, applySteps_eq_matrix_mul]
  rfl

theorem reduced_zero_below {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ)
    (row : Fin N) (col : Fin M) (below : col.val < row.val) :
    reduced A row col = 0 := by
  exact sweep_upperPrefix A 0 M (by omega) (by intro col impossible; omega)
    col (by simpa using col.isLt) row below

theorem decompose_length_le {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ) :
    (decompose A).length ≤ N * M := sweepSteps_length_le A 0 M _

theorem transform_orthogonal {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ) :
    (transform A).transpose * transform A = 1 := stepsMatrix_orthogonal _

theorem transform_det {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ) :
    (transform A).det = 1 := stepsMatrix_det _

theorem exact_recovery {N M : ℕ} (A : _root_.Matrix (Fin N) (Fin M) ℝ) :
    (transform A).transpose * reduced A = A := by
  rw [← transform_mul, ← _root_.Matrix.mul_assoc, transform_orthogonal,
    _root_.Matrix.one_mul]

end QuantumBlockEncoding.RectangularGivens
