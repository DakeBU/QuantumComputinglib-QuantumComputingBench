# Non-Lean State Preparation contribution cohort

This is an additive, unadmitted cohort for QuantumComputingBench: **12 complete
contribution packets, comprising four existing-core views and eight candidate
targets**. `COHORT.md` is the readable complete question/answer/rubric collection;
`qa/*.json` are the authoritative payloads. `CONTRIBUTIONS.md` and `manifest.json`
give the exact final identities, splits, content digests and actual review status.

The cohort concentrates on normalization, clean block projection, coherent phase,
register conventions, tensor-train algebra, polynomial sampling and conditional
precision costs. It proposes no permanent core numbers. D0 is a knowledge facet;
D1–D4 describe provisional reasoning routes rather than measured model difficulty.

## Baseline and preservation

| Binding | Exact value |
| --- | --- |
| Repository | `DakeBU/QuantumComputinglib-QuantumComputingBench` |
| Current-main base | `6b23dab68c2970062ddfd568ce94bce74b566483` |
| Base tree | `2ed1159e1973e65295c3e2a7dce73efc79244caf` |
| Working branch | `codex/nonlean-cohort-20261103` |
| Frozen snapshot | `qcb-snapshot-ffa644f0da3031a1ce754b9a` |
| Snapshot source commit | `86b9e677566498da04faebcf4e5ed57f177c6bb1` |
| Snapshot file SHA-256 | `71a08777e01af1b6e5bd3dd88ba6443efe9aea41240c09303d4bcc0a7cd8058b` |
| Resolved catalog hash | `5269b9f2521e3bf14db293fea34895f6e44a387c2479c164407b4d16dd9a2247` |
| Retained / reserved | 198 / 15; original historical obligation scope 213 |
| Frozen graph inventory | 5,153 nodes; 5,200 edges; 10 conceptual hyperedges |

The current policy-resolved export, not historical preview answers, supplied the
four immutable existing contracts. SP006, SP007 and LA015 retain `test_public`;
SP114 retains `dev`. Every one of their nine contract fields is unchanged.
These are proposed views, not installed answer replacements. Existing Lean
companions remain views of the same cores. No reader policy, reserved identity,
production Lean source, Lean-track file, generated website page, old report or
frozen release is edited.

All candidate identities have `candidate:<UUID>`, `candidate_not_counted` and
`dedup_review_required: true`. Their splits remain
`unassigned_pending_reconciliation`. All materials are public diagnostics;
public solutions are not a hidden evaluation set, and no training transfer or
independent train/test pooling is authorized. No out-of-snapshot node is used by
an active proposal. `appendix/` describes the required future refresh boundary.

## Read the package

| File or directory | Purpose |
| --- | --- |
| `COHORT.md`, `qa/` | Complete self-contained questions, rigorous answers, ten-point rubrics, mistakes, boundary cases, difficulty rationales and author-supplied reasoning maps |
| `CONTRIBUTIONS.md`, `OVERLAP.md` | Final contribution and semantic/split-overlap tables |
| `coverage-plan.json`, `coverage-amendment-B3.json` | Plan frozen before drafting and explicit replacement of an overlapping generic circuit-error idea |
| `evidence/coverage-audit.*` | Full current question inventory, nearest-target comparison, reservations, legacy screening and source checks |
| `SOURCE_AND_GRAPH.md`, `evidence/source-graph-index.json` | Exact graph/source anchors and evidence classes |
| `GRAPH_AND_REUSE.md` | Reading/import/conceptual/proof distinctions, AND joins, shared lemmas and incompatible conventions |
| `blind/`, `reviews/` | Frozen questions, actual question-first independent derivations, original findings and exact-content comparisons |
| `REVIEW_SUMMARY.md`, `REVIEW_REQUESTS.md` | Resolved findings, honest review limits and still-required maintainer decisions |
| `OPEN_PR_RECONCILIATION.md` | Corrected 16-open-PR listing, bounded conflict audit and branch-only evidence limits |
| `VALIDATION.md`, `evidence/*tests*`, `evidence/curriculum-validate.log` | Exact commands, outcomes, initial environmental failure and corrected rerun |
| `GOAL.md`, `NEXT_COHORT.md`, `HANDOFF.md` | Resumable objective, completed milestone and prioritized remaining work |
| `manifest.json` | Relative file paths and SHA-256 hashes, exact base/snapshot identities and contribution statuses |

