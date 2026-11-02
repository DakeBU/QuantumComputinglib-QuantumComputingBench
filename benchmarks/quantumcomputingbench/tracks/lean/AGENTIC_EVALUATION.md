# Lean-enabled agentic proof evaluation

Local goal started on 2026-11-03, from repository main
`ea125cfe09e0e94bfcd14ea12d1a52e01a02b9e3`. This workstream develops the Lean
assessment track. Website presentation and the separate shadow-teacher project
are not substitutes for a functioning benchmark.

## Frozen objective and evidence frontier

Assess quantum-computing knowledge and mathematical reasoning as prerequisites
for precise formal proof work: interpreting assumptions, finding premises,
constructing multi-step proofs, using Lean feedback, and repairing mistakes.
Maintain the [shared-core contract](../../shared/CONTRACT.md). Natural-language,
Lean and mixed views of one mathematical target remain one core in one split.

The first milestone is an executable audit and answer-free projection of the
existing native formal warmups, not a new question release. Obtain current
counts from the audit command rather than maintaining a parallel count ledger:

```sh
python benchmarks/quantumcomputingbench/scripts/lean_agentic.py audit
python benchmarks/quantumcomputingbench/scripts/lean_agentic.py export-warmups \
  --output _out/lean-agentic-warmups.json
```

Outputs require fresh paths. The export copies only explicit question/target
fields from the resolved catalog, preserving the core contract, item identity,
family, split and graph snapshot. Reference proofs, answers, rubrics, reviews and
solution steps are not projected. Existing references are nevertheless public:
these warmups are not blind tests or evidence of contamination-free discovery.
The new export schema is not automatically consumed by the old baseline runner.

The existing native formal views are library-lemma applications. Their exact
reference checks and semantic reviews are valuable calibration evidence, but do
not establish deep synthesis, successful tool scheduling, or kernel certification
of every sentence in their NL explanations. Current `qcb_lean` candidate syntax
is a restricted application grammar, not general Lean tactic blocks. Its
isolated candidate execution gate remains disabled. This milestone changes none
of those boundaries and executes no candidate proof.

## Capability slices to implement and validate

1. **Knowledge and statement understanding.** Preserve the actual domain,
   quantifiers, dimensions, normalization, phase/register conventions and resource
   model. Use independent semantic rubrics; a knowledge answer is not a Lean
   certificate. Withheld cores stay out of current gold.
2. **Proof completion / library application.** Retain existing easy warmups as
   explicitly labelled baselines. Do not conceal a one-call solution to inflate
   apparent reasoning depth.
3. **Premise retrieval.** Freeze task-specific admitted declaration interfaces.
   Measure relevant-premise and complete-route coverage, with all AND premises.
   Keep implementation imports, conceptual transports and reviewed inference
   edges distinct. Do not expose held-out answers through search results.
4. **Multi-node construction.** Select genuinely composed targets supported by
   current local formalization. Review the composition, not just the existence
   of its ingredients. Graph distance, import depth, distinct premise count and
   semantic reasoning steps are different quantities; unknown depth stays unknown.
5. **Incremental feedback.** Evaluate complete parseable blocks, record parent and
   child states, retain failed attempts, and independently replay the final proof
   of the unchanged root. Restoring a Lean state does not undo IO.
6. **Diagnostic-driven repair.** Bind attempts to task/context/dependency versions.
   Distinguish implementation errors, unavailable APIs, resource failures and
   checked mathematical counterexamples. Accepted execution is not automatically
   useful progress or a positive PRM label.

These are requirements, not six already implemented evaluators. The audit
reports the implemented frontier and gaps explicitly. New mathematical targets
use the existing proposal/reconciliation process; new modes never manufacture
new core IDs. Planned graph nodes may motivate future/source-grounded tasks but
cannot be promoted into locally kernel-verified test claims.

## Agent protocol and comparison requirements

The obligation milestone defines evaluator-owned, versioned interactions for
bounded declaration retrieval, fixed-target verification, and (where supported)
tactic-state execution. Agent output may not change imports, hypotheses, target,
split, reference corpus, axiom policy or budget. Persist exact actions,
observations, failures, replay identities and costs. Never infer semantic
alignment from a successful formal subclaim.

Compare full-proof attempts, incremental short blocks and longer complete
blocks under identical task/model/exposure settings and declared ceilings.
Record realized input/output tokens, verifier calls, elapsed time and retained
prefixes. Those strategies change more than feedback timing; an advantage is
initially a strategy result, not a causal attribution to early feedback alone.
Keep retrieval conditions as a separate factor. Public-reference warmups and
future private evaluation instances must never be pooled as a blind score.

## Local verification and stop conditions

Use only inspected repository-authored reference proofs for trusted local Lean
checks, with exact compiler/library and source digests, transitive axiom audits,
and actual sorry/wrong-target negative controls. Historical receipts remain
historical; a matching proof-input digest does not turn an older checkout into
the current main commit. Run the repository Lean gate for proof-bearing work.

