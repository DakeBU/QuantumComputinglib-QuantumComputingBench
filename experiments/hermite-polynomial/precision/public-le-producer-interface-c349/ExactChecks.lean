import PublicLEProducerDefinitions

/-! C349 own-output consumer candidate, not run by its author.
Eq.refl below checks ONLY definitional equality of a named Prop with its
literal expanded type. It does not inhabit or prove any of the three Props.
All newly introduced vector/map aliases are expanded in the last two checks.
-/

open QuantumBlockEncoding HermitePublicLEProducer

#check (eLE : ∀ w : ℕ, TensorTrainCanonical.Word w ≃ Fin (gridSize w))
#check (producerVector : ∀ (k n : ℕ), ℚ → ℚ →
  EuclideanSpace ℂ (Fin (gridSize (n+1))))

#check (Eq.refl wordIndex_public_LE :
  wordIndex_public_LE =
    (∀ (n : ℕ) (x : TensorTrainCanonical.Word (n+1)),
      HermitePiecewiseAssembly.wordIndex n x =
        primitiveBasisLEEquiv (n+1) (TensorTrainWord.toBasis x)))

#check (Eq.refl producerVector_eq_finiteVector :
  producerVector_eq_finiteVector =
    (∀ (k n : ℕ) (R delta : ℚ) (_hR : 0 < R),
      WithLp.toLp 2 (fun j : Fin (gridSize (n+1)) =>
        ((TensorTrainCanonical.contract
          (StoredTensorTrain.denoteChain
            (HermiteExplicitCachedStored.produceExplicitStored k n R delta).run.value)
          (((TensorTrainWord.basisEquiv (n+1)).trans
            (primitiveBasisLEEquiv (n+1))).symm j) 0 0 : ℝ) : ℂ)) =
      WithLp.toLp 2 (fun j : Fin (gridSize (n+1)) =>
        ((HermitePiecewiseSourceBudget.piecewiseValue k delta
          (HermitePiecewiseSourceBudget.rationalGrid n R j) : ℝ) : ℂ))))

#check (Eq.refl normalized_allocated_producer_original_error :
  normalized_allocated_producer_original_error =
    (∀ (k n : ℕ) (L epsilon : ℚ) (_hL : 0 < L) (_he : 0 < epsilon),
      ‖NormedSpace.normalize
        (WithLp.toLp 2 (fun j : Fin (gridSize (n+1)) =>
          ((TensorTrainCanonical.contract
            (StoredTensorTrain.denoteChain
              (HermiteExplicitCachedStored.produceExplicitStored k n
                (ExperimentalGlobalRadiusBudget.allocatedRadius k n L epsilon)
                (HermitePiecewiseSourceBudget.sourceDelta k n epsilon)).run.value)
            (((TensorTrainWord.basisEquiv (n+1)).trans
              (primitiveBasisLEEquiv (n+1))).symm j) 0 0 : ℝ) : ℂ))) -
        WithLp.toLp 2
          (HermiteStatePreparation.normalizedAmplitude k (n+1) (L : ℝ))‖ ≤
        (epsilon : ℝ)/2))

#print HermitePublicLEProducer.eLE
#print HermitePublicLEProducer.producerVector
#print HermitePublicLEProducer.wordIndex_public_LE
#print HermitePublicLEProducer.producerVector_eq_finiteVector
#print HermitePublicLEProducer.normalized_allocated_producer_original_error
#print axioms HermitePublicLEProducer.eLE
#print axioms HermitePublicLEProducer.producerVector
#print axioms HermitePublicLEProducer.wordIndex_public_LE
#print axioms HermitePublicLEProducer.producerVector_eq_finiteVector
#print axioms HermitePublicLEProducer.normalized_allocated_producer_original_error
