import ChronologicalTransport

namespace HermiteNominalStageTransport
open HermiteSavedStageInterpreter HermiteSavedRounding
open QuantumBlockEncoding.ExperimentalNonunitaryTransport

def changingWord : List (Instruction 3) :=
  [.ry (-9/7) 0, .cx 0 2 (by decide), .ry (5/3) 2,
   .cx 2 1 (by decide), .ry (-1/2) 1]

theorem changing_full_norm (x : StageSpace 3) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (realWord changingWord realIdentity) x‖ = ‖x‖ :=
  nominal_norm_preservation changingWord x

theorem changing_full_valid (degree bits : ℕ) :
    Valid (actualStages [changingWord, [.ry (2 : ℚ) 1], []] degree bits) :=
  actual_stages_valid _ degree bits

theorem changing_full_apply (degree bits : ℕ) (x : StageSpace 3) :
    ‖surrogateProduct (actualStages [changingWord, [.ry (2 : ℚ) 1], []] degree bits) x -
      nominalProduct (actualStages [changingWord, [.ry (2 : ℚ) 1], []] degree bits) x‖ ≤
    (growth (actualStages [changingWord, [.ry (2 : ℚ) 1], []] degree bits) - 1) * ‖x‖ :=
  actual_apply_error _ degree bits x

theorem empty_width_valid (degree bits : ℕ) :
    Valid (actualStages ([[], []] : List (List (Instruction 0))) degree bits) :=
  actual_stages_valid _ degree bits

theorem literal_signed_high_column (theta : ℚ) :
    vectorStep (.ry theta (0 : Fin 1))
      (fun j : Basis 1 => if j = 1 then 1 else 0) 0 =
      -Real.sin ((theta : ℝ) / 2) := by
  norm_num [vectorStep, low, high, bit, HermiteSavedStageInterpreter.flip, realRyRow]

theorem literal_signed_low_column (theta : ℚ) :
    vectorStep (.ry theta (0 : Fin 1))
      (fun j : Basis 1 => if j = 0 then 1 else 0) 1 =
      Real.sin ((theta : ℝ) / 2) := by
  norm_num [vectorStep, low, high, bit, HermiteSavedStageInterpreter.flip, realRyRow]

example : (cxRow (0 : Fin 3) (2 : Fin 3) (1 : Basis 3)).val = 5 := by decide
example : (cxRow (2 : Fin 3) (0 : Fin 3) (1 : Basis 3)).val = 1 := by decide
example : (flip (0 : Fin 3) (4 : Basis 3)).val = 5 := by decide

#check nominal_norm_preservation
#check nominal_contraction
#check actual_stages_valid
#check actual_product_error
#check actual_apply_error
#print axioms sum_involution
#print axioms ry_pair_square
#print axioms vectorStep_ry_pair
#print axioms vectorStep_sum_square
#print axioms realStep_mulVec
#print axioms realStep_norm_preservation
#print axioms realWord_norm_preservation
#print axioms nominal_norm_preservation
#print axioms nominal_contraction
#print axioms stageEta_nonneg
#print axioms actual_stage_valid
#print axioms actual_stages_valid
#print axioms actual_product_error
#print axioms actual_apply_error
#print axioms changing_full_norm
#print axioms changing_full_valid
#print axioms changing_full_apply
#print axioms empty_width_valid
#print axioms literal_signed_high_column
#print axioms literal_signed_low_column
#check nominalProduct_eq_flatten
#check actual_flatten_product_error
#check actual_flatten_apply_error
#print axioms realIdentity_eq_one
#print axioms realStep_right_mul
#print axioms realWord_right_mul
#print axioms realWord_append_composition
#print axioms nominalProduct_eq_flatten
#print axioms actual_flatten_product_error
#print axioms actual_flatten_apply_error
end HermiteNominalStageTransport
