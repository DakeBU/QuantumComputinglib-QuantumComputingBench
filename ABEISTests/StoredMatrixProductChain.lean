import QuantumBlockEncoding.StoredMatrixProductChain

namespace QuantumBlockEncoding.StoredMatrixProductChainTests
open StoredGivens StoredTensorTrain TensorTrainCanonical StoredMatrixProductChain

def emptyTables (n : ℕ) : Vector (StoredCore 0 0) (n + 1) :=
  Vector.ofFn fun _ => Vector.ofFn fun a => Fin.elim0 a

def emptyBoundary : Vector ℝ 0 := Vector.ofFn Fin.elim0

set_option backward.isDefEq.respectTransparency false in
example (n : ℕ) (x : Word (n + 1)) :
    contract (denoteChain (ofTable (emptyTables n) emptyBoundary emptyBoundary).value) x 0 0 = 0 := by
  rw [ofTable_refines _ _ _ (fun _ _ a => Fin.elim0 a) 7]
  · rw [MatrixProductChain.ofKernel_contract]
    simp
  · intro i
    ext a
    exact Fin.elim0 a

example : StoredRectangularGivens.total
    (ofTable (emptyTables 0) emptyBoundary emptyBoundary).cost ≤ 31 := by
  simpa using ofTable_total_cost_le (emptyTables 0) emptyBoundary emptyBoundary

example : StoredRectangularGivens.total
    (ofTable (emptyTables 0) emptyBoundary emptyBoundary).cost = 31 := by
  norm_num [ofTable, tailChain, closeLeft, bind, Run.bind,
    StoredRectangularGivens.total, terminal_cost, initial_cost,
    nodeBudget, StoredGivens.read, charge, tick]
  decide

noncomputable def signedTables : Vector (StoredCore 1 1) 1 :=
  Vector.ofFn fun _ => Vector.ofFn fun _ => Vector.ofFn fun _ => -2

noncomputable def left : Vector ℝ 1 := Vector.ofFn fun _ => 3
noncomputable def right : Vector ℝ 1 := Vector.ofFn fun _ => -4

example : StoredRectangularGivens.total (ofTable signedTables left right).cost = 63 := by
  norm_num [ofTable, tailChain, closeLeft, bind, Run.bind,
    StoredRectangularGivens.total, terminal_cost, initial_cost,
    nodeBudget, StoredGivens.read, charge, tick]
  decide

set_option backward.isDefEq.respectTransparency false in
/-- Both boundaries must be absorbed even for the single core. -/
example (bit : Fin 2) :
    contract (denoteChain (ofTable signedTables left right).value) (bit, ()) 0 0 = 24 := by
  rw [ofTable_refines _ _ _ (fun _ _ _ _ => -2) 0]
  · norm_num [MatrixProductChain.ofKernel, MatrixProductChain.closeLeft,
      MatrixProductChain.tailChain, contract, slice, Matrix.mul_apply,
      Matrix.mulVec, dotProduct, left, right]
  · intro i
    ext a out
    simp [signedTables, denoteCore, denote]

noncomputable def orderedTables : Vector (StoredCore 1 1) 2 :=
  Vector.ofFn fun i => Vector.ofFn fun _ => Vector.ofFn fun j =>
    if i.val = 0 then (if j.val = 0 then -2 else 3) else 5

set_option backward.isDefEq.respectTransparency false in
/-- Chronological order, signed nonzero values, and two distinct bit slices. -/
example :
    contract (denoteChain (ofTable orderedTables left right).value) (0, 1, ()) 0 0 = 120 := by
  rw [ofTable_refines _ _ _ (fun level bit _ _ =>
    if level = 0 then (if bit.val = 0 then -2 else 3) else 5) 0]
  · norm_num [MatrixProductChain.ofKernel, MatrixProductChain.closeLeft,
      MatrixProductChain.tailChain, contract, slice, Matrix.mul_apply,
      Matrix.mulVec, dotProduct, left, right]
  · intro i
    ext a out
    rcases out with ⟨bit, b⟩
    fin_cases b
    fin_cases bit <;> simp [orderedTables, denoteCore, denote, finProdFinEquiv]

example :
    StoredRectangularGivens.total (ofTable orderedTables left right).cost ≤ 93 := by
  simpa using ofTable_total_cost_le orderedTables left right

#print axioms StoredMatrixProductChain.ofTable_refines
#print axioms StoredMatrixProductChain.ofTable_total_cost_le
#print axioms StoredMatrixProductChain.ofTable_certified

end QuantumBlockEncoding.StoredMatrixProductChainTests
