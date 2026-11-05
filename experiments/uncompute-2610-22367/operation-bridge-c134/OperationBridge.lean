import StatementProbe
import Mathlib.Logic.Equiv.Fin.Basic
import Mathlib.Data.Fin.Tuple.Basic

namespace ASPBE.Uncompute.MBU.OperationBridge

open QuantumBlockEncoding

private theorem data_decompose (x : DataBasis) :
    ∃ a b : Fin 2, x = ![a, b] := by
  refine ⟨x 0, x 1, ?_⟩
  funext i
  fin_cases i <;> rfl

private theorem work_decompose (x : WorkBasis) :
    ∃ a b t : Fin 2, x = ![a, b, t] := by
  refine ⟨x 0, x 1, x 2, ?_⟩
  funext i
  fin_cases i <;> rfl

@[simp] private theorem work_vec_two (a b t : Fin 2) :
    (![a, b, t] : WorkBasis) 2 = t := rfl

private theorem sum_data {A : Type*} [AddCommMonoid A] (f : DataBasis → A) :
    (∑ x : DataBasis, f x) = ∑ a : Fin 2, ∑ b : Fin 2, f ![a, b] := by
  classical
  calc
    (∑ x : DataBasis, f x) =
        ∑ p : Fin 2 × Fin 2, f ((finTwoArrowEquiv (Fin 2)).symm p) :=
      ((finTwoArrowEquiv (Fin 2)).symm.sum_comp f).symm
    _ = _ := by rw [Fintype.sum_prod_type]; rfl

private theorem sum_work {A : Type*} [AddCommMonoid A] (f : WorkBasis → A) :
    (∑ x : WorkBasis, f x) =
      ∑ a : Fin 2, ∑ b : Fin 2, ∑ t : Fin 2, f ![a, b, t] := by
  classical
  have snoc_vector (a b t : Fin 2) :
      Fin.snoc (![a, b] : DataBasis) t = (![a, b, t] : WorkBasis) := by
    funext i
    fin_cases i <;> simp [Fin.snoc]
  calc
    (∑ x : WorkBasis, f x) =
        ∑ p : Fin 2 × DataBasis,
          f ((Fin.snocEquiv (fun _ : Fin 3 => Fin 2)) p) :=
      ((Fin.snocEquiv (fun _ : Fin 3 => Fin 2)).sum_comp f).symm
    _ = ∑ t : Fin 2, ∑ a : Fin 2, ∑ b : Fin 2, f ![a, b, t] := by
      rw [Fintype.sum_prod_type]
      apply Finset.sum_congr rfl
      intro t _
      rw [sum_data]
      change (∑ a : Fin 2, ∑ b : Fin 2,
        f (Fin.snoc (![a, b] : DataBasis) t)) = _
      simp_rw [snoc_vector]
    _ = _ := by
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro a _
      rw [Finset.sum_comm]

private theorem zeroInsert_mulVec (v : DataBasis → ℂ) (x : WorkBasis) :
    zeroInsert.mulVec v x =
      if x 2 = 0 then v ![x 0, x 1] else 0 := by
  classical
  obtain ⟨a, b, t, rfl⟩ := work_decompose x
  fin_cases a <;> fin_cases b <;> fin_cases t <;>
    simp [Matrix.mulVec, dotProduct, sum_data, Fin.sum_univ_two, zeroInsert]

private theorem conditionalCZ_mulVec (m : Fin 2) (v : DataBasis → ℂ)
    (y : DataBasis) :
    (conditionalCZ m).mulVec v y =
      conditionalCZSign m (y 0) (y 1) * v y := by
  classical
  obtain ⟨a, b, rfl⟩ := data_decompose y
  fin_cases m <;> fin_cases a <;> fin_cases b <;>
    simp [Matrix.mulVec, dotProduct, sum_data, Fin.sum_univ_two,
      conditionalCZ, phasePermutationMatrix, conditionalCZSign,
      funext_iff, Fin.forall_fin_succ]

private theorem xBra_mulVec (m : Fin 2) (v : WorkBasis → ℂ) (y : DataBasis) :
    (xBra m).mulVec v y =
      ∑ t : Fin 2, hadamardMatrix m t * v ![y 0, y 1, t] := by
  classical
  obtain ⟨a, b, rfl⟩ := data_decompose y
  fin_cases a <;> fin_cases b <;>
    simp [Matrix.mulVec, dotProduct, sum_work, Fin.sum_univ_two, xBra]

