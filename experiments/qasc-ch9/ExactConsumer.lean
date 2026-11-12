import QuantumBlockEncoding.ConcreteSemantics
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Algebra.Order.BigOperators.Group.Finset

/-! Staged exact consumer of the shared block-encoding semantics.
Source: Lin--Wiebe, QASC (29 April 2026), (9.2), (9.9), (9.10), (9.12).
No alternative block-encoding or quantum-state foundation is introduced. -/

namespace QuantumBlockEncoding.QASCChapter9

open ConcreteSemantics BlockEncodingClassics
open scoped BigOperators

noncomputable def cleanInput {s d : Nat} (a : Fin s) (b : StateVector d ℂ) :
    StateVector (s * d) ℂ :=
  ∑ j : Fin d, b j • basisKet (s * d) (productIndex a j)

noncomputable def cleanOutput {s d : Nat}
    (U : FiniteMatrix (s * d) (s * d) ℂ) (a : Fin s)
    (b : StateVector d ℂ) : StateVector d ℂ :=
  fun i => applyVec U (cleanInput a b) (productIndex a i)

theorem cleanOutput_eq_blockAction {s d : Nat}
    (U : FiniteMatrix (s * d) (s * d) ℂ) (a : Fin s)
    (b : StateVector d ℂ) :
    cleanOutput U a b =
      applyVec (signalSystemBlockProjection s d d U a) b := by
  funext i
  unfold cleanOutput cleanInput
  simp only [applyVec, basisKet, _root_.Matrix.mulVec_sum, _root_.Matrix.mulVec_smul,
    _root_.Matrix.mulVec_single_one, Finset.sum_apply,
    Pi.smul_apply, smul_eq_mul]
  unfold _root_.Matrix.mulVec dotProduct
  apply Finset.sum_congr rfl
  intro j _
  change b j * U (productIndex a i) (productIndex a j) =
    signalSystemBlockProjection s d d U a i j * b j
  rw [mul_comm]
  rfl

theorem scaled_cleanOutput {s d : Nat} (alpha : ℝ)
    (A : FiniteMatrix d d ℂ) (U : FiniteMatrix (s * d) (s * d) ℂ)
    (a : Fin s) (b : StateVector d ℂ)
    (hBlock : ∀ i j, A i j = (alpha : ℂ) *
      signalSystemBlockProjection s d d U a i j) :
    (alpha : ℂ) • cleanOutput U a b = applyVec A b := by
  rw [cleanOutput_eq_blockAction]
  have hA : A = (alpha : ℂ) • signalSystemBlockProjection s d d U a := by
    ext i j
    exact hBlock i j
  rw [hA]
  exact (_root_.Matrix.smul_mulVec _ _ _).symm

private theorem weight_nonneg {d : Nat} (v : StateVector d ℂ) :
    0 ≤ ∑ i, Complex.normSq (v i) :=
  Finset.sum_nonneg fun _ _ => Complex.normSq_nonneg _

private theorem weight_eq_zero_iff {d : Nat} (v : StateVector d ℂ) :
    (∑ i, Complex.normSq (v i)) = 0 ↔ v = 0 := by
  rw [Finset.sum_eq_zero_iff_of_nonneg (fun i _ => Complex.normSq_nonneg (v i))]
  simp only [Finset.mem_univ, forall_true_left, Complex.normSq_eq_zero]
  exact ⟨fun h => funext h, fun h i => congrFun h i⟩

theorem exact_weight {s d : Nat} (alpha : ℝ)
    (A : FiniteMatrix d d ℂ) (U : FiniteMatrix (s * d) (s * d) ℂ)
    (a : Fin s) (b : StateVector d ℂ) (hAlpha : 0 < alpha)
    (hBlock : ∀ i j, A i j = (alpha : ℂ) *
      signalSystemBlockProjection s d d U a i j) :
    (∑ i, Complex.normSq (cleanOutput U a b i)) =
      (∑ i, Complex.normSq (applyVec A b i)) / alpha ^ 2 := by
  have h := scaled_cleanOutput alpha A U a b hBlock
  have hw : (∑ i, Complex.normSq (applyVec A b i)) =
      alpha ^ 2 * (∑ i, Complex.normSq (cleanOutput U a b i)) := by
    rw [← h]
    simp only [Pi.smul_apply, smul_eq_mul, Complex.normSq_mul, Complex.normSq_ofReal]
    rw [← Finset.mul_sum]
    ring
  rw [hw]
  field_simp

