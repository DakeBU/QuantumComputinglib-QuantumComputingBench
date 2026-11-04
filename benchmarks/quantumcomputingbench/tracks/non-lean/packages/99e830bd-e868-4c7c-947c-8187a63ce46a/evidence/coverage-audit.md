# Coverage planning audit

Planning only, by `/root/coverage_audit`, against main `6b23dab68c2970062ddfd568ce94bce74b566483` and catalog `5269b9f2521e3bf14db293fea34895f6e44a387c2479c164407b4d16dd9a2247`. No questions, reference answers, rubrics, admission decisions or independent mathematical acceptance were authored in this pass.

The current inventory contains **198 retained cores and 15 reserved cores**. The recommended bounded cohort is **four unchanged-contract refinements and eight uncounted candidate targets, with B3 explicitly amended before drafting**. State preparation is the organizing objective; linear algebra, representations, registers, polynomial structure, resources and the approximate block-to-state bridge serve that objective.

## Frozen evidence boundary

Use snapshot `qcb-snapshot-ffa644f0da3031a1ce754b9a` at source commit `86b9e677566498da04faebcf4e5ed57f177c6bb1` from `benchmarks/quantumcomputingbench/manifests/release-v3/snapshot.json`. Every proposed graph anchor exists there. All 13 source files listed in the JSON were compared byte-for-byte with that commit; all are unchanged in the current worktree. Their exact hashes, declaration lines and MIT license are recorded in the JSON. Source inventory status is historical evidence, not a new Lean run or proof that these new NL translations are correct.

The screening loaded the complete current title/question inventory, all 15 reservations and all existing proposal identities, then compared nearest questions and relevant source definitions in detail. This is a bounded coverage and conflict audit, not a complete mathematical rereview of all retained answers or global semantic deduplication. The JSON preserves every current title/question and binding for reproducibility. Parent reports an empty open-PR search and GitHub push permission false; this worker did not independently query that service.

There are 15 existing Lean proposals and no existing non-Lean proposals in the planning snapshot. Concurrent authoring after the plan freeze is not part of that inventory. SP007 and SP114 have existing Lean companion proposals; preserve their common core IDs and frozen contract bindings. No proposed new target collides by literal ID with a reservation. Semantic adjudication remains mandatory, particularly B2.

## Recommended leaves

| Slot | Identity | Mathematical objective | Key overlap / disposition |
| --- | --- | --- | --- |
| A1 | `qcb-core-sp-006` | Make the nonzero normalizer boundary explicit | Same core; unchanged contract |
| B1 | `qcb-core-sp-007` | Expose the full chronological transfer induction | Same core; unchanged contract |
| C1 | `qcb-core-sp-114` | Make shifted-Taylor cut factors explicit | Same core; unchanged contract |
| A4 | `qcb-core-la-015` | Derive the sharp rotation norm through its Gram matrix | Same core; unchanged contract |
| A2 | Unassigned candidate | Normalization sensitivity and the nonzero denominator | qcb-core-sp-006, qcb-core-sp-113 |
| A3 | Unassigned candidate | Approximate projected block to normalized state and success | qcb-core-be-001, qcb-core-plan-010, qcb-core-plan-011, qcb-core-plan-510 |
| B2 | Unassigned candidate | Coherent families require aligned phases | qcb-core-la-016, qcb-core-be-104, qcb-core-plan-207 |
| B3 | Unassigned candidate | Optimal precision allocation under a supplied telescoping error budget | qcb-core-la-015, qcb-core-la-120, qcb-core-sp-117 |
| C2 | Unassigned candidate | Internal TT basis gauges preserve the represented state | qcb-core-la-002, qcb-core-sp-003, qcb-core-sp-004, qcb-core-sp-012 |
| C3 | Unassigned candidate | Gram environments characterize boundary norms and invisible directions | qcb-core-la-209, qcb-core-la-210, qcb-core-sp-004 |
| B4 | Unassigned candidate | Head-first TT words versus little-endian public samples | qcb-core-la-004, qcb-core-la-013, qcb-core-sp-007 |
| C4 | Unassigned candidate | Bernstein coefficient accuracy to normalized sample accuracy | qcb-core-sp-108, qcb-core-sp-110, qcb-core-sp-111, qcb-core-sp-113 |

For existing refinements the exact current question, assumptions, conventions, family, split, source scope and contract hash are fixed. Expand or repair explanations only within that request; if authoring uncovers an actual false question, stop that leaf and return a typed successor need. Do not conceal it in an answer-only proposal.

