# Fixed-source replay tooling corrections

This successor updates the portable replay tooling only. The mathematical
source, signatures, statement/formal seals and earlier proof/runtime evidence
are unchanged. `REPLAY_HANDOFF.md` remains the original 19-test record, SHA-256
`ae7ada451c9579b5412f8734792523adac1ddca5625dcad1327f6542d7e8adca`.
No Git, production, benchmark/split, dependency or toolchain writes occurred.

## Corrected files and exact hashes

- `replay.py`: SHA-256
  `f83a926e2ee3aed5de18fbe88b678970693bd029f37412f0e49bc1d76ec433b9`.
- `test_replay.py`: SHA-256
  `2eb1e896c2c6ef3bbc8a4820753c8b993ba523830a45d5d5048c1ca376eae7d4`.
- `REPLAY.md`: SHA-256
  `1e592ec0dc7bfc5b9beb2805f26a4ac417a2ccc4734999e93134a1773c94e485`.

Only two code behaviors changed:

1. `check_providers` permits repeated non-owned dependencies, such as the two
   legitimate `Init.olean` rows emitted for separate imports. It still requires
   exactly one matching own provider and rejects duplicate own providers,
   foreign same-basename providers, absent providers and malformed rows. No
   source, axiom, root, memory, time or success gate was relaxed.
2. Static path tests use Python's configured temporary directory, not an
   unpublished `PACKAGE/PRIVATE` path. A clean-empty-package regression patches
   `PACKAGE` to a directory without `PRIVATE` and exercises path-test setup.
   Hosts may configure `tempfile.tempdir` to an existing writable local ignored
   output area before invoking the static suite.

## Actual failure and regression evidence

The parent reported portable replay attempt `c408` failed with
`IMPLEMENTATION_FAILED / observation_rejected` after predecessor compilation
and the source dependency query both returned exit 0. The old provider parser
rejected the legitimate repeated `Init.olean` rows despite exactly one correct
own predecessor provider. This was a replay-parser implementation bug, not a
Lean source failure or mathematical refutation. The parent preserves that raw
failed output unchanged; this worker neither overwrote it nor invented a
successful successor replay receipt.

Added a platform-neutral repeated-`Init.olean` regression, including an explicit
duplicate-own rejection in the same repeated-import setting. Existing foreign,
missing and malformed provider tests remain. Added the clean-package setup
regression described above.

The first direct static invocation after these edits hit sandbox-default
temporary-directory permission errors (21 tests, 12 setup/cleanup errors):
`ENV_BLOCKED` test execution, not theorem or provider-parser evidence. No
permissions were loosened or cleanup errors suppressed. The unchanged tests
were then rerun with `tempfile.tempdir` explicitly configured to the writable
packet-local `_out/static-test-temp` area: **21 passed, no skips**, exit 0.
No Lake or Lean process was launched for either static invocation.

The corrected portable runner has not been rerun against Lean by this worker.
Use a new output directory for any parent rerun; preserve c408 and every prior
receipt. Source/consumer success, graph success and whole replay success remain
separate, and main/full-repository/QA admission remains false.
