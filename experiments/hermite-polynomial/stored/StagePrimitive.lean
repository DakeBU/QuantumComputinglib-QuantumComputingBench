import ActiveColumns
import GrayTable
import LocalSOEmission

/-! Same-run stored completion to actual named-wire primitive stage.
This internal staging composition does not certify finite-bit computation,
global placement, saved-circuit acceptance or the full scientific ROOT. -/
namespace QuantumBlockEncoding.StagedStagePrimitive
open StoredGivens StoredTensorTrain TensorTrainCanonical TensorTrainSchedule
open ConstructiveIsometryLocal TensorTrainLocalCompiler

noncomputable def compileAt {n l r q : ℕ} (C : StoredChain n l r)
    (hB : maxBond (denoteChain C) ≤ 2^q) (t : ℕ) (ht : t<n) :
    Run (PrimitiveCircuit (q+1)) := do
  let physical ← StagedActiveColumns.completeAt C hB t ht
  let gray ← StagedGrayTable.reindex q physical
  StagedLocalSOEmission.compileGray gray

theorem gray_value {n l r q : ℕ} (C : StoredChain n l r)
    (hB : maxBond (denoteChain C) ≤ 2^q) (t : ℕ) (ht : t<n) :
    denote (StagedGrayTable.reindex q
      (StagedActiveColumns.completeAt C hB t ht).value).value =
      GrayGivensCompiler.grayCoordinates (completeStage (denoteChain C) hB t) := by
  rw [StagedGrayTable.reindex_grayCoordinates, StagedActiveColumns.completeAt_value]
  congr 1
  ext row col
  simp

theorem compileAt_eval {n l r q : ℕ} (C : StoredChain n l r)
    (hC : RightCanonical (denoteChain C))
    (hB : maxBond (denoteChain C) ≤ 2^q) (t : ℕ) (ht : t<n) :
    evalPrimitiveCircuit (compileAt C hB t ht).value =
      (completeStage (denoteChain C) hB t).map Complex.ofReal := by
  have spec := completeStage_spec (denoteChain C) hC hB t ht
  have hO := GrayGivensCompiler.grayCoordinates_orthogonal
    (completeStage (denoteChain C) hB t) spec.1
  have hD := (GrayGivensCompiler.grayCoordinates_det
    (completeStage (denoteChain C) hB t)).trans spec.2.1
  have gray := gray_value C hB t ht
  simp only [compileAt, bind, Run.bind]
  rw [StagedLocalSOEmission.compileGray_eval _ (by rw [gray]; exact hO)
    (by rw [gray]; exact hD), gray]
  ext row col
  simp [GrayGivensCompiler.transport, GrayGivensCompiler.realTransport,
    GrayGivensCompiler.grayCoordinates, Matrix.reindexAlgEquiv_apply,
    Matrix.reindex_apply]

theorem compileAt_column {n l r q : ℕ} (C : StoredChain n l r)
    (hC : RightCanonical (denoteChain C))
    (hB : maxBond (denoteChain C) ≤ 2^q) (t : ℕ) (ht : t<n)
    (bit : Fin 2) (b a : PrimitiveBasis q)
    (ha : (primitiveBasisLEEquiv q a).val < rankAt (denoteChain C) t) :
    evalPrimitiveCircuit (compileAt C hB t ht).value
      (Fin.snoc b bit) (Fin.snoc a 0) =
      paddedAt (denoteChain C) t
        (bit, primitiveBasisLEEquiv q b) (primitiveBasisLEEquiv q a) := by
  rw [compileAt_eval C hC hB t ht]
  exact (completeStage_spec (denoteChain C) hC hB t ht).2.2 bit b a ha

def stageBudget (q rank t : ℕ) : ℕ :=
  StagedActiveColumns.stageBudget q rank t +
    8*StagedGrayTable.tableBudget q + StagedLocalSOEmission.compilerBudget q

private theorem total_add (a b : Cost) :
    StoredRectangularGivens.total (a+b) =
      StoredRectangularGivens.total a + StoredRectangularGivens.total b := by
  simp [StoredRectangularGivens.total]
  omega

theorem compileAt_total_cost {n l r q : ℕ} (C : StoredChain n l r)
    (hB : maxBond (denoteChain C) ≤ 2^q) (t : ℕ) (ht : t<n) :
    StoredRectangularGivens.total (compileAt C hB t ht).cost ≤
      stageBudget q (rankAt (denoteChain C) t) t := by
  have hA := StagedActiveColumns.completeAt_total_cost_le C hB t ht
  have hG := StagedGrayTable.reindex_total_cost q
    (StagedActiveColumns.completeAt C hB t ht).value
  have hE := StagedLocalSOEmission.compileGray_total_cost_le
    (StagedGrayTable.reindex q (StagedActiveColumns.completeAt C hB t ht).value).value
  simp only [compileAt, bind, Run.bind, total_add, stageBudget]
  omega

theorem compileAt_gateCount {n l r q : ℕ} (C : StoredChain n l r)
    (hB : maxBond (denoteChain C) ≤ 2^q) (t : ℕ) (ht : t<n) :
    (compileAt C hB t ht).value.gateCount =
      (2^(q+1)*(2^(q+1)-1)/2)*StagedLocalSOEmission.gatesPerPlane q := by
  simp only [compileAt, bind, Run.bind]
  exact StagedLocalSOEmission.compileGray_gateCount _

#print axioms compileAt_eval
#print axioms compileAt_column
#print axioms compileAt_total_cost
#print axioms compileAt_gateCount
end QuantumBlockEncoding.StagedStagePrimitive
