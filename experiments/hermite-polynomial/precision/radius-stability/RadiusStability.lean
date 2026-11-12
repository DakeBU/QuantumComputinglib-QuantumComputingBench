import CoefficientRange
import NormalizationStability
import Mathlib.Analysis.Calculus.MeanValue

noncomputable section
open scoped BigOperators

namespace QuantumBlockEncoding.ExperimentalRadiusStability
open HermitePolynomial HermiteBernstein ExperimentalCoefficientRange

def sourceLipschitzConstant (k : ℕ) : ℝ :=
  2 * coarseBound k * (2*k+2 : ℝ) * (2*k+1 : ℝ) * 2^(2*k+1)

def radiusGrid (n : ℕ) (R : ℝ) (j : Fin (gridSize (n+1))) : ℝ :=
  -R + 2*R*(j.val : ℝ)/(gridSize (n+1) : ℝ)

def radiusVector (k n : ℕ) (R : ℝ) : EuclideanSpace ℂ (Fin (gridSize (n+1))) :=
  WithLp.toLp 2 (fun j => (smoothInitial k (radiusGrid n R j) : ℂ))

theorem sourceLipschitzConstant_ge_one (k : ℕ) : 1 ≤ sourceLipschitzConstant k := by
  have hp : (1 : ℝ) ≤ 2^(3*k) := one_le_pow₀ (by norm_num)
  have hk : (0 : ℝ) ≤ k := Nat.cast_nonneg _
  have hb : 1 ≤ coarseBound k := by unfold coarseBound; nlinarith [sq_nonneg (k : ℝ)]
  have hd : (1 : ℝ) ≤ 2*k+1 := by linarith
  have he : (1 : ℝ) ≤ 2*k+2 := by linarith
  have hf : (1 : ℝ) ≤ 2^(2*k+1) := one_le_pow₀ (by norm_num)
  unfold sourceLipschitzConstant
  calc
    1 ≤ 2*coarseBound k := by linarith
    _ ≤ 2*coarseBound k*(2*k+2) := le_mul_of_one_le_right (by positivity) he
    _ ≤ 2*coarseBound k*(2*k+2)*(2*k+1) := le_mul_of_one_le_right (by positivity) hd
    _ ≤ _ := le_mul_of_one_le_right (by positivity) hf

theorem unit_power_difference (a b : ℝ) (ha : a ∈ Set.Icc 0 1)
    (hb : b ∈ Set.Icc 0 1) (m : ℕ) : |a^m-b^m| ≤ (m : ℝ)*|a-b| := by
  have hm : max |a| |b| ≤ 1 := by
    rw [abs_of_nonneg ha.1, abs_of_nonneg hb.1]
    exact max_le ha.2 hb.2
  calc
    _ ≤ |a-b| * m*(max |a| |b|)^(m-1) := abs_pow_sub_pow_le a b m
    _ ≤ |a-b| * m*1 := mul_le_mul_of_nonneg_left
      (pow_le_one₀ (by positivity) hm) (by positivity)
    _ = _ := by ring

