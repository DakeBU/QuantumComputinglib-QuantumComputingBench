# C31 CI3 root-interface correction — private proposal

Status: Python-tested proposal only; not installed and no Lean run by this worker. No successful C31 fresh-target or collector evidence is claimed. Acceptance/sourceAgreement/axiomPolicyPass remain false/null. This is an ENV/API correction, not a mathematical change or refutation.

## Actual CI2 boundary

`verify_ci2.py` checks the authorized ZIP SHA, exact four members, byte equality with the authorized extracted public directory, and all three public derivative receipts. The old observation failed before child startup at 01-help, with FileNotFoundError and incomplete accounting. MemAvailable was 15220740096 bytes, above 7516192768 bytes, but that alone did not establish effective headroom. The old public snapshot lacks a failed logical coordinate. The actual missing file cannot be localized to the root from that evidence. All old CI1/CI2 artifacts and all earlier seals remain unchanged.

## Exact versioned delta

Only `runner_v3.py` and `resource_gate_v3.py` are new runtime code. The thin adapter loads the exact sealed installed CI2 package, which loads the unchanged V1 14-file package and shared runner. All prior SHA checks, source/config pins, same-cohort fresh compilation, private-name APIs, dynamic owned/generated partition, exact 87 roots / 3 modules, signatures/types/universes/unsafe/value availability/recursive axioms, ordinary-value request boundary, provider OS inventory/redaction, PID/timeout/exit/UTC/raw stream hashes and no-cache-fallback remain in the old code. No mathematical vector is copied or changed.

The callback's captured default sampler is deliberately replaced through a temporary factory, not merely by changing a module name. CI3 code/profile/manifest and CI2 code/seal pins are rechecked together with all prior pins before/after every child. Both adapter layers restore hooks in finally blocks. Existing `ci2-*` runtime filenames/schema binding coordinates are retained for compatibility, but resource snapshots have a distinct CI3 schema and nested ci3Binding.

## Root applicability and resource gate

Before treating a boundary as real root, require one cgroup2 mount, its mount root exactly `/`, and actual readlink observations for both self and PID1 cgroup namespaces equal to the explicitly documented reserved initial-namespace implementation fingerprint. Equal but dynamically allocated namespaces, delegated/hidden mount roots, unknown/missing/permission-denied observations, v1/ambiguous membership, and root-only process shapes all fail closed. Root-only is conservatively unsupported, even though the API itself permits root members. See PRIMARY-SOURCES.md for source and trust limits.

Every non-root ancestor's memory.max/current/events is still actually read and hashed. Missing any one is a failure, never unlimited. At the verified real root, mandatory cgroup.controllers (including memory) and cgroup.procs are read and hashed. The three documented non-root-only memory interfaces are explicitly `DOCUMENTED_TRUE_ROOT_NOT_APPLICABLE_NOT_UNLIMITED`, with value null, readRequested false and unlimitedObserved false. They are not fabricated as max, not charged zero usage and not inserted as synthetic unlimited cgroup rows. Every attempted read/readlink is recorded before I/O; exceptions retain errno/type, attempted logical path, UTC and atVerifiedMountRoot, including failures.

The measured minimum remains min(MemAvailable, max(0, memory.max-memory.current) for each finite non-root ancestor). It must be at least 7168 MiB = 5120 MiB budget + 2048 MiB reserve. One byte less fails. Threads=1; only Linux with explicit GitHub CI identity is eligible. Windows/local higher-budget use is forbidden; the original local gate is untouched. There is no lower threshold for a nominal 7-GiB runner. The unchanged process classifier distinguishes internal cap exceptions, wrapper timeout, SIGKILL with/without event correlation, API errors and incomplete metadata; it does not infer OS OOM from an interpreter memory exception.

## Public-safe evidence and hashes

Runtime raw JSON/logs remain private. Stable `/proc` interface coordinates are fixed API names; cgroup hierarchy/member/mount paths may contain host-specific identifiers and must not be published raw. The unchanged shared exporter produces explicitly redacted/logical derivatives and a separate raw-to-public receipt. `$PROC`, `$CGROUP_NONROOT_n` and `$CGROUP_REAL_ROOT` are logical coordinates, not claims that raw bytes had those names. fileReads.sha256 always hashes original OS bytes, never a rewritten path string; namespaceReads.sha256 explicitly hashes READLINK_TARGET_UTF8, not file bytes. Public derivative SHA belongs to the separate derivation receipt, and may differ. Failed reads have no invented byte hash. Do not publish private snapshots, raw mountinfo/member strings, raw logs, provider binaries, source copies or full environment.

The seal's `publicSafeReviewAllowlist` is the exact only review-package file allowlist; no directory glob. The runtime public allowlist remains only existing sanitized exporter derivatives, including the pre/post/observation JSON with nested CI3 bindings. Input ZIPs and old installed packages are not copied into this package.

## Review, install and rollback (parent-owned)

After full review and Python gate, the only proposed installation is a new `tools/primitive_compiler_native_profile_ci3/` directory containing the seal allowlist and the single command-line replacement in workflow-one-line.PROPOSAL.patch. No existing package byte is replaced. Existing upload path, permissions contents:read, SHA concurrency/cancel=false, always sanitized artifact upload, optional-job and required-check semantics stay unchanged. This worker does not install or trigger CI. New execution must keep the inherited exclusive output-directory check; never delete/reuse a prior output to force a run.

Rollback is one line back to the CI2 entrypoint, or disable this optional job. Keep the failed run and its bytes; do not rewrite a failure. Removing an unneeded newly installed CI3 directory is parent-controlled and not required for rollback. No verifier, scoring, trust policy, registry, target or production source changes.

Python development provenance: an initial 12-test run had three fixture-write permission errors from sandbox system-temp redirection; fixture temp directories were moved into the exclusive proposal subtree. A following run exposed a synthetic low-memory fixture incorrectly using max (unlimited); the fixture was corrected to a finite parent, without weakening the gate. The final sealed receipt is the actual later Python run; none of these steps invoked Lean.
