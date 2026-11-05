import QuantumBlockEncoding.AdjacentGivens

/-!
# Materialized, costed rectangular Givens sweeps

This is an extended exact-real, word-RAM operation model, not a finite-bit
runtime theorem. Field operations, square roots, arccos, trigonometric calls,
exact comparisons, stored-word reads/writes, and emitted rotation records
are separate counters. Stored matrices are nested vectors, never entry
callbacks. `collect` first materializes every counted result in a vector,
then projects its values and sums its stored counters. All scalar work is
performed by charged primitives. Proof checking and counter bookkeeping are
outside the model. Vector replacement is charged for a full copy, so no
in-place-update or copy-on-write optimization is needed for the bound.
-/

namespace QuantumBlockEncoding.StoredGivens

open AdjacentGivens RealAmplitudePreparation

-- The generated finite-enumeration membership proof needs definitional
-- unfolding of the list-to-multiset coercion under Lean 4.33.
set_option backward.isDefEq.respectTransparency false in
inductive Op where
  | field | sqrt | angle | trig | compare | read | write | emit
  deriving DecidableEq, Fintype

abbrev Cost := Op → ℕ

def tick (op : Op) : Cost := fun q => if q = op then 1 else 0

structure Run (α : Type) where
  value : α
  cost : Cost

def Run.pure (x : α) : Run α := ⟨x, 0⟩

def Run.bind (x : Run α) (f : α → Run β) : Run β :=
  let y := f x.value
  ⟨y.value, x.cost + y.cost⟩

instance : Monad Run where
  pure := Run.pure
  bind := Run.bind

def charge (op : Op) (x : α) : Run α := ⟨x, tick op⟩

noncomputable def add (x y : ℝ) : Run ℝ := charge .field (x + y)
noncomputable def sub (x y : ℝ) : Run ℝ := charge .field (x - y)
noncomputable def mul (x y : ℝ) : Run ℝ := charge .field (x * y)
noncomputable def div (x y : ℝ) : Run ℝ := charge .field (x / y)
noncomputable def sqrt (x : ℝ) : Run ℝ := charge .sqrt (Real.sqrt x)
noncomputable def arccos (x : ℝ) : Run ℝ := charge .angle (Real.arccos x)
noncomputable def cos (x : ℝ) : Run ℝ := charge .trig (Real.cos x)
noncomputable def sin (x : ℝ) : Run ℝ := charge .trig (Real.sin x)
noncomputable def zeroTest (x : ℝ) : Run Bool := charge .compare (decide (x = 0))
noncomputable def signTest (x : ℝ) : Run Bool := charge .compare (decide (x < 0))

def read {n : ℕ} (xs : Vector α n) (i : Fin n) : Run α := charge .read xs[i.val]

/-- Two materialized passes: write counted entries, read them for projection
and summation, and write the projected output. Counter words are metadata. -/
def collect {n : ℕ} (f : Fin n → Run α) : Run (Vector α n) :=
  let entries : Vector (Run α) n := Vector.ofFn f
  ⟨entries.map Run.value,
    (fun op => ∑ i : Fin n, entries[i.val].cost op) +
      n • (2 • tick .read + 2 • tick .write)⟩

/-- Persistent full-copy replacement; row references are stored words. -/
def replace {n : ℕ} (xs : Vector α n) (i : Fin n) (x : α) : Run (Vector α n) :=
  ⟨xs.set i.val x, n • (tick .read + tick .write)⟩

abbrev StoredMatrix (N M : ℕ) := Vector (Vector ℝ M) N

def denote {N M : ℕ} (A : StoredMatrix N M) : _root_.Matrix (Fin N) (Fin M) ℝ :=
  fun i j => A[i.val][j.val]

/-- Materializing an input callback is an explicit boundary: this constructor
charges storage but does not certify the callback's scalar evaluation cost. -/
def materialize {N M : ℕ} (f : Fin N → Fin M → Run ℝ) : Run (StoredMatrix N M) :=
  collect (fun i => collect (f i))

