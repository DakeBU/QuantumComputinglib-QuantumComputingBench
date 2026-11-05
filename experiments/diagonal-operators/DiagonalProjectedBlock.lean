import QuantumBlockEncoding.TextbookStatePreparation
import QuantumBlockEncoding.Robin.ComplexLCU
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Inverse

/-!
# Literal Figure 3 diagonal supplier, staging only

Source: https://arxiv.org/pdf/2404.02819v4, printed pp.10-12.
Signal-first register order; source system labels are preserved. The input
signal is 0 and acceptance is signal 1. This is NOT Eq.(18)'s same-sector
clean-block contract. Literal H--controlled phases--H--P gives cos(theta)
on signal 0, whereas Eqs.(19)-(20) print -i cos(theta); the discrepancy is
retained in statement-seal.json, not repaired by changing the circuit.
No parallelization, synthesis, approximation or resource theorem is claimed.
-/

namespace QuantumBlockEncoding.DiagonalProjectedBlock

open Robin.ComplexLCU
open TextbookStatePreparation

noncomputable def sourceH : _root_.Matrix (Fin 2) (Fin 2) ℂ := hadamard

private theorem sourceH_apply (r c : Fin 2) :
    sourceH r c = if r.val = 1 ∧ c.val = 1 then -invSqrtTwo else invSqrtTwo := by
  rfl

noncomputable def sourceP : _root_.Matrix (Fin 2) (Fin 2) ℂ :=
  _root_.Matrix.diagonal (fun j => if j = 0 then 1 else -Complex.I)

noncomputable def sourceControlledPhase (θ : ℝ) : _root_.Matrix (Fin 2) (Fin 2) ℂ :=
  _root_.Matrix.diagonal (fun j =>
    Complex.exp (((if j = 0 then θ else -θ : ℝ) : ℂ) * Complex.I))

/-- Exact chronological Figure 3 matrix: H, e^(iθZ), H, P. -/
noncomputable def sourceScalarCircuit (θ : ℝ) : _root_.Matrix (Fin 2) (Fin 2) ℂ :=
  sourceP * sourceH * sourceControlledPhase θ * sourceH

/-- No abstract block premise: a literal controlled diagonal family. -/
noncomputable def literalDilation {N : Nat} (d : Fin N → ℝ) (β : ℝ) :
    _root_.Matrix (Fin 2 × Fin N) (Fin 2 × Fin N) ℂ :=
  _root_.Matrix.blockDiagonal (fun j => sourceScalarCircuit (Real.arcsin (d j / β)))

def diagonalTarget {N : Nat} (d : Fin N → ℝ) : _root_.Matrix (Fin N) (Fin N) ℂ :=
  _root_.Matrix.diagonal (fun j => (d j : ℂ))

/-- Apply the supplied unitary to |0>⊗ψ, then read output signal 1. -/
noncomputable def acceptedBranch {N : Nat} (d : Fin N → ℝ) (β : ℝ)
    (ψ : Fin N → ℂ) (j : Fin N) : ℂ :=
  _root_.Matrix.mulVec (literalDilation d β)
    (fun input => if input.1 = 0 then ψ input.2 else 0) (1, j)

