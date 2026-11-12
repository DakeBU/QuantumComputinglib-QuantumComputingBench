import QuantumBlockEncoding.Robin.PaperSevenPrimitive

/-!
# Exact paper-seven amplitude compiler

The coefficient signal is `q6`.  The six controls are the three system wires
`q0-q2` and three selector wires `q3-q5`; the reversible workspace `q7` is a
spectator.  The reference uniformly-controlled-RY compiler emits only the
repository primitive basis and is proved equal to the logical amplitude lift.
-/

namespace QuantumBlockEncoding.Robin

def warmRobinPaperSevenAmplitudeControlWires : Fin 6 → Fin 8 := fun wire =>
  ⟨wire.val, by omega⟩

theorem warmRobinPaperSevenAmplitudeControlWires_ne_target
    (wire : Fin 6) :
    warmRobinPaperSevenAmplitudeControlWires wire ≠ (6 : Fin 8) := by
  intro equality
  have valueEquality : wire.val = 6 := congrArg Fin.val equality
  omega

def warmRobinPaperSevenAmplitudeSystem
    (bits : PrimitiveBasis 6) : Fin 8 :=
  ⟨(bits 0).val + 2 * (bits 1).val + 4 * (bits 2).val, by omega⟩

def warmRobinPaperSevenAmplitudeSelector
    (bits : PrimitiveBasis 6) : Fin 8 :=
  ⟨(bits 3).val + 2 * (bits 4).val + 4 * (bits 5).val, by omega⟩

noncomputable def warmRobinPaperSevenAmplitudeAngle
    (bits : PrimitiveBasis 6) : ExactAngle :=
  .twiceArccosRational
    (warmRobinPaperSevenCoefficientRat
      (warmRobinPaperSevenAmplitudeSelector bits)
      (warmRobinPaperSevenAmplitudeSystem bits))
    (by
      simpa [warmRobinPaperSevenCoefficient] using
        warmRobinPaperSevenCoefficient_abs_le_one
          (warmRobinPaperSevenAmplitudeSelector bits)
          (warmRobinPaperSevenAmplitudeSystem bits))

theorem warmRobinPaperSevenAmplitudeRy_eq_rotation
    (bits : PrimitiveBasis 6) :
    standardRyMatrix (warmRobinPaperSevenAmplitudeAngle bits).eval =
      warmRobinPaperSevenRotation
        (warmRobinPaperSevenAmplitudeSelector bits)
        (warmRobinPaperSevenAmplitudeSystem bits) := by
  unfold warmRobinPaperSevenAmplitudeAngle warmRobinPaperSevenRotation
  have bounded := abs_le.mp
    (warmRobinPaperSevenCoefficient_abs_le_one
      (warmRobinPaperSevenAmplitudeSelector bits)
      (warmRobinPaperSevenAmplitudeSystem bits))
  exact standardRyMatrix_two_arccos_eq_amplitudeRotation _
    bounded.1 bounded.2

def warmRobinPaperSevenAmplitudeContextIndex
    (context : OtherPrimitiveWires (6 : Fin 8) → Fin 2) :
    Fin 8 × WarmRobinPaperSevenFullSystem :=
  let bit (wire : Fin 6) : Fin 2 :=
    context ⟨warmRobinPaperSevenAmplitudeControlWires wire,
      warmRobinPaperSevenAmplitudeControlWires_ne_target wire⟩
  let system : Fin 8 :=
    ⟨(bit 0).val + 2 * (bit 1).val + 4 * (bit 2).val, by omega⟩
  let selector : Fin 8 :=
    ⟨(bit 3).val + 2 * (bit 4).val + 4 * (bit 5).val, by omega⟩
  (selector, (system, context ⟨7, by decide⟩))

theorem warmRobinPaperSevenAmplitudeContextIndex_bijective :
    Function.Bijective warmRobinPaperSevenAmplitudeContextIndex := by
  native_decide

noncomputable def warmRobinPaperSevenAmplitudeContextEquiv :
    (OtherPrimitiveWires (6 : Fin 8) → Fin 2) ≃
      Fin 8 × WarmRobinPaperSevenFullSystem :=
  Equiv.ofBijective warmRobinPaperSevenAmplitudeContextIndex
    warmRobinPaperSevenAmplitudeContextIndex_bijective

@[simp] theorem warmRobinPaperSevenAmplitudeContextEquiv_apply
    (context : OtherPrimitiveWires (6 : Fin 8) → Fin 2) :
    warmRobinPaperSevenAmplitudeContextEquiv context =
      warmRobinPaperSevenAmplitudeContextIndex context := rfl

