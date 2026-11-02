# Lean contribution track

This folder receives formal views and proof tasks over the
[same shared cores](../../shared/CONTRACT.md) as the non-Lean track. It is not an
independent dataset with its own split allocation. Read
[the executable agent goal](AGENT_GOAL.md) and
[the proposal example](../../shared/proposal.example.json).

The local workstream now prioritizes the
[Lean-enabled agentic evaluation contract](AGENTIC_EVALUATION.md): knowledge and
precise statement understanding support proof completion, premise retrieval,
multi-node construction, incremental feedback and repair. The existing views are
warmups, not evidence that these interactive capabilities are already evaluated.
Run `scripts/lean_agentic.py audit` from the benchmark folder to inspect the
resolved frontier without executing proofs or reading gold into agent prompts.

The experimental [obligation protocol](OBLIGATION_PROTOCOL.md) adds scoped
declaration retrieval, fixed-target proof submissions, diagnostic-driven repair
and independent final replay over two existing cores. Its inspected authored
fixtures exercise the engineering protocol, with original one-call controls
retained. They are not new admitted mathematical cores, blind tests, model
scores, autonomous proof decomposition, or incremental Lean tactic states.

The [sequential proof companions](SEQUENTIAL_PROOFS.md) add prospective SP007
transfer-induction and SP008 real-probability views, with a source-blind decoder,
distinct comparison and fixed references. They remain experimental proposals.
[Capability diagnostics](CAPABILITY_SCORING.md) separately bind curated retrieval
coverage, complete canonical explanation rubrics and evaluator-owned marks;
they never turn a valid proof into an automatic NL or model score.

Prioritize exact formal views of admitted source-supported NL targets. Record
the literal imports, assumptions, target, readable correspondence, source hashes,
fixed-reference proof, axiom audit and genuine execution class. A formal target
that silently adds assumptions is not a verified view of the original question.
An API application warmup is not a deep proof-synthesis benchmark.

Use `proposals/<UUID>.json`. Existing-core contracts and splits are immutable;
semantic target changes require a separately reviewed successor. New candidates
remain uncounted until reconciliation. Semantic review, successful elaboration,
helpfulness of a tactic and isolated untrusted-output evaluation are distinct
evidence fields. Trusted local reference compilation does not certify a sandbox.

The reader path is `quantumcomputingbench/lean/`. Canonical exercise pages can
show both NL and formal views with solutions folded by default. The existing
three corrected-v3 API warmups remain a separate diagnostic reference section
until cross-cohort/core admission is resolved; they do not silently add to the
native core count.

## First native formal-view batch

[`views/native-v1.json`](views/native-v1.json) binds three existing cores:
the marginal squared-norm identity (`sp-005`), real-row Gram to complex-column
isometry (`sp-009`), and determinant preservation by a half-angle row rotation
(`la-102`). These are **library-lemma applications**, not deep synthesis tasks.
They preserve the original contracts, families and splits and add no core IDs.

The [evidence directory](../../reports/textbook-v1/formal-native/) separates a
source-blind statement reconstruction, a distinct NL/formal comparison, and
actual fixed-reference elaboration with transitive axiom checks and negative
controls. The full unchanged production proof tree passed `lake build`,
`lake build Tests`, and all 202 explicit module targets in a matching cached
checkout. The receipt records that actual checkout, not an invented current
commit build. No arbitrary model output was run on the host.

To inspect the blinded input or recheck the fixed references:

```sh
python benchmarks/quantumcomputingbench/scripts/native_views.py decoder-input --output _out/native-decoder.json
python benchmarks/quantumcomputingbench/scripts/native_views.py check-references --build-root PATH_TO_MATCHING_BUILT_CHECKOUT --trusted-local-reference --output _out/native-reference-checks.json
```

Do not overwrite sealed reports after changing the pipeline. A fresh batch or
fresh evidence review is needed when mathematical content or bound inputs change.
Kernel acceptance of these conclusions does not certify every NL explanatory
sentence, useful process reward, isolated evaluation, or a real-model baseline.
