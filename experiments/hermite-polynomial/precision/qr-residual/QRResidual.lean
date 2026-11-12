import QuantumBlockEncoding.TensorTrainNormEnvironment
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Normed.Module.Normalize

/-! Exact a-posteriori cross-Gram certificate for an actual stored TT pair.
No QR, orthogonality, rank or exact computed-normalizer premise is used.
The exponentially large vector occurs only in the specification, not the
cross-Gram producer. This is not Python interpreter or circuit refinement. -/

noncomputable section
open scoped BigOperators

namespace QuantumBlockEncoding.ExperimentalQRResidual
open TensorTrainCanonical
open NormedSpace

noncomputable def crossGram : {n l m : ℕ} → Chain n l 1 → Chain n m 1 →
    _root_.Matrix (Fin l) (Fin m) ℝ
  | _, _, _, .nil _, .nil _ => 1
  | _, _, _, .cons A C, .cons B D =>
      ∑ bit : Fin 2, slice A bit * crossGram C D * (slice B bit).transpose

noncomputable def ttVector {n : ℕ} (C : Chain n 1 1) : EuclideanSpace ℝ (Word n) :=
  WithLp.toLp 2 (fun x => contract C x 0 0)

theorem crossGram_eq_sum {n l m : ℕ} (C : Chain n l 1) (D : Chain n m 1) :
    crossGram C D = ∑ x : Word n, contract C x * (contract D x).transpose := by
  induction n generalizing l m with
  | zero =>
    cases C
    cases D
    change (1 : _root_.Matrix (Fin 1) (Fin 1) ℝ) =
      ∑ _x : Unit, (1 : _root_.Matrix (Fin 1) (Fin 1) ℝ) *
        (1 : _root_.Matrix (Fin 1) (Fin 1) ℝ).transpose
    simp
  | succ n ih =>
    cases C with
    | cons A C => cases D with
      | cons B D =>
      change (∑ bit : Fin 2, slice A bit * crossGram C D * (slice B bit).transpose) =
        ∑ x : Fin 2 × Word n, (slice A x.1 * contract C x.2) *
          (slice B x.1 * contract D x.2).transpose
      rw [Fintype.sum_prod_type, ih]
      simp only [_root_.Matrix.transpose_mul, _root_.Matrix.mul_sum,
        _root_.Matrix.sum_mul, _root_.Matrix.mul_assoc]

theorem crossGram_scalar {n : ℕ} (C D : Chain n 1 1) :
    crossGram C D 0 0 = ∑ x : Word n, contract C x 0 0 * contract D x 0 0 := by
  rw [crossGram_eq_sum]
  simp [_root_.Matrix.sum_apply, _root_.Matrix.mul_apply, _root_.Matrix.transpose_apply]

theorem gram_vector_norm_sq {n : ℕ} (C : Chain n 1 1) :
    TensorTrainNormEnvironment.gram C 0 0 = ‖ttVector C‖ ^ 2 := by
  rw [TensorTrainNormEnvironment.gram_scalar, EuclideanSpace.real_norm_sq_eq]
  rfl

theorem residual_identity {n : ℕ} (C D : Chain n 1 1) (s : ℝ) :
    ‖ttVector D - s⁻¹ • ttVector C‖ ^ 2 =
      TensorTrainNormEnvironment.gram D 0 0 - 2 * s⁻¹ * crossGram C D 0 0 +
        (s⁻¹) ^ 2 * TensorTrainNormEnvironment.gram C 0 0 := by
  rw [EuclideanSpace.real_norm_sq_eq, TensorTrainNormEnvironment.gram_scalar,
    TensorTrainNormEnvironment.gram_scalar, crossGram_scalar]
  change (∑ x : Word n, (contract D x 0 0 - s⁻¹ * contract C x 0 0) ^ 2) = _
  calc
    _ = ∑ x : Word n, (contract D x 0 0 ^ 2 -
        2 * s⁻¹ * (contract C x 0 0 * contract D x 0 0) +
          (s⁻¹) ^ 2 * contract C x 0 0 ^ 2) := by
      apply Finset.sum_congr rfl
      intro x hx
      ring
    _ = _ := by
      simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib, Finset.mul_sum]

theorem ratio_error_of_square_error {a τ : ℝ} (ha : 0 ≤ a)
    (error : |a ^ 2 - 1| ≤ τ) : |a - 1| ≤ τ := by
  have he := abs_le.mp error
  by_cases h : 1 ≤ a
  · rw [abs_of_nonneg (by linarith)]
    nlinarith [sq_nonneg (a - 1)]
  · rw [abs_of_nonpos (by linarith)]
    have hm : 0 ≤ a * (1 - a) := mul_nonneg ha (by linarith)
    nlinarith

