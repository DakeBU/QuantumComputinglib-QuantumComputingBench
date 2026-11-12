import QuantumBlockEncoding.Robin.Figure4Loaders
import QuantumBlockEncoding.Robin.PaperSevenPreparePrimitive

/-!
# Exact nine-wire embedding of the Figure-4 PREPARE

The source circuit prepares the padded seven-slot selector on `q0-q2`.
This module proves that physical circuit equal to the corresponding selector
lift while leaving the system, coefficient, indicator, and workspace wires
untouched.
-/

namespace QuantumBlockEncoding.Robin

abbrev WarmRobinFigure4FullSystem := Fin 8 × (Fin 2 × Fin 2)

def warmRobinFigure4EncodeBits
    (coefficient : Fin 2) (selector : Fin 8)
    (system : WarmRobinFigure4FullSystem) : PrimitiveBasis 9
  | ⟨0, _⟩ => primitiveBits3LE selector 0
  | ⟨1, _⟩ => primitiveBits3LE selector 1
  | ⟨2, _⟩ => primitiveBits3LE selector 2
  | ⟨3, _⟩ => primitiveBits3LE system.1 0
  | ⟨4, _⟩ => primitiveBits3LE system.1 1
  | ⟨5, _⟩ => primitiveBits3LE system.1 2
  | ⟨6, _⟩ => coefficient
  | ⟨7, _⟩ => system.2.1
  | _ => system.2.2

def warmRobinFigure4BitsIndex (bits : PrimitiveBasis 9) :
    ComplexLCU.LCUIndex (Fin 2) (Fin 8) WarmRobinFigure4FullSystem :=
  (bits 6, (warmRobinFigure4AddressBits bits,
    (warmRobinFigure4SystemBits bits, (bits 7, bits 8))))

theorem warmRobinFigure4BitsIndex_bijective :
    Function.Bijective warmRobinFigure4BitsIndex := by
  native_decide

noncomputable def warmRobinFigure4BitsEquiv :
    PrimitiveBasis 9 ≃
      ComplexLCU.LCUIndex (Fin 2) (Fin 8) WarmRobinFigure4FullSystem :=
  Equiv.ofBijective warmRobinFigure4BitsIndex
    warmRobinFigure4BitsIndex_bijective

@[simp] theorem warmRobinFigure4BitsEquiv_apply (bits : PrimitiveBasis 9) :
    warmRobinFigure4BitsEquiv bits = warmRobinFigure4BitsIndex bits := rfl

@[simp] theorem warmRobinFigure4BitsEquiv_encode
    (coefficient : Fin 2) (selector : Fin 8)
    (system : WarmRobinFigure4FullSystem) :
    warmRobinFigure4BitsEquiv
        (warmRobinFigure4EncodeBits coefficient selector system) =
      (coefficient, (selector, system)) := by
  rw [warmRobinFigure4BitsEquiv_apply]
  native_decide +revert

def warmRobinFigure4PrepareMiddleWires : Fin 1 → Fin 9 := fun _ => 2

theorem warmRobinFigure4PrepareMiddleWires_ne_target (wire : Fin 1) :
    warmRobinFigure4PrepareMiddleWires wire ≠ (1 : Fin 9) := by
  fin_cases wire
  decide

def warmRobinFigure4PrepareLowWires : Fin 2 → Fin 9
  | 0 => 1
  | _ => 2

theorem warmRobinFigure4PrepareLowWires_ne_target (wire : Fin 2) :
    warmRobinFigure4PrepareLowWires wire ≠ (0 : Fin 9) := by
  fin_cases wire <;> decide

@[simp] theorem warmRobinFigure4SelectorBits_decode
    (bits : PrimitiveBasis 9) (wire : Fin 3) :
    primitiveBits3LE (warmRobinFigure4AddressBits bits) wire =
      bits ⟨wire.val, by omega⟩ := by
  fin_cases wire <;> native_decide +revert

