import ComplexStageTransport

namespace HermiteComplexStageReviewC21
open HermiteComplexStageTransport HermiteLiteralComplexAdapter
open HermiteSavedStageInterpreter QuantumBlockEncoding
open QuantumBlockEncoding.ExperimentalNonunitaryTransport
open scoped Matrix

theorem full_complex_signature {w : ℕ} (words : List (List (Instruction w)))
    (d b : ℕ) (x : EuclideanSpace ℂ (PrimitiveBasis w)) :
    ‖surrogateProduct (actualStages words d b) x -
      Matrix.toEuclideanCLM (𝕜 := ℂ)
        (evalPrimitiveCircuit (compileWord words.flatten)) x‖ ≤
      (growth (actualStages words d b) - 1) * ‖x‖ :=
  actual_flatten_apply_error words d b x

theorem error_imaginary_part_zero {w : ℕ} (word : List (Instruction w))
    (d b : ℕ) (i j : PrimitiveBasis w) :
    ((namedCast (stageCenter word d b) -
      evalPrimitiveCircuit (compileWord word)) i j).im = 0 := by
  rw [← namedCast_nominal]
  change (((stageCenter word d b (primitiveBasisLEEquiv w i)
    (primitiveBasisLEEquiv w j) : ℝ) : ℂ) -
    ((realWord word realIdentity (primitiveBasisLEEquiv w i)
    (primitiveBasisLEEquiv w j) : ℝ) : ℂ)).im = 0
  simp

#check @stage_operator_error
#check @nominal_contraction
#check @actual_stage_valid
#check @actual_stages_valid
#check @nominalProduct_eq_flatten
#check @actual_flatten_product_error
#check @actual_flatten_apply_error
#print axioms full_complex_signature
#print axioms error_imaginary_part_zero
end HermiteComplexStageReviewC21
