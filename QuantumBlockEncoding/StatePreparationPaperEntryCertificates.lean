import QuantumBlockEncoding.StatePreparationPrimitiveRoutes
import Mathlib.Tactic

/-!
# Finite scalar certificates for paper state-preparation routes

The Möttönen and Li--Luo benchmark routes only need a handful of UCRY matrix
entries on the clean-input support.  These scalar facts are compiled in a
separate module so higher-level state-action proofs can compose already checked
leaves without rebuilding the UCRY semantic proof terms.
-/

namespace QuantumBlockEncoding.StatePreparationPaperEntryCertificates

open ConcreteSemantics
open Robin.ComplexLCU
open StatePreparationBenchmarks

attribute [local simp] primitiveBits2LE primitiveBits3LE
attribute [local simp] primitiveBits2LEWithout primitiveBits3LEWithout
attribute [local simp] splitPrimitiveWire_other_apply

private theorem standardRyMatrix_ryAngle35_explicit :
    standardRyMatrix ryAngle35.eval =
      realOrthogonalRotation ((3 : Real) / 5) ((4 : Real) / 5) := by
  rw [standardRyMatrix_ryAngle35]
  change
    realOrthogonalRotation ((3 / 5 : Rat) : Real) ((4 / 5 : Rat) : Real) =
      realOrthogonalRotation ((3 : Real) / 5) ((4 : Real) / 5)
  ext row column
  fin_cases row <;> fin_cases column <;> norm_num [realOrthogonalRotation]

private theorem standardRyMatrix_ryAngle513_explicit :
    standardRyMatrix ryAngle513.eval =
      realOrthogonalRotation ((5 : Real) / 13) ((12 : Real) / 13) := by
  rw [standardRyMatrix_ryAngle513]
  change
    realOrthogonalRotation ((5 / 13 : Rat) : Real) ((12 / 13 : Rat) : Real) =
      realOrthogonalRotation ((5 : Real) / 13) ((12 : Real) / 13)
  ext row column
  fin_cases row <;> fin_cases column <;> norm_num [realOrthogonalRotation]

noncomputable def mottonenConditionalAngles (bits : PrimitiveBasis 1) : ExactAngle :=
  if bits 0 = 0 then ryAngle35 else ryAngle513

noncomputable def mottonenDenseUcryCircuit : PrimitiveCircuit 2 :=
  compileUniformlyControlledRy 1 groverRudolphControlWire (0 : Fin 2)
    groverRudolphControlWire_ne_target mottonenConditionalAngles

theorem mottonenDenseUcry_entry_zero_of_context_ne
    (row column : Fin (gridSize 2))
    (contextNe :
      (splitPrimitiveWire (0 : Fin 2) (primitiveLEBits 2 row)).2 ≠
        (splitPrimitiveWire (0 : Fin 2) (primitiveLEBits 2 column)).2) :
    evalPrimitiveCircuitLE mottonenDenseUcryCircuit row column = 0 := by
  unfold mottonenDenseUcryCircuit
  rw [evalPrimitiveCircuitLE_compileUniformlyControlledRy_apply]
  rw [if_neg contextNe]

theorem mottonenDenseUcry_entry_00 :
    evalPrimitiveCircuitLE mottonenDenseUcryCircuit (0 : Fin 4) (0 : Fin 4) =
      (3 : ℂ) / 5 := by
  unfold mottonenDenseUcryCircuit
  change evalPrimitiveCircuitLE _
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = _
  rw [evalPrimitiveCircuitLE_compileUniformlyControlledRy_apply]
  rw [if_pos (by native_decide)]
  simp [mottonenConditionalAngles, groverRudolphControlWire,
    primitiveControlAssignment, primitiveLEBits,
    standardRyMatrix_ryAngle35_explicit, realOrthogonalRotation]

theorem mottonenDenseUcry_entry_10 :
    evalPrimitiveCircuitLE mottonenDenseUcryCircuit (1 : Fin 4) (0 : Fin 4) =
      (4 : ℂ) / 5 := by
  unfold mottonenDenseUcryCircuit
  change evalPrimitiveCircuitLE _
      (⟨1, by norm_num [gridSize]⟩ : Fin (gridSize 2))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = _
  rw [evalPrimitiveCircuitLE_compileUniformlyControlledRy_apply]
  rw [if_pos (by native_decide)]
  simp [mottonenConditionalAngles, groverRudolphControlWire,
    primitiveControlAssignment, primitiveLEBits,
    standardRyMatrix_ryAngle35_explicit, realOrthogonalRotation]

