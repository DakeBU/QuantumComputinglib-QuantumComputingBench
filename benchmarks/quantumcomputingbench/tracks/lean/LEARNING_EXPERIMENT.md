# Matched learning registration and offline analysis

This is an optional future evaluation specification. The current task is to
author and qualify [questions and reference answers](LEARNING_VALIDITY.md);
actual model responses, training runs and learning measurements are not required
to accept that question-authoring work.

The current learning-validity cohort is **public semantic calibration**. Its
sixteen contrasted propositions form eight true/refuted contrasts, not eight
pairs of interchangeable pre/post questions. Public questions, source proofs and
source aliases may already be familiar to a model. A successful semantic decision
or Lean root does not by itself establish learning or understanding.

`src/qcb_learning_design.py` adds pure registration and imported-record analysis.
It starts no model, training job, endpoint, compiler or GPU process. It changes
none of the historical course pipelines, receipts, core contracts or splits.
The registered intervention is a plan; an operator's declarations and signed-looking
JSON are not independently authenticated evidence.

Generic `REGISTERED` status grants no 4B model SFT-to-RL progression gate. A
parameter-count declaration, a public-retest contrast or this template cannot
authorize SFT, RL, endpoint spending or a training launch. Model-specific stage
gates need separately accepted training, resource and evaluation evidence.

## Supported scope and readiness

`experiment_template(packet, scope="public_retest")` creates an explicit
`NOT_READY` draft with null operator/model/material identities. Fill actual
identities before registration. `validate_experiment(registration, packet)`
returns `REGISTERED` only when the public-retest plan is complete and consistent;
this status establishes neither execution nor semantic review.

The other scopes are `fresh_instance_transfer`, `family_transfer` and
`composition_transfer`. Their templates exclude train aliases but always remain
`NOT_READY`: this version has no independently reviewed parallel-form registry.
An invented form-review digest is rejected. A changed polarity or hypothesis is
not a fresh matched form, and a composition-labelled question does not establish
transfer to a held-out composition. No transfer score is computed by this version.

All source/solution aliases retain their inherited `train`, `dev` or
`test_public` split. Known train parents may be reserved for instruction. Train
aliases cannot enter a heldout-transfer assessment. A public-retest plan may
include train probes, but reports them explicitly as in-sample calibration;
they cannot support heldout claims. This bounded registration accepts training
parents present in the normalized cohort only. Broader training-source admission
needs an explicitly reviewed source registry rather than an unbound split label.

## Four matched cells

Each selected probe requires `update_pre`, `update_post`, `no_update_pre` and
`no_update_post`. Model ID, architecture/runtime digests, positive integer
parameter count, dtype, quantization, actual chat-template/tokenizer/adapter
digests, fixed prompt policy, sampling, NL-only closed-book exposure and declared
resource ceilings must match across all four profiles. The control's checkpoint
and both pretest checkpoints must be identical. The architecture digest binds
the actual model configuration; the runtime digest binds the inspected inference
engine/configuration. Their actual identities, size and precision need external
evidence, not just matching strings. Resource ceilings apply to the whole probe
episode, not each provider call. Matching ceilings does not mean identical
realized compute.

`profile_template()` returns the complete profile shape with null identity
placeholders and explicit small ceilings, with **zero endpoint spend by default**.
It grants no execution authorization.
Fill actual `model_id`, `checkpoint_revision` (40/64 lowercase hex),
`chat_template_sha256`, `tokenizer_sha256`, `adapter_sha256` and
`architecture_sha256`/`runtime_sha256` (64 lowercase hex), plus `parameter_count`
(a positive integer, not a Boolean or floating-point number), `dtype` (for example
`bfloat16`) and explicit `quantization` (for example `none`). Null draft values
and placeholder precision labels remain unready. Sampling specifies seed,
temperature, top-p and thinking mode; `unspecified` thinking mode is explicitly
`NOT_READY`. Resources specify maximum calls, total input/output tokens, wall
seconds and endpoint charge. Zero endpoint charge is not zero hardware cost.

