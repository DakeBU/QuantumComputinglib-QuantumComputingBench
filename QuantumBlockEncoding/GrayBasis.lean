import QuantumBlockEncoding.PrimitiveBasisLE

/-! Binary-reflected Gray order on little-endian primitive basis states.
The recursion for index `2*q+b` is `(b xor (q mod 2), Gray(q))`.
The equivalence and single-wire adjacency are proved for arbitrary width. -/

namespace QuantumBlockEncoding.GrayBasis

def twist (n : ℕ) : Equiv.Perm (Fin (2 ^ n) × Fin 2) where
  toFun pair := (pair.1, if pair.1.val % 2 = 0 then pair.2 else flipBit pair.2)
  invFun pair := (pair.1, if pair.1.val % 2 = 0 then pair.2 else flipBit pair.2)
  left_inv pair := by by_cases h : pair.1.val % 2 = 0 <;> simp [h]
  right_inv pair := by by_cases h : pair.1.val % 2 = 0 <;> simp [h]

def equiv : (n : ℕ) → Fin (2 ^ n) ≃ PrimitiveBasis n
  | 0 => (primitiveBasisLEEquiv 0).symm
  | n + 1 =>
      (finCongr (pow_succ 2 n)).trans finProdFinEquiv.symm
        |>.trans (twist n)
        |>.trans (Equiv.prodCongr (equiv n) (Equiv.refl (Fin 2)))
        |>.trans (Equiv.prodComm _ _)
        |>.trans (Fin.consEquiv (fun _ : Fin (n + 1) => Fin 2))

def headBit (index : ℕ) : Fin 2 :=
  if (index / 2) % 2 = 0 then ⟨index % 2, by omega⟩
  else flipBit ⟨index % 2, by omega⟩

@[simp] theorem equiv_head (n : ℕ) (index : Fin (2 ^ (n + 1))) :
    equiv (n + 1) index 0 = headBit index.val := rfl

@[simp] theorem equiv_tail (n : ℕ) (index : Fin (2 ^ (n + 1))) (wire : Fin n) :
    equiv (n + 1) index wire.succ =
      equiv n ⟨index.val / 2, by
        have bound : index.val < 2 ^ n * 2 := by simpa only [pow_succ] using index.isLt
        omega⟩ wire := rfl

theorem headBit_even (index : ℕ) (even : index % 2 = 0) :
    headBit (index + 1) = flipBit (headBit index) := by
  have quotient : (index + 1) / 2 = index / 2 := by omega
  have remainder : (index + 1) % 2 = 1 := by omega
  by_cases parity : (index / 2) % 2 = 0 <;>
    simp [headBit, quotient, remainder, even, parity, flipBit]

theorem headBit_odd (index : ℕ) (odd : index % 2 = 1) :
    headBit (index + 1) = headBit index := by
  have quotient : (index + 1) / 2 = index / 2 + 1 := by omega
  have remainder : (index + 1) % 2 = 0 := by omega
  by_cases parity : (index / 2) % 2 = 0
  · have next : (index / 2 + 1) % 2 = 1 := by omega
    simp [headBit, quotient, remainder, odd, parity, next, flipBit]
  · have next : (index / 2 + 1) % 2 = 0 := by omega
    simp [headBit, quotient, remainder, odd, parity, next, flipBit]

/-- Numerically adjacent Gray labels differ by exactly one physical X action. -/
theorem adjacent {n : ℕ} (first second : Fin (2 ^ n))
    (next : first.val + 1 = second.val) :
    ∃ target : Fin n, equiv n second = xBasisAction target (equiv n first) := by
  induction n with
  | zero =>
      have h1 := first.isLt
      have h2 := second.isLt
      simp only [pow_zero] at h1 h2
      omega
  | succ n ih =>
      let firstTail : Fin (2 ^ n) := ⟨first.val / 2, by
        have bound : first.val < 2 ^ n * 2 := by simpa only [pow_succ] using first.isLt
        omega⟩
      let secondTail : Fin (2 ^ n) := ⟨second.val / 2, by
        have bound : second.val < 2 ^ n * 2 := by simpa only [pow_succ] using second.isLt
        omega⟩
      by_cases even : first.val % 2 = 0
      · have tailEq : secondTail = firstTail := by
          apply Fin.ext
          dsimp [firstTail, secondTail]
          omega
        refine ⟨0, ?_⟩
        funext wire
        refine Fin.cases ?_ (fun rest => ?_) wire
        · simpa [xBasisAction, equiv_head, ← next] using headBit_even first.val even
        · change equiv n secondTail rest =
            (Function.update (equiv (n + 1) first) 0 (flipBit (equiv (n + 1) first 0))) rest.succ
          simp [tailEq, firstTail]
      · have odd : first.val % 2 = 1 := by omega
        have tailNext : firstTail.val + 1 = secondTail.val := by
          dsimp [firstTail, secondTail]
          omega
        obtain ⟨target, action⟩ := ih firstTail secondTail tailNext
        refine ⟨target.succ, ?_⟩
        have targetSuccNeZero : target.succ ≠ (0 : Fin (n + 1)) := by simp
        funext wire
        refine Fin.cases ?_ (fun rest => ?_) wire
        · simpa [xBasisAction, Function.update_apply, equiv_head, ← next,
            targetSuccNeZero, Ne.symm targetSuccNeZero] using
            headBit_odd first.val odd
        · have entry := congrFun action rest
          simpa [xBasisAction, Function.update_apply, equiv_tail,
            firstTail, secondTail] using entry

end QuantumBlockEncoding.GrayBasis