@[simp] theorem collect_value {n : ℕ} (f : Fin n → Run α) (i : Fin n) :
    (collect f).value[i.val] = (f i).value := by simp [collect]

@[simp] theorem collect_cost {n : ℕ} (f : Fin n → Run α) (op : Op) :
    (collect f).cost op = (∑ i : Fin n, (f i).cost op) +
      n * (2 * tick .read op + 2 * tick .write op) := by simp [collect]; ring

/-- Compute the norm once, then the exact signed angle once. -/
noncomputable def angle (x y : ℝ) : Run ℝ := do
  let xx ← mul x x
  let yy ← mul y y
  let ss ← add xx yy
  let r ← sqrt ss
  let zero ← zeroTest r
  if zero then pure 0 else do
    let ratio ← div x r
    let a ← arccos ratio
    let negative ← signTest y
    let signed ← if negative then sub 0 a else pure a
    let doubled ← mul 2 signed
    sub 0 doubled

theorem angle_value (x y : ℝ) : (angle x y).value = eliminationAngle x y := by
  simp only [angle, mul, add, sqrt, zeroTest, div, arccos, signTest, sub,
    charge, bind, pure, Run.bind, Run.pure]
  by_cases hz : Real.sqrt (x * x + y * y) = 0 <;> by_cases hy : y < 0 <;>
    simp [eliminationAngle, splitAngle, pairNorm, pow_two, hz, hy, ExactAngle.eval]

/-- One angle and one pair of trigonometric coefficients are shared by all
entries of the two output rows. -/
noncomputable def coefficients (x y : ℝ) : Run (ℝ × ℝ × ℝ) := do
  let theta ← angle x y
  let half ← div theta 2
  let c ← cos half
  let s ← sin half
  pure (theta, c, s)

theorem coefficients_value (x y : ℝ) : (coefficients x y).value =
    (eliminationAngle x y, Real.cos (eliminationAngle x y / 2),
      Real.sin (eliminationAngle x y / 2)) := by
  simp [coefficients, bind, pure, Run.bind, Run.pure, div, cos, sin, charge, angle_value]

/-- The six actual field operations for a pair of entries. -/
noncomputable def entryPair (c s : ℝ) (u v : ℝ) : Run (ℝ × ℝ) := do
  let cu ← mul c u
  let sv ← mul s v
  let su ← mul s u
  let cv ← mul c v
  let first ← sub cu sv
  let second ← add su cv
  pure (first, second)

@[simp] theorem entryPair_value (c s u v : ℝ) :
    (entryPair c s u v).value = (c * u - s * v, s * u + c * v) := rfl

theorem entryPair_cost (c s u v : ℝ) (op : Op) :
    (entryPair c s u v).cost op = 6 * tick .field op := by
  simp [entryPair, mul, sub, add, charge, bind, pure, Run.bind, Run.pure]
  omega

/-- Materialize both rows from a single stored vector of computed pairs. -/
noncomputable def rowPair {M : ℕ} (u v : Vector ℝ M) (c s : ℝ) :
    Run (Vector ℝ M × Vector ℝ M) := do
  let pairs ← collect fun j => do
    let x ← read u j
    let y ← read v j
    entryPair c s x y
  let first ← collect fun j => do
    let pair ← read pairs j
    pure pair.1
  let second ← collect fun j => do
    let pair ← read pairs j
    pure pair.2
  pure (first, second)

theorem rowPair_value {M : ℕ} (u v : Vector ℝ M) (c s : ℝ) (j : Fin M) :
    (rowPair u v c s).value.1[j.val] = c * u[j.val] - s * v[j.val] ∧
    (rowPair u v c s).value.2[j.val] = s * u[j.val] + c * v[j.val] := by
  simp [rowPair, bind, pure, Run.bind, Run.pure, read, charge]

