import QuantumBlockEncoding.MatrixProductChain
import QuantumBlockEncoding.StoredMatrixProductChain
import QuantumBlockEncoding.StoredBinaryCoordinates
import Mathlib.Tactic

namespace HermitePiecewiseUniform
open scoped BigOperators
open QuantumBlockEncoding TensorTrainCanonical

/-- The public physical convention: first word bit is q0, the LSB. -/
def wordValue : {n : ℕ} → Word n → ℕ
  | 0, _ => 0
  | _+1, x => x.1.val + 2*wordValue x.2

theorem wordValue_lt (n : ℕ) (x : Word n) : wordValue x < 2^n := by
  induction n with
  | zero => simp [wordValue]
  | succ n ih =>
    have hb := x.1.isLt
    have ht := ih x.2
    simp only [wordValue, pow_succ]
    omega

/-- Equal higher digits preserve the lower-digit relation; unequal higher
digits overwrite it.0=less,1=equal,2=greater. -/
def finish (a : Fin 3) (x y : ℕ) : Fin 3 :=
  if x < y then 0 else if y < x then 2 else a

def scan (cut : ℕ) : {n : ℕ} → Word n → Fin 3 → Fin 3
  | 0, _, a => a
  | _+1, x, a => scan (cut/2) x.2 (finish a x.1.val (cut%2))

theorem scan_spec (n cut : ℕ) (hcut : cut < 2^n) (x : Word n) (a : Fin 3) :
    scan cut x a = finish a (wordValue x) cut := by
  induction n generalizing cut a with
  | zero =>
    have hc : cut = 0 := by simpa using hcut
    simp [scan, wordValue, finish, hc]
  | succ n ih =>
    have hq : cut/2 < 2^n := by rw [pow_succ] at hcut; omega
    have hr : cut%2 < 2 := Nat.mod_lt _ (by decide)
    have hd := Nat.mod_add_div cut 2
    have hb := x.1.isLt
    simp only [scan, ih _ hq, wordValue]
    by_cases hl : wordValue x.2 < cut/2
    · have h : x.1.val+2*wordValue x.2 < cut := by omega
      simp [finish, hl, h]
    · by_cases hg : cut/2 < wordValue x.2
      · have h : cut < x.1.val+2*wordValue x.2 := by omega
        simp [finish, hl, hg, h, show ¬x.1.val+2*wordValue x.2 < cut by omega]
      · have he : wordValue x.2 = cut/2 := by omega
        have hL : x.1.val+2*wordValue x.2 < cut ↔ x.1.val < cut%2 := by omega
        have hG : cut < x.1.val+2*wordValue x.2 ↔ cut%2 < x.1.val := by omega
        simp [finish, hl, hg, hL, hG]

def comparisonEntry (cut q : ℕ) (bit : Fin 2) (a b : Fin 3) : ℚ :=
  if finish a bit.val ((cut/2^q)%2) = b then 1 else 0

noncomputable def comparisonKernel (cut : ℕ) : MatrixProductChain.Kernel 3 :=
  fun q bit a b => (comparisonEntry cut q bit a b : ℝ)

private theorem shifted_cut (cut q : ℕ) : (cut/2^q)/2 = cut/2^(q+1) := by
  rw [Nat.div_div_eq_div_mul, pow_succ]

theorem readout_scan (cut start n : ℕ) (right : Fin 3 → ℝ)
    (x : Word n) (a : Fin 3) :
    MatrixProductChain.readout (comparisonKernel cut) right start x a =
      right (scan (cut/2^start) x a) := by
  induction n generalizing start a with
  | zero => rfl
  | succ n ih =>
    simp only [MatrixProductChain.readout, Matrix.mulVec, dotProduct,
      comparisonKernel, comparisonEntry, ih]
    rw [Finset.sum_eq_single (finish a x.1.val ((cut/2^start)%2))]
    · simp [scan, shifted_cut]
    · intro b _ hb
      simp [show finish a x.1.val ((cut/2^start)%2) ≠ b from Ne.symm hb]
    · simp

def equalBoundary (a : Fin 3) : ℝ := if a = 1 then 1 else 0

def acceptBoundary (width cut : ℕ) (a : Fin 3) : ℝ :=
  if cut = 0 then 0 else if cut = 2^width then 1 else if a = 0 then 1 else 0

