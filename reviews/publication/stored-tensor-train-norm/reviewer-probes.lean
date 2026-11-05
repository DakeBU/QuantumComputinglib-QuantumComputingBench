namespace QuantumBlockEncoding.StoredTensorTrainNorm
open scoped BigOperators
open StoredGivens StoredTensorTrain TensorTrainCanonical

-- The terminal label is summed, never projected to a preferred sector.
example {n l r : ℕ} (C : StoredChain n l r) (a c : Fin l) :
    denote (gram C).value a c = ∑ x : Word n, ∑ t : Fin r,
      contract (denoteChain C) x a t * contract (denoteChain C) x c t := by
  rw [gram_value, TensorTrainNormEnvironment.gram_eq_sum]
  simp [Matrix.sum_apply, Matrix.mul_apply, Matrix.transpose_apply]

example {n : ℕ} (C : StoredChain n 1 1)
    (zero : ∀ x, contract (denoteChain C) x 0 0 = 0) : (norm C).value = 0 := by
  rw [norm_eq_sum]
  simp [zero]

example : (norm (StoredChain.nil 1)).value = 1 := by
  rw [norm_value]
  simp [TensorTrainNormEnvironment.norm, TensorTrainNormEnvironment.gram, denoteChain]

example (r : ℕ) : StoredRectangularGivens.total (gram (StoredChain.nil r)).cost =
    5 * r ^ 2 + 4 * r + 6 := by
  simp [gram, cacheNode, StoredRectangularGivens.total,
    StoredRectangularGivens.identity_cost, StoredRectangularGivens.identityBudget,
    nodeBudget, tick]
  ring

example : StoredRectangularGivens.total (norm (StoredChain.nil 1)).cost = 18 := by
  simp [StoredRectangularGivens.total, norm_cost, gram, cacheNode,
    StoredRectangularGivens.identity_cost, StoredRectangularGivens.identityBudget,
    nodeBudget, tick]

example {l : ℕ} (A : StoredCore l 0) (E : StoredMatrix 0 0) (bit : Fin 2)
    (a c : Fin l) : (secondEntry (firstPass A E bit).value A bit a c).value = 0 := rfl

example {m : ℕ} (bit : Fin 2) (j : Fin m) :
    (finProdFinEquiv (bit, j)).val = bit.val * m + j.val := by
  simp [finProdFinEquiv, Nat.mul_comm, Nat.add_comm]

-- No costed cell is evaluated for zero output columns, but outer rows cost words.
example {l : ℕ} (A : StoredCore l 0) (E : StoredMatrix 0 0) (bit : Fin 2) :
    StoredRectangularGivens.total (firstPass A E bit).cost = 4 * l := by
  simp [firstPass, materialize_cost, StoredRectangularGivens.total, tick]
  ring

example (l m r : ℕ) : StoredRectangularGivens.total (productBudget l m r) =
    6 * l * m * r + 4 * (l * r + l) := by
  simp [StoredRectangularGivens.total, productBudget, tick]
  ring

example (l : ℕ) : StoredRectangularGivens.total (additionBudget l) =
    9 * l ^ 2 + 4 * l := by
  simp [StoredRectangularGivens.total, additionBudget, tick]
  ring

example {n : ℕ} (C : StoredChain n 1 1) (D : ℕ)
    (bound : maxBond (denoteChain C) ≤ D) : 1 ≤ D := by
  cases C with
  | nil => exact bound
  | cons A C => exact (max_le_iff.mp bound).1

end QuantumBlockEncoding.StoredTensorTrainNorm
