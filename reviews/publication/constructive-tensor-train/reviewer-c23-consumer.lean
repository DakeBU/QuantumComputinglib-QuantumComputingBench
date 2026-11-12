import QuantumBlockEncoding.ConstructiveTensorTrain

namespace CTTSourceFirstReviewerC23
open scoped BigOperators
open QuantumBlockEncoding.TensorTrainCanonical
open QuantumBlockEncoding.ConstructiveTensorTrain

#check CoreFactorization
#check factorCore
#check Result
#check canonicalize
#check canonicalize_rightCanonical
#check canonicalize_rankReduced
#check canonicalize_action
#check canonicalize_maxBond_le
#check boundary
#check boundary_action
#check boundary_mass
#check boundary_normalized
#check stateBoundary
#check stateBoundary_action
#check stateBoundary_normalized

-- The conjunction consumes the very same specified output; no existence replacement.
theorem symbolic_root {n l r : ℕ} (C : Chain n l r) (v : Fin l → ℝ) :
    RightCanonical (canonicalize C).canonical ∧
    RankReduced C (canonicalize C).canonical ∧
    maxBond (canonicalize C).canonical ≤ maxBond C ∧
    (∀ x : Word n, ∀ a : Fin l, ∀ j : Fin r,
      contract C x a j =
      ∑ k, (canonicalize C).residual a k *
        contract (canonicalize C).canonical x k j) ∧
    (∀ x : Word n, ∀ j : Fin r,
      _root_.Matrix.vecMul v (contract C x) j =
      _root_.Matrix.vecMul (boundary C v) (contract (canonicalize C).canonical x) j) ∧
    (∑ x : Word n, ∑ j : Fin r,
      (_root_.Matrix.vecMul v (contract C x) j) ^ 2) =
      ∑ k, (boundary C v k) ^ 2 := by
  refine ⟨canonicalize_rightCanonical C, canonicalize_rankReduced C,
    canonicalize_maxBond_le C, ?_, ?_, ?_⟩
  · intro x a j
    have h := congrFun (congrFun (canonicalize_action C x) a) j
    simpa only [_root_.Matrix.mul_apply] using h
  · intro x j
    exact congrFun (boundary_action C v x) j
  · exact boundary_mass C v

theorem normalized_only_with_source_premise {n l r : ℕ}
    (C : Chain n l r) (v : Fin l → ℝ) (source : chainMass C v = 1) :
    (∑ k, boundary C v k ^ 2) = 1 := boundary_normalized C v source

theorem scalar_consumer {n : ℕ} (C : Chain n 1 1)
    (source : (∑ x : Word n, contract C x 0 0 ^ 2) = 1) :
    (∀ x : Word n, contract C x 0 0 =
      ∑ a, stateBoundary C a * contract (canonicalize C).canonical x a 0) ∧
    (∑ a, stateBoundary C a ^ 2) = 1 :=
  ⟨stateBoundary_action C, stateBoundary_normalized C source⟩

theorem empty_dimension (r : ℕ) :
    (canonicalize (Chain.nil r)).rank = r := rfl

theorem empty_boundary (r : ℕ) (v : Fin r → ℝ) :
    boundary (Chain.nil r) v = v := by
  simp [boundary, canonicalize]

theorem head_dimension {n l m r : ℕ} (A : Core l m) (C : Chain n m r) :
    (canonicalize (Chain.cons A C)).rank = min l (2 * (canonicalize C).rank) := rfl

theorem zero_terminal_mass {n l : ℕ} (C : Chain n l 0) (v : Fin l → ℝ) :
    chainMass C v = 0 := by simp [chainMass, mass]

theorem zero_terminal_not_normalized {n l : ℕ} (C : Chain n l 0) (v : Fin l → ℝ) :
    chainMass C v ≠ 1 := by rw [zero_terminal_mass C v]; norm_num

theorem intermediate_zero_action {n l r : ℕ} (A : Core l 0)
    (C : Chain n 0 r) (x : Word (n + 1)) :
    contract (Chain.cons A C) x = 0 := by
  ext a j
  simp [contract, _root_.Matrix.mul_apply]

theorem product_address {r : ℕ} (b : Fin 2) (j : Fin r) :
    (finProdFinEquiv (b,j) : Fin (2 * r)).val = b.val * r + j.val := by
  change j.val + r * b.val = b.val * r + j.val
  simp only [Nat.mul_comm, Nat.add_comm]

theorem actual_core_factor {l r : ℕ} (A : Core l r) :
    A = (factorCore A).R * (factorCore A).Q ∧
    (factorCore A).Q * (factorCore A).Q.transpose = 1 :=
  ⟨(factorCore A).factorization, (factorCore A).orthogonal⟩

#print axioms symbolic_root
#print axioms scalar_consumer
#print axioms actual_core_factor
#print axioms zero_terminal_not_normalized
end CTTSourceFirstReviewerC23
