import QuantumBlockEncoding.Robin.PaperSevenAmplitudePrimitive

/-!
# Physical embedding of the paper-seven PREPARE

The three selector wires are `q3-q5`.  This file proves the physical eight-wire
PREPARE equal to the selector lift of the already certified three-wire
uniform-seven construction.
-/

namespace QuantumBlockEncoding.Robin

noncomputable def warmRobinPaperSevenSelectorHighMatrix :
    _root_.Matrix (Fin 8) (Fin 8) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv 3)
    (evalPrimitiveGate (.ry (2 : Fin 3) warmRobinUniformSevenHighAngle))

noncomputable def warmRobinPaperSevenSelectorMiddleMatrix :
    _root_.Matrix (Fin 8) (Fin 8) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv 3)
    (controlledRyBlockMatrix warmRobinUniformSevenMiddleWires 1
      warmRobinUniformSevenMiddleWires_ne_target
      warmRobinUniformSevenMiddleAngles)

noncomputable def warmRobinPaperSevenSelectorLowMatrix :
    _root_.Matrix (Fin 8) (Fin 8) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv 3)
    (controlledRyBlockMatrix warmRobinUniformSevenLowWires 0
      warmRobinUniformSevenLowWires_ne_target warmRobinUniformSevenLowAngles)

theorem warmRobinPaperSevenSelectorStages_eq_prepare :
    warmRobinPaperSevenSelectorLowMatrix *
        (warmRobinPaperSevenSelectorMiddleMatrix *
          warmRobinPaperSevenSelectorHighMatrix) =
      warmRobinPaperSevenSelectorPrepare := by
  unfold warmRobinPaperSevenSelectorLowMatrix
    warmRobinPaperSevenSelectorMiddleMatrix
    warmRobinPaperSevenSelectorHighMatrix
    warmRobinPaperSevenSelectorPrepare warmRobinUniformSevenPrepareMatrix
  simp only [map_mul]
  rfl

def warmRobinPaperSevenMiddlePhysicalWires : Fin 1 → Fin 8 := fun _ => 5

theorem warmRobinPaperSevenMiddlePhysicalWires_ne_target
    (wire : Fin 1) :
    warmRobinPaperSevenMiddlePhysicalWires wire ≠ (4 : Fin 8) := by
  fin_cases wire
  decide

def warmRobinPaperSevenLowPhysicalWires : Fin 2 → Fin 8
  | 0 => 4
  | _ => 5

theorem warmRobinPaperSevenLowPhysicalWires_ne_target
    (wire : Fin 2) :
    warmRobinPaperSevenLowPhysicalWires wire ≠ (3 : Fin 8) := by
  fin_cases wire <;> decide

@[simp] theorem warmRobinPaperSevenSelectorBits_decode
    (bits : PrimitiveBasis 8) (wire : Fin 3) :
    primitiveBits3LE (warmRobinPaperSevenSelectorBits bits) wire =
      bits ⟨wire.val + 3, by omega⟩ := by
  fin_cases wire <;> native_decide +revert

theorem warmRobinPaperSevenHighContext_iff
    (row column : PrimitiveBasis 8) :
    (splitPrimitiveWire (5 : Fin 8) row).2 =
        (splitPrimitiveWire (5 : Fin 8) column).2 ↔
      row 6 = column 6 ∧
        (splitPrimitiveWire (2 : Fin 3)
            (primitiveBits3LE (warmRobinPaperSevenSelectorBits row))).2 =
          (splitPrimitiveWire (2 : Fin 3)
            (primitiveBits3LE (warmRobinPaperSevenSelectorBits column))).2 ∧
        (warmRobinPaperSevenSystemBits row, row 7) =
          (warmRobinPaperSevenSystemBits column, column 7) := by
  native_decide +revert

-- Retain pre-4.33 elaboration across the definitionally equal finite index types.
-- This affects tactic unification only; the Lean kernel still checks the proof.
set_option backward.isDefEq.respectTransparency false in
theorem warmRobinPaperSevenHighPhysical_eval :
    evalPrimitiveGate (.ry (5 : Fin 8) warmRobinUniformSevenHighAngle) =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinPaperSevenBitsEquiv.symm
        (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinPaperSevenFullSystem)
          warmRobinPaperSevenSelectorHighMatrix) := by
  rw [evalPrimitiveGate]
  ext row column
  simp only [warmRobinPaperSevenSelectorHighMatrix,
    ComplexLCU.selectorLift, warmRobinPaperSevenBitsEquiv_apply,
    warmRobinPaperSevenBitsIndex, liftPrimitiveOneQubit_apply,
    _root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply,
    _root_.Matrix.submatrix_apply, Equiv.symm_symm,
    _root_.Matrix.kroneckerMap_apply, _root_.Matrix.one_apply,
    evalPrimitiveGate]
  have contextIff := warmRobinPaperSevenHighContext_iff row column
  simp only [primitiveBasisLEEquiv_three_symm]
  by_cases contextsEqual :
      (splitPrimitiveWire (5 : Fin 8) row).2 =
        (splitPrimitiveWire (5 : Fin 8) column).2
  · obtain ⟨h6, hSelector, hSystem⟩ := contextIff.mp contextsEqual
    rw [if_pos contextsEqual, if_pos hSelector]
    simp only [h6, hSystem, if_pos, one_mul, mul_one,
      warmRobinPaperSevenSelectorBits_decode]
    congr 2 <;> norm_num
  · have rhsMiss := not_congr contextIff |>.mp contextsEqual
    rw [if_neg contextsEqual]
    rcases not_and_or.mp rhsMiss with h6 | rest
    · simp [h6]
    · rcases not_and_or.mp rest with hSelector | hSystem
      · simp [hSelector]
      · simp [hSystem]

