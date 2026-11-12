import QuantumBlockEncoding.PrimitiveMacros

namespace ASPBE.Uncompute.MBU

noncomputable def branchScale : ℂ := ((Real.sqrt 2 / 2 : ℝ) : ℂ)

def andBit (a b : Fin 2) : Fin 2 := if a = 1 ∧ b = 1 then 1 else 0

def conditionalCZSign (m a b : Fin 2) : ℂ :=
  if m = 1 ∧ a = 1 ∧ b = 1 then -1 else 1

noncomputable def correctedTemporaryAndBranch {R : Type*}
    (alpha : R → Fin 2 → Fin 2 → ℂ) (m : Fin 2) (r : R) (a b t : Fin 2) : ℂ :=
  if t = 0 then conditionalCZSign m a b *
    QuantumBlockEncoding.hadamardMatrix m (andBit a b) * alpha r a b else 0

theorem correctedTemporaryAndBranch_eq {R : Type*}
    (alpha : R → Fin 2 → Fin 2 → ℂ) (m : Fin 2) (r : R) (a b t : Fin 2) :
    correctedTemporaryAndBranch alpha m r a b t =
      branchScale * (if t = 0 then alpha r a b else 0) := by
  fin_cases m <;> fin_cases a <;> fin_cases b <;> fin_cases t <;>
    simp [correctedTemporaryAndBranch, conditionalCZSign, andBit,
      QuantumBlockEncoding.hadamardMatrix_apply, branchScale]

theorem branchScale_normSq : Complex.normSq branchScale = (1 / 2 : ℝ) := by
  rw [branchScale, Complex.normSq_ofReal]
  have h : Real.sqrt (2 : ℝ) * Real.sqrt 2 = 2 := Real.mul_self_sqrt (by norm_num)
  nlinarith

noncomputable def inputMass {R : Type*} [Fintype R]
    (alpha : R → Fin 2 → Fin 2 → ℂ) : ℝ :=
  ∑ r, ∑ a, ∑ b, Complex.normSq (alpha r a b)

noncomputable def branchMass {R : Type*} [Fintype R]
    (alpha : R → Fin 2 → Fin 2 → ℂ) (m : Fin 2) : ℝ :=
  ∑ r, ∑ a, ∑ b, ∑ t, Complex.normSq (correctedTemporaryAndBranch alpha m r a b t)

theorem correctedTemporaryAndBranch_mass {R : Type*} [Fintype R]
    (alpha : R → Fin 2 → Fin 2 → ℂ) (m : Fin 2) :
    branchMass alpha m = inputMass alpha / 2 := by
  have per (r : R) (a b : Fin 2) :
      (∑ t : Fin 2, Complex.normSq (correctedTemporaryAndBranch alpha m r a b t)) =
        (1 / 2 : ℝ) * Complex.normSq (alpha r a b) := by
    simp [correctedTemporaryAndBranch_eq, Fin.sum_univ_two,
      Complex.normSq_mul, branchScale_normSq]
  unfold branchMass inputMass
  simp_rw [per]
  simp_rw [← Finset.mul_sum]
  ring

theorem outcomeMass_of_normalized {R : Type*} [Fintype R]
    (alpha : R → Fin 2 → Fin 2 → ℂ) (h : inputMass alpha = 1) (m : Fin 2) :
    branchMass alpha m = (1 / 2 : ℝ) := by
  rw [correctedTemporaryAndBranch_mass, h]

theorem sum_branchMass {R : Type*} [Fintype R]
    (alpha : R → Fin 2 → Fin 2 → ℂ) :
    (∑ m : Fin 2, branchMass alpha m) = inputMass alpha := by
  simp only [Fin.sum_univ_two, correctedTemporaryAndBranch_mass]
  ring

end ASPBE.Uncompute.MBU

#check ASPBE.Uncompute.MBU.correctedTemporaryAndBranch_eq
#check ASPBE.Uncompute.MBU.correctedTemporaryAndBranch_mass
#print axioms ASPBE.Uncompute.MBU.correctedTemporaryAndBranch_eq
#print axioms ASPBE.Uncompute.MBU.correctedTemporaryAndBranch_mass
#print axioms ASPBE.Uncompute.MBU.sum_branchMass
