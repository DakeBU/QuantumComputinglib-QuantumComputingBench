# Polynomial-resource Hermite preparation frontier

Root acceptance target: the unchanged normalized Hermite sample state, an
explicit primitive circuit with clean ancillary output, and polynomial-in-data-
width resources with separately stated parameter/precision/preprocessing costs.
This is a live frontier, not a rewrite of historical trial results.

**Highest certified frontier:** the complete exact-real quantum circuit root
is closed. The all-parameter bound is `48*n_p*(2*k+6)^3` on the actual list
length, with `ceil(log2(2*k+6))` clean bond wires and zero oracle calls.
The full classical-cost and uniformly rounded executable gate remains open.
The original exponential reference remains unchanged.

| Node | Interface | Checked Lean evidence | Current status |
| --- | --- | --- | --- |
| H0 | Literal polynomial/splice, positivity, normalized reference | `HermitePolynomial`, `HermiteSmoothness`, `HermiteStatePreparation` | existing certified baseline |
| R1a | Exact sample cuts through width `8*k+12` | `HermiteSampleStructure.sampled_cut_factorization`, `normalized_cut_factorization` | compiled algebraic alternative; not needed as a free premise of the new root |
| R1b | Monomial polynomial transfer | `HermiteTransferCores.sourceInterpolant_transfer` | compiled reusable algebra; direct float implementation failed |
| R1c | Positive Bernstein coefficients, restriction and readout | `HermiteBernstein.sourceInterpolant_bernstein`, `sourceInterpolant_subdivision_readout` | compiled |
| R1d | Complete three-branch source kernel of width `2*k+6` | `HermiteBoundaryInjection.hermiteKernel_eq_sample`, `hermiteFiniteBond_card` | compiled for every path, not numerical rank |
| R2a | Thin real LQ, including rank deficiency | `ThinLQ.exists_thin_lq`; `ConstructiveThinLQ.factor_correct`; `StoredThinLQ.compile_R`, `compile_Q`, `compile_total_cost_le` | existence baseline retained; deterministic stored factor supplier and scoped exact-real cost compiled |
| R2b | Supported sequential action and terminal cleanup | `SequentialBondPreparation.run_eq_transfer_of_supported`, `run_terminal_clean` | compiled generic bridge |
| R2c | All-length canonicalization and no bond growth | `TensorTrainCanonical.exists_rightCanonical`; `ConstructiveTensorTrain.canonicalize_action`, `canonicalize_maxBond_le`, `stateBoundary_normalized` | actual deterministic producer compiled; baseline basis choices no longer needed by new quantum producer |
| R2d | Preserve active columns in SO completion | `ConstructiveIsometryCompletion.complete_spec`; `ConstructiveIsometryLocal.completeStage_spec` | actual deterministic completion compiled; finite swaps/parity, no determinant evaluation or chosen basis |
| R2e | Kernel to actual bounded normalized chain | `MatrixProductChain.ofKernel_contract`; `HermiteFiniteChain.sourceChain_contract`, `sourceChain_normalized`, `sourceChain_storage` | compiled; no assumed target-action oracle |
| R2f | Varying active ranks to one padded schedule | `TensorTrainSchedule.exists_normalized_preparation_schedule`, `paddedAt_active_isometry` | compiled |
| R3a | Selected real plane to actual recursive RY/CX list | `compileSelectedRy_eval_plane`, `compileSelectedRySteps_cubic_bound` | compiled |
| R3b | SO decomposition, Gray transport and actual local compiler | `AdjacentGivens.decomposeSO_matrix`; `GrayGivensCompiler.compileSO_eval`, `compileSO_cubic_bound`; `TensorTrainLocalCompiler.exists_local_circuit_with_resources` | compiled; all local instructions counted |
| R3c | Actual gate placement, public LE order, clean full state | `SequentialPrimitiveAssembly.publicCircuit_column`; `TensorTrainWord.sampleEquiv_public`; `TensorTrainPrimitivePreparation.publicCircuit_clean` | compiled; no uncharged arbitrary initial state |
| R3 | Complete source-derived polynomial-gate quantum root | `HermitePolynomialPreparation.exists_polynomial_preparation`; `ConstructiveHermitePreparation.prepare_spec` | both roots passed the full Lean gate, including every production/test module; publication integration recorded separately |
| C1 | Non-enumerating source norm | `TensorTrainNormEnvironment.gram_eq_sum`; `HermiteFiniteNorm.localSampleNorm_eq_sampleNorm`, `sourceChain_eq_local`, `norm_arithmetic_budget` | compiled; local schedule <=`9*n_p*D^3` add/multiply, plus one sqrt |
| C2 | Deterministic core/basis/angle computation and total real-operation cost | no complete implementation-level cost theorem | open; small matrices alone are not a runtime proof |
| C2a | Stored rectangular elimination and thin LQ | `StoredRectangularGivens.compile_total_cost_le`; `StoredThinLQ.compile_total_cost_le` | compiled cubic local bounds, including cached transforms and copying, in a declared exact-real model |
| C2b | Stored positive-coefficient interval restriction | `StoredBernstein.restrict_value`, `restrict_total_cost_le` | compiled actual producer, <=`20*d^3+42*d^2+32*d+13`; source coefficient/cutoff/exp generation not included |
| C2c | Stored all-length TT canonicalization | `StoredTensorTrain.canonicalize_refines`, `canonicalize_total_cost_le` | compiled equality to actual deterministic result and polynomial stored-operation bound; not a complete source compiler |
| C2d | Stored active-column completion | `StoredIsometryCompletion.complete_value`, `complete_total_cost_le` | compiled actual completion refinement and local polynomial cost; suppliers charged separately |
| C2e | Exact-comparison source cutoff | `HermiteBinaryCutoff.compute_value`, `compute_cost` | scoped compile passed: exactly `n_p` comparisons and `2*n_p` real field operations; finite-bit classification remains C3 |
| C2f | Explicit source-bond layout | `HermiteExplicitBond.bondEquiv`, `same_literal_source`, `rawSourceChain_norm` | scoped compile passed: executable layout and unchanged observable source, not old/new matrix-entry equality or complete core production |
| C2g | Stored source Bernstein coefficients | `StoredHermiteCoefficients.compile_value`, `compile_pos`, `compile_total_cost_le`, `compile_exponentialCalls` | scoped compile passed: ordinary counters <=`864*(k+1)^2`, plus one separate exp call; raw-chain assembly still open |
| C2h | Stored norm environments | `StoredTensorTrainNorm.gram_value`, `norm_value`, `norm_total_cost_le` | cached two-pass Gram supplier and signed/zero/internal-zero-bond tests passed; full cycle-04 Lean and website integration passed; whole compiler composition remains open |
| C2i | Stored recursive local rotation emission | `StoredSelectedRyTrace.compile_value`, `selected_value`, `selected_total_cost_le` | scoped compile passed: full ordered trace equality and local stored-operation ledger; angle evaluation, physical whole-pipeline placement and serialization excluded |
| C3 | Input representation, cutoff separation, rounding, bit complexity | no uniform epsilon/cost certificate | open; real scientific input and rational executable input remain distinct |
| C2j | Actual stored source from k,n,L | `StoredHermiteRawSource.raw_value`, `raw_contract`; `StoredHermiteRawCost.raw_certified` | full canonical Lean and local website integration passed; same actual raw chain, polynomial ordinary work and separately counted exp/integer operations |
| C3a | Actual RY and whole-circuit conditional error | `PrimitiveRyPerturbation.eval_ry_distance`; `PrimitiveCircuitPerturbation.prepare_conditional_clm_distance_le` | full canonical Lean and local website integration passed; supplied aligned circuit and angle accuracy, not a numerical backend |
| M1 | Interval masses and actual-grid `Z>=1` | `HermiteIntervalMass.hermite_polynomial_mass`, `exponentialMassClosed_eq`, `sampled_mass_ge_one` | compiled; independent target/norm validation reuse |
| M2 | Coherent mass/angle arithmetic with uncompute | no supplied circuit | inactive alternative, not combined into the MPS quantum circuit |
| K1 | Exact-signature retrieval and narrow instantiation | 32 checked signatures, 6 applications; context-pack regression | diagnostic; no claim of general workflow speedup |
| X1 | Saved-QASM replay and non-enumerating large-width construction | MPS-02 `n=8,k=8,L=10/300` finite replays; `n=128` original-backend streaming scan; cycle-03 recursive replay and 129-case exact trace comparison | finite numerical/cross-language evidence; not a uniform backend certificate |
| X2 | Rounded backend refinement and independent family acceptance | no uniform backend/rounding theorem | open |
| ROOT | Full frozen scientific and classical/executable resource contract | R3, C1, C2, C3, X2, integration gates | open; exact quantum sub-root closed |

## Next admissible work

1. Revalidate the cycle-05 supplier in the current Lean/toolchain context and
   retain its source/publication debt separately from compilation. Its actual
   raw-chain producer already exists; do not schedule a duplicate implementation.
2. Admit the staged same-run normalized canonical supplier below after genuine
   independent review, then extract stored active columns and compose completion
   and the local Gray emitter. Charge angle instantiation and final placement;
   local cost theorems still do not bound the whole classical compiler.
3. Relate one executable primitive backend to the proved backend, then budget
   input approximation, core rounding, orthogonalization and angle error.
4. Keep any approximate tolerance explicit; finite Qiskit checks never close a
   symbolic all-parameter certificate.

[Cycle-04 evidence and remaining composition work](../experiments/hermite-polynomial/CYCLE04-RESULT.md)
separates scoped checks from full publication acceptance. No C2/C3/X2/ROOT
status is promoted merely because a supplier compiles.

The five cycle-04 interfaces C2e--C2i also passed the complete local publication
pipeline with proof-input digest
`448914e875837c53a5b2a5d08260c9eab4009eb75fd6a9e60503b66aeaf1866a`.
This integration acceptance does not change the open C2/C3/X2/ROOT boundary.

The [cycle-05 source and accuracy packet](../experiments/hermite-polynomial/CYCLE05-RESULT.md)
records the new source composition, conditional angle bound, preserved
regressions and explicit operation-model omissions. Its proof inputs differ
from cycle 04 and require their own integration gate.

## Preserved falsifier

MPS-01's direct monomial/mask arithmetic had normalized state error about
`1.529` at `(n_p,k,L)=(8,8,10)` despite near-orthonormal QR, and overflowed
for `L=300`. MPS-02 changes the representation, not the target. Its float64
success does not prove a uniform precision bound. Do not repeat the failed
route unchanged or accept norms/isometries in place of actual source action.

Diagnostic nodes are not mathematical dependencies. A crossover must name
the shared verified interface; no lineage transfers an unearned certificate.

## 2026-10-08 bounded staging frontier (not production admission)

The current Lean 4.33.0 checkout passed a fresh exhaustive 202-module gate,
with proof-input digest
`5a8f47f8d0afd1d4f957e55babde52a9e9c01babf05c481b988e99ebca2f7758`.
New experimental files were checked separately; they are not silently covered
by that production-module inventory.

- `QuantumBlockEncoding.StagedNormalizedCanonical.compile_certified` now
  proves the same actual normalized/right-canonical chain, its literal Hermite
  contraction, bond bound and declared-model polynomial cost. With `N=n+1`
  and `D=2*k+6`, the ordinary bound is
  `rawBudget k n + N*(200*D^3+141*D^2+49*D+14)+10*D^2+44*D+100`.
  Raw exponential and selected integer counters are carried through unchanged.
  Signed residuals are read and absorbed, not replaced by positive norms.
- `QuantumBlockEncoding.HermiteExplicitControlsCandidate.selected_plane`
  removes choice-based control enumeration through an explicit increasing skip
  table. Its actual stored trace has cost at most
  `(16*q+12)*2^q+5*q^2+14*q`, including cached table/pattern traffic.
  Gray target discovery, input-word production and angle instantiation remain
  separate suppliers. This local `q` is not the data width; the Hermite caller
  must supply the existing logarithmic bond-width relation.
- The preserved float64 falsifier at `(n_p,k,L)=(1025,0,1/100)` motivated an
  isolated positive-scaling mutation. All 32 MPS tests passed after independent
  rerun, including old failure retention and large cache-only diagnostics.
  This is not an exporter replacement, uniform backward-error proof or family
  executable acceptance.

Evidence and exact scope: [staging result packet](../experiments/hermite-polynomial/stored/cycle06-staging-result.json).
The first two items are **PROVED_LOCAL**, not independently source-reviewed,
production-admitted, merged or purified. C2/C3/X2/ROOT remain open. In particular,
the bound omits complete primitive emission and finite-bit/transcendental/index
costs; those omissions cannot be hidden by summing unrelated supplier ledgers.

### Cycle 7 exact provider and scaling bridges

`HermiteGrayTargetCandidate.discover_step_target` now proves that an explicit
parity recursion returns the very same unique physical target as the existing
Gray compiler. Its actual returned record uses at most `2*w` quotients,
`w` remainders and `w` comparisons for local width `w`. The stored Gray-word
producer additionally proves exact bit equality and ordinary cost at most
`8*w*(w+9)`, including vector materialization. Its selected integer work is
explicitly overcharged under `field`, not reinterpreted as real arithmetic.
Evidence: [Gray target packet](../experiments/hermite-polynomial/stored/gray-target-result.json).
These close the target-discovery and stored-input-word subinterfaces locally;
angle instantiation, SO sweep/log composition and physical final placement
are still separate. Local width is bond width plus one, not `n_p`.

`ExperimentalScaledInvariant.hermite_target_public` now proves literal signed
Hermite amplitudes are unchanged by exact positive per-core scaling and
subsequent normalization. The removed product, compensating Gram norm,
signed boundaries, storage/bond invariance and scaled residual absorption
are proved with the existing TT semantics and explicit public LE adapter.
Evidence: [scaling invariant packet](../experiments/hermite-polynomial/precision/scaled-invariant-result.json).
The factors are supplied exact positive reals; this does **not** prove the
computed max-scales, QR, float contractions, underflow, mantissa/exponent
arithmetic or saved circuit. It supports the mathematical mechanism of
`MPS-02-SCALE-01`, not a certified numerical backend.

Both new files passed master focused checks under Lean 4.33.0 and use only
ordinary `propext`, `Classical.choice`, `Quot.sound` in the printed roots.
The production/test sources and proof-input digest are unchanged, and the
full `lake build` and `lake build Tests` passed again. Independent review,
production/reader integration and C2/C3/X2/ROOT remain open.

