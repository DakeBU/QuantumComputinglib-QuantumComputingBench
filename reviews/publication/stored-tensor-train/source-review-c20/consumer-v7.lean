namespace SourceReviewC20V7
open QuantumBlockEncoding
open StoredTensorTrain StoredGivens TensorTrainCanonical
open scoped BigOperators
example {n l r : ℕ} (C : StoredChain n l r) (x : Word n) (a : Fin l) (j : Fin r) :
    contract (denoteChain C) x a j =
      (denote (canonicalize C).value.residual *
        contract (denoteChain (canonicalize C).value.canonical) x) a j :=
  congrFun (congrFun ((canonicalize C).value.action x) a) j
example {n l r : ℕ} (C : StoredChain n l r) : (canonicalize C).value.toSemantic =
    ConstructiveTensorTrain.canonicalize (denoteChain C) := canonicalize_refines C
example {n l m r : ℕ} (A : StoredCore l m) (C : StoredChain n m r) :
    (canonicalize (.cons A C)).value.rank = min l (2 * (canonicalize C).value.rank) := rfl
example (A : StoredCore 7 2) : (factorCore A).value.Q.size = 4 := by rfl
example (A : StoredCore 7 0) : (factorCore A).value.Q.size = 0 := by rfl
example : finProdFinEquiv ((1 : Fin 2), (1 : Fin 4)) = (5 : Fin 8) := rfl
example : finProdFinEquiv ((0 : Fin 2), (3 : Fin 4)) = (3 : Fin 8) := rfl
example (v : Fin 3 → ℝ) : boundary (.nil 3) v = v := by
  simp [boundary, canonicalize, StoredRectangularGivens.identity_value]
example : chainMass (denoteChain (StoredChain.nil 3))
    (fun j => if j = (2 : Fin 3) then 2 else 0) = 4 := by
  norm_num [denoteChain, chainMass, contract, mass, Fin.sum_univ_succ]
  change Fintype.card Unit = 1
  simp
example : chainMass (denoteChain (StoredChain.nil 0)) (fun _ => 0) = 0 := by
  simp [denoteChain, chainMass, contract, mass, Word]
example {n l r : ℕ} (C : StoredChain n l r) (v : Fin l → ℝ) :
    chainMass (denoteChain C) v = mass (boundary C v) := boundary_mass C v
example {n l r : ℕ} (C : StoredChain n l r) (v : Fin l → ℝ)
    (h : chainMass (denoteChain C) v = 1) : mass (boundary C v) = 1 := boundary_normalized C v h
example {n l r : ℕ} (C : StoredChain n l r) (D : ℕ) (h : maxBond (denoteChain C) ≤ D) :
    StoredRectangularGivens.total (canonicalize C).cost ≤
      n * (176 * D^3 + 116 * D^2 + 29 * D + 8) + 5 * D^2 + 4 * D + 6 := canonicalize_total_cost_le C D h
example : StoredRectangularGivens.total (canonicalize (StoredChain.nil 0)).cost = 6 := by
  norm_num [canonicalize, nodeBudget, StoredRectangularGivens.identity_cost,
    StoredRectangularGivens.identityBudget, StoredRectangularGivens.total, tick]
  decide
example {l m r : ℕ} (A : StoredCore l m) (R : StoredMatrix m r) :
    denoteCore (absorption A R).value = absorb (denoteCore A) (denote R) := absorption_value A R
example {k : ℕ} (f : Fin k → Run ℝ) (op : Op) (B : ℕ) (h : ∀ i, (f i).cost op ≤ B) :
    (sumEntries f).cost op ≤ k * (B + tick .field op) := sumEntries_cost_le f op B h
end SourceReviewC20V7
