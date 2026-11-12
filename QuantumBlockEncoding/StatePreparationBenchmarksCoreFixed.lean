import QuantumBlockEncoding.ConcreteSemantics
import QuantumBlockEncoding.TextbookStatePreparation
import Mathlib.Tactic

/-!
# Exact finite state-preparation benchmark certificates

This module contains the matrix-level authority for representative fixed state-
preparation targets. Each benchmark closes normalization, full unitarity, and
`U |0^n> = |psi>` exactly. Circuit synthesis and same-target resource comparisons
are kept in a separate primitive-route layer.
-/

open scoped ComplexConjugate

namespace QuantumBlockEncoding.StatePreparationBenchmarks

open ConcreteSemantics

/-! ## Bell state -/

noncomputable abbrev bellAmplitude : ℂ :=
  TextbookStatePreparation.invSqrtTwo

noncomputable def bellState : StateVector (gridSize 2) ℂ := fun index =>
  if index.val = 0 ∨ index.val = 3 then bellAmplitude else 0

noncomputable def bellTarget : StatePreparationTarget ℂ 2 where
  amplitudes := bellState
  normalization := ∑ index, Complex.normSq (bellState index) = 1
  source := "Bell-state textbook benchmark"

theorem bellTarget_normalized : bellTarget.normalization := by
  change ∑ index : Fin 4, Complex.normSq (bellState index) = 1
  rw [Finset.sum_fin_eq_sum_range]
  have hs : Complex.normSq bellAmplitude = (1 : ℝ) / 2 := by
    simp [bellAmplitude, TextbookStatePreparation.invSqrtTwo,
      Complex.normSq_apply]
  norm_num [bellState, Finset.sum_range_succ, hs]

noncomputable def bellMatrix : FiniteMatrix 4 4 ℂ :=
  fun row column =>
    match row.val, column.val with
    | 0, 0 => bellAmplitude
    | 0, 3 => bellAmplitude
    | 1, 1 => bellAmplitude
    | 1, 2 => bellAmplitude
    | 2, 1 => bellAmplitude
    | 2, 2 => -bellAmplitude
    | 3, 0 => bellAmplitude
    | 3, 3 => -bellAmplitude
    | _, _ => 0

theorem star_bellMatrix : star bellMatrix = bellMatrix := by
  ext row column
  fin_cases row <;> fin_cases column <;>
    simp [bellMatrix, bellAmplitude, TextbookStatePreparation.invSqrtTwo]

theorem bellMatrix_unitary :
    bellMatrix ∈ _root_.Matrix.unitaryGroup (Fin (gridSize 2)) ℂ := by
  change bellMatrix ∈ _root_.Matrix.unitaryGroup (Fin 4) ℂ
  have hmul : bellAmplitude * bellAmplitude = (1 : ℂ) / 2 := by
    simpa [bellAmplitude] using TextbookStatePreparation.invSqrtTwo_mul_self
  rw [_root_.Matrix.mem_unitaryGroup_iff, star_bellMatrix]
  ext row column
  fin_cases row <;> fin_cases column <;>
    rw [_root_.Matrix.mul_apply, Finset.sum_fin_eq_sum_range] <;>
    norm_num [gridSize, bellMatrix, Finset.sum_range_succ,
      _root_.Matrix.one_apply, hmul]

noncomputable def bellGate : ComplexUnitaryGate 2 where
  matrix := bellMatrix
  unitary := bellMatrix_unitary

theorem bellMatrix_prepares_target :
    applyVec bellMatrix (zeroKet 2) = bellTarget.amplitudes := by
  change applyVec bellMatrix (basisKet 4 (0 : Fin 4)) =
    (fun index : Fin 4 =>
      if index.val = 0 ∨ index.val = 3 then bellAmplitude else 0)
  rw [applyVec_basisKet]
  funext row
  fin_cases row <;> simp [bellMatrix, bellAmplitude]

noncomputable def bellCertificate : ComplexStatePreparationCertificate 2 where
  target := bellTarget
  gate := bellGate
  normalizationProof := bellTarget_normalized
  preparationProof := bellMatrix_prepares_target

/-! ## Dense Möttönen-style benchmark -/

