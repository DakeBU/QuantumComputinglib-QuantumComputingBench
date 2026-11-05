# Current-source Lean gate context

The adjacent `c25-cf77-lean-gate.json` is the unchanged standard runner's exact
output, SHA256 `cb686076b8d517923182f4a1b23b6fb0805b988e066635e7048cda6d2426e60c`.
It records contribution `cf77fde090fff00fcb829d1684b85596eec4949f` under Lean
4.33.0, with content digest
`5a8f47f8d0afd1d4f957e55babde52a9e9c01babf05c481b988e99ebca2f7758`.

The parent actually ran the unmodified `website/scripts/run_lean_gate.py`:
library, Tests, and every discovered source-module target passed. The complete
target list is in `compiledModules`; unimported files were not silently omitted.
Inputs were checked before and after by that runner. This is an incremental
Lake gate against inherited provider/build artifacts, not a clean transitive
rebuild, a trust-zero dependency audit or independent source review.

The only modified dependency source observed in Verso is the existing bounded
Windows search-asset path-separator fix, reproducible by the tracked
`tools/apply_verso_windows_compat.py` at its exact manifest pin. It changes no
production theorem. The corresponding pinned compatibility tests passed. No
unrecorded general elaboration override or split-library experiment was adopted.

Expanded raw command logs stay private because they include machine paths.
They are not missing public positive-admission inputs. The public report is a
content-bound build record, not an aggregate publication success certificate.
Reproduce on a configured checkout with:

```text
python website/scripts/run_lean_gate.py --output _out/new-current-lean-gate.json
```

The canonical source-review registry still has unadmitted changed modules;
the full publication gate remains fail-closed. Main remains Lean4.29.1. No
scientific ROOT, finite-bit/resource, family executable, reader or PURIFIED
acceptance follows from this build record.

## Small reversible transport change

Changed files: `.gitattributes` and
`website/scripts/test_publication_byte_transport.py`. Only JSON receipts in
`reports/lean-433-migration/` gain raw-byte Git transport, so a Windows checkout
cannot silently alter a frozen report hash. A CRLF fixture now round-trips
through real Git checkouts with autocrlf true, false and input. The unchanged
checker still rejects ambient proof-byte drift and missing bound inputs.

Tests run: the byte-transport, fail-closed Lean-publication and research-atlas
modules (45 passed), plus the HCR integration suite (6 passed). No Lean source,
scientific target, scoring or verifier logic changes. Rollback is limited to
the one scoped attribute and its fixture/assertion; do not normalize or rehash
existing frozen reports. Cross-platform byte transport is tested, but this
does not establish a clean dependency rebuild, reader admission or source
agreement for the still-WIP paired modules.
