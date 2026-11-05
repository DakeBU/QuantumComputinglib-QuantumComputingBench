# Lean 4.33 / frozen QA integration boundary

Status: **integration blocked; diagnosis and next-gate design only**. This is
not a solver benchmark, a mathematical impossibility, or permission to bypass
the existing QA checks.

The [source-object audit](report.json) compares the exact main snapshot, proof
contribution and automatic merge tree. [Per-object evidence](git-object-evidence.json)
retains every measured mismatch and the earlier missing-object observation.
Its hashes are LF text hashes, not raw publication-binding hashes.

The parent independently repeated the existing `source_matches` checks on
merged checkpoint `01be0f83c9216a516f2439e00f6c554ddd556c92`: **58 unsupported
inputs, including 51 Lean modules**, agree with the audit. The ordinary source
publication gate accepting 50 modules plus one compatibility case does not
automatically rebind benchmark questions or old reference runs.

The site test stops at `ConcreteSemantics.lean`. Even after that first check,
old reference receipts carry another proof-input digest, and the warmup/native
source associations also bind older source bytes. Conversely, `build_site.py`
already satisfies the existing exact organizer-compatibility case: changing
that allowlist again would not solve this migration.

## Minimal additive migration experiment

1. Freeze an explicit **new reader/current-runtime association version** for
   the exact old snapshot and final Lean4.33 source/configuration/graph context.
   Preserve every historical snapshot, question, answer, core ID, split, score,
   review and reference report. Do not edit the old compatibility manifest to
   append hashes without an independently reviewed semantic association.
2. Classify all 58 deltas: mathematical interface/proof, toolchain/dependency,
   source/publication metadata, and generated graph/statement anchors. Existing
   whole-module reviews may be evidence inputs, not automatic QA equivalence.
   Review each affected question-to-theorem association, including warmup and
   native formal views. Changed premises, normalizers, registers or resources
   require an explicit bridge or remain unsupported; they are not metadata.
3. Bind an exact old-node/current-node/source-anchor map. Retain old graph IDs
   and full AND dependencies; distinguish compile evidence, source equivalence,
   partial support and complete QA formal-view equivalence. The preparatory
   measurement candidates remain outside production/gold until their own
   publication and graph admission succeeds.
4. After the actual matching full library/Tests gate, run new deterministic
   reference probes in new output paths. Require own-source provider checks,
   actual full signatures and axiom observations, and rejected wrong-type and
   `sorry` controls. Do not copy a success flag or relabel an old receipt as a
   current execution.
5. Only then independently review a minimal version-dispatch/loader change.
   Admit exact reviewed old/current pairs; reject unknown paths/hashes, altered
   questions or splits, stale source/review/reference bindings, missing graph
   nodes, changed generator/anchor conventions and absent compiled evidence.
   The unchanged historical mode must still reject the current mismatches.
6. Run the full QA release/curriculum/integrity suite and complete website,
   Blueprint, browser, source-link and final path-leakage gates at the final
   integrated head. Main deployment additionally requires real commit-bound
   live verification. No release or score improvement follows from this design.

Stop the experiment if an association changes the mathematical contract, an
unreviewed case is needed, any negative control passes, a historical artifact
changes, or the runtime graph cannot explain the claimed support. Keep the
failed evidence and mark that case unsupported; do not weaken the guard.

This sequence changes no production loader, verifier or benchmark behavior in
the current checkpoint. The [main-sync receipt](../c411-main-sync-qa-frontier.json)
records already passed local checks separately from the still-open QA and
final integration gates. The public presentation release is independently
complete on main via PR115; it does not imply this proof migration is deployed.
