# C399 measurement-completeness canonical-node seal

Sealed before local proof implementation, 2026-10-23. Declaration class B:
canonical library nodes, not an entire textbook/paper Source Anchor.

Root: for a finite family of bounded operators between complex Hilbert spaces,
the actual completeness equation sum(M_i^* M_i)=id preserves total squared norm.
For a norm-one input, every squared output norm lies in [0,1]. No state wrapper,
density operator, instrument or quantum-system type is introduced.

Upstream source correspondence: Axiomatic-AI/AxQM, independent commit
2ccf167efca86eb5164f1df8cedb72b84626b479, AxQM/Basic/Measurement.lean,
Git blob 1a078f8cd71d6b41c3e87bb70c763c3a2a628aa0. The source's Measurement.op
and complete fields specify finite endomorphisms with sum adjoint-comp = 1.
Its bornProb and sum_bornProb_eq_one concern density states. This batch proves
the pure-vector operator substrate, generalized to rectangular E -> F; it does
NOT establish a density/trace adapter, full Measurement equivalence, an upstream
build, or any private AxQM task solution. Existing upstream proofs are not used.
Nielsen-Chuang section 2.2.3 is an upstream citation, not a claim of fresh
inspection or redistribution of the book. Authors Winston Yin/Frank Koppens and
Axiomatic AI are attributed; upstream Apache-2.0/NOTICE boundaries remain.

Reuse audit: current main 8d7ba4cd5b786706796df15777bcb5a5403723d0 and current
Lean4.33 contribution ea0d8727f9d225f5af52e4bd5b62d02fe5d35cde have no Kraus,
POVM, density or measurement-completeness implementation in QuantumBlockEncoding.
The unmerged contrib/effect-probability-stability branch already owns distinct
effect/Born stability results; do not recreate those. Mathlib's existing
ContinuousLinearMap.adjoint, comp, sum application, inner-product sums and
apply_norm_sq_eq_inner_adjoint_left supply this proof. Searches of the relevant
Mathlib InnerProductSpace/CStarAlgebra directories found no exact finite-family
completeness-to-squared-norm-sum theorem. This is bounded retrieval, not a
whole-ecosystem nonexistence or novelty claim. Existing external library cards
remain candidates, not imported proof dependencies.

Semantic slots: complex scalar; finite outcome carrier, possibly empty;
arbitrary Hilbert input/output spaces, including zero space. Completeness is a
SOURCE mathematical premise; norm-one is SOURCE only on the probability bound.
CompleteSpace/inner-product structures are TYPING/generalization conditions.
No norm bound, already-normalized output, positivity of every effect, nonzero
branch or hidden existence premise is added. No choice/quotient definitions.
All phases and operators remain literal; no tensor/register reordering is done.
No post-measurement normalized state, cleanup, instrument, circuit, resource,
oracle, physical implementation or finite-bit theorem is asserted.

Source construction inventory: operator family and completeness -> NODE;
adjoint identity -> Mathlib dependency; finite linearity/sum -> dependency;
squared norm mass identity -> local root; nonnegative summands -> per-outcome
bound. Mixed-state Born trace, postMeasurement, orthonormal-basis construction,
POVM packaging and all textbook exercises -> EXCLUDED from this batch, retained
as future obligations rather than implicitly proved nodes.

## Frozen formal context and two signatures

```lean
import Mathlib.Analysis.InnerProductSpace.Adjoint
namespace QuantumBlockEncoding.MeasurementProbability
open scoped InnerProductSpace
variable {ι E F : Type*} [Fintype ι]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

theorem sum_norm_sq_eq (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ : E) :
    ∑ i, ‖M i ψ‖ ^ 2 = ‖ψ‖ ^ 2

theorem outcome_probability_mem_Icc (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ : E)
    (hψ : ‖ψ‖ = 1) (i : ι) : ‖M i ψ‖ ^ 2 ∈ Set.Icc (0 : ℝ) 1
end QuantumBlockEncoding.MeasurementProbability
```

Acceptance: actual Lean4.33 focused own-output and consumer compilation;
ordinary-three-axiom checks; actual wrong-target and sorry negative controls;
independent source-blind decoder and separate semantic comparison; whole-module
publication binding and normal full integration gates before main admission.
QA remains an unadmitted proposal until the canonical graph snapshot is refreshed
and its content/split reviewed. No frozen core or question is overwritten.