theorem basis_difference (d r : ℕ) (hr : r ≤ d) (a b : ℝ)
    (ha : a ∈ Set.Icc 0 1) (hb : b ∈ Set.Icc 0 1) :
    |basis d r a-basis d r b| ≤ (2 : ℝ)^d*(d : ℝ)*|a-b| := by
  have hc : (d.choose r : ℝ) ≤ (2 : ℝ)^d := by exact_mod_cast Nat.choose_le_two_pow d r
  have ha' : 1-a ∈ Set.Icc (0 : ℝ) 1 := ⟨by linarith [ha.2], by linarith [ha.1]⟩
  have hb' : 1-b ∈ Set.Icc (0 : ℝ) 1 := ⟨by linarith [hb.2], by linarith [hb.1]⟩
  have h1 := unit_power_difference a b ha hb r
  have h2 := unit_power_difference (1-a) (1-b) ha' hb' (d-r)
  have hid : (1-a)-(1-b) = -(a-b) := by ring
  rw [hid, abs_neg] at h2
  have h3 : |a^r| ≤ 1 := by rw [abs_of_nonneg (pow_nonneg ha.1 _)]; exact pow_le_one₀ ha.1 ha.2
  have h4 : |(1-b)^(d-r)| ≤ 1 := by
    rw [abs_of_nonneg (pow_nonneg hb'.1 _)]; exact pow_le_one₀ hb'.1 hb'.2
  have hprod : |a^r*(1-a)^(d-r)-b^r*(1-b)^(d-r)| ≤ (d : ℝ)*|a-b| := by
    have heq : a^r*(1-a)^(d-r)-b^r*(1-b)^(d-r) =
        a^r*((1-a)^(d-r)-(1-b)^(d-r))+(a^r-b^r)*(1-b)^(d-r) := by ring
    rw [heq]
    calc
      _ ≤ |a^r*((1-a)^(d-r)-(1-b)^(d-r))|+|(a^r-b^r)*(1-b)^(d-r)| := abs_add_le _ _
      _ = |a^r| * |(1-a)^(d-r)-(1-b)^(d-r)|+|a^r-b^r| * |(1-b)^(d-r)| := by rw [abs_mul, abs_mul]
      _ ≤ 1*((d-r : ℕ) : ℝ)*|a-b|+(r : ℝ)*|a-b| * 1 := by
        apply add_le_add
        · simpa [mul_assoc] using mul_le_mul h3 h2 (by positivity) (by positivity)
        · exact mul_le_mul h1 h4 (by positivity) (by positivity)
      _ = _ := by rw [Nat.cast_sub hr]; ring
  rw [basis_eq, basis_eq]
  have hid' : (d.choose r : ℝ)*a^r*(1-a)^(d-r)-(d.choose r : ℝ)*b^r*(1-b)^(d-r) =
      (d.choose r : ℝ)*(a^r*(1-a)^(d-r)-b^r*(1-b)^(d-r)) := by ring
  rw [hid', abs_mul, abs_of_nonneg (Nat.cast_nonneg _)]
  exact (mul_le_mul hc hprod (by positivity) (by positivity)).trans_eq (by ring)

theorem sourceInterpolant_lipschitz (k : ℕ) (x y : ℝ)
    (hx : x ∈ Set.Icc (-1) 0) (hy : y ∈ Set.Icc (-1) 0) :
    |(sourceInterpolant k).eval x-(sourceInterpolant k).eval y| ≤ sourceLipschitzConstant k*|x-y| := by
  have hx' : x+1 ∈ Set.Icc (0 : ℝ) 1 := ⟨by linarith [hx.1], by linarith [hx.2]⟩
  have hy' : y+1 ∈ Set.Icc (0 : ℝ) 1 := ⟨by linarith [hy.1], by linarith [hy.2]⟩
  have he1 := sourceInterpolant_bernstein k (x+1)
  have he2 := sourceInterpolant_bernstein k (y+1)
  simp only [add_sub_cancel_right] at he1 he2
  rw [← he1, ← he2, ← Finset.sum_sub_distrib]
  calc
    _ ≤ ∑ r ∈ Finset.range (2*k+2),
        |sourceBernsteinCoefficient k r*basis (2*k+1) r (x+1)-sourceBernsteinCoefficient k r*basis (2*k+1) r (y+1)| :=
      Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ _r ∈ Finset.range (2*k+2),
        2*coarseBound k*((2 : ℝ)^(2*k+1)*(2*k+1 : ℝ)*|x-y|) := by
      apply Finset.sum_le_sum
      intro r hr
      have hr' : r ≤ 2*k+1 := by have := Finset.mem_range.mp hr; omega
      rw [← mul_sub, abs_mul, abs_of_nonneg (sourceBernsteinCoefficient_nonneg _ _)]
      have hd := basis_difference (2*k+1) r hr' (x+1) (y+1) hx' hy'
      rw [show x+1-(y+1)=x-y by ring] at hd
      push_cast at hd
      exact mul_le_mul (sourceBernsteinCoefficient_range k r).2 hd (by positivity) (by unfold coarseBound; positivity)
    _ = _ := by simp only [Finset.sum_const, Finset.card_range, nsmul_eq_mul]; unfold sourceLipschitzConstant; push_cast; ring

theorem exp_nonpositive_difference (x y : ℝ) (hx : x ≤ 0) (hy : y ≤ 0) :
    |Real.exp x-Real.exp y| ≤ |x-y| := by
  have h := Convex.norm_image_sub_le_of_norm_hasDerivWithin_le
    (f := Real.exp) (f' := Real.exp) (s := Set.Iic (0 : ℝ)) (C := 1)
    (fun t _ => (Real.hasDerivAt_exp t).hasDerivWithinAt)
    (fun t ht => by
      rw [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
      calc Real.exp t ≤ Real.exp 0 := Real.exp_le_exp.mpr ht
           _ = 1 := Real.exp_zero)
    (convex_Iic _) hy hx
  simpa only [Real.norm_eq_abs, one_mul] using h

theorem smoothInitial_left_closed (k : ℕ) (x : ℝ) (hx : x ≤ -1) : smoothInitial k x=Real.exp x := by
  by_cases h : x < -1
  · exact smoothInitial_left k x h
  · have he : x = -1 := by linarith
    subst x
    rw [smoothInitial_middle k (-1) ⟨by norm_num, by norm_num⟩]
    simpa using sourceInterpolant_left_jet k 0 (Nat.zero_le _)

theorem smoothInitial_right_closed (k : ℕ) (x : ℝ) (hx : 0 ≤ x) : smoothInitial k x=Real.exp (-x) := by
  by_cases h : 0 < x
  · exact smoothInitial_right k x h
  · have he : x = 0 := by linarith
    subst x
    rw [smoothInitial_middle k 0 ⟨by norm_num, by norm_num⟩]
    simpa using sourceInterpolant_right_jet k 0 (Nat.zero_le _)

theorem smoothInitial_middle_difference (k : ℕ) (x y : ℝ)
    (hx : x ∈ Set.Icc (-1) 0) (hy : y ∈ Set.Icc (-1) 0) :
    |smoothInitial k x-smoothInitial k y| ≤ sourceLipschitzConstant k*|x-y| := by
  rw [smoothInitial_middle k x hx, smoothInitial_middle k y hy]
  exact sourceInterpolant_lipschitz k x y hx hy

theorem smoothInitial_left_difference (k : ℕ) (x y : ℝ) (hx : x ≤ -1) (hy : y ≤ -1) :
    |smoothInitial k x-smoothInitial k y| ≤ sourceLipschitzConstant k*|x-y| := by
  rw [smoothInitial_left_closed k x hx, smoothInitial_left_closed k y hy]
  exact (exp_nonpositive_difference x y (by linarith) (by linarith)).trans
    (le_mul_of_one_le_left (abs_nonneg _) (sourceLipschitzConstant_ge_one k))

theorem smoothInitial_right_difference (k : ℕ) (x y : ℝ) (hx : 0 ≤ x) (hy : 0 ≤ y) :
    |smoothInitial k x-smoothInitial k y| ≤ sourceLipschitzConstant k*|x-y| := by
  rw [smoothInitial_right_closed k x hx, smoothInitial_right_closed k y hy]
  have h := exp_nonpositive_difference (-x) (-y) (by linarith) (by linarith)
  rw [show -x- -y = -(x-y) by ring, abs_neg] at h
  exact h.trans (le_mul_of_one_le_left (abs_nonneg _) (sourceLipschitzConstant_ge_one k))

theorem smoothInitial_ordered_difference (k : ℕ) (x y : ℝ) (hxy : x ≤ y) :
    |smoothInitial k x-smoothInitial k y| ≤ sourceLipschitzConstant k*(y-x) := by
  have hab : |x-y|=y-x := by rw [abs_of_nonpos (by linarith)]; ring
  by_cases hx : x ≤ -1
  · by_cases hy : y ≤ -1
    · simpa [hab] using smoothInitial_left_difference k x y hx hy
    · by_cases hy0 : y ≤ 0
      · have h1 := smoothInitial_left_difference k x (-1) hx le_rfl
        have h2 := smoothInitial_middle_difference k (-1) y ⟨le_rfl, by norm_num⟩ ⟨by linarith, hy0⟩
        have h3 := abs_sub_le (smoothInitial k x) (smoothInitial k (-1)) (smoothInitial k y)
        rw [abs_of_nonpos (by linarith : x- -1 ≤ 0)] at h1
        rw [abs_of_nonpos (by linarith : -1-y ≤ 0)] at h2
        nlinarith
      · have h1 := smoothInitial_left_difference k x (-1) hx le_rfl
        have h2 := smoothInitial_middle_difference k (-1) 0 ⟨le_rfl, by norm_num⟩ ⟨by norm_num, le_rfl⟩
        have h3 := smoothInitial_right_difference k 0 y le_rfl (by linarith)
        have ht1 := abs_sub_le (smoothInitial k x) (smoothInitial k (-1)) (smoothInitial k y)
        have ht2 := abs_sub_le (smoothInitial k (-1)) (smoothInitial k 0) (smoothInitial k y)
        rw [abs_of_nonpos (by linarith : x- -1 ≤ 0)] at h1
        norm_num at h2
        rw [abs_of_nonpos (by linarith : 0-y ≤ 0)] at h3
        nlinarith
  · by_cases hx0 : x ≤ 0
    · by_cases hy0 : y ≤ 0
      · simpa [hab] using smoothInitial_middle_difference k x y ⟨by linarith, hx0⟩ ⟨by linarith, hy0⟩
      · have h1 := smoothInitial_middle_difference k x 0 ⟨by linarith, hx0⟩ ⟨by norm_num, le_rfl⟩
        have h2 := smoothInitial_right_difference k 0 y le_rfl (by linarith)
        have h3 := abs_sub_le (smoothInitial k x) (smoothInitial k 0) (smoothInitial k y)
        rw [sub_zero, abs_of_nonpos hx0] at h1
        rw [abs_of_nonpos (by linarith : 0-y ≤ 0)] at h2
        nlinarith
    · simpa [hab] using smoothInitial_right_difference k x y (by linarith) (by linarith)

theorem smoothInitial_lipschitz (k : ℕ) (x y : ℝ) :
    |smoothInitial k x-smoothInitial k y| ≤ sourceLipschitzConstant k*|x-y| := by
  rcases le_total x y with h | h
  · have he := smoothInitial_ordered_difference k x y h
    rwa [abs_of_nonpos (by linarith : x-y ≤ 0), neg_sub] at ⊢
  · have he := smoothInitial_ordered_difference k y x h
    rw [abs_sub_comm (smoothInitial k x) (smoothInitial k y)]
    simpa [abs_of_nonneg (sub_nonneg.mpr h)] using he

theorem radius_grid_difference (n : ℕ) (R S : ℝ) (j : Fin (gridSize (n+1))) :
    |radiusGrid n R j-radiusGrid n S j| ≤ |R-S| := by
  have hN : (0 : ℝ) < gridSize (n+1) := by unfold gridSize; positivity
  have hj : (j.val : ℝ) ≤ gridSize (n+1) := by exact_mod_cast j.isLt.le
  have hj0 : (0 : ℝ) ≤ j.val := Nat.cast_nonneg _
  have ht : |-1+2*(j.val : ℝ)/(gridSize (n+1) : ℝ)| ≤ 1 := by
    apply abs_le.mpr
    constructor
    · have := div_nonneg (show (0 : ℝ) ≤ 2*j.val by positivity) hN.le
      linarith
    · have := (div_le_iff₀ hN).mpr (show 2*(j.val : ℝ) ≤ 2*gridSize (n+1) by linarith)
      linarith
  have he : radiusGrid n R j-radiusGrid n S j =
      (R-S)*(-1+2*(j.val : ℝ)/(gridSize (n+1) : ℝ)) := by unfold radiusGrid; ring
  rw [he, abs_mul]
  simpa using mul_le_mul_of_nonneg_left ht (abs_nonneg (R-S))

theorem radiusVector_error (k n : ℕ) (R S : ℝ) :
    ‖radiusVector k n R-radiusVector k n S‖ ≤
      Real.sqrt (gridSize (n+1) : ℝ)*sourceLipschitzConstant k*|R-S| := by
  let D : ℝ := sourceLipschitzConstant k*|R-S|
  have hD : 0 ≤ D := mul_nonneg (le_trans (by norm_num) (sourceLipschitzConstant_ge_one k)) (abs_nonneg _)
  have hp (j : Fin (gridSize (n+1))) :
      ‖(radiusVector k n R-radiusVector k n S) j‖ ≤ D := by
    change ‖(smoothInitial k (radiusGrid n R j) : ℂ)-(smoothInitial k (radiusGrid n S j) : ℂ)‖ ≤ D
    rw [← Complex.ofReal_sub, Complex.norm_real, Real.norm_eq_abs]
    exact (smoothInitial_lipschitz k _ _).trans
      (mul_le_mul_of_nonneg_left (radius_grid_difference n R S j)
        (le_trans (by norm_num) (sourceLipschitzConstant_ge_one k)))
  have hs : ‖radiusVector k n R-radiusVector k n S‖^2 ≤ (gridSize (n+1) : ℝ)*D^2 := by
    rw [EuclideanSpace.norm_sq_eq]
    calc
      _ ≤ ∑ _j : Fin (gridSize (n+1)), D^2 := by
        apply Finset.sum_le_sum
        intro j _
        exact pow_le_pow_left₀ (norm_nonneg _) (hp j) 2
      _ = _ := by simp
  have hN : (0 : ℝ) ≤ gridSize (n+1) := Nat.cast_nonneg _
  have hs' : ‖radiusVector k n R-radiusVector k n S‖^2 ≤
      (Real.sqrt (gridSize (n+1) : ℝ)*D)^2 := by
    rw [mul_pow, Real.sq_sqrt hN]
    exact hs
  have h := (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (Real.sqrt_nonneg _) hD)).mp hs'
  simpa only [D, mul_assoc] using h

theorem radiusVector_source (k n : ℕ) (L : ℝ) :
    radiusVector k n (Real.pi*L)=ExperimentalNormalizationStability.sourceVector k n L := by
  ext j
  change (smoothInitial k (radiusGrid n (Real.pi*L) j) : ℂ)=
    (smoothInitial k (HermiteStatePreparation.gridPoint (n+1) L j) : ℂ)
  congr 2
  unfold radiusGrid HermiteStatePreparation.gridPoint
  ring

theorem normalized_radius_error (k n : ℕ) (L : ℝ) (hL : 0 < L)
    (Rhat : ℚ) (hRhat : 0 < Rhat) :
    ‖NormedSpace.normalize (radiusVector k n (Rhat : ℝ))-
        ExperimentalNormalizationStability.targetVector k n L‖ ≤
      2*Real.sqrt (gridSize (n+1) : ℝ)*sourceLipschitzConstant k*|(Rhat : ℝ)-Real.pi*L| := by
  have he := radiusVector_error k n (Rhat : ℝ) (Real.pi*L)
  rw [radiusVector_source] at he
  have h := ExperimentalNormalizationStability.hermite_scaled_error k n L
    (F := 1) (by norm_num) (y := radiusVector k n (Rhat : ℝ))
    (δ := Real.sqrt (gridSize (n+1) : ℝ)*sourceLipschitzConstant k*|(Rhat : ℝ)-Real.pi*L|)
    (by simpa using he)
  simpa only [one_mul, mul_assoc] using h

#print axioms sourceLipschitzConstant_ge_one
#print axioms unit_power_difference
#print axioms basis_difference
#print axioms sourceInterpolant_lipschitz
#print axioms exp_nonpositive_difference
#print axioms smoothInitial_left_closed
#print axioms smoothInitial_right_closed
#print axioms smoothInitial_middle_difference
#print axioms smoothInitial_left_difference
#print axioms smoothInitial_right_difference
#print axioms smoothInitial_ordered_difference
#print axioms smoothInitial_lipschitz
#print axioms radius_grid_difference
#print axioms radiusVector_error
#print axioms radiusVector_source
#print axioms normalized_radius_error

end QuantumBlockEncoding.ExperimentalRadiusStability
