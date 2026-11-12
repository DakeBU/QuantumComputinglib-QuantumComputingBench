import FirstSlice

open scoped ComplexOrder
open QuantumBlockEncoding.ConcreteSemantics

namespace QITFirstSlice.Tests

-- Carrier compatibility is definitional, not a copied matrix foundation.
example {d : Nat} (ψ : StateVector d ℂ) : FiniteMatrix d d ℂ :=
  Matrix.vecMulVec ψ (star ψ)

-- A genuinely complex normalized vector, with checked projector identity.
example :
    Matrix.vecMulVec (fun _ : Fin 1 => Complex.I) (star (fun _ : Fin 1 => Complex.I)) *
      Matrix.vecMulVec (fun _ : Fin 1 => Complex.I) (star (fun _ : Fin 1 => Complex.I)) =
    Matrix.vecMulVec (fun _ : Fin 1 => Complex.I) (star (fun _ : Fin 1 => Complex.I)) := by
  apply pureState_projector
  norm_num [dotProduct, Fin.sum_univ_succ]

-- Arbitrary dimension and basis index: a checked shared-backend instantiation.
example {d : Nat} (i : Fin d) :
    (Matrix.vecMulVec (basisKet d (α := ℂ) i)
      (star (basisKet d (α := ℂ) i))).PosSemidef ∧
    (Matrix.vecMulVec (basisKet d (α := ℂ) i)
      (star (basisKet d (α := ℂ) i))).trace = 1 := by
  apply pureState_density
  simp [basisKet, dotProduct_single]

-- An unnormalized vector must not satisfy the source normalization premise.
example : star (fun _ : Fin 1 => (2 : ℂ)) ⬝ᵥ (fun _ : Fin 1 => (2 : ℂ)) ≠ 1 := by
  norm_num [dotProduct, Fin.sum_univ_succ]

-- Empty-dimensional source normalization is impossible (no nonempty shortcut).
example (ψ : StateVector 0 ℂ) : star ψ ⬝ᵥ ψ ≠ 1 := by
  simp [dotProduct]

-- Complex coordinates distinguish ψψ† from the incorrectly swapped bra/ket.
example : Matrix.vecMulVec (fun i : Fin 2 => if i = 0 then 1 else Complex.I)
    (star (fun i : Fin 2 => if i = 0 then 1 else Complex.I)) 0 1 = -Complex.I := by
  simp [Matrix.vecMulVec]

#print axioms QITFirstSlice.pureState_density
#print axioms QITFirstSlice.pureState_projector
#check QITFirstSlice.pureState_density
#check QITFirstSlice.pureState_projector

end QITFirstSlice.Tests
