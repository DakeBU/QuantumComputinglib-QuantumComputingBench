import QuantumBlockEncoding.StatePreparationBenchmarksCoreFixed
import QuantumBlockEncoding.PrimitiveBasisLE
import QuantumBlockEncoding.UniformlyControlledRy
import Mathlib.Tactic

/-!
# Proof-bearing primitive routes for state preparation

`VerifiedStatePreparation` certifies a target matrix and its first column.  For
resource comparisons we need one stronger layer: the scored circuit itself must
have exact matrix semantics and must prepare that target.  This module therefore
scores typed `PrimitiveCircuit`s only after their evaluated matrix has an exact
state-action proof.
-/

namespace QuantumBlockEncoding.StatePreparationBenchmarks

open ConcreteSemantics
open Robin.ComplexLCU

noncomputable def evalPrimitiveCircuitLE {qubits : Nat}
    (circuit : PrimitiveCircuit qubits) :
    FiniteMatrix (gridSize qubits) (gridSize qubits) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv qubits)
    (evalPrimitiveCircuit circuit)

theorem evalPrimitiveCircuitLE_unitary {qubits : Nat}
    (circuit : PrimitiveCircuit qubits) :
    evalPrimitiveCircuitLE circuit ∈
      _root_.Matrix.unitaryGroup (Fin (gridSize qubits)) ℂ := by
  exact reindex_unitary (primitiveBasisLEEquiv qubits)
    (evalPrimitiveCircuit circuit) (evalPrimitiveCircuit_unitary circuit)

structure ExactPrimitiveStatePreparationRoute (qubits : Nat) where
  target : StatePreparationTarget ℂ qubits
  circuit : PrimitiveCircuit qubits
  normalizationProof : target.normalization
  preparationProof :
    applyVec (evalPrimitiveCircuitLE circuit) (zeroKet qubits) =
      target.amplitudes

namespace ExactPrimitiveStatePreparationRoute

def cost (route : ExactPrimitiveStatePreparationRoute qubits) :
    BlockEncodingCost where
  auxiliaryQubits := 0
  gateCount := route.circuit.resource.gates
  depth := route.circuit.resource.depth
  oracleCalls := route.circuit.resource.oracleCalls

theorem unitary (route : ExactPrimitiveStatePreparationRoute qubits) :
    evalPrimitiveCircuitLE route.circuit ∈
      _root_.Matrix.unitaryGroup (Fin (gridSize qubits)) ℂ :=
  evalPrimitiveCircuitLE_unitary route.circuit

end ExactPrimitiveStatePreparationRoute

/-! ## Exact Pythagorean rotations -/

private theorem amplitudeRotation_eq_pythagorean
    (cosine sine : Real)
    (lower : -1 ≤ cosine) (upper : cosine ≤ 1)
    (sine_nonneg : 0 ≤ sine)
    (normalization : cosine * cosine + sine * sine = 1) :
    amplitudeRotation cosine = realOrthogonalRotation cosine sine := by
  unfold amplitudeRotation realRotation
  have cosine_eval : Real.cos (Real.arccos cosine) = cosine :=
    Real.cos_arccos lower upper
  have sine_nonneg' : 0 ≤ Real.sin (Real.arccos cosine) := by
    exact Real.sin_nonneg_of_nonneg_of_le_pi
      (Real.arccos_nonneg cosine) (Real.arccos_le_pi cosine)
  have circle := Real.sin_sq_add_cos_sq (Real.arccos cosine)
  have sine_eval : Real.sin (Real.arccos cosine) = sine := by
    rw [cosine_eval] at circle
    nlinarith
  rw [cosine_eval, sine_eval]

private def cosine35 : Rat := 3 / 5
private def sine35 : Rat := 4 / 5
private def cosine513 : Rat := 5 / 13
private def sine513 : Rat := 12 / 13

noncomputable def ryAngle35 : ExactAngle :=
  .twiceArccosRational cosine35 (by
    norm_num [cosine35, abs_of_nonneg])

noncomputable def ryAngle513 : ExactAngle :=
  .twiceArccosRational cosine513 (by
    norm_num [cosine513, abs_of_nonneg])

