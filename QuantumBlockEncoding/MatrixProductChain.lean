import QuantumBlockEncoding.TensorTrainCanonical

/-! Fixed-width matrix products with explicit boundaries become actual
dependent tensor chains. Boundary vectors are absorbed into the first and
last cores; no dense amplitude table or full-state decomposition is used.
The stored-core count below counts scalar addresses, not arithmetic runtime. -/

namespace QuantumBlockEncoding.MatrixProductChain
open TensorTrainCanonical

abbrev Kernel (D : Nat) := Nat → Fin 2 → _root_.Matrix (Fin D) (Fin D) ℝ

/-- Chronological finite matrix contraction, read from the first emitted bit. -/
noncomputable def readout {D : Nat} (K : Kernel D) (right : Fin D → ℝ)
    (start : Nat) : {n : Nat} → Word n → Fin D → ℝ
  | 0, _ => right
  | _ + 1, x => (K start x.1).mulVec (readout K right (start + 1) x.2)

/-- Absorb the terminal vector into the last core, leaving terminal rank one. -/
noncomputable def tailChain {D : Nat} (K : Kernel D) (right : Fin D → ℝ)
    (start : Nat) : (n : Nat) → Chain (n + 1) D 1
  | 0 => .cons (fun a out => (K start out.1).mulVec right a) (.nil 1)
  | n + 1 => .cons (fun a out => K start out.1 a out.2)
      (tailChain K right (start + 1) n)

theorem tailChain_contract {D : Nat} (K : Kernel D) (right : Fin D → ℝ)
    (start n : Nat) (x : Word (n + 1)) (a : Fin D) :
    contract (tailChain K right start n) x a 0 = readout K right start x a := by
  induction n generalizing start a with
  | zero => simp [tailChain, contract, slice, readout]
  | succ n ih =>
    change (∑ b, K start x.1 a b *
      contract (tailChain K right (start + 1) n) x.2 b 0) = _
    simp only [ih]
    rfl

/-- Contract an explicit left boundary into the first core only. -/
noncomputable def closeLeft {n D : Nat} (left : Fin D → ℝ) :
    Chain (n + 1) D 1 → Chain (n + 1) 1 1
  | .cons A C => .cons (fun _ out => ∑ a, left a * A a out) C

theorem closeLeft_contract {n D : Nat} (left : Fin D → ℝ)
    (C : Chain (n + 1) D 1) (x : Word (n + 1)) :
    contract (closeLeft left C) x 0 0 = ∑ a, left a * contract C x a 0 := by
  cases C with
  | cons A C =>
    simp only [closeLeft, contract, slice, _root_.Matrix.mul_apply,
      Finset.sum_mul, Finset.mul_sum, mul_assoc]
    exact Finset.sum_comm

/-- A scalar-boundary train whose coefficients are built from small matrices. -/
noncomputable def ofKernel {D : Nat} (K : Kernel D) (left right : Fin D → ℝ)
    (start n : Nat) : Chain (n + 1) 1 1 := closeLeft left (tailChain K right start n)

theorem ofKernel_contract {D : Nat} (K : Kernel D) (left right : Fin D → ℝ)
    (start n : Nat) (x : Word (n + 1)) :
    contract (ofKernel K left right start n) x 0 0 =
      ∑ a, left a * readout K right start x a := by
  rw [ofKernel, closeLeft_contract]
  simp only [tailChain_contract]

theorem tailChain_maxBond {D : Nat} (K : Kernel D) (right : Fin D → ℝ)
    (start n : Nat) : maxBond (tailChain K right start n) ≤ max D 1 := by
  induction n generalizing start with
  | zero => simp [tailChain, maxBond]
  | succ n ih => exact max_le (le_max_left _ _) (ih _)

theorem ofKernel_maxBond {D : Nat} (K : Kernel D) (left right : Fin D → ℝ)
    (start n : Nat) : maxBond (ofKernel K left right start n) ≤ max D 1 := by
  cases n with
  | zero =>
    change 1 ≤ max D 1
    exact le_max_right _ _
  | succ n => exact max_le (le_max_right _ _) (tailChain_maxBond K right (start + 1) n)

/-- Number of entries in the explicit dense *local* cores. -/
def storedScalars : {n l r : Nat} → Chain n l r → Nat
  | _, _, _, .nil _ => 0
  | _, l, _, @Chain.cons _ _ m _ _ C => 2 * l * m + storedScalars C

theorem storedScalars_le {n l r : Nat} (C : Chain n l r) (D : Nat)
    (h : maxBond C ≤ D) : storedScalars C ≤ 2 * n * D ^ 2 := by
  induction C with
  | nil r => simp [storedScalars]
  | @cons n l m r A C ih =>
    have hl : l ≤ D := (max_le_iff.mp h).1
    have ht : maxBond C ≤ D := (max_le_iff.mp h).2
    have hm : m ≤ D := by
      cases C with
      | nil r => exact ht
      | cons B C => exact (max_le_iff.mp ht).1
    have hc := ih ht
    have hab : l * m ≤ D * D := Nat.mul_le_mul hl hm
    simp only [storedScalars]
    nlinarith

theorem ofKernel_storedScalars {D : Nat} (K : Kernel D) (left right : Fin D → ℝ)
    (start n : Nat) : storedScalars (ofKernel K left right start n) ≤
      2 * (n + 1) * (max D 1) ^ 2 :=
  storedScalars_le _ _ (ofKernel_maxBond K left right start n)

end QuantumBlockEncoding.MatrixProductChain
