namespace DecoderC17
open QuantumBlockEncoding
open StoredGivens StoredTensorTrain TensorTrainCanonical StoredMatrixProductChain
open scoped BigOperators

-- Exact symbolic storage counters; every constructor of Op is discriminated.
example {D : ℕ} (A : StoredCore D D) (v : Vector ℝ D) :
    (terminal A v).cost .field = 4 * D^2 ∧
    (terminal A v).cost .read = 6 * D^2 + 6 * D ∧
    (terminal A v).cost .write = 6 * D ∧
    (terminal A v).cost .sqrt = 0 ∧ (terminal A v).cost .angle = 0 ∧
    (terminal A v).cost .trig = 0 ∧ (terminal A v).cost .compare = 0 ∧
    (terminal A v).cost .emit = 0 := by
  simp [terminal_cost, tick]
  constructor <;> ring

example {D r : ℕ} (v : Vector ℝ D) (A : StoredCore D r) :
    (initial v A).cost .field = 4*r*D ∧
    (initial v A).cost .read = 6*r*D + 4*r+2 ∧
    (initial v A).cost .write = 4*r+2 ∧
    (initial v A).cost .sqrt = 0 ∧ (initial v A).cost .angle = 0 ∧
    (initial v A).cost .trig = 0 ∧ (initial v A).cost .compare = 0 ∧
    (initial v A).cost .emit = 0 := by
  simp [initial_cost, tick]
  constructor <;> ring

example {α : Type} {n : ℕ} (xs : Vector α (n+1)) :
    (tailTable xs).cost .read = 3*n ∧ (tailTable xs).cost .write = 2*n ∧
    (tailTable xs).cost .field = 0 := by
  simp [tailTable_cost, tick]; omega

example (f : Fin 0 → Fin 3 → Run ℝ) (op : Op) :
    (materialize f).cost op = 0 := by simp [materialize_cost]
example (f : Fin 1 → Fin 0 → Run ℝ) (op : Op) :
    (materialize f).cost op = 2*tick .read op + 2*tick .write op := by
  simp [materialize_cost]

example {D : ℕ} (tables : Vector (StoredCore D D) 1) (l r : Vector ℝ D) :
    StoredRectangularGivens.total (ofTable tables l r).cost = 10*D^2+22*D+31 := by
  simp [ofTable, tailChain, closeLeft, bind, Run.bind,
    StoredGivens.read, charge, initial_cost, terminal_cost,
    StoredRectangularGivens.total, nodeBudget, tick]
  ring

example {D : ℕ} (tables : Vector (StoredCore D D) 3) (l r : Vector ℝ D) :
    StoredRectangularGivens.total (ofTable tables l r).cost = 20*D^2+20*D+52 := by
  simp [ofTable, tailChain, closeLeft, bind, Run.bind,
    StoredGivens.read, charge, tailTable_cost, initial_cost, terminal_cost,
    StoredRectangularGivens.total, nodeBudget, tick]
  ring

def A : StoredCore 2 2 := #v[#v[(1:ℝ),2,10,20], #v[3,4,30,40]]
def B : StoredCore 2 2 := #v[#v[(0:ℝ),1,5,6], #v[-1,2,7,8]]
def L : Vector ℝ 2 := #v[(2:ℝ),-1]
def R : Vector ℝ 2 := #v[(-1:ℝ),3]

-- Window outside the supplied range is not an assumption of any producer.
def K : MatrixProductChain.Kernel 2 := fun k bit a b =>
  if k = 7 then denoteCore A a (bit,b) else denoteCore B a (bit,b)
theorem window : Window #v[A,B] K 7 := by
  intro i
  fin_cases i <;> simp [K]

theorem chronological_signed :
    contract (denoteChain (ofTable #v[A,B] L R).value) (0,0,()) 0 0 = -3 := by
  erw [ofTable_refines #v[A,B] L R K 7 window, MatrixProductChain.ofKernel_contract]
  norm_num [MatrixProductChain.readout, _root_.Matrix.mulVec, dotProduct,
    Fin.sum_univ_two, K, A, B, L, R, denoteCore, denote, finProdFinEquiv]

theorem physical_first_bit :
    contract (denoteChain (ofTable #v[A,B] L R).value) (1,0,()) 0 0 = -30 := by
  erw [ofTable_refines #v[A,B] L R K 7 window, MatrixProductChain.ofKernel_contract]
  norm_num [MatrixProductChain.readout, _root_.Matrix.mulVec, dotProduct,
    Fin.sum_univ_two, K, A, B, L, R, denoteCore, denote, finProdFinEquiv]

theorem physical_second_bit :
    contract (denoteChain (ofTable #v[A,B] L R).value) (0,1,()) 0 0 = -13 := by
  erw [ofTable_refines #v[A,B] L R K 7 window, MatrixProductChain.ofKernel_contract]
  norm_num [MatrixProductChain.readout, _root_.Matrix.mulVec, dotProduct,
    Fin.sum_univ_two, K, A, B, L, R, denoteCore, denote, finProdFinEquiv]

theorem singleton :
    contract (denoteChain (ofTable #v[A] L R).value) (0,()) 0 0 = 1 := by
  have h : Window #v[A] K 7 := by intro i; fin_cases i; simp [K]
  erw [ofTable_refines #v[A] L R K 7 h, MatrixProductChain.ofKernel_contract]
  norm_num [MatrixProductChain.readout, _root_.Matrix.mulVec, dotProduct,
    Fin.sum_univ_two, K, A, B, L, R, denoteCore, denote, finProdFinEquiv]

theorem empty_bond :
    contract (denoteChain (ofTable (#v[#v[]] : Vector (StoredCore 0 0) 1)
      #v[] #v[]).value) (0,()) 0 0 = 0 := by
  simp [ofTable, tailChain, closeLeft, terminal, initial, initialEntry,
    sumEntries, materialize, collect, denoteChain, contract, slice,
    denoteCore, denote, bind, Run.bind, pure, Run.pure, StoredGivens.read, charge]

#print axioms chronological_signed
#print axioms physical_first_bit
#print axioms physical_second_bit
#print axioms singleton
#print axioms empty_bond
end DecoderC17
