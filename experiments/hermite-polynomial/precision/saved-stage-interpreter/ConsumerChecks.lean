import StageOperatorBound

namespace HermiteSavedStageInterpreter
open HermiteSavedRounding

example : (flip (0 : Fin 2) (0 : Basis 2)).val = 1 := by decide
example : (flip (1 : Fin 2) (0 : Basis 2)).val = 2 := by decide
example : (cxRow (0 : Fin 2) (1 : Fin 2) (1 : Basis 2)).val = 3 := by decide
example : (cxRow (1 : Fin 2) (0 : Fin 2) (1 : Basis 2)).val = 1 := by decide

def changingWord : List (Instruction 2) :=
  [.ry (-9/7) 0, .cx 0 1 (by decide), .ry (5/3) 1,
   .cx 1 0 (by decide), .ry (-1/2) 0]

theorem changing_target_CX_full_matrix (degree bits : ℕ) (i j : Basis 2) :
    Mem (intervalWord changingWord degree bits intervalIdentity i j)
      (realWord changingWord realIdentity i j) :=
  stage_enclosure changingWord degree bits i j

theorem changing_target_CX_end_error (degree bits : ℕ) (i j : Basis 2) :
    |realWord changingWord realIdentity i j -
      (midpoint (intervalWord changingWord degree bits intervalIdentity i j) : ℝ)| ≤
    ((((intervalWord changingWord degree bits intervalIdentity i j).hi -
      (intervalWord changingWord degree bits intervalIdentity i j).lo) / 2 : ℚ) : ℝ) :=
  stage_midpoint_error changingWord degree bits i j

theorem actual_first_saved_angle_full_matrix {width : ℕ} (q : Fin width)
    (i j : Basis width) :
    Mem (intervalWord [.ry (-86958955523179937 / 100000000000000000) q]
      96 80 intervalIdentity i j)
      (realWord [.ry (-86958955523179937 / 100000000000000000) q] realIdentity i j) :=
  stage_enclosure _ _ _ i j

#print axioms flip_flip
#print axioms bit_flip
#print axioms bit_flip_other
#print axioms cxRow_involutive
#print axioms identity_encloses
#print axioms step_encloses
#print axioms word_encloses
#print axioms stage_enclosure
#print axioms stage_midpoint_error
#print axioms changing_target_CX_full_matrix
#print axioms changing_target_CX_end_error
#print axioms actual_first_saved_angle_full_matrix
#check stage_enclosure
#check stage_midpoint_error

theorem changing_target_CX_eta (degree bits : ℕ) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ)
      (stageCenter changingWord degree bits - realWord changingWord realIdentity)‖ ≤
    (stageEta changingWord degree bits : ℝ) :=
  stage_euclidean_operator_error changingWord degree bits

#print axioms stage_maxRadius_nonneg
#print axioms stage_max_entry_error
#print axioms real_entry_bound_euclidean_opnorm
#print axioms stage_euclidean_operator_error
#print axioms changing_target_CX_eta
#check stage_euclidean_operator_error
end HermiteSavedStageInterpreter
