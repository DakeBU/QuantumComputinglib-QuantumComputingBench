import QuantumBlockEncoding.TensorTrainLocalCompiler

namespace QuantumBlockEncoding.TensorTrainLocalCompilerChecks

open scoped BigOperators
open TensorTrainCanonical TensorTrainSchedule TensorTrainLocalCompiler

example (q : ℕ) (bond : PrimitiveBasis q) (bit : Fin 2) :
    localIndex q (Fin.snoc bond bit) = (bit, primitiveBasisLEEquiv q bond) :=
  localIndex_snoc q bond bit

/-- A signed one-qubit source, including its exact negative amplitude. -/
def negativeOne : Chain 1 1 1 :=
  .cons (fun _ out => if out.1 = 1 then -1 else 0) (.nil 1)

theorem negativeOne_canonical : RightCanonical negativeOne := by
  constructor
  · ext a b
    fin_cases a
    fin_cases b
    change (∑ out : Fin 2 × Fin 1, (if out.1 = 1 then (-1 : ℝ) else 0) *
      (if out.1 = 1 then (-1 : ℝ) else 0)) = 1
    norm_num [Fintype.sum_prod_type, Fin.sum_univ_two]
  · trivial

theorem negativeOne_actual :
    ∃ c : PrimitiveCircuit 1, c.gateCount ≤ 6 ∧ c.resource.oracleCalls = 0 ∧
      ∀ bit : Fin 2,
        evalPrimitiveCircuit c (Fin.snoc (fun _ : Fin 0 => 0) bit) (fun _ => 0) =
          if bit = 1 then -1 else 0 := by
  have hB : maxBond negativeOne ≤ 2 ^ 0 := by norm_num [negativeOne, maxBond]
  obtain ⟨c, hc, ho, columns⟩ := exists_local_circuit_with_resources
    negativeOne negativeOne_canonical hB 0 (by omega)
  refine ⟨c, by simpa using hc, ho, ?_⟩
  intro bit
  have h := columns bit (fun _ => 0) (fun _ => 0) (by decide)
  by_cases hb : bit = 1 <;>
    simpa [hb, Fin.snoc_zero, negativeOne, paddedAt, paddedCore] using h

/-- Empty active space is still valid: orientation correction uses unused
physical columns, and no active-column witness is fabricated. -/
def emptyInput : Chain 1 0 1 := .cons (fun a => Fin.elim0 a) (.nil 1)

example : ∃ c : PrimitiveCircuit 1, c.gateCount ≤ 6 ∧ c.resource.oracleCalls = 0 := by
  have hC : RightCanonical emptyInput := by
    constructor
    · ext a
      exact Fin.elim0 a
    · trivial
  have hB : maxBond emptyInput ≤ 2 ^ 0 := by norm_num [emptyInput, maxBond]
  obtain ⟨c, hc, ho, _⟩ := exists_local_circuit_with_resources emptyInput hC hB 0 (by omega)
  exact ⟨c, by simpa using hc, ho⟩

#print axioms TensorTrainLocalCompiler.exists_SO_named
#print axioms TensorTrainLocalCompiler.activeColumns_isometry
#print axioms TensorTrainLocalCompiler.exists_local_circuit_with_resources
#print axioms TensorTrainLocalCompiler.exists_local_circuit
#print axioms negativeOne_actual

end QuantumBlockEncoding.TensorTrainLocalCompilerChecks
