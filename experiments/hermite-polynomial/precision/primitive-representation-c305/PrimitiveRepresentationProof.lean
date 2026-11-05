import Definitions
import Mathlib.Data.Int.Basic
import Mathlib.Algebra.Order.Ring.Int
import Mathlib.Order.MinMax

namespace HermiteRationalHeight

/-- An internal canonical-reduction bridge; positivity will be discharged for
the literal rawWitness in every operation branch, not supplied by the caller. -/
private theorem witnessReduction (w : Witness) (hw : 0 < w.denominator) :
    (witnessValue w).den ∣ w.denominator ∧
      (witnessValue w).num.natAbs ≤ w.numerator.natAbs ∧
      height (witnessValue w) ≤ witnessWidth w := by
  have hdZ : (w.denominator : ℤ) ≠ 0 := Int.natCast_ne_zero.mpr (Nat.ne_of_gt hw)
  have hpair : witnessValue w = Rat.divInt w.numerator (w.denominator : ℤ) := by
    unfold witnessValue
    rw [← Int.cast_natCast w.denominator, Rat.intCast_div_eq_divInt]
  have hden : (witnessValue w).den ∣ w.denominator := by
    apply Int.natCast_dvd_natCast.mp
    rw [hpair]
    exact Rat.den_dvd w.numerator (w.denominator : ℤ)
  have hnumDvd : (witnessValue w).num ∣ w.numerator := by
    rw [hpair]
    exact Rat.num_dvd w.numerator hdZ
  have hnum : (witnessValue w).num.natAbs ≤ w.numerator.natAbs := by
    by_cases hz : w.numerator = 0
    · have hzero : witnessValue w = 0 := by simp [witnessValue, hz]
      simpa only [hzero, Rat.num_zero, hz, Int.natAbs_zero] using (Nat.le_refl 0)
    · exact Int.natAbs_le_of_dvd_ne_zero hnumDvd hz
  have hdenLe : (witnessValue w).den ≤ w.denominator := Nat.le_of_dvd hw hden
  have hh : height (witnessValue w) ≤ witnessWidth w := by
    dsimp only [height, witnessWidth, integerBits]
    exact max_le_max (le_refl 1)
      (max_le_max (Nat.size_le_size hnum) (Nat.size_le_size hdenLe))
  exact ⟨hden, hnum, hh⟩

/-- Exact canonical result versus the sealed literal unreduced pair.
No extra sign, nonzero-divisor, cache or producer premise is assumed. -/
theorem primitiveRepresentation : PrimitiveRepresentationSpec := by
  unfold PrimitiveRepresentationSpec
  intro op x y
  have hpos : 0 < (rawWitness op x y).denominator := by
    cases op with
    | add => exact Nat.mul_pos (Rat.pos x) (Rat.pos y)
    | sub => exact Nat.mul_pos (Rat.pos x) (Rat.pos y)
    | mul => exact Nat.mul_pos (Rat.pos x) (Rat.pos y)
    | div =>
      by_cases hy : y.num = 0
      · simpa only [rawWitness, if_pos hy] using Nat.zero_lt_one
      · have hyabs : 0 < y.num.natAbs := by
          apply Nat.pos_of_ne_zero
          intro hz
          apply hy
          have heq : (y.num.natAbs : ℤ) = 0 :=
            congrArg (fun z : ℕ => (z : ℤ)) hz
          simpa only [Int.natCast_natAbs, abs_eq_zero] using heq
        simpa only [rawWitness, if_neg hy] using Nat.mul_pos (Rat.pos x) hyabs
  have hvalue : witnessValue (rawWitness op x y) = operationValue op x y := by
    cases op with
    | add =>
      change ((x.num * (y.den : ℤ) + y.num * (x.den : ℤ) : ℤ) : ℚ) /
        ((x.den * y.den : ℕ) : ℚ) = x + y
      rw [← Int.cast_natCast (x.den * y.den), Rat.intCast_div_eq_divInt,
        Int.natCast_mul]
      simpa only [mul_comm] using (Rat.add_num_den x y).symm
    | sub =>
      change ((x.num * (y.den : ℤ) - y.num * (x.den : ℤ) : ℤ) : ℚ) /
        ((x.den * y.den : ℕ) : ℚ) = x - y
      rw [← Int.cast_natCast (x.den * y.den), Rat.intCast_div_eq_divInt,
        Int.natCast_mul]
      simpa only [sub_eq_add_neg, Rat.num_neg_eq_neg_num, Rat.den_neg_eq_den,
        mul_neg, neg_mul, mul_comm] using (Rat.add_num_den x (-y)).symm
    | mul =>
      change ((x.num * y.num : ℤ) : ℚ) / ((x.den * y.den : ℕ) : ℚ) = x * y
      rw [← Int.cast_natCast (x.den * y.den), Rat.intCast_div_eq_divInt]
      exact ((Rat.mul_eq_mkRat x y).trans (Rat.mkRat_eq_divInt _ _)).symm
    | div =>
      by_cases hy : y.num = 0
      · have hyzero : y = 0 := Rat.zero_of_num_zero hy
        subst y
        simp [rawWitness, witnessValue, operationValue]
      · by_cases hyneg : y.num < 0
        · simp only [rawWitness, if_neg hy, if_pos hyneg, witnessValue, operationValue]
          rw [← Int.cast_natCast (x.den * y.num.natAbs), Rat.intCast_div_eq_divInt,
            Int.natCast_mul, Int.natCast_natAbs, abs_of_neg hyneg, mul_neg,
            Rat.divInt_neg, neg_neg]
          exact (Rat.div_def' x y).symm
        · simp only [rawWitness, if_neg hy, if_neg hyneg, witnessValue, operationValue]
          rw [← Int.cast_natCast (x.den * y.num.natAbs), Rat.intCast_div_eq_divInt,
            Int.natCast_mul, Int.natCast_natAbs, abs_of_nonneg (le_of_not_gt hyneg)]
          exact (Rat.div_def' x y).symm
  have hred := witnessReduction (rawWitness op x y) hpos
  rw [hvalue] at hred
  exact ⟨hpos, hvalue, hred.1, hred.2.1, hred.2.2⟩

end HermiteRationalHeight
