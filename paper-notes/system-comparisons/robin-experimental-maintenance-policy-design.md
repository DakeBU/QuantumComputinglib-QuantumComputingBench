# RobinMatrix: experimental research versus Lean toolchain maintenance

Status: diagnostic and proposed design, **not an approved or implemented
publication-policy change**. Main has not migrated. Existing Lean verification,
publication rejection, scoring, source bytes and historical evidence are intact.

## Observed conflict

The fresh canonical extractor and committed declaration inventory both contain
395 public RobinMatrix declarations, all experimental, none with an open proof.
`scripts/generate-blueprint-catalog.py` assigns the experimental flag by exact
filename. It is not waiting for a future review to clear that flag.

The unchanged `website/scripts/check_research_publications.py` requires a
record for every changed production module, but rejects any record containing
an experimental declaration before checking its scientific binding. A synthetic
non-review probe with the exact current public name set reproduces that
rejection. See the [bounded diagnostic](../../reports/lean-433-migration/c119-robin-policy-conflict.json).
This does not question Lean soundness or claim the module's physical BE route
is complete. It means adding the missing row alone cannot satisfy this policy.

The actual main-to-contribution RobinMatrix diff is only 26 added and 26 removed
lines: tactic/definitional-reduction repairs plus a local recursion-depth
option. The current independent source-first whole-module reconstruction reads
all 677 declarations and 1950 fields; actual decoder comparison follows its
freeze. Neither that review nor the compatibility diff closes the raw-fold
counterexample, physical preparation/unpreparation, clean workspace, full
normalized block, analytic coefficient realization or resource obligations.

## Decision requested asynchronously

Recommended for review: retain `experimental=true` and design a separate,
explicit **toolchain-maintenance review lane** for this precise compatibility
change. The alternative is to retain the current policy unchanged and defer
main migration. No reply is consent to neither option; unaffected mathematical
and provenance work continues. No behavior-changing patch is installed here.

Do not solve this by flipping the filename flag, editing generated JSON,
omitting the module, inventing reviewer acceptance, weakening scientific targets,
or suppressing a failing check. The mathematical source-assimilated lane and
the proposed maintenance lane have different claims and must remain visible.

## Minimum proposed maintenance contract

If the user authorizes the direction, first produce and independently review a
small policy patch and its negative tests. The Lean verifier is unchanged.

1. Pin exact old/new module bytes, toolchains/manifests and the compatibility
   diff. Independently verify that mathematical definitions, source-facing
   statements and all logical binders are preserved; compiler/proof options
   remain explicit. A changed target does not qualify for this maintenance case.
2. Retain the same whole-module source-blind decoder and own-source/own-formal
   independent review, raw association, exact context, real compilation, Tests,
   trust/axiom, executable, site and reader obligations. An agent success JSON
   or controller replay is not proof of these gates.
3. Record maintenance evidence in the existing canonical publication ledger,
   under a distinct typed collection/role, not a competing status database.
   Existing source-assimilated record validation remains unchanged. An exact
   module cannot simultaneously claim both lanes.
4. Keep all 395 experimental flags and their exclusion from certified research
   cards. Do not promote the physical BE construction, convert refuted suppliers
   into open candidates, or count maintenance as scientific success.
5. Report source-assimilated and maintenance-reviewed counts separately. A
   hypothetical `50 source-correspondence + 1 maintenance` must never be called
   `51 source-assimilated modules`. Full main integration is a further gate.

## Required negative tests before any policy implementation

Reject missing or stale evidence, forged roles, partial declaration/field
coverage, changed signatures/definitions/binders, a different module, a changed
base/head or config, a hidden scientific-target edit, a claimed physical success,
experimental-flag removal, a hole/unsafe axiom, and a missing/failed actual gate.
Keep the current source-assimilation guard's rejection test intact. Test both
lanes against one shared immutable context and reject duplicate/mixed claims.
An unknown future module/change must not inherit this one compatibility case.

## Reversibility and current boundary

No maintenance implementation, exception, new source record or accepted
maintenance verdict exists. A future approved implementation must be separately
tested/reviewed and reversible without deleting proofs, failures, logs or user
files. The present change is only evidence and a design for a human decision.
The final integration still owes current applicable CI and genuine publication
policy approval. Hermite finite-bit SP and new textbook roots remain open.
