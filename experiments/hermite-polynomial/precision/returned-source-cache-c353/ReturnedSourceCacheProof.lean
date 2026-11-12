import SourceSuffixBindingProof
import SourceSuffixEnvelopeProof

/-! C353: only the sealed THIRD root. The actual returned C23 vector is
connected to the already proved binding and mathematical envelope roots. -/

namespace HermiteSourceSuffix

/-- The same actual returned cache entry, with all table correctness supplied
internally by the original factorial producer. No producer or root is changed. -/
theorem returnedCache : ReturnedCacheSpec := by
  unfold ReturnedCacheSpec
  intro k i
  dsimp only
  have hFactorials : ∀ r : Fin (2*k+2),
      (actualFactorials k)[r.val] = (r.val.factorial : ℚ) := by
    intro r
    exact HermiteChargedSourceCache.factorials_value (2*k+1) r
  have hBinding := actualSuffix k i ⟨0, by omega⟩
  have hEnvelope := suffixEnvelope k i ⟨0, by omega⟩
  have hEntry := HermiteChargedSourceCache.sourceEntry_value
    k (actualFactorials k) hFactorials i
  have hReturned :
      (HermiteChargedSourceCache.produceSourceCache k).value[i.val] =
        actualSuffixObservation k i ⟨0, by omega⟩ :=
    (HermiteChargedSourceCache.produceSourceCache_entry k i).trans
      (hEntry.symm.trans hBinding.2.1.symm)
  have hMath :
      (HermiteChargedSourceCache.produceSourceCache k).value[i.val] =
        SourceSuffix k i ⟨0, by omega⟩ :=
    hReturned.trans hBinding.1
  refine ⟨hReturned, ?_, ?_, ?_⟩
  · rw [hMath]
    exact hEnvelope.1
  · rw [hMath]
    exact hEnvelope.2.1
  · rw [hMath]
    have hUpper : SourceSuffix k i ⟨0, by omega⟩ ≤
        (((i.val+1)*2^(2*k) : ℕ) : ℚ) := by
      simpa only [Nat.sub_zero] using hEnvelope.2.2
    have hi : i.val+1 ≤ k+1 := by
      have hiLt := i.isLt
      omega
    have hNat : (i.val+1)*2^(2*k) ≤ (k+1)*2^(2*k) :=
      Nat.mul_le_mul_right (2^(2*k)) hi
    have hRat : (((i.val+1)*2^(2*k) : ℕ) : ℚ) ≤
        (((k+1)*2^(2*k) : ℕ) : ℚ) := by
      exact_mod_cast hNat
    exact hUpper.trans hRat

#check (returnedCache : ReturnedCacheSpec)
#print axioms returnedCache

end HermiteSourceSuffix
