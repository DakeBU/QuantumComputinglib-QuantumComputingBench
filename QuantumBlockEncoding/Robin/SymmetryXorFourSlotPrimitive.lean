import QuantumBlockEncoding.PrimitiveRefinement
import QuantumBlockEncoding.Robin.SymmetryFourSlotPrimitive
import QuantumBlockEncoding.Robin.SymmetryXorFourSlotLogicalUnitary
import QuantumBlockEncoding.UniformlyControlledRy
import Mathlib.Tactic

/-!
# Primitive XOR SELECT for the Robin four-slot route

The selector occupies wires `q3,q4`; the pair coordinate occupies `q0,q1`.
The chronological circuit is exactly `CX(q3,q0); CX(q4,q1)`.
-/

namespace QuantumBlockEncoding.Robin

open scoped Kronecker

def warmRobinXorFourSlotSelectCircuit : PrimitiveCircuit 6 :=
  [ .cx 3 0 (by decide), .cx 4 1 (by decide) ]

def warmRobinXorFourSlotSelectBasisEquiv :
    PrimitiveBasis 6 ≃ PrimitiveBasis 6 :=
  (cxBasisEquiv (3 : Fin 6) (0 : Fin 6) (by decide)).trans
    (cxBasisEquiv (4 : Fin 6) (1 : Fin 6) (by decide))

/-- The two selected system bits are XORed with the selector, while the sector,
selector, and coefficient wires are unchanged. -/
theorem warmRobinXorFourSlotSelectBasisAction_eq_perm :
    ∀ bits : PrimitiveBasis 6,
      let selected := warmRobinXorFourSlotSelectBasisEquiv bits
      (selected 0).val + 2 * (selected 1).val =
          ((bits 0).val + 2 * (bits 1).val) ^^^
            ((bits 3).val + 2 * (bits 4).val) ∧
        selected 2 = bits 2 ∧ selected 3 = bits 3 ∧
        selected 4 = bits 4 ∧ selected 5 = bits 5 := by
  native_decide +revert

/-- Exact matrix semantics of the physical XOR SELECT program. -/
theorem warmRobinXorFourSlotSelectProgram_eval :
    evalPrimitiveCircuit warmRobinXorFourSlotSelectCircuit =
      ComplexLCU.equivPermutationMatrix warmRobinXorFourSlotSelectBasisEquiv := by
  simp only [warmRobinXorFourSlotSelectCircuit, evalPrimitiveCircuit,
    evalPrimitiveGate, Matrix.one_mul]
  rw [ComplexLCU.equivPermutationMatrix_mul]
  rfl

theorem warmRobinXorFourSlotSelectProgram_noOracleCalls :
    warmRobinXorFourSlotSelectCircuit.resource.oracleCalls = 0 :=
  PrimitiveCircuit.resource_oracleCalls_eq_zero _

def warmRobinXorFourSlotControlWires : Fin 5 → Fin 6 := fun wire =>
  ⟨wire.val, by omega⟩

theorem warmRobinXorFourSlotControlWires_ne_target
    (wire : Fin 5) : warmRobinXorFourSlotControlWires wire ≠ (5 : Fin 6) := by
  intro equality
  have valueEquality : wire.val = 5 := congrArg Fin.val equality
  omega

def warmRobinXorFourSlotControlPair
    (bits : PrimitiveBasis 5) : Fin 4 :=
  ⟨(bits 0).val + 2 * (bits 1).val, by omega⟩

def warmRobinXorFourSlotControlSector
    (bits : PrimitiveBasis 5) : Fin 2 := bits 2

def warmRobinXorFourSlotControlSelector
    (bits : PrimitiveBasis 5) : Fin 4 :=
  ⟨(bits 3).val + 2 * (bits 4).val, by omega⟩

/-- Exact standard-RY angle for each of the 32 multiplexor branches. -/
noncomputable def warmRobinXorFourSlotAmplitudeAngle
    (bits : PrimitiveBasis 5) : ExactAngle :=
  let column : WarmRobinSymmetrySystem :=
    (warmRobinXorFourSlotControlSector bits,
      warmRobinXorFourSlotControlPair bits)
  let slot := warmRobinXorFourSlotControlSelector bits
  .twiceArccosRational
    (warmRobinSymmetryXorAmplitude column.1 slot column.2)
    (by
      simpa [warmRobinXorFourSlotCoefficient] using
        warmRobinXorFourSlotCoefficient_abs_le_one slot column)

theorem warmRobinXorFourSlotAmplitudeAngle_eval
    (bits : PrimitiveBasis 5) :
    (warmRobinXorFourSlotAmplitudeAngle bits).eval =
      2 * Real.arccos
        (warmRobinXorFourSlotCoefficient
          (warmRobinXorFourSlotControlSelector bits)
          (warmRobinXorFourSlotControlSector bits,
            warmRobinXorFourSlotControlPair bits)) := by
  rfl

