import Hddivsteps590.Recovery

namespace ASPBE.Uncompute

open Hddivsteps

/-- Mathematical decoder on unrestricted integer tuples. Correctness is only
asserted on the proved reachable active domain; no finite-bit cost is claimed. -/
noncomputable def recoverStepBits (p : Int) (u : ZState) : Int × Int :=
  (if u.fv % 4 = 2 then 1 else 0,
    if u.fv % 4 = 2 then 1 else
    if u.g = 0 then 1 else
    if 1 ≤ u.z then 0 else
      let j := padicValInt 2 u.fv
      let q := u.fv / 2 ^ j
      bitk (((p : ZMod (2 ^ j)) *
        ((u.f * q : Int) : ZMod (2 ^ j))⁻¹).val : Int) (j - 1))

private theorem recoverStepBits_of_inv {p : Int} {s : ZState}
    (hp : p % 2 = 1) (h : Inv p s) (hactive : s.g ≠ 0) :
    recoverStepBits p (zStep s) =
      ((if 0 ≤ s.z ∧ s.g % 2 = 1 then 1 else 0), s.g % 2) := by
  have hiff := (sigma_class h hp).1
  change (0 ≤ s.z ∧ s.g % 2 = 1) ↔ (zStep s).fv % 4 = 2 % 4 at hiff
  norm_num at hiff
  by_cases hswap : 0 ≤ s.z ∧ s.g % 2 = 1
  · have hvisible := hiff.mp hswap
    simp only [recoverStepBits, if_pos hvisible, if_pos hswap]
    exact congrArg (fun b : Int => ((1 : Int), b)) hswap.2.symm
  · have hvisible : ¬ (zStep s).fv % 4 = 2 := fun hfv => hswap (hiff.mpr hfv)
    by_cases hzero : (zStep s).g = 0
    · have hb : s.g % 2 = 1 :=
        (bbit_of_nonswap hswap).symm.trans (bbit_of_freeze h.fodd hactive hzero)
      simp only [recoverStepBits, if_neg hvisible, if_pos hzero, if_neg hswap]
      exact congrArg (fun b : Int => ((0 : Int), b)) hb.symm
    · by_cases hramp : 1 ≤ (zStep s).z
      · have hb : s.g % 2 = 0 :=
          (bbit_of_nonswap hswap).symm.trans (bbit_of_ramp hswap hramp)
        simp only [recoverStepBits, if_neg hvisible, if_neg hzero, if_pos hramp,
          if_neg hswap]
        exact congrArg (fun b : Int => ((0 : Int), b)) hb.symm
      · have hcounter : (zStep s).z = s.z + 1 := by
          rw [zStep_nonswap hswap]
        have hz : s.z < 0 := by omega
        have hb := (bbit_of_nonswap hswap).symm.trans
          (ladder_det h hp hz rfl rfl)
        simp only [recoverStepBits, if_neg hvisible, if_neg hzero, if_neg hramp,
          if_neg hswap]
        exact congrArg (fun b : Int => ((0 : Int), b)) hb.symm

theorem recover_zWalk_active (p x : Int) (hp : p % 2 = 1) (t : Nat)
    (hactive : (Hddivsteps.zWalk p x t).g ≠ 0) :
    recoverStepBits p (Hddivsteps.zWalk p x (t + 1)) =
      ((if 0 ≤ (Hddivsteps.zWalk p x t).z ∧
          (Hddivsteps.zWalk p x t).g % 2 = 1 then 1 else 0),
        (Hddivsteps.zWalk p x t).g % 2) := by
  have hstep : zWalk p x (t + 1) = zStep (zWalk p x t) := by
    rw [zWalk_succ, if_neg hactive]
  rw [hstep]
  exact recoverStepBits_of_inv hp (invariant_zWalk hp x t) hactive

end ASPBE.Uncompute

#check ASPBE.Uncompute.recover_zWalk_active
#print axioms ASPBE.Uncompute.recover_zWalk_active
