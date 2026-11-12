import QuantumBlockEncoding.StoredHermiteRawSource
import QuantumBlockEncoding.StoredTensorTrainNorm
import QuantumBlockEncoding.HermiteIntervalMass

/-! Unpublished global-consumer tests. No scientific producer is replaced by
a fixture. All arbitrary-word results use the actual raw producer and its
strong refinement. Norms below consume stored local cores, not an evaluated
all-word table. Raw-construction costs remain separate from norm costs. -/

namespace QuantumBlockEncoding.StoredHermiteRawSourceTests

open StoredGivens StoredTensorTrain TensorTrainCanonical TensorTrainWord
open StoredHermiteRawSource

example (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    denoteChain (raw k n L).run.value = HermiteExplicitBond.rawSourceChain k n L :=
  raw_value k n L hL

example (k n : ℕ) (L : ℝ) (hL : 0 < L) (x : Word (n+1)) :
    contract (denoteChain (raw k n L).run.value) x 0 0 =
      HermiteStatePreparation.sampledAmplitude k (n+1) L (sampleEquiv (n+1) x) :=
  raw_contract k n L hL x

theorem raw_contract_pos (k n : ℕ) (L : ℝ) (hL : 0 < L) (x : Word (n+1)) :
    0 < contract (denoteChain (raw k n L).run.value) x 0 0 := by
  rw [raw_contract k n L hL]
  exact HermiteStatePreparation.sampledAmplitude_pos k (n+1) L _

theorem raw_maxBond (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    maxBond (denoteChain (raw k n L).run.value) ≤ 2*k+6 := by
  rw [raw_value k n L hL]
  exact HermiteExplicitBond.rawSourceChain_maxBond k n L

theorem raw_norm (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    TensorTrainNormEnvironment.norm (denoteChain (raw k n L).run.value) =
      HermiteStatePreparation.sampleNorm k (n+1) L := by
  rw [raw_value k n L hL]
  exact HermiteExplicitBond.rawSourceChain_norm k n L hL

theorem raw_norm_pos (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    0 < TensorTrainNormEnvironment.norm (denoteChain (raw k n L).run.value) := by
  rw [raw_norm k n L hL]
  exact HermiteStatePreparation.sampleNorm_pos k (n+1) L

/-- A real global consumer: the stored norm supplier receives the actual raw
tables, not a semantic core callback. Its returned scalar is the source norm. -/
theorem stored_raw_norm (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    (StoredTensorTrainNorm.norm (raw k n L).run.value).value =
      HermiteStatePreparation.sampleNorm k (n+1) L := by
  rw [StoredTensorTrainNorm.norm_value, raw_norm k n L hL]

theorem stored_raw_norm_pos (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    0 < (StoredTensorTrainNorm.norm (raw k n L).run.value).value := by
  rw [stored_raw_norm k n L hL]
  exact HermiteStatePreparation.sampleNorm_pos k (n+1) L

theorem stored_raw_norm_ge_one (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    1 ≤ (StoredTensorTrainNorm.norm (raw k n L).run.value).value := by
  rw [stored_raw_norm k n L hL, HermiteStatePreparation.sampleNorm]
  have h := Real.sqrt_le_sqrt (HermiteIntervalMass.sampled_mass_ge_one k n L)
  simpa using h

/-- Work of the norm consumer alone, on the same actual stored raw input.
This bound does not silently include or assume a zero-cost raw construction. -/
theorem stored_raw_norm_cost_le (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    StoredRectangularGivens.total (StoredTensorTrainNorm.norm (raw k n L).run.value).cost ≤
      (n+1) * (24*(2*k+6)^3 + 25*(2*k+6)^2 + 20*(2*k+6) + 6) +
        5*(2*k+6)^2 + 4*(2*k+6) + 9 :=
  StoredTensorTrainNorm.norm_total_cost_le _ (2*k+6) (raw_maxBond k n L hL)

section ConcreteWordFixtures

-- Concrete recursive word literals end in `Word 0 = Unit`. Restore the
-- definitional unfolding needed by rewrite matching, without changing any
-- endpoint, bit-order, or cutoff assertion.
set_option backward.isDefEq.respectTransparency false

/-- N=1, false digit is the literal left endpoint. -/
theorem raw_one_bit_left (k : ℕ) (L : ℝ) (hL : 0 < L) :
    contract (denoteChain (raw k 0 L).run.value) (0, ()) 0 0 =
      HermitePolynomial.smoothInitial k (-Real.pi*L) := by
  have hi : (sampleEquiv 1 ((0, ()) : Word 1)).val = 0 := by
    rw [sampleEquiv_value]
    rfl
  rw [raw_contract k 0 L hL]
  simp only [HermiteStatePreparation.sampledAmplitude, HermiteStatePreparation.gridPoint,
    hi, Nat.cast_zero, zero_mul, add_zero]

/-- N=1, true digit is the central zero sample. Both boundary contractions
must survive, including the right first-stage selector. -/
theorem raw_one_bit_right (k : ℕ) (L : ℝ) (hL : 0 < L) :
    contract (denoteChain (raw k 0 L).run.value) (1, ()) 0 0 = 1 := by
  have hi : sampleEquiv 1 ((1, ()) : Word 1) = HermiteIntervalMass.centralIndex 0 := by
    apply Fin.ext
    rw [sampleEquiv_value]
    rfl
  rw [raw_contract k 0 L hL, hi, HermiteStatePreparation.sampledAmplitude,
    HermiteIntervalMass.gridPoint_central, HermiteIntervalMass.smoothInitial_zero]

-- Cutoff zero: the sample exactly -1 uses the Hermite endpoint value.
example (k : ℕ) :
    contract (denoteChain (raw k 0 (1 / Real.pi)).run.value) (0, ()) 0 0 = Real.exp (-1) := by
  rw [raw_one_bit_left k _ (by positivity)]
  have hp : -Real.pi * (1 / Real.pi) = (-1 : ℝ) := by field_simp
  rw [hp, HermitePolynomial.smoothInitial_middle k (-1) (by constructor <;> norm_num)]
  simpa using HermitePolynomial.sourceInterpolant_left_jet k 0 (Nat.zero_le k)

example (k : ℕ) :
    contract (denoteChain (raw k 0 (1 / Real.pi)).run.value) (1, ()) 0 0 = 1 :=
  raw_one_bit_right k _ (by positivity)

-- Cutoff equals midpoint at N=1: the middle interval is empty.
example (k : ℕ) :
    contract (denoteChain (raw k 0 (2 / Real.pi)).run.value) (0, ()) 0 0 = Real.exp (-2) := by
  rw [raw_one_bit_left k _ (by positivity)]
  have hp : -Real.pi * (2 / Real.pi) = (-2 : ℝ) := by field_simp
  rw [hp]
  exact HermitePolynomial.smoothInitial_left k (-2) (by norm_num)

example (k : ℕ) :
    contract (denoteChain (raw k 0 (2 / Real.pi)).run.value) (1, ()) 0 0 = 1 :=
  raw_one_bit_right k _ (by positivity)

-- The distinct words 01 and 10 discriminate chronological bit order.
example (k : ℕ) (L : ℝ) (hL : 0 < L) :
    contract (denoteChain (raw k 1 L).run.value) (0, 1, ()) 0 0 =
      HermitePolynomial.smoothInitial k (-Real.pi*L/2) := by
  have hi : (sampleEquiv 2 ((0, 1, ()) : Word 2)).val = 1 := by
    rw [sampleEquiv_value]
    rfl
  rw [raw_contract k 1 L hL]
  simp only [HermiteStatePreparation.sampledAmplitude, HermiteStatePreparation.gridPoint,
    hi, Nat.cast_one, one_mul]
  congr 1
  norm_num [gridSize]
  ring

example (k : ℕ) (L : ℝ) (hL : 0 < L) :
    contract (denoteChain (raw k 1 L).run.value) (1, 0, ()) 0 0 = 1 := by
  have hi : sampleEquiv 2 ((1, 0, ()) : Word 2) = HermiteIntervalMass.centralIndex 1 := by
    apply Fin.ext
    rw [sampleEquiv_value]
    rfl
  rw [raw_contract k 1 L hL, hi, HermiteStatePreparation.sampledAmplitude,
    HermiteIntervalMass.gridPoint_central, HermiteIntervalMass.smoothInitial_zero]

end ConcreteWordFixtures

#print axioms raw_value
#print axioms raw_contract
#print axioms raw_maxBond
#print axioms stored_raw_norm
#print axioms stored_raw_norm_pos
#print axioms stored_raw_norm_ge_one
#print axioms stored_raw_norm_cost_le

end QuantumBlockEncoding.StoredHermiteRawSourceTests
