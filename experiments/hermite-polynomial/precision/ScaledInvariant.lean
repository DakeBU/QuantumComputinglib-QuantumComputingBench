import QuantumBlockEncoding.HermiteExplicitBond

/-!
Exact mathematical part of `mps/scaled_canonicalize.py` only. Positive
per-core divisions and pre-absorption residual divisions remove a product
scalar without changing the literal signed normalized action. Factors are
supplied exact reals; computing maxima, float QR, underflow, rounded factor
products/logarithms, Python execution and circuit export remain unproved.
The ambient chain, word, local Gram norm and LE adapter are reused unchanged.
-/

namespace QuantumBlockEncoding.ExperimentalScaledInvariant

open TensorTrainCanonical
open scoped BigOperators

/-- Chronological product of removed factors, including empty product one. -/
def factorProduct : {n : ℕ} → (Fin n → ℝ) → ℝ
  | 0, _ => 1
  | _ + 1, factors => factors 0 * factorProduct (Fin.tail factors)

/-- Deterministically divide every core; dimensions and bit labels are unchanged. -/
noncomputable def rescale : {n l r : ℕ} → Chain n l r → (Fin n → ℝ) → Chain n l r
  | _, _, _, .nil r, _ => .nil r
  | _, _, _, .cons A C, factors =>
      .cons ((factors 0)⁻¹ • A) (rescale C (Fin.tail factors))

theorem factorProduct_pos {n : ℕ} (factors : Fin n → ℝ)
    (positive : ∀ i, 0 < factors i) : 0 < factorProduct factors := by
  induction n with
  | zero => simp [factorProduct]
  | succ n ih => exact mul_pos (positive 0) (ih _ (fun i => positive i.succ))