`StagedActiveColumns.hermiteStage_certified` additionally consumes the actual
returned normalized chain and supplies an actual stored local SO completion,
with physical column action and source-plus-stage cost. The stored matrix is
proved equal to `ConstructiveIsometryLocal.completeStage` under the explicit
bit/bond coordinates, not just an arbitrary existential completion. Extraction
costs at most `22*S*r+8*S+3*(t+1)`, prefix positions exactly `5*r`, and the
existing stored completion bound is charged separately (`S=2^q`, actual rank
`r`, stage `t`). The master recompiled the frozen normalized dependency into
an ignored relative cache, then independently checked every extraction,
completion and regression proof with exit zero.
Evidence: [active-column packet](../experiments/hermite-polynomial/stored/active-columns-result.json).
An all-stage compiler must bind the source once and call `completeAt` on that
cached chain; repeated `hermiteStage` calls rebuild the source. Traversing
from the root for each stage adds a quadratic classical traversal term.
This local provider is not complete C2 or primitive-emitter closure.

### Cycle 8 actual stored primitive-stage composition

`StagedStagePrimitive.compileAt_eval` now composes the actual cached chain's
`completeAt` matrix, a charged materialized Gray reindexer, and the actual
stored SO sweep/reversed-inverse log/selected-RY emitter. Its returned elementary
primitive circuit equals the existing named `completeStage` matrix exactly,
including signs, physical low-bond/high-data wire order and active-column action.
Generic SO premises are derived inside the composition, not added to Hermite's
public source contract. The same return has a checked sum-of-actual-run cost:
`ActiveColumns.stageBudget(q,rank,t) + 8*GrayTable.tableBudget(q) + LocalSOEmission.compilerBudget(q)`.
All three new files passed master focused compilation under Lean 4.33.0;
printed roots depend only on ordinary `propext`, `Classical.choice`, `Quot.sound`.
Evidence: [stage primitive packet](../experiments/hermite-polynomial/stored/stage-primitive-result.json).

With `H=2^(q+1)`, `E=H*(H-1)/2`, `G=2^q+2*(2^q-1)`, the actual local final
gate count is `E*G`. The emission ledger is separately `E*(1+2*G)`, because
it also charges intermediate sweep/template records. No optimization or
resource improvement is inferred from that difference. Selected natural
index operations remain explicit field-tag overcounts, not bounded-bit
arithmetic. The source must still be bound once across all stages; global
placement/copying, whole returned-circuit Hermite action, numerical/finite-bit
cost and independent serialized executable acceptance remain open. This is
a higher **PROVED_LOCAL** C2 subfrontier, not C2/C3/X2/ROOT closure or admission.

### Cycle 9 cached global return and precision discriminator

`StagedGlobalAssembly.compile` now binds the literal normalized source once,
collects every actual primitive-stage return and charges global placement,
padding, persistent list copying and final public reindexing. `compile_eval`
proves full operator refinement to the deterministic compiler on that same
cached chain. The legacy Hermite preparation comparison is deliberately only
its clean-input column, not whole-unitary equality across different chains.
All nonzero terminal bond sectors vanish; signed normalized Hermite amplitudes
are literal. For `N=n_p`, `D=2*k+6`, `q=ceil(log2 D)`, final gates are exactly
`N*K`, bounded by `48*N*D^3`. With `H=2^(q+1)`, `E=H*(H-1)/2`,
`G=2^q+2*(2^q-1)` and `K=E*G`, charged assembly is bounded by
`N^2*(32*K+6)+10*N*K+1`. Source production and every materialized stage are
charged additionally; `compile_total_polynomial` closes their explicit
polynomial envelope in the **declared exact-real/index-word model**.
It does not price arbitrary-precision arithmetic or physical angle synthesis.
Evidence: [global assembly](../experiments/hermite-polynomial/stored/global-assembly-result.json).

`ExperimentalNormalizationStability` proves source norm at least one from
the actual zero-grid sample and a Euclidean normalization/serialization bound
`2*F*delta + eta/(1-eta) + zeta`, for exact positive reference scale `F`
and `0<=eta<1`. The producer must still establish core/QR contraction error
`delta`, computed normalizer error `eta` and full serialized-action error
`zeta`, including ancilla/garbage embedding. Supplying these numbers is not
a numerical backend certificate. The independent dyadic witness shows that
max-core scaling can round the only surviving small branch to zero even for
a finite nonzero TT. This refutes **generic nonzero-TT totality only**;
reachability by the frozen Hermite producer is unproved. It is not a Hermite
impossibility result.
Evidence: [precision result](../experiments/hermite-polynomial/precision/normalization-stability-result.json).

Master focused source checks and production build/tests passed Lean4.33.0.
The general printed roots use the three ordinary logical axioms; finite
native regression proofs have their separately retained evaluator boundary.
Finite-bit complexity, source-reachable numerical stability, independent
full executable acceptance, source admission and C2/C3/X2/ROOT remain open.

### Cycle 10 actual dyadic return and source-reachable failure

`DyadicSupplier.compile` rounds the **actual cached global return**, preserving
physical targets, chronological instruction positions, list length and resource
bookkeeping. Constructor-level closure proves every actual returned instruction
is CX or RY with an integer-over-power-of-two rational angle. Internally proved
alignment, RY sensitivity and circuit telescoping yield full signed Euclidean
state error at most `A/2^b`, where `A=24*n_p*(2*k+6)^3`. The allocation
`b=clog2(max(1,ceil(A/epsilon)))` proves error at most positive `epsilon`.
This includes every garbage sector: approximate garbage is bounded, **not
asserted exactly zero**. The same return retains gate/depth bound
`48*n_p*(2*k+6)^3`, bond width `ceil(log2(2*k+6))` and zero oracle calls.
Its `pureAncilla=0` bookkeeping does not erase those physical bond wires.
Evidence: [dyadic supplier](../experiments/hermite-polynomial/precision/dyadic-supplier/result.json).

The numerator still uses a noncomputable exact-real floor. A finite enclosure
crossing a bin boundary need not determine that literal floor, as the compiled
`floor_boundary_discriminator` proves. This is an exact-refinement issue,
not an impossibility of safe approximate angle computation. Input representation,
computable angle enclosures, integer bit growth, preprocessing runtime,
finite-gate synthesis and saved-parser refinement remain open. Polynomial
dependence on both `n_p` and `k` does not itself provide a relation
`k(n_p,L,epsilon)` or a finite-bit polynomial route.

`ExperimentalHermiteSourcePrecision` adds exact Bernstein coefficient-error,
restriction and rounded-de-Casteljau residual propagation, linked to the literal
Hermite interpolant. Actual residual/coordinate bounds remain obligations.
The **unpatched frozen producer** fails for legal `n_p=2,k=0,L=1/10^100`:
91-digit affine coordinates near1 collapse a positive-width restriction to
`[1,1]`, before QR/normalization. Root and a distinct evidence auditor reproduced
the failure; its classification is `IMPLEMENTATION_FAILED`, not a Hermite
lower bound. Keep it as a successor-supplier regression.
Evidence: [source audit](../experiments/hermite-polynomial/precision/source-reachable/independent-audit.json),
[failure memory](../failure-memory/SP-HERMITE-POLY-002-tiny-L-coordinate-collapse.json).
Actual `n_p=2,k=0,L=1000` instead returns `[0,0,1,0]` with normalizer1 and
a finite exact-source tail-error derivation below `10^-300`; it is not all-zero
normalization failure. The human all-`k` Bernstein range derivation remains
unformalized and is not a uniform numerical backend certificate.

The new saved-QASM diagnostic separately measures exact decimal text,
binary64 reference and parsed-binary discrepancies. Missing files and
structural gate/wire mismatches fail closed; nonzero angle discrepancy is
reported, not disguised as exact identity. Two actual small saved source
circuits pass separate Qiskit replay, including signed state and garbage.
These are finite diagnostics, not the exact Lean producer, parser refinement
or symbolic family acceptance. An independently reproduced schema-type bug
has a versioned correction and regression; its rejected v1 evidence is retained.
Scientific C2/C3/X2/ROOT and production/source/reader integration remain open.

### Cycle 11 computable local suppliers without a substituted target

`SafeEnclosure.safeNumerator` computes a nearest dyadic integer from finite
rational endpoints, using rational midpoint rounding with ties toward positive
infinity. It does not evaluate a real floor or require a unique exact-floor
bin. Ordered intervals of width at most `2^-b` give absolute angle error at
most `2^-b` when they enclose the true angle. The literal list consumer rejects
invalid, missing and excess intervals; its completeness, full resource equality
and chronology theorem preserve actual constructors and ordered wires, not
merely wire footprints. `hermite_internal_supplier` composes this actual return
with the existing exact cached compiler and full signed/all-garbage error bound.
Here the formal parameter `n` means physical `n_p=n+1`.

The real-angle enclosure condition is an **unproved internal supplier edge**,
not a new public Hermite assumption. The exact input list is still noncomputable.
Output numerator and grid-denominator bit bounds are proved; endpoint denominator,
intermediate arithmetic, enclosure generation and total preprocessing runtime
are not. This removes a local exact-bin obstacle, not the finite-bit ROOT gap.
Evidence: [safe finite-data supplier](../experiments/hermite-polynomial/precision/safe-enclosure/result.json).

The separate `offset_hermite_tt` successor retains small rational offsets,
restricts reflected Bernstein coefficients, and reverses their order back to
the original increasing sample coordinate. `offset_grid_source_eval` certifies
the exact original grid expression, while interval-row and stored-dyadic
endpoint bounds provide local coefficient-error interfaces. The old supplier
and its tiny-L failure remain unchanged. The successor actually reaches scaled
normalization and RY/CX construction for `n_p=2,k=0,L=1/10^100`; fresh finite
full-state comparison measures error about `1.57e-16`, whereas its local
polynomial coefficient bound is about `1.986e-100`. These are different errors,
not a global tolerance certificate. No dense source vector enters construction.

A legal near-cutoff regression now refines a coarse pi enclosure rather than
immediately rejecting it. Insufficient retry caps and unattainable float64 local
tolerances fail honestly. No all-L totality or arbitrary-epsilon float64 claim
is made. The saved coefficient-endpoint bit statistic is not a maximum of all
intermediate operands. Pi/exp executable refinement, cutoff separation, float
subdivision/exponential errors, QR/absorption, computed normalizer and saved
circuit action remain open. The safe angle consumer and this numerical source
mutation have **not** been certified as one end-to-end pipeline.
Evidence: [actual offset successor](../experiments/hermite-polynomial/precision/offset-source/result.json).

Root fresh checks: both complete experimental Lean sources compile with ordinary
axioms at their printed roots; project-environment8 successor tests and five
witness records pass. Using an unrelated Python initially failed3 circuit imports
because Qiskit was absent; the existing project environment rerun passed without
skips or dependency installation. This was an environment failure, not a proof
or construction lower bound. C2/C3/X2/ROOT remain open.

Seal provenance is a separate debt: the offset worker amended the internal
interface inventory during proof development and did not retain its initial
snapshot. The final seal hash is not evidence that every signature preceded
proof search. Preserve the final bytes and the
[separate clarification](../experiments/hermite-polynomial/precision/offset-source/seal-clarification.json).
Do not issue a public ProofSeal from this packet. Future signature additions
need immutable versioned pre-proof packets rather than in-place inventory edits.

The distinct offset reviewer reproduced the finite witnesses and reconstructed
five coefficient injections from endpoint jets independently of the producer.
This is scoped numerical evidence, not a new rigorous scalar enclosure proof.
The reviewer also found that a zero-polynomial-injection branch bypasses the
entry's positive exact-Fraction tolerance check. No global epsilon certificate
was emitted. Preserve the frozen implementation and add uniform entry validation
with zero-injection regressions in a separately sealed successor.
See [independent audit](../experiments/hermite-polynomial/precision/offset-source/independent-audit.json)
and [cycle11 aggregate](../experiments/hermite-polynomial/precision/cycle11-staging-result.json).

### Cycle 12 exact rational budgets and stored TT error certificates

The all-`k` range node now has a compiled literal-source proof. With
`B=(k+1)^2*2^(3*k)`, source Bernstein coefficients and valid restrictions
lie in `[0,2*B]`. The actual factorial/binomial formula also has a proved
natural numerator and positive common denominator at valid indices, with
explicit power-of-two output envelopes polynomial in numeric `k` and supplied
scalar operand bits. These are output bounds, not a bound on all intermediate
integers, reduction/GCD, runtime or fixed-float conversion. Keep valid-index,
denominator and scalar-membership domains separate.
Evidence: [coefficient range audit](../experiments/hermite-polynomial/precision/coefficient-range/independent-audit.json).

`RationalBudget` computes the precision from an exact positive rational budget
using integer ceiling division and `Nat.clog`, then passes that actual result
to the unchanged finite angle-list consumer. Its same-return theorem preserves
chronology, ordered wires, resources and the conditional signed/all-garbage
error bound. Zero and negative budgets reject. True-angle containment remains
an internal supplier obligation: deliberately wrong point intervals can pass
width/arity validation but cannot satisfy `Sound`. The angle allocation spends
the entire budget on perturbing an exact list; a numerical source pipeline
must still allocate and compose its other errors.
Evidence: [rational budget audit](../experiments/hermite-polynomial/precision/rational-budget/independent-audit.json).

`QRResidual` uses the actual stored binary64 cores, the same returned QR train
and its literal mantissa/exponent normalizer. Three exact cross-Gram contractions
certify the signed residual and scale drift against the normalized **stored raw
TT**, without assuming exact QR, orthogonality or an exact accumulated scale.
Lean proves the full-word identities and a `27*n*B^3` certificate-contraction
field-operation bound. A 64-core instance used 1,081,560 such operations without
calling a dense amplitude method. This does not certify ideal Hermite source
conversion, repeated compiler QR, angles, circuit garbage, serialized action,
Python-to-Lean refinement or total bit-runtime. Certificate grid precision does
not eliminate backend error.
Evidence: [stored TT residual audit](../experiments/hermite-polynomial/precision/qr-residual/independent-audit.json).

