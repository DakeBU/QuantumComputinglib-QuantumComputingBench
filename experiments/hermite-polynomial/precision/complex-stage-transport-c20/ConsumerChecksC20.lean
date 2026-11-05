import ComplexStageTransport

namespace HermiteComplexStageTransport.ConsumerChecksC20
open HermiteComplexStageTransport HermiteLiteralComplexAdapter
open HermiteSavedStageInterpreter QuantumBlockEncoding
open QuantumBlockEncoding.ExperimentalNonunitaryTransport
open scoped Matrix

theorem arbitrary_complex_input_bound {width : ℕ}
    (words : List (List (Instruction width))) (degree bits : ℕ)
    (x : EuclideanSpace ℂ (PrimitiveBasis width)) :
    ‖surrogateProduct (actualStages words degree bits) x -
      Matrix.toEuclideanCLM (𝕜 := ℂ)
        (evalPrimitiveCircuit (compileWord words.flatten)) x‖ ≤
      (growth (actualStages words degree bits) - 1) * ‖x‖ :=
  actual_flatten_apply_error words degree bits x

theorem arbitrary_complex_nominal_contraction {width : ℕ}
    (word : List (Instruction width)) (x : EuclideanSpace ℂ (PrimitiveBasis width)) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℂ)
      (evalPrimitiveCircuit (compileWord word)) x‖ ≤ ‖x‖ := by
  calc
    _ ≤ ‖Matrix.toEuclideanCLM (𝕜 := ℂ)
      (evalPrimitiveCircuit (compileWord word))‖ * ‖x‖ := ContinuousLinearMap.le_opNorm _ _
    _ ≤ 1 * ‖x‖ := mul_le_mul_of_nonneg_right (nominal_contraction word) (norm_nonneg x)
    _ = _ := one_mul _

theorem exact_saved_surrogate {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) :
    (actualStage word degree bits).surrogate =
      Matrix.toEuclideanCLM (𝕜 := ℂ) (namedCast (stageCenter word degree bits)) := rfl

theorem exact_saved_error {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) : (actualStage word degree bits).error =
      (stageEta word degree bits : ℝ) := rfl

theorem chronological_two_stages {width : ℕ} (left right : List (Instruction width))
    (degree bits : ℕ) :
    nominalProduct (actualStages [left,right] degree bits) =
      Matrix.toEuclideanCLM (𝕜 := ℂ) (evalPrimitiveCircuit (compileWord right)) *
      Matrix.toEuclideanCLM (𝕜 := ℂ) (evalPrimitiveCircuit (compileWord left)) := by
  simp [actualStages, nominalProduct, actualStage]

theorem spectator_bits_retained {width : ℕ} (i : Basis width) (q s : Fin width)
    (h : s ≠ q) :
    (primitiveBasisLEEquiv width).symm (low q i) s =
      (primitiveBasisLEEquiv width).symm i s ∧
    (primitiveBasisLEEquiv width).symm (high q i) s =
      (primitiveBasisLEEquiv width).symm i s := by
  constructor
  · rw [decode_low]; simp [splitPrimitiveWire, h]
  · rw [decode_high]; simp [splitPrimitiveWire, h]

theorem negative_rational_signed_halfangle :
    standardRyMatrix (ExactAngle.eval (.rational (-3/2))) 0 1 =
      (Real.sin (3/4 : ℝ) : ℂ) := by
  norm_num [standardRyMatrix, ExactAngle.eval, Robin.ComplexLCU.realRotation,
    Robin.ComplexLCU.realOrthogonalRotation, Real.sin_neg]

theorem cx_control_target_direction {width : ℕ} (i : Basis width) (c t : Fin width) :
    (primitiveBasisLEEquiv width).symm (cxRow c t i) =
      cxBasisAction c t ((primitiveBasisLEEquiv width).symm i) ∧
    (primitiveBasisLEEquiv width).symm (cxRow t c i) =
      cxBasisAction t c ((primitiveBasisLEEquiv width).symm i) :=
  ⟨decode_cxRow i c t, decode_cxRow i t c⟩

theorem width_zero_instructions_empty (word : List (Instruction 0)) : word = [] := by
  cases word with
  | nil => rfl
  | cons g rest =>
      cases g with
      | ry theta q => exact Fin.elim0 q
      | cx c t h => exact Fin.elim0 c

theorem width_zero_nominal (words : List (List (Instruction 0))) (degree bits : ℕ) :
    nominalProduct (actualStages words degree bits) = 1 := by
  rw [nominalProduct_eq_flatten]
  have h : words.flatten = [] := width_zero_instructions_empty _
  simp [h, compileWord, evalPrimitiveCircuit]

theorem width_zero_arbitrary_complex_input (words : List (List (Instruction 0)))
    (degree bits : ℕ)
    (x : EuclideanSpace ℂ (PrimitiveBasis 0)) :
    ‖surrogateProduct (actualStages words degree bits) x - x‖ ≤
      (growth (actualStages words degree bits) - 1) * ‖x‖ := by
  have h : words.flatten = [] := width_zero_instructions_empty _
  simpa [h, compileWord, evalPrimitiveCircuit] using actual_flatten_apply_error words degree bits x

#print axioms arbitrary_complex_input_bound
#print axioms arbitrary_complex_nominal_contraction
#print axioms exact_saved_surrogate
#print axioms exact_saved_error
#print axioms chronological_two_stages
#print axioms spectator_bits_retained
#print axioms negative_rational_signed_halfangle
#print axioms cx_control_target_direction
#print axioms width_zero_nominal
#print axioms width_zero_arbitrary_complex_input
end HermiteComplexStageTransport.ConsumerChecksC20
