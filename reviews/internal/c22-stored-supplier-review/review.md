# C22 stored supplier: independent internal review

Verdict: **ACCEPT_INTERNAL_LOCAL_SEMANTICS_AND_PARTIAL_LEDGER**. No mismatched rational cast, reindexing, finite-window refinement, or returned-object linkage was found. Reject any reading of this packet as a full scalar-runtime, finite-bit, normalized preparation, physical-circuit, source-blind publication, or main-admission certificate.

Direction fingerprint: `C22_INDEPENDENT_SAME_OBJECT_AND_COST_BOUNDARY`.
Expected information gain: falsify cast/refinement drift or hidden scalar-resource overclaim.

## Scope, independence and evidence

This review started with the frozen original task `tasks/SP-HERMITE-POLY-002.md`, then c21 `ActualCoefficients.lean` and `ActualAssembly.lean`, then the four C22 Lean sources. Required AGENTS/HARNESS, worker/master skills, and publication/digestion/evidence-memory protocols were read. The C22 author result/handoff and parent verdict were not opened to determine a conclusion. A later broad lexical dependency search incidentally displayed some C22 and earlier-stage result metadata; it was not used as evidence for this verdict. This is an internal provider/checkpoint audit, not an independent encoder-denoiser/publication review.

An ordinary independent consumer `IndependentConsumer.lean` compiled in `consumer-v2.log` with exit 0, all selected inputs stable before/after, and seven named symbolic theorems reporting only `[propext, Classical.choice, Quot.sound]`. The finite examples use `native_decide` and are supporting screenings, not the arbitrary-width proof. The source/cache/toolchain/manifest bindings and replay timestamps are in `consumer-v2.json`. It records branch `work/lean433-curriculum-20261008` and observed HEAD `91da307279b96fc4124bf80aafda1679ac8a769b`; the parent's concurrent Git checkpoints are not review-owned edits. Existing caches were read only. The parent separately replays focused source compilation; this consumer is not a complete transitive-cache or repository-build gate.

Retained test failure: `consumer-v1.log`/`.json` record exit 1, unchanged inputs. Kernel `decide` became stuck on imported logarithm/floor/ceiling expressions. This is `IMPLEMENTATION_FAILED` in the review test, not a mathematical refutation. Its exact original bytes are retained as `consumer-v1-source.txt`. The test author's incorrect degree-two signed-coefficient expectation was also corrected from -1/4 to -4 before the successful run. No production/C22 source was repaired or reinterpreted.

An initial read attempted c21 `ActualDecomposition.lean` and failed because that file belongs to `piecewise-kernel-producer`; the corrected dependency was read. This file-location failure supplies no negative mathematics.

## Reconstructed source and binder boundary

Let `width=n+1`, `j=wordValue x`, `p=-R+2*R*j/2^width`, `T=tailCutoff delta`, `d=sourceDegree delta=4*T^2+2*T+1`, and `c=2^(-T)/2`. The full finite rational source is

- `negativeMidpoint p delta` if `p < -1`;
- `middleValueQ k delta p` if `-1 ≤ p ≤ 0`;
- `negativeMidpoint (-p) delta` if `0 < p`.

Each negative midpoint is `c` for its argument `≤ -T`, otherwise the signed Taylor polynomial of degree `d`. The middle polynomial uses the source's exact rational coefficient formula, with its exp(-1) coefficient replaced by the finite enclosure midpoint. It is not an absolute-value or square-root amplitude map.

The generic exact-source theorem takes `hR : 0 < R` only. It assumes neither a caller-provided kernel Window nor cast/refinement/source-equality nor a resource premise. `n,k,R,delta,x` are typing/input data; `hR` is the necessary positive-grid convention. Equality still holds for arbitrary rational delta: scalar-error guarantees are a different positive-tolerance theorem. The allocated consumer assumes `0<L` and `0<epsilon`; it derives positive allocated R internally and uses actual `sourceDelta`, not an arbitrary postulated allocation.

C22's equality is to the literal **finite rational piecewise source**, not to the original exact Hermite/exponential vector. Normalization, radius/source error and the frozen original target remain distinct inherited prerequisites; C22 does not return a quantum circuit.

## Whole-word semantics and boundary ownership

The assembly is the sum of five disjoint, source-owned components:

| component | active mask | value |
| --- | --- | --- |
| left clipped | `p<-1` and `p≤-T` | `c` |
| left active | `p<-1` and `p>-T` | Taylor polynomial at p |
| middle | `p≥-1` and `p≤0` | signed middle polynomial |
| right clipped | `p>0` and `p≥T` | `c` |
| right active | `p>0` and `p<T` | Taylor polynomial at -p |

Strict and inclusive cuts are not exchanged. A's cut is strict at -1, B's is inclusive at 0, C's is inclusive at -T, and D is the complement of a strict cut at +T. `acceptQ` overrides comparison-state readout for cuts 0 and 2^width, so truncating cuts to the physical grid does not wrap the all-zero/all-one masks.

