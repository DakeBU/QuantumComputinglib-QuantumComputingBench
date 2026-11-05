import QuantumBlockEncoding.StoredBinaryCoordinates
import QuantumBlockEncoding.StoredHermiteGeometry

/-! conditional child-geometry supplier. Integer `span`, cutoff,
and midpoint and the cached parent/width are supplied inputs; generating them
is NOT charged or certified here. In refinement, span = 2^r. No natural-to-real
cast or natural exponentiation is evaluated by this producer.

Each Nat addition is counted separately as a single-word integer operation;
Nat comparisons use the compare counter. These are unit-operation counts for
integers fitting the chosen word, not bit complexity for arbitrary naturals.
Boolean conjunction/negation, finite loop indexing, register-local tuple
access, proofs and counter arithmetic are outside the selected counters.
Stored record payload fields and vector materialization are charged explicitly.
-/
namespace QuantumBlockEncoding.StoredHermiteChildGeometry
open StoredGivens StoredBinaryCoordinates StoredHermiteGeometry HermiteBoundaryInjection

structure Flags where
  full : Bool
  isPartial : Bool

/-- Four actual integer comparisons; `last` is the excluded integer endpoint. -/
def flags (lower upper first last : ℕ) : Run Flags := do
  let lo ← charge .compare (decide (lower ≤ first))
  let hi ← charge .compare (decide (last ≤ upper))
  let below ← charge .compare (decide (last ≤ lower))
  let above ← charge .compare (decide (upper ≤ first))
  let full := lo && hi
  ⟨⟨full, !full && !(below || above)⟩, 2 • tick .write⟩

theorem flags_full (lower upper first size : ℕ) :
    (flags lower upper first (first + size)).value.full = decide (Full lower upper first size) := by
  by_cases hlo : lower ≤ first <;> by_cases hhi : first + size ≤ upper <;>
    simp [flags, bind, Run.bind, charge, Full, hlo, hhi]

theorem flags_partial (lower upper first size : ℕ) :
    (flags lower upper first (first + size)).value.isPartial = decide (Partial lower upper first size) := by
  by_cases hlo : lower ≤ first <;> by_cases hhi : first + size ≤ upper <;>
    by_cases hbelow : first + size ≤ lower <;> by_cases habove : upper ≤ first <;>
    simp [flags, bind, Run.bind, charge, Full, Partial, Outside, hlo, hhi, hbelow, habove]

theorem flags_cost (lower upper first last : ℕ) (op : Op) :
    (flags lower upper first last).cost op = 4 * tick .compare op + 2 * tick .write op := by
  simp [flags, bind, Run.bind, charge]
  ring

structure Child where
  first : ℕ
  lower : ℝ
  upper : ℝ
  leftFull : Bool
  leftPartial : Bool
  middleFull : Bool
  middlePartial : Bool

structure ChildRun (α : Type) where
  run : Run α
  integerAdditions : ℕ

noncomputable def child (parent : Point) (level : TailLevel)
    (span cut midpoint : ℕ) (bit : Bool) : ChildRun Child :=
  let result : Run Child := do
    let parentFirst ← charge .read parent.first
    let parentLower ← charge .read parent.lower
    let width ← charge .read level.width
    let offset ← charge .compare (if bit then ((1 : ℝ), span) else (0, 0))
    let first := parentFirst + offset.2
    let last := first + span
    let shift ← StoredGivens.mul offset.1 width
    let lower ← StoredGivens.add parentLower shift
    let upper ← StoredGivens.add lower width
    let left ← flags 0 cut first last
    let middle ← flags cut midpoint first last
    let lf ← charge .read left.full
    let lp ← charge .read left.isPartial
    let mf ← charge .read middle.full
    let mp ← charge .read middle.isPartial
    ⟨⟨first, lower, upper, lf, lp, mf, mp⟩, 7 • tick .write⟩
  ⟨result, 2⟩

theorem child_first (parent : Point) (level : TailLevel)
    (span cut midpoint : ℕ) (bit : Bool) :
    (child parent level span cut midpoint bit).run.value.first =
      parent.first + if bit then span else 0 := by
  cases bit <;> rfl

theorem child_lower (parent : Point) (level : TailLevel)
    (span cut midpoint : ℕ) (bit : Bool) :
    (child parent level span cut midpoint bit).run.value.lower =
      parent.lower + (if bit then 1 else 0) * level.width := by
  cases bit <;> rfl

theorem child_upper (parent : Point) (level : TailLevel)
    (span cut midpoint : ℕ) (bit : Bool) :
    (child parent level span cut midpoint bit).run.value.upper =
      (child parent level span cut midpoint bit).run.value.lower + level.width := rfl