/-- Algebraic law is total, even at zero factors; recovery uses positivity below. -/
theorem contract_rescale {n l r : ℕ} (C : Chain n l r) (factors : Fin n → ℝ)
    (x : Word n) :
    contract (rescale C factors) x = (factorProduct factors)⁻¹ • contract C x := by
  induction C with
  | nil r => simp [rescale, contract, factorProduct]
  | cons A C ih =>
      ext a b
      simp only [rescale, contract, slice, ih, factorProduct, _root_.Matrix.mul_apply,
        _root_.Matrix.smul_apply, smul_eq_mul, mul_inv_rev, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i _
      ring

theorem recover_contract {n l r : ℕ} (C : Chain n l r) (factors : Fin n → ℝ)
    (positive : ∀ i, 0 < factors i) (x : Word n) :
    factorProduct factors • contract (rescale C factors) x = contract C x := by
  rw [contract_rescale, smul_smul, mul_inv_cancel₀ (ne_of_gt (factorProduct_pos factors positive)),
    one_smul]

theorem maxBond_rescale {n l r : ℕ} (C : Chain n l r) (factors : Fin n → ℝ) :
    maxBond (rescale C factors) = maxBond C := by
  induction C with
  | nil r => rfl
  | cons A C ih => simp only [rescale, maxBond, ih]

theorem storedScalars_rescale {n l r : ℕ} (C : Chain n l r) (factors : Fin n → ℝ) :
    MatrixProductChain.storedScalars (rescale C factors) = MatrixProductChain.storedScalars C := by
  induction C with
  | nil r => rfl
  | cons A C ih => simp only [rescale, MatrixProductChain.storedScalars, ih]

theorem norm_rescale {n : ℕ} (C : Chain n 1 1) (factors : Fin n → ℝ)
    (positive : ∀ i, 0 < factors i) :
    TensorTrainNormEnvironment.norm (rescale C factors) =
      TensorTrainNormEnvironment.norm C / factorProduct factors := by
  have squared : TensorTrainNormEnvironment.norm (rescale C factors) ^ 2 =
      (TensorTrainNormEnvironment.norm C / factorProduct factors) ^ 2 := by
    rw [TensorTrainNormEnvironment.norm_sq, div_pow, TensorTrainNormEnvironment.norm_sq]
    simp only [contract_rescale, _root_.Matrix.smul_apply, smul_eq_mul, mul_pow]
    rw [← Finset.mul_sum, inv_pow, ← div_eq_inv_mul]
  apply (sq_eq_sq₀ (Real.sqrt_nonneg _)
    (div_nonneg (Real.sqrt_nonneg _) (factorProduct_pos factors positive).le)).mp
  exact squared

/-- Equality of signed amplitudes, not equality of probabilities/up to phase. -/
theorem normalized_action {n : ℕ} (C : Chain n 1 1) (factors : Fin n → ℝ)
    (positive : ∀ i, 0 < factors i) (nonzero : 0 < TensorTrainNormEnvironment.norm C)
    (x : Word n) :
    contract (rescale C factors) x 0 0 / TensorTrainNormEnvironment.norm (rescale C factors) =
      contract C x 0 0 / TensorTrainNormEnvironment.norm C := by
  rw [norm_rescale C factors positive, contract_rescale]
  simp only [_root_.Matrix.smul_apply, smul_eq_mul]
  field_simp [ne_of_gt (factorProduct_pos factors positive), ne_of_gt nonzero]

/-- The Python residual is scaled before absorption; positive factors recover it. -/
theorem absorb_recovered {l m r : ℕ} (A : Core l m)
    (R : _root_.Matrix (Fin m) (Fin r) ℝ) (a b : ℝ) (ha : 0 < a) (hb : 0 < b) :
    (a * b) • absorb (a⁻¹ • A) (b⁻¹ • R) = absorb A R := by
  ext i out
  simp only [absorb, _root_.Matrix.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j _
  field_simp [ne_of_gt ha, ne_of_gt hb]

/-- Also restore the positive max-scale removed after residual absorption. -/
theorem absorb_rescale_recovered {l m r : ℕ} (A : Core l m)
    (R : _root_.Matrix (Fin m) (Fin r) ℝ) (a b c : ℝ)
    (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    (a * b * c) • (c⁻¹ • absorb (a⁻¹ • A) (b⁻¹ • R)) = absorb A R := by
  rw [smul_smul, mul_assoc, mul_inv_cancel₀ (ne_of_gt hc), mul_one]
  exact absorb_recovered A R a b ha hb

/-- Both explicit signed boundaries remain contracted; neither is discarded. -/
theorem boundary_action {D : ℕ} (K : MatrixProductChain.Kernel D)
    (left right : Fin D → ℝ) (start n : ℕ) (factors : Fin (n + 1) → ℝ)
    (positive : ∀ i, 0 < factors i) (x : Word (n + 1)) :
    factorProduct factors *
      contract (rescale (MatrixProductChain.ofKernel K left right start n) factors) x 0 0 =
        ∑ a, left a * MatrixProductChain.readout K right start x a := by
  have h := congrFun (congrFun (recover_contract
    (MatrixProductChain.ofKernel K left right start n) factors positive x) 0) 0
  simpa only [_root_.Matrix.smul_apply, smul_eq_mul, MatrixProductChain.ofKernel_contract] using h

/-- Literal raw Hermite producer normalized after rescaling, same sample index. -/
theorem hermite_target (k n : ℕ) (L : ℝ) (hL : 0 < L)
    (factors : Fin (n + 1) → ℝ) (positive : ∀ i, 0 < factors i)
    (x : Word (n + 1)) :
    contract (rescale (HermiteExplicitBond.rawSourceChain k n L) factors) x 0 0 /
      TensorTrainNormEnvironment.norm (rescale (HermiteExplicitBond.rawSourceChain k n L) factors) =
        HermiteStatePreparation.sampledAmplitude k (n + 1) L
          (TensorTrainWord.sampleEquiv (n + 1) x) / HermiteStatePreparation.sampleNorm k (n + 1) L := by
  rw [normalized_action _ factors positive (by
    rw [HermiteExplicitBond.rawSourceChain_norm k n L hL]
    exact HermiteStatePreparation.sampleNorm_pos k (n + 1) L)]
  rw [HermiteExplicitBond.rawSourceChain_contract k n L hL,
    HermiteExplicitBond.rawSourceChain_norm k n L hL]

theorem hermite_target_public (k n : ℕ) (L : ℝ) (hL : 0 < L)
    (factors : Fin (n + 1) → ℝ) (positive : ∀ i, 0 < factors i)
    (x : PrimitiveBasis (n + 1)) :
    ((contract (rescale (HermiteExplicitBond.rawSourceChain k n L) factors)
        (TensorTrainSchedule.wordOfBasis (fun i => x i.rev)) 0 0 /
      TensorTrainNormEnvironment.norm (rescale (HermiteExplicitBond.rawSourceChain k n L) factors) : ℝ) : ℂ) =
        HermiteStatePreparation.normalizedAmplitude k (n + 1) L
          (primitiveBasisLEEquiv (n + 1) x) := by
  rw [hermite_target k n L hL factors positive, TensorTrainWord.sampleEquiv_public]
  rfl

-- Focused edge cases: no full-rank assumption; empty product and zero core
-- have algebraic semantics, but the zero train cannot satisfy nonzero norm.
example (r : ℕ) (factors : Fin 0 → ℝ) : rescale (.nil r) factors = .nil r := rfl
example (factors : Fin 0 → ℝ) : factorProduct factors = 1 := rfl
example (factors : Fin 0 → ℝ) : rescale (.nil 0) factors = .nil 0 := rfl
example (factors : Fin 1 → ℝ) (x : Word 1) :
    contract (rescale (.cons (0 : Core 1 1) (.nil 1)) factors) x = 0 := by
  ext a b
  simp [rescale, contract, slice, _root_.Matrix.mul_apply]
example (factors : Fin 1 → ℝ) (positive : ∀ i, 0 < factors i) (x : Word 1) :
    factorProduct factors • contract
      (rescale (.cons (fun (_ : Fin 1) (_ : Fin 2 × Fin 1) => (-3 : ℝ)) (.nil 1)) factors) x =
        contract (.cons (fun (_ : Fin 1) (_ : Fin 2 × Fin 1) => (-3 : ℝ)) (.nil 1)) x :=
  recover_contract _ factors positive x
example (C : Chain 2 1 0) (factors : Fin 2 → ℝ) :
    maxBond (rescale C factors) = maxBond C := maxBond_rescale C factors
example (factors : Fin 1 → ℝ) (positive : ∀ i, 0 < factors i) (x : Word 1) :
    factorProduct factors • contract
      (rescale (.cons (fun (_ : Fin 2) (_ : Fin 2 × Fin 1) => (-3 : ℝ)) (.nil 1)) factors) x =
        contract (.cons (fun (_ : Fin 2) (_ : Fin 2 × Fin 1) => (-3 : ℝ)) (.nil 1)) x :=
  recover_contract _ factors positive x

#check factorProduct_pos
#check contract_rescale
#check recover_contract
#check maxBond_rescale
#check storedScalars_rescale
#check norm_rescale
#check normalized_action
#check absorb_recovered
#check absorb_rescale_recovered
#check boundary_action
#check hermite_target
#check hermite_target_public
#print axioms factorProduct_pos
#print axioms contract_rescale
#print axioms recover_contract
#print axioms maxBond_rescale
#print axioms storedScalars_rescale
#print axioms norm_rescale
#print axioms normalized_action
#print axioms absorb_recovered
#print axioms absorb_rescale_recovered
#print axioms boundary_action
#print axioms hermite_target
#print axioms hermite_target_public

end QuantumBlockEncoding.ExperimentalScaledInvariant