private theorem ccx3_mulVec (v : WorkBasis → ℂ) (x : WorkBasis) :
    (evalPrimitiveProgram ccx3Program).mulVec v x =
      v (ccxBasisAction (0 : Fin 3) (1 : Fin 3) (2 : Fin 3) x) := by
  classical
  rw [ccx3Program, primitiveCCXProgram_eval]
  have h := Robin.ComplexLCU.equivPermutationMatrix_mul_apply
    (ccxBasisEquiv (0 : Fin 3) (1 : Fin 3) (2 : Fin 3)
      (by decide) (by decide))
    (fun z (_ : Unit) => v z) x ()
  change (∑ z : WorkBasis,
      Robin.ComplexLCU.equivPermutationMatrix
        (ccxBasisEquiv (0 : Fin 3) (1 : Fin 3) (2 : Fin 3)
          (by decide) (by decide)) x z * v z) =
    v (ccxBasisAction (0 : Fin 3) (1 : Fin 3) (2 : Fin 3) x) at h
  exact h

theorem ccx3_zeroInsert_apply {R : Type*}
    (alpha : R → Fin 2 → Fin 2 → ℂ) (r : R) (x : WorkBasis) :
    ((_root_.Matrix.mulVec
      (evalPrimitiveProgram ccx3Program * zeroInsert)
      (fun y : DataBasis => alpha r (y 0) (y 1))) x) =
    if x 2 = andBit (x 0) (x 1)
      then alpha r (x 0) (x 1) else 0 := by
  rw [← Matrix.mulVec_mulVec, ccx3_mulVec, zeroInsert_mulVec]
  obtain ⟨a, b, t, rfl⟩ := work_decompose x
  fin_cases a <;> fin_cases b <;> fin_cases t <;>
    simp [ccxBasisAction, xBasisAction, flipBit, andBit, Function.update]

theorem zeroInsert_isometry :
    zeroInsert.conjTranspose * zeroInsert =
      (1 : _root_.Matrix DataBasis DataBasis ℂ) := by
  classical
  ext y z
  obtain ⟨a, b, rfl⟩ := data_decompose y
  obtain ⟨c, d, rfl⟩ := data_decompose z
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    simp [Matrix.mul_apply, Matrix.conjTranspose_apply, sum_work,
      Fin.sum_univ_two, zeroInsert,
      funext_iff, Fin.forall_fin_succ]

theorem conditionalCZ_isometry (m : Fin 2) :
    (conditionalCZ m).conjTranspose * conditionalCZ m =
      (1 : _root_.Matrix DataBasis DataBasis ℂ) := by
  classical
  ext y z
  obtain ⟨a, b, rfl⟩ := data_decompose y
  obtain ⟨c, d, rfl⟩ := data_decompose z
  fin_cases m <;> fin_cases a <;> fin_cases b <;>
    fin_cases c <;> fin_cases d <;>
    simp [Matrix.mul_apply, Matrix.conjTranspose_apply, sum_data,
      Fin.sum_univ_two, conditionalCZ, phasePermutationMatrix,
      conditionalCZSign, funext_iff, Fin.forall_fin_succ]

private theorem hadamard_entry (m t : Fin 2) :
    hadamardMatrix m t =
      if m = 1 ∧ t = 1 then -branchScale else branchScale := by
  fin_cases m <;> fin_cases t <;> simp [hadamardMatrix_apply, branchScale]

private theorem star_branchScale :
    (starRingEnd ℂ) branchScale = branchScale := by
  change star branchScale = branchScale
  simp [branchScale]

private theorem branchScale_mul_self :
    branchScale * branchScale = (1 / 2 : ℂ) := by
  have h : (Real.sqrt 2 / 2 : ℝ) * (Real.sqrt 2 / 2) = 1 / 2 := by
    nlinarith [Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)]
  unfold branchScale
  rw [← Complex.ofReal_mul, h]
  norm_num

theorem xBra_complete :
    (∑ m : Fin 2, (xBra m).conjTranspose * xBra m) =
      (1 : _root_.Matrix WorkBasis WorkBasis ℂ) := by
  classical
  ext x z
  obtain ⟨a, b, t, rfl⟩ := work_decompose x
  obtain ⟨c, d, s, rfl⟩ := work_decompose z
  fin_cases a <;> fin_cases b <;> fin_cases t <;>
    fin_cases c <;> fin_cases d <;> fin_cases s <;>
    norm_num [Matrix.sum_apply, Matrix.mul_apply, Matrix.conjTranspose_apply,
      sum_data, Fin.sum_univ_two, xBra, hadamard_entry,
      star_branchScale, branchScale_mul_self, neg_mul, mul_neg,
      funext_iff, Fin.forall_fin_succ]