- `weight_update`: register material identity, train parents and optimizer-step
  count. The updated artifact must have a different checkpoint revision. All
  assessment lesson prefixes and `intervention.lesson_text` are null. Actual
  intervention evidence must connect the registered base to that artifact; a
  changed hash alone is not learning.
- `in_context`: all four checkpoints stay identical and optimizer steps are
  null. Register the actual nonempty `intervention.lesson_text` (at most 64,000
  characters) and set `material_sha256` to SHA-256 of its exact UTF-8 bytes.
  Whitespace and Unicode are not normalized. Only `update_post` carries
  `lesson_prefix_sha256`, equal to that material digest. A prefix hash without
  literal lesson text cannot qualify the experiment. This is contextual
  instruction, not parameter learning.

Every probe uses a fresh independent context with no assessment feedback.
Assessment gold and pretest transcripts must not be ingested into the intervention.
Canonical train material may intentionally overlap the in-sample retest probes;
that exposure is not heldout evidence. Dev/test answers are excluded from
instruction. These conditions begin as explicit operator declarations and need
external checking before any attested contrast is computed. The posttest must
not receive pretest answers through history, persistent memory or a hidden adapter
prefix. Public pretraining exposure remains unknown.

## Canonical declared messages and actual rendered input

`canonical_prompt_policy()` returns this implementation's fixed policy object.
`profile_template()` binds `prompt_policy_sha256` to
`digest(canonical_prompt_policy())`; an alternative opaque policy hash is rejected,
even if all four cells use it. The known implementation-policy identity does not
fill any unknown model/runtime identity.

`canonical_messages(registration, probe, cell=...)` returns the exact list of
role/content objects. It starts with the fixed system instruction, optionally
adds the literal lesson as a user message for in-context `update_post`, then adds
one user message containing canonical JSON for the Stage-A `question`,
`assumptions`, `conventions` and `response_format`. JSON uses sorted keys,
unescaped Unicode and compact separators, with no nonfinite values. Probe IDs,
schema/state/session IDs, arm, phase, model identity and evaluator gold remain
outside the model messages. The four weight-update cell prompts are identical
for the same probe; an in-context update can differ only by its registered
literal lesson message. Controller metadata may remain in private record fields.

The measurement must include this exact `session.messages` list and set
`session.prompt_digest = digest(canonical_messages(...))`. Extra system/tool
instructions, added metadata, changed JSON content/formatting or a caller's
unrelated prompt hash are rejected even when `input_digest` still matches.

These checks establish **declared canonical messages**, not the actual input
rendered by a chat template. An adapter, runtime or endpoint may add instructions,
use another template, or send another token stream. To compute an attested
contrast, the external verifier must inspect the bound actual request/transcript,
rendered input and token IDs and verify that they implement the canonical
messages under the registered template/runtime, with no hidden additions. A
provider that cannot expose sufficiently authenticated rendering/token evidence
leaves this condition unverified and the learning estimate null. Neither hashes
nor an operator's unchecked assertion close that gap.

## Executable planning example

From the repository root, the following reads the normalized cohort and analyzes
an empty plan. It performs no model or Lean execution and prints null gain:

```python
import json
import sys
from pathlib import Path

bench = Path("benchmarks/quantumcomputingbench")
sys.path.insert(0, str(bench / "src"))
from qcb_learning_validity import load_cohort
from qcb_learning_design import (
    analyze_experiment, experiment_template, validate_experiment,
)

packet, cohort_status = load_cohort()
registration = experiment_template(packet, scope="fresh_instance_transfer")
print(json.dumps(validate_experiment(registration, packet), indent=2))
print(json.dumps(analyze_experiment(registration, packet, []), indent=2))
```

