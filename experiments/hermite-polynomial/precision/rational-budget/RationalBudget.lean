import SafeEnclosure

/-!
Computable exact-rational budget allocation for the frozen interval consumer.
This INTERNAL provider does not generate true source-angle enclosures or an
executable Hermite source list, and makes no total finite-bit runtime claim.
-/
namespace QuantumBlockEncoding.RationalBudget

def coefficientNat (k n : ℕ) : ℕ := 24*(n+1)*(2*k+6)^3

def ceilingThreshold (k n : ℕ) (epsilon : ℚ) : ℕ :=
  Nat.ceil ((coefficientNat k n : ℚ)/epsilon)

def bits (k n : ℕ) (epsilon : ℚ) : ℕ :=
  Nat.clog 2 (max 1 (ceilingThreshold k n epsilon))

def allocate (k n : ℕ) (epsilon : ℚ) : Option ℕ :=
  if 0<epsilon then some (bits k n epsilon) else none

def supplyBudget (k n : ℕ) (epsilon : ℚ) (exact : PrimitiveCircuit qubits)
    (intervals : List (ℚ×ℚ)) : Option (ℕ×PrimitiveCircuit qubits) := do
  let b ← allocate k n epsilon
  let returned ← SafeEnclosure.supplyCircuit b exact intervals
  pure (b,returned)

theorem coefficientNat_cast (k n : ℕ) :
    (coefficientNat k n : ℝ) = DyadicSupplier.errorCoefficient k n := by
  simp [coefficientNat, DyadicSupplier.errorCoefficient]

