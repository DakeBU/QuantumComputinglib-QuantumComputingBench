-- SPDX-License-Identifier: Apache-2.0
-- C230 proof candidate for the exact C229 sealed integer-model statement.
-- Imports the unchanged C227 core; no fixed table is evaluated here.
import GaussianIntegerCore
import Mathlib.Data.List.Range
import Mathlib.Tactic.NormNum
import Lean.Elab.Tactic.Omega

namespace UncomputeGaussian206

private theorem c230_quotient_constancy (D e : Nat) (he : 7 ≤ e) :
    D / 2^e = (128*(D/128)) / 2^e := by
  have hexp : e = 7 + (e-7) := by omega
  have hpow : (2 : Nat)^e = 128 * 2^(e-7) := by
    calc
      (2 : Nat)^e = 2^(7+(e-7)) := congrArg (fun n : Nat => (2 : Nat)^n) hexp
      _ = 2^7 * 2^(e-7) := by rw [Nat.pow_add]
      _ = 128 * 2^(e-7) := by norm_num
  have hround : (128*(D/128))/128 = D/128 := by omega
  calc
    D / 2^e = (D/128) / 2^(e-7) := by
      rw [hpow, Nat.div_div_eq_div_mul]
    _ = ((128*(D/128))/128) / 2^(e-7) := by rw [hround]
    _ = (128*(D/128)) / 2^e := by
      rw [hpow, Nat.div_div_eq_div_mul]

private theorem c230_localU_constancy (D : Nat) :
    localU D = localU (128*(D/128)) := by
  exact c230_quotient_constancy D 14 (by omega)

private theorem c230_middleRow_constancy (j D t : Nat) :
    middleRow j D t = middleRow j (128*(D/128)) t := by
  unfold middleRow
  rw [c230_localU_constancy D]

private theorem c230_slopeWord_constancy (j D : Nat) :
    slopeWord j D = slopeWord j (128*(D/128)) := by
  have hstep :
      (fun (s t : Nat) => modBits ((s : Int)+middleRow j D t / 4) 19) =
      (fun (s t : Nat) => modBits ((s : Int)+middleRow j (128*(D/128)) t / 4) 19) := by
    funext s t
    rw [c230_middleRow_constancy j D t]
  unfold slopeWord slopeStored
  rw [hstep]

private theorem c230_finalRow_constancy (F D i : Nat) (hi : 2 ≤ i) (hi' : i ≤ 10) :
    finalRow F D i = finalRow F (128*(D/128)) i := by
  have hsecond : 7 ≤ finalShift i - 1 + finalDrop i := by
    by_cases hsmall : i ≤ 9
    · have hdrop : 6 ≤ finalDrop i := by
        unfold finalDrop
        exact le_max_left _ _
      have hshift : 3 ≤ finalShift i := by
        unfold finalShift
        omega
      omega
    · have hten : i = 10 := by omega
      subst i
      norm_num [finalShift, finalDrop]
  have hfirst : 7 ≤ finalShift i + finalDrop i := by omega
  have hq1 := c230_quotient_constancy D (finalShift i + finalDrop i) hfirst
  have hq2 := c230_quotient_constancy D (finalShift i - 1 + finalDrop i) hsecond
  dsimp only [finalRow]
  rw [hq1, hq2]

-- Congruence is required only on visited row indices, not on all naturals.
private theorem c230_foldl_congr_on (xs : List Nat) (f g : Int → Nat → Int)
    (h : ∀ r ∈ xs, ∀ s, f s r = g s r) (s : Int) :
    xs.foldl f s = xs.foldl g s := by
  revert h s
  induction xs with
  | nil =>
      intro h s
      rfl
  | cons r rs ih =>
      intro h s
      change rs.foldl f (f s r) = rs.foldl g (g s r)
      have hr : f s r = g s r := h r (by simp) s
      rw [hr]
      apply ih
      intro q hq t
      exact h q (by simp only [List.mem_cons]; exact Or.inr hq) t

private theorem c230_finalSum_constancy (F D : Nat) :
    finalSum F D = finalSum F (128*(D/128)) := by
  unfold finalSum
  apply c230_foldl_congr_on
  intro r hr s
  have hr' : r < 9 := List.mem_range.mp hr
  rw [c230_finalRow_constancy F D (r+2) (by omega) (by omega)]

/-- The exact C229 sealed statement, retaining both original domain premises. -/
theorem localIncrement_block128_constancy :
  ∀ (j D : Nat), j < 1024 → D < 2^25 →
    localIncrement j D = localIncrement j (128*(D/128)) := by
  intro j D _hj _hD
  unfold localIncrement
  rw [c230_slopeWord_constancy j D,
    c230_finalSum_constancy (slopeWord j (128*(D/128))) D]

end UncomputeGaussian206
