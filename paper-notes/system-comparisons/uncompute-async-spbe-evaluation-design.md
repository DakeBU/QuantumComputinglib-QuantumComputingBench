# Asynchronous proof and experiment lanes for SP/BE construction evolution

Status: design and bounded app-coordinated execution policy, not an implemented
production scheduler or a measured efficiency improvement. This refines the
human's 18 October 2026 priority for digesting arXiv:2610.22367v1 and applying
its mechanisms to SP/BE. Canonical scientific targets, candidate/trial ledgers,
publication gates and scoring remain unchanged.

## 1. Decisions that belong to the user

Ask before a materially new scientific or resource trade-off: changing the
target state/operator, weakening precision or success requirements, adding a
stronger oracle assumption, exceeding an authorized spending/compute envelope,
or choosing between incomparable application goals. Show the alternatives,
their assumptions and evidence, their costs, and what decision each unlocks.
Existing explicit authorization, including a frozen tolerance ladder, does not
require the same question at every already-authorized step.

Within the frozen contract and authorized envelope, the harness may choose
ordinary tactics, retrieval queries, bounded diagnostics, proposal variants and
which dependency-ready fork runs next. Asking the user about every tactic or
worker assignment is not the desired interface. The user can override this
policy at any time. An unresolved preference must not be silently converted
into a changed scientific target.

## 2. Two lanes, different evidence

```text
                       frozen contract + candidate revision
                         /                         \
        proof / symbolic refinement         executable / finite screening
        source -> Lean -> review            output + phase + cleanup + cost
                         \                         /
                         typed, digest-bound evidence
                                     |
                     select the next dependency-ready action
```

The lanes may proceed concurrently when they resolve independent uncertainty.
A finite experiment can cheaply falsify a concrete candidate or inform a proof
strategy; a proved invariant can remove an invalid experiment domain. Neither
lane waits for every unrelated worker to finish. Both consume the same frozen
contract and exact candidate bytes, not a shared mutable "latest" candidate.
When one lane changes a candidate, that creates a successor version rather
than silently reusing the other lane's old result.

The join is an evidence gate, not a vote or averaged confidence. A finite pass
cannot close a symbolic family theorem, and a scalar/integer Lean theorem
cannot accept its circuit export, phase, workspace cleanup or finite-bit cost.
The full root retains ALL required evidence. Source-first/own-formal-first
seals precede decoder release; asynchronous scheduling never bypasses those
anti-anchoring barriers.

## 3. Event-driven decisions and local retirement

Each event binds task ID, workflow version, contract digest, candidate ID and
revision, parent lineage, evidence layer, artifact digest, producer identity,
measurement provenance, and explicitly unknown fields. Events are appended to
the existing run/candidate/trial evidence, not a second competing acceptance
database. The parent verifies bytes and reruns applicable deterministic gates;
an agent's success JSON is not acceptance.

| Event | Next action | What it cannot authorize |
| --- | --- | --- |
| Reproduced counterexample on the exact contract | Retire that revision's affected claim; preserve witness; salvage independent verified fragments | Retire a different contract or all mechanisms in the family |
| Finite tests and measured resources pass | Queue the missing symbolic/refinement obligation; retain the candidate as promising | Certified population winner, uniform BE guarantee, or source closure |
| Focused Lean theorem closes | Unlock exact dependency consumers and independent review | Executable export, full integration or resource success |
| A compatible interface is verified | Permit a named mutation/crossover proposal using its exact assumptions | Inherit a parent's certificate after changing its contract |
| API/environment/timeout failure | Route bounded repair or defer the specific computation | Declare mathematical impossibility |
| Stale or mismatched revision arrives | Archive as stale; do not advance current frontier | Refresh acceptance by renaming the artifact |
| Materially new trade-off appears | Ask the user with a compact comparison | Change target, oracle, scoring or failure budget silently |

Before launching another expensive fork, state its distinct uncertainty,
expected information gain and discriminator. A cheap exact discriminator is
preferred when available. There is no unsupported claim that a universal
information-gain scalar is calibrated. Keep a small complementary portfolio
when routes win in different regimes; do not impose one global champion.

