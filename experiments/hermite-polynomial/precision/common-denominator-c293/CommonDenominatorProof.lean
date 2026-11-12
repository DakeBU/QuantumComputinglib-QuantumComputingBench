import HeightBoundProof
import Mathlib.Data.Nat.Cast.Order.Ring
import Mathlib.Algebra.Order.GroupWithZero.Basic

namespace HermiteRationalHeight

/-- The literal commonWitness, including signed and zero numerators.
Its assumptions are precisely the sealed local mathematical bridge conditions. -/
theorem commonDenominator : CommonDenominatorSpec := by
  unfold CommonDenominatorSpec
  intro q Q M hQ hdiv hmag
  have hdQ : q.den ≤ Q := Nat.le_of_dvd hQ hdiv
  have hquot : (Q / q.den) * q.den = Q := Nat.div_mul_cancel hdiv
  have hdRat : (0 : ℚ) < (q.den : ℚ) := Nat.cast_pos.mpr (Rat.pos q)
  have hQRat : (0 : ℚ) < (Q : ℚ) := Nat.cast_pos.mpr hQ
  have habs : |q| = (q.num.natAbs : ℚ) / (q.den : ℚ) := by
    rw [Rat.abs_def, Rat.natCast_div_eq_divInt]
  have hnRat : (q.num.natAbs : ℚ) ≤ (M : ℚ) * (q.den : ℚ) :=
    (div_le_iff₀ hdRat).mp (habs ▸ hmag)
  have hn : q.num.natAbs ≤ M * q.den := by
    apply (Nat.cast_le (α := ℚ)).mp
    simpa only [Nat.cast_mul] using hnRat
  have hnQ : q.num.natAbs ≤ M * Q :=
    le_trans hn (Nat.mul_le_mul_left M hdQ)
  have hcross :
      ((q.num * ((Q / q.den : ℕ) : ℤ) : ℤ) : ℚ) = q * (Q : ℚ) := by
    rw [Int.cast_mul, Int.cast_natCast, ← Rat.mul_den_eq_num q,
      mul_assoc, mul_comm (q.den : ℚ) ((Q / q.den : ℕ) : ℚ),
      ← Nat.cast_mul, hquot]
  have hvalue : witnessValue (commonWitness q Q) = q := by
    change ((q.num * ((Q / q.den : ℕ) : ℤ) : ℤ) : ℚ) / (Q : ℚ) = q
    exact (div_eq_iff hQRat.ne').mpr hcross
  have hraw : (commonWitness q Q).numerator.natAbs ≤ M * Q := by
    change (q.num * ((Q / q.den : ℕ) : ℤ)).natAbs ≤ M * Q
    rw [Int.natAbs_mul, Int.natAbs_natCast]
    calc
      q.num.natAbs * (Q / q.den) ≤ (M * q.den) * (Q / q.den) :=
        Nat.mul_le_mul_right _ hn
      _ = M * Q := by
        rw [Nat.mul_assoc, Nat.mul_comm q.den (Q / q.den), hquot]
  have hh : height q ≤ max 1 (max (Nat.size (M * Q)) (Nat.size Q)) := by
    apply (heightBound q _).mpr
    refine ⟨le_max_left _ _, ?_, ?_⟩
    · apply Nat.size_le.mp
      exact le_trans (Nat.size_le_size hnQ)
        (le_trans (le_max_left _ _) (le_max_right _ _))
    · apply Nat.size_le.mp
      exact le_trans (Nat.size_le_size hdQ)
        (le_trans (le_max_right _ _) (le_max_right _ _))
  exact ⟨hQ, hvalue, hraw, hh⟩

end HermiteRationalHeight
