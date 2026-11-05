import QuantumBlockEncoding.RectangularGivens
import QuantumBlockEncoding.ThinLQ

/-!
# Deterministic exact-real thin LQ factors

For a wide matrix, eliminate its transpose and extract the prefix of the
accumulated orthogonal transform. For a tall matrix, use the original matrix
and the identity. No basis-extension or existential factor selection is used.
The factors have exactly `min m n` inner dimension, even at deficient rank.
No arithmetic evaluation or bit-complexity claim is made here.
-/

namespace QuantumBlockEncoding.ConstructiveThinLQ

open scoped BigOperators
open RectangularGivens

/-- Actual factors together with the same two equations as `ThinLQ`. -/
structure Factorization {m n : ℕ} (A : _root_.Matrix (Fin m) (Fin n) ℝ) (r : ℕ) where
  R : _root_.Matrix (Fin m) (Fin r) ℝ
  Q : _root_.Matrix (Fin r) (Fin n) ℝ
  factorization : A = R * Q
  orthogonal : Q * Q.transpose = 1

noncomputable def wideR {m n : ℕ} (hmn : m ≤ n)
    (A : _root_.Matrix (Fin m) (Fin n) ℝ) : _root_.Matrix (Fin m) (Fin m) ℝ :=
  fun i k => reduced A.transpose (Fin.castLE hmn k) i

noncomputable def wideQ {m n : ℕ} (hmn : m ≤ n)
    (A : _root_.Matrix (Fin m) (Fin n) ℝ) : _root_.Matrix (Fin m) (Fin n) ℝ :=
  fun k j => transform A.transpose (Fin.castLE hmn k) j

theorem wide_factorization {m n : ℕ} (hmn : m ≤ n)
    (A : _root_.Matrix (Fin m) (Fin n) ℝ) : A = wideR hmn A * wideQ hmn A := by
  have recovery : (reduced A.transpose).transpose * transform A.transpose = A := by
    have h := congrArg _root_.Matrix.transpose (exact_recovery A.transpose)
    simpa only [_root_.Matrix.transpose_mul, _root_.Matrix.transpose_transpose] using h
  ext i j
  have entry := congrFun (congrFun recovery i) j
  have restrictedSum := ThinLQ.sum_prefix_of_zero hmn
    (fun k => reduced A.transpose k i * transform A.transpose k j) (by
      intro k hk
      change reduced A.transpose k i * transform A.transpose k j = 0
      rw [reduced_zero_below A.transpose k i (by omega), zero_mul])
  change A i j = ∑ k : Fin m,
    reduced A.transpose (Fin.castLE hmn k) i * transform A.transpose (Fin.castLE hmn k) j
  rw [restrictedSum]
  exact entry.symm

theorem wide_orthogonal {m n : ℕ} (hmn : m ≤ n)
    (A : _root_.Matrix (Fin m) (Fin n) ℝ) : wideQ hmn A * (wideQ hmn A).transpose = 1 := by
  have orthogonal : transform A.transpose * (transform A.transpose).transpose = 1 :=
    mul_eq_one_comm.mp (transform_orthogonal A.transpose)
  ext i j
  have entry := congrFun (congrFun orthogonal (Fin.castLE hmn i)) (Fin.castLE hmn j)
  simpa [wideQ, _root_.Matrix.mul_apply, _root_.Matrix.transpose_apply,
    _root_.Matrix.one_apply] using entry

/-- A deterministic wide-matrix supplier, including zero and repeated rows. -/
noncomputable def factorOfLE {m n : ℕ} (hmn : m ≤ n)
    (A : _root_.Matrix (Fin m) (Fin n) ℝ) : Factorization A m where
  R := wideR hmn A
  Q := wideQ hmn A
  factorization := wide_factorization hmn A
  orthogonal := wide_orthogonal hmn A

/-- All shapes are handled by an explicit dimension comparison and recursion. -/
noncomputable def factor {m n : ℕ} (A : _root_.Matrix (Fin m) (Fin n) ℝ) :
    Factorization A (min m n) := by
  by_cases hmn : m ≤ n
  · rw [min_eq_left hmn]
    exact factorOfLE hmn A
  · rw [min_eq_right (show n ≤ m by omega)]
    exact ⟨A, 1, by simp, by simp⟩

/-- The concrete output satisfies the existing all-shape thin-LQ contract. -/
theorem factor_correct {m n : ℕ} (A : _root_.Matrix (Fin m) (Fin n) ℝ) :
    A = (factor A).R * (factor A).Q ∧ (factor A).Q * (factor A).Q.transpose = 1 :=
  ⟨(factor A).factorization, (factor A).orthogonal⟩

end QuantumBlockEncoding.ConstructiveThinLQ