theorem child_flags (parent : Point) (level : TailLevel)
    (span cut midpoint : ℕ) (bit : Bool) :
    let c := (child parent level span cut midpoint bit).run.value
    c.leftFull = decide (Full 0 cut c.first span) ∧
    c.leftPartial = decide (Partial 0 cut c.first span) ∧
    c.middleFull = decide (Full cut midpoint c.first span) ∧
    c.middlePartial = decide (Partial cut midpoint c.first span) := by
  cases bit <;>
    simp only [child, bind, Run.bind, charge, Bool.false_eq_true, if_false, if_true,
      flags_full, flags_partial] <;> trivial

theorem child_cost (parent : Point) (level : TailLevel)
    (span cut midpoint : ℕ) (bit : Bool) (op : Op) :
    (child parent level span cut midpoint bit).run.cost op =
      3 * tick .field op + 9 * tick .compare op +
        7 * tick .read op + 11 * tick .write op := by
  simp [child, bind, Run.bind, charge, StoredGivens.mul, StoredGivens.add, flags_cost]
  ring

theorem child_integerAdditions (parent : Point) (level : TailLevel)
    (span cut midpoint : ℕ) (bit : Bool) :
    (child parent level span cut midpoint bit).integerAdditions = 2 := rfl

/-- Value-only specification: all cached-data hypotheses are explicit. -/
theorem child_refines (parent : Point) (level : TailLevel)
    (span cut midpoint n r : ℕ) (origin grid : ℝ) (bit : Bool)
    (hp : parent.first = boundarySchedule cut (r + 1))
    (hl : parent.lower = affinePoint origin grid parent.first)
    (hw : level.width = grid * (2 : ℝ)^r)
    (hs : span = 2^r) (hm : midpoint = 2^n) :
    let c := (child parent level span cut midpoint bit).run.value
    c.first = selectedChild (boundarySchedule cut) r bit ∧
    c.lower = affinePoint origin grid (selectedChild (boundarySchedule cut) r bit) ∧
    c.upper = affinePoint origin grid (selectedChild (boundarySchedule cut) r bit + 2^r) ∧
    c.leftFull = decide (Full 0 cut (selectedChild (boundarySchedule cut) r bit) (2^r)) ∧
    c.leftPartial = decide (Partial 0 cut (selectedChild (boundarySchedule cut) r bit) (2^r)) ∧
    c.middleFull = decide (Full cut (2^n) (selectedChild (boundarySchedule cut) r bit) (2^r)) ∧
    c.middlePartial = decide (Partial cut (2^n) (selectedChild (boundarySchedule cut) r bit) (2^r)) := by
  have hf : (child parent level span cut midpoint bit).run.value.first =
      selectedChild (boundarySchedule cut) r bit := by
    rw [child_first, hp, hs]
    rfl
  have hc : (child parent level span cut midpoint bit).run.value.lower =
      affinePoint origin grid (selectedChild (boundarySchedule cut) r bit) := by
    rw [child_lower, hl, hw]
    cases bit <;> simp [selectedChild, affinePoint, hp, Nat.cast_add, Nat.cast_pow]
    ring
  have hu : (child parent level span cut midpoint bit).run.value.upper =
      affinePoint origin grid (selectedChild (boundarySchedule cut) r bit + 2^r) := by
    rw [child_upper, hc, hw]
    simp [affinePoint, Nat.cast_add, Nat.cast_pow]
    ring
  have hg := child_flags parent level span cut midpoint bit
  dsimp only at hg
  rw [hf] at hg
  refine ⟨hf, hc, hu, ?_⟩
  simpa only [hs, hm] using hg

/-- False/true children are computed once each, then stored in this order. -/
noncomputable def children (parent : Point) (level : TailLevel)
    (span cut midpoint : ℕ) : ChildRun (Vector Child 2) :=
  let left := child parent level span cut midpoint false
  let right := child parent level span cut midpoint true
  let stored := collect fun i : Fin 2 => do
    let selectRight ← charge .compare (decide (i.val = 1))
    pure (if selectRight then right.run.value else left.run.value)
  ⟨⟨stored.value, left.run.cost + right.run.cost + stored.cost⟩,
    left.integerAdditions + right.integerAdditions⟩

theorem children_value (parent : Point) (level : TailLevel)
    (span cut midpoint : ℕ) (bit : Bool) :
    (children parent level span cut midpoint).run.value[if bit then 1 else 0]'(by cases bit <;> decide) =
      (child parent level span cut midpoint bit).run.value := by
  cases bit <;> simp [children, collect, bind, Run.bind, pure, Run.pure, charge]

