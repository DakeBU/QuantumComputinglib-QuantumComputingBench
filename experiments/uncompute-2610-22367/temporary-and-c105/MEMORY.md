# Candidate technical memory: temporary-AND MBU

Evidence class: isolated Lean 4.33 `proved_locally`; NOT an admitted reusable
library node yet. Source: arXiv:2610.22367v1 Methods Eq. (12), attributed there
to Gidney's 2018 temporary-AND technique. No novelty or Gaussian closure claim.

Purpose: remove a CURRENT computed-AND ancilla by destructive X measurement,
reset and outcome-conditioned CZ without data-dependent residual phase.

Local candidate import: `TemporaryAnd` from this package's isolated output,
after compiling its exact source in the project context. Do not assume a
production import exists. Main roots:

```lean
theorem correctedTemporaryAndBranch_eq {R : Type*}
    (alpha : R → Fin 2 → Fin 2 → ℂ) (m : Fin 2) (r : R) (a b t : Fin 2) :
    correctedTemporaryAndBranch alpha m r a b t =
      branchScale * (if t = 0 then alpha r a b else 0)

theorem correctedTemporaryAndBranch_mass {R : Type*} [Fintype R]
    (alpha : R → Fin 2 → Fin 2 → ℂ) (m : Fin 2) :
    branchMass alpha m = inputMass alpha / 2
```

Both names live in `ASPBE.Uncompute.MBU`. `alpha` can include arbitrary
reference correlations. No normalization premise is needed until the
probability corollary. The actual current types, source hashes and axiom output
are in `compile-observations.json`; finite Python regressions are separate.

Known invalid substitutions: measuring a different/modified Boolean function;
changing retained controls without reestablishing the current-AND relation;
omitting conditional CZ; silently dropping the unnormalized branch factor;
claiming uniform numerical error or a circuit cost from this amplitude lemma.

Potential consumer: `BE.QueryModel.ValueToAmplitude` cleanup obligation.
Required before promotion: independent source-blind decode and source-first
review, raw/provider binding, actual gadget/instrument adapter, and applicable
integration/reader gates. Gaussian's whole modified coefficient needs its own
live-function and all-record correction theorem; this is not that theorem.
