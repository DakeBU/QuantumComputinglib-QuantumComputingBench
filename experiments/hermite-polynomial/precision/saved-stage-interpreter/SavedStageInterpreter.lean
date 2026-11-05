import SavedRounding
import Mathlib.Data.Nat.Bitwise
import Mathlib.Data.Matrix.Basic

/-! Internal literal full-matrix interval interpreter. Physical q0 is LSB.
No Python runtime refinement, stage partition, contraction, or ROOT claim. -/
namespace HermiteSavedStageInterpreter
open HermiteSavedRounding

abbrev Basis (width : ℕ) := Fin (2 ^ width)
abbrev IntervalMatrix (width : ℕ) := Matrix (Basis width) (Basis width) Interval
abbrev RealMatrix (width : ℕ) := Matrix (Basis width) (Basis width) ℝ

def flip {width : ℕ} (q : Fin width) (i : Basis width) : Basis width :=
  ⟨i.val ^^^ 2 ^ q.val, Nat.xor_lt_two_pow i.isLt
    (pow_lt_pow_right₀ (by norm_num : 1 < (2 : ℕ)) q.isLt)⟩
def bit {width : ℕ} (q : Fin width) (i : Basis width) : Bool := i.val.testBit q.val
def low {width : ℕ} (q : Fin width) (i : Basis width) : Basis width :=
  if bit q i then flip q i else i
def high {width : ℕ} (q : Fin width) (i : Basis width) : Basis width :=
  if bit q i then i else flip q i
def cxRow {width : ℕ} (control target : Fin width) (i : Basis width) : Basis width :=
  if bit control i then flip target i else i

inductive Instruction (width : ℕ) where
  | ry (theta : ℚ) (target : Fin width)
  | cx (control target : Fin width) (distinct : control ≠ target)

def intervalIdentity {width : ℕ} : IntervalMatrix width :=
  fun i j => if i = j then ⟨1, 1⟩ else ⟨0, 0⟩
def realIdentity {width : ℕ} : RealMatrix width :=
  fun i j => if i = j then 1 else 0
def Encloses {width : ℕ} (a : IntervalMatrix width) (m : RealMatrix width) : Prop :=
  ∀ i j, Mem (a i j) (m i j)

def intervalStep {width : ℕ} (g : Instruction width) (degree bits : ℕ)
    (a : IntervalMatrix width) : IntervalMatrix width :=
  match g with
  | .ry theta q => fun i j =>
      let p := ryRow theta degree bits (a (low q i) j) (a (high q i) j)
      if bit q i then p.2 else p.1
  | .cx c t _ => fun i j => a (cxRow c t i) j

noncomputable def realStep {width : ℕ} (g : Instruction width)
    (m : RealMatrix width) : RealMatrix width :=
  match g with
  | .ry theta q => fun i j =>
      let p := realRyRow theta (m (low q i) j, m (high q i) j)
      if bit q i then p.2 else p.1
  | .cx c t _ => fun i j => m (cxRow c t i) j

def intervalWord {width : ℕ} (word : List (Instruction width)) (degree bits : ℕ)
    (a : IntervalMatrix width) : IntervalMatrix width :=
  word.foldl (fun m g => intervalStep g degree bits m) a
noncomputable def realWord {width : ℕ} (word : List (Instruction width))
    (m : RealMatrix width) : RealMatrix width := word.foldl (fun m g => realStep g m) m

theorem flip_flip {width : ℕ} (q : Fin width) (i : Basis width) :
    flip q (flip q i) = i := by
  apply Fin.ext
  simp [flip, Nat.xor_assoc]

theorem bit_flip {width : ℕ} (q : Fin width) (i : Basis width) :
    bit q (flip q i) = !(bit q i) := by
  simp [bit, flip, Nat.testBit_xor, Nat.testBit_two_pow]

theorem bit_flip_other {width : ℕ} (q t : Fin width) (hne : q ≠ t) (i : Basis width) :
    bit q (flip t i) = bit q i := by
  have hv : q.val ≠ t.val := fun h => hne (Fin.ext h)
  simp [bit, flip, Nat.testBit_xor, Nat.testBit_two_pow, hv, Ne.symm hv]

theorem cxRow_involutive {width : ℕ} (c t : Fin width) (hne : c ≠ t) (i : Basis width) :
    cxRow c t (cxRow c t i) = i := by
  by_cases h : bit c i = true
  · simp [cxRow, h, bit_flip_other c t hne, flip_flip]
  · simp [cxRow, h]

theorem identity_encloses {width : ℕ} :
    Encloses (intervalIdentity : IntervalMatrix width) realIdentity := by
  intro i j
  by_cases h : i = j <;> simp [intervalIdentity, realIdentity, h, Mem]

theorem step_encloses {width : ℕ} (g : Instruction width) (degree bits : ℕ)
    (a : IntervalMatrix width) (m : RealMatrix width) (h : Encloses a m) :
    Encloses (intervalStep g degree bits a) (realStep g m) := by
  intro i j
  cases g with
  | ry theta q =>
      have hp := ryRow_mem theta degree bits (a (low q i) j) (a (high q i) j)
        (m (low q i) j) (m (high q i) j) (h _ _) (h _ _)
      by_cases hb : bit q i = true
      · simpa [intervalStep, realStep, realRyRow, hb] using hp.2
      · simpa [intervalStep, realStep, realRyRow, hb] using hp.1
  | cx c t hne => exact h (cxRow c t i) j

theorem word_encloses {width : ℕ} (word : List (Instruction width)) (degree bits : ℕ)
    (a : IntervalMatrix width) (m : RealMatrix width) (h : Encloses a m) :
    Encloses (intervalWord word degree bits a) (realWord word m) := by
  induction word generalizing a m with
  | nil => exact h
  | cons g rest ih =>
      exact ih (intervalStep g degree bits a) (realStep g m)
        (step_encloses g degree bits a m h)

theorem stage_enclosure {width : ℕ} (word : List (Instruction width)) (degree bits : ℕ)
    (i j : Basis width) :
    Mem (intervalWord word degree bits intervalIdentity i j)
      (realWord word realIdentity i j) :=
  word_encloses word degree bits intervalIdentity realIdentity identity_encloses i j

theorem stage_midpoint_error {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) (i j : Basis width) :
    |realWord word realIdentity i j -
      (midpoint (intervalWord word degree bits intervalIdentity i j) : ℝ)| ≤
      ((((intervalWord word degree bits intervalIdentity i j).hi -
        (intervalWord word degree bits intervalIdentity i j).lo) / 2 : ℚ) : ℝ) :=
  midpoint_error _ _ (stage_enclosure word degree bits i j)

end HermiteSavedStageInterpreter