Untrusted model-generated proof execution requires a separately accepted
isolation boundary. The experimental no-admin bwrap work on newton05 does not
automatically enable this repository's verifier. Do not contact administrators,
repurpose Cosmos3 privileges, execute arbitrary generated Lean on the host,
download model weights, or start GPU training or unattended model batches.

Finish each milestone with code/data identities, actual tests, covered targets,
exposure and leakage checks, and unresolved limitations. Do not declare a stable
release, source review, sandbox acceptance or measured model result by renaming
a version or filling a metadata field. The website may later project these
verified distinctions using the existing system, but a render is not an
evaluation gate.

## Initial local checkpoint

The first code milestone adds `src/qcb_agentic.py`, `scripts/lean_agentic.py`
and regression tests. It adds no mathematical core, formal-view admission,
agentic executor, new theorem or model score. Current counts and uncovered IDs
are generated by the audit from the resolved registry, not maintained here.

Validation on 2026-11-03:

- The full benchmark suite passes 182 tests and 226 subtests, including seven
  new projection/frontier tests. Ruff, Python compilation and whitespace checks
  pass for the new code.
- `curriculum.py validate`, the frontier audit and warmup export succeed.
- Fresh `lake build` and `lake build Tests` succeed in the clean cached checkout
  `../Quantum-Computing-Block-Encoding` at
  `f2cba045611a0d11c5995c29607569726bf1d6c5`, using installed Lean 4.29.1.
  Existing linter warnings remain; this is not a warning-free claim.
- The cached checkout and current benchmark tree have matching production
  proof-input digest
  `1e65e7d2984e4542ca2747837d71c516847e4e987d3bbd6c48b8a803eb36806e`.
  The existing `native_views.py check-references` command freshly checks the
  three inspected references and rejects actual sorry/wrong-type controls.
  The receipt is `trusted_local_reference`, explicitly not isolated candidate
  evaluation. Its digest is
  `bbbe3b15fcccd82c4a5ffa96d3309fc4393411d10327525d2439d9889c782042`.

Fresh local artifacts are under `_out/lean-agentic-20261103/`: the frontier
audit, answer-free warmup inputs and native reference replay. Previously sealed
receipts and frozen releases were not overwritten. This does not certify every
NL answer, refresh an old receipt's recorded commit, or enable generated proofs.

## Bounded obligation milestone

The [experimental obligation protocol](OBLIGATION_PROTOCOL.md) now implements
scoped search, fixed-node proof checks, version-bound repair and fresh root
replay. It includes two existing roots with inspected nontrivial constructions,
alongside the original direct library applications. Its supplied decomposition
is not autonomous agent planning or a Lean tactic-state REPL. Intermediate
obligations remain experimental, not new semantic/formal admissions.

The [source-aware review](../../reports/lean-agentic-v1/protocol-review.json)
records exact inspected file hashes, mathematical scope, five concrete fixes and
the limits of that review. The fixed pilot has operator-only reference proofs
and assumption/mechanism rubrics. Its exported agent inputs omit those bodies
and answers. Actual model use remains blocked pending an accepted candidate
verifier and an authorized model adapter; public references remain public.

### Actual authored execution checkpoint

The [sanitized execution summary](../../reports/lean-agentic-v1/execution-summary.json)
binds the tested code, fixture, pipeline sources, actual Lean runtime and cached
library checkout. The final 300-second authored profile passes all six
conditions over the same two existing cores: original lemma application,
self-contained whole-root construction, and provided-DAG repair for each core.
There are 22 actual Lean checks: 20 verified and two deliberately ill-typed
attempts rejected, including six successful fresh final-root replays. Verified
roots use only the approved standard axioms. This admits no new core or formal
view and measures no model.

The matching production tree passes `lake build` and `lake build Tests`, with
existing linter warnings. The current benchmark suite passes 203 tests and 226
subtests. Exact identities, per-condition budgets/costs, the five reviewed fixes,
and remaining boundaries are in the linked reports.

The earlier complete 180-second draft is preserved under
`_out/lean-agentic-20261103/obligation-smoke-v1.json`: all obligations checked,
but the row-rotation final replay timed out and the overall run failed. The
successful run is a separate receipt, not an edited pass label. Its local raw
receipt is `obligation-smoke-300s.json`; the exported proof-free inputs are
`obligation-agent-inputs-reviewed.json`. Historical sealed releases and the
independent non-Lean contributor track are unchanged.

Next frontier: complete semantic admission of new decompositions and graph-
supported targets, connect the isolated verifier/model adapter, and measure
retrieval, reasoning and repair with actual model/token identities. Inspect
formalization before selecting compositions; neither graph distance nor a
provided-node count substitutes for mathematical reasoning depth.
