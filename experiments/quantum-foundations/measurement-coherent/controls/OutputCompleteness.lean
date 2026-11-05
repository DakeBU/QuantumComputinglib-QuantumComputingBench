import QuantumBlockEncoding.MeasurementCoherent

-- Deliberately ill-typed orientation control; not a library declaration.
example {ι E F : Type*} [Fintype ι]
    [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
    [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]
    (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).comp (M i).adjoint = 1) :
    E →ₗᵢ[ℂ] PiLp 2 (fun _ : ι => F) :=
  QuantumBlockEncoding.MeasurementCoherent.branchIsometry M hM
