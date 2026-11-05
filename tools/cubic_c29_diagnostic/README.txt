WIP: independent cubic c29 formal-runtime diagnostic, not scientific acceptance

CI2 direction: realCIlegacyFixtureimportbindingrepair, not new mathematics.
The first actual independent CI run38968346344/job117200296308 at commit40d7904
terminated: real fixture compile exit0/PID6427; fixture probe exit1/PID6433.
The fixture driver incorrectly imported the Cubic module despite runtime target
Fixture. FixtureProbe-v5.lean corrects ONLY its first import to Fixture; all
remaining bytes equal retained v4. Original v3/v4 files and actual CI failure
evidence remain preserved. Cubic Probe-v4.lean is unchanged. pins.json now
explicitly selects activeFixtureProbe, and runner checks both direct import and
runtime target against the requested fixture/Cubic modules before any Lean run.
Unit tests reject the actual old wrong-import driver and any target/key drift.
This fix does not establish that the remaining Lean APIs execute successfully.

Planned package: tools/cubic_c29_diagnostic/
Planned independent workflow: .github/workflows/cubic-c29-diagnostic.yml
No existing workflow, required check, verifier, theorem, scoring or acceptance
condition is edited. Rollback is deletion of this new job/workflow and package.

Probe.lean, expected-roots.json and validate-output.py are exact immutable
candidate3 copies. Original Probe.lean is RETAINED BUT NOT EXECUTED: a parent's
actual tiny-fixture run proved its module/import-all header cannot import a
legacy/non-module target. Active Probe-v4.lean removes the module/import-all
and meta-import header only; root identities and actual API algorithm remain
unchanged. It has independent pins. The package-local .gitattributes preserves raw bytes
when committed. pins.json fails closed on any changed raw target/provider
source/toolchain/manifest/lakefile byte or changed frozen payload; no newline
normalization or silent pin refresh is permitted. A mismatch requires resealing.

Workflow uses the existing lean-action@v1 configuration with auto-config false
and GitHub/Mathlib caches, then lake build BlockEncodingClassics solely to
prepare the five project providers. Runner executes inside lake env. Those
providers are inherited, not clean-transitive proof rebuilding. Linux actual
provider artifact hashes are collected anew; no Windows artifact hash is used
as a Linux equality claim. Inventory conservatively hashes potential olean,
private/server sidecars, IR/C/native-library files under configured roots; it
is NOT an actual-load tracer. Native libraries outside those roots remain an
explicit boundary. Runtime actual Lean binary and native invocation logs are
also bound. A fresh QuantumBlockEncoding namespace contains exact copies of
the five local inherited providers before target output is created, avoiding
first-namespace-root shadowing of BlockEncodingClassics.

Parent integration refinement: a configured but absent optional Lake search
directory is recorded as absent rather than mistaken for a required missing
module. All five required local provider files are still mandatory. If an
initially absent search directory appears during the diagnostic, the run fails
RESEAL; existing non-directory search roots are rejected. Actual imported/fresh
artifact checks and all acceptance boundaries are unchanged. Two focused tests
cover this distinction. This is diagnostic instrumentation, not verifier logic.

Runner creates exclusive _out/cubic-c29-diagnostic/{private,public,fresh,driver}.
Never reuse/clean an old output directory. Native help/prefix, separately bound
real legacy Fixture and fixture Probe, one target fresh compile, then the actual
Probe-v4 run are serial. Lean threads=1/memory=3072;
native help/prefix limit30s and target/probe limit600s each. Timeout kills only
the runner's own child and returns failure; no same-state retry. All PID, argv,
UTC, elapsed, native exit, stdout/stderr bytes and raw hashes are retained in
private/. Existing outputs/production/cache content are not overwritten.

Only public/ is uploaded, even on failure. Its text contains logical $PROJECT,
$TOOLCHAIN or $SEARCH_ROOT_n paths, credential/unknown-absolute-path redactions,
and rawSHA receipts. Original raw streams/setup/results stay private and are
never the upload path. No full environment dump is captured. The workflow
contents permission is read-only. Concurrency uses github.sha without cancelling
other runs. Python-only tests run before Lean setup. All streams/records use
no source alignment, no publication binding, no axiom-policy pass, no native
accepted and scientific_ROOT=false. Successful process exits certify diagnostic
output completeness only. Nonzero native exits or partial streams cannot pass.

319 is the explicit source-root vector (269 non-private, 50 private), including
7 opaque source declarations and 11 structures. Actual private names are resolved
with actual kernel ownership plus privateToUserName? and uniqueness checks;
never guessed numeric mangling. Each root reports actual type/universes/kind/
unsafe/collectAxioms. Opaque syntax does not imply no axioms. Generated target-
owned declarations remain a separate metadata partition. Their full type/axiom
audit is still pending; do not call this an all-target-owned trust audit.

The active Lean Probe/API phase has NOT been compiled by the decoder. Parent
tiny-fixture evidence confirms the original header failure; a legacy 512MiB
attempt hit the memory cap, so cascading diagnostics are not independent API
findings. No actual Cubic compile or 319 result is claimed. The Python unittest
synthetic streams are explicitly in-memory parser fixtures, not native Lean
evidence. Tests using an actual Python subprocess exercise logging failures,
not compilation. A small independent Lean axiom/private/opaque-body/structure
fixture is included as a separate real CI regression with a 3072MiB cap, not a
substitute Cubic certificate. Any actual Lean repair must create
a separately versioned probe/pins successor while preserving failed logs and
original candidate3 files. Actual CI is the intended next implementation test.
