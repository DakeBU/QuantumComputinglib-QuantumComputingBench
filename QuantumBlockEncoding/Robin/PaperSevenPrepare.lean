import QuantumBlockEncoding.Robin.EvolvedCandidates
import QuantumBlockEncoding.PrimitiveBasisLE
import QuantumBlockEncoding.UniformlyControlledRy
import Mathlib.Tactic

/-!
# Padded physical selector PREPARE for the Robin paper-seven route

The source route uses seven active terms but requires three physical selector
qubits.  Slot seven is therefore present in the Hilbert space and receives
zero clean-column amplitude.  This module closes the exact selector PREPARE
stage; it does not promote the still-open source SELECT/Figure-4 route.
-/

namespace QuantumBlockEncoding.Robin

def warmRobinUniformSevenHighAngle : ExactAngle :=
  .twiceArccosSqrtRational (4 / 7) (by norm_num)

def warmRobinUniformSevenTailAngle : ExactAngle :=
  .twiceArccosSqrtRational (2 / 3) (by norm_num)

def warmRobinUniformSevenMiddleAngles
    (bits : PrimitiveBasis 1) : ExactAngle :=
  if bits 0 = 0 then .piRational (1 / 2)
  else warmRobinUniformSevenTailAngle

def warmRobinUniformSevenLowAngles
    (bits : PrimitiveBasis 2) : ExactAngle :=
  if bits 0 = 1 ∧ bits 1 = 1 then .rational 0
  else .piRational (1 / 2)

def warmRobinUniformSevenMiddleWires : Fin 1 → Fin 3 := fun _ => 2

theorem warmRobinUniformSevenMiddleWires_ne_target
    (wire : Fin 1) : warmRobinUniformSevenMiddleWires wire ≠ (1 : Fin 3) := by
  fin_cases wire
  decide

def warmRobinUniformSevenLowWires : Fin 2 → Fin 3
  | 0 => 1
  | _ => 2

theorem warmRobinUniformSevenLowWires_ne_target
    (wire : Fin 2) : warmRobinUniformSevenLowWires wire ≠ (0 : Fin 3) := by
  fin_cases wire <;> decide

noncomputable def warmRobinUniformSevenPrepareCircuit : PrimitiveCircuit 3 :=
  [.ry 2 warmRobinUniformSevenHighAngle] ++
    compileUniformlyControlledRy 1 warmRobinUniformSevenMiddleWires 1
      warmRobinUniformSevenMiddleWires_ne_target
      warmRobinUniformSevenMiddleAngles ++
    compileUniformlyControlledRy 2 warmRobinUniformSevenLowWires 0
      warmRobinUniformSevenLowWires_ne_target warmRobinUniformSevenLowAngles

noncomputable def warmRobinUniformSevenPrepareProgram : PrimitiveProgram 3 where
  circuit := warmRobinUniformSevenPrepareCircuit
  globalPhase := .rational 0

/-- Independent stagewise matrix specification for the padded selector. -/
noncomputable def warmRobinUniformSevenPrepareMatrix :
    _root_.Matrix (PrimitiveBasis 3) (PrimitiveBasis 3) ℂ :=
  controlledRyBlockMatrix warmRobinUniformSevenLowWires 0
      warmRobinUniformSevenLowWires_ne_target warmRobinUniformSevenLowAngles *
    (controlledRyBlockMatrix warmRobinUniformSevenMiddleWires 1
        warmRobinUniformSevenMiddleWires_ne_target
        warmRobinUniformSevenMiddleAngles *
      evalPrimitiveGate (.ry 2 warmRobinUniformSevenHighAngle))

theorem warmRobinUniformSevenPrepareProgram_eval :
    evalPrimitiveProgram warmRobinUniformSevenPrepareProgram =
      warmRobinUniformSevenPrepareMatrix := by
  change evalGlobalPhase (.rational 0) •
      evalPrimitiveCircuit warmRobinUniformSevenPrepareCircuit = _
  have phaseZero : evalGlobalPhase (.rational 0) = 1 := by
    norm_num [evalGlobalPhase, ExactAngle.eval]
  rw [phaseZero, one_smul]
  unfold warmRobinUniformSevenPrepareCircuit
  rw [evalPrimitiveCircuit_append, evalPrimitiveCircuit_append,
    compileUniformlyControlledRy_eval_controlledRyBlockMatrix,
    compileUniformlyControlledRy_eval_controlledRyBlockMatrix]
  simp [warmRobinUniformSevenPrepareMatrix, evalPrimitiveCircuit]

