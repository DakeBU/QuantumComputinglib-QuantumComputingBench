import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Data.Nat.Log
import Mathlib.Data.Nat.Size
import Mathlib.Algebra.Order.Floor.Ring
import Mathlib.Tactic

namespace HermiteFiniteExp

def poly (q : ℚ) (n : ℕ) : ℚ :=
  ∑ i ∈ Finset.range (n+1), q^i/(i.factorial : ℚ)
def radius (q : ℚ) (n : ℕ) : ℚ := |q|^(n+1)/((n+1).factorial : ℚ)
def tailRadius (T : ℕ) : ℚ := 1/(2 : ℚ)^T
def bounds (q : ℚ) (T n : ℕ) : ℚ × ℚ :=
  if q ≤ -(T : ℚ) then (0, tailRadius T)
  else (poly q n-radius q n, poly q n+radius q n)
def checked (q epsilon : ℚ) (T n : ℕ) : Option (ℚ × ℚ) :=
  if q ≤ 0 ∧ 0 < epsilon ∧ (bounds q T n).2-(bounds q T n).1 ≤ epsilon
  then some (bounds q T n) else none
def tailCutoff (epsilon : ℚ) : ℕ :=
  Nat.clog 2 (max 1 (Nat.ceil (1/epsilon)))

private theorem taylor_eq_sum (f : ℝ → ℝ) (n : ℕ) (s : Set ℝ) (x : ℝ) :
    taylorWithinEval f n s 0 x =
      ∑ i ∈ Finset.range (n+1), iteratedDerivWithin i f s 0*x^i/(i.factorial : ℝ) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [taylorWithinEval_succ, Finset.sum_range_succ, ih]
    simp only [sub_zero, smul_eq_mul, Nat.factorial_succ, Nat.cast_mul,
      Nat.cast_add, Nat.cast_one]
    ring

private theorem exp_iterated (n : ℕ) : iteratedDeriv n Real.exp = Real.exp := by
  rw [iteratedDeriv_eq_iterate, Real.iter_deriv_exp]

private theorem exp_taylor (q : ℚ) (n : ℕ) (hq : (0 : ℝ) ≠ q) :
    taylorWithinEval Real.exp n (Set.uIcc 0 (q : ℝ)) 0 q = (poly q n : ℝ) := by
  rw [taylor_eq_sum]
  simp only [poly, Rat.cast_sum, Rat.cast_div, Rat.cast_pow, Rat.cast_natCast]
  apply Finset.sum_congr rfl
  intro i _
  rw [iteratedDerivWithin_eq_iteratedDeriv (uniqueDiffOn_uIcc hq)
    Real.contDiff_exp.contDiffAt Set.left_mem_uIcc, exp_iterated]
  simp

private theorem poly_zero (n : ℕ) : poly 0 n = 1 := by
  unfold poly
  rw [Finset.sum_eq_single 0]
  · norm_num
  · intro i _ hne
    simp [zero_pow hne]
  · simp

theorem error (q : ℚ) (n : ℕ) (hq : q ≤ 0) :
    |Real.exp (q : ℝ)-(poly q n : ℝ)| ≤ (radius q n : ℝ) := by
  by_cases hz : (0 : ℝ) = q
  · have hz' : q = 0 := by exact_mod_cast hz.symm
    subst q
    simp [poly_zero, radius]
  · obtain ⟨y, hy, he⟩ := taylor_mean_remainder_lagrange_iteratedDeriv hz
      (Real.contDiff_exp.contDiffOn (n := n+1))
    have hqR : (q : ℝ) ≤ 0 := by exact_mod_cast hq
    have hy0 : y ≤ 0 := by
      rw [Set.uIoo_comm, Set.uIoo_of_le hqR] at hy
      exact hy.2.le
    have hd : |iteratedDeriv (n+1) Real.exp y| ≤ 1 := by
      rw [exp_iterated, abs_of_pos (Real.exp_pos y)]
      exact Real.exp_le_one_iff.mpr hy0
    rw [exp_taylor q n hz] at he
    rw [he, abs_div, abs_mul, abs_pow]
    simpa [radius, Rat.cast_div, Rat.cast_pow, Rat.cast_abs, Rat.cast_natCast] using
      div_le_div_of_nonneg_right
        (mul_le_mul_of_nonneg_right hd
          (by positivity : (0 : ℝ) ≤ |(q : ℝ)-0|^(n+1)))
        (by positivity : (0 : ℝ) ≤ |((n+1).factorial : ℝ)|)

