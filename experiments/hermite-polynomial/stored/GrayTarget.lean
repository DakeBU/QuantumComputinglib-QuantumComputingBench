import QuantumBlockEncoding.GrayGivensCompiler
import QuantumBlockEncoding.StoredSelectedRyTrace

/-! A staged, explicit producer for the physical target of a Gray-adjacent
elimination record. Integer counters describe the actual recursion, not a
finite-bit runtime or a complete circuit compiler. -/
namespace QuantumBlockEncoding.HermiteGrayTargetCandidate
open StoredGivens

structure Discovery (n : ℕ) where
  target : Fin n
  quotients : ℕ
  remainders : ℕ
  comparisons : ℕ

def discover : (n : ℕ) → (first second : Fin (2 ^ n)) →
    first.val + 1 = second.val → Discovery n
  | 0, first, second, _ => by
      have a := first.isLt
      have b := second.isLt
      simp only [pow_zero] at a b
      omega
  | n + 1, first, second, next =>
      let remainder := first.val % 2
      if even : remainder = 0 then
        ⟨0, 0, 1, 1⟩
      else
        let firstTail : Fin (2 ^ n) := ⟨first.val / 2, by
          have bound : first.val < 2 ^ n * 2 := by
            simpa only [pow_succ] using first.isLt
          omega⟩
        let secondTail : Fin (2 ^ n) := ⟨second.val / 2, by
          have bound : second.val < 2 ^ n * 2 := by
            simpa only [pow_succ] using second.isLt
          omega⟩
        let result := discover n firstTail secondTail (by
          dsimp [firstTail, secondTail]
          change first.val % 2 ≠ 0 at even
          omega)
        ⟨result.target.succ, result.quotients + 2,
          result.remainders + 1, result.comparisons + 1⟩

theorem discover_action (n : ℕ) (first second : Fin (2 ^ n))
    (next : first.val + 1 = second.val) :
    GrayBasis.equiv n second =
      xBasisAction (discover n first second next).target (GrayBasis.equiv n first) := by
  induction n with
  | zero =>
      have a := first.isLt
      have b := second.isLt
      simp only [pow_zero] at a b
      omega
  | succ n ih =>
      let firstTail : Fin (2 ^ n) := ⟨first.val / 2, by
        have bound : first.val < 2 ^ n * 2 := by simpa only [pow_succ] using first.isLt
        omega⟩
      let secondTail : Fin (2 ^ n) := ⟨second.val / 2, by
        have bound : second.val < 2 ^ n * 2 := by simpa only [pow_succ] using second.isLt
        omega⟩
      by_cases even : first.val % 2 = 0
      · have tails : secondTail = firstTail := by
          apply Fin.ext
          dsimp [firstTail, secondTail]
          omega
        have target : (discover (n+1) first second next).target = 0 := by
          simp [discover, even]
        rw [target]
        funext wire
        refine Fin.cases ?_ (fun rest => ?_) wire
        · simpa [xBasisAction, GrayBasis.equiv_head, ← next] using
            GrayBasis.headBit_even first.val even
        · change GrayBasis.equiv n secondTail rest =
            (Function.update (GrayBasis.equiv (n+1) first) 0
              (flipBit (GrayBasis.equiv (n+1) first 0))) rest.succ
          simp [tails, firstTail]
      · have odd : first.val % 2 = 1 := by omega
        have tailNext : firstTail.val + 1 = secondTail.val := by
          dsimp [firstTail, secondTail]
          omega
        let result := discover n firstTail secondTail tailNext
        have target : (discover (n+1) first second next).target = result.target.succ := by
          simp [discover, even, result, firstTail, secondTail]
        have action := ih firstTail secondTail tailNext
        rw [target]
        have nz : result.target.succ ≠ (0 : Fin (n+1)) := by simp
        funext wire
        refine Fin.cases ?_ (fun rest => ?_) wire
        · simpa [xBasisAction, Function.update_apply, GrayBasis.equiv_head, ← next,
            nz, Ne.symm nz] using GrayBasis.headBit_odd first.val odd
        · have entry := congrFun action rest
          simpa [xBasisAction, Function.update_apply, GrayBasis.equiv_tail,
            firstTail, secondTail, result] using entry

theorem discover_cost (n : ℕ) (first second : Fin (2 ^ n))
    (next : first.val + 1 = second.val) :
    (discover n first second next).quotients ≤ 2*n ∧
    (discover n first second next).remainders ≤ n ∧
    (discover n first second next).comparisons ≤ n := by
  induction n with
  | zero =>
      have a := first.isLt
      have b := second.isLt
      simp only [pow_zero] at a b
      omega
  | succ n ih =>
      by_cases even : first.val % 2 = 0
      · simp [discover, even]
      · simp only [discover, even, ↓reduceDIte]
        have bound := ih
          ⟨first.val / 2, by
            have h : first.val < 2 ^ n * 2 := by simpa only [pow_succ] using first.isLt
            omega⟩
          ⟨second.val / 2, by
            have h : second.val < 2 ^ n * 2 := by simpa only [pow_succ] using second.isLt
            omega⟩
          (by dsimp; omega)
        omega

theorem target_unique {n : ℕ} (bits : PrimitiveBasis n) (a b : Fin n)
    (equal : xBasisAction a bits = xBasisAction b bits) : a = b := by
  by_contra different
  have entry := congrFun equal a
  have flipped : flipBit (bits a) = bits a := by
    simpa [xBasisAction, Function.update_apply, different, Ne.symm different] using entry
  have impossible : ∀ bit : Fin 2, flipBit bit ≠ bit := by
    intro bit
    fin_cases bit <;> decide
  exact impossible (bits a) flipped