theorem warmRobinPaperSevenSelectorPrepare_unitary :
    warmRobinUniformSevenPrepareMatrix ∈
      _root_.Matrix.unitaryGroup (PrimitiveBasis 3) ℂ := by
  rw [← warmRobinUniformSevenPrepareProgram_eval]
  exact evalPrimitiveProgram_unitary _

theorem warmRobinUniformSevenPrepare_noOracleCalls :
    warmRobinUniformSevenPrepareProgram.resource.oracleCalls = 0 :=
  PrimitiveCircuit.resource_oracleCalls_eq_zero _

theorem warmRobinUniformSevenPrepare_counts :
    warmRobinUniformSevenPrepareCircuit.ryCount = 7 ∧
      warmRobinUniformSevenPrepareCircuit.cxCount = 8 := by
  constructor
  · simp only [warmRobinUniformSevenPrepareCircuit,
      PrimitiveCircuit.ryCount_append,
      PrimitiveCircuit.ryCount_singleton_ry,
      compileUniformlyControlledRy_ryCount]
    norm_num
  · simp only [warmRobinUniformSevenPrepareCircuit,
      PrimitiveCircuit.cxCount_append,
      PrimitiveCircuit.cxCount_singleton_ry,
      compileUniformlyControlledRy_cxCount]
    norm_num

/-- The source selector has eight physical states even though only seven are
active.  This prevents accidental use of `Fin 7` as a three-qubit register. -/
def warmRobinPaperSevenPaddedSlot (slot : Fin 8) : Option (Fin 7) :=
  if h : slot.val < 7 then some ⟨slot.val, h⟩ else none

theorem warmRobinPaperSevenPaddedSlot_seven :
    warmRobinPaperSevenPaddedSlot 7 = none := by decide

/-- The physical three-qubit PREPARE, flattened with the repository's declared
little-endian convention. -/
noncomputable def warmRobinPaperSevenSelectorPrepare :
    _root_.Matrix (Fin 8) (Fin 8) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv 3)
    warmRobinUniformSevenPrepareMatrix

theorem warmRobinPaperSevenSelectorPrepare_unitary_flat :
    warmRobinPaperSevenSelectorPrepare ∈
      _root_.Matrix.unitaryGroup (Fin 8) ℂ := by
  apply ComplexLCU.reindex_unitary
  exact warmRobinPaperSevenSelectorPrepare_unitary

set_option maxHeartbeats 2000000

