import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Tactic

/- Internal finite rational supplier. No transcendental evaluation in the producer. -/
namespace HermiteFiniteTrig

def sinCoeff (i : ℕ) : ℚ := if i % 4 = 1 then 1 else if i % 4 = 3 then -1 else 0
def cosCoeff (i : ℕ) : ℚ := if i % 4 = 0 then 1 else if i % 4 = 2 then -1 else 0
def sinPoly (q : ℚ) (n : ℕ) : ℚ :=
  ∑ i ∈ Finset.range (n + 1), sinCoeff i * q ^ i / (i.factorial : ℚ)
def cosPoly (q : ℚ) (n : ℕ) : ℚ :=
  ∑ i ∈ Finset.range (n + 1), cosCoeff i * q ^ i / (i.factorial : ℚ)
def radius (q : ℚ) (n : ℕ) : ℚ := |q| ^ (n + 1) / ((n + 1).factorial : ℚ)
def sinBounds (q : ℚ) (n : ℕ) : ℚ × ℚ :=
  (sinPoly q n - radius q n, sinPoly q n + radius q n)
def cosBounds (q : ℚ) (n : ℕ) : ℚ × ℚ :=
  (cosPoly q n - radius q n, cosPoly q n + radius q n)

private theorem coeff_step (i : ℕ) :
    sinCoeff (i + 1) = cosCoeff i ∧ cosCoeff (i + 1) = -sinCoeff i := by
  have h : i % 4 < 4 := Nat.mod_lt i (by norm_num)
  interval_cases hi : i % 4 <;> simp [sinCoeff, cosCoeff, Nat.add_mod, hi]

theorem derivative_coeff (i : ℕ) :
    iteratedDeriv i Real.sin 0 = (sinCoeff i : ℝ) ∧
    iteratedDeriv i Real.cos 0 = (cosCoeff i : ℝ) := by
  induction i with
  | zero => simp [sinCoeff, cosCoeff]
  | succ i ih =>
    rw [Real.iteratedDeriv_add_one_sin,
      Real.iteratedDeriv_add_one_cos]
    simpa [ih.1, ih.2, (coeff_step i).1, (coeff_step i).2] using ih

private theorem sinPoly_zero (n : ℕ) : sinPoly 0 n = 0 := by
  unfold sinPoly
  rw [Finset.sum_eq_single 0]
  · norm_num [sinCoeff]
  · intro i hi hne
    simp [zero_pow hne]
  · simp

private theorem cosPoly_zero (n : ℕ) : cosPoly 0 n = 1 := by
  unfold cosPoly
  rw [Finset.sum_eq_single 0]
  · norm_num [cosCoeff]
  · intro i hi hne
    simp [zero_pow hne]
  · simp

private theorem taylor_eq_sum (f : ℝ → ℝ) (n : ℕ) (s : Set ℝ) (x : ℝ) :
    taylorWithinEval f n s 0 x =
      ∑ i ∈ Finset.range (n + 1), iteratedDerivWithin i f s 0 * x ^ i / (i.factorial : ℝ) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [taylorWithinEval_succ, Finset.sum_range_succ, ih]
    simp only [sub_zero, smul_eq_mul, Nat.factorial_succ, Nat.cast_mul, Nat.cast_add, Nat.cast_one]
    ring

private theorem sin_taylor (q : ℚ) (n : ℕ) (hq : (0 : ℝ) ≠ q) :
    taylorWithinEval Real.sin n (Set.uIcc 0 (q : ℝ)) 0 q = (sinPoly q n : ℝ) := by
  rw [taylor_eq_sum]
  simp only [sinPoly, Rat.cast_sum, Rat.cast_div, Rat.cast_mul, Rat.cast_pow, Rat.cast_natCast]
  apply Finset.sum_congr rfl
  intro i hi
  rw [iteratedDerivWithin_eq_iteratedDeriv (uniqueDiffOn_uIcc hq)
    Real.contDiff_sin.contDiffAt (Set.left_mem_uIcc), (derivative_coeff i).1]

