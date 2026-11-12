# First shared QIT slice: local verified handoff

Status: PROVED_LOCAL experimental adapter; independent admission pending.
No production, canonical source/publication ledger, dependency, test registry,
commit or deployment file was edited. Owned files are only this directory.

## Mathematical delta and source round trip

For a shared finite vector psi with sum_i conjugate(psi_i) psi_i = 1, the
literal matrix P_ij = psi_i conjugate(psi_j) is positive semidefinite, has
trace one, and satisfies P P = P. Positivity follows because every quadratic
form is the squared modulus of the inner product with psi. Trace is the
sum of diagonal squared magnitudes. Multiplying outer products gives
P P = psi (psi-dagger psi) psi-dagger = P by source normalization.
This is the forward projector assertion of the source's p.4 paragraph tied
to Definition 2.1 and Eq. (2.4), not its extremal-point/rank characterization.
This round trip is author evidence, not independent decoder approval.

Named roots (module `FirstSlice`):

- `QITFirstSlice.pureState_density`
- `QITFirstSlice.pureState_projector`

No new quantum state, density, tensor or unitary definition is introduced.
The vector carrier is shared `ConcreteSemantics.StateVector`; matrix
compatibility with shared `ConcreteSemantics.FiniteMatrix` is definitionally
checked by a test. PSD, trace and outer product are Mathlib objects. The sole
logical premise is source unit norm, with no EXCESS ingredient binders.

## Focused gate evidence

2026-10-08 final focused command (proof object generation, then test compilation)
terminated with exit code 0. Last handle 97000 is complete; no live terminal
process remains. Six checked tests in `FirstSliceTests.lean` cover:
definitional matrix compatibility; normalized complex-I projector; arbitrary
basis family density; failure of normalization for amplitude 2; impossible
empty-dimensional normalization; non-real off-diagonal conjugation orientation.

Final axiom reports for both roots:

```text
[propext, Classical.choice, Quot.sound]
```

No `sorryAx`, custom axiom, opaque acceptance token or executable checker is
used. A lexical placeholder scan of owned Lean files returned no matches.
An initial successful proof/test run was followed by import minimization:
too-small intermediate imports lacked Complex order/StarOrderedRing instances;
the final import `Mathlib.Analysis.Complex.Basic` restores them without the
unneeded spectral-analysis module. Those intermediate API failures did not
change the signature or source contract.

Repository aggregate `lake build` / `lake build Tests` is owned by the root
integration worker and has not been duplicated here. It must pass against the
final frozen cohort before integration. These experiments are not Lake roots;
the focused commands are therefore additionally required. Site/publication
gates, source-blind decoder, distinct anti-anchored reviewer, topology reviewer,
and Exposition Seal are pending. Do not claim PROOF_SEALED or PURIFIED.

## Replay from repository root

PowerShell:

```powershell
lake env lean -o experiments/qit-first-slice/FirstSlice.olean experiments/qit-first-slice/FirstSlice.lean
$env:LEAN_PATH = (Resolve-Path experiments/qit-first-slice).Path
lake env lean experiments/qit-first-slice/FirstSliceTests.lean
```

POSIX equivalent (portable commands, not executed on this Windows host):

```sh
lake env lean -o experiments/qit-first-slice/FirstSlice.olean experiments/qit-first-slice/FirstSlice.lean
LEAN_PATH="$PWD/experiments/qit-first-slice${LEAN_PATH:+:$LEAN_PATH}" lake env lean experiments/qit-first-slice/FirstSliceTests.lean
```

Source replay: download the primary URL named in statement-seal.md into the
ignored `cache/source.pdf`, verify its SHA256, then
`pdftoppm -f 3 -l 4 -scale-to 1700 -png cache/source.pdf cache/page` from this
directory and view both complete page images. No copyrighted PDF/render is
vendored; local `.gitignore` was checked to exclude all caches and Lean objects.

## Exact bindings

