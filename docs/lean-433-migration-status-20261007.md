# Lean 4.33 migration and curriculum acceptance

Date: 7 October 2026.

The project toolchain is pinned to Lean 4.33.0, with Mathlib and
VersoBlueprint on their corresponding `v4.33.0` revisions. The local compiler
has been checked as 4.33.0. An upstream package's toolchain declaration does not
override this root pin; all local acceptance must run with the root compiler.
In particular, the selected VersoBlueprint `v4.33.0` revision declares
4.33.1 in its own checkout. That declaration is not a local 4.33.0
compatibility result: the Blueprint's assembly has now actually compiled
with the root 4.33.0 compiler; HTML generation is checked separately below.
No automatic switch to 4.33.1 is authorized by this dependency declaration.

## Compatibility changes

The migration repairs tactic/API differences in existing finite-matrix,
rotation, reversible-circuit and tensor-train proofs. Explicit finite indices,
matrix-entry adapters and product identities replace brittle implicit
rewrites. A few physical PREPARE proofs use the narrowly scoped
`backward.isDefEq.respectTransparency false` elaboration option. This restores
implicit definitional unfolding; it does not bypass kernel checking.

The Windows Verso search-asset patch now recognizes only the new, exact pinned
Verso revision and its reviewed source pattern. Unknown pins/layouts still fail
closed. The technical-lemma registry checker additionally rejects a compiled
entry whose recorded Lean version differs from `lean-toolchain`.

The real 4.33 Blueprint HTML exposed a second compatibility boundary: Verso's
search initialization now passes search/document priorities and a search-page
path. The declaration adapter initially rejected that new shape. It now
accepts the two inspected call/import pairs only, preserves the initializer
unchanged, and rejects mismatched imports, extra calls or unknown arguments
before writing an adapter. The new positive and negative regression tests pass.

The first assembled-site check then exposed two real renderer migrations: the
declaration catalog still generated the old external-declaration anchors, and
the no-preview-data mode referenced a page runtime without emitting it.
The catalog now uses the inspected 4.33 statement anchors. The generator's
no-preview-data branch now emits the official runtime dependency closure via
VersoBlueprint's public emitter; it does not invent a preview manifest or
cached source fragments. Catalog regressions and compilation of the generator
pass. Fresh HTML and the unchanged assembled-site checks subsequently confirmed
the fix; the earlier failed check remains a failure, not a retroactive pass.

The path scanner now includes emitted `.mjs` modules. Its new regression also
exposed a detection gap for JSON/JavaScript-escaped Windows separators. The
scanner checks a detection-only unescaped view, leaving code rewriting and
canonical inline-xref serialization unchanged. The full sanitizer regression
suite and the fresh Blueprint path scan pass.

The native Windows aggregate build now runs the process-memory check already
required by the canonical shell build. The existing parity tests caught the
missing step; both entry points still propagate failures instead of skipping
them.

Website source-link eligibility is now checked once per module in each
inventory pass, rather than once per declaration. The cache is local to that
pass: line anchors remain exact, dirty sources remain unlinked, and a subsequent
build performs fresh checks. A regression test covers those boundaries.

The final site's required-artifact check now rejects missing files, directories
and empty files. It explicitly requires all four peer textbook pages and the
generated curriculum catalog. A regression test covers both the rejected cases
and a valid nonempty file. This is a fail-closed reader check, not a new theorem
or a replacement for independent publication review.

No `sorry`, `admit`, unsafe reducibility override, new preparation oracle or
replacement scientific target is permitted by this migration.

## Current verification

