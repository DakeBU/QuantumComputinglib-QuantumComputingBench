import ConsumerChecks
import GlobalRadiusBudget

/-! Literal rational source on the physical rational-radius grid. All source
and radius errors are supplied internally. No TT or finite-bit cost claim. -/

namespace HermitePiecewiseSourceBudget

open scoped BigOperators
open QuantumBlockEncoding HermitePolynomial HermiteFiniteMiddleSource
open ExperimentalRadiusStability ExperimentalNormalizationStability
open ExperimentalGlobalRadiusBudget

def negativeMidpoint (q delta : ℚ) : ℚ :=
  let I := HermiteFiniteExp.bounds q (HermiteFiniteExp.tailCutoff delta)
    (HermiteFiniteExpDegree.sourceDegree delta)
  (I.1+I.2)/2

def piecewiseValue (k : ℕ) (delta p : ℚ) : ℚ :=
  if p < -1 then negativeMidpoint p delta
  else if p ≤ 0 then middleValueQ k delta p
  else negativeMidpoint (-p) delta

def rationalGrid (n : ℕ) (R : ℚ) (j : Fin (gridSize (n+1))) : ℚ :=
  -R+2*R*(j.val : ℚ)/(gridSize (n+1) : ℚ)

noncomputable def finiteVector (k n : ℕ) (R delta : ℚ) :
    EuclideanSpace ℂ (Fin (gridSize (n+1))) :=
  WithLp.toLp 2 (fun j => ((piecewiseValue k delta (rationalGrid n R j) : ℝ) : ℂ))

def sourceDelta (k n : ℕ) (epsilon : ℚ) : ℚ :=
  epsilon/(4*2^(n+1)*amplificationQ k)

noncomputable def allocatedVector (k n : ℕ) (L epsilon : ℚ) :
    EuclideanSpace ℂ (Fin (gridSize (n+1))) :=
  finiteVector k n (allocatedRadius k n L epsilon) (sourceDelta k n epsilon)

theorem amplification_ge_one (k : ℕ) : (1 : ℚ) ≤ amplificationQ k := by
  have hp : (1 : ℚ) ≤ 2^(2*k) := one_le_pow₀ (by norm_num)
  unfold amplificationQ
  have hk : (0 : ℚ) ≤ k := Nat.cast_nonneg _
  nlinarith [sq_nonneg (k : ℚ)]

theorem negativeMidpoint_error (q delta : ℚ) (hq : q ≤ 0) (hd : 0 < delta) :
    |(negativeMidpoint q delta : ℝ)-Real.exp (q : ℝ)| ≤ (delta : ℝ)/2 := by
  have h := HermiteFiniteExpDegree.complete_enclosure q delta hq hd
  have hw : ((HermiteFiniteExp.bounds q (HermiteFiniteExp.tailCutoff delta)
    (HermiteFiniteExpDegree.sourceDegree delta)).2 : ℝ)-
    ((HermiteFiniteExp.bounds q (HermiteFiniteExp.tailCutoff delta)
    (HermiteFiniteExpDegree.sourceDegree delta)).1 : ℝ) ≤ (delta : ℝ) := by
    exact_mod_cast h.2
  simp only [Set.mem_Icc] at h
  simp only [negativeMidpoint, Rat.cast_div, Rat.cast_add, Rat.cast_ofNat]
  apply abs_le.mpr
  constructor <;> linarith [h.1.1, h.1.2]

theorem piecewise_error (k : ℕ) (delta p : ℚ) (hd : 0 < delta) :
    |(piecewiseValue k delta p : ℝ)-smoothInitial k (p : ℝ)| ≤
      (delta : ℝ)/2*(amplificationQ k : ℝ) := by
  have hb : (1 : ℝ) ≤ amplificationQ k := by exact_mod_cast amplification_ge_one k
  have hdR : (0 : ℝ) < delta := by exact_mod_cast hd
  by_cases hl : p < -1
  · rw [piecewiseValue, if_pos hl,
      smoothInitial_left k (p : ℝ) (by exact_mod_cast hl)]
    exact (negativeMidpoint_error p delta (by linarith) hd).trans
      (le_mul_of_one_le_right (by positivity) hb)
  · by_cases hm : p ≤ 0
    · rw [piecewiseValue, if_neg hl, if_pos hm]
      exact rational_middle_error k delta p ⟨by linarith, hm⟩ hd
    · rw [piecewiseValue, if_neg hl, if_neg hm,
        smoothInitial_right k (p : ℝ) (by exact_mod_cast (show 0 < p by linarith))]
      have h := negativeMidpoint_error (-p) delta (by linarith) hd
      simp only [Rat.cast_neg] at h
      exact h.trans (le_mul_of_one_le_right (by positivity) hb)

