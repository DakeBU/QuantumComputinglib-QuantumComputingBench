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

namespace IndependentSourceReviewer
open QuantumBlockEncoding.TensorTrainCanonical
open QuantumBlockEncoding.MatrixProductChain
set_option pp.explicit false
set_option pp.universes false

example {D : Nat} (K : Kernel D) (r : Fin D → ℝ) (s : Nat) :
    readout K r s (n := 0) () = r := rfl
example (r : Nat) : storedScalars (Chain.nil r) = 0 := rfl
example (r : Nat) : maxBond (Chain.nil r) = r := rfl
example (K : Kernel 0) (l r : Fin 0 → ℝ) (s n : Nat) (x : Word (n+1)) :
    contract (ofKernel K l r s n) x 0 0 = 0 := by
  rw [ofKernel_contract]
  simp
example {D : Nat} (K : Kernel D) (l r : Fin D → ℝ) (s : Nat) :
    storedScalars (ofKernel K l r s 0) = 2 := rfl
example {D : Nat} (K : Kernel D) (l r : Fin D → ℝ) (s : Nat) :
    maxBond (ofKernel K l r s 0) = 1 := rfl
example (K : Kernel 0) (l r : Fin 0 → ℝ) (s : Nat) :
    storedScalars (ofKernel K l r s 2) = 0 := rfl
example {D : Nat} (K : Kernel D) (l r : Fin D → ℝ) (s : Nat) :
    storedScalars (ofKernel K l r s 3) =
      2 * 1 * D + (2 * D * D + (2 * D * D + (2 * D * 1 + 0))) := rfl
example (A : Core 0 0) : storedScalars (.cons A (.nil 0)) = 0 := rfl

def word01 : Word 2 := (0, 1, ())
def word10 : Word 2 := (1, 0, ())
def word0 : Word 1 := (0, ())
noncomputable def l2 : Fin 2 → ℝ := fun i => if i = 0 then 1 else 0
noncomputable def r2 : Fin 2 → ℝ := fun i => if i = 1 then 1 else 0
noncomputable def A : _root_.Matrix (Fin 2) (Fin 2) ℝ :=
  fun i j => if i = 0 ∧ j = 1 then 1 else 0
noncomputable def B : _root_.Matrix (Fin 2) (Fin 2) ℝ :=
  fun i j => if i = 0 ∧ j = 0 then 1 else 0
noncomputable def AB : Kernel 2 := fun s _ => if s = 5 then A else B
noncomputable def BA : Kernel 2 := fun s _ => if s = 5 then B else A
example : contract (ofKernel AB l2 r2 5 1) word01 0 0 = 0 := by
  rw [ofKernel_contract]
  norm_num [readout, word01, AB, A, B, l2, r2, _root_.Matrix.mulVec,
    dotProduct, Fin.sum_univ_two]
example : contract (ofKernel BA l2 r2 5 1) word01 0 0 = 1 := by
  rw [ofKernel_contract]
  norm_num [readout, word01, BA, A, B, l2, r2, _root_.Matrix.mulVec,
    dotProduct, Fin.sum_univ_two]
noncomputable def signed : Kernel 1 := fun _ _ _ _ => -2
example : contract (ofKernel signed (fun _ => 1) (fun _ => 1) 7 0) word0 0 0 = -2 := by
  rw [ofKernel_contract]
  norm_num [readout, word0, signed, _root_.Matrix.mulVec, dotProduct]
noncomputable def indexed : Kernel 1 := fun s b _ _ => (s : ℝ) + 2 * (b.val : ℝ)
example : contract (ofKernel indexed (fun _ => -2) (fun _ => 3) 3 1) word01 0 0 = -108 := by
  rw [ofKernel_contract]
  norm_num [readout, word01, indexed, _root_.Matrix.mulVec, dotProduct]
example : contract (ofKernel indexed (fun _ => -2) (fun _ => 3) 3 1) word10 0 0 = -120 := by
  rw [ofKernel_contract]
  norm_num [readout, word10, indexed, _root_.Matrix.mulVec, dotProduct]
end IndependentSourceReviewer