/-- Every exact angle denotes the corresponding T2 amplitude rotation. -/
theorem warmRobinXorFourSlotAmplitudeRy_eq_rotation
    (bits : PrimitiveBasis 5) :
    standardRyMatrix (warmRobinXorFourSlotAmplitudeAngle bits).eval =
      warmRobinXorFourSlotRotation
        (warmRobinXorFourSlotControlSelector bits)
        (warmRobinXorFourSlotControlSector bits,
          warmRobinXorFourSlotControlPair bits) := by
  rw [warmRobinXorFourSlotAmplitudeAngle_eval]
  unfold warmRobinXorFourSlotRotation
  have bounded := abs_le.mp
    (warmRobinXorFourSlotCoefficient_abs_le_one
      (warmRobinXorFourSlotControlSelector bits)
      (warmRobinXorFourSlotControlSector bits,
        warmRobinXorFourSlotControlPair bits))
  exact standardRyMatrix_two_arccos_eq_amplitudeRotation _
    bounded.1 bounded.2

def warmRobinXorFourSlotContextIndex
    (context : OtherPrimitiveWires (5 : Fin 6) → Fin 2) :
    Fin 4 × WarmRobinSymmetrySystem :=
  let bit (wire : Fin 5) : Fin 2 :=
    context ⟨warmRobinXorFourSlotControlWires wire,
      warmRobinXorFourSlotControlWires_ne_target wire⟩
  (⟨(bit 3).val + 2 * (bit 4).val, by omega⟩,
    (bit 2, ⟨(bit 0).val + 2 * (bit 1).val, by omega⟩))

theorem warmRobinXorFourSlotContextIndex_bijective :
    Function.Bijective warmRobinXorFourSlotContextIndex := by
  native_decide

noncomputable def warmRobinXorFourSlotContextEquiv :
    (OtherPrimitiveWires (5 : Fin 6) → Fin 2) ≃
      Fin 4 × WarmRobinSymmetrySystem :=
  Equiv.ofBijective warmRobinXorFourSlotContextIndex
    warmRobinXorFourSlotContextIndex_bijective

@[simp] theorem warmRobinXorFourSlotContextEquiv_apply
    (context : OtherPrimitiveWires (5 : Fin 6) → Fin 2) :
    warmRobinXorFourSlotContextEquiv context =
      warmRobinXorFourSlotContextIndex context := rfl

noncomputable def warmRobinXorFourSlotMiddleBitsEquiv :
    PrimitiveBasis 6 ≃
      ComplexLCU.LCUIndex (Fin 2) (Fin 4) WarmRobinSymmetrySystem :=
  (splitPrimitiveWire 5).trans
    (Equiv.prodCongr (Equiv.refl (Fin 2))
      warmRobinXorFourSlotContextEquiv)

@[simp] theorem warmRobinXorFourSlotMiddleBitsEquiv_apply
    (bits : PrimitiveBasis 6) :
    warmRobinXorFourSlotMiddleBitsEquiv bits =
      (bits 5,
        (⟨(bits 3).val + 2 * (bits 4).val, by omega⟩,
          (bits 2, ⟨(bits 0).val + 2 * (bits 1).val, by omega⟩))) := by
  rfl

theorem warmRobinXorFourSlotSelectBasisAction_middleIndex
    (bits : PrimitiveBasis 6) :
    warmRobinXorFourSlotMiddleBitsEquiv
        (warmRobinXorFourSlotSelectBasisEquiv bits) =
      ComplexLCU.controlledSystemEquiv warmRobinXorFourSlotSystemEquiv
        (warmRobinXorFourSlotMiddleBitsEquiv bits) := by
  change
    (warmRobinXorFourSlotSelectBasisEquiv bits 5,
      ((⟨(warmRobinXorFourSlotSelectBasisEquiv bits 3).val +
          2 * (warmRobinXorFourSlotSelectBasisEquiv bits 4).val, by omega⟩ : Fin 4),
        (warmRobinXorFourSlotSelectBasisEquiv bits 2,
          ⟨(warmRobinXorFourSlotSelectBasisEquiv bits 0).val +
            2 * (warmRobinXorFourSlotSelectBasisEquiv bits 1).val, by omega⟩))) =
      (bits 5,
        ((⟨(bits 3).val + 2 * (bits 4).val, by omega⟩ : Fin 4),
          warmRobinXorFourSlotSystemPerm
            ⟨(bits 3).val + 2 * (bits 4).val, by omega⟩
            (bits 2, ⟨(bits 0).val + 2 * (bits 1).val, by omega⟩)))
  native_decide +revert

/-- Matrix-level SELECT refinement under the exact middle-register reindex. -/
theorem warmRobinXorFourSlotSelectProgram_eval_reindexed :
    evalPrimitiveCircuit warmRobinXorFourSlotSelectCircuit =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinXorFourSlotMiddleBitsEquiv.symm
        (ComplexLCU.selectLift (coefficient := Fin 2)
          warmRobinXorFourSlotSystemEquiv) := by
  rw [warmRobinXorFourSlotSelectProgram_eval]
  ext row column
  simp only [ComplexLCU.equivPermutationMatrix,
    ComplexLCU.selectLift, _root_.Matrix.reindexAlgEquiv_apply,
    _root_.Matrix.reindex_apply, _root_.Matrix.submatrix_apply,
    Equiv.symm_symm]
  by_cases selected : row = warmRobinXorFourSlotSelectBasisEquiv column
  · rw [if_pos selected]
    rw [if_pos]
    simpa [selected] using
      warmRobinXorFourSlotSelectBasisAction_middleIndex column
  · rw [if_neg selected]
    rw [if_neg]
    intro logicalHit
    apply selected
    apply warmRobinXorFourSlotMiddleBitsEquiv.injective
    rw [warmRobinXorFourSlotSelectBasisAction_middleIndex]
    exact logicalHit