The manifest's file list excludes the manifest itself to avoid recursive hashing.
The delivery-level `SHA256SUMS` additionally binds the manifest, patch and delivery
receipt. Raw-file hashes and canonical `qcb_core.digest` item hashes are explicitly
distinguished. Old draft/review files under `evidence/history/` and `*-review-v1.json`
are audit history, never alternative current answers or transferred approvals.

## Apply without changing main

Use a clean isolated checkout or worktree at the exact base above. The ZIP contains
only the two additive contribution locations and supporting delivery evidence.
Either copy its `benchmarks/` subtree into the checkout **or** apply the included
`contribution.patch`; do not do both. With Git, first inspect:

```sh
git rev-parse HEAD
git apply --check /path/to/contribution.patch
git apply /path/to/contribution.patch
```

If main or the source snapshot has advanced, inspect the changed contracts and
sources before rebasing. Do not rewrite hashes to force compatibility. Source
migration PR86 and question-successor PR114 especially require reconciliation;
their reported branch counts and verification do not replace this baseline.
The existing proposals are advisory conflict checks, not distributed locks.

## Reproduce the checks

Use a supported Python environment; this run used Python **3.11.17** and
`jsonschema==4.26.0`. The repository dependency declaration is
`benchmarks/quantumcomputingbench/requirements.txt`. Lean is unnecessary for this
package and was neither installed nor executed. A writable temporary directory
**outside the repository** is needed by the existing safety tests. Set `TMPDIR`
to such a directory before running the following from the repository root:

```sh
python -m unittest discover -s benchmarks/quantumcomputingbench/tests -v
python -m unittest website.scripts.test_quantumcomputingbench -v
python benchmarks/quantumcomputingbench/scripts/curriculum.py validate
python benchmarks/quantumcomputingbench/tracks/non-lean/packages/99e830bd-e868-4c7c-947c-8187a63ce46a/verify_package.py
```

The first benchmark test attempt used an unsuitable sandbox fallback temporary
directory inside the checkout; the existing guard rejected fixture output there.
The original failure log is retained. Setting an external `TMPDIR` fixed the
environment, and all 317 benchmark tests passed. All 25 website tests passed.
No validator was relaxed and no model inference was run; evaluator-related tests
use their existing mocked/fixture paths. `VALIDATION.md` records the additional
integration checks and exact limitations.

To reproduce the readable companion, run `render_cohort.py` in this package.
`build_metadata.py` regenerates proposal wrappers and source/overlap inventories
from the authoritative payloads; `--manifest` also rebuilds the inventory and
requires all actual review reports. It refuses stale content digests and changed
catalogs. A regenerated manifest is not approval of edited mathematics: edited
payloads require new exact-content review first. `verify_package.py` checks
compatibility, file/source hashes, unchanged contracts, question-freeze continuity
and review bindings, not mathematical truth.

To reconstruct the baseline exports, use the existing `curriculum.py export`
and `export-reader` commands with `--output` pointing outside the checkout.
Baseline export hashes are recorded in `evidence/baseline.json`; no historical
reader or preview was overwritten. The required unit suites test repository
behavior; they do not certify these English answers or admit candidates.

## Remaining gates

The independent reviewers are actual AI agents, distinct from the packet authors.
They first derived answers from frozen questions and named sources, then compared
the complete proposed answers, rubrics and maps. Prior coverage/source exposure
is disclosed, especially for group C. This is not human approval or a new Lean
check. Maintainers still need to decide semantic distinctness, specialization,
split handling and whether to install any view or admit any candidate. B2 is the
highest overlap risk. Resource assumptions remain conditional, especially actual
finite-bit angle/phase suppliers and gate synthesis.

Repository access was read-only (`push: false`), so no remote branch or PR was
created. The delivery includes coherent local commits and an applicable patch.
No main merge, stable release, deployment, whole-graph coverage or measured model
performance is claimed. The runtime exposes no persistent Goal-creation API;
`GOAL.md` is the resumable work ledger, not a fabricated hosted Goal identifier.
