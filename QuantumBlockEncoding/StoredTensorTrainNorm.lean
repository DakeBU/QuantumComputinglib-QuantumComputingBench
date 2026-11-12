import QuantumBlockEncoding.StoredTensorTrain
import QuantumBlockEncoding.TensorTrainNormEnvironment

/-!
# Stored local Gram environments and tensor-train norms

The input cores are stored tables. Each recursive tail environment is computed
once. For each physical bit, two charged matrix contractions are materialized
before the next pass reads them. Only local bond matrices are evaluated; the
all-word sum occurs solely in the semantic correctness theorem.

Costs use `StoredGivens`' extended exact-real word-operation model, including
its full materialization passes. They are not finite-bit or whole-machine
runtime bounds. Input-core generation, proof checking and counter bookkeeping
are outside this supplier's interface.
-/

namespace QuantumBlockEncoding.StoredTensorTrainNorm

open scoped BigOperators
open StoredGivens StoredTensorTrain TensorTrainCanonical

private theorem bind_value (x : Run α) (f : α → Run β) :
    (x >>= f).value = (f x.value).value := rfl

/-- The first pass computes one entry of `A_bit * E`. -/
noncomputable def firstEntry {l m : ℕ} (A : StoredCore l m)
    (E : StoredMatrix m m) (bit : Fin 2) (a : Fin l) (j : Fin m) : Run ℝ :=
  sumEntries fun b => do
    let x ← StoredThinLQ.entry A a (finProdFinEquiv (bit, b))
    let y ← StoredThinLQ.entry E b j
    StoredGivens.mul x y

noncomputable def firstPass {l m : ℕ} (A : StoredCore l m)
    (E : StoredMatrix m m) (bit : Fin 2) : Run (StoredMatrix l m) :=
  materialize (firstEntry A E bit)

theorem firstPass_value {l m : ℕ} (A : StoredCore l m)
    (E : StoredMatrix m m) (bit : Fin 2) :
    denote (firstPass A E bit).value = slice (denoteCore A) bit * denote E := by
  ext a j
  simp only [firstPass, materialize, denote, collect_value, firstEntry, sumEntries_value]
  rfl

/-- The second pass reads the stored first pass and the original core.
The transpose is an index exchange, not an uncharged matrix constructor. -/
noncomputable def secondEntry {l m : ℕ} (F : StoredMatrix l m)
    (A : StoredCore l m) (bit : Fin 2) (a c : Fin l) : Run ℝ :=
  sumEntries fun j => do
    let x ← StoredThinLQ.entry F a j
    let y ← StoredThinLQ.entry A c (finProdFinEquiv (bit, j))
    StoredGivens.mul x y

noncomputable def secondPass {l m : ℕ} (F : StoredMatrix l m)
    (A : StoredCore l m) (bit : Fin 2) : Run (StoredMatrix l l) :=
  materialize (secondEntry F A bit)

theorem secondPass_value {l m : ℕ} (F : StoredMatrix l m)
    (A : StoredCore l m) (bit : Fin 2) :
    denote (secondPass F A bit).value = denote F * (slice (denoteCore A) bit).transpose := by
  ext a c
  simp only [secondPass, materialize, denote, collect_value, secondEntry, sumEntries_value]
  rfl

noncomputable def addMatrices {l : ℕ} (A B : StoredMatrix l l) :
    Run (StoredMatrix l l) :=
  materialize fun a c => do
    let x ← StoredThinLQ.entry A a c
    let y ← StoredThinLQ.entry B a c
    StoredGivens.add x y

theorem addMatrices_value {l : ℕ} (A B : StoredMatrix l l) :
    denote (addMatrices A B).value = denote A + denote B := by
  ext a c
  simp only [addMatrices, materialize, denote, collect_value]
  rfl

/-- All four contraction outputs and the sum are materialized.
The two uses of `E` are stored reads of the same cached environment. -/
noncomputable def update {l m : ℕ} (A : StoredCore l m)
    (E : StoredMatrix m m) : Run (StoredMatrix l l) := do
  let F₀ ← firstPass A E 0
  let G₀ ← secondPass F₀ A 0
  let F₁ ← firstPass A E 1
  let G₁ ← secondPass F₁ A 1
  addMatrices G₀ G₁

