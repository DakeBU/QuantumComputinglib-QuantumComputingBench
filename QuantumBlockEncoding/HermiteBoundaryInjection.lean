import QuantumBlockEncoding.HermiteBernstein
import QuantumBlockEncoding.HermiteSampleStructure

/-!
# One-boundary Bernstein injection

Exact, MSB-first dyadic interval traversal for the stable Hermite candidate.
Fully included nodes inject restricted source coefficients; subsequent digits
use the shared half-subdivision states. Outside nodes return zero. Theorems
below identify this traversal with the literal source polynomial on the grid.
The finite matrix contraction is proved for all three branches and their
fixed-width direct sum. This does not certify the subsequent QR, primitive
circuit, or finite-precision code.
-/

noncomputable section

namespace QuantumBlockEncoding.HermiteBoundaryInjection

open HermiteBernstein

/-- The first list entry is the most significant digit. -/
def wordValue : List Bool → ℕ
  | [] => 0
  | bit :: bits => (if bit then 2 ^ bits.length else 0) + wordValue bits

theorem wordValue_lt (bits : List Bool) : wordValue bits < 2 ^ bits.length := by
  induction bits with
  | nil => simp [wordValue]
  | cons bit bits ih =>
    cases bit <;> simp only [wordValue, List.length_cons, Bool.false_eq_true,
      if_false, if_true, zero_add, pow_succ] <;> omega

/-- Reconciles the polynomial's real path coordinate with integer bit order. -/
theorem pathCoordinate_eq_wordValue (bits : List Bool) :
    pathCoordinate bits 0 = (wordValue bits : ℝ) / 2 ^ bits.length := by
  induction bits with
  | nil => simp [pathCoordinate, wordValue]
  | cons bit bits ih =>
    cases bit <;>
      simp only [pathCoordinate, childCoordinate, Bool.false_eq_true,
        if_false, if_true, wordValue, List.length_cons, Nat.cast_add,
        Nat.cast_pow, Nat.cast_ofNat, zero_add, pow_succ, ih] <;>
      field_simp

/-- A dyadic node lies entirely in the half-open target interval. -/
def Full (lower upper first size : ℕ) : Prop :=
  lower ≤ first ∧ first + size ≤ upper

/-- A dyadic node is disjoint from the half-open target interval. -/
def Outside (lower upper first size : ℕ) : Prop :=
  first + size ≤ lower ∨ upper ≤ first

instance (lower upper first size : ℕ) : Decidable (Full lower upper first size) :=
  inferInstanceAs (Decidable (_ ∧ _))

instance (lower upper first size : ℕ) : Decidable (Outside lower upper first size) :=
  inferInstanceAs (Decidable (_ ∨ _))

/-- A genuinely unresolved interval, not a wholly included or outside node. -/
def Partial (lower upper first size : ℕ) : Prop :=
  ¬ Full lower upper first size ∧ ¬ Outside lower upper first size

instance (lower upper first size : ℕ) : Decidable (Partial lower upper first size) :=
  inferInstanceAs (Decidable (_ ∧ _))

/-- At an upper-aligned cut there is only one possible unresolved prefix.
The quotient is computed directly; no list of prefixes is constructed. -/
theorem partial_prefix_eq (lower M B x : ℕ) (hM : 0 < M)
    (hp : Partial lower (M * B) (M * x) M) : x = lower / M := by
  obtain ⟨hnf, hno⟩ := hp
  simp only [Full, Outside, not_or] at hnf hno
  have hxB : x < B := by
    by_contra hx
    have hm := Nat.mul_le_mul_left M (show B ≤ x by omega)
    omega
  have hend : M * x + M ≤ M * B := by
    have hm := Nat.mul_le_mul_left M (show x + 1 ≤ B by omega)
    nlinarith
  have hfirst : M * x < lower := by
    by_contra h
    exact hnf ⟨by omega, hend⟩
  have hlast : lower < M * x + M := by omega
  have hrem := Nat.mod_lt lower hM
  have hdiv := Nat.div_add_mod lower M
  by_contra he
  rcases lt_or_gt_of_ne he with hl | hr
  · have hm := Nat.mul_le_mul_left M (show x + 1 ≤ lower / M by omega)
    simp only [Nat.mul_add, Nat.mul_one] at hm
    omega
  · have hm := Nat.mul_le_mul_left M (show lower / M + 1 ≤ x by omega)
    simp only [Nat.mul_add, Nat.mul_one] at hm
    omega

theorem partial_prefix_unique (lower M B x y : ℕ) (hM : 0 < M)
    (hx : Partial lower (M * B) (M * x) M)
    (hy : Partial lower (M * B) (M * y) M) : x = y := by
  rw [partial_prefix_eq lower M B x hM hx, partial_prefix_eq lower M B y hM hy]

/-- The integer endpoint prevents an unresolved state at the last bit. -/
theorem not_partial_unit (lower upper first : ℕ) :
    ¬ Partial lower upper first 1 := by
  simp only [Partial, Full, Outside]
  omega

/-- Every cut after the first consumed bit in an `n+1`-bit middle interval
has an upper endpoint aligned with the remaining dyadic block size. -/
theorem partial_middle_prefix_unique (lower pWidth sWidth x y : ℕ)
    (hx : Partial lower (2 ^ (pWidth + sWidth)) (2 ^ sWidth * x) (2 ^ sWidth))
    (hy : Partial lower (2 ^ (pWidth + sWidth)) (2 ^ sWidth * y) (2 ^ sWidth)) :
    x = y := by
  apply partial_prefix_unique lower (2 ^ sWidth) (2 ^ pWidth) x y (by positivity)
  · simpa only [pow_add, Nat.mul_comm] using hx
  · simpa only [pow_add, Nat.mul_comm] using hy

/-- The initial whole-grid node cannot inject directly: its upper child is
outside the middle component. Thus nonempty traversal begins with a digit. -/
theorem middle_root_not_full (lower n : ℕ) : ¬ Full lower (2 ^ n) 0 (2 ^ (n + 1)) := by
  have hp : 0 < 2 ^ n := by positivity
  simp only [Full, zero_add, pow_succ]
  omega

/-- Affine source coordinate, also meaningful at a block's excluded endpoint. -/
def affinePoint (origin step : ℝ) (j : ℕ) : ℝ := origin + step * j

/-- Literal restricted Bernstein row readout for a fully included dyadic node. -/
def injectedReadout (k : ℕ) (origin step : ℝ) (first : ℕ) (bits : List Bool) : ℝ :=
  subdivisionPath (2 * k + 1)
    (restrictCoefficients (2 * k + 1)
      (1 + affinePoint origin step first)
      (1 + affinePoint origin step (first + 2 ^ bits.length))
      (sourceBernsteinCoefficient k)) bits 0

theorem injectedReadout_eq (k : ℕ) (origin step : ℝ) (first : ℕ)
    (bits : List Bool) (hfirst : affinePoint origin step first ≠ 0) :
    injectedReadout k origin step first bits =
      (HermitePolynomial.sourceInterpolant k).eval
        (affinePoint origin step (first + wordValue bits)) := by
  unfold injectedReadout
  rw [sourceInterpolant_subdivision_readout k _ _ (by simpa using hfirst),
    pathCoordinate_eq_wordValue]
  congr 1
  simp only [affinePoint, Nat.cast_add, Nat.cast_pow, Nat.cast_ofNat]
  field_simp
  ring

/-- A finite coefficient basis vector, extended by zero to the existing
Bernstein coefficient API. -/
def unitCoefficient (d : ℕ) (i : Fin (d + 1)) : ℕ → ℝ :=
  fun j => if j = i.val then 1 else 0

/-- The actual finite row-update matrix: input coefficient `i`, output `j`.
It is the transpose of the usual coefficient-column subdivision matrix. -/
def sharedCore (d : ℕ) (bit : Bool) :
    _root_.Matrix (Fin (d + 1)) (Fin (d + 1)) ℝ :=
  fun i j => halfSubdivision d bit (unitCoefficient d i) j.val

