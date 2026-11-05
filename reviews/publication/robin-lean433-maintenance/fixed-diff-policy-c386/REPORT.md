# C386 independent fixed-abbreviation review

Verdict: **accepted-for-compatibility-only** for the exact source/test candidate below. No required change found. This accepts a diff-serialization repair, not a real maintenance record, production/main admission, successful Linux CI, BE research closure or TCB clearance.

Reviewer: `/root/robin_compatibility_review_c364`, not the repair author. Logical paths `R/` and `W/` denote repository/work roots. Prior review and scientific scopes remain unchanged.

## Exact inputs and delta

All three candidate files were newly read completely:

| Input under W/c386-fixed-diff-candidate/ | Bytes | SHA256 |
| --- | ---: | --- |
| check_toolchain_maintenance.py | 13434 | `e5d411116296caffc80db5d479a3c7b7dfdea344876bec737aacb80d8e4b7c43` |
| test_toolchain_maintenance.py | 18631 | `f486902cd77bffc521c31311c34b31060a021a6636b962163dbbbcc4c7bf3a37` |
| REPRODUCTION.json | 406 | `5d93ab5da42c20479ee7aefdb11fdf09514cfdd38bab5b62c85a753cfc1990d6` |

Mechanical raw comparisons confirm current `R/website/scripts/check_toolchain_maintenance.py` equals accepted C375 code at 13339 bytes / `f178ba5a2475086b7714076f3867f2c06c96ca412401500a78315fdf56338ea0`. Removing candidate comment line 105 and only the added `'--abbrev=8'` argument from line 106 exactly reconstructs those bytes. No constants, source hashes, frozen diff hash, scientific flags, actor rules, scope, metadata/type bindings or validation predicates changed.

The current production test and accepted test are both 17047 bytes / `94081fee920cd36a78656ba02c0dc4679f020902f61398821387c7f79a49a738`. Removing the candidate's real-Git test class at 301-327 and its added mock argument exactly reconstructs that test. Prior/current files were mechanically compared, not newly expanded into another semantic review. No registry or ordinary dispatcher was edited or newly reviewed.

## Independent execution and local reproduction

I ran the complete candidate suite. First sandboxed run: **34 tests, 19.672 s, one error**; the 33 existing tests passed, but disposable-repository `git init` exited 128. Its stderr was captured by the test and not printed, so this transcript alone does not establish a more specific cause. A single scoped permission escalation reran the unchanged command: **34 tests, 11.384 s, OK**. The successful real-Git test creates/commits only in an automatically cleaned temporary repository, varies `core.abbrev` over 7/8/12/40, and proves four distinct default outputs but identical explicit-8 outputs with 8-character index names. This is configuration invariance in that fixture, not proof against every Git setting or hypothetical abbreviation collision.

Separately, authorized read-only Git against the actual local repository, with optional locks disabled, produced:

| Actual local command format | Bytes | SHA256 | Index header |
| --- | ---: | --- | --- |
| Explicit `--abbrev=8` | 5426 | `9418ed5a4e1754b042d03084cab78ac171794cd35f71ed469ea94f0933df4bd2` | `ac371ae9..d80cfba8` |
| Explicit `--abbrev=7` | 5424 | `baf1d672dc5b1dfb8f127bc82e8410122f731231ff7d4b0f42ec4020830fef17` | `ac371ae..d80cfba` |

Both target only `R/QuantumBlockEncoding/RobinMatrix.lean` against base `af585d9cbbb299c1c8c48647627a2cb820ef536a`, retaining `--no-ext-diff --no-renames`. Raw stdout was captured as bytes. Explicit-8 output equals the immutable `W/c363-robin-exact-compatibility.patch` byte for byte; explicit-7 differs only in its index line. No source or patch bytes were normalized, overwritten or relaxed to obtain acceptance.

This independently supports the abbreviation-width failure mechanism. The actual failing Linux patch bytes were **not** captured or inspected here. The reported `maintenance compatibility diff changed` Linux failure and pushed commit identity are parent-supplied context, not a newly authenticated CI diagnosis or commit association. The local result does not establish that the next Linux run has passed.

## Boundary and stop

The repair makes the existing eight-character serialization expectation explicit; it does not weaken either the frozen patch SHA or exact file comparison. Other render mismatches still fail closed. The maintenance checker itself is root-bound, so the changed checker requires fresh integration bindings/receipts; this review does not update them or validate an actual registry record.

No Lean, new mathematical/actor/TCB review, production Git write, production branch creation, push, restart/cancel, network or subagent occurred. The two reported live CI runs were not queried or touched. Production and historical evidence stayed unchanged. Writes were only this new three-file review packet and automatically cleaned synthetic fixtures, including the authorized disposable Git repository. Failure class after the successful scoped rerun: NONE for this bounded repair; retain the first environment-dependent failure as recorded above. STOP after freeze.
