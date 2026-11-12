import RationalBlocks
import QuantumBlockEncoding.StoredMatrixProductChain

namespace HermitePiecewiseStored
open scoped BigOperators
open QuantumBlockEncoding TensorTrainCanonical StoredTensorTrain StoredGivens
open HermitePiecewiseAssembly HermitePiecewiseSourceBudget HermiteFiniteExpDegree

abbrev RationalCore (D : ℕ) := Vector (Vector ℚ (2*D)) D

structure RationalData (n D : ℕ) where
  tables : Vector (RationalCore D) (n+1)
  left : Vector ℚ D
  right : Vector ℚ D

/-- Computable exact data. The counter records container materialization only;
source/entry scalar evaluation is explicitly UNACCOUNTED, not an O(1) primitive.
One rational block object is captured once for the whole local-table pass. -/
def produceQData (k n : ℕ) (R delta : ℚ) : Run (RationalData n (assemblySize k delta)) :=
  let b := actualBlocksQ k n R delta
  let e := fullEquiv k delta
  do
    let tables ← collect fun q : Fin (n+1) =>
      collect fun a : Fin (assemblySize k delta) =>
        collect fun j : Fin (2*assemblySize k delta) =>
          pure (b.kernel q.val (finProdFinEquiv.symm j).1 (e.symm a)
            (e.symm (finProdFinEquiv.symm j).2))
    let left ← collect fun a : Fin (assemblySize k delta) => pure (b.left (e.symm a))
    let right ← collect fun a : Fin (assemblySize k delta) => pure (b.right (e.symm a))
    pure ⟨tables,left,right⟩

theorem produceQData_entry (k n : ℕ) (R delta : ℚ) (q : Fin (n+1))
    (a : Fin (assemblySize k delta)) (j : Fin (2*assemblySize k delta)) :
    (produceQData k n R delta).value.tables[q.val][a.val][j.val] =
      actualEntryQ k n R delta q.val (finProdFinEquiv.symm j).1 a
        (finProdFinEquiv.symm j).2 := by
  simp [produceQData, bind, Run.bind, pure, Run.pure, actualEntryQ]

theorem produceQData_left (k n : ℕ) (R delta : ℚ) (a : Fin (assemblySize k delta)) :
    (produceQData k n R delta).value.left[a.val] = actualLeftQ k n R delta a := by
  simp [produceQData, bind, Run.bind, pure, Run.pure, actualLeftQ]

theorem produceQData_right (k n : ℕ) (R delta : ℚ) (a : Fin (assemblySize k delta)) :
    (produceQData k n R delta).value.right[a.val] = actualRightQ k n R delta a := by
  simp [produceQData, bind, Run.bind, pure, Run.pure, actualRightQ]

noncomputable def castVector {N : ℕ} (v : Vector ℚ N) : Run (Vector ℝ N) :=
  collect fun i => do
    let x ← read v i
    pure (x : ℝ)

noncomputable def castCore {D : ℕ} (A : RationalCore D) : Run (StoredCore D D) :=
  collect fun a => do
    let row ← read A a
    castVector row

structure RealData (n D : ℕ) where
  tables : Vector (StoredCore D D) (n+1)
  left : Vector ℝ D
  right : Vector ℝ D

noncomputable def castData {n D : ℕ} (data : RationalData n D) : Run (RealData n D) := do
  let tables ← collect fun q => do
    let core ← read data.tables q
    castCore core
  let left ← castVector data.left
  let right ← castVector data.right
  pure ⟨tables,left,right⟩

theorem castVector_entry {N : ℕ} (v : Vector ℚ N) (i : Fin N) :
    (castVector v).value[i.val] = (v[i.val] : ℝ) := by
  simp [castVector, StoredGivens.read, charge, bind, Run.bind, pure, Run.pure]

