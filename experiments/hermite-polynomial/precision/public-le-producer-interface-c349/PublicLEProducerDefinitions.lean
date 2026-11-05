import ExplicitFiveBlockDefinitions
import PiecewiseSourceBudget
import QuantumBlockEncoding.TensorTrainWord

/-! C349 interface formation only. These three closed Props are not theorems.
The Euclidean vector is a noncomputable denotational specification of the
unchanged literal producer, not a new dense executable table or algorithm.
No reverseBasis/sampleEquiv, new error allocation or source-correctness oracle.
-/

namespace HermitePublicLEProducer

open QuantumBlockEncoding

/-- Direct public little-endian map, with no reversal. -/
def eLE (w : ℕ) : TensorTrainCanonical.Word w ≃ Fin (gridSize w) :=
  (TensorTrainWord.basisEquiv w).trans (primitiveBasisLEEquiv w)

/-- Exact denotation of the returned stored chain on the public LE grid. -/
noncomputable def producerVector (k n : ℕ) (R delta : ℚ) :
    EuclideanSpace ℂ (Fin (gridSize (n+1))) :=
  WithLp.toLp 2 (fun j =>
    ((TensorTrainCanonical.contract
      (StoredTensorTrain.denoteChain
        (HermiteExplicitCachedStored.produceExplicitStored k n R delta).run.value)
      ((eLE (n+1)).symm j) 0 0 : ℝ) : ℂ))

/-- Interface 1: first word bit is the least-significant public bit. -/
def wordIndex_public_LE : Prop :=
  ∀ (n : ℕ) (x : TensorTrainCanonical.Word (n+1)),
    HermitePiecewiseAssembly.wordIndex n x =
      primitiveBasisLEEquiv (n+1) (TensorTrainWord.toBasis x)

/-- Interface 2: hR is the existing source supplier's local domain premise.
No correctness, normalization, error or cost witness is assumed. -/
def producerVector_eq_finiteVector : Prop :=
  ∀ (k n : ℕ) (R delta : ℚ) (_hR : 0 < R),
    producerVector k n R delta =
      HermitePiecewiseSourceBudget.finiteVector k n R delta

/-- Interface 3: reuse the existing allocation and epsilon/2 conclusion.
This positive-Rat-L branch does not settle arbitrary original Real L. -/
def normalized_allocated_producer_original_error : Prop :=
  ∀ (k n : ℕ) (L epsilon : ℚ) (_hL : 0 < L) (_he : 0 < epsilon),
    ‖NormedSpace.normalize
        (producerVector k n
          (ExperimentalGlobalRadiusBudget.allocatedRadius k n L epsilon)
          (HermitePiecewiseSourceBudget.sourceDelta k n epsilon)) -
      ExperimentalNormalizationStability.targetVector k n (L : ℝ)‖ ≤
        (epsilon : ℝ)/2

end HermitePublicLEProducer