/-- Cached input rows, materialized output rows, then two stored replacements. -/
noncomputable def rotate {N M : ℕ} (A : StoredMatrix N M) (i j : Fin N)
    (c s : ℝ) : Run (StoredMatrix N M) := do
  let u ← read A i
  let v ← read A j
  let rows ← rowPair u v c s
  let B ← replace A j rows.2
  replace B i rows.1

theorem rotate_value {N M : ℕ} (A : StoredMatrix N M) (i j : Fin N)
    (theta : ℝ) :
    denote (rotate A i j (Real.cos (theta / 2)) (Real.sin (theta / 2))).value =
      rotateRows (denote A) i j theta := by
  ext row col
  have hi : i.val = row.val ↔ row = i := by simp [Fin.ext_iff, eq_comm]
  have hj : j.val = row.val ↔ row = j := by simp [Fin.ext_iff, eq_comm]
  simp only [rotate, bind, Run.bind, read, charge, replace, denote,
    Vector.getElem_set]
  by_cases ri : row = i
  · subst row
    simpa [rotateRows, denote] using (rowPair_value A[i.val] A[j.val]
      (Real.cos (theta / 2)) (Real.sin (theta / 2)) col).1
  · by_cases rj : row = j
    · subst row
      simpa [rotateRows, denote, hi, ri] using (rowPair_value A[i.val] A[j.val]
        (Real.cos (theta / 2)) (Real.sin (theta / 2)) col).2
    · simp [rotateRows, denote, ri, rj, hi, hj]

structure Elimination (N M : ℕ) where
  matrix : StoredMatrix N M
  angle : ℝ

noncomputable def eliminate {N M : ℕ} (A : StoredMatrix N M)
    (i j : Fin N) (col : Fin M) : Run (Elimination N M) := do
  let u ← read A i
  let v ← read A j
  let x ← read u col
  let y ← read v col
  let cs ← coefficients x y
  let B ← rotate A i j cs.2.1 cs.2.2
  pure ⟨B, cs.1⟩

theorem eliminate_angle {N M : ℕ} (A : StoredMatrix N M)
    (i j : Fin N) (col : Fin M) :
    (eliminate A i j col).value.angle = eliminationAngle (denote A i col) (denote A j col) := by
  simp [eliminate, bind, pure, Run.bind, Run.pure, read, charge, coefficients_value, denote]

theorem eliminate_matrix {N M : ℕ} (A : StoredMatrix N M)
    (i j : Fin N) (col : Fin M) :
    denote (eliminate A i j col).value.matrix = eliminateEntry (denote A) i j col := by
  simp only [eliminate, bind, pure, Run.bind, Run.pure, read, charge, coefficients_value]
  exact rotate_value A i j _

structure Sweep (N M : ℕ) where
  matrix : StoredMatrix N M
  steps : List (Step N)

/-- One recursion returns both the residual and its actual chronological log.
No separate rerun is used to generate angles or the next matrix. -/
noncomputable def columnSweep {N M : ℕ} (A : StoredMatrix N M)
    (col : Fin M) (lo : ℕ) : (count : ℕ) → lo + count < N → Run (Sweep N M)
  | 0, _ => pure ⟨A, []⟩
  | count + 1, bound => do
      let first : Fin N := ⟨lo + count, by omega⟩
      let second : Fin N := ⟨lo + count + 1, by omega⟩
      let next ← eliminate A first second col
      let tail ← columnSweep next.matrix col lo count (by omega)
      let steps ← charge .emit
        ({ first := first, second := second, adjacent := rfl, angle := next.angle } :: tail.steps)
      pure ⟨tail.matrix, steps⟩

