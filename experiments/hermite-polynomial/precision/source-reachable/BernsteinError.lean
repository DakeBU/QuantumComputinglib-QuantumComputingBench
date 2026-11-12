import QuantumBlockEncoding.HermiteBernstein

/-! Internal producer-error interfaces. These do not assert a floating-point
error budget: the actual producer must supply one. Convex Bernstein contraction
does not amplify a uniform coefficient error, including after exact restriction.
-/

noncomputable section
open scoped BigOperators

namespace QuantumBlockEncoding.ExperimentalHermiteSourcePrecision

open HermiteBernstein

theorem convex_step_error (t a b a' b' δ : ℝ)
    (ht : t ∈ Set.Icc 0 1) (ha : |a' - a| ≤ δ) (hb : |b' - b| ≤ δ) :
    |((1 - t) * a' + t * b') - ((1 - t) * a + t * b)| ≤ δ := by
  have hid : ((1 - t) * a' + t * b') - ((1 - t) * a + t * b) =
      (1 - t) * (a' - a) + t * (b' - b) := by ring
  rw [hid]
  calc
    _ ≤ |(1 - t) * (a' - a)| + |t * (b' - b)| := abs_add_le _ _
    _ = (1 - t) * |a' - a| + t * |b' - b| := by
      rw [abs_mul, abs_mul, abs_of_nonneg (by linarith [ht.2]), abs_of_nonneg ht.1]
    _ ≤ δ := by
      have h1 := mul_le_mul_of_nonneg_left ha (show 0 ≤ 1 - t by linarith [ht.2])
      have h2 := mul_le_mul_of_nonneg_left hb ht.1
      nlinarith

