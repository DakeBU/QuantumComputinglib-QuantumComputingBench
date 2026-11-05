# Lean course handoff

The course is an experimental evaluator sidecar over existing shared cores.
It does not increase the mathematical question count, change canonical formal
admissions, create a hidden test set or promote the public preview to stable.
Use [COURSE.md](COURSE.md) for the versioned mathematical scope and commands.

## Current continuation

The [version-4 guide](COURSE_V4.md) extends the preserved version-3 slice below
to 21 existing cores, adding Bernstein restriction, finite
XOR cancellation and phase-aware compiler reasoning. It provides the explicit
`evaluate_agentic.py --suite course-v4` selection and a separate train-only
whole-root reference exporter. BE120 author work remains deferred because its
frozen source anchors are `Partial route`; no inventory/admission gate is
relaxed. SP116's correct specialized theorem remains diagnostic after source-scope
rejection. Version-3 counts and execution identities below are historical.

## Readiness and evidence

Authoring and review are AI-assisted. Reported zero model calls refer to
benchmark-provider/candidate experiments, not to the absence of AI assistance
in creating the exercises. Automated role separation and content bindings do
not imply human expert review or authenticate reviewer identity.

The version-3 plan contains 18 distinct existing cores: nine train, four dev
and five public test. Construction bands contain one D1, eight D2, five D3 and
four D4 items. These are provisional, exposure-dependent mathematical labels,
not measured Qwen or other model difficulty. D0 knowledge facets belong to the
same cores. An exact library application or finite decision procedure can be
much easier than the disclosed construction route.

Before using this version, run from the repository root:

```sh
python benchmarks/quantumcomputingbench/scripts/lean_course_v3.py audit
python benchmarks/quantumcomputingbench/scripts/lean_course_v3.py export \
  --split train --output _out/course-v3-train-fresh.json
python benchmarks/quantumcomputingbench/scripts/lean_course_v3.py export \
  --band D4 --mode root_only --exposure closed_book \
  --output _out/course-v3-D4-root-fresh.json
```

These commands do not run Lean or a model. Audit/export must reject missing or
inconsistent reference, semantic or historical-source evidence. Keep the full
Git history: qualification inspects exact recorded blobs. Use a merge commit
for the development PR; do not squash or rebase away evidence commits.

The machine-readable plan, fixtures and reports have distinct purposes:

- `curriculum/course-v3.json`: shared IDs, splits, prerequisites, conditional
  bands, mathematical rationales, skills and provided-obligation topology.
- `fixtures/graph-course-v3.json`: fixed authored targets, imports, reference
  blocks, comparison controls and approved declaration-only retrieval entries.
  References are public; exported agent inputs omit them.
- `reports/lean-course-v3/`: exact source-aware and source-blind bindings,
  signature evidence, source-input hygiene, actual reference receipt and
  execution checkpoint, when the required gates have completed.
- `reports/lean-course-v3/legacy-v2/`: a fresh sanitized alignment supplement
  for the unchanged second-cohort roots. This is not a new Lean replay.
- `curriculum/backlog-v3.json`: five reserved, unprepared cores, not current
  evaluation gold.

Old nine-core and 13-core plans and their receipts stay preserved. Current
reader hashes can differ after metadata hardening; the reader still verifies
the exact original Git blobs. Never relabel a historical replay as execution
of a newer reader or as fresh proof evidence.

## What the harness assesses

`root_only` permits repeated whole-root checks. `proof_dag` also permits checks
of the supplied intermediate obligations and their reuse. Both modes see the
same provided decomposition, so root-only is neither an unguided nor a one-shot
baseline. This comparison varies checking/reuse behavior, not whether the model
was given a decomposition. Neither measures autonomous decomposition discovery.
Both use complete proof blocks, not incremental Lean tactic states or a
persistent REPL fork.

`approved_interface` offers a small curated declaration/type search set;
`closed_book` disables that search. Imports remain callable in either mode.
The 13 new third-cohort entries have actual type-ascription evidence. Search
hits and graph distance receive no mathematical credit by themselves. The
Hermite endpoint example has genuine independent branches sharing a reusable
provider, but the topology remains the supplied graph, not an exported
elaborated proof-term DAG.

Keep these outcomes separate: execution legality, accepted scoped statements,
independently replayed root correctness, NL explanation/rubric coverage,
proof-method fidelity and useful search behavior. A verified statement is not
automatically a positive process reward. Wrong-type and `sorryAx` controls
exercise rejection; they are not mathematical counterexamples or measured
model repair. SP113 and BE102 contain actual mathematical witnesses.

## Safe operator boundary

Real model-generated formal execution remains `ENV_BLOCKED` until an accepted
isolated verifier is connected. Metadata/profile validation is not sandbox
acceptance. Do not use the authored-reference flag to execute model output on
the host, widen the axiom whitelist, contact administrators, reuse Cosmos3
privileges or start an inference/training service as part of this handoff.

The authored checker permits only inspected, hash-allowlisted references in a
matching pinned, already-built Lean checkout. Its third-cohort limits are
2,700 seconds per batch, 600 per supplied-DAG session, 120 per compiler check
and 180 per standalone control. It is trusted-local execution, not isolation
or matched model-compute evidence. Always choose fresh summary/raw paths;
raw diagnostics belong outside the public repository.

The fixed five-core batch requires 46 actual checks: 21 positive obligations,
ten standalone controls, ten expected negatives and five distinct final-root
replays. Controls checked once in fresh processes are not completed two-check
protocol sessions. Every proof-bearing batch ends with actual `lake build`
and `lake build Tests` in the matching production tree. Existing warning,
failure, source-audit and policy limitations remain visible.

Some finite source theorems have native-generated axioms outside the fixed
three-axiom policy. Importing their module does not taint unused declarations.
Do not silently accept an ineligible shortcut or call it mathematically false:
audit the exact transitive root axioms and retain a policy-admissible proof or
an explicit obstruction.

## Continue the curriculum

The next reserved groups are Bernstein restriction/Hermite cut rank and
loader/indicator/compiler semantics. Select a source-coherent mathematical
objective from the backlog. Preserve its contract and split; source changes
need an explicit successor rather than an easier replacement theorem.

With Lean available, seal literal roots/imports/types before proof search,
build useful obligations, audit exact shortcuts, and inspect authored proof
blocks. Require anonymous source-blind reconstruction followed by a distinct
source-aware reviewer receiving only the four-field source projection, formal
context and substantive reconstruction. Keep historical review verdicts and
author proof/binder classifications out of that packet. Bind the actual source
projection, not just a labelled item hash. Record failures and scope limits;
freeze the reviewed pipeline before real authored replay and production gates.

Without Lean, contribute source-grounded mathematical explanations, candidate
questions and correspondence proposals through the shared UUID mechanism.
Mark formal targets and reference proofs unverified. Do not invent compilation
receipts, new canonical IDs, split allocations or admission status. NL, Lean
and mixed views of one mathematical target count once.

Future model comparisons must pin model/tokenizer/template, exposure, sampling,
input/output tokens, tool calls, restarts and actual latency/cost. Keep shared
source dependencies and public-answer exposure explicit. No whole-graph
question-capacity estimate, calibrated PRM, faithful internal chain of thought,
whole-module semantic clearance or stable release follows from this course.
