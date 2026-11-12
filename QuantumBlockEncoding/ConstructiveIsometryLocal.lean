import QuantumBlockEncoding.ConstructiveIsometryCompletion
import QuantumBlockEncoding.TensorTrainLocalCompiler

/-! Deterministic SO completion at the actual local primitive-basis positions.
The old local module is used only for its explicit coordinates, active columns,
and their isometry theorem; none of its existential completion APIs is called.
No arithmetic evaluation-cost bound is asserted. -/

namespace QuantumBlockEncoding.ConstructiveIsometryLocal

open TensorTrainCanonical TensorTrainSchedule TensorTrainLocalCompiler
open ConstructiveIsometryCompletion

/-- Low bond wires, highest emitted bit, with an explicit finite coordinate map. -/
def coordinates (q : ℕ) : PrimitiveBasis (q + 1) ≃ Fin (2 * 2 ^ q) :=
  (localIndex q).trans finProdFinEquiv

noncomputable def localCompletion {q r : ℕ} (hr : r ≤ 2 ^ q)
    (V : _root_.Matrix (PrimitiveBasis (q + 1)) (Fin r) ℝ) :
    _root_.Matrix (PrimitiveBasis (q + 1)) (PrimitiveBasis (q + 1)) ℝ :=
  completeNamed (coordinates q) (by
    have : 0 < 2 ^ q := by positivity
    omega)
    V (activePositions hr)

theorem localCompletion_spec {q r : ℕ} (hr : r ≤ 2 ^ q)
    (V : _root_.Matrix (PrimitiveBasis (q + 1)) (Fin r) ℝ) (hV : V.transpose * V = 1) :
    (localCompletion hr V).transpose * localCompletion hr V = 1 ∧
    (localCompletion hr V).det = 1 ∧
    ∀ row a, localCompletion hr V row (activePositions hr a) = V row a :=
  completeNamed_spec (coordinates q) _ V (activePositions hr) hV

/-- Actual stage matrix derived from the chain's real occupied columns. -/
noncomputable def completeStage {n l r q : ℕ} (C : Chain n l r)
    (hB : maxBond C ≤ 2 ^ q) (t : ℕ) :
    _root_.Matrix (PrimitiveBasis (q + 1)) (PrimitiveBasis (q + 1)) ℝ :=
  localCompletion ((rankAt_le_maxBond C t).trans hB) (activeColumns C t hB)

theorem completeStage_spec {n l r q : ℕ} (C : Chain n l r)
    (hC : RightCanonical C) (hB : maxBond C ≤ 2 ^ q) (t : ℕ) (ht : t < n) :
    (completeStage C hB t).transpose * completeStage C hB t = 1 ∧
    (completeStage C hB t).det = 1 ∧
    ∀ (bit : Fin 2) (b a : PrimitiveBasis q),
      (primitiveBasisLEEquiv q a).val < rankAt C t →
      (completeStage C hB t (Fin.snoc b bit) (Fin.snoc a 0) : ℂ) =
        paddedAt C t (bit, primitiveBasisLEEquiv q b) (primitiveBasisLEEquiv q a) := by
  have hl : rankAt C t ≤ 2 ^ q := (rankAt_le_maxBond C t).trans hB
  obtain ⟨ho, hd, hc⟩ := localCompletion_spec hl (activeColumns C t hB)
    (activeColumns_isometry C hC hB t ht)
  refine ⟨ho, hd, ?_⟩
  intro bit b a ha
  let aa : Fin (rankAt C t) := ⟨(primitiveBasisLEEquiv q a).val, ha⟩
  have hcast : Fin.castLE hl aa = primitiveBasisLEEquiv q a := Fin.ext rfl
  have he : activePositions hl aa = Fin.snoc a 0 := by
    apply (localIndex q).injective
    change localIndex q ((localIndex q).symm (0, Fin.castLE hl aa)) =
      localIndex q (Fin.snoc a 0)
    rw [Equiv.apply_symm_apply, localIndex_snoc, hcast]
    rfl
  change (localCompletion hl (activeColumns C t hB) _ _ : ℂ) = _
  rw [← he, hc]
  change ((paddedAt C t (localIndex q (Fin.snoc b bit)) (Fin.castLE hl aa)).re : ℂ) = _
  rw [localIndex_snoc, hcast]
  exact paddedAt_real C t (bit, primitiveBasisLEEquiv q b) (primitiveBasisLEEquiv q a)

end QuantumBlockEncoding.ConstructiveIsometryLocal