Wrapper CLIs can import these functions directly. No function imports an adapter
or takes an executable module/name from a record. Freeze the complete registration
before assessment; retain its digest and original bytes outside the public
repository alongside private raw trajectories. Do not replace an earlier run
with a revised favorable selection.

## Measurement and blinded semantic review records

`analyze_experiment(registration, packet, measurements, *,
operator_attestation=None, attestation_verifier=None)` accepts a list of exact
`qcb.learning_measurement.v1` objects. Each has these fields:

| Field | Required meaning |
| --- | --- |
| `measurement_id`, `registration_digest`, `cohort_digest` | Unique execution identity and exact frozen inputs |
| `cell`, `probe_id`, `profile_digest` | One selected probe in one registered matched cell |
| `execution_class` | `synthetic_fixture`, `unattested_import` or `operator_model_observation` |
| `generation_status` | `answered`, `abstained`, `not_run`, `env_blocked`, `protocol_error` or `budget_exhausted` |
| `answer`, `answer_digest` | Parent protocol's exact decision/explanation object, or null for unanswered outcomes |
| `semantic_review` | Separate exact-content review, or null pending actual review |
| `session` | Unique ID, literal `fresh_context: true`, `assessment_feedback_received: false`, public Stage-A `input_digest`, exact canonical `messages`, their `prompt_digest` |
| `usage` | Actual calls, input/output tokens, wall seconds and endpoint USD; null stays unknown |

Unsubmitted planned cells are added as `not_submitted`. Wrong answers, abstention,
missing records and environment failures remain different outcomes. Unknown
usage is never fabricated. Out-of-ceiling usage is rejected for this matched
analysis; preserve its original record separately as an over-budget execution.
Session reuse, duplicate cells and stale profile/input bindings are rejected.

`review_input(probe, answer)` creates a review projection containing only the
public semantic input, exact answer and full criterion rubric. It omits arm,
phase, model/checkpoint identity and formal result. Actual review work must
preserve those blinding boundaries, including avoiding identity cues in answers.

A `qcb.learning_semantic_review.v1` object binds `probe_id`, `answer_digest`,
`rubric_digest` and `blinded_packet_digest`. It records a reviewer object with
`identity`, `kind` (`human`/`ai`) and actual `method`; the exact
`respondent_identity`; four literal blinding flags (`arm_hidden`, `phase_hidden`,
`model_hidden`, `formal_result_hidden`); a nonempty reason for each criterion
mark; `semantic_fidelity` (`faithful`, `unfaithful`, `uncertain`); and substantive
overall `reasoning`. `criteria` contains exactly every rubric ID with finite
`score` in [0,1] and a `reason`. Self/author grades, renamed rubrics, stale answer
hashes and extra direct score fields fail validation. Distinct identity strings
still do not authenticate real independence.

The supplied partial mark is the rubric-weighted mean. For the matched semantic
measure, an incorrect polarity or unfaithful answer receives zero; faithful
answers retain their rubric mark. Uncertain/unreviewed explanations remain null.
Thus partial mechanism credit does not override a false or changed contract.
These fields are explicitly labelled unauthenticated until external attestation.
Binary decision correctness is separate from explanation correctness and is not
a substitute learning score. This component accepts no formal-proof self-grade.

## Operator evidence boundary

Supplying an `operator_attestation` file alone never unlocks a gain. The optional
`attestation_verifier` must be trusted caller code that authenticates the **whole**
attestation against independently accepted operator evidence and returns literal
`True`. It is never loaded by name from imported data. No built-in verifier,
automatic trust store or authentication claim is supplied here. A CLI that only
loads JSON should omit the callback and report unverified imported evidence.

