import QuantumBlockEncoding.TensorTrainSchedule
import QuantumBlockEncoding.RealIsometryCompletion
import QuantumBlockEncoding.GrayGivensCompiler

namespace QuantumBlockEncoding.TensorTrainLocalCompiler

open scoped BigOperators
open TensorTrainCanonical TensorTrainSchedule SequentialBondPreparation

/-- Coordinate adapter for special-orthogonal completion on any finite
named basis, with prescribed columns at arbitrary physical labels. -/
theorem exists_SO_named {I : Type*} [Fintype I] [DecidableEq I] {r : ℕ}
    (hr : r < Fintype.card I) (V : _root_.Matrix I (Fin r) ℝ) (e : Fin r ↪ I)
    (hV : V.transpose * V = 1) :
    ∃ U : _root_.Matrix I I ℝ, U.transpose * U = 1 ∧ U.det = 1 ∧
      ∀ i a, U i (e a) = V i a := by
  classical
  let f := Fintype.equivFin I
  let W : _root_.Matrix (Fin (Fintype.card I)) (Fin r) ℝ := fun i a => V (f.symm i) a
  have hW : W.transpose * W = 1 := by
    ext a b
    have h := congrFun (congrFun hV a) b
    simp only [_root_.Matrix.mul_apply, _root_.Matrix.transpose_apply] at h ⊢
    exact ((f.symm).sum_comp (fun i => V i a * V i b)).trans h
  obtain ⟨U, hU, hd, hc⟩ := RealIsometryCompletion.exists_specialOrthogonal_completion
    hr W (e.trans f.toEmbedding) hW
  let tr := _root_.Matrix.reindexAlgEquiv ℝ ℝ f.symm
  refine ⟨tr U, ?_, ?_, ?_⟩
  · change tr U.transpose * tr U = 1
    rw [← map_mul, hU, map_one]
  · simpa [tr, _root_.Matrix.reindexAlgEquiv_apply] using hd
  · intro i a
    simpa [tr, W, _root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply] using hc (f i) a

/-- The bit is the highest local physical wire; the bond uses low wires. -/
def localIndex (q : ℕ) : PrimitiveBasis (q + 1) ≃ Fin 2 × Fin (2 ^ q) :=
  (localBasisEquiv q).trans (Equiv.prodCongr (Equiv.refl _) (primitiveBasisLEEquiv q))

@[simp] theorem localIndex_snoc (q : ℕ) (b : PrimitiveBasis q) (bit : Fin 2) :
    localIndex q (Fin.snoc b bit) = (bit, primitiveBasisLEEquiv q b) := by
  simp [localIndex, localBasisEquiv, RealAmplitudePreparation.lastBasisEquiv]
  rfl

theorem paddedAt_real {n l r B : ℕ} (C : Chain n l r) (t : ℕ)
    (out : Fin 2 × Fin B) (a : Fin B) :
    ((paddedAt C t out a).re : ℂ) = paddedAt C t out a := by
  induction C generalizing t with
  | nil _ => simp [paddedAt]
  | cons A C ih =>
    cases t with
    | zero =>
      simp only [paddedAt, paddedCore]
      split_ifs <;> simp
    | succ t => exact ih t

theorem paddedAt_im_zero {n l r B : ℕ} (C : Chain n l r) (t : ℕ)
    (out : Fin 2 × Fin B) (a : Fin B) : (paddedAt C t out a).im = 0 := by
  have h := congrArg Complex.im (paddedAt_real C t out a)
  simpa only [Complex.ofReal_im] using h.symm

def activePositions {q l : ℕ} (hl : l ≤ 2 ^ q) : Fin l ↪ PrimitiveBasis (q + 1) where
  toFun a := (localIndex q).symm (0, Fin.castLE hl a)
  inj' a b h := by
    have he := congrArg (fun x => ((localIndex q) x).2.val) h
    apply Fin.ext
    simpa only [Equiv.apply_symm_apply, Fin.castLE] using he

/-- The occupied real columns of a padded core, in physical named-wire order. -/
def activeColumns {n l r q : ℕ} (C : Chain n l r) (t : ℕ)
    (hB : maxBond C ≤ 2 ^ q) :
    _root_.Matrix (PrimitiveBasis (q + 1)) (Fin (rankAt C t)) ℝ :=
  fun row a => (paddedAt C t (localIndex q row)
    (Fin.castLE ((rankAt_le_maxBond C t).trans hB) a)).re