Retirement is local to the failed version/dependency cone. Stop or redirect
stale dependent work at a safe checkpoint; do not kill unrelated useful work
or discard frozen proofs. Shared Git writes remain parent-serialized. Separate
task scopes or isolated checkouts protect simultaneous authoring. Compiler and
simulator concurrency must fit measured aggregate memory headroom and reserves;
"parallel agents" does not require running multiple heavy compilers together.

## 4. Real measurement boundary in the current CLI

`tools/qbe.py:execute_prompt_stage` currently starts parallel processes together,
but calls `wait_agent_process` and `log_agent_attempt` in launch order. Its
reported `time.perf_counter() - start` is computed when the parent collects each
process, not necessarily when that process exited. A quick second process can
therefore receive the slow first process's observation delay. This is a
code-supported measurement limitation, not evidence that a strategy is slow.

`log_agent_attempt` already records wall time, prompt characters and an input
token proxy with `exact_token_accounting=False`.
`tools/qbe_control.py:write_control_state` and `prompt_budget_violation` already
maintain estimated input budgets. `summarize_candidate_population` already
checks active lineage, mutation/crossover parents and selection eligibility.
Reuse these mechanisms; do not add a second mutable population state or
replace their stale/evidence protection with free-form asynchronous messages.

The next low-risk instrumentation experiment should distinguish:

- enqueue time and queue delay;
- actual worker start and child-observed exit time;
- parent observation time and observation lag;
- candidate proposal time, first finite discriminator, first Lean closure,
  independent acceptance and export closure;
- provider/model invocation count versus actual provider-internal calls;
- exact input/output tokens where exposed, separately labelled proxies and
  unknowns otherwise;
- total CPU/compiler/simulator/model work and peak memory, not only elapsed
  wall time or the fastest successful worker.

Do not infer per-worker tokens from account/Goal totals, treat exit0 as a
mathematical acceptance, or present parent-observed elapsed time as exact child
runtime. Existing historical measurements are not rewritten.

## 5. Minimal controlled efficiency experiment

Hypothesis: completion-event scheduling reduces idle/observation delay without
changing accepted mathematical claims or increasing total work excessively.
This is a hypothesis, not a result from the paper or this repository.

First use deterministic synthetic child processes with deliberately different
durations, including a fast later-launched child. Compare existing stage-barrier
collection with a proposed event-driven measurement/dispatch adapter. Tests
must include out-of-order completion, concurrent completion, failure, timeout,
duplicate events, stale candidate digests, mismatched contract, interruption,
and a forged success result. Preserve launch-order outcome reporting if needed
for compatibility; completion timing can be measured independently of ordering.
Do not alter controller scoring or acceptance to make the experiment pass.

Then use a small frozen set of matched quantum Lean/implementation obligations
under the same model, concurrency limit, context policy and per-task budget:
proof-first, experiment-first, and bounded dual-lane variants. Public source
tasks are training/reproduction tasks, not clean held-out generalization data.
Claim generalization only after separately generated/sealed held-out tasks and
retrieval exclusions exist. Each arm needs the same target semantics and
acceptance strength; do not compare a finite screen's time to a family proof's
time as though they were the same deliverable.

Metrics: accepted closure rate, time to the first useful discriminator and to
matched-layer acceptance, total resource/model cost, unsuccessful work,
reusable verified output, orchestration-only time and observation lag. Report
per-task paired outcomes and censored/failed runs, not only winners. Set budgets
before execution. Stop on the fixed budget, unchanged repeated route failure,
unsafe headroom, or an integrity violation; classify the stop honestly.

Required artifacts are the frozen split and budgets, workflow revisions,
append-only event trace, candidate lineage, raw timing provenance, exact Lean
and executable gate records, failure classifications and a paired comparison.
Any production adapter comes only after focused tests and a reversible pilot;
this design does not implement or empirically validate that adapter.

## 6. SP/BE-specific acceptance remains unchanged

For function-oracle -> amplitude transduction -> SP/diagonal BE, retain coherent
function semantics, domain/scaling, approximation norm, rotation synthesis and
uncomputation. SP additionally retains normalization, postselection probability
and amplification cost; BE requires the advertised uniform block/operator
guarantee. For LCU, PREPARE, SELECT and unprepare with exact coefficient/phase
normalization are jointly required. Record classical data generation/storage,
oracle construction/queries, Toffoli/other gates, depth, peak qubits, cleanup,
finite precision and readout. TQ or a fast finite sample cannot replace them.

