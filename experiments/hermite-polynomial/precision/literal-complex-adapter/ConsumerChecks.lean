import LiteralComplexAdapter

namespace HermiteLiteralComplexAdapter
open HermiteSavedStageInterpreter HermiteSavedRounding QuantumBlockEncoding
open QuantumBlockEncoding.Robin.ComplexLCU
open scoped Matrix
set_option allowUnsafeReducibility true in
attribute [local reducible] gridSize

theorem primitive_entry_enclosure {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) (i j : Basis width) :
    Mem (intervalWord word degree bits intervalIdentity i j)
      ((Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv width)
        (evalPrimitiveCircuit (compileWord word))) i j).re := by
  rw [← realWord_eq_primitive]
  simpa [castMatrix] using stage_enclosure word degree bits i j

theorem primitive_entry_midpoint_error {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) (i j : Basis width) :
    |((Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv width)
      (evalPrimitiveCircuit (compileWord word))) i j).re -
      (midpoint (intervalWord word degree bits intervalIdentity i j) : ℝ)| ≤
      ((((intervalWord word degree bits intervalIdentity i j).hi -
        (intervalWord word degree bits intervalIdentity i j).lo) / 2 : ℚ) : ℝ) := by
  rw [← realWord_eq_primitive]
  simpa [castMatrix] using stage_midpoint_error word degree bits i j

theorem primitive_has_exact_real_entries {width : ℕ} (word : List (Instruction width))
    (i j : Basis width) :
    ((Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv width)
      (evalPrimitiveCircuit (compileWord word))) i j).im = 0 := by
  rw [← realWord_eq_primitive]
  simp [castMatrix]

theorem chronological_consumer {width : ℕ} (left right : List (Instruction width)) :
    castMatrix (realWord (left ++ right) realIdentity) =
      Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv width)
        (evalPrimitiveCircuit (compileWord right)) *
      Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv width)
        (evalPrimitiveCircuit (compileWord left)) := by
  rw [realWord_eq_primitive]
  simp only [compileWord, List.map_append, evalPrimitiveCircuit_append,
    map_mul]

theorem arbitrary_complex_input_consumer {width : ℕ} (word : List (Instruction width))
    (x : Basis width → ℂ) :
    castMatrix (realWord word realIdentity) *ᵥ x =
      Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv width)
        (evalPrimitiveCircuit (compileWord word)) *ᵥ x := by
  rw [realWord_eq_primitive]

theorem width_zero_word_empty (word : List (Instruction 0)) : word = [] := by
  cases word with
  | nil => rfl
  | cons g rest =>
      cases g with
      | ry theta q => exact Fin.elim0 q
      | cx c t h => exact Fin.elim0 c

example (word : List (Instruction 0)) :
    castMatrix (realWord word realIdentity) = (1 : Matrix (Basis 0) (Basis 0) ℂ) := by
  rw [width_zero_word_empty word, realWord_eq_primitive]
  simp [compileWord, evalPrimitiveCircuit]

example (theta : ℚ) :
    (castMatrix (realWord [.ry theta (0 : Fin 1)] realIdentity)) 0 1 =
      -(Real.sin ((theta : ℝ) / 2) : ℂ) := by
  change ((realStep (.ry theta (0 : Fin 1)) realIdentity) 0 1 : ℂ) = _
  norm_num [realStep, realIdentity,
    low, high, bit, HermiteSavedStageInterpreter.flip, realRyRow]

example (theta : ℚ) :
    (castMatrix (realWord [.ry theta (0 : Fin 1)] realIdentity)) 1 0 =
      (Real.sin ((theta : ℝ) / 2) : ℂ) := by
  change ((realStep (.ry theta (0 : Fin 1)) realIdentity) 1 0 : ℂ) = _
  norm_num [realStep, realIdentity,
    low, high, bit, HermiteSavedStageInterpreter.flip, realRyRow]

#print axioms realWord_eq_primitive
#print axioms primitive_entry_enclosure
#print axioms arbitrary_complex_input_consumer
end HermiteLiteralComplexAdapter
