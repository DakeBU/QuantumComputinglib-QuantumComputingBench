import QuantumBlockEncoding.HermitePolynomial
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Algebra.Order.Floor.Semiring

/-!
# Explicit separation interfaces for structured Hermite samples

These algebraic factorization certificates are prerequisites for a low-rank
state-preparation route. They are not a gate compiler, an isometry completion,
or a finite-precision algorithm. In particular, a rank bound alone does not
close the polynomial-resource state-preparation task.
-/

noncomputable section

namespace QuantumBlockEncoding.HermiteCutRank

open Polynomial
open scoped BigOperators

variable {α β ι κ : Type*}

/-- Explicit finite-width separation, retaining both factors as witnesses. -/
def FactorsThrough [Fintype ι] (F : Matrix α β ℝ) : Prop :=
  ∃ A : Matrix α ι ℝ, ∃ B : Matrix ι β ℝ,
    ∀ x y, F x y = ∑ i, A x i * B i y

theorem FactorsThrough.rank_le [Fintype β] [Fintype ι]
    {F : Matrix α β ℝ} (h : FactorsThrough (ι := ι) F) :
    F.rank ≤ Fintype.card ι := by
  obtain ⟨A, B, h⟩ := h
  have hmul : F = A * B := by
    ext x y
    rw [Matrix.mul_apply]
    exact h x y
  rw [hmul]
  exact (Matrix.rank_mul_le_left A B).trans (Matrix.rank_le_card_width A)

/-- Taylor coefficients give a degree-sized factorization at any additive cut. -/
theorem polynomial_add_factorization (p : ℝ[X]) (d : ℕ)
    (hd : p.natDegree ≤ d) (u : α → ℝ) (v : β → ℝ) :
    FactorsThrough (ι := Fin (d + 1)) (fun x y => p.eval (u x + v y)) := by
  refine ⟨((fun x i => (taylor (u x) p).coeff i) :
      Matrix α (Fin (d + 1)) ℝ),
    ((fun i y => v y ^ (i : ℕ)) : Matrix (Fin (d + 1)) β ℝ), ?_⟩
  intro x y
  have hdegree : (taylor (u x) p).natDegree < d + 1 := by
    rw [natDegree_taylor]
    omega
  have he := eval_eq_sum_range' hdegree (v y)
  rw [taylor_eval, ← Fin.sum_univ_eq_sum_range] at he
  simpa only [add_comm] using he

theorem polynomial_add_rank_le [Fintype β] (p : ℝ[X]) (d : ℕ)
    (hd : p.natDegree ≤ d) (u : α → ℝ) (v : β → ℝ) :
    Matrix.rank (fun x y => p.eval (u x + v y) : Matrix α β ℝ) ≤ d + 1 := by
  simpa using (polynomial_add_factorization p d hd u v).rank_le

/-- Instantiates the existing Hermite degree theorem, rather than reproving it. -/
theorem hermite_polynomial_add_rank_le [Fintype β] (k : ℕ)
    (u : α → ℝ) (v : β → ℝ) :
    Matrix.rank (fun x y => (HermitePolynomial.sourceInterpolant k).eval (u x + v y) :
      Matrix α β ℝ) ≤ 2 * k + 2 := by
  simpa [Nat.add_assoc] using polynomial_add_rank_le
    (HermitePolynomial.sourceInterpolant k) (2 * k + 1)
    (HermitePolynomial.sourceInterpolant_degree k) u v

theorem product_factorization (u : α → ℝ) (v : β → ℝ) :
    FactorsThrough (ι := Unit) (fun x y => u x * v y) := by
  refine ⟨((fun x _ => u x) : Matrix α Unit ℝ),
    ((fun _ y => v y) : Matrix Unit β ℝ), ?_⟩
  intro x y
  simp

theorem exponential_add_factorization (u : α → ℝ) (v : β → ℝ) :
    FactorsThrough (ι := Unit) (fun x y => Real.exp (u x + v y)) := by
  simpa only [Real.exp_add] using product_factorization
    (fun x => Real.exp (u x)) (fun y => Real.exp (v y))

