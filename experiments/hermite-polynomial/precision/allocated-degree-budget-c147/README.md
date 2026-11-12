# An explicit qubit-width bound for the allocated Taylor index

Status: `proved_locally`, independently reviewed source/runtime admission and
full integration pending. Lean 4.33.0 accepted the exact sealed four-theorem
module; its own output was separately imported for definitions/types/axioms.
This is a Hermite parameter-budget provider, not a completed SP circuit.

## What is now bounded

The existing source uses the literal cutoff

    T(e) = clog_2(max(1, ceil_N(1/e))),
    delta = epsilon / [4 * 2^n_p * (k+1)^2 * 2^(2*k)].

The new theorem proves, for all natural k and n_p=n+1>=1 and rational epsilon>0,

    M = n_p + 2*k + T(epsilon / [4*(k+1)^2]),
    T(delta) <= M,
    sourceDegree(delta) <= 4*M^2 + 2*M + 1.

For fixed k and epsilon, the last bound is explicitly quadratic in n_p. The
quantity sourceDegree is the Taylor truncation index: its sum has D+1 terms.
It is not the degree of the entire piecewise source or its separately
k-dependent middle polynomial, a minimal approximation degree, a TT rank,
stored-address count, circuit size or runtime bound.

The mechanism is short: shrinking a positive tolerance by 2^m adds at most m
to this exact cutoff. Factor the original allocation, apply that cutoff
lemma, then substitute the existing degree formula. No tolerance, state,
oracle, normalization or success requirement is changed. Large tolerances,
k=0 and n=0 remain in scope; max(1,...) is not silently dropped.

## Evidence and failures

The first actual proof compile exited0 in31.844 parent-observed seconds.
The successful separate audit exited0 in23.328 seconds, printed six actual
definition bodies and all four new theorem types/proofs/axioms. Each reported
exactly propext, Classical.choice, Quot.sound. The directly executed Lean
binary, sources, selected current project outputs and inherited13-member
experimental cache have explicit hashes. These are inherited provider
contexts, not a clean transitive source-to-binary build.

The first context-only probe exited1 before proof loading: a partial old
QuantumBlockEncoding namespace shadowed a missing provider. The corrected
path places the complete current project namespace before that legacy cache.
No mathematical source repair was needed. The first audit wrapper then
failed to parse universe-qualified axiom names; original output is preserved.
A tested strict parser recognizes printed universe suffixes, still rejects
unknown axioms, and requires the exact four expected roots. No production
verifier or ordinary-axiom allowlist was changed.

The compiler's unused/unreachable-tactic warnings remain in the observation
archive. They are not hidden by disabling linters or relabeled as PURIFIED.
The exact pre-proof seal and original author freeze remain unchanged.

## Still open

This does not bound coefficient bitlength, rational GCD/reduction, full
classical preprocessing, QR/angle extraction, gate synthesis, physical
ancillas/cleanup or uniform saved-executable error. In particular the old
exact-real 2*k+6 bond does not transfer to this precision-dependent source.
The source-to-stored-chain consumer and its actual address/cost contracts are
separate next obligations; Hermite scientific ROOT remains open.

To inspect, start with the four declarations in AllocatedDegreeBudget.lean.
RootAudit.lean specifies the actual diagnostic commands. Reproduction needs
the pinned current project namespace and the separately staged standalone
PiecewiseSourceBudget import closure (including the finite-middle
ConsumerChecks provider), not an arbitrary same-named cache. Observations
record the chosen providers and binary; no automated clean-room rebuild or
missing-input success is claimed. Full actual printed output and failures are
available losslessly in observations-original.zip.

Rollback is additive: remove this experimental packet; no production source,
target, scoring, verifier or historical evidence was changed.
