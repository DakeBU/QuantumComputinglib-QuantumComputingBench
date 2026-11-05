import QuantumBlockEncoding.HermitePolynomial
import Mathlib.Analysis.Calculus.ContDiff.Polynomial
import Mathlib.Analysis.Calculus.Deriv.Slope
import Mathlib.Topology.Piecewise

/-!
# Global regularity of the Hermite initial datum

Matching derivatives are used to prove a reusable finite-order gluing theorem.
Applying that theorem at both source junctions proves global `C^k` regularity
of the actual exponential/Hermite/exponential function.
-/

noncomputable section

open Filter Set Topology Polynomial
open QuantumBlockEncoding.HermitePolynomial

namespace QuantumBlockEncoding.HermiteSmoothness

/-- Join two real functions at a threshold, taking the right value at the threshold. -/
def splice (c : ℝ) (f g : ℝ → ℝ) (x : ℝ) : ℝ := if x < c then f x else g x

/-- Any selector preserves a common derivative when both branch values agree. -/
theorem hasDerivAt_ite_of_eq (pred : ℝ → Prop) [DecidablePred pred]
    {f g : ℝ → ℝ} {d x : ℝ} (hf : HasDerivAt f d x) (hg : HasDerivAt g d x)
    (hv : f x = g x) :
    HasDerivAt (fun y => if pred y then f y else g y) d x := by
  apply hasDerivAt_iff_tendsto_slope.mpr
  have he : slope (fun y => if pred y then f y else g y) x =
      fun y => if pred y then slope f x y else slope g x y := by
    funext y
    by_cases hx : pred x <;> by_cases hy : pred y <;>
      simp [slope_def_field, hx, hy, hv]
  rw [he]
  exact hf.tendsto_slope.if' hg.tendsto_slope

theorem hasDerivAt_splice (c : ℝ) (f g : ℝ → ℝ)
    (hf : Differentiable ℝ f) (hg : Differentiable ℝ g)
    (hv : f c = g c) (hd : deriv f c = deriv g c) (x : ℝ) :
    HasDerivAt (splice c f g) (splice c (deriv f) (deriv g) x) x := by
  rcases lt_trichotomy x c with hx | hxc | hx
  · rw [splice, if_pos hx]
    apply (hf x).hasDerivAt.congr_of_eventuallyEq
    filter_upwards [eventually_lt_nhds hx] with y hy
    simp [splice, hy]
  · subst x
    simp only [splice, lt_self_iff_false, if_false]
    exact hasDerivAt_ite_of_eq (fun y => y < c)
      (hd ▸ (hf c).hasDerivAt) (hg c).hasDerivAt hv
  · rw [splice, if_neg (not_lt.mpr hx.le)]
    apply (hg x).hasDerivAt.congr_of_eventuallyEq
    filter_upwards [eventually_gt_nhds hx] with y hy
    simp [splice, not_lt.mpr hy.le]

theorem deriv_splice (c : ℝ) (f g : ℝ → ℝ)
    (hf : Differentiable ℝ f) (hg : Differentiable ℝ g)
    (hv : f c = g c) (hd : deriv f c = deriv g c) :
    deriv (splice c f g) = splice c (deriv f) (deriv g) := by
  funext x
  exact (hasDerivAt_splice c f g hf hg hv hd x).deriv

