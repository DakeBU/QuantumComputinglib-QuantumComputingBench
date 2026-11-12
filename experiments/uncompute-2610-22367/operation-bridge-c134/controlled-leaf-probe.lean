import StatementProbe
import Mathlib.Data.Fin.Tuple.Basic

/-
Uncompiled, isolated C132 proposal. This is precisely the positive-target leaf
after the existing full-vector hgraph rewrite, not a replacement root contract.
-/
namespace ASPBE.Uncompute.MBU.OperationBridge.C132NormalizationRepair

open QuantumBlockEncoding

theorem sum_alignment_leaf {R : Type*}
    (alpha : R → Fin 2 → Fin 2 → ℂ)
    (m : Fin 2) (r : R) (x : WorkBasis) (ht : x 2 = 0) :
    conditionalCZSign m (x 0) (x 1) *
      (∑ t : Fin 2, hadamardMatrix m t *
        (fun z : WorkBasis => if z 2 = andBit (z 0) (z 1)
          then alpha r (z 0) (z 1) else 0) ![x 0, x 1, t]) =
      correctedTemporaryAndBranch alpha m r (x 0) (x 1) (x 2) := by
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

end ASPBE.Uncompute.MBU.OperationBridge.C132NormalizationRepair