## Candidate distinction and source anchors

### A2: Normalization sensitivity and the nonzero denominator

Derive a uniform Euclidean bound for the difference between normalized nonzero vectors from an absolute input error and a lower bound on one input norm. Treat error below the lower bound, and show why a positive norm margin is indispensable. Exact-vector and physical-ray metrics must remain distinct.

**Distinct target:** The existing questions establish exact normalization or one specific mass anchor; neither assesses perturbation conditioning or a family approaching the zero vector.

**Boundary:** No frozen declaration is asserted to prove the perturbation theorem; this is a new elementary NL derivation from the normalization interface.

Anchors: `declaration:QuantumBlockEncoding.RealAmplitudePreparation.normalized_sum_sq`, `declaration:QuantumBlockEncoding.StatePreparationTarget`.

### A3: Approximate projected block to normalized state and success

For an explicit clean isometric embedding, unitary U, positive alpha, operator-norm error epsilon and unit input b with a stated positive lower bound on ||A b||, derive the accepted-branch success interval and normalized-state error. Preserve the clean branch, nonzero condition, normalizer factors and separately charged repeated-attempt access; never infer universal necessity of postselection.

**Distinct target:** Plan011 treats exact SVD dilation and exact success; BE001 defines error. This target composes approximate operator error with input overlap, conditioning and success.

**Boundary:** The abstract approximationBound field is not itself an operator-norm theorem. The actual induced-L2 inequality and positive alpha must be explicit in the candidate.

Anchors: `declaration:QuantumBlockEncoding.ApproximateOperatorBlockEncodingCandidate`, `declaration:QuantumBlockEncoding.signalSystemBlockProjection`, `declaration:QuantumBlockEncoding.StatePreparationTarget`.

### B2: Coherent families require aligned phases

For controlled preparations of unit vectors with branch-specific exact phases and an orthonormal label register, characterize exact equality and common-global-phase equivalence on a populated label superposition, quantify its Euclidean phase error, and state an explicit label-phase correction. Include unused labels and singleton support.

**Distinct target:** LA016 includes a single 2pi rotation/coherent-branch warning, BE104 one compiled stored phase, and plan207 environment-record dephasing. The proposed target assesses arbitrary controlled-family phase alignment and support-dependent necessary/sufficient conditions.

**Boundary:** Highest semantic-overlap risk: independent reviewer must decide whether the generalized label theorem is a distinct target or should be a view/refinement of LA016. Do not count before that ruling.

Anchors: `declaration:QuantumBlockEncoding.evalPrimitiveProgram`, `declaration:QuantumBlockEncoding.evalGlobalPhase`, `declaration:QuantumBlockEncoding.evalGlobalPhase_unitary`.

### B3: Optimal precision allocation under a supplied telescoping error budget

**Amendment:** the original aligned-circuit/Hermite-budget target was rejected as new because `breadth-hermite-angle-budget` already assesses it in the legacy `dev` cohort. Root approved the replacement before B3 drafting; the rejected original remains in the JSON as a superseded planning entry, not a counted contribution.

For m>=1, positive weights a_j and 0<eta<1/2, optimize the stipulated weighted precision cost sum_j a_j log2(1/delta_j) subject to 0<delta_j<=1 and sum_j delta_j<=2eta. Require a proof of optimality, integer-ceiling precision conversion, the resulting cost overhead, and explicit m=0/eta=0 boundaries. The supplied telescoping error bound is a shared prerequisite. The new assessment is constrained allocation and rounding, not another uniform Hermite budget derivation.

Anchors: `declaration:QuantumBlockEncoding.PrimitiveCircuitPerturbation.Aligned`, `declaration:QuantumBlockEncoding.PrimitiveCircuitPerturbation.aligned_eval_distance_le`. These support the error interface; the optimization is an original NL derivation. No actual compiler, angle supplier, finite-bit runtime or hardware gate cost is inferred from a stipulated precision objective.

### C2: Internal TT basis gauges preserve the represented state

For finite real scalar-boundary matrix-product amplitudes and invertible changes of each internal bond basis, prove cancellation through the complete contraction, explain boundary transformations, preserve the normalized target, and show that arbitrary invertible gauges need not preserve right canonicality.

**Distinct target:** SP012 concerns arbitrary inactive completion columns under support propagation, not invertible changes in active bond coordinates. LA002 absorbs one residual; the new target is full-chain gauge equivalence and its canonicality boundary.

