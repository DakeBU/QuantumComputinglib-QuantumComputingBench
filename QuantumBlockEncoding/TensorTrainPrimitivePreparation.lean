import QuantumBlockEncoding.TensorTrainSchedule
import QuantumBlockEncoding.RealIsometryCompletion
import QuantumBlockEncoding.GrayGivensCompiler
import QuantumBlockEncoding.SequentialPrimitiveAssembly
import QuantumBlockEncoding.TensorTrainLocalCompiler

/-!
# Primitive preparation from bounded normalized real tensor trains

The signed residual boundary is absorbed into the first canonical core, so
initialization is the genuine empty circuit on a computational-zero bond.
Local matrices are completed on their occupied columns and compiled through
the checked special-orthogonal Gray/Givens backend. Classical existence is
kept separate from arithmetic preprocessing complexity.
-/

namespace QuantumBlockEncoding.TensorTrainPrimitivePreparation

open scoped BigOperators
open TensorTrainCanonical TensorTrainSchedule SequentialBondPreparation

def boundaryRow {l : ℕ} (u : Fin l → ℝ) : _root_.Matrix (Fin 1) (Fin l) ℝ := fun _ a => u a

theorem boundaryRow_isometry {l : ℕ} (u : Fin l → ℝ) (hu : mass u = 1) :
    boundaryRow u * (boundaryRow u).transpose = 1 := by
  ext a b
  fin_cases a
  fin_cases b
  simpa [boundaryRow, mass, pow_two, _root_.Matrix.mul_apply,
    _root_.Matrix.transpose_apply, _root_.Matrix.one_apply] using hu

theorem boundaryCore_isometry {l r : ℕ} (u : Fin l → ℝ) (hu : mass u = 1)
    (A : TensorTrainCanonical.Core l r) (hA : A * A.transpose = 1) :
    (boundaryRow u * A) * (boundaryRow u * A).transpose = 1 := by
  rw [_root_.Matrix.transpose_mul]
  calc
    _ = boundaryRow u * (A * A.transpose) * (boundaryRow u).transpose := by
      simp only [_root_.Matrix.mul_assoc]
    _ = 1 := by rw [hA, _root_.Matrix.mul_one, boundaryRow_isometry u hu]

theorem boundaryCore_contract {n l m r : ℕ} (u : Fin l → ℝ)
    (A : TensorTrainCanonical.Core l m) (C : Chain n m r) (x : Word (n + 1)) :
    contract (.cons (boundaryRow u * A) C) x = boundaryRow u * contract (.cons A C) x := by
  have hs : slice (boundaryRow u * A) x.1 = boundaryRow u * slice A x.1 := by
    ext a b
    rfl
  simp only [contract, hs, _root_.Matrix.mul_assoc]

/-- Eliminate the signed initial residual by absorbing it into the first
row-isometric core. This is not a free state-initialization assumption. -/
theorem exists_unitBoundary_canonical {n B : ℕ} (C : Chain (n + 1) 1 1)
    (hB : maxBond C ≤ B)
    (hNorm : (∑ x : Word (n + 1), (contract C x 0 0) ^ 2) = 1) :
    ∃ D : Chain (n + 1) 1 1, RightCanonical D ∧ maxBond D ≤ B ∧
      ∀ x, contract D x 0 0 = contract C x 0 0 := by
  obtain ⟨l', u, D, hD, hRanks, hu, hAmp⟩ := exists_normalized_state C hNorm
  have hDB : maxBond D ≤ B := hRanks.maxBond_le.trans hB
  have hOne : 1 ≤ B := by
    have h := (rankAt_le_maxBond C 0).trans hB
    simpa only [rankAt_zero] using h
  cases D with
  | @cons _ _ m _ A tail =>
    refine ⟨.cons (boundaryRow u * A) tail, ⟨boundaryCore_isometry u hu A hD.1, hD.2⟩,
      max_le hOne ((le_max_right _ _).trans hDB), ?_⟩
    intro x
    rw [boundaryCore_contract]
    simpa [boundaryRow, _root_.Matrix.mul_apply] using (hAmp x).symm