theorem positive_weight_iff {s d : Nat} (alpha : ℝ)
    (A : FiniteMatrix d d ℂ) (U : FiniteMatrix (s * d) (s * d) ℂ)
    (a : Fin s) (b : StateVector d ℂ) (hAlpha : 0 < alpha)
    (hBlock : ∀ i j, A i j = (alpha : ℂ) *
      signalSystemBlockProjection s d d U a i j) :
    0 < (∑ i, Complex.normSq (cleanOutput U a b i)) ↔ applyVec A b ≠ 0 := by
  rw [exact_weight alpha A U a b hAlpha hBlock,
    div_pos_iff_of_pos_right (sq_pos_of_pos hAlpha)]
  constructor
  · intro hp hz
    have hw := (weight_eq_zero_iff (applyVec A b)).mpr hz
    linarith
  · intro hz
    apply lt_of_le_of_ne (weight_nonneg (applyVec A b))
    intro heq
    exact hz ((weight_eq_zero_iff (applyVec A b)).mp heq.symm)

theorem normalized_cleanOutput {s d : Nat} (alpha : ℝ)
    (A : FiniteMatrix d d ℂ) (U : FiniteMatrix (s * d) (s * d) ℂ)
    (a : Fin s) (b : StateVector d ℂ) (hAlpha : 0 < alpha)
    (hBlock : ∀ i j, A i j = (alpha : ℂ) *
      signalSystemBlockProjection s d d U a i j)
    (hImage : applyVec A b ≠ 0) :
    ∀ i, cleanOutput U a b i /
        (Real.sqrt (∑ j, Complex.normSq (cleanOutput U a b j)) : ℂ) =
      applyVec A b i / (Real.sqrt (∑ j, Complex.normSq (applyVec A b j)) : ℂ) := by
  have hScale := scaled_cleanOutput alpha A U a b hBlock
  have hWeight := exact_weight alpha A U a b hAlpha hBlock
  have hcpos := (positive_weight_iff alpha A U a b hAlpha hBlock).mpr hImage
  have hRoot : Real.sqrt (∑ j, Complex.normSq (applyVec A b j)) =
      alpha * Real.sqrt (∑ j, Complex.normSq (cleanOutput U a b j)) := by
    have hw : (∑ j, Complex.normSq (applyVec A b j)) =
        alpha ^ 2 * (∑ j, Complex.normSq (cleanOutput U a b j)) := by
      have ha : alpha ^ 2 ≠ 0 := ne_of_gt (sq_pos_of_pos hAlpha)
      exact (eq_div_iff ha).mp hWeight |>.symm.trans (mul_comm _ _)
    rw [hw, Real.sqrt_mul (sq_nonneg alpha), Real.sqrt_sq_eq_abs,
      abs_of_pos hAlpha]
  intro i
  rw [hRoot, Complex.ofReal_mul, ← congrFun hScale i]
  change _ = (alpha : ℂ) * cleanOutput U a b i /
    ((alpha : ℂ) * (Real.sqrt (∑ j, Complex.normSq (cleanOutput U a b j)) : ℂ))
  have ha : (alpha : ℂ) ≠ 0 := by exact_mod_cast ne_of_gt hAlpha
  field_simp

/-- The explicit conditional normalized vector really has Born weight one.
This is an internal scalar provider, not a new state/measurement API. -/
theorem normalized_vector_weight {d : Nat} (v : StateVector d ℂ) (hv : v ≠ 0) :
    (∑ i, Complex.normSq
      (v i / (Real.sqrt (∑ j, Complex.normSq (v j)) : ℂ))) = 1 := by
  have hp : 0 < ∑ j, Complex.normSq (v j) := by
    apply lt_of_le_of_ne (weight_nonneg v)
    intro heq
    exact hv ((weight_eq_zero_iff v).mp heq.symm)
  simp only [Complex.normSq_div, Complex.normSq_ofReal]
  rw [Real.mul_self_sqrt (weight_nonneg v)]
  simp only [div_eq_mul_inv]
  rw [← Finset.sum_mul, mul_inv_cancel₀ (ne_of_gt hp)]

