# Portable fixed-source replay handoff

Added only `replay.py`, `test_replay.py`, `REPLAY.md` and this handoff. Existing
mathematical source, seals, original handoffs/bindings, raw run evidence and
parent graph evidence were not edited. No Git, production, benchmark/split,
dependency or toolchain changes were made.

## Exact files

- `replay.py`: SHA-256
  `424cd8f06d95341d1809a68a41e6110a2779ae82aaf2af50de9f240b2fec7991`.
- `test_replay.py`: SHA-256
  `7f766b40b6ee72ed9e53c62178c2e120e3dc3a36fe5bf4044da03058644d2136`.
- `REPLAY.md`: SHA-256
  `5a2f5f1ee1ebc0c85f524ac2f75cad65f268239d7f2f39d918d7b1023b95c7da`.

The fixed-source runner pins the exact predecessor, coherent source, consumer,
checked-signature fixture, orientation negative and parent `ExportHelpers.lean`
(`51cdde5efef3359dc3be057e5a887675fcc3253158c84d3be5e42865c1c02880`).
It also requires the matching provisioned manifest. Its only parameters are
`--repo` and a new repo-relative `--output _out/...`. Actual Lean prefix and
dependency paths come from `lake env`, not host constants. It exposes no source,
root, axiom, budget, overwrite or skip-gate parameter.

Source/consumer stages use 1536 MiB, reserve 5120 MiB; graph-only stages
(including their dependency query) use 2048 MiB, reserve 6144 MiB. All are
one-job, 120-second launches.
Own predecessor/source outputs are freshly compiled and selected explicitly.
The root parser requires exact ordered coverage and exactly the ordinary three
axioms. The orientation fixture must produce the actual typed completeness
order mismatch. The graph parser follows bounded compiler-generated helpers,
accepting the actual outlined norm-proof edge without pretending the slice is
a whole-library transitive graph.

Failures preserve non-success and typed stage status, return nonzero, and keep
source/consumer success separate from graph success. Main, full repository and
stable QA flags always remain false. `result.json` has hashes and logical
output names only; raw stdout/stderr remain local diagnostic files. The runner
tests fixed authored sources; it is not a new production verifier or sandbox.

## Tests actually run

`python -B -m unittest -v test_replay`: **19 passed, no skips**. These are static
tests only. They reject missing/duplicate/reordered roots, extra/sorry/native
and missing axioms, malformed/foreign/duplicate providers, invalid/existing/
linked output paths, missing/reordered signatures, an untyped negative error,
lowered memory reserves and malformed/out-of-scope/incomplete helper slices;
they also check nonzero environment-failure propagation and public-safe status. A source-hash test
checks every fixed Lean fixture against its pinned bytes.

A separate static parser check accepted all **14 rows** of the already saved
`PARENT_GRAPH_V2.json` helper slice. This read existing evidence; it was not a
new graph compilation. No Lake or Lean process was launched in this task.
The runner itself has not yet received a new end-to-end focused replay receipt.
