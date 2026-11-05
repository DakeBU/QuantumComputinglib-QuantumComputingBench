# Registered agentic evaluation pilot

The four-view default below is preserved. The optional
[`--suite course-v4`](COURSE_V4.md) now selects the entire qualified Lean course
for list, export, plan and bounded episode commands, preserving each view's
task and recorded reference lineage. The same real-formal isolation gate
applies before provider initialization. Synthetic course fixtures remain
protocol tests; they do not run Lean or a model. Offline profile commands do
not accept a suite or load a task registry.

The evaluator registers four public, reference-qualified task views over existing
shared cores. It supplies a bounded action loop and exports answer-free inputs.
It does not enable execution of model-generated Lean, establish a stable release,
or report model performance. Mathematical explanations require separate review.

## Task frontier

| View suffix | Existing core | Fixed split | Formal task |
| --- | --- | --- | --- |
| `la-102-v1` | `qcb-core-la-102` | `test_public` | Half-angle row rotation and determinant preservation |
| `sp-005-v1` | `qcb-core-sp-005` | `test_public` | Marginal squared-norm identity |
| `sp-007-v1` | `qcb-core-sp-007` | `test_public` | Sequential transfer induction from clean zero columns |
| `sp-008-v1` | `qcb-core-sp-008` | `train` | Real total probability over the joint word and bond register |

Each full view ID starts with `qcb-agentic-`. SP007 permits an arbitrary complex
boundary and does not add a normalization or unitarity premise to its transfer
claim. SP008 has the actual normalization premises and a bridge to a real sum of
squared norms. See [the reviewed contracts](SEQUENTIAL_PROOFS.md). A proof of a
provided formal root does not establish every sentence of the original NL answer.

The registry is a separate experimental evaluation manifest. It adds no
mathematical core, changes no split, and does not admit the companion proposals
into the canonical reader catalog. Running two strategies or two input views of
one core never creates two independent questions. References are public, so this
pilot is not a blind or contamination-free test. No dev tasks are manufactured.

## Inspect or export without executing a proof

Run these commands from the repository root. Use fresh output names:

```sh
python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py validate
python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py list
python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py export \
  --split test_public --mode proof_dag --exposure approved_interface \
  --output _out/agentic-public-inputs.json
```

Validation checks the exact shared contracts, targets, fixture identities,
recorded reference checks, fresh-root outcomes, approved axiom sets and pinned
historical Git source blobs. It does not run Lean or issue live certificates.
The older obligation checkpoint and newer sequential checkpoint retain their
different source revisions. `recorded_pipeline_matches_current_sources` is
reported separately; historical success is never relabelled as a current replay.
A shallow clone missing a required evidence commit fails qualification until
that history is available. Preserve the original reference commits when
integrating this pilot: use a merge commit, not squash/rebase. The evidence
checks require their exact Git blobs. Rewriting ancestry requires a separately
reviewed evidence-distribution change, not edited historical receipt hashes.

Agent exports omit references, answers, rubrics, controls and checkpoint bodies.
Search exposes only the approved declaration-interface corpus, not an arbitrary
filesystem or web search. Both strategies see a supplied obligation graph:
`root_only` permits repeated whole-root attempts; `proof_dag` also permits checks
of its provided intermediate nodes. Neither condition measures autonomous
decomposition or a persistent Lean tactic-state REPL. Root-only is not one-shot.

## Run a synthetic protocol smoke

Keep raw episode directories outside the repository. For example, from its root:

```sh
python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py run-fixture \
  --view qcb-agentic-sp-007-v1 --mode proof_dag \
  --episode-dir ../qcb-eval-private/sp007-fixture-001
```

The fixture exercises explanation, interface search, a deliberate failure,
repair and completion. It uses synthetic token values and a simulation verifier.
No model, Lean compiler, correct reference proof or network service is called.
`fixture_protocol_complete` never means a checked formal proof or measured model.
Use `--mode root_only` for the whole-root strategy; use `--purpose
explanation_only` for an NL-only smoke, which automatically uses closed-book
exposure. Directory reuse is rejected, preserving old trajectories.

## Operator adapter and frozen model profile

There is deliberately no bundled endpoint client or automatic model discovery.
Prepare and validate its profile without reading the task registry or loading
any adapter:

```sh
python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py profile-template \
  --output ../qcb-eval-private/model-profile.json
python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py schema \
  --output _out/operator-profile-schema.json
# Fill the actual adapter and model metadata in model-profile.json first.
python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py validate-config \
  --config ../qcb-eval-private/model-profile.json
```

The [canonical template](../../configs/agentic-operator.template.json) contains
null adapter/model identities and deliberately fails validation until filled.
It invents no checkpoint or template hash. Its small default budget does not
start an experiment or grant permission. Choose the profile's actual limits
before a model call; it is not a GPU-memory estimator for a particular Qwen.
Use `profile-template --purpose explanation_only` for a closed-book NL profile.
Conflicting explicit exposure flags are rejected rather than silently changed.

The [JSON Schema](../../schemas/operator-run-config-v1.schema.json) provides a
closed machine-readable structure. `validate-config`, `plan` and `run` also
apply the existing runtime cross-field, finite-number and strict-type checks.
Schema validation alone does not establish endpoint identity or usable isolation.
Profile inputs are limited to 64 KiB; credentials belong in the adapter's
private environment, not additional profile fields or a public JSON artifact.