theorem exactConsumer (m n : Nat) (alpha : ℝ)
    (A : FiniteMatrix (gridSize n) (gridSize n) ℂ)
    (U : FiniteMatrix (gridSize m * gridSize n) (gridSize m * gridSize n) ℂ)
    (b : StateVector (gridSize n) ℂ) (hAlpha : 0 < alpha)
    (_hUnitary : U ∈ _root_.Matrix.unitaryGroup
      (Fin (gridSize m * gridSize n)) ℂ)
    (_hInput : (∑ i, Complex.normSq (b i)) = 1)
    (hBlock : ∀ i j, A i j = (alpha : ℂ) *
      signalSystemBlockProjection (gridSize m) (gridSize n) (gridSize n)
        U (zeroBasisIndex m) i j) :
    (alpha : ℂ) • cleanOutput U (zeroBasisIndex m) b = applyVec A b ∧
    (∑ i, Complex.normSq (cleanOutput U (zeroBasisIndex m) b i)) =
      (∑ i, Complex.normSq (applyVec A b i)) / alpha ^ 2 ∧
    (0 < (∑ i, Complex.normSq (cleanOutput U (zeroBasisIndex m) b i)) ↔
      applyVec A b ≠ 0) ∧
    (applyVec A b ≠ 0 → ∀ i,
      cleanOutput U (zeroBasisIndex m) b i /
          (Real.sqrt (∑ j, Complex.normSq (cleanOutput U (zeroBasisIndex m) b j)) : ℂ) =
        applyVec A b i / (Real.sqrt (∑ j, Complex.normSq (applyVec A b j)) : ℂ)) := by
  exact ⟨scaled_cleanOutput alpha A U _ b hBlock,
    exact_weight alpha A U _ b hAlpha hBlock,
    positive_weight_iff alpha A U _ b hAlpha hBlock,
    normalized_cleanOutput alpha A U _ b hAlpha hBlock⟩

#print axioms exactConsumer
#print axioms normalized_vector_weight

-- Regression: a zero image has zero accepted weight, never a valid branch.
example {s d : Nat} (U : FiniteMatrix (s * d) (s * d) ℂ)
    (a : Fin s) (b : StateVector d ℂ)
    (hBlock : ∀ i j, (0 : FiniteMatrix d d ℂ) i j =
      (1 : ℂ) * signalSystemBlockProjection s d d U a i j) :
    ¬0 < (∑ i, Complex.normSq (cleanOutput U a b i)) := by
  rw [positive_weight_iff 1 0 U a b (by norm_num) hBlock]
  simp [applyVec]

-- Regression: empty system carriers are handled by the algebraic provider.
example (alpha : ℝ) (_hAlpha : 0 < alpha)
    (U : FiniteMatrix 0 0 ℂ) (a : Fin 1)
    (_hBlock : ∀ i j, (0 : FiniteMatrix 0 0 ℂ) i j =
      (alpha : ℂ) * signalSystemBlockProjection 1 0 0 U a i j) :
    (∑ i, Complex.normSq (cleanOutput U a (0 : StateVector 0 ℂ) i)) = 0 := by
  simp

-- Regression: imaginary amplitudes retain their relative phase under action.
example : applyVec (1 : FiniteMatrix 2 2 ℂ) (fun _ => Complex.I) =
    (fun _ => Complex.I) := by
  simp [applyVec]

-- Checked source-root instantiation: zero qubits/ancillas, identity, success one.
example : 0 < (∑ i : Fin (gridSize 0), Complex.normSq
    (cleanOutput (1 : FiniteMatrix (gridSize 0 * gridSize 0)
      (gridSize 0 * gridSize 0) ℂ) (zeroBasisIndex 0) (fun _ => 1) i)) := by
  have hBlock : ∀ i j : Fin (gridSize 0),
      (1 : FiniteMatrix (gridSize 0) (gridSize 0) ℂ) i j =
        (1 : ℂ) * signalSystemBlockProjection (gridSize 0) (gridSize 0)
          (gridSize 0)
          (1 : FiniteMatrix (gridSize 0 * gridSize 0) (gridSize 0 * gridSize 0) ℂ)
          (zeroBasisIndex 0) i j := by
    intro i j
    fin_cases i
    fin_cases j
    norm_num [signalSystemBlockProjection, signalSystemBlockRowIndex,
      signalSystemBlockColIndex, gridSize, zeroBasisIndex, _root_.Matrix.one_apply]
  have h := exactConsumer 0 0 1 1 1 (fun _ => 1) (by norm_num)
    (by exact (_root_.Matrix.unitaryGroup
      (Fin (gridSize 0 * gridSize 0)) ℂ).one_mem)
    (by norm_num [gridSize, Complex.normSq_one, Finset.card_univ]) hBlock
  apply h.2.2.1.mpr
  change _root_.Matrix.mulVec (1 : FiniteMatrix (gridSize 0) (gridSize 0) ℂ)
    (fun _ => 1) ≠ 0
  rw [_root_.Matrix.one_mulVec]
  intro hz
  have hf := congrFun hz (zeroBasisIndex 0)
  norm_num at hf

end QuantumBlockEncoding.QASCChapter9
