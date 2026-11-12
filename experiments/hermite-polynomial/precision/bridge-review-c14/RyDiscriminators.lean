import SavedRyInterval

namespace IndependentBridgeReviewC14
open QuantumBlockEncoding HermiteFiniteTrig HermiteSavedRyInterval
open scoped Matrix.Norms.L2Operator

theorem literal_signed_rotation :
    HermiteSavedRyInterval.midpoint 2 1 = !![(1 : ℚ), -1; 1, 1] ∧
    HermiteSavedRyInterval.midpoint (-2) 1 = !![(1 : ℚ), 1; -1, 1] := by
  constructor <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [HermiteSavedRyInterval.midpoint, rationalRotation, cosPoly, sinPoly, cosCoeff,
      sinCoeff, Finset.sum_range_succ]

theorem surrogate_first_column_not_unit_norm :
    Complex.normSq (finiteRy 2 1 0 0) + Complex.normSq (finiteRy 2 1 1 0) = 2 := by
  norm_num [finiteRy, HermiteSavedRyInterval.midpoint, rationalRotation, cosPoly, sinPoly, cosCoeff,
    sinCoeff, Finset.sum_range_succ, Complex.normSq]

private theorem context_q1 :
    (splitPrimitiveWire (1 : Fin 3) (primitiveBits3LE 0)).2 =
      (splitPrimitiveWire (1 : Fin 3) (primitiveBits3LE 2)).2 := by
  funext wire
  rcases wire with ⟨wire, h⟩
  fin_cases wire <;> norm_num [splitPrimitiveWire, primitiveBits3LE] at *
  exact (h rfl).elim

theorem named_wire_upper_sign :
    liftPrimitiveOneQubit (1 : Fin 3) (finiteRy 2 1)
      (primitiveBits3LE 0) (primitiveBits3LE 2) = -1 := by
  rw [liftPrimitiveOneQubit_apply, if_pos context_q1]
  change finiteRy 2 1 0 1 = -1
  norm_num [finiteRy, HermiteSavedRyInterval.midpoint, rationalRotation, cosPoly, sinPoly, cosCoeff,
    sinCoeff, Finset.sum_range_succ]

theorem named_wire_spectator_refusal :
    liftPrimitiveOneQubit (1 : Fin 3) (finiteRy 2 1)
      (primitiveBits3LE 0) (primitiveBits3LE 6) = 0 := by
  have h : (splitPrimitiveWire (1 : Fin 3) (primitiveBits3LE 0)).2 ≠
      (splitPrimitiveWire (1 : Fin 3) (primitiveBits3LE 6)).2 := by
    intro he
    have hc := congrFun he (⟨2, by decide⟩ : OtherPrimitiveWires (1 : Fin 3))
    change (0 : Fin 2) = 1 at hc
    norm_num at hc
  rw [liftPrimitiveOneQubit_apply, if_neg h]

theorem actual_full_euclidean_operator_supplier {qubits : ℕ} (target : Fin qubits)
    (theta : ℚ) (n : ℕ) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℂ)
      (liftPrimitiveOneQubit target (finiteRy theta n) -
        evalPrimitiveGate (.ry target (.rational theta)))‖ ≤
      2 * (radius (theta / 2) n : ℝ) := lifted_clm_error target theta n

#print axioms literal_signed_rotation
#print axioms surrogate_first_column_not_unit_norm
#print axioms named_wire_upper_sign
#print axioms named_wire_spectator_refusal
#print axioms actual_full_euclidean_operator_supplier

end IndependentBridgeReviewC14
