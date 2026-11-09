# QuantumComputingBench non-Lean batch 2

This package proposes six mathematical targets: rounded Gram contraction,
approximate sequential isometries, a coherent finite-word phase supplier, sharp
column-to-operator error, residual-certified preparation error, and two-sided
approximate LCU. Each has a complete English question, reference derivation,
ten-point rubric, boundary diagnostics, scoped reasoning map and exact source
provenance. They are public, unassigned candidates, not admitted benchmark cores.

The base is current main as retrieved on 6 November 2026:
`bb260f4e27360a0d3791b40cb22638af4b086fc9`. Work occurred on the isolated branch
`codex/nonlean-batch2-20261106`. The frozen graph is
`qcb-snapshot-ffa644f0da3031a1ce754b9a`, sourced from
`86b9e677566498da04faebcf4e5ed57f177c6bb1`; its raw SHA-256 is
`71a08777e01af1b6e5bd3dd88ba6443efe9aea41240c09303d4bcc0a7cd8058b`.
All active anchors are already in that snapshot. No snapshot refresh or new
live-only node is included. Historical compiled/source inventory labels are
preserved as metadata; no Lean check was run for these new arguments.

The earlier overlapping ZIP deliveries are one twelve-packet cohort in package
`99e830bd-e868-4c7c-947c-8187a63ce46a`: four existing-core expositions and eight
unassigned candidates. All 103 files bound by its manifest were checked unchanged.
None is regenerated or counted in this batch. Existing cores, splits, quarantines,
reserved identities, releases and sealed reports remain unchanged.

## Reading order

1. [QUESTIONS.md](QUESTIONS.md) contains questions, assumptions and conventions
   without answers. [questions-only.jsonl](questions-only.jsonl) is its machine
   projection; `questions/` preserves the individually frozen packets.
2. [REFERENCES.md](REFERENCES.md) contains complete solutions and rubrics.
   [references-rubrics.jsonl](references-rubrics.jsonl) is the separate machine
   export. `qa/` is the authoritative full authored payload, including source
   roles, common errors, boundary cases, uncertainty and all map inputs.
3. [COVERAGE.md](COVERAGE.md) and [coverage-overlap.json](coverage-overlap.json)
   describe assessed deltas, shared subproofs and split conflicts.
   [COVERAGE_PLAN.md](COVERAGE_PLAN.md) preserves the pre-authoring plan.
4. [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md), [review-index.json](review-index.json)
   and `reviews/` record source-aware question-first derivations, seals, complete
   answer comparisons and adverse findings. History is retained, not overwritten.
5. [VALIDATION.md](VALIDATION.md), [HANDOFF.md](HANDOFF.md),
   [REVIEW_REQUESTS.md](REVIEW_REQUESTS.md) and [BACKLOG.md](BACKLOG.md) separate
   completed checks from decisions and mathematical suppliers still missing.

The six UUID proposal files are in the sibling `tracks/non-lean/proposals/`
directory. `manifest.json` lists their exact repository-relative paths alongside
every package file and raw-byte SHA-256. The manifest excludes itself; the outer
delivery checksum file binds it. `source-index.json` binds exact source files
and frozen graph nodes without copying a clone into the deliverable.

## Reproduce integration

Use Python 3.11 or later with the repository's existing Python dependencies.
The recorded run used Python 3.11.17 with `jsonschema` available. No Lean or
model inference environment is required. Start from a separate checkout of the
full base SHA, then either apply the supplied patch or overlay the ZIP's
`benchmarks/` tree. Do not do both. These additions do not modify main or allocate
permanent core numbers.

From the repository root:

```bash
python benchmarks/quantumcomputingbench/scripts/curriculum.py export --output _out/qcb-cores.json
python benchmarks/quantumcomputingbench/scripts/curriculum.py export-reader --output _out/qcb-reader.json
python benchmarks/quantumcomputingbench/tracks/non-lean/packages/3703ef46-1a1d-47ab-a991-dc9d94a0f386/verify_package.py
python -m unittest discover -s benchmarks/quantumcomputingbench/tests -v
python benchmarks/quantumcomputingbench/scripts/curriculum.py validate
```

`assemble.py` deterministically rebuilds projections, proposals, indexes and the
manifest from the final QA and exact review records. It does not author or repair
mathematics and refuses stale review hashes. Run it only when intentionally
rebuilding those projections, followed by `verify_package.py`. The authoring and
finite-diagnostic scripts under `evidence/` and `reviews/` are historical records;
some recreate an earlier authored version or update a recorded diagnostic. They
are not the final integration command. Do not overwrite sealed evidence to rerun
experiments; copy it into a disposable working directory first.

GitHub access was readable but `push=false`, so no branch push or PR was attempted.
Open PR metadata and the relevant Plan 208 branch packet were inspected; exact
scope and hashes are in `evidence/github-access.json` and
`evidence/pr114-comparison.json`. The current reader export, not that unmerged
packet or historical preview gold, determines current contracts. Full
owner-sealed assessment question bundles were unavailable. Persistent Goal
creation was not exposed in this session; this batch was completed synchronously.

## Evidence and reuse boundaries

Imports and ownership identify available declarations; they do not prove a
mathematical route. The graph's conceptual relationships suggest interfaces to
inspect. Author-supplied maps identify actual premises, AND joins, alternative
routes and counterexample regimes. They are not extracted Lean proof-term
dependencies. Exact-real Gram identities, register conventions and clean-column
projections make reusable premises precise; new roundoff, perturbation and
resource conclusions are derived explicitly in natural language.

All six candidates require maintainer semantic deduplication, assessed-subproof
and split reconciliation, and any admission decision. Public references are not
a hidden evaluation set; no transfer of test solutions into training is cleared.
D0 is an embedded contract-reading facet. D3/D4 labels annotate the supplied
reasoning routes and are not measured model difficulty. AI mathematical review,
structural validation, human approval and formal certification remain distinct.
The repository's existing MIT license remains unchanged; exact source license
identity is recorded in the baseline evidence.
