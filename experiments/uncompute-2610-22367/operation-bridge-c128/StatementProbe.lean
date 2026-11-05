import TemporaryAnd

/-! Untracked interface-only probe. There are no new theorem proofs here.
The expressions checked below are propositions, not accepted certificates. -/
namespace ASPBE.Uncompute.MBU.OperationBridge

abbrev DataBasis := QuantumBlockEncoding.PrimitiveBasis 2
abbrev WorkBasis := QuantumBlockEncoding.PrimitiveBasis 3

noncomputable def ccx3Program : QuantumBlockEncoding.PrimitiveProgram 3 :=
  QuantumBlockEncoding.primitiveCCXProgram (0 : Fin 3) (1 : Fin 3) (2 : Fin 3)
    (by decide) (by decide) (by decide)

noncomputable def zeroInsert : _root_.Matrix WorkBasis DataBasis ℂ :=
  fun x y => if x 0 = y 0 ∧ x 1 = y 1 ∧ x 2 = 0 then 1 else 0

noncomputable def xBra (m : Fin 2) : _root_.Matrix DataBasis WorkBasis ℂ :=
  fun y x => if x 0 = y 0 ∧ x 1 = y 1 then
    QuantumBlockEncoding.hadamardMatrix m (x 2) else 0

noncomputable def conditionalCZ (m : Fin 2) : _root_.Matrix DataBasis DataBasis ℂ :=
  QuantumBlockEncoding.phasePermutationMatrix
    (fun y => conditionalCZSign m (y 0) (y 1)) (Equiv.refl DataBasis)

#check (∀ m : Fin 2,
  zeroInsert * conditionalCZ m * xBra m *
    QuantumBlockEncoding.evalPrimitiveProgram ccx3Program * zeroInsert =
  branchScale • zeroInsert)

#check (zeroInsert.conjTranspose * zeroInsert =
  (1 : _root_.Matrix DataBasis DataBasis ℂ))

#check (∀ m : Fin 2, (conditionalCZ m).conjTranspose * conditionalCZ m =
  (1 : _root_.Matrix DataBasis DataBasis ℂ))

#check ((∑ m : Fin 2, (xBra m).conjTranspose * xBra m) =
  (1 : _root_.Matrix WorkBasis WorkBasis ℂ))

#check (∀ {R : Type} (alpha : R → Fin 2 → Fin 2 → ℂ) (r : R) (x : WorkBasis),
  ((_root_.Matrix.mulVec
    (QuantumBlockEncoding.evalPrimitiveProgram ccx3Program * zeroInsert)
    (fun y : DataBasis => alpha r (y 0) (y 1))) x) =
  if x 2 = andBit (x 0) (x 1) then alpha r (x 0) (x 1) else 0)

#check (∀ {R : Type} (alpha : R → Fin 2 → Fin 2 → ℂ)
    (m : Fin 2) (r : R) (x : WorkBasis),
  ((_root_.Matrix.mulVec
    (zeroInsert * conditionalCZ m * xBra m *
      QuantumBlockEncoding.evalPrimitiveProgram ccx3Program * zeroInsert)
    (fun y : DataBasis => alpha r (y 0) (y 1))) x) =
  correctedTemporaryAndBranch alpha m r (x 0) (x 1) (x 2))

#check (∀ {R : Type} [Fintype R] (alpha : R → Fin 2 → Fin 2 → ℂ) (m : Fin 2),
  (∑ r : R, ∑ x : WorkBasis,
    Complex.normSq
      ((_root_.Matrix.mulVec
        (zeroInsert * conditionalCZ m * xBra m *
          QuantumBlockEncoding.evalPrimitiveProgram ccx3Program * zeroInsert)
        (fun y : DataBasis => alpha r (y 0) (y 1))) x)) = inputMass alpha / 2)

end ASPBE.Uncompute.MBU.OperationBridge
