import CoefficientRange
import FiniteExpDegree

/-! Literal finite rational Hermite middle supplier. The scalar interval-width
budget is amplified explicitly, and is not a normalized-state budget. -/

namespace HermiteFiniteMiddleSource

open Polynomial
open QuantumBlockEncoding
open HermitePolynomial
open ExperimentalCoefficientRange

def coefficientQ (k i : ℕ) : ℚ := (sourceNumerator k i : ℚ) / (k.factorial : ℚ)

noncomputable def coefficientPolynomialQ (k : ℕ) : ℚ[X] :=
  ∑ i ∈ Finset.range (k+1), monomial i (coefficientQ k i)

noncomputable def endpointPolynomialQ (k : ℕ) : ℚ[X] :=
  (1-X)^(k+1)*coefficientPolynomialQ k

noncomputable def middlePolynomialQ (k : ℕ) (e : ℚ) : ℚ[X] :=
  C e * (endpointPolynomialQ k).comp (X+1) + (endpointPolynomialQ k).comp (-X)

def expMidpoint (delta : ℚ) : ℚ :=
  let I := HermiteFiniteExp.bounds (-1) (HermiteFiniteExp.tailCutoff delta)
    (HermiteFiniteExpDegree.sourceDegree delta)
  (I.1+I.2)/2

noncomputable def sourcePolynomial (k : ℕ) (delta : ℚ) : ℚ[X] := middlePolynomialQ k (expMidpoint delta)

def amplificationQ (k : ℕ) : ℚ := (k+1)^2*2^(2*k)

theorem coefficientQ_cast (k i : ℕ) (hi : i ≤ k) :
    (coefficientQ k i : ℝ) = HermiteBernstein.sourceCoefficient k i := by
  simpa [coefficientQ] using (sourceNumerator_value k i hi).symm

theorem coefficientQ_formula (k i : ℕ) (hi : i ≤ k) :
    coefficientQ k i = ∑ m ∈ Finset.range (i+1),
      (Nat.choose (k+i-m) k : ℚ)/(m.factorial : ℚ) := by
  apply Rat.cast_injective (α := ℝ)
  rw [coefficientQ_cast k i hi, HermiteBernstein.sourceCoefficient_eq]
  simp

theorem coefficientPolynomialQ_eval (k : ℕ) (t : ℝ) :
    (coefficientPolynomialQ k).eval₂ (Rat.castHom ℝ) t =
      (coefficientPolynomial k).eval t := by
  simp only [coefficientPolynomialQ, eval₂_finsetSum, eval₂_monomial,
    Rat.coe_castHom]
  rw [coefficientPolynomial_eval]
  apply Finset.sum_congr rfl
  intro i hi
  rw [coefficientQ_cast k i (by simpa using hi), HermiteBernstein.sourceCoefficient_eq]

theorem endpointPolynomialQ_eval (k : ℕ) (t : ℝ) :
    (endpointPolynomialQ k).eval₂ (Rat.castHom ℝ) t =
      (1-t)^(k+1)*(coefficientPolynomial k).eval t := by
  simp only [endpointPolynomialQ, eval₂_mul, eval₂_pow, eval₂_sub, eval₂_one,
    eval₂_X, coefficientPolynomialQ_eval]

theorem middlePolynomialQ_eval (k : ℕ) (e : ℚ) (p : ℝ) :
    (middlePolynomialQ k e).eval₂ (Rat.castHom ℝ) p =
      (e : ℝ)*(1-(p+1))^(k+1)*(coefficientPolynomial k).eval (p+1) +
      (p+1)^(k+1)*(coefficientPolynomial k).eval (1-(p+1)) := by
  simp only [middlePolynomialQ, eval₂_add, eval₂_mul, eval₂_C, eval₂_comp,
    eval₂_X, eval₂_one, eval₂_neg, Rat.coe_castHom]
  rw [endpointPolynomialQ_eval, endpointPolynomialQ_eval]
  rw [show 1- -p = p+1 by ring, show -p = 1-(p+1) by ring]
  ring

theorem coefficientPolynomial_bound (k : ℕ) (t : ℝ) (ht : t ∈ Set.Icc 0 1) :
    (coefficientPolynomial k).eval t ∈ Set.Icc 0 (amplificationQ k : ℝ) := by
  constructor
  · exact (coefficientPolynomial_pos k t ht.1).le
  · rw [coefficientPolynomial_eval]
    calc
      _ ≤ ∑ _i ∈ Finset.range (k+1), (k+1 : ℝ)*2^(2*k) := by
        apply Finset.sum_le_sum
        intro i hi
        have hpow : t^i ≤ (1 : ℝ) := by
          simpa using pow_le_pow_left₀ ht.1 ht.2 i
        rw [← HermiteBernstein.sourceCoefficient_eq]
        exact (mul_le_of_le_one_right (HermiteBernstein.sourceCoefficient_nonneg k i) hpow).trans
          (sourceCoefficient_upper k i (by simpa using hi))
      _ = (amplificationQ k : ℝ) := by simp [amplificationQ]; ring

