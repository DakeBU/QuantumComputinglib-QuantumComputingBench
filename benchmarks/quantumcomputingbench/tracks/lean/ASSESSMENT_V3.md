# Sealed assessment v3: explicit study and training boundaries

V3 preserves all fourteen v2 propositions and appends four Promise-register
questions. The eighteen propositions form nine contrasts. The additional two
contrasts share **one** source/exposure group; they are not two independent
domains. The canonical public catalog and its historical split labels stay
unchanged.

The four new `candidate:<UUID>` study cores bind their question, assumptions,
conventions, standalone proposition and source files. An NL answer and a Lean
challenge are stages of the same question, not two independently counted
mathematical cores. These study contracts do not grant public-catalog or native
formal admission.

## Choose supervision before interpreting a score

| Training profile | Existing train cores | NL / semantic views | Lean views | Appropriate interpretation |
| --- | ---: | ---: | ---: | --- |
| `baseline` | 74 | 86 | 12 | Held-out target compositions using already taught subproofs and witness patterns. |
| `promise_register_family_holdout` | 61 | 69 | 8 | Controlled task-family template withholding relative to this exact export, under declared generic foundations. |

The filtered profile omits thirteen whole cores and twenty-one views. It
removes all modalities of each excluded core; omitted train examples are not
reclassified as test examples. The exact public profile manifest binds every
mathematical training record and its core/view relationships. Producer commit
metadata is separate from the fingerprint of the mathematical records.

Independent review found substantial baseline overlap: involution versus
double-application failure, arbitrary entering scratch restoration, the role
of an intervening read, preserved-control inverse proofs, target-H/CCZ/target-H,
and wrong-selector X witnesses. The baseline therefore does **not** establish
an unseen mechanism or source family. The filtered profile removes these
templates while retaining explicitly declared permutation, matrix, sector,
reindexing, placement and state-support foundations.

The exact positive identities and short proofs are public library source.
Neither export establishes unknown pretraining exposure, actual checkpoint
training history, statistical independence, whole-graph mastery or internal
understanding. Adding the omitted baseline examples, public evaluation
solutions, workbook or full source proofs as training material invalidates the
filtered-profile study boundary. Record that exposure rather than silently
keeping the same interpretation. A CLI profile declaration is not training
authentication. Use the same declared profile and budgets for matched SFT/RL
comparisons; different package sizes alone do not establish causal gain.

## Reproducible entry points

All evaluation inputs, grader records and the bank must occupy disjoint
directories outside the public checkout. Give a model only the current
per-task leaf or the current `model_messages` payload.

```sh
python benchmarks/quantumcomputingbench/scripts/assessment_v3.py audit
python benchmarks/quantumcomputingbench/scripts/assessment_v3.py export-training \
  --training-profile baseline --output BASELINE.json
python benchmarks/quantumcomputingbench/scripts/assessment_v3.py export-training \
  --training-profile promise_register_family_holdout --output FAMILY.json

python benchmarks/quantumcomputingbench/scripts/assessment_v3.py prepare \
  --bank PRIVATE_V3_BANK --split test_public \
  --training-profile promise_register_family_holdout \
  --student RUN/student/tasks.json --controller RUN/grader/controller.json
```

The development split retains eight old propositions. The test selection has
six old and four additional propositions. Visibility is owner-sealed; the
inherited `test_public` split enum does not publish their questions or answers.
The unchanged v2 commands and bank remain available for frozen reproduction.

Collect each first answer in a fresh context without tools or feedback. Save
raw replies and exact messages separately. Then use the same stages as v2:

```sh
python benchmarks/quantumcomputingbench/scripts/assessment_v3.py freeze \
  --bank PRIVATE_V3_BANK --student RUN/student/tasks.json \
  --controller RUN/grader/controller.json --responses RUN/grader/responses.json \
  --output RUN/grader/first-answers.json
python benchmarks/quantumcomputingbench/scripts/assessment_v3.py review-template \
  --bank PRIVATE_V3_BANK --student RUN/student/tasks.json \
  --controller RUN/grader/controller.json --locked RUN/grader/first-answers.json \
  --output RUN/grader/reviews.json
python benchmarks/quantumcomputingbench/scripts/assessment_v3.py score \
  --bank PRIVATE_V3_BANK --student RUN/student/tasks.json \
  --controller RUN/grader/controller.json --locked RUN/grader/first-answers.json \
  --reviews RUN/grader/reviews.json --evidence-kind operator_supplied \
  --output RUN/grader/scores.json
```

V3 controller and first-answer envelopes commit the declared profile before
feedback. A changed profile is rejected by an existing lock. The underlying
v2 pure response/rubric protocol remains unchanged. Rewriting every artifact
can still forge an unauthenticated operator transcript; hashes are not an
external append-only service.

Missing and abstained tasks stay in planned denominators. Correct labels with
false or unreviewed explanations cannot pass the argument gate. Require all
exact rubric criteria for a qualified pass and both questions for a complete
contrast. Imported AI or human review identities are not authenticated.

## Mathematical and execution evidence

Historical reviews decoded the original literal propositions. One helper is
expanded into explicit control guards for standalone challenge imports; all
four propositions have a one-line transport spelling. Separate Lean
`Iff.rfl` checks establish definitional equivalence. This is an explicit
transport of existing review, not a claim that earlier reviewers saw the new
spelling. Original packets, rejected routes and first verdicts remain intact.

V3 mathematical qualification inherits the unchanged v2 receipt and uses a
committed pipeline for four submissions, four fresh final roots, four
equivalence roots, and wrong-target/`sorryAx` rejection controls. Source origin,
current bytes, exact requests, generated source, proof hashes, distinct
execution identities, runtime and transitive axiom policy are checked in
proportion to the advertised root claims.

These are inspected trusted authored references. Generated student proof
execution remains `ENV_BLOCKED` until an accepted isolated verifier is
connected. Formal challenges follow the locked student's belief, not the gold
label. Library lookup, isolated proof completion, mathematical argument quality
and unaided first-answer knowledge remain separate outcomes. No model
performance or calibrated difficulty is established by dataset qualification.