/-- The new producer returns the same unique physical target as the existing
compiler, not a target for an unrelated equivalent plane. -/
theorem discover_step_target {q : ℕ} (step : AdjacentGivens.Step (2^(q+1))) :
    (discover (q+1) step.first step.second step.adjacent).target =
      GrayGivensCompiler.stepTarget step := by
  apply target_unique (GrayBasis.equiv (q+1) step.first)
  exact (discover_action (q+1) step.first step.second step.adjacent).symm.trans
    (GrayGivensCompiler.stepTarget_action step)

/-- Integer quotient/modulo/bit arithmetic is locally charged in `field`,
not claimed to be a real-field computation or bounded-bit instruction. -/
def head (index : ℕ) : Run (Fin 2) := do
  let quotient ← charge .field (index / 2)
  let parity ← charge .field (quotient % 2)
  let low ← charge .field (⟨index % 2, by omega⟩ : Fin 2)
  let even ← charge .compare (decide (parity = 0))
  if even then pure low else charge .field (flipBit low)

theorem head_value (index : ℕ) : (head index).value = GrayBasis.headBit index := by
  by_cases parity : index / 2 % 2 = 0
  all_goals simp [head, bind, pure, Run.bind, Run.pure, charge, GrayBasis.headBit, parity]

def bit : (n : ℕ) → Fin (2^n) → Fin n → Run (Fin 2)
  | 0, _, wire => Fin.elim0 wire
  | n+1, index, wire => Fin.cases (head index.val)
      (fun rest => do
        let tail ← charge .field (⟨index.val / 2, by
          have bound : index.val < 2^n * 2 := by simpa only [pow_succ] using index.isLt
          omega⟩ : Fin (2^n))
        bit n tail rest) wire

theorem bit_value (n : ℕ) (index : Fin (2^n)) (wire : Fin n) :
    (bit n index wire).value = GrayBasis.equiv n index wire := by
  induction n with
  | zero => exact Fin.elim0 wire
  | succ n ih =>
      refine Fin.cases ?_ (fun rest => ?_) wire
      · simpa [bit] using head_value index.val
      · simp only [bit, Fin.cases_succ, bind, Run.bind, charge]
        exact ih _ rest

theorem tick_le_one (chosen op : Op) : tick chosen op ≤ 1 := by
  dsimp [tick]
  split_ifs <;> omega

theorem head_cost_le (index : ℕ) (op : Op) : (head index).cost op ≤ 5 := by
  simp only [head, bind, pure, Run.bind, Run.pure, charge]
  by_cases parity : index / 2 % 2 = 0
  all_goals simp [parity]
  all_goals have hf := tick_le_one .field op
  all_goals have hc := tick_le_one .compare op
  all_goals omega

theorem bit_cost_le (n : ℕ) (index : Fin (2^n)) (wire : Fin n) (op : Op) :
    (bit n index wire).cost op ≤ n+5 := by
  induction n with
  | zero => exact Fin.elim0 wire
  | succ n ih =>
      refine Fin.cases ?_ (fun rest => ?_) wire
      · have bound := head_cost_le index.val op
        simpa only [bit, Fin.cases_zero] using bound.trans (by omega)
      · simp only [bit, Fin.cases_succ, bind, Run.bind, charge, Pi.add_apply]
        have bound := ih
          ⟨index.val / 2, by
            have h : index.val < 2^n * 2 := by simpa only [pow_succ] using index.isLt
            omega⟩ rest
        have tick := tick_le_one .field op
        omega

def word (n : ℕ) (index : Fin (2^n)) : Run (Vector (Fin 2) n) :=
  collect (bit n index)

theorem word_value (n : ℕ) (index : Fin (2^n)) (wire : Fin n) :
    (word n index).value[wire.val] = GrayBasis.equiv n index wire := by
  simp [word, bit_value]

theorem word_cost_le (n : ℕ) (index : Fin (2^n)) (op : Op) :
    (word n index).cost op ≤ n*(n+9) := by
  simp only [word, collect_cost]
  have sum := Finset.sum_le_sum (fun wire (_ : wire ∈ Finset.univ) =>
    bit_cost_le n index wire op)
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, smul_eq_mul] at sum
  have hr := tick_le_one .read op
  have hw := tick_le_one .write op
  nlinarith

theorem word_total_cost_le (n : ℕ) (index : Fin (2^n)) :
    StoredRectangularGivens.total (word n index).cost ≤ 8*n*(n+9) := by
  have a := word_cost_le n index .field
  have b := word_cost_le n index .sqrt
  have c := word_cost_le n index .angle
  have d := word_cost_le n index .trig
  have e := word_cost_le n index .compare
  have f := word_cost_le n index .read
  have g := word_cost_le n index .write
  have h := word_cost_le n index .emit
  dsimp [StoredRectangularGivens.total]
  nlinarith

example : (discover 3 (0 : Fin 8) 1 rfl).target = 0 := by native_decide
example : (discover 3 (1 : Fin 8) 2 rfl).target = 1 := by native_decide
example : (discover 3 (3 : Fin 8) 4 rfl).target = 2 := by native_decide
example : (word 3 (3 : Fin 8)).value = #v[0,1,0] := by native_decide
example : (word 3 (4 : Fin 8)).value = #v[0,1,1] := by native_decide
example : (word 0 (0 : Fin 1)).value = #v[] := by native_decide
example (first second : Fin (2^0)) : first.val+1 ≠ second.val := by
  have a := first.isLt
  have b := second.isLt
  simp only [pow_zero] at a b
  omega

#print axioms discover_action
#print axioms discover_cost
#print axioms discover_step_target
#print axioms word_value
#print axioms word_total_cost_le
end QuantumBlockEncoding.HermiteGrayTargetCandidate