The optional checked entry rejects invalid local coefficient budgets before
delegation, including the previously unchecked zero-injection branch. Valid
calls return the identical original object and preserve exceptions; the
frozen numerical supplier and production behavior are unchanged. Independently
reproduced tests also preserve a legal positive rational `L` for which all
64 fixed cutoff attempts from 8 through 512 terms fail. This is a fixed-cap
**implementation failure**, not a mathematical impossibility or an accepted
construction. Approximate-radius stability is the next source-linked route;
no successful generator or error certificate is inferred from this failure.
Evidence: [entry and cutoff audit](../experiments/hermite-polynomial/precision/offset-entry-v2/independent-audit.json),
[fixed-cap failure](../failure-memory/SP-HERMITE-POLY-002-fixed-cutoff-cap.json).

All three new complete Lean sources were recompiled by root and distinct scoped
reviewers with ordinary axioms at their 17, 12 and 9 printed roots. Context reuse
and upstream authorship are disclosed, not called clean-room review. Separate
immutable signature deltas are retained; the coefficient v3 delta names but
does not hash-pin its parent, while its final result binds all three files.
Earlier OffsetSource seal-history debt remains unchanged. C2/C3/X2/ROOT and
publication, reader, main-migration and deployment gates remain open.

#### Original source stability under radius approximation

`RadiusStability` proves a global bound for the actual `smoothInitial`, for
every natural `k`, including `k=0` and pairs crossing either splice. The
explicit coarse constant is
`C(k)=2^(5*k+2)*(k+1)^2*(2*k+2)*(2*k+1)`. Bernstein finite-power differences
bound the middle polynomial; exponential tail bounds and existing zero-order
endpoint jets join the pieces. No global differentiability or assumed
Lipschitz premise is introduced.

For physical `n_p=n+1`, replacing the internal radius `pi*L` by a positive
rational `Rhat` contributes at most
`2*sqrt(2^n_p)*C(k)*abs(Rhat-pi*L)` to the Euclidean normalized-state error
against the **original** target. The actual grid equality and midpoint norm
floor are reused. The square-root dimension factor is retained, not replaced
by a sup norm or constant dimension. Its logarithmic precision interpretation
adds `O(n_p+k+log(k+1))` bits, but is not a new compiled bit-runtime theorem.

Root freshly recompiled all 16 provider roots with ordinary axioms and all
six kernel consumer checks. Separate signature and consumer seals are retained.
This is a mathematical approximation interface: finite rational radius
generation, pi/exp refinement, input `L` multiplication costs, all numerical
error contributions and total runtime remain open. The fixed-cutoff failure
is unchanged, and no new source target or successful pipeline is substituted.
Evidence: [radius provider](../experiments/hermite-polynomial/precision/radius-stability/result.json).

The distinct radius reviewer independently recompiled all 16 roots and six
consumers, and added seven kernel discriminators for endpoints, Euclidean norm,
original normalization, arbitrary radii and an explicit conditional budget.
No hidden Lipschitz premise, metric substitution or target drift was found.
Reuse of upstream author/reviewer context is disclosed; this is not whole-chain
clean-room or publication review.
See [radius audit](../experiments/hermite-polynomial/precision/radius-stability/independent-audit.json)
and [cycle12 aggregate](../experiments/hermite-polynomial/precision/cycle12-staging-result.json).

#### Next saved circuit interface

The actual diagnostic compiler prunes stored-zero paths and performs another
legacy QR after the scaled return. Completion, `atan2`, Gray expansion and
decimal export then introduce further objects and interpretations; the
stored-TT residual is not a certificate for these stages. The older transport
fixtures also use a different source producer and cannot be relabelled.

The next bounded experiment should bind one actual plan, its saved gate order,
and a compact stage-action chain retaining **all** terminal bond labels. A
finite rational surrogate must have a sound trigonometric enclosure; because
it need not be unitary, its stage errors cannot simply be summed without an
amplification bound. Compare its full signed action to the literal returned
TT padded with zero ancillas, not to a freshly normalized replacement. This
is a design, with no new experiment, producer or theorem yet accepted.
Evidence: [next circuit design](../experiments/hermite-polynomial/precision/next-circuit-frontier-design.json).

### Cycle 13 finite suppliers and actual saved action

The radius approximation is now a computable Lean rational producer, not an
assumed interval around `pi`. `logRadius` uses finite Machin sums and a checked
logarithmic term allocation. It returns a positive rational with proved
membership around the original `pi*L` and error at most its requested **radius**
tolerance. The normalized consumer preserves the charge
`2*sqrt(2^n_p)*C(k)*radiusTolerance`. This tolerance is not automatically the
global state budget. Canonical input-size translation, every stored
intermediate, GCD/allocation/runtime and an external implementation refinement
remain open. [Radius supplier](../experiments/hermite-polynomial/precision/radius-supplier/result.json).

For every rational angle and natural degree, literal finite sin/cos Taylor
polynomials now enclose the exact trigonometric values with radius
`abs(q)^(degree+1)/(degree+1)!`. The bounded degree search either returns a
checked width or honestly fails at its cap. There is no magnitude hypothesis
or free transcendental evaluator. Parent replay compiled scalar, producer and
consumer sources and passed seven exact Python tests; those tests do not
prove Python, decimal parsing or outward-rounding refinement.
[Trigonometric supplier](../experiments/hermite-polynomial/precision/finite-trig/result.json).

The previously proposed saved-action experiment has been performed for the
actual OffsetSource `n_p=3,k=1,L=1` return. One compiler plan produced 456 saved
gates; the compact action chain retains all four terminal bond labels. Its
exact-rational candidate bound to the **literal**, unrenormalized stored
return is approximately `1.18153e-13`; the separate saved-Qiskit binary64
diagnostic observed approximately `2.00613e-15`. Fifteen regressions passed,
including missing artifacts and signed/order/readout discriminators. This is
one finite diagnostic, not a symbolic family certificate or ideal-source
error bound. Parser, interval/stage/readout and Python-to-Lean refinement remain
open. [Saved action](../experiments/hermite-polynomial/precision/saved-action/result-v1.json).

A separate kernel provider proves the required nonunitary-surrogate transport:
chronological product error is at most `product(1+eta_i)-1`. Its operator-action
consumer retains the input norm factor. Two scalar surrogates `11/10` already
give error `21/100`, greater than the naive summed `20/100`. The actual saved
stage interval-to-operator-norm bridge must still supply this provider's
internal local-error interface; no such condition is added to the scientific
Anchor. [Transport](../experiments/hermite-polynomial/precision/nonunitary-transport/result.json).

All four packages are contribution-branch research checkpoints, with distinct
scoped reviews pending at checkpoint time. Complete provider and consumer
compilations use ordinary foundational axioms. C2/C3/X2/ROOT, whole-module
publication, clean reader/CI and main admission remain open. Earlier frozen
packets and failures remain immutable. Checkpoints `667cc30`, `0fe774c` and
`fa5866a` were pushed and their exact remote heads verified; pushing is not
acceptance. Main remains at `305952f` with Lean 4.29.1, while these local proofs
use Lean 4.33.0. User-owned images and Robin artifacts were excluded.

The next root interfaces are a charged global rational precision allocation,
ideal source/scalar-to-stored-TT error, the actual full saved-action refinement,
and total finite-bit preprocessing/synthesis cost. New textbook slices and the
four bounded publication records retain their previous status; this cycle
does not claim whole-textbook or changed-module admission.

Distinct fresh-context reviewers subsequently accepted the three internal
proof providers and the narrow saved-action diagnostic, with independent
complete-source recompilation, exact word-Gram/readout and rebound-QASM
checks. Parent reproduced the six reviewer kernel discriminators, all five
exact-rational tests and the saved-action independent checker. Exciting a
terminal ancilla gives full error about `sqrt(2)`, rather than disappearing
under an accepted-sector projection. This is scoped internal review, not
source-blind approval of the complete Hermite construction.

Two additional small cases also show why the layers remain separate: binary64
Qiskit diagnostic errors can exceed their tiny exact-textual-decimal candidate
bounds. The latter do not bound simulator rounding; neither observation
certifies arbitrary-epsilon binary64 success. Logical matrix-cell copying
counts are not literal Python allocations, and a largest local matrix is not
total peak live memory. Full numerical-backend and bit-cost accounting remain
required. Frozen author records are retained unchanged, with these limitations
in the new independent audits.

### Cycle 14 dimension aware precision and finite exponential tails

The actual positive rational radius is now selected from the **global** state
budget. With physical width `n_p=n+1`, `N=2^n_p` and the already proved source
constant `C(k)`, the literal tolerance is `epsilon/(8*N*Cq(k))`, where `Cq`
casts exactly to `C`. Its original normalized signed-source error is proved
at most `epsilon/4`, rather than merely a radius error. This is a conservative
allocation using `sqrt(N)<=N`; its exponential-looking denominator charges
precision, not an exponential number of output samples. The actual Machin
term count has a checked threshold-size bound. Canonical input-size, all
intermediate integer/rational sizes and runtime are still open.
[Global radius allocation](../experiments/hermite-polynomial/precision/global-radius-budget/result.json).

A separate finite rational supplier now encloses literal `exp(q)` for `q<=0`
using a Taylor remainder with `(degree+1)!`. At `q<=-T`, it returns `[0,2^-T]`
without expanding powers of huge `|q|`; positive scalar-width epsilon supplies
a checked logarithmic cutoff. The clipped mass is **bounded**, not silently
discarded. Actual original Hermite left/right tails at rational coordinates,
and the middle polynomial's `exp(-1)` scalar, consume this enclosure. Active
Taylor degrees may fail the width check, and no uniform degree/runtime bound
or original irrational-grid-to-stored-TT refinement is claimed.
[Finite exponential supplier](../experiments/hermite-polynomial/precision/finite-exp/result.json).

These two immutable internal-provider packages are compiled research WIP,
with distinct review initially pending. Parent full focused replays and
`lake build` / `lake build Tests` pass under Lean 4.33.0. Scalar interval width
is not global state epsilon; the other source, QR, saved-circuit and physical
synthesis contributions remain charged and open. Scientific C2/C3/X2/ROOT,
complete-module source admission, reader/CI and main migration are unchanged.
Checkpoint `6d56dda` was pushed and its exact remote head verified. Existing
failures, user-owned files and unique branch histories remain preserved.

The concrete RY bridge now derives the signed half-angle Taylor matrix error
against `standardRyMatrix`: each entry is within delta, and its Euclidean
operator error, including an arbitrary named physical wire with unchanged
spectators, is at most `2*delta`. The proof decomposes the literal error into
cosine error times identity and sine error times `RY(pi)`. It does not assume
the surrogate is unitary. Kernel fixtures discriminate signs, half angles,
q0/q1/q2, spectator preservation and reused exact CX basis action; the actual
first saved decimal token also has a theorem instance.
[RY bridge](../experiments/hermite-polynomial/precision/saved-ry-interval/result-v2.json).

This supplier's exact Taylor midpoint is **not** identified with the existing
saved-action producer's outward-rounded completed stage midpoint. Stage
chronology, rounding, text decoding, full terminal readout and nonunitary
amplification still need a complete bridge. Initial unpublished path-bearing
metadata was quarantined unchanged; the safe successor has relative commands
and sanitized logs. No private output, Source Anchor approval or ROOT success
is promoted by that recovery.

The distinct fresh-context reviewer subsequently accepted all three scoped
internal packages, rebuilding the analytic suppliers and dependencies from
complete source and checking the RY source/consumer in a separate cache.
Parent repeated both reviewer kernel probe files and all five independent
exact blind-spot tests. A reviewer-only elaboration failure is explicitly
retained as a failed composite, followed by successful corrected probes; it
is not relabelled as a green run. These reviews do not approve the complete
scientific construction, source-blind publication or main admission.
[Cycle 14 evidence](../experiments/hermite-polynomial/precision/cycle14-staging-result.json).

The next scalar proposal uses a factorial-block estimate to obtain a
polynomial sufficient active Taylor degree. It remains **design only**;
neither completeness nor a finite-bit runtime bound is credited before Lean
proof and actual consumers. Radius has spent `epsilon/4`; a provisional
`3*epsilon/16` reserve for each other stage is accounting design, not four
closed bounds. Actual stage midpoint, source/storage and physical synthesis
are still separate obligations.

### Uniform degree and literal rounded rows

The degree-allocation design above is now proved for the existing finite
negative-exponential checker: `checked_complete` and `complete_enclosure`
provide sound bounds for every legal rational input and positive tolerance.
The sufficient active degree is `4*T^2+2*T+1`; the all-k original tail and
endpoint consumers compile. Scalar width does not discharge vector or
normalized-state error, coefficient amplification or intermediate bit cost.
[Degree provider](../experiments/hermite-polynomial/precision/finite-exp-degree/independent-audit.json).

`HermiteSavedRounding` proves signed integer floor/ceil formulas, outward
enclosure, four-corner products, literal signed-half-angle RY row updates,
same-pair chronological enclosure and end-only midpoint error. The distinct
review and independent sign/order/center discriminators pass. A failed
reviewer fixture is retained as an implementation failure, not erased.
[Rounding provider](../experiments/hermite-polynomial/precision/saved-rounding/independent-audit.json).

The stored Gram whole-module review closes one publication obligation without
changing production source. All five registered packets validate against the
current complete source context; 46 of the 51 changed modules still lack
packets, so the aggregate admission gate fails closed. Parent legacy-shell
stdin encoding failed; the unchanged replay passed under UTF-8 PowerShell 7.
Scientific C2/C3/X2/ROOT, full executable family acceptance, finite-bit
resources, main migration and reader purification remain open.
[Aggregate](../experiments/hermite-polynomial/precision/cycle15-staging-result.json).

### Literal middle source and complete real-stage enclosure

The all-k rational middle evaluator now has a proved error against the
unchanged original source: `delta/2 * (k+1)^2 * 2^(2*k)` on `[-1,0]`,
with exact central value 1. Its distinct whole-source review passes.
This is a scalar bound, not an allocated normalized-state epsilon or a
finite-bit preprocessing theorem. The original tails, rational-radius grid,
stored cores and dimension-aware normalization still need composition.

Changing-target RY/CX words now have a literal full-matrix interval interpreter
and a produced real Euclidean operator error bound
`eta = 2^width * maximum entry halfwidth`. RY is rounded outward at every step;
CX permutes physical rows; midpoint extraction occurs only after the stage.
Distinct review and parent corrected kernel/finite discriminators pass.
The nominal exact-stage contraction and actual nonunitary product transport,
complex primitive adapter, parser and complete garbage/readout are still open.
The midpoint surrogate is not assumed unitary or contractive.

