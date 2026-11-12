import QuantumBlockEncoding.HermitePolynomial
import Mathlib.Data.Matrix.Mul

/-!
# Formula-derived polynomial transfer cores

The transfer matrix is explicit and has dimension `d + 1`, independent of
the number of binary digits.  This file proves forward amplitude semantics,
not a numerical QR guarantee or a primitive-gate compilation theorem.
-/

noncomputable section

open scoped BigOperators Matrix
open Matrix

namespace QuantumBlockEncoding.HermiteTransferCores

/-- Monomial row features through degree `d`. -/
def rowFeatures (d : ℕ) (x : ℝ) : Fin (d + 1) → ℝ := fun i => x ^ i.val

/-- Explicit binomial translation core.  Entries below the diagonal vanish
because the corresponding binomial coefficient is zero. -/
def translationCore (d : ℕ) (w : ℝ) : Matrix (Fin (d + 1)) (Fin (d + 1)) ℝ :=
  Matrix.of fun i j => (j.val.choose i.val : ℝ) * w ^ (j.val - i.val)

theorem translationCore_below_diagonal (d : ℕ) (w : ℝ) (i j : Fin (d + 1))
    (h : j.val < i.val) : translationCore d w i j = 0 := by
  simp [translationCore, Nat.choose_eq_zero_of_lt h]

/-- The binomial theorem gives the exact single-core update. -/
theorem rowFeatures_translationCore (d : ℕ) (x w : ℝ) :
    rowFeatures d x ᵥ* translationCore d w = rowFeatures d (x + w) := by
  funext j
  simp only [Matrix.vecMul, dotProduct, rowFeatures, translationCore, Matrix.of_apply]
  rw [Fin.sum_univ_eq_sum_range (fun i => x ^ i * ((j.val.choose i : ℝ) * w ^ (j.val - i)))]
  have hs : (∑ i ∈ Finset.range (d + 1),
      x ^ i * ((j.val.choose i : ℝ) * w ^ (j.val - i))) =
      ∑ i ∈ Finset.range (j.val + 1),
        x ^ i * ((j.val.choose i : ℝ) * w ^ (j.val - i)) := by
    apply (Finset.sum_subset (Finset.range_mono (by omega)) ?_).symm
    intro i hi hnot
    have hj : j.val < i := by
      simp only [Finset.mem_range, not_lt] at hnot
      omega
    simp [Nat.choose_eq_zero_of_lt hj]
  rw [hs, add_pow]
  apply Finset.sum_congr rfl
  intro i hi
  ring

/-- Sequentially contract the explicit cores, without enumerating bit strings. -/
def transfer (d : ℕ) : List ℝ → (Fin (d + 1) → ℝ) → (Fin (d + 1) → ℝ)
  | [], v => v
  | w :: ws, v => transfer d ws (v ᵥ* translationCore d w)

theorem transfer_rowFeatures (d : ℕ) (weights : List ℝ) (origin : ℝ) :
    transfer d weights (rowFeatures d origin) = rowFeatures d (origin + weights.sum) := by
  induction weights generalizing origin with
  | nil => simp [transfer]
  | cons w ws ih =>
    simp only [transfer, rowFeatures_translationCore, ih, List.sum_cons]
    congr 1
    ring

/-- Contract the last bond against the polynomial's coefficient vector. -/
def polynomialAmplitude (d : ℕ) (p : Polynomial ℝ) (origin : ℝ) (weights : List ℝ) : ℝ :=
  transfer d weights (rowFeatures d origin) ⬝ᵥ fun i => p.coeff i.val

theorem polynomialAmplitude_eq_eval (d : ℕ) (p : Polynomial ℝ)
    (hp : p.natDegree ≤ d) (origin : ℝ) (weights : List ℝ) :
    polynomialAmplitude d p origin weights = p.eval (origin + weights.sum) := by
  rw [polynomialAmplitude, transfer_rowFeatures]
  simp only [dotProduct, rowFeatures]
  rw [Fin.sum_univ_eq_sum_range (fun i => (origin + weights.sum) ^ i * p.coeff i),
    Polynomial.eval_eq_sum_range' (by omega : p.natDegree < d + 1)]
  apply Finset.sum_congr rfl
  intro i hi
  exact mul_comm _ _

/-- The actual source Hermite polynomial, with no assumed interpolation data. -/
theorem sourceInterpolant_transfer (k : ℕ) (origin : ℝ) (weights : List ℝ) :
    polynomialAmplitude (2 * k + 1) (HermitePolynomial.sourceInterpolant k) origin weights =
      (HermitePolynomial.sourceInterpolant k).eval (origin + weights.sum) :=
  polynomialAmplitude_eq_eval _ _ (HermitePolynomial.sourceInterpolant_degree k) _ _

/-- The exact core dimensions are linear in the interpolation order. -/
theorem source_transfer_dimension (k : ℕ) : Fintype.card (Fin ((2 * k + 1) + 1)) =
    2 * k + 2 := by simp

end QuantumBlockEncoding.HermiteTransferCores