private theorem cos_taylor (q : ℚ) (n : ℕ) (hq : (0 : ℝ) ≠ q) :
    taylorWithinEval Real.cos n (Set.uIcc 0 (q : ℝ)) 0 q = (cosPoly q n : ℝ) := by
  rw [taylor_eq_sum]
  simp only [cosPoly, Rat.cast_sum, Rat.cast_div, Rat.cast_mul, Rat.cast_pow, Rat.cast_natCast]
  apply Finset.sum_congr rfl
  intro i hi
  rw [iteratedDerivWithin_eq_iteratedDeriv (uniqueDiffOn_uIcc hq)
    Real.contDiff_cos.contDiffAt (Set.left_mem_uIcc), (derivative_coeff i).2]

theorem sin_error (q : ℚ) (n : ℕ) :
    |Real.sin (q : ℝ) - (sinPoly q n : ℝ)| ≤ (radius q n : ℝ) := by
  by_cases hq : (0 : ℝ) = q
  · have hq' : q = 0 := by exact_mod_cast hq.symm
    subst q
    simp [sinPoly_zero, radius]
  · obtain ⟨y, hy, he⟩ := taylor_mean_remainder_lagrange_iteratedDeriv hq
      (Real.contDiff_sin.contDiffOn (n := n + 1))
    rw [sin_taylor q n hq] at he
    rw [he, abs_div, abs_mul, abs_pow]
    simpa [radius, Rat.cast_div, Rat.cast_pow, Rat.cast_abs, Rat.cast_natCast] using
      div_le_div_of_nonneg_right
        (mul_le_mul_of_nonneg_right (Real.abs_iteratedDeriv_sin_le_one (n + 1) y)
          (by positivity : (0 : ℝ) ≤ |(q : ℝ) - 0| ^ (n + 1)))
        (by positivity : (0 : ℝ) ≤ |((n + 1).factorial : ℝ)|)

theorem cos_error (q : ℚ) (n : ℕ) :
    |Real.cos (q : ℝ) - (cosPoly q n : ℝ)| ≤ (radius q n : ℝ) := by
  by_cases hq : (0 : ℝ) = q
  · have hq' : q = 0 := by exact_mod_cast hq.symm
    subst q
    simp [cosPoly_zero, radius]
  · obtain ⟨y, hy, he⟩ := taylor_mean_remainder_lagrange_iteratedDeriv hq
      (Real.contDiff_cos.contDiffOn (n := n + 1))
    rw [cos_taylor q n hq] at he
    rw [he, abs_div, abs_mul, abs_pow]
    simpa [radius, Rat.cast_div, Rat.cast_pow, Rat.cast_abs, Rat.cast_natCast] using
      div_le_div_of_nonneg_right
        (mul_le_mul_of_nonneg_right (Real.abs_iteratedDeriv_cos_le_one (n + 1) y)
          (by positivity : (0 : ℝ) ≤ |(q : ℝ) - 0| ^ (n + 1)))
        (by positivity : (0 : ℝ) ≤ |((n + 1).factorial : ℝ)|)

theorem sin_mem (q : ℚ) (n : ℕ) :
    ((sinBounds q n).1 : ℝ) ≤ Real.sin (q : ℝ) ∧
    Real.sin (q : ℝ) ≤ ((sinBounds q n).2 : ℝ) := by
  have h := abs_le.mp (sin_error q n)
  simp only [sinBounds, Rat.cast_sub, Rat.cast_add]
  constructor <;> linarith

theorem cos_mem (q : ℚ) (n : ℕ) :
    ((cosBounds q n).1 : ℝ) ≤ Real.cos (q : ℝ) ∧
    Real.cos (q : ℝ) ≤ ((cosBounds q n).2 : ℝ) := by
  have h := abs_le.mp (cos_error q n)
  simp only [cosBounds, Rat.cast_sub, Rat.cast_add]
  constructor <;> linarith

theorem sin_width (q : ℚ) (n : ℕ) :
    (sinBounds q n).2 - (sinBounds q n).1 = 2 * radius q n := by
  simp only [sinBounds]; ring

theorem cos_width (q : ℚ) (n : ℕ) :
    (cosBounds q n).2 - (cosBounds q n).1 = 2 * radius q n := by
  simp only [cosBounds]; ring

end HermiteFiniteTrig
