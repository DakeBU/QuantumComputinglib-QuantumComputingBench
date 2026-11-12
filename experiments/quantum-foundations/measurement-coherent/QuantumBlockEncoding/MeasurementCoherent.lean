import QuantumBlockEncoding.MeasurementProbability
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
The literal finite coherent branch map on Mathlib's Hilbert-space API.
This is a mathematical finite direct-sum isometry, not a tensor-register
identification, unitary/dilation implementation, density/trace adapter,
instrument, circuit or resource theorem. No second measurement/state API
is introduced. The input completeness lemma is a preparatory dependency.
-/

namespace QuantumBlockEncoding.MeasurementCoherent

open scoped InnerProductSpace

variable {ι E F : Type*} [Fintype ι]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

/-- Retain every measurement-operator branch in the canonical finite Hilbert
direct sum. Empty outcomes, zero spaces and rectangular maps are allowed. -/
noncomputable def branchIsometry (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) :
    E →ₗᵢ[ℂ] PiLp 2 (fun _ : ι => F) where
  toFun ψ := WithLp.toLp 2 (fun i => M i ψ)
  map_add' ψ φ := by
    ext i
    exact (M i).map_add ψ φ
  map_smul' c ψ := by
    ext i
    exact (M i).map_smul c ψ
  norm_map' ψ := by
    apply (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp
    rw [PiLp.norm_sq_eq_of_L2]
    exact MeasurementProbability.sum_norm_sq_eq M hM ψ

/-- The coherent output has exactly the supplied operator-family coordinates. -/
@[simp] theorem branchIsometry_apply (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ : E) (i : ι) :
    branchIsometry M hM ψ i = M i ψ := rfl

/-- Finite branch amplitudes preserve complex cross-overlaps, not only total
squared norm. This consequence uses the actual assembled linear isometry. -/
theorem sum_inner_eq (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ φ : E) :
    ∑ i, inner ℂ (M i ψ) (M i φ) = inner ℂ ψ φ := by
  simpa only [PiLp.inner_apply, branchIsometry_apply] using
    (branchIsometry M hM).inner_map_map ψ φ

end QuantumBlockEncoding.MeasurementCoherent