theorem endpointFactor_bound (k : ℕ) (t : ℝ) (ht : t ∈ Set.Icc 0 1) :
    (1-t)^(k+1)*(coefficientPolynomial k).eval t ∈ Set.Icc 0 (amplificationQ k : ℝ) := by
  have ha := coefficientPolynomial_bound k t ht
  have hp0 : 0 ≤ (1-t)^(k+1) := pow_nonneg (by linarith [ht.2]) _
  have hp1 : (1-t)^(k+1) ≤ (1 : ℝ) := by
    simpa using pow_le_pow_left₀ (by linarith [ht.2] : 0 ≤ 1-t) (by linarith [ht.1] : 1-t ≤ 1) (k+1)
  exact ⟨mul_nonneg hp0 ha.1, (mul_le_of_le_one_left ha.1 hp1).trans ha.2⟩

theorem expMidpoint_error (delta : ℚ) (hd : 0 < delta) :
    |(expMidpoint delta : ℝ) - Real.exp (-1)| ≤ (delta : ℝ)/2 := by
  have h := HermiteFiniteExpDegree.complete_enclosure (-1) delta (by norm_num) hd
  have hw : ((HermiteFiniteExp.bounds (-1) (HermiteFiniteExp.tailCutoff delta)
    (HermiteFiniteExpDegree.sourceDegree delta)).2 : ℝ) -
    ((HermiteFiniteExp.bounds (-1) (HermiteFiniteExp.tailCutoff delta)
    (HermiteFiniteExpDegree.sourceDegree delta)).1 : ℝ) ≤ (delta : ℝ) := by
    exact_mod_cast h.2
  simp only [Rat.cast_neg, Rat.cast_one, Set.mem_Icc] at h
  simp only [expMidpoint, Rat.cast_div, Rat.cast_add, Rat.cast_ofNat]
  apply abs_le.mpr
  constructor <;> linarith [h.1.1, h.1.2]

theorem middle_error (k : ℕ) (delta : ℚ) (p : ℝ)
    (hp : p ∈ Set.Icc (-1) 0) (hd : 0 < delta) :
    |(sourcePolynomial k delta).eval₂ (Rat.castHom ℝ) p-smoothInitial k p| ≤
      (delta : ℝ)/2*(amplificationQ k : ℝ) := by
  have ht : p+1 ∈ Set.Icc (0 : ℝ) 1 := ⟨by linarith [hp.1], by linarith [hp.2]⟩
  have hf := endpointFactor_bound k (p+1) ht
  rw [smoothInitial_middle k p hp, sourcePolynomial, middlePolynomialQ_eval,
    sourceInterpolant_eval]
  rw [show (expMidpoint delta : ℝ)*(1-(p+1))^(k+1)*(coefficientPolynomial k).eval (p+1) +
      (p+1)^(k+1)*(coefficientPolynomial k).eval (1-(p+1)) -
      (Real.exp (-1)*(1-(p+1))^(k+1)*(coefficientPolynomial k).eval (p+1) +
      (p+1)^(k+1)*(coefficientPolynomial k).eval (1-(p+1))) =
      ((expMidpoint delta : ℝ)-Real.exp (-1))*
      ((1-(p+1))^(k+1)*(coefficientPolynomial k).eval (p+1)) by ring]
  rw [abs_mul, abs_of_nonneg hf.1]
  exact mul_le_mul (expMidpoint_error delta hd) hf.2 hf.1 (by positivity)

theorem middle_central (k : ℕ) (delta : ℚ) : (sourcePolynomial k delta).eval 0 = 1 := by
  have hzero : (coefficientPolynomialQ k).eval 0 = 1 := by
    simp only [coefficientPolynomialQ, eval_finsetSum, eval_monomial]
    rw [Finset.sum_eq_single 0]
    · rw [coefficientQ_formula k 0 (by omega)]
      simp
    · intro i hi hne
      simp [zero_pow hne]
    · simp
  simp [sourcePolynomial, middlePolynomialQ, endpointPolynomialQ, hzero]

#print axioms coefficientQ_cast
#print axioms coefficientQ_formula
#print axioms coefficientPolynomialQ_eval
#print axioms endpointPolynomialQ_eval
#print axioms middlePolynomialQ_eval
#print axioms coefficientPolynomial_bound
#print axioms endpointFactor_bound
#print axioms expMidpoint_error
#print axioms middle_error
#print axioms middle_central

end HermiteFiniteMiddleSource