/-- The generic five-control multiplexor is exactly the T2 amplitude lift after
the explicit little-endian product-register reindexing. -/
theorem warmRobinXorFourSlotControlledRy_eq_amplitudeLift :
    controlledRyBlockMatrix warmRobinXorFourSlotControlWires 5
        warmRobinXorFourSlotControlWires_ne_target
        warmRobinXorFourSlotAmplitudeAngle =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinXorFourSlotMiddleBitsEquiv.symm
        (ComplexLCU.amplitudeLift warmRobinXorFourSlotRotation) := by
  ext row column
  simp only [controlledRyBlockMatrix,
    _root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply,
    _root_.Matrix.submatrix_apply, _root_.Matrix.blockDiagonal_apply,
    ComplexLCU.amplitudeLift_apply, Equiv.symm_symm]
  have contextIff :
      (splitPrimitiveWire (5 : Fin 6) row).2 =
          (splitPrimitiveWire (5 : Fin 6) column).2 ↔
        (warmRobinXorFourSlotMiddleBitsEquiv row).2 =
          (warmRobinXorFourSlotMiddleBitsEquiv column).2 := by
    change _ ↔
      warmRobinXorFourSlotContextEquiv
          (splitPrimitiveWire (5 : Fin 6) row).2 =
        warmRobinXorFourSlotContextEquiv
          (splitPrimitiveWire (5 : Fin 6) column).2
    exact warmRobinXorFourSlotContextEquiv.injective.eq_iff.symm
  by_cases contextsEqual :
      (splitPrimitiveWire (5 : Fin 6) row).2 =
        (splitPrimitiveWire (5 : Fin 6) column).2
  · rw [if_pos contextsEqual, if_pos (contextIff.mp contextsEqual)]
    have rotation := warmRobinXorFourSlotAmplitudeRy_eq_rotation
      (primitiveControlAssignment warmRobinXorFourSlotControlWires 5
        warmRobinXorFourSlotControlWires_ne_target
        (splitPrimitiveWire (5 : Fin 6) row).2)
    have rotationEntry := congrFun (congrFun rotation
      (splitPrimitiveWire (5 : Fin 6) row).1)
      (splitPrimitiveWire (5 : Fin 6) column).1
    simpa [warmRobinXorFourSlotMiddleBitsEquiv,
      warmRobinXorFourSlotContextEquiv_apply,
      warmRobinXorFourSlotContextIndex, primitiveControlAssignment,
      warmRobinXorFourSlotControlWires,
      warmRobinXorFourSlotControlSelector,
      warmRobinXorFourSlotControlSector,
      warmRobinXorFourSlotControlPair, splitPrimitiveWire] using rotationEntry
  · rw [if_neg contextsEqual, if_neg (not_congr contextIff |>.mp contextsEqual)]

noncomputable def warmRobinXorFourSlotSelectorLowMatrix :
    _root_.Matrix (Fin 4) (Fin 4) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ warmRobinFourSlotBitsEquiv
    ((1 : _root_.Matrix (Fin 2) (Fin 2) ℂ) ⊗ₖ warmRobinUniformBitPrepare)

noncomputable def warmRobinXorFourSlotSelectorHighMatrix :
    _root_.Matrix (Fin 4) (Fin 4) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ warmRobinFourSlotBitsEquiv
    (warmRobinUniformBitPrepare ⊗ₖ (1 : _root_.Matrix (Fin 2) (Fin 2) ℂ))

theorem warmRobinXorFourSlotSelectorHighLow_eq_prepare :
    warmRobinXorFourSlotSelectorHighMatrix *
        warmRobinXorFourSlotSelectorLowMatrix =
      warmRobinFourSlotSelectorPrepare := by
  unfold warmRobinXorFourSlotSelectorHighMatrix
    warmRobinXorFourSlotSelectorLowMatrix warmRobinFourSlotSelectorPrepare
    warmRobinFourSlotBitsPrepare
  rw [← _root_.Matrix.reindexAlgEquiv_mul]
  congr 1
  rw [← _root_.Matrix.mul_kronecker_mul]
  simp

def warmRobinXorFourSlotSelectorPrepareCircuit : PrimitiveCircuit 6 :=
  [ .ry 3 (.piRational (1 / 2)), .ry 4 (.piRational (1 / 2)) ]

@[simp] theorem warmRobinFourSlotBitsEquiv_symm_pack
    (low high : Fin 2) :
    warmRobinFourSlotBitsEquiv.symm
        ⟨low.val + 2 * high.val, by omega⟩ = (high, low) := by
  native_decide +revert

theorem warmRobinXorFourSlotLowContext_iff
    (row column : PrimitiveBasis 6) :
    (splitPrimitiveWire (3 : Fin 6) row).2 =
        (splitPrimitiveWire (3 : Fin 6) column).2 ↔
      row 5 = column 5 ∧ row 4 = column 4 ∧ row 2 = column 2 ∧
        (⟨(row 0).val + 2 * (row 1).val, by omega⟩ : Fin 4) =
          ⟨(column 0).val + 2 * (column 1).val, by omega⟩ := by
  native_decide +revert

