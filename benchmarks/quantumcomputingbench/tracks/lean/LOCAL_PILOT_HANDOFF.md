# Lean-enabled local pilot handoff

This checkpoint implements the first evaluation slice for agentic
quantum-computing proof AI. Knowledge and reasoning support precise proof work;
website presentation and the separate Leanlib shadow-teacher system do not
substitute for evaluation. This is a local engineering/reference checkpoint,
not a stable benchmark release or a model leaderboard.

## Delivered evaluation slice

- Four experimental views preserve existing core IDs, contracts, families and
  splits. They cover marginal normalization, row-rotation determinant
  preservation, sequential transfer induction and real total probability.
  The last two have separately reconstructed/reviewed mathematical contracts
  and remain companion proposals rather than canonical formal admissions.
- Fixed-target complete proof blocks, scoped interface search, a supplied
  obligation frontier, retained failures/repairs and independent fresh-root
  replay are implemented. The protocol does not provide a tactic-state REPL.
- Each reference task retains a direct library control and an authored
  construction. One-call shortcuts are disclosed. Provided node count is not
  mathematical depth; neither strategy establishes autonomous decomposition.
- Capability diagnostics keep full canonical explanation rubrics, AND/OR
  retrieval coverage, reviewed semantic marks and formal outcomes separate.
  Unreviewed answers receive null semantic scores, not automatic full credit.
- One registry validates exact recorded evidence and exports answer-free inputs.
  One bounded model-action loop supplies zero-call plans and simulation smokes;
  real formal execution is blocked before loading an adapter.
- Raw episodes stay outside the repository. Frozen data, old failed runs,
  collaborator work, canonical catalog counts and the non-Lean track are
  preserved. The website and published releases are unchanged.

Read [EVALUATOR.md](EVALUATOR.md) for the unified commands, profiles, adapter
contract and accounting limits. The [final software checkpoint](../../reports/lean-agentic-registry-v1/execution-summary.json)
binds the exact source freeze, tests, synthetic runs, negative gates and
unchanged catalog. Its [independent implementation review](../../reports/lean-agentic-registry-v1/protocol-review.json)
records both corrected cost-control defects and the review's actual scope.

## Actual mathematics and Lean evidence

The two authored execution checkpoints are deliberately separate:

- [Obligation pilot](../../reports/lean-agentic-v1/execution-summary.json):
  SP005 and LA102, with library application, whole-root construction and
  provided-DAG repair; 20 verified checks, two expected type failures and
  six fresh final-root replays.
- [Sequential companions](../../reports/lean-agentic-capabilities-v1/sequential-execution.json):
  SP007 and SP008, with the same three comparison conditions; 16 verified checks,
  two expected type failures and six fresh final-root replays.

These are actual inspected repository-authored Lean executions on pinned Lean
4.29.1 and the matching cached production library, with approved transitive
axioms. The production tree also passed `lake build` and `lake build Tests`;
existing linter warnings remain. Execution records retain their original code
and library revisions. New registry validation reads historical Git blobs as
data and does not rerun or relabel those checks. The larger canonical native
warmup cohort remains separately documented and is not added to these counts.

Correctness of the fixed roots does not certify the full requested exposition,
all NL answers, useful process rewards, sandbox safety, or model performance.

## First commands on another machine

Use a separate clean checkout and preserve existing work/results. Run from the
repository root with Python 3.11 and the existing benchmark test dependencies:

```sh
python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py validate
python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py list
python -m pytest benchmarks/quantumcomputingbench/tests -q
python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py run-fixture \
  --view qcb-agentic-sp-007-v1 --mode proof_dag \
  --episode-dir ../qcb-eval-private/sp007-fixture-fresh
```

The first two commands validate recorded evidence without Lean. A fresh
clone must include the original evidence history; integration must preserve
the recorded commits using a merge commit rather than squash/rebase.
The [offline profile commands](EVALUATOR.md#operator-adapter-and-frozen-model-profile)
generate an intentionally unfilled operator template and validate the completed
metadata/budgets without importing adapters or loading the task corpus.

A fresh reference replay additionally needs the exact already-built library checkout,
pinned compiler and explicit trusted-authored-reference flag. For example:

```sh
python benchmarks/quantumcomputingbench/scripts/sequential_proofs.py check-references \
  --build-root PATH_TO_MATCHING_BUILT_CHECKOUT --trusted-local-reference \
  --output _out/sequential-authored-replay-fresh.json
```

The replay accepts only the inspected authored proof allowlist. It is not an
entry point for arbitrary candidate proofs. Finish any proof-bearing run with
the repository's production Lean build and Tests gates in that matching tree.

## Follow-on gates

1. Reconcile companion proposals through shared formal-view admission while
   preserving the partial whole-question explanation scope. Do not count them
   as extra independent mathematics or silently change the existing split.
2. Independently review an actual isolated verifier and its resource limits.
   The no-admin experimental backend from another project is not automatically
   accepted here. Do not contact administrators or reuse Cosmos3 privileges.
3. Review and pin a real Qwen/model adapter, actual checkpoint/template and
   bounded profile. Start with an explicitly authorized small smoke. A larger
   model changes its profile and realized compute, not the core definition.
   Do not start GPU training or an unattended batch as part of this checkpoint.
4. Admit independently reviewed private instances/families before claiming
   contamination-free performance. Public pilot references remain public;
   hiding a local answer field does not make them blind tests.
5. Measure actual knowledge, premise use, reasoning/repair and costs separately.
   Report real input/output/thinking tokens, verifier calls, latency and
   endpoint/compute accounting. Equal nominal token caps are not matched compute.
6. Add a persistent incremental tactic-state executor only if that becomes an
   evaluation target. Do not rename the current obligation protocol to imply it
   already measures that capability.

Stable release, broader graph coverage and website publication require their
own unresolved mathematical/source, deduplication and publication gates. This
handoff neither clears them nor automatically resumes website deployment.
