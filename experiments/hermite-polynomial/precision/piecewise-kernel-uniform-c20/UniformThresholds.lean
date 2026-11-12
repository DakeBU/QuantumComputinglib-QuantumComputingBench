import UniformComparison

namespace HermitePiecewiseUniform
open QuantumBlockEncoding TensorTrainCanonical StoredTensorTrain

def gridStepQ (width : ℕ) (R : ℚ) : ℚ := 2*R/(2:ℚ)^width
def strictCut (width : ℕ) (R s : ℚ) : ℕ :=
  min (2^width) (Nat.ceil ((s+R)/gridStepQ width R))
def inclusiveCut (width : ℕ) (R s : ℚ) : ℕ :=
  let q := (s+R)/gridStepQ width R
  min (2^width) (if q < 0 then 0 else Nat.floor q+1)

theorem strictCut_correct (width : ℕ) (R s : ℚ) (hR : 0 < R)
    (j : ℕ) (hj : j < 2^width) :
    j < strictCut width R s ↔ -R+2*R*(j:ℚ)/(2:ℚ)^width < s := by
  have hs : 0 < gridStepQ width R := by unfold gridStepQ; positivity
  simp only [strictCut, lt_min_iff, hj, true_and, Nat.lt_ceil]
  rw [lt_div_iff₀ hs]
  have hm : (j:ℚ)*gridStepQ width R = 2*R*(j:ℚ)/(2:ℚ)^width := by
    unfold gridStepQ
    ring
  rw [hm]
  constructor <;> intro h <;> linarith

theorem inclusiveCut_correct (width : ℕ) (R s : ℚ) (hR : 0 < R)
    (j : ℕ) (hj : j < 2^width) :
    j < inclusiveCut width R s ↔ -R+2*R*(j:ℚ)/(2:ℚ)^width ≤ s := by
  have hs : 0 < gridStepQ width R := by unfold gridStepQ; positivity
  have hmul : (j:ℚ)*gridStepQ width R = 2*R*(j:ℚ)/(2:ℚ)^width := by
    unfold gridStepQ
    ring
  by_cases hq : (s+R)/gridStepQ width R < 0
  · have hn : s+R < 0 := by
      have hh := (div_lt_iff₀ hs).mp hq
      simpa using hh
    have hj0 : 0 ≤ (j:ℚ)*gridStepQ width R := mul_nonneg (Nat.cast_nonneg _) hs.le
    simp only [inclusiveCut, hq, if_true, Nat.min_zero, Nat.not_lt_zero, false_iff]
    rw [← hmul]
    linarith
  · simp only [inclusiveCut, hq, if_false, lt_min_iff, hj, true_and,
      Nat.lt_add_one_iff, Nat.le_floor_iff (le_of_not_gt hq)]
    rw [le_div_iff₀ hs, hmul]
    constructor <;> intro h <;> linarith

theorem stored_strict_grid_mask (n : ℕ) (R s : ℚ) (hR : 0 < R) (x : Word (n+1)) :
    contract (denoteChain (produceComparison n (strictCut (n+1) R s)).run.value) x 0 0 =
      if -R+2*R*(wordValue x:ℚ)/(2:ℚ)^(n+1) < s then 1 else 0 := by
  rw [stored_comparison_contract n (strictCut (n+1) R s)
    (by unfold strictCut; exact min_le_left _ _) x]
  simp only [strictCut_correct _ _ _ hR _ (wordValue_lt _ x)]

theorem stored_inclusive_grid_mask (n : ℕ) (R s : ℚ) (hR : 0 < R) (x : Word (n+1)) :
    contract (denoteChain (produceComparison n (inclusiveCut (n+1) R s)).run.value) x 0 0 =
      if -R+2*R*(wordValue x:ℚ)/(2:ℚ)^(n+1) ≤ s then 1 else 0 := by
  rw [stored_comparison_contract n (inclusiveCut (n+1) R s)
    (by unfold inclusiveCut; exact min_le_left _ _) x]
  simp only [inclusiveCut_correct _ _ _ hR _ (wordValue_lt _ x)]

#print axioms strictCut_correct
#print axioms inclusiveCut_correct
#print axioms stored_strict_grid_mask
#print axioms stored_inclusive_grid_mask
end HermitePiecewiseUniform