def ryAngleZero : ExactAngle := .rational 0

theorem standardRyMatrix_ryAngle35 :
    standardRyMatrix ryAngle35.eval =
      realOrthogonalRotation (cosine35 : Real) (sine35 : Real) := by
  calc
    standardRyMatrix ryAngle35.eval =
        amplitudeRotation (cosine35 : Real) := by
      simpa [ryAngle35, ExactAngle.eval] using
        standardRyMatrix_two_arccos_eq_amplitudeRotation
          (cosine35 : Real) (by norm_num [cosine35]) (by norm_num [cosine35])
    _ = realOrthogonalRotation (cosine35 : Real) (sine35 : Real) := by
      apply amplitudeRotation_eq_pythagorean
      · norm_num [cosine35]
      · norm_num [cosine35]
      · norm_num [sine35]
      · norm_num [cosine35, sine35]

theorem standardRyMatrix_ryAngle513 :
    standardRyMatrix ryAngle513.eval =
      realOrthogonalRotation (cosine513 : Real) (sine513 : Real) := by
  calc
    standardRyMatrix ryAngle513.eval =
        amplitudeRotation (cosine513 : Real) := by
      simpa [ryAngle513, ExactAngle.eval] using
        standardRyMatrix_two_arccos_eq_amplitudeRotation
          (cosine513 : Real) (by norm_num [cosine513]) (by norm_num [cosine513])
    _ = realOrthogonalRotation (cosine513 : Real) (sine513 : Real) := by
      apply amplitudeRotation_eq_pythagorean
      · norm_num [cosine513]
      · norm_num [cosine513]
      · norm_num [sine513]
      · norm_num [cosine513, sine513]

@[simp] theorem standardRyMatrix_ryAngleZero :
    standardRyMatrix ryAngleZero.eval = 1 := by
  simp [ryAngleZero, ExactAngle.eval]

/-! ## Reusable little-endian circuit semantics -/

def primitiveLEBits (qubits : Nat) (index : Fin (gridSize qubits)) :
    PrimitiveBasis qubits :=
  (primitiveBasisLEEquiv qubits).symm index

theorem evalPrimitiveCircuitLE_append {qubits : Nat}
    (left right : PrimitiveCircuit qubits) :
    evalPrimitiveCircuitLE (left ++ right) =
      evalPrimitiveCircuitLE right * evalPrimitiveCircuitLE left := by
  unfold evalPrimitiveCircuitLE
  rw [evalPrimitiveCircuit_append, _root_.Matrix.reindexAlgEquiv_mul]

@[simp] theorem evalPrimitiveCircuitLE_singleton_ry_apply {qubits : Nat}
    (target : Fin qubits) (angle : ExactAngle)
    (row column : Fin (gridSize qubits)) :
    evalPrimitiveCircuitLE ([PrimitiveGate.ry target angle]) row column =
      if (splitPrimitiveWire target (primitiveLEBits qubits row)).2 =
          (splitPrimitiveWire target (primitiveLEBits qubits column)).2 then
        standardRyMatrix angle.eval
          ((primitiveLEBits qubits row) target)
          ((primitiveLEBits qubits column) target)
      else 0 := by
  simp [evalPrimitiveCircuitLE, primitiveLEBits, evalPrimitiveCircuit,
    evalPrimitiveGate, _root_.Matrix.reindexAlgEquiv_apply,
    _root_.Matrix.reindex_apply, _root_.Matrix.submatrix_apply,
    liftPrimitiveOneQubit_apply] <;> rfl

theorem evalPrimitiveCircuitLE_compileUniformlyControlledRy_apply
    {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle)
    (row column : Fin (gridSize qubits)) :
    evalPrimitiveCircuitLE
        (compileUniformlyControlledRy controls wires target distinct angles)
        row column =
      if (splitPrimitiveWire target (primitiveLEBits qubits row)).2 =
          (splitPrimitiveWire target (primitiveLEBits qubits column)).2 then
        standardRyMatrix
          (angles (primitiveControlAssignment wires target distinct
            (splitPrimitiveWire target (primitiveLEBits qubits row)).2)).eval
          ((primitiveLEBits qubits row) target)
          ((primitiveLEBits qubits column) target)
      else 0 := by
  unfold evalPrimitiveCircuitLE
  rw [compileUniformlyControlledRy_eval_controlledRyBlockMatrix]
  simpa [primitiveLEBits, _root_.Matrix.reindexAlgEquiv_apply,
    _root_.Matrix.reindex_apply, _root_.Matrix.submatrix_apply] using
    controlledRyBlockMatrix_apply wires target distinct angles
      (primitiveLEBits qubits row) (primitiveLEBits qubits column)

