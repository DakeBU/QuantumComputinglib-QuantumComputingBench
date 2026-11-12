import ChronologicalTransport

namespace Cycle17StageReview
open HermiteSavedStageInterpreter HermiteSavedRounding HermiteNominalStageTransport
open QuantumBlockEncoding.ExperimentalNonunitaryTransport

theorem arbitrary_full_isometry {width : ℕ} (word : List (Instruction width))
    (x : StageSpace width) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (realWord word realIdentity) x‖ = ‖x‖ :=
  nominal_norm_preservation word x
theorem produced_valid_zero (degree bits : ℕ) :
    Valid (actualStages ([[],[],[]] : List (List (Instruction 0))) degree bits) :=
  actual_stages_valid _ degree bits
theorem partition_chronology {width : ℕ} (u v : List (Instruction width)) (degree bits : ℕ) :
    nominalProduct (actualStages [u, [], v] degree bits) =
      Matrix.toEuclideanCLM (𝕜 := ℝ) (realWord (u ++ v) realIdentity) := by
  simpa using nominalProduct_eq_flatten [u, [], v] degree bits
theorem cx_chronology_discriminates :
    cxRow (0 : Fin 3) (1 : Fin 3) (cxRow (1 : Fin 3) (2 : Fin 3) (7 : Basis 3)) = 1 ∧
    cxRow (1 : Fin 3) (2 : Fin 3) (cxRow (0 : Fin 3) (1 : Fin 3) (7 : Basis 3)) = 5 := by decide
theorem spectator_not_discarded :
    cxRow (0 : Fin 4) (2 : Fin 4) (9 : Basis 4) = 13 := by decide
theorem signed_high (theta : ℚ) :
    vectorStep (.ry theta (0 : Fin 1)) (fun j : Basis 1 => if j = 1 then 1 else 0) 0 =
      -Real.sin ((theta : ℝ)/2) := by
  norm_num [vectorStep, low, high, bit, HermiteSavedStageInterpreter.flip, realRyRow]
theorem local_dense_counts : 4^(2+1) = 64 ∧ 4^(12+2) > 4^(2+1) := by norm_num
theorem product_budget_not_sum : (1+(1/3 : ℝ))*(1+1/4)-1 > 1/3+1/4 := by norm_num

#print axioms arbitrary_full_isometry
#print axioms produced_valid_zero
#print axioms partition_chronology
#print axioms cx_chronology_discriminates
#print axioms spectator_not_discarded
#print axioms signed_high
#print axioms local_dense_counts
#print axioms product_budget_not_sum
end Cycle17StageReview
