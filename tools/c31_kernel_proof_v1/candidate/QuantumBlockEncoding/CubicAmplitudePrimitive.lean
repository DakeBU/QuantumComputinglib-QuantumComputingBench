import QuantumBlockEncoding.CubicStatePreparation
import QuantumBlockEncoding.PrimitiveBasisLE
import QuantumBlockEncoding.UniformlyControlledRy
import Mathlib.Tactic

/-!
# A fully expanded finite cubic amplitude oracle

The scalable cubic arithmetic route intentionally remains a separate research
problem.  This module closes the executable semantic route on the smallest
nontrivial two-qubit grid.  Its emitted circuit uses only the repository's
primitive basis `{X, RY, RZ, CX}` and its clean block is the exact diagonal
operator with entries `(j / 4)^3`.
-/

namespace QuantumBlockEncoding
namespace CubicDiagonalOracle

open Robin.ComplexLCU

/-- The first two wires are system controls and wire two is the clean signal. -/
def cubicN2ControlWires : Fin 2 → Fin 3
  | 0 => 0
  | _ => 1

theorem cubicN2ControlWires_ne_signal (wire : Fin 2) :
    cubicN2ControlWires wire ≠ (2 : Fin 3) := by
  fin_cases wire <;> decide

/-- Decode the two little-endian system controls. -/
def cubicN2ControlIndex (bits : PrimitiveBasis 2) : Fin 4 :=
  ⟨(bits 0).val + 2 * (bits 1).val, by omega⟩

theorem cubicN2Amplitude_abs_le_one (bits : PrimitiveBasis 2) :
    |((CubicStatePreparation.cubicAmplitude 2
      (cubicN2ControlIndex bits) : Rat) : Real)| ≤ 1 := by
  have rationalBound :
      |CubicStatePreparation.cubicAmplitude 2
        (cubicN2ControlIndex bits)| ≤ (1 : Rat) := by
    decide +kernel +revert
  exact_mod_cast rationalBound

/-- Exact standard-RY angle for the selected cubic amplitude. -/
noncomputable def cubicN2Angle (bits : PrimitiveBasis 2) : ExactAngle :=
  .twiceArccosRational
    (CubicStatePreparation.cubicAmplitude 2 (cubicN2ControlIndex bits))
    (cubicN2Amplitude_abs_le_one bits)

/-- Four-way uniformly controlled rotation, compiled to primitive gates. -/
noncomputable def cubicN2PrimitiveCircuit : PrimitiveCircuit 3 :=
  compileUniformlyControlledRy 2 cubicN2ControlWires 2
    cubicN2ControlWires_ne_signal cubicN2Angle

noncomputable def cubicN2PrimitiveProgram : PrimitiveProgram 3 where
  circuit := cubicN2PrimitiveCircuit
  globalPhase := .rational 0

/-- Exact matrix semantics of the emitted gate list. -/
theorem cubicN2PrimitiveCircuit_eval :
    evalPrimitiveCircuit cubicN2PrimitiveCircuit =
      controlledRyBlockMatrix cubicN2ControlWires 2
        cubicN2ControlWires_ne_signal cubicN2Angle := by
  exact compileUniformlyControlledRy_eval_controlledRyBlockMatrix
    cubicN2ControlWires 2 cubicN2ControlWires_ne_signal cubicN2Angle

theorem cubicN2PrimitiveProgram_eval :
    evalPrimitiveProgram cubicN2PrimitiveProgram =
      controlledRyBlockMatrix cubicN2ControlWires 2
        cubicN2ControlWires_ne_signal cubicN2Angle := by
  change evalGlobalPhase (.rational 0) •
      evalPrimitiveCircuit cubicN2PrimitiveCircuit = _
  have phaseZero : evalGlobalPhase (.rational 0) = 1 := by
    simp [evalGlobalPhase, ExactAngle.eval]
  rw [phaseZero, one_smul, cubicN2PrimitiveCircuit_eval]