An exact `qcb.learning_operator_attestation.v1` binds registration/cohort/operator
identities, all unique measurement digests, and the deduplicated set of all
semantic-review digests. Identical answers and rubrics can share an identical
blinded judgment; this does not turn it into multiple independent judgments.
It also requires one `prompt_execution_receipts` entry for each measurement that
claims generation. Each entry binds `measurement_digest`, canonical
`prompt_digest`, `rendered_input_sha256`, `rendered_token_ids_sha256`,
`transcript_sha256` and `evidence_reference`. These fields identify actual private
execution evidence for the trusted verifier to authenticate and inspect. They
are not authenticated simply because their strings are valid hashes. Missing,
duplicate or differently bound prompt receipts fail validation.
It contains an evidence reference and signature plus a completed intervention
receipt binding kind, base/post checkpoint revisions, material digest, actual
optimizer steps and an actual evidence reference. It must attest that:

- actual model execution was observed and checkpoint identities were checked;
- actual architecture, runtime, parameter count, dtype and quantization were checked;
- actual request/transcript messages matched the canonical payload, and rendered
  tokens matched the registered template/runtime/policy without hidden instructions;
- registration preceded assessment;
- independent contexts and no-feedback conditions were checked;
- actual blinded and independent review was checked, including the cohort gold
  and rubric mathematics;
- instruction excluded dev/test answers and assessment records were not trained on.

Exact `claims` keys are `actual_model_execution_observed`,
`checkpoint_identities_checked`, `registration_precedes_assessment_checked`,
`fresh_context_and_no_feedback_checked`, `reviews_blinded_and_independent_checked`,
`cohort_gold_and_rubrics_reviewed_checked`,
`architecture_runtime_precision_and_size_checked`,
`actual_prompt_transcripts_match_canonical_messages_checked`,
`rendered_tokens_match_registered_template_and_policy_checked`,
`training_excludes_dev_test_answers_checked` and
`assessment_records_excluded_from_training_checked`; every value must be literal
`true`. The receipt fields are `kind`, `base_checkpoint_revision`,
`post_checkpoint_revision`, `material_sha256`, `completed`, `optimizer_steps` and
`evidence_reference`. All must agree with the frozen plan.

Synthetic or unattested record provenance blocks actual gain even if a trusted
callback returns true. An authentication exception or nonboolean return also
cannot award a gain. Software tests deliberately mock this boundary to exercise
validation/arithmetic; their engineered records are not an actual experiment.

## Complete-matrix analysis and limits

A contrast requires every selected probe's four answered, semantically reviewed
cells, actual usage, operator-model provenance, a ready public-retest registration
and authenticated external execution/rendering/review evidence. One missing/uncertain/unreviewed cell keeps
the entire primary `learning_gain` null; the analyzer does not select favorable
complete cases. Planned and not-run records stay null.

Probes sharing a declared mechanism **or any parent core** are merged into
connected clusters. Average probe marks within each cluster and cell, then compute

```text
cluster_DiD = (update_post - update_pre) - (no_update_post - no_update_pre)
learning_gain = mean(cluster_DiD)
```

This weights clusters equally rather than treating sixteen propositions as
sixteen independent samples. Report the full planned/submitted counts, typed
outcomes, complete four-cell count, all omitted identities and individual cluster
contrasts. Unknown additional shared mechanisms can leave residual dependence.

The minimum registered cluster threshold is ten. Below it, the report says
`too_few_clusters_no_significance_claim`. This version supplies neither p-values
nor confidence intervals even above that threshold. It reports no established
understanding, causal learning claim or heldout transfer. A positive externally
attested public-retest contrast is limited evidence of changed performance on
these public items. It can reflect familiarity or memorization. New independently
reviewed parallel forms and mechanism/family/composition holdouts are a separate
required milestone. Formal root correctness, NL semantics, process-reward value
and parameter learning remain distinct claims.

Run the owned software checks without Lean or models:

```sh
python -m unittest discover -s benchmarks/quantumcomputingbench/tests -p test_learning_design.py -v
python -m ruff check benchmarks/quantumcomputingbench/src/qcb_learning_design.py benchmarks/quantumcomputingbench/tests/test_learning_design.py
```
