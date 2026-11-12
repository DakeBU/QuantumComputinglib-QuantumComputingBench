import QuantumBlockEncoding.ConcreteSemantics
import Mathlib.Analysis.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.Trace

/-!
Experimental forward pure-state interface for Leditzky's 10 April 2026 notes,
Definition 2.1, Eq. (2.4), and the pure-state paragraph on printed page 4.
This is not the rank-one/extreme-point characterization or a production claim.
See statement-seal.md for the pre-proof exact contract and binder audit.
-/

open scoped ComplexOrder
open QuantumBlockEncoding.ConcreteSemantics

namespace QITFirstSlice

theorem pureState_density {d : Nat}
    (ψ : QuantumBlockEncoding.ConcreteSemantics.StateVector d ℂ)
    (hnorm : star ψ ⬝ᵥ ψ = 1) :
    (Matrix.vecMulVec ψ (star ψ)).PosSemidef ∧
      (Matrix.vecMulVec ψ (star ψ)).trace = 1 := by
  refine ⟨Matrix.posSemidef_vecMulVec_self_star ψ, ?_⟩
  rw [Matrix.trace_vecMulVec, dotProduct_comm]
  exact hnorm

theorem pureState_projector {d : Nat}
    (ψ : QuantumBlockEncoding.ConcreteSemantics.StateVector d ℂ)
    (hnorm : star ψ ⬝ᵥ ψ = 1) :
    Matrix.vecMulVec ψ (star ψ) * Matrix.vecMulVec ψ (star ψ) =
      Matrix.vecMulVec ψ (star ψ) := by
  rw [Matrix.vecMulVec_mul_vecMulVec, hnorm, one_smul]

end QITFirstSlice
