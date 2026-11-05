import QuantumBlockEncoding.HermiteExplicitBond
import QuantumBlockEncoding.StoredTensorTrain

/-!
stored block assembly. Inputs are two materialized field records,
not semantic matrix callbacks. Their production and source correctness remain
separate supplier obligations. Each numerical read, Boolean selection, fixed
tag dispatch, index decode and output materialization is charged below.

The fixed explicit bond decoder includes sum threshold tests and the
finSuccEquiv/insertNth/succAboveCases tests: equality with zero and, on the
failed branch, a less-than-zero test. Inspection bounds the decoder by six
comparisons per index; we conservatively charge eight per decode and eight
for the two decoded tag dispatches. Natural index arithmetic and
proof/counter bookkeeping remain outside the exact-real word operation model;
in particular finProdFinEquiv decoding is index-word arithmetic, not a
finite-bit runtime claim. Small record/vector references are stored words.
No scalar source kernel, exponential, subdivision or coordinate callback is
evaluated by this producer. This does not produce the whole raw source chain.
-/

namespace QuantumBlockEncoding.StoredHermiteKernelTable

open StoredGivens StoredTensorTrain HermiteBoundaryInjection
open scoped BigOperators

/-- P=2k+2, written in the definitional form used by InjectionBond. -/
structure Fields (k : ℕ) where
  leftPartial : Bool
  leftInjection : ℝ
  leftFree : ℝ
  middlePartial : Bool
  middleInjection : Vector ℝ (2 * k + 1 + 1)
  shared : StoredMatrix (2 * k + 1 + 1) (2 * k + 1 + 1)
  rightCore : ℝ

/-- Mathematical block interpretation; not used to evaluate stored entries. -/
def blockView {k : ℕ} (f : Fields k) :
    HermiteFiniteBond k → HermiteFiniteBond k → ℝ
  | .inl none, .inl none => if f.leftPartial then 1 else 0
  | .inl none, .inl (some _) => f.leftInjection
  | .inl (some _), .inl (some _) => f.leftFree
  | .inr (.inl none), .inr (.inl none) => if f.middlePartial then 1 else 0
  | .inr (.inl none), .inr (.inl (some j)) => f.middleInjection[j.val]
  | .inr (.inl (some i)), .inr (.inl (some j)) => denote f.shared i j
  | .inr (.inr _), .inr (.inr _) => f.rightCore
  | _, _ => 0

/-- Actual stored-word readers and literal-zero blocks. -/
def storedBlock {k : ℕ} (f : Fields k)
    (a b : HermiteFiniteBond k) : Run ℝ :=
  let result : Run ℝ := match a, b with
    | .inl none, .inl none => do
        let flag ← charge .read f.leftPartial
        charge .compare (if flag then 1 else 0)
    | .inl none, .inl (some _) => charge .read f.leftInjection
    | .inl (some _), .inl (some _) => charge .read f.leftFree
    | .inr (.inl none), .inr (.inl none) => do
        let flag ← charge .read f.middlePartial
        charge .compare (if flag then 1 else 0)
    | .inr (.inl none), .inr (.inl (some j)) => do
        let row ← charge .read f.middleInjection
        StoredGivens.read row j
    | .inr (.inl (some i)), .inr (.inl (some j)) => do
        let table ← charge .read f.shared
        StoredThinLQ.entry table i j
    | .inr (.inr _), .inr (.inr _) => charge .read f.rightCore
    | _, _ => pure 0
  ⟨result.value, 8 • tick .compare + result.cost⟩

theorem storedBlock_value {k : ℕ} (f : Fields k) (a b : HermiteFiniteBond k) :
    (storedBlock f a b).value = blockView f a b := by
  rcases a with a | (a | a) <;> rcases b with b | (b | b)
  all_goals cases a <;> cases b <;>
    simp [storedBlock, blockView, bind, pure, Run.bind, Run.pure,
      charge, StoredGivens.read, StoredThinLQ.entry, denote] <;> rfl