/-- A sum preserves an explicit direct-sum factorization. -/
theorem FactorsThrough.add [Fintype ι] [Fintype κ]
    {F G : Matrix α β ℝ} (hf : FactorsThrough (ι := ι) F)
    (hg : FactorsThrough (ι := κ) G) :
    FactorsThrough (ι := Sum ι κ) (fun x y => F x y + G x y) := by
  obtain ⟨A, B, hf⟩ := hf
  obtain ⟨C, D, hg⟩ := hg
  refine ⟨((fun x i => Sum.elim (A x) (C x) i) : Matrix α (Sum ι κ) ℝ),
    (Sum.elim B D : Matrix (Sum ι κ) β ℝ), ?_⟩
  intro x y
  change F x y + G x y = _
  rw [hf x y, hg x y, Fintype.sum_sum_type]
  rfl

theorem FactorsThrough.neg [Fintype ι]
    {F : Matrix α β ℝ} (hf : FactorsThrough (ι := ι) F) :
    FactorsThrough (ι := ι) (fun x y => -F x y) := by
  obtain ⟨A, B, hf⟩ := hf
  refine ⟨-A, B, ?_⟩
  intro x y
  change -F x y = _
  rw [hf x y]
  simp

/-- Entrywise multiplication multiplies widths, without constructing a dense matrix. -/
theorem FactorsThrough.pointwise_mul [Fintype ι] [Fintype κ]
    {F G : Matrix α β ℝ} (hf : FactorsThrough (ι := ι) F)
    (hg : FactorsThrough (ι := κ) G) :
    FactorsThrough (ι := ι × κ) (fun x y => F x y * G x y) := by
  obtain ⟨A, B, hf⟩ := hf
  obtain ⟨C, D, hg⟩ := hg
  refine ⟨((fun x i => A x i.1 * C x i.2) : Matrix α (ι × κ) ℝ),
    ((fun i y => B i.1 y * D i.2 y) : Matrix (ι × κ) β ℝ), ?_⟩
  intro x y
  change F x y * G x y = _
  rw [hf x y, hg x y]
  change (∑ i, A x i * B i y) * (∑ j, C x j * D j y) =
    ∑ ij : ι × κ, (A x ij.1 * C x ij.2) * (B ij.1 y * D ij.2 y)
  simp only [Fintype.sum_prod_type, Finset.sum_mul, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  ring

/-- The comparison of a concatenated prefix/suffix has only one boundary row. -/
theorem blockIndex_lt_iff (M x y T : ℕ) (hy : y < M) :
    M * x + y < T ↔ x < T / M ∨ (x = T / M ∧ y < T % M) := by
  have hM : 0 < M := by omega
  have hrem := Nat.mod_lt T hM
  have hdecomp := Nat.div_add_mod T M
  constructor
  · intro h
    by_cases hx : x < T / M
    · exact Or.inl hx
    · right
      have he : x = T / M := by
        by_contra hn
        have hq : T / M + 1 ≤ x := by omega
        nlinarith
      exact ⟨he, by subst x; omega⟩
  · rintro (hx | ⟨rfl, hy'⟩)
    · have hx' : x + 1 ≤ T / M := by omega
      have hmul := Nat.mul_le_mul_left M hx'
      calc
        M * x + y < M * x + M := Nat.add_lt_add_left hy _
        _ = M * (x + 1) := by rw [Nat.mul_add, Nat.mul_one]
        _ ≤ M * (T / M) := hmul
        _ ≤ T := by omega
    · omega

/-- An arbitrary threshold has a two-state separation across a binary cut. -/
theorem threshold_factorization (M T : ℕ) (u : α → ℕ) (v : β → ℕ)
    (hv : ∀ y, v y < M) :
    FactorsThrough (ι := Fin 2)
      (fun x y => if M * u x + v y < T then (1 : ℝ) else 0) := by
  refine ⟨((fun x => ![if u x < T / M then 1 else 0,
    if u x = T / M then 1 else 0]) : Matrix α (Fin 2) ℝ),
    (![(fun _ => 1), (fun y => if v y < T % M then 1 else 0)] :
      Matrix (Fin 2) β ℝ), ?_⟩
  intro x y
  change (if M * u x + v y < T then (1 : ℝ) else 0) =
    ∑ i : Fin 2, (![if u x < T / M then (1 : ℝ) else 0,
      if u x = T / M then 1 else 0] i) *
      (![(fun _ => (1 : ℝ)), (fun y => if v y < T % M then 1 else 0)] i y)
  simp only [Fin.sum_univ_two, Matrix.cons_val_zero,
    Matrix.cons_val_one, mul_one]
  simp only [blockIndex_lt_iff M (u x) (v y) T (hv y)]
  by_cases hl : u x < T / M
  · have he : u x ≠ T / M := Nat.ne_of_lt hl
    simp [hl, he]
  · by_cases he : u x = T / M <;> simp [hl, he]

/-- Complementing a threshold still needs two states, not a dense complement. -/
theorem threshold_complement_factorization (M T : ℕ) (u : α → ℕ) (v : β → ℕ)
    (hv : ∀ y, v y < M) :
    FactorsThrough (ι := Fin 2)
      (fun x y => 1 - if M * u x + v y < T then (1 : ℝ) else 0) := by
  refine ⟨((fun x => ![1 - if u x < T / M then 1 else 0,
    -(if u x = T / M then 1 else 0)]) : Matrix α (Fin 2) ℝ),
    (![(fun _ => 1), (fun y => if v y < T % M then 1 else 0)] :
      Matrix (Fin 2) β ℝ), ?_⟩
  intro x y
  change (1 - if M * u x + v y < T then (1 : ℝ) else 0) =
    ∑ i : Fin 2, (![1 - if u x < T / M then (1 : ℝ) else 0,
      -(if u x = T / M then 1 else 0)] i) *
      (![(fun _ => (1 : ℝ)), (fun y => if v y < T % M then 1 else 0)] i y)
  simp only [Fin.sum_univ_two, Matrix.cons_val_zero,
    Matrix.cons_val_one, mul_one]
  simp only [blockIndex_lt_iff M (u x) (v y) T (hv y)]
  by_cases hl : u x < T / M
  · have he : u x ≠ T / M := Nat.ne_of_lt hl
    simp [hl, he]
  · by_cases he : u x = T / M
    · by_cases hr : v y < T % M <;> simp [he, hr]
    · simp [hl, he]

/-- Relates the exact real grid to an integer cut; no bit-complexity claim. -/
theorem affine_lt_cut (a h t : ℝ) (hh : 0 < h) (j : ℕ) :
    a + h * (j : ℝ) < t ↔ j < Nat.ceil ((t - a) / h) := by
  rw [Nat.lt_ceil, lt_div_iff₀ hh]
  constructor <;> intro hc <;> nlinarith

/-- Endpoint continuity permits the zero sample to use the right exponential. -/
theorem smoothInitial_strict (k : ℕ) (p : ℝ) :
    HermitePolynomial.smoothInitial k p =
      if p < -1 then Real.exp p else
        if p < 0 then (HermitePolynomial.sourceInterpolant k).eval p
        else Real.exp (-p) := by
  have hzero : (HermitePolynomial.sourceInterpolant k).eval 0 = 1 := by
    simpa using HermitePolynomial.sourceInterpolant_right_jet k 0 (Nat.zero_le k)
  by_cases hl : p < -1
  · simp [HermitePolynomial.smoothInitial, hl]
  · by_cases hm : p < 0
    · simp [HermitePolynomial.smoothInitial, hl, hm, hm.le]
    · by_cases hz : p = 0
      · simp [hz, HermitePolynomial.smoothInitial, hzero]
      · have hp : ¬p ≤ 0 := by intro hp; exact hz (by linarith)
        simp [HermitePolynomial.smoothInitial, hl, hm, hp]

/-- Explicit index type of the three separated pieces. -/
abbrev HermiteBond (k : ℕ) :=
  Sum (Sum (Fin 2 × Unit) ((Sum (Fin 2) (Fin 2)) × Fin (2 * k + 2)))
    (Fin 2 × Unit)

theorem hermiteBond_card (k : ℕ) : Fintype.card (HermiteBond k) = 8 * k + 12 := by
  simp [HermiteBond, Fintype.card_sum, Fintype.card_prod]
  omega

/-- The literal Hermite samples, including both junctions, admit a bounded cut factorization. -/
theorem hermite_affine_factorization (k M : ℕ) (a h : ℝ) (hh : 0 < h)
    (u : α → ℕ) (v : β → ℕ) (hv : ∀ y, v y < M) :
    FactorsThrough (ι := HermiteBond k)
      (fun x y => HermitePolynomial.smoothInitial k
        (a + h * ((M * u x + v y : ℕ) : ℝ))) := by
  let A := Nat.ceil ((-1 - a) / h)
  let B := Nat.ceil ((0 - a) / h)
  let row : α → ℝ := fun x => a + h * ((M * u x : ℕ) : ℝ)
  let col : β → ℝ := fun y => h * (v y : ℝ)
  have hA := threshold_factorization M A u v hv
  have hB := threshold_factorization M B u v hv
  have hpoly := polynomial_add_factorization (HermitePolynomial.sourceInterpolant k)
    (2 * k + 1) (HermitePolynomial.sourceInterpolant_degree k) row col
  have hleft := hA.pointwise_mul (exponential_add_factorization row col)
  have hmiddle := (hB.add hA.neg).pointwise_mul hpoly
  have hright := (threshold_complement_factorization M B u v hv).pointwise_mul
    (exponential_add_factorization (fun x => -row x) (fun y => -col y))
  have hsum := (hleft.add hmiddle).add hright
  obtain ⟨leftFactor, rightFactor, hfactor⟩ := hsum
  refine ⟨leftFactor, rightFactor, ?_⟩
  intro x y
  rw [← hfactor x y]
  have hgrid : row x + col y = a + h * ((M * u x + v y : ℕ) : ℝ) := by
    simp only [row, col, Nat.cast_add]
    ring
  have hneg : -row x + -col y = -(row x + col y) := by ring
  simp only [Matrix.add_apply, Matrix.neg_apply, hneg, hgrid]
  rw [smoothInitial_strict]
  have hcutA := affine_lt_cut a h (-1) hh (M * u x + v y)
  have hcutB := affine_lt_cut a h 0 hh (M * u x + v y)
  change _ = ((if M * u x + v y < A then 1 else 0) * _ +
    ((if M * u x + v y < B then 1 else 0) +
      -(if M * u x + v y < A then 1 else 0)) * _) +
    (1 - if M * u x + v y < B then 1 else 0) * _
  dsimp [A, B]
  simp only [← hcutA, ← hcutB]
  by_cases hl : a + h * ((M * u x + v y : ℕ) : ℝ) < -1
  · have hm : a + h * ((M * u x + v y : ℕ) : ℝ) < 0 := by linarith
    simp only [hl, hm, if_true]
    ring
  · by_cases hm : a + h * ((M * u x + v y : ℕ) : ℝ) < 0 <;>
      simp only [hl, hm, if_true, if_false] <;> ring

theorem hermite_affine_cut_rank_le [Fintype β] (k M : ℕ) (a h : ℝ) (hh : 0 < h)
    (u : α → ℕ) (v : β → ℕ) (hv : ∀ y, v y < M) :
    Matrix.rank (fun x y => HermitePolynomial.smoothInitial k
      (a + h * ((M * u x + v y : ℕ) : ℝ))) ≤ 8 * k + 12 := by
  simpa only [hermiteBond_card] using
    (hermite_affine_factorization k M a h hh u v hv).rank_le

/-- A constant normalization can be absorbed into the left factor. -/
theorem FactorsThrough.scale [Fintype ι] {F : Matrix α β ℝ}
    (hf : FactorsThrough (ι := ι) F) (c : ℝ) :
    FactorsThrough (ι := ι) (fun x y => c * F x y) := by
  obtain ⟨A, B, hf⟩ := hf
  refine ⟨((fun x i => c * A x i) : Matrix α ι ℝ), B, ?_⟩
  intro x y
  change c * F x y = _
  rw [hf x y]
  simp [Finset.mul_sum, mul_assoc]

end QuantumBlockEncoding.HermiteCutRank