theorem castData_entry {n D : ℕ} (data : RationalData n D) (q : Fin (n+1))
    (a : Fin D) (j : Fin (2*D)) :
    (castData data).value.tables[q.val][a.val][j.val] =
      (data.tables[q.val][a.val][j.val] : ℝ) := by
  simp [castData, castCore, castVector_entry, StoredGivens.read, charge, bind, Run.bind, pure, Run.pure]

noncomputable def produceData (k n : ℕ) (R delta : ℚ) :
    Run (RealData n (assemblySize k delta)) := do
  let qdata ← produceQData k n R delta
  castData qdata

theorem produceData_window (k n : ℕ) (R delta : ℚ) :
    StoredMatrixProductChain.Window (produceData k n R delta).value.tables
      (reindexKernel (fullEquiv k delta) (actualBlocks k n R delta).kernel) 0 := by
  apply StoredMatrixProductChain.window_of_entries
  intro q a b bit
  simp only [produceData, bind, Run.bind, denoteCore, denote, castData_entry,
    produceQData_entry, Equiv.symm_apply_apply, Nat.zero_add, actualEntryQ_cast]

theorem produceData_left (k n : ℕ) (R delta : ℚ) (a : Fin (assemblySize k delta)) :
    (produceData k n R delta).value.left[a.val] =
      (actualBlocks k n R delta).left ((fullEquiv k delta).symm a) := by
  simp only [produceData, castData, bind, Run.bind, pure, Run.pure,
    castVector_entry, produceQData_left, actualLeftQ_cast]

theorem produceData_right (k n : ℕ) (R delta : ℚ) (a : Fin (assemblySize k delta)) :
    (produceData k n R delta).value.right[a.val] =
      (actualBlocks k n R delta).right ((fullEquiv k delta).symm a) := by
  simp only [produceData, castData, bind, Run.bind, pure, Run.pure,
    castVector_entry, produceQData_right, actualRightQ_cast]

/-- The same generated stored tables and boundaries are passed to canonical
assembly. Its cost field is a partial ledger, NOT a full scalar-runtime claim. -/
noncomputable def produceStored (k n : ℕ) (R delta : ℚ) : Run (StoredChain (n+1) 1 1) := do
  let data ← produceData k n R delta
  StoredMatrixProductChain.ofTable data.tables data.left data.right

theorem produceStored_refines (k n : ℕ) (R delta : ℚ) :
    denoteChain (produceStored k n R delta).value = actualChain k n R delta := by
  simp only [produceStored, bind, Run.bind]
  rw [StoredMatrixProductChain.ofTable_refines _ _ _ _ 0 (produceData_window k n R delta)]
  simp only [actualChain, Function.comp_def]
  congr 1 <;> funext a
  · exact produceData_left k n R delta a
  · exact produceData_right k n R delta a

theorem produceStored_source (k n : ℕ) (R delta : ℚ) (hR : 0 < R)
    (x : Word (n+1)) :
    contract (denoteChain (produceStored k n R delta).value) x 0 0 =
      (piecewiseValue k delta (rationalGrid n R (wordIndex n x)) : ℝ) := by
  rw [produceStored_refines]
  exact actualChain_contract k n R delta hR x

theorem produceStored_maxBond (k n : ℕ) (R delta : ℚ) :
    maxBond (denoteChain (produceStored k n R delta).value) ≤
      18*(sourceDegree delta+1)+9*(2*k+1+1)+18 := by
  rw [produceStored_refines]
  exact actualChain_maxBond k n R delta

theorem produceStored_scalars (k n : ℕ) (R delta : ℚ) :
    MatrixProductChain.storedScalars (denoteChain (produceStored k n R delta).value) ≤
      2*(n+1)*(18*(sourceDegree delta+1)+9*(2*k+1+1)+18)^2 := by
  rw [produceStored_refines]
  exact actualChain_scalarEnvelope k n R delta

#print axioms produceQData_entry
#print axioms produceData_window
#print axioms produceStored_refines
#print axioms produceStored_source
#print axioms produceStored_maxBond
#print axioms produceStored_scalars
end HermitePiecewiseStored
