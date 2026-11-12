import Mathlib.Analysis.SpecialFunctions.Complex.Arctan
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Algebra.Order.Floor.Ring
import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.Data.Nat.Log
import Mathlib.Data.Nat.Size
import Mathlib.Tactic

open scoped BigOperators

namespace QuantumBlockEncoding.ExperimentalRadiusSupplier

def atanSum (q : ℚ) (m : ℕ) : ℚ :=
  ∑ i ∈ Finset.range m, (-1)^i / ((2*i+1 : ℚ)*q^(2*i+1))

def piApprox (m : ℕ) : ℚ := 16*atanSum 5 m-4*atanSum 239 m
def piError (m : ℕ) : ℚ := 20/(2*m+1)
def termCount (L epsilon : ℚ) : ℕ := (⌈20*L/epsilon⌉ : ℤ).toNat+1
def radius (L epsilon : ℚ) : ℚ := piApprox (termCount L epsilon)*L
def radiusInterval (L epsilon : ℚ) : ℚ × ℚ :=
  ((piApprox (termCount L epsilon)-piError (termCount L epsilon))*L,
   (piApprox (termCount L epsilon)+piError (termCount L epsilon))*L)

theorem atan_remainder_sharp (x : ℝ) (hx : 0 ≤ x) (hx1 : x < 1) (m : ℕ) :
    |Real.arctan x-∑ i ∈ Finset.range m, (-1)^i*x^(2*i+1)/(2*i+1)| ≤
      x^(2*m+1)/(2*m+1 : ℝ) := by
  let f : ℕ → ℝ := fun i => x^(2*i+1)/(2*i+1)
  have hf0 (i : ℕ) : 0 ≤ f i := by dsimp [f]; positivity
  have hfa : Antitone f := by
    intro i j hij
    dsimp [f]
    apply div_le_div₀ (pow_nonneg hx _) _ (by positivity) _
    · exact pow_le_pow_of_le_one hx hx1.le (by omega)
    · exact_mod_cast (show 2*i+1 ≤ 2*j+1 by omega)
  have hbound (i : ℕ) : f i ≤ x^i := by
    dsimp [f]
    calc
      _ ≤ x^(2*i+1) := div_le_self (pow_nonneg hx _) (by have := Nat.cast_nonneg (α := ℝ) i; linarith)
      _ ≤ x^i := pow_le_pow_of_le_one hx hx1.le (by omega)
  have hfs : Summable f := (summable_geometric_of_lt_one hx hx1).of_nonneg_of_le hf0 hbound
  have hs := Real.hasSum_arctan (x := x) (by simpa [Real.norm_eq_abs, abs_of_nonneg hx])
  have hts : (∑' i : ℕ, (-1)^i*f i) = Real.arctan x := by
    simpa [f, mul_div_assoc] using hs.tsum_eq
  have he := alternating_series_error_bound f hfa hfs m
  rw [hts] at he
  simpa [f, mul_div_assoc] using he

theorem atan_remainder (x : ℝ) (hx : 0 ≤ x) (hx1 : x < 1) (m : ℕ) :
    |Real.arctan x-∑ i ∈ Finset.range m, (-1)^i*x^(2*i+1)/(2*i+1)| ≤
      1/(2*m+1 : ℝ) :=
  (atan_remainder_sharp x hx hx1 m).trans
    (div_le_div_of_nonneg_right (pow_le_one₀ hx hx1.le) (by positivity))

theorem atan_remainder_geometric (x : ℝ) (hx : 0 ≤ x) (hxhalf : x ≤ 1/2) (m : ℕ) :
    |Real.arctan x-∑ i ∈ Finset.range m, (-1)^i*x^(2*i+1)/(2*i+1)| ≤
      1/(2 : ℝ)^m := by
  have hx1 : x < 1 := by linarith
  apply (atan_remainder_sharp x hx hx1 m).trans
  calc
    _ ≤ x^(2*m+1) := div_le_self (pow_nonneg hx _) (by have := Nat.cast_nonneg (α := ℝ) m; linarith)
    _ ≤ x^m := pow_le_pow_of_le_one hx hx1.le (by omega)
    _ ≤ (1/2 : ℝ)^m := pow_le_pow_left₀ hx hxhalf m
    _ = _ := by rw [div_pow, one_pow]

theorem atanSum_cast (q : ℚ) (m : ℕ) :
    (atanSum q m : ℝ) = ∑ i ∈ Finset.range m,
      (-1)^i*((q : ℝ)^(2*i+1))⁻¹/(2*i+1) := by
  unfold atanSum
  push_cast
  apply Finset.sum_congr rfl
  intro i _
  simp [div_eq_mul_inv, mul_inv_rev, mul_comm, mul_left_comm]

theorem piApprox_error (m : ℕ) : |(piApprox m : ℝ)-Real.pi| ≤ (piError m : ℝ) := by
  have h5 := atan_remainder (1/5) (by norm_num) (by norm_num) m
  have h239 := atan_remainder (1/239) (by norm_num) (by norm_num) m
  have hc5 : (atanSum 5 m : ℝ) = ∑ i ∈ Finset.range m,
      (-1)^i*(1/5 : ℝ)^(2*i+1)/(2*i+1) := by
    rw [atanSum_cast]
    apply Finset.sum_congr rfl
    intro i _
    simp only [Rat.cast_ofNat, one_div, inv_pow]
  have hc239 : (atanSum 239 m : ℝ) = ∑ i ∈ Finset.range m,
      (-1)^i*(1/239 : ℝ)^(2*i+1)/(2*i+1) := by
    rw [atanSum_cast]
    apply Finset.sum_congr rfl
    intro i _
    simp only [Rat.cast_ofNat, one_div, inv_pow]
  rw [← hc5] at h5
  rw [← hc239] at h239
  have hpi := Real.four_mul_arctan_inv_5_sub_arctan_inv_239
  have hid : (piApprox m : ℝ)-Real.pi =
      16*((atanSum 5 m : ℝ)-Real.arctan (1/5))-
      4*((atanSum 239 m : ℝ)-Real.arctan (1/239)) := by
    unfold piApprox
    push_cast
    norm_num [one_div] at hpi ⊢
    linarith
  rw [hid]
  calc
    _ ≤ |16*((atanSum 5 m : ℝ)-Real.arctan (1/5))|+
        |4*((atanSum 239 m : ℝ)-Real.arctan (1/239))| := abs_sub _ _
    _ = 16*|Real.arctan (1/5)-(atanSum 5 m : ℝ)|+
        4*|Real.arctan (1/239)-(atanSum 239 m : ℝ)| := by
      rw [abs_mul, abs_mul, abs_sub_comm (atanSum 5 m : ℝ), abs_sub_comm (atanSum 239 m : ℝ)]
      norm_num
    _ ≤ 16*(1/(2*m+1 : ℝ))+4*(1/(2*m+1 : ℝ)) := by gcongr
    _ = (piError m : ℝ) := by unfold piError; push_cast; ring

theorem piApprox_positive (m : ℕ) (hm : 1 ≤ m) : 0 < piApprox m := by
  by_cases h4 : 4 ≤ m
  · have he := piApprox_error m
    have hb : (piError m : ℝ) ≤ 20/9 := by
      unfold piError
      push_cast
      apply div_le_div_of_nonneg_left (by norm_num) (by norm_num)
      exact_mod_cast (show 9 ≤ 2*m+1 by omega)
    have ha := (abs_le.mp he).1
    have hp := Real.pi_gt_three
    have hpos : 0 < (piApprox m : ℝ) := by linarith
    exact_mod_cast hpos
  · have hc : m=1 ∨ m=2 ∨ m=3 := by omega
    rcases hc with rfl | rfl | rfl <;> norm_num [piApprox, atanSum, Finset.sum_range_succ]

theorem radius_budget (L epsilon : ℚ) (hL : 0 < L) (hepsilon : 0 < epsilon) :
    piError (termCount L epsilon)*L ≤ epsilon := by
  have hc := Int.le_ceil (20*L/epsilon)
  have hn : (⌈20*L/epsilon⌉ : ℤ) ≤ (⌈20*L/epsilon⌉ : ℤ).toNat := by omega
  have hnq : (⌈20*L/epsilon⌉ : ℚ) ≤ ((⌈20*L/epsilon⌉ : ℤ).toNat : ℚ) := by exact_mod_cast hn
  have hb : 20*L/epsilon ≤ (termCount L epsilon : ℚ) := by
    unfold termCount
    push_cast
    linarith
  have hc' := (div_le_iff₀ hepsilon).mp hb
  unfold piError
  have hd : (0 : ℚ) < 2*(termCount L epsilon : ℚ)+1 := by positivity
  rw [div_mul_eq_mul_div]
  apply (div_le_iff₀ hd).mpr
  have hN : (0 : ℚ) ≤ termCount L epsilon := Nat.cast_nonneg _
  nlinarith

theorem radius_error (L epsilon : ℚ) (hL : 0 < L) (hepsilon : 0 < epsilon) :
    |(radius L epsilon : ℝ)-Real.pi*(L : ℝ)| ≤ (epsilon : ℝ) := by
  have hLR : (0 : ℝ) < L := by exact_mod_cast hL
  have he := piApprox_error (termCount L epsilon)
  have hb : (piError (termCount L epsilon) : ℝ)*(L : ℝ) ≤ (epsilon : ℝ) := by
    exact_mod_cast radius_budget L epsilon hL hepsilon
  calc
    _ = |(piApprox (termCount L epsilon) : ℝ)-Real.pi| * (L : ℝ) := by
      unfold radius
      push_cast
      rw [← sub_mul, abs_mul, abs_of_pos hLR]
    _ ≤ (piError (termCount L epsilon) : ℝ)*(L : ℝ) := mul_le_mul_of_nonneg_right he hLR.le
    _ ≤ _ := hb

theorem radius_positive (L epsilon : ℚ) (hL : 0 < L) (hepsilon : 0 < epsilon) :
    0 < radius L epsilon := by
  unfold radius
  exact mul_pos (piApprox_positive _ (by unfold termCount; omega)) hL

theorem radius_membership (L epsilon : ℚ) (hL : 0 < L) (hepsilon : 0 < epsilon) :
    Real.pi*(L : ℝ) ∈ Set.Icc ((radiusInterval L epsilon).1 : ℝ)
      ((radiusInterval L epsilon).2 : ℝ) := by
  have he := abs_le.mp (piApprox_error (termCount L epsilon))
  have hLR : (0 : ℝ) ≤ L := by exact_mod_cast hL.le
  constructor
  · have h := mul_le_mul_of_nonneg_right he.2 hLR
    dsimp [radiusInterval]
    push_cast
    nlinarith
  · have h := mul_le_mul_of_nonneg_right he.1 hLR
    dsimp [radiusInterval]
    push_cast
    nlinarith

def logTermCount (L epsilon : ℚ) : ℕ :=
  Nat.clog 2 (max 1 (Nat.ceil (20*L/epsilon)))+1
def logRadius (L epsilon : ℚ) : ℚ := piApprox (logTermCount L epsilon)*L
def logRadiusInterval (L epsilon : ℚ) : ℚ × ℚ :=
  ((piApprox (logTermCount L epsilon)-20/(2 : ℚ)^(logTermCount L epsilon))*L,
   (piApprox (logTermCount L epsilon)+20/(2 : ℚ)^(logTermCount L epsilon))*L)

theorem piApprox_error_geometric (m : ℕ) :
    |(piApprox m : ℝ)-Real.pi| ≤ 20/(2 : ℝ)^m := by
  have h5 : |Real.arctan (1/5)-(atanSum 5 m : ℝ)| ≤ 1/(2 : ℝ)^m := by
    rw [atanSum_cast]
    simpa only [Rat.cast_ofNat, one_div, inv_pow] using
      atan_remainder_geometric (1/5) (by norm_num) (by norm_num) m
  have h239 : |Real.arctan (1/239)-(atanSum 239 m : ℝ)| ≤ 1/(2 : ℝ)^m := by
    rw [atanSum_cast]
    simpa only [Rat.cast_ofNat, one_div, inv_pow] using
      atan_remainder_geometric (1/239) (by norm_num) (by norm_num) m
  have hpi := Real.four_mul_arctan_inv_5_sub_arctan_inv_239
  have hid : (piApprox m : ℝ)-Real.pi =
      16*((atanSum 5 m : ℝ)-Real.arctan (1/5))-
      4*((atanSum 239 m : ℝ)-Real.arctan (1/239)) := by
    unfold piApprox
    push_cast
    norm_num [one_div] at hpi ⊢
    linarith
  rw [hid]
  calc
    _ ≤ |16*((atanSum 5 m : ℝ)-Real.arctan (1/5))|+
        |4*((atanSum 239 m : ℝ)-Real.arctan (1/239))| := abs_sub _ _
    _ = 16*|Real.arctan (1/5)-(atanSum 5 m : ℝ)|+
        4*|Real.arctan (1/239)-(atanSum 239 m : ℝ)| := by
      rw [abs_mul, abs_mul, abs_sub_comm (atanSum 5 m : ℝ), abs_sub_comm (atanSum 239 m : ℝ)]
      norm_num
    _ ≤ 16*(1/(2 : ℝ)^m)+4*(1/(2 : ℝ)^m) := by gcongr
    _ = _ := by ring

theorem logRadius_budget (L epsilon : ℚ) (hL : 0 < L) (hepsilon : 0 < epsilon) :
    (20/(2 : ℚ)^(logTermCount L epsilon))*L ≤ epsilon := by
  have ht : 20*L/epsilon ≤ (max 1 (Nat.ceil (20*L/epsilon)) : ℚ) :=
    (Nat.le_ceil _).trans (by exact_mod_cast le_max_right 1 (Nat.ceil (20*L/epsilon)))
  have hp : max 1 (Nat.ceil (20*L/epsilon)) ≤ 2^(logTermCount L epsilon) := by
    unfold logTermCount
    exact (Nat.le_pow_clog (by norm_num) _).trans
      (Nat.pow_le_pow_right (by norm_num) (by omega))
  have hb : 20*L/epsilon ≤ (2 : ℚ)^(logTermCount L epsilon) :=
    ht.trans (by exact_mod_cast hp)
  rw [div_mul_eq_mul_div]
  apply (div_le_iff₀ (by positivity : (0 : ℚ) < 2^(logTermCount L epsilon))).mpr
  have h := (div_le_iff₀ hepsilon).mp hb
  nlinarith

theorem logRadius_error (L epsilon : ℚ) (hL : 0 < L) (hepsilon : 0 < epsilon) :
    |(logRadius L epsilon : ℝ)-Real.pi*(L : ℝ)| ≤ (epsilon : ℝ) := by
  have hLR : (0 : ℝ) < L := by exact_mod_cast hL
  have he := piApprox_error_geometric (logTermCount L epsilon)
  have hb : (20/(2 : ℝ)^(logTermCount L epsilon))*(L : ℝ) ≤ (epsilon : ℝ) := by
    have h := (Rat.cast_le (K := ℝ)).mpr (logRadius_budget L epsilon hL hepsilon)
    simpa using h
  calc
    _ = |(piApprox (logTermCount L epsilon) : ℝ)-Real.pi| * (L : ℝ) := by
      unfold logRadius
      push_cast
      rw [← sub_mul, abs_mul, abs_of_pos hLR]
    _ ≤ (20/(2 : ℝ)^(logTermCount L epsilon))*(L : ℝ) := mul_le_mul_of_nonneg_right he hLR.le
    _ ≤ _ := hb

theorem logRadius_positive (L epsilon : ℚ) (hL : 0 < L) (hepsilon : 0 < epsilon) :
    0 < logRadius L epsilon := by
  unfold logRadius
  exact mul_pos (piApprox_positive _ (by unfold logTermCount; omega)) hL

theorem logRadius_membership (L epsilon : ℚ) (hL : 0 < L) (hepsilon : 0 < epsilon) :
    Real.pi*(L : ℝ) ∈ Set.Icc ((logRadiusInterval L epsilon).1 : ℝ)
      ((logRadiusInterval L epsilon).2 : ℝ) := by
  have he := abs_le.mp (piApprox_error_geometric (logTermCount L epsilon))
  have hLR : (0 : ℝ) ≤ L := by exact_mod_cast hL.le
  constructor
  · have h := mul_le_mul_of_nonneg_right he.2 hLR
    dsimp [logRadiusInterval]
    push_cast
    nlinarith
  · have h := mul_le_mul_of_nonneg_right he.1 hLR
    dsimp [logRadiusInterval]
    push_cast
    nlinarith

theorem logTermCount_size (L epsilon : ℚ) :
    logTermCount L epsilon ≤ Nat.size (max 1 (Nat.ceil (20*L/epsilon)))+1 := by
  unfold logTermCount
  exact Nat.add_le_add_right (Nat.clog_le_of_le_pow (Nat.lt_size_self _).le) 1

#print axioms atan_remainder_sharp
#print axioms atan_remainder_geometric
#print axioms atan_remainder
#print axioms atanSum_cast
#print axioms piApprox_error
#print axioms piApprox_positive
#print axioms radius_budget
#print axioms radius_error
#print axioms radius_positive
#print axioms radius_membership
#print axioms piApprox_error_geometric
#print axioms logRadius_budget
#print axioms logRadius_error
#print axioms logRadius_positive
#print axioms logRadius_membership
#print axioms logTermCount_size

end QuantumBlockEncoding.ExperimentalRadiusSupplier