**Boundary:** No existing gauge theorem is claimed. Invertibility is an explicit sufficient hypothesis for this construction, not a necessary condition for all equivalent TT representations.

Anchors: `declaration:QuantumBlockEncoding.TensorTrainCanonical.contract`, `declaration:QuantumBlockEncoding.TensorTrainCanonical.absorb_slice`, `declaration:QuantumBlockEncoding.TensorTrainCanonical.RightCanonical`.

### C3: Gram environments characterize boundary norms and invisible directions

Starting from the exact local right Gram recursion with every terminal bond label included, establish symmetry/positive semidefiniteness, the quadratic form for an arbitrary left boundary, and the kernel as directions annihilating all word contractions. Distinguish this characterization from a stored operation-cost bound.

**Distinct target:** LA209 counts a stored recursion; LA210 states the scalar-boundary norm. This target assesses the full matrix, arbitrary boundary vectors, positivity and an exact kernel criterion.

**Boundary:** For this real source use transpose, not unexplained complex conjugation; zero/empty bonds and zero-length identity environment need explicit treatment.

Anchors: `declaration:QuantumBlockEncoding.TensorTrainNormEnvironment.gram`, `declaration:QuantumBlockEncoding.TensorTrainNormEnvironment.gram_eq_sum`, `declaration:QuantumBlockEncoding.TensorTrainNormEnvironment.gram_scalar`, `declaration:QuantumBlockEncoding.TensorTrainNormEnvironment.norm_pos_of_nonzero`.

### B4: Head-first TT words versus little-endian public samples

Derive the index represented by a head-first TT word, the physical wire reversal required for public little-endian sampling, and the resulting amplitude relabeling. Check a non-palindromic word, empty/one-bit cases, and distinguish a mathematical relabeling from charged physical routing.

**Distinct target:** LA004 groups ancilla and system indices; LA013 proves generic wire conjugation. This target establishes the exact compiler-specific TT word/public sample map and detects a real reversal mismatch.

**Boundary:** Do not silently use the source reversed sample map as the unreversed physical basis map. No free SWAP circuit or routing count follows.

Anchors: `declaration:QuantumBlockEncoding.TensorTrainWord.basisEquiv`, `declaration:QuantumBlockEncoding.TensorTrainWord.reverseBasis`, `declaration:QuantumBlockEncoding.TensorTrainWord.sampleEquiv`, `declaration:QuantumBlockEncoding.TensorTrainWord.sampleEquiv_value`, `declaration:QuantumBlockEncoding.TensorTrainWord.sampleEquiv_public`.

### C4: Bernstein coefficient accuracy to normalized sample accuracy

For two same-degree Bernstein coefficient rows uniformly close on a grid in [0,1], derive pointwise and finite-sample vector error and then a normalized-state error under an explicit positive mass/norm margin. Account for sample count and exhibit why the interval and normalization premises matter.

**Distinct target:** SP108 proves exact source representation, SP110 coefficient ranges after restriction, SP111 exact mass. This target propagates coefficient error through sampling and normalization.

**Boundary:** The partition-of-unity argument is a shared assessed subproof, not additional novelty. Bernstein degree elevation alone was rejected as too close to SP108.

Anchors: `declaration:QuantumBlockEncoding.HermiteBernstein.basis_nonneg`, `declaration:QuantumBlockEncoding.HermiteBernstein.basis_sum`, `declaration:QuantumBlockEncoding.HermiteBernstein.bernstein_sum_bounds`, `declaration:QuantumBlockEncoding.RealAmplitudePreparation.normalized_sum_sq`.

## Split and proof-reuse treatment

Retain every existing refinement split verbatim. New candidates have `unassigned_pending_reconciliation` and `public_diagnostic_only` usage. No candidate is assigned to train, dev or test before semantic reconciliation; no pooling or blind/independent held-out claim is justified. A maintainer must resolve full equivalence before assigning a permanent core or treating a proposed family as distinct. The candidates remain `candidate_not_counted` with `dedup_review_required: true`.