theorem warmRobinPaperSevenMiddleContext_iff
    (row column : PrimitiveBasis 8) :
    (splitPrimitiveWire (4 : Fin 8) row).2 =
        (splitPrimitiveWire (4 : Fin 8) column).2 ↔
      row 6 = column 6 ∧
        (splitPrimitiveWire (1 : Fin 3)
            (primitiveBits3LE (warmRobinPaperSevenSelectorBits row))).2 =
          (splitPrimitiveWire (1 : Fin 3)
            (primitiveBits3LE (warmRobinPaperSevenSelectorBits column))).2 ∧
        (warmRobinPaperSevenSystemBits row, row 7) =
          (warmRobinPaperSevenSystemBits column, column 7) := by
  native_decide +revert

set_option backward.isDefEq.respectTransparency false in
theorem warmRobinPaperSevenMiddlePhysical_eval :
    controlledRyBlockMatrix warmRobinPaperSevenMiddlePhysicalWires 4
        warmRobinPaperSevenMiddlePhysicalWires_ne_target
        warmRobinUniformSevenMiddleAngles =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinPaperSevenBitsEquiv.symm
        (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinPaperSevenFullSystem)
          warmRobinPaperSevenSelectorMiddleMatrix) := by
  ext row column
  simp only [warmRobinPaperSevenSelectorMiddleMatrix,
    ComplexLCU.selectorLift, warmRobinPaperSevenBitsEquiv_apply,
    warmRobinPaperSevenBitsIndex, controlledRyBlockMatrix_apply,
    _root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply,
    _root_.Matrix.submatrix_apply, Equiv.symm_symm,
    _root_.Matrix.kroneckerMap_apply, _root_.Matrix.one_apply,
    primitiveBasisLEEquiv_three_symm]
  have contextIff := warmRobinPaperSevenMiddleContext_iff row column
  by_cases contextsEqual :
      (splitPrimitiveWire (4 : Fin 8) row).2 =
        (splitPrimitiveWire (4 : Fin 8) column).2
  · obtain ⟨h6, hSelector, hSystem⟩ := contextIff.mp contextsEqual
    rw [if_pos contextsEqual, if_pos hSelector]
    simp only [h6, hSystem, if_pos, one_mul, mul_one]
    have rowControl :
        primitiveControlAssignment warmRobinPaperSevenMiddlePhysicalWires 4
            warmRobinPaperSevenMiddlePhysicalWires_ne_target
            (splitPrimitiveWire (4 : Fin 8) row).2 =
          primitiveControlAssignment warmRobinUniformSevenMiddleWires 1
            warmRobinUniformSevenMiddleWires_ne_target
            (splitPrimitiveWire (1 : Fin 3)
              (primitiveBits3LE (warmRobinPaperSevenSelectorBits row))).2 := by
      funext wire
      fin_cases wire
      simp [primitiveControlAssignment,
        warmRobinPaperSevenMiddlePhysicalWires,
        warmRobinUniformSevenMiddleWires, splitPrimitiveWire]
    rw [rowControl]
    congr 2 <;> simp [warmRobinPaperSevenSelectorBits_decode]
  · have rhsMiss := not_congr contextIff |>.mp contextsEqual
    rw [if_neg contextsEqual]
    rcases not_and_or.mp rhsMiss with h6 | rest
    · simp [h6]
    · rcases not_and_or.mp rest with hSelector | hSystem
      · simp [hSelector]
      · simp [hSystem]

theorem warmRobinPaperSevenLowContext_iff
    (row column : PrimitiveBasis 8) :
    (splitPrimitiveWire (3 : Fin 8) row).2 =
        (splitPrimitiveWire (3 : Fin 8) column).2 ↔
      row 6 = column 6 ∧
        (splitPrimitiveWire (0 : Fin 3)
            (primitiveBits3LE (warmRobinPaperSevenSelectorBits row))).2 =
          (splitPrimitiveWire (0 : Fin 3)
            (primitiveBits3LE (warmRobinPaperSevenSelectorBits column))).2 ∧
        (warmRobinPaperSevenSystemBits row, row 7) =
          (warmRobinPaperSevenSystemBits column, column 7) := by
  native_decide +revert