theorem warmRobinFigure4PrepareHighContext_iff
    (row column : PrimitiveBasis 9) :
    (splitPrimitiveWire (2 : Fin 9) row).2 =
        (splitPrimitiveWire (2 : Fin 9) column).2 ↔
      row 6 = column 6 ∧
        (splitPrimitiveWire (2 : Fin 3)
            (primitiveBits3LE (warmRobinFigure4AddressBits row))).2 =
          (splitPrimitiveWire (2 : Fin 3)
            (primitiveBits3LE (warmRobinFigure4AddressBits column))).2 ∧
        (warmRobinFigure4SystemBits row, (row 7, row 8)) =
          (warmRobinFigure4SystemBits column, (column 7, column 8)) := by
  native_decide +revert

set_option backward.isDefEq.respectTransparency false in
theorem warmRobinFigure4PrepareHighPhysical_eval :
    evalPrimitiveGate (.ry (2 : Fin 9) warmRobinUniformSevenHighAngle) =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinFigure4BitsEquiv.symm
        (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinFigure4FullSystem)
          warmRobinPaperSevenSelectorHighMatrix) := by
  rw [evalPrimitiveGate]
  ext row column
  simp only [warmRobinPaperSevenSelectorHighMatrix,
    ComplexLCU.selectorLift, warmRobinFigure4BitsEquiv_apply,
    warmRobinFigure4BitsIndex, liftPrimitiveOneQubit_apply,
    _root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply,
    _root_.Matrix.submatrix_apply, Equiv.symm_symm,
    _root_.Matrix.kroneckerMap_apply, _root_.Matrix.one_apply,
    evalPrimitiveGate]
  have contextIff := warmRobinFigure4PrepareHighContext_iff row column
  simp only [primitiveBasisLEEquiv_three_symm]
  by_cases contextsEqual :
      (splitPrimitiveWire (2 : Fin 9) row).2 =
        (splitPrimitiveWire (2 : Fin 9) column).2
  · obtain ⟨h6, hSelector, hSystem⟩ := contextIff.mp contextsEqual
    rw [if_pos contextsEqual, if_pos hSelector]
    simp only [h6, hSystem, if_pos, one_mul, mul_one,
      warmRobinFigure4SelectorBits_decode]
    congr 2 <;> norm_num
  · have rhsMiss := not_congr contextIff |>.mp contextsEqual
    rw [if_neg contextsEqual]
    rcases not_and_or.mp rhsMiss with h6 | rest
    · simp [h6]
    · rcases not_and_or.mp rest with hSelector | hSystem
      · simp [hSelector]
      · simp [hSystem]

theorem warmRobinFigure4PrepareMiddleContext_iff
    (row column : PrimitiveBasis 9) :
    (splitPrimitiveWire (1 : Fin 9) row).2 =
        (splitPrimitiveWire (1 : Fin 9) column).2 ↔
      row 6 = column 6 ∧
        (splitPrimitiveWire (1 : Fin 3)
            (primitiveBits3LE (warmRobinFigure4AddressBits row))).2 =
          (splitPrimitiveWire (1 : Fin 3)
            (primitiveBits3LE (warmRobinFigure4AddressBits column))).2 ∧
        (warmRobinFigure4SystemBits row, (row 7, row 8)) =
          (warmRobinFigure4SystemBits column, (column 7, column 8)) := by
  native_decide +revert