theorem warmRobinXorFourSlotHighContext_iff
    (row column : PrimitiveBasis 6) :
    (splitPrimitiveWire (4 : Fin 6) row).2 =
        (splitPrimitiveWire (4 : Fin 6) column).2 ↔
      row 5 = column 5 ∧ row 3 = column 3 ∧ row 2 = column 2 ∧
        (⟨(row 0).val + 2 * (row 1).val, by omega⟩ : Fin 4) =
          ⟨(column 0).val + 2 * (column 1).val, by omega⟩ := by
  native_decide +revert

theorem warmRobinXorFourSlotSelectorLow_eval :
    evalPrimitiveGate (.ry (3 : Fin 6) (.piRational (1 / 2))) =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinXorFourSlotMiddleBitsEquiv.symm
        (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinSymmetrySystem)
          warmRobinXorFourSlotSelectorLowMatrix) := by
  rw [evalPrimitiveGate]
  have angleEval : (ExactAngle.piRational (1 / 2)).eval = Real.pi / 2 := by
    norm_num [ExactAngle.eval]
    ring
  rw [angleEval]
  rw [standardRyMatrix_pi_div_two_eq_warmRobinUniformBitPrepare]
  ext row column
  simp [warmRobinXorFourSlotSelectorLowMatrix,
    ComplexLCU.selectorLift, warmRobinXorFourSlotMiddleBitsEquiv_apply,
    liftPrimitiveOneQubit_apply]
  by_cases h5 : row 5 = column 5 <;>
    by_cases h4 : row 4 = column 4 <;>
    by_cases h2 : row 2 = column 2 <;>
    by_cases hp :
      (⟨(row 0).val + 2 * (row 1).val, by omega⟩ : Fin 4) =
        ⟨(column 0).val + 2 * (column 1).val, by omega⟩ <;>
    simp_all [warmRobinXorFourSlotLowContext_iff, _root_.Matrix.one_apply]

theorem warmRobinXorFourSlotSelectorHigh_eval :
    evalPrimitiveGate (.ry (4 : Fin 6) (.piRational (1 / 2))) =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinXorFourSlotMiddleBitsEquiv.symm
        (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinSymmetrySystem)
          warmRobinXorFourSlotSelectorHighMatrix) := by
  rw [evalPrimitiveGate]
  have angleEval : (ExactAngle.piRational (1 / 2)).eval = Real.pi / 2 := by
    norm_num [ExactAngle.eval]
    ring
  rw [angleEval]
  rw [standardRyMatrix_pi_div_two_eq_warmRobinUniformBitPrepare]
  ext row column
  simp [warmRobinXorFourSlotSelectorHighMatrix,
    ComplexLCU.selectorLift, warmRobinXorFourSlotMiddleBitsEquiv_apply,
    liftPrimitiveOneQubit_apply]
  by_cases h5 : row 5 = column 5 <;>
    by_cases h3 : row 3 = column 3 <;>
    by_cases h2 : row 2 = column 2 <;>
    by_cases hp :
      (⟨(row 0).val + 2 * (row 1).val, by omega⟩ : Fin 4) =
        ⟨(column 0).val + 2 * (column 1).val, by omega⟩ <;>
    simp_all [warmRobinXorFourSlotHighContext_iff, _root_.Matrix.one_apply]

theorem warmRobinXorFourSlotSelectorPrepareCircuit_eval :
    evalPrimitiveCircuit warmRobinXorFourSlotSelectorPrepareCircuit =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinXorFourSlotMiddleBitsEquiv.symm
        (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinSymmetrySystem)
          warmRobinFourSlotSelectorPrepare) := by
  simp only [warmRobinXorFourSlotSelectorPrepareCircuit,
    evalPrimitiveCircuit, _root_.Matrix.one_mul]
  rw [warmRobinXorFourSlotSelectorLow_eval,
    warmRobinXorFourSlotSelectorHigh_eval,
    ← _root_.Matrix.reindexAlgEquiv_mul]
  congr 1
  unfold ComplexLCU.selectorLift
  rw [← _root_.Matrix.mul_kronecker_mul,
    ← _root_.Matrix.mul_kronecker_mul]
  simp only [_root_.Matrix.one_mul]
  rw [warmRobinXorFourSlotSelectorHighLow_eq_prepare]

def warmRobinXorFourSlotSelectorUnprepareCircuit : PrimitiveCircuit 6 :=
  warmRobinXorFourSlotSelectorPrepareCircuit.reverse.map PrimitiveGate.dagger

theorem warmRobinXorFourSlotSelectorUnprepareCircuit_eval :
    evalPrimitiveCircuit warmRobinXorFourSlotSelectorUnprepareCircuit =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinXorFourSlotMiddleBitsEquiv.symm
        (star (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinSymmetrySystem)
          warmRobinFourSlotSelectorPrepare)) := by
  rw [warmRobinXorFourSlotSelectorUnprepareCircuit,
    evalPrimitiveCircuit_dagger,
    warmRobinXorFourSlotSelectorPrepareCircuit_eval]
  ext row column
  rfl

noncomputable def warmRobinXorFourSlotAmplitudeCircuit : PrimitiveCircuit 6 :=
  compileUniformlyControlledRy 5 warmRobinXorFourSlotControlWires 5
    warmRobinXorFourSlotControlWires_ne_target
    warmRobinXorFourSlotAmplitudeAngle

