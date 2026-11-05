import StoredConsumerChecks

namespace C22IndependentReview
open QuantumBlockEncoding TensorTrainCanonical StoredTensorTrain StoredGivens
open HermitePiecewiseStored HermitePiecewiseAssembly HermitePiecewiseUniform
open HermitePiecewiseSourceBudget HermitePiecewiseKernelProducer
open HermiteFiniteExp HermiteFiniteExpDegree HermiteFiniteMiddleSource

/-- An ordinary external consumer links the exact same returned value and ledger.
The ledger is deliberately not represented as full scalar runtime. -/
theorem same_returned_source_and_partial_cost (k n : Nat) (R delta : Rat)
    (hR : 0 < R) (x : Word (n+1)) :
    let result := produceStored k n R delta
    denoteChain result.value = actualChain k n R delta ∧
    contract (denoteChain result.value) x 0 0 =
      (piecewiseValue k delta (rationalGrid n R (wordIndex n x)) : Real) ∧
    StoredRectangularGivens.total result.cost ≤
      9*passContainers n (assemblySize k delta)+20*(assemblySize k delta)^2+
      30*assemblySize k delta+5*n^2+7*n+31 :=
  ⟨produceStored_refines _ _ _ _, produceStored_source _ _ _ _ hR x,
    produceStored_accounted_traffic_le _ _ _ _⟩

/-- Falsifies interpreting the materialization ledger as scalar-evaluation cost. -/
theorem generation_charges_no_field_work (k n : Nat) (R delta : Rat) :
    (produceQData k n R delta).cost .field = 0 := by
  rw [produceQData_traffic]
  simp [tick]

theorem generation_charges_no_comparisons (k n : Nat) (R delta : Rat) :
    (produceQData k n R delta).cost .compare = 0 := by
  rw [produceQData_traffic]
  simp [tick]

example : tailCutoff (2 : Rat) = 0 := by native_decide
example : tailCutoff (1/2 : Rat) = 1 := by native_decide
example : sourceDegree (2 : Rat) = 1 := by native_decide
example : sourceDegree (1/2 : Rat) = 7 := by native_decide

-- T0: empty active tails do not erase nonzero clipped tails.
example : piecewiseValue 0 2 (-2) = (1/2 : Rat) := by native_decide
example : piecewiseValue 0 2 (-1) = (1/2 : Rat) := by native_decide
example : piecewiseValue 0 2 0 = (1 : Rat) := by native_decide
example : piecewiseValue 0 2 1 = (1/2 : Rat) := by native_decide
-- T1: -1 is still owned by the middle; +1 is a clipped-tail boundary.
example : piecewiseValue 0 (1/2) (-1) = (1/4 : Rat) := by native_decide
example : piecewiseValue 0 (1/2) 0 = (1 : Rat) := by native_decide
example : piecewiseValue 0 (1/2) 1 = (1/4 : Rat) := by native_decide
example : strictCut 2 2 (-1) = 1 := by native_decide
example : inclusiveCut 2 2 (-1) = 2 := by native_decide
example : strictCut 2 2 0 = 2 := by native_decide
example : inclusiveCut 2 2 0 = 3 := by native_decide
-- Clipped endpoint acceptance is independent of the scan state.
example (a : Fin 3) : acceptQ 2 0 a = 0 := by simp [acceptQ]
example (a : Fin 3) : acceptQ 2 4 a = 1 := by simp [acceptQ]
-- q0 is the first, least significant bit, not the MSB.
example : wordValue (n := 2) (1, 0, ()) = 1 := by decide
example : wordValue (n := 2) (0, 1, ()) = 2 := by decide
-- Signed coefficients survive: the rational cast bridge is not an abs/sqrt map.
example : middleCoeffQ 1 (1/2) 2 = (-4 : Rat) := by native_decide

theorem minus_one_owned_by_middle (k : Nat) (delta : Rat) :
    piecewiseValue k delta (-1) = middleValueQ k delta (-1) := by
  simp [piecewiseValue]

theorem zero_owned_by_middle (k : Nat) (delta : Rat) :
    piecewiseValue k delta 0 = middleValueQ k delta 0 := by
  simp [piecewiseValue]

theorem left_cut_owned_by_clipped (k : Nat) (delta p : Rat)
    (ha : p < -1) (hc : p ≤ -(tailCutoff delta : Rat)) :
    piecewiseValue k delta p = clippedValue delta := by
  simp [piecewiseValue, ha, negativeMidpoint_split, hc]

theorem right_cut_owned_by_clipped (k : Nat) (delta p : Rat)
    (hb : 0 < p) (hd : (tailCutoff delta : Rat) ≤ p) :
    piecewiseValue k delta p = clippedValue delta := by
  have ha : ¬ p < -1 := by linarith
  have hc : -p ≤ -(tailCutoff delta : Rat) := by linarith
  simp [piecewiseValue, ha, not_le.mpr hb, negativeMidpoint_split, hc]

#print axioms same_returned_source_and_partial_cost
#print axioms generation_charges_no_field_work
#print axioms generation_charges_no_comparisons
#print axioms minus_one_owned_by_middle
#print axioms zero_owned_by_middle
#print axioms left_cut_owned_by_clipped
#print axioms right_cut_owned_by_clipped
end C22IndependentReview
