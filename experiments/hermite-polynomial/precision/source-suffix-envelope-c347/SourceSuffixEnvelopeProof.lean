import SourceSuffixDefinitions
import Mathlib.Data.Rat.Lemmas
import Mathlib.Data.Nat.Choose.Bounds
import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset

/-! C347: the sealed SECOND mathematical suffix root only.
No source producer, cost model, observation or public premise is changed. -/

namespace HermiteSourceSuffix

open scoped BigOperators

/-- Canonical reduction cannot introduce a denominator outside the supplied
natural denominator. This also holds for a zero supplied denominator, although
the application below uses actual positive factorials. -/
private theorem fraction_den_dvd (a b : ℕ) :
    ((a : ℚ) / (b : ℚ)).den ∣ b := by
  apply Int.natCast_dvd_natCast.mp
  rw [Rat.natCast_div_eq_divInt]
  exact Rat.den_dvd (a : ℤ) (b : ℤ)

/-- A fixed common denominator is retained under a finite sum, by the existing
canonical Rat addition/lcm theorem, not by a product-denominator estimate. -/
private theorem finiteSum_den_dvd (D : ℕ) (f : ℕ → ℚ) (S : Finset ℕ) :
    (∀ r ∈ S, (f r).den ∣ D) → (∑ r ∈ S, f r).den ∣ D := by
  classical
  induction S using Finset.induction_on with
  | empty =>
      intro _
      simp
  | @insert a S ha ih =>
      intro h
      rw [Finset.sum_insert ha]
      exact (Rat.add_den_dvd_lcm _ _).trans
        (Nat.lcm_dvd (h a (Finset.mem_insert_self a S))
          (ih (fun r hr => h r (Finset.mem_insert_of_mem hr))))

/-- Every literal summand is bounded by the same 2^(2*k), including r=0 and
all truncated-subtraction cases. The suffix membership is needed only for
factorial divisibility, not for this upper bound. -/
private theorem sourceTerm_le (k : ℕ) (i : Fin (k+1)) (r : ℕ) :
    (Nat.choose (k+i.val-r) k : ℚ) / (r.factorial : ℚ) ≤
      ((2^(2*k) : ℕ) : ℚ) := by
  have htop : k+i.val-r ≤ 2*k := by
    have hi := i.isLt
    omega
  have hchoose : Nat.choose (k+i.val-r) k ≤ 2^(2*k) :=
    (Nat.choose_le_choose k htop).trans (Nat.choose_le_two_pow (2*k) k)
  have hchooseQ : (Nat.choose (k+i.val-r) k : ℚ) ≤
      ((2^(2*k) : ℕ) : ℚ) := by
    exact_mod_cast hchoose
  have hfactorial : 1 ≤ r.factorial :=
    Nat.one_le_iff_ne_zero.mpr (Nat.factorial_ne_zero r)
  have hfactorialQ : (1 : ℚ) ≤ (r.factorial : ℚ) := by
    exact_mod_cast hfactorial
  exact (div_le_self (Nat.cast_nonneg _) hfactorialQ).trans hchooseQ

/-- Exact C345 second root: all offsets, including the empty suffix, and all
orders, including k=i=0. All positivity and divisibility are dependencies. -/
theorem suffixEnvelope : SuffixEnvelopeSpec := by
  unfold SuffixEnvelopeSpec
  intro k i s
  dsimp only
  refine ⟨?_, ?_, ?_⟩
  · unfold SourceSuffix
    apply finiteSum_den_dvd
    intro r hr
    have hrk : r ≤ k := by
      have hi := i.isLt
      have hri := (Finset.mem_Ico.mp hr).2
      omega
    exact (fraction_den_dvd _ _).trans (Nat.factorial_dvd_factorial hrk)
  · unfold SourceSuffix
    exact Finset.sum_nonneg (fun r _ =>
      div_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _))
  · unfold SourceSuffix
    calc
      (∑ r ∈ Finset.Ico s.val (i.val+1),
          (Nat.choose (k+i.val-r) k : ℚ) / (r.factorial : ℚ)) ≤
          ∑ _r ∈ Finset.Ico s.val (i.val+1), ((2^(2*k) : ℕ) : ℚ) :=
        Finset.sum_le_sum (fun r _ => sourceTerm_le k i r)
      _ = (((i.val+1-s.val)*2^(2*k) : ℕ) : ℚ) := by
        simp only [Finset.sum_const, Nat.card_Ico, nsmul_eq_mul, Nat.cast_mul]

#check (suffixEnvelope : SuffixEnvelopeSpec)
#print axioms suffixEnvelope

end HermiteSourceSuffix
