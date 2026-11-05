import QuantumBlockEncoding.StatePreparationPrimitiveRoutes
import QuantumBlockEncoding.StatePreparationPaperEntryCertificates
import Mathlib.Tactic

/-!
# Compact certificate-composed paper state-preparation routes

The expensive UCRY semantic entries are compiled in
`StatePreparationPaperEntryCertificates`.  This module only assembles those
scalar certificates into the clean-input state-action statements required by
the public routes.  Coordinate-level linearity avoids rebuilding a full
matrix-vector rewrite inside each finite paper witness.
-/

namespace QuantumBlockEncoding.StatePreparationBenchmarks

open ConcreteSemantics
open Robin.ComplexLCU

attribute [local simp] Pi.single_apply
attribute [local simp] primitiveBits2LE primitiveBits3LE
attribute [local simp] primitiveBits2LEWithout primitiveBits3LEWithout
attribute [local simp] splitPrimitiveWire_other_apply

private theorem standardRyMatrix_ryAngle513_explicit_paper :
    standardRyMatrix ryAngle513.eval =
      realOrthogonalRotation ((5 : Real) / 13) ((12 : Real) / 13) := by
  rw [standardRyMatrix_ryAngle513]
  change
    realOrthogonalRotation ((5 / 13 : Rat) : Real) ((12 / 13 : Rat) : Real) =
      realOrthogonalRotation ((5 : Real) / 13) ((12 : Real) / 13)
  ext row column
  fin_cases row <;> fin_cases column <;> norm_num [realOrthogonalRotation]

/-! ## Möttönen dense two-qubit route -/

noncomputable def mottonenConditionalAngles : PrimitiveBasis 1 → ExactAngle :=
  StatePreparationPaperEntryCertificates.mottonenConditionalAngles

noncomputable def mottonenDenseUcryCircuit : PrimitiveCircuit 2 :=
  StatePreparationPaperEntryCertificates.mottonenDenseUcryCircuit

noncomputable def mottonenDensePrimitiveCircuit : PrimitiveCircuit 2 :=
  [PrimitiveGate.ry (1 : Fin 2) ryAngle513] ++ mottonenDenseUcryCircuit

noncomputable def mottonenRootState : StateVector 4 ℂ :=
  (5 / 13 : ℂ) • basisKet 4 (0 : Fin 4) +
    (12 / 13 : ℂ) • basisKet 4 (2 : Fin 4)

private theorem mottonenRootState_0 :
    mottonenRootState (0 : Fin 4) = (5 : ℂ) / 13 := by
  simp [mottonenRootState, basisKet]

private theorem mottonenRootState_1 :
    mottonenRootState (1 : Fin 4) = 0 := by
  simp [mottonenRootState, basisKet]

private theorem mottonenRootState_2 :
    mottonenRootState (2 : Fin 4) = (12 : ℂ) / 13 := by
  simp [mottonenRootState, basisKet]

private theorem mottonenRootState_3 :
    mottonenRootState (3 : Fin 4) = 0 := by
  simp [mottonenRootState, basisKet]

theorem mottonenRootRy_col_zero :
    (evalPrimitiveCircuitLE [PrimitiveGate.ry (1 : Fin 2) ryAngle513]).col
        (0 : Fin 4) = mottonenRootState := by
  funext row
  fin_cases row
  · change
      evalPrimitiveCircuitLE [PrimitiveGate.ry (1 : Fin 2) ryAngle513]
          (0 : Fin 4) (0 : Fin 4) = mottonenRootState (0 : Fin 4)
    rw [mottonenRootState_0]
    change evalPrimitiveCircuitLE _
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = (5 : ℂ) / 13
    norm_num [evalPrimitiveCircuitLE_singleton_ry_apply, primitiveLEBits,
      standardRyMatrix_ryAngle513_explicit_paper, realOrthogonalRotation]
  · change
      evalPrimitiveCircuitLE [PrimitiveGate.ry (1 : Fin 2) ryAngle513]
          (1 : Fin 4) (0 : Fin 4) = mottonenRootState (1 : Fin 4)
    rw [mottonenRootState_1]
    change evalPrimitiveCircuitLE _
      (⟨1, by norm_num [gridSize]⟩ : Fin (gridSize 2))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = 0
    norm_num [evalPrimitiveCircuitLE_singleton_ry_apply, primitiveLEBits,
      standardRyMatrix_ryAngle513_explicit_paper, realOrthogonalRotation]
  · change
      evalPrimitiveCircuitLE [PrimitiveGate.ry (1 : Fin 2) ryAngle513]
          (2 : Fin 4) (0 : Fin 4) = mottonenRootState (2 : Fin 4)
    rw [mottonenRootState_2]
    change evalPrimitiveCircuitLE _
      (⟨2, by norm_num [gridSize]⟩ : Fin (gridSize 2))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = (12 : ℂ) / 13
    norm_num [evalPrimitiveCircuitLE_singleton_ry_apply, primitiveLEBits,
      standardRyMatrix_ryAngle513_explicit_paper, realOrthogonalRotation]
  · change
      evalPrimitiveCircuitLE [PrimitiveGate.ry (1 : Fin 2) ryAngle513]
          (3 : Fin 4) (0 : Fin 4) = mottonenRootState (3 : Fin 4)
    rw [mottonenRootState_3]
    change evalPrimitiveCircuitLE _
      (⟨3, by norm_num [gridSize]⟩ : Fin (gridSize 2))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = 0
    norm_num [evalPrimitiveCircuitLE_singleton_ry_apply, primitiveLEBits,
      standardRyMatrix_ryAngle513_explicit_paper, realOrthogonalRotation]