At T=0 both active-tail regions are empty, but clipped tails remain nonzero (`c=1/2`). At T=1 the left-active interval is empty while the right-active interval `(0,1)` can contain grid points. Source ownership at -1 and 0 stays middle; +T is right clipped only if positive; -T is left clipped only if strictly below -1. The symbolic consumer proves these owners without imposing `T≥2`. Finite tests certify T0/T1, d=1/7, nonzero clipped values, strict/inclusive cut disagreement at exact grid points and cut 0/N acceptance.

`wordValue` recursively gives the first bit weight 1 and higher bits weight 2, while polynomial kernels use `step*2^q`. The q0-LSB convention therefore survives chronological storage; independent word examples distinguish `(1,0)` from `(0,1)`.

`BlockQ.prod_cast` and `.sum_cast` preserve actual kernels and both boundaries, not merely values on selected samples. Polynomial casting preserves rational powers and all signed coefficients. `actualBlocksQ_cast` consequently identifies the complete five-component block. `fullEquiv.symm` is used consistently for entries and both boundaries. `finProdFinEquiv.symm` encodes the physical bit/bond column with the exact inverse used by stored denotation; no semantic flattening reversal was found.

## Same returned object

`produceQData` materializes all local entries, rows, cores and two boundaries from one captured rational block expression. `castData` reads and collects those very vectors. `produceData_window` supplies the finite kernel Window internally; `produceData_left/right` link both generated boundaries. `produceStored` then passes exactly those generated tables and boundaries to `StoredMatrixProductChain.ofTable`.

`produceStored_refines` is equality of the complete denoted returned chain to c21 `actualChain`; it is stronger than isolated finite contractions. The source, max-bond and final-local-scalar envelopes transport through that equality. The independent `same_returned_source_and_partial_cost` combines this very Run's exact source and cost without extra hypotheses. No producer-existence witness or unrelated cheap cost Run is substituted.

The local supplier has `(n+1)` cores of shape `D × 2D`, plus boundaries, where `D=18*(d+1)+9*(2*k+2)+18`. It does not enumerate 2^width amplitudes. Local tables are dense in D, which must not be confused with a dense physical-state vector. `storedScalars` counts final local scalar addresses; it is not bit size, peak RAM, caching verification, or classical work.

## Actual cost boundary

Let `P=(n+1)*(2*D^2+D+1)+2*D`. The exact ledger says

- rational materialization: `P*(2 read + 2 write)`;
- rational-to-real stored cast/copies: `P*(3 read + 2 write)`;
- their composition: `5P` reads, `4P` writes, total `9P`;
- same-returned stored assembly: total at most `9P+20D^2+30D+5n^2+7n+31`.

This genuinely counts collection containers and stored-data reads/copies, plus assembly boundary contractions. Canonical assembly's terminal and initial entry loops charge read, multiply and add primitives; tail-vector reference copies and chain nodes are also represented. It is not merely an output-size inequality.

However, rational scalar evaluation occurs inside `pure`: comparison transitions, cut computation, floor/ceil/logarithm, choose/factorial, powers/divisions, middle/source coefficient sums, clipped value, grid step and source parameter production are not charged. Construction of `actualBlocksQ`/`fullEquiv`, evaluation/loop-index/bond-address arithmetic, and rational-to-real conversion are not finite-bit primitives here. The independent consumer proves that generation charges exactly zero `.field` and `.compare` operations despite these expressions. This decisively rules out equating the ledger with complete scalar runtime; it does not refute the explicitly partial C22 theorem.

Capturing `b` and `e` once is a lexical fact, not proof of compiled-machine caching, memoization or peak RAM. Rational numerators/denominators can grow, and all such bit costs remain open. No quantum gates, finite-precision synthesis, readout, normalized-state preparation or coherent access are certified by these traffic bounds.

## Recommendation and next prerequisite

Keep the C22 checkpoint classified as an internal exact-source stored supplier with a partial counted ledger, conditional on the parent's fresh focused replay matching these source hashes. Do not promote it to PROOF_SEALED/PUBLISHED/main or a completed polynomial classical compiler claim.

The next substantive prerequisite is an actual charged rational/setup producer with stored intermediate contracts and a refinement theorem to `produceQData`/`actualBlocksQ`, preserving the complete masks/signs/q0 order. Charge sourceDelta/allocatedRadius, coefficients, factorials/choose, powers, cuts and repeated scalar work; prove a uniform bound with explicit input representation and integer/rational bit-length dependence. A separate integration consumer must then transport the stored finite source through normalization/error and the actual stored compiler. Full source-blind publication and repository/reader gates remain required before admission.

Failure class of final scoped semantic review: NONE. Salvage: exact same-returned consumer and symbolic ownership/zero-charge boundary facts retained locally; finite screenings remain supporting evidence. No process-memory mathematical verdict was imported. Common-blind-spot comparison of competing complete constructions is outside this one-provider review. Purification/Exposition Seal: not claimed. All review-owned writes are limited to this new review directory; no production/configuration/C22 frozen evidence or shared cache changes and no Git writes were made.
