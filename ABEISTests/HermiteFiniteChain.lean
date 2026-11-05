import QuantumBlockEncoding.HermiteFiniteChain

open QuantumBlockEncoding TensorTrainCanonical TensorTrainWord HermiteFiniteChain

example : toBits (n := 3) (((1 : Fin 2), ((0 : Fin 2), ((1 : Fin 2), ()))) : Word 3) =
    [true, false, true] := rfl

example : (sampleEquiv 3 (((1 : Fin 2), ((1 : Fin 2), ((0 : Fin 2), ()))) : Word 3)).val = 6 := by
  exact (sampleEquiv_value (n := 3) (1, (1, (0, ())))).trans (by decide)

example : (sampleEquiv 3 (((0 : Fin 2), ((1 : Fin 2), ((1 : Fin 2), ()))) : Word 3)).val = 3 := by
  exact (sampleEquiv_value (n := 3) (0, (1, (1, ())))).trans (by decide)

example (n : Nat) (x : PrimitiveBasis n) :
    sampleEquiv n (TensorTrainSchedule.wordOfBasis (fun i => x i.rev)) =
      primitiveBasisLEEquiv n x := sampleEquiv_public x

example (k n : Nat) (L : ℝ) (hL : 0 < L) :
    (∑ x : Word (n + 1), (contract (sourceChain k n L) x 0 0) ^ 2) = 1 :=
  sourceChain_normalized k n L hL

example (k n : Nat) (L : ℝ) :
    maxBond (sourceChain k n L) ≤ 2 * k + 6 := sourceChain_maxBond k n L

example : bondQubits 2 = 4 := by decide
example : bondQubits 8 = 5 := by decide

#print axioms sampleEquiv_value
#print axioms sampleEquiv_public
#print axioms sourceChain_contract
#print axioms sourceChain_normalized
#print axioms sourceChain_storage
#print axioms cubic_stage_budget
