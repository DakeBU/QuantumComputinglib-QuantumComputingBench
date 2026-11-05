import ActualCoefficients
import QuantumBlockEncoding.StoredGivens
import Mathlib.Data.Nat.Choose.Cast

/-! Computable rational refinement of the factorial/choose/source slice of
StoredHermiteCoefficients. Every rational arithmetic operation is charged.
Index-word arithmetic, fixed record projections and counter metadata are outside
the inherited scalar/word model. No bitlength or GCD bound is asserted. -/
namespace HermiteChargedSourceCache
open scoped BigOperators
open QuantumBlockEncoding.StoredGivens HermitePiecewiseAssembly

def qAdd (x y : ℚ) : Run ℚ := charge .field (x+y)
def qMul (x y : ℚ) : Run ℚ := charge .field (x*y)
def qDiv (x y : ℚ) : Run ℚ := charge .field (x/y)

structure FactorialTable (n : ℕ) where
  values : Vector ℚ (n+1)
  next : ℚ

def extend {n : ℕ} (xs : Vector ℚ (n+1)) (last : ℚ) : Run (Vector ℚ (n+2)) :=
  collect fun i =>
    let result := if h : i.val < n+1 then QuantumBlockEncoding.StoredGivens.read xs ⟨i.val,h⟩ else pure last
    ⟨result.value, tick .compare+result.cost⟩

theorem extend_value {n : ℕ} (xs : Vector ℚ (n+1)) (last : ℚ) (i : Fin (n+2)) :
    (extend xs last).value[i.val] = if h : i.val < n+1 then xs[i.val] else last := by
  simp only [extend, collect_value]
  split <;> rfl

def factorials : (n : ℕ) → Run (FactorialTable n)
  | 0 => do
    let values ← collect (fun _ : Fin 1 => pure (1 : ℚ))
    pure ⟨values,1⟩
  | n+1 => do
    let previous ← factorials n
    let last ← QuantumBlockEncoding.StoredGivens.read previous.values (Fin.last n)
    let value ← qMul previous.next last
    let next ← qAdd previous.next 1
    let values ← extend previous.values value
    pure ⟨values,next⟩

theorem factorials_next (n : ℕ) : (factorials n).value.next = (n+1 : ℕ) := by
  induction n with
  | zero => simp [factorials, bind, pure, Run.bind, Run.pure]
  | succ n ih => simp [factorials, bind, pure, Run.bind, Run.pure, qAdd, charge, ih]

theorem factorials_value (n : ℕ) (i : Fin (n+1)) :
    (factorials n).value.values[i.val] = (i.val.factorial : ℚ) := by
  induction n with
  | zero =>
    have hi : i = 0 := Fin.eq_zero i
    subst i
    simp [factorials, bind, pure, Run.bind, Run.pure, collect]
  | succ n ih =>
    simp only [factorials, bind, pure, Run.bind, Run.pure, QuantumBlockEncoding.StoredGivens.read, qMul, charge, extend_value]
    split_ifs with h
    · exact ih ⟨i.val,h⟩
    · have hi : i.val = n+1 := by omega
      rw [factorials_next, ih (Fin.last n), hi, Nat.factorial_succ]
      simp

def chooseFrom {N : ℕ} (F : Vector ℚ (N+1)) (n r : ℕ)
    (hr : r ≤ n) (hn : n ≤ N) : Run ℚ := do
  let top ← QuantumBlockEncoding.StoredGivens.read F ⟨n,by omega⟩
  let first ← QuantumBlockEncoding.StoredGivens.read F ⟨r,by omega⟩
  let second ← QuantumBlockEncoding.StoredGivens.read F ⟨n-r,by omega⟩
  let denominator ← qMul first second
  qDiv top denominator