set_option backward.isDefEq.respectTransparency false in
theorem warmRobinPaperSevenLowPhysical_eval :
    controlledRyBlockMatrix warmRobinPaperSevenLowPhysicalWires 3
        warmRobinPaperSevenLowPhysicalWires_ne_target
        warmRobinUniformSevenLowAngles =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinPaperSevenBitsEquiv.symm
        (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinPaperSevenFullSystem)
          warmRobinPaperSevenSelectorLowMatrix) := by
  ext row column
  simp only [warmRobinPaperSevenSelectorLowMatrix,
    ComplexLCU.selectorLift, warmRobinPaperSevenBitsEquiv_apply,
    warmRobinPaperSevenBitsIndex, controlledRyBlockMatrix_apply,
    _root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply,
    _root_.Matrix.submatrix_apply, Equiv.symm_symm,
    _root_.Matrix.kroneckerMap_apply, _root_.Matrix.one_apply,
    primitiveBasisLEEquiv_three_symm]
  have contextIff := warmRobinPaperSevenLowContext_iff row column
  by_cases contextsEqual :
      (splitPrimitiveWire (3 : Fin 8) row).2 =
        (splitPrimitiveWire (3 : Fin 8) column).2
  · obtain ⟨h6, hSelector, hSystem⟩ := contextIff.mp contextsEqual
    rw [if_pos contextsEqual, if_pos hSelector]
    simp only [h6, hSystem, if_pos, one_mul, mul_one]
    have rowControl :
        primitiveControlAssignment warmRobinPaperSevenLowPhysicalWires 3
            warmRobinPaperSevenLowPhysicalWires_ne_target
            (splitPrimitiveWire (3 : Fin 8) row).2 =
          primitiveControlAssignment warmRobinUniformSevenLowWires 0
            warmRobinUniformSevenLowWires_ne_target
            (splitPrimitiveWire (0 : Fin 3)
              (primitiveBits3LE (warmRobinPaperSevenSelectorBits row))).2 := by
      funext wire
      fin_cases wire <;>
        simp [primitiveControlAssignment,
          warmRobinPaperSevenLowPhysicalWires,
          warmRobinUniformSevenLowWires, splitPrimitiveWire]
    rw [rowControl]
    congr 2 <;> simp [warmRobinPaperSevenSelectorBits_decode]
  · have rhsMiss := not_congr contextIff |>.mp contextsEqual
    rw [if_neg contextsEqual]
    rcases not_and_or.mp rhsMiss with h6 | rest
    · simp [h6]
    · rcases not_and_or.mp rest with hSelector | hSystem
      · simp [hSelector]
      · simp [hSystem]

noncomputable def warmRobinPaperSevenSelectorPrepareCircuit :
    PrimitiveCircuit 8 :=
  [.ry 5 warmRobinUniformSevenHighAngle] ++
    compileUniformlyControlledRy 1 warmRobinPaperSevenMiddlePhysicalWires 4
      warmRobinPaperSevenMiddlePhysicalWires_ne_target
      warmRobinUniformSevenMiddleAngles ++
    compileUniformlyControlledRy 2 warmRobinPaperSevenLowPhysicalWires 3
      warmRobinPaperSevenLowPhysicalWires_ne_target
      warmRobinUniformSevenLowAngles

theorem warmRobinPaperSevenSelectorPrepareCircuit_eval :
    evalPrimitiveCircuit warmRobinPaperSevenSelectorPrepareCircuit =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinPaperSevenBitsEquiv.symm
        (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinPaperSevenFullSystem)
          warmRobinPaperSevenSelectorPrepare) := by
  unfold warmRobinPaperSevenSelectorPrepareCircuit
  rw [evalPrimitiveCircuit_append, evalPrimitiveCircuit_append,
    compileUniformlyControlledRy_eval_controlledRyBlockMatrix,
    compileUniformlyControlledRy_eval_controlledRyBlockMatrix]
  simp only [evalPrimitiveCircuit, _root_.Matrix.one_mul]
  rw [
    warmRobinPaperSevenHighPhysical_eval,
    warmRobinPaperSevenMiddlePhysical_eval,
    warmRobinPaperSevenLowPhysical_eval,
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

noncomputable def warmRobinPaperSevenSelectorUnprepareCircuit : PrimitiveCircuit 8 :=
  warmRobinPaperSevenSelectorPrepareCircuit.reverse.map PrimitiveGate.dagger

theorem warmRobinPaperSevenSelectorUnprepareCircuit_eval :
    evalPrimitiveCircuit warmRobinPaperSevenSelectorUnprepareCircuit =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinPaperSevenBitsEquiv.symm
        (star (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinPaperSevenFullSystem)
          warmRobinPaperSevenSelectorPrepare)) := by
  rw [warmRobinPaperSevenSelectorUnprepareCircuit,
    evalPrimitiveCircuit_dagger,
    warmRobinPaperSevenSelectorPrepareCircuit_eval]
  ext row column
  rfl

end QuantumBlockEncoding.Robin
