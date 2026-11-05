# Bounded asynchronous timing pilot (C93)

This standalone synthetic experiment tests measurement provenance, not SP/BE
construction quality. It imports no ASPBE controller and changes no verifier,
acceptance anchor, score, scientific target, historical log or production
scheduler. The accompanying design is
`paper-notes/system-comparisons/uncompute-async-spbe-evaluation-design.md`.

## Frozen plan

`timing_pilot.py:PLAN` fixes two child sleeps (0.7 and 0.05 seconds), two
repetitions per arm in counterbalanced order, 5-second arm deadlines and a
5-ms polling interval. Both arms launch two processes before collecting them.
The comparison is launch-order collection versus ready-first polling. No model,
Lean or simulator calls are allowed. The parent cleans up only its own two
direct children on timeout/interruption; child code launches no descendants.
The workflow's raw source hash and canonical plan hash bind each measurement.
Source and plan are frozen before execution; any change requires a new result.

Run from this directory, with a supported Python 3.10+ interpreter:

```sh
python -B -m unittest test_timing_pilot
python -B timing_pilot.py
```

The CLI writes JSON to stdout, never a success/acceptance file. Record that
output additively as a new observation; do not overwrite historical runs.

## Interpretation and limits

The code-supported concern is in `tools/qbe.py:execute_prompt_stage`: parallel
processes are collected in launch order, with elapsed time measured when the
parent collects them. A later fast worker may therefore receive an inflated
elapsed value. This pilot reproduces that collection pattern but does not call
the controller, its model backend or its logging implementation.

Use `child_work_ns` separately from `parent_elapsed_ns`. The difference between
the child work-finish sample and parent observation includes JSON serialization,
process exit and polling delay. It is **not** a precise OS-exit observation lag.
Interpreter/import startup is outside the child's work timer. CPU deltas are
sampled intervals, not whole-process accounting. Queue time, peak memory and
tokens remain unmeasured. Nanosecond representation does not imply nanosecond
accuracy. Python documents `monotonic` as using the same clock across processes;
the runtime version and clock implementation are recorded in every result.
See the [primary Python time documentation](https://docs.python.org/3/library/time.html#time.monotonic).

Small synthetic sleeps can demonstrate a measurement artifact, not demonstrate
that proof-first, experiment-first or dual-lane quantum search is faster. A
future matched quantum ablation still needs frozen tasks/budgets, equivalent
acceptance strength, route-total costs and independently sealed held-out data.
The pilot's measurement-shape checks are not an anti-malicious-worker sandbox
or an alternative evidence-admission runtime. No timing event grants acceptance.

Rollback: remove this standalone experiment and its new checkpoint references;
production behavior remains identical. Keep the recorded result as history.