/-- The prototype's lower triangular subdivision, transposed for row updates. -/
theorem sharedCore_false (d : ℕ) (i j : Fin (d + 1)) :
    sharedCore d false i j =
      if i.val ≤ j.val then (j.val.choose i.val : ℝ) / 2 ^ j.val else 0 := by
  simp only [sharedCore, halfSubdivision, Bool.false_eq_true, if_false]
  rw [leftRestriction_half]
  simp only [unitCoefficient, ite_mul, one_mul, zero_mul, ite_div, zero_div]
  rw [Finset.sum_ite_eq']
  simp only [Finset.mem_range, Nat.lt_succ_iff]

/-- The prototype's upper triangular subdivision, in the same row orientation. -/
theorem sharedCore_true (d : ℕ) (i j : Fin (d + 1)) :
    sharedCore d true i j =
      if j.val ≤ i.val then ((d - j.val).choose (i.val - j.val) : ℝ) /
        2 ^ (d - j.val) else 0 := by
  simp only [sharedCore, halfSubdivision, if_true]
  rw [rightRestriction_half d j.val (by omega)]
  simp only [unitCoefficient, ite_mul, one_mul, zero_mul, ite_div, zero_div]
  by_cases hij : j.val ≤ i.val
  · rw [if_pos hij]
    have he (m : ℕ) : j.val + m = i.val ↔ m = i.val - j.val := by omega
    simp only [he]
    rw [Finset.sum_ite_eq']
    have hm : i.val - j.val ∈ Finset.range (d - j.val + 1) := by
      simp only [Finset.mem_range]
      omega
    rw [if_pos hm]
  · rw [if_neg hij]
    apply Finset.sum_eq_zero
    intro m _
    rw [if_neg (by omega : ¬ j.val + m = i.val)]

/-- One finite core has the Bernstein basis pullback dictated by its bit. -/
theorem sharedCore_basis (d : ℕ) (bit : Bool) (i : Fin (d + 1)) (t : ℝ) :
    (∑ j : Fin (d + 1), sharedCore d bit i j * basis d j.val t) =
      basis d i.val (childCoordinate bit t) := by
  have h := halfSubdivision_eval d (unitCoefficient d i) bit t
  simp only [unitCoefficient, ite_mul, one_mul, zero_mul] at h
  have hi : i.val ∈ Finset.range (d + 1) := Finset.mem_range.mpr i.isLt
  simp only [Finset.sum_ite_eq', hi, if_true] at h
  rw [← Fin.sum_univ_eq_sum_range] at h
  exact h

/-- Backward finite-matrix contraction with the terminal coefficient-zero
selector. Every summation has `d+1` entries, independent of the grid width. -/
def sharedContract (d : ℕ) : List Bool → Fin (d + 1) → ℝ
  | [], i => if i.val = 0 then 1 else 0
  | bit :: bits, i => ∑ j : Fin (d + 1), sharedCore d bit i j * sharedContract d bits j

/-- All finite shared-core products, with arbitrary MSB-first suffix length. -/
theorem sharedContract_eq_basis (d : ℕ) (bits : List Bool) (i : Fin (d + 1)) :
    sharedContract d bits i = basis d i.val (pathCoordinate bits 0) := by
  induction bits generalizing i with
  | nil => simp [sharedContract, pathCoordinate, basis, bernsteinPolynomial.eval_at_0]
  | cons bit bits ih =>
    simp only [sharedContract, ih, pathCoordinate]
    exact sharedCore_basis d bit i (pathCoordinate bits 0)

/-- The restricted coefficient row contracted with the finite core matrices. -/
def injectedFiniteReadout (k : ℕ) (origin step : ℝ) (first : ℕ)
    (bits : List Bool) : ℝ :=
  ∑ i : Fin (2 * k + 1 + 1),
    restrictCoefficients (2 * k + 1)
      (1 + affinePoint origin step first)
      (1 + affinePoint origin step (first + 2 ^ bits.length))
      (sourceBernsteinCoefficient k) i.val * sharedContract (2 * k + 1) bits i

/-- Matrix-level finite restriction/suffix adapter, not an assumed contract. -/
theorem injectedFiniteReadout_eq_injectedReadout (k : ℕ) (origin step : ℝ)
    (first : ℕ) (bits : List Bool) :
    injectedFiniteReadout k origin step first bits =
      injectedReadout k origin step first bits := by
  unfold injectedFiniteReadout injectedReadout
  rw [subdivisionPath_readout, ← Fin.sum_univ_eq_sum_range]
  simp only [sharedContract_eq_basis]

theorem injectedFiniteReadout_eq (k : ℕ) (origin step : ℝ) (first : ℕ)
    (bits : List Bool) (hfirst : affinePoint origin step first ≠ 0) :
    injectedFiniteReadout k origin step first bits =
      (HermitePolynomial.sourceInterpolant k).eval
        (affinePoint origin step (first + wordValue bits)) := by
  rw [injectedFiniteReadout_eq_injectedReadout]
  exact injectedReadout_eq k origin step first bits hfirst

/-- Follow one query path. Once injected, remaining digits update only the
shared polynomial row. Before injection, only the boundary branch continues. -/
def boundaryReadout (k : ℕ) (origin step : ℝ) (lower upper first : ℕ)
    (bits : List Bool) : ℝ :=
  if Full lower upper first (2 ^ bits.length) then
    injectedReadout k origin step first bits
  else if Outside lower upper first (2 ^ bits.length) then 0
  else match bits with
    | [] => 0
    | bit :: rest => boundaryReadout k origin step lower upper
        (first + if bit then 2 ^ rest.length else 0) rest
termination_by bits.length

/-- Exact traversal semantics. The sole coordinate hypothesis is a restriction
domain condition, not an assumed equality between the source and the cores. -/
theorem boundaryReadout_eq (k : ℕ) (origin step : ℝ) (lower upper : ℕ)
    (hvalid : ∀ j, lower ≤ j → j < upper → affinePoint origin step j ≠ 0)
    (first : ℕ) (bits : List Bool) :
    boundaryReadout k origin step lower upper first bits =
      if lower ≤ first + wordValue bits ∧ first + wordValue bits < upper then
        (HermitePolynomial.sourceInterpolant k).eval
          (affinePoint origin step (first + wordValue bits)) else 0 := by
  induction bits generalizing first with
  | nil =>
    rw [boundaryReadout]
    by_cases hf : Full lower upper first (2 ^ ([] : List Bool).length)
    · rw [if_pos hf, injectedReadout_eq]
      · simp only [List.length_nil, pow_zero, Full] at hf
        simp [wordValue, show lower ≤ first ∧ first < upper by omega]
      · apply hvalid first hf.1
        have hs : 0 < 2 ^ ([] : List Bool).length := by positivity
        have := hf.2
        omega
    · rw [if_neg hf]
      have hn : ¬(lower ≤ first ∧ first < upper) := by
        simp only [Full, List.length_nil, pow_zero] at hf
        omega
      simp [wordValue, hn]
  | cons bit bits ih =>
    rw [boundaryReadout]
    by_cases hf : Full lower upper first (2 ^ (bit :: bits).length)
    · rw [if_pos hf, injectedReadout_eq]
      · have hw := wordValue_lt (bit :: bits)
        have hm : lower ≤ first + wordValue (bit :: bits) ∧
            first + wordValue (bit :: bits) < upper := by
          obtain ⟨hl, hu⟩ := hf
          omega
        rw [if_pos hm]
      · apply hvalid first hf.1
        have hs : 0 < 2 ^ (bit :: bits).length := by positivity
        have := hf.2
        omega
    · rw [if_neg hf]
      by_cases ho : Outside lower upper first (2 ^ (bit :: bits).length)
      · rw [if_pos ho]
        have hw := wordValue_lt (bit :: bits)
        have hn : ¬(lower ≤ first + wordValue (bit :: bits) ∧
            first + wordValue (bit :: bits) < upper) := by
          rcases ho with ho | ho <;> omega
        rw [if_neg hn]
      · rw [if_neg ho, ih]
        simp only [wordValue, Nat.add_assoc] <;> rfl

/-- One unresolved boundary scalar and one shared degree-sized coefficient row. -/
abbrev InjectionBond (k : ℕ) := Option (Fin (2 * k + 1 + 1))

/-- First integer index of the selected child; `r` is its remaining width. -/
def selectedChild (schedule : ℕ → ℕ) (r : ℕ) (bit : Bool) : ℕ :=
  schedule (r + 1) + if bit then 2 ^ r else 0

/-- Full-block injection parameters are exactly `u=1+origin+step*first` and
`v=1+origin+step*(first+2^r)`. This row has only `2*k+2` entries. -/
def blockInjectionRow (k : ℕ) (origin step : ℝ) (first r : ℕ) :
    Fin (2 * k + 1 + 1) → ℝ :=
  fun i => restrictCoefficients (2 * k + 1)
    (1 + affinePoint origin step first)
    (1 + affinePoint origin step (first + 2 ^ r))
    (sourceBernsteinCoefficient k) i.val

/-- Actual finite core, with one shared boundary state at every level.
Rows are input states; columns are output states. No prefix-indexed space occurs. -/
def injectionCore (k : ℕ) (origin step : ℝ) (lower upper : ℕ)
    (schedule : ℕ → ℕ) (r : ℕ) (bit : Bool) :
    _root_.Matrix (InjectionBond k) (InjectionBond k) ℝ
  | none, none => if Partial lower upper (selectedChild schedule r bit) (2 ^ r) then 1 else 0
  | none, some j => if Full lower upper (selectedChild schedule r bit) (2 ^ r) then
      blockInjectionRow k origin step (selectedChild schedule r bit) r j else 0
  | some _, none => 0
  | some i, some j => sharedCore (2 * k + 1) bit i j

/-- Finite matrix contraction, terminating with the coefficient-zero selector.
The level is read from the suffix length, so every word shares one core sequence. -/
def injectionContract (k : ℕ) (origin step : ℝ) (lower upper : ℕ)
    (schedule : ℕ → ℕ) : List Bool → InjectionBond k → ℝ
  | [], none => 0
  | [], some i => if i.val = 0 then 1 else 0
  | bit :: bits, i => ∑ j : InjectionBond k,
      injectionCore k origin step lower upper schedule bits.length bit i j *
        injectionContract k origin step lower upper schedule bits j

/-- After injection, the finite contraction never re-enters the boundary state. -/
theorem injectionContract_shared (k : ℕ) (origin step : ℝ) (lower upper : ℕ)
    (schedule : ℕ → ℕ) (bits : List Bool) (i : Fin (2 * k + 1 + 1)) :
    injectionContract k origin step lower upper schedule bits (some i) =
      sharedContract (2 * k + 1) bits i := by
  induction bits generalizing i with
  | nil => rfl
  | cons bit bits ih =>
    simp only [injectionContract, Fintype.sum_option, injectionCore, zero_mul, zero_add,
      ih, sharedContract]

/-- The schedule obligation is purely integer control flow: any partial child
must be the unique boundary node used by the next finite matrix. -/
def ScheduleValid (lower upper : ℕ) (schedule : ℕ → ℕ) (width : ℕ) : Prop :=
  ∀ r, r < width → ∀ bit,
    Partial lower upper (selectedChild schedule r bit) (2 ^ r) →
      schedule r = selectedChild schedule r bit

/-- Finite Option(Fin) contraction equals the verified tree traversal whenever
the current node is genuinely partial. There is no assumed source/core equality. -/
theorem injectionContract_boundary (k : ℕ) (origin step : ℝ) (lower upper : ℕ)
    (schedule : ℕ → ℕ) (bits : List Bool)
    (hnext : ScheduleValid lower upper schedule bits.length)
    (hp : Partial lower upper (schedule bits.length) (2 ^ bits.length)) :
    injectionContract k origin step lower upper schedule bits none =
      boundaryReadout k origin step lower upper (schedule bits.length) bits := by
  induction bits with
  | nil => exact False.elim (not_partial_unit lower upper (schedule 0) hp)
  | cons bit bits ih =>
    have hs : ScheduleValid lower upper schedule bits.length := by
      intro r hr b hb
      exact hnext r (by simpa only [List.length_cons] using Nat.lt_succ_of_lt hr) b hb
    rw [injectionContract, Fintype.sum_option, boundaryReadout,
      if_neg hp.1, if_neg hp.2]
    simp only [injectionCore, injectionContract_shared]
    change (if Partial lower upper (selectedChild schedule bits.length bit)
        (2 ^ bits.length) then 1 else 0) *
          injectionContract k origin step lower upper schedule bits none +
        (∑ j : Fin (2 * k + 1 + 1),
          (if Full lower upper (selectedChild schedule bits.length bit)
            (2 ^ bits.length) then
              blockInjectionRow k origin step (selectedChild schedule bits.length bit)
                bits.length j else 0) * sharedContract (2 * k + 1) bits j) =
      boundaryReadout k origin step lower upper
        (selectedChild schedule bits.length bit) bits
    by_cases hf : Full lower upper (selectedChild schedule bits.length bit) (2 ^ bits.length)
    · have hnp : ¬ Partial lower upper (selectedChild schedule bits.length bit)
          (2 ^ bits.length) := fun h => h.1 hf
      simp only [if_neg hnp, zero_mul, zero_add, if_pos hf]
      rw [boundaryReadout.eq_def, if_pos hf]
      exact injectedFiniteReadout_eq_injectedReadout k origin step _ bits
    · by_cases ho : Outside lower upper (selectedChild schedule bits.length bit) (2 ^ bits.length)
      · have hnp : ¬ Partial lower upper (selectedChild schedule bits.length bit)
            (2 ^ bits.length) := fun h => h.2 ho
        simp only [if_neg hnp, if_neg hf, zero_mul, Finset.sum_const_zero, add_zero]
        rw [boundaryReadout.eq_def, if_neg hf, if_pos ho]
      · have hpc : Partial lower upper (selectedChild schedule bits.length bit)
            (2 ^ bits.length) := ⟨hf, ho⟩
        simp only [if_pos hpc, if_neg hf, one_mul, zero_mul, Finset.sum_const_zero, add_zero]
        have he := hnext bits.length (by simp) bit hpc
        have hp' : Partial lower upper (schedule bits.length) (2 ^ bits.length) := by
          rw [he]
          exact hpc
        rw [ih hs hp', he]

/-- Closed-form boundary schedule, computed by a single integer quotient per level. -/
def boundarySchedule (lower r : ℕ) : ℕ := 2 ^ r * (lower / 2 ^ r)

theorem boundarySchedule_child (lower r : ℕ) (bit : Bool) :
    selectedChild (boundarySchedule lower) r bit =
      2 ^ r * (2 * (lower / 2 ^ (r + 1)) + if bit then 1 else 0) := by
  cases bit <;> simp [selectedChild, boundarySchedule, pow_succ] <;> ring

/-- The upper-half interval makes the quotient schedule valid at every level. -/
theorem boundarySchedule_valid (lower n : ℕ) :
    ScheduleValid lower (2 ^ n) (boundarySchedule lower) (n + 1) := by
  intro r hr bit hp
  have hrn : r ≤ n := by omega
  have he : 2 ^ n = 2 ^ r * 2 ^ (n - r) := by
    rw [← pow_add, Nat.add_sub_of_le hrn]
  rw [he, boundarySchedule_child] at hp
  have hx := partial_prefix_eq lower (2 ^ r) (2 ^ (n - r))
    (2 * (lower / 2 ^ (r + 1)) + if bit then 1 else 0) (by positivity) hp
  rw [boundarySchedule_child, hx]
  rfl

theorem boundarySchedule_root (lower n : ℕ) (hl : lower ≤ 2 ^ n) :
    boundarySchedule lower (n + 1) = 0 := by
  have hpos : 0 < 2 ^ n := by positivity
  have hlt : lower < 2 ^ (n + 1) := by rw [pow_succ]; omega
  simp [boundarySchedule, Nat.div_eq_of_lt hlt]

theorem middle_root_partial (lower n : ℕ) (hl : lower < 2 ^ n) :
    Partial lower (2 ^ n) 0 (2 ^ (n + 1)) := by
  refine ⟨middle_root_not_full lower n, ?_⟩
  have hpos : 0 < 2 ^ n := by positivity
  simp only [Outside, zero_add, pow_succ]
  omega

/-- A prefix interval `[0,upper)` has one unresolved aligned block as well. -/
theorem partial_left_prefix_eq (upper M x : ℕ) (hM : 0 < M)
    (hp : Partial 0 upper (M * x) M) : x = upper / M := by
  have hfirst : M * x < upper := by
    have := hp.2
    simp only [Outside] at this
    omega
  have hlast : upper < M * x + M := by
    have := hp.1
    simp only [Full, Nat.zero_le, true_and] at this
    omega
  have hd := Nat.div_add_mod upper M
  have hm := Nat.mod_lt upper hM
  by_contra he
  rcases lt_or_gt_of_ne he with h | h
  · have hh := Nat.mul_le_mul_left M (show x + 1 ≤ upper / M by omega)
    simp only [Nat.mul_add, Nat.mul_one] at hh
    omega
  · have hh := Nat.mul_le_mul_left M (show upper / M + 1 ≤ x by omega)
    simp only [Nat.mul_add, Nat.mul_one] at hh
    omega

theorem boundarySchedule_left_valid (upper width : ℕ) :
    ScheduleValid 0 upper (boundarySchedule upper) width := by
  intro r _ bit hp
  rw [boundarySchedule_child] at hp
  have hx := partial_left_prefix_eq upper (2 ^ r)
    (2 * (upper / 2 ^ (r + 1)) + if bit then 1 else 0) (by positivity) hp
  rw [boundarySchedule_child, hx]
  rfl

/-- A scalar free branch needs only the boundary state and one shared state. -/
abbrev ScalarBond := Option Unit

def scalarFreeContract (free : ℕ → Bool → ℝ) : List Bool → ℝ
  | [] => 1
  | bit :: bits => free bits.length bit * scalarFreeContract free bits

def scalarCore (lower upper : ℕ) (schedule : ℕ → ℕ)
    (inject : ℕ → ℕ → ℝ) (free : ℕ → Bool → ℝ) (r : ℕ) (bit : Bool) :
    _root_.Matrix ScalarBond ScalarBond ℝ
  | none, none => if Partial lower upper (selectedChild schedule r bit) (2 ^ r) then 1 else 0
  | none, some _ => if Full lower upper (selectedChild schedule r bit) (2 ^ r) then
      inject (selectedChild schedule r bit) r else 0
  | some _, none => 0
  | some _, some _ => free r bit

def scalarContract (lower upper : ℕ) (schedule : ℕ → ℕ)
    (inject : ℕ → ℕ → ℝ) (free : ℕ → Bool → ℝ) : List Bool → ScalarBond → ℝ
  | [], none => 0
  | [], some _ => 1
  | bit :: bits, i => ∑ j : ScalarBond,
      scalarCore lower upper schedule inject free bits.length bit i j *
        scalarContract lower upper schedule inject free bits j

theorem scalarContract_shared (lower upper : ℕ) (schedule : ℕ → ℕ)
    (inject : ℕ → ℕ → ℝ) (free : ℕ → Bool → ℝ) (bits : List Bool) :
    scalarContract lower upper schedule inject free bits (some ()) =
      scalarFreeContract free bits := by
  induction bits with
  | nil => rfl
  | cons bit bits ih =>
    simp [scalarContract, Fintype.sum_option, scalarCore, ih, scalarFreeContract]

def scalarBoundaryReadout (lower upper : ℕ) (inject : ℕ → ℕ → ℝ)
    (free : ℕ → Bool → ℝ) (first : ℕ) (bits : List Bool) : ℝ :=
  if Full lower upper first (2 ^ bits.length) then
    inject first bits.length * scalarFreeContract free bits
  else if Outside lower upper first (2 ^ bits.length) then 0
  else match bits with
    | [] => 0
    | bit :: rest => scalarBoundaryReadout lower upper inject free
        (first + if bit then 2 ^ rest.length else 0) rest
termination_by bits.length

/-- A generic scalar source bridge, consumed below with a proved exponential
suffix identity. `hinject` is local injection algebra, not a target/TT contract. -/
theorem scalarBoundaryReadout_eq (lower upper : ℕ) (inject : ℕ → ℕ → ℝ)
    (free : ℕ → Bool → ℝ) (target : ℕ → ℝ)
    (hinject : ∀ first bits, inject first bits.length * scalarFreeContract free bits =
      target (first + wordValue bits)) (first : ℕ) (bits : List Bool) :
    scalarBoundaryReadout lower upper inject free first bits =
      if lower ≤ first + wordValue bits ∧ first + wordValue bits < upper then
        target (first + wordValue bits) else 0 := by
  induction bits generalizing first with
  | nil =>
    rw [scalarBoundaryReadout]
    by_cases hf : Full lower upper first 1
    · simp only [List.length_nil, pow_zero, if_pos hf]
      have hm : lower ≤ first + wordValue [] ∧ first + wordValue [] < upper := by
        obtain ⟨hl, hu⟩ := hf
        simp only [wordValue]
        omega
      rw [if_pos hm]
      exact hinject first []
    · simp only [List.length_nil, pow_zero, if_neg hf]
      have hn : ¬(lower ≤ first + wordValue [] ∧ first + wordValue [] < upper) := by
        simp only [Full] at hf
        simp only [wordValue]
        omega
      simp [hn]
  | cons bit bits ih =>
    rw [scalarBoundaryReadout]
    by_cases hf : Full lower upper first (2 ^ (bit :: bits).length)
    · rw [if_pos hf, hinject]
      have hw := wordValue_lt (bit :: bits)
      have hm : lower ≤ first + wordValue (bit :: bits) ∧
          first + wordValue (bit :: bits) < upper := by
        obtain ⟨hl, hu⟩ := hf
        omega
      rw [if_pos hm]
    · rw [if_neg hf]
      by_cases ho : Outside lower upper first (2 ^ (bit :: bits).length)
      · rw [if_pos ho]
        have hw := wordValue_lt (bit :: bits)
        have hn : ¬(lower ≤ first + wordValue (bit :: bits) ∧
            first + wordValue (bit :: bits) < upper) := by
          rcases ho with ho | ho <;> omega
        rw [if_neg hn]
      · rw [if_neg ho, ih]
        simp only [wordValue, Nat.add_assoc] <;> rfl

theorem scalarContract_boundary (lower upper : ℕ) (schedule : ℕ → ℕ)
    (inject : ℕ → ℕ → ℝ) (free : ℕ → Bool → ℝ) (bits : List Bool)
    (hnext : ScheduleValid lower upper schedule bits.length)
    (hp : Partial lower upper (schedule bits.length) (2 ^ bits.length)) :
    scalarContract lower upper schedule inject free bits none =
      scalarBoundaryReadout lower upper inject free (schedule bits.length) bits := by
  induction bits with
  | nil => exact False.elim (not_partial_unit lower upper (schedule 0) hp)
  | cons bit bits ih =>
    have hs : ScheduleValid lower upper schedule bits.length := by
      intro r hr b hb
      exact hnext r (by simpa only [List.length_cons] using Nat.lt_succ_of_lt hr) b hb
    rw [scalarContract, Fintype.sum_option, scalarBoundaryReadout,
      if_neg hp.1, if_neg hp.2]
    simp only [Fintype.sum_unique, scalarCore]
    rw [show (default : Unit) = () from rfl, scalarContract_shared]
    change (if Partial lower upper (selectedChild schedule bits.length bit)
        (2 ^ bits.length) then 1 else 0) *
          scalarContract lower upper schedule inject free bits none +
        (if Full lower upper (selectedChild schedule bits.length bit) (2 ^ bits.length)
          then inject (selectedChild schedule bits.length bit) bits.length else 0) *
            scalarFreeContract free bits =
      scalarBoundaryReadout lower upper inject free
        (selectedChild schedule bits.length bit) bits
    by_cases hf : Full lower upper (selectedChild schedule bits.length bit) (2 ^ bits.length)
    · have hn : ¬ Partial lower upper (selectedChild schedule bits.length bit)
          (2 ^ bits.length) := fun h => h.1 hf
      simp only [if_neg hn, zero_mul, zero_add, if_pos hf]
      rw [scalarBoundaryReadout.eq_def, if_pos hf]
    · by_cases ho : Outside lower upper (selectedChild schedule bits.length bit) (2 ^ bits.length)
      · have hn : ¬ Partial lower upper (selectedChild schedule bits.length bit)
            (2 ^ bits.length) := fun h => h.2 ho
        simp only [if_neg hn, if_neg hf, zero_mul, add_zero]
        rw [scalarBoundaryReadout.eq_def, if_neg hf, if_pos ho]
      · have hc : Partial lower upper (selectedChild schedule bits.length bit)
            (2 ^ bits.length) := ⟨hf, ho⟩
        simp only [if_pos hc, if_neg hf, one_mul, zero_mul, add_zero]
        have he := hnext bits.length (by simp) bit hc
        have hp' : Partial lower upper (schedule bits.length) (2 ^ bits.length) := by
          rw [he]
          exact hc
        rw [ih hs hp', he]

/-- Stable left-tail factors use only nonpositive exponential arguments for
positive step. The one digit contributes no factor. -/
def leftFree (step : ℝ) (r : ℕ) (bit : Bool) : ℝ :=
  if bit then 1 else Real.exp (-step * 2 ^ r)

def leftInject (origin step : ℝ) (first r : ℕ) : ℝ :=
  Real.exp (affinePoint origin step first + step * (2 ^ r - 1))

theorem leftFreeContract_eq (step : ℝ) (bits : List Bool) :
    scalarFreeContract (leftFree step) bits =
      Real.exp (-step * (2 ^ bits.length - 1 - (wordValue bits : ℝ))) := by
  induction bits with
  | nil => simp [scalarFreeContract, wordValue]
  | cons bit bits ih =>
    cases bit <;> simp only [scalarFreeContract, leftFree, Bool.false_eq_true,
      if_false, if_true, one_mul, wordValue, List.length_cons, Nat.cast_add,
      Nat.cast_pow, Nat.cast_ofNat, zero_add, pow_succ, ih]
    · rw [← Real.exp_add]
      congr 1
      ring
    · congr 1
      ring

theorem leftInject_readout (origin step : ℝ) (first : ℕ) (bits : List Bool) :
    leftInject origin step first bits.length * scalarFreeContract (leftFree step) bits =
      Real.exp (affinePoint origin step (first + wordValue bits)) := by
  rw [leftFreeContract_eq]
  unfold leftInject
  rw [← Real.exp_add]
  congr 1
  simp only [affinePoint, Nat.cast_add]
  ring

/-- Exact correspondence with the prototype's last included block index. -/
theorem leftInject_eq_last (origin step : ℝ) (first r : ℕ) :
    leftInject origin step first r =
      Real.exp (affinePoint origin step (first + 2 ^ r - 1)) := by
  have hp : 0 < 2 ^ r := by positivity
  have he : 1 ≤ first + 2 ^ r := by omega
  unfold leftInject affinePoint
  congr 1
  rw [Nat.cast_sub he]
  push_cast
  ring

theorem leftFree_bounds (step : ℝ) (hs : 0 ≤ step) (r : ℕ) (bit : Bool) :
    0 ≤ leftFree step r bit ∧ leftFree step r bit ≤ 1 := by
  cases bit
  · simp only [leftFree, Bool.false_eq_true, if_false]
    refine ⟨(Real.exp_pos _).le, Real.exp_le_one_iff.mpr ?_⟩
    have hp : 0 ≤ (2 : ℝ) ^ r := by positivity
    nlinarith
  · norm_num [leftFree]

/-- The exact grid step on `n+1` qubits; `n` may be zero. -/
def gridStep (n : ℕ) (L : ℝ) : ℝ :=
  2 * Real.pi * L / (gridSize (n + 1) : ℝ)

def gridPointNat (n : ℕ) (L : ℝ) (j : ℕ) : ℝ :=
  affinePoint (-Real.pi * L) (gridStep n L) j

theorem gridStep_pos (n : ℕ) (L : ℝ) (hL : 0 < L) : 0 < gridStep n L := by
  unfold gridStep gridSize
  positivity

theorem gridPointNat_eq_gridPoint (n : ℕ) (L : ℝ) (j : Fin (gridSize (n + 1))) :
    gridPointNat n L j = HermiteStatePreparation.gridPoint (n + 1) L j := by
  simp only [gridPointNat, affinePoint, gridStep, HermiteStatePreparation.gridPoint,
    mul_comm]

theorem gridPointNat_midpoint (n : ℕ) (L : ℝ) :
    gridPointNat n L (2 ^ n) = 0 := by
  simp only [gridPointNat, affinePoint, gridStep, gridSize, Nat.cast_pow,
    Nat.cast_ofNat, pow_succ]
  push_cast
  field_simp
  ring

theorem gridPointNat_strictMono (n : ℕ) (L : ℝ) (hL : 0 < L) :
    StrictMono (gridPointNat n L) := by
  intro i j hij
  have hcast : (i : ℝ) < j := by exact_mod_cast hij
  have hs := gridStep_pos n L hL
  simp only [gridPointNat, affinePoint]
  nlinarith

theorem gridPointNat_lt_zero_iff (n : ℕ) (L : ℝ) (hL : 0 < L) (j : ℕ) :
    gridPointNat n L j < 0 ↔ j < 2 ^ n := by
  rw [← gridPointNat_midpoint n L]
  exact (gridPointNat_strictMono n L hL).lt_iff_lt

/-- Natural ceiling implements the lower clamp at zero. The upper clamp is
redundant for positive `L`, as `cutIndex_le_midpoint` proves. -/
def cutIndex (n : ℕ) (L : ℝ) : ℕ :=
  Nat.ceil ((-1 - (-Real.pi * L)) / gridStep n L)

theorem gridPointNat_lt_neg_one_iff (n : ℕ) (L : ℝ) (hL : 0 < L) (j : ℕ) :
    gridPointNat n L j < -1 ↔ j < cutIndex n L :=
  HermiteCutRank.affine_lt_cut (-Real.pi * L) (gridStep n L) (-1)
    (gridStep_pos n L hL) j

theorem cutIndex_le_midpoint (n : ℕ) (L : ℝ) (hL : 0 < L) :
    cutIndex n L ≤ 2 ^ n := by
  by_contra hn
  have h := (gridPointNat_lt_neg_one_iff n L hL (2 ^ n)).mpr (by omega)
  rw [gridPointNat_midpoint] at h
  norm_num at h

/-- This is the candidate's exact clamped ceiling, before any rounding of pi. -/
theorem cutIndex_eq_clamped (n : ℕ) (L : ℝ) (hL : 0 < L) :
    cutIndex n L = min
      (Nat.ceil ((2 ^ n : ℕ) - (gridSize (n + 1) : ℝ) / (2 * Real.pi * L)))
      (2 ^ n) := by
  have he : (-1 - (-Real.pi * L)) / gridStep n L =
      (2 ^ n : ℕ) - (gridSize (n + 1) : ℝ) / (2 * Real.pi * L) := by
    have hpi := Real.pi_ne_zero
    have hLn : L ≠ 0 := ne_of_gt hL
    simp only [gridStep, gridSize, Nat.cast_pow, Nat.cast_ofNat, pow_succ]
    push_cast
    field_simp
    ring
  rw [← he, ← cutIndex]
  exact (min_eq_left (cutIndex_le_midpoint n L hL)).symm

theorem middle_membership_iff (n : ℕ) (L : ℝ) (hL : 0 < L) (j : ℕ) :
    (cutIndex n L ≤ j ∧ j < 2 ^ n) ↔
      (-1 ≤ gridPointNat n L j ∧ gridPointNat n L j < 0) := by
  have ha := gridPointNat_lt_neg_one_iff n L hL j
  have hb := gridPointNat_lt_zero_iff n L hL j
  constructor
  · rintro ⟨ha', hb'⟩
    exact ⟨by by_contra hn; have := ha.mp (by linarith); omega, hb.mpr hb'⟩
  · rintro ⟨ha', hb'⟩
    exact ⟨by by_contra hn; have := ha.mpr (by omega); linarith, hb.mp hb'⟩

/-- Every actual injected dyadic block has valid de Casteljau parameters,
including a block whose excluded endpoint is the zero-coordinate midpoint. -/
theorem injection_domain (n : ℕ) (L : ℝ) (hL : 0 < L) (first size : ℕ)
    (hs : 0 < size) (hf : Full (cutIndex n L) (2 ^ n) first size) :
    0 ≤ 1 + gridPointNat n L first ∧
      1 + gridPointNat n L first < 1 + gridPointNat n L (first + size) ∧
      1 + gridPointNat n L (first + size) ≤ 1 := by
  obtain ⟨hl, hu⟩ := hf
  have hm := (middle_membership_iff n L hL first).mp ⟨hl, by omega⟩
  have hlt := gridPointNat_strictMono n L hL (show first < first + size by omega)
  have hle := (gridPointNat_strictMono n L hL).monotone hu
  rw [gridPointNat_midpoint] at hle
  exact ⟨by linarith, by linarith, by linarith⟩

/-- The middle component uses the same one-boundary traversal as the prototype. -/
def middleReadout (k n : ℕ) (L : ℝ) (bits : List Bool) : ℝ :=
  boundaryReadout k (-Real.pi * L) (gridStep n L) (cutIndex n L) (2 ^ n) 0 bits

theorem middleReadout_eq (k n : ℕ) (L : ℝ) (hL : 0 < L) (bits : List Bool) :
    middleReadout k n L bits =
      if -1 ≤ gridPointNat n L (wordValue bits) ∧
          gridPointNat n L (wordValue bits) < 0 then
        (HermitePolynomial.sourceInterpolant k).eval
          (gridPointNat n L (wordValue bits)) else 0 := by
  unfold middleReadout
  rw [boundaryReadout_eq]
  · simp only [zero_add, middle_membership_iff n L hL, gridPointNat] <;> rfl
  · intro j _ hj
    exact ne_of_lt ((gridPointNat_lt_zero_iff n L hL j).mpr hj)

/-- A cutoff at the midpoint gives the prototype's zero middle component. -/
theorem middleReadout_empty (k n : ℕ) (L : ℝ) (hL : 0 < L)
    (hcut : cutIndex n L = 2 ^ n) (bits : List Bool) :
    middleReadout k n L bits = 0 := by
  rw [middleReadout_eq k n L hL]
  have hm := middle_membership_iff n L hL (wordValue bits)
  rw [hcut] at hm
  have hn : ¬(-1 ≤ gridPointNat n L (wordValue bits) ∧
      gridPointNat n L (wordValue bits) < 0) := by
    intro h
    obtain ⟨ha, hb⟩ := hm.mpr h
    omega
  exact if_neg hn

/-- Word-to-public-grid adapter, with explicit width equality. -/
def wordSampleIndex (n : ℕ) (bits : List Bool) (hbits : bits.length = n + 1) :
    Fin (gridSize (n + 1)) :=
  ⟨wordValue bits, by simpa only [gridSize, ← hbits] using wordValue_lt bits⟩

private theorem sampledAmplitude_word (k n : ℕ) (L : ℝ)
    (bits : List Bool) (hbits : bits.length = n + 1) :
    HermiteStatePreparation.sampledAmplitude k (n + 1) L
      (wordSampleIndex n bits hbits) =
      HermitePolynomial.smoothInitial k (gridPointNat n L (wordValue bits)) := by
  unfold HermiteStatePreparation.sampledAmplitude
  rw [← gridPointNat_eq_gridPoint]
  rfl

/-- All-bit exact source readout on the actual public sample API. The center
belongs to the right tail, while the sample at `p=-1` belongs to this component. -/
theorem middleReadout_eq_masked_sample (k n : ℕ) (L : ℝ) (hL : 0 < L)
    (bits : List Bool) (hbits : bits.length = n + 1) :
    middleReadout k n L bits =
      if cutIndex n L ≤ wordValue bits ∧ wordValue bits < 2 ^ n then
        HermiteStatePreparation.sampledAmplitude k (n + 1) L
          (wordSampleIndex n bits hbits) else 0 := by
  rw [middleReadout_eq k n L hL]
  simp only [← middle_membership_iff n L hL]
  by_cases hm : cutIndex n L ≤ wordValue bits ∧ wordValue bits < 2 ^ n
  · rw [if_pos hm, if_pos hm]
    have hc := (middle_membership_iff n L hL _).mp hm
    rw [sampledAmplitude_word, HermiteCutRank.smoothInitial_strict]
    rw [if_neg (by linarith : ¬ gridPointNat n L (wordValue bits) < -1), if_pos hc.2]
  · rw [if_neg hm, if_neg hm]

/-- The exact finite middle TT, including the prototype's empty-interval fast
path. Its boundary schedule and all source rows are formula-derived. -/
def middleFiniteReadout (k n : ℕ) (L : ℝ) (bits : List Bool) : ℝ :=
  if cutIndex n L = 2 ^ n then 0 else
    injectionContract k (-Real.pi * L) (gridStep n L) (cutIndex n L) (2 ^ n)
      (boundarySchedule (cutIndex n L)) bits none

/-- Source-derived one-boundary finite TT equals the verified interval traversal. -/
theorem middleFiniteReadout_eq_middleReadout (k n : ℕ) (L : ℝ) (hL : 0 < L)
    (bits : List Bool) (hbits : bits.length = n + 1) :
    middleFiniteReadout k n L bits = middleReadout k n L bits := by
  unfold middleFiniteReadout
  by_cases he : cutIndex n L = 2 ^ n
  · rw [if_pos he, middleReadout_empty k n L hL he]
  · rw [if_neg he]
    have hl := cutIndex_le_midpoint n L hL
    have hlt : cutIndex n L < 2 ^ n := by omega
    have hn : ScheduleValid (cutIndex n L) (2 ^ n)
        (boundarySchedule (cutIndex n L)) bits.length := by
      rw [hbits]
      exact boundarySchedule_valid (cutIndex n L) n
    have hp : Partial (cutIndex n L) (2 ^ n)
        (boundarySchedule (cutIndex n L) bits.length) (2 ^ bits.length) := by
      rw [hbits, boundarySchedule_root _ _ hl]
      exact middle_root_partial _ _ hlt
    rw [injectionContract_boundary _ _ _ _ _ _ _ hn hp,
      hbits, boundarySchedule_root _ _ hl]
    rfl

/-- Complete all-bit, actual-grid semantics of the finite middle TT. Its fixed
bond is `InjectionBond k`, of cardinality `2*k+3`, at every interior level. -/
theorem middleFiniteReadout_eq_masked_sample (k n : ℕ) (L : ℝ) (hL : 0 < L)
    (bits : List Bool) (hbits : bits.length = n + 1) :
    middleFiniteReadout k n L bits =
      if cutIndex n L ≤ wordValue bits ∧ wordValue bits < 2 ^ n then
        HermiteStatePreparation.sampledAmplitude k (n + 1) L
          (wordSampleIndex n bits hbits) else 0 := by
  rw [middleFiniteReadout_eq_middleReadout k n L hL bits hbits]
  exact middleReadout_eq_masked_sample k n L hL bits hbits

def leftFiniteReadout (n : ℕ) (L : ℝ) (bits : List Bool) : ℝ :=
  if cutIndex n L = 0 then 0 else
    scalarContract 0 (cutIndex n L) (boundarySchedule (cutIndex n L))
      (leftInject (-Real.pi * L) (gridStep n L)) (leftFree (gridStep n L)) bits none

theorem leftFiniteReadout_eq (n : ℕ) (L : ℝ) (hL : 0 < L)
    (bits : List Bool) (hbits : bits.length = n + 1) :
    leftFiniteReadout n L bits = if wordValue bits < cutIndex n L then
      Real.exp (gridPointNat n L (wordValue bits)) else 0 := by
  unfold leftFiniteReadout
  by_cases he : cutIndex n L = 0
  · simp [he]
  · rw [if_neg he]
    have hl := cutIndex_le_midpoint n L hL
    have hpos : 0 < 2 ^ n := by positivity
    have hc : 0 < cutIndex n L := by omega
    have hn := boundarySchedule_left_valid (cutIndex n L) bits.length
    have hp : Partial 0 (cutIndex n L) (boundarySchedule (cutIndex n L) bits.length)
        (2 ^ bits.length) := by
      rw [hbits, boundarySchedule_root _ _ hl]
      simp only [Partial, Full, Outside, Nat.zero_le, true_and, zero_add, pow_succ]
      omega
    rw [scalarContract_boundary _ _ _ _ _ _ hn hp,
      scalarBoundaryReadout_eq _ _ _ _
        (fun j => Real.exp (affinePoint (-Real.pi * L) (gridStep n L) j))
        (leftInject_readout (-Real.pi * L) (gridStep n L)),
      hbits, boundarySchedule_root _ _ hl]
    simp only [zero_add, Nat.zero_le, true_and, gridPointNat]

theorem leftInject_bounds (n : ℕ) (L : ℝ) (hL : 0 < L) (first r : ℕ)
    (hf : Full 0 (cutIndex n L) first (2 ^ r)) :
    0 ≤ leftInject (-Real.pi * L) (gridStep n L) first r ∧
      leftInject (-Real.pi * L) (gridStep n L) first r ≤ 1 := by
  rw [leftInject_eq_last]
  have hp : 0 < 2 ^ r := by positivity
  have hj : first + 2 ^ r - 1 < cutIndex n L := by
    have := hf.2
    omega
  have hg := (gridPointNat_lt_neg_one_iff n L hL _).mpr hj
  exact ⟨(Real.exp_pos _).le, Real.exp_le_one_iff.mpr (by
    change gridPointNat n L _ ≤ 0
    linarith)⟩

theorem leftFiniteReadout_eq_masked_sample (k n : ℕ) (L : ℝ) (hL : 0 < L)
    (bits : List Bool) (hbits : bits.length = n + 1) :
    leftFiniteReadout n L bits = if wordValue bits < cutIndex n L then
      HermiteStatePreparation.sampledAmplitude k (n + 1) L
        (wordSampleIndex n bits hbits) else 0 := by
  rw [leftFiniteReadout_eq n L hL bits hbits]
  by_cases hj : wordValue bits < cutIndex n L
  · rw [if_pos hj, if_pos hj]
    rw [sampledAmplitude_word, HermiteCutRank.smoothInitial_strict]
    rw [if_pos ((gridPointNat_lt_neg_one_iff n L hL _).mpr hj)]
  · rw [if_neg hj, if_neg hj]

def rightFree (step : ℝ) (r : ℕ) (bit : Bool) : ℝ :=
  if bit then Real.exp (-step * 2 ^ r) else 1

theorem rightFree_bounds (step : ℝ) (hs : 0 ≤ step) (r : ℕ) (bit : Bool) :
    0 ≤ rightFree step r bit ∧ rightFree step r bit ≤ 1 := by
  cases bit
  · norm_num [rightFree]
  · exact leftFree_bounds step hs r false

theorem rightFreeContract_eq (step : ℝ) (bits : List Bool) :
    scalarFreeContract (rightFree step) bits =
      Real.exp (-step * (wordValue bits : ℝ)) := by
  induction bits with
  | nil => simp [scalarFreeContract, wordValue]
  | cons bit bits ih =>
    cases bit <;> simp only [scalarFreeContract, rightFree, Bool.false_eq_true,
      if_false, if_true, one_mul, wordValue, Nat.cast_add, Nat.cast_pow,
      Nat.cast_ofNat, zero_add, ih]
    rw [← Real.exp_add]
    congr 1
    ring

/-- Rank-one right component: the first MSB selects the right half; subsequent
bits use bounded negative exponential factors. -/
def rightCore (n : ℕ) (step : ℝ) (r : ℕ) (bit : Bool) : ℝ :=
  if r = n then (if bit then 1 else 0) else rightFree step r bit

theorem rightCore_suffix (n : ℕ) (step : ℝ) (bits : List Bool)
    (hlen : bits.length ≤ n) :
    scalarFreeContract (rightCore n step) bits =
      scalarFreeContract (rightFree step) bits := by
  induction bits with
  | nil => rfl
  | cons bit bits ih =>
    have hr : bits.length ≠ n := by simp only [List.length_cons] at hlen; omega
    have hs : bits.length ≤ n := by simp only [List.length_cons] at hlen; omega
    simp only [scalarFreeContract, rightCore, if_neg hr, ih hs]

def rightFiniteReadout (n : ℕ) (L : ℝ) (bits : List Bool) : ℝ :=
  scalarFreeContract (rightCore n (gridStep n L)) bits

theorem rightFiniteReadout_eq (n : ℕ) (L : ℝ) (bits : List Bool)
    (hbits : bits.length = n + 1) :
    rightFiniteReadout n L bits = if wordValue bits < 2 ^ n then 0 else
      Real.exp (-gridPointNat n L (wordValue bits)) := by
  cases bits with
  | nil => simp at hbits
  | cons bit bits =>
    have hs : bits.length = n := by simpa using hbits
    unfold rightFiniteReadout
    rw [scalarFreeContract]
    simp only [rightCore, hs]
    rw [rightCore_suffix n _ bits (by omega), rightFreeContract_eq]
    have hw : wordValue bits < 2 ^ n := by simpa only [hs] using wordValue_lt bits
    cases bit
    · simp [wordValue, hw]
    · simp only [if_true, one_mul, wordValue, hs]
      rw [if_neg (by omega : ¬ 2 ^ n + wordValue bits < 2 ^ n)]
      congr 1
      have hm := gridPointNat_midpoint n L
      simp only [gridPointNat, affinePoint, Nat.cast_add] at hm ⊢
      linarith

theorem rightFiniteReadout_eq_masked_sample (k n : ℕ) (L : ℝ) (hL : 0 < L)
    (bits : List Bool) (hbits : bits.length = n + 1) :
    rightFiniteReadout n L bits = if wordValue bits < 2 ^ n then 0 else
      HermiteStatePreparation.sampledAmplitude k (n + 1) L
        (wordSampleIndex n bits hbits) := by
  rw [rightFiniteReadout_eq n L bits hbits]
  by_cases hj : wordValue bits < 2 ^ n
  · rw [if_pos hj, if_pos hj]
  · rw [if_neg hj, if_neg hj]
    have hp : ¬ gridPointNat n L (wordValue bits) < 0 := by
      intro hh
      exact hj ((gridPointNat_lt_zero_iff n L hL _).mp hh)
    rw [sampledAmplitude_word, HermiteCutRank.smoothInitial_strict]
    rw [if_neg (by linarith : ¬ gridPointNat n L (wordValue bits) < -1), if_neg hp]

/-- Exact three-component source action. No cancellation between masked
polynomials or out-of-domain exponential evaluations appears in the construction. -/
theorem threeBranchReadout_eq_sample (k n : ℕ) (L : ℝ) (hL : 0 < L)
    (bits : List Bool) (hbits : bits.length = n + 1) :
    leftFiniteReadout n L bits + middleFiniteReadout k n L bits +
      rightFiniteReadout n L bits =
        HermiteStatePreparation.sampledAmplitude k (n + 1) L
          (wordSampleIndex n bits hbits) := by
  rw [leftFiniteReadout_eq_masked_sample k n L hL bits hbits,
    middleFiniteReadout_eq_masked_sample k n L hL bits hbits,
    rightFiniteReadout_eq_masked_sample k n L hL bits hbits]
  have hc := cutIndex_le_midpoint n L hL
  by_cases hl : wordValue bits < cutIndex n L
  · have hm : wordValue bits < 2 ^ n := by omega
    simp [hl, hm, show ¬ cutIndex n L ≤ wordValue bits by omega]
  · by_cases hm : wordValue bits < 2 ^ n
    · simp [hl, hm, show cutIndex n L ≤ wordValue bits by omega]
    · simp [hl, hm]

/-- A common fixed-bond kernel interface. The natural level counts unconsumed
digits after the current digit; its stage-`t` value is `n-t` on `n+1` qubits. -/
abbrev Kernel (B : Type*) := ℕ → Bool → _root_.Matrix B B ℝ

def kernelContract {B : Type*} [Fintype B] (K : Kernel B) (right : B → ℝ) :
    List Bool → B → ℝ
  | [], i => right i
  | bit :: bits, i => ∑ j : B, K bits.length bit i j * kernelContract K right bits j

def kernelAmplitude {B : Type*} [Fintype B] (K : Kernel B) (left right : B → ℝ)
    (bits : List Bool) : ℝ := ∑ i : B, left i * kernelContract K right bits i

def sumKernel {B C : Type*} (K : Kernel B) (H : Kernel C) : Kernel (Sum B C) :=
  fun r bit i j => match i, j with
    | .inl a, .inl b => K r bit a b
    | .inr a, .inr b => H r bit a b
    | _, _ => 0

theorem kernelContract_sum_inl {B C : Type*} [Fintype B] [Fintype C]
    (K : Kernel B) (H : Kernel C) (right : B → ℝ) (last : C → ℝ)
    (bits : List Bool) (i : B) :
    kernelContract (sumKernel K H) (Sum.elim right last) bits (.inl i) =
      kernelContract K right bits i := by
  induction bits generalizing i with
  | nil => rfl
  | cons bit bits ih =>
    simp only [kernelContract, Fintype.sum_sum_type, sumKernel, zero_mul,
      Finset.sum_const_zero, add_zero, ih]

theorem kernelContract_sum_inr {B C : Type*} [Fintype B] [Fintype C]
    (K : Kernel B) (H : Kernel C) (right : B → ℝ) (last : C → ℝ)
    (bits : List Bool) (i : C) :
    kernelContract (sumKernel K H) (Sum.elim right last) bits (.inr i) =
      kernelContract H last bits i := by
  induction bits generalizing i with
  | nil => rfl
  | cons bit bits ih =>
    simp only [kernelContract, Fintype.sum_sum_type, sumKernel, zero_mul,
      Finset.sum_const_zero, zero_add, ih]

theorem kernelAmplitude_sum {B C : Type*} [Fintype B] [Fintype C]
    (K : Kernel B) (H : Kernel C) (left right : B → ℝ) (first last : C → ℝ)
    (bits : List Bool) :
    kernelAmplitude (sumKernel K H) (Sum.elim left first) (Sum.elim right last) bits =
      kernelAmplitude K left right bits + kernelAmplitude H first last bits := by
  simp only [kernelAmplitude, Fintype.sum_sum_type, Sum.elim_inl, Sum.elim_inr,
    kernelContract_sum_inl, kernelContract_sum_inr]

def injectionTerminal (k : ℕ) : InjectionBond k → ℝ
  | none => 0
  | some i => if i.val = 0 then 1 else 0

def scalarTerminal : ScalarBond → ℝ
  | none => 0
  | some _ => 1

theorem kernelContract_injection (k : ℕ) (origin step : ℝ) (lower upper : ℕ)
    (schedule : ℕ → ℕ) (bits : List Bool) (i : InjectionBond k) :
    kernelContract (injectionCore k origin step lower upper schedule)
      (injectionTerminal k) bits i =
        injectionContract k origin step lower upper schedule bits i := by
  induction bits generalizing i with
  | nil => cases i <;> rfl
  | cons bit bits ih => simp only [kernelContract, ih, injectionContract]

theorem kernelContract_scalar (lower upper : ℕ) (schedule : ℕ → ℕ)
    (inject : ℕ → ℕ → ℝ) (free : ℕ → Bool → ℝ) (bits : List Bool) (i : ScalarBond) :
    kernelContract (scalarCore lower upper schedule inject free) scalarTerminal bits i =
      scalarContract lower upper schedule inject free bits i := by
  induction bits generalizing i with
  | nil => cases i <;> rfl
  | cons bit bits ih => simp only [kernelContract, ih, scalarContract]

theorem kernelContract_unit (free : ℕ → Bool → ℝ) (bits : List Bool) (i : Unit) :
    kernelContract (fun r bit (_ _ : Unit) => free r bit) (fun _ => 1) bits i =
      scalarFreeContract free bits := by
  induction bits generalizing i with
  | nil => rfl
  | cons bit bits ih => simp only [kernelContract, Fintype.sum_unique, ih, scalarFreeContract]

def leftKernel (n : ℕ) (L : ℝ) : Kernel ScalarBond :=
  scalarCore 0 (cutIndex n L) (boundarySchedule (cutIndex n L))
    (leftInject (-Real.pi * L) (gridStep n L)) (leftFree (gridStep n L))

def middleKernel (k n : ℕ) (L : ℝ) : Kernel (InjectionBond k) :=
  injectionCore k (-Real.pi * L) (gridStep n L) (cutIndex n L) (2 ^ n)
    (boundarySchedule (cutIndex n L))

def rightKernel (n : ℕ) (L : ℝ) : Kernel Unit :=
  fun r bit _ _ => rightCore n (gridStep n L) r bit

def leftInitial (n : ℕ) (L : ℝ) : ScalarBond → ℝ
  | none => if cutIndex n L = 0 then 0 else 1
  | some _ => 0

def middleInitial (k n : ℕ) (L : ℝ) : InjectionBond k → ℝ
  | none => if cutIndex n L = 2 ^ n then 0 else 1
  | some _ => 0

theorem kernelAmplitude_left (n : ℕ) (L : ℝ) (bits : List Bool) :
    kernelAmplitude (leftKernel n L) (leftInitial n L) scalarTerminal bits =
      leftFiniteReadout n L bits := by
  simp only [kernelAmplitude, Fintype.sum_option, leftInitial, zero_mul,
    Finset.sum_const_zero, add_zero, leftKernel, kernelContract_scalar]
  by_cases he : cutIndex n L = 0 <;> simp [he, leftFiniteReadout]

theorem kernelAmplitude_middle (k n : ℕ) (L : ℝ) (bits : List Bool) :
    kernelAmplitude (middleKernel k n L) (middleInitial k n L) (injectionTerminal k) bits =
      middleFiniteReadout k n L bits := by
  simp only [kernelAmplitude, Fintype.sum_option, middleInitial, zero_mul,
    Finset.sum_const_zero, add_zero, middleKernel, kernelContract_injection]
  by_cases he : cutIndex n L = 2 ^ n <;> simp [he, middleFiniteReadout]

theorem kernelAmplitude_right (n : ℕ) (L : ℝ) (bits : List Bool) :
    kernelAmplitude (rightKernel n L) (fun _ => 1) (fun _ => 1) bits =
      rightFiniteReadout n L bits := by
  simp only [kernelAmplitude, Fintype.sum_unique, one_mul, rightFiniteReadout]
  exact kernelContract_unit (rightCore n (gridStep n L)) bits ()

/-- One fixed direct-sum bond, with no state allocated per dyadic prefix. -/
abbrev HermiteFiniteBond (k : ℕ) := Sum ScalarBond (Sum (InjectionBond k) Unit)

def hermiteKernel (k n : ℕ) (L : ℝ) : Kernel (HermiteFiniteBond k) :=
  sumKernel (leftKernel n L) (sumKernel (middleKernel k n L) (rightKernel n L))

def hermiteInitial (k n : ℕ) (L : ℝ) : HermiteFiniteBond k → ℝ :=
  Sum.elim (leftInitial n L) (Sum.elim (middleInitial k n L) (fun _ => 1))

def hermiteTerminal (k : ℕ) : HermiteFiniteBond k → ℝ :=
  Sum.elim scalarTerminal (Sum.elim (injectionTerminal k) (fun _ => 1))

/-- Main exact real-algebra root: one formula-derived fixed-width kernel family
and explicit left/right boundaries produce every literal Hermite sample. -/
theorem hermiteKernel_eq_sample (k n : ℕ) (L : ℝ) (hL : 0 < L)
    (bits : List Bool) (hbits : bits.length = n + 1) :
    kernelAmplitude (hermiteKernel k n L) (hermiteInitial k n L) (hermiteTerminal k) bits =
      HermiteStatePreparation.sampledAmplitude k (n + 1) L
        (wordSampleIndex n bits hbits) := by
  unfold hermiteKernel hermiteInitial hermiteTerminal
  rw [kernelAmplitude_sum, kernelAmplitude_sum, kernelAmplitude_left,
    kernelAmplitude_middle, kernelAmplitude_right, ← add_assoc]
  exact threeBranchReadout_eq_sample k n L hL bits hbits

theorem hermiteFiniteBond_card (k : ℕ) :
    Fintype.card (HermiteFiniteBond k) = 2 * k + 6 := by
  simp [HermiteFiniteBond, ScalarBond, InjectionBond]
  omega

/-- Address space of the actual two-slice cores on `n+1` qubits. Its size is
polynomial; this is a storage count, not a finite-bit arithmetic cost theorem. -/
abbrev HermiteCoreAddress (k n : ℕ) :=
  Fin (n + 1) × Bool × HermiteFiniteBond k × HermiteFiniteBond k

def hermiteCoreEntry (k n : ℕ) (L : ℝ) (a : HermiteCoreAddress k n) : ℝ :=
  hermiteKernel k n L (n - a.1.val) a.2.1 a.2.2.1 a.2.2.2

theorem hermiteCoreAddress_card (k n : ℕ) :
    Fintype.card (HermiteCoreAddress k n) = 2 * (n + 1) * (2 * k + 6) ^ 2 := by
  simp only [HermiteCoreAddress, Fintype.card_prod, Fintype.card_fin,
    Fintype.card_bool, hermiteFiniteBond_card]
  ring

theorem injectionBond_card (k : ℕ) : Fintype.card (InjectionBond k) = 2 * k + 3 := by
  simp [InjectionBond]

/-- Candidate middle register: one boundary scalar plus the shared coefficients.
The cardinality is not, by itself, a matrix-product realization theorem. -/
abbrev MiddleBond (k : ℕ) := Option (Fin (2 * k + 2))

theorem middleBond_card (k : ℕ) : Fintype.card (MiddleBond k) = 2 * k + 3 := by
  simp [MiddleBond]

end QuantumBlockEncoding.HermiteBoundaryInjection