theorem children_cost (parent : Point) (level : TailLevel)
    (span cut midpoint : ℕ) (op : Op) :
    (children parent level span cut midpoint).run.cost op =
      6 * tick .field op + 20 * tick .compare op +
        18 * tick .read op + 26 * tick .write op := by
  simp [children, child_cost, collect_cost, bind, Run.bind, pure, Run.pure, charge]
  ring

theorem children_integerAdditions (parent : Point) (level : TailLevel)
    (span cut midpoint : ℕ) :
    (children parent level span cut midpoint).integerAdditions = 4 := rfl

/-- Fixed charged work for both children; integer additions remain separate. -/
theorem children_total_cost (parent : Point) (level : TailLevel)
    (span cut midpoint : ℕ) :
    (∑ op : Op, (children parent level span cut midpoint).run.cost op) = 70 := by
  simp only [children_cost, Finset.sum_add_distrib, ← Finset.mul_sum]
  have ht (op : Op) : (∑ q : Op, tick op q) = 1 := by simp [tick]
  simp only [ht]
  norm_num

def Refines (c : Child) (cut n r : ℕ) (origin grid : ℝ) (bit : Bool) : Prop :=
  c.first = selectedChild (boundarySchedule cut) r bit ∧
  c.lower = affinePoint origin grid (selectedChild (boundarySchedule cut) r bit) ∧
  c.upper = affinePoint origin grid (selectedChild (boundarySchedule cut) r bit + 2^r) ∧
  c.leftFull = decide (Full 0 cut (selectedChild (boundarySchedule cut) r bit) (2^r)) ∧
  c.leftPartial = decide (Partial 0 cut (selectedChild (boundarySchedule cut) r bit) (2^r)) ∧
  c.middleFull = decide (Full cut (2^n) (selectedChild (boundarySchedule cut) r bit) (2^r)) ∧
  c.middlePartial = decide (Partial cut (2^n) (selectedChild (boundarySchedule cut) r bit) (2^r))

theorem children_refines (parent : Point) (level : TailLevel)
    (span cut midpoint n r : ℕ) (origin grid : ℝ) (bit : Bool)
    (hp : parent.first = boundarySchedule cut (r + 1))
    (hl : parent.lower = affinePoint origin grid parent.first)
    (hw : level.width = grid * (2 : ℝ)^r)
    (hs : span = 2^r) (hm : midpoint = 2^n) :
    Refines ((children parent level span cut midpoint).run.value[
      if bit then 1 else 0]'(by cases bit <;> decide)) cut n r origin grid bit := by
  rw [children_value]
  exact child_refines parent level span cut midpoint n r origin grid bit hp hl hw hs hm

/-- Refinement and charged work belong to the same pair-producing run. -/
theorem children_certified (parent : Point) (level : TailLevel)
    (span cut midpoint n r : ℕ) (origin grid : ℝ)
    (hp : parent.first = boundarySchedule cut (r + 1))
    (hl : parent.lower = affinePoint origin grid parent.first)
    (hw : level.width = grid * (2 : ℝ)^r)
    (hs : span = 2^r) (hm : midpoint = 2^n) :
    let result := children parent level span cut midpoint
    (∀ bit : Bool, Refines (result.run.value[
      if bit then 1 else 0]'(by cases bit <;> decide)) cut n r origin grid bit) ∧
    (∑ op : Op, result.run.cost op) = 70 ∧ result.integerAdditions = 4 :=
  ⟨fun bit => children_refines parent level span cut midpoint n r origin grid bit hp hl hw hs hm,
    children_total_cost parent level span cut midpoint, rfl⟩

/-- With legal source indices, every generated endpoint fits in n+2 bits.
This states a word-size requirement, not the cost of implementing word arithmetic. -/
theorem child_index_word_bound (parent : Point) (level : TailLevel)
    (span cut midpoint n r : ℕ) (bit : Bool)
    (hp : parent.first = boundarySchedule cut (r + 1))
    (hs : span = 2^r) (hc : cut ≤ 2^n) (hr : r ≤ n) :
    (child parent level span cut midpoint bit).run.value.first + span < 2^(n + 2) := by
  have hparent : parent.first ≤ 2^n := by
    rw [hp]
    have hd := Nat.mod_add_div cut (2^(r + 1))
    unfold boundarySchedule
    omega
  have hspan : span ≤ 2^n := by
    rw [hs]
    gcongr
    norm_num
  have hpos : 0 < (2 : ℕ)^n := pow_pos (by decide) _
  rw [child_first]
  cases bit <;> simp only [Bool.false_eq_true, if_false, if_true, pow_succ] <;> omega

end QuantumBlockEncoding.StoredHermiteChildGeometry
