# C368 RobinMatrix export-observation instrumentation

Frozen source and mock tests only. No Lean/Lake command was executed in C368.
The existing `qbe-substantive-worker` protocol keeps this an instrumentation
dependency, not a mathematical advance, independent semantic review, publication
approval, or scientific ROOT closure. Previously fully read protocol files were
personally re-hashed unchanged; this task re-read the worker skill itself.

## Exact target and correction

The pinned catalog has **395 selected rows / 395 ordinal, case-sensitive unique
names / zero exact duplicates**, all `experimental=true`, `openProof=false`.
Its source filter is exactly `QuantumBlockEncoding/RobinMatrix.lean`, whose raw
SHA256 is `1cca5119ac056fe041b25c529909b9fb6c3e4995e04ebde2f69e83fce47a0835`.
These catalog rows are NOT the exhaustive set of elaborated module exports.

An initial PowerShell default case-insensitive grouping incorrectly suggested
393 unique names. That diagnostic was retracted before any freeze. Personal
`.NET HashSet[string](StringComparer.Ordinal)` and `Group-Object -CaseSensitive`
checks both give 395. Python equality and all parser comparisons are case-sensitive.
The following four distinct names are regression fixtures, not duplicate rows:

```
QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinBlockEncodingProofRoute
QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute
QuantumBlockEncoding.Examples.RobinHeat.RobinOracleComposition
QuantumBlockEncoding.Examples.RobinHeat.robinOracleComposition
```

## Tool contract

After the existing actual Lean4.33 library + Tests full build, a future authorized
runner can call (paths relative to its repository):

```
python path/to/audit_robin_exports.py --repo . --out _out/robin-export-audit --full-build-report _out/installed-lean433-public/result.json
```

The input receipt must claim successful full library/Tests execution, bind current
source/config bytes, and supply actual Lean version/binary hash. Every receipt
input is checked before and after observation. The receipt is inherited evidence:
this tool neither re-runs nor independently attests that previous build. This
matches the already-existing `installed-lean433-full.yml` workflow's receipt;
no duplicate full-build mechanism or CI edit is added here.

Before any new input validation or subprocess, an old active report is archived
byte-for-byte under content hash and replaced with `success:false`. History files
are not overwritten. One writer per output directory is required; a lock blocks
ordinary concurrent execution. Do not use the output directory as a CI history
archive, and do not manually remove its lock while an audit is active.

The source pin is fixed in code (no CLI override). The tool checks all 395 exact
rows/flags/names, current raw catalog/config/source/olean/receipt hashes, then:

1. Runs `lake env lean --print-prefix` and `lake env lean --version`, binds the
   actual binary and exact version against the receipt.
2. Writes a fresh relative-path probe importing `QuantumBlockEncoding.RobinMatrix`,
   with `pp.fullNames=true` (printing only), and per-row CHECK / AXIOMS / END markers,
   `#check <fullName>` and `#print axioms <fullName>`.
3. Runs `lake env lean --deps <probe>` and requires exactly the production
   `.lake/build/lib/lean/QuantumBlockEncoding/RobinMatrix.olean` target selection,
   not an unrelated cached file with the same basename.
4. Runs `lake env lean -M1536 -j1 <probe>` with a finite timeout (default180s).
   Every command must return a captured `CompletedProcess`, exit0, and the final
   raw output must contain all 395 ordered exact-name/type/axiom observations.
5. Rechecks input/tool/probe/binary bytes. Only then writes observation success.

The per-attempt nonce is a freshness label, not random acceptance logic. Given
the same exact inputs and corresponding command output, decisions/classifications
are deterministic. Every stdout/stderr is saved in full before parsing and hashed;
failed/nonzero and timed-out partial output are retained too. Run-directory raw
logs may contain local paths; treat them as private and do not publish them
without separate sanitization. Report paths/commands are repository-relative.

The report includes all rows, full observed signatures and axiom lists, raw-log
hashes/lengths, tool/source/config/catalog/receipt/olean/binary pins and commands.
`#check` observes name/type output: it is NOT per-declaration semantic review.
Direct `--deps` and inherited full-build inputs do not establish a clean
transitive TCB or, from hashes alone, source-to-binary correctness.

## Parser / native disclosure

The strict grammar accepts one exact fully qualified `#check` signature followed
by one exact `#print axioms` message between each marker pair. Signatures may wrap;
the axiom list may wrap and its names may include numeric private-name components.
Unexpected warnings/prelude text, alternate quotation/name syntax, missing markers
or unfamiliar Lean output fail closed. The full raw output remains available for
a later explicit parser repair; no unknown form is declared successful here.

Observed actual historical Lean4.33 stdout was read in full (94 bytes):

```
'HermiteSourceSuffix.actualSuffix' depends on axioms: [propext, Classical.choice, Quot.sound]
```

This is a parser grammar witness, NOT C368 RobinMatrix output. Local Lean
`Print.lean` lines240–251 confirm both the list and no-axiom message forms.
`Init/Core.lean` lines2364–2453 and the full `Lean/Meta/Native.lean` identify legacy
`Lean.ofReduceBool`, `Lean.ofReduceNat`, `Lean.trustCompiler` and modern auxiliary
`_native.<tactic>.ax...` conventions; `Decide.lean` was only searched around its
nativeEqTrue call. Additional targeted native occurrence searches were not a
whole RobinMatrix semantic review; one broad occurrence output was truncated.

All axioms outside `{propext, Classical.choice, Quot.sound}` are disclosed as
additional. Native-name matches are separately marked by the explicit legacy-name
set / `_native.*.ax...` pattern; this is a source-informed naming classifier, not
a theorem of axiom provenance. Other additional axioms remain fully listed and
must not be interpreted as ordinary or harmless merely because unrecognized.
No axiom is removed or hidden, and additional/native dependence does not by itself
cause this observation tool to reject or approve a mathematical result.

## Tests and handoff

Command actually run: `python -B -m unittest -v test_audit_robin_exports`.
Exit0: **19 tests passed**, including real temporary fixture files/hashes but
**every subprocess mocked**. Synthetic output is labeled as such in tests.
Coverage includes missing files/name rows, exact duplicates versus case-distinct
names, bad flags, failed command, stale green invalidation/history preservation,
tampered source/config/olean/binary, no actual subprocess result, empty/missing/
case-mismatched output, wrong dependency selection, timeout partial raw capture,
failed full-build receipt and unknown print grammar. No real RobinMatrix green
report exists from this package.

Failure class: NONE for these mock tests; actual Lean integration remains PENDING.
Mathematical delta: none. Source/Lean graph and BE root are unchanged. No old
packet, production file, compiler option, verifier, scoring rule, axiom allowlist
or lint rule was changed. Discarded diagnostic: case-insensitive393 inference.
Promoted: source-only instrument with case-sensitive395 regression. Pending:
parent's actual post-fullbuild run, real output grammar/resource fit and review.
No parallel delegation. Direction: exact source-bound name/axiom observation,
not another mathematical proof lane. Process-memory context reused:
`QBE-PM-LOW-TOKEN-CONTROL-PLANE`, `QBE-PM-VERIFIER-SEMANTIC-LEVEL`.
Publication/purification/Exposition-Seal: not performed or claimed.
Recommended next step: parent inspect this freeze and execute its real CI gate;
any parser failure retains evidence and must not be converted into an old green.
