# Fixed-source focused replay

`replay.py` tests only the pinned authored files listed in its `FILES` map and
the exact measurement-completeness predecessor at the fixed repository-relative
path. It is not a new production theorem verifier, model-output evaluator,
sandbox or full repository/publication/QA gate. There is no arbitrary-source,
root, budget, axiom, skip-stage or overwrite parameter.

Use an already provisioned matching Lean 4.33.0 checkout with the pinned
manifest. From a transported package, run `python -B replay.py --repo REPO
--output _out/NEW-NAME`; `--repo` is optional only when a matching checkout is
an ancestor of the package. The runner does not invoke dependency installation,
update, build or toolchain provisioning, and does not author files in `.lake`.
`lake env` supplies the actual Lean prefix and dependency path; the actual
binary version and digest are observed rather than assumed. The production
project build directory is excluded from the explicit dependency path.

The output must be a new repository-relative `_out/...` directory. Absolute,
drive-relative, traversal, empty-component, existing, link/junction, Windows
device and alternate-stream paths are rejected. Nothing in an old output is
overwritten. Source bytes are checked against fixed hashes before copying and
again at completion.

The runner freshly compiles the exact predecessor and coherent module, checks
their own-output provider selection, compiles the fixed consumer, observes all
four roots with exactly the ordinary three axioms, prints the full checked
signatures, and requires the actual adjoint-order type-mismatch diagnostic in
the negative orientation fixture. Source/consumer processes use one job, a
1536 MiB cap, 120-second timeout and measured available-memory reserve of at
least 5120 MiB before every launch.

`ExportHelpers.lean` is a separate graph stage: one job, 2048 MiB cap, 120-second
timeout and reserve of at least 6144 MiB. It observes three public roots plus
reachable compiler-generated `branchIsometry` helpers only. The parser accepts
the actual outlined-proof predecessor path and direct overlap-consumer edge;
it does not mistake a root-only slice for all generated proof helpers, nor
claim whole-library transitive/minimal support.

Any failed stage returns nonzero and retains its typed stage status and
stdout/stderr. `source_consumer_success` and `graph_status` remain separate;
partial source success never means whole replay/main/QA success. `result.json`
contains hashes and logical output names only—no raw command, absolute host
path, traceback or `LEAN_PATH` value. Raw stdout/stderr are local diagnostics
inside the new output directory and must not be published wholesale. Always
retain failed outputs; a source edit requires new statement/review evidence
where applicable, not a modified acceptance rule.

`test_replay.py` consists of static parser/path/fixture tests; it does not launch
Lake or Lean. Run `python -B -m unittest -v test_replay`. It checks exact ordered
root coverage; extra, missing and duplicate axioms; provider/path rejection;
signature coverage; the typed negative fixture; resource thresholds; and the
bounded generated-helper graph boundary. Its synthetic strings are test
fixtures, not theorem evidence.

## Portable-test and dependency-parser corrections

Tests use Python's configured temporary-directory location and do not require
an unpublished `PRIVATE/` directory. A clean-package regression explicitly
checks path-test setup with no such directory. The caller may configure
`tempfile.tempdir` for its static test invocation.

Parent replay attempt `c408` freshly compiled the predecessor and completed
the source dependency query (both exit 0), then failed with
`IMPLEMENTATION_FAILED / observation_rejected`: the initial parser incorrectly
rejected repeated non-owned `Init.olean` lines legitimately emitted by Lean
for separate imports. The parent retains that failed output unchanged; this
is a replay-tooling bug, not a mathematical refutation or a source failure.
The parser now allows repeated non-owned dependencies while still requiring
exactly one matching own provider and rejecting duplicate own providers,
foreign providers with the same basename, and malformed dependency rows.
A platform-neutral repeated-`Init.olean` regression covers the actual case.
`REPLAY_HANDOFF-v2.md` binds this corrected runner and the static test result.

The frozen initial handoff, seals, source and prior run records remain
unchanged. This added runner has not been executed against Lean by its author;
the static tests alone do not constitute a new focused compilation receipt.
