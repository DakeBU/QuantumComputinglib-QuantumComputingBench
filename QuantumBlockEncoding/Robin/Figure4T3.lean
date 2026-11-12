import QuantumBlockEncoding.Robin.Figure4MiddlePrimitive
import QuantumBlockEncoding.PrimitiveRefinement

/-!
# Complete fixed-N8 Figure-4 T3 certificate

The certified program is the standard-RY-corrected, homogeneous `f=1`
specialization.  Its clean block follows symbolically from the padded-seven
PREPARE probability, the exact middle-program coefficient theorem, and the
source sparse decomposition.
-/

namespace QuantumBlockEncoding.Robin

private theorem transportInput_eq_encode (slot system : Fin 8)
    (coefficient indicator : Fin 2) :
    warmRobinFigure4TransportInput slot system coefficient indicator =
      warmRobinFigure4EncodeBits coefficient slot (system, (indicator, 0)) := by
  funext wire
  fin_cases wire <;> rfl

set_option maxRecDepth 100000
set_option maxHeartbeats 800000

noncomputable def warmRobinFigure4PrimitiveProgram : PrimitiveProgram 9 :=
  PrimitiveProgram.seq warmRobinFigure4SelectorPrepareProgram
    (PrimitiveProgram.seq warmRobinFigure4MiddleProgram
      warmRobinFigure4SelectorPrepareProgram.dagger)

/-- Both Figure-4 work wires return clean on every selector/system branch.
The coefficient loader may superpose `q6`, but it does not alter this classical
context, so the statement is quantified over both coefficient basis values. -/
theorem warmRobinFigure4AllWorkspaceClean
    (slot column : Fin 8) (coefficient : Fin 2) :
    let afterIndicator := warmRobinFigure4DTIndicatorBasisEquiv
      (warmRobinFigure4TransportInput slot column coefficient 0)
    let output := warmRobinFigure4PostLoaderBasisEquiv afterIndicator
    output 7 = 0 ∧ output 8 = 0 := by
  rw [warmRobinFigure4IndicatorBasisEquiv_clean]
  dsimp only
  rw [warmRobinFigure4PostLoader_cleanAction]
  simp

noncomputable def warmRobinFigure4LogicalMiddle :
    _root_.Matrix
      (ComplexLCU.LCUIndex (Fin 2) (Fin 8) WarmRobinFigure4FullSystem)
      (ComplexLCU.LCUIndex (Fin 2) (Fin 8) WarmRobinFigure4FullSystem) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ warmRobinFigure4BitsEquiv
    (evalPrimitiveProgram warmRobinFigure4MiddleProgram)

theorem warmRobinFigure4LogicalMiddle_apply
    (row column :
      ComplexLCU.LCUIndex (Fin 2) (Fin 8) WarmRobinFigure4FullSystem) :
    warmRobinFigure4LogicalMiddle row column =
      evalPrimitiveProgram warmRobinFigure4MiddleProgram
        (warmRobinFigure4BitsEquiv.symm row)
        (warmRobinFigure4BitsEquiv.symm column) := by
  rfl

theorem warmRobinFigure4LogicalMiddle_cleanEntry
    (coefficientRow coefficientColumn : Fin 2)
    (leftSlot rightSlot row column : Fin 8) :
    warmRobinFigure4LogicalMiddle
        (coefficientRow, (leftSlot, (row, (0, 0))))
        (coefficientColumn, (rightSlot, (column, (0, 0)))) =
      if leftSlot = rightSlot ∧
          warmRobinSourceDTRow rightSlot column = row then
        ComplexLCU.amplitudeRotation
          (((warmRobinFigure4SourceCoefficient rightSlot column : Rat) : Real))
          coefficientRow coefficientColumn
      else 0 := by
  rw [warmRobinFigure4LogicalMiddle_apply]
  have rowEncode :
      warmRobinFigure4BitsEquiv.symm
          (coefficientRow, (leftSlot, (row, (0, 0)))) =
        warmRobinFigure4TransportInput leftSlot row coefficientRow 0 := by
    apply warmRobinFigure4BitsEquiv.injective
    rw [Equiv.apply_symm_apply]
    rw [transportInput_eq_encode]
    exact
      (warmRobinFigure4BitsEquiv_encode coefficientRow leftSlot
        (row, (0, 0))).symm
  have columnEncode :
      warmRobinFigure4BitsEquiv.symm
          (coefficientColumn, (rightSlot, (column, (0, 0)))) =
        warmRobinFigure4TransportInput rightSlot column coefficientColumn 0 := by
    apply warmRobinFigure4BitsEquiv.injective
    rw [Equiv.apply_symm_apply]
    rw [transportInput_eq_encode]
    exact
      (warmRobinFigure4BitsEquiv_encode coefficientColumn rightSlot
        (column, (0, 0))).symm
  rw [rowEncode, columnEncode]
  exact warmRobinFigure4MiddleProgram_cleanEntry _ _ _ _ _ _

