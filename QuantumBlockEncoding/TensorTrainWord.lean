import QuantumBlockEncoding.TensorTrainSchedule
import QuantumBlockEncoding.HermiteBoundaryInjection

/-! Explicit conversion between head-first tensor words, Boolean words, and
little-endian public samples. Reversal is a stated index map, never implicit. -/

namespace QuantumBlockEncoding.TensorTrainWord
open TensorTrainCanonical TensorTrainSchedule RealAmplitudePreparation

def toBasis : {n : Nat} → Word n → PrimitiveBasis n
  | 0, _ => Fin.elim0
  | _ + 1, x => Fin.cons x.1 (toBasis x.2)

theorem toBasis_wordOfBasis {n : Nat} (x : PrimitiveBasis n) :
    toBasis (wordOfBasis x) = x := by
  induction n with
  | zero => exact Subsingleton.elim _ _
  | succ n ih => simpa only [wordOfBasis, toBasis, ih] using Fin.cons_self_tail x

theorem wordOfBasis_toBasis {n : Nat} (x : Word n) :
    wordOfBasis (toBasis x) = x := by
  induction n with
  | zero => cases x; rfl
  | succ n ih => simp [wordOfBasis, toBasis, ih] <;> rfl

def basisEquiv (n : Nat) : Word n ≃ PrimitiveBasis n where
  toFun := toBasis
  invFun := wordOfBasis
  left_inv := wordOfBasis_toBasis
  right_inv := toBasis_wordOfBasis

def reverseBasis (n : Nat) : PrimitiveBasis n ≃ PrimitiveBasis n where
  toFun x := fun i => x i.rev
  invFun x := fun i => x i.rev
  left_inv x := by funext i; simp
  right_inv x := by funext i; simp

def sampleEquiv (n : Nat) : Word n ≃ Fin (gridSize n) :=
  (basisEquiv n).trans ((reverseBasis n).trans (primitiveBasisLEEquiv n))

def toBits : {n : Nat} → Word n → List Bool
  | 0, _ => []
  | _ + 1, x => decide (x.1 = 1) :: toBits x.2

@[simp] theorem toBits_length {n : Nat} (x : Word n) : (toBits x).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [toBits, ih]

theorem primitive_snoc_value (n : Nat) (x : PrimitiveBasis n) (bit : Fin 2) :
    (primitiveBasisLEEquiv (n + 1) (Fin.snoc x bit)).val =
      (primitiveBasisLEEquiv n x).val + 2 ^ n * bit.val := by
  induction n with
  | zero => simp [primitiveBasisLEEquiv_succ_value, Fin.snoc]
  | succ n ih =>
    rw [primitiveBasisLEEquiv_succ_value]
    have ht : (fun w : Fin (n + 1) =>
        (Fin.snoc x bit : PrimitiveBasis (n + 2)) w.succ) =
        (Fin.snoc (Fin.tail x) bit : PrimitiveBasis (n + 1)) := by
      funext w
      refine Fin.lastCases ?_ (fun i => ?_) w
      · simp
      · rw [show i.castSucc.succ = i.succ.castSucc from rfl]
        simp only [Fin.snoc_castSucc]
        rfl
    rw [ht, ih, primitiveBasisLEEquiv_succ_value]
    simp only [Fin.snoc_apply_zero]
    change (x 0).val + 2 * ((primitiveBasisLEEquiv n (Fin.tail x)).val + 2 ^ n * bit.val) =
      (x 0).val + 2 * (primitiveBasisLEEquiv n (Fin.tail x)).val + 2 ^ (n + 1) * bit.val
    rw [pow_succ]
    ring

theorem sampleEquiv_value {n : Nat} (x : Word n) :
    (sampleEquiv n x).val = HermiteBoundaryInjection.wordValue (toBits x) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rcases x with ⟨bit, x⟩
    change (primitiveBasisLEEquiv (n + 1)
      (fun i => (Fin.cons bit (toBasis x) : PrimitiveBasis (n + 1)) i.rev)).val = _
    have hr : (fun i : Fin (n + 1) =>
        (Fin.cons bit (toBasis x) : PrimitiveBasis (n + 1)) i.rev) =
        (Fin.snoc (fun i => toBasis x i.rev) bit : PrimitiveBasis (n + 1)) :=
      Fin.cons_comp_rev bit (toBasis x)
    rw [hr, primitive_snoc_value]
    change (sampleEquiv n x).val + 2 ^ n * bit.val = _
    rw [ih]
    fin_cases bit <;> simp [toBits, HermiteBoundaryInjection.wordValue, Nat.add_comm]

theorem wordSampleIndex_eq (n : Nat) (x : Word (n + 1)) :
    HermiteBoundaryInjection.wordSampleIndex n (toBits x) (toBits_length x) =
      sampleEquiv (n + 1) x := by
  apply Fin.ext
  exact (sampleEquiv_value x).symm

theorem sampleEquiv_public {n : Nat} (x : PrimitiveBasis n) :
    sampleEquiv n (wordOfBasis (fun i => x i.rev)) = primitiveBasisLEEquiv n x := by
  change primitiveBasisLEEquiv n
    (fun i => toBasis (wordOfBasis (fun j => x j.rev)) i.rev) = _
  simp only [toBasis_wordOfBasis, Fin.rev_rev]

end QuantumBlockEncoding.TensorTrainWord
