namespace ReviewerC17
open QuantumBlockEncoding
open StoredGivens StoredTensorTrain TensorTrainCanonical StoredMatrixProductChain
open scoped BigOperators

def A : StoredCore 2 2 := #v[#v[(2:ℝ),-1,-2,4], #v[3,0,1,-3]]
def B : StoredCore 2 2 := #v[#v[(1:ℝ),5,0,-4], #v[-2,1,6,2]]
def L : Vector ℝ 2 := #v[(-1:ℝ),2]
def R : Vector ℝ 2 := #v[(3:ℝ),-2]
def K : MatrixProductChain.Kernel 2 := fun k bit a b =>
  if k = 11 then denoteCore A a (bit,b)
  else if k = 12 then denoteCore B a (bit,b) else 999
theorem finite_window : Window #v[A,B] K 11 := by
  intro i
  fin_cases i <;> simp [K]

theorem signed_chronological :
    contract (denoteChain (ofTable #v[A,B] L R).value) (0,0,()) 0 0 = -36 := by
  erw [ofTable_refines #v[A,B] L R K 11 finite_window, MatrixProductChain.ofKernel_contract]
  norm_num [MatrixProductChain.readout, _root_.Matrix.mulVec, dotProduct,
    Fin.sum_univ_two, K, A, B, L, R, denoteCore, denote, finProdFinEquiv]

theorem first_bit_column :
    contract (denoteChain (ofTable #v[A,B] L R).value) (1,0,()) 0 0 = 52 := by
  erw [ofTable_refines #v[A,B] L R K 11 finite_window, MatrixProductChain.ofKernel_contract]
  norm_num [MatrixProductChain.readout, _root_.Matrix.mulVec, dotProduct,
    Fin.sum_univ_two, K, A, B, L, R, denoteCore, denote, finProdFinEquiv]

theorem second_bit_column :
    contract (denoteChain (ofTable #v[A,B] L R).value) (0,1,()) 0 0 = 46 := by
  erw [ofTable_refines #v[A,B] L R K 11 finite_window, MatrixProductChain.ofKernel_contract]
  norm_num [MatrixProductChain.readout, _root_.Matrix.mulVec, dotProduct,
    Fin.sum_univ_two, K, A, B, L, R, denoteCore, denote, finProdFinEquiv]

theorem both_bits :
    contract (denoteChain (ofTable #v[A,B] L R).value) (1,1,()) 0 0 = -108 := by
  erw [ofTable_refines #v[A,B] L R K 11 finite_window, MatrixProductChain.ofKernel_contract]
  norm_num [MatrixProductChain.readout, _root_.Matrix.mulVec, dotProduct,
    Fin.sum_univ_two, K, A, B, L, R, denoteCore, denote, finProdFinEquiv]

def KReverse : MatrixProductChain.Kernel 2 := fun k bit a b =>
  if k = 11 then denoteCore B a (bit,b) else denoteCore A a (bit,b)
theorem reversed_product_discriminator :
    contract (MatrixProductChain.ofKernel KReverse (fun i => L[i.val])
      (fun i => R[i.val]) 11 1) (0,0,()) 0 0 = -67 := by
  rw [MatrixProductChain.ofKernel_contract]
  norm_num [MatrixProductChain.readout, _root_.Matrix.mulVec, dotProduct,
    Fin.sum_univ_two, KReverse, A, B, L, R, denoteCore, denote, finProdFinEquiv]

theorem singleton_both_boundaries :
    contract (denoteChain (ofTable #v[A] L R).value) (0,()) 0 0 = 10 := by
  have h : Window #v[A] K 11 := by intro i; fin_cases i; simp [K]
  erw [ofTable_refines #v[A] L R K 11 h, MatrixProductChain.ofKernel_contract]
  norm_num [MatrixProductChain.readout, _root_.Matrix.mulVec, dotProduct,
    Fin.sum_univ_two, K, A, B, L, R, denoteCore, denote, finProdFinEquiv]

theorem swapped_boundary_discriminator :
    contract (denoteChain (ofTable #v[A] R L).value) (0,()) 0 0 = -6 := by
  have h : Window #v[A] K 11 := by intro i; fin_cases i; simp [K]
  erw [ofTable_refines #v[A] R L K 11 h, MatrixProductChain.ofKernel_contract]
  norm_num [MatrixProductChain.readout, _root_.Matrix.mulVec, dotProduct,
    Fin.sum_univ_two, K, A, B, L, R, denoteCore, denote, finProdFinEquiv]

theorem empty_bond_scalar :
    contract (denoteChain (ofTable (#v[#v[]] : Vector (StoredCore 0 0) 1)
      #v[] #v[]).value) (1,()) 0 0 = 0 := by
  simp [ofTable, tailChain, closeLeft, terminal, initial, initialEntry,
    sumEntries, materialize, collect, denoteChain, contract, slice,
    denoteCore, denote, bind, Run.bind, pure, Run.pure, StoredGivens.read, charge]

theorem empty_bond_nonzero_materialization :
    StoredRectangularGivens.total (ofTable (#v[#v[]] : Vector (StoredCore 0 0) 1)
      #v[] #v[]).cost = 31 := by
  simp [ofTable, tailChain, closeLeft, bind, Run.bind, StoredGivens.read, charge,
    initial_cost, terminal_cost, StoredRectangularGivens.total, nodeBudget, tick]

theorem singleton_exact_cost {D : ℕ} (tables : Vector (StoredCore D D) 1)
    (l r : Vector ℝ D) :
    StoredRectangularGivens.total (ofTable tables l r).cost = 10*D^2+22*D+31 := by
  simp [ofTable, tailChain, closeLeft, bind, Run.bind, StoredGivens.read, charge,
    initial_cost, terminal_cost, StoredRectangularGivens.total, nodeBudget, tick]
  ring

theorem two_site_exact_cost {D : ℕ} (tables : Vector (StoredCore D D) 2)
    (l r : Vector ℝ D) :
    StoredRectangularGivens.total (ofTable tables l r).cost = 20*D^2+20*D+35 := by
  simp [ofTable, tailChain, closeLeft, bind, Run.bind, StoredGivens.read, charge,
    tailTable_cost, initial_cost, terminal_cost, StoredRectangularGivens.total, nodeBudget, tick]
  ring

theorem four_site_exact_cost {D : ℕ} (tables : Vector (StoredCore D D) 4)
    (l r : Vector ℝ D) :
    StoredRectangularGivens.total (ofTable tables l r).cost = 20*D^2+20*D+74 := by
  simp [ofTable, tailChain, closeLeft, bind, Run.bind, StoredGivens.read, charge,
    tailTable_cost, initial_cost, terminal_cost, StoredRectangularGivens.total, nodeBudget, tick]
  ring

theorem all_terminal_counters {D : ℕ} (A : StoredCore D D) (r : Vector ℝ D) :
    (terminal A r).cost .field = 4*D^2 ∧
    (terminal A r).cost .read = 6*D^2+6*D ∧
    (terminal A r).cost .write = 6*D ∧
    (terminal A r).cost .sqrt = 0 ∧ (terminal A r).cost .angle = 0 ∧
    (terminal A r).cost .trig = 0 ∧ (terminal A r).cost .compare = 0 ∧
    (terminal A r).cost .emit = 0 := by
  simp [terminal_cost, tick]
  constructor <;> ring

theorem all_initial_counters {D q : ℕ} (l : Vector ℝ D) (A : StoredCore D q) :
    (initial l A).cost .field = 4*q*D ∧
    (initial l A).cost .read = 6*q*D+4*q+2 ∧
    (initial l A).cost .write = 4*q+2 ∧
    (initial l A).cost .sqrt = 0 ∧ (initial l A).cost .angle = 0 ∧
    (initial l A).cost .trig = 0 ∧ (initial l A).cost .compare = 0 ∧
    (initial l A).cost .emit = 0 := by
  simp [initial_cost, tick]
  constructor <;> ring

theorem actual_singleton_bond :
    maxBond (denoteChain (ofTable #v[A] L R).value) = 1 := by
  simp [ofTable, tailChain, closeLeft, bind, Run.bind, maxBond, denoteChain]

theorem actual_two_site_bond :
    maxBond (denoteChain (ofTable #v[A,B] L R).value) = 2 := by
  simp [ofTable, tailChain, closeLeft, bind, Run.bind, maxBond, denoteChain]

theorem tail_reference_identity {α : Type} {n : ℕ} (xs : Vector α (n+1)) (i : Fin n) :
    (tailTable xs).value[i.val] = xs[i.succ.val] := tailTable_value xs i

theorem source_coefficient_bridge {n D : ℕ}
    (tables : Vector (StoredCore D D) (n+1)) (l r : Vector ℝ D)
    (K : MatrixProductChain.Kernel D) (s : ℕ) (h : Window tables K s)
    (x : Word (n+1)) :
    contract (denoteChain (ofTable tables l r).value) x 0 0 =
      ∑ a, l[a.val] * MatrixProductChain.readout K (fun i => r[i.val]) s x a := by
  rw [ofTable_refines tables l r K s h, MatrixProductChain.ofKernel_contract]

#print axioms signed_chronological
#print axioms first_bit_column
#print axioms second_bit_column
#print axioms both_bits
#print axioms reversed_product_discriminator
#print axioms singleton_both_boundaries
#print axioms swapped_boundary_discriminator
#print axioms empty_bond_scalar
#print axioms empty_bond_nonzero_materialization
#print axioms singleton_exact_cost
#print axioms two_site_exact_cost
#print axioms four_site_exact_cost
#print axioms all_terminal_counters
#print axioms all_initial_counters
#print axioms actual_singleton_bond
#print axioms actual_two_site_bond
#print axioms tail_reference_identity
#print axioms source_coefficient_bridge
end ReviewerC17