/-- Exact physical-program semantics, including all macro compiler phases. -/
theorem warmRobinFigure4Primitive_eval_eq_logical :
    evalPrimitiveProgram warmRobinFigure4PrimitiveProgram =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinFigure4BitsEquiv.symm
        (star (ComplexLCU.selectorLift (coefficient := Fin 2)
            (system := WarmRobinFigure4FullSystem)
            warmRobinPaperSevenSelectorPrepare) *
          warmRobinFigure4LogicalMiddle *
          ComplexLCU.selectorLift (coefficient := Fin 2)
            (system := WarmRobinFigure4FullSystem)
            warmRobinPaperSevenSelectorPrepare) := by
  have middleReindex :
      evalPrimitiveProgram warmRobinFigure4MiddleProgram =
        _root_.Matrix.reindexAlgEquiv ℂ ℂ
          warmRobinFigure4BitsEquiv.symm
          warmRobinFigure4LogicalMiddle := by
    unfold warmRobinFigure4LogicalMiddle
    ext row column
    simp only [_root_.Matrix.reindexAlgEquiv_apply,
      _root_.Matrix.reindex_apply, _root_.Matrix.submatrix_apply,
      Equiv.symm_symm, warmRobinFigure4BitsEquiv_apply]
    have rowInverse :
        warmRobinFigure4BitsEquiv.symm (warmRobinFigure4BitsIndex row) = row :=
      warmRobinFigure4BitsEquiv.symm_apply_apply row
    have columnInverse :
        warmRobinFigure4BitsEquiv.symm (warmRobinFigure4BitsIndex column) = column :=
      warmRobinFigure4BitsEquiv.symm_apply_apply column
    rw [rowInverse, columnInverse]
  have starReindex :
      star (_root_.Matrix.reindexAlgEquiv ℂ ℂ
        warmRobinFigure4BitsEquiv.symm
        (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinFigure4FullSystem)
          warmRobinPaperSevenSelectorPrepare)) =
        _root_.Matrix.reindexAlgEquiv ℂ ℂ
          warmRobinFigure4BitsEquiv.symm
          (star (ComplexLCU.selectorLift (coefficient := Fin 2)
            (system := WarmRobinFigure4FullSystem)
            warmRobinPaperSevenSelectorPrepare)) := by
    ext row column
    rfl
  unfold warmRobinFigure4PrimitiveProgram
  rw [evalPrimitiveProgram_seq, evalPrimitiveProgram_seq,
    evalPrimitiveProgram_dagger, warmRobinFigure4_after_prepare,
    middleReindex, starReindex,
    ← _root_.Matrix.reindexAlgEquiv_mul,
    ← _root_.Matrix.reindexAlgEquiv_mul]

