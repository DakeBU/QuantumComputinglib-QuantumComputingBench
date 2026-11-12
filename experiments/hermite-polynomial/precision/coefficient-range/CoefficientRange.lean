import QuantumBlockEncoding.StoredHermiteCoefficients
import Mathlib.Data.Nat.Choose.Bounds

/-!
# Literal Hermite coefficient ranges and rational output envelopes

This experiment proves coarse bounds for the existing source, not a replacement
coefficient formula. For i ≤ k, each source-series summand is at most 2^(2k)
because the binomial top is at most 2k and m! ≥ 1. A left coefficient has at
most k+1 contributing terms, an elevation numerator at most 2^k and a positive
integer denominator at least 1. Hence B=(k+1)^2 2^(3k) bounds every left
coefficient. The source coefficient is in [0,2B] because exp(-1) is in [0,1].
The shared exact restriction theorem transports this range to each valid
injection, and the stored fromConstant theorem is a concrete consumer.

Every contributing m! divides k!. Clearing that denominator gives the literal
natural sourceNumerator and leftNumerator, with D=k! choose(2k+1,r). For valid
r, D is positive, D ≤ 2^(k²+3k+1), and A ≤ 2^(2k²+9k+3). Thus A/D has a
polynomial-in-numeric-k binary output envelope. Supplying a finite rational
scalar p/q gives the exact reflected source coefficient numerator/denominator
and explicitly retains p,q size. This is output size, not runtime, executable
Python refinement, scalar analytic enclosure membership or float64 totality.

Signatures are retained in immutable versioned pre-proof seals. These internal
providers do not clear the previous offset seal-history debt or quantum ROOT.
-/

noncomputable section
open scoped BigOperators

namespace QuantumBlockEncoding.ExperimentalCoefficientRange
open HermiteBernstein

def coarseBound (k : ℕ) : ℝ := (k + 1 : ℝ)^2 * 2^(3*k)
def factorialEnvelope (k : ℕ) : ℕ := (k+1)^k
def commonDenominator (k r : ℕ) : ℕ := k.factorial * (2*k+1).choose r

theorem sourceCoefficient_upper (k i : ℕ) (hi : i ≤ k) :
    sourceCoefficient k i ≤ (k+1 : ℝ) * 2^(2*k) := by
  rw [sourceCoefficient_eq]
  calc
    _ ≤ ∑ _m ∈ Finset.range (i+1), (2 : ℝ)^(2*k) := by
      apply Finset.sum_le_sum
      intro m hm
      have hc : (Nat.choose (k+i-m) k : ℝ) ≤ (2 : ℝ)^(2*k) := by
        have h := (Nat.choose_le_two_pow (k+i-m) k).trans
          (Nat.pow_le_pow_right (by decide : 1 ≤ (2 : ℕ)) (by omega : k+i-m ≤ 2*k))
        exact_mod_cast h
      have hf : (1 : ℝ) ≤ (m.factorial : ℝ) := by
        exact_mod_cast Nat.factorial_pos m
      exact (div_le_self (Nat.cast_nonneg _) hf).trans hc
    _ = (i+1 : ℝ) * 2^(2*k) := by simp
    _ ≤ (k+1 : ℝ) * 2^(2*k) := by
      gcongr