| Leaves | Shared assessed reasoning | Consequence |
| --- | --- | --- |
| A1, A2, A3, C4 | finite-vector normalization with nonzero denominator (qcb-core-sp-006) | test_public normalization material must not be copied into a train candidate; A3 and C4 are not independent held-out assessments of A2 |
| A4, B3 | single RY induced operator norm (qcb-core-la-015) | single-gate error and whole-list telescoping are shared, including legacy dev; amended B3 novelty is constrained allocation and integer rounding |
| B2 | global phase becomes relative under control (qcb-core-la-016, qcb-core-be-104) | cross existing test_public/train overlap; generalized target is provisional pending semantic ruling |
| C2, C3, B1, B4 | matrix-product contraction and coordinate conventions (qcb-core-la-002, qcb-core-la-109, qcb-core-la-110, qcb-core-sp-007) | same mechanism does not prove full equivalence, but must be disclosed in split independence claims |
| C3 | Gram recursion semantics and scalar specialization (qcb-core-la-209, qcb-core-la-210) | train cost/norm results partly support proposed public-test kernel question; no independent assessment claim for the shared formula |
| C4 | nonnegative Bernstein weights summing to one (qcb-core-sp-110) | range preservation and error stability share convexity; count only new coefficient-to-normalized-state objective |

Generic Bernstein degree elevation was considered and rejected as a fresh target because SP108 already assesses that mechanism. Exact normalization, exact SVD block success and inactive padded-column gauge are existing targets SP006, plan011 and SP012 respectively. Plan208 remains reserved and must not be bypassed with a new candidate ID.

## Legacy and reserved conflicts

All 26 legacy questions in `data/public/release-v3/release.json` were screened; their exact question inventory and file hash are in the JSON. Existing historical reconciliation reports are snapshot-bound evidence, not current pooling clearance. The only registered complete native/legacy alias remains `qcb-authored-0007` / SP009; it is not rediscovered or counted here.

| Slot | Closest legacy target | Disposition |
| --- | --- | --- |
| A1 | `r-preparecircuit-firstcolumn-normalization` | Exact normalization is a shared subproof; keep the nonnegative loader contract distinct. |
| A2 | `breadth-cubic-unnormalized-operator` | Related normalization boundary; new perturbation-conditioning target. |
| A3 | legacy LCU sum/product error diagnostics | Shared scaled operator-error conventions; new output conditioning/success interface. |
| A4 | `breadth-hermite-angle-budget`, `k-ry-half-angle-convention` | Exact single-gate distance is a shared prerequisite across test/dev. |
| B1 | `qcb-authored-0005`, `qcb-authored-0006` | Contraction and mass mechanisms shared; transfer-action proof is separate. |
| B2 | `qs-global-phase-program-semantics` | High overlap; label-family alignment criterion and error must justify a distinct target. |
| B3 | `breadth-hermite-angle-budget` | Original plan duplicate, superseded before drafting; only new allocation/rounding objective proposed. |
| B4 | `breadth-bell-chronological-wires`, `qcb-authored-0005` | Conventions shared; exact all-width reversal bridge is different. |
| C1 | `breadth-hermite-resource-scope` | Related source context; factorization target differs. |
| C2 | `qcb-authored-0005`, `qcb-authored-0006` | Active-gauge equivalence differs from type and canonical-mass descriptions. |
| C3 | `qcb-authored-0006` | Right-canonical mass identity is a constrained specialization of general Gram semantics. |
| C4 | `breadth-hermite-angle-budget` | Shared accuracy objective; coefficient-to-state conditioning is different. |

The 15 reserved IDs remain untouched. A3 is related to plan203/plan208 vocabulary but assumes a fully specified approximate projected block; it neither fixes the reserved POVM amplification count nor derives a complex amplitude oracle from the reserved magnitude-only premise. No reservation is restored or bypassed.

## Frozen authoring assignments

1. **A:** A1=SP006, A2=normalization stability, A3=approximate block-to-state, A4=LA015. Own the shared normalization-error lemma once; A3 and C4 disclose reuse.
2. **B:** B1=SP007, B2=coherent-family phase alignment, B3=amended precision allocation, B4=TT/public sample index reversal. Preserve the legacy B3 collision and shared telescoping fragment. Independently adjudicate B2 novelty.
3. **C:** C1=SP114, C2=TT active gauge, C3=Gram PSD/boundary/kernel, C4=Bernstein coefficient-to-state accuracy. Reuse A2 explicitly rather than inventing a contradictory normalization bound.

No candidate UUID is allocated by this report. Authors allocate actual UUIDs; the root integration manifest binds those identities to A1–C4. Each leaf later needs complete mathematics, useful partial credit and actual distinct content-bound review. No new Lean run, model baseline, training, container, stable release or global deduplication clearance is part of this plan. Only this report and its machine-readable companion were changed by this worker. No author QA draft has been read by this worker.