/-- The production explicit equivalence is executable, not a cardinality
choice. A fixed overcharge covers its sum and option comparisons. -/
def decode (k : ℕ) (a : Fin (2 * k + 6)) : Run (HermiteFiniteBond k) :=
  ⟨HermiteExplicitBond.bondEquiv k a, 8 • tick .compare⟩

def entry {k : ℕ} (fields : Vector (Fields k) 2)
    (a : Fin (2 * k + 6)) (out : Fin 2 × Fin (2 * k + 6)) : Run ℝ := do
  let f ← StoredGivens.read fields out.1
  let row ← decode k a
  let col ← decode k out.2
  storedBlock f row col

theorem entry_value {k : ℕ} (fields : Vector (Fields k) 2)
    (a : Fin (2 * k + 6)) (out : Fin 2 × Fin (2 * k + 6)) :
    (entry fields a out).value = blockView fields[out.1.val]
      (HermiteExplicitBond.bondEquiv k a) (HermiteExplicitBond.bondEquiv k out.2) := by
  simp only [entry, bind, Run.bind, StoredGivens.read, charge, decode, storedBlock_value]

/-- Output columns are exactly finProdFinEquiv (bit, outgoing bond), as in
StoredTensorTrain.denoteCore. Thus each row stores both bit slices. -/
def assemble {k : ℕ} (fields : Vector (Fields k) 2) :
    Run (StoredCore (2 * k + 6) (2 * k + 6)) :=
  materialize fun a j => entry fields a (finProdFinEquiv.symm j)

theorem assemble_value {k : ℕ} (fields : Vector (Fields k) 2)
    (a : Fin (2 * k + 6)) (out : Fin 2 × Fin (2 * k + 6)) :
    denoteCore (assemble fields).value a out = blockView fields[out.1.val]
      (HermiteExplicitBond.bondEquiv k a) (HermiteExplicitBond.bondEquiv k out.2) := by
  simp only [assemble, denoteCore, denote, materialize, collect_value,
    Equiv.symm_apply_apply, entry_value]

private theorem tick_le_one (a b : Op) : tick a b ≤ 1 := by
  unfold tick
  split <;> omega

theorem storedBlock_cost_le {k : ℕ} (f : Fields k)
    (a b : HermiteFiniteBond k) (op : Op) : (storedBlock f a b).cost op ≤ 12 := by
  have hc := tick_le_one .compare op
  have hr := tick_le_one .read op
  rcases a with a | (a | a) <;> rcases b with b | (b | b)
  all_goals cases a <;> cases b <;>
    simp [storedBlock, bind, pure, Run.bind, Run.pure, charge, StoredGivens.read,
      StoredThinLQ.entry_cost, Pi.add_apply] <;> omega

theorem entry_cost_le {k : ℕ} (fields : Vector (Fields k) 2)
    (a : Fin (2 * k + 6)) (out : Fin 2 × Fin (2 * k + 6)) (op : Op) :
    (entry fields a out).cost op ≤ 29 := by
  have hc := tick_le_one .compare op
  have hr := tick_le_one .read op
  have hb := storedBlock_cost_le fields[out.1.val]
    (HermiteExplicitBond.bondEquiv k a) (HermiteExplicitBond.bondEquiv k out.2) op
  simp only [entry, bind, Run.bind, StoredGivens.read, charge, decode, Pi.add_apply,
    Pi.smul_apply, smul_eq_mul]
  omega

theorem assemble_cost_le {k : ℕ} (fields : Vector (Fields k) 2) (op : Op) :
    (assemble fields).cost op ≤ 72 * (2 * k + 6)^2 := by
  rw [assemble, materialize_cost]
  have hb : (∑ a : Fin (2 * k + 6), ∑ j : Fin (2 * (2 * k + 6)),
      (entry fields a (finProdFinEquiv.symm j)).cost op) ≤
        (2 * k + 6) * (2 * (2 * k + 6)) * 29 := by
    calc
      _ ≤ ∑ _a : Fin (2 * k + 6), ∑ _j : Fin (2 * (2 * k + 6)), 29 := by
        apply Finset.sum_le_sum
        intro a _
        apply Finset.sum_le_sum
        intro j _
        exact entry_cost_le fields a _ op
      _ = _ := by simp; ring
  have hr := tick_le_one .read op
  have hw := tick_le_one .write op
  nlinarith