theorem update_value {l m : ℕ} (A : StoredCore l m) (E : StoredMatrix m m) :
    denote (update A E).value =
      ∑ bit : Fin 2, slice (denoteCore A) bit * denote E *
        (slice (denoteCore A) bit).transpose := by
  simp only [update, bind_value, addMatrices_value, secondPass_value, firstPass_value]
  simp [Fin.sum_univ_two]

/-- A fixed six-word traversal/cache-record allowance per chain node, as in
the stored canonicalizer. Matrix copying is charged separately by each pass. -/
def cacheNode (run : Run α) : Run α := ⟨run.value, nodeBudget + run.cost⟩

private theorem cacheNode_value (run : Run α) : (cacheNode run).value = run.value := rfl

/-- Streaming cached Gram environments. The recursive result is bound once
and remains a stored matrix throughout the two physical-bit updates. -/
noncomputable def gram : {n l r : ℕ} → StoredChain n l r → Run (StoredMatrix l l)
  | _, _, _, .nil r => cacheNode (StoredRectangularGivens.identity r)
  | _, _, _, .cons A C => cacheNode do
      let E ← gram C
      update A E

theorem gram_value {n l r : ℕ} (C : StoredChain n l r) :
    denote (gram C).value = TensorTrainNormEnvironment.gram (denoteChain C) := by
  induction C with
  | nil r => exact StoredRectangularGivens.identity_value r
  | cons A C ih =>
      rw [gram, cacheNode_value, bind_value, update_value, ih]
      rfl

/-- Scalar-boundary norm with the final table lookup and square root charged. -/
noncomputable def norm {n : ℕ} (C : StoredChain n 1 1) : Run ℝ := do
  let E ← gram C
  let mass ← StoredThinLQ.entry E 0 0
  StoredGivens.sqrt mass

theorem norm_value {n : ℕ} (C : StoredChain n 1 1) :
    (norm C).value = TensorTrainNormEnvironment.norm (denoteChain C) := by
  change Real.sqrt (denote (gram C).value 0 0) = _
  rw [gram_value]
  rfl

theorem norm_eq_sum {n : ℕ} (C : StoredChain n 1 1) :
    (norm C).value = Real.sqrt (∑ x : Word n, contract (denoteChain C) x 0 0 ^ 2) :=
  (norm_value C).trans (TensorTrainNormEnvironment.norm_eq (denoteChain C))

/-! ## Operation counts for the same producer -/

def productBudget (l m r : ℕ) : Cost := fun op =>
  l * r * m * (4 * tick .read op + 2 * tick .field op) +
    (l * r + l) * (2 * tick .read op + 2 * tick .write op)

def additionBudget (l : ℕ) : Cost := fun op =>
  l * l * (4 * tick .read op + tick .field op) +
    (l * l + l) * (2 * tick .read op + 2 * tick .write op)

def updateBudget (l m : ℕ) : Cost :=
  productBudget l m m + productBudget l m l +
    productBudget l m m + productBudget l m l + additionBudget l

private theorem materialize_cost_le {N M : ℕ} (f : Fin N → Fin M → Run ℝ)
    (op : Op) (B : ℕ) (bound : ∀ i j, (f i j).cost op ≤ B) :
    (materialize f).cost op ≤ N * M * B +
      (N * M + N) * (2 * tick .read op + 2 * tick .write op) := by
  rw [materialize_cost]
  have h : (∑ i : Fin N, ∑ j : Fin M, (f i j).cost op) ≤ N * M * B := by
    calc
      _ ≤ ∑ _i : Fin N, ∑ _j : Fin M, B := by
        apply Finset.sum_le_sum
        intro i _
        apply Finset.sum_le_sum
        intro j _
        exact bound i j
      _ = _ := by simp; ring
  omega