/-- Encode a signal value and a two-qubit system index into three named wires. -/
def cubicN2EncodeBits (signal : Fin 2) (system : Fin 4) : PrimitiveBasis 3
  | 0 => ⟨system.val % 2, by omega⟩
  | 1 => ⟨(system.val / 2) % 2, by omega⟩
  | _ => signal

@[simp] theorem cubicN2EncodeBits_signal (signal : Fin 2) (system : Fin 4) :
    cubicN2EncodeBits signal system 2 = signal := by
  rfl

@[simp] theorem cubicN2ControlIndex_encode
    (signal : Fin 2) (system : Fin 4) :
    cubicN2ControlIndex
        (primitiveControlAssignment cubicN2ControlWires 2
          cubicN2ControlWires_ne_signal
          (splitPrimitiveWire 2 (cubicN2EncodeBits signal system)).2) =
      system := by
  decide +kernel +revert

@[simp] theorem cubicN2EncodeBits_context_eq_iff
    (leftSignal rightSignal : Fin 2) (left right : Fin 4) :
    (splitPrimitiveWire 2 (cubicN2EncodeBits leftSignal left)).2 =
        (splitPrimitiveWire 2 (cubicN2EncodeBits rightSignal right)).2 ↔
      left = right := by
  decide +kernel +revert

/-- The primitive program's clean signal block is exactly the cubic diagonal. -/
theorem cubicN2PrimitiveProgram_cleanEntry (row column : Fin 4) :
    evalPrimitiveProgram cubicN2PrimitiveProgram
        (cubicN2EncodeBits 0 row) (cubicN2EncodeBits 0 column) =
      ((cubicDiagonalOperator 2 row column : Rat) : ℂ) := by
  rw [cubicN2PrimitiveProgram_eval, controlledRyBlockMatrix_apply]
  by_cases equal : row = column
  · subst column
    rw [if_pos rfl]
    simp only [cubicN2EncodeBits_signal]
    let bits : PrimitiveBasis 2 :=
      primitiveControlAssignment cubicN2ControlWires 2
        cubicN2ControlWires_ne_signal
        (splitPrimitiveWire 2 (cubicN2EncodeBits 0 row)).2
    have indexEq : cubicN2ControlIndex bits = row := by
      simpa [bits] using cubicN2ControlIndex_encode (0 : Fin 2) row
    have amplitudeBound :
        |((CubicStatePreparation.cubicAmplitude 2 row : Rat) : Real)| ≤ 1 := by
      rw [← indexEq]
      exact cubicN2Amplitude_abs_le_one bits
    have bounded := abs_le.mp amplitudeBound
    change standardRyMatrix (cubicN2Angle bits).eval 0 0 =
      ((cubicDiagonalOperator 2 row row : Rat) : ℂ)
    simp only [cubicN2Angle, ExactAngle.eval]
    rw [indexEq]
    rw [standardRyMatrix_two_arccos_eq_amplitudeRotation _
      bounded.1 bounded.2]
    rw [amplitudeRotation_cleanEntry _ bounded.1 bounded.2]
    change ((CubicStatePreparation.cubicAmplitude 2 row : Rat) : ℂ) =
      (((if row = row then CubicStatePreparation.cubicAmplitude 2 row else 0) : Rat) : ℂ)
    rw [if_pos rfl]
  · have contextsDifferent :
        (splitPrimitiveWire 2 (cubicN2EncodeBits 0 row)).2 ≠
          (splitPrimitiveWire 2 (cubicN2EncodeBits 0 column)).2 := by
      simpa [cubicN2EncodeBits_context_eq_iff] using equal
    rw [if_neg contextsDifferent]
    change (0 : ℂ) =
      (((if row = column then
        CubicStatePreparation.cubicAmplitude 2 row else 0) : Rat) : ℂ)
    rw [if_neg equal]
    norm_num

/-- Flat little-endian unitary used by the operator-certificate interface. -/
noncomputable def cubicN2PrimitiveFlatUnitary :
    _root_.Matrix (Fin (gridSize 3)) (Fin (gridSize 3)) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv 3)
    (evalPrimitiveProgram cubicN2PrimitiveProgram)

