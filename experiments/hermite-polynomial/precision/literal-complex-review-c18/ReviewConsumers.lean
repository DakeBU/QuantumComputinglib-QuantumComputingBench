import ConsumerChecks

namespace C18IndependentReview
open HermiteLiteralComplexAdapter HermiteSavedStageInterpreter HermiteSavedRounding
open QuantumBlockEncoding QuantumBlockEncoding.Robin.ComplexLCU
open scoped Matrix

-- Explicit result typing fixes typeclass elaboration; no unsafe reducibility option.
noncomputable def flatPrimitive {w : ℕ} (word : List (Instruction w)) :
    Matrix (Basis w) (Basis w) ℂ :=
  Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv w)
    (evalPrimitiveCircuit (compileWord word))

theorem arbitrary_nonidentity_input {w : ℕ} (word : List (Instruction w))
    (m : RealMatrix w) :
    castMatrix (realWord word m) = flatPrimitive word * castMatrix m :=
  realWord_input_eq_primitive word m

noncomputable def nonidentity : RealMatrix 2 := fun i j =>
  (i.val : ℝ) - 3 * (j.val : ℝ) + 2

example : nonidentity (0 : Basis 2) (1 : Basis 2) = -1 := by
  norm_num [nonidentity]

example (word : List (Instruction 2)) :
    castMatrix (realWord word nonidentity) = flatPrimitive word * castMatrix nonidentity :=
  arbitrary_nonidentity_input word nonidentity

theorem all_spectators_low {w : ℕ} (i : Basis w) (q s : Fin w) (h : s ≠ q) :
    (primitiveBasisLEEquiv w).symm (low q i) s =
      (primitiveBasisLEEquiv w).symm i s := by
  rw [decode_low]
  simp [splitPrimitiveWire, h]

theorem all_spectators_high {w : ℕ} (i : Basis w) (q s : Fin w) (h : s ≠ q) :
    (primitiveBasisLEEquiv w).symm (high q i) s =
      (primitiveBasisLEEquiv w).symm i s := by
  rw [decode_high]
  simp [splitPrimitiveWire, h]

theorem cx_inverse_row_direction {w : ℕ} (c t : Fin w) (h : c ≠ t)
    (a : Matrix (PrimitiveBasis w) (PrimitiveBasis w) ℂ)
    (r k : PrimitiveBasis w) :
    (evalPrimitiveGate (.cx c t h) * a) r k =
      a ((cxBasisEquiv c t h).symm r) k := by
  exact equivPermutationMatrix_mul_apply _ a r k

theorem cx_full_input {w : ℕ} (c t : Fin w) (h : c ≠ t) (m : RealMatrix w) :
    castMatrix (realWord [.cx c t h] m) = flatPrimitive [.cx c t h] * castMatrix m :=
  arbitrary_nonidentity_input [.cx c t h] m

theorem signed_negative_rational :
    standardRyMatrix (ExactAngle.eval (.rational (-3/2))) 0 1 =
      (Real.sin (3/4 : ℝ) : ℂ) := by
  norm_num [standardRyMatrix, ExactAngle.eval, realRotation, realOrthogonalRotation,
    Real.sin_neg]

theorem chronological_all_inputs {w : ℕ} (left right : List (Instruction w))
    (m : RealMatrix w) :
    castMatrix (realWord (left ++ right) m) =
      flatPrimitive right * (flatPrimitive left * castMatrix m) := by
  rw [arbitrary_nonidentity_input]
  have h : flatPrimitive (left ++ right) = flatPrimitive right * flatPrimitive left := by
    simp only [flatPrimitive, compileWord, List.map_append, evalPrimitiveCircuit_append, map_mul]
    rfl
  rw [h, mul_assoc]

theorem arbitrary_complex_vector {w : ℕ} (word : List (Instruction w))
    (v : Basis w → ℂ) :
    castMatrix (realWord word realIdentity) *ᵥ v = flatPrimitive word *ᵥ v := by
  exact congrArg (fun a => a *ᵥ v) (realWord_eq_primitive word)

theorem width_zero_arbitrary_input (word : List (Instruction 0)) (m : RealMatrix 0) :
    castMatrix (realWord word m) = castMatrix m := by
  rw [width_zero_word_empty word]
  rfl

#print HermiteLiteralComplexAdapter.realWord_eq_primitive
#print HermiteLiteralComplexAdapter.realWord_input_eq_primitive
#print axioms HermiteLiteralComplexAdapter.realWord_eq_primitive
#print axioms HermiteLiteralComplexAdapter.realWord_input_eq_primitive
#print axioms arbitrary_nonidentity_input
#print axioms all_spectators_low
#print axioms all_spectators_high
#print axioms cx_inverse_row_direction
#print axioms cx_full_input
#print axioms signed_negative_rational
#print axioms chronological_all_inputs
#print axioms arbitrary_complex_vector
#print axioms width_zero_arbitrary_input
end C18IndependentReview
