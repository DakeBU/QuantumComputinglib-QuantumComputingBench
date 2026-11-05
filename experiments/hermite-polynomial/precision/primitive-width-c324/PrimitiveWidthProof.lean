import Definitions
import Mathlib.Algebra.Order.Ring.Int
import Mathlib.Data.Nat.Cast.Order.Ring
import Mathlib.Order.MinMax

namespace HermiteRationalHeight

private theorem natMulSize {a b A B : ℕ}
    (ha : Nat.size a ≤ A) (hb : Nat.size b ≤ B) : Nat.size (a * b) ≤ A + B := by
  apply Nat.size_le.mpr
  have ha' : a < 2^A := Nat.size_le.mp ha
  have hb' : b < 2^B := Nat.size_le.mp hb
  rw [pow_add]
  exact lt_of_le_of_lt (Nat.mul_le_mul_left a hb'.le)
    (Nat.mul_lt_mul_of_pos_right ha' (pow_pos (by decide : 0 < (2 : ℕ)) B))

private theorem intMulBits {a b : ℤ} {A B : ℕ}
    (ha : integerBits a ≤ A) (hb : integerBits b ≤ B) :
    integerBits (a * b) ≤ A + B := by
  simpa only [integerBits, Int.natAbs_mul] using
    (natMulSize (a := a.natAbs) (b := b.natAbs) ha hb)

private theorem intAddBits {a b : ℤ} {B : ℕ}
    (ha : integerBits a ≤ B) (hb : integerBits b ≤ B) :
    integerBits (a + b) ≤ B + 1 := by
  change Nat.size (a + b).natAbs ≤ B + 1
  apply Nat.size_le.mpr
  have ha' : a.natAbs < 2^B := Nat.size_le.mp ha
  have hb' : b.natAbs < 2^B := Nat.size_le.mp hb
  have htri : (a + b).natAbs ≤ a.natAbs + b.natAbs := by
    apply (Nat.cast_le (α := ℤ)).mp
    simpa only [Nat.cast_add, Int.natCast_natAbs] using (abs_add_le a b)
  calc
    (a + b).natAbs ≤ a.natAbs + b.natAbs := htri
    _ < 2^B + 2^B := add_lt_add ha' hb'
    _ = 2^(B + 1) := by rw [pow_succ, mul_two]

private theorem intSubBits {a b : ℤ} {B : ℕ}
    (ha : integerBits a ≤ B) (hb : integerBits b ≤ B) :
    integerBits (a - b) ≤ B + 1 := by
  have hb' : integerBits (-b) ≤ B := by
    simpa only [integerBits, Int.natAbs_neg] using hb
  simpa only [sub_eq_add_neg] using (intAddBits (a := a) (b := -b) ha hb')

private theorem heightCaps (q : ℚ) :
    1 ≤ height q ∧ integerBits q.num ≤ height q ∧ Nat.size q.den ≤ height q := by
  refine ⟨le_max_left _ _, ?_, ?_⟩
  · exact le_trans (le_max_left _ _) (le_max_right _ _)
  · exact le_trans (le_max_right _ _) (le_max_right _ _)

private theorem pairWidth (w : Witness) (B : ℕ) (h1 : 1 ≤ B)
    (hn : integerBits w.numerator ≤ B) (hd : Nat.size w.denominator ≤ B) :
    witnessWidth w ≤ B := by
  exact max_le_iff.mpr ⟨h1, max_le_iff.mpr ⟨hn, hd⟩⟩

/-- Widths of the exact raw pair and every listed intermediate integer only.
No canonical-result, execution-coverage, native/GCD or caller-bound premise. -/
theorem primitiveWidth : PrimitiveWidthSpec := by
  unfold PrimitiveWidthSpec
  intro op x y
  let S := height x + height y
  have hx := heightCaps x
  have hy := heightCaps y
  have hS : 1 ≤ S := le_trans hx.1 (Nat.le_add_right _ _)
  have hnext : S ≤ S + 1 := Nat.le_succ _
  have hSnext : 1 ≤ S + 1 := le_trans hS hnext
  have hxD : integerBits (x.den : ℤ) ≤ height x := by
    simpa only [integerBits, Int.natAbs_natCast] using hx.2.2
  have hyD : integerBits (y.den : ℤ) ≤ height y := by
    simpa only [integerBits, Int.natAbs_natCast] using hy.2.2
  have hcrossL : integerBits (x.num * (y.den : ℤ)) ≤ S :=
    intMulBits hx.2.1 hyD
  have hcrossR : integerBits (y.num * (x.den : ℤ)) ≤ S := by
    simpa only [S, Nat.add_comm] using (intMulBits hy.2.1 hxD)
  have hmulN : integerBits (x.num * y.num) ≤ S := intMulBits hx.2.1 hy.2.1
  have hden : Nat.size (x.den * y.den) ≤ S := natMulSize hx.2.2 hy.2.2
  have hdivSigned : integerBits ((x.den : ℤ) * y.num) ≤ S :=
    intMulBits hxD hy.2.1
  have hdivDen : Nat.size (x.den * y.num.natAbs) ≤ S := natMulSize hx.2.2 hy.2.1
  cases op with
  | add =>
    have hn : integerBits (rawWitness .add x y).numerator ≤ S + 1 :=
      intAddBits hcrossL hcrossR
    have hd : Nat.size (rawWitness .add x y).denominator ≤ S + 1 := le_trans hden hnext
    refine ⟨pairWidth _ _ hSnext hn hd, ?_⟩
    intro z hz
    simp only [rawIntegers, List.mem_cons, List.mem_singleton, List.mem_nil_iff, or_false] at hz
    rcases hz with rfl | rfl | rfl | rfl
    · exact le_trans hcrossL hnext
    · exact le_trans hcrossR hnext
    · exact hn
    · simpa only [integerBits, Int.natAbs_natCast, operationWidth, S, Nat.add_zero] using hd
  | sub =>
    have hn : integerBits (rawWitness .sub x y).numerator ≤ S + 1 :=
      intSubBits hcrossL hcrossR
    have hd : Nat.size (rawWitness .sub x y).denominator ≤ S + 1 := le_trans hden hnext
    refine ⟨pairWidth _ _ hSnext hn hd, ?_⟩
    intro z hz
    simp only [rawIntegers, List.mem_cons, List.mem_singleton, List.mem_nil_iff, or_false] at hz
    rcases hz with rfl | rfl | rfl | rfl
    · exact le_trans hcrossL hnext
    · exact le_trans hcrossR hnext
    · exact hn
    · simpa only [integerBits, Int.natAbs_natCast, operationWidth, S, Nat.add_zero] using hd
  | mul =>
    have hn : integerBits (rawWitness .mul x y).numerator ≤ S := hmulN
    have hd : Nat.size (rawWitness .mul x y).denominator ≤ S := hden
    refine ⟨pairWidth _ _ hS hn hd, ?_⟩
    intro z hz
    simp only [rawIntegers, List.mem_cons, List.mem_singleton, List.mem_nil_iff, or_false] at hz
    rcases hz with rfl | rfl
    · exact hn
    · simpa only [integerBits, Int.natAbs_natCast, operationWidth, S, Nat.add_zero] using hd
  | div =>
    have hn : integerBits (rawWitness .div x y).numerator ≤ S := by
      by_cases hy0 : y.num = 0
      · simpa only [rawWitness, if_pos hy0, integerBits, Int.natAbs_zero,
          Nat.size_zero] using (Nat.zero_le S)
      · by_cases hyneg : y.num < 0
        · simpa only [rawWitness, if_neg hy0, if_pos hyneg, integerBits,
            Int.natAbs_neg] using hcrossL
        · simpa only [rawWitness, if_neg hy0, if_neg hyneg] using hcrossL
    have hd : Nat.size (rawWitness .div x y).denominator ≤ S := by
      by_cases hy0 : y.num = 0
      · simpa only [rawWitness, if_pos hy0, Nat.size_one] using hS
      · simpa only [rawWitness, if_neg hy0] using hdivDen
    refine ⟨pairWidth _ _ hS hn hd, ?_⟩
    intro z hz
    simp only [rawIntegers, List.mem_cons, List.mem_singleton, List.mem_nil_iff, or_false] at hz
    rcases hz with rfl | rfl | rfl | rfl
    · exact hcrossL
    · exact hdivSigned
    · exact hn
    · simpa only [integerBits, Int.natAbs_natCast, operationWidth, S, Nat.add_zero] using hd

end HermiteRationalHeight