theorem mottonenRootRy_prepares :
    applyVec
        (evalPrimitiveCircuitLE [PrimitiveGate.ry (1 : Fin 2) ryAngle513])
        (zeroKet 2) = mottonenRootState := by
  rw [applyVec_zeroKet]
  exact mottonenRootRy_col_zero

private theorem mottonenDenseUcry_entry_00 :
    evalPrimitiveCircuitLE mottonenDenseUcryCircuit (0 : Fin 4) (0 : Fin 4) =
      (3 : ℂ) / 5 := by
  simpa [mottonenDenseUcryCircuit] using
    StatePreparationPaperEntryCertificates.mottonenDenseUcry_entry_00

private theorem mottonenDenseUcry_entry_10 :
    evalPrimitiveCircuitLE mottonenDenseUcryCircuit (1 : Fin 4) (0 : Fin 4) =
      (4 : ℂ) / 5 := by
  simpa [mottonenDenseUcryCircuit] using
    StatePreparationPaperEntryCertificates.mottonenDenseUcry_entry_10

private theorem mottonenDenseUcry_entry_22 :
    evalPrimitiveCircuitLE mottonenDenseUcryCircuit (2 : Fin 4) (2 : Fin 4) =
      (5 : ℂ) / 13 := by
  simpa [mottonenDenseUcryCircuit] using
    StatePreparationPaperEntryCertificates.mottonenDenseUcry_entry_22

private theorem mottonenDenseUcry_entry_32 :
    evalPrimitiveCircuitLE mottonenDenseUcryCircuit (3 : Fin 4) (2 : Fin 4) =
      (12 : ℂ) / 13 := by
  simpa [mottonenDenseUcryCircuit] using
    StatePreparationPaperEntryCertificates.mottonenDenseUcry_entry_32

private theorem mottonenZeroEntry (row column : Fin 4)
    (h :
      (splitPrimitiveWire (0 : Fin 2) (primitiveLEBits 2 row)).2 ≠
        (splitPrimitiveWire (0 : Fin 2) (primitiveLEBits 2 column)).2) :
    evalPrimitiveCircuitLE mottonenDenseUcryCircuit row column = 0 := by
  simpa [mottonenDenseUcryCircuit] using
    StatePreparationPaperEntryCertificates.mottonenDenseUcry_entry_zero_of_context_ne
      row column h

private theorem mottonenDenseUcry_entry_02 :
    evalPrimitiveCircuitLE mottonenDenseUcryCircuit (0 : Fin 4) (2 : Fin 4) = 0 :=
  mottonenZeroEntry (0 : Fin 4) (2 : Fin 4) (by native_decide)

private theorem mottonenDenseUcry_entry_12 :
    evalPrimitiveCircuitLE mottonenDenseUcryCircuit (1 : Fin 4) (2 : Fin 4) = 0 :=
  mottonenZeroEntry (1 : Fin 4) (2 : Fin 4) (by native_decide)

private theorem mottonenDenseUcry_entry_20 :
    evalPrimitiveCircuitLE mottonenDenseUcryCircuit (2 : Fin 4) (0 : Fin 4) = 0 :=
  mottonenZeroEntry (2 : Fin 4) (0 : Fin 4) (by native_decide)

private theorem mottonenDenseUcry_entry_30 :
    evalPrimitiveCircuitLE mottonenDenseUcryCircuit (3 : Fin 4) (0 : Fin 4) = 0 :=
  mottonenZeroEntry (3 : Fin 4) (0 : Fin 4) (by native_decide)

private theorem mottonenDenseUcry_scalar_0 :
    (5 / 13 : ℂ) * evalPrimitiveCircuitLE mottonenDenseUcryCircuit (0 : Fin 4) (0 : Fin 4) +
      (12 / 13 : ℂ) * evalPrimitiveCircuitLE mottonenDenseUcryCircuit (0 : Fin 4) (2 : Fin 4) =
      (39 : ℂ) / 169 := by
  rw [mottonenDenseUcry_entry_00, mottonenDenseUcry_entry_02]
  norm_num

private theorem mottonenDenseUcry_scalar_1 :
    (5 / 13 : ℂ) * evalPrimitiveCircuitLE mottonenDenseUcryCircuit (1 : Fin 4) (0 : Fin 4) +
      (12 / 13 : ℂ) * evalPrimitiveCircuitLE mottonenDenseUcryCircuit (1 : Fin 4) (2 : Fin 4) =
      (52 : ℂ) / 169 := by
  rw [mottonenDenseUcry_entry_10, mottonenDenseUcry_entry_12]
  norm_num

