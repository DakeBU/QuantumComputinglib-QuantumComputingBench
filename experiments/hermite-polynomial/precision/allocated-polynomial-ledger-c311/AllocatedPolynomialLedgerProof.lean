import AllocatedPolynomialCostInterface

/-! C295-sealed partial-operation parameter bounds, author-uncompiled.
Actual C147 allocation and C262 SAME returned-run suppliers are dependencies.
No value/cost/normalization callback promise is a public hypothesis. -/

namespace HermiteAllocatedPolynomialCost

open HermiteFiniteExp HermiteFiniteExpDegree
open HermitePiecewiseSourceBudget HermitePiecewiseAssembly
open HermiteExplicitCachedStored
open QuantumBlockEncoding

theorem allocatedBudgetEnvelope : intendedAllocatedBudgetEnvelope := by
  intro k n epsilon hepsilon
  dsimp only
  let delta := sourceDelta k n epsilon
  let M := operationScale k n epsilon
  let T := tailCutoff delta
  let d := sourceDegree delta
  let L := d+2*k+1
  let D := assemblySize k delta
  let P := (n+1)*(2*D^2+D+1)+2*D
  change frontierBudget k n delta ≤ 5000000*M^7 ∧
    14*(n+1)*D^2+4*D ≤ 500000*M^5
  have hM : 1 ≤ M := by dsimp [M, operationScale]; omega
  have hnp : n+1 ≤ M := by dsimp [M, operationScale]; omega
  have hn : n ≤ M := by omega
  have hk : k+1 ≤ M := by dsimp [M, operationScale]; omega
  have hmid : 2*k+1 ≤ M := by dsimp [M, operationScale]; omega
  have hp {a b : ℕ} (hab : a ≤ b) : M^a ≤ M^b :=
    pow_le_pow_right' hM hab
  have h12 : M ≤ M^2 := by simpa only [pow_one] using hp (by decide : 1 ≤ 2)
  have h02 : 1 ≤ M^2 := hM.trans h12
  have h15 : M ≤ M^5 := by simpa only [pow_one] using hp (by decide : 1 ≤ 5)
  have h25 : M^2 ≤ M^5 := hp (by decide : 2 ≤ 5)
  have h35 : M^3 ≤ M^5 := hp (by decide : 3 ≤ 5)
  have h17 : M ≤ M^7 := by simpa only [pow_one] using hp (by decide : 1 ≤ 7)
  have h27 : M^2 ≤ M^7 := hp (by decide : 2 ≤ 7)
  have h47 : M^4 ≤ M^7 := hp (by decide : 4 ≤ 7)
  have h57 : M^5 ≤ M^7 := hp (by decide : 5 ≤ 7)
  have h07 : 1 ≤ M^7 := by simpa only [pow_zero] using hp (by decide : 0 ≤ 7)
  have hT : T ≤ M := by
    simpa only [T, delta, M, operationScale] using
      HermiteAllocatedDegreeBudget.allocated_tailCutoff_le k n epsilon hepsilon
  have hd0 : d ≤ 4*M^2+2*M+1 := by
    simpa only [d, delta, M, operationScale] using
      HermiteAllocatedDegreeBudget.allocated_sourceDegree_le k n epsilon hepsilon
  have hd : d ≤ 7*M^2 := by omega
  have hd1 : d+1 ≤ 8*M^2 := by omega
  have hL : L ≤ 8*M^2 := by dsimp only [L]; omega
  have hL1 : L+1 ≤ 9*M^2 := by omega
  have hDformula : D = 18*d+9*(2*k+1)+45 := by
    change assemblySize k delta = 18*sourceDegree delta+9*(2*k+1)+45
    rw [assemblySize_eq]
    ring
  have hD : D ≤ 180*M^2 := by omega
  have hD2 : D^2 ≤ 32400*M^4 := by
    calc
      D^2 ≤ (180*M^2)^2 := by gcongr
      _ = 32400*M^4 := by ring
  have hP : P ≤ 65341*M^5 := by
    calc
      P = (n+1)*(2*D^2+D+1)+2*D := rfl
      _ ≤ M*(2*(32400*M^4)+(180*M^2)+1)+2*(180*M^2) := by
        gcongr <;> assumption
      _ = 64800*M^5+180*M^3+M+360*M^2 := by ring
      _ ≤ 65341*M^5 := by omega
  have hwide : n+L+34 ≤ 43*M^2 := by omega
  have hboundary : L+61 ≤ 69*M^2 := by omega
  constructor
  · change 816*(k+1)^2+81*(d+1)^2+8*(d+1)+80*(L+1)^2+
      2*(n+1)*D^2*(n+L+34)+D*(L+61)+9*P+20*D^2+
      5*n^2+9*n+T+59 ≤ 5000000*M^7
    calc
      _ ≤ 816*M^2+81*(8*M^2)^2+8*(8*M^2)+80*(9*M^2)^2+
          2*M*(180*M^2)^2*(43*M^2)+(180*M^2)*(69*M^2)+
          9*(65341*M^5)+20*(180*M^2)^2+5*M^2+9*M+M+59 := by
        gcongr <;> assumption
      _ = 2786400*M^7+672084*M^4+588069*M^5+885*M^2+10*M+59 := by
        ring
      _ ≤ 4047507*M^7 := by omega
      _ ≤ 5000000*M^7 := by omega
  · calc
      14*(n+1)*D^2+4*D ≤ 14*M*(180*M^2)^2+4*(180*M^2) := by
        gcongr <;> assumption
      _ = 453600*M^5+720*M^2 := by ring
      _ ≤ 454320*M^5 := by omega
      _ ≤ 500000*M^5 := by omega

theorem allocatedSameRunPartialLedger : intendedAllocatedSameRunPartialLedger := by
  intro k n R epsilon hepsilon
  have envelope := allocatedBudgetEnvelope k n epsilon hepsilon
  have actual := produceExplicitStored_cost_counters k n R
    (sourceDelta k n epsilon)
  dsimp only at envelope actual ⊢
  exact ⟨actual.1.trans envelope.1,
    actual.2.1.trans envelope.2, actual.2.2.trans envelope.2⟩

#check HermiteAllocatedPolynomialCost.allocatedBudgetEnvelope
#print axioms HermiteAllocatedPolynomialCost.allocatedBudgetEnvelope
#check HermiteAllocatedPolynomialCost.allocatedSameRunPartialLedger
#print axioms HermiteAllocatedPolynomialCost.allocatedSameRunPartialLedger

end HermiteAllocatedPolynomialCost