theorem piecewise_central (k : ℕ) (delta : ℚ) : piecewiseValue k delta 0 = 1 := by
  simp [piecewiseValue, rational_central]

theorem rationalGrid_cast (n : ℕ) (R : ℚ) (j : Fin (gridSize (n+1))) :
    (rationalGrid n R j : ℝ) = radiusGrid n (R : ℝ) j := by
  unfold rationalGrid radiusGrid
  push_cast
  rfl

theorem rationalGrid_central (n : ℕ) (R : ℚ) :
    rationalGrid n R (HermiteIntervalMass.centralIndex n) = 0 := by
  simp only [rationalGrid, HermiteIntervalMass.centralIndex, gridSize,
    Nat.cast_pow, Nat.cast_ofNat, pow_succ]
  have hn : (2 : ℚ)^n ≠ 0 := pow_ne_zero n (by norm_num)
  field_simp
  push_cast
  ring

theorem finiteVector_central (k n : ℕ) (R delta : ℚ) :
    finiteVector k n R delta (HermiteIntervalMass.centralIndex n) = 1 := by
  simp [finiteVector, rationalGrid_central, piecewise_central]

theorem finiteVector_norm_floor (k n : ℕ) (R delta : ℚ) :
    1 ≤ ‖finiteVector k n R delta‖ := by
  have h := Finset.single_le_sum
    (f := fun j : Fin (gridSize (n+1)) => ‖finiteVector k n R delta j‖^2)
    (fun j _ => sq_nonneg _) (Finset.mem_univ (HermiteIntervalMass.centralIndex n))
  rw [finiteVector_central] at h
  simp only [norm_one, one_pow] at h
  rw [← EuclideanSpace.norm_sq_eq] at h
  nlinarith [norm_nonneg (finiteVector k n R delta)]

theorem radiusVector_norm_floor (k n : ℕ) (R : ℝ) : 1 ≤ ‖radiusVector k n R‖ := by
  have hi : Real.pi*(R/Real.pi) = R := by
    field_simp
  rw [← hi, radiusVector_source, sourceVector_norm]
  exact hermite_norm_floor k n _

theorem finiteVector_error (k n : ℕ) (R delta : ℚ) (hd : 0 < delta) :
    ‖finiteVector k n R delta-radiusVector k n (R : ℝ)‖ ≤
      Real.sqrt (gridSize (n+1) : ℝ)*((delta : ℝ)/2*(amplificationQ k : ℝ)) := by
  let D : ℝ := (delta : ℝ)/2*(amplificationQ k : ℝ)
  have hdR : (0 : ℝ) < delta := by exact_mod_cast hd
  have hb : (1 : ℝ) ≤ amplificationQ k := by exact_mod_cast amplification_ge_one k
  have hD : 0 ≤ D := by dsimp [D]; positivity
  have hp (j : Fin (gridSize (n+1))) :
      ‖(finiteVector k n R delta-radiusVector k n (R : ℝ)) j‖ ≤ D := by
    change ‖((piecewiseValue k delta (rationalGrid n R j) : ℝ) : ℂ)-
      (smoothInitial k (radiusGrid n (R : ℝ) j) : ℂ)‖ ≤ D
    rw [← Complex.ofReal_sub, Complex.norm_real, Real.norm_eq_abs,
      ← rationalGrid_cast]
    exact piecewise_error k delta _ hd
  have hs : ‖finiteVector k n R delta-radiusVector k n (R : ℝ)‖^2 ≤
      (gridSize (n+1) : ℝ)*D^2 := by
    rw [EuclideanSpace.norm_sq_eq]
    calc
      _ ≤ ∑ _j : Fin (gridSize (n+1)), D^2 := by
        apply Finset.sum_le_sum
        intro j _
        exact pow_le_pow_left₀ (norm_nonneg _) (hp j) 2
      _ = _ := by simp
  have hs' : ‖finiteVector k n R delta-radiusVector k n (R : ℝ)‖^2 ≤
      (Real.sqrt (gridSize (n+1) : ℝ)*D)^2 := by
    rw [mul_pow, Real.sq_sqrt (by positivity)]
    exact hs
  exact (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (Real.sqrt_nonneg _) hD)).mp hs'

theorem sourceDelta_positive (k n : ℕ) (epsilon : ℚ) (he : 0 < epsilon) :
    0 < sourceDelta k n epsilon := by
  have hb := amplification_ge_one k
  unfold sourceDelta
  positivity

