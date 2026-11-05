import CachedRightSetup
import StoredProducer

/-! Same-object C22 dataflow with actual C23 cache consumption.
Kernel and left-boundary scalar evaluation remain explicitly UNACCOUNTED.
The old right-boundary callback is not executed. Rational source/middle/right
work and concrete right setup are counted, without a full-runtime claim. -/

namespace HermiteCachedPiecewiseStored
open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open QuantumBlockEncoding.StoredTensorTrain
open HermitePiecewiseAssembly HermitePiecewiseStored

/-- One outer C23 cache bind, one actual midpoint/setup, one signed middle
vector, actual stored reads at the middle right boundary, same local kernels
and left boundary. No call to the old QData producer supplies this output. -/
def produceCachedQData (k n : ℕ) (R delta : ℚ) :
    Run (RationalData n (assemblySize k delta)) := do
  let cache ← HermiteChargedSourceCache.produceSourceCache k
  let setup ← rightSetup n R delta
  let middle ← middleFromCache k setup.midpoint cache
  let block := HermitePiecewiseStored.actualBlocksQ k n R delta
  let e := fullEquiv k delta
  let tables ← collect fun q : Fin (n+1) =>
    collect fun a : Fin (assemblySize k delta) =>
      collect fun j : Fin (2*assemblySize k delta) =>
        -- UNACCOUNTED: original kernel scalar evaluation, not O(1).
        pure (block.kernel q.val (finProdFinEquiv.symm j).1 (e.symm a)
          (e.symm (finProdFinEquiv.symm j).2))
  let left ← collect fun a : Fin (assemblySize k delta) =>
    -- UNACCOUNTED: original left-boundary scalar evaluation, not O(1).
    pure (block.left (e.symm a))
  let right ← collect fun a : Fin (assemblySize k delta) =>
    rightEntry k n R delta setup middle (e.symm a)
  pure ⟨tables,left,right⟩

noncomputable def produceCachedData (k n : ℕ) (R delta : ℚ) :
    Run (RealData n (assemblySize k delta)) := do
  let qdata ← produceCachedQData k n R delta
  HermitePiecewiseStored.castData qdata

/-- Canonical assembly consumes the very data returned by the cached pass.
Its cost is still a partial ledger because kernel/left scalar work is open. -/
noncomputable def produceCachedStored (k n : ℕ) (R delta : ℚ) :
    Run (StoredChain (n+1) 1 1) := do
  let data ← produceCachedData k n R delta
  StoredMatrixProductChain.ofTable data.tables data.left data.right

end HermiteCachedPiecewiseStored
