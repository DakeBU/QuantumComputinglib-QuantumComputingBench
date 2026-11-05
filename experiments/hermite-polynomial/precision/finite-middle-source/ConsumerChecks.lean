import FiniteMiddleSource

namespace HermiteFiniteMiddleSource

open Polynomial QuantumBlockEncoding HermitePolynomial

def coefficientValueQ (k : ℕ) (t : ℚ) : ℚ :=
  ∑ i ∈ Finset.range (k+1), coefficientQ k i*t^i

def middleValueQ (k : ℕ) (delta p : ℚ) : ℚ :=
  expMidpoint delta*(1-(p+1))^(k+1)*coefficientValueQ k (p+1) +
    (p+1)^(k+1)*coefficientValueQ k (1-(p+1))

theorem coefficientValueQ_eq (k : ℕ) (t : ℚ) :
    coefficientValueQ k t = (coefficientPolynomialQ k).eval t := by
  simp only [coefficientValueQ, coefficientPolynomialQ, eval_finsetSum, eval_monomial]

theorem middleValueQ_eq (k : ℕ) (delta p : ℚ) :
    middleValueQ k delta p = (sourcePolynomial k delta).eval p := by
  simp only [middleValueQ, sourcePolynomial, middlePolynomialQ, endpointPolynomialQ,
    eval_add, eval_mul, eval_C, eval_comp, eval_pow, eval_sub, eval_one,
    eval_X, eval_neg, coefficientValueQ_eq]
  rw [show 1- -p = p+1 by ring, show 1-(p+1) = -p by ring]
  ring

theorem rational_middle_error (k : ℕ) (delta p : ℚ)
    (hp : p ∈ Set.Icc (-1) 0) (hd : 0 < delta) :
    |(middleValueQ k delta p : ℝ) - smoothInitial k (p : ℝ)| ≤
      (delta : ℝ)/2*(amplificationQ k : ℝ) := by
  have hp' : (p : ℝ) ∈ Set.Icc (-1) 0 :=
    ⟨by exact_mod_cast hp.1, by exact_mod_cast hp.2⟩
  have h := middle_error k delta (p : ℝ) hp' hd
  rw [middleValueQ_eq]
  simpa only [← Rat.coe_castHom (α := ℝ), ← eval₂_at_apply] using h

theorem rational_central (k : ℕ) (delta : ℚ) : middleValueQ k delta 0 = 1 := by
  rw [middleValueQ_eq, middle_central]

theorem literal_left_endpoint (k : ℕ) (delta : ℚ) :
    middleValueQ k delta (-1) = expMidpoint delta := by
  have hc : coefficientValueQ k 0 = 1 := by
    simp only [coefficientValueQ]
    rw [Finset.sum_eq_single 0]
    · rw [coefficientQ_formula k 0 (by omega)]
      simp
    · intro i hi hne
      simp [zero_pow hne]
    · simp
  simp [middleValueQ, hc]

example : coefficientQ 3 0 = 1 := by norm_num [coefficientQ, ExperimentalCoefficientRange.sourceNumerator]
example : coefficientQ 3 1 = 5 := by norm_num [coefficientQ, ExperimentalCoefficientRange.sourceNumerator, Finset.sum_range_succ]
example : coefficientQ 3 2 = 29/2 := by norm_num [coefficientQ, ExperimentalCoefficientRange.sourceNumerator, Finset.sum_range_succ, Nat.choose]
example : coefficientQ 3 3 = 193/6 := by norm_num [coefficientQ, ExperimentalCoefficientRange.sourceNumerator, Finset.sum_range_succ, Nat.choose]
example : amplificationQ 0 = 1 := by norm_num [amplificationQ]
example : amplificationQ 3 = 1024 := by norm_num [amplificationQ]

#eval (List.map (fun k => middleValueQ k (1/1000) 0) [0,1,3,10,20])
#eval (List.map (fun k => decide (middleValueQ k 2 (-1) = expMidpoint 2)) [0,1,3,10,20])
#eval (List.map (fun k => middleValueQ k 0 0) [0,1,3,10,20])
#eval (coefficientQ 3 0, coefficientQ 3 1, coefficientQ 3 2, coefficientQ 3 3)
#eval (expMidpoint 2, middleValueQ 0 2 (-1/2))
#eval (middleValueQ 0 (1/1000) (-1/2) = (expMidpoint (1/1000)+1)/2)
#eval (decide (expMidpoint (1/1000) > 0), decide (expMidpoint (1/1000) < 1))
#print axioms coefficientValueQ_eq
#print axioms middleValueQ_eq
#print axioms rational_middle_error
#print axioms rational_central
#print axioms literal_left_endpoint

end HermiteFiniteMiddleSource