theorem normalized_source_error (k n : ℕ) (R epsilon : ℚ) (he : 0 < epsilon) :
    ‖NormedSpace.normalize (finiteVector k n R (sourceDelta k n epsilon))-
      NormedSpace.normalize (radiusVector k n (R : ℝ))‖ ≤ (epsilon : ℝ)/4 := by
  have hf := radiusVector_norm_floor k n (R : ℝ)
  have hx : radiusVector k n (R : ℝ) ≠ 0 := by
    intro hz
    rw [hz, norm_zero] at hf
    linarith
  have h := normalization_stability (radiusVector k n (R : ℝ))
    (finiteVector k n R (sourceDelta k n epsilon)) hx
  have ha := finiteVector_error k n R (sourceDelta k n epsilon)
    (sourceDelta_positive k n epsilon he)
  have hN : (1 : ℝ) ≤ gridSize (n+1) := by
    unfold gridSize
    exact_mod_cast (Nat.one_le_pow (n+1) 2 (by norm_num))
  have hs : Real.sqrt (gridSize (n+1) : ℝ) ≤ (gridSize (n+1) : ℝ) := by
    have hsq := Real.sq_sqrt (show (0 : ℝ) ≤ gridSize (n+1) by positivity)
    nlinarith [Real.sqrt_nonneg (gridSize (n+1) : ℝ)]
  have hb : (0 : ℝ) < amplificationQ k := by
    have hq := amplification_ge_one k
    exact_mod_cast (show (0 : ℚ) < amplificationQ k by linarith)
  have hd : (sourceDelta k n epsilon : ℝ) =
      (epsilon : ℝ)/(4*(gridSize (n+1) : ℝ)*(amplificationQ k : ℝ)) := by
    unfold sourceDelta gridSize
    push_cast
    rfl
  have hd0 : (0 : ℝ) ≤ sourceDelta k n epsilon := by
    exact_mod_cast (sourceDelta_positive k n epsilon he).le
  calc
    _ ≤ 2*‖finiteVector k n R (sourceDelta k n epsilon)-radiusVector k n (R : ℝ)‖ /
        ‖radiusVector k n (R : ℝ)‖ := h
    _ ≤ 2*‖finiteVector k n R (sourceDelta k n epsilon)-radiusVector k n (R : ℝ)‖ :=
      div_le_self (by positivity) hf
    _ ≤ 2*(Real.sqrt (gridSize (n+1) : ℝ)*
        ((sourceDelta k n epsilon : ℝ)/2*(amplificationQ k : ℝ))) := by gcongr
    _ ≤ 2*((gridSize (n+1) : ℝ)*
        ((sourceDelta k n epsilon : ℝ)/2*(amplificationQ k : ℝ))) := by gcongr
    _ = _ := by rw [hd]; field_simp

theorem normalized_original_error (k n : ℕ) (L epsilon : ℚ)
    (hL : 0 < L) (he : 0 < epsilon) :
    ‖NormedSpace.normalize (allocatedVector k n L epsilon)-targetVector k n (L : ℝ)‖ ≤
      (epsilon : ℝ)/2 := by
  have hs := normalized_source_error k n (allocatedRadius k n L epsilon) epsilon he
  have hr := normalized_allocatedRadius_error k n L epsilon hL he
  have ht := norm_add_le
    (NormedSpace.normalize (allocatedVector k n L epsilon)-
      NormedSpace.normalize (radiusVector k n (allocatedRadius k n L epsilon : ℝ)))
    (NormedSpace.normalize (radiusVector k n (allocatedRadius k n L epsilon : ℝ))-
      targetVector k n (L : ℝ))
  rw [sub_add_sub_cancel] at ht
  change ‖NormedSpace.normalize (allocatedVector k n L epsilon)-
    NormedSpace.normalize (radiusVector k n (allocatedRadius k n L epsilon : ℝ))‖ ≤
    (epsilon : ℝ)/4 at hs
  linarith

#print axioms amplification_ge_one
#print axioms negativeMidpoint_error
#print axioms piecewise_error
#print axioms piecewise_central
#print axioms rationalGrid_cast
#print axioms rationalGrid_central
#print axioms finiteVector_central
#print axioms finiteVector_norm_floor
#print axioms radiusVector_norm_floor
#print axioms finiteVector_error
#print axioms sourceDelta_positive
#print axioms normalized_source_error
#print axioms normalized_original_error

end HermitePiecewiseSourceBudget