/-- Reindex only the finite bond labels of a local stage. -/
def transportStage {B C : Type*} (e : B ≃ C) (U : Stage C) : Stage B :=
  fun row col => U (row.1, e row.2) (col.1, e col.2)

theorem run_transport {B C : Type*} [Fintype B] [Fintype C] [DecidableEq B] [DecidableEq C]
    (e : B ≃ C) (U : ℕ → Stage C) (boundary : B → ℂ)
    (n : ℕ) (x : PrimitiveBasis n) (b : C) :
    run U (fun c => boundary (e.symm c)) n (x, b) =
      run (fun t => transportStage e (U t)) boundary n (x, e.symm b) := by
  induction n generalizing b with
  | zero => rfl
  | succ n ih =>
    rw [run, step_apply, run, step_apply]
    simp_rw [ih]
    have he := e.symm.sum_comp (fun a : B => U n (x (Fin.last n), b) (0, e a) *
      run (fun t => transportStage e (U t)) boundary n (Fin.init x, a))
    simpa only [transportStage, Equiv.apply_symm_apply] using he

theorem bondIndex_zero (q : ℕ) : (primitiveBasisLEEquiv q (fun _ => 0)).val = 0 := by
  induction q with
  | zero => rfl
  | succ q ih =>
    rw [primitiveBasisLEEquiv_succ_value]
    simpa only [Fin.val_zero, Nat.zero_add, Nat.mul_zero] using congrArg (2 * ·) ih

theorem bondIndex_zero_iff {q : ℕ} (b : PrimitiveBasis q) :
    (primitiveBasisLEEquiv q b).val = 0 ↔ b = (fun _ => 0) := by
  constructor
  · intro hb
    apply (primitiveBasisLEEquiv q).injective
    apply Fin.ext
    rw [hb, bondIndex_zero]
  · rintro rfl
    exact bondIndex_zero q

theorem initial_padding {q : ℕ} (b : PrimitiveBasis q) :
    padVector (fun _ : Fin 1 => (1 : ℂ)) (primitiveBasisLEEquiv q b) =
      evalPrimitiveCircuit ([] : PrimitiveCircuit q) b (fun _ => 0) := by
  by_cases hb : b = (fun _ => 0)
  · subst b
    simp [padVector, zeroBasisIndex, evalPrimitiveCircuit]
  · have hz : ¬ (primitiveBasisLEEquiv q b).val < 1 := by
      have h := (bondIndex_zero_iff b).not.mpr hb
      omega
    simp [padVector, hz, evalPrimitiveCircuit, hb]

-- Lean 4.33 requires explicit permission to unfold the definitionally equal
-- grid-size aliases when matching named-basis and finite-index columns.
set_option backward.isDefEq.respectTransparency false in
/-- Actual local circuit columns imply the complete sequential source state
from an empty initial circuit, including terminal cleanup. -/
theorem run_circuits_clean {n q : ℕ} (D : Chain n 1 1) (hB : maxBond D ≤ 2 ^ q)
    (stages : ℕ → PrimitiveCircuit (q + 1))
    (columns : ∀ t, t < n → ∀ bit (b a : PrimitiveBasis q),
      (primitiveBasisLEEquiv q a).val < rankAt D t →
      evalPrimitiveCircuit (stages t) (Fin.snoc b bit) (Fin.snoc a 0) =
        paddedAt D t (bit, primitiveBasisLEEquiv q b) (primitiveBasisLEEquiv q a))
    (x : PrimitiveBasis n) (b : PrimitiveBasis q) :
    run (fun t => circuitStage (stages t))
      (fun c => evalPrimitiveCircuit ([] : PrimitiveCircuit q) c (fun _ => 0)) n (x, b) =
      if b = (fun _ => 0) then (contract D (wordOfBasis x) 0 0 : ℂ) else 0 := by
  let e : Fin (2 ^ q) ≃ PrimitiveBasis q := (primitiveBasisLEEquiv q).symm
  let U := fun t => transportStage e (circuitStage (stages t))
  have hc : ∀ t, t < n → ∀ bit (b a : Fin (2 ^ q)), a.val < rankAt D t →
      U t (bit, b) (0, a) = paddedAt D t (bit, b) a := by
    intro t ht bit b a ha
    have he (a : Fin (2 ^ q)) : primitiveBasisLEEquiv q (e a) = a :=
      (primitiveBasisLEEquiv q).apply_symm_apply a
    change evalPrimitiveCircuit (stages t) (Fin.snoc (e b) bit) (Fin.snoc (e a) 0) = _
    simpa only [he] using columns t ht bit (e b) (e a) (by rw [he]; exact ha)
  have hrun := TensorTrainSchedule.run_terminal_clean D hB U hc (fun _ => 1)
    x (primitiveBasisLEEquiv q b)
  have htransport := run_transport e (fun t => circuitStage (stages t))
    (padVector (fun _ : Fin 1 => (1 : ℂ))) n x b
  change run (fun t => circuitStage (stages t))
    (fun c => padVector (fun _ : Fin 1 => (1 : ℂ)) (primitiveBasisLEEquiv q c)) n (x, b) =
      run U (padVector (fun _ : Fin 1 => (1 : ℂ))) n (x, primitiveBasisLEEquiv q b) at htransport
  simp_rw [initial_padding] at htransport
  rw [htransport]
  simp only [bondIndex_zero_iff] at hrun
  simpa [U, _root_.Matrix.vecMul, dotProduct] using hrun

