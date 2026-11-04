# Continuation checkpoint — 4 November 2026

The non-Lean work can continue without additional user files. This checkpoint
checks the delivered twelve-packet cohort against the new current-main baseline
and screens the sixteen newly merged semantic diagnostic propositions for overlap.
It adds no question, permanent core, split assignment or admission decision.

| Binding | Value |
| --- | --- |
| New current-main base | `abfd4f5b8b52de29ed0e23f15d355e46f21748df` |
| New base tree | `61782d98de30b022b0662ef541f0c6a8c853dbf3` |
| Original cohort base | `6b23dab68c2970062ddfd568ce94bce74b566483` |
| Original cohort package | `99e830bd-e868-4c7c-947c-8187a63ce46a` |
| Original contribution commit | `89739e7d6bf9e5f711545fd7d778754c80c56847` |
| Continuation branch | `codex/nonlean-followup-20261104` |
| Frozen graph | `qcb-snapshot-ffa644f0da3031a1ce754b9a` |
| Resolved catalog | `5269b9f2521e3bf14db293fea34895f6e44a387c2479c164407b4d16dd9a2247` |
| Current retained / reserved cores | 198 / 15 |

The original patch applies to the new base. The original package checker and
current curriculum validator pass. All nineteen indexed source/evidence files
used by the first cohort are unchanged. Its twelve exact payloads, review reports,
questions, four existing-core contracts and original manifest remain unchanged.
The earlier package's base and test records remain historical; they are not
rewritten to pretend that review or execution happened on this new commit.
Fresh command results are in `evidence/compatibility.json` and
`evidence/required-tests.json`.

Main advanced through four commits and merged PR119. Its new diagnostic pilot
contains sixteen public candidate propositions in eight contrast pairs over five
existing parent cores. It adds zero canonical cores or native formal admissions.
The upstream report describes its own Lean qualification; this continuation
does not inherit that report as a new execution by this agent. The full new
question inventory and its exact source-file hash are retained in this checkpoint.

`OVERLAP.md` records a bounded mathematical-target comparison. It distinguishes
shared assessed subproofs, specializations and conceptual context from full
question equivalence. The new pilot strengthens the reason to reuse existing
normalization/orientation/composition diagnostics. It does not by itself replace
the original cohort's conditioning, precision-allocation, gauge, cross-Gram or
Bernstein-error targets. Global semantic reconciliation remains pending.

`NEXT_ACTIONS.md` separates work that can proceed now from external conditions.
`B2_DECISION.md` makes the phase-family admission choice reviewable without
silently rebinding the candidate to an existing immutable contract.
Repository metadata still reports `pull: true`, `push: false`; a remote PR cannot
be opened through this connection without a writable repository/fork. PR114 is
still open at `ff361a6ee91352f9692b3716c03b677ead9918be`; its Plan208 successor
remains branch-only. No Goal-creation API is exposed. Those access conditions do
not prevent source analysis, authoring, AI review, local validation or ZIP/patch
delivery in the conversation.

This is an integration and overlap audit authored by `/root`, which already saw
the previous QA and reviews. It is not an independent mathematical re-review or
maintainer approval. No new mathematical answer or rubric is introduced here.
No Lean execution, inference/training, paid API, main merge, Lean-track edit,
website generation or stable publication was performed.

## Apply and reproduce

The continuation archive includes the unchanged original cohort and this additive
checkpoint, with a patch based on the new current-main commit above. Start in an
isolated checkout at that exact base. Copy the archive's `benchmarks/` subtree or
apply its patch, not both. For an existing checkout already containing the first
cohort, copy only this checkpoint's UUID directory; do not apply the full patch
over existing files. Review the delivery receipt and verify the manifest hashes.

From the repository root, use the supported Python environment and the existing
dependency file `benchmarks/quantumcomputingbench/requirements.txt`:

```sh
python -m unittest discover -s benchmarks/quantumcomputingbench/tests -v
python -m unittest website.scripts.test_quantumcomputingbench -v
python benchmarks/quantumcomputingbench/scripts/curriculum.py validate
python benchmarks/quantumcomputingbench/tracks/non-lean/packages/99e830bd-e868-4c7c-947c-8187a63ce46a/verify_package.py
```

Use a writable `TMPDIR` outside the repository. The original raw failure log's
known trailing-space warning is preserved. No validator or historical evidence
is changed to make a check pass. Current test logs record the actual results;
schema/compatibility success is not mathematical correctness or admission.