theorem tail_bound (q : ℚ) (T : ℕ) (hq : q ≤ -(T : ℚ)) :
    Real.exp (q : ℝ) ≤ (tailRadius T : ℝ) := by
  have hqR : (q : ℝ) ≤ -(T : ℝ) := by exact_mod_cast hq
  have h2 : (2 : ℝ) ≤ Real.exp 1 := by linarith [Real.add_one_le_exp 1]
  calc
    Real.exp (q : ℝ) ≤ Real.exp (-(T : ℝ)) := Real.exp_le_exp.mpr hqR
    _ = ((Real.exp 1)^T)⁻¹ := by
      rw [Real.exp_neg]
      congr 1
      simpa using Real.exp_nat_mul 1 T
    _ ≤ ((2 : ℝ)^T)⁻¹ := (inv_le_inv₀ (by positivity) (by positivity)).mpr
      (pow_le_pow_left₀ (by norm_num) h2 T)
    _ = (tailRadius T : ℝ) := by simp [tailRadius, one_div]

theorem membership (q : ℚ) (T n : ℕ) (hq : q ≤ 0) :
    Real.exp (q : ℝ) ∈ Set.Icc ((bounds q T n).1 : ℝ) ((bounds q T n).2 : ℝ) := by
  by_cases hc : q ≤ -(T : ℚ)
  · simp only [bounds, if_pos hc, Rat.cast_zero, Set.mem_Icc]
    exact ⟨(Real.exp_pos _).le, tail_bound q T hc⟩
  · have he := abs_le.mp (error q n hq)
    simp only [bounds, if_neg hc, Rat.cast_sub, Rat.cast_add, Set.mem_Icc]
    constructor <;> linarith

theorem active_magnitude (q : ℚ) (T : ℕ) (hq : q ≤ 0)
    (hactive : ¬ q ≤ -(T : ℚ)) : |q| < (T : ℚ) := by
  rw [abs_of_nonpos hq]
  linarith [lt_of_not_ge hactive]

theorem checked_sound (q epsilon : ℚ) (T n : ℕ) (I : ℚ × ℚ)
    (h : checked q epsilon T n = some I) :
    0 < epsilon ∧ Real.exp (q : ℝ) ∈ Set.Icc (I.1 : ℝ) (I.2 : ℝ) ∧
      I.2-I.1 ≤ epsilon := by
  unfold checked at h
  split_ifs at h with hc
  · have hi : bounds q T n = I := Option.some.inj h
    subst I
    exact ⟨hc.2.1, membership q T n hc.1, hc.2.2⟩

theorem tailCutoff_budget (epsilon : ℚ) (he : 0 < epsilon) :
    tailRadius (tailCutoff epsilon) ≤ epsilon := by
  have ht : 1/epsilon ≤ (max 1 (Nat.ceil (1/epsilon)) : ℚ) :=
    (Nat.le_ceil _).trans (by exact_mod_cast le_max_right 1 (Nat.ceil (1/epsilon)))
  have hp : max 1 (Nat.ceil (1/epsilon)) ≤ 2^(tailCutoff epsilon) := by
    unfold tailCutoff
    exact Nat.le_pow_clog (by norm_num) _
  have hb : 1/epsilon ≤ (2 : ℚ)^(tailCutoff epsilon) :=
    ht.trans (by exact_mod_cast hp)
  unfold tailRadius
  apply (div_le_iff₀ (by positivity : (0 : ℚ) < 2^(tailCutoff epsilon))).mpr
  have h := (div_le_iff₀ he).mp hb
  nlinarith

theorem tailCutoff_size (epsilon : ℚ) :
    tailCutoff epsilon ≤ Nat.size (max 1 (Nat.ceil (1/epsilon))) := by
  unfold tailCutoff
  exact Nat.clog_le_of_le_pow (Nat.lt_size_self _).le

theorem checked_tail (q epsilon : ℚ) (n : ℕ) (he : 0 < epsilon)
    (hq : q ≤ -(tailCutoff epsilon : ℚ)) :
    checked q epsilon (tailCutoff epsilon) n =
      some (0, tailRadius (tailCutoff epsilon)) := by
  have hq0 : q ≤ 0 := by
    have : (0 : ℚ) ≤ tailCutoff epsilon := Nat.cast_nonneg _
    linarith
  simp [checked, bounds, hq, hq0, he, tailCutoff_budget epsilon he]

#print axioms error
#print axioms tail_bound
#print axioms membership
#print axioms active_magnitude
#print axioms checked_sound
#print axioms tailCutoff_budget
#print axioms tailCutoff_size
#print axioms checked_tail

end HermiteFiniteExp
