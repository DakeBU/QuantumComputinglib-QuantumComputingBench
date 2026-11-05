import QuantumBlockEncoding.StoredTensorTrain
import QuantumBlockEncoding.MatrixProductChain

/-! Stored boundary-chain assembly. Stored inputs only; no kernel callbacks are
evaluated by production. Exact-real operations and stored-word traffic are
counted; finite-bit and loop-index arithmetic are outside this model. -/
namespace QuantumBlockEncoding.StoredMatrixProductChain
open scoped BigOperators
open StoredGivens StoredTensorTrain TensorTrainCanonical

noncomputable def terminalEntry {D : ℕ} (A : StoredCore D D)
    (right : Vector ℝ D) (a : Fin D) (bit : Fin 2) : Run ℝ :=
  sumEntries fun b => do
    let x ← StoredThinLQ.entry A a (finProdFinEquiv (bit, b))
    let y ← read right b
    StoredGivens.mul x y

noncomputable def terminal {D : ℕ} (A : StoredCore D D)
    (right : Vector ℝ D) : Run (StoredCore D 1) :=
  materialize fun a j => terminalEntry A right a (finProdFinEquiv.symm j).1

noncomputable def initialEntry {D r : ℕ} (left : Vector ℝ D)
    (A : StoredCore D r) (j : Fin (2 * r)) : Run ℝ :=
  sumEntries fun a => do
    let x ← read left a
    let y ← StoredThinLQ.entry A a j
    StoredGivens.mul x y

noncomputable def initial {D r : ℕ} (left : Vector ℝ D)
    (A : StoredCore D r) : Run (StoredCore 1 r) :=
  materialize fun _ j => initialEntry left A j

/-- Copy only references to already materialized local cores. -/
def tailTable {α : Type} {n : ℕ} (xs : Vector α (n + 1)) : Run (Vector α n) :=
  collect fun i => read xs i.succ

noncomputable def tailChain {D : ℕ} : {n : ℕ} →
    Vector (StoredCore D D) (n + 1) → Vector ℝ D → Run (StoredChain (n + 1) D 1)
  | 0, tables, right => do
      let A ← read tables 0
      let B ← terminal A right
      (⟨.cons B (.nil 1), 2 • nodeBudget⟩ : Run _)
  | _n + 1, tables, right => do
      let A ← read tables 0
      let ts ← tailTable tables
      let C ← tailChain ts right
      (⟨.cons A C, nodeBudget⟩ : Run _)

noncomputable def closeLeft {n D : ℕ} (left : Vector ℝ D) :
    StoredChain (n + 1) D 1 → Run (StoredChain (n + 1) 1 1)
  | .cons A C => do
      let B ← initial left A
      (⟨.cons B C, nodeBudget⟩ : Run _)

noncomputable def ofTable {n D : ℕ} (tables : Vector (StoredCore D D) (n + 1))
    (left right : Vector ℝ D) : Run (StoredChain (n + 1) 1 1) := do
  let C ← tailChain tables right
  closeLeft left C

theorem terminal_value {D : ℕ} (A : StoredCore D D) (right : Vector ℝ D) :
    denoteCore (terminal A right).value =
      fun a out => ∑ b, denoteCore A a (out.1, b) * right[b.val] := by
  ext a out
  simp only [terminal, denoteCore, materialize, denote, collect_value,
    Equiv.symm_apply_apply, terminalEntry, sumEntries_value]
  rfl

theorem initial_value {D r : ℕ} (left : Vector ℝ D) (A : StoredCore D r) :
    denoteCore (initial left A).value = fun _ out => ∑ a, left[a.val] * denoteCore A a out := by
  ext a out
  simp only [initial, denoteCore, materialize, denote, collect_value,
    initialEntry, sumEntries_value]
  rfl

@[simp] theorem tailTable_value {α : Type} {n : ℕ} (xs : Vector α (n + 1)) (i : Fin n) :
    (tailTable xs).value[i.val] = xs[i.succ.val] := by
  simp [tailTable, StoredGivens.read, charge]

/-- Kernel appears only in this finite-window specification, never production. -/
def Window {n D : ℕ} (tables : Vector (StoredCore D D) (n + 1))
    (K : MatrixProductChain.Kernel D) (start : ℕ) : Prop :=
  ∀ i : Fin (n + 1), denoteCore tables[i.val] = fun a out => K (start + i.val) out.1 a out.2