set_option backward.isDefEq.respectTransparency false in
theorem warmRobinFigure4PrepareMiddlePhysical_eval :
    controlledRyBlockMatrix warmRobinFigure4PrepareMiddleWires 1
        warmRobinFigure4PrepareMiddleWires_ne_target
        warmRobinUniformSevenMiddleAngles =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinFigure4BitsEquiv.symm
        (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinFigure4FullSystem)
          warmRobinPaperSevenSelectorMiddleMatrix) := by
  ext row column
  simp only [warmRobinPaperSevenSelectorMiddleMatrix,
    ComplexLCU.selectorLift, warmRobinFigure4BitsEquiv_apply,
    warmRobinFigure4BitsIndex, controlledRyBlockMatrix_apply,
    _root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply,
    _root_.Matrix.submatrix_apply, Equiv.symm_symm,
    _root_.Matrix.kroneckerMap_apply, _root_.Matrix.one_apply,
    primitiveBasisLEEquiv_three_symm]
  have contextIff := warmRobinFigure4PrepareMiddleContext_iff row column
  by_cases contextsEqual :
      (splitPrimitiveWire (1 : Fin 9) row).2 =
        (splitPrimitiveWire (1 : Fin 9) column).2
  · obtain ⟨h6, hSelector, hSystem⟩ := contextIff.mp contextsEqual
    rw [if_pos contextsEqual, if_pos hSelector]
    simp only [h6, hSystem, if_pos, one_mul, mul_one]
    have rowControl :
        primitiveControlAssignment warmRobinFigure4PrepareMiddleWires 1
            warmRobinFigure4PrepareMiddleWires_ne_target
            (splitPrimitiveWire (1 : Fin 9) row).2 =
          primitiveControlAssignment warmRobinUniformSevenMiddleWires 1
            warmRobinUniformSevenMiddleWires_ne_target
            (splitPrimitiveWire (1 : Fin 3)
              (primitiveBits3LE (warmRobinFigure4AddressBits row))).2 := by
      funext wire
      fin_cases wire
      simp [primitiveControlAssignment, warmRobinFigure4PrepareMiddleWires,
        warmRobinUniformSevenMiddleWires, splitPrimitiveWire]
    rw [rowControl]
    congr 2 <;> simp [warmRobinFigure4SelectorBits_decode]
  · have rhsMiss := not_congr contextIff |>.mp contextsEqual
    rw [if_neg contextsEqual]
    rcases not_and_or.mp rhsMiss with h6 | rest
    · simp [h6]
    · rcases not_and_or.mp rest with hSelector | hSystem
      · simp [hSelector]
      · simp [hSystem]

theorem warmRobinFigure4PrepareLowContext_iff
    (row column : PrimitiveBasis 9) :
    (splitPrimitiveWire (0 : Fin 9) row).2 =
        (splitPrimitiveWire (0 : Fin 9) column).2 ↔
      row 6 = column 6 ∧
        (splitPrimitiveWire (0 : Fin 3)
            (primitiveBits3LE (warmRobinFigure4AddressBits row))).2 =
          (splitPrimitiveWire (0 : Fin 3)
            (primitiveBits3LE (warmRobinFigure4AddressBits column))).2 ∧
        (warmRobinFigure4SystemBits row, (row 7, row 8)) =
          (warmRobinFigure4SystemBits column, (column 7, column 8)) := by
  native_decide +revert

set_option backward.isDefEq.respectTransparency false in
theorem warmRobinFigure4PrepareLowPhysical_eval :
    controlledRyBlockMatrix warmRobinFigure4PrepareLowWires 0
        warmRobinFigure4PrepareLowWires_ne_target
        warmRobinUniformSevenLowAngles =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinFigure4BitsEquiv.symm
        (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinFigure4FullSystem)
          warmRobinPaperSevenSelectorLowMatrix) := by
  ext row column
  simp only [warmRobinPaperSevenSelectorLowMatrix,
    ComplexLCU.selectorLift, warmRobinFigure4BitsEquiv_apply,
    warmRobinFigure4BitsIndex, controlledRyBlockMatrix_apply,
    _root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply,
    _root_.Matrix.submatrix_apply, Equiv.symm_symm,
    _root_.Matrix.kroneckerMap_apply, _root_.Matrix.one_apply,
    primitiveBasisLEEquiv_three_symm]
  have contextIff := warmRobinFigure4PrepareLowContext_iff row column
  by_cases contextsEqual :
      (splitPrimitiveWire (0 : Fin 9) row).2 =
        (splitPrimitiveWire (0 : Fin 9) column).2
  · obtain ⟨h6, hSelector, hSystem⟩ := contextIff.mp contextsEqual
    rw [if_pos contextsEqual, if_pos hSelector]
    simp only [h6, hSystem, if_pos, one_mul, mul_one]
    have rowControl :
        primitiveControlAssignment warmRobinFigure4PrepareLowWires 0
            warmRobinFigure4PrepareLowWires_ne_target
            (splitPrimitiveWire (0 : Fin 9) row).2 =
          primitiveControlAssignment warmRobinUniformSevenLowWires 0
            warmRobinUniformSevenLowWires_ne_target
            (splitPrimitiveWire (0 : Fin 3)
              (primitiveBits3LE (warmRobinFigure4AddressBits row))).2 := by
      funext wire
      fin_cases wire <;>
        simp [primitiveControlAssignment, warmRobinFigure4PrepareLowWires,
          warmRobinUniformSevenLowWires, splitPrimitiveWire]
    rw [rowControl]
    congr 2 <;> simp [warmRobinFigure4SelectorBits_decode]
  · have rhsMiss := not_congr contextIff |>.mp contextsEqual
    rw [if_neg contextsEqual]
    rcases not_and_or.mp rhsMiss with h6 | rest
    · simp [h6]
    · rcases not_and_or.mp rest with hSelector | hSystem
      · simp [hSelector]
      · simp [hSystem]

