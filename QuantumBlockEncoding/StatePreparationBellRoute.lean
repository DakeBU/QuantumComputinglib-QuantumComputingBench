import QuantumBlockEncoding.StatePreparationPrimitiveRoutes
import Mathlib.Tactic

/-!
# Proof-bearing Bell state-preparation route

The public Bell benchmark uses the same primitive semantics as the paper-derived
state-preparation routes.  A standard `RY(pi/2)` creates the equal positive
superposition on the little-endian q0 wire; `CX(q0,q1)` moves the `|01>` branch
to `|11>`.  The resource tuple is computed from this exact typed circuit.
-/

namespace QuantumBlockEncoding.StatePreparationBenchmarks

open ConcreteSemantics
open Robin.ComplexLCU

noncomputable def bellRyAngle : ExactAngle :=
  .piRational (1 / 2)

theorem bellRyAngle_eval : bellRyAngle.eval = Real.pi / 2 := by
  change Real.pi * (((1 / 2 : Rat) : Real)) = Real.pi / 2
  norm_num
  ring

theorem standardRyMatrix_bellRyAngle :
    standardRyMatrix bellRyAngle.eval = Robin.warmRobinUniformBitPrepare := by
  rw [bellRyAngle_eval]
  exact standardRyMatrix_pi_div_two_eq_warmRobinUniformBitPrepare

def bellControl : Fin 2 := 0

def bellTargetWire : Fin 2 := 1

theorem bellControl_ne_target : bellControl ≠ bellTargetWire := by
  decide

noncomputable def bellRyCircuit : PrimitiveCircuit 2 :=
  [PrimitiveGate.ry (0 : Fin 2) bellRyAngle]

noncomputable def bellCxCircuit : PrimitiveCircuit 2 :=
  [PrimitiveGate.cx bellControl bellTargetWire bellControl_ne_target]

noncomputable def bellPrimitiveCircuit : PrimitiveCircuit 2 :=
  bellRyCircuit ++ bellCxCircuit

noncomputable def bellAfterRy : StateVector 4 ℂ :=
  bellAmplitude • basisKet 4 (0 : Fin 4) +
    bellAmplitude • basisKet 4 (1 : Fin 4)

@[simp] theorem evalPrimitiveCircuitLE_singleton_cx_apply
    {qubits : Nat} (control target : Fin qubits) (distinct : control ≠ target)
    (row column : Fin (gridSize qubits)) :
    evalPrimitiveCircuitLE ([PrimitiveGate.cx control target distinct]) row column =
      if primitiveLEBits qubits row =
          cxBasisEquiv control target distinct (primitiveLEBits qubits column)
      then 1 else 0 := by
  simp [evalPrimitiveCircuitLE, evalPrimitiveCircuit, evalPrimitiveGate,
    _root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply,
    _root_.Matrix.submatrix_apply, equivPermutationMatrix, primitiveLEBits] <;> rfl

private theorem bellAfterRy_0 :
    bellAfterRy (0 : Fin 4) = bellAmplitude := by
  simp [bellAfterRy, show (1 : Fin 4) ≠ (0 : Fin 4) by decide]

private theorem bellAfterRy_1 :
    bellAfterRy (1 : Fin 4) = bellAmplitude := by
  simp [bellAfterRy, show (0 : Fin 4) ≠ (1 : Fin 4) by decide]

private theorem bellAfterRy_2 :
    bellAfterRy (2 : Fin 4) = 0 := by
  simp [bellAfterRy,
    show (0 : Fin 4) ≠ (2 : Fin 4) by decide,
    show (1 : Fin 4) ≠ (2 : Fin 4) by decide]

private theorem bellAfterRy_3 :
    bellAfterRy (3 : Fin 4) = 0 := by
  simp [bellAfterRy,
    show (0 : Fin 4) ≠ (3 : Fin 4) by decide,
    show (1 : Fin 4) ≠ (3 : Fin 4) by decide]

