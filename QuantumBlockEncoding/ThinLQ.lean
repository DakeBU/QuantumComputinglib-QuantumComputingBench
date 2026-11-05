import Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho
import Mathlib.Data.Matrix.Basic

/-!
# Exact finite real thin LQ factorization

The factor with orthonormal rows has exactly `min m n` rows, including for
rank-deficient matrices. These are existence and matrix-semantics theorems;
the noncomputable orthonormal completion does not supply an efficient algorithm.
-/

namespace QuantumBlockEncoding.ThinLQ

open scoped BigOperators
open InnerProductSpace

/-- Restrict a finite sum to a prefix when all remaining summands vanish. -/
theorem sum_prefix_of_zero {m n : ℕ} {M : Type*} [AddCommMonoid M]
    (hmn : m ≤ n) (f : Fin n → M) (hf : ∀ j, m ≤ j.val → f j = 0) :
    (∑ i : Fin m, f (Fin.castLE hmn i)) = ∑ j : Fin n, f j := by
  classical
  calc
    _ = ∑ j ∈ Finset.univ.image (Fin.castLE hmn), f j := by
      symm
      apply Finset.sum_image
      intro a _ b _ hab
      exact Fin.ext (congrArg (fun x : Fin n => x.val) hab)
    _ = _ := by
      apply Finset.sum_subset (Finset.subset_univ _)
      intro j _ hj
      apply hf
      by_contra hn
      apply hj
      exact Finset.mem_image.mpr ⟨⟨j.val, by omega⟩, Finset.mem_univ _, Fin.ext rfl⟩

/-- A wide real matrix has an exact factorization with orthonormal rows.
No linear-independence or nonzero-row assumption is required. -/
theorem exists_factor_of_le {m n : ℕ} (hmn : m ≤ n)
    (A : _root_.Matrix (Fin m) (Fin n) ℝ) :
    ∃ (R : _root_.Matrix (Fin m) (Fin m) ℝ)
      (Q : _root_.Matrix (Fin m) (Fin n) ℝ),
      A = R * Q ∧ Q * Q.transpose = 1 := by
  classical
  let f : Fin n → EuclideanSpace ℝ (Fin n) := fun i =>
    WithLp.toLp 2 (if h : i.val < m then A ⟨i.val, h⟩ else 0)
  have hd : Module.finrank ℝ (EuclideanSpace ℝ (Fin n)) = Fintype.card (Fin n) := by
    simp
  let b := gramSchmidtOrthonormalBasis (𝕜 := ℝ) hd f
  let R : _root_.Matrix (Fin m) (Fin m) ℝ := fun i k =>
    b.repr (f (Fin.castLE hmn i)) (Fin.castLE hmn k)
  let Q : _root_.Matrix (Fin m) (Fin n) ℝ := fun k j => b (Fin.castLE hmn k) j
  refine ⟨R, Q, ?_, ?_⟩
  · ext i j
    have hz (k : Fin n) (hk : m ≤ k.val) :
        b.repr (f (Fin.castLE hmn i)) k = 0 := by
      apply gramSchmidtOrthonormalBasis_inv_triangular' hd f
      change i.val < k.val
      omega
    have hs := sum_prefix_of_zero hmn
      (fun k => b.repr (f (Fin.castLE hmn i)) k * b k j)
      (fun k hk => by simp only [hz k hk, zero_mul])
    have hb := congrArg (fun v : EuclideanSpace ℝ (Fin n) => v j)
      (b.sum_repr (f (Fin.castLE hmn i)))
    simp only [WithLp.ofLp_sum, Finset.sum_apply, WithLp.ofLp_smul,
      Pi.smul_apply, smul_eq_mul] at hb
    rw [_root_.Matrix.mul_apply]
    change A i j = ∑ k : Fin m,
      b.repr (f (Fin.castLE hmn i)) (Fin.castLE hmn k) * b (Fin.castLE hmn k) j
    rw [hs, hb]
    simp [f, i.isLt]
  · ext i j
    have hb := b.inner_eq_ite (Fin.castLE hmn i) (Fin.castLE hmn j)
    simp only [PiLp.inner_apply] at hb
    rw [_root_.Matrix.mul_apply]
    change (∑ k, b (Fin.castLE hmn i) k * b (Fin.castLE hmn j) k) =
      (if i = j then (1 : ℝ) else 0)
    simpa [mul_comm] using hb

/-- Every finite real matrix admits a thin factorization with exactly
`min m n` orthonormal rows. This includes rank-deficient and empty matrices. -/
theorem exists_thin_lq {m n : ℕ} (A : _root_.Matrix (Fin m) (Fin n) ℝ) :
    ∃ (R : _root_.Matrix (Fin m) (Fin (min m n)) ℝ)
      (Q : _root_.Matrix (Fin (min m n)) (Fin n) ℝ),
      A = R * Q ∧ Q * Q.transpose = 1 := by
  by_cases hmn : m ≤ n
  · have hmin : min m n = m := min_eq_left hmn
    rw [hmin]
    exact exists_factor_of_le hmn A
  · have hnm : n ≤ m := by omega
    have hmin : min m n = n := min_eq_right hnm
    rw [hmin]
    exact ⟨A, 1, by simp, by simp⟩

end QuantumBlockEncoding.ThinLQ
