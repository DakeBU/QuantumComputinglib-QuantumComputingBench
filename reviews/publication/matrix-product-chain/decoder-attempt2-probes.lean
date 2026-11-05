
set_option pp.universes true
set_option pp.explicit true

#check QuantumBlockEncoding.MatrixProductChain.Kernel
#print axioms QuantumBlockEncoding.MatrixProductChain.Kernel
#check QuantumBlockEncoding.MatrixProductChain.readout
#print axioms QuantumBlockEncoding.MatrixProductChain.readout
#check QuantumBlockEncoding.MatrixProductChain.tailChain
#print axioms QuantumBlockEncoding.MatrixProductChain.tailChain
#check QuantumBlockEncoding.MatrixProductChain.tailChain_contract
#print axioms QuantumBlockEncoding.MatrixProductChain.tailChain_contract
#check QuantumBlockEncoding.MatrixProductChain.closeLeft
#print axioms QuantumBlockEncoding.MatrixProductChain.closeLeft
#check QuantumBlockEncoding.MatrixProductChain.closeLeft_contract
#print axioms QuantumBlockEncoding.MatrixProductChain.closeLeft_contract
#check QuantumBlockEncoding.MatrixProductChain.ofKernel
#print axioms QuantumBlockEncoding.MatrixProductChain.ofKernel
#check QuantumBlockEncoding.MatrixProductChain.ofKernel_contract
#print axioms QuantumBlockEncoding.MatrixProductChain.ofKernel_contract
#check QuantumBlockEncoding.MatrixProductChain.tailChain_maxBond
#print axioms QuantumBlockEncoding.MatrixProductChain.tailChain_maxBond
#check QuantumBlockEncoding.MatrixProductChain.ofKernel_maxBond
#print axioms QuantumBlockEncoding.MatrixProductChain.ofKernel_maxBond
#check QuantumBlockEncoding.MatrixProductChain.storedScalars
#print axioms QuantumBlockEncoding.MatrixProductChain.storedScalars
#check QuantumBlockEncoding.MatrixProductChain.storedScalars_le
#print axioms QuantumBlockEncoding.MatrixProductChain.storedScalars_le
#check QuantumBlockEncoding.MatrixProductChain.ofKernel_storedScalars
#print axioms QuantumBlockEncoding.MatrixProductChain.ofKernel_storedScalars

namespace DecoderFresh
open QuantumBlockEncoding.TensorTrainCanonical
open QuantumBlockEncoding.MatrixProductChain

example {D : Nat} (K : Kernel D) (right : Fin D → ℝ) (start : Nat) :
    readout K right start (n := 0) () = right := rfl

example (r : Nat) : storedScalars (Chain.nil r) = 0 := rfl

example (r : Nat) : maxBond (Chain.nil r) = r := rfl

example (K : Kernel 0) (left right : Fin 0 → ℝ) (s n : Nat)
    (x : Word (n + 1)) : contract (ofKernel K left right s n) x 0 0 = 0 := by
  rw [ofKernel_contract]
  simp

example {D : Nat} (K : Kernel D) (left right : Fin D → ℝ) (s : Nat) :
    storedScalars (ofKernel K left right s 0) = 2 := rfl

example {D : Nat} (K : Kernel D) (left right : Fin D → ℝ) (s : Nat) :
    storedScalars (ofKernel K left right s 1) = 2 * 1 * D + (2 * D * 1 + 0) := rfl

example {D : Nat} (K : Kernel D) (left right : Fin D → ℝ) (s : Nat) :
    storedScalars (ofKernel K left right s 2) =
      2 * 1 * D + (2 * D * D + (2 * D * 1 + 0)) := rfl

example (K : Kernel 0) (left right : Fin 0 → ℝ) (s : Nat) :
    storedScalars (ofKernel K left right s 1) = 0 := rfl

example (K : Kernel 2) (left right : Fin 2 → ℝ) (s : Nat) :
    storedScalars (ofKernel K left right s 0) = 2 := rfl

example (K : Kernel 2) (left right : Fin 2 → ℝ) (s : Nat) :
    storedScalars (ofKernel K left right s 1) = 8 := rfl

example (K : Kernel 2) (left right : Fin 2 → ℝ) (s : Nat) :
    storedScalars (ofKernel K left right s 2) = 16 := rfl

example (K : Kernel 2) (left right : Fin 2 → ℝ) (s : Nat) :
    maxBond (ofKernel K left right s 0) = 1 := rfl

example (K : Kernel 0) (right : Fin 0 → ℝ) (s : Nat) :
    maxBond (tailChain K right s 0) = 1 := rfl

noncomputable def unitBoundary : Fin 2 → ℝ := fun a => if a = 0 then 1 else 0
noncomputable def A : _root_.Matrix (Fin 2) (Fin 2) ℝ :=
  fun a b => if a = 0 then (if b = 0 then 1 else 2) else (if b = 0 then 0 else 1)
noncomputable def B : _root_.Matrix (Fin 2) (Fin 2) ℝ :=
  fun a b => if a = 0 then (if b = 0 then 1 else 0) else (if b = 0 then 3 else 1)
noncomputable def ordered : Kernel 2 := fun s _ => if s = 4 then A else B
noncomputable def reversed : Kernel 2 := fun s _ => if s = 4 then B else A

example : contract (ofKernel ordered unitBoundary unitBoundary 4 1)
    (0, 1, ()) 0 0 = 7 := by
  norm_num [ofKernel, closeLeft, tailChain, contract, slice, Word, ordered,
    A, B, unitBoundary, _root_.Matrix.mulVec, _root_.Matrix.mul_apply,
    dotProduct, Fin.sum_univ_two]

example : contract (ofKernel reversed unitBoundary unitBoundary 4 1)
    (0, 1, ()) 0 0 = 1 := by
  norm_num [ofKernel, closeLeft, tailChain, contract, slice, Word, reversed,
    A, B, unitBoundary, _root_.Matrix.mulVec, _root_.Matrix.mul_apply,
    dotProduct, Fin.sum_univ_two]

noncomputable def indexed : Kernel 1 := fun s bit _ _ => (s : ℝ) + (bit.val : ℝ)

example : contract (ofKernel indexed (fun _ => 2) (fun _ => 3) 4 1)
    (0, 1, ()) 0 0 = 144 := by
  norm_num [ofKernel, closeLeft, tailChain, contract, slice, Word, indexed,
    _root_.Matrix.mulVec, _root_.Matrix.mul_apply, dotProduct]

example : contract (ofKernel indexed (fun _ => 2) (fun _ => 3) 4 1)
    (1, 0, ()) 0 0 = 150 := by
  norm_num [ofKernel, closeLeft, tailChain, contract, slice, Word, indexed,
    _root_.Matrix.mulVec, _root_.Matrix.mul_apply, dotProduct]

end DecoderFresh