noncomputable def warmRobinXorFourSlotAmplitudeProgram : PrimitiveProgram 6 where
  circuit := warmRobinXorFourSlotAmplitudeCircuit
  globalPhase := .rational 0

theorem warmRobinXorFourSlotAmplitudeProgram_eval :
    evalPrimitiveProgram warmRobinXorFourSlotAmplitudeProgram =
      controlledRyBlockMatrix warmRobinXorFourSlotControlWires 5
        warmRobinXorFourSlotControlWires_ne_target
        warmRobinXorFourSlotAmplitudeAngle := by
  change evalGlobalPhase (.rational 0) •
      evalPrimitiveCircuit warmRobinXorFourSlotAmplitudeCircuit = _
  have phase : evalGlobalPhase (.rational 0) = 1 := by
    simp [evalGlobalPhase, ExactAngle.eval]
  rw [phase, one_smul]
  unfold warmRobinXorFourSlotAmplitudeCircuit
  exact compileUniformlyControlledRy_eval_controlledRyBlockMatrix _ _ _ _

theorem warmRobinXorFourSlotAmplitudeCircuit_eval_reindexed :
    evalPrimitiveCircuit warmRobinXorFourSlotAmplitudeCircuit =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinXorFourSlotMiddleBitsEquiv.symm
        (ComplexLCU.amplitudeLift warmRobinXorFourSlotRotation) := by
  unfold warmRobinXorFourSlotAmplitudeCircuit
  rw [compileUniformlyControlledRy_eval_controlledRyBlockMatrix,
    warmRobinXorFourSlotControlledRy_eq_amplitudeLift]

noncomputable def warmRobinXorFourSlotPrimitiveMiddleCircuit :
    PrimitiveCircuit 6 :=
  warmRobinXorFourSlotSelectorPrepareCircuit ++
    warmRobinXorFourSlotAmplitudeCircuit ++
    warmRobinXorFourSlotSelectCircuit ++
    warmRobinXorFourSlotSelectorUnprepareCircuit

theorem warmRobinXorFourSlotPrimitiveMiddle_eval :
    evalPrimitiveCircuit warmRobinXorFourSlotPrimitiveMiddleCircuit =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinXorFourSlotMiddleBitsEquiv.symm
        warmRobinXorFourSlotMiddleLogicalUnitary := by
  unfold warmRobinXorFourSlotPrimitiveMiddleCircuit
  rw [evalPrimitiveCircuit_append, evalPrimitiveCircuit_append,
    evalPrimitiveCircuit_append,
    warmRobinXorFourSlotSelectorPrepareCircuit_eval,
    warmRobinXorFourSlotAmplitudeCircuit_eval_reindexed,
    warmRobinXorFourSlotSelectProgram_eval_reindexed,
    warmRobinXorFourSlotSelectorUnprepareCircuit_eval,
    ← _root_.Matrix.reindexAlgEquiv_mul,
    ← _root_.Matrix.reindexAlgEquiv_mul,
    ← _root_.Matrix.reindexAlgEquiv_mul]
  rfl

def warmRobinXorFourSlotPairCoordinateCircuit : PrimitiveCircuit 6 :=
  [ .cx 2 1 (by decide), .cx 2 0 (by decide) ]

def warmRobinXorFourSlotPairCoordinateBasisEquiv :
    PrimitiveBasis 6 ≃ PrimitiveBasis 6 :=
  (cxBasisEquiv (2 : Fin 6) (1 : Fin 6) (by decide)).trans
    (cxBasisEquiv (2 : Fin 6) (0 : Fin 6) (by decide))

theorem warmRobinXorFourSlotPairCoordinateCircuit_eval :
    evalPrimitiveCircuit warmRobinXorFourSlotPairCoordinateCircuit =
      ComplexLCU.equivPermutationMatrix
        warmRobinXorFourSlotPairCoordinateBasisEquiv := by
  simp only [warmRobinXorFourSlotPairCoordinateCircuit,
    evalPrimitiveCircuit, evalPrimitiveGate, _root_.Matrix.one_mul]
  rw [ComplexLCU.equivPermutationMatrix_mul]
  rfl

theorem warmRobinXorFourSlotPairCoordinateBasisEquiv_involutive :
    Function.Involutive warmRobinXorFourSlotPairCoordinateBasisEquiv := by
  intro bits
  funext wire
  native_decide +revert

theorem warmRobinXorFourSlotSymmetryContext_iff
    (row column : PrimitiveBasis 6) :
    (splitPrimitiveWire (2 : Fin 6) row).2 =
        (splitPrimitiveWire (2 : Fin 6) column).2 ↔
      row 5 = column 5 ∧
        (⟨(row 3).val + 2 * (row 4).val, by omega⟩ : Fin 4) =
          ⟨(column 3).val + 2 * (column 4).val, by omega⟩ ∧
        (⟨(row 0).val + 2 * (row 1).val, by omega⟩ : Fin 4) =
          ⟨(column 0).val + 2 * (column 1).val, by omega⟩ := by
  native_decide +revert

def warmRobinXorFourSlotSymmetryPrepareCircuit : PrimitiveCircuit 6 :=
  [ .ry 2 (.piRational (1 / 2)) ]

