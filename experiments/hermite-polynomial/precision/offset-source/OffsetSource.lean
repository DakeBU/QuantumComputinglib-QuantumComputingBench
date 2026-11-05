import QuantumBlockEncoding.HermiteBernstein
import QuantumBlockEncoding.StoredBernstein

/-! Exact source-coordinate and local interval certificate interfaces.
These are not a theorem about Python, floating-point QR, or global state error.
-/

noncomputable section
open scoped BigOperators

namespace QuantumBlockEncoding.ExperimentalOffsetSource

open HermiteBernstein

theorem offset_interval (R N a b : ℝ) (hR : 0 < R) (hN : 0 < N)
    (_ha : 0 ≤ a) (hab : a < b) (hb : 2 * b ≤ N)
    (active : R * (N - 2 * a) / N ≤ 1) :
    0 ≤ R * (N - 2 * b) / N ∧
      R * (N - 2 * b) / N < R * (N - 2 * a) / N ∧
      R * (N - 2 * a) / N ≤ 1 := by
  refine ⟨div_nonneg (mul_nonneg hR.le (by linarith)) hN.le, ?_, active⟩
  apply (div_lt_div_iff_of_pos_right hN).mpr
  nlinarith

theorem normalized_parameter_mono (R S A B : ℝ) (hRS : R ≤ S)
    (hA : 0 ≤ A) (hΔ : 0 ≤ B - A) (hSA : S * A < 1) :
    R * (B - A) / (1 - R * A) ≤ S * (B - A) / (1 - S * A) := by
  have hRA : R * A ≤ S * A := mul_le_mul_of_nonneg_right hRS hA
  have hdenR : 0 < 1 - R * A := by linarith
  have hdenS : 0 < 1 - S * A := by linarith
  apply (div_le_div_iff₀ hdenR hdenS).mpr
  nlinarith [mul_nonneg (sub_nonneg.mpr hRS) hΔ]

/-- Reflected restriction with coefficients reversed back to increasing j.
The sample coordinate is not reversed: only the small offset chart is. -/
def offsetRestriction (d : ℕ) (lo hi : ℝ) (c : ℕ → ℝ) (r : ℕ) : ℝ :=
  restrictCoefficients d lo hi (fun j => c (d - j)) (d - r)

theorem offsetRestriction_eval (d : ℕ) (c : ℕ → ℝ) (lo hi y : ℝ)
    (hlo : lo ≠ 1) :
    (∑ r ∈ Finset.range (d + 1), offsetRestriction d lo hi c r * basis d r y) =
      ∑ r ∈ Finset.range (d + 1), c r * basis d r (1 - hi + (hi - lo) * y) := by
  unfold offsetRestriction
  rw [reflected_sum, restrictCoefficients_eval _ _ _ _ _ hlo, reflected_sum]
  congr 1
  ext r
  congr 2
  ring

theorem offset_source_eval (k : ℕ) (lo hi y : ℝ) (hlo : lo ≠ 1) :
    (∑ r ∈ Finset.range (2 * k + 2),
      offsetRestriction (2 * k + 1) lo hi (sourceBernsteinCoefficient k) r *
        basis (2 * k + 1) r y) =
      (HermitePolynomial.sourceInterpolant k).eval (-hi + (hi - lo) * y) := by
  rw [show 2 * k + 2 = (2 * k + 1) + 1 by omega, offsetRestriction_eval _ _ _ _ _ hlo]
  rw [sourceInterpolant_bernstein]
  congr 1
  ring

theorem offset_grid_coordinate (R N a b j : ℝ) (hN : N ≠ 0) (hab : b - a ≠ 0) :
    -(R * (N - 2 * a) / N) +
      (R * (N - 2 * a) / N - R * (N - 2 * b) / N) * ((j - a) / (b - a)) =
      -R + 2 * R * j / N := by
  field_simp
  ring

/-- All-parameter action refinement: the offset chart preserves the original
increasing grid index j, with no reflection of physical output labels. -/
theorem offset_grid_source_eval (k : ℕ) (R N a b j : ℝ)
    (hN : N ≠ 0) (hab : b - a ≠ 0) (hlo : R * (N - 2 * b) / N ≠ 1) :
    (∑ r ∈ Finset.range (2 * k + 2),
      offsetRestriction (2 * k + 1) (R * (N - 2 * b) / N) (R * (N - 2 * a) / N)
        (sourceBernsteinCoefficient k) r * basis (2 * k + 1) r ((j - a) / (b - a))) =
      (HermitePolynomial.sourceInterpolant k).eval (-R + 2 * R * j / N) := by
  rw [offset_source_eval _ _ _ _ hlo, offset_grid_coordinate _ _ _ _ _ hN hab]

