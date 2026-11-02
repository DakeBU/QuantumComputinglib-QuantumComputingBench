# Separate capability diagnostics

The offline assessor separates retrieval observations, supplied semantic marks
and formal evidence over the same mathematical cores. It starts no model,
compiler or automatic semantic judge and produces no combined capability score.

| Output | Meaning | Boundary |
| --- | --- | --- |
| Curated target coverage | Fraction of reviewed interface targets returned by search | Not exhaustive proof-premise recall, use or usefulness |
| Curated route completion | All curated AND premises of at least one reviewed root route returned | OR applies only between whole-root alternatives |
| Local obligation coverage | Returned names relevant to one provided obligation | Empty groups are unscored; provider proofs remain separate |
| Weighted supplied mark | Externally supplied criterion marks | Not an automated mathematical truth verdict |
| Semantic fidelity | Faithful, unfaithful or uncertain relative to the question | Separate from partial credit; uncertainty keeps the aggregate null |
| Reported formal-root status | Existing status in an evaluator-owned record | Offline assessment issues no new certificate |

All current corpus entries support the authored route, so whole-root
route-aligned return fraction is degenerate. Do not present it as discriminating
retrieval precision. Imported original root theorems remain callable outside
the search corpus; a correct proof can accompany zero retrieved names. A
completed leaf group never counts as a completed root route.

## Complete canonical rubric

The fixed pilot uses the complete **current canonical question rubric**:
literal criterion IDs, text and weights, exact source item, task and corpus.
SP005's normalization-invariant explanation is retained; the shorter
proof-obligation authoring rubric is not substituted for the original question.

Only recorded `explain` answers can receive supplied marks. Adjudication binds
the chosen answer index/digest, full report, task and rubric. Each criterion
needs a finite mark and substantive reason. Actual reviewer identity, human/AI
kind, method and a distinct declared respondent are explicit. These checks
neither authenticate people nor establish the truth or independence of a
judgment. Unreviewed prose stays null even when Lean checks the root.

Two engineered positive/negative pairs test the software. Their fixed answer
hashes, full expected criteria, provenance and typed assumption audits are
validated before replay. They are authored expectations, not model responses,
fresh judge calls or human/blind review.

## Commands

Assess an evaluator-owned session or authored smoke without semantic marks:

```sh
python benchmarks/quantumcomputingbench/scripts/capabilities.py assess-pilot \
  --input _out/obligation-smoke.json --output _out/capability-assessment.json
```

Create evaluator-only review templates outside the public repository:

```sh
python benchmarks/quantumcomputingbench/scripts/capabilities.py review-templates \
  --input _out/obligation-smoke.json \
  --output ../qcb-eval-private/explanation-templates.json
```

Templates contain answers and rubrics and must not be sent to the prover.
Blanks are not accepted grades. After actual review, follow their instructions
to create separate `qcb.explanation_adjudication.v1` records and pass the list
with `assess-pilot --adjudications PATH`. One explanation per report is chosen
explicitly; unknown or duplicate report adjudications fail closed. Do not
retrospectively choose the highest-scoring explanation without a declared
selection rule. Raw predictions and judge packets stay outside the repository.

Exercise the fixed expected-label examples:

```sh
python benchmarks/quantumcomputingbench/scripts/capabilities.py fixture-smoke \
  --output _out/capability-fixture-smoke.json
```

Commands require fresh outputs, bound inputs to 10 MiB and reject source drift.
No result alone establishes model performance, useful PRM reward, autonomous
decomposition, matched compute or stable acceptance. Views/conditions do not
increase mathematical core counts.

The [source-aware code review](../../reports/lean-agentic-capabilities-v1/code-review.json)
records exact inspected hashes and corrected issues. Actual model comparisons
still need an accepted isolated verifier, a bounded model adapter with real
usage accounting, reviewed route relevance and a private-instance protocol.
The public authored cohort is not blind. New corpora/distractors need new
relevance review rather than inheriting these labels.
