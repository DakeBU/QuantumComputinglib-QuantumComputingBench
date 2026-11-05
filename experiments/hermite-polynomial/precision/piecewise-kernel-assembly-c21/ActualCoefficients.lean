import ActualDecomposition
import Mathlib.Algebra.Polynomial.Eval.Degree

namespace HermitePiecewiseAssembly
open scoped BigOperators
open Polynomial HermiteFiniteMiddleSource

def sourceCoefficientQ (k i : ℕ) : ℚ :=
  ∑ r ∈ Finset.range (i+1), (Nat.choose (k+i-r) k : ℚ)/(r.factorial : ℚ)

theorem sourceCoefficientQ_eq (k i : ℕ) (hi : i ≤ k) :
    sourceCoefficientQ k i = coefficientQ k i :=
  (coefficientQ_formula k i hi).symm

def middleCoeffQ (k : ℕ) (delta : ℚ) (j : ℕ) : ℚ :=
  (∑ i ∈ Finset.range (k+1),
    if k+1 ≤ j then expMidpoint delta*sourceCoefficientQ k i*(-1)^(k+1)*
      (Nat.choose i (j-(k+1)) : ℚ) else 0) +
  ∑ i ∈ Finset.range (k+1),
    if i ≤ j then sourceCoefficientQ k i*(-1)^i*(Nat.choose (k+1) (j-i) : ℚ) else 0

noncomputable def expandedMiddle (k : ℕ) (delta : ℚ) : ℚ[X] :=
  (∑ i ∈ Finset.range (k+1),
    monomial (k+1) (expMidpoint delta*sourceCoefficientQ k i*(-1)^(k+1))*(X+1)^i) +
  ∑ i ∈ Finset.range (k+1),
    monomial i (sourceCoefficientQ k i*(-1)^i)*(X+1)^(k+1)

private theorem shiftedCoeff (a : ℚ) (r i j : ℕ) :
    (monomial r a*(X+1)^i).coeff j =
      if r ≤ j then a*(Nat.choose i (j-r) : ℚ) else 0 := by
  rw [← C_mul_X_pow_eq_monomial, mul_assoc, coeff_C_mul, coeff_X_pow_mul']
  split_ifs <;> simp [coeff_X_add_one_pow]

theorem middleCoeffQ_eq (k : ℕ) (delta : ℚ) (j : ℕ) :
    middleCoeffQ k delta j = (expandedMiddle k delta).coeff j := by
  simp [middleCoeffQ, expandedMiddle, shiftedCoeff]

theorem expandedMiddle_eval (k : ℕ) (delta p : ℚ) :
    (expandedMiddle k delta).eval p = middleValueQ k delta p := by
  have hs : ∀ i ∈ Finset.range (k+1), sourceCoefficientQ k i = coefficientQ k i := by
    intro i hi
    exact sourceCoefficientQ_eq k i (by simp only [Finset.mem_range] at hi; omega)
  simp only [expandedMiddle, eval_add, eval_finsetSum, eval_mul, eval_monomial,
    eval_pow, eval_X, eval_one]
  unfold middleValueQ coefficientValueQ
  rw [show 1-(p+1) = -p by ring]
  have hpow : ∀ j : ℕ, (-p)^j = (-1)^j*p^j := fun j => neg_pow p j
  simp only [hpow, Finset.mul_sum]
  congr 1 <;> apply Finset.sum_congr rfl <;> intro i hi <;> rw [hs i hi] <;> ring

theorem expandedMiddle_degree (k : ℕ) (delta : ℚ) :
    (expandedMiddle k delta).natDegree ≤ 2*k+1 := by
  have hx : (X+1 : ℚ[X]).natDegree ≤ 1 := by
    exact (natDegree_add_le _ _).trans (by simp)
  unfold expandedMiddle
  apply natDegree_add_le_of_degree_le
  · apply natDegree_sum_le_of_forall_le
    intro i hi
    have hi' : i ≤ k := by simp only [Finset.mem_range] at hi; omega
    have hh := natDegree_mul_le_of_le
      (natDegree_monomial_le (m := k+1) (expMidpoint delta*sourceCoefficientQ k i*(-1)^(k+1)))
      (natDegree_pow_le_of_le i hx)
    simp only [Nat.mul_one] at hh
    omega
  · apply natDegree_sum_le_of_forall_le
    intro i hi
    have hi' : i ≤ k := by simp only [Finset.mem_range] at hi; omega
    have hh := natDegree_mul_le_of_le
      (natDegree_monomial_le (m := i) (sourceCoefficientQ k i*(-1)^i))
      (natDegree_pow_le_of_le (k+1) hx)
    simp only [Nat.mul_one] at hh
    omega

theorem middleCoeffQ_eval (k : ℕ) (delta p : ℚ) :
    (∑ j : Fin (2*k+1+1), middleCoeffQ k delta j.val*p^j.val) =
      middleValueQ k delta p := by
  simp only [middleCoeffQ_eq]
  calc
    _ = ∑ j ∈ Finset.range (2*k+1+1), (expandedMiddle k delta).coeff j*p^j :=
      Fin.sum_univ_eq_sum_range (fun j => (expandedMiddle k delta).coeff j*p^j) _
    _ = (expandedMiddle k delta).eval p :=
      (eval_eq_sum_range' (by have h := expandedMiddle_degree k delta; omega) p).symm
    _ = _ := expandedMiddle_eval k delta p

#print axioms sourceCoefficientQ_eq
#print axioms middleCoeffQ_eq
#print axioms middleCoeffQ_eval
end HermitePiecewiseAssembly
