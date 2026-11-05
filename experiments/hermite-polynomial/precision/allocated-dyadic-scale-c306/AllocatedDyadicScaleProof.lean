import AllocatedPolynomialCostInterface

namespace HermiteAllocatedPolynomialCost

/-- First C295 target only: remove the smoothness-dependent factor from the
dyadic precision scale, without changing the actual allocation or producer. -/
theorem scaleDyadicBound : intendedScaleDyadicBound := by
  unfold intendedScaleDyadicBound
  intro k n epsilon hepsilon
  have hk : k + 1 ≤ 2^k := by
    induction k with
    | zero => norm_num
    | succ k ih =>
      rw [pow_succ]
      omega
  have hfactor : (4 : ℚ) * ((k+1 : ℕ) : ℚ)^2 ≤ (2 : ℚ)^(2*k+2) := by
    calc
      _ ≤ 4 * ((2 : ℚ)^k)^2 := by
        gcongr
        exact_mod_cast hk
      _ = (2 : ℚ)^(2*k+2) := by
        rw [show 2*k+2 = k*2+2 by omega, pow_add, pow_mul]
        norm_num <;> ring
  have hceil : 1/epsilon ≤ (max 1 (Nat.ceil (1/epsilon)) : ℚ) :=
    (Nat.le_ceil _).trans
      (by exact_mod_cast le_max_right 1 (Nat.ceil (1/epsilon)))
  have hpow : max 1 (Nat.ceil (1/epsilon)) ≤
      2^(HermiteFiniteExp.tailCutoff epsilon) := by
    unfold HermiteFiniteExp.tailCutoff
    exact Nat.le_pow_clog (by norm_num) _
  have hinv : 1/epsilon ≤ (2 : ℚ)^(HermiteFiniteExp.tailCutoff epsilon) :=
    hceil.trans (by exact_mod_cast hpow)
  have hscaled : 1/(epsilon/(4 * ((k+1 : ℕ) : ℚ)^2)) ≤
      (2 : ℚ)^(2*k+2+HermiteFiniteExp.tailCutoff epsilon) := by
    calc
      _ = (4 * ((k+1 : ℕ) : ℚ)^2) * (1/epsilon) := by
        field_simp [ne_of_gt hepsilon] <;> ring
      _ ≤ (2 : ℚ)^(2*k+2) * (2 : ℚ)^(HermiteFiniteExp.tailCutoff epsilon) := by
        exact mul_le_mul hfactor hinv (by positivity) (by positivity)
      _ = _ := (pow_add _ _ _).symm
  have hcut : HermiteFiniteExp.tailCutoff
      (epsilon/(4 * ((k+1 : ℕ) : ℚ)^2)) ≤
      2*k+2+HermiteFiniteExp.tailCutoff epsilon := by
    unfold HermiteFiniteExp.tailCutoff
    apply (Nat.clog_le_iff_le_pow (by norm_num : 1 < 2)).mpr
    apply max_le
    · exact one_le_pow₀ (by norm_num : (1 : ℕ) ≤ 2)
    · apply Nat.ceil_le.mpr
      exact_mod_cast hscaled
  unfold operationScale
  omega

end HermiteAllocatedPolynomialCost