private theorem mottonenDenseUcry_scalar_2 :
    (5 / 13 : ℂ) * evalPrimitiveCircuitLE mottonenDenseUcryCircuit (2 : Fin 4) (0 : Fin 4) +
      (12 / 13 : ℂ) * evalPrimitiveCircuitLE mottonenDenseUcryCircuit (2 : Fin 4) (2 : Fin 4) =
      (60 : ℂ) / 169 := by
  rw [mottonenDenseUcry_entry_20, mottonenDenseUcry_entry_22]
  norm_num

private theorem mottonenDenseUcry_scalar_3 :
    (5 / 13 : ℂ) * evalPrimitiveCircuitLE mottonenDenseUcryCircuit (3 : Fin 4) (0 : Fin 4) +
      (12 / 13 : ℂ) * evalPrimitiveCircuitLE mottonenDenseUcryCircuit (3 : Fin 4) (2 : Fin 4) =
      (144 : ℂ) / 169 := by
  rw [mottonenDenseUcry_entry_30, mottonenDenseUcry_entry_32]
  norm_num

theorem mottonenDenseUcry_on_root :
    applyVec (evalPrimitiveCircuitLE mottonenDenseUcryCircuit) mottonenRootState =
      mottonenDenseState := by
  funext row
  fin_cases row
  · change
      applyVec (evalPrimitiveCircuitLE mottonenDenseUcryCircuit)
          ((5 / 13 : ℂ) • basisKet (gridSize 2) (0 : Fin 4) +
            (12 / 13 : ℂ) • basisKet (gridSize 2) (2 : Fin 4)) (0 : Fin 4) =
        (39 : ℂ) / 169
    exact
      (applyVec_twoBasisSuperposition_apply
        (evalPrimitiveCircuitLE mottonenDenseUcryCircuit)
        (5 / 13 : ℂ) (12 / 13 : ℂ) (0 : Fin 4) (2 : Fin 4) (0 : Fin 4)).trans
        mottonenDenseUcry_scalar_0
  · change
      applyVec (evalPrimitiveCircuitLE mottonenDenseUcryCircuit)
          ((5 / 13 : ℂ) • basisKet (gridSize 2) (0 : Fin 4) +
            (12 / 13 : ℂ) • basisKet (gridSize 2) (2 : Fin 4)) (1 : Fin 4) =
        (52 : ℂ) / 169
    exact
      (applyVec_twoBasisSuperposition_apply
        (evalPrimitiveCircuitLE mottonenDenseUcryCircuit)
        (5 / 13 : ℂ) (12 / 13 : ℂ) (0 : Fin 4) (2 : Fin 4) (1 : Fin 4)).trans
        mottonenDenseUcry_scalar_1
  · change
      applyVec (evalPrimitiveCircuitLE mottonenDenseUcryCircuit)
          ((5 / 13 : ℂ) • basisKet (gridSize 2) (0 : Fin 4) +
            (12 / 13 : ℂ) • basisKet (gridSize 2) (2 : Fin 4)) (2 : Fin 4) =
        (60 : ℂ) / 169
    exact
      (applyVec_twoBasisSuperposition_apply
        (evalPrimitiveCircuitLE mottonenDenseUcryCircuit)
        (5 / 13 : ℂ) (12 / 13 : ℂ) (0 : Fin 4) (2 : Fin 4) (2 : Fin 4)).trans
        mottonenDenseUcry_scalar_2
  · change
      applyVec (evalPrimitiveCircuitLE mottonenDenseUcryCircuit)
          ((5 / 13 : ℂ) • basisKet (gridSize 2) (0 : Fin 4) +
            (12 / 13 : ℂ) • basisKet (gridSize 2) (2 : Fin 4)) (3 : Fin 4) =
        (144 : ℂ) / 169
    exact
      (applyVec_twoBasisSuperposition_apply
        (evalPrimitiveCircuitLE mottonenDenseUcryCircuit)
        (5 / 13 : ℂ) (12 / 13 : ℂ) (0 : Fin 4) (2 : Fin 4) (3 : Fin 4)).trans
        mottonenDenseUcry_scalar_3

theorem mottonenDensePrimitive_prepares_target :
    applyVec (evalPrimitiveCircuitLE mottonenDensePrimitiveCircuit) (zeroKet 2) =
      mottonenDenseTarget.amplitudes := by
  unfold mottonenDensePrimitiveCircuit
  rw [evalPrimitiveCircuitLE_append]
  unfold applyVec
  rw [← _root_.Matrix.mulVec_mulVec]
  change
    applyVec (evalPrimitiveCircuitLE mottonenDenseUcryCircuit)
        (applyVec
          (evalPrimitiveCircuitLE [PrimitiveGate.ry (1 : Fin 2) ryAngle513])
          (zeroKet 2)) = mottonenDenseState
  rw [mottonenRootRy_prepares]
  exact mottonenDenseUcry_on_root