/-- The actual threshold computation is finite integer numerator/denominator
division on the normalized rational ratio, not a Real ceiling oracle. -/
theorem ceilingThreshold_num_den (k n : ℕ) (epsilon : ℚ) :
    let q : ℚ := (coefficientNat k n : ℚ)/epsilon
    ceilingThreshold k n epsilon = (-(-q.num / (q.den : ℤ))).toNat := by
  dsimp [ceilingThreshold]
  rw [← Int.ceil_toNat, Rat.ceil_def']

theorem ceilingThreshold_bound (k n : ℕ) (epsilon : ℚ) :
    (coefficientNat k n : ℚ)/epsilon ≤ (ceilingThreshold k n epsilon : ℚ) :=
  Nat.le_ceil _

theorem bits_pow_bound (k n : ℕ) (epsilon : ℚ) :
    ceilingThreshold k n epsilon ≤ 2^(bits k n epsilon) :=
  (le_max_right 1 _).trans (Nat.le_pow_clog (by norm_num) _)

theorem bits_error_rat (k n : ℕ) (epsilon : ℚ) (he : 0<epsilon) :
    (coefficientNat k n : ℚ)/(2 : ℚ)^(bits k n epsilon) ≤ epsilon := by
  have hp : (coefficientNat k n : ℚ)/epsilon ≤ (2 : ℚ)^(bits k n epsilon) :=
    (ceilingThreshold_bound k n epsilon).trans (by exact_mod_cast bits_pow_bound k n epsilon)
  rw [div_le_iff₀ (by positivity)]
  have hh := (div_le_iff₀ he).mp hp
  nlinarith

theorem bits_error_real (k n : ℕ) (epsilon : ℚ) (he : 0<epsilon) :
    DyadicSupplier.errorCoefficient k n/(2 : ℝ)^(bits k n epsilon) ≤ (epsilon : ℝ) := by
  rw [← coefficientNat_cast]
  have bound := (Rat.cast_le (K := ℝ)).mpr (bits_error_rat k n epsilon he)
  simpa using bound

theorem allocate_positive (k n : ℕ) (epsilon : ℚ) (he : 0<epsilon) :
    allocate k n epsilon = some (bits k n epsilon) := if_pos he

theorem allocate_nonpositive (k n : ℕ) (epsilon : ℚ) (he : epsilon≤0) :
    allocate k n epsilon = none := if_neg (not_lt.mpr he)

theorem bits_size_bound (k n : ℕ) (epsilon : ℚ) :
    bits k n epsilon ≤ Nat.size (max 1 (ceilingThreshold k n epsilon)) :=
  Nat.clog_le_of_le_pow (Nat.lt_size_self _).le

theorem allocated_numerator_bits (k n : ℕ) (epsilon lo hi : ℚ) :
    Nat.size (SafeEnclosure.nearestNumerator (bits k n epsilon) lo hi).natAbs ≤
      Nat.size (lo.num.natAbs+hi.num.natAbs+1) +
        Nat.size (max 1 (ceilingThreshold k n epsilon)) :=
  (SafeEnclosure.numerator_bits_bound _ _ _).trans
    (Nat.add_le_add_left (bits_size_bound k n epsilon) _)

/-- Positive rational input has an integer numerator at least one. This
input-size bound is intentionally coarser than the actual allocator. -/
theorem threshold_input_bound (k n : ℕ) (epsilon : ℚ) (he : 0<epsilon) :
    ceilingThreshold k n epsilon ≤ coefficientNat k n * epsilon.den := by
  apply Nat.ceil_le.mpr
  rw [div_le_iff₀ he]
  have hn : (1 : ℚ) ≤ (epsilon.num : ℚ) := by
    exact_mod_cast (Int.add_one_le_iff.mpr (Rat.num_pos.mpr he))
  have hden : (epsilon.den : ℚ) ≠ 0 := by exact_mod_cast epsilon.den_ne_zero
  have hnum : (epsilon.num : ℚ) = epsilon*(epsilon.den : ℚ) :=
    (div_eq_iff hden).mp epsilon.num_div_den
  have hm := mul_le_mul_of_nonneg_left hn (Nat.cast_nonneg (coefficientNat k n) :
    (0 : ℚ) ≤ coefficientNat k n)
  rw [hnum] at hm
  push_cast
  nlinarith

theorem bits_input_size_bound (k n : ℕ) (epsilon : ℚ) (he : 0<epsilon) :
    bits k n epsilon ≤ Nat.size (coefficientNat k n * epsilon.den) := by
  have positive : 0 < coefficientNat k n * epsilon.den := by
    have := epsilon.den_pos
    unfold coefficientNat
    positivity
  exact Nat.clog_le_of_le_pow
    ((max_le (by omega) (threshold_input_bound k n epsilon he)).trans (Nat.lt_size_self _).le)

theorem bits_input_sum_size_bound (k n : ℕ) (epsilon : ℚ) (he : 0<epsilon) :
    bits k n epsilon ≤ Nat.size (coefficientNat k n) + Nat.size epsilon.den := by
  apply (bits_input_size_bound k n epsilon he).trans
  apply Nat.size_le.mpr
  rw [pow_add]
  calc
    _ < 2^(Nat.size (coefficientNat k n))*epsilon.den :=
      Nat.mul_lt_mul_of_pos_right (Nat.lt_size_self _) epsilon.den_pos
    _ ≤ _ := Nat.mul_le_mul_left _ (Nat.lt_size_self _).le

theorem allocated_numerator_input_bits (k n : ℕ) (epsilon lo hi : ℚ) (he : 0<epsilon) :
    Nat.size (SafeEnclosure.nearestNumerator (bits k n epsilon) lo hi).natAbs ≤
      Nat.size (lo.num.natAbs+hi.num.natAbs+1) + Nat.size (coefficientNat k n) +
        Nat.size epsilon.den := by
  simpa only [Nat.add_assoc] using
    (SafeEnclosure.numerator_bits_bound _ _ _).trans
      (Nat.add_le_add_left (bits_input_sum_size_bound k n epsilon he) _)

theorem supplyBudget_positive {k n : ℕ} {epsilon : ℚ} (he : 0<epsilon)
    {exact returned : PrimitiveCircuit qubits} {intervals : List (ℚ×ℚ)}
    (success : SafeEnclosure.supplyCircuit (bits k n epsilon) exact intervals = some returned) :
    supplyBudget k n epsilon exact intervals = some (bits k n epsilon,returned) := by
  simp [supplyBudget, allocate, he, success]

theorem supplyBudget_nonpositive {k n : ℕ} {epsilon : ℚ} (he : epsilon≤0)
    (exact : PrimitiveCircuit qubits) (intervals : List (ℚ×ℚ)) :
    supplyBudget k n epsilon exact intervals = none := by
  simp [supplyBudget, allocate, not_lt.mpr he]

/-- The accepted finite budget and interval validity produce actual Some data.
Sound is the missing INTERNAL source-enclosure interface, not a Source Anchor
assumption or an unconditional finite-bit Hermite pipeline certificate. -/
theorem hermite_internal_supplier (k n : ℕ) (L : ℝ) (hL : 0<L)
    (epsilon : ℚ) (he : 0<epsilon) (intervals : List (ℚ×ℚ))
    (count : intervals.length =
      PrimitiveCircuit.ryCount (StagedGlobalAssembly.compile k n L hL).run.value)
    (valid : SafeEnclosure.ValidIntervals (bits k n epsilon) intervals)
    (sound : SafeEnclosure.Sound (StagedGlobalAssembly.compile k n L hL).run.value intervals) :
    ∃ returned,
      supplyBudget k n epsilon (StagedGlobalAssembly.compile k n L hL).run.value intervals =
        some (bits k n epsilon,returned) ∧
      returned.resource = (StagedGlobalAssembly.compile k n L hL).run.value.resource ∧
      returned.map SafeEnclosure.eraseRyAngle =
        (StagedGlobalAssembly.compile k n L hL).run.value.map SafeEnclosure.eraseRyAngle ∧
      ‖DyadicSupplier.column (evalPrimitiveCircuit returned) - DyadicSupplier.target k n L‖ ≤
        (epsilon : ℝ) := by
  obtain ⟨returned,success⟩ := SafeEnclosure.supplyCircuit_complete _ _ intervals count valid
  exact ⟨returned,supplyBudget_positive he success,SafeEnclosure.supplyCircuit_resource success,
    SafeEnclosure.supplyCircuit_chronology success,
    (SafeEnclosure.hermite_internal_state_error k n L hL _ intervals returned sound success).trans
      (bits_error_real k n epsilon he)⟩

namespace Tests
#eval allocate 0 0 0
#eval allocate 0 0 (-1/10)
#eval allocate 0 0 1
#eval allocate 0 0 (1/10)
#eval allocate 0 0 10000
#eval allocate 0 0 (100000000000000000000000000000000000000000000000000 : ℚ)
#eval allocate 0 0 (1/(10:ℚ)^100)
#eval allocate 2 5 (1/1000)
#eval decide (allocate 0 0 0 = none)
#eval decide (allocate 0 0 (-1/10) = none)
#eval decide (allocate 0 0 1 = some 13)
#eval decide (allocate 0 0 (1/10) = some 16)
#eval decide (allocate 0 0 10000 = some 0)
#eval decide (allocate 0 0 (1/(10:ℚ)^100) = some 345)
#eval decide (allocate 2 5 (1/1000) = some 28)
#eval (supplyBudget 0 0 1 SafeEnclosure.Tests.physical [(1/10,1/10),(-1/10,-1/10)]).map
  (fun bc => (bc.1, bc.2.map (fun g => match g with
    | .ry t (.rational a) => ("ry",t.val,a)
    | .cx c t _ => ("cx",c.val,(t.val : ℚ))
    | _ => ("other",0,0))))
#eval (supplyBudget 0 0 0 SafeEnclosure.Tests.physical []).isNone
#eval (supplyBudget 0 0 1 SafeEnclosure.Tests.physical []).isNone
#eval (supplyBudget 0 0 1 SafeEnclosure.Tests.physical
  [(1/10,1/10),(-1/10,-1/10),(0,0)]).isNone
#eval (supplyBudget 0 0 1 SafeEnclosure.Tests.physical [(0,1),(-1/10,-1/10)]).isNone
example : allocate 0 0 0 = none := by norm_num [allocate]
example : allocate 0 0 (-1/10) = none := by norm_num [allocate]
end Tests

#print axioms ceilingThreshold_num_den
#print axioms bits_error_rat
#print axioms bits_error_real
#print axioms allocate_nonpositive
#print axioms bits_size_bound
#print axioms allocated_numerator_bits
#print axioms threshold_input_bound
#print axioms bits_input_size_bound
#print axioms bits_input_sum_size_bound
#print axioms allocated_numerator_input_bits
#print axioms supplyBudget_nonpositive
#print axioms hermite_internal_supplier
end QuantumBlockEncoding.RationalBudget
