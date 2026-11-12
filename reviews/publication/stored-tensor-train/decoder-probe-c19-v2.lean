namespace StoredTTDecoderC19
open QuantumBlockEncoding
open StoredGivens StoredTensorTrain TensorTrainCanonical
open scoped BigOperators

def table {l r : ℕ} (f : Fin l → Fin r → ℝ) : StoredMatrix l r :=
  Vector.ofFn (fun i => Vector.ofFn (f i))

example : (finProdFinEquiv ((1 : Fin 2), (0 : Fin 3))).val = 3 := by decide
example : (finProdFinEquiv ((0 : Fin 2), (2 : Fin 3))).val = 2 := by decide
example : (finProdFinEquiv ((1 : Fin 2), (2 : Fin 3))).val = 5 := by decide

def asymmetric : StoredCore 1 2 := table fun _ j =>
  if j.val = 0 then 1 else if j.val = 1 then 2 else if j.val = 2 then 4 else 8
def signedResidual : StoredMatrix 2 1 := table fun i _ => if i.val = 0 then 3 else -1

example : (absorptionEntry asymmetric signedResidual 0 (0, 0)).value = 1 := by
  rw [absorptionEntry_value]
  norm_num [absorb, denoteCore, denote, table, asymmetric, signedResidual,
    Fin.sum_univ_succ, finProdFinEquiv]
example : (absorptionEntry asymmetric signedResidual 0 (1, 0)).value = 4 := by
  rw [absorptionEntry_value]
  norm_num [absorb, denoteCore, denote, table, asymmetric, signedResidual,
    Fin.sum_univ_succ, finProdFinEquiv]

def deficient : StoredChain 1 2 3 := .cons (table fun _ _ => 0) (.nil 3)
example : (canonicalize deficient).value.rank = 2 := rfl
example : RightCanonical (denoteChain (canonicalize deficient).value.canonical) :=
  (canonicalize deficient).value.rightCanonical
example : (canonicalize deficient).value.toSemantic =
    ConstructiveTensorTrain.canonicalize (denoteChain deficient) := canonicalize_refines deficient
def tallZero : StoredChain 1 5 1 := .cons (table fun _ _ => 0) (.nil 1)
example : (canonicalize tallZero).value.rank = 2 := rfl

def emptyInternal : StoredChain 1 1 0 := .cons (table fun _ _ => 0) (.nil 0)
example : (canonicalize emptyInternal).value.rank = 0 := rfl
example : chainMass (denoteChain emptyInternal) (fun _ => 7) = 0 := by
  simp [emptyInternal, denoteChain, chainMass, mass]
example : mass (boundary emptyInternal (fun _ => 7)) = 0 := by
  rw [← boundary_mass]
  simp [emptyInternal, denoteChain, chainMass, mass]
example : (canonicalize (.nil 0)).value.rank = 0 := rfl
example : mass (boundary (.nil 0) (fun _ => 9)) = 0 := by
  rw [← boundary_mass]
  simp [denoteChain, chainMass, mass]

-- Empty length does not remove or project the two-dimensional terminal carrier.
def terminalBoundary : Fin 2 → ℝ := fun j => if j.val = 0 then 0 else 1
example : Matrix.vecMul terminalBoundary (contract (denoteChain (.nil 2)) ()) 0 = 0 := by
  simp [denoteChain, contract, terminalBoundary]
example : Matrix.vecMul terminalBoundary (contract (denoteChain (.nil 2)) ()) 1 = 1 := by
  simp [denoteChain, contract, terminalBoundary]
example : chainMass (denoteChain (.nil 2)) terminalBoundary = 1 := by
  norm_num [denoteChain, chainMass, contract, mass, terminalBoundary, Fin.sum_univ_succ, Word, wordFintype]
example : mass (boundary (.nil 2) terminalBoundary) = 1 := by
  apply boundary_normalized
  norm_num [denoteChain, chainMass, contract, mass, terminalBoundary, Fin.sum_univ_succ, Word, wordFintype]

-- Universally quantified action, not just one word or one terminal component.
example {n l r : ℕ} (C : StoredChain n l r) (x : Word n) (i : Fin l) (j : Fin r) :
    contract (denoteChain C) x i j =
      (denote (canonicalize C).value.residual *
        contract (denoteChain (canonicalize C).value.canonical) x) i j :=
  congrFun (congrFun ((canonicalize C).value.action x) i) j
example {n l r : ℕ} (C : StoredChain n l r) (v : Fin l → ℝ)
    (h : chainMass (denoteChain C) v = 1) : mass (boundary C v) = 1 :=
  boundary_normalized C v h
example {n l r : ℕ} (C : StoredChain n l r) (D : ℕ)
    (h : maxBond (denoteChain C) ≤ D) :
    StoredRectangularGivens.total (canonicalize C).cost ≤
      n * (176 * D ^ 3 + 116 * D ^ 2 + 29 * D + 8) + 5 * D ^ 2 + 4 * D + 6 :=
  canonicalize_total_cost_le C D h
example {l r : ℕ} (A : StoredCore l r) :
    denote (factorCore A).value.R = (ConstructiveTensorTrain.factorCore (denoteCore A)).R :=
  factorCore_R A
example {l r : ℕ} (A : StoredCore l r) :
    denoteCore (factorCore A).value.Q = (ConstructiveTensorTrain.factorCore (denoteCore A)).Q :=
  factorCore_Q A
example {n l r : ℕ} (C : StoredChain n l r) :
    (canonicalize C).value.toSemantic = ConstructiveTensorTrain.canonicalize (denoteChain C) :=
  canonicalize_refines C

example (cost : Cost) : StoredRectangularGivens.total cost =
    cost .field + cost .sqrt + cost .angle + cost .trig + cost .compare +
    cost .read + cost .write + cost .emit := rfl

end StoredTTDecoderC19