private theorem bellRy_entry_00 :
    evalPrimitiveCircuitLE bellRyCircuit (0 : Fin 4) (0 : Fin 4) =
      bellAmplitude := by
  unfold bellRyCircuit
  change evalPrimitiveCircuitLE _
    (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2))
    (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = bellAmplitude
  rw [evalPrimitiveCircuitLE_singleton_ry_apply]
  rw [if_pos (by native_decide)]
  rw [standardRyMatrix_bellRyAngle]
  norm_num [primitiveLEBits,
    Robin.warmRobinUniformBitPrepare, realOrthogonalRotation,
    bellAmplitude, TextbookStatePreparation.invSqrtTwo]

private theorem bellRy_entry_10 :
    evalPrimitiveCircuitLE bellRyCircuit (1 : Fin 4) (0 : Fin 4) =
      bellAmplitude := by
  unfold bellRyCircuit
  change evalPrimitiveCircuitLE _
    (⟨1, by norm_num [gridSize]⟩ : Fin (gridSize 2))
    (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = bellAmplitude
  rw [evalPrimitiveCircuitLE_singleton_ry_apply]
  rw [if_pos (by native_decide)]
  rw [standardRyMatrix_bellRyAngle]
  norm_num [primitiveLEBits,
    Robin.warmRobinUniformBitPrepare, realOrthogonalRotation,
    bellAmplitude, TextbookStatePreparation.invSqrtTwo]

private theorem bellRy_entry_20 :
    evalPrimitiveCircuitLE bellRyCircuit (2 : Fin 4) (0 : Fin 4) = 0 := by
  unfold bellRyCircuit
  change evalPrimitiveCircuitLE _
    (⟨2, by norm_num [gridSize]⟩ : Fin (gridSize 2))
    (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = 0
  rw [evalPrimitiveCircuitLE_singleton_ry_apply]
  rw [if_neg (by native_decide)]

private theorem bellRy_entry_30 :
    evalPrimitiveCircuitLE bellRyCircuit (3 : Fin 4) (0 : Fin 4) = 0 := by
  unfold bellRyCircuit
  change evalPrimitiveCircuitLE _
    (⟨3, by norm_num [gridSize]⟩ : Fin (gridSize 2))
    (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = 0
  rw [evalPrimitiveCircuitLE_singleton_ry_apply]
  rw [if_neg (by native_decide)]

theorem bellRy_col_zero :
    (evalPrimitiveCircuitLE bellRyCircuit).col (0 : Fin 4) = bellAfterRy := by
  funext row
  fin_cases row
  · change evalPrimitiveCircuitLE bellRyCircuit (0 : Fin 4) (0 : Fin 4) =
      bellAfterRy (0 : Fin 4)
    rw [bellRy_entry_00, bellAfterRy_0]
  · change evalPrimitiveCircuitLE bellRyCircuit (1 : Fin 4) (0 : Fin 4) =
      bellAfterRy (1 : Fin 4)
    rw [bellRy_entry_10, bellAfterRy_1]
  · change evalPrimitiveCircuitLE bellRyCircuit (2 : Fin 4) (0 : Fin 4) =
      bellAfterRy (2 : Fin 4)
    rw [bellRy_entry_20, bellAfterRy_2]
  · change evalPrimitiveCircuitLE bellRyCircuit (3 : Fin 4) (0 : Fin 4) =
      bellAfterRy (3 : Fin 4)
    rw [bellRy_entry_30, bellAfterRy_3]

theorem bellRy_prepares :
    applyVec (evalPrimitiveCircuitLE bellRyCircuit) (zeroKet 2) = bellAfterRy := by
  rw [applyVec_zeroKet]
  exact bellRy_col_zero

private theorem bellCx_entry_00 :
    evalPrimitiveCircuitLE bellCxCircuit (0 : Fin 4) (0 : Fin 4) = 1 := by
  unfold bellCxCircuit
  change evalPrimitiveCircuitLE _
    (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2))
    (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = 1
  rw [evalPrimitiveCircuitLE_singleton_cx_apply]
  rw [if_pos (by native_decide)]

private theorem bellCx_entry_10 :
    evalPrimitiveCircuitLE bellCxCircuit (1 : Fin 4) (0 : Fin 4) = 0 := by
  unfold bellCxCircuit
  change evalPrimitiveCircuitLE _
    (⟨1, by norm_num [gridSize]⟩ : Fin (gridSize 2))
    (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = 0
  rw [evalPrimitiveCircuitLE_singleton_cx_apply]
  rw [if_neg (by native_decide)]

private theorem bellCx_entry_20 :
    evalPrimitiveCircuitLE bellCxCircuit (2 : Fin 4) (0 : Fin 4) = 0 := by
  unfold bellCxCircuit
  change evalPrimitiveCircuitLE _
    (⟨2, by norm_num [gridSize]⟩ : Fin (gridSize 2))
    (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = 0
  rw [evalPrimitiveCircuitLE_singleton_cx_apply]
  rw [if_neg (by native_decide)]

private theorem bellCx_entry_30 :
    evalPrimitiveCircuitLE bellCxCircuit (3 : Fin 4) (0 : Fin 4) = 0 := by
  unfold bellCxCircuit
  change evalPrimitiveCircuitLE _
    (⟨3, by norm_num [gridSize]⟩ : Fin (gridSize 2))
    (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = 0
  rw [evalPrimitiveCircuitLE_singleton_cx_apply]
  rw [if_neg (by native_decide)]

private theorem bellCx_entry_01 :
    evalPrimitiveCircuitLE bellCxCircuit (0 : Fin 4) (1 : Fin 4) = 0 := by
  unfold bellCxCircuit
  change evalPrimitiveCircuitLE _
    (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2))
    (⟨1, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = 0
  rw [evalPrimitiveCircuitLE_singleton_cx_apply]
  rw [if_neg (by native_decide)]

private theorem bellCx_entry_11 :
    evalPrimitiveCircuitLE bellCxCircuit (1 : Fin 4) (1 : Fin 4) = 0 := by
  unfold bellCxCircuit
  change evalPrimitiveCircuitLE _
    (⟨1, by norm_num [gridSize]⟩ : Fin (gridSize 2))
    (⟨1, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = 0
  rw [evalPrimitiveCircuitLE_singleton_cx_apply]
  rw [if_neg (by native_decide)]

private theorem bellCx_entry_21 :
    evalPrimitiveCircuitLE bellCxCircuit (2 : Fin 4) (1 : Fin 4) = 0 := by
  unfold bellCxCircuit
  change evalPrimitiveCircuitLE _
    (⟨2, by norm_num [gridSize]⟩ : Fin (gridSize 2))
    (⟨1, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = 0
  rw [evalPrimitiveCircuitLE_singleton_cx_apply]
  rw [if_neg (by native_decide)]

private theorem bellCx_entry_31 :
    evalPrimitiveCircuitLE bellCxCircuit (3 : Fin 4) (1 : Fin 4) = 1 := by
  unfold bellCxCircuit
  change evalPrimitiveCircuitLE _
    (⟨3, by norm_num [gridSize]⟩ : Fin (gridSize 2))
    (⟨1, by norm_num [gridSize]⟩ : Fin (gridSize 2)) = 1
  rw [evalPrimitiveCircuitLE_singleton_cx_apply]
  rw [if_pos (by native_decide)]

private theorem bellCx_output_0 :
    (bellAmplitude • (evalPrimitiveCircuitLE bellCxCircuit).col (0 : Fin 4) +
      bellAmplitude • (evalPrimitiveCircuitLE bellCxCircuit).col (1 : Fin 4))
        (0 : Fin 4) = bellState (0 : Fin 4) := by
  change
    bellAmplitude * evalPrimitiveCircuitLE bellCxCircuit (0 : Fin 4) (0 : Fin 4) +
      bellAmplitude * evalPrimitiveCircuitLE bellCxCircuit (0 : Fin 4) (1 : Fin 4) =
      bellState (0 : Fin 4)
  rw [bellCx_entry_00, bellCx_entry_01]
  simp [bellState]

private theorem bellCx_output_1 :
    (bellAmplitude • (evalPrimitiveCircuitLE bellCxCircuit).col (0 : Fin 4) +
      bellAmplitude • (evalPrimitiveCircuitLE bellCxCircuit).col (1 : Fin 4))
        (1 : Fin 4) = bellState (1 : Fin 4) := by
  change
    bellAmplitude * evalPrimitiveCircuitLE bellCxCircuit (1 : Fin 4) (0 : Fin 4) +
      bellAmplitude * evalPrimitiveCircuitLE bellCxCircuit (1 : Fin 4) (1 : Fin 4) =
      bellState (1 : Fin 4)
  rw [bellCx_entry_10, bellCx_entry_11]
  simp [bellState]

private theorem bellCx_output_2 :
    (bellAmplitude • (evalPrimitiveCircuitLE bellCxCircuit).col (0 : Fin 4) +
      bellAmplitude • (evalPrimitiveCircuitLE bellCxCircuit).col (1 : Fin 4))
        (2 : Fin 4) = bellState (2 : Fin 4) := by
  change
    bellAmplitude * evalPrimitiveCircuitLE bellCxCircuit (2 : Fin 4) (0 : Fin 4) +
      bellAmplitude * evalPrimitiveCircuitLE bellCxCircuit (2 : Fin 4) (1 : Fin 4) =
      bellState (2 : Fin 4)
  rw [bellCx_entry_20, bellCx_entry_21]
  simp [bellState]

private theorem bellCx_output_3 :
    (bellAmplitude • (evalPrimitiveCircuitLE bellCxCircuit).col (0 : Fin 4) +
      bellAmplitude • (evalPrimitiveCircuitLE bellCxCircuit).col (1 : Fin 4))
        (3 : Fin 4) = bellState (3 : Fin 4) := by
  change
    bellAmplitude * evalPrimitiveCircuitLE bellCxCircuit (3 : Fin 4) (0 : Fin 4) +
      bellAmplitude * evalPrimitiveCircuitLE bellCxCircuit (3 : Fin 4) (1 : Fin 4) =
      bellState (3 : Fin 4)
  rw [bellCx_entry_30, bellCx_entry_31]
  simp [bellState]

theorem bellCx_on_afterRy :
    applyVec (evalPrimitiveCircuitLE bellCxCircuit) bellAfterRy = bellState := by
  unfold bellAfterRy
  let matrix : _root_.Matrix (Fin 4) (Fin 4) ℂ :=
    evalPrimitiveCircuitLE bellCxCircuit
  change applyVec matrix
    (bellAmplitude • basisKet 4 0 + bellAmplitude • basisKet 4 1) = bellState
  rw [applyVec_twoBasisSuperposition]
  funext row
  fin_cases row
  · exact bellCx_output_0
  · exact bellCx_output_1
  · exact bellCx_output_2
  · exact bellCx_output_3

theorem bellPrimitive_prepares_target :
    applyVec (evalPrimitiveCircuitLE bellPrimitiveCircuit) (zeroKet 2) =
      bellTarget.amplitudes := by
  unfold bellPrimitiveCircuit
  rw [evalPrimitiveCircuitLE_append]
  unfold applyVec
  rw [← _root_.Matrix.mulVec_mulVec]
  change
    applyVec (evalPrimitiveCircuitLE bellCxCircuit)
        (applyVec (evalPrimitiveCircuitLE bellRyCircuit) (zeroKet 2)) = bellState
  rw [bellRy_prepares]
  exact bellCx_on_afterRy

noncomputable def bellPrimitiveRoute : ExactPrimitiveStatePreparationRoute 2 where
  target := bellTarget
  circuit := bellPrimitiveCircuit
  normalizationProof := bellTarget_normalized
  preparationProof := bellPrimitive_prepares_target

theorem bellVerified_cost :
    bellPrimitiveRoute.cost =
      { auxiliaryQubits := 0, gateCount := 2, depth := 2, oracleCalls := 0 } := by
  decide

end QuantumBlockEncoding.StatePreparationBenchmarks