theorem affine_endpoint_bounds (a b u v t : ℝ) (hut : u ≤ t) (htv : t ≤ v) :
    (1 - t) * a + t * b ∈ Set.Icc
      (min ((1 - u) * a + u * b) ((1 - v) * a + v * b))
      (max ((1 - u) * a + u * b) ((1 - v) * a + v * b)) := by
  by_cases hab : 0 ≤ b - a
  · have hlo : (1 - u) * a + u * b ≤ (1 - t) * a + t * b := by
      nlinarith [mul_nonneg (sub_nonneg.mpr hut) hab]
    have hhi : (1 - t) * a + t * b ≤ (1 - v) * a + v * b := by
      nlinarith [mul_nonneg (sub_nonneg.mpr htv) hab]
    exact ⟨(min_le_left _ _).trans hlo, hhi.trans (le_max_right _ _)⟩
  · have hba : 0 ≤ a - b := by linarith
    have hlo : (1 - v) * a + v * b ≤ (1 - t) * a + t * b := by
      nlinarith [mul_nonneg (sub_nonneg.mpr htv) hba]
    have hhi : (1 - t) * a + t * b ≤ (1 - u) * a + u * b := by
      nlinarith [mul_nonneg (sub_nonneg.mpr hut) hba]
    exact ⟨(min_le_right _ _).trans hlo, hhi.trans (le_max_left _ _)⟩

/-- Exact soundness of the four-corner convex update used by the rational
interval implementation; sharing t avoids naive interval weight-sum inflation. -/
theorem convex_interval_step (a b alo ahi blo bhi u v t : ℝ)
    (ha : a ∈ Set.Icc alo ahi) (hb : b ∈ Set.Icc blo bhi)
    (ht : t ∈ Set.Icc 0 1) (hparam : t ∈ Set.Icc u v) :
    (1 - t) * a + t * b ∈ Set.Icc
      (min ((1 - u) * alo + u * blo) ((1 - v) * alo + v * blo))
      (max ((1 - u) * ahi + u * bhi) ((1 - v) * ahi + v * bhi)) := by
  have hl := affine_endpoint_bounds alo blo u v t hparam.1 hparam.2
  have hh := affine_endpoint_bounds ahi bhi u v t hparam.1 hparam.2
  have hw : 0 ≤ 1 - t := by linarith [ht.2]
  have hlow : (1 - t) * alo + t * blo ≤ (1 - t) * a + t * b :=
    add_le_add (mul_le_mul_of_nonneg_left ha.1 hw) (mul_le_mul_of_nonneg_left hb.1 ht.1)
  have hhigh : (1 - t) * a + t * b ≤ (1 - t) * ahi + t * bhi :=
    add_le_add (mul_le_mul_of_nonneg_left ha.2 hw) (mul_le_mul_of_nonneg_left hb.2 ht.1)
  exact ⟨hl.1.trans hlow, hhigh.trans hh.2⟩

/-- Mathematical rational-interval row producer. No default invalid interval
is used; soundness concerns exactly the finite dependency cone. -/
def intervalRows (u v : ℝ) : ℕ → (ℕ → ℝ × ℝ) → ℕ → ℝ × ℝ
  | 0, xs => xs
  | d + 1, xs => fun i =>
      let a := intervalRows u v d xs i
      let b := intervalRows u v d xs (i + 1)
      (min ((1 - u) * a.1 + u * b.1) ((1 - v) * a.1 + v * b.1),
       max ((1 - u) * a.2 + u * b.2) ((1 - v) * a.2 + v * b.2))

theorem intervalRows_sound (d : ℕ) (xs : ℕ → ℝ × ℝ) (c : ℕ → ℝ)
    (u v t : ℝ) (ht : t ∈ Set.Icc 0 1) (hparam : t ∈ Set.Icc u v)
    (i : ℕ) (initial : ∀ j ≤ i + d, c j ∈ Set.Icc (xs j).1 (xs j).2) :
    casteljau d c t i ∈ Set.Icc
      (intervalRows u v d xs i).1 (intervalRows u v d xs i).2 := by
  induction d generalizing i with
  | zero => simpa [intervalRows, casteljau] using initial i (by omega)
  | succ d ih =>
    have ha := ih i (fun j hj => initial j (by omega))
    have hb := ih (i + 1) (fun j hj => initial j (by omega))
    have hs := convex_interval_step (casteljau d c t i) (casteljau d c t (i + 1))
      _ _ _ _ u v t ha hb ht hparam
    simpa only [intervalRows, StoredBernstein.casteljau_succ] using hs

/-- Once a stored dyadic value and true coefficient are enclosed, the exact
endpoint distances certify the local conversion error without a relative-error
assumption, even if the stored value is zero or has a different sign. -/
theorem interval_rounding_error (lo hi stored x : ℝ) (hx : x ∈ Set.Icc lo hi) :
    |stored - x| ≤ max |stored - lo| |stored - hi| := by
  have hl := abs_le.mp (le_max_left |stored - lo| |stored - hi|)
  have hh := abs_le.mp (le_max_right |stored - lo| |stored - hi|)
  exact abs_le.mpr ⟨by linarith [hx.2, hh.1], by linarith [hx.1, hl.2]⟩

#check offset_interval
#check normalized_parameter_mono
#check offset_source_eval
#check offset_grid_source_eval
#check convex_interval_step
#check intervalRows_sound
#check interval_rounding_error
#print axioms offset_interval
#print axioms normalized_parameter_mono
#print axioms offset_source_eval
#print axioms offset_grid_source_eval
#print axioms convex_interval_step
#print axioms intervalRows_sound
#print axioms interval_rounding_error

end QuantumBlockEncoding.ExperimentalOffsetSource