theorem mottonenDenseUcry_entry_22 :
    evalPrimitiveCircuitLE mottonenDenseUcryCircuit (2 : Fin 4) (2 : Fin 4) =
      (5 : ℂ) / 13 := by
  unfold mottonenDenseUcryCircuit
  change evalPrimitiveCircuitLE _
      (⟨2, by norm_num [gridSize]⟩ : Fin (gridSize 2))
      (⟨2, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = _
  rw [evalPrimitiveCircuitLE_compileUniformlyControlledRy_apply]
  rw [if_pos (by native_decide)]
  simp [mottonenConditionalAngles, groverRudolphControlWire,
    primitiveControlAssignment, primitiveLEBits,
    standardRyMatrix_ryAngle513_explicit, realOrthogonalRotation]

theorem mottonenDenseUcry_entry_32 :
    evalPrimitiveCircuitLE mottonenDenseUcryCircuit (3 : Fin 4) (2 : Fin 4) =
      (12 : ℂ) / 13 := by
  unfold mottonenDenseUcryCircuit
  change evalPrimitiveCircuitLE _
      (⟨3, by norm_num [gridSize]⟩ : Fin (gridSize 2))
      (⟨2, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = _
  rw [evalPrimitiveCircuitLE_compileUniformlyControlledRy_apply]
  rw [if_pos (by native_decide)]
  simp [mottonenConditionalAngles, groverRudolphControlWire,
    primitiveControlAssignment, primitiveLEBits,
    standardRyMatrix_ryAngle513_explicit, realOrthogonalRotation]

def sparseControlWire : Fin 1 → Fin 3 := fun _ => 2

theorem sparseControlWire_ne_target :
    ∀ control, sparseControlWire control ≠ (1 : Fin 3) := by
  intro control
  fin_cases control
  decide

noncomputable def sparseConditionalAngles (bits : PrimitiveBasis 1) : ExactAngle :=
  if bits 0 = 0 then ryAngle35 else ryAngleZero

noncomputable def sparsePrunedUcryCircuit : PrimitiveCircuit 3 :=
  compileUniformlyControlledRy 1 sparseControlWire (1 : Fin 3)
    sparseControlWire_ne_target sparseConditionalAngles

theorem sparsePrunedUcry_entry_zero_of_context_ne
    (row column : Fin (gridSize 3))
    (contextNe :
      (splitPrimitiveWire (1 : Fin 3) (primitiveLEBits 3 row)).2 ≠
        (splitPrimitiveWire (1 : Fin 3) (primitiveLEBits 3 column)).2) :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit row column = 0 := by
  unfold sparsePrunedUcryCircuit
  rw [evalPrimitiveCircuitLE_compileUniformlyControlledRy_apply]
  rw [if_neg contextNe]

theorem sparsePrunedUcry_entry_00 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (0 : Fin 8) (0 : Fin 8) =
      (3 : ℂ) / 5 := by
  unfold sparsePrunedUcryCircuit
  change evalPrimitiveCircuitLE _
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 3))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 3)) = _
  rw [evalPrimitiveCircuitLE_compileUniformlyControlledRy_apply]
  rw [if_pos (by native_decide)]
  simp [sparseConditionalAngles, sparseControlWire, primitiveControlAssignment,
    primitiveLEBits, standardRyMatrix_ryAngle35_explicit,
    realOrthogonalRotation]

theorem sparsePrunedUcry_entry_20 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (2 : Fin 8) (0 : Fin 8) =
      (4 : ℂ) / 5 := by
  unfold sparsePrunedUcryCircuit
  change evalPrimitiveCircuitLE _
      (⟨2, by norm_num [gridSize]⟩ : Fin (gridSize 3))
      (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 3)) = _
  rw [evalPrimitiveCircuitLE_compileUniformlyControlledRy_apply]
  rw [if_pos (by native_decide)]
  simp [sparseConditionalAngles, sparseControlWire, primitiveControlAssignment,
    primitiveLEBits, standardRyMatrix_ryAngle35_explicit,
    realOrthogonalRotation]

theorem sparsePrunedUcry_entry_44 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (4 : Fin 8) (4 : Fin 8) = 1 := by
  unfold sparsePrunedUcryCircuit
  change evalPrimitiveCircuitLE _
      (⟨4, by norm_num [gridSize]⟩ : Fin (gridSize 3))
      (⟨4, by norm_num [gridSize]⟩ : Fin (gridSize 3)) = _
  rw [evalPrimitiveCircuitLE_compileUniformlyControlledRy_apply]
  rw [if_pos (by native_decide)]
  simp [sparseConditionalAngles, sparseControlWire, primitiveControlAssignment,
    primitiveLEBits, standardRyMatrix_ryAngleZero]

theorem sparsePrunedUcry_entry_64 :
    evalPrimitiveCircuitLE sparsePrunedUcryCircuit (6 : Fin 8) (4 : Fin 8) = 0 := by
  unfold sparsePrunedUcryCircuit
  change evalPrimitiveCircuitLE _
      (⟨6, by norm_num [gridSize]⟩ : Fin (gridSize 3))
      (⟨4, by norm_num [gridSize]⟩ : Fin (gridSize 3)) = _
  rw [evalPrimitiveCircuitLE_compileUniformlyControlledRy_apply]
  rw [if_pos (by native_decide)]
  simp [sparseConditionalAngles, sparseControlWire, primitiveControlAssignment,
    primitiveLEBits, standardRyMatrix_ryAngleZero]

end QuantumBlockEncoding.StatePreparationPaperEntryCertificates
