# C380 independent CLI-entry repair review

Verdict: **accepted-for-compatibility-only** for the exact bounded C379 code repair. No required change found. This is not real maintenance-record acceptance, main/release admission, scientific BE-root closure or TCB certification.

Reviewer: `/root/robin_compatibility_review_c364`, not the repair author. Paths use logical `R/` and `W/` roots. Prior review packets remain unchanged.

## Exact inputs and preservation

| Input under W/c379-cli-successor/ | Bytes | SHA256 |
| --- | ---: | --- |
| check_research_publications.py | 11616 | `7908c68d22e5a7e2da9375e5e69b191c4d336eb7f864e5b26da81f0758863466` |
| test_publication_cli_entry.py | 2518 | `f5831ce9dc940d7372adf7a2a84620ef1697a724058bbe78642681488dd2e0bd` |
| README.md | 815 | `efe82438aa9f55ca1acef8dfa8ab0a19bfbefec33894356653ea99f0e04d4f84` |
| check_toolchain_maintenance.py | 13339 | `f178ba5a2475086b7714076f3867f2c06c96ca412401500a78315fdf56338ea0` |
| test_toolchain_maintenance.py | 17047 | `94081fee920cd36a78656ba02c0dc4679f020902f61398821387c7f79a49a738` |

The first three files were newly read completely. The last two exactly match C375's reviewed bytes and are mechanically reused, not newly fully reread or rerun. I byte-compared the publication checker to the unchanged previously reviewed `W/c373-typed-policy-successor/check_research_publications.py`: removing only new lines 151-155 leaves exactly its 11374 bytes, SHA256 `c97f4da5fc7ca47c866ee4514a3c23e299b7117bb8993d2ad57575397aac10ad`.

Thus the entire ordinary `validate_record`, previous dispatcher, main/error handling, maintenance leaf and type bindings remain unchanged except for the five-line bootstrap before the lazy import. No fresh 33-test, 12-ordinary or broader suite result is claimed. The parent's reported 67-test run and production CLI failure are context, not independently revalidated evidence here.

## Repair and actual execution

`ROOT` is fixed from the executing script's resolved `__file__` at line 17. New lines 151-155 insert that root into `sys.path` if absent, immediately before importing `website.scripts.check_toolchain_maintenance`. They do not insert the `root` argument or the `--root` value. Registry/data-root selection remains separate from this script-root code lookup. The change fixes the missing package-parent path for a cold direct-script-style entry without replacing validation logic.

I independently ran the supplied **2 tests, 1.142 s, OK**. Each creates real temporary sibling script/package files and an empty registry, then launches Python with `-I -B`, a foreign working directory, a cold script-style path and real `main` via `runpy.run_path(..., run_name='__main__')`. Only Git subprocess replies are mocked; the mock rejects unexpected non-Git commands.

- Valid empty-change CLI: returns zero, parses real JSON, reports zero accepted/maintenance packets and no natural-language equivalence claim.
- One changed module with no record: returns nonzero with the real missing-reviewed-record error, not `ModuleNotFoundError`.

These tests exercise actual isolated child/main/import behavior, not an API call with a preloaded package. They do not execute an actual Git command or admit a nonempty real maintenance case. They emulate direct-script `sys.path` using a child wrapper so Git can remain mocked; they are not a production end-to-end CLI run. The fixed-root check is not a general sandbox against hostile preloaded modules or every possible Python environment.

## Boundary and stop

Accept the precise import bootstrap and its tests only. Existing C375 compatibility-only classification, historical eleven-input scope, actor/evidence obligations, F1/F2 protections, native debt and scientific gaps remain unchanged. Because the publication-checker bytes changed and are themselves bound by maintenance policy, real-case root bindings/receipts must use the new exact bytes; old C375-era receipt bindings are not silently current. Actual record intake and full integration gates remain separate.

No production/candidate/old artifact edit, Git, network, Lean or subagent work occurred. Only this new three-file packet and automatically cleaned temporary CLI fixtures were written. Authorized isolated Python child processes were used; no permission escalation was needed. Failure class: NONE for this bounded repair. STOP after freeze.
