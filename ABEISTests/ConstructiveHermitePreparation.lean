import QuantumBlockEncoding.ConstructiveHermitePreparation

open QuantumBlockEncoding
open QuantumBlockEncoding.TensorTrainCanonical
open QuantumBlockEncoding.TensorTrainSchedule
open QuantumBlockEncoding.ConstructiveTensorTrainCompiler
open scoped BigOperators

noncomputable section
namespace ConstructiveCompilerChecks

def negativeZero : Chain 1 1 1 :=
  .cons (fun _ out => if out.1 = 0 then -1 else 0) (.nil 1)

theorem negativeZero_normalized : (∑ x : Word 1, (contract negativeZero x 0 0) ^ 2) = 1 := by
  change (∑ x : Fin 2 × Unit, (contract negativeZero x 0 0) ^ 2) = 1
  simp only [Fintype.sum_prod_type]
  norm_num [negativeZero, contract, slice, _root_.Matrix.mul_apply,
    _root_.Matrix.one_apply, Fintype.sum_prod_type, Fin.sum_univ_succ]

def negativeCircuit : PrimitiveCircuit 1 := compile (q := 0) negativeZero
  (by norm_num [negativeZero, maxBond])

example : negativeCircuit.gateCount ≤ 6 ∧ negativeCircuit.resource.depth ≤ 6 := by
  exact ⟨compile_gateCount negativeZero _, compile_depth negativeZero _⟩

example : evalPrimitiveCircuit negativeCircuit (fun _ => 0) (fun _ => 0) = -1 := by
  have h := compile_columns (q := 0) negativeZero (by norm_num [negativeZero, maxBond])
    negativeZero_normalized (fun _ => 0) (fun _ => 0)
  have he : Fin.append (fun _ : Fin 1 => (0 : Fin 2)) (fun _ : Fin 0 => (0 : Fin 2)) =
      (fun _ : Fin 1 => (0 : Fin 2)) := by
    funext i
    fin_cases i
    rfl
  rw [he] at h
  simpa [negativeCircuit, negativeZero, wordOfBasis, contract, slice,
    _root_.Matrix.mul_apply, _root_.Matrix.one_apply] using h

example : RightCanonical (unitBoundary negativeZero) :=
  unitBoundary_canonical negativeZero negativeZero_normalized

/-- Three identical raw rows test deficient local factors before compilation. -/
def repeatedSource : Chain 2 1 1 :=
  .cons (fun _ out => if out.1 = 0 ∧ out.2 = 0 then 1 else 0)
    (.cons (fun _ out => if out.1 = 0 then 3 / 5 else 4 / 5) (.nil 1) : Chain 1 3 1)

theorem repeatedSource_normalized :
    (∑ x : Word 2, (contract repeatedSource x 0 0) ^ 2) = 1 := by
  change (∑ x : Fin 2 × (Fin 2 × Unit), (contract repeatedSource x 0 0) ^ 2) = 1
  simp only [Fintype.sum_prod_type]
  norm_num [repeatedSource, contract, slice, _root_.Matrix.mul_apply,
    _root_.Matrix.one_apply, Fintype.sum_prod_type, Fin.sum_univ_succ]

def repeatedCircuit : PrimitiveCircuit 4 := compile (q := 2) repeatedSource
  (by norm_num [repeatedSource, maxBond])

example : repeatedCircuit.gateCount ≤ 768 ∧ repeatedCircuit.resource.depth ≤ 768 ∧
    repeatedCircuit.resource.oracleCalls = 0 ∧
    evalPrimitiveCircuit repeatedCircuit ∈ _root_.Matrix.unitaryGroup (PrimitiveBasis 4) ℂ ∧
    ∀ (x : PrimitiveBasis 2) (b : PrimitiveBasis 2),
      evalPrimitiveCircuit repeatedCircuit (Fin.append x b) (fun _ => 0) =
        if b = (fun _ => 0) then
          (contract repeatedSource (wordOfBasis (fun i => x i.rev)) 0 0 : ℂ) else 0 := by
  simpa [repeatedCircuit] using compile_spec (q := 2) repeatedSource
    (by norm_num [repeatedSource, maxBond]) repeatedSource_normalized

example : evalPrimitiveCircuit repeatedCircuit
    (Fin.append (fun i => TensorTrainWord.toBasis (n := 2) (0, (1, ())) i.rev)
      (fun _ : Fin 2 => 0))
      (fun _ => 0) = (4 / 5 : ℂ) := by
  have h := compile_word (q := 2) repeatedSource
    (by norm_num [repeatedSource, maxBond]) repeatedSource_normalized (0, (1, ())) (fun _ => 0)
  have ha : contract repeatedSource ((0, (1, ())) : Word 2) 0 0 = 4 / 5 := by
    norm_num [repeatedSource, contract, slice, _root_.Matrix.mul_apply,
      _root_.Matrix.one_apply, Fin.sum_univ_succ]
  rw [if_pos rfl, ha] at h
  simpa only [repeatedCircuit, Complex.ofReal_div, Complex.ofReal_ofNat] using h

example : evalPrimitiveCircuit repeatedCircuit
    (Fin.append (fun _ => 0) (![1, 0] : PrimitiveBasis 2)) (fun _ => 0) = 0 := by
  have h := compile_columns (q := 2) repeatedSource
    (by norm_num [repeatedSource, maxBond]) repeatedSource_normalized (fun _ => 0) ![1, 0]
  have hb : (![1, 0] : PrimitiveBasis 2) ≠ (fun _ => 0) := by decide
  simpa only [repeatedCircuit, if_neg hb] using h

example : (ConstructiveHermitePreparation.prepare 0 0 1).gateCount ≤ 10368 ∧
    (ConstructiveHermitePreparation.prepare 0 0 1).resource.depth ≤ 10368 := by
  exact ⟨ConstructiveHermitePreparation.prepare_gateCount 0 0 1,
    ConstructiveHermitePreparation.prepare_depth 0 0 1⟩

example (x : PrimitiveBasis 3) (b : PrimitiveBasis (HermiteFiniteChain.bondQubits 1)) :
    evalPrimitiveCircuit (ConstructiveHermitePreparation.prepare 1 2 1)
      (Fin.append x b) (fun _ => 0) =
      if b = (fun _ => 0) then
        HermiteStatePreparation.normalizedAmplitude 1 3 1 (primitiveBasisLEEquiv 3 x) else 0 :=
  ConstructiveHermitePreparation.prepare_columns 1 2 1 (by norm_num) x b

#check compile
#check compile_spec
#check compile_word
#check ConstructiveHermitePreparation.prepare
#check ConstructiveHermitePreparation.prepare_spec
#print axioms unitBoundary_canonical
#print axioms stage_columns
#print axioms compile_spec
#print axioms compile_word
#print axioms ConstructiveHermitePreparation.prepare_spec

end ConstructiveCompilerChecks
