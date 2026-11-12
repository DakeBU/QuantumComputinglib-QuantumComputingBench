# Independent review of the C407 identity-display patch

Verdict: **ACCEPT for this exact four-file display-only patch.** No actionable defect was found within the reviewed scope. This is a code review, not a new mathematical review, source acceptance, QA certification, deployment check or publication approval.

Reviewer identity: `agent-task:root/finite_branch_semantics_c405`. Author identity: `agent-task:root/publication_identity_display_c407`. These are reversible display spellings of the actual canonical task identities: replace the `agent-task:` prefix with a leading slash. They denote tasks, not filesystem paths. The reviewer is distinct from the author and parent. `publication-identity-c410` is the artifact scope of this follow-up, not an invented new agent or runtime run identifier.

## Exact scope and order

I inspected the code changes before reading any author handoff/verdict. I did not need the C407 handoff for the verdict. A later finalization notification identified the fixture-only successor; I reread its final diff and independently ran the tests against those final bytes.

The independently resolved review base is commit `37ebfef80e0043ff96b54796a6a8fe747f983644`. The final reviewed files and actual whole-file SHA-256 values are:

| Repository-relative file | SHA-256 |
| --- | --- |
| `website/scripts/research_atlas.py` | `a9e217939839e7b8a8609187b698e022e0c7df5abc1d495b73659caf9d72c2fa` |
| `website/scripts/check_deployed_research.py` | `16d96c41fedbc7be4e117eea8744c16be8121b9e67c15d1af7b64d1795be8d2d` |
| `website/scripts/test_research_atlas.py` | `6944342b485d2c3ff44c30519cf80d5dbdd4e507d2a2d967c33f7d7eb8409fcb` |
| `website/scripts/test_deployed_research.py` | `47bf8dc14b3496603d82a906ab59fc04ea951204c379a5ff808127c09bd7335c` |

Ordinary Git work-tree diff access failed in the sandbox. I instead read the exact base blobs through read-only Git object access and independently reconstructed the complete content diff against current file bytes. Checkout CRLF spellings were normalized to LF for the content comparison only. Raw baseline and current byte hashes/lengths are recorded separately in `INPUT_PINS.json`; no normalized hash is presented as an actual file hash. No Git write or repository source edit was performed.

The existing sanitizer was read in full, relevant publishing/live-check context and all patch hunks were inspected, and the complete canonical catalog was parsed for structural checks. The three affected canonical records were inspected in full. The scientific content of the other source records was not re-reviewed. Ten control files, including all three canonical catalog files, the publication registry, path sanitizer, proof-input checker, browser contract, publication checker and build entry points, were compared to the base. They are unchanged modulo checkout newline spelling; exact raw hashes remain available. This is a bounded control comparison, not an assertion that every file in the repository was audited.

## Why the change is narrow and reversible

`public_catalog` validates the canonical catalog first, rejects a preexisting `public_projection` field, then deep-copies the catalog. It does not mutate the caller or write canonical files. The only rewrites require both an exact source ID and the exact complete `authors` value. The allowlist contains precisely:

- `aspbe-local-exact-primitives-controlled-rotations-finite-cubic`;
- `aspbe-local-stored-rectangular-elimination-v1`;
- `aspbe-local-retrospective-sequential-primitive-assembly-c48`.

For those three existing field values, known canonical task identity tokens receive the `agent-task:` display spelling. The historical formalizer remains `UNKNOWN`; retrospective/local/source-scope and pending-review qualifications are preserved. The mapping is a lossless encoding of the supplied identities, not a newly established author identity, historical independence or pre-proof provenance claim. Every other field, record, nested value, atlas object and research-route object is preserved. Removing the explicit projection disclosure and decoding the three fields restores the canonical source object exactly.

It is not a regex-based path scrubber or a general task-name rewriter. Different IDs with the same author text, extended or altered author strings, nested fields, and actual path-shaped strings are left untouched. They remain visible to the existing scanner. The new disclosure explicitly identifies the canonical source and unchanged digest basis, documents decoding, and disclaims any new source, mathematical or formalization review. The rejection of already-projected canonical data avoids silently overwriting source metadata or confusing a derived payload with its input.

The final negative fixtures construct artificial path-shaped strings from `PurePosixPath`/`PureWindowsPath` components. They are passed to string-scanning tests, never used as filesystem destinations. This successor changes only test-fixture expression spelling, not the runtime allowlist, projection, scanner or live equality behavior.

## Publishing, validation and live-check boundaries

