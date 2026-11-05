import SavedStageInterpreter
import QuantumBlockEncoding.PrimitiveBasisLE

namespace HermiteLiteralComplexAdapter
open HermiteSavedStageInterpreter QuantumBlockEncoding
-- Only unfold the definition gridSize n = 2^n for elaboration; no new equality axiom.
set_option allowUnsafeReducibility true in
attribute [local reducible] gridSize

theorem encode_testBit (width : ℕ) (b : PrimitiveBasis width) (q : Fin width) :
    (primitiveBasisLEEquiv width b).val.testBit q.val = decide (b q = 1) := by
  induction width with
  | zero => exact Fin.elim0 q
  | succ n ih =>
      rw [primitiveBasisLEEquiv_succ_value]
      have hb : (b 0).val + 2 * (primitiveBasisLEEquiv n (fun w => b w.succ)).val =
          Nat.bit (decide (b 0 = 1)) (primitiveBasisLEEquiv n (fun w => b w.succ)).val := by
        generalize b 0 = v
        fin_cases v <;> simp [Nat.bit, two_mul] <;> omega
      rw [hb]
      refine Fin.cases ?_ (fun w => ?_) q
      · simp
      · simpa only [Fin.val_succ, Nat.testBit_bit_succ] using ih (fun w => b w.succ) w

theorem decode_bit {width : ℕ} (i : Basis width) (q : Fin width) :
    (primitiveBasisLEEquiv width).symm i q = if bit q i then 1 else 0 := by
  have h := encode_testBit width ((primitiveBasisLEEquiv width).symm i) q
  simp only [Equiv.apply_symm_apply] at h
  change bit q i = decide (((primitiveBasisLEEquiv width).symm i) q = 1) at h
  generalize ((primitiveBasisLEEquiv width).symm i) q = v at *
  fin_cases v <;> simp_all

theorem decode_flip {width : ℕ} (i : Basis width) (q : Fin width) :
    (primitiveBasisLEEquiv width).symm (flip q i) =
      xBasisAction q ((primitiveBasisLEEquiv width).symm i) := by
  funext w
  by_cases hw : w = q
  · subst w
    rw [decode_bit, bit_flip]
    simp only [xBasisAction, Function.update_self]
    rw [decode_bit]
    cases bit q i <;> rfl
  · rw [decode_bit, bit_flip_other w q hw]
    simp [xBasisAction, hw, decode_bit]

theorem decode_cxRow {width : ℕ} (i : Basis width) (c t : Fin width) :
    (primitiveBasisLEEquiv width).symm (cxRow c t i) =
      cxBasisAction c t ((primitiveBasisLEEquiv width).symm i) := by
  unfold cxRow cxBasisAction
  rw [decode_bit]
  cases h : bit c i <;> simp [decode_flip]

theorem decode_low {width : ℕ} (i : Basis width) (q : Fin width) :
    (primitiveBasisLEEquiv width).symm (low q i) =
      (splitPrimitiveWire q).symm
        (0, (splitPrimitiveWire q ((primitiveBasisLEEquiv width).symm i)).2) := by
  apply (splitPrimitiveWire q).injective
  simp only [Equiv.apply_symm_apply]
  apply Prod.ext
  · change ((primitiveBasisLEEquiv width).symm (low q i)) q = 0
    cases h : bit q i <;> simp [low, h, decode_bit, bit_flip]
  · funext w
    change ((primitiveBasisLEEquiv width).symm (low q i)) w.val =
      ((primitiveBasisLEEquiv width).symm i) w.val
    cases h : bit q i <;> simp [low, h, decode_flip, xBasisAction, w.property]

theorem decode_high {width : ℕ} (i : Basis width) (q : Fin width) :
    (primitiveBasisLEEquiv width).symm (high q i) =
      (splitPrimitiveWire q).symm
        (1, (splitPrimitiveWire q ((primitiveBasisLEEquiv width).symm i)).2) := by
  apply (splitPrimitiveWire q).injective
  simp only [Equiv.apply_symm_apply]
  apply Prod.ext
  · change ((primitiveBasisLEEquiv width).symm (high q i)) q = 1
    cases h : bit q i <;> simp [high, h, decode_bit, bit_flip]
  · funext w
    change ((primitiveBasisLEEquiv width).symm (high q i)) w.val =
      ((primitiveBasisLEEquiv width).symm i) w.val
    cases h : bit q i <;> simp [high, h, decode_flip, xBasisAction, w.property]

end HermiteLiteralComplexAdapter