/-- The published data-low/bond-high circuit realizes the chain in the
corresponding most-significant-bit-first word order. -/
theorem publicCircuit_clean {n q : ℕ} (D : Chain n 1 1) (hB : maxBond D ≤ 2 ^ q)
    (stages : ℕ → PrimitiveCircuit (q + 1))
    (columns : ∀ t, t < n → ∀ bit (b a : PrimitiveBasis q),
      (primitiveBasisLEEquiv q a).val < rankAt D t →
      evalPrimitiveCircuit (stages t) (Fin.snoc b bit) (Fin.snoc a 0) =
        paddedAt D t (bit, primitiveBasisLEEquiv q b) (primitiveBasisLEEquiv q a))
    (x : PrimitiveBasis n) (b : PrimitiveBasis q) :
    evalPrimitiveCircuit (SequentialPrimitiveAssembly.publicCircuit [] stages n)
      (Fin.append x b) (fun _ => 0) = if b = (fun _ => 0) then
        (contract D (wordOfBasis (fun i => x i.rev)) 0 0 : ℂ) else 0 := by
  have hzero : (fun _ : Fin (n + q) => (0 : Fin 2)) = Fin.append (fun _ => 0) (fun _ => 0) := by
    funext i
    refine Fin.addCases (fun i => ?_) (fun i => ?_) i <;> simp
  rw [hzero, SequentialPrimitiveAssembly.publicCircuit_column]
  exact run_circuits_clean D hB stages columns _ b

theorem assemble_gateCount (q : ℕ) (stages : ℕ → PrimitiveCircuit (q + 1)) (n : ℕ) :
    (SequentialPrimitiveAssembly.assemble q stages n).gateCount =
      ∑ t ∈ Finset.range n, (stages t).gateCount := by
  induction n with
  | zero => simp [SequentialPrimitiveAssembly.assemble, PrimitiveCircuit.gateCount]
  | succ n ih =>
    simp only [SequentialPrimitiveAssembly.assemble, PrimitiveCircuit.gateCount,
      List.length_append, List.length_map, Finset.sum_range_succ]
    have hp : (SequentialPrimitiveAssembly.placeStage n (stages n)).length = (stages n).length :=
      SequentialPrimitiveAssembly.placeStage_gateCount n (stages n)
    rw [hp]
    exact congrArg (fun k => k + (stages n).length) ih