noncomputable def mottonenDenseState : StateVector (gridSize 2) ℂ := fun index =>
  match index.val with
  | 0 => (39 : ℂ) / 169
  | 1 => (52 : ℂ) / 169
  | 2 => (60 : ℂ) / 169
  | _ => (144 : ℂ) / 169

noncomputable def mottonenDenseTarget : StatePreparationTarget ℂ 2 where
  amplitudes := mottonenDenseState
  normalization := ∑ index, Complex.normSq (mottonenDenseState index) = 1
  source := "Möttönen-style dense two-qubit nested-Pythagorean benchmark"

theorem mottonenDenseTarget_normalized : mottonenDenseTarget.normalization := by
  change ∑ index : Fin 4, Complex.normSq (mottonenDenseState index) = 1
  rw [Finset.sum_fin_eq_sum_range]
  norm_num [mottonenDenseState, Complex.normSq_apply, Finset.sum_range_succ]

/-- Rational quaternion completion with first column `(39,52,60,144)/169`. -/
noncomputable def mottonenDenseMatrix :
    FiniteMatrix 4 4 ℂ := fun row column =>
  match row.val, column.val with
  | 0, 0 => (39 : ℂ) / 169
  | 0, 1 => -(52 : ℂ) / 169
  | 0, 2 => -(60 : ℂ) / 169
  | 0, 3 => -(144 : ℂ) / 169
  | 1, 0 => (52 : ℂ) / 169
  | 1, 1 => (39 : ℂ) / 169
  | 1, 2 => -(144 : ℂ) / 169
  | 1, 3 => (60 : ℂ) / 169
  | 2, 0 => (60 : ℂ) / 169
  | 2, 1 => (144 : ℂ) / 169
  | 2, 2 => (39 : ℂ) / 169
  | 2, 3 => -(52 : ℂ) / 169
  | 3, 0 => (144 : ℂ) / 169
  | 3, 1 => -(60 : ℂ) / 169
  | 3, 2 => (52 : ℂ) / 169
  | _, _ => (39 : ℂ) / 169