The JSON publication loop now writes the declared projection. It retains the canonical catalog for scientific rendering, source digests and existing references. The canonical `source_digest` function is unchanged and continues hashing the original catalog files, not projected output. Runtime checks and the independent test run confirmed canonical objects, canonical bytes and that digest remain unchanged by projection.

`check_published` now compares each complete published catalog object to its exact expected projection before continuing the existing page, digest, graph and research-route checks. It does not compare a reduced subset or ignore unknown keys. This adds strict output checking; original schema validation remains enforced inside `public_catalog`.

The live checker likewise computes the projection from validated original canonical inputs and compares all three fetched JSON objects by full equality. Only the exact declared identity display is an allowed difference from raw canonical data. Altered author fields, source status/anchors/scope/formal status, record sets, extra metadata, disclosure text and either other catalog are rejected. Raw unprojected source data and forged display identities are also rejected by the tests. The added `source_author_display_projection_match` flag makes the comparison boundary explicit. Existing `canonical_sources_match` must consequently be read together with that flag and the disclosure: it is not a raw-byte identity claim for `sources.json`.

The commit format/version, proof-input/module inventory, origin/response-size constraints, curriculum, route/navigation, progress/browser coverage and final deployment-version checks were not relaxed. The original live `fetch` and CLI `main` functions are AST-identical to the base. Within `research_atlas`, all 25 preexisting functions other than the two intentionally changed publishing/check functions are AST-identical, including `validate_catalog`, `context_packet` scoring, `progress_payload`, `source_digest` and graph-delta logic. The schema/QA/scoring/publication controls compared separately are unchanged.

The projection does not itself promise to detect all filesystem paths. The existing publication scanner remains the detection gate; neither this helper nor mocked live-check tests substitute for a full assembled-site path scan. No generic scanner exception or path stripping was added.

## Independently executed checks

I executed the local `review_checks.py` helper with the private runtime repository argument and a scratch directory confined to this new review artifact directory. Bytecode writes were disabled. The helper performs read-only Git object comparisons, AST checks, independent projection invariants, then runs:

`website.scripts.test_research_atlas` and `website.scripts.test_deployed_research`.

Actual result: **55 tests in 9.351 seconds; 0 failures, 0 errors, 0 skips; exit 0**, using Python `3.11.9`. That duration is the unittest suite's reported duration, not a total-work or efficiency measurement. `TEST_OBSERVATIONS.json` records the actual result, and `INPUT_PINS.json` binds the exact code/control bytes used.

The tests include real calls to the existing scanner on bounded temporary fixtures, canonical-byte/digest preservation, round-trip restoration, exact-ID/value gating, malformed schema and projection-field rejection, unknown/extended/nested path-shaped data remaining detectable, real publication JSON writing before an intentional stop ahead of reader rendering, and full mock-live catalog tamper rejection. All live fetches in these tests are mocked; none demonstrate that a website is currently live. Existing publication-binding and browser-report coverage tests also ran as part of the 55-test suite, not an actual browser session.

Independent helper assertions additionally confirmed the exact three changed author records, unchanged nonscientific/scientific record fields, unchanged atlas/wiki objects, canonical immutability, allowed runtime function-diff boundaries, and all ten unchanged controls. All 14 scoped source/control files were byte-identical before and after the test run. Temporary fixtures were cleaned by their normal test lifecycle; the review scratch directory was empty afterward.

No Lean, full browser, genuine live network verification, full-site build or whole sanitizer test suite was run by this reviewer. No author-reported run is relabeled as my independent execution, and no timeout or partial run is counted as a pass. I did not independently run Git's whitespace-diff checker.

## Remaining gates and immutability boundary

This approval is sufficient only for the reviewed narrow code change. Before production/publication claims, preserve these exact input bindings or obtain a successor review for material changes; run the applicable CI/full documentation/site and assembled-output path checks; obtain the remaining full sanitizer-suite result; run required actual browser/reader checks; and, after deployment, run the genuine commit-bound live checker. The helper's intentional pre-render stop and the mocked live tests cannot supply those gates. Required Lean/library/Tests evidence belongs to the broader integration policy and was neither rerun nor waived here.

The earlier `finite-branch-semantics-c405/REPORT.md`, `INPUT_PINS.json` and `FREEZE.json` were not edited. Their hashes were rechecked against the previously frozen values and match exactly. This report makes no new finding about that mathematical candidate and does not extend its acceptance scope. No historical source, mathematical statement, QA score, source-review verdict or canonical publication record was changed by this reviewer or promoted by this patch.

All authored review files are new files under the logical artifact scope `publication-identity-c410/`, written via `apply_patch`. Any runtime locations were supplied privately, not embedded in this report or its pin records. No separate reviewer identity or unknown run ID has been manufactured.