| Artifact | SHA256 |
| --- | --- |
| PDF | `90784b02b568b8c7bb6a1ec20588d801541d047779333bd2b2b8e63749dc0fe3` |
| pre-proof statement seal | `56f10f781b9fe88f19a5380b9fe69c3e6797a3781545a6b8b1f0f4401057ff0f` |
| pre-proof source topology | `94d63e64895d395e7527999627a29b073dab32ff6d2292ceba6fef9077247c72` |
| reuse audit | `203a4db2a3e26ce49f2bf9dd20c6b3f4decd5cbf9327bdb41989fd810dfd6850` |
| final FirstSlice.lean | `ac2f4f74e1ff523067adfc09ff5711a64d70330b669119ee61f67a133af91eb5` |
| final FirstSliceTests.lean | `55f4c75768d63f9f89246fbc14c2571b7878925edf16875d9ad583444b021c83` |
| shared ConcreteSemantics.lean | `4b4e1c3612ea2d4eed3a2d5dbfec39ffae81263fd9ceb521c1a59231f786caa1` |
| lean-toolchain | `302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b` |
| lake-manifest.json | `510171e8214a2ac5e00f16c1bf92ad474d2de42c4cd2dc2b3d411272f7b58763` |

Lean 4.33.0, compiler commit `d8b18978322de05a8f3dba51ef03cf5461676c17`;
Mathlib manifest rev `db584cd6d46c92f209a44c0f1c829460d327499d`.
Repository HEAD at inspection `8c341b099e21ca98c264076837f10787a80d0c8f`;
working tree already dirty. Root-supplied production proof input digest
`5a8f47f8d0afd1d4f957e55babde52a9e9c01babf05c481b988e99ebca2f7758`
is provenance only, not independently recomputed or inherited as this gate.

## Protocol handoff and remaining boundary

- Objective/frontier: first finite pure-vector -> positive trace-one projector
  interface needed by the peer QIT textbook, not a full section/chapter claim.
- Graph delta: bounded source-to-semantics bridge; all four distinct graph
  views and exhaustive p.3-p.4 dispositions are in source-topology.md.
- Existing substrate: ASPBE finite carriers and pinned Mathlib algebra.
  Bookkeeping: normalization orientation and complex conjugation conventions.
  New topology/novel quantum primitive: none claimed.
- Failure class: NONE at final focus; transient import minimization was
  API_BLOCKED, corrected by the explicit complex-instance import.
- Salvage: both roots compiled; no failed proof residue retained. Promotion
  remains pending canonical/independent review, especially wrapper-only audit.
- Process memory: `QBE-PM-LOW-TOKEN-CONTROL-PLANE` and
  `QBE-PM-VERIFIER-SEMANTIC-LEVEL`; no simulator as theorem evidence.
- Direction fingerprint: source-pure-projector/shared-carriers/direct-Mathlib;
  expected gain is an exact source bridge without duplicate density APIs.
- Parallel admission: distinct source interface task authorized by parent;
  this worker spawned no subagents. Only one proof route survives, so no
  multi-route comparator or common-blind-spot verdict is manufactured.
- Default route: direct reused algebra. No copied external quantum proofs or
  OpenAI/math foundation. External upstream retrieval remains design evidence,
  not a compiled/pinned dependency.
- Purification/Exposition Seal: pending admission. Local residue/import scan
  complete, exact source/Lean expansion preserved; no claim of independent
  accepted review. No production promotion recommended before fresh review.
- Boundary: no rank-one/extremal converse, convexity/compactness, spectral
  theorem, ensemble/measurement/Born-rule, unitary action, tensor/partial trace,
  channel, representation theorem, circuit, approximation or resource result.
- Next dependency-ready choice after review: source-backed unitary conjugation
  invariance above the shared unitary gate API, or rank-one characterization
  with a separately sealed rank/extremal target. Neither follows by status
  promotion from this packet alone.
- Residual risk: source-forward interpretation and ComplexOrder/PSD convention
  require independent semantic review; focused Lean confidence is high.
