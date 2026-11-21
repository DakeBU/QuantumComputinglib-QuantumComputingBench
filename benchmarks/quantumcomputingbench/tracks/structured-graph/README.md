# Graph-given diagnostics — optional information condition

This is a proposal namespace for optional graph-given variants within the two
existing tracks, not a third evaluation track or scored release. Follow [Goal C](../../CONTRIBUTOR_GOALS.md#optional-goal-c--graph-given-diagnostics-within-both-tracks)
and the [shared contract](../../shared/CONTRACT.md).

Use UUID-named draft JSON packets under `proposals/`. Bind the exact question and
answer to a mathematical core or `candidate:<UUID>` and a frozen graph slice.
The proposed packet must record:

- UUID, proposed `core_id`, contract/snapshot hashes, family, split and review status;
- graph version, node IDs, source locators, typed edges and complete hyperedge tails;
- student-visible graph slice and supplied theorem statements, or closed-book policy;
- question, notation, hypotheses, answer type, reference solution structure and rationale;
- accepted alternate answers, semantic rubric, negative controls and scoring scope;
- difficulty rationale, motif, source status, license, author and independent review provenance.

Keep the status `candidate_not_counted` until maintainer admission. Do not pass
these draft packets off as existing `curriculum.py` proposal-schema records or
modify the canonical registry to accept them without review. A future validator
and scorer will bind the accepted schema; until then use reviewed draft evidence.