theorem tailChain_value {n D : ℕ} (tables : Vector (StoredCore D D) (n + 1))
    (right : Vector ℝ D) (K : MatrixProductChain.Kernel D) (start : ℕ)
    (h : Window tables K start) :
    denoteChain (tailChain tables right).value =
      MatrixProductChain.tailChain K (fun i => right[i.val]) start n := by
  induction n generalizing start with
  | zero =>
      simp only [tailChain, bind, Run.bind, StoredGivens.read, charge, denoteChain,
        terminal_value, MatrixProductChain.tailChain]
      have h0 := h 0
      simp only [Fin.val_zero, Nat.add_zero] at h0
      simp only [Fin.val_zero]
      rw [h0]
      rfl
  | succ n ih =>
      simp only [tailChain, bind, Run.bind, StoredGivens.read, charge, denoteChain,
        MatrixProductChain.tailChain]
      have h0 := h 0
      simp only [Fin.val_zero, Nat.add_zero] at h0
      simp only [Fin.val_zero]
      rw [h0, ih (tailTable tables).value (start + 1)]
      intro i
      rw [tailTable_value, h i.succ]
      simp [Fin.val_succ, Nat.add_comm, Nat.add_left_comm] <;> rfl

theorem closeLeft_value {n D : ℕ} (left : Vector ℝ D) (C : StoredChain (n + 1) D 1) :
    denoteChain (closeLeft left C).value =
      MatrixProductChain.closeLeft (fun i => left[i.val]) (denoteChain C) := by
  cases C with
  | cons A C =>
      simp only [closeLeft, bind, Run.bind, denoteChain, initial_value,
        MatrixProductChain.closeLeft]

theorem ofTable_refines {n D : ℕ} (tables : Vector (StoredCore D D) (n + 1))
    (left right : Vector ℝ D) (K : MatrixProductChain.Kernel D) (start : ℕ)
    (h : Window tables K start) :
    denoteChain (ofTable tables left right).value =
      MatrixProductChain.ofKernel K (fun i => left[i.val]) (fun i => right[i.val]) start n := by
  simp only [ofTable, bind, Run.bind, closeLeft_value, tailChain_value tables right K start h,
    MatrixProductChain.ofKernel]

private theorem sumEntries_cost_eq {k : ℕ} (f : Fin k → Run ℝ) (op : Op) (B : ℕ)
    (h : ∀ i, (f i).cost op = B) :
    (sumEntries f).cost op = k * (B + tick .field op) := by
  induction k with
  | zero => simp [sumEntries, pure, Run.pure]
  | succ k ih =>
      simp only [sumEntries, bind, Run.bind, StoredGivens.add, charge, Pi.add_apply]
      rw [h 0, ih (fun i => f i.succ) (fun i => h i.succ)]
      ring

theorem terminalEntry_cost {D : ℕ} (A : StoredCore D D) (right : Vector ℝ D)
    (a : Fin D) (bit : Fin 2) (op : Op) :
    (terminalEntry A right a bit).cost op = D * (3 * tick .read op + 2 * tick .field op) := by
  unfold terminalEntry
  rw [sumEntries_cost_eq _ op (3 * tick .read op + tick .field op)]
  · ring
  · intro b
    simp [bind, Run.bind, StoredGivens.read, StoredGivens.mul, charge]
    ring

theorem initialEntry_cost {D r : ℕ} (left : Vector ℝ D) (A : StoredCore D r)
    (j : Fin (2 * r)) (op : Op) :
    (initialEntry left A j).cost op = D * (3 * tick .read op + 2 * tick .field op) := by
  unfold initialEntry
  rw [sumEntries_cost_eq _ op (3 * tick .read op + tick .field op)]
  · ring
  · intro a
    simp [bind, Run.bind, StoredGivens.read, StoredGivens.mul, charge]
    ring

theorem terminal_cost {D : ℕ} (A : StoredCore D D) (right : Vector ℝ D) (op : Op) :
    (terminal A right).cost op =
      2 * D ^ 2 * (3 * tick .read op + 2 * tick .field op) +
      6 * D * (tick .read op + tick .write op) := by
  simp [terminal, materialize_cost, terminalEntry_cost]
  ring

theorem initial_cost {D r : ℕ} (left : Vector ℝ D) (A : StoredCore D r) (op : Op) :
    (initial left A).cost op =
      2 * r * D * (3 * tick .read op + 2 * tick .field op) +
      (4 * r + 2) * (tick .read op + tick .write op) := by
  simp [initial, materialize_cost, initialEntry_cost]
  ring

theorem tailTable_cost {α : Type} {n : ℕ} (xs : Vector α (n + 1)) (op : Op) :
    (tailTable xs).cost op = n * (3 * tick .read op + 2 * tick .write op) := by
  simp [tailTable, collect_cost, StoredGivens.read, charge]
  ring

private theorem total_add (a b : Cost) :
    StoredRectangularGivens.total (a + b) =
      StoredRectangularGivens.total a + StoredRectangularGivens.total b := by
  simp only [StoredRectangularGivens.total, Pi.add_apply]
  ring

theorem terminal_total_cost {D : ℕ} (A : StoredCore D D) (right : Vector ℝ D) :
    StoredRectangularGivens.total (terminal A right).cost = 10 * D ^ 2 + 12 * D := by
  simp [StoredRectangularGivens.total, terminal_cost, tick]
  ring

