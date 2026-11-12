# Tests-only public-fixture hygiene successor

Only `test_replay.py` and this new successor handoff changed. The portable
runner remains byte-identical to the version used by the parent's successful
`c409` replay, SHA-256
`f83a926e2ee3aed5de18fbe88b678970693bd029f37412f0e49bc1d76ec433b9`.
No mathematical source, seal, source fixture, prior handoff, raw evidence,
scanner, transport rule or acceptance condition was changed.

The parent reported transport auto-review rejected literal artificial absolute
path examples in the public test file. The safer alternative implemented here
changes the source representation of those synthetic test inputs only; it does
not retry a rejected transport or conceal real host data.

## Exact diff scope

- Import `PurePosixPath` and `PureWindowsPath` alongside `Path`.
- In `test_invalid_output_paths`, construct synthetic POSIX-rooted,
  Windows-drive-rooted, drive-relative and UNC inputs from explicit separate
  drive/root/components, rather than embedding absolute path examples.
- Assert each constructed input's absolute/drive-relative category before
  passing its string representation to the unchanged rejection checks.
- Retain every relative malformed case unchanged and preserve the original
  four rooted/drive/UNC rejection cases. No negative coverage was removed.

New `test_replay.py` SHA-256:
`b9fc8630cc7c6eef00218dc81b351cdf910c1014381240d82e34ec3e80b9f1a2`.
Previous test SHA-256:
`2eb1e896c2c6ef3bbc8a4820753c8b993ba523830a45d5d5048c1ca376eae7d4`.
`REPLAY_HANDOFF-v2.md` remains unchanged, SHA-256
`6df7cffb9936cd40f0edf26f368be0d112046e9275e449a7f17bacfb55edb18e`.

## Actual checks

Static unittest invocation with `tempfile.tempdir` configured to the existing
writable `_out/static-test-temp` area: **21 passed, no skips**, exit 0.
No Lake or Lean process was launched. This is static test evidence only, not a
new compiler receipt or a claim that auto-review/transport has now accepted.
The mathematical source SHA-256 remains
`22ef9784a3fe636b9ea07cf622bce01572425e2706e540e547934ec078dba34c`;
both exact pre-proof seal/formal-packet hashes were rechecked unchanged.