theorem leftCoefficient_upper (k r : ℕ) : leftCoefficient k r ≤ coarseBound k := by
  rw [leftCoefficient_eq]
  calc
    _ ≤ ∑ _i ∈ Finset.range (k+1), (k+1 : ℝ) * 2^(2*k) * 2^k := by
      apply Finset.sum_le_sum
      intro i hi
      split_ifs with h
      · have hi' : i ≤ k := by simpa using hi
        have hc : ((k-i).choose (r-i) : ℝ) ≤ (2 : ℝ)^k := by
          exact_mod_cast (Nat.choose_le_two_pow (k-i) (r-i)).trans
            (Nat.pow_le_pow_right (by decide : 1 ≤ (2 : ℕ)) (Nat.sub_le k i))
        have hd : (1 : ℝ) ≤ ((2*k+1).choose r : ℝ) := by
          exact_mod_cast Nat.choose_pos (show r ≤ 2*k+1 by omega)
        exact (div_le_self (mul_nonneg (sourceCoefficient_nonneg _ _) (Nat.cast_nonneg _)) hd).trans
          (mul_le_mul (sourceCoefficient_upper k i hi') hc (Nat.cast_nonneg _)
            (mul_nonneg (by positivity) (by positivity)))
      · positivity
    _ = coarseBound k := by
      simp only [Finset.sum_const, Finset.card_range, nsmul_eq_mul]
      unfold coarseBound
      rw [show 3*k = 2*k+k by omega, pow_add]
      push_cast
      ring

theorem sourceBernsteinCoefficient_range (k r : ℕ) :
    sourceBernsteinCoefficient k r ∈ Set.Icc 0 (2 * coarseBound k) := by
  refine ⟨sourceBernsteinCoefficient_nonneg _ _, ?_⟩
  have he : Real.exp (-1) ≤ 1 := by
    calc
      Real.exp (-1) ≤ Real.exp 0 := Real.exp_le_exp.mpr (by norm_num)
      _ = 1 := Real.exp_zero
  unfold sourceBernsteinCoefficient
  have h := mul_le_mul_of_nonneg_right he (leftCoefficient_nonneg k r)
  have h1 := leftCoefficient_upper k r
  have h2 := leftCoefficient_upper k (2*k+1-r)
  nlinarith

theorem restricted_source_range (k : ℕ) (u v : ℝ)
    (hu : 0 ≤ u) (huv : u < v) (hv : v ≤ 1) (r : ℕ) (hr : r ≤ 2*k+1) :
    restrictCoefficients (2*k+1) u v (sourceBernsteinCoefficient k) r ∈
      Set.Icc 0 (2 * coarseBound k) :=
  restrictCoefficients_bounds _ _ _ _ _ _ hu huv hv
    (fun i _ => sourceBernsteinCoefficient_range k i) r hr

theorem factorial_output_bound (k : ℕ) : k.factorial ≤ factorialEnvelope k := by
  exact k.factorial_le_pow.trans (Nat.pow_le_pow_left (Nat.le_succ k) k)

theorem commonDenominator_bound (k r : ℕ) :
    commonDenominator k r ≤ factorialEnvelope k * 2^(2*k+1) :=
  Nat.mul_le_mul (factorial_output_bound k) (Nat.choose_le_two_pow _ _)

theorem commonDenominator_pos (k r : ℕ) (hr : r ≤ 2*k+1) :
    0 < commonDenominator k r := Nat.mul_pos (Nat.factorial_pos _) (Nat.choose_pos hr)

def sourceNumerator (k i : ℕ) : ℕ :=
  ∑ m ∈ Finset.range (i+1), (k+i-m).choose k * (k.factorial / m.factorial)

def leftNumerator (k r : ℕ) : ℕ :=
  ∑ i ∈ Finset.range (k+1),
    if i ≤ r ∧ r ≤ k then sourceNumerator k i * (k-i).choose (r-i) else 0

theorem sourceNumerator_value (k i : ℕ) (hi : i ≤ k) :
    sourceCoefficient k i = (sourceNumerator k i : ℝ) / (k.factorial : ℝ) := by
  rw [sourceCoefficient_eq, sourceNumerator, Nat.cast_sum, Finset.sum_div]
  apply Finset.sum_congr rfl
  intro m hm
  have hm' : m ≤ k := by have := Finset.mem_range.mp hm; omega
  have hf : (k.factorial : ℝ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero k
  have hfm : (m.factorial : ℝ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero m
  rw [Nat.cast_mul, Nat.cast_div (Nat.factorial_dvd_factorial hm') hfm]
  field_simp

theorem leftNumerator_value (k r : ℕ) :
    leftCoefficient k r = (leftNumerator k r : ℝ) / (commonDenominator k r : ℝ) := by
  rw [leftCoefficient_eq, leftNumerator, Nat.cast_sum, Finset.sum_div]
  apply Finset.sum_congr rfl
  intro i hi
  have hi' : i ≤ k := by simpa using hi
  simp only [Nat.cast_ite, Nat.cast_zero, Nat.cast_mul, commonDenominator]
  split_ifs with h
  · rw [sourceNumerator_value k i hi']
    ring
  · simp

theorem leftNumerator_bound (k r : ℕ) (hr : r ≤ 2*k+1) :
    leftNumerator k r ≤ (k+1)^2 * 2^(3*k) * commonDenominator k r := by
  have hD : (0 : ℝ) < (commonDenominator k r : ℝ) := by
    exact_mod_cast commonDenominator_pos k r hr
  have h := (div_le_iff₀ hD).mp
    (show (leftNumerator k r : ℝ) / (commonDenominator k r : ℝ) ≤ coarseBound k by
      rw [← leftNumerator_value]
      exact leftCoefficient_upper _ _)
  unfold coarseBound at h
  exact_mod_cast h

theorem commonDenominator_binary_bound (k r : ℕ) :
    commonDenominator k r ≤ 2^(k*(k+1)+2*k+1) := by
  calc
    _ ≤ (k+1)^k * 2^(2*k+1) := commonDenominator_bound k r
    _ ≤ (2^(k+1))^k * 2^(2*k+1) := by
      exact Nat.mul_le_mul_right _ (Nat.pow_le_pow_left (Nat.lt_two_pow_self (n := k+1)).le k)
    _ = _ := by rw [← pow_mul, ← pow_add]; congr 1; ring

theorem leftNumerator_binary_bound (k r : ℕ) (hr : r ≤ 2*k+1) :
    leftNumerator k r ≤ 2^((k+2)*(k+1)+k*(k+1)+5*k+1) := by
  have hsmall : (k+1)^2 ≤ 2^((k+2)*(k+1)) := by
    calc
      _ ≤ (2^(k+1))^2 := Nat.pow_le_pow_left (Nat.lt_two_pow_self (n := k+1)).le 2
      _ = 2^((k+1)*2) := by rw [pow_mul]
      _ ≤ _ := Nat.pow_le_pow_right (by decide : 1 ≤ (2 : ℕ)) (by nlinarith)
  calc
    _ ≤ (k+1)^2 * 2^(3*k) * commonDenominator k r := leftNumerator_bound k r hr
    _ ≤ 2^((k+2)*(k+1)) * 2^(3*k) * 2^(k*(k+1)+2*k+1) :=
      Nat.mul_le_mul (Nat.mul_le_mul_right _ hsmall) (commonDenominator_binary_bound k r)
    _ = _ := by rw [← pow_add, ← pow_add]; congr 1; ring

theorem fromConstant_range (k : ℕ) (e : ℝ) (he : e ∈ Set.Icc 0 1)
    (r : Fin (2*k+2)) :
    (StoredHermiteCoefficients.fromConstant k e).value[r.val] ∈ Set.Icc 0 (2 * coarseBound k) := by
  rw [StoredHermiteCoefficients.fromConstant_value]
  constructor
  · exact add_nonneg (mul_nonneg he.1 (leftCoefficient_nonneg _ _))
      (leftCoefficient_nonneg _ _)
  · have h := mul_le_mul_of_nonneg_right he.2 (leftCoefficient_nonneg k r.val)
    have h1 := leftCoefficient_upper k r.val
    have h2 := leftCoefficient_upper k (2*k+1-r.val)
    nlinarith

def rationalSourceNumerator (k r p q : ℕ) : ℕ :=
  p * leftNumerator k r * commonDenominator k (2*k+1-r) +
  q * leftNumerator k (2*k+1-r) * commonDenominator k r

def rationalSourceDenominator (k r q : ℕ) : ℕ :=
  q * commonDenominator k r * commonDenominator k (2*k+1-r)

theorem rationalSourceDenominator_pos (k r q : ℕ) (hr : r ≤ 2*k+1) (hq : 0 < q) :
    0 < rationalSourceDenominator k r q :=
  Nat.mul_pos (Nat.mul_pos hq (commonDenominator_pos k r hr))
    (commonDenominator_pos k _ (Nat.sub_le _ _))

theorem rationalSource_value (k r p q : ℕ) (hr : r ≤ 2*k+1) (hq : 0 < q) :
    (p : ℝ)/(q : ℝ)*leftCoefficient k r + leftCoefficient k (2*k+1-r) =
      (rationalSourceNumerator k r p q : ℝ)/(rationalSourceDenominator k r q : ℝ) := by
  have hq' : (q : ℝ) ≠ 0 := by exact_mod_cast hq.ne'
  have hD : (commonDenominator k r : ℝ) ≠ 0 := by
    exact_mod_cast (commonDenominator_pos k r hr).ne'
  have hD' : (commonDenominator k (2*k+1-r) : ℝ) ≠ 0 := by
    exact_mod_cast (commonDenominator_pos k _ (Nat.sub_le _ _)).ne'
  rw [leftNumerator_value, leftNumerator_value]
  simp only [rationalSourceNumerator, rationalSourceDenominator, Nat.cast_add, Nat.cast_mul]
  field_simp

theorem rationalSourceDenominator_bound (k r q : ℕ) :
    rationalSourceDenominator k r q ≤ q * 2^(2*(k*(k+1)+2*k+1)) := by
  unfold rationalSourceDenominator
  calc
    _ ≤ q * 2^(k*(k+1)+2*k+1) * 2^(k*(k+1)+2*k+1) :=
      Nat.mul_le_mul (Nat.mul_le_mul_left q (commonDenominator_binary_bound k r))
        (commonDenominator_binary_bound k _)
    _ = _ := by rw [Nat.mul_assoc, ← pow_add]; congr 2; ring

theorem rationalSourceNumerator_bound (k r p q : ℕ) (hr : r ≤ 2*k+1) :
    rationalSourceNumerator k r p q ≤
      (p+q) * 2^((k+2)*(k+1)+2*k*(k+1)+7*k+2) := by
  let A := 2^((k+2)*(k+1)+k*(k+1)+5*k+1)
  let D := 2^(k*(k+1)+2*k+1)
  have hA := leftNumerator_binary_bound k r hr
  have hA' := leftNumerator_binary_bound k (2*k+1-r) (Nat.sub_le _ _)
  have hD := commonDenominator_binary_bound k r
  have hD' := commonDenominator_binary_bound k (2*k+1-r)
  calc
    _ ≤ p * A * D + q * A * D :=
      Nat.add_le_add (Nat.mul_le_mul (Nat.mul_le_mul_left p hA) hD')
        (Nat.mul_le_mul (Nat.mul_le_mul_left q hA') hD)
    _ = (p+q) * (A * D) := by ring
    _ = _ := by
      dsimp [A, D]
      rw [← pow_add]
      congr 2
      ring

#check sourceCoefficient_upper
#check leftCoefficient_upper
#check sourceBernsteinCoefficient_range
#check restricted_source_range
#check factorial_output_bound
#check commonDenominator_bound
#check commonDenominator_pos
#print axioms sourceCoefficient_upper
#print axioms leftCoefficient_upper
#print axioms sourceBernsteinCoefficient_range
#print axioms restricted_source_range
#print axioms factorial_output_bound
#print axioms commonDenominator_bound
#print axioms commonDenominator_pos
#check sourceNumerator_value
#check leftNumerator_value
#check leftNumerator_bound
#check commonDenominator_binary_bound
#check leftNumerator_binary_bound
#print axioms sourceNumerator_value
#print axioms leftNumerator_value
#print axioms leftNumerator_bound
#print axioms commonDenominator_binary_bound
#print axioms leftNumerator_binary_bound
#check fromConstant_range
#check rationalSource_value
#check rationalSourceDenominator_pos
#check rationalSourceDenominator_bound
#check rationalSourceNumerator_bound
#print axioms fromConstant_range
#print axioms rationalSource_value
#print axioms rationalSourceDenominator_pos
#print axioms rationalSourceDenominator_bound
#print axioms rationalSourceNumerator_bound

end QuantumBlockEncoding.ExperimentalCoefficientRange
