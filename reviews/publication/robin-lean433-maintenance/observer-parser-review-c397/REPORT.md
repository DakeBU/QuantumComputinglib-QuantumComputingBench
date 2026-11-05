# C397 bounded observer-parser repair review

Verdict: **accepted-for-observer-parser-repair-only** for the exact candidate source/tests. No required code change found within this scope. This does not accept a completed runtime audit, semantic export review, source/publication claim, BE root or clean/transitive TCB.

Reviewer: `/root/robin_compatibility_review_c364`, not the repair author. Logical paths use `R/` and `W/`. All prior review scopes remain unchanged.

## Inputs and exact change

Candidate files were read completely:

| W/c396-observer-signature-repair/ file | Bytes | SHA256 |
| --- | ---: | --- |
| audit_robin_exports.py | 16987 | `b0259025755b5de41936c002e05301c4dd15f28c7b9ff11b3a674b8be1395347` |
| test_audit_robin_exports.py | 15426 | `39dfed16a4b4a9c1e50eb9d25cc6028157014ed44181da30ab2df3fd3b0ab9e2` |
| ACTUAL_REPLAY.json | 1159 | `4857a25cf80cf72953a74e1bcb296bb9f98115e1fe0062019a57c1123efc6b7f` |
| INITIAL_REPLAY_FAILURE.json | 520 | `69608ec654e0f8a72c2017e7f01d32b276eacb177c4fb01be0fb347751ff6988` |

I compared complete raw source/tests with current `R/tools/robin_maintenance_export_audit/` originals: source 15509 bytes / `65cbb128ca1c762e71a3f03464717ea5e902d5f059114abeac60a6a808c03151`; tests 12590 bytes / `7ec5d54233b407ae2b02ca323b6deaa85ee4d8e55769d278590a5f0127d673a4`. The full source delta is the balanced-prefix helper, its call replacing the old signature regex, and permitting one terminal `✝` in axiom labels. Four test methods are added. Function/class AST comparison finds only `parse_observations` changed and `exact_signature` added. The native classifier, ordinary/legacy axiom sets, inventory rules, runtime command handling, dependency/binary/source/probe/tool pins and post-observation checks are unchanged.

## Parser/trust assessment

The signature recognizer retains exact case-sensitive declaration names, the previous optional universe suffix, balanced explicit/implicit/instance/strict-implicit binder delimiters, quoted-string escape handling, a result colon and nonempty result text. It rejects missing/wrong names, unknown intervening prefixes, unclosed/mismatched binder delimiters and unterminated quoted prefixes in the exercised cases. It is deliberately **not** a Lean binder/type parser and does not establish that a printed type is a sound mathematical contract. Ordered nonce markers, exact declaration names in axiom results, duplicate-label checks, unsupported axiom syntax and trailing-output rejection remain in place.

`AXIOM_NAME.fullmatch` permits only a single terminal dagger, never an internal/repeated dagger or arbitrary replacement glyph. Printed plain and dagger-bearing labels are retained as distinct strings, without stripping or merging. The three ordinary axiom names are unchanged; e.g. a dagger-bearing different label cannot become ordinary by normalization. All other labels remain additional. Native-pattern classification remains disclosure, not an approval/whitelist or a proof of axiom provenance. The change does not convert a native-bearing observation into an ordinary-three-axiom claim.

## Independent tests and offline replay

First default-sandbox test run: 23 methods, 2.477 s, 21 errors from temporary JSON `os.replace` PermissionError/WinError 5 (including subtest errors). This was retained as an environment failure, not hidden as a code pass. One scoped escalation reran unchanged code: **23 tests, 1.842 s, OK**. Every subprocess was mocked by the suite. I redirected only the fixture `BASE` to an automatically cleaned temporary root, so neither candidate nor original packages acquired test fixture writes. No Lean/Lake command executed.

Offline replay used the saved original stdout and generated probe, not a newly invoked compiler:

- Raw stdout: 1424745 bytes / `8153173f89edffc70271ec1006ee6348f0f80550544ba3a995fe7955ec2ecee9`.
- Probe: 165368 bytes / `59220ed81ab5cdd9fc15781f8a92c16b34ffba0b55470208dae4093917a94c18`.
- Stored observation stderr is empty. Its stored report records observation exit 0, but report success remains false with the original row-0 parser error.

I extracted 395 ordinal, case-sensitive unique `#check` names and the nonce from that probe, verified the current unchanged generator recomposes the probe byte for byte, then parsed the complete raw stdout. This is probe-based replay, not a fresh catalog inventory or semantic interpretation of every type.

| Parsed classification | Rows |
| --- | ---: |
| ordinary-only | 88 |
| no-axioms | 68 |
| additional-with-native-name-marker | 239 |

The replay retains **496 distinct additional printed labels**, including **126 distinct labels ending in `✝`**. All match the disclosed native-name pattern. These are not guaranteed unique/full kernel-name identities: pretty-printing, including inaccessible/hygienic-name display, may hide details. They are not counts of added source axioms or the two migration `native_decide` sites, and do not reconstruct a transitive TCB.

As causal regressions, the unchanged original parser independently fails on these bytes at row 0. The new binder recognizer with only the original axiom-name regex restored in memory independently fails at row 134. The complete candidate parses all 395 blocks. No source file was altered to perform these probes. I did not open/execute the archived initial-candidate ZIP or independently authenticate the remote artifact download/run identity; local hashes and stored command pins are the evidence checked here.

Crucially, offline parsing does not perform the original audit's post-observation input/binary/tool/probe rechecks. Its original report stays failed. A fresh complete, source-bound observer execution remains required; the existing full-build success is not replaced or rerun by this review.

## Historical freeze and integration boundary

Original `TOOL_FREEZE.json` remains 1558 bytes / `9029a7b80661bba87ffed92ea9854f2acfa16084697d95a6b22cb32a7b771b30`. I mechanically verified all five payloads named by that freeze still match their recorded lengths/hashes, including the original report, manifest and test log; those three texts were not newly semantically reviewed.

Before installation, preserve an exact v1 archive of the historical source/tests/seal and its referenced evidence payloads; never rewrite the historical report or repoint its old hash claims at repaired code. A **new** current binding must identify repaired source/tests and the explicit v1 archive. This review verifies current original bytes, not completion of the parent's future archive/install/rebinding operation.

Only this new C397 three-file packet and automatically cleaned mocked temporary fixtures were written. No production/candidate/historical edits, Git, network, Lean, subagents or CI query/restart occurred. The live Pages run was untouched. Failure class after successful scoped testing: NONE for this bounded code repair. STOP after freeze.
