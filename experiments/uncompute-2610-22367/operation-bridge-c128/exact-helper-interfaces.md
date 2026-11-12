# Exact dependency definitions and full theorem signatures

Version C125.v1: additive supplement to the unchanged C117 design candidate.
This is an interface transcript, not an executable Lean module, placeholder,
proof, compiler result, prior review or acceptance. Definitions include their
complete literal bodies; theorem statements omit only `:= by` and proof bodies.
No declaration is asserted into a Lean environment by this document.

Original experimental source: `experiments/uncompute-2610-22367/temporary-and-c105/TemporaryAnd.lean`.
Original raw SHA256: `26d7ed676f345a671d020e76078b0b866ff4364ca1632698d22027d3a9695be4`.
Ambient input: `import QuantumBlockEncoding.PrimitiveMacros`, namespace
`ASPBE.Uncompute.MBU`, no section variables or other local imports.
Existing isolated module name: `TemporaryAnd`. There is no already-admitted
production import for this helper. Any later proof must stage this exact source
and compile/import it in an exclusive context, or separately admit it. Never
duplicate definitions or invent a production import to close that boundary.

## branchScale

```text
noncomputable def branchScale : ℂ := ((Real.sqrt 2 / 2 : ℝ) : ℂ)
```

## andBit

```text
def andBit (a b : Fin 2) : Fin 2 := if a = 1 ∧ b = 1 then 1 else 0
```

## conditionalCZSign

```text
def conditionalCZSign (m a b : Fin 2) : ℂ :=
  if m = 1 ∧ a = 1 ∧ b = 1 then -1 else 1
```

## correctedTemporaryAndBranch

```text
noncomputable def correctedTemporaryAndBranch {R : Type*}
    (alpha : R → Fin 2 → Fin 2 → ℂ) (m : Fin 2) (r : R) (a b t : Fin 2) : ℂ :=
  if t = 0 then conditionalCZSign m a b *
    QuantumBlockEncoding.hadamardMatrix m (andBit a b) * alpha r a b else 0
```

## correctedTemporaryAndBranch_eq

```text
theorem correctedTemporaryAndBranch_eq {R : Type*}
    (alpha : R → Fin 2 → Fin 2 → ℂ) (m : Fin 2) (r : R) (a b t : Fin 2) :
    correctedTemporaryAndBranch alpha m r a b t =
      branchScale * (if t = 0 then alpha r a b else 0)
```

## branchScale_normSq

```text
theorem branchScale_normSq : Complex.normSq branchScale = (1 / 2 : ℝ)
```

## inputMass

```text
noncomputable def inputMass {R : Type*} [Fintype R]
    (alpha : R → Fin 2 → Fin 2 → ℂ) : ℝ :=
  ∑ r, ∑ a, ∑ b, Complex.normSq (alpha r a b)
```

## branchMass

```text
noncomputable def branchMass {R : Type*} [Fintype R]
    (alpha : R → Fin 2 → Fin 2 → ℂ) (m : Fin 2) : ℝ :=
  ∑ r, ∑ a, ∑ b, ∑ t, Complex.normSq (correctedTemporaryAndBranch alpha m r a b t)
```

## correctedTemporaryAndBranch_mass

```text
theorem correctedTemporaryAndBranch_mass {R : Type*} [Fintype R]
    (alpha : R → Fin 2 → Fin 2 → ℂ) (m : Fin 2) :
    branchMass alpha m = inputMass alpha / 2
```

## outcomeMass_of_normalized

```text
theorem outcomeMass_of_normalized {R : Type*} [Fintype R]
    (alpha : R → Fin 2 → Fin 2 → ℂ) (h : inputMass alpha = 1) (m : Fin 2) :
    branchMass alpha m = (1 / 2 : ℝ)
```

## sum_branchMass

```text
theorem sum_branchMass {R : Type*} [Fintype R]
    (alpha : R → Fin 2 → Fin 2 → ℂ) :
    (∑ m : Fin 2, branchMass alpha m) = inputMass alpha
```