New best-known resources are an outcome to test against an explicit matched
baseline, not a promised stopping condition. A scoped rigorous obstruction is
valuable; an environment or review gap is not a mathematical obstruction.

## 7. Choosing the lanes without making the user a scheduler

The user's refinement is an asynchronous decision policy, not a permanent
choice between rigor and experiments. An experiment-first route still owes the
same mandatory symbolic certificate. A proof-first route still owes any
required executable and resource gates. Choose the next action from the
current uncertainty and a bounded discriminator, not the route's label.

| Current uncertainty | Default within the authorized contract | Ask the user when |
| --- | --- | --- |
| A cheap exact example may disprove the literal target | Run that discriminator before expensive search | The proposed response would change the target rather than reject the candidate |
| Symbolic refinement and finite implementation behavior can be investigated independently | Run bounded proof and experiment lanes concurrently if aggregate memory and compute headroom permit | Their combined cost would exceed the authorized envelope |
| The experiment needs an unprovided coefficient, phase convention or error reference | Resolve the source/interface first; independent unaffected work may continue | More than one scientifically inequivalent interpretation remains |
| Only tactic, retrieval or implementation technique differs | Select or compare autonomously with exact revisions and bounded costs | The alternatives introduce materially different oracle or physical assumptions |
| Two routes have incomparable resource/error/success trade-offs | Retain a small non-dominated portfolio with explicit regimes | An application preference is needed to choose the final trade-off |

A compact user decision card contains the unresolved choice, options with
assumptions and evidence, incremental cost/unknowns, the recommended option and
the downstream obligation it unlocks. Ask asynchronously while continuing only
already-authorized unaffected work. No answer is not consent to a changed
target or enlarged budget. There is no need to interrupt the user for every
test or worker assignment.

At each useful completion event, verify contract/revision/artifact bindings,
classify the evidence, update the affected dependency cone, and dispatch the
next ready action without waiting for unrelated lanes. A stop request retires
only affected work at a safe checkpoint; already consumed work and pending
partial results remain in the cost record. Do not interrupt a live, useful
proof merely to manufacture a scheduling event. Source-blindness barriers are
dependencies too: early results cannot be disclosed to a reviewer before its
required independent freeze.

The next matched comparison has three arms: proof-first; a bounded finite
screen followed by proof when the candidate survives; and concurrent bounded
proof plus screen. Freeze the task instances, endpoint evidence layer, resource
caps, seed policy, environment and stopping rule before running. All arms must
reach the same endpoint to count as successful. A faster finite screen is a
discriminator result, not a faster theorem. Counterexample discovery time is
reported separately from accepted-closure time. Budget-exhausted or interrupted
arms are censored/failed as appropriate, never omitted from the denominator.

Report paired per-instance outcomes before aggregates: matched-layer closure,
time to useful information, time to independent acceptance, total model calls
and known/proxy tokens, CPU/compiler/simulator work, peak memory, stale/cancelled
work, and parent reconciliation cost. More concurrency can lower latency while
increasing total cost; report that trade-off rather than declaring a universal
winner. Choose by feasibility and non-domination under the frozen application
contract, not a new unapproved scalar score. Changes to production scheduling
or scoring require their own tested, reversible follow-up.

### Current evidence and next boundary

The isolated [C93 timing pilot](../../experiments/uncompute-2610-22367/async-timing-c93/RESULT.md)
shows earlier observation of a fast later-launched child (656/671 ms versus
16/16 ms), not a reduction in whole-pair time (844–859 ms), mathematical work
or quantum-resource cost. It is not the three-arm quantum comparison above.
No measured superiority of experiment-first, proof-first or dual-lane SP/BE
search is established. Missing per-worker provider telemetry remains unknown.

For the paper's Gaussian example, source topology and error-reference
interpretation must be settled before freezing a code-refinement statement.
Once that interface is sealed, symbolic integer/phase/cleanup refinement and a
bounded independent fixed-witness diagnostic may run in parallel. Reproducing
the supplied witness is distinct from rerunning the authors' large parameter
search. Numerical additive error alone cannot certify state/operator distance,
normalization, amplitude conversion, uncomputation or the final SP/BE root.