theorem initial_total_cost {D r : ℕ} (left : Vector ℝ D) (A : StoredCore D r) :
    StoredRectangularGivens.total (initial left A).cost = 10 * r * D + 8 * r + 4 := by
  simp [StoredRectangularGivens.total, initial_cost, tick]
  ring

theorem tailTable_total_cost {α : Type} {n : ℕ} (xs : Vector α (n + 1)) :
    StoredRectangularGivens.total (tailTable xs).cost = 5 * n := by
  simp [StoredRectangularGivens.total, tailTable_cost, tick]
  ring

private theorem node_total : StoredRectangularGivens.total nodeBudget = 6 := by
  simp [StoredRectangularGivens.total, nodeBudget, tick]

private theorem read_total {α : Type} {n : ℕ} (xs : Vector α n) (i : Fin n) :
    StoredRectangularGivens.total (StoredGivens.read xs i).cost = 1 := by
  simp [StoredRectangularGivens.total, StoredGivens.read, charge, tick]

theorem tailChain_total_cost_le {n D : ℕ} (tables : Vector (StoredCore D D) (n + 1))
    (right : Vector ℝ D) :
    StoredRectangularGivens.total (tailChain tables right).cost ≤
      10 * D ^ 2 + 12 * D + 5 * n ^ 2 + 7 * n + 13 := by
  induction n with
  | zero =>
      simp only [tailChain, bind, Run.bind, total_add, read_total, terminal_total_cost]
      simp [StoredRectangularGivens.total, nodeBudget, tick]
      omega
  | succ n ih =>
      simp only [tailChain, bind, Run.bind, total_add, read_total, tailTable_total_cost, node_total]
      have h := ih (tailTable tables).value
      nlinarith

theorem closeLeft_tail_total_cost_le {n D : ℕ} (tables : Vector (StoredCore D D) (n + 1))
    (left right : Vector ℝ D) :
    StoredRectangularGivens.total (closeLeft left (tailChain tables right).value).cost ≤
      10 * D ^ 2 + 18 * D + 18 := by
  cases n with
  | zero =>
      simp only [tailChain, bind, Run.bind, closeLeft, total_add, initial_total_cost, node_total]
      nlinarith
  | succ n =>
      simp only [tailChain, bind, Run.bind, closeLeft, total_add, initial_total_cost, node_total]
      nlinarith

/-- Bound for the very same run whose value refines `ofKernel`; includes
terminal/initial arithmetic, materialization, copied references, and nodes. -/
theorem ofTable_total_cost_le {n D : ℕ} (tables : Vector (StoredCore D D) (n + 1))
    (left right : Vector ℝ D) :
    StoredRectangularGivens.total (ofTable tables left right).cost ≤
      20 * D ^ 2 + 30 * D + 5 * n ^ 2 + 7 * n + 31 := by
  have h := tailChain_total_cost_le tables right
  have g := closeLeft_tail_total_cost_le tables left right
  simp only [ofTable, bind, Run.bind, total_add]
  omega

/-- Entrywise supplier adapter; only the stored finite window is constrained. -/
theorem window_of_entries {n D : ℕ} (tables : Vector (StoredCore D D) (n + 1))
    (K : MatrixProductChain.Kernel D) (start : ℕ)
    (h : ∀ (i : Fin (n + 1)) (a b : Fin D) (bit : Fin 2),
      denoteCore tables[i.val] a (bit, b) = K (start + i.val) bit a b) :
    Window tables K start := by
  intro i
  ext a out
  exact h i a out.2 out.1

theorem ofTable_maxBond {n D : ℕ} (tables : Vector (StoredCore D D) (n + 1))
    (left right : Vector ℝ D) (K : MatrixProductChain.Kernel D) (start : ℕ)
    (h : Window tables K start) :
    maxBond (denoteChain (ofTable tables left right).value) ≤ max D 1 := by
  rw [ofTable_refines tables left right K start h]
  exact MatrixProductChain.ofKernel_maxBond K _ _ start n

/-- One producer, with both exact returned data and polynomial charged work. -/
theorem ofTable_certified {n D : ℕ} (tables : Vector (StoredCore D D) (n + 1))
    (left right : Vector ℝ D) (K : MatrixProductChain.Kernel D) (start : ℕ)
    (h : Window tables K start) :
    let result := ofTable tables left right
    denoteChain result.value =
      MatrixProductChain.ofKernel K (fun i => left[i.val]) (fun i => right[i.val]) start n ∧
    StoredRectangularGivens.total result.cost ≤
      20 * D ^ 2 + 30 * D + 5 * n ^ 2 + 7 * n + 31 :=
  ⟨ofTable_refines tables left right K start h, ofTable_total_cost_le tables left right⟩

end QuantumBlockEncoding.StoredMatrixProductChain