/-- Gate-list length, not only an arithmetic count proxy, is bounded. -/
theorem publicCircuit_gateCount_bound {q : ℕ} (stages : ℕ → PrimitiveCircuit (q + 1))
    (n bound : ℕ) (h : ∀ t, t < n → (stages t).gateCount ≤ bound) :
    (SequentialPrimitiveAssembly.publicCircuit [] stages n).gateCount ≤ n * bound := by
  have he : (SequentialPrimitiveAssembly.publicCircuit [] stages n).gateCount =
      ∑ t ∈ Finset.range n, (stages t).gateCount := by
    simp only [SequentialPrimitiveAssembly.publicCircuit, PrimitiveWireRename.circuit,
      SequentialPrimitiveAssembly.withInitial, PrimitiveCircuit.gateCount, List.length_map,
      List.length_append]
    change (SequentialPrimitiveAssembly.pad ([] : PrimitiveCircuit q) n).gateCount +
      (SequentialPrimitiveAssembly.assemble q stages n).gateCount = _
    rw [SequentialPrimitiveAssembly.pad_gateCount, assemble_gateCount]
    simp [PrimitiveCircuit.gateCount]
  rw [he]
  calc
    _ ≤ ∑ _t ∈ Finset.range n, bound :=
      Finset.sum_le_sum (fun t ht => h t (Finset.mem_range.mp ht))
    _ = _ := by simp

/-- Any bounded normalized nonempty real scalar-boundary tensor train has
an actual clean primitive preparation. The bound counts every instruction in
the circuit list; initialization uses zero gates after exact boundary absorption.
This theorem makes no claim about classical computation of its exact angles. -/
theorem exists_primitive_preparation {n q : ℕ} (C : Chain (n + 1) 1 1)
    (hB : maxBond C ≤ 2 ^ q)
    (hNorm : (∑ x : Word (n + 1), (contract C x 0 0) ^ 2) = 1) :
    ∃ circuit : PrimitiveCircuit ((n + 1) + q),
      circuit.gateCount ≤ (n + 1) * (6 * (2 ^ q) ^ 3) ∧ circuit.resource.oracleCalls = 0 ∧
      evalPrimitiveCircuit circuit ∈ _root_.Matrix.unitaryGroup (PrimitiveBasis ((n + 1) + q)) ℂ ∧
      ∀ (x : PrimitiveBasis (n + 1)) (b : PrimitiveBasis q),
        evalPrimitiveCircuit circuit (Fin.append x b) (fun _ => 0) =
          if b = (fun _ => 0) then
            (contract C (wordOfBasis (fun i => x i.rev)) 0 0 : ℂ) else 0 := by
  classical
  obtain ⟨D, hD, hDB, hAmp⟩ := exists_unitBoundary_canonical C hB hNorm
  have hex : ∀ t : ℕ, ∃ stage : PrimitiveCircuit (q + 1),
      stage.gateCount ≤ 6 * (2 ^ q) ^ 3 ∧
      (t < n + 1 → ∀ bit (b a : PrimitiveBasis q),
        (primitiveBasisLEEquiv q a).val < rankAt D t →
        evalPrimitiveCircuit stage (Fin.snoc b bit) (Fin.snoc a 0) =
          paddedAt D t (bit, primitiveBasisLEEquiv q b) (primitiveBasisLEEquiv q a)) := by
    intro t
    by_cases ht : t < n + 1
    · obtain ⟨stage, hgate, hcol⟩ := TensorTrainLocalCompiler.exists_local_circuit D hD hDB t ht
      exact ⟨stage, hgate, fun _ => hcol⟩
    · exact ⟨[], by simp [PrimitiveCircuit.gateCount], fun h => False.elim (ht h)⟩
  choose stages hgate hcols using hex
  let circuit := SequentialPrimitiveAssembly.publicCircuit [] stages (n + 1)
  refine ⟨circuit, publicCircuit_gateCount_bound stages (n + 1) _ (fun t _ => hgate t),
    rfl, evalPrimitiveCircuit_unitary circuit, ?_⟩
  intro x b
  rw [show circuit = SequentialPrimitiveAssembly.publicCircuit [] stages (n + 1) from rfl,
    publicCircuit_clean D hDB stages hcols x b, hAmp]

end QuantumBlockEncoding.TensorTrainPrimitivePreparation