| Check | Result |
| --- | --- |
| Website Python tests in the repository environment | 134 passed |
| Technical-memory version and Windows Verso compatibility tests | 15 passed |
| Blueprint declaration-catalog tests | 10 passed |
| Native Windows build-entry parity and failure propagation | 10 passed |
| Proof-trust scan and regression tests | Passed: no source-level axioms or holes; 4 tests |
| Harness/runtime/control/context/mutation/memory regressions | 97 passed; 1 Windows symlink-permission test skipped (not synthesis evidence) |
| Existing Hermite finite-export regressions | 15 passed, including Qiskit/QASM round trips; not a new polynomial-family executable certificate |
| Research source/card contracts | Passed; no theorem promotion |
| Paper/example source-anchor taxonomy | Passed |
| Exhaustive Lean library and tests | Passed under 4.33.0: both roots and all 202 discovered source modules |
| Main `QuantumBlockEncoding` root and stored Hermite raw-cost chain | Passed; exact targets, negative orientations, endpoint and bit-order tests retained |
| Active technical-lemma registry | Ten compiled entries updated to 4.33.0 only after exhaustive acceptance |
| Regenerated Blueprint assembly and HTML generation | Passed under root Lean 4.33.0; required routes/styles, fragments, unique declaration search and path checks passed |
| Blueprint path-sanitizer / search / preview-authentication regression tests | 14 / 13 / 1 passed |
| Local curriculum preview | Generated; source-link and local-path checks passed; not a release artifact |
| Assembled local site with fresh Blueprint | Passed: internal links, fragments, required files, counts and common navigation; not independent source admission |
| Browser reader checks after the curriculum layout correction | 42 route/viewport/theme combinations and all authored method/Wiki formula pages passed using installed Edge |
| Real Blueprint browser search | Passed: emitted mapper has unique exact names; keyboard search finds the Hermite root and its jump reaches an existing statement anchor |
| Content-bound source publication review | Not passed: 51 changed production modules need independent packets |
| Remote update verification | Initial fetch failed; 8 October CLI fetch succeeded using the existing system proxy, with remote main still at the original baseline |

Parallel local builds encountered file-read failures and memory pressure.
Serial dependency-ordered prebuilding is used to populate the cache before
rerunning the unchanged exhaustive Lean gate. Cache timestamps are only
a prebuilding heuristic, not acceptance evidence. The unchanged exhaustive
Lean gate subsequently passed, with equal input digests before and after compilation:
`5a8f47f8d0afd1d4f957e55babde52a9e9c01babf05c481b988e99ebca2f7758`.
Its report is `_out/lean-gate.json`; the Git HEAD alone does not describe the
uncommitted migration, so the content digest is essential.

The current local preview is `_out/curriculum-preview-20261007-v4`, with
Blueprint output from `_out/blueprint-433-20261007-v2`. Its curriculum browser
report is `_out/research-browser-curriculum-20261007-v4/browser-report.json`.
The final joint browser report is
`_out/research-browser-curriculum-20261007-v4-final/browser-report.json`:
`blueprint_search_required: true`, `blueprint_search_passed: true`, 42 reader
cases and no reported failures. The first search smoke attempt used a synthetic
input fill, which does not trigger Verso's keyboard listener, and timed out.
The corrected test uses real key events; it now also records a failed Blueprint
check in the report and exits unsuccessfully rather than leaving that attempt
without a report. Both CI website entry points require this real search check.
The new peer-part hero sections no longer reserve an empty second column;
the correction is covered by the planned-part rendering test. Desktop and
mobile screenshots of the new curriculum pages were also inspected, without
claiming manual inspection of every automated browser case.
Preview links to dirty Lean sources are deliberately absent; retained links
refer only to unchanged, commit-pinned sources. The private preview does not
replace the content-bound publication gate or the final assembled Pages gate.

## Additional documentation-build changes

| Files | Exact change |
| --- | --- |
| `ABEISBlueprintMain.lean` | Emit the official page-runtime dependency closure in no-preview-data mode; no invented manifest/cache |
| `scripts/generate-blueprint-catalog.py`, `tools/test_blueprint_catalog.py` | Use the inspected 4.33 statement anchor; add anchor/runtime regressions |
| `website/scripts/augment_blueprint_search.py`, `website/scripts/test_blueprint_search.py` | Admit only the inspected legacy/current search call pairs, preserving priorities and fail-closed behavior |
| `website/scripts/check_site.py`, `website/scripts/test_site_contracts.py` | Require nonempty files for four textbook entries and catalog; reject directories/empty files |
| `scripts/sanitize-blueprint-paths.py`, `scripts/test-sanitize-blueprint-paths.py` | Include ESM modules and detect escaped Windows separators without rewriting through that detection view |
| `website/scripts/test_research_browser.py`, both `scripts/build-website` entry points | Test real declaration search/jump when Blueprint is required; report failures and fail the build |

These changes affect documentation emission, retrieval and testing only.
They do not change the production Lean statement, verifier, scientific target,
scoring or historical run log. The patches are independently reversible;
regenerating ignored output is sufficient to discard their preview effects.
The complete production-proof compatibility migration is still subject to the
separate independent-review requirement below.

## Curriculum and external proof assets

The homepage, navigation and reading guide expose four peer parts. Walsh-series
preparation and diagonal-operator space–time–accuracy trade-offs are planned
extensions of Parts I/II. Representation-theoretic QIT and scientific quantum
algorithms are Parts III/IV. Their chapter plans and extended chapters do not
claim new local formalizations.