/-- The theorem uses probabilities directly, so no arbitrary clean-column
phase convention for `1 / sqrt 7` enters the LCU proof. -/
theorem warmRobinUniformSevenPrepare_probability (slot : Fin 8) :
    star (warmRobinPaperSevenSelectorPrepare slot 0) *
        warmRobinPaperSevenSelectorPrepare slot 0 =
      if slot.val < 7 then (1 / 7 : ℂ) else 0 := by
  have sumLE (f : PrimitiveBasis 3 → ℂ) :
      ∑ bits, f bits =
        ∑ index : Fin 8, f ((primitiveBasisLEEquiv 3).symm index) :=
    Fintype.sum_equiv (primitiveBasisLEEquiv 3) f
      (fun index => f ((primitiveBasisLEEquiv 3).symm index))
      (fun _ => by simp)
  have flattenedEntry (row column : Fin 8) :
      warmRobinPaperSevenSelectorPrepare row column =
        warmRobinUniformSevenPrepareMatrix
          ((primitiveBasisLEEquiv 3).symm row)
          ((primitiveBasisLEEquiv 3).symm column) := by
    rfl
  have piQuarter : Real.pi * (2 : Real)⁻¹ / 2 = Real.pi / 4 := by ring
  have complexPiQuarter :
      (↑Real.pi * (2 : ℂ)⁻¹ / 2) =
        ((Real.pi * (2 : Real)⁻¹ / 2 : Real) : ℂ) := by
    norm_num
  have complexSevenInv :
      (7 : ℂ)⁻¹ = (((7 : Real)⁻¹ : Real) : ℂ) := by
    norm_num
  have sqrtTwoSquare : (Real.sqrt 2) ^ 2 = (2 : Real) :=
    Real.sq_sqrt (by norm_num)
  have quarterCosSquare :
      (Real.cos (Real.pi * (2 : Real)⁻¹ / 2)) ^ 2 = (1 / 2 : Real) := by
    rw [piQuarter, Real.cos_pi_div_four]
    nlinarith
  have quarterSinSquare :
      (Real.sin (Real.pi * (2 : Real)⁻¹ / 2)) ^ 2 = (1 / 2 : Real) := by
    rw [piQuarter, Real.sin_pi_div_four]
    nlinarith
  have highCosSquare :
      (Real.cos (Real.arccos (Real.sqrt 4 / Real.sqrt 7))) ^ 2 =
        (4 / 7 : Real) := by
    have sqrtSevenSquare : (Real.sqrt 7) ^ 2 = (7 : Real) :=
      Real.sq_sqrt (by norm_num)
    have sqrtSevenNonnegative : 0 ≤ Real.sqrt 7 := Real.sqrt_nonneg _
    have sqrtSevenPositive : 0 < Real.sqrt 7 := Real.sqrt_pos.2 (by norm_num)
    have sqrtFour : Real.sqrt 4 = 2 := by norm_num
    have ratioNonnegative : 0 ≤ Real.sqrt 4 / Real.sqrt 7 :=
      div_nonneg (Real.sqrt_nonneg _) sqrtSevenNonnegative
    have ratioUpper : Real.sqrt 4 / Real.sqrt 7 ≤ 1 := by
      rw [sqrtFour]
      apply (div_le_one sqrtSevenPositive).2
      nlinarith
    rw [Real.cos_arccos (by linarith) ratioUpper, sqrtFour]
    field_simp
    nlinarith
  have highSinSquare :
      (Real.sin (Real.arccos (Real.sqrt 4 / Real.sqrt 7))) ^ 2 =
        (3 / 7 : Real) := by
    nlinarith [Real.sin_sq_add_cos_sq
      (Real.arccos (Real.sqrt 4 / Real.sqrt 7))]
  have tailCosSquare :
      (Real.cos (Real.arccos (Real.sqrt 2 / Real.sqrt 3))) ^ 2 =
        (2 / 3 : Real) := by
    have sqrtThreeSquare : (Real.sqrt 3) ^ 2 = (3 : Real) :=
      Real.sq_sqrt (by norm_num)
    have sqrtThreeNonnegative : 0 ≤ Real.sqrt 3 := Real.sqrt_nonneg _
    have sqrtThreePositive : 0 < Real.sqrt 3 := Real.sqrt_pos.2 (by norm_num)
    have ratioNonnegative : 0 ≤ Real.sqrt 2 / Real.sqrt 3 :=
      div_nonneg (Real.sqrt_nonneg _) sqrtThreeNonnegative
    have ratioUpper : Real.sqrt 2 / Real.sqrt 3 ≤ 1 := by
      apply (div_le_one sqrtThreePositive).2
      nlinarith [sqrtTwoSquare]
    rw [Real.cos_arccos (by linarith) ratioUpper]
    field_simp
    nlinarith
  have tailSinSquare :
      (Real.sin (Real.arccos (Real.sqrt 2 / Real.sqrt 3))) ^ 2 =
        (1 / 3 : Real) := by
    nlinarith [Real.sin_sq_add_cos_sq
      (Real.arccos (Real.sqrt 2 / Real.sqrt 3))]
  have headCosProbability :
      (Real.cos (Real.pi * (2 : Real)⁻¹ / 2)) ^ 4 *
          (Real.cos (Real.arccos (Real.sqrt 4 / Real.sqrt 7))) ^ 2 =
        (1 / 7 : Real) := by
    rw [show (Real.cos (Real.pi * (2 : Real)⁻¹ / 2)) ^ 4 =
      ((Real.cos (Real.pi * (2 : Real)⁻¹ / 2)) ^ 2) ^ 2 by ring,
      quarterCosSquare, highCosSquare]
    norm_num
  have headMixedProbability :
      (Real.cos (Real.pi * (2 : Real)⁻¹ / 2)) ^ 2 *
          (Real.sin (Real.pi * (2 : Real)⁻¹ / 2)) ^ 2 *
          (Real.cos (Real.arccos (Real.sqrt 4 / Real.sqrt 7))) ^ 2 =
        (1 / 7 : Real) := by
    rw [quarterCosSquare, quarterSinSquare, highCosSquare]
    norm_num
  have headSinProbability :
      (Real.sin (Real.pi * (2 : Real)⁻¹ / 2)) ^ 4 *
          (Real.cos (Real.arccos (Real.sqrt 4 / Real.sqrt 7))) ^ 2 =
        (1 / 7 : Real) := by
    rw [show (Real.sin (Real.pi * (2 : Real)⁻¹ / 2)) ^ 4 =
      ((Real.sin (Real.pi * (2 : Real)⁻¹ / 2)) ^ 2) ^ 2 by ring,
      quarterSinSquare, highCosSquare]
    norm_num
  have tailCosProbability :
      (Real.cos (Real.pi * (2 : Real)⁻¹ / 2)) ^ 2 *
          (Real.cos (Real.arccos (Real.sqrt 2 / Real.sqrt 3))) ^ 2 *
          (Real.sin (Real.arccos (Real.sqrt 4 / Real.sqrt 7))) ^ 2 =
        (1 / 7 : Real) := by
    rw [quarterCosSquare, tailCosSquare, highSinSquare]
    norm_num
  have tailSinProbability :
      (Real.sin (Real.pi * (2 : Real)⁻¹ / 2)) ^ 2 *
          (Real.cos (Real.arccos (Real.sqrt 2 / Real.sqrt 3))) ^ 2 *
          (Real.sin (Real.arccos (Real.sqrt 4 / Real.sqrt 7))) ^ 2 =
        (1 / 7 : Real) := by
    rw [quarterSinSquare, tailCosSquare, highSinSquare]
    norm_num
  have lastProbability :
      (Real.sin (Real.arccos (Real.sqrt 2 / Real.sqrt 3))) ^ 2 *
          (Real.sin (Real.arccos (Real.sqrt 4 / Real.sqrt 7))) ^ 2 =
        (1 / 7 : Real) := by
    rw [tailSinSquare, highSinSquare]
    norm_num
  rw [flattenedEntry]
  fin_cases slot <;>
    simp [warmRobinPaperSevenSelectorPrepare,
      warmRobinUniformSevenPrepareMatrix,
      warmRobinUniformSevenLowWires, warmRobinUniformSevenMiddleWires,
      warmRobinUniformSevenLowAngles, warmRobinUniformSevenMiddleAngles,
      warmRobinUniformSevenHighAngle, warmRobinUniformSevenTailAngle,
      primitiveControlAssignment, primitiveBits3LE,
      primitiveBits3LEWithout,
      standardRyMatrix, ComplexLCU.realRotation,
      ComplexLCU.realOrthogonalRotation, ExactAngle.eval,
      evalPrimitiveGate, liftPrimitiveOneQubit_apply,
      splitPrimitiveWire_other_apply, _root_.Matrix.mul_apply,
      sumLE, Fin.sum_univ_succ]
  all_goals
    try rw [complexPiQuarter]
    try simp_rw [← Complex.ofReal_cos]
    try simp_rw [← Complex.ofReal_sin]
    try simp only [Complex.conj_ofReal]
    rw [complexSevenInv]
    norm_cast
    ring_nf at quarterCosSquare quarterSinSquare highCosSquare highSinSquare tailCosSquare tailSinSquare headCosProbability headMixedProbability headSinProbability tailCosProbability tailSinProbability lastProbability ⊢
    first
    | exact headCosProbability
    | exact headMixedProbability
    | exact headSinProbability
    | exact tailCosProbability
    | exact tailSinProbability
    | exact lastProbability

set_option maxHeartbeats 200000

end QuantumBlockEncoding.Robin