theorem certificate_to_normalized {n : ℕ} (C D : Chain n 1 1) {s r τ : ℝ}
    (hs : 0 < s) (hr : 0 ≤ r)
    (raw_positive : 0 < TensorTrainNormEnvironment.gram C 0 0)
    (residual : TensorTrainNormEnvironment.gram D 0 0 -
      2 * s⁻¹ * crossGram C D 0 0 + (s⁻¹) ^ 2 *
        TensorTrainNormEnvironment.gram C 0 0 ≤ r ^ 2)
    (norm_square_error : |(s⁻¹) ^ 2 * TensorTrainNormEnvironment.gram C 0 0 - 1| ≤ τ) :
    ‖ttVector D - normalize (ttVector C)‖ ≤ r + τ := by
  have hC : ttVector C ≠ 0 := by
    intro hz
    rw [gram_vector_norm_sq, hz, norm_zero, zero_pow (by decide)] at raw_positive
    exact lt_irrefl 0 raw_positive
  have hres : ‖ttVector D - s⁻¹ • ttVector C‖ ≤ r := by
    rw [← residual_identity] at residual
    nlinarith [norm_nonneg (ttVector D - s⁻¹ • ttVector C)]
  have hsq : (‖ttVector C‖ / s) ^ 2 =
      (s⁻¹) ^ 2 * TensorTrainNormEnvironment.gram C 0 0 := by
    rw [gram_vector_norm_sq, div_eq_mul_inv]
    ring
  have hratio : |‖ttVector C‖ / s - 1| ≤ τ :=
    ratio_error_of_square_error (div_nonneg (norm_nonneg _) hs.le) (by rwa [hsq])
  have hi : s⁻¹ • ttVector C - normalize (ttVector C) =
      (‖ttVector C‖ / s - 1) • normalize (ttVector C) := by
    rw [sub_smul, one_smul, div_eq_inv_mul, mul_smul, norm_smul_normalize]
  have hn : ‖s⁻¹ • ttVector C - normalize (ttVector C)‖ ≤ τ := by
    rw [hi, norm_smul, Real.norm_eq_abs, norm_normalize hC, mul_one]
    exact hratio
  have ht := norm_add_le (ttVector D - s⁻¹ • ttVector C)
    (s⁻¹ • ttVector C - normalize (ttVector C))
  simp only [sub_add_sub_cancel] at ht
  linarith

def crossUpdateBudget (lC mC lD mD : ℕ) : ℕ :=
  4 * (lC * mC * mD + lC * mD * lD) + lC * lD

theorem crossUpdateBudget_le (lC mC lD mD B : ℕ)
    (hlC : lC ≤ B) (hmC : mC ≤ B) (hlD : lD ≤ B) (hmD : mD ≤ B) :
    crossUpdateBudget lC mC lD mD ≤ 9 * B ^ 3 := by
  have h1 : lC * mC * mD ≤ B * B * B :=
    Nat.mul_le_mul (Nat.mul_le_mul hlC hmC) hmD
  have h2 : lC * mD * lD ≤ B * B * B :=
    Nat.mul_le_mul (Nat.mul_le_mul hlC hmD) hlD
  have h3 : lC * lD ≤ B * B := Nat.mul_le_mul hlC hlD
  have h4 : B * B ≤ B * B * B := by
    by_cases hz : B = 0
    · simp [hz]
    · have hb : 1 ≤ B := by omega
      simpa using Nat.mul_le_mul_left (B * B) hb
  unfold crossUpdateBudget
  nlinarith

def crossArithmeticBudget : {n l m : ℕ} → Chain n l 1 → Chain n m 1 → ℕ
  | _, _, _, .nil _, .nil _ => 0
  | _, l, m, @Chain.cons _ _ p _ _ C, @Chain.cons _ _ q _ _ D =>
      crossUpdateBudget l p m q + crossArithmeticBudget C D

theorem crossArithmeticBudget_le {n l m : ℕ} (C : Chain n l 1) (D : Chain n m 1)
    (B : ℕ) (hC : maxBond C ≤ B) (hD : maxBond D ≤ B) :
    crossArithmeticBudget C D ≤ 9 * n * B ^ 3 := by
  induction n generalizing l m with
  | zero => cases C; cases D; simp [crossArithmeticBudget]
  | succ n ih =>
    cases C with
    | @cons _ l p _ A C => cases D with
      | @cons _ m q _ E D =>
      have hl := (max_le_iff.mp hC).1
      have hc := (max_le_iff.mp hC).2
      have hm := (max_le_iff.mp hD).1
      have hd := (max_le_iff.mp hD).2
      have hp : p ≤ B := by
        cases C with
        | nil _ => exact hc
        | cons _ _ => exact (max_le_iff.mp hc).1
      have hq : q ≤ B := by
        cases D with
        | nil _ => exact hd
        | cons _ _ => exact (max_le_iff.mp hd).1
      have hu := crossUpdateBudget_le l p m q B hl hp hm hq
      have ht := ih C D hc hd
      simp only [crossArithmeticBudget]
      nlinarith

def certificateArithmeticBudget {n : ℕ} (C D : Chain n 1 1) : ℕ :=
  crossArithmeticBudget C C + crossArithmeticBudget D D + crossArithmeticBudget C D

theorem certificateArithmeticBudget_le {n : ℕ} (C D : Chain n 1 1) (B : ℕ)
    (hC : maxBond C ≤ B) (hD : maxBond D ≤ B) :
    certificateArithmeticBudget C D ≤ 27 * n * B ^ 3 := by
  have h1 := crossArithmeticBudget_le C C B hC hC
  have h2 := crossArithmeticBudget_le D D B hD hD
  have h3 := crossArithmeticBudget_le C D B hC hD
  unfold certificateArithmeticBudget
  nlinarith

#check crossGram_eq_sum
#check crossGram_scalar
#check gram_vector_norm_sq
#check residual_identity
#check ratio_error_of_square_error
#check certificate_to_normalized
#check crossUpdateBudget_le
#check crossArithmeticBudget_le
#check certificateArithmeticBudget_le
#print axioms crossGram_eq_sum
#print axioms crossGram_scalar
#print axioms gram_vector_norm_sq
#print axioms residual_identity
#print axioms ratio_error_of_square_error
#print axioms certificate_to_normalized
#print axioms crossUpdateBudget_le
#print axioms crossArithmeticBudget_le
#print axioms certificateArithmeticBudget_le

end QuantumBlockEncoding.ExperimentalQRResidual