noncomputable def mottonenDensePrimitiveRoute :
    ExactPrimitiveStatePreparationRoute 2 where
  target := mottonenDenseTarget
  circuit := mottonenDensePrimitiveCircuit
  normalizationProof := mottonenDenseTarget_normalized
  preparationProof := mottonenDensePrimitive_prepares_target

theorem mottonenDenseVerified_cost :
    mottonenDensePrimitiveRoute.cost =
      { auxiliaryQubits := 0, gateCount := 5, depth := 4, oracleCalls := 0 } := by
  decide

/-! ## Zero-angle UCRY identity used by the dense-tree sparse baseline -/

theorem zeroAngleCompiledUcry_eval_eq_one
    {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target) :
    evalPrimitiveCircuit
        (compileUniformlyControlledRy controls wires target distinct
          (fun _ => ryAngleZero)) = 1 := by
  rw [compileUniformlyControlledRy_eval_controlledRyBlockMatrix]
  ext row column
  rw [controlledRyBlockMatrix_apply]
  by_cases contextsEqual :
      (splitPrimitiveWire target row).2 = (splitPrimitiveWire target column).2
  · have rowEq_iff : row = column ↔ row target = column target := by
      constructor
      · intro equality
        exact congrFun equality target
      · intro targetEqual
        apply (splitPrimitiveWire target).injective
        apply Prod.ext
        · simpa [splitPrimitiveWire] using targetEqual
        · exact contextsEqual
    rw [if_pos contextsEqual, standardRyMatrix_ryAngleZero]
    simpa only [_root_.Matrix.one_apply, rowEq_iff]
  · have rowNe : row ≠ column := by
      intro equality
      subst column
      exact contextsEqual rfl
    rw [if_neg contextsEqual]
    simp [rowNe]

/-! ## Li--Luo sparse three-qubit route -/

def sparseControlWire : Fin 1 → Fin 3 :=
  StatePreparationPaperEntryCertificates.sparseControlWire

theorem sparseControlWire_ne_target :
    ∀ control, sparseControlWire control ≠ (1 : Fin 3) := by
  simpa [sparseControlWire] using
    StatePreparationPaperEntryCertificates.sparseControlWire_ne_target

noncomputable def sparseConditionalAngles : PrimitiveBasis 1 → ExactAngle :=
  StatePreparationPaperEntryCertificates.sparseConditionalAngles

noncomputable def sparsePrunedUcryCircuit : PrimitiveCircuit 3 :=
  StatePreparationPaperEntryCertificates.sparsePrunedUcryCircuit

noncomputable def sparsePrunedCircuit : PrimitiveCircuit 3 :=
  [PrimitiveGate.ry (2 : Fin 3) ryAngle513] ++ sparsePrunedUcryCircuit

noncomputable def sparseRootState : StateVector 8 ℂ :=
  (5 / 13 : ℂ) • basisKet 8 (0 : Fin 8) +
    (12 / 13 : ℂ) • basisKet 8 (4 : Fin 8)

private theorem sparseRootState_0 : sparseRootState (0 : Fin 8) = (5 : ℂ) / 13 := by
  simp [sparseRootState, basisKet]
private theorem sparseRootState_1 : sparseRootState (1 : Fin 8) = 0 := by
  simp [sparseRootState, basisKet]
private theorem sparseRootState_2 : sparseRootState (2 : Fin 8) = 0 := by
  simp [sparseRootState, basisKet]
private theorem sparseRootState_3 : sparseRootState (3 : Fin 8) = 0 := by
  simp [sparseRootState, basisKet]
private theorem sparseRootState_4 : sparseRootState (4 : Fin 8) = (12 : ℂ) / 13 := by
  simp [sparseRootState, basisKet]
private theorem sparseRootState_5 : sparseRootState (5 : Fin 8) = 0 := by
  simp [sparseRootState, basisKet]
private theorem sparseRootState_6 : sparseRootState (6 : Fin 8) = 0 := by
  simp [sparseRootState, basisKet]
private theorem sparseRootState_7 : sparseRootState (7 : Fin 8) = 0 := by
  simp [sparseRootState, basisKet]