theorem assemble_total_cost_le {k : ℕ} (fields : Vector (Fields k) 2) :
    (∑ op : Op, (assemble fields).cost op) ≤ 576 * (2 * k + 6)^2 := by
  have h := Finset.sum_le_sum (fun op (_ : op ∈ Finset.univ) => assemble_cost_le fields op)
  have hc : Fintype.card Op = 8 := by decide
  calc
    _ ≤ 8 * (72 * (2 * k + 6)^2) := by simpa [hc] using h
    _ = _ := by ring

/-- Explicit supplier obligations. Injections must ALREADY contain their
Full guard, including zero on disabled children. No source callback is run. -/
structure SourceCorrect (k n t : ℕ) (L : ℝ) (bit : Fin 2) (f : Fields k) : Prop where
  leftPartial : f.leftPartial = decide (Partial 0 (cutIndex n L)
    (selectedChild (boundarySchedule (cutIndex n L)) (n - t) (decide (bit = 1)))
    (2^(n-t)))
  leftInjection : f.leftInjection = if Full 0 (cutIndex n L)
    (selectedChild (boundarySchedule (cutIndex n L)) (n - t) (decide (bit = 1)))
    (2^(n-t)) then leftInject (-Real.pi * L) (gridStep n L)
      (selectedChild (boundarySchedule (cutIndex n L)) (n - t) (decide (bit = 1)))
      (n-t) else 0
  leftFree : f.leftFree = HermiteBoundaryInjection.leftFree (gridStep n L) (n-t)
    (decide (bit = 1))
  middlePartial : f.middlePartial = decide (Partial (cutIndex n L) (2^n)
    (selectedChild (boundarySchedule (cutIndex n L)) (n - t) (decide (bit = 1)))
    (2^(n-t)))
  middleInjection : ∀ j : Fin (2*k+1+1), f.middleInjection[j.val] =
    if Full (cutIndex n L) (2^n)
      (selectedChild (boundarySchedule (cutIndex n L)) (n - t) (decide (bit = 1)))
      (2^(n-t)) then blockInjectionRow k (-Real.pi * L) (gridStep n L)
        (selectedChild (boundarySchedule (cutIndex n L)) (n - t) (decide (bit = 1)))
        (n-t) j else 0
  shared : ∀ i j, denote f.shared i j = sharedCore (2*k+1) (decide (bit = 1)) i j
  rightCore : f.rightCore = HermiteBoundaryInjection.rightCore n (gridStep n L)
    (n-t) (decide (bit = 1))

theorem blockView_source {k n t : ℕ} {L : ℝ} {bit : Fin 2} {f : Fields k}
    (h : SourceCorrect k n t L bit f) (a b : HermiteFiniteBond k) :
    blockView f a b = hermiteKernel k n L (n-t) (decide (bit = 1)) a b := by
  rcases a with a | (a | a) <;> rcases b with b | (b | b)
  all_goals cases a <;> cases b <;>
    simp [blockView, hermiteKernel, sumKernel, leftKernel, middleKernel, rightKernel,
      scalarCore, injectionCore, h.leftPartial, h.leftInjection, h.leftFree,
      h.middlePartial, h.middleInjection, h.shared, h.rightCore]

/-- Strong entry refinement to the exact explicit layout kernel. Its seven
field hypotheses are supplier obligations, not asserted source generation. -/
theorem assemble_source {k n t : ℕ} {L : ℝ} (fields : Vector (Fields k) 2)
    (correct : ∀ bit : Fin 2, SourceCorrect k n t L bit fields[bit.val])
    (a : Fin (2*k+6)) (out : Fin 2 × Fin (2*k+6)) :
    denoteCore (assemble fields).value a out =
      HermiteExplicitBond.kernel k n L t out.1 a out.2 := by
  rw [assemble_value]
  exact blockView_source (correct out.1) _ _

end QuantumBlockEncoding.StoredHermiteKernelTable