theorem chooseFrom_value {N : ℕ} (F : Vector ℚ (N+1))
    (correct : ∀ i : Fin (N+1), F[i.val] = (i.val.factorial : ℚ))
    (n r : ℕ) (hr : r ≤ n) (hn : n ≤ N) :
    (chooseFrom F n r hr hn).value = (n.choose r : ℚ) := by
  simp only [chooseFrom, bind, Run.bind, QuantumBlockEncoding.StoredGivens.read, qMul, qDiv, charge]
  rw [correct ⟨n,by omega⟩, correct ⟨r,by omega⟩, correct ⟨n-r,by omega⟩]
  exact (Nat.cast_choose ℚ hr).symm

def sumEntries : {n : ℕ} → (Fin n → Run ℚ) → Run ℚ
  | 0, _ => pure 0
  | n+1, f => do
    let first ← f 0
    let rest ← sumEntries (fun i : Fin n => f i.succ)
    qAdd first rest

theorem sumEntries_value {n : ℕ} (f : Fin n → Run ℚ) :
    (sumEntries f).value = ∑ i, (f i).value := by
  induction n with
  | zero => simp [sumEntries, pure, Run.pure]
  | succ n ih =>
    simp only [sumEntries, bind, Run.bind, qAdd, charge]
    rw [ih, Fin.sum_univ_succ]

def sourceEntry (k : ℕ) (F : Vector ℚ (2*k+2)) (i : Fin (k+1)) : Run ℚ :=
  sumEntries fun r : Fin (i.val+1) => do
    let binomial ← chooseFrom F (k+i.val-r.val) k (by omega) (by omega)
    let denominator ← QuantumBlockEncoding.StoredGivens.read F ⟨r.val,by omega⟩
    qDiv binomial denominator

theorem sourceEntry_value (k : ℕ) (F : Vector ℚ (2*k+2))
    (correct : ∀ i : Fin (2*k+2), F[i.val] = (i.val.factorial : ℚ))
    (i : Fin (k+1)) : (sourceEntry k F i).value = sourceCoefficientQ k i.val := by
  rw [sourceEntry, sumEntries_value, sourceCoefficientQ]
  rw [← Fin.sum_univ_eq_sum_range]
  apply Finset.sum_congr rfl
  intro r _
  simp only [bind, Run.bind, QuantumBlockEncoding.StoredGivens.read, qDiv, charge, chooseFrom_value F correct]
  rw [correct ⟨r.val,by omega⟩]

def sources (k : ℕ) (F : Vector ℚ (2*k+2)) : Run (Vector ℚ (k+1)) :=
  collect (sourceEntry k F)

def produceSourceCache (k : ℕ) : Run (Vector ℚ (k+1)) := do
  let F ← factorials (2*k+1)
  sources k F.values

theorem produceSourceCache_entry (k : ℕ) (i : Fin (k+1)) :
    (produceSourceCache k).value[i.val] = sourceCoefficientQ k i.val := by
  simp only [produceSourceCache, bind, Run.bind, sources, collect_value]
  exact sourceEntry_value k _ (factorials_value _) i

private theorem tick_le (a b : Op) : tick a b ≤ 1 := by
  unfold tick
  split <;> omega

private theorem collect_cost_le {n : ℕ} (f : Fin n → Run α) (op : Op) (B : ℕ)
    (h : ∀ i, (f i).cost op ≤ B) : (collect f).cost op ≤ n*(B+4) := by
  rw [collect_cost]
  have hs : (∑ i : Fin n, (f i).cost op) ≤ n*B := by
    calc
      _ ≤ ∑ _i : Fin n, B := Finset.sum_le_sum (fun i _ => h i)
      _ = _ := by simp
  have hr := tick_le .read op
  have hw := tick_le .write op
  nlinarith

theorem extend_cost_le {n : ℕ} (xs : Vector ℚ (n+1)) (last : ℚ) (op : Op) :
    (extend xs last).cost op ≤ 6*(n+2) := by
  unfold extend
  have h := collect_cost_le (fun i : Fin (n+2) =>
    let result := if h : i.val < n+1 then QuantumBlockEncoding.StoredGivens.read xs ⟨i.val,h⟩ else pure last
    ⟨result.value, tick .compare+result.cost⟩) op 2 (by
    intro i
    have hc := tick_le .compare op
    have hr := tick_le .read op
    by_cases h : i.val < n+1 <;>
      simp [h, QuantumBlockEncoding.StoredGivens.read, charge, pure, Run.pure, Pi.add_apply] <;> omega)
  nlinarith

