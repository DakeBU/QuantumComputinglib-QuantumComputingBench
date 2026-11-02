# QuantumComputingBench dataset card (working release)

## Current version: release-v3 (2026-10-21)

26 unchanged authored items retain their original content-bound AI reviews.
Four v2 answers are withdrawn from scoring/export, while original files remain
audit-only. Twelve corrected/new candidates have actual local Lean reference
evidence but await independent natural-language/source review; eight other
historical candidates remain pending. Provisional material is NOT reviewed gold.

There are 16 compiled fixed reference theorems, three real generated-harness
replays, and negative controls rejecting wrong-type proofs and sorryAx. These
are trusted-local-reference checks, not isolated model-output certification.
The complete production Lean gate passed on identical source/configuration
inputs. No production library theorem/source-review debt is newly promoted.

The v3 public split uses explicit construction-family holdouts in addition to
solution-family/target unions: 11 train, 4 dev, 11 test_public (7 core + 4 planned).
This is retrospective public diagnostic evaluation: old questions/answers were
already public. It is not an unseen, private or contamination-free assessment.
Target-node coverage and target-or-support membership are reported separately.
See the current README and repair audit; statements below about the original
hash-based split describe the historical policy unless superseded here.

## Purpose and scope

Original graph-grounded quantum-computing questions for diagnostic evaluation and
training. The frozen coverage universe includes all local Lean modules/public
declarations, shared foundations, all four curriculum parts, and explicitly
planned research/source records. A node's presence is not a question, and a
question's presence is not validated coverage. Read the generated coverage ledger
for the actual released scope and every uncovered node.

The objective and completion criteria remain in `AGENT_GOAL.md`. This working
release does **not** claim the full implementation goal is complete.

## Evidence ladder

- `source_inspected`: actual local declaration/type/ambient definitions inspected;
  does not establish compilation in this run or source-faithfulness to a paper.
- `planned_source_inspected`: accessible primary text inspected with exact anchor;
  explicitly not a local Lean certificate.
- `planned_evidence_pending`: planned record or secondary metadata only; unscored.
- `validation.formal`: separate from natural-language alignment and answer quality.
  Formal tasks require isolated replay and a transitive axiom policy check.
- Distinct-context AI content review is recorded as such, not as a human review
  or proof of real-world reviewer independence. No fabricated review identities.
- Legacy publication/semantic debt remains visible even when a historical source
  inventory describes a declaration as compiled.

## Mathematical depth

`support_count` counts distinct target/support nodes, including actual hypotheses
and constructions. `semantic_step_count` counts authored inference steps mapped to
support nodes; only separately reviewed arguments are released. These counts are
not difficulty by themselves. Structural graph distance remains `null` unless
computed with a declared edge meaning. Module imports and declaration ownership
are **not** elaborated proof dependencies. Conditional hyperedges retain all AND
premises; alternative sufficient routes remain distinct.

## Splits and exposure

Families and shared target solutions are unioned before splitting, including
reverse questions and substituted/template variants. Planned QIT and scientific
computing use topic holdouts; other split groups use a fixed family hash. This is
not a random row split. Supporting foundational lemmas may occur across splits;
no claim of disjoint dependency sets is made. Later batch additions may merge
components: create a new release version rather than silently changing old splits.

All released material, including `test_public` answers, is **public**. It is not
secret, contamination-free, or blind evaluation. No pretraining exposure is known.
Private future instances need separate authorized storage and release governance.

- Closed book: prompt and explicitly stated context only; no gold/review/proof.
- Approved interface: explicitly bound `name`/`type` statements only, no proof
  bodies. Interface policy approval is a maintainer action, not inferred by code.
- Open library: public proof retrieval is permitted; measures retrieval/application
  under that setting, not necessarily new proof discovery. Prompt export is not a
  tool-execution sandbox; the baseline runner currently supports closed book only.

## Generation, validation and scoring

The shipped authoring batches are original, source-inspected candidate material;
no API key is needed. Replaying deterministic authoring is not model generation
validation. Endpoint generation/baselines are operator-configurable via a bounded
adapter protocol. Default operation makes zero endpoint calls. Call/token/time/
cost reservations and actual usage are required; a fixture is never a baseline.
Session authoring/review token and monetary telemetry is unavailable and stays
unknown rather than fabricated as zero.

Exact answers use exact string grading only when the authored format warrants it.
Natural-language answers/proofs need explicit evaluator rubric marks bound to the
item and prediction hashes. No keyword, word-count or conclusion-only scoring.
Uncertain semantic judgments remain pending. Formal answers cannot score through
a substring scan or successful process exit. Evidence, correctness and semantic
fidelity are separate outputs. No model judge is enabled or claimed calibrated.

## License and permitted reuse

Original question/answer/rubric text and code are offered under the repository's
Apache License 2.0, subject to LICENSE_SCOPE.md, with source attribution and retained earlier MIT notices. This does not relicense external papers,
textbooks or upstream libraries. No external long source proofs/textbook passages
are redistributed. External citations are evidence pointers, not permission to
copy their text or a guarantee of training reuse rights. Planned source evidence
with unresolved access/license status remains blocked.

## Limitations and intended users

Designed for researchers who can inspect hypotheses, register/phase conventions,
normalization, success probability, ancilla cleanup and resource tiers. Not a
universal process reward model, physical hardware certificate, model training run,
or automatic source-faithfulness checker. Finite counterexample checks do not
establish arbitrary-width circuit theorems. Query, logical-gate, exact-real storage
and finite-bit complexity remain distinct.

No real model baseline has been measured. Local fixed reference theorems have
been checked; isolated untrusted-output certification remains ENV_BLOCKED.
See the current validation and coverage reports for the actual gates run,
typed blockers and next resumable batch.