theorem warmRobinFigure4Logical_cleanEntry (row column : Fin 8) :
    (star (ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinFigure4FullSystem)
          warmRobinPaperSevenSelectorPrepare) *
        warmRobinFigure4LogicalMiddle *
        ComplexLCU.selectorLift (coefficient := Fin 2)
          (system := WarmRobinFigure4FullSystem)
          warmRobinPaperSevenSelectorPrepare)
      (0, (0, (row, (0, 0))))
      (0, (0, (column, (0, 0)))) =
        (warmRobinSourceSevenCleanFormula row column : ℂ) := by
  rw [mul_assoc]
  rw [ComplexLCU.star_selectorLift_mul_clean]
  have castFormula :
      (warmRobinSourceSevenCleanFormula row column : ℂ) =
        ∑ slot : Fin 8,
          if warmRobinSourceDTRow slot column = row then
            ((warmRobinSourceSevenSelectorProbability slot : Rat) : ℂ) *
              ((warmRobinSourceSevenPaddedCoefficient slot column : Rat) : ℂ)
          else 0 := by
    norm_num [warmRobinSourceSevenCleanFormula]
    apply Finset.sum_congr rfl
    intro slot _
    by_cases selected : warmRobinSourceDTRow slot column = row <;>
      simp [selected]
  rw [castFormula]
  apply Finset.sum_congr rfl
  intro slot _
  rw [_root_.Matrix.mul_apply]
  simp_rw [ComplexLCU.selectorLift_cleanColumn_apply]
  simp_rw [Fintype.sum_prod_type]
  simp only [ite_and]
  simp
  simp_rw [warmRobinFigure4LogicalMiddle_cleanEntry]
  simp
  by_cases selected : warmRobinSourceDTRow slot column = row
  · simp only [selected, if_pos]
    have selectorSum :
        (∑ x : Fin 8,
          if slot = x ∧ warmRobinSourceDTRow x column = row then
            ComplexLCU.amplitudeRotation
                (((warmRobinFigure4SourceCoefficient x column : Rat) : Real))
                0 0 *
              warmRobinPaperSevenSelectorPrepare x 0
          else 0) =
        ComplexLCU.amplitudeRotation
            (((warmRobinFigure4SourceCoefficient slot column : Rat) : Real))
            0 0 *
          warmRobinPaperSevenSelectorPrepare slot 0 := by
      rw [Finset.sum_eq_single slot]
      · simp [selected]
      · intro candidate _ candidateNe
        simp [Ne.symm candidateNe]
      · simp
    rw [selectorSum]
    have bounded := abs_le.mp
      (warmRobinFigure4SourceCoefficient_abs_le_one slot column)
    rw [ComplexLCU.amplitudeRotation_cleanEntry _ bounded.1 bounded.2]
    calc
      star (warmRobinPaperSevenSelectorPrepare slot 0) *
            ((((warmRobinFigure4SourceCoefficient slot column : Rat) : Real) : ℂ) *
              warmRobinPaperSevenSelectorPrepare slot 0) =
          (star (warmRobinPaperSevenSelectorPrepare slot 0) *
            warmRobinPaperSevenSelectorPrepare slot 0) *
              (((warmRobinFigure4SourceCoefficient slot column : Rat) : Real) : ℂ) := by
                ring
      _ = _ := by
        rw [warmRobinUniformSevenPrepare_probability slot]
        by_cases active : slot.val < 7
        · simp [warmRobinSourceSevenSelectorProbability,
            warmRobinSourceSevenPaddedCoefficient, active,
            warmRobinFigure4SourceCoefficient_eq_weight]
        · simp [warmRobinSourceSevenSelectorProbability, active]
  · have selectorSum :
        (∑ x : Fin 8,
          if slot = x ∧ warmRobinSourceDTRow x column = row then
            ComplexLCU.amplitudeRotation
                (((warmRobinFigure4SourceCoefficient x column : Rat) : Real))
                0 0 *
              warmRobinPaperSevenSelectorPrepare x 0
          else 0) = 0 := by
      apply Finset.sum_eq_zero
      intro candidate _
      by_cases same : slot = candidate
      · subst candidate
        simp [selected]
      · simp [same]
    rw [selectorSum]
    simp [selected]

noncomputable def warmRobinFigure4PrimitiveFlatUnitary :
    _root_.Matrix (Fin (gridSize 9)) (Fin (gridSize 9)) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv 9)
    (evalPrimitiveProgram warmRobinFigure4PrimitiveProgram)

theorem warmRobinFigure4PrimitiveCircuit_unitary :
    warmRobinFigure4PrimitiveFlatUnitary ∈
      _root_.Matrix.unitaryGroup (Fin (gridSize 9)) ℂ := by
  apply ComplexLCU.reindex_unitary
  exact evalPrimitiveProgram_unitary _

noncomputable def warmRobinFigure4PrimitiveCleanIndex
    (system : Fin 8) : Fin (gridSize 9) :=
  primitiveBasisLEEquiv 9
    (warmRobinFigure4TransportInput 0 system 0 0)

/-- Required whole-circuit clean entry; this is symbolic, not numerical. -/
theorem warmRobinFigure4PrimitiveCircuit_cleanEntry (row column : Fin 8) :
    warmRobinFigure4PrimitiveFlatUnitary
        (warmRobinFigure4PrimitiveCleanIndex row)
        (warmRobinFigure4PrimitiveCleanIndex column) =
      (warmRobinSourceSevenCleanFormula row column : ℂ) := by
  unfold warmRobinFigure4PrimitiveFlatUnitary
    warmRobinFigure4PrimitiveCleanIndex
  simp only [_root_.Matrix.reindexAlgEquiv_apply,
    _root_.Matrix.reindex_apply, _root_.Matrix.submatrix_apply,
    Equiv.symm_symm, Equiv.symm_apply_apply]
  rw [warmRobinFigure4Primitive_eval_eq_logical]
  simp only [_root_.Matrix.reindexAlgEquiv_apply,
    _root_.Matrix.reindex_apply, _root_.Matrix.submatrix_apply,
    Equiv.symm_symm]
  have encode (system : Fin 8) :
      warmRobinFigure4BitsEquiv
          (warmRobinFigure4TransportInput 0 system 0 0) =
        (0, (0, (system, (0, 0)))) := by
    rw [transportInput_eq_encode]
    exact
      warmRobinFigure4BitsEquiv_encode (0 : Fin 2) (0 : Fin 8)
        (system, (0, 0))
  rw [encode row, encode column]
  exact warmRobinFigure4Logical_cleanEntry row column

