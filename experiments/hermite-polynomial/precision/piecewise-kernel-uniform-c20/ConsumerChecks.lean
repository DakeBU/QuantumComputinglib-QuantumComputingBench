import UniformTranslation
import UniformThresholds

namespace HermitePiecewiseUniform
open QuantumBlockEncoding TensorTrainCanonical StoredTensorTrain

theorem actual_source_mask_consumers (n T : ℕ) (R : ℚ) (hR : 0<R)
    (x : Word (n+1)) :
    let p := -R+2*R*(wordValue x:ℚ)/(2:ℚ)^(n+1)
    contract (denoteChain (produceComparison n (strictCut (n+1) R (-1))).run.value) x 0 0 =
        (if p < -1 then 1 else 0) ∧
    contract (denoteChain (produceComparison n (inclusiveCut (n+1) R 0)).run.value) x 0 0 =
        (if p ≤ 0 then 1 else 0) ∧
    contract (denoteChain (produceComparison n (inclusiveCut (n+1) R (-(T:ℚ)))).run.value) x 0 0 =
        (if p ≤ -(T:ℚ) then 1 else 0) ∧
    1-contract (denoteChain (produceComparison n (strictCut (n+1) R (T:ℚ))).run.value) x 0 0 =
        (if (T:ℚ) ≤ p then 1 else 0) := by
  dsimp only
  refine ⟨stored_strict_grid_mask _ _ _ hR _, stored_inclusive_grid_mask _ _ _ hR _,
    stored_inclusive_grid_mask _ _ _ hR _, ?_⟩
  rw [stored_strict_grid_mask _ _ _ hR]
  split_ifs <;> norm_num at * <;> linarith

theorem same_returned_maxBond (n cut : ℕ) :
    maxBond (denoteChain (produceComparison n cut).run.value) ≤ 3 := by
  rw [produceComparison_refines]
  exact MatrixProductChain.ofKernel_maxBond _ _ _ _ _

theorem same_returned_storage (n cut : ℕ) :
    MatrixProductChain.storedScalars (denoteChain (produceComparison n cut).run.value) ≤
      18*(n+1) := by
  have h := MatrixProductChain.storedScalars_le _ 3 (same_returned_maxBond n cut)
  norm_num at h
  omega

theorem inclusive_N_endpoint (n : ℕ) (x : Word (n+1)) :
    contract (denoteChain (produceComparison n (2^(n+1))).run.value) x 0 0 = 1 := by
  rw [stored_comparison_contract n _ le_rfl]
  simp [wordValue_lt]

theorem zero_endpoint (n : ℕ) (x : Word (n+1)) :
    contract (denoteChain (produceComparison n 0).run.value) x 0 0 = 0 := by
  rw [stored_comparison_contract n _ (by positivity)]
  simp

#print axioms actual_source_mask_consumers
#print axioms same_returned_maxBond
#print axioms same_returned_storage
#print axioms inclusive_N_endpoint
#print axioms zero_endpoint
end HermitePiecewiseUniform