/-- Exact real orthonormality is extracted from the proved complex padded-core
semantics; no ambient matrix or desired circuit action is assumed. -/
theorem activeColumns_isometry {n l r q : ℕ} (C : Chain n l r)
    (hC : RightCanonical C) (hB : maxBond C ≤ 2 ^ q) (t : ℕ) (ht : t < n) :
    (activeColumns C t hB).transpose * activeColumns C t hB = 1 := by
  classical
  ext a c
  have h := congrArg Complex.re (paddedAt_active_isometry C hC hB t ht a c)
  have hr : (∑ out : Fin 2 × Fin (2 ^ q),
      (paddedAt C t out (Fin.castLE ((rankAt_le_maxBond C t).trans hB) a)).re *
        (paddedAt C t out (Fin.castLE ((rankAt_le_maxBond C t).trans hB) c)).re) =
      if a = c then 1 else 0 := by
    by_cases hac : a = c <;>
      simpa [hac, map_sum, Complex.mul_re, Complex.star_def, paddedAt_im_zero] using h
  simp only [_root_.Matrix.mul_apply, _root_.Matrix.transpose_apply,
    _root_.Matrix.one_apply, activeColumns]
  exact ((localIndex q).sum_comp (fun out =>
    (paddedAt C t out (Fin.castLE ((rankAt_le_maxBond C t).trans hB) a)).re *
      (paddedAt C t out (Fin.castLE ((rankAt_le_maxBond C t).trans hB) c)).re)).trans hr

/-- Every actual canonical stage has an exact primitive implementation on the
`q` low bond wires and one highest output wire. Completion has a spare column
because the active rank is at most half the physical dimension. The existence
proof uses exact real choices and is not a classical preprocessing-cost bound. -/
theorem exists_local_circuit_with_resources {n l r q : ℕ} (C : Chain n l r)
    (hC : RightCanonical C) (hB : maxBond C ≤ 2 ^ q) (t : ℕ) (ht : t < n) :
    ∃ c : PrimitiveCircuit (q + 1),
      c.gateCount ≤ 6 * (2 ^ q) ^ 3 ∧ c.resource.oracleCalls = 0 ∧
      ∀ (bit : Fin 2) (b a : PrimitiveBasis q),
        (primitiveBasisLEEquiv q a).val < rankAt C t →
        evalPrimitiveCircuit c (Fin.snoc b bit) (Fin.snoc a 0) =
          paddedAt C t (bit, primitiveBasisLEEquiv q b) (primitiveBasisLEEquiv q a) := by
  classical
  have hl : rankAt C t ≤ 2 ^ q := (rankAt_le_maxBond C t).trans hB
  have hs : rankAt C t < Fintype.card (PrimitiveBasis (q + 1)) := by
    have hp : 0 < 2 ^ q := by positivity
    have hc : Fintype.card (PrimitiveBasis (q + 1)) = 2 ^ q * 2 := by
      simp [PrimitiveBasis, pow_succ]
    rw [hc]
    omega
  obtain ⟨U, hU, hd, columns⟩ := exists_SO_named hs (activeColumns C t hB)
    (activePositions hl) (activeColumns_isometry C hC hB t ht)
  refine ⟨GrayGivensCompiler.compileSO U,
    (GrayGivensCompiler.compileSO_cubic_bound U).1,
    (GrayGivensCompiler.compileSO_cubic_bound U).2, ?_⟩
  intro bit b a ha
  let aa : Fin (rankAt C t) := ⟨(primitiveBasisLEEquiv q a).val, ha⟩
  have hcast : Fin.castLE hl aa = primitiveBasisLEEquiv q a := by
    apply Fin.ext
    rfl
  have he : activePositions hl aa = Fin.snoc a 0 := by
    apply (localIndex q).injective
    change localIndex q ((localIndex q).symm (0, Fin.castLE hl aa)) =
      localIndex q (Fin.snoc a 0)
    rw [Equiv.apply_symm_apply, localIndex_snoc, hcast]
    rfl
  rw [GrayGivensCompiler.compileSO_eval U hU hd]
  change (U (Fin.snoc b bit) (Fin.snoc a 0) : ℂ) = _
  rw [← he, columns]
  change ((paddedAt C t (localIndex q (Fin.snoc b bit)) (Fin.castLE hl aa)).re : ℂ) = _
  rw [localIndex_snoc, hcast]
  exact paddedAt_real C t (bit, primitiveBasisLEEquiv q b) (primitiveBasisLEEquiv q a)

/-- Minimal local-column interface for sequential tensor-train assembly. -/
theorem exists_local_circuit {n l r q : ℕ} (C : Chain n l r)
    (hC : RightCanonical C) (hB : maxBond C ≤ 2 ^ q) (t : ℕ) (ht : t < n) :
    ∃ c : PrimitiveCircuit (q + 1), c.gateCount ≤ 6 * (2 ^ q) ^ 3 ∧
      ∀ (bit : Fin 2) (b a : PrimitiveBasis q),
        (primitiveBasisLEEquiv q a).val < rankAt C t →
        evalPrimitiveCircuit c (Fin.snoc b bit) (Fin.snoc a 0) =
          paddedAt C t (bit, primitiveBasisLEEquiv q b) (primitiveBasisLEEquiv q a) := by
  obtain ⟨c, hc, _, columns⟩ := exists_local_circuit_with_resources C hC hB t ht
  exact ⟨c, hc, columns⟩

end QuantumBlockEncoding.TensorTrainLocalCompiler
