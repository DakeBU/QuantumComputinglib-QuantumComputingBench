import QuantumBlockEncoding.RealIsometryCompletion

open QuantumBlockEncoding.RealIsometryCompletion

noncomputable section

def nonPrefixPosition : Fin 1 ↪ Fin 3 :=
  ⟨fun _ => 2, fun _ _ _ => Subsingleton.elim _ _⟩

def rationalColumn : _root_.Matrix (Fin 3) (Fin 1) ℝ :=
  fun i _ => if i = 0 then 3 / 5 else if i = 1 then 4 / 5 else 0

example : ∃ U : _root_.Matrix (Fin 3) (Fin 3) ℝ,
    U.transpose * U = 1 ∧ U.det = 1 ∧ ∀ i a, U i (nonPrefixPosition a) = rationalColumn i a := by
  apply exists_specialOrthogonal_completion (by norm_num)
  ext a b
  fin_cases a
  fin_cases b
  have h21 : (2 : Fin 3) ≠ (1 : Fin 3) := by decide
  norm_num [rationalColumn, _root_.Matrix.mul_apply, _root_.Matrix.transpose_apply,
    _root_.Matrix.one_apply, Fin.sum_univ_succ, h21]

-- A negative initial orientation still admits an SO completion because two
-- columns remain unspecified.
example : ∃ U : _root_.Matrix (Fin 3) (Fin 3) ℝ,
    U.transpose * U = 1 ∧ U.det = 1 ∧
    ∀ i a : Fin 1, U (Fin.castLE (by norm_num) i) (nonPrefixPosition a) = -1 := by
  let V : _root_.Matrix (Fin 3) (Fin 1) ℝ := fun i _ => if i = 0 then -1 else 0
  have hV : V.transpose * V = 1 := by
    ext a b
    fin_cases a
    fin_cases b
    change (∑ i : Fin 3, (if i = 0 then (-1 : ℝ) else 0) *
      (if i = 0 then (-1 : ℝ) else 0)) = 1
    norm_num [Fin.sum_univ_succ]
  obtain ⟨U, hU, hd, hc⟩ := exists_specialOrthogonal_completion (by norm_num : 1 < 3)
    V nonPrefixPosition hV
  refine ⟨U, hU, hd, ?_⟩
  intro i a
  fin_cases i
  simpa [V] using hc 0 a

-- Zero prescribed columns are included.
example : ∃ U : _root_.Matrix (Fin 2) (Fin 2) ℝ,
    U.transpose * U = 1 ∧ U.det = 1 := by
  let e : Fin 0 ↪ Fin 2 := ⟨Fin.elim0, fun a => Fin.elim0 a⟩
  obtain ⟨U, hU, hd, _⟩ := exists_specialOrthogonal_completion (by norm_num : 0 < 2)
    (0 : _root_.Matrix (Fin 2) (Fin 0) ℝ) e (Subsingleton.elim _ _)
  exact ⟨U, hU, hd⟩

-- The orthogonal theorem also includes the completely empty space.
example : ∃ U : _root_.Matrix (Fin 0) (Fin 0) ℝ, U.transpose * U = 1 := by
  obtain ⟨U, hU, _⟩ := exists_orthogonal_completion
    (1 : _root_.Matrix (Fin 0) (Fin 0) ℝ) (Function.Embedding.refl _) (by simp)
  exact ⟨U, hU⟩

-- Without a spare column, prescribed orientation can obstruct SO completion.
example : ¬ ∃ U : _root_.Matrix (Fin 1) (Fin 1) ℝ, U.det = 1 ∧ U 0 0 = -1 := by
  rintro ⟨U, hd, hu⟩
  simp only [_root_.Matrix.det_fin_one, hu] at hd
  norm_num at hd

#print axioms exists_orthogonal_completion
#print axioms signFlip_orthogonal
#print axioms signFlip_det
#print axioms mul_signFlip_preserves
#print axioms exists_specialOrthogonal_completion_of_unused
#print axioms exists_specialOrthogonal_completion
