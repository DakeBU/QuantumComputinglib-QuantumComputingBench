import UniformComparison
import QuantumBlockEncoding.HermiteTransferCores

namespace HermitePiecewiseUniform
open scoped BigOperators Matrix
open QuantumBlockEncoding TensorTrainCanonical Matrix

def translationCoreQ (d : ℕ) (w : ℚ) : Matrix (Fin (d+1)) (Fin (d+1)) ℚ :=
  fun i j => (j.val.choose i.val : ℚ)*w^(j.val-i.val)

theorem translationCoreQ_cast (d : ℕ) (w : ℚ) :
    (fun i j => (translationCoreQ d w i j : ℝ)) = HermiteTransferCores.translationCore d (w : ℝ) := by
  ext i j
  simp [translationCoreQ, HermiteTransferCores.translationCore]

noncomputable def polynomialKernel (d : ℕ) (step : ℚ) : MatrixProductChain.Kernel (d+1) :=
  fun q bit i j => (translationCoreQ d (step*2^q*(bit.val : ℚ)) i j : ℝ)

theorem polynomialKernel_cast (d q : ℕ) (step : ℚ) (bit : Fin 2) :
    polynomialKernel d step q bit =
      HermiteTransferCores.translationCore d ((step : ℝ)*2^q*(bit.val : ℝ)) := by
  change (fun i j => (translationCoreQ d (step*2^q*(bit.val:ℚ)) i j : ℝ)) = _
  rw [translationCoreQ_cast]
  push_cast
  rfl

private theorem polynomial_readout (d n start : ℕ) (step : ℚ) (origin : ℝ)
    (right : Fin (d+1) → ℝ) (x : Word n) :
    (∑ a, HermiteTransferCores.rowFeatures d origin a *
      MatrixProductChain.readout (polynomialKernel d step) right start x a) =
    ∑ b, HermiteTransferCores.rowFeatures d
      (origin+(step : ℝ)*2^start*(wordValue x : ℝ)) b*right b := by
  induction n generalizing start origin with
  | zero => simp [MatrixProductChain.readout, wordValue]
  | succ n ih =>
    simp only [MatrixProductChain.readout, Matrix.mulVec, dotProduct, polynomialKernel_cast,
      Finset.mul_sum]
    rw [Finset.sum_comm]
    simp only [← mul_assoc, ← Finset.sum_mul]
    change (∑ b, (HermiteTransferCores.rowFeatures d origin ᵥ*
      HermiteTransferCores.translationCore d ((step : ℝ)*2^start*(x.1.val : ℝ))) b *
      MatrixProductChain.readout (polynomialKernel d step) right (start+1) x.2 b) = _
    rw [HermiteTransferCores.rowFeatures_translationCore, ih]
    have he : origin+(step : ℝ)*2^start*(x.1.val : ℝ)+
        (step : ℝ)*2^(start+1)*(wordValue x.2 : ℝ) =
        origin+(step : ℝ)*2^start*(wordValue x : ℝ) := by
      simp only [wordValue, Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat, pow_succ]
      ring
    rw [he]

theorem polynomial_mask_free_contract (d n : ℕ) (origin step : ℚ)
    (coeff : Fin (d+1) → ℚ) (x : Word (n+1)) :
    contract (MatrixProductChain.ofKernel (polynomialKernel d step)
      (HermiteTransferCores.rowFeatures d (origin : ℝ))
      (fun i => (coeff i : ℝ)) 0 n) x 0 0 =
      (∑ i : Fin (d+1), coeff i*(origin+step*(wordValue x : ℚ))^i.val : ℚ) := by
  rw [MatrixProductChain.ofKernel_contract, polynomial_readout]
  simp only [pow_zero, mul_one, HermiteTransferCores.rowFeatures,
    Rat.cast_sum, Rat.cast_mul, Rat.cast_pow, Rat.cast_add, Rat.cast_natCast]
  apply Finset.sum_congr rfl
  intro i _
  ring

#print axioms translationCoreQ_cast
#print axioms polynomialKernel_cast
#print axioms polynomial_mask_free_contract
end HermitePiecewiseUniform