theorem columnSweep_matrix {N M : ℕ} (A : StoredMatrix N M)
    (col : Fin M) (lo count : ℕ) (bound : lo + count < N) :
    denote (columnSweep A col lo count bound).value.matrix =
      AdjacentGivens.columnSweep (denote A) col lo count bound := by
  induction count generalizing A with
  | zero => rfl
  | succ count ih =>
    simp only [columnSweep, bind, pure, Run.bind, Run.pure, charge]
    rw [ih, eliminate_matrix]
    rfl

theorem columnSweep_steps {N M : ℕ} (A : StoredMatrix N M)
    (col : Fin M) (lo count : ℕ) (bound : lo + count < N) :
    (columnSweep A col lo count bound).value.steps =
      columnSweepSteps (denote A) col lo count bound := by
  induction count generalizing A with
  | zero => rfl
  | succ count ih =>
    simp only [columnSweep, bind, pure, Run.bind, Run.pure, charge]
    rw [ih, eliminate_matrix, eliminate_angle]
    rfl

/-- Branch-independent upper bound; the zero pair uses fewer operations. -/
def angleBudget : Cost :=
  7 • tick .field + tick .sqrt + tick .angle + 2 • tick .compare

theorem angle_cost_le (x y : ℝ) (op : Op) : (angle x y).cost op ≤ angleBudget op := by
  simp only [angle, mul, add, sqrt, zeroTest, div, arccos, signTest, sub,
    charge, bind, pure, Run.bind, Run.pure]
  by_cases hz : Real.sqrt (x * x + y * y) = 0 <;> by_cases hy : y < 0 <;>
    cases op <;> simp [hz, hy, angleBudget, tick]

def coefficientBudget : Cost := angleBudget + tick .field + 2 • tick .trig

theorem coefficients_cost_le (x y : ℝ) (op : Op) :
    (coefficients x y).cost op ≤ coefficientBudget op := by
  have h := angle_cost_le x y op
  simp [coefficients, bind, pure, Run.bind, Run.pure, div, cos, sin, charge,
    coefficientBudget] at *
  omega

theorem rowPair_cost {M : ℕ} (u v : Vector ℝ M) (c s : ℝ) (op : Op) :
    (rowPair u v c s).cost op =
      M * (6 * tick .field op + 10 * tick .read op + 6 * tick .write op) := by
  simp [rowPair, bind, pure, Run.bind, Run.pure, read, charge, collect_cost,
    entryPair_cost]
  ring

theorem rotate_cost {N M : ℕ} (A : StoredMatrix N M) (i j : Fin N)
    (c s : ℝ) (op : Op) :
    (rotate A i j c s).cost op =
      M * (6 * tick .field op + 10 * tick .read op + 6 * tick .write op) +
      2 * N * (tick .read op + tick .write op) + 2 * tick .read op := by
  simp [rotate, bind, Run.bind, read, charge, replace, rowPair_cost]
  ring

def eliminationBudget (N M : ℕ) : Cost := fun op =>
  coefficientBudget op +
    M * (6 * tick .field op + 10 * tick .read op + 6 * tick .write op) +
    2 * N * (tick .read op + tick .write op) + 6 * tick .read op

theorem eliminate_cost_le {N M : ℕ} (A : StoredMatrix N M)
    (i j : Fin N) (col : Fin M) (op : Op) :
    (eliminate A i j col).cost op ≤ eliminationBudget N M op := by
  have h := coefficients_cost_le (denote A i col) (denote A j col) op
  simp [eliminate, bind, pure, Run.bind, Run.pure, read, charge,
    rotate_cost, eliminationBudget, denote] at *
  omega

def stepBudget (N M : ℕ) : Cost := eliminationBudget N M + tick .emit

theorem columnSweep_cost_succ {N M : ℕ} (A : StoredMatrix N M)
    (col : Fin M) (lo count : ℕ) (bound : lo + (count + 1) < N) (op : Op) :
    (columnSweep A col lo (count + 1) bound).cost op =
      (eliminate A ⟨lo + count, by omega⟩ ⟨lo + count + 1, by omega⟩ col).cost op +
      (columnSweep
        (eliminate A ⟨lo + count, by omega⟩ ⟨lo + count + 1, by omega⟩ col).value.matrix
        col lo count (by omega)).cost op + tick .emit op := by
  simp [columnSweep, bind, pure, Run.bind, Run.pure, charge]
  omega