theorem cubicN2PrimitiveFlatUnitary_unitary :
    cubicN2PrimitiveFlatUnitary ∈
      _root_.Matrix.unitaryGroup (Fin (gridSize 3)) ℂ := by
  apply Robin.ComplexLCU.reindex_unitary
  exact evalPrimitiveProgram_unitary _

noncomputable def cubicN2PrimitiveCleanIndex (system : Fin 4) : Fin (gridSize 3) :=
  primitiveBasisLEEquiv 3 (cubicN2EncodeBits 0 system)

theorem cubicN2PrimitiveFlatUnitary_cleanBlock (row column : Fin 4) :
    cubicN2PrimitiveFlatUnitary
        (cubicN2PrimitiveCleanIndex row)
        (cubicN2PrimitiveCleanIndex column) =
      ((cubicDiagonalOperator 2 row column : Rat) : ℂ) := by
  unfold cubicN2PrimitiveFlatUnitary cubicN2PrimitiveCleanIndex
  simp only [_root_.Matrix.reindexAlgEquiv_apply,
    _root_.Matrix.reindex_apply, _root_.Matrix.submatrix_apply,
    Equiv.symm_symm, Equiv.symm_apply_apply]
  exact cubicN2PrimitiveProgram_cleanEntry row column

noncomputable def cubicN2ComplexTarget :
    QueryOperatorTarget ℂ (gridSize 2) (gridSize 2) where
  operator := fun row column => ((cubicDiagonalOperator 2 row column : Rat) : ℂ)
  normalizer := 1
  source := "finite two-qubit exact cubic amplitude oracle"
  semanticContract := "clean signal block equals diag((j/4)^3)"

noncomputable def cubicN2PrimitivePresentation : Circuit :=
  cubicN2PrimitiveCircuit.map fun gate =>
    match gate with
    | .x target => .oneQubit "X" target.val
    | .ry target _ => .rotationY target.val "exact-angle"
    | .rz target _ => .rotationZ target.val "exact-angle"
    | .cx control target _ => .cnot control.val target.val

noncomputable def cubicN2PrimitiveResource : Resource :=
  cubicN2PrimitiveProgram.resource

noncomputable def cubicN2PrimitiveOperatorCandidate :
    OperatorBlockEncodingCandidate ℂ 2 where
  auxiliaryQubits := 1
  target := cubicN2ComplexTarget
  unitary := cubicN2PrimitiveFlatUnitary
  layout := {
    systemQubits := 2
    signalQubits := 1
    pureAncillas := 0
  }
  circuit := cubicN2PrimitivePresentation
  resource := cubicN2PrimitiveResource
  layoutMatches := by decide
  isUnitary := cubicN2PrimitiveFlatUnitary ∈
    _root_.Matrix.unitaryGroup (Fin (gridSize 3)) ℂ
  blockContainsTarget := ∀ row column : Fin 4,
    cubicN2PrimitiveFlatUnitary
        (cubicN2PrimitiveCleanIndex row)
        (cubicN2PrimitiveCleanIndex column) =
      cubicN2ComplexTarget.operator row column /
        cubicN2ComplexTarget.normalizer

/-- Exact unitarity and clean-block promotion for the finite cubic route. -/
noncomputable def cubicN2PrimitiveVerifiedBlockEncoding :
    VerifiedOperatorBlockEncoding ℂ 2 where
  candidate := cubicN2PrimitiveOperatorCandidate
  unitaryProof := cubicN2PrimitiveFlatUnitary_unitary
  blockProof := by
    intro row column
    rw [cubicN2PrimitiveFlatUnitary_cleanBlock]
    simp [cubicN2ComplexTarget]

/-- No opaque oracle survives in the accepted primitive resource row. -/
theorem cubicN2Primitive_oracleCalls_eq_zero :
    cubicN2PrimitiveResource.oracleCalls = 0 :=
  PrimitiveCircuit.resource_oracleCalls_eq_zero _

/-- Resource ownership is definitional rather than a handwritten tuple. -/
theorem cubicN2Primitive_resource_faithful :
    cubicN2PrimitiveResource = cubicN2PrimitiveCircuit.resource := rfl

end CubicDiagonalOracle
end QuantumBlockEncoding