The OpenAI Math intake remains pinned source/adapter input. Its Lean 4.34.1
snapshot is not imported as a package into the local Lean 4.33.0 library.
See [the curriculum audit](openai-math-quantum-curriculum-audit-20261007.md) and
[the source-route audit](state-preparation-frontier-audit-20260929.md).

## Publication boundary and rollback

The existing publication gate is unchanged. Source-blind decoder and
anti-anchored reviewer records must be produced by genuinely distinct reviewers
and bound to the final stable module, toolchain and dependency content. The
formalizer must not invent those records to make CI green. Compilation and
source fidelity remain separate checks.

No historical run or acceptance record is rewritten. Existing unrelated
working-tree changes remain outside this migration. The compatibility checker
changes and the curriculum additions are ordinary tracked-file patches;
generated previews and build caches are not release evidence. No deployment or
push is claimed in this record.

## 8 October publication follow-up

Fresh CLI fetch confirmed remote `main` at
`c681192368c2fed4e055928480cefe8544cf30f1`, matching the migration baseline.
The GitHub connector also confirmed repository push permission, and the CLI
push preflight succeeded with existing credentials. The machine's existing
system proxy was supplied per command; no proxy, token or local absolute path
was added to repository configuration or source.

The changes can be submitted on a review branch, but compilation, browser
success and write permission do not discharge the 51 missing content-bound
independent publication records. Main-branch merge and deployment remain
withheld until that admission succeeds. Unrelated images, Robin exports and
historical replay output remain outside the migration commit.


## 16 October: fixed-source migration priority checkpoint

Remote main was safely fetched and remains `f2cba045611a0d11c5995c29607569726bf1d6c5`,
using **Lean 4.29.1**, not 4.33.0. Contribution checkpoint
`565516d28bcab79f39301c92f669ff43bbc68428` is pushed and independently confirmed
on the remote branch. Nine exact whole-module publication records validate;
the unchanged aggregate gate still rejects the other 42 of 51 changed modules.
PR #86 is not an approved main migration.

The current production sources retain the prior incremental 4.33 library/Tests
pass; inherited caches and local Verso compatibility edits remain disclosed.
Forty-five focused byte-transport/publication/atlas tests pass and the research
source contracts pass. One transient Git subprocess resource error passed both
isolated and complete focused reruns. Frozen historical failure logs retain
their original trailing whitespace; non-log staged whitespace checks pass.

The next fixed-source slice is the whole 20-root HermiteCutRank module. A distinct
formal-only decoder freshly compiles its actual source and runs 20 signature and
axiom checks against the explicitly fresh target. Only ordinary logical axioms
occur (the index abbreviation has none). Imported providers remain inherited.
The first `bad_alloc` and the successful bounded retry/warnings are retained.
Independent source-first comparison finds all 20 roots and semantic slots match,
but graph/coverage admission is still under review. Earlier refusals remain:
actual input witnesses were missing from AND-tails, eight indented formulas
were omitted, and stable open consumer-gap nodes were absent. Versioned repairs
do not alter the lesson, theorem source or scientific target. Current artifacts
are [staged review material](../reviews/publication/hermite-cut-rank/), not a
tenth canonical publication approval, main admission or PURIFIED.

A separate standard-Lake compatibility experiment restored the exact main
GHL2025/HermiteCutRank bytes with scoped elaboration options. The three focused
GHL/HermiteCutRank/RobinMatrix builds passed, but the full library attempt was
stopped after import-read failures under resource pressure. All three named
dependency files existed and were nonempty; the exact OS cause was not isolated.
Tests/exhaustive phases never started. Potential native/shared library cycles
were not resolved or tested. This experiment is retained as PARTIAL_ENV_RESOURCE,
not adopted as the release route and not a mathematical obstruction.

The delivery bottleneck is not installing Lean: it is the broad combined PR,
whole-module source fidelity review, stable global input bindings, and reliable
build resources. The response is fixed production inputs, bounded independent
review slices, serialized heavy compiler windows and pushed recoverable
checkpoints, not weaker verifier/publication rules or a new controller rewrite.

Hermite's C23 charged coefficient cache has bounded independent internal review;
C22 consumption, total preprocessing, finite-bit/normalization/physical costs,
family executable acceptance and ROOT remain open. New textbook frontiers remain
bounded experimental local results: Walsh interference, projected diagonal
blocks, the shared QIT pure-state projector/density slice, and the QASC exact
block consumer. They are not whole-book formalizations or main-admitted new
resource certificates. The pinned OpenAI Math snapshot/adapter boundary is
unchanged. No branch is deleted during this unresolved migration checkpoint.