theorem warmRobinPaperSevenAmplitude_context_iff
    (row column : PrimitiveBasis 8) :
    (splitPrimitiveWire (6 : Fin 8) row).2 =
        (splitPrimitiveWire (6 : Fin 8) column).2 ↔
      (warmRobinPaperSevenBitsEquiv row).2 =
        (warmRobinPaperSevenBitsEquiv column).2 := by
  change _ ↔
    warmRobinPaperSevenAmplitudeContextEquiv
        (splitPrimitiveWire (6 : Fin 8) row).2 =
      warmRobinPaperSevenAmplitudeContextEquiv
        (splitPrimitiveWire (6 : Fin 8) column).2
  exact warmRobinPaperSevenAmplitudeContextEquiv.injective.eq_iff.symm

/-- Exact equality between the physical six-control RY block and the logical
amplitude lift, including the otherwise dirty `q7` workspace coordinate. -/
theorem warmRobinPaperSevenControlledRy_eq_amplitudeLift :
    controlledRyBlockMatrix warmRobinPaperSevenAmplitudeControlWires 6
        warmRobinPaperSevenAmplitudeControlWires_ne_target
        warmRobinPaperSevenAmplitudeAngle =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinPaperSevenBitsEquiv.symm
        (ComplexLCU.amplitudeLift warmRobinPaperSevenWorkspaceRotation) := by
  ext row column
  simp only [controlledRyBlockMatrix,
    _root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply,
    _root_.Matrix.submatrix_apply, _root_.Matrix.blockDiagonal_apply,
    ComplexLCU.amplitudeLift_apply, Equiv.symm_symm]
  have contextIff := warmRobinPaperSevenAmplitude_context_iff row column
  by_cases contextsEqual :
      (splitPrimitiveWire (6 : Fin 8) row).2 =
        (splitPrimitiveWire (6 : Fin 8) column).2
  · rw [if_pos contextsEqual, if_pos (contextIff.mp contextsEqual)]
    have rotation := warmRobinPaperSevenAmplitudeRy_eq_rotation
      (primitiveControlAssignment warmRobinPaperSevenAmplitudeControlWires 6
        warmRobinPaperSevenAmplitudeControlWires_ne_target
        (splitPrimitiveWire (6 : Fin 8) row).2)
    have rotationEntry := congrFun (congrFun rotation
      (splitPrimitiveWire (6 : Fin 8) row).1)
      (splitPrimitiveWire (6 : Fin 8) column).1
    simpa [warmRobinPaperSevenWorkspaceRotation,
      warmRobinPaperSevenBitsEquiv_apply,
      warmRobinPaperSevenBitsIndex,
      warmRobinPaperSevenAmplitudeContextIndex,
      primitiveControlAssignment,
      warmRobinPaperSevenAmplitudeControlWires,
      warmRobinPaperSevenAmplitudeSelector,
      warmRobinPaperSevenAmplitudeSystem,
      warmRobinPaperSevenSelectorBits, warmRobinPaperSevenSystemBits,
      splitPrimitiveWire] using rotationEntry
  · rw [if_neg contextsEqual, if_neg (not_congr contextIff |>.mp contextsEqual)]

noncomputable def warmRobinPaperSevenAmplitudeCircuit : PrimitiveCircuit 8 :=
  compileUniformlyControlledRy 6 warmRobinPaperSevenAmplitudeControlWires 6
    warmRobinPaperSevenAmplitudeControlWires_ne_target
    warmRobinPaperSevenAmplitudeAngle

noncomputable def warmRobinPaperSevenAmplitudeProgram : PrimitiveProgram 8 where
  circuit := warmRobinPaperSevenAmplitudeCircuit
  globalPhase := .rational 0

theorem warmRobinPaperSevenAmplitudeProgram_eval :
    evalPrimitiveProgram warmRobinPaperSevenAmplitudeProgram =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinPaperSevenBitsEquiv.symm
        (ComplexLCU.amplitudeLift warmRobinPaperSevenWorkspaceRotation) := by
  change evalGlobalPhase (.rational 0) •
      evalPrimitiveCircuit warmRobinPaperSevenAmplitudeCircuit = _
  have phaseZero : evalGlobalPhase (.rational 0) = 1 := by
    simp [evalGlobalPhase, ExactAngle.eval]
  rw [phaseZero, one_smul]
  unfold warmRobinPaperSevenAmplitudeCircuit
  rw [compileUniformlyControlledRy_eval_controlledRyBlockMatrix,
    warmRobinPaperSevenControlledRy_eq_amplitudeLift]

theorem warmRobinPaperSevenAmplitudeProgram_noOracleCalls :
    warmRobinPaperSevenAmplitudeProgram.resource.oracleCalls = 0 :=
  PrimitiveCircuit.resource_oracleCalls_eq_zero _

end QuantumBlockEncoding.Robin