Full matrix expansion has `4^width` entries; these symbolic semantic theorems
do not make that expansion efficient. Local-support lifting or explicitly
charged dense work is required before a polynomial-resource claim. All
intermediate bit/GCD/storage/runtime and physical synthesis costs remain open.

The unchanged MatrixProductChain module has completed its 13-declaration
source-blind and separate source-first review. Six local publication records
validate, but 45 of the 51 changed modules still lack records, so the whole
admission gate rejects. Main migration, clean reader/CI, C2/C3/X2/ROOT and
full executable family acceptance are not promoted.
[Cycle 16 evidence](../experiments/hermite-polynomial/precision/cycle16-staging-result.json).

### Cycle 17 local source budget and actual nominal transport

The frozen finite rational piecewise evaluator now has a locally compiled
normalized Euclidean error at most `epsilon/2` against the unchanged original
signed `pi*L` target, for every k,n and positive rational L,epsilon with
physical width `n_p=n+1`. Its source `epsilon/4`, produced-radius
`epsilon/4`, dimension aggregation and central-value norm floors are proved
internally. The amplitude consumer gives squared error at most `epsilon^2/4`.
This is a source-only approximation certificate: exact mathematical
normalization is not a finite-bit circuit producer. Distinct review is pending.

The actual real-stage construction now locally proves whole-carrier nominal
RY/CX norm preservation, internally supplies every `Valid` conjunct and
identifies chronological nominal products with the literal flattened word.
The actual surrogate action is bounded by `(product(1+eta)-1)*norm(x)`.
Neither surrogate unitarity nor contraction is assumed. This does not yet
identify the custom real word with the existing complex primitive evaluator;
that canonical little-endian adapter is a separate sealed worker objective.
[Frozen checkpoint](../experiments/hermite-polynomial/precision/cycle17-author-checkpoint.json).

The next stored-source obligation must use this precision-dependent source,
not the old exact-exponential rank. Active tails have degree
`d=4*T^2+2*T+1`, clipped tails retain the nonzero midpoint `2^(-T-1)`, and
the +/-T masks interact with the -1/0 splice even when T is0 or1. A five-term
masked-polynomial construction is proposed, but its comparator contraction,
actual rational core producer, rank/storage and same-run generation costs are
not yet proved. The proposed bond envelope is not a certificate.
[Design only](../experiments/hermite-polynomial/precision/piecewise-tt-next-design-c17.json).

The generic interval matrix needs `4^width` entries if materialized. The
existing saved-action producer instead uses local stage width `a+1`; its
physical local-to-global lifting and a certified bound on a must be proved
before either efficient execution or exponential execution is inferred.
All bit/GCD/QR/storage/normalizer/synthesis costs, full terminal readout,
independent scientific-family acceptance and C2/C3/X2/ROOT remain open.
No main merge or deployment follows from these local checkpoints.

### Cycle 18 scoped review successor and canonical complex-evaluator bridge

The cycle17 distinct internal review is now complete. It accepts only the
original signed-grid normalized source `epsilon/2` bound and the actual real
nominal isometry/produced-`Valid`/chronological product transport. Its fresh
17+9 selected-source builds, 162 ordinary-axiom roots, retained failures and
finite local-carrier discriminator are bound by
[the final review](../experiments/hermite-polynomial/precision/source-stage-review-c17/independent-audit.json).
The earlier mathematical audit remains explicitly pending as historical
evidence; the final success is a separate frozen successor. This is internal
provider review, not public SourceAnchor admission or a source-blind decoder.

The locally proved complex adapter now identifies the literal real full word
with `QuantumBlockEncoding.evalPrimitiveCircuit` under the already existing
canonical little-endian basis equivalence. It proves the arbitrary real
matrix-input version and consumes the equality on arbitrary complex vectors,
entry enclosures and chronology. It does not assume basis agreement, drop
spectators, identify states modulo phase, discard garbage or redefine the
primitive semantics. Its distinct source/semantic review is still pending.
[Local exact bridge](../experiments/hermite-polynomial/precision/literal-complex-adapter/result-v1.json).

[The parent focused checkpoint](../experiments/hermite-polynomial/precision/cycle18-parent-checkpoint.json)
rehashes actual inputs/private caches and checks the actual consumers. It is
not an all-transitive rebuild or scientific-family executable acceptance.
The operator-norm eta transport to the complex carrier and physical local
stage-to-global tensor support are still separate obligations. This matrix
equality alone does not finish end-to-end epsilon allocation or state readout.

StoredMatrixProductChain's whole 29-declaration correspondence is admitted as
the seventh local publication packet, with source-first gaps preserved.
The complete production gate still rejects 44 unreviewed changed modules out
of 51. Main remains on Lean4.29.1; this contribution uses Lean4.33.0. No ROOT,
finite-bit efficiency, resource winner or deployed new proof claim follows.
The immediate construction supplier is actual precision-aware nondense
piecewise cores with the same returned stored chain and charged generation,
including T=0/1 threshold coincidences and the nonzero clipped tails.

The current contribution also passes `lake build` and `lake build Tests` under
Lean4.33.0. All 245 parent-checkpoint source/private-cache bindings still match
after these incremental builds; the 67 atlas/site regressions pass. This is
not clean CI, an independent all-transitive rebuild, main migration or the
full reader/publication gate. Existing local Verso compatibility changes are
disclosed rather than treated as a clean environment.
[Cycle 18 synthesis](../experiments/hermite-polynomial/precision/cycle18-staging-result.json).

### Cycle 19 frozen internal checkpoint; publication is still fail-closed

The distinct review of the literal real-to-complex adapter accepts the exact
full-carrier bridge, including signed half-angles, all spectators, arbitrary
real matrix inputs and consumption on arbitrary complex vectors. Its accepted
scope is an internal provider, not a public source-blind publication record.
[Independent review](../experiments/hermite-polynomial/precision/literal-complex-review-c18/review-verdict-v1.json).

The precision-aware rational source has an unconditional five-component
identity on every rational point and the actual rational grid. A concrete
formula-derived Python producer retains all splice/cut ownership, nonzero
clipped tails and the same returned stored chain. Its finite exact diagnostics
pass, but arbitrary-width generated-core contraction, same-object Lean
refinement and uniform generation/finite-bit cost are not yet certified.
[Frozen producer scope](../experiments/hermite-polynomial/precision/piecewise-kernel-producer/result.json).

The parent independently reruns 44 declaration/axiom reports and thirteen
finite tests, requires the saved chain to exist and rejects skipped tests.
All bound inputs/private caches remain unchanged. The first parent validator
misclassified printed universe suffixes and missed an axiom-free declaration;
its failed record is preserved, and a separately versioned replay passes.
[Parent replay](../experiments/hermite-polynomial/precision/cycle19-parent-checkpoint-v2.json).
These are focused checks with pinned inherited caches, not clean transitive CI.

StoredTensorTrain's whole actual source and source-blind independent consumers
elaborate successfully, but the distinct source-first reviewer found an
exact-signature extraction collision: the decoder artifact's `absorption`
signature records `absorptionEntry`. The successful execution does not repair
that artifact discrepancy. Preserve both records and require a versioned
correction plus distinct review before admission. The module remains pending;
seven existing records and the 44-of-51 production admission debt are unchanged.

The website priority is separately delivered by PR90, merged at
`e71ed7555d03efc808978f9f52f34ac9a9b54589`: four peer textbook parts and
reader-facing curriculum/navigation are live. Published main remains on
Lean4.29.1; these proof checkpoints use Lean4.33.0. Neither reader deployment
nor these focused tests closes the scientific ROOT, finite-bit resource tuple,
independent family executable acceptance, publication purification or migration.

### Cycle 20 actual uniform masks and complex precision transport

The generated comparison supplier now proves the arbitrary-width q0-LSB scan,
actual one-hot matrix contraction, strict/inclusive rational-grid thresholds,
and the finite Window of its generated tables. The SAME returned stored chain
contracts to its intended mask; it has maximum bond at most3 and at most
`18*width` stored scalars. Its charged extended exact-real operation count is
at most `5*n^2+149*n+479` for width `n+1`, with `18*width` quotient calls and
`18*width` remainder calls counted separately. This is not a finite-bit runtime
or the cost/rank of the complete Hermite piecewise producer. All cut0/N and
T0/T1 ownership is handled symbolically, not by testing selected grids.
The rational binomial translation supplier gives arbitrary-width polynomial
contraction; actual Hermite coefficient generation and five-way mask/product
assembly are still required.
[Uniform supplier and precise omissions](../experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/result.json).
[Parent replay:21 reports](../experiments/hermite-polynomial/precision/cycle20-uniform-parent-checkpoint.json).

The actual saved interval center and `stageEta` now supply an induced-operator
bound on the complete existing complex Euclidean carrier. Nominal contraction
and `Valid` are proved internally; chronological products equal the actual
flattened primitive evaluator. The apply bound holds for arbitrary complex
vectors, not only real inputs, first columns or clean sectors. No phase quotient
or terminal garbage projection is introduced. A distinct review is pending.
[Actual complex transport](../experiments/hermite-polynomial/precision/complex-stage-transport-c20/result-v1.json).
[Parent replay:16 reports and7 diagnostics](../experiments/hermite-polynomial/precision/cycle20-complex-parent-checkpoint.json).

The versioned StoredTensorTrain decoder v4 corrects the exact-name extraction
collision and preserves v3 byte-identically. Parent checking matches all30
signatures/axiom reports to the actual successful execution messages. It also
explicitly records that the prior provider scanner missed combined
`public meta import`: those pinned providers were a partial inherited closure,
not an exhaustive rebuild. Distinct source review and admission remain open.
[Correction provenance](../reviews/publication/stored-tensor-train/decoder-provenance-c19-v4.json).

The current local repository build and Tests pass under Lean4.33.0, using
inherited caches and disclosed local Verso edits. Sealed author inputs remain
unchanged. This internal WIP checkpoint is not clean CI, reader/publication
admission, a new scientific winner or main migration.
[Actual integration gate](../experiments/hermite-polynomial/precision/cycle20-integration-gate.json).

### Cycle 21 distinct actual-complex-stage review

A reviewer distinct from the C20 author reconstructed the full complex carrier,
actual saved midpoint/radius, signed half-angle and later-left product convention
before inspecting the new proofs. Its independent symbolic checks preserve
arbitrary complex inputs and show that the actual error entries have zero
imaginary part. The scoped verdict is internal acceptance, with no supplied
`Valid`, contraction or error-bound premise at the actual-stage roots.
[Frozen independent review](../experiments/hermite-polynomial/precision/complex-stage-review-c21/review-result-v1.json).

Parent replay passes all18 ordinary-axiom reports and35 independently authored
finite discriminators, without writing the frozen review receipts or caches.
All bound inputs and selected private outputs remain unchanged.
[Parent replay](../experiments/hermite-polynomial/precision/cycle21-review-parent-checkpoint.json).
The16 selected modules were freshly checked in the reviewer packet;3404
inherited caches still have explicitly unknown source correspondence. This is
not a clean full transitive rebuild or a public source-blind publication.
Uniform whole-family error allocation, physical local/global support, the
complete stored piecewise producer, actual QR/finite-bit runtime, finite-gate
synthesis, independent family executable acceptance and ROOT remain open.
The existing website release is main PR90; main Lean4.33 migration and the
51-module publication debt are separate, still-unfinished gates.

### Cycle 21 actual five-component source chain and eighth module review

The actual rational middle coefficients are now produced by explicit finite
binomial/factorial sums and proved equal to the original `coefficientQ` and
`middleValueQ`. Two actual three-state masks per component, actual polynomial
translation and five diagonal blocks form ONE explicit chain. Its contraction
equals the actual `piecewiseValue` on the actual q0-LSB `rationalGrid` for every
word. The allocated consumer obtains radius positivity from the real supplier;
no desired mask, coefficient, Window, rank or approximation is a root premise.
The SAME chain has bond at most `18*(d+1)+9*(m+1)+18`, with actual
`d=sourceDegree(delta)=4*T^2+2*T+1` and `m=2*k+1`, and scalar-address envelope
`2*(n+1)*D^2`. This envelope is NOT a stored-data producer or runtime bound.
[Full actual algebraic supplier](../experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/result.json).
[Parent replay:13 reports](../experiments/hermite-polynomial/precision/cycle21-assembly-parent-checkpoint.json).

All19 fresh supplier calls and the parent's four actual-source replay calls
pass. The separate outer launcher exit1 remains ENV_BLOCKED in its original
receipt; it is not reported as process success. Historical source-name shadowing
and stale initial attempt bindings remain visible, with final accepted source
and ordered cache selection explicitly pinned. Distinct source review is pending.
The next blocking interface is actual rational table/boundary production,
unconditional Window for these tables, SAME returned stored-chain refinement,
and charged coefficient/cut/product/directsum/materialization/copy/assembly
costs. Finite-bit/GCD/QR/normalization/error composition/physical export/ROOT
remain separate obligations.

StoredTensorTrain now has a distinct whole-module source-blind decoder and
source-first reviewer, all30 exact types/ordinary axioms and complete-terminal
consumers, a parent fresh whole-source replay, and passing local Lean4.33
build/Tests. The corrected v4 decoder extraction preserves the failed original;
metadata-only wrappers are independently compared and do not invent new runs.
[Independent review](../reviews/publication/stored-tensor-train/source-review-c20/reviewer-admission-evidence-v1.json).
[Parent gate](../reviews/publication/stored-tensor-train/parent-admission-check-v1.json).
Its scoped registry admission raises the reviewed total to8, leaving43 of51
changed production modules. This retrospective stored exact-real contract does
not admit its whole providers, establish source/cache equivalence or supply
finite-bit runtime/scientific ROOT. Main4.33 and PURIFIED reader gates remain open.

### Cycle 22 actual stored full-source producer, partial cost boundary

`produceQData` now creates the actual rational five-component block once and
materializes only `(n+1)` local `D`-by-`2D` tables and two `D` boundary vectors.
It does not enumerate the amplitude vector. Literal casts identify their entries
with C21's real full source. Their generated Window is proved internally, and
`produceStored` feeds these same stored tables and boundaries to canonical
`StoredMatrixProductChain.ofTable`. The returned chain equals `actualChain`,
including the signed q0-LSB source action, strict/inclusive splice ownership,
cut0/N and T0/T1 cases. No desired Window/refinement/coefficient/rank premise
is introduced. The allocated consumer derives positive radius internally.
[Frozen producer](../experiments/hermite-polynomial/precision/piecewise-kernel-stored-c22/result.json).