/-! ## Grover--Rudolph structured probability benchmark -/

def groverRudolphControlWire : Fin 1 → Fin 2 := fun _ => 1

theorem groverRudolphControlWire_ne_target :
    ∀ control, groverRudolphControlWire control ≠ (0 : Fin 2) := by
  intro control
  fin_cases control
  decide

noncomputable def groverRudolphConstantAngles (_ : PrimitiveBasis 1) : ExactAngle :=
  ryAngle35

/-- Generic binary-tree route: a root split followed by a one-control UCRY. -/
noncomputable def groverRudolphTreeCircuit : PrimitiveCircuit 2 :=
  [PrimitiveGate.ry (1 : Fin 2) ryAngle35] ++
    compileUniformlyControlledRy 1 groverRudolphControlWire (0 : Fin 2)
      groverRudolphControlWire_ne_target groverRudolphConstantAngles

/-- Product-aware route: the two independent rotations can occupy one layer. -/
noncomputable def groverRudolphFactorizedCircuit : PrimitiveCircuit 2 :=
  [PrimitiveGate.ry (1 : Fin 2) ryAngle35] ++
    [PrimitiveGate.ry (0 : Fin 2) ryAngle35]

theorem groverRudolphConstantUcry_eval :
    evalPrimitiveCircuit
        (compileUniformlyControlledRy 1 groverRudolphControlWire (0 : Fin 2)
          groverRudolphControlWire_ne_target groverRudolphConstantAngles) =
      evalPrimitiveGate (PrimitiveGate.ry (0 : Fin 2) ryAngle35) := by
  rw [compileUniformlyControlledRy_eval_controlledRyBlockMatrix]
  ext row column
  simp [controlledRyBlockMatrix_apply, groverRudolphConstantAngles,
    evalPrimitiveGate, liftPrimitiveOneQubit_apply]

theorem groverRudolphTree_eval_eq_factorized :
    evalPrimitiveCircuit groverRudolphTreeCircuit =
      evalPrimitiveCircuit groverRudolphFactorizedCircuit := by
  unfold groverRudolphTreeCircuit groverRudolphFactorizedCircuit
  rw [evalPrimitiveCircuit_append, evalPrimitiveCircuit_append,
    groverRudolphConstantUcry_eval]
  simp [evalPrimitiveCircuit]

theorem groverRudolphTree_evalLE_eq_factorized :
    evalPrimitiveCircuitLE groverRudolphTreeCircuit =
      evalPrimitiveCircuitLE groverRudolphFactorizedCircuit := by
  unfold evalPrimitiveCircuitLE
  rw [groverRudolphTree_eval_eq_factorized]