theorem warmRobinXorFourSlotSymmetryPrepareCircuit_eval :
    evalPrimitiveCircuit warmRobinXorFourSlotSymmetryPrepareCircuit =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinXorFourSlotMiddleBitsEquiv.symm
        (ComplexLCU.systemLift (coefficient := Fin 2) (selector := Fin 4)
          warmRobinSymmetryBasisChange) := by
  simp only [warmRobinXorFourSlotSymmetryPrepareCircuit,
    evalPrimitiveCircuit, _root_.Matrix.one_mul, evalPrimitiveGate]
  have angleEval : (ExactAngle.piRational (1 / 2)).eval = Real.pi / 2 := by
    norm_num [ExactAngle.eval]
    ring
  rw [angleEval, standardRyMatrix_pi_div_two_eq_warmRobinUniformBitPrepare]
  ext row column
  simp [ComplexLCU.systemLift, warmRobinSymmetryBasisChange,
    warmRobinXorFourSlotMiddleBitsEquiv_apply,
    liftPrimitiveOneQubit_apply]
  by_cases h5 : row 5 = column 5 <;>
    by_cases hs :
      (⟨(row 3).val + 2 * (row 4).val, by omega⟩ : Fin 4) =
        ⟨(column 3).val + 2 * (column 4).val, by omega⟩ <;>
    by_cases hp :
      (⟨(row 0).val + 2 * (row 1).val, by omega⟩ : Fin 4) =
        ⟨(column 0).val + 2 * (column 1).val, by omega⟩ <;>
    simp_all [warmRobinXorFourSlotSymmetryContext_iff,
      _root_.Matrix.one_apply]

def warmRobinXorFourSlotSymmetryUnprepareCircuit : PrimitiveCircuit 6 :=
  warmRobinXorFourSlotSymmetryPrepareCircuit.reverse.map PrimitiveGate.dagger

theorem warmRobinXorFourSlotSymmetryUnprepareCircuit_eval :
    evalPrimitiveCircuit warmRobinXorFourSlotSymmetryUnprepareCircuit =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinXorFourSlotMiddleBitsEquiv.symm
        (star (ComplexLCU.systemLift (coefficient := Fin 2) (selector := Fin 4)
          warmRobinSymmetryBasisChange)) := by
  rw [warmRobinXorFourSlotSymmetryUnprepareCircuit,
    evalPrimitiveCircuit_dagger,
    warmRobinXorFourSlotSymmetryPrepareCircuit_eval]
  ext row column
  rfl

/-- The middle logical unitary conjugated back from symmetry-sector to pair
coordinates, still expressed on the six named primitive wires. -/
noncomputable def warmRobinXorFourSlotPrimitivePairCircuit :
    PrimitiveCircuit 6 :=
  warmRobinXorFourSlotSymmetryUnprepareCircuit ++
    warmRobinXorFourSlotPrimitiveMiddleCircuit ++
    warmRobinXorFourSlotSymmetryPrepareCircuit

theorem warmRobinXorFourSlotPrimitivePair_eval :
    evalPrimitiveCircuit warmRobinXorFourSlotPrimitivePairCircuit =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinXorFourSlotMiddleBitsEquiv.symm
        warmRobinXorFourSlotPairLogicalUnitary := by
  unfold warmRobinXorFourSlotPrimitivePairCircuit
  rw [evalPrimitiveCircuit_append, evalPrimitiveCircuit_append,
    warmRobinXorFourSlotSymmetryPrepareCircuit_eval,
    warmRobinXorFourSlotPrimitiveMiddle_eval,
    warmRobinXorFourSlotSymmetryUnprepareCircuit_eval,
    ← _root_.Matrix.reindexAlgEquiv_mul,
    ← _root_.Matrix.reindexAlgEquiv_mul]
  rfl

/-- The basis interpretation after the physical pair-coordinate CX stage. -/
noncomputable def warmRobinXorFourSlotOriginalBitsEquiv :
    PrimitiveBasis 6 ≃
      ComplexLCU.LCUIndex (Fin 2) (Fin 4) WarmRobinSymmetrySystem :=
  warmRobinXorFourSlotPairCoordinateBasisEquiv.trans
    warmRobinXorFourSlotMiddleBitsEquiv

/-- The pair-coordinate circuit, the logical pair circuit, and its inverse in
the chronological physical order required by the six-wire implementation. -/
noncomputable def warmRobinXorFourSlotPrimitiveCircuit : PrimitiveCircuit 6 :=
  warmRobinXorFourSlotPairCoordinateCircuit ++
    warmRobinXorFourSlotPrimitivePairCircuit ++
    warmRobinXorFourSlotPairCoordinateCircuit

theorem warmRobinXorFourSlotPrimitive_eval_reindexedPair :
    evalPrimitiveCircuit warmRobinXorFourSlotPrimitiveCircuit =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinXorFourSlotOriginalBitsEquiv.symm
        warmRobinXorFourSlotPairLogicalUnitary := by
  unfold warmRobinXorFourSlotPrimitiveCircuit
  rw [evalPrimitiveCircuit_append, evalPrimitiveCircuit_append,
    warmRobinXorFourSlotPairCoordinateCircuit_eval,
    warmRobinXorFourSlotPrimitivePair_eval]
  simpa [warmRobinXorFourSlotOriginalBitsEquiv, mul_assoc] using
    (ComplexLCU.equivPermutationMatrix_conjugates_reindex
      warmRobinXorFourSlotPairCoordinateBasisEquiv
      warmRobinXorFourSlotMiddleBitsEquiv
      warmRobinXorFourSlotPairLogicalUnitary
      warmRobinXorFourSlotPairCoordinateBasisEquiv_involutive)