The SAME returned value has bond at most
`D=18*(sourceDegree(delta)+1)+9*(2*k+2)+18` and address envelope
`2*(n+1)*D^2`. With `A=(n+1)*(2*D^2+D+1)+2*D`, rational materialization and
explicit real casting/copies charge `9*A` traffic operations; canonical assembly
gives the partial upper ledger `9*A+20*D^2+30*D+5*n^2+7*n+31`.
**This is not total producer runtime.** Literal scalar formula evaluation
currently occurs inside `pure`, an unaccounted boundary, not a free operation.
Cut/degree/preprocessing, coefficient cache generation, powers, binomial and
factorial operations, index quotient/remainder, rational bitlength/GCD and
representation costs must still be produced and charged. Inspection of
Mathlib compiler replacements is not their cost certificate.

The parent re-elaborates all four actual C22 sources without emitting or
overwriting caches: fourteen ordinary-axiom reports pass, and 215 bound inputs
are checked unchanged before and after. Explicit C22/C21/C19/C20 import order
retains inherited caches; this is not a clean transitive rebuild.
[Parent focused replay](../experiments/hermite-polynomial/precision/piecewise-kernel-stored-c22/parent-verification-v1.json).
The checkpoint is pushed as `91da307279b96fc4124bf80aafda1679ac8a769b`.
Independent internal semantic review is running separately; public source-blind
admission, full classical/finite-bit cost, normalization/error composition,
physical circuit/synthesis/export, independent family acceptance and ROOT remain
open. The next shared scalar prerequisite is an actual charged coefficient cache,
not an assumed cost for an arbitrary entry callback.

Latest reader main `740c3a4080e2866c78024c9ed42e908d50089f1b` is reconciled into
the proof contribution at `d78c167db67b4f36d913a0de91b38322592e23c7` with no
production Lean changes. All eight review bindings remain valid, 95 reader
regressions pass, and incremental local Lean4.33 build/Tests pass with inherited
caches and existing Verso compatibility edits disclosed. The full production
publication gate still fails closed on 43 of 51 changed modules. Main remains
Lean4.29.1; reader delivery and contribution pushes do not close migration.

The distinct C22 internal reviewer has now accepted literal rational/real
casting, complete signed q0-LSB source, splice ownership and same-returned
object linkage. Its independent consumer also proves generation charges zero
field/comparison operations: this supports the explicit partial-cost boundary,
not a complete runtime claim. T0/T1, 0/N cuts and signed-coefficient native
examples are finite screenings only. Its initial stuck `decide` test and wrong
finite coefficient expectation remain retained with the exact failed source.
[Independent review](../reviews/internal/c22-stored-supplier-review/review.md).
The parent's fresh independent-consumer elaboration passes seven named ordinary
axiom reports; all70 bound inputs/review artifacts remain unchanged.
[Parent review replay](../reviews/internal/c22-stored-supplier-review/parent-replay-v1.json).
This closes internal self-review debt for this provider only; it is not a
source-blind public admission, full transitive build, normalized-state or ROOT
certificate. No production-module publication record is added.

### Cycle 23 actual charged rational source-coefficient cache

The existing factorial/choose/source mechanism now has a computable rational
refinement returning one `Run (Vector Rat (k+1))`. Every returned entry equals
C21's `sourceCoefficientQ`, hence its actual `coefficientQ` on the full index
range. An additional bridge identifies the rational-to-real cast with the
actual existing real `sources` return supplied by its actual factorial table.
The same returned run has cost at most `52*(k+1)^2` per ordinary operation
category and `416*(k+1)^2` in total. No desired-value, desired-cost or arbitrary
coefficient-oracle premise is added to the final roots.
[Frozen bounded result](../experiments/hermite-polynomial/precision/charged-coefficient-cache-c23/result.json).

The parent re-elaborates the two actual C23 sources without changing any frozen
cache: ten symbolic axiom reports use only ordinary logical axioms; 866 bound
source, artifact and cache inputs stay unchanged before and after. The selected
fresh-v3 project providers are checked explicitly. Mathlib and the remaining
C19/C20/C21 imports are inherited and pinned, not a clean transitive rebuild.
Earlier launcher, elaboration and namespace-root selection failures remain
retained as implementation/environment evidence, never mathematical refutation.
[Parent replay](../experiments/hermite-polynomial/precision/charged-coefficient-cache-c23/parent-verification-v1.json).
Local Lean4.33 library and Tests builds also pass using inherited build artifacts
and the existing local Verso compatibility edits; no clean CI claim is made.

This closes only the charged source-coefficient producer prerequisite. C22 does
not yet consume this cache. Middle coefficients, exponential/cut/index setup,
remaining local table/boundary arithmetic and consumption traffic, rational
bitlength/GCD, finite-bit stability, normalization/error composition, circuit
synthesis, family executable acceptance and the scientific ROOT remain open.
The exact rational scalar/word counter model excludes natural-index arithmetic,
loop/counter metadata and allocator implementation. Independent internal review
is in progress; public source admission, main4.33 migration and PURIFIED reader
gates remain pending. The frozen scientific contract and exponential baseline
are unchanged.

### Cycle 24: frozen C23 internal review replay, 15 October 2026

The distinct internal review accepts the bounded same-object coefficient-cache
contract, including charged lookup, denominator positivity, exact per-term
cost and two counterexamples excluding invalid helper/full-carrier readings.
The parent freshly re-elaborated its independent consumer under Lean 4.33.0:
all 22 axiom reports use only ordinary logical axioms and all 1,616 bound inputs
remain unchanged. Providers are the frozen reviewed outputs, explicitly inherited;
this is not a clean transitive build or source-blind publication admission.
[Review](../reviews/internal/c23-charged-cache-review/review.md) and
[parent replay](../reviews/internal/c23-charged-cache-review/parent-replay-c24-v1.json).

Current main was safely reconciled without changing any production source or
the 16 protected local files. The contribution's incremental Lean 4.33 library
and Tests gates both pass; 89 reader/research regressions pass. All eight
existing publication bindings still validate. The full publication gate remains
closed on 43 changed modules (2,094 inventoried public declarations), and main
still uses 4.29.1. Exact compatibility-delta minimization is a controlled
experiment: changing even one ambient source invalidates existing global
bindings and requires a new evidence scope. No verifier or publication rule is
relaxed. C22 consumption, total preprocessing, finite-bit and scientific ROOT
obligations above remain open.


### Cycle 24: ConstructiveTensorTrain independent publication checkpoint

The distinct c24 source-blind decoder and source-first reviewer agree on the
whole 15-root module, the exact retrospective lesson and repaired v2 graph.
The later wrapper attestation checks the exact three parent metadata transports;
it does not manufacture a historical pre-proof seal or a new proof execution.
See [independent review](../reviews/publication/constructive-tensor-train/reviewer-c24/review.md)
and [portable integrity replay](../reviews/publication/constructive-tensor-train/verify-c24.py).
The previous c23 changes-required record and graph failure remain retained.

Nine current publication records now validate mechanically on this contribution.
The full changed-module gate remains blocked on the other 42 modules. This is
SOURCE_REVIEWED_LOCAL_INTEGRATION_PENDING, not main admission or PURIFIED.
The decoder freshly compiled the actual target and checked 15 signatures/axiom
reports against an explicitly fresh target; imported providers were inherited.
Maximum algebraic bond bounds and exact complete-terminal action/mass are not
physical qubit, cleanup, precision or total gate-cost certificates. No scientific
target, scoring, winner, Hermite ROOT or exponential baseline is changed.


### Cycle 24: fixed-source HermiteCutRank staging, 16 October 2026

The whole existing 20-root exact-real cut-factorization module now has a fresh
actual-source Lean 4.33 compile and fresh-target signature/axiom probe from a
distinct formal-only decoder. The separate source-first review matches the
20 mathematical roots but correctly rejects earlier graph/coverage versions.
Versioned repairs retain all 42 source blocks/formulas and explicit F/G witness
premises, actual imports/ownership, and open scientific-grid/normalization,
physical/cleanup and uniform-precision/total-resource SOURCE_GAP nodes.
See [staging packet](../reviews/publication/hermite-cut-rank/).
Independent successor topology/decoder comparison and canonical admission are
pending; nine current publication records still validate and 42 modules remain
unadmitted. This does not close a new scientific leaf or the Hermite ROOT.

The compatibility experiment ended PARTIAL_ENV_RESOURCE after three import-read
failures; those files exist and are nonempty, and exact OS cause is not isolated.
It is neither compatibility nor mathematical refutation and is not the release
route. Frozen target, source baseline and all scientific obligations are unchanged.


### Cycle 24: HermiteCutRank exact-source review registered, 16 October 2026

The distinct source-first reviewer now accepts the frozen new decoder comparison
for all20 public roots and seven semantic slots. The final graph retains the
actual F/G separation premises, three literal imports and declaration ownership,
all42 source blocks including eight previously omitted formulas, and three stable
OPEN/SOURCE_GAP consumer nodes. Historical rejected metadata versions are retained.
The exact original review, fresh-target20-signature/axiom evidence and the later
independently attested schema transport are now linked in the canonical registry.
Ten current records validate mechanically;41 of51 changed production modules
still lack admission records. See
[independent review](../reviews/publication/hermite-cut-rank/reviewer-c24/review.md).

Status remains SOURCE_REVIEWED_LOCAL_INTEGRATION_PENDING, not main, reader,
PURIFIED or scientific ROOT acceptance. This retrospective exact-real cut-rank
explanation certifies no new physical/finite-bit/resource algorithm and supplies
no complete poly(n_p) state-preparation route. No target, scoring, champion,
production source, original frozen artifact or historical failure was modified.

### Cycle 25-27: migration and review frontier, 17 October 2026

The Canonical/Norm pair has genuine distinct decoder and source-first reviewer
acceptance for its bounded whole-module contracts. Twelve current publication
records validate; the aggregate gate still correctly fails on 39 of 51 changed
production modules. See the
[paired independent review](../reviews/publication/finite-real-tensor-train/reviewer-c25/final-review.md).
The contribution uses Lean 4.33.0, while fetched main remains Lean 4.29.1 at
`f2cba045611a0d11c5995c29607569726bf1d6c5`. PR #86 is still a draft, not a
completed migration. Its current contracts check fails at changed-module
publication evidence, not at authored-contract or process-memory validation.

The unchanged-content-bound standard
[Lean gate](../reports/lean-433-migration/c25-cf77-lean-gate.json) records
`lake build`, `lake build Tests`, and all 202 discovered module targets passing
under Lean 4.33.0. These are incremental builds with inherited provider artifacts,
not a clean transitive rebuild, independent semantic acceptance, or a new
scientific resource certificate.

The next three-module physical TT packet has three fresh target compiles and
37 successful signature/ordinary-axiom probes from its original independent
decoder. Its source, author metadata and native decoder evidence are preserved
in the [WIP packet](../reviews/publication/finite-real-tt-physical/). The previous
reviewer left source-only and static-comparison work, but no final joint seal was
found after the worker became unavailable. That work is retained, not relabelled
as accepted. A new distinct source-first reviewer is checking this packet before
canonical admission; its result must not be attributed to the old run.

The following five-module Hermite substrate batch is under separate source
curation and formal-only decoding. Neither batch changes the frozen scientific
target. C23's computable rational coefficient-cache result remains a bounded
arithmetic-model supplier, not complete preprocessing or finite-bit synthesis.
C22 consumption, full source-to-stored-chain production, precision/stability,
physical synthesis and independent family executable acceptance remain open.
There is no newly closed Hermite ROOT and no mathematical-impossibility claim.

The next five-module substrate now has a frozen formal-only reconstruction,
five fresh actual-source Lean 4.33 compilations and successful final type/axiom
outputs for all 71 public plus four private named roots. Parent integrity checks
match the current whole-module inventory and 57 inherited source/olean pairs;
seven staging tests pass. See the [WIP transport](../reviews/publication/hermite-substrate-c27/parent-wip-transport.json).
This is not clean-transitive evidence or source-equivalence acceptance. A distinct
source-first reader has frozen its independent S1-S14 mathematical reconstruction;
actual formal/author-metadata comparison remains pending.

All 14 proof/probe calls include three failed diagnostic assemblies, with total
wall time 318.701 seconds and failed-call time 59.432 seconds. These are not failed
production theorems or mathematical obstructions. The first failed partial stdout
was reused by the original decoder; its surviving error/tool evidence and this
limitation are disclosed, not described as a complete retained raw failure log.
The local child geometry still costs 70 selected counters plus four separately
counted natural additions. Local kernel-table assembly consumes two already
stored records satisfying seven source clauses each; it is not their producer.
Source-data production, finite-bit error/synthesis, scientific ROOT, main and
reader/purification gates remain open.

### Cycle 26: physical tensor-train whole-module review registered

The actual new source-first reviewer has accepted the final source/formal/
original-decoder comparison for the entire LocalCompiler, Word and Primitive-
Preparation cohort (10/12/15 public roots). The original decoder and the new
reviewer each authored their own native evidence. The new review preserves its
source-only -> joint static -> separately delivered decoder/compilation order;
the unavailable old reviewer's missing final seal was not fabricated.
See the [final independent review](../reviews/publication/finite-real-tt-physical/reviewer-c26r/final-review.md).

All 15 actual canonical records now validate against the unchanged checker and
current ambient sources. The aggregate gate still fails closed on 36 of 51
changed production modules. Fourteen c26 packet tests, seven c27 staging tests
and 46 publication/atlas/raw-Git-transport regressions pass, including missing
actual decoder/reviewer/output rejection. The proof-input digest remains
`5a8f47f8d0afd1d4f957e55babde52a9e9c01babf05c481b988e99ebca2f7758`.

This is SOURCE_REVIEWED_LOCAL_INTEGRATION_PENDING. Exact-real finite instruction
lists, full signed state action and scalar-terminal cleanup do not supply the
missing deterministic preprocessing, finite-bit synthesis/error or scientific
family certificate. Main remains 4.29.1; no main/reader/PURIFIED or Hermite ROOT
closure is inferred. The frozen author recipe's eleven-versus-twelve selected-
field wording discrepancy is explicitly retained as nonblocking prose debt;
neither the checker nor any original frozen evidence was edited to conceal it.