theorem firstEntry_cost_le {l m : ℕ} (A : StoredCore l m)
    (E : StoredMatrix m m) (bit : Fin 2) (a : Fin l) (j : Fin m) (op : Op) :
    (firstEntry A E bit a j).cost op ≤ m * (4 * tick .read op + 2 * tick .field op) := by
  have h := sumEntries_cost_le (fun b => do
    let x ← StoredThinLQ.entry A a (finProdFinEquiv (bit, b))
    let y ← StoredThinLQ.entry E b j
    StoredGivens.mul x y) op (4 * tick .read op + tick .field op) (by
      intro b
      simp [bind, Run.bind, StoredGivens.mul, charge]
      omega)
  simpa only [firstEntry, Nat.add_assoc, ← two_mul] using h

theorem secondEntry_cost_le {l m : ℕ} (F : StoredMatrix l m)
    (A : StoredCore l m) (bit : Fin 2) (a c : Fin l) (op : Op) :
    (secondEntry F A bit a c).cost op ≤ m * (4 * tick .read op + 2 * tick .field op) := by
  have h := sumEntries_cost_le (fun j => do
    let x ← StoredThinLQ.entry F a j
    let y ← StoredThinLQ.entry A c (finProdFinEquiv (bit, j))
    StoredGivens.mul x y) op (4 * tick .read op + tick .field op) (by
      intro j
      simp [bind, Run.bind, StoredGivens.mul, charge]
      omega)
  simpa only [secondEntry, Nat.add_assoc, ← two_mul] using h

theorem firstPass_cost_le {l m : ℕ} (A : StoredCore l m)
    (E : StoredMatrix m m) (bit : Fin 2) (op : Op) :
    (firstPass A E bit).cost op ≤ productBudget l m m op := by
  have h := materialize_cost_le (firstEntry A E bit) op
    (m * (4 * tick .read op + 2 * tick .field op))
    (fun a j => firstEntry_cost_le A E bit a j op)
  simpa only [firstPass, productBudget, Nat.mul_assoc] using h

theorem secondPass_cost_le {l m : ℕ} (F : StoredMatrix l m)
    (A : StoredCore l m) (bit : Fin 2) (op : Op) :
    (secondPass F A bit).cost op ≤ productBudget l m l op := by
  have h := materialize_cost_le (secondEntry F A bit) op
    (m * (4 * tick .read op + 2 * tick .field op))
    (fun a c => secondEntry_cost_le F A bit a c op)
  simpa only [secondPass, productBudget, Nat.mul_assoc] using h

theorem addMatrices_cost_le {l : ℕ} (A B : StoredMatrix l l) (op : Op) :
    (addMatrices A B).cost op ≤ additionBudget l op := by
  apply materialize_cost_le
  intro a c
  simp only [bind, Run.bind, StoredThinLQ.entry_cost, StoredGivens.add, charge, Pi.add_apply]
  omega

theorem update_cost_le {l m : ℕ} (A : StoredCore l m)
    (E : StoredMatrix m m) (op : Op) :
    (update A E).cost op ≤ updateBudget l m op := by
  have f₀ := firstPass_cost_le A E 0 op
  have g₀ := secondPass_cost_le (firstPass A E 0).value A 0 op
  have f₁ := firstPass_cost_le A E 1 op
  have g₁ := secondPass_cost_le (firstPass A E 1).value A 1 op
  have s := addMatrices_cost_le
    (secondPass (firstPass A E 0).value A 0).value
    (secondPass (firstPass A E 1).value A 1).value op
  simp only [update, bind, Run.bind, updateBudget, Pi.add_apply]
  omega

private theorem total_add (a b : Cost) :
    StoredRectangularGivens.total (a + b) =
      StoredRectangularGivens.total a + StoredRectangularGivens.total b := by
  simp only [StoredRectangularGivens.total, Pi.add_apply]
  ring

private theorem total_mono {a b : Cost} (h : ∀ op, a op ≤ b op) :
    StoredRectangularGivens.total a ≤ StoredRectangularGivens.total b := by
  unfold StoredRectangularGivens.total
  gcongr <;> apply h