theorem sparseRootRy_col_zero :
    (evalPrimitiveCircuitLE [PrimitiveGate.ry (2 : Fin 3) ryAngle513]).col
        (0 : Fin 8) = sparseRootState := by
  funext row
  fin_cases row
  · change evalPrimitiveCircuitLE [PrimitiveGate.ry (2 : Fin 3) ryAngle513]
      (0 : Fin 8) (0 : Fin 8) = sparseRootState (0 : Fin 8)
    rw [sparseRootState_0]
    change evalPrimitiveCircuitLE _
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 3))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 3)) = (5 : ℂ) / 13
    norm_num [evalPrimitiveCircuitLE_singleton_ry_apply, primitiveLEBits,
      standardRyMatrix_ryAngle513_explicit_paper, realOrthogonalRotation]
  · change evalPrimitiveCircuitLE [PrimitiveGate.ry (2 : Fin 3) ryAngle513]
      (1 : Fin 8) (0 : Fin 8) = sparseRootState (1 : Fin 8)
    rw [sparseRootState_1]
    change evalPrimitiveCircuitLE _
      (⟨1, by norm_num [gridSize]⟩ : Fin (gridSize 3))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 3)) = 0
    norm_num [evalPrimitiveCircuitLE_singleton_ry_apply, primitiveLEBits,
      standardRyMatrix_ryAngle513_explicit_paper, realOrthogonalRotation]
  · change evalPrimitiveCircuitLE [PrimitiveGate.ry (2 : Fin 3) ryAngle513]
      (2 : Fin 8) (0 : Fin 8) = sparseRootState (2 : Fin 8)
    rw [sparseRootState_2]
    change evalPrimitiveCircuitLE _
      (⟨2, by norm_num [gridSize]⟩ : Fin (gridSize 3))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 3)) = 0
    norm_num [evalPrimitiveCircuitLE_singleton_ry_apply, primitiveLEBits,
      standardRyMatrix_ryAngle513_explicit_paper, realOrthogonalRotation]
  · change evalPrimitiveCircuitLE [PrimitiveGate.ry (2 : Fin 3) ryAngle513]
      (3 : Fin 8) (0 : Fin 8) = sparseRootState (3 : Fin 8)
    rw [sparseRootState_3]
    change evalPrimitiveCircuitLE _
      (⟨3, by norm_num [gridSize]⟩ : Fin (gridSize 3))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 3)) = 0
    norm_num [evalPrimitiveCircuitLE_singleton_ry_apply, primitiveLEBits,
      standardRyMatrix_ryAngle513_explicit_paper, realOrthogonalRotation]
  · change evalPrimitiveCircuitLE [PrimitiveGate.ry (2 : Fin 3) ryAngle513]
      (4 : Fin 8) (0 : Fin 8) = sparseRootState (4 : Fin 8)
    rw [sparseRootState_4]
    change evalPrimitiveCircuitLE _
      (⟨4, by norm_num [gridSize]⟩ : Fin (gridSize 3))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 3)) = (12 : ℂ) / 13
    norm_num [evalPrimitiveCircuitLE_singleton_ry_apply, primitiveLEBits,
      standardRyMatrix_ryAngle513_explicit_paper, realOrthogonalRotation]
  · change evalPrimitiveCircuitLE [PrimitiveGate.ry (2 : Fin 3) ryAngle513]
      (5 : Fin 8) (0 : Fin 8) = sparseRootState (5 : Fin 8)
    rw [sparseRootState_5]
    change evalPrimitiveCircuitLE _
      (⟨5, by norm_num [gridSize]⟩ : Fin (gridSize 3))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 3)) = 0
    norm_num [evalPrimitiveCircuitLE_singleton_ry_apply, primitiveLEBits,
      standardRyMatrix_ryAngle513_explicit_paper, realOrthogonalRotation]
  · change evalPrimitiveCircuitLE [PrimitiveGate.ry (2 : Fin 3) ryAngle513]
      (6 : Fin 8) (0 : Fin 8) = sparseRootState (6 : Fin 8)
    rw [sparseRootState_6]
    change evalPrimitiveCircuitLE _
      (⟨6, by norm_num [gridSize]⟩ : Fin (gridSize 3))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 3)) = 0
    norm_num [evalPrimitiveCircuitLE_singleton_ry_apply, primitiveLEBits,
      standardRyMatrix_ryAngle513_explicit_paper, realOrthogonalRotation]
  · change evalPrimitiveCircuitLE [PrimitiveGate.ry (2 : Fin 3) ryAngle513]
      (7 : Fin 8) (0 : Fin 8) = sparseRootState (7 : Fin 8)
    rw [sparseRootState_7]
    change evalPrimitiveCircuitLE _
      (⟨7, by norm_num [gridSize]⟩ : Fin (gridSize 3))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 3)) = 0
    norm_num [evalPrimitiveCircuitLE_singleton_ry_apply, primitiveLEBits,
      standardRyMatrix_ryAngle513_explicit_paper, realOrthogonalRotation]

theorem sparseRootRy_prepares :
    applyVec
        (evalPrimitiveCircuitLE [PrimitiveGate.ry (2 : Fin 3) ryAngle513])
        (zeroKet 3) = sparseRootState := by
  rw [applyVec_zeroKet]
  exact sparseRootRy_col_zero

private theorem sparsePrunedUcry_entry_00 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (0 : Fin 8) (0 : Fin 8) =
      (3 : ℂ) / 5 := by
  simpa [sparsePrunedUcryCircuit] using
    StatePreparationPaperEntryCertificates.sparsePrunedUcry_entry_00

private theorem sparsePrunedUcry_entry_20 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (2 : Fin 8) (0 : Fin 8) =
      (4 : ℂ) / 5 := by
  simpa [sparsePrunedUcryCircuit] using
    StatePreparationPaperEntryCertificates.sparsePrunedUcry_entry_20

