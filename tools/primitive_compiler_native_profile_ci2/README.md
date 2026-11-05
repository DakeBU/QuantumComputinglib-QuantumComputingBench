# C31 CI2 finite memory successor — private proposal, not installed

Direction: actual CI fresh-target internal-cap evidence to a finite gated
CI-only successor. This is ENV/instrumentation work, not a mathematical
refutation, new scientific objective, benchmark result or trusted-verifier change.
No Lean command was executed while preparing this proposal.

## Independently checked first failure

The authorized CI1 public ZIP SHA is
`a2edbb904f6be270e3b1c7dabc1090808390667ecf95f8dee323dbbe9de70dd6`.
`verify_ci1.py` actually verified all 21 unique safe members against the allowed
extracted public directory and all 20 raw-to-sanitized derivative receipt hashes.
Only that ZIP and public directory were read; no job raw log or other raw capture,
author context, mathematical review or other decoder result was consulted.

Actual help/prefix exits were zero. First target PrimitiveMacros used one thread
and --memory=3072; PID13289 exited -6 after 17.50306339 seconds, without timeout,
with empty stdout and a Lean interpreter memory_exception/excessive-memory
message. This is observed Lean internal memory-exception/SIGABRT evidence, not
OS OOM-kill proof or a source-mathematics failure. No completed fresh-cohort or
collector/signature receipt occurs in this bundle. Absence from the ZIP does not
prove that no unuploaded partial filesystem artifact ever existed.

The complete independently derived analysis, member hashes, UTC/PID/exit and
stream hashes are preserved in `actual-ci1-analysis.json`. Parent-reported
run/job/artifact identities are labeled as such in ci2-profile.json; this worker
did not fetch or independently authenticate the official API metadata.

The original failure artifact/capture is unchanged. This proposal does not
overwrite it, relabel it as successful, or promote Python tests to Lean evidence.

## Why 5120 MiB is only a candidate

The measured failure supplies a concrete reason not to repeat the 3072-MiB cap.
It does not report peak RSS or prove any replacement budget sufficient. The
requested 5120-MiB cap is a finite first CI-only candidate (not unlimited), with
one thread and a fixed additional 2048-MiB measured-headroom reserve. No host
capacity, successful compile, speed improvement or resource victory is assumed.
The test may still refuse the host or fail internally; there is no auto-escalation,
fallback cap, reserve reduction, patch/retry loop or local override.

Every actual native_call, including help/prefix, must first pass Linux GitHub-CI
context checks and real OS reads of /proc/meminfo MemAvailable, process cgroup
membership/mount metadata, and cgroup v2 memory.max, memory.current and memory.events
for the current group and every visible ancestor up to the mount root. Effective
headroom is min(MemAvailable, max(0,max-current) for all finite visible limits).
The required minimum is 7168 MiB. A cgroup value `max` is recorded as observed
unlimited and still bounded by measured MemAvailable/other finite ancestors.

v1, unknown or missing/malformed/ambiguous fields, hidden/delegated ancestor
limits, inconsistent metadata, non-Linux, non-CI and Windows refuse before any
child starts. This does not lower or change the original Windows/local resource
gate. Sampling is a point-in-time gate, not an OS memory reservation; contention
or invisible infrastructure constraints can still cause a later failure. There
is no claim of measuring peak process RSS or proving host isolation.

Each child has a new preflight; every raw resource-file read is SHA-bound with
actual parsed byte values and UTC. Postflight resources/OOM counters and existing
native PID/exit/timing/timeout/stdout/stderr hashes are retained as well. Metadata
gaps never grant success. Negative exits distinguish internal-memory SIGABRT,
SIGKILL without attribution, SIGKILL correlated with a cgroup OOM event (explicitly
not PID causation proof), wrapper timeout, Lean-reported API/implementation error,
and unclassified/startup failures. A failed call remains failed and stops the base
runner; there is no retry or other-process termination.

## Minimal adapter, unchanged scientific machinery

Install only after parent review, for example as the new sibling
`tools/primitive_compiler_native_profile_ci2/`. The frozen installed v1 package
and its 14-file manifest remain byte-identical. The raw 87-source-root profile
remains `72c0931c4c62906835d831742a3b797b381e947fbb8e3ecb58c4ad62aaa64473`:
79 public, 8 private, 3 modules. No foreign literal root/generated tables are used.

runner_v2.py loads the pinned old runner/validator and hash-pinned public shared
instrumentation. It adapts only the native_call callback and one narrow runtime
budget-description write. All CLI calls get --threads=1 and --memory=5120 only
after the resource preflight. The base's nominal budget field is recorded as
3072 and the actual executed budget as 5120, so the metadata does not lie about
the callback. Callbacks are restored in finally; installed files are not patched.

All original target-source/config/artifact before/after checks, isolated fresh
source/provider copies, same-cohort topological compiles, actual olean-path checks,
API private-name resolution, module-index generated enumeration, full type/kernel/
universe/unsafe/value-availability/recursive-axiom observations, structure fields,
87-root vector and disjoint complete generated partition remain the old pinned
code. Its exact collector, pp limits, strict validator and no-cache-fallback
checks are not weakened. Both new and old code/profile/source pins are checked
around every child. Unknown native fields and any nonzero exit still fail.

The original exclusive `_out/primitive-compiler-native-profile-v1` path is retained
only so the existing always-upload public path requires no change. It is never
deleted or reused: the original exclusive mkdir still refuses any pre-existing
directory. A future CI run must use a new clean checkout/job. Existing CI1 output
is not modified. The one-line workflow proposal changes only the command to the
new adapter; permissions, concurrency, artifact paths and existing required
checks remain unchanged. Parent must review and run the new Python tests before
installing anything; the old workflow's separate Python step is not silently
rewritten into new tests.

## Tests, output allowlist and rollback

Run the new implementation tests only:

    python3 -B -m unittest discover -s tools/primitive_compiler_native_profile_ci2 -p 'test*.py' -v

Fixtures are synthetic Linux resources. The only real child processes in the
tests are Python (zero/nonzero/timeout), not Lean. The --memory/--threads strings
after Python -c are script arguments, not a claim that Python enforces Lean caps.
`python-only-tests.json` contains the actual run receipt, not a fabricated native
log. No Linux hardware gate or fresh target/collector success was observed here.

The private review allowlist and hashes are in ci2-seal.json/ci2-bindings.json.
Resource read records include stable $PROC and indexed $CGROUP_ANCESTOR_n logical
coordinates, so sanitization does not collapse distinct ancestor observations
into an indistinguishable host-path placeholder.
Future runtime uploads remain restricted to the existing fail-closed sanitized
public directory, now with ci2-*.preflight/postflight/observation JSON and narrow
budget-binding metadata. Raw host paths/resources/logs remain private and raw
hashes remain available; sources, providers, binaries and private directories
must not be uploaded. No axiom whitelist is added. sourceAgreement,
axiomPolicyPass/publicationBinding remain null; all scientific/native acceptance
and trust-closure flags remain false. Inherited providers, non-load-trace OS
inventory, imported axiom-extension/native trust residuals remain unchanged.

Rollback before integration: leave this new proposal uninstalled. After optional
integration: revert only the one runner command to v1/runner.py and remove or
retire the new sibling adapter package, preserving all old14 bytes, manifests,
source/proposal seals, required checks and the first failure/raw evidence.
At process scope callbacks are restored automatically. No deletion, Git command,
workflow edit, installation or rollback execution was performed in this task.