theorem casteljau_succ (d : ℕ) (c : ℕ → ℝ) (t : ℝ) (i : ℕ) :
    casteljau (d + 1) c t i =
      (1 - t) * casteljau d c t i + t * casteljau d c t (i + 1) := by
  unfold casteljau
  rw [pow_succ', Module.End.mul_apply, casteljauStep_apply]

/-- Actual rounded row operations may supply rho; this theorem then accumulates
their absolute residuals linearly, rather than multiplying by the degree. -/
theorem rounded_casteljau_error (d : ℕ) (c : ℕ → ℝ) (rows : ℕ → ℕ → ℝ)
    (t δ ρ : ℝ) (ht : t ∈ Set.Icc 0 1)
    (initial : ∀ i, |rows 0 i - c i| ≤ δ)
    (rounding : ∀ m i,
      |rows (m + 1) i - ((1 - t) * rows m i + t * rows m (i + 1))| ≤ ρ) :
    ∀ i, |rows d i - casteljau d c t i| ≤ δ + d * ρ := by
  induction d with
  | zero => simpa [casteljau] using initial
  | succ d ih =>
    intro i
    rw [casteljau_succ]
    have hid : rows (d + 1) i -
        ((1 - t) * casteljau d c t i + t * casteljau d c t (i + 1)) =
        (rows (d + 1) i - ((1 - t) * rows d i + t * rows d (i + 1))) +
        (((1 - t) * rows d i + t * rows d (i + 1)) -
          ((1 - t) * casteljau d c t i + t * casteljau d c t (i + 1))) := by ring
    rw [hid]
    have hc := convex_step_error t (casteljau d c t i) (casteljau d c t (i + 1))
      (rows d i) (rows d (i + 1)) (δ + d * ρ) ht (ih i) (ih (i + 1))
    calc
      _ ≤ |rows (d + 1) i - ((1 - t) * rows d i + t * rows d (i + 1))| +
          |((1 - t) * rows d i + t * rows d (i + 1)) -
            ((1 - t) * casteljau d c t i + t * casteljau d c t (i + 1))| := abs_add_le _ _
      _ ≤ ρ + (δ + d * ρ) := add_le_add (rounding d i) hc
      _ = δ + (d + 1 : ℕ) * ρ := by push_cast; ring

theorem bernstein_eval_error (d : ℕ) (c e : ℕ → ℝ) (t δ : ℝ)
    (ht : t ∈ Set.Icc 0 1) (he : ∀ r ≤ d, |e r - c r| ≤ δ) :
    |(∑ r ∈ Finset.range (d + 1), e r * basis d r t) -
      (∑ r ∈ Finset.range (d + 1), c r * basis d r t)| ≤ δ := by
  have hb := bernstein_sum_bounds d (fun r => e r - c r) t (-δ) δ ht
    (fun r hr => abs_le.mp (he r hr))
  rw [← Finset.sum_sub_distrib]
  have hid : (∑ r ∈ Finset.range (d + 1),
      (e r * basis d r t - c r * basis d r t)) =
      ∑ r ∈ Finset.range (d + 1), (e r - c r) * basis d r t := by
    apply Finset.sum_congr rfl
    intro r hr
    ring
  rw [hid]
  exact abs_le.mpr hb

theorem leftRestriction_sub (u : ℝ) (c e : ℕ → ℝ) (i : ℕ) :
    leftRestriction u (fun r => e r - c r) i =
      leftRestriction u e i - leftRestriction u c i := by
  change ((casteljauStep u ^ i) (e - c)) 0 = _
  rw [map_sub]
  rfl

theorem rightRestriction_sub (d : ℕ) (u : ℝ) (c e : ℕ → ℝ) (i : ℕ) :
    rightRestriction d u (fun r => e r - c r) i =
      rightRestriction d u e i - rightRestriction d u c i := by
  exact leftRestriction_sub (1 - u) (fun r => c (d - r))
    (fun r => e (d - r)) (d - i)

theorem restriction_sub (d : ℕ) (u v : ℝ) (c e : ℕ → ℝ) (i : ℕ) :
    restrictCoefficients d u v (fun r => e r - c r) i =
      restrictCoefficients d u v e i - restrictCoefficients d u v c i := by
  unfold restrictCoefficients
  have hid : rightRestriction d u (fun r => e r - c r) =
      fun r => rightRestriction d u e r - rightRestriction d u c r := by
    funext r
    exact rightRestriction_sub d u c e r
  rw [hid, leftRestriction_sub]

theorem restriction_coefficient_error (d : ℕ) (c e : ℕ → ℝ)
    (u v δ : ℝ) (hu : 0 ≤ u) (huv : u < v) (hv : v ≤ 1)
    (he : ∀ r ≤ d, |e r - c r| ≤ δ) (i : ℕ) (hi : i ≤ d) :
    |restrictCoefficients d u v e i - restrictCoefficients d u v c i| ≤ δ := by
  have hb := restrictCoefficients_bounds d (fun r => e r - c r) u v (-δ) δ
    hu huv hv (fun r hr => abs_le.mp (he r hr)) i hi
  rw [restriction_sub] at hb
  exact abs_le.mpr hb

theorem source_perturbed_eval (k : ℕ) (e : ℕ → ℝ) (t δ : ℝ)
    (ht : t ∈ Set.Icc 0 1)
    (he : ∀ r ≤ 2 * k + 1, |e r - sourceBernsteinCoefficient k r| ≤ δ) :
    |(∑ r ∈ Finset.range (2 * k + 2), e r * basis (2 * k + 1) r t) -
      (HermitePolynomial.sourceInterpolant k).eval (t - 1)| ≤ δ := by
  rw [← sourceInterpolant_bernstein]
  simpa only [show 2 * k + 1 + 1 = 2 * k + 2 by omega] using
    bernstein_eval_error (2 * k + 1) (sourceBernsteinCoefficient k) e t δ ht he

theorem exp_underflow_error (x T : ℝ) (h : T ≤ x) :
    |(0 : ℝ) - Real.exp (-x)| ≤ Real.exp (-T) := by
  rw [zero_sub, abs_neg, abs_of_pos (Real.exp_pos _)]
  exact Real.exp_le_exp.mpr (by linarith)

#check bernstein_eval_error
#check rounded_casteljau_error
#check restriction_coefficient_error
#check source_perturbed_eval
#check exp_underflow_error
#print axioms bernstein_eval_error
#print axioms rounded_casteljau_error
#print axioms restriction_coefficient_error
#print axioms source_perturbed_eval
#print axioms exp_underflow_error

end QuantumBlockEncoding.ExperimentalHermiteSourcePrecision