private theorem sparsePrunedUcry_entry_44 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (4 : Fin 8) (4 : Fin 8) = 1 := by
  simpa [sparsePrunedUcryCircuit] using
    StatePreparationPaperEntryCertificates.sparsePrunedUcry_entry_44

private theorem sparsePrunedUcry_entry_64 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (6 : Fin 8) (4 : Fin 8) = 0 := by
  simpa [sparsePrunedUcryCircuit] using
    StatePreparationPaperEntryCertificates.sparsePrunedUcry_entry_64

private theorem sparseZeroEntry (row column : Fin 8)
    (h :
      (splitPrimitiveWire (1 : Fin 3) (primitiveLEBits 3 row)).2 ≠
        (splitPrimitiveWire (1 : Fin 3) (primitiveLEBits 3 column)).2) :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit row column = 0 := by
  simpa [sparsePrunedUcryCircuit] using
    StatePreparationPaperEntryCertificates.sparsePrunedUcry_entry_zero_of_context_ne
      row column h

private theorem sparsePrunedUcry_entry_10 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (1 : Fin 8) (0 : Fin 8) = 0 :=
  sparseZeroEntry (1 : Fin 8) (0 : Fin 8) (by native_decide)
private theorem sparsePrunedUcry_entry_30 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (3 : Fin 8) (0 : Fin 8) = 0 :=
  sparseZeroEntry (3 : Fin 8) (0 : Fin 8) (by native_decide)
private theorem sparsePrunedUcry_entry_40 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (4 : Fin 8) (0 : Fin 8) = 0 :=
  sparseZeroEntry (4 : Fin 8) (0 : Fin 8) (by native_decide)
private theorem sparsePrunedUcry_entry_50 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (5 : Fin 8) (0 : Fin 8) = 0 :=
  sparseZeroEntry (5 : Fin 8) (0 : Fin 8) (by native_decide)
private theorem sparsePrunedUcry_entry_60 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (6 : Fin 8) (0 : Fin 8) = 0 :=
  sparseZeroEntry (6 : Fin 8) (0 : Fin 8) (by native_decide)
private theorem sparsePrunedUcry_entry_70 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (7 : Fin 8) (0 : Fin 8) = 0 :=
  sparseZeroEntry (7 : Fin 8) (0 : Fin 8) (by native_decide)
private theorem sparsePrunedUcry_entry_04 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (0 : Fin 8) (4 : Fin 8) = 0 :=
  sparseZeroEntry (0 : Fin 8) (4 : Fin 8) (by native_decide)
private theorem sparsePrunedUcry_entry_14 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (1 : Fin 8) (4 : Fin 8) = 0 :=
  sparseZeroEntry (1 : Fin 8) (4 : Fin 8) (by native_decide)
private theorem sparsePrunedUcry_entry_24 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (2 : Fin 8) (4 : Fin 8) = 0 :=
  sparseZeroEntry (2 : Fin 8) (4 : Fin 8) (by native_decide)
private theorem sparsePrunedUcry_entry_34 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (3 : Fin 8) (4 : Fin 8) = 0 :=
  sparseZeroEntry (3 : Fin 8) (4 : Fin 8) (by native_decide)
private theorem sparsePrunedUcry_entry_54 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (5 : Fin 8) (4 : Fin 8) = 0 :=
  sparseZeroEntry (5 : Fin 8) (4 : Fin 8) (by native_decide)
private theorem sparsePrunedUcry_entry_74 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (7 : Fin 8) (4 : Fin 8) = 0 :=
  sparseZeroEntry (7 : Fin 8) (4 : Fin 8) (by native_decide)