theorem comparison_mask_contract (n cut : ℕ) (hcut : cut ≤ 2^(n+1))
    (x : Word (n+1)) :
    contract (MatrixProductChain.ofKernel (comparisonKernel cut) equalBoundary
      (acceptBoundary (n+1) cut) 0 n) x 0 0 =
      if wordValue x < cut then 1 else 0 := by
  rw [MatrixProductChain.ofKernel_contract]
  rw [Finset.sum_eq_single 1]
  · simp only [equalBoundary, readout_scan, pow_zero, Nat.div_one]
    by_cases hz : cut = 0
    · simp [acceptBoundary, hz]
    · by_cases hN : cut = 2^(n+1)
      · simp [acceptBoundary, hN, wordValue_lt]
      · have hc : cut < 2^(n+1) := by omega
        rw [scan_spec _ _ hc]
        by_cases hl : wordValue x < cut
        · simp [finish, acceptBoundary, hz, hN, hl]
        · by_cases hg : cut < wordValue x
          · simp [finish, acceptBoundary, hz, hN, hl, hg]
          · simp [finish, acceptBoundary, hz, hN, hl, hg]
  · intro b _ hb
    simp [equalBoundary, hb]
  · simp

#print axioms scan_spec
#print axioms readout_scan
#print axioms comparison_mask_contract

open StoredGivens StoredTensorTrain StoredBinaryCoordinates

/--3 comparisons are evaluated once; integer extraction is separately
counted. Powers/address arithmetic and finite-bit costs are not free claims. -/
def generatedEntry (cut q : ℕ) (bit : Fin 2) (a b : Fin 3) : IndexedRun ℝ :=
  let digit := (cut/2^q)%2
  let low := charge .compare (decide (bit.val < digit))
  let high := charge .compare (decide (digit < bit.val))
  let next : Fin 3 := if low.value then 0 else if high.value then 2 else a
  let hit := charge .compare (decide (next = b))
  ⟨⟨if hit.value then 1 else 0, low.cost+high.cost+hit.cost⟩,1,1⟩

theorem generatedEntry_value (cut q : ℕ) (bit : Fin 2) (a b : Fin 3) :
    (generatedEntry cut q bit a b).run.value = comparisonKernel cut q bit a b := by
  simp [generatedEntry, comparisonKernel, comparisonEntry, finish, charge]
  split_ifs <;> norm_num

def generatedTable (cut q : ℕ) : IndexedRun (StoredCore 3 3) :=
  collectIndexed fun a => collectIndexed fun j =>
    generatedEntry cut q (finProdFinEquiv.symm j).1 a (finProdFinEquiv.symm j).2

def comparisonTables (n cut : ℕ) : IndexedRun (Vector (StoredCore 3 3) (n+1)) :=
  collectIndexed fun q => generatedTable cut q.val

theorem generated_window (n cut : ℕ) :
    StoredMatrixProductChain.Window (comparisonTables n cut).run.value (comparisonKernel cut) 0 := by
  apply StoredMatrixProductChain.window_of_entries
  intro q a b bit
  simp only [comparisonTables, collectIndexed_value, generatedTable, denoteCore,
    denote, collectIndexed_value, Equiv.symm_apply_apply, generatedEntry_value, Nat.zero_add]

def storedLeft : Run (Vector ℝ 3) :=
  collect fun a => charge .compare (equalBoundary a)

def storedRight (width cut : ℕ) : Run (Vector ℝ 3) :=
  collect fun a =>
    let zero := charge .compare (decide (cut=0))
    let endpoint := charge .compare (decide (cut=2^width))
    let less := charge .compare (decide (a=0))
    ⟨if zero.value then 0 else if endpoint.value then 1 else if less.value then 1 else 0,
      zero.cost+endpoint.cost+less.cost⟩

@[simp] theorem storedLeft_value (a : Fin 3) : storedLeft.value[a.val] = equalBoundary a := by
  simp [storedLeft, charge]

@[simp] theorem storedRight_value (width cut : ℕ) (a : Fin 3) :
    (storedRight width cut).value[a.val] = acceptBoundary width cut a := by
  simp [storedRight, acceptBoundary, charge]

noncomputable def produceComparison (n cut : ℕ) : IndexedRun (StoredChain (n+1) 1 1) :=
  let tables := comparisonTables n cut
  let left := storedLeft
  let right := storedRight (n+1) cut
  let closed := StoredMatrixProductChain.ofTable tables.run.value left.value right.value
  ⟨⟨closed.value,tables.run.cost+left.cost+right.cost+closed.cost⟩,
    tables.quotientCalls,tables.remainderCalls⟩