### Current integration and next scientific interfaces, 18 October 2026

Earlier cycle counts above are historical snapshots, not the current registry.
At contribution `67b750fcf30ac988df0a66d7af8f27e51a0fb74d`, all50 existing
whole-module source-correspondence records validate against the unchanged
checker; the changed-module gate still fails on experimental RobinMatrix.
Main remains `af585d9cbbb299c1c8c48647627a2cb820ef536a`/Lean4.29.1, versus
Lean4.33.0 on the contribution. No maintenance-policy exception is approved or
implemented. Historical full Lean/Tests evidence and its limited input
association are not a fresh clean-transitive build. Current CI outcomes remain
separate from the successful pinned historical Python35 replay.
[Evidence](../reports/lean-433-migration/c135-local-operation-proof-and-real-replays.json).

The Hermite C2/C3/X2/ROOT boundary is unchanged. The accepted internal C23
same-object cache and charged lookup have not yet been wired into C22.
C145 is inspecting precisely that consumption edge, preserving actual C21
source coefficients, middle boundaries and the SAME returned stored chain.
Setup, tails, kernels, arithmetic/traffic, bitlength/GCD and numerical/physical
costs are not erased by a cached lookup.

C147 has a pre-proof internal parameter contract for the actual precision
source: with physical `n_p=n+1`, bound its Taylor degree by `4*M^2+2*M+1`,
where `M=n_p+2*k+tailCutoff(epsilon/(4*(k+1)^2))`. This is a new proof
obligation, not a proved theorem at this snapshot. It must use the existing
literal cutoff and source allocation, cover all natural k,n and positive
rational epsilon, and cannot inherit the exact-real `2*k+6` bond. Even if
closed, it will not certify coefficient bitlengths, QR, finite-bit gates,
normalization/export or the scientific ROOT.

The independently reviewed ideal CCX cleanup bridge is separately staged in
the Uncompute experiment; it is not a replacement Hermite construction or a
claimed improvement to this task's resource tuple. Methods may run
asynchronously under one frozen contract, with matched endpoint and total-work
accounting. Seven recorded wrapper observations include all three failed
whole-proof calls; their sum is not a controlled SP/BE efficiency result.
[Read-only cost observation](../experiments/uncompute-2610-22367/operation-bridge-c134/retrospective-cost-observation.json).


### Subsequent local parameter proof and current full gate

The C147 allocated Taylor-index root subsequently compiled under Lean4.33.0
(31.844s), with its exact own-output definition/type/axiom audit passing
(23.328s). All4 new roots report only the ordinary3 axioms. This is
proved_locally, not the complete finite-bit resource/root certificate.
[Exact scope and evidence](../experiments/hermite-polynomial/precision/allocated-degree-budget-c147/README.md).

The PR merge snapshot b95220ce6ebe9b6b7a965b4437f43b26fb673c03 also completed
full library/Tests and original Hermite executable replay successfully; its
selected proof/replay Git inputs equal contribution67b750f. This is a real
current PR integration gate, not main merge, clean TCB, new finite-bit poly-SP
executable acceptance or resolution of the experimental publication conflict.
[Source association](../reports/lean-433-migration/c153-current-PRmerge-full-gate-association.json).


### Independent scalar review and actual cached-supplier type probe

The C147 arithmetic provider now has a separately frozen C151 independent
source-first mathematical/binder/definition review and C154 subsequent actual
runtime association review. Both support their bounded internal claims, with
inherited/dirty/transitive provenance limitations retained; neither grants
source-publication, clean-TCB or scientific ROOT credit.

C150 actual cache -> signed middle -> five-branch right table -> existing
stored-chain definitions typechecked in C155: three modules plus seventeen
candidate propositions, all exit0. Type formation is not a proof. C156 seals
their exact bodies/signatures before subsequent bounded proof search. The
400/816 proposed bounds and final cached same-run refinement remain OPEN.
Subsequently C159 actually compiled seven C157 primitive/right roots, including
rightEntry partial counter<=11, and a fresh-own-output exact-type/axiom consumer
(25.578s/24.531s), all seven ordinary-three axioms. This is proved_locally with
independent static review pending, not full producer/runtime/root acceptance.
[Exact compiled primitives](../experiments/hermite-polynomial/precision/cached-primitives-c157/README.md).
Kernel/left and captured-block setup/native/bit/GCD costs remain unaccounted.
[Exact original stages](../reviews/publication/migration-checkpoints-c158/README.md).

The asynchronous policy retains human choice for material unapproved trade-offs,
autonomous bounded same-contract work, typed immutable evidence, matched
acceptance endpoints and all observed failed/cancelled/stale cost. No measured
quantum proof-first/screen-first/dual-lane efficiency winner or production
scheduler change is claimed. Original finite-bit Hermite ROOT remains OPEN.


### Actual cached setup and signed-middle VALUE certificates

C168 closes the actual setup-value conjunction after an exact two-block proof-only
repair of C165's rejected dependent-Decidable rewrite attempt. Four cuts, the
full factorial-reciprocal tail, clipped value and midpoint match the unchanged
source, including R/delta zero/negative and T0/T1. Source/own-output type+axiom
gates pass (30.000s/22.406s); original exit1, recovery sorryAx rejection and all
warnings are retained. No executable body or public type was changed.
[Setup certificate](../experiments/hermite-polynomial/precision/cached-setup-c166/README.md).

C174 closes generic signed middle entries and actual C23 cache substitution to
C21 middleCoeffQ (24.688s/25.062s exact source/own-output gates). Both roots use
only the ordinary3 axioms, no added correctness premise. Independent C178
static review is a separate pending stage at this checkpoint preparation.
[Middle certificates](../experiments/hermite-polynomial/precision/cached-middle-values-c167/README.md).

Complementary C172 executable screening passed1456 exact rational entries in a
25.906s parent subprocess while symbolic authoring continued. The result was
withheld until author freeze. It is finite discriminator evidence, not theorem,
SP state/export acceptance or matched-endpoint strategy comparison. Unknown
CPU/model/tokens/peak-memory remain unknown.
[Finite evidence](../experiments/hermite-polynomial/precision/cached-middle-finite-c172/README.md).

C161/C164 primitive and C169/C173 setup static-then-runtime internal reviews are
now preserved in13 exact original members. No source-publication, ProofSeal,
clean-TCB/native-cost or scientific ROOT promotion. Cost400, cached whole-data/
chain/source integration and816 are next obligations, not silently accepted.
Kernel/left/captured setup, native/bit/GCD/synthesis and finite-bit ROOT remain OPEN.


### Actual cached same-returned-data chain and partial middle-cost certificate

C193 verifies five unchanged C156 VALUE roots: all actual right coordinates,
whole returned RationalData, Window, same cast/ofTable dependent chain and
literal original piecewise grid source. Source/own-output gates pass34.016s/
26.672s; five typed consumers and all five ordinary-axiom reports pass. Parent
read the five actual types and seven printed loaded bodies, not every proof
term. Independent C188 source-first review is frozen; C196 static comparison is
separate, not inferred from compilation.
[Same-chain values](../experiments/hermite-polynomial/precision/cached-chain-values-c187/README.md).

C189 verifies actual middleFromCache partial total<=400*(k+1)^2 with no new
public assumption (24.922s/23.093s source/own-output exact type+ordinary axioms).
All generated factorial/sign/guarded-sum/collect work in that eight-counter
annotation is retained. Independent C194 source derivation is frozen separately;
comparison to the actual proof is pending, not self-approved.
[Partial cost](../experiments/hermite-polynomial/precision/cached-middle-cost-c183/README.md).

C178/C184 middle static-then-runtime internal reviews retain six exact original
members. Source first and later runtime exposure are separate freezes, with
inherited/dirty-TCB and direct-dependency-not-loader limits unchanged.
[Independent stages](../reviews/publication/migration-checkpoints-c190/README.md).

Failures remain exact: rejected Sum/implicit-index proof attempts, precompiler
memory deferral, low-cap interpreter exhaustion, and rejected cost normalization
attempt. Four failed compiler processes consumed129.299 observed subprocess
seconds; this is not total workflow/model/CPU time. Unknown calls/tokens/CPU/peak
memory stay unknown. Fin-index repair changed only proof; final run used actual
restored headroom and original3GiB cap plus2GiB reserve. No finite-screen/family
endpoint substitution or universal efficiency winner is claimed.

Previous ba2afcc1 full CI39075097319 succeeded (library/Tests and original15-test
finite replay), not a new finite-bit family acceptance. New checkpoint CI is
unverified. Cost816/same-run, kernel/left/captured setup, native/bit/GCD/finite-bit
synthesis/export and scientific ROOT remain OPEN; four textbook final admissions
and main4.33 migration are still OPEN. Robin publication policy is unchanged.


### Same-returned-run conjunction and bounded asynchronous decisions

C211 now proves the exact last C156 internal statement: the SAME returned
producer value refines the original chain AND its SAME annotated cost obeys
the unchanged816-plus-actual-setup/traffic/ofTable bound. Source32.953s and
fresh own-output exact-type/ordinary-axiom consumer28.047s pass. No new public
premise, weakened contract or increased proof budget was introduced. This is
an internal partial-cost result, not physical one-evaluation/sharing or full
finite-bit/poly(n_p) preparation.
[Exact proof and preserved failure](../experiments/hermite-polynomial/precision/cached-same-run-c208/README.md).

Ten original members preserve C199/C208 and rejected C207 exit1/47.563s;
no failed olean or zero-row axiom report is promoted. Eighteen further original
review members preserve six separately frozen source/static/runtime stages
for prerequisite same-chain values and middle cost. Those prerequisite reviews
are not an independent review of this new conjunction or a clean TCB rerun.
[Independent stages](../reviews/publication/migration-checkpoints-c205/README.md).

HARNESS section8a now routes to the existing asynchronous policy: autonomously
select bounded same-contract methods; ask asynchronously for material target,
error/success/oracle/budget/application trade-offs; continue unaffected work.
Proof and finite screens may run concurrently with immutable bindings and
source-blind release barriers. Compare all three methods only at matched
acceptance endpoints, retaining failed/censored work and unknown telemetry.
No new production event scheduler, scoring or measured strategy advantage.

Actual setup cost remains OPEN: C210 source failed29.094s; C216 proof-only
successor failed22.5s at no-progress simp, zero roots/no accepted output. C217
is authored, not proved. C219's precompiler check rejected the changed HARNESS
context; no compiler started. This is documented context drift caused by this
policy entry, not mathematical refutation, and no pin was waived or rewritten.
The new context must be explicitly bound before further proof validation.

Priorc913 fullHermiteCI39076442370/job117524465547 succeeded: actual fullTests
3460jobs and original15-test saved executable replay; this is not a new
finite-bit family acceptance. New checkpoint fullCI is unverified. Robin source
publication conflict still blocks main4.33 admission; no policy approval/change,
mainmerge, deployment, branchdelete, scientificROOT or textbookfinaladmission.


### Closed setup annotation and first Gaussian integer invariant

C223 closes the exact C202 partial setup target, with no public premise:
total(rightSetup n R delta).cost<=81*(d+1)^2+8*(d+1)+n+T+22,
d=sourceDegree(delta),T=tailCutoff(delta). Actual source27.422s, exact own-output
type/ordinary-axiom consumer24.969s, loaded-definition audit24.687s all pass.
Parent read actual type/axioms and loaded definitions, not every expanded root
proof or private recursive body.26 original seal/author/failure/preparer members
remain exact. C222->C224 is explicitly reviewed process-context succession with
the linked async policy additionally pinned, not a scientific/policy exception.
[Setup proof](../experiments/hermite-polynomial/precision/cached-setup-cost-c217/README.md).

The fixed Gaussian witness now has actual typed integer definitions and
independent source-first/static/successor-static review freezes. C225 original
Decidable failure remains; C227 adds only an explicit local constructive domain
decision, C228 types all31 names using its own table/core outputs. The final
literal1024 words and81local/eightsigned input diagnostics are parent-replayed,
not a uniform error/circuit proof. Apache-2.0/NOTICE and exact ancestry accompany it.
[Fixed model](../experiments/uncompute-2610-22367/gaussian-integer-model-c206/README.md).

C240 proves the exact C229 sealed all-D aligned128-block constancy theorem for
the actual integer model (source12.265s/own-output consumer9.859s, ordinary
axioms). It preserves six signed truncated middle rows, modular stored slope,
nine biased final rows and the special top-row drop. This is a symbolic integer
supplier, not finite screening or a replacement floor(full product), and not
Gaussian real-exp/f64 error, coherent circuit/cleanup/resource or SP/BE closure.
[Constancy proof](../experiments/uncompute-2610-22367/gaussian-constancy-c230/README.md).

Main migration diagnostic C234 actually compiles unmodified main Robin against
the4.33 context: exit1/86.344s, seven type/recursion errors, no accepted output.
Thus simply keeping that old file does not solve migration in this context.
No production source was changed. The separate experimental/source-publication
conflict remains; human approval for maintenance-rule design/review is pending.

Previous268522fc fullHermiteCI39078495808/job117530481115 terminalSUCCESS:
actual Tests3460jobs and original15-test finite replay. This is not the new
experimental proof set or a uniform finite-bit family acceptance. Current
checkpoint CI remains unverified; main4.29.1/fullHermitefinitebitROOT and four
bounded textbook final admissions are OPEN. Kernel/left/capturedsetup/native
bit/GCD/evaluator/synthesis/cleanup/export remain missing; C237 now designs the
literal fully costed kernel/left producer, not a return to the old2k+6 layout.


### Explicit five-block producer: typed sealed frontier, not a cost proof

C243 replaces the previously unaccounted kernel/left scalar callbacks with
literal comparison, factorial-binomial, charged powers/products and complete
materialization. Numerical loop dimensions use the actual second charged
cutoff result. The five-sum index, reflected signs, actual right boundary and
same returned data/cast/ofTable are retained; no canonical2k+6 layout replaces D.
C246 fails one dependent cast (exit1/28.671s), preserved unchanged. C248 changes
only that cast. C249 types source24.750s and own-output consumer24.063s; eight
Prop formations are NOT eight proofs. C250 seals exact bodies/statements BEFORE
new value/cost authoring. No new proved root or complete budget is claimed.
[Exact typed checkpoint](../experiments/hermite-polynomial/precision/explicit-five-block-c243/README.md).