set_option maxHeartbeats 2000000 in
set_option maxRecDepth 20000 in
theorem mottonenDenseMatrix_unitary :
    mottonenDenseMatrix ∈
      _root_.Matrix.unitaryGroup (Fin (gridSize 2)) ℂ := by
  change mottonenDenseMatrix ∈ _root_.Matrix.unitaryGroup (Fin 4) ℂ
  rw [_root_.Matrix.mem_unitaryGroup_iff']
  ext row column
  fin_cases row <;> fin_cases column <;>
    rw [_root_.Matrix.mul_apply, Finset.sum_fin_eq_sum_range] <;>
    simp only [Finset.sum_range_succ, Finset.sum_range_zero,
      mottonenDenseMatrix, _root_.Matrix.star_apply,
      _root_.Matrix.one_apply] <;>
    apply Complex.ext <;> norm_num

noncomputable def mottonenDenseGate : ComplexUnitaryGate 2 where
  matrix := mottonenDenseMatrix
  unitary := mottonenDenseMatrix_unitary

theorem mottonenDenseMatrix_prepares_target :
    applyVec mottonenDenseMatrix (zeroKet 2) =
      mottonenDenseTarget.amplitudes := by
  change applyVec mottonenDenseMatrix (basisKet 4 (0 : Fin 4)) =
    (fun index : Fin 4 =>
      match index.val with
      | 0 => (39 : ℂ) / 169
      | 1 => (52 : ℂ) / 169
      | 2 => (60 : ℂ) / 169
      | _ => (144 : ℂ) / 169)
  rw [applyVec_basisKet]
  funext row
  fin_cases row <;> norm_num [mottonenDenseMatrix]

noncomputable def mottonenDenseCertificate :
    ComplexStatePreparationCertificate 2 where
  target := mottonenDenseTarget
  gate := mottonenDenseGate
  normalizationProof := mottonenDenseTarget_normalized
  preparationProof := mottonenDenseMatrix_prepares_target

/-! ## Structured Grover--Rudolph-style product distribution -/

noncomputable def groverRudolphProductState : StateVector (gridSize 2) ℂ :=
  fun index =>
    match index.val with
    | 0 => (9 : ℂ) / 25
    | 1 => (12 : ℂ) / 25
    | 2 => (12 : ℂ) / 25
    | _ => (16 : ℂ) / 25

noncomputable def groverRudolphProductTarget : StatePreparationTarget ℂ 2 where
  amplitudes := groverRudolphProductState
  normalization := ∑ index, Complex.normSq (groverRudolphProductState index) = 1
  source := "Grover--Rudolph structured product-distribution benchmark"

theorem groverRudolphProductTarget_normalized :
    groverRudolphProductTarget.normalization := by
  change ∑ index : Fin 4, Complex.normSq (groverRudolphProductState index) = 1
  rw [Finset.sum_fin_eq_sum_range]
  norm_num [groverRudolphProductState, Complex.normSq_apply,
    Finset.sum_range_succ]

noncomputable def groverRudolphProductMatrix :
    FiniteMatrix 4 4 ℂ := fun row column =>
  match row.val, column.val with
  | 0, 0 => (9 : ℂ) / 25
  | 0, 1 => -(12 : ℂ) / 25
  | 0, 2 => -(12 : ℂ) / 25
  | 0, 3 => (16 : ℂ) / 25
  | 1, 0 => (12 : ℂ) / 25
  | 1, 1 => (9 : ℂ) / 25
  | 1, 2 => -(16 : ℂ) / 25
  | 1, 3 => -(12 : ℂ) / 25
  | 2, 0 => (12 : ℂ) / 25
  | 2, 1 => -(16 : ℂ) / 25
  | 2, 2 => (9 : ℂ) / 25
  | 2, 3 => -(12 : ℂ) / 25
  | 3, 0 => (16 : ℂ) / 25
  | 3, 1 => (12 : ℂ) / 25
  | 3, 2 => (12 : ℂ) / 25
  | _, _ => (9 : ℂ) / 25

set_option maxHeartbeats 2000000 in
set_option maxRecDepth 20000 in
theorem groverRudolphProductMatrix_unitary :
    groverRudolphProductMatrix ∈
      _root_.Matrix.unitaryGroup (Fin (gridSize 2)) ℂ := by
  change groverRudolphProductMatrix ∈
    _root_.Matrix.unitaryGroup (Fin 4) ℂ
  rw [_root_.Matrix.mem_unitaryGroup_iff']
  ext row column
  fin_cases row <;> fin_cases column <;>
    rw [_root_.Matrix.mul_apply, Finset.sum_fin_eq_sum_range] <;>
    simp only [Finset.sum_range_succ, Finset.sum_range_zero,
      groverRudolphProductMatrix, _root_.Matrix.star_apply,
      _root_.Matrix.one_apply] <;>
    apply Complex.ext <;> norm_num

noncomputable def groverRudolphProductGate : ComplexUnitaryGate 2 where
  matrix := groverRudolphProductMatrix
  unitary := groverRudolphProductMatrix_unitary

theorem groverRudolphProductMatrix_prepares_target :
    applyVec groverRudolphProductMatrix (zeroKet 2) =
      groverRudolphProductTarget.amplitudes := by
  change applyVec groverRudolphProductMatrix (basisKet 4 (0 : Fin 4)) =
    (fun index : Fin 4 =>
      match index.val with
      | 0 => (9 : ℂ) / 25
      | 1 => (12 : ℂ) / 25
      | 2 => (12 : ℂ) / 25
      | _ => (16 : ℂ) / 25)
  rw [applyVec_basisKet]
  funext row
  fin_cases row <;> norm_num [groverRudolphProductMatrix]

noncomputable def groverRudolphProductCertificate :
    ComplexStatePreparationCertificate 2 where
  target := groverRudolphProductTarget
  gate := groverRudolphProductGate
  normalizationProof := groverRudolphProductTarget_normalized
  preparationProof := groverRudolphProductMatrix_prepares_target

/-! ## Fixed three-sparse benchmark -/

noncomputable def sparseThreeState : StateVector (gridSize 3) ℂ := fun index =>
  if index.val = 0 then (3 : ℂ) / 13
  else if index.val = 2 then (4 : ℂ) / 13
  else if index.val = 4 then (12 : ℂ) / 13
  else 0

noncomputable def sparseThreeTarget : StatePreparationTarget ℂ 3 where
  amplitudes := sparseThreeState
  normalization := ∑ index, Complex.normSq (sparseThreeState index) = 1
  source := "Li--Luo sparse-state finite witness of Eq. (2), n=3 and d=3"

theorem sparseThreeTarget_normalized : sparseThreeTarget.normalization := by
  change ∑ index : Fin 8, Complex.normSq (sparseThreeState index) = 1
  rw [Finset.sum_fin_eq_sum_range]
  norm_num [sparseThreeState, Complex.normSq_apply, Finset.sum_range_succ]

/-- Rational orthogonal completion on rows `0,2,4`, identity on the complement. -/
noncomputable def sparseThreeMatrix :
    FiniteMatrix 8 8 ℂ := fun row column =>
  match row.val, column.val with
  | 0, 0 => (3 : ℂ) / 13
  | 0, 1 => -(4 : ℂ) / 5
  | 0, 2 => -(36 : ℂ) / 65
  | 2, 0 => (4 : ℂ) / 13
  | 2, 1 => (3 : ℂ) / 5
  | 2, 2 => -(48 : ℂ) / 65
  | 4, 0 => (12 : ℂ) / 13
  | 4, 1 => 0
  | 4, 2 => (25 : ℂ) / 65
  | 1, 3 => 1
  | 3, 4 => 1
  | 5, 5 => 1
  | 6, 6 => 1
  | 7, 7 => 1
  | _, _ => 0

set_option maxHeartbeats 5000000 in
set_option maxRecDepth 100000 in
theorem sparseThreeMatrix_unitary :
    sparseThreeMatrix ∈
      _root_.Matrix.unitaryGroup (Fin (gridSize 3)) ℂ := by
  change sparseThreeMatrix ∈ _root_.Matrix.unitaryGroup (Fin 8) ℂ
  rw [_root_.Matrix.mem_unitaryGroup_iff']
  ext row column
  fin_cases row <;> fin_cases column <;>
    rw [_root_.Matrix.mul_apply, Finset.sum_fin_eq_sum_range] <;>
    simp only [Finset.sum_range_succ, Finset.sum_range_zero,
      sparseThreeMatrix, _root_.Matrix.star_apply,
      _root_.Matrix.one_apply] <;>
    apply Complex.ext <;> norm_num

noncomputable def sparseThreeGate : ComplexUnitaryGate 3 where
  matrix := sparseThreeMatrix
  unitary := sparseThreeMatrix_unitary

theorem sparseThreeMatrix_prepares_target :
    applyVec sparseThreeMatrix (zeroKet 3) = sparseThreeTarget.amplitudes := by
  change applyVec sparseThreeMatrix (basisKet 8 (0 : Fin 8)) =
    (fun index : Fin 8 =>
      if index.val = 0 then (3 : ℂ) / 13
      else if index.val = 2 then (4 : ℂ) / 13
      else if index.val = 4 then (12 : ℂ) / 13
      else 0)
  rw [applyVec_basisKet]
  funext row
  fin_cases row <;> norm_num [sparseThreeMatrix]

noncomputable def sparseThreeCertificate : ComplexStatePreparationCertificate 3 where
  target := sparseThreeTarget
  gate := sparseThreeGate
  normalizationProof := sparseThreeTarget_normalized
  preparationProof := sparseThreeMatrix_prepares_target

/-! ## Low--Kliuchnikov--Schaeffer SelectSwap resource arithmetic -/

def selectSwapCleanTCount (N b lambda : Nat) : Nat :=
  4 * ((N + lambda - 1) / lambda) + 8 * b * lambda

theorem selectSwapCleanTCount_16_1_1 :
    selectSwapCleanTCount 16 1 1 = 72 := by decide

theorem selectSwapCleanTCount_16_1_4 :
    selectSwapCleanTCount 16 1 4 = 48 := by decide

theorem selectSwapCleanTCount_lambda4_better_lambda1 :
    selectSwapCleanTCount 16 1 4 < selectSwapCleanTCount 16 1 1 := by decide

end QuantumBlockEncoding.StatePreparationBenchmarks