theorem warmRobinFigure4PrimitiveCircuit_cleanBlock (row column : Fin 8) :
    warmRobinFigure4PrimitiveFlatUnitary
        (warmRobinFigure4PrimitiveCleanIndex row)
        (warmRobinFigure4PrimitiveCleanIndex column) =
      ((RobinEvolution.warmRobinTarget row column /
        RobinEvolution.warmRobinNormalizer : Rat) : ℂ) := by
  rw [warmRobinFigure4PrimitiveCircuit_cleanEntry]
  exact_mod_cast warmRobinSourceSevenCleanFormula_eq_target row column

def warmRobinFigure4PrimitiveBlockContainsTarget : Prop :=
  ∀ row column : Fin 8,
    warmRobinFigure4PrimitiveFlatUnitary
        (warmRobinFigure4PrimitiveCleanIndex row)
        (warmRobinFigure4PrimitiveCleanIndex column) =
      warmRobinQueryTarget.operator row column /
        warmRobinQueryTarget.normalizer

theorem warmRobinFigure4PrimitiveBlockContainsTarget_proof :
    warmRobinFigure4PrimitiveBlockContainsTarget := by
  intro row column
  rw [warmRobinFigure4PrimitiveCircuit_cleanBlock]
  norm_num [warmRobinQueryTarget, warmRobinComplexTarget]

noncomputable def warmRobinFigure4PrimitivePresentation : Circuit :=
  warmRobinFigure4PrimitiveProgram.circuit.map fun gate =>
    match gate with
    | .x target => .oneQubit "X" target.val
    | .ry target _ => .rotationY target.val "exact-angle"
    | .rz target _ => .rotationZ target.val "exact-angle"
    | .cx control target _ => .cnot control.val target.val

noncomputable def warmRobinFigure4PrimitiveResource : Resource :=
  warmRobinFigure4PrimitiveProgram.resource

noncomputable def warmRobinFigure4PrimitiveOperatorCandidate :
    OperatorBlockEncodingCandidate ℂ 3 where
  auxiliaryQubits := 6
  target := warmRobinQueryTarget
  unitary := warmRobinFigure4PrimitiveFlatUnitary
  layout := {
    systemQubits := 3
    signalQubits := 4
    pureAncillas := 2
  }
  circuit := warmRobinFigure4PrimitivePresentation
  resource := warmRobinFigure4PrimitiveResource
  layoutMatches := by decide
  isUnitary := warmRobinFigure4PrimitiveFlatUnitary ∈
    _root_.Matrix.unitaryGroup (Fin (gridSize 9)) ℂ
  blockContainsTarget := warmRobinFigure4PrimitiveBlockContainsTarget

noncomputable def warmRobinFigure4PrimitiveRefinement :
    PrimitiveProgramRefinement 9 where
  program := warmRobinFigure4PrimitiveProgram
  target := _root_.Matrix.reindexAlgEquiv ℂ ℂ
    warmRobinFigure4BitsEquiv.symm
    (star (ComplexLCU.selectorLift (coefficient := Fin 2)
        (system := WarmRobinFigure4FullSystem)
        warmRobinPaperSevenSelectorPrepare) *
      warmRobinFigure4LogicalMiddle *
      ComplexLCU.selectorLift (coefficient := Fin 2)
        (system := WarmRobinFigure4FullSystem)
        warmRobinPaperSevenSelectorPrepare)
  exact := warmRobinFigure4Primitive_eval_eq_logical

/-- Fixed-N8, f=1, standard-RY-corrected Figure-4 realization. -/
noncomputable def warmRobinFigure4PrimitiveVerifiedBlockEncoding :
    VerifiedOperatorBlockEncoding ℂ 3 where
  candidate := warmRobinFigure4PrimitiveOperatorCandidate
  unitaryProof := warmRobinFigure4PrimitiveCircuit_unitary
  blockProof := warmRobinFigure4PrimitiveBlockContainsTarget_proof

end QuantumBlockEncoding.Robin