theorem produceComparison_refines (n cut : ℕ) :
    denoteChain (produceComparison n cut).run.value =
      MatrixProductChain.ofKernel (comparisonKernel cut) equalBoundary
        (acceptBoundary (n+1) cut) 0 n := by
  unfold produceComparison
  rw [StoredMatrixProductChain.ofTable_refines _ _ _ _ _ (generated_window n cut)]
  simp only [storedLeft_value, storedRight_value]

theorem stored_comparison_contract (n cut : ℕ) (hcut : cut ≤ 2^(n+1))
    (x : Word (n+1)) :
    contract (denoteChain (produceComparison n cut).run.value) x 0 0 =
      if wordValue x < cut then 1 else 0 := by
  rw [produceComparison_refines]
  exact comparison_mask_contract n cut hcut x

theorem generatedEntry_cost (cut q : ℕ) (bit : Fin 2) (a b : Fin 3) (op : Op) :
    (generatedEntry cut q bit a b).run.cost op = 3*tick .compare op := by
  simp [generatedEntry, charge, Pi.add_apply]
  omega

theorem comparisonTables_cost (n cut : ℕ) (op : Op) :
    (comparisonTables n cut).run.cost op =
      (n+1)*(54*tick .compare op+44*tick .read op+44*tick .write op) := by
  simp [comparisonTables, generatedTable, collectIndexed_cost, generatedEntry_cost]
  ring

theorem comparisonTables_quotients (n cut : ℕ) :
    (comparisonTables n cut).quotientCalls = 18*(n+1) := by
  have he (cut q : ℕ) (bit : Fin 2) (a b : Fin 3) :
      (generatedEntry cut q bit a b).quotientCalls = 1 := rfl
  have hcollect {α : Type} {m : ℕ} (f : Fin m → IndexedRun α) :
      (collectIndexed f).quotientCalls = ∑ i, (f i).quotientCalls := by
    simp [collectIndexed]
  simp only [comparisonTables, hcollect, generatedTable, he]
  simp
  omega

theorem comparisonTables_remainders (n cut : ℕ) :
    (comparisonTables n cut).remainderCalls = 18*(n+1) := by
  have he (cut q : ℕ) (bit : Fin 2) (a b : Fin 3) :
      (generatedEntry cut q bit a b).remainderCalls = 1 := rfl
  have hcollect {α : Type} {m : ℕ} (f : Fin m → IndexedRun α) :
      (collectIndexed f).remainderCalls = ∑ i, (f i).remainderCalls := by
    simp [collectIndexed]
  simp only [comparisonTables, hcollect, generatedTable, he]
  simp
  omega

theorem produceComparison_cost (n cut : ℕ) :
    StoredRectangularGivens.total (produceComparison n cut).run.cost ≤ 5*n^2+149*n+479 := by
  have h := StoredMatrixProductChain.ofTable_total_cost_le
    (comparisonTables n cut).run.value storedLeft.value (storedRight (n+1) cut).value
  have hc : StoredRectangularGivens.total (comparisonTables n cut).run.cost = 142*(n+1) := by
    simp [StoredRectangularGivens.total, comparisonTables_cost, tick]
    ring
  have hl : StoredRectangularGivens.total storedLeft.cost = 15 := by
    simp [storedLeft, collect_cost, charge, StoredRectangularGivens.total, tick]
  have hr : StoredRectangularGivens.total (storedRight (n+1) cut).cost = 21 := by
    simp [storedRight, collect_cost, charge, Pi.add_apply, StoredRectangularGivens.total, tick]
  have hadd (a b : Cost) : StoredRectangularGivens.total (a+b) =
      StoredRectangularGivens.total a+StoredRectangularGivens.total b := by
    simp [StoredRectangularGivens.total, Pi.add_apply]
    ring
  simp only [produceComparison, hadd, hc, hl, hr] at *
  norm_num at h
  omega

theorem produceComparison_quotients (n cut : ℕ) :
    (produceComparison n cut).quotientCalls = 18*(n+1) :=
  comparisonTables_quotients n cut

theorem produceComparison_remainders (n cut : ℕ) :
    (produceComparison n cut).remainderCalls = 18*(n+1) :=
  comparisonTables_remainders n cut

#print axioms generated_window
#print axioms produceComparison_refines
#print axioms stored_comparison_contract
#print axioms produceComparison_cost
#print axioms produceComparison_quotients
#print axioms produceComparison_remainders
end HermitePiecewiseUniform