C245 independent original-source baseline precedes C247 static comparison;
parent whole-read,31/40 raw pins respectively verified. This supports literal
semantics and branch-local ledgers, not full budget, proof/runtime association
or universal source-publication admission. Six original review members remain
frozen. C248 successor review and C252/C253 value/cost proofs are separate work.
[Review scope](../reviews/publication/migration-checkpoints-c254/README.md).

C244 isolates Gaussian's ACTUAL math.exp/half-away/centered429 reference. Negative
fold partners require the inclusive magnitude endpoint2^35 via valid xs=-2^35.
The compressed uniform route still needs119,275,520 quadratic blocks and an
operational monotonicity/enclosure supplier; sparse/NumPy scans are not enough.
The four-point/capped preflights are proposed, not executed. No refit/recenter,
source-target swap or uniform/circuit/error/resource/SPBE acceptance occurred.
[Operational reference audit](../experiments/uncompute-2610-22367/gaussian-error-reference-c244/README.md).

Priorc661 fullHermiteCI39079883741/job117534493326 now terminalSUCCESS: parent
actual logs read, Tests3460jobs23:57:45UTC, prooftrust0holes/axioms23:57:46,
15original finite replay tests23:58:02. This is the production frontier/baseline,
not the new experimental supplier or a uniform finite-bit family certificate.
Current checkpoint fullCI remains unverified; main4.29.1/Robin publication
conflict, fullHermitefinitebitROOT and four textbook final admissions stay OPEN.
No verifier/scoring/target/publication-policy/history/user-file/branch mutation.


### Same-return explicit cost checkpoint and asynchronous choice boundary

C263 actually closes the C250-sealed cost/counter projection for the SAME
explicit five-block result: source44.391s, separate exact-statement own-output
consumer26.968s, one public root, ordinary propext/Classical.choice/Quot.sound.
Actual selected quotient/remainder counts each <=14(n+1)D^2+4D and the full
named finite-operation frontierBudget are proved without added cache/F/value/
cost promises. C256/C259 normalization failures and C253/C258/C262 exact
source lineage remain immutable. Independent proof review is still PENDING;
source-only transport review C251 is not retroactive review of this new proof.
[Focused cost certificate](../experiments/hermite-polynomial/precision/explicit-five-block-cost-c262/README.md).

C257 gives separate source-derived canonical Rat data/working/raw-witness
height envelopes, with actual signed suffix/common-denominator invariants.
Parent whole-read and21direct+40retained hash checks match. Exact primitive
Sites coverage, Statement Seal and Lean height proofs are NOT supplied.
Native GCD/bigint scratch/control/evaluator/allocation, radius encoding, QR,
angles/gates/cleanup and full finite-bit SP remain OPEN.
[Bit-growth design, not proof](../experiments/hermite-polynomial/precision/rational-bit-growth-c257/README.md).

The value lane is separate: C260 scalar exit1/28.078s, C261 normalization then
C266 scalar exit1/28.672s; current remaining error is nested inverse-equivalence
normalization. Compiler recovery sorryAx is REJECTED, no accepted own value
supplier/root. C265 parent-wrapper schema failure occurred BEFORE any compiler,
was preserved, and C266 uses the original frozen root list with unchanged
consumer/signatures/caps. These are implementation failures, not mathematical
refutations. No old cached cost ledger is substituted for this new producer.

The human's asynchronous method-choice policy is already in HARNESS8a and
the bounded asynchronous design: autonomously choose bounded discriminators
inside the fixed contract, ask asynchronously for changed target/error/success/
oracle/budget or incomparable application trade-offs, and continue only
unaffected authorized work while waiting. Compare proof-first, screen-then-proof
and dual-lane at the SAME evidence endpoint with failures/censoring and TOTAL
cost. The14 isolated timing tests pass again; they establish no quantum-search
efficiency winner. No production event scheduler or score change was made.

C254 actual fullHermiteCI39081435433/job117538996204 is terminalSUCCESS:
Tests3460jobs00:22:37UTC, prooftrust0holes/axioms00:22:38,15original baseline
finite export tests00:22:53. This is not acceptance of the new experimental
cost proof or uniform finite-bit family. Research-publication CI still fails
on Robin alone; main stays4.29.1 and maintenance-rule human choice is pending.
Current new-head full CI remains unverified. No merge/deploy/branch deletion,
verifier/scoring/target/publication-policy/history or user-file mutation.

Append-only privacy clarification for C254's historical shorthand: its public
inventory is30 EXACT original archive members PLUS1 explicitly path-redacted
diagnostic member, not31 byte-identical originals. Original private receipts
are preserved, and source-binding/report record the exact redaction and hashes.


### Canonical height foundation proved locally; explicit cost independently reviewed

C278 actually types the exact canonical Rat height/unreduced-witness definitions
and four closed targets (12.094s+12.281s). C280 freezes exact bodies/statements
BEFORE C282 first-root proof authoring. C285 source0/11.781s and separate exact
expanded own-output consumer0/12.156s close ONE root, heightBound: h(q)<=B iff
1<=B AND abs(q.num)<2^B AND q.den<2^B, for all q/B including zero and signs.
Actual consumer selects the fresh own output and prints ordinary3axioms for
root and expanded assignment. Source zero axiom rows are not an empty proof.
Common-denominator/primitive-representation/primitive-width targets remain OPEN,
as do actual suffix/Sites coverage, producer-wide bit height and native costs.
Independent source-first height review C288 is separately frozen; not yet
author/runtime-associated or public-admitted. This is proved_locally, not ROOT.
[Exact height checkpoint](../experiments/hermite-polynomial/precision/rational-height-c269/README.md).

C264 independent actual-operation derivation froze BEFORE reading C262 proof;
parent whole-read,44raw/retainedlength/hashchecks match. C273 subsequently binds
that exact source to C263 own output/exact consumer/type/ordinary root axioms
and actual selected directdeps; parent whole-read,34direct+10private member
pins match. No concrete omission/association mismatch found. This completes
scoped internal static review+recorded-runtime association, NOT universal
source publication, independent rerun, complete loader/cleanTCB or fullSPBE.
Historical C263 receipt is not rewritten to upgrade its old review status.
[Separate freezes and limits](../reviews/publication/migration-checkpoints-c287/README.md).

The value lane remains REJECTED: C270 scalar exit1/28.015s; C272 explicit
instantiation reaches first inr but rw cannot see the term under its match.
C275 isolates a probe; C279 exit1/27.938s. C281 adds only rfl; C284 probe
exit1/27.016s explicitly rejects definitional equality despite apparently
matching ordinary print. The prior alpha-only explanation is NOT accepted.
No probe-own-consumer/scalar/chain ran after probe failures; zero accepted own
VALUE roots. All frozen authors and actual failures are retained in68members.
Full explicit-type diagnostics are separate work; this is implementation
failure, NOT a mathematical route obstruction or compiler-bug conclusion.
[Recoverable value/failure checkpoint](../experiments/hermite-polynomial/precision/explicit-five-block-values-c252/README.md).

Prior6c33fullHermiteCI39083056338/job117543833064 is terminalSUCCESS: actual
complete logs read, Tests3460jobs00:46:00UTC, prooftrust0holes/axioms00:46:01,
15ORIGINAL finite baseline tests00:46:13. This does NOT accept new experiments
or a uniform finitebit family. PublicationCI39083056333/job117543833032 still
fails only missing Robin record;50valid/51changedproductionmodules, main4.29.1,
human compatibility-maintenance choice pending. Current new-head CI unverified.
No verifier/scoring/target/policy/history/user-file change, merge/deploy or
branch deletion. Full Hermite finitebit ROOT, four textbook final admissions
and Gaussian operational/circuit/resource/SPBE ROOT stay OPEN. Async matched
three-arm strategy superiority remains unmeasured; ordinary fixed-contract
method choices autonomous, material assumption/budget choices ask the user.


### Common-denominator foundation locally proved; independent first-height review completed

C296 closes the second C280 rational foundation commonDenominator against the
exact signed/zero canonical Rat and unreduced commonWitness definitions.
Actual source0/13.172s -> own proof15c8671c... -> exact expanded own-output
consumer0/12.188s, two ordinary3axiom rows (root plus assignment, ONE root).
The local conditions Q>0, den(q) divides Q, abs(q)<=M are witness bridges,
not new scientific-target premises. Primitive representation/width, actual
suffix invariants, complete Sites coverage and producer-wide nativebit/GCD/
allocator/CPU bounds remain OPEN. Independent common-denominator review is
separate; this new root is proved_locally, not source-publication or fullSP.
[Exact proof and immutable original receipts](../experiments/hermite-polynomial/precision/common-denominator-c293/README.md).

C288 source-first -> C290 author/static comparison -> C291 recorded-runtime
association are separate immutable freezes for the earlier heightBound root.
Parent whole-read and rehashes match13/19/31direct input bindings respectively,
plus10private C291 runtime members. No concrete focused mismatch was found;
not an independent rerun, fresh universal decoder, complete loader/cleanTCB
or main/publication admission. Old pending-review receipts remain historical.
[Scoped height review](../reviews/publication/height-foundation-checkpoint-c300/README.md).

C283 actually forms three unchanged allocated partial-ledger targets in
27.968s+27.859s. C295 exact preproof seal then freezes them before any proof
authorization. M=n+1+2k+tailCutoff(eps/(4(k+1)^2)); proposed 5e6*M^7 operation
and5e5*M^5 selected-index bounds are NOT proved. Types/manual coefficients
are not nativebit/quantum-resource/value/root certificates.
[Typed and sealed, zero proofs](../experiments/hermite-polynomial/precision/allocated-polynomial-interface-c276/README.md).

The bounded asynchronous organization remains fixed-contract autonomy plus
user choice for material scientific/oracle/error/success/budget trade-offs.
Proof and finite screening may run concurrently for distinct uncertainties;
matching contract/revision/evidence endpoints and TOTAL consumed cost are
required for comparisons. No three-arm quantum strategy winner is measured,
and no production scheduler/scoring/verifier change is installed.

Current c221 publicationCI39084745643/job117548849697 actual complete logs
read: changed-module gate fails only missing RobinMatrix reviewed record.
Stateprep smoke39084745652 and fastwebsite39084745615 pass. FullHermite
run39084745630/job117548849683 was still compiling when this note was formed;
completion is separately required before pushing the same ref. Main remains
Lean4.29.1; contribution4.33.0. Compatibility-maintenance policy choice remains
unanswered; no waiver or false source record. No mainmerge/deploy/branchdelete.
Hermite finitebit ROOT, four textbook admissions and Gaussian operational
error/circuit/phase/cleanup/resources/SPBE root remain OPEN.


### Actual primitive representation and allocated dyadic-scale roots; chain remains open

C309 accepts the unchanged C280 primitiveRepresentation target, including all
signed/zero/add/sub/mul/div actual raw witnesses. Source0/18.531s -> own
ebf25188... -> exact expanded own-output consumer0/16.625s; root+assignment
ordinary3axioms. C303 parser failure0acceptedroots is preserved; C305 changes
only notation to explicit Rat.divInt, consumer byte-identical. This does NOT
prove primitiveWidth, actual suffix/Sites coverage or producer-wide nativebits.
[Actual representation proof and preserved failure](../experiments/hermite-polynomial/precision/primitive-representation-c305/README.md).

C307 accepts C295's FIRST exact scale target: with n_p=n+1 and the original
M=n+1+2k+tailCutoff(eps/(4(k+1)^2)), M<=n_p+4k+2+tailCutoff eps for all k,n
and positive rational eps, including eps>1. Actual source0/43.234s -> own
6e7f984f... -> operationScale-expanded exact ownconsumer0/40.562s ordinary3.
Original unused/unreachable/sequencing/defProp warnings retained. Two other
C295 polynomial budget/same-run roots are NOT proved by this packet. Native
Rat/GCD/CPU/allocator, finite-angle/quantum gates/cleanup/export remain OPEN.
[Exact scale proof](../experiments/hermite-polynomial/precision/allocated-dyadic-scale-c306/README.md).

C299 independently reconstructs CommonDenominator before C293 proof release;
C302 then compares author source; C308 later associates C296 raw runtime.
Parent whole-read23/24/43direct inputs+10private raw members and payloads MATCH.
No concrete scoped source/type/axiom mismatch. Recorded association is NOT
independent rerun, clean loader/TCB or source-publication admission. Init path
vs prefix provenance limitation and defProp warning remain. Old receipts
are not rewritten. [Separate review freezes](../reviews/publication/common-denominator-checkpoint-c314/README.md).

Value progress is precise: C301 closes probe/own-consumer and THREE scalar
roots (decode/comparison/actual factorial translation), using the unchanged
C275/C281 scalar that earlier failed probes had prevented from running.
C301 chain fails3interfaces. C304 proof-only successor clears the right-index
transport goal, but C313 source exit1/57.734s rejects two remaining interfaces:
column rewrite fails under implicit transparency because assemblySize/fiveSize
carrier types differ syntactically; final dependent cutoff/degree carrier
normalization still fails. No accepted C313 own chain, no final consumer run,
compiler-recovery sorryAx rejected. Keep prior THREE scalar roots, not seven.
This is implementation failure, not scientific impossibility/compiler bug.
[Exact success/failure boundary](../experiments/hermite-polynomial/precision/explicit-value-refinement-c313/README.md).

Current ee6a publicationCI39085996428/job117552571755 actual complete logs read:
fails only RobinMatrix missing reviewed record.50valid/51changedproduction
modules, main4.29.1, contribution4.33.0. FullHermite39085996387/job117552571580
is live at preparation; do not cancel it with premature same-ref push. No
maintenance-policy approval, waiver, mainmerge/deploy/branchdelete or production
behavior/target/scoring/verifier/history/user-file change. Hermite finitebit
ROOT, four textbook admissions and Gaussian operational/circuit/resource/SPBE
ROOT remain OPEN; async strategy superiority remains unmeasured.


### Actual polynomial partial-ledger envelopes and all raw primitive widths locally proved

C316 closes BOTH remaining C295 targets against the unchanged actual sourceDelta
and SAME returned produceExplicitStored result. Source0/43.875s -> ownab75d04e...
-> exactownconsumer0/36.391s ownc5a4d475..., ordinary3axioms on2root+3provider
rows. For M=n+1+2k+tailCutoff(eps/(4(k+1)^2)), total partial ledger<=5e6*M^7
and selected quotient/remainder calls each<=5e5*M^5, allk/n,positiveRat eps,
allRat R. Intermediate facts are proved, not public assumptions. Combined
with prior scaleDyadicBound, all3C295 local suppliers now pass focused gates.
[Exact allocated ledger proof](../experiments/hermite-polynomial/precision/allocated-polynomial-ledger-c311/README.md).