theorem compiledAndBranch_eq_helper {R : Type*}
    (alpha : R → Fin 2 → Fin 2 → ℂ)
    (m : Fin 2) (r : R) (x : WorkBasis) :
    ((_root_.Matrix.mulVec
      (zeroInsert * conditionalCZ m * xBra m *
        evalPrimitiveProgram ccx3Program * zeroInsert)
      (fun y : DataBasis => alpha r (y 0) (y 1))) x) =
    correctedTemporaryAndBranch alpha m r (x 0) (x 1) (x 2) := by
  have hgraph :
      (evalPrimitiveProgram ccx3Program).mulVec
        (zeroInsert.mulVec (fun y : DataBasis => alpha r (y 0) (y 1))) =
      (fun z : WorkBasis => if z 2 = andBit (z 0) (z 1)
        then alpha r (z 0) (z 1) else 0) := by
    funext z
    rw [Matrix.mulVec_mulVec]
    exact ccx3_zeroInsert_apply alpha r z
  simp only [← Matrix.mulVec_mulVec]
  rw [zeroInsert_mulVec]
  by_cases ht : x 2 = 0
  · rw [if_pos ht, conditionalCZ_mulVec, xBra_mulVec]
    change conditionalCZSign m (x 0) (x 1) *
      (∑ t : Fin 2, hadamardMatrix m t *
        (evalPrimitiveProgram ccx3Program).mulVec
          (zeroInsert.mulVec (fun y : DataBasis => alpha r (y 0) (y 1)))
          ![x 0, x 1, t]) = _
    rw [hgraph]
    have hsum (q : Fin 2) :
        (∑ t : Fin 2, hadamardMatrix m t *
          (if t = q then alpha r (x 0) (x 1) else 0)) =
        hadamardMatrix m q * alpha r (x 0) (x 1) := by
      fin_cases q <;> simp
    change conditionalCZSign m (x 0) (x 1) *
        (∑ t : Fin 2, hadamardMatrix m t *
          (if t = andBit (x 0) (x 1) then alpha r (x 0) (x 1) else 0)) =
      (if x 2 = 0 then conditionalCZSign m (x 0) (x 1) *
        hadamardMatrix m (andBit (x 0) (x 1)) * alpha r (x 0) (x 1) else 0)
    rw [if_pos ht, hsum, mul_assoc]
  · simp [ht, correctedTemporaryAndBranch]

theorem compiledAndCleanupKernel_eq (m : Fin 2) :
    zeroInsert * conditionalCZ m * xBra m *
      QuantumBlockEncoding.evalPrimitiveProgram ccx3Program * zeroInsert =
    ASPBE.Uncompute.MBU.branchScale • zeroInsert := by
  classical
  apply Matrix.mulVec_injective
  funext v x
  let alpha : Unit → Fin 2 → Fin 2 → ℂ := fun _ a b => v ![a, b]
  have hv : (fun y : DataBasis => alpha () (y 0) (y 1)) = v := by
    funext y
    obtain ⟨a, b, rfl⟩ := data_decompose y
    rfl
  have h := compiledAndBranch_eq_helper alpha m () x
  rw [hv, correctedTemporaryAndBranch_eq] at h
  rw [h, Matrix.smul_mulVec]
  change branchScale * (if x 2 = 0 then alpha () (x 0) (x 1) else 0) =
    branchScale * zeroInsert.mulVec v x
  rw [zeroInsert_mulVec]

theorem compiledAndBranch_mass {R : Type*} [Fintype R]
    (alpha : R → Fin 2 → Fin 2 → ℂ) (m : Fin 2) :
    (∑ r : R, ∑ x : WorkBasis,
      Complex.normSq
        ((_root_.Matrix.mulVec
          (zeroInsert * conditionalCZ m * xBra m *
            evalPrimitiveProgram ccx3Program * zeroInsert)
          (fun y : DataBasis => alpha r (y 0) (y 1))) x)) =
    inputMass alpha / 2 := by
  classical
  simp_rw [compiledAndBranch_eq_helper]
  calc
    (∑ r : R, ∑ x : WorkBasis,
      Complex.normSq (correctedTemporaryAndBranch alpha m r (x 0) (x 1) (x 2))) =
        branchMass alpha m := by
      unfold branchMass
      apply Finset.sum_congr rfl
      intro r _
      rw [sum_work]
      rfl
    _ = inputMass alpha / 2 := correctedTemporaryAndBranch_mass alpha m

end ASPBE.Uncompute.MBU.OperationBridge
