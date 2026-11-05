# Actual CI3 evidence and bounded static successors (WIP)

Main remains Lean 4.29.1; this contribution uses Lean 4.33.0. This checkpoint
does not register a new accepted publication, close the Hermite root, or merge main.

## Evidence that changes the next action

- [Actual CI3 fact receipt](c29-actual-ci3-runtime.json): job 117216834833,
  run 38973372595, contribution 6e67939, actual merge checkout
  84613488476803f84482d5ac74661f339326fe3b. Fresh target and probe exited zero.
  The exact sanitized 38-file artifact is preserved; 319 explicit records match
  CI2 and 450 generated records now include actual type/value/universe/axiom fields.
- [Independent runtime transport](c29-ci3-independent-transport.json) preserves
  the original source-blind packet. Two generated theorem signatures have real
  data/binder-domain pretty-print omissions; 96 generated value strings also
  contain omissions. This is not a lossless Expr export or a claim all value
  characters were cognitively reread.
- [Immutable correction](c29-ci3-omission-correction-transport.json) fixes the
  pre-review table's U+2026-only flag scan by appending a corrected table. The
  old table, packet, seal, allowlist and bundle remain byte-exact history.
  The old final omission boundary already correctly reported 2/96/1004.
- [Two-signature integration](c29-two-signatures-integration.json) adds only one
  bounded serial diagnostic child after the original 319+450 checks. It imports
  the same fresh target and requests only the two incomplete types with finite
  larger pretty-print budgets. Actual supplemental Lean output is PENDING CI;
  missing, omitted, stale, partial or nonzero output fails closed. No ordinary
  generated values are reprinted and no target is recompiled by the supplement.
- C31 v3 resolves the omitted dependent-Pi metadata and coarse source links in
  the original reviewer's STATIC scope. The v4 graph adds exactly one existing
  compiler-definition producer tail. The [same original reviewer's receipt](../../reviews/publication/primitive-compiler-c31/parent-v4-review-transport-c31.json)
  resolves OPEN-F3-D1 STATIC ONLY, preserves F1/F2 context and leaves full F3
  closure not redetermined. Seven stronger-consumer gaps and native/formal
  correspondence remain open. Natural source and production Lean are unchanged.

## Trust and resource boundaries

The recursive Cubic axiom closure contains Classical.choice, Quot.sound,
propext and nine target-owned native_decide axioms. They are traced observations,
not an automatic axiom allowlist or a mathematical refutation. Compiler/evaluator
trust policy, actual source/formal correspondence and publication binding remain
unassessed. Safe declaration flags do not remove the native compiler trust boundary.

Hermite job 117216834821 on 6e67939 actually completed SUCCESS at
2026-10-16T22:18:30Z before the next push. Its compile and existing finite
executable replay do not establish the full finite-bit polynomial-resource family.
No new whole-library `lake build && lake build Tests` or Pages gate is claimed.

## Behavior, tests and rollback

The production Lean tree, frozen scientific targets, trusted verifier, scoring,
required acceptance workflows and historical logs are not modified. The optional
Cubic diagnostic workflow now discovers `test*.py` instead of only test_runner.py.
Focused Python tests cover parsing failures, actual artifact hashes/fields, the
immutable table correction and the narrow original reviewer result. Exact executed
counts and gate output are recorded in the adjacent focused-checks receipt.

Rollback is confined to the optional runner append, five new package files and
the optional test-discovery line. Original drivers/validators remain exact. Retain
historical observations and typed failures even if the diagnostic is rolled back.
The aggregate publication gate must still reject the 28 unadmitted modules;
23 canonical records are not upgraded by this checkpoint.