C325 closes primitiveWidth, the FOURTH C280 local foundation: source0/21.312s
own05ceefc5... -> original expandedexactownconsumer0/17.375s own83bdc961...,
root+assignmentordinary3. All listed raw intermediates retained, signed/zero
division and add/sub carry1 unchanged. C318 membership endpointfailure and
C322 localwidth unfoldingfailure are preserved; C324 changes only4finalsimp
calls after C321's4membershiplists. C323 separately discloses C321 inherited
ancestor outputs metadata; current authorfreezepayloads/stagesource, not that
array, bind actual source. C324 fresh outputs correct and all old bytes stay.
[Exact width proof and failure lineage](../experiments/hermite-polynomial/precision/primitive-width-c324/README.md).

These are THREE new locally proved suppliers, NOT all native/quantum resource
costs or full state preparation. Actual source-suffix denominator/magnitude
invariants, complete primitive Sites coverage and producer-wide bit heights
remain OPEN. Rational epsilon input height can grow with fixed cutoff (e.g.
(2^B+1)/2^B>1), so native input/GCD/ceil/clog/index/allocator/CPU work cannot
be inferred from M counters. Radius height, finite QR/angle synthesis/gates/
depth/cleanup/export and global normalized-state/error acceptance remain OPEN.
Independent reviews/source-publication/main/reader/PURIFIED not claimed.

C315 exactC313 carrierforensics parentwhole-read31inputs+6private members+
2payloadsMATCH: hidden assemblySize/fiveSize product widths and whole dependent
QData cutoff/degree carriers need synchronized typing, not a new mathematical
premise. Prior THREE scalar VALUE roots remain; no accepted chain. C319 new
two-carrier author checkpoint is frozen but actual gate PENDING; not success.
[Forensic evidence, not a repair certificate](../reviews/publication/chain-carrier-forensics-c326/README.md).

Current fef8 publicationCI39087045546/job117555679611 actual complete logs read:
fails only missing RobinMatrix record,50valid/51changedproductionmodules.
Main4.29.1 vs contribution4.33.0; maintenancechoicepending, no policy waiver.
FullHermite39087045543/job117555679666 live at preparation. No premature
same-refpush/mainmerge/deploy/branchdelete; no verifier/scoring/scientifictarget/
productionbehavior/history/userfile change. Hermite finitebitROOT, fourtextbook
finaladmissions, Gaussianoperationalerror/circuit/resource/SPBEroot stayOPEN;
matched async strategy superiority unmeasured. Full Goal stays ACTIVE.


### Actual producer VALUE chain and same-result partial-cost composition locally closed

C329 now closes the EXACT seven C250 VALUE interfaces. C319 source0/62.265s
-> own d515494b... -> unchanged full exact own-output consumer0/37.437s
own bd6fd1d9.... Nine private helper and seven public rows have only ordinary
axioms (comparison needs propext/Quot.sound, others ordinary3). Three scalar
roots were already accepted; FOUR chain VALUE interfaces newly close, not
seven new algorithms. Only two proof-body carrier conversions change from
C304; all sealed statements, executable definitions and scalar/consumer bytes
stay fixed. This closes actual QData equality, table window, chain refinement
and the rational-grid source action with its original R>0 premise.
[Exact VALUE refinement](../experiments/hermite-polynomial/precision/explicit-value-chain-c319/README.md).

C337 then closes the EIGHTH original C250 same_run proposition: correctness
and partial total/quotient/remainder bounds for the SAME literal returned
result. Unchanged C332 source uses And.intro of the accepted VALUE and cost
suppliers. Source0/37.563s own c41a071c... -> exact own-output consumer0/39.735s
own e7607a8f..., one source/four root-consumer-provider rows ordinary3.
C335's first attempt failed24.719s on missing transitive CachedMiddleCostProof
BEFORE theorem checking, zero accepted output/consumer not run. C337 adds the
pinned prior C263 cost path after the value path and verifies the cost context;
no source, target, cost, scoring, verifier or resource-cap change. Original
failed plan/result retained; raw feedback with an inherited local search path
stays private, and a separately hash-bound sanitized public derivative is used.
[Same actual result, not physical runtime](../experiments/hermite-polynomial/precision/explicit-same-run-c332/README.md).

This adds FIVE closed local interfaces (four VALUE plus one composition) on
the prior frontier, not a new algorithm or full poly(n_p) finite-bit result.
All8C250 and all3C295 local suppliers now compile with exact own consumers.
Partial M^7 operation/counter bounds still do NOT supply producer-wide operand
bits/common-denominator/magnitude/Sites coverage, native GCD/floor/ceil/clog/
index/CPU/allocator or physical once-only evaluation/sharing. Normalized-state
error, finite QR/angles, synthesized gates/depth, phase/clean-workspace and
independent family executable acceptance remain OPEN. New chain/same-run
independent review, clean transitive TCB, source-publication and PURIFIED remain
separate. Earlier failed receipts are immutable, not overwritten by success.

Two existing foundations now have scoped independent internal reviews:
C317 source-first -> C327 static -> C331 recorded association for dyadic scale;
C320 source-first -> C330 static -> C334 recorded association for primitive
representation. Parent whole-read and exact pins+10private runtime members
per root MATCH. Separate source/proof/runtime releases preserve anti-anchoring
barriers, with all previous authorship/partial-source exposures disclosed.
These are NOT fresh universal decoders, independent reruns or full loader/TCB
attestations. Old pending-review receipts remain historical.
[Scale review](../reviews/publication/dyadic-scale-review-c340/README.md) /
[Representation review](../reviews/publication/primitive-representation-review-c340/README.md).

Current de7b full Hermite CI39087980863/job117558461294 terminalSUCCESS;
actual complete logs obtained, relevant build/trust/finite sections read:
3460jobs at2026-10-18T02:06:07.5940969UTC; zero unapproved holes/source axioms
02:06:08.4306813;15ORIGINALfinite export tests02:06:20.4638003, independent
finite replay(k1,n3,L1)passed, lean_certificate_claimed=false. NOT new C340
or uniform finite-bit family acceptance. Current complete publication logs
39087980753/job117558460730 still fail missing RobinMatrix reviewed record
only:50valid/51changedproductionmodules. Main actual4.29.1, contribution4.33.0;
maintenance choice unresolved, no waiver/merge/deploy/branch deletion.
FullHermitefinitebitROOT,four textbook admissions,Gaussian operational error/
circuit/phase/cleanup/resources/SPBE ROOT remain OPEN. Matched asynchronous
strategy superiority remains unmeasured. Full Goal unchanged ACTIVE.


### Actual suffix targets typed/sealed; source input-height and normalized-error analysis

Recoverable WIP checkpoint, ZERO newly accepted mathematical roots. C338
inspects the literal producer's internal suffixes, k! common-denominator
strategy, signed middle denominator and radius/epsilon input bit heights.
Its proposed global bit-height envelope remains UNPROVED; hand-derived
stress families are not executed or Lean-certified evidence.
[Actual producer height strategy](../experiments/hermite-polynomial/precision/producer-height-analysis-c338/README.md).

C342 fixes the actual C23 factorial table and original recursive sumEntries
observations, including every dropped offset, next-tail connection and the
empty k=i=0 boundaries. C344 actually forms all3closedProps in39.610s+39.578s,
own f7e5fc3d... -> exact type consumer own62a9f346.... C345 then issues the
exact preproof Statement Seal. No mathematical proof follows merely from
Prop formation. Two distinct author proof branches are successor work,
not accepted by this checkpoint. No producer or resource model changed.
[Typed, sealed, unproved targets](../experiments/hermite-polynomial/precision/source-suffix-interface-c342/README.md).

C341 source analysis identifies the existing positive-Rat L/epsilon
normalized_original_error <=epsilon/2 and a necessary direct public-LE
adapter: wordIndex is LSB-first while sampleEquiv adds reversal. Reuse the
old error theorem rather than duplicate it or import the old exact chain's
bond/cost bound. IMPORTANT EXPLICIT CORRECTION: C341 incorrectly describes
the exponential argument as -p^2. Actual tails are exp(p) for p<-1 and
exp(-p) for p>0; middle uses exp(-1). Parent directly re-read the literal
definitions/proof. Inputs are still nonpositive, so enclosure domain and
existing error allocation are unchanged. Original erroneous bytes/hashes
are preserved together with a separate correction; hash integrity is not
semantic accuracy. No Gaussian target substitution is authorized.
[Source bridge analysis and explicit correction](../experiments/hermite-polynomial/precision/normalized-source-analysis-c341/README.md).

Producer-wide middle/Sites/operand heights, native integer/GCD/floor/ceil/
clog/index/CPU/allocation/sharing, original arbitrary-Real-L representation,
actual rounding/QR/angles/synthesis/phase/cleanup and independent family
acceptance remain OPEN. No scientific ROOT, new source publication, reader
seal or PURIFIED status. Four textbook admissions and Gaussian operational
error/circuit/resources/SPBE ROOT also remain OPEN.

Prior836b actual full HermiteCI39089118282/job117561835681 now terminalSUCCESS:
3460jobs2026-10-18T02:27:58.5312687UTC; proof trust0unapprovedholes/0sourceaxioms
02:27:59.5935468;15ORIGINALfiniteexporttests02:28:18.4866912; independent
finite replay(k1,n3,L1)passes with lean_certificate_claimed=false. Actual
complete logs obtained, relevant sections read; NOT new checkpoint build or
poly(n_p) finite-bit family acceptance. Current publication39089118289/
job117561835817 still fails ONLY missing RobinMatrix whole-module reviewed
record. Main actual4.29.1, contribution4.33.0,50valid/51changedmodules.
Maintenance policy choice unresolved; no waiver, main merge, deploy or
branch deletion. Async proof/screen policy retains fixed-contract autonomy,
material-choice user approval, exact event bindings and matched acceptance
endpoints/total-work comparison; no measured strategy superiority claimed.


### Two exact internal suffix roots locally proved; returned-cache join uncompiled

C352 fresh parent gate closes original C345 actualSuffix: literal actual
factorial table, every dropped sum=Ico, actual recursive tail=next offset,
zero offset=original sourceEntry, explicit empty branch. Source0/40.734s
own5c7a7631... -> complete expanded own consumer0/30.875s ownc84e4d26...;
source and two consumer rows ordinary3. C346 author first attempt failed
41.125s on two Fin/reindex elaborations; no own output or failed import.
Original source/plan/result and full private streams retained. Successful
author attempt and fresh parent run are separate; proof-only repair never
changes sealed targets/definitions. Public failure feedback is a separately
hash-bound privacy derivative, not a rewritten original.
[Actual recursive binding](../experiments/hermite-polynomial/precision/source-suffix-binding-c346/README.md).

C351 closes original suffixEnvelope, all k/i/s including empty and k=i=0:
canonical denominator divides SAME k!, nonnegative, precise remaining-count
bound(i+1-s)*2^(2k). Source0/39.609s ownbed2da08... -> complete expanded own
consumer0/36.547s ownbe0a7530..., ordinary3. Factorial/choose/finite-sum
facts are internal proof dependencies, not new source assumptions.
[Shared denominator and magnitude](../experiments/hermite-polynomial/precision/source-suffix-envelope-c347/README.md).
These are TWO new local suppliers, not a whole-producer bit/CPU theorem.

C353 third C345 returnedCache AND-join is authored but UNCOMPILED. C358
available3927MiB<3072+2048 reserve deferred BEFORE any Lean invocation.
C359 unchanged source/consumer/target lowered cap to1536 but kept2048
reserve; available3532<3584 again deferred BEFORE compiler/consumer. Zero
Lean attempts, not proof/API failure or mathematical obstruction. Both
original plans/results retained; no repeated cap-lowering loop, no user
application killed. The two accepted suppliers do not prove this WIP join.
[Uncompiled same returned-cache join](../experiments/hermite-polynomial/precision/returned-source-cache-c353/README.md).

C349 direct public-LE producer vector interfaces now actually typecheck in
C35439.703s+30.797s, ownb2a7b205... -> exact type ownconsumerae6fa88c....
C356 preproof seal follows: wordIndex direct-LE, actual returned chain's
Euclidean vector=finiteVector, existing allocated error<=epsilon/2 for
positive rationalL/epsilon. Eq.refl only checks Prop expansion: ZERO proofs
of these3targets. No reversal, dense executable table, source oracle or new
error allocation. Unused-k warning retained, no linter disabled. C357 new
proof chain is successor work, not accepted by this checkpoint.
[Typed and sealed direct-LE bridge](../experiments/hermite-polynomial/precision/public-le-producer-interface-c349/README.md).

Complete primitive Sites, signed middle/producer-wide operand heights,
native integer/GCD/floor/ceil/clog/index/CPU/memory/physical-sharing costs,
original arbitrary-Real-L input, actual finite rounding/norm/QR/angles/
synthesis/phase/cleanworkspace/export and independent family acceptance
remain OPEN. Internal focused proofs are not independent source review,
clean transitive TCB, source-publication/main/reader/PURIFIED or ROOT.
Four textbook admissions and Gaussian operational-error/circuit/resources/
SPBE ROOT remain OPEN. Fixed-contract async policy unchanged; strategy
superiority unmeasured, no verifier/scoring/runtime policy change.

Prior7f7297b fullHermiteCI39090933770/job117567343869 terminalSUCCESS;
complete logs obtained,relevant build/trust/finite sections read:3460jobs
2026-10-18T02:58:02.3702520UTC;prooftrust0unapprovedholes/0sourceaxioms
02:58:03.4198684;15ORIGINALfiniteexporttests02:58:19.4768695;
independentfinite replay(k1,n3,L1)passed,lean_certificate_claimed=false.
This is NOT new C355/fullfinitebitfamily acceptance. Current publication
39090933990/job117567344631 actualcomplete logs still fail missing
RobinMatrix whole-module reviewed record only,50valid/51changedmodules.
Main af585d9... actualLean4.29.1, contribution4.33.0. Maintenance policy
choice unanswered; no waiver, main merge/deploy or branch deletion.