/-- The physical pair-coordinate convention agrees with the original Robin
system order and the repository-wide six-wire little-endian convention. -/
theorem warmRobinXorFourSlotOriginalBitsEquiv_index
    (bits : PrimitiveBasis 6) :
    warmRobinFourSlotIndexEquiv
        (warmRobinXorFourSlotOriginalBitsEquiv bits) =
      primitiveBasisLEEquiv 6 bits := by
  apply Fin.ext
  rw [primitiveBasisLEEquiv_six_value]
  simp only [warmRobinFourSlotIndexEquiv,
    warmRobinFourSlotProductSystemEquiv,
    warmRobinFourSlotOriginalIndexEquiv,
    warmRobinXorFourSlotOriginalBitsEquiv,
    warmRobinXorFourSlotMiddleBitsEquiv_apply,
    warmRobinPairSystemEquiv_apply, Equiv.trans_apply,
    Equiv.prodCongr_apply, Prod.map_def]
  native_decide +revert

/-- Exact T3 refinement root: the primitive `{X, RY, RZ, CX}` circuit denotes
the XOR four-slot T2 unitary after the explicit little-endian reindexing. -/
theorem warmRobinXorFourSlotPrimitive_eval_eq_flatUnitary :
    evalPrimitiveCircuit warmRobinXorFourSlotPrimitiveCircuit =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        (primitiveBasisLEEquiv 6).symm
        warmRobinXorFourSlotFlatUnitary := by
  rw [warmRobinXorFourSlotPrimitive_eval_reindexedPair]
  ext row column
  have rowIndex :
      warmRobinXorFourSlotOriginalBitsEquiv row =
        warmRobinFourSlotIndexEquiv.symm (primitiveBasisLEEquiv 6 row) := by
    apply warmRobinFourSlotIndexEquiv.injective
    simp [warmRobinXorFourSlotOriginalBitsEquiv_index]
  have columnIndex :
      warmRobinXorFourSlotOriginalBitsEquiv column =
        warmRobinFourSlotIndexEquiv.symm (primitiveBasisLEEquiv 6 column) := by
    apply warmRobinFourSlotIndexEquiv.injective
    simp [warmRobinXorFourSlotOriginalBitsEquiv_index]
  simp only [_root_.Matrix.reindexAlgEquiv_apply,
    _root_.Matrix.reindex_apply, _root_.Matrix.submatrix_apply,
    Equiv.symm_symm, warmRobinXorFourSlotFlatUnitary]
  rw [rowIndex, columnIndex]

noncomputable def warmRobinXorFourSlotPrimitiveProgram : PrimitiveProgram 6 where
  circuit := warmRobinXorFourSlotPrimitiveCircuit
  globalPhase := .rational 0

theorem warmRobinXorFourSlotPrimitiveProgram_eval :
    evalPrimitiveProgram warmRobinXorFourSlotPrimitiveProgram =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        (primitiveBasisLEEquiv 6).symm
        warmRobinXorFourSlotFlatUnitary := by
  rw [evalPrimitiveProgram]
  change evalGlobalPhase (.rational 0) •
      evalPrimitiveCircuit warmRobinXorFourSlotPrimitiveCircuit = _
  have phaseZero : evalGlobalPhase (.rational 0) = 1 := by
    norm_num [evalGlobalPhase, ExactAngle.eval]
  rw [phaseZero, one_smul]
  exact warmRobinXorFourSlotPrimitive_eval_eq_flatUnitary

noncomputable def warmRobinXorFourSlotPrimitiveCleanIndex
    (system : Fin 8) : PrimitiveBasis 6 :=
  (primitiveBasisLEEquiv 6).symm (warmRobinFourSlotCleanIndex system)

/-- The executable primitive circuit has the required exact clean block. -/
theorem warmRobinXorFourSlotPrimitive_cleanBlock (row column : Fin 8) :
    evalPrimitiveCircuit warmRobinXorFourSlotPrimitiveCircuit
        (warmRobinXorFourSlotPrimitiveCleanIndex row)
        (warmRobinXorFourSlotPrimitiveCleanIndex column) =
      ((RobinEvolution.warmRobinTarget row column /
        RobinEvolution.warmRobinNormalizer : Rat) : ℂ) := by
  rw [warmRobinXorFourSlotPrimitive_eval_eq_flatUnitary]
  simp only [warmRobinXorFourSlotPrimitiveCleanIndex,
    _root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply,
    _root_.Matrix.submatrix_apply, Equiv.symm_symm,
    Equiv.apply_symm_apply]
  exact warmRobinXorFourSlotFlatUnitary_cleanBlock row column

theorem warmRobinXorFourSlotPrimitive_unitary :
    evalPrimitiveCircuit warmRobinXorFourSlotPrimitiveCircuit ∈
      _root_.Matrix.unitaryGroup (PrimitiveBasis 6) ℂ :=
  evalPrimitiveCircuit_unitary _

