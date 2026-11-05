import QuantumBlockEncoding.ConstructiveTensorTrain

open scoped BigOperators
open QuantumBlockEncoding.TensorTrainCanonical
open QuantumBlockEncoding.ConstructiveTensorTrain

namespace DecoderC23

-- Every terminal component, not a selected terminal sector.
theorem all_terminal_action {n l r : ℕ} (C : Chain n l r)
    (v : Fin l → ℝ) (x : Word n) (b : Fin r) :
    (∑ a : Fin l, v a * contract C x a b) =
      ∑ a : Fin (canonicalize C).rank,
        boundary C v a * contract (canonicalize C).canonical x a b := by
  exact congrFun (boundary_action C v x) b

theorem full_terminal_mass {n l r : ℕ} (C : Chain n l r) (v : Fin l → ℝ) :
    (∑ x : Word n, ∑ b : Fin r,
      (∑ a : Fin l, v a * contract C x a b) ^ 2) =
      ∑ a : Fin (canonicalize C).rank, boundary C v a ^ 2 := by
  exact boundary_mass C v

theorem normalization_iff {n l r : ℕ} (C : Chain n l r) (v : Fin l → ℝ) :
    mass (boundary C v) = 1 ↔ chainMass C v = 1 := by
  rw [boundary_mass]

theorem nil_rank (r : ℕ) : (canonicalize (Chain.nil r)).rank = r := rfl

theorem nil_boundary (r : ℕ) (v : Fin r → ℝ) :
    boundary (Chain.nil r) v = v := by
  simp [boundary, canonicalize]

theorem backward_rank {n l m r : ℕ} (A : Core l m) (C : Chain n m r) :
    (canonicalize (.cons A C)).rank = min l (2 * (canonicalize C).rank) := rfl

theorem empty_left_mass {n r : ℕ} (C : Chain n 0 r) (v : Fin 0 → ℝ) :
    chainMass C v = 0 := by
  simp [chainMass, mass, _root_.Matrix.vecMul, dotProduct]

theorem empty_terminal_mass {n l : ℕ} (C : Chain n l 0) (v : Fin l → ℝ) :
    mass (boundary C v) = 0 := by
  rw [← boundary_mass]
  simp [chainMass, mass]

theorem empty_terminal_not_normalized {n l : ℕ} (C : Chain n l 0)
    (v : Fin l → ℝ) : chainMass C v ≠ 1 := by
  have hz : chainMass C v = 0 := by simp [chainMass, mass]
  rw [hz]
  norm_num

-- Rank-deficient zero cores are legal inputs, without a normalization proof.
theorem zero_head_mass {n l m r : ℕ} (C : Chain n m r) (v : Fin l → ℝ) :
    mass (boundary (.cons (0 : Core l m) C) v) = 0 := by
  rw [← boundary_mass]
  simp [chainMass, contract, slice, mass, _root_.Matrix.vecMul, dotProduct,
    _root_.Matrix.mul_apply]

-- Signed, non-unit mass survives unchanged at length zero.
theorem signed_nil_mass : mass (boundary (Chain.nil 1) (fun _ => -3)) = 9 := by
  rw [nil_boundary]
  norm_num [mass]

-- Selecting one of two terminal labels loses half the mass in this example.
theorem two_terminal_mass : mass (boundary (Chain.nil 2) (fun _ => 1)) = 2 := by
  rw [nil_boundary]
  norm_num [mass, Fin.sum_univ_two]

theorem selected_terminal_mass :
    (∑ _x : Word 0,
      (_root_.Matrix.vecMul (fun _ : Fin 2 => (1 : ℝ))
        (contract (Chain.nil 2) _x) 0) ^ 2) = 1 := by
  simp [Word, contract]

end DecoderC23

#print axioms DecoderC23.all_terminal_action
#print axioms DecoderC23.full_terminal_mass
#print axioms DecoderC23.normalization_iff
#print axioms DecoderC23.nil_rank
#print axioms DecoderC23.nil_boundary
#print axioms DecoderC23.backward_rank
#print axioms DecoderC23.empty_left_mass
#print axioms DecoderC23.empty_terminal_mass
#print axioms DecoderC23.empty_terminal_not_normalized
#print axioms DecoderC23.zero_head_mass
#print axioms DecoderC23.signed_nil_mass
#print axioms DecoderC23.two_terminal_mass
#print axioms DecoderC23.selected_terminal_mass