theorem groverRudolphFactorized_evalLE_eq_matrix :
    evalPrimitiveCircuitLE groverRudolphFactorizedCircuit =
      groverRudolphProductMatrix := by
  unfold groverRudolphFactorizedCircuit
  rw [evalPrimitiveCircuitLE_append]
  let lowMatrix : _root_.Matrix (Fin (gridSize 2)) (Fin (gridSize 2)) ℂ := fun row column =>
    match row.val, column.val with
    | 0, 0 | 2, 2 => (3 : ℂ) / 5
    | 0, 1 | 2, 3 => -(4 : ℂ) / 5
    | 1, 0 | 3, 2 => (4 : ℂ) / 5
    | 1, 1 | 3, 3 => (3 : ℂ) / 5
    | _, _ => 0
  let highMatrix : _root_.Matrix (Fin (gridSize 2)) (Fin (gridSize 2)) ℂ := fun row column =>
    match row.val, column.val with
    | 0, 0 | 1, 1 => (3 : ℂ) / 5
    | 0, 2 | 1, 3 => -(4 : ℂ) / 5
    | 2, 0 | 3, 1 => (4 : ℂ) / 5
    | 2, 2 | 3, 3 => (3 : ℂ) / 5
    | _, _ => 0
  have lowEval :
      evalPrimitiveCircuitLE [PrimitiveGate.ry (0 : Fin 2) ryAngle35] =
        lowMatrix := by
    ext row column
    fin_cases row <;> fin_cases column <;>
      rw [evalPrimitiveCircuitLE_singleton_ry_apply]
    all_goals first | rw [if_pos (by native_decide)] | rw [if_neg (by native_decide)]
    all_goals norm_num [lowMatrix, primitiveLEBits, primitiveBasisLEEquiv_two_symm,
      primitiveBits2LE, primitiveBits2LEWithout,
      standardRyMatrix_ryAngle35, realOrthogonalRotation, cosine35, sine35]
  have highEval :
      evalPrimitiveCircuitLE [PrimitiveGate.ry (1 : Fin 2) ryAngle35] =
        highMatrix := by
    ext row column
    fin_cases row <;> fin_cases column <;>
      rw [evalPrimitiveCircuitLE_singleton_ry_apply]
    all_goals first | rw [if_pos (by native_decide)] | rw [if_neg (by native_decide)]
    all_goals norm_num [highMatrix, primitiveLEBits, primitiveBasisLEEquiv_two_symm,
      primitiveBits2LE, primitiveBits2LEWithout,
      standardRyMatrix_ryAngle35, realOrthogonalRotation, cosine35, sine35]
  rw [lowEval, highEval]
  ext row column
  fin_cases row <;> fin_cases column <;>
    rw [_root_.Matrix.mul_apply, Finset.sum_fin_eq_sum_range] <;>
    norm_num [gridSize, Finset.sum_range_succ, lowMatrix, highMatrix,
      groverRudolphProductMatrix]

theorem groverRudolphFactorized_prepares_target :
    applyVec (evalPrimitiveCircuitLE groverRudolphFactorizedCircuit) (zeroKet 2) =
      groverRudolphProductTarget.amplitudes := by
  rw [groverRudolphFactorized_evalLE_eq_matrix]
  exact groverRudolphProductMatrix_prepares_target

theorem groverRudolphTree_prepares_target :
    applyVec (evalPrimitiveCircuitLE groverRudolphTreeCircuit) (zeroKet 2) =
      groverRudolphProductTarget.amplitudes := by
  rw [groverRudolphTree_evalLE_eq_factorized]
  exact groverRudolphFactorized_prepares_target

noncomputable def groverRudolphFactorizedRoute :
    ExactPrimitiveStatePreparationRoute 2 where
  target := groverRudolphProductTarget
  circuit := groverRudolphFactorizedCircuit
  normalizationProof := groverRudolphProductTarget_normalized
  preparationProof := groverRudolphFactorized_prepares_target

noncomputable def groverRudolphTreeRoute :
    ExactPrimitiveStatePreparationRoute 2 where
  target := groverRudolphProductTarget
  circuit := groverRudolphTreeCircuit
  normalizationProof := groverRudolphProductTarget_normalized
  preparationProof := groverRudolphTree_prepares_target

theorem groverRudolphFactorizedVerified_cost :
    groverRudolphFactorizedRoute.cost =
      { auxiliaryQubits := 0, gateCount := 2, depth := 1, oracleCalls := 0 } := by
  decide

theorem groverRudolphTreeVerified_cost :
    groverRudolphTreeRoute.cost =
      { auxiliaryQubits := 0, gateCount := 5, depth := 4, oracleCalls := 0 } := by
  decide

theorem groverRudolphFactorized_betterThan_tree :
    groverRudolphFactorizedRoute.cost.betterThan groverRudolphTreeRoute.cost := by
  rw [groverRudolphFactorizedVerified_cost, groverRudolphTreeVerified_cost]
  exact Or.inl (by decide)

end QuantumBlockEncoding.StatePreparationBenchmarks
