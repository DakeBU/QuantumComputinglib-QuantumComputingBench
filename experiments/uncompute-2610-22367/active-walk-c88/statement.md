# C88: active-walk branch-recovery composition

Status: STATEMENT_SEALED_TEXT, before proof search; not elaborated, not proved,
not independently source-reviewed, not a circuit/resource certificate.

Source: arXiv:2610.22367v1, Appendix A, A.4-A.6 and the all-active branch
partition. Author implementation substrate: andigu/uncompute commit
64b5a13aa249f1360846657392e6c66817b26d0f, Recovery.lean. This is a proposed
ASPBE composition of existing author lemmas, not original discovery of the
branch-recovery method. The source graph node is `allactive` and its complete
partition dependencies; the decoder is not supplied as a theorem hypothesis.

## Mathematical contract

Let p be any odd integer, x any integer and t a natural scheduled walk index.
Let s=zWalk(p,x,t), and assume s.g is nonzero. The walk's own initialization and
preservation lemmas supply every invariant field. From only p and the actual
successor zWalk(p,x,t+1), return the swap bit and incoming parity g mod 2.

The source assumes p>0 and 0<=x<p. This composition aims to prove a larger
domain, using the actual author substrate; restricting it to the source locus
does not require a new premise. All integers are unbounded mathematical
integers. No word width, arithmetic circuit, phase, coherent extension,
ancilla, stopping bound or resource guarantee is asserted.

The decoder first tests F' mod4=2. If true return (1,1). Otherwise its first
output is0; its second output is1 if g'=0, is0 if z'>=1, and otherwise is the
determinant-ladder bit using j=v2(F'), q=F'/2^j and the canonical residue of
p*(f'*q)^(-1) modulo2^j. Its total off-domain extension is an internal
mathematical definition, not a claim that the source specifies all arbitrary
states. Odd-unit conditions for the actual fallback must be supplied by the
author's proved ladder theorem, not new oracle assumptions.

## Exact planned public signature

```lean
theorem recover_zWalk_active (p x : Int) (hp : p % 2 = 1) (t : Nat)
    (hactive : (Hddivsteps.zWalk p x t).g ≠ 0) :
    recoverStepBits p (Hddivsteps.zWalk p x (t + 1)) =
      ((if 0 ≤ (Hddivsteps.zWalk p x t).z ∧
          (Hddivsteps.zWalk p x t).g % 2 = 1 then 1 else 0),
        (Hddivsteps.zWalk p x t).g % 2)
```

Namespace: ASPBE.Uncompute. `recoverStepBits` is the deterministic mathematical
case split defined above, not a supplied functional argument.

Binder audit: p,x,t are TYPING carrier/input data. hp is SOURCE oddness. hactive
is SOURCE restriction to an active transition. Inv, fodd, determinant, window,
swap classification, odd-factor/residue existence and ladder correctness are
dependency conclusions, never final hypotheses. No EXCESS binder is intended.

Acceptance: actual Lean4.33.0 elaboration, exact type/axiom inspection, direct
use of the fixed author sources, independent source-blind reconstruction and
distinct source/formal review before any local admission. Preserve failures
and this pre-proof signature even if a successor is necessary. Production Lean
and its current publication bindings remain unchanged.
