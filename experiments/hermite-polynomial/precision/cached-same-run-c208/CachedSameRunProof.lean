import CachedChainValueProof
import CachedMiddleCostProof
import CacheConsumerChecks
import AccountedTraffic

/-! C208 proof-only successor to the preserved C199/C207 timeout.
Only the hcost proof exposes named local aliases and Run.bind explicitly before
linear cost algebra; actual cache/setup/middle definitions stay unopened.
C150 bodies, exact C156 conclusion, all budgets and public premises are unchanged.
Kernel/left scalar work AND captured actualBlocksQ setup remain UNACCOUNTED.
Same-returned-run is not native runtime or physical one-evaluation. Uncompiled. -/

namespace HermiteCachedPiecewiseStored
open scoped BigOperators
open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open QuantumBlockEncoding.StoredTensorTrain
open HermitePiecewiseAssembly HermitePiecewiseStored

private theorem c199_total_add (a b : Cost) :
    StoredRectangularGivens.total (a+b) =
      StoredRectangularGivens.total a + StoredRectangularGivens.total b := by
  simp only [StoredRectangularGivens.total, Pi.add_apply]
  ring

/-- Exact annotation of the literal three collects. Arbitrary right-entry
work remains in the finite sum. The pure scalar callbacks are the original
UNACCOUNTED kernel/left boundary, not a native-cost claim or a new producer. -/
private theorem c199_pass_total {n D : ℕ}
    (kernel : Fin (n+1) → Fin D → Fin (2*D) → ℚ)
    (leftEntry : Fin D → ℚ) (rightEntryRun : Fin D → Run ℚ) :
    StoredRectangularGivens.total (do
      let tables ← collect fun q : Fin (n+1) =>
        collect fun a : Fin D =>
          collect fun j : Fin (2*D) => pure (kernel q a j)
      let left ← collect fun a : Fin D => pure (leftEntry a)
      let right ← collect rightEntryRun
      pure ⟨tables,left,right⟩ : Run (RationalData n D)).cost =
        4*passContainers n D +
          ∑ a : Fin D, StoredRectangularGivens.total (rightEntryRun a).cost := by
  simp [StoredRectangularGivens.total, bind, Run.bind, pure, Run.pure,
    collect_cost, passContainers, tick, Finset.sum_add_distrib] <;> ring

private theorem c199_qdata_total (k n : ℕ) (R delta : ℚ) :
    StoredRectangularGivens.total (produceCachedQData k n R delta).cost ≤
      816*(k+1)^2 + StoredRectangularGivens.total (rightSetup n R delta).cost +
      11*assemblySize k delta + 4*passContainers n (assemblySize k delta) := by
  let D := assemblySize k delta
  let cache := (HermiteChargedSourceCache.produceSourceCache k).value
  let setup := (rightSetup n R delta).value
  let middle := (middleFromCache k setup.midpoint cache).value
  let block := actualBlocksQ k n R delta
  let e := fullEquiv k delta
  let entries : Fin D → Run ℚ := fun a =>
    rightEntry k n R delta setup middle (e.symm a)
  let pass : Run (RationalData n D) := do
    let tables ← collect fun q : Fin (n+1) =>
      collect fun a : Fin D =>
        collect fun j : Fin (2*D) =>
          pure (block.kernel q.val (finProdFinEquiv.symm j).1 (e.symm a)
            (e.symm (finProdFinEquiv.symm j).2))
    let left ← collect fun a : Fin D => pure (block.left (e.symm a))
    let right ← collect entries
    pure ⟨tables,left,right⟩
  have hs : (∑ a : Fin D, StoredRectangularGivens.total (entries a).cost) ≤ 11*D := by
    calc
      _ ≤ ∑ _a : Fin D, 11 := Finset.sum_le_sum (fun a _ =>
        rightEntry_total_le k n R delta setup middle (e.symm a))
      _ = _ := by simp [Nat.mul_comm]
  have hp : StoredRectangularGivens.total pass.cost =
      4*passContainers n D +
        ∑ a : Fin D, StoredRectangularGivens.total (entries a).cost := by
    exact c199_pass_total
      (fun q a j => block.kernel q.val (finProdFinEquiv.symm j).1 (e.symm a)
        (e.symm (finProdFinEquiv.symm j).2))
      (fun a => block.left (e.symm a)) entries
  have hc := HermiteChargedSourceCache.produceSourceCache_total_le k
  have hm := middleFromCache_total_le k setup.midpoint cache
  have hcost : StoredRectangularGivens.total (produceCachedQData k n R delta).cost =
      StoredRectangularGivens.total (HermiteChargedSourceCache.produceSourceCache k).cost +
      StoredRectangularGivens.total (rightSetup n R delta).cost +
      StoredRectangularGivens.total (middleFromCache k setup.midpoint cache).cost +
      StoredRectangularGivens.total pass.cost := by
    simp only [produceCachedQData, pass, entries, D, cache, setup, middle,
      block, e, bind, Run.bind, c199_total_add]
    ring
  rw [hcost, hp]
  change _ ≤ 816*(k+1)^2 +
    StoredRectangularGivens.total (rightSetup n R delta).cost +
    11*D + 4*passContainers n D
  omega

private theorem c199_cast_total {n D : ℕ} (data : RationalData n D) :
    StoredRectangularGivens.total (castData data).cost = 5*passContainers n D := by
  simp [StoredRectangularGivens.total, castData_traffic, tick] <;> ring

private theorem c199_data_total (k n : ℕ) (R delta : ℚ) :
    StoredRectangularGivens.total (produceCachedData k n R delta).cost ≤
      816*(k+1)^2 + StoredRectangularGivens.total (rightSetup n R delta).cost +
      11*assemblySize k delta + 9*passContainers n (assemblySize k delta) := by
  have hq := c199_qdata_total k n R delta
  simp only [produceCachedData, bind, Run.bind, c199_total_add, c199_cast_total]
  omega

theorem produceCachedStored_same_run :
    ∀ (k n : ℕ) (R delta : ℚ),
    let result := produceCachedStored k n R delta
    let D := assemblySize k delta
    denoteChain result.value = actualChain k n R delta ∧
    StoredRectangularGivens.total result.cost ≤
      816*(k+1)^2 + StoredRectangularGivens.total (rightSetup n R delta).cost +
      11*D + 9*HermitePiecewiseStored.passContainers n D +
      20*D^2 + 30*D + 5*n^2 + 7*n + 31 := by
  intro k n R delta
  dsimp only
  constructor
  · exact produceCachedStored_refines k n R delta
  · have hd := c199_data_total k n R delta
    have ha := StoredMatrixProductChain.ofTable_total_cost_le
      (produceCachedData k n R delta).value.tables
      (produceCachedData k n R delta).value.left
      (produceCachedData k n R delta).value.right
    simp only [produceCachedStored, bind, Run.bind, c199_total_add]
    omega

end HermiteCachedPiecewiseStored
