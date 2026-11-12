# C31 native profile v1 — private implementation proposal

No Lean command was run by this worker. The Python tests exercise synthetic
streams and real Python child-process failures/timeouts only. The original
source-only C31 reconstruction/seal is unchanged.

This is a bounded three-module executable profile, not a production-controller
refactor. Its 87 roots (79 public, 8 private) are mechanically rendered only
from this decoder's own sealed C31 inventory. There is no generated-name/count
baseline and no prior mathematical verdict. Shared code is limited to the
hash-pinned public `tools/cubic_c29_diagnostic/runner.py` instrumentation APIs:
safe paths, SHA/pins, native subprocess PID/exit/timeout receipts, artifact-type
OS inventory, optional-root partitioning, and redacted derivative export.
It does not invoke that module's C29 validators, profiles, expected sets or run.

## Proposed execution after parent review, on CI only

The proposed integration destination is
`tools/primitive_compiler_native_profile_v1/`. Copy the package intact, with the
manifest. This does not install the workflow proposal. A parent may separately
review/install it as a new independent job. Existing required checks remain
unchanged. The workflow has contents:read, SHA-scoped concurrency without
cancellation, and an always-step uploading only the sanitized public directory.

    python3 -m unittest discover -s tools/primitive_compiler_native_profile_v1 -p 'test*.py' -v
    lake build QuantumBlockEncoding.ReversibleClassical QuantumBlockEncoding.PrimitiveBasisLE QuantumBlockEncoding.CubicStatePreparation
    lake env python3 tools/primitive_compiler_native_profile_v1/runner.py

The last two commands are future CI instructions, not locally executed claims.
The runner refuses an existing output directory instead of clearing/reusing it.

## Exact evidence boundary

The runner pins raw profile bytes, package code/manifest, all three source
targets, 25 imported project-provider sources and all three source configuration
files. It checks source/config/code hashes before and after the diagnostic and
around target compilation. The shared instrumentation bytes are separately
pinned. It resolves the actual Lean binary and hashes it; inherited external
artifact files under configured roots are OS-inventoried and rechecked. Missing
optional search roots are explicitly recorded and must remain absent.

All 25 project provider artifacts are copied, with available sidecars and
before/after hashes, into an exclusive fresh filesystem module namespace. The
original project build root is removed from LEAN_PATH, and other unexpected
project fallback roots are rejected. The target sources are copied byte-for-byte
and compiled separately in order PrimitiveMacros, UniformlyControlledRy,
CubicAmplitudePrimitive; target artifacts cannot be inherited or reused. Later
compiles and the observer see the same fresh cohort. Every target's actual
findOLean/realPath is compared with that cohort. This preserves the original
Lean module names; it does not rewrite mathematical namespaces or source bytes.

The collector uses Environment module indices for complete ownership, and
isPrivateName/privateToUserName? for unique private roots, never private-name
numeric guessing or namespace-prefix ownership. Every source root and every
owned non-source constant gets actual kind/kernel agreement/type/universes,
unsafe/value-availability, recursive collectAxioms, self-occurrence, actual
axiom/opaque and source-opaque observations. Generated is exactly the enumerated
owned set minus resolved source roots. Full ownership lists and structure
field/projection/constructor metadata must match the disjoint emitted partition.
New generated identities are allowed only when actually enumerated and fully
observed; the first run cannot pretend to know their count or names.

Types use actual Meta.ppExpr with pp.deepTerms/proofs/explicit/universes/fullNames/
privateNames/binder types enabled and notation disabled. pp.maxSteps=2,000,000
and maxRecDepth=10,000 are finite bounds, not a completeness assumption: any
type containing ⋯ or … fails. Values are explicitly NOT requested, including
ordinary proof values; value text is null with availability separately observed
through value?(allowOpaque=true) and hasValue. Actual axiomInfo has no body and
its self-dependency must remain in the observed recursive axiom set. No body is
inferred, reconstructed or fabricated from an opaque/source/native label.

This is not clean-transitive, not an actual native load trace, and not a full
trust closure. collectAxioms uses Lean's actual imported exported-axiom extension
and available local bodies. Inherited provider trust/native mechanisms and
dynamic libraries outside inventoried roots remain explicit residuals. No axiom
whitelist is introduced. sourceAgreement, axiomPolicyPass and publicationBinding
remain null; scientificAcceptance/nativeAccepted/trustClosure remain false.
Even a complete future runtime stream is not scientific acceptance or source
agreement. Fresh source/runtime diagnostics do not replace repository gates.

The validator rejects nonzero/unknown/timed-out exits, zero-exit partial streams,
missing/duplicate/colliding roots or generated constants, duplicate JSON keys,
wrong bindings/options, missing kernel/type fields, ellipses, source-kind drift,
incomplete structure metadata, incorrect partitions and any acceptance claim.

## Public-safe derivative allowlist and rollback

Only the runner's `public/` derivative files may be uploaded: sanitized stdout/
stderr text and redacted JSON input/provider/copy/cohort/driver/process/result/
completeness records, with raw-to-derived SHA receipts. Raw source copies,
profile/collector binaries, .olean/.private/.server/.ir/native provider files and
the entire private directory are excluded. Redaction is inherited fail-closed;
the raw hash receipts do not publish private bytes. The private proposal code
and profile are for parent review, not a scientific publication artifact.

Rollback is to leave this proposal unintegrated (no production mutation has
occurred). After optional integration, remove only the separately added package
and separately added workflow job/file, preserving existing tools/workflows/
required checks and any collected raw evidence. Never delete the original C31
source seal. No automatic cleanup/reset/deletion is included here.