/-- Two `C^k` real functions glue to a `C^k` function if their jets agree at the cut. -/
theorem contDiff_splice (k : ℕ) (c : ℝ) (f g : ℝ → ℝ)
    (hf : ContDiff ℝ k f) (hg : ContDiff ℝ k g)
    (hjet : ∀ j ≤ k, iteratedDeriv j f c = iteratedDeriv j g c) :
    ContDiff ℝ k (splice c f g) := by
  induction k generalizing f g with
  | zero =>
    rw [Nat.cast_zero, contDiff_zero]
    apply Continuous.if ?_ hf.continuous hg.continuous
    intro x hx
    have hxc : x = c := by
      change x ∈ frontier (Iio c) at hx
      simpa only [frontier_Iio, mem_singleton_iff] using hx
    subst x
    simpa using hjet 0 le_rfl
  | succ k ih =>
    rw [Nat.cast_add, Nat.cast_one] at hf hg ⊢
    obtain ⟨hfd, _, hfder⟩ := contDiff_succ_iff_deriv.mp hf
    obtain ⟨hgd, _, hgder⟩ := contDiff_succ_iff_deriv.mp hg
    have hv : f c = g c := by simpa using hjet 0 (Nat.zero_le _)
    have hd : deriv f c = deriv g c := by simpa using hjet 1 (by omega)
    apply contDiff_succ_iff_deriv.mpr
    refine ⟨fun x => (hasDerivAt_splice c f g hfd hgd hv hd x).differentiableAt,
      by simp, ?_⟩
    rw [deriv_splice c f g hfd hgd hv hd]
    apply ih (deriv f) (deriv g) hfder hgder
    intro j hj
    simpa only [iteratedDeriv_succ'] using hjet (j + 1) (by omega)

theorem iteratedDeriv_exp (j : ℕ) (x : ℝ) : iteratedDeriv j Real.exp x = Real.exp x := by
  simpa using congrFun (iteratedDeriv_exp_const_mul j (1 : ℝ)) x

theorem iteratedDeriv_exp_neg (j : ℕ) (x : ℝ) :
    iteratedDeriv j (fun y : ℝ => Real.exp (-y)) x = (-1 : ℝ) ^ j * Real.exp (-x) := by
  simpa using congrFun (iteratedDeriv_exp_const_mul j (-1 : ℝ)) x

/-- First join: the source polynomial and right exponential meet smoothly at zero. -/
theorem contDiff_right_splice (k : ℕ) :
    ContDiff ℝ k
      (splice 0 (fun p => (sourceInterpolant k).eval p) (fun p => Real.exp (-p))) := by
  apply contDiff_splice k 0
  · induction sourceInterpolant k using Polynomial.induction_on' with
    | add p q hp hq => simpa using hp.add hq
    | monomial n a => simpa using contDiff_const.mul (contDiff_id.pow n)
  · exact Real.contDiff_exp.comp contDiff_id.neg
  · intro j hj
    rw [sourceInterpolant_right_iteratedDeriv k j hj, iteratedDeriv_exp_neg]
    simp

/-- The right splice coincides with the polynomial on a neighborhood of the left junction. -/
theorem right_splice_eventuallyEq (k : ℕ) :
    splice 0 (fun p => (sourceInterpolant k).eval p) (fun p => Real.exp (-p))
      =ᶠ[𝓝 (-1)] (fun p => (sourceInterpolant k).eval p) := by
  filter_upwards [eventually_lt_nhds (show (-1 : ℝ) < 0 by norm_num)] with p hp
  simp [splice, hp]

/-- Two applications of the reusable gluing theorem close both source junctions. -/
theorem contDiff_double_splice (k : ℕ) :
    ContDiff ℝ k
      (splice (-1) Real.exp
        (splice 0 (fun p => (sourceInterpolant k).eval p) (fun p => Real.exp (-p)))) := by
  apply contDiff_splice k (-1) Real.exp _ Real.contDiff_exp (contDiff_right_splice k)
  intro j hj
  rw [iteratedDeriv_exp, (right_splice_eventuallyEq k).iteratedDeriv_eq j]
  exact (sourceInterpolant_left_iteratedDeriv k j hj).symm

/-- The original `≤ 0` middle-branch convention equals the smooth double splice exactly. -/
theorem smoothInitial_eq_double_splice (k : ℕ) :
    smoothInitial k = splice (-1) Real.exp
      (splice 0 (fun p => (sourceInterpolant k).eval p) (fun p => Real.exp (-p))) := by
  funext p
  by_cases hl : p < -1
  · simp [smoothInitial, splice, hl]
  · by_cases hr : p < 0
    · simp [smoothInitial, splice, hl, hr, hr.le]
    · by_cases hz : p = 0
      · subst p
        have hp0 : (sourceInterpolant k).eval 0 = 1 := by
          simpa using sourceInterpolant_right_jet k 0 (Nat.zero_le k)
        simp [smoothInitial, splice, hp0]
      · have hp : 0 < p := lt_of_le_of_ne (not_lt.mp hr) (Ne.symm hz)
        simp [smoothInitial, splice, hl, hr, not_le.mpr hp]

/-- The literal source initial datum is globally `C^k`, for every natural order `k`. -/
theorem smoothInitial_contDiff (k : ℕ) : ContDiff ℝ k (smoothInitial k) := by
  rw [smoothInitial_eq_double_splice]
  exact contDiff_double_splice k

end QuantumBlockEncoding.HermiteSmoothness
