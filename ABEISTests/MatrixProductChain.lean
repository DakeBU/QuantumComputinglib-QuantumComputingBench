import QuantumBlockEncoding.MatrixProductChain

open QuantumBlockEncoding.TensorTrainCanonical QuantumBlockEncoding.MatrixProductChain

noncomputable section

def scalarKernel : Kernel 1 := fun t bit _ _ =>
  if t = 0 then (if bit = 0 then 2 else 3) else (if bit = 0 then 5 else 7)

-- The first emitted bit is the first kernel argument; this catches reversal.
example : contract (ofKernel scalarKernel (fun _ => 1) (fun _ => 1) 0 1)
    ((0 : Fin 2), ((1 : Fin 2), ())) 0 0 = 14 := by
  have h := ofKernel_contract scalarKernel (fun _ => 1) (fun _ => 1) 0 1 (0, (1, ()))
  norm_num [readout, scalarKernel, _root_.Matrix.mulVec, dotProduct] at h
  exact h

example : contract (ofKernel scalarKernel (fun _ => 1) (fun _ => 1) 0 1)
    ((1 : Fin 2), ((0 : Fin 2), ())) 0 0 = 15 := by
  have h := ofKernel_contract scalarKernel (fun _ => 1) (fun _ => 1) 0 1 (1, (0, ()))
  norm_num [readout, scalarKernel, _root_.Matrix.mulVec, dotProduct] at h
  exact h

-- An empty interior bond yields zero amplitudes, without nonempty assumptions.
example (K : Kernel 0) (left right : Fin 0 → ℝ) (n : Nat) (x : Word (n + 1)) :
    contract (ofKernel K left right 0 n) x 0 0 = 0 := by
  rw [ofKernel_contract]
  simp

example (D n : Nat) (K : Kernel D) (left right : Fin D → ℝ) :
    storedScalars (ofKernel K left right 0 n) ≤ 2 * (n + 1) * (max D 1) ^ 2 :=
  ofKernel_storedScalars K left right 0 n

#print axioms ofKernel_contract
#print axioms ofKernel_maxBond
#print axioms ofKernel_storedScalars