private theorem sparsePrunedUcry_scalar_0 :
    (5 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (0 : Fin 8) (0 : Fin 8) +
      (12 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (0 : Fin 8) (4 : Fin 8) =
      (3 : ℂ) / 13 := by
  rw [sparsePrunedUcry_entry_00, sparsePrunedUcry_entry_04]
  norm_num

private theorem sparsePrunedUcry_scalar_1 :
    (5 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (1 : Fin 8) (0 : Fin 8) +
      (12 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (1 : Fin 8) (4 : Fin 8) = 0 := by
  rw [sparsePrunedUcry_entry_10, sparsePrunedUcry_entry_14]
  norm_num

private theorem sparsePrunedUcry_scalar_2 :
    (5 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (2 : Fin 8) (0 : Fin 8) +
      (12 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (2 : Fin 8) (4 : Fin 8) =
      (4 : ℂ) / 13 := by
  rw [sparsePrunedUcry_entry_20, sparsePrunedUcry_entry_24]
  norm_num

private theorem sparsePrunedUcry_scalar_3 :
    (5 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (3 : Fin 8) (0 : Fin 8) +
      (12 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (3 : Fin 8) (4 : Fin 8) = 0 := by
  rw [sparsePrunedUcry_entry_30, sparsePrunedUcry_entry_34]
  norm_num

private theorem sparsePrunedUcry_scalar_4 :
    (5 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (4 : Fin 8) (0 : Fin 8) +
      (12 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (4 : Fin 8) (4 : Fin 8) =
      (12 : ℂ) / 13 := by
  rw [sparsePrunedUcry_entry_40, sparsePrunedUcry_entry_44]
  norm_num

private theorem sparsePrunedUcry_scalar_5 :
    (5 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (5 : Fin 8) (0 : Fin 8) +
      (12 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (5 : Fin 8) (4 : Fin 8) = 0 := by
  rw [sparsePrunedUcry_entry_50, sparsePrunedUcry_entry_54]
  norm_num

private theorem sparsePrunedUcry_scalar_6 :
    (5 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (6 : Fin 8) (0 : Fin 8) +
      (12 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (6 : Fin 8) (4 : Fin 8) = 0 := by
  rw [sparsePrunedUcry_entry_60, sparsePrunedUcry_entry_64]
  norm_num

private theorem sparsePrunedUcry_scalar_7 :
    (5 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (7 : Fin 8) (0 : Fin 8) +
      (12 / 13 : ℂ) * evalPrimitiveCircuitLE sparsePrunedUcryCircuit (7 : Fin 8) (4 : Fin 8) = 0 := by
  rw [sparsePrunedUcry_entry_70, sparsePrunedUcry_entry_74]
  norm_num

theorem sparsePrunedUcry_on_root :
    applyVec (evalPrimitiveCircuitLE sparsePrunedUcryCircuit) sparseRootState = sparseThreeState := by
  funext row
  fin_cases row
  · change
      applyVec (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
          ((5 / 13 : ℂ) • basisKet (gridSize 3) (0 : Fin 8) +
            (12 / 13 : ℂ) • basisKet (gridSize 3) (4 : Fin 8)) (0 : Fin 8) =
        (3 : ℂ) / 13
    exact
      (applyVec_twoBasisSuperposition_apply
        (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
        (5 / 13 : ℂ) (12 / 13 : ℂ) (0 : Fin 8) (4 : Fin 8) (0 : Fin 8)).trans
        sparsePrunedUcry_scalar_0
  · change
      applyVec (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
          ((5 / 13 : ℂ) • basisKet (gridSize 3) (0 : Fin 8) +
            (12 / 13 : ℂ) • basisKet (gridSize 3) (4 : Fin 8)) (1 : Fin 8) = 0
    exact
      (applyVec_twoBasisSuperposition_apply
        (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
        (5 / 13 : ℂ) (12 / 13 : ℂ) (0 : Fin 8) (4 : Fin 8) (1 : Fin 8)).trans
        sparsePrunedUcry_scalar_1
  · change
      applyVec (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
          ((5 / 13 : ℂ) • basisKet (gridSize 3) (0 : Fin 8) +
            (12 / 13 : ℂ) • basisKet (gridSize 3) (4 : Fin 8)) (2 : Fin 8) =
        (4 : ℂ) / 13
    exact
      (applyVec_twoBasisSuperposition_apply
        (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
        (5 / 13 : ℂ) (12 / 13 : ℂ) (0 : Fin 8) (4 : Fin 8) (2 : Fin 8)).trans
        sparsePrunedUcry_scalar_2
  · change
      applyVec (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
          ((5 / 13 : ℂ) • basisKet (gridSize 3) (0 : Fin 8) +
            (12 / 13 : ℂ) • basisKet (gridSize 3) (4 : Fin 8)) (3 : Fin 8) = 0
    exact
      (applyVec_twoBasisSuperposition_apply
        (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
        (5 / 13 : ℂ) (12 / 13 : ℂ) (0 : Fin 8) (4 : Fin 8) (3 : Fin 8)).trans
        sparsePrunedUcry_scalar_3
  · change
      applyVec (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
          ((5 / 13 : ℂ) • basisKet (gridSize 3) (0 : Fin 8) +
            (12 / 13 : ℂ) • basisKet (gridSize 3) (4 : Fin 8)) (4 : Fin 8) =
        (12 : ℂ) / 13
    exact
      (applyVec_twoBasisSuperposition_apply
        (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
        (5 / 13 : ℂ) (12 / 13 : ℂ) (0 : Fin 8) (4 : Fin 8) (4 : Fin 8)).trans
        sparsePrunedUcry_scalar_4
  · change
      applyVec (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
          ((5 / 13 : ℂ) • basisKet (gridSize 3) (0 : Fin 8) +
            (12 / 13 : ℂ) • basisKet (gridSize 3) (4 : Fin 8)) (5 : Fin 8) = 0
    exact
      (applyVec_twoBasisSuperposition_apply
        (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
        (5 / 13 : ℂ) (12 / 13 : ℂ) (0 : Fin 8) (4 : Fin 8) (5 : Fin 8)).trans
        sparsePrunedUcry_scalar_5
  · change
      applyVec (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
          ((5 / 13 : ℂ) • basisKet (gridSize 3) (0 : Fin 8) +
            (12 / 13 : ℂ) • basisKet (gridSize 3) (4 : Fin 8)) (6 : Fin 8) = 0
    exact
      (applyVec_twoBasisSuperposition_apply
        (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
        (5 / 13 : ℂ) (12 / 13 : ℂ) (0 : Fin 8) (4 : Fin 8) (6 : Fin 8)).trans
        sparsePrunedUcry_scalar_6
  · change
      applyVec (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
          ((5 / 13 : ℂ) • basisKet (gridSize 3) (0 : Fin 8) +
            (12 / 13 : ℂ) • basisKet (gridSize 3) (4 : Fin 8)) (7 : Fin 8) = 0
    exact
      (applyVec_twoBasisSuperposition_apply
        (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
        (5 / 13 : ℂ) (12 / 13 : ℂ) (0 : Fin 8) (4 : Fin 8) (7 : Fin 8)).trans
        sparsePrunedUcry_scalar_7

theorem sparsePruned_prepares_target :
    applyVec (evalPrimitiveCircuitLE sparsePrunedCircuit) (zeroKet 3) =
      sparseThreeTarget.amplitudes := by
  unfold sparsePrunedCircuit
  rw [evalPrimitiveCircuitLE_append]
  unfold applyVec
  rw [← _root_.Matrix.mulVec_mulVec]
  change
    applyVec (evalPrimitiveCircuitLE sparsePrunedUcryCircuit)
        (applyVec
          (evalPrimitiveCircuitLE [PrimitiveGate.ry (2 : Fin 3) ryAngle513])
          (zeroKet 3)) = sparseThreeState
  rw [sparseRootRy_prepares]
  exact sparsePrunedUcry_on_root

noncomputable def sparsePrunedRoute : ExactPrimitiveStatePreparationRoute 3 where
  target := sparseThreeTarget
  circuit := sparsePrunedCircuit
  normalizationProof := sparseThreeTarget_normalized
  preparationProof := sparsePruned_prepares_target

def sparseDenseControlWires : Fin 2 → Fin 3
  | ⟨0, _⟩ => 1
  | _ => 2

theorem sparseDenseControlWires_ne_target :
    ∀ control, sparseDenseControlWires control ≠ (0 : Fin 3) := by
  intro control
  fin_cases control <;> decide

noncomputable def sparseZeroFillCircuit : PrimitiveCircuit 3 :=
  compileUniformlyControlledRy 2 sparseDenseControlWires (0 : Fin 3)
    sparseDenseControlWires_ne_target (fun _ => ryAngleZero)

noncomputable def sparseDenseTreeCircuit : PrimitiveCircuit 3 :=
  sparsePrunedCircuit ++ sparseZeroFillCircuit

theorem sparseZeroFill_eval_eq_one :
    evalPrimitiveCircuit sparseZeroFillCircuit = 1 := by
  unfold sparseZeroFillCircuit
  exact zeroAngleCompiledUcry_eval_eq_one
    sparseDenseControlWires (0 : Fin 3) sparseDenseControlWires_ne_target

theorem sparseZeroFill_evalLE_eq_one :
    evalPrimitiveCircuitLE sparseZeroFillCircuit = 1 := by
  unfold evalPrimitiveCircuitLE
  rw [sparseZeroFill_eval_eq_one]
  simp

theorem sparseDenseTree_evalLE_eq_pruned :
    evalPrimitiveCircuitLE sparseDenseTreeCircuit =
      evalPrimitiveCircuitLE sparsePrunedCircuit := by
  unfold sparseDenseTreeCircuit
  rw [evalPrimitiveCircuitLE_append, sparseZeroFill_evalLE_eq_one]
  simp

theorem sparseDenseTree_prepares_target :
    applyVec (evalPrimitiveCircuitLE sparseDenseTreeCircuit) (zeroKet 3) =
      sparseThreeTarget.amplitudes := by
  rw [sparseDenseTree_evalLE_eq_pruned]
  exact sparsePruned_prepares_target

noncomputable def sparseDenseTreeRoute : ExactPrimitiveStatePreparationRoute 3 where
  target := sparseThreeTarget
  circuit := sparseDenseTreeCircuit
  normalizationProof := sparseThreeTarget_normalized
  preparationProof := sparseDenseTree_prepares_target

theorem sparsePrunedVerified_cost :
    sparsePrunedRoute.cost =
      { auxiliaryQubits := 0, gateCount := 5, depth := 4, oracleCalls := 0 } := by
  decide

theorem sparseDenseTreeVerified_cost :
    sparseDenseTreeRoute.cost =
      { auxiliaryQubits := 0, gateCount := 15, depth := 13, oracleCalls := 0 } := by
  decide

theorem sparsePruned_betterThan_denseTree :
    sparsePrunedRoute.cost.betterThan sparseDenseTreeRoute.cost := by
  rw [sparsePrunedVerified_cost, sparseDenseTreeVerified_cost]
  exact Or.inl (by decide)

end QuantumBlockEncoding.StatePreparationBenchmarks