theorem warmRobinXorFourSlotPrimitive_noOracleCalls :
    warmRobinXorFourSlotPrimitiveProgram.resource.oracleCalls = 0 :=
  PrimitiveCircuit.resource_oracleCalls_eq_zero _

/-- Presentation-only conversion into the repository's legacy circuit list.
The authoritative T3 semantics and resources remain those of PrimitiveCircuit. -/
noncomputable def warmRobinXorFourSlotPrimitivePresentation : Circuit :=
  warmRobinXorFourSlotPrimitiveCircuit.map fun gate =>
    match gate with
    | .x target => .oneQubit "X" target.val
    | .ry target _ => .rotationY target.val "exact-angle"
    | .rz target _ => .rotationZ target.val "exact-angle"
    | .cx control target _ => .cnot control.val target.val

noncomputable def warmRobinXorFourSlotPrimitiveResource : Resource :=
  warmRobinXorFourSlotPrimitiveProgram.resource

/-- Resource ownership is definitional: no handwritten gate or depth tuple is
used by the promoted candidate. -/
theorem warmRobinXorFourSlotPrimitive_resource_faithful :
    warmRobinXorFourSlotPrimitiveResource =
      warmRobinXorFourSlotPrimitiveCircuit.resource := rfl

def warmRobinXorFourSlotPrimitiveBlockContainsTarget : Prop :=
  ∀ row column : Fin 8,
    warmRobinXorFourSlotFlatUnitary
        (warmRobinFourSlotCleanIndex row)
        (warmRobinFourSlotCleanIndex column) =
      warmRobinQueryTarget.operator row column /
        warmRobinQueryTarget.normalizer

theorem warmRobinXorFourSlotPrimitiveBlockContainsTarget_proof :
    warmRobinXorFourSlotPrimitiveBlockContainsTarget := by
  intro row column
  rw [warmRobinXorFourSlotFlatUnitary_cleanBlock]
  norm_num [warmRobinQueryTarget, warmRobinComplexTarget]

/-- T3 candidate whose resource row is computed from its exact primitive
program.  The refinement theorem above links this circuit to this unitary. -/
noncomputable def warmRobinXorFourSlotPrimitiveOperatorCandidate :
    OperatorBlockEncodingCandidate ℂ 3 where
  auxiliaryQubits := 3
  target := warmRobinQueryTarget
  unitary := warmRobinXorFourSlotFlatUnitary
  layout := {
    systemQubits := 3
    signalQubits := 3
    pureAncillas := 0
  }
  circuit := warmRobinXorFourSlotPrimitivePresentation
  resource := warmRobinXorFourSlotPrimitiveResource
  layoutMatches := by decide
  isUnitary := warmRobinXorFourSlotFlatUnitary ∈
    _root_.Matrix.unitaryGroup (Fin (gridSize 6)) ℂ
  blockContainsTarget := warmRobinXorFourSlotPrimitiveBlockContainsTarget

noncomputable def warmRobinXorFourSlotPrimitiveRefinement :
    PrimitiveRefinement 6 where
  circuit := warmRobinXorFourSlotPrimitiveCircuit
  target := _root_.Matrix.reindexAlgEquiv ℂ ℂ
    (primitiveBasisLEEquiv 6).symm warmRobinXorFourSlotFlatUnitary
  exact := warmRobinXorFourSlotPrimitive_eval_eq_flatUnitary

/-- Exact primitive verified block encoding for the XOR evolved route. -/
noncomputable def warmRobinXorFourSlotPrimitiveVerifiedBlockEncoding :
    VerifiedOperatorBlockEncoding ℂ 3 where
  candidate := warmRobinXorFourSlotPrimitiveOperatorCandidate
  unitaryProof := warmRobinXorFourSlotFlatUnitary_unitary
  blockProof := warmRobinXorFourSlotPrimitiveBlockContainsTarget_proof

/-- Dashboard-compatible names explicitly pointing to the XOR T3 route. -/
noncomputable abbrev warmRobinFourSlotT3FlatUnitary :=
  warmRobinXorFourSlotFlatUnitary

theorem warmRobinFourSlotPrimitive_eval_eq_flatUnitary :
    evalPrimitiveCircuit warmRobinXorFourSlotPrimitiveCircuit =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        (primitiveBasisLEEquiv 6).symm
        warmRobinFourSlotT3FlatUnitary :=
  warmRobinXorFourSlotPrimitive_eval_eq_flatUnitary

noncomputable abbrev warmRobinFourSlotPrimitiveVerifiedBlockEncoding :=
  warmRobinXorFourSlotPrimitiveVerifiedBlockEncoding

theorem warmRobinXorFourSlotAmplitudeCircuit_counts :
    warmRobinXorFourSlotAmplitudeCircuit.ryCount = 32 ∧
      warmRobinXorFourSlotAmplitudeCircuit.cxCount = 62 := by
  exact compileUniformlyControlledRy_five_control_counts _ _ _ _

theorem warmRobinXorFourSlotAmplitudeProgram_noOracleCalls :
    warmRobinXorFourSlotAmplitudeProgram.resource.oracleCalls = 0 :=
  PrimitiveCircuit.resource_oracleCalls_eq_zero _

end QuantumBlockEncoding.Robin