An operator may provide a trusted Python `module:factory` adapter. The factory
must not generate text during construction. Its object exposes:

```python
is_fixture = False
implementation_sha256 = "<actual reviewed adapter implementation SHA-256>"

async def respond(request):
    # Forward request["messages"] verbatim with the pinned chat template.
    # Enforce the requested transport timeout, token limits and cost ceiling.
    # Parse one JSON action. Report real endpoint usage, including input-template
    # tokens and reasoning tokens. Never add verifier results to model output.
    return response_envelope(request, action, fixture=False, usage={
        "input_tokens": actual_input_tokens,
        "output_tokens": actual_output_tokens,
        "endpoint_cost_usd": actual_endpoint_cost,
        "source": "endpoint_reported",
    })
```

Import `response_envelope` from `qcb_model_loop`. The adapter is trusted operator
code; an echoed identity or prompt digest is not independent attestation of an
endpoint's behavior. Audit the actual adapter and endpoint configuration before
use. No adapter should take code or import names from model output.

Create an explicit JSON profile with schema `qcb.agentic_run_config.v1`:

- `provider_kind`: `operator_adapter`.
- `adapter`: its `id` (`module:factory`) and actual `revision_sha256`.
- `model`: exact `id`, a pinned 40- or 64-hex `revision`, and the actual
  `chat_template_sha256`; floating `main` is rejected.
- `sampling`: explicit `seed`, `temperature`, `top_p` and `thinking_mode`
  (`enabled`, `disabled` or `unspecified`).
- `condition`: `purpose` (`formal_proof` or `explanation_only`), `mode`
  (`root_only` or `proof_dag`), and `exposure` (`closed_book` or
  `approved_interface`). Explanation-only requires closed-book exposure.
- `limits`: all eleven fields supplied in the canonical template, with explicit
  per-call and total input/output tokens, calls, request/response bytes, time and
  endpoint cost. This bounded pilot allows at most 32 calls and 600 seconds.
- `session_limits`: every field of `dataclasses.asdict(SessionLimits())`, with
  tool wall time no greater than the model-loop wall ceiling.

`fixture_config()` is reserved for simulation and is not an operator profile.
Use the canonical operator template and reviewed actual values; do not invent
hashes or usage to satisfy validation.
For a local endpoint, zero endpoint charge does not mean zero GPU/CPU cost.

```sh
python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py plan \
  --view qcb-agentic-sp-007-v1 --config ../qcb-eval-private/model-profile.json \
  --episode-dir ../qcb-eval-private/sp007-model-001 \
  --adapter reviewed_adapter:create
```

`plan` performs no adapter import, initialization, discovery or generation and
creates no episode directory. An actual call requires `run` plus
`--authorize-model`; neither the profile nor a previous plan grants permission.
Without that flag, `run` is also a zero-call plan.
Supplying `--authorize-model` to `plan` or a non-generation command is an error.
Episode summaries include `failure_class`, `reason`, `provider_constructed` and
`episode_directory_created` so an environment gate is visible without opening a
raw trajectory. Episode commands return 0 for a completed simulation/NL answer
or dry plan, 2 for a blocked/incomplete episode, and 1 for input/data errors;
argument-parser usage errors follow Python's standard exit code 2. Inspect the
typed status instead of interpreting an exit code as mathematical correctness.

Real `formal_proof` runs currently return `ENV_BLOCKED` **before** adapter import
or construction, even when explicitly authorized. No accepted isolated candidate
verifier is connected. The host's hash-allowlisted authored-reference compiler is
never a model fallback. Adding an adapter alone cannot remove this gate.

An explicitly authorized `explanation_only` run can call an operator adapter.
It receives only the NL question, assumptions and conventions, with no Lean
target, imports or obligation nodes. Only an explanation is accepted; attempted
proof actions cannot reach a verifier. Error feedback also omits Lean state.
The recorded answer's semantic score remains null pending independent review.
This is the usable low-risk generation boundary, not a formal-proof baseline.

## Budgets and evidence

The driver reserves worst-case tokens and endpoint spend in `episode.json`
before generation. Unknown usage after a timeout, malformed reply, cancellation
or transport failure remains unknown, retains its reservation and stops the run.
It never retries or resumes automatically. Missing telemetry is not replaced
with invented counts. Known overuse is preserved rather than clamped to a limit.
Tool-action, verifier, total-token, request-size and time exhaustion stop further
provider calls. History is not silently truncated to fit a budget.

Async cancellation is cooperative. The driver rejects a late action but does
not claim to kill a remote job or guarantee a provider's billing ceiling. The
adapter must enforce endpoint transport and generation limits; external compute
accounting remains an operator responsibility.

Raw episodes contain model text and must stay private outside the repository.
No raw trajectory is automatically published. Share a separately inspected,
sanitized report with source/profile identities, actual exposure and costs,
failures and nullable semantic marks. Keep public-pilot, private evaluation,
authored reference and synthetic protocol results separate. Formal acceptance,
mathematical explanation quality and useful process reward remain different
labels; no combined score is manufactured.

The next real-model gate is an independently accepted isolated verifier plus a
reviewed pinned adapter and task instances. It requires no administrator contact
as part of this workstream; unavailable infrastructure remains an explicit gate.