private theorem sourceP_unitary : sourceP ∈ _root_.Matrix.unitaryGroup (Fin 2) ℂ := by
  rw [_root_.Matrix.mem_unitaryGroup_iff']
  ext r c
  fin_cases r <;> fin_cases c <;>
    simp [sourceP, _root_.Matrix.mul_apply, Fin.sum_univ_two]

private theorem sourceControlledPhase_unitary (θ : ℝ) :
    sourceControlledPhase θ ∈ _root_.Matrix.unitaryGroup (Fin 2) ℂ := by
  have htrig : (Real.cos θ : ℂ)^2 + (Real.sin θ : ℂ)^2 = 1 := by
    exact_mod_cast Real.cos_sq_add_sin_sq θ
  rw [_root_.Matrix.mem_unitaryGroup_iff']
  ext r c
  fin_cases r <;> fin_cases c <;>
    simp [sourceControlledPhase, _root_.Matrix.mul_apply, Fin.sum_univ_two,
      Complex.exp_mul_I, ← Complex.ofReal_cos, ← Complex.ofReal_sin] <;>
    ring_nf <;> simp only [Complex.I_sq] <;> linear_combination htrig

private theorem sourceScalarCircuit_unitary (θ : ℝ) :
    sourceScalarCircuit θ ∈ _root_.Matrix.unitaryGroup (Fin 2) ℂ :=
  (_root_.Matrix.unitaryGroup (Fin 2) ℂ).mul_mem
    ((_root_.Matrix.unitaryGroup (Fin 2) ℂ).mul_mem
      ((_root_.Matrix.unitaryGroup (Fin 2) ℂ).mul_mem sourceP_unitary
        (show sourceH ∈ _root_.Matrix.unitaryGroup (Fin 2) ℂ from hadamard_unitary))
      (sourceControlledPhase_unitary θ))
    (show sourceH ∈ _root_.Matrix.unitaryGroup (Fin 2) ℂ from hadamard_unitary)

private theorem sourceScalarCircuit_firstColumn (θ : ℝ) (s : Fin 2) :
    sourceScalarCircuit θ s 0 =
      if s = 0 then (Real.cos θ : ℂ) else (Real.sin θ : ℂ) := by
  have hsq : invSqrtTwo ^ 2 = (1 : ℂ) / 2 := by
    simpa [pow_two] using invSqrtTwo_mul_self
  fin_cases s <;>
    simp [sourceScalarCircuit, sourceP, sourceControlledPhase, sourceH_apply,
      _root_.Matrix.mul_apply, Fin.sum_univ_two, Complex.exp_mul_I,
      ← Complex.ofReal_cos, ← Complex.ofReal_sin] <;>
    ring_nf <;> rw [hsq] <;> (try simp only [Complex.I_sq]) <;> ring

theorem literalDilation_unitary {N : Nat} (d : Fin N → ℝ) (β : ℝ) :
    literalDilation d β ∈ _root_.Matrix.unitaryGroup (Fin 2 × Fin N) ℂ :=
  blockDiagonal_unitary _ (fun _ => sourceScalarCircuit_unitary _)

/-- Internal notation adapter for Eq19's |ψ>⊗|signal> tensor order. -/
noncomputable def sourceSystemFirstDilation {N : Nat} (d : Fin N → ℝ) (β : ℝ) :
    _root_.Matrix (Fin N × Fin 2) (Fin N × Fin 2) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ (Equiv.prodComm (Fin 2) (Fin N))
    (literalDilation d β)

theorem sourceSystemFirstDilation_entry {N : Nat} (d : Fin N → ℝ) (β : ℝ)
    (sout sin : Fin 2) (row col : Fin N) :
    sourceSystemFirstDilation d β (row, sout) (col, sin) =
      literalDilation d β (sout, row) (sin, col) := by
  rfl

theorem sourceSystemFirstDilation_unitary {N : Nat} (d : Fin N → ℝ) (β : ℝ) :
    sourceSystemFirstDilation d β ∈ _root_.Matrix.unitaryGroup (Fin N × Fin 2) ℂ :=
  reindex_unitary _ _ (literalDilation_unitary d β)

theorem literalDilation_projectedBlock {N : Nat} (d : Fin N → ℝ) (β : ℝ)
    (hβ : 0 < β) (hd : ∀ j, |d j| ≤ β) (row col : Fin N) :
    literalDilation d β (1, row) (0, col) = diagonalTarget d row col / (β : ℂ) := by
  have bounds := abs_le.mp (hd row)
  have lower : -1 ≤ d row / β := (le_div_iff₀ hβ).2 (by linarith)
  have upper : d row / β ≤ 1 := (div_le_iff₀ hβ).2 (by linarith)
  by_cases h : row = col
  · subst col
    simp [literalDilation, _root_.Matrix.blockDiagonal_apply,
      sourceScalarCircuit_firstColumn, diagonalTarget, Real.sin_arcsin lower upper]
  · simp [literalDilation, _root_.Matrix.blockDiagonal_apply, diagonalTarget, h]

theorem literalDilation_acceptedBranch {N : Nat} (d : Fin N → ℝ) (β : ℝ)
    (hβ : 0 < β) (hd : ∀ j, |d j| ≤ β) (ψ : Fin N → ℂ) (j : Fin N) :
    acceptedBranch d β ψ j = (d j : ℂ) * ψ j / (β : ℂ) := by
  simp only [acceptedBranch, _root_.Matrix.mulVec, dotProduct,
    Fintype.sum_prod_type, Fin.sum_univ_two]
  simp only [ite_true]
  simp_rw [literalDilation_projectedBlock d β hβ hd]
  simp only [diagonalTarget, _root_.Matrix.diagonal_apply, div_mul_eq_mul_div,
    ite_mul, zero_mul]
  rw [← Finset.sum_div]
  simp [eq_comm]

theorem literalDilation_success {N : Nat} (d : Fin N → ℝ) (β : ℝ)
    (hβ : 0 < β) (hd : ∀ j, |d j| ≤ β) (ψ : Fin N → ℂ) :
    (∑ j, Complex.normSq (acceptedBranch d β ψ j)) =
      (∑ j, (d j)^2 * Complex.normSq (ψ j)) / β^2 := by
  simp_rw [literalDilation_acceptedBranch d β hβ hd, Complex.normSq_div,
    Complex.normSq_mul, Complex.normSq_ofReal, ← pow_two]
  exact (Finset.sum_div _ _ _).symm

theorem literalDilation_normalizedBranch {N : Nat} (d : Fin N → ℝ) (β : ℝ)
    (hβ : 0 < β) (hd : ∀ j, |d j| ≤ β) (ψ : Fin N → ℂ)
    (hm : 0 < ∑ j, (d j)^2 * Complex.normSq (ψ j)) (j : Fin N) :
    acceptedBranch d β ψ j /
        (Real.sqrt (∑ k, Complex.normSq (acceptedBranch d β ψ k)) : ℂ) =
      ((d j : ℂ) * ψ j) /
        (Real.sqrt (∑ k, (d k)^2 * Complex.normSq (ψ k)) : ℂ) := by
  rw [literalDilation_acceptedBranch d β hβ hd,
    literalDilation_success d β hβ hd]
  rw [Real.sqrt_div (le_of_lt hm), Real.sqrt_sq (le_of_lt hβ)]
  push_cast
  have hb : (β : ℂ) ≠ 0 := Complex.ofReal_ne_zero.mpr (ne_of_gt hβ)
  field_simp [hb]

/-- The normalized accepted branch has actual Euclidean mass one. -/
theorem literalDilation_normalized_mass {N : Nat} (d : Fin N → ℝ) (β : ℝ)
    (hβ : 0 < β) (hd : ∀ j, |d j| ≤ β) (ψ : Fin N → ℂ)
    (hm : 0 < ∑ j, (d j)^2 * Complex.normSq (ψ j)) :
    (∑ j, Complex.normSq (acceptedBranch d β ψ j /
      (Real.sqrt (∑ k, Complex.normSq (acceptedBranch d β ψ k)) : ℂ))) = 1 := by
  simp_rw [literalDilation_normalizedBranch d β hβ hd ψ hm,
    Complex.normSq_div, Complex.normSq_mul, Complex.normSq_ofReal, ← pow_two]
  rw [← Finset.sum_div, Real.sq_sqrt (le_of_lt hm), div_self (ne_of_gt hm)]

/-- A Born probability upper bound needs the source's normalized input state. -/
theorem literalDilation_probability_le_one {N : Nat} (d : Fin N → ℝ) (β : ℝ)
    (hβ : 0 < β) (hd : ∀ j, |d j| ≤ β) (ψ : Fin N → ℂ)
    (hψ : ∑ j, Complex.normSq (ψ j) = 1) :
    (∑ j, Complex.normSq (acceptedBranch d β ψ j)) ≤ 1 := by
  rw [literalDilation_success d β hβ hd]
  apply (div_le_one (sq_pos_of_pos hβ)).2
  calc
    _ ≤ ∑ j, β^2 * Complex.normSq (ψ j) := by
      apply Finset.sum_le_sum
      intro j _
      have bounds := abs_le.mp (hd j)
      have hs : (d j)^2 ≤ β^2 := by
        nlinarith [mul_nonneg (sub_nonneg.mpr bounds.2) (by linarith : 0 ≤ β + d j)]
      exact mul_le_mul_of_nonneg_right hs (Complex.normSq_nonneg _)
    _ = β^2 := by rw [← Finset.mul_sum, hψ, mul_one]

/- Minimal discriminators are symbolic Lean examples, not simulation evidence. -/

/-- At θ=0 the literal rejected coefficient is 1, not the printed -i. -/
theorem source_zero_angle_failure_discriminator :
    sourceScalarCircuit 0 0 0 = 1 ∧ sourceScalarCircuit 0 0 0 ≠ -Complex.I := by
  have h : sourceScalarCircuit 0 0 0 = 1 := by
    simpa using sourceScalarCircuit_firstColumn 0 0
  constructor
  · exact h
  · rw [h]
    intro bad
    have := congrArg Complex.re bad
    norm_num at this

/-- Negative values retain their sign in the accepted amplitude. -/
example : acceptedBranch (fun _ : Fin 1 => (-1 : ℝ)) 1 (fun _ => 1) 0 = -1 := by
  rw [literalDilation_acceptedBranch _ 1 (by norm_num) (by intro j; norm_num)]
  norm_num

/-- A genuinely nonunitary diagonal gives success 1/4, not deterministic success. -/
example : (∑ j, Complex.normSq
    (acceptedBranch (fun _ : Fin 1 => (1/2 : ℝ)) 1 (fun _ => 1) j)) = 1/4 := by
  rw [literalDilation_success _ 1 (by norm_num) (by intro j; norm_num)]
  norm_num

/-- A zero diagonal is meaningful at positive scale and gives the zero branch. -/
example : acceptedBranch (fun _ : Fin 1 => (0 : ℝ)) 1 (fun _ => 1) 0 = 0 := by
  rw [literalDilation_acceptedBranch _ 1 (by norm_num) (by intro j; norm_num)]
  norm_num

/-- Zero entries are kept as data slots rather than removed from the carrier. -/
example : literalDilation ![(-1 : ℝ), 0] 1 (1, 1) (0, 1) = 0 := by
  rw [literalDilation_projectedBlock _ 1 (by norm_num)
    (by intro j; fin_cases j <;> norm_num)]
  simp [diagonalTarget]

/-- Signed and nonsigned slots are simultaneous coherent amplitudes. -/
example : acceptedBranch ![(-1 : ℝ), 1/2] 1 (fun _ => 1) 0 = -1 ∧
    acceptedBranch ![(-1 : ℝ), 1/2] 1 (fun _ => 1) 1 = 1/2 := by
  have bounds : ∀ j : Fin 2, |(![(-1 : ℝ), 1/2]) j| ≤ 1 := by
    intro j
    fin_cases j <;> norm_num
  constructor <;> rw [literalDilation_acceptedBranch _ 1 (by norm_num) bounds] <;> norm_num

/-- Nonzero diagonal, but an input supported on its zero slot, has zero success. -/
example : (∑ j, Complex.normSq
    (acceptedBranch ![(-1 : ℝ), 0] 1 ![0, 1] j)) = 0 := by
  rw [literalDilation_success _ 1 (by norm_num)
    (by intro j; fin_cases j <;> norm_num)]
  norm_num [Fin.sum_univ_two]

#print axioms literalDilation_unitary
#print axioms literalDilation_projectedBlock
#print axioms literalDilation_acceptedBranch
#print axioms literalDilation_success
#print axioms literalDilation_normalizedBranch
#print axioms literalDilation_normalized_mass
#print axioms literalDilation_probability_le_one
#print axioms source_zero_angle_failure_discriminator

end QuantumBlockEncoding.DiagonalProjectedBlock
