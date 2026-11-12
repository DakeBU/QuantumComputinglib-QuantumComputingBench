import PiecewiseSourceBudget

/-!
Internal parameter-budget provider for the actual allocated Taylor source.
The physical register count is `n + 1`.  This does not count producer time,
finite-bit arithmetic, angle synthesis, ancillas, or physical gates.
The selected root signature is fixed by the accompanying pre-proof seal.
-/

namespace HermiteAllocatedDegreeBudget

/-- Dyadic shrinking of a positive rational tolerance adds at most the
dyadic exponent to the literal ceiling/log cutoff. -/
theorem tailCutoff_div_pow_two_le (e : ℚ) (m : ℕ) (he : 0 < e) :
    HermiteFiniteExp.tailCutoff (e / (2 : ℚ)^m) ≤
      m + HermiteFiniteExp.tailCutoff e := by
  have hceil : 1/e ≤ (max 1 (Nat.ceil (1/e)) : ℚ) :=
    (Nat.le_ceil _).trans
      (by exact_mod_cast le_max_right 1 (Nat.ceil (1/e)))
  have hpow : max 1 (Nat.ceil (1/e)) ≤
      2^(HermiteFiniteExp.tailCutoff e) := by
    unfold HermiteFiniteExp.tailCutoff
    exact Nat.le_pow_clog (by norm_num) _
  have hinv : 1/e ≤ (2 : ℚ)^(HermiteFiniteExp.tailCutoff e) :=
    hceil.trans (by exact_mod_cast hpow)
  have hscaled : 1/(e/(2 : ℚ)^m) ≤
      (2 : ℚ)^(m + HermiteFiniteExp.tailCutoff e) := by
    calc
      1/(e/(2 : ℚ)^m) = (2 : ℚ)^m*(1/e) := by
        field_simp [ne_of_gt he] <;> ring
      _ ≤ (2 : ℚ)^m*(2 : ℚ)^(HermiteFiniteExp.tailCutoff e) :=
        mul_le_mul_of_nonneg_left hinv (by positivity)
      _ = (2 : ℚ)^(m + HermiteFiniteExp.tailCutoff e) :=
        (pow_add _ _ _).symm
  have hceil_scaled : Nat.ceil (1/(e/(2 : ℚ)^m)) ≤
      2^(m + HermiteFiniteExp.tailCutoff e) := by
    apply Nat.ceil_le.mpr
    exact_mod_cast hscaled
  unfold HermiteFiniteExp.tailCutoff
  apply (Nat.clog_le_iff_le_pow (by norm_num : 1 < 2)).mpr
  exact max_le (one_le_pow₀ (by norm_num : (1 : ℕ) ≤ 2)) hceil_scaled

/-- Exact factorization of the allocation, including the physical `n + 1`
and the exponential part of the literal amplification factor. -/
theorem sourceDelta_factorization (k n : ℕ) (epsilon : ℚ) :
    HermitePiecewiseSourceBudget.sourceDelta k n epsilon =
      (epsilon / (4 * ((k+1 : ℕ) : ℚ)^2)) /
        (2 : ℚ)^(n + 1 + 2*k) := by
  unfold HermitePiecewiseSourceBudget.sourceDelta
    HermiteFiniteMiddleSource.amplificationQ
  simp only [Nat.cast_add, Nat.cast_one, div_div, pow_add]
  congr 1
  ring

/-- A stronger intermediate bound on the actual cutoff, not an assumed
correctness or resource premise of the selected root. -/
theorem allocated_tailCutoff_le (k n : ℕ) (epsilon : ℚ)
    (hepsilon : 0 < epsilon) :
    HermiteFiniteExp.tailCutoff
      (HermitePiecewiseSourceBudget.sourceDelta k n epsilon) ≤
      n + 1 + 2*k + HermiteFiniteExp.tailCutoff
        (epsilon / (4 * ((k+1 : ℕ) : ℚ)^2)) := by
  rw [sourceDelta_factorization]
  apply tailCutoff_div_pow_two_le
  positivity

theorem allocated_sourceDegree_le (k n : ℕ) (epsilon : ℚ) (hepsilon : 0 < epsilon) :
    HermiteFiniteExpDegree.sourceDegree
      (HermitePiecewiseSourceBudget.sourceDelta k n epsilon) ≤
    4 * (n + 1 + 2*k + HermiteFiniteExp.tailCutoff
      (epsilon / (4 * ((k+1 : ℕ) : ℚ)^2)))^2 +
    2 * (n + 1 + 2*k + HermiteFiniteExp.tailCutoff
      (epsilon / (4 * ((k+1 : ℕ) : ℚ)^2))) + 1 := by
  unfold HermiteFiniteExpDegree.sourceDegree
  rw [HermiteFiniteExpDegree.degree_formula]
  have h := allocated_tailCutoff_le k n epsilon hepsilon
  gcongr <;> exact h

end HermiteAllocatedDegreeBudget