theorem factorials_cost_le (n : ℕ) (op : Op) :
    (factorials n).cost op ≤ 10*(n+1)^2 := by
  induction n with
  | zero =>
    have hr := tick_le .read op
    have hw := tick_le .write op
    simp [factorials, bind, pure, Run.bind, Run.pure, collect_cost]
    omega
  | succ n ih =>
    have extension := extend_cost_le (factorials n).value.values
      ((factorials n).value.next*(factorials n).value.values[n]) op
    have hr := tick_le .read op
    have hf := tick_le .field op
    simp only [factorials, bind, pure, Run.bind, Run.pure, QuantumBlockEncoding.StoredGivens.read,
      qMul, qAdd, charge, Pi.add_apply, add_zero]
    nlinarith

theorem chooseFrom_cost {N : ℕ} (F : Vector ℚ (N+1)) (n r : ℕ)
    (hr : r ≤ n) (hn : n ≤ N) (op : Op) :
    (chooseFrom F n r hr hn).cost op = 3*tick .read op+2*tick .field op := by
  simp [chooseFrom, bind, Run.bind, QuantumBlockEncoding.StoredGivens.read, qMul, qDiv, charge]
  omega

private theorem sumEntries_cost_le {n : ℕ} (f : Fin n → Run ℚ) (op : Op) (B : ℕ)
    (h : ∀ i, (f i).cost op ≤ B) :
    (sumEntries f).cost op ≤ n*(B+tick .field op) := by
  induction n with
  | zero => simp [sumEntries, pure, Run.pure]
  | succ n ih =>
    simp only [sumEntries, bind, Run.bind, qAdd, charge, Pi.add_apply]
    have first := h 0
    have rest := ih (fun i => f i.succ) (fun i => h i.succ)
    rw [Nat.succ_mul]
    omega

theorem sourceEntry_cost_le (k : ℕ) (F : Vector ℚ (2*k+2))
    (i : Fin (k+1)) (op : Op) : (sourceEntry k F i).cost op ≤ 8*(k+1) := by
  have hr := tick_le .read op
  have hf := tick_le .field op
  unfold sourceEntry
  have bound := sumEntries_cost_le (fun r : Fin (i.val+1) => do
    let binomial ← chooseFrom F (k+i.val-r.val) k (by omega) (by omega)
    let denominator ← QuantumBlockEncoding.StoredGivens.read F ⟨r.val,by omega⟩
    qDiv binomial denominator) op 7 (by
      intro r
      simp only [bind, Run.bind, QuantumBlockEncoding.StoredGivens.read, qDiv, charge, Pi.add_apply, chooseFrom_cost]
      omega)
  have hi := i.isLt
  nlinarith

theorem sources_cost_le (k : ℕ) (F : Vector ℚ (2*k+2)) (op : Op) :
    (sources k F).cost op ≤ 12*(k+1)^2 := by
  have bound := collect_cost_le (sourceEntry k F) op (8*(k+1))
    (fun i => sourceEntry_cost_le k F i op)
  change (collect (sourceEntry k F)).cost op ≤ _
  nlinarith

theorem produceSourceCache_cost_le (k : ℕ) (op : Op) :
    (produceSourceCache k).cost op ≤ 52*(k+1)^2 := by
  have fact := factorials_cost_le (2*k+1) op
  have src := sources_cost_le k (factorials (2*k+1)).value.values op
  simp only [produceSourceCache, bind, Run.bind, Pi.add_apply]
  nlinarith

#print axioms factorials_value
#print axioms factorials_cost_le
#print axioms chooseFrom_value
#print axioms sourceEntry_value
#print axioms produceSourceCache_entry
#print axioms produceSourceCache_cost_le
end HermiteChargedSourceCache
