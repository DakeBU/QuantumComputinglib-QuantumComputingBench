# Statement Seal v1: normalized pure-state projector

State: STATEMENT_SEALED; independent source-topology review pending. This is
an experiment, not an admitted production module or a chapter-completion record.
Seal written before proof implementation on 2026-10-08.

Primary source: `leditzky-2025-repth-qit`, Felix Leditzky, lecture notes,
[10 April 2026 edition](https://www.felixleditzky.info/teaching/FT25/math595-repth-qit.pdf).
PDF SHA256: `90784b02b568b8c7bb6a1ec20588d801541d047779333bd2b2b8e63749dc0fe3`;
554175 bytes, 79 pages. Downloaded and checked 2026-10-08. Printed pages 3 and
4 equal PDF pages 3 and 4 (one-based). Both complete pages rendered and viewed.

Bounded anchor: Definition 2.1 (positivity, trace normalization), Eq. (2.4)
(conjugate-linear first argument), and the pure-state paragraph on printed p.4
before Definition 2.3. The delta certifies the forward assertion: a normalized
vector gives a positive trace-one projector. It does not prove the extremal
point/rank-one characterization, its converse, or any later theorem.

## Exact public signatures

Namespace `QITFirstSlice`; imports provide shared `StateVector` and `FiniteMatrix`.
`P` below is exposition only, not a new definition: `Matrix.vecMulVec ψ (star ψ)`.

```lean
theorem pureState_density {d : Nat}
    (ψ : QuantumBlockEncoding.ConcreteSemantics.StateVector d ℂ)
    (hnorm : star ψ ⬝ᵥ ψ = 1) :
    (Matrix.vecMulVec ψ (star ψ)).PosSemidef ∧
      (Matrix.vecMulVec ψ (star ψ)).trace = 1

theorem pureState_projector {d : Nat}
    (ψ : QuantumBlockEncoding.ConcreteSemantics.StateVector d ℂ)
    (hnorm : star ψ ⬝ᵥ ψ = 1) :
    Matrix.vecMulVec ψ (star ψ) * Matrix.vecMulVec ψ (star ψ) =
      Matrix.vecMulVec ψ (star ψ)
```

## Binder and definition audit

- `d : Nat`: TYPING, finite dimension. No nonempty carrier premise needed;
  when d=0, source normalization is impossible, not given fallback semantics.
- `ψ : StateVector d ℂ`: SOURCE vector, carrier abbreviation expands literally
  to `Fin d → ℂ`; complex field and standard basis are STANDING (p.3).
- `hnorm`: SOURCE, the p.4 unit-vector condition, expanded without a project
  normalization bundle as `∑ i, conj(ψ i) * ψ i = 1`.
- `Matrix.PosSemidef`: reused Mathlib predicate, expanding to Hermitian plus
  nonnegative quadratic form; ComplexOrder is the real-axis order on complex
  values. Hermitian positivity is source-implicit, not an added theorem binder.
- `Matrix.trace`: reused finite diagonal sum. `vecMulVec` entry is literally
  `ψ i * conj(ψ j)`, with no choice, quotient or default behavior.
- No EXCESS, RULED or opaque project-owned Prop/structure input.

No subsystem split/reordering, oracle, circuit, ancilla, error tolerance,
postselection or cost claim is involved. Coordinates use the shared backend;
global phase is not quotiented, and quotient equivalence is not claimed.
Exact ideal finite complex linear algebra, not synthesis/resource certification.

The seal's SHA256 binds the exact signature text above before proof search.
A separate whole-module SHA256 will bind completed proof implementation;
signature and module bindings are distinct. The signature text above remains
unchanged during proof implementation.
