import StageOperatorBound

namespace StageReviewC16V2
open HermiteSavedStageInterpreter HermiteSavedRounding

theorem q0_is_lsb : (flip (0 : Fin 3) (3 : Basis 3)).val = 2 := by decide
theorem cx_direction_first : (cxRow (0 : Fin 3) (2 : Fin 3) (1 : Basis 3)).val = 5 := by decide
theorem cx_direction_reverse : (cxRow (2 : Fin 3) (0 : Fin 3) (1 : Basis 3)).val = 1 := by decide

theorem zero_width_empty_identity :
    intervalWord ([] : List (Instruction 0)) 0 0 intervalIdentity
      (0 : Basis 0) (0 : Basis 0) = ⟨1,1⟩ := by rfl

def asymmetricWord : List (Instruction 3) :=
  [.ry (-4/5) 2, .cx 2 0 (by decide), .ry (2/7) 0,
   .cx 0 1 (by decide), .ry (-3/2) 1]

theorem all_entries_produced (degree bits : ℕ) (i j : Basis 3) :
    Mem (intervalWord asymmetricWord degree bits intervalIdentity i j)
      (realWord asymmetricWord realIdentity i j) := stage_enclosure _ _ _ i j

theorem eta_without_Valid (degree bits : ℕ) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ)
      (stageCenter asymmetricWord degree bits - realWord asymmetricWord realIdentity)‖ ≤
      (stageEta asymmetricWord degree bits : ℝ) :=
  stage_euclidean_operator_error _ _ _

theorem constant_entry_bound_has_dimension_factor :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ)
      ((fun _ _ => (1/10 : ℝ)) : RealMatrix 2)‖ ≤ 4/10 := by
  have h := real_entry_bound_euclidean_opnorm
    ((fun _ _ => (1/10 : ℝ)) : RealMatrix 2) (1/10) (by norm_num)
    (by intro i j; norm_num)
  convert h using 1 <;> norm_num

theorem exact_squared_vector_rejects_entry_norm :
    (1/10:ℚ)^2*4 < 4*((4:ℚ)/10)^2 := by norm_num

theorem dense_carrier_count (width : ℕ) :
    Fintype.card (Basis width × Basis width) = (2^width)^2 := by simp [Basis, pow_two]

#print axioms q0_is_lsb
#print axioms cx_direction_first
#print axioms cx_direction_reverse
#print axioms zero_width_empty_identity
#print axioms all_entries_produced
#print axioms eta_without_Valid
#print axioms constant_entry_bound_has_dimension_factor
#print axioms exact_squared_vector_rejects_entry_norm
#print axioms dense_carrier_count
end StageReviewC16V2