noncomputable def warmRobinFigure4SelectorPrepareCircuit : PrimitiveCircuit 9 :=
  [.ry 2 warmRobinUniformSevenHighAngle] ++
    compileUniformlyControlledRy 1 warmRobinFigure4PrepareMiddleWires 1
      warmRobinFigure4PrepareMiddleWires_ne_target
      warmRobinUniformSevenMiddleAngles ++
    compileUniformlyControlledRy 2 warmRobinFigure4PrepareLowWires 0
      warmRobinFigure4PrepareLowWires_ne_target
      warmRobinUniformSevenLowAngles

noncomputable def warmRobinFigure4SelectorPrepareProgram : PrimitiveProgram 9 where
  circuit := warmRobinFigure4SelectorPrepareCircuit
  globalPhase := .rational 0

/-- Required stage root: the physical first stage is the exact selector lift. -/
theorem warmRobinFigure4_after_prepare :
    evalPrimitiveProgram warmRobinFigure4SelectorPrepareProgram =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinFigure4BitsEquiv.symm
        (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinFigure4FullSystem)
          warmRobinPaperSevenSelectorPrepare) := by
  change evalGlobalPhase (.rational 0) •
      evalPrimitiveCircuit warmRobinFigure4SelectorPrepareCircuit = _
  have phaseZero : evalGlobalPhase (.rational 0) = 1 := by
    simp [evalGlobalPhase, ExactAngle.eval]
  rw [phaseZero, one_smul]
  unfold warmRobinFigure4SelectorPrepareCircuit
  rw [evalPrimitiveCircuit_append, evalPrimitiveCircuit_append,
    compileUniformlyControlledRy_eval_controlledRyBlockMatrix,
    compileUniformlyControlledRy_eval_controlledRyBlockMatrix]
  simp only [evalPrimitiveCircuit, _root_.Matrix.one_mul]
  rw [warmRobinFigure4PrepareHighPhysical_eval,
    warmRobinFigure4PrepareMiddlePhysical_eval,
    warmRobinFigure4PrepareLowPhysical_eval,
    ← _root_.Matrix.reindexAlgEquiv_mul,
    ← _root_.Matrix.reindexAlgEquiv_mul]
  congr 1
  unfold ComplexLCU.selectorLift
  rw [← _root_.Matrix.mul_kronecker_mul,
    ← _root_.Matrix.mul_kronecker_mul,
    ← _root_.Matrix.mul_kronecker_mul,
    ← _root_.Matrix.mul_kronecker_mul]
  simp only [_root_.Matrix.one_mul]
  rw [warmRobinPaperSevenSelectorStages_eq_prepare]

noncomputable def warmRobinFigure4SelectorUnprepareProgram : PrimitiveProgram 9 :=
  warmRobinFigure4SelectorPrepareProgram.dagger

theorem warmRobinFigure4_after_unprepare :
    evalPrimitiveProgram warmRobinFigure4SelectorUnprepareProgram =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinFigure4BitsEquiv.symm
        (star (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinFigure4FullSystem)
          warmRobinPaperSevenSelectorPrepare)) := by
  rw [warmRobinFigure4SelectorUnprepareProgram,
    evalPrimitiveProgram_dagger, warmRobinFigure4_after_prepare]
  ext row column
  rfl

end QuantumBlockEncoding.Robin