/-- Symbolic bound on the actual fused producer, not on just its log length. -/
theorem columnSweep_cost_le {N M : ℕ} (A : StoredMatrix N M)
    (col : Fin M) (lo count : ℕ) (bound : lo + count < N) (op : Op) :
    (columnSweep A col lo count bound).cost op ≤ count * stepBudget N M op := by
  induction count generalizing A with
  | zero => simp [columnSweep, pure, Run.pure]
  | succ count ih =>
    rw [columnSweep_cost_succ]
    have first := eliminate_cost_le A ⟨lo + count, by omega⟩
      ⟨lo + count + 1, by omega⟩ col op
    have rest := ih
      (eliminate A ⟨lo + count, by omega⟩ ⟨lo + count + 1, by omega⟩ col).value.matrix
      (by omega)
    simp only [stepBudget, Pi.add_apply] at *
    nlinarith

theorem stepBudget_fields (N M : ℕ) :
    stepBudget N M .field = 6 * M + 8 ∧
    stepBudget N M .sqrt = 1 ∧
    stepBudget N M .angle = 1 ∧
    stepBudget N M .trig = 2 ∧
    stepBudget N M .compare = 2 ∧
    stepBudget N M .read = 10 * M + 2 * N + 6 ∧
    stepBudget N M .write = 6 * M + 2 * N ∧
    stepBudget N M .emit = 1 := by
  simp [stepBudget, eliminationBudget, coefficientBudget, angleBudget, tick]
  omega

/-- Each iteration emits exactly one record, including a harmless zero-pair
rotation. This is a counter theorem for the producer in addition to its
independent list-length refinement. -/
theorem columnSweep_emit {N M : ℕ} (A : StoredMatrix N M)
    (col : Fin M) (lo count : ℕ) (bound : lo + count < N) :
    (columnSweep A col lo count bound).cost .emit = count := by
  induction count generalizing A with
  | zero => rfl
  | succ count ih =>
    rw [columnSweep_cost_succ, ih]
    have h := eliminate_cost_le A ⟨lo + count, by omega⟩
      ⟨lo + count + 1, by omega⟩ col .emit
    simp [eliminationBudget, coefficientBudget, angleBudget, tick] at h ⊢
    omega

theorem columnSweep_steps_length {N M : ℕ} (A : StoredMatrix N M)
    (col : Fin M) (lo count : ℕ) (bound : lo + count < N) :
    (columnSweep A col lo count bound).value.steps.length = count := by
  rw [columnSweep_steps, AdjacentGivens.columnSweepSteps_length]

/-- The emitted list and materialized residual are a single coherent run. -/
theorem columnSweep_action {N M : ℕ} (A : StoredMatrix N M)
    (col : Fin M) (lo count : ℕ) (bound : lo + count < N) :
    applySteps (columnSweep A col lo count bound).value.steps (denote A) =
      denote (columnSweep A col lo count bound).value.matrix := by
  rw [columnSweep_steps, columnSweep_matrix, columnSweepSteps_action]

/-- Input generation is charged once per materialized entry, and the
specified callback must itself use the counted scalar interface. -/
theorem materialize_cost {N M : ℕ} (f : Fin N → Fin M → Run ℝ) (op : Op) :
    (materialize f).cost op =
      (∑ i : Fin N, ∑ j : Fin M, (f i j).cost op) +
      (N * M + N) * (2 * tick .read op + 2 * tick .write op) := by
  simp [materialize, collect_cost, Finset.sum_add_distrib]
  ring

end QuantumBlockEncoding.StoredGivens