theorem update_total_cost_le {l m : ℕ} (A : StoredCore l m) (E : StoredMatrix m m) :
    StoredRectangularGivens.total (update A E).cost ≤
      12 * l * m * m + 12 * l * l * m + 8 * l * m + 17 * l * l + 20 * l := by
  have h := total_mono (update_cost_le A E)
  have value : StoredRectangularGivens.total (updateBudget l m) =
      12 * l * m * m + 12 * l * l * m + 8 * l * m + 17 * l * l + 20 * l := by
    simp [StoredRectangularGivens.total, updateBudget, productBudget, additionBudget, tick]
    ring
  rwa [value] at h

private theorem identity_total_cost (r : ℕ) :
    StoredRectangularGivens.total (StoredRectangularGivens.identity r).cost =
      5 * r ^ 2 + 4 * r := by
  simp [StoredRectangularGivens.total, StoredRectangularGivens.identity_cost,
    StoredRectangularGivens.identityBudget, tick]
  ring

private theorem node_total : StoredRectangularGivens.total nodeBudget = 6 := by
  simp [nodeBudget, StoredRectangularGivens.total, tick]

/-- Total of all eight counters, including every materialization pass and the
fixed node records. The bond bound concerns the already stored input chain. -/
theorem gram_total_cost_le {n l r : ℕ} (C : StoredChain n l r) (D : ℕ)
    (bound : maxBond (denoteChain C) ≤ D) :
    StoredRectangularGivens.total (gram C).cost ≤
      n * (24 * D ^ 3 + 25 * D ^ 2 + 20 * D + 6) + 5 * D ^ 2 + 4 * D + 6 := by
  induction C with
  | nil r =>
      have hr : r ≤ D := bound
      simp only [gram, cacheNode, total_add, node_total, identity_total_cost,
        Nat.zero_mul, zero_add]
      have square := Nat.pow_le_pow_left hr 2
      omega
  | @cons n l m r A C ih =>
      have hl : l ≤ D := (max_le_iff.mp bound).1
      have ht : maxBond (denoteChain C) ≤ D := (max_le_iff.mp bound).2
      have hm : m ≤ D := by
        cases C with
        | nil r => exact ht
        | cons B C => exact (max_le_iff.mp ht).1
      have tail := ih ht
      have head := update_total_cost_le A (gram C).value
      have headBound : 12 * l * m * m + 12 * l * l * m +
          8 * l * m + 17 * l * l + 20 * l ≤
          24 * D ^ 3 + 25 * D ^ 2 + 20 * D := by
        calc
          _ ≤ 12 * D * D * D + 12 * D * D * D +
              8 * D * D + 17 * D * D + 20 * D := by gcongr
          _ = _ := by ring
      simp only [gram, cacheNode, bind, Run.bind, total_add, node_total]
      nlinarith

theorem norm_cost {n : ℕ} (C : StoredChain n 1 1) (op : Op) :
    (norm C).cost op = (gram C).cost op + 2 * tick .read op + tick .sqrt op := by
  simp only [norm, bind, Run.bind, StoredThinLQ.entry_cost,
    StoredGivens.sqrt, charge, Pi.add_apply]
  omega

/-- The scalar supplier adds precisely two stored reads and one square root. -/
theorem norm_total_cost_le {n : ℕ} (C : StoredChain n 1 1) (D : ℕ)
    (bound : maxBond (denoteChain C) ≤ D) :
    StoredRectangularGivens.total (norm C).cost ≤
      n * (24 * D ^ 3 + 25 * D ^ 2 + 20 * D + 6) + 5 * D ^ 2 + 4 * D + 9 := by
  have h := gram_total_cost_le C D bound
  have extra : StoredRectangularGivens.total (norm C).cost =
      StoredRectangularGivens.total (gram C).cost + 3 := by
    simp [StoredRectangularGivens.total, norm_cost, tick]
    omega
  omega

end QuantumBlockEncoding.StoredTensorTrainNorm
