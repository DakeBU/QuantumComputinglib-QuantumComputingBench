# C341: normalized source-error bridge, source-based author-context analysis

No proofs, compilation or new runtime evidence. Not an independent reviewer.
Important retrieval disclosure: one directory rg lacked a Lean-only filter and
matched legacy result/seal/independent-audit JSON snippets; it was truncated.
Those assertions are NOT evidence here. All conclusions below follow from actual
Lean bodies/signatures; exact exposures/pins are in INPUT_MANIFEST.json.
No C338 packet or other new worker review was opened.

## Result: reuse the existing error bridge; first fix the index adapter

The source approximation, norm floor and rational-radius error chain ALREADY
exist. The smallest useful next proof is actual producer -> public-LE Euclidean
vector -> allocatedVector, not another normalization/error lemma.
There is a real adapter hazard: C20 wordValue is LSB-first; TensorTrainWord's
sampleEquiv inserts reverseBasis and is NOT the same map on the same Word.
For symbolic two-bit x=(1,0), wordIndex=1 but sampleEquiv=2. This is a converter
counterexample, not a counterexample to the source/circuit theorem.

## Frozen target and conditioning

Let w=n+1 be physical qubits, N=2^w; original task n_phys>=1 means producer
n=n_phys-1. HermiteStatePreparation.gridPoint w L j is exactly
-pi*L+j*(2*pi*L/N), sampledAmplitude=g_k(p_j), sampleNorm=sqrt(sum g_k^2).
normalizedAmplitude is the SIGNED function value / sampleNorm, cast to Complex;
no amplitude square root, phase quotient or replacement target is allowed.

“Sample zero” must mean coordinate p=0, NOT index j=0.
HermiteIntervalMass.centralIndex n has j=2^n=N/2, gridPoint_central=0 and
smoothInitial_zero k=1. sampled_mass_ge_one and NormalizationStability.
hermite_norm_floor already yield Z>=1 and sampleNorm>=1, uniformly in k,n,L.
At j=0 the coordinate is -pi*L and amplitude is generally not 1.
Producer n=0 still means ONE physical qubit; the zero-qubit grid has no such
uniform central anchor and is outside the frozen physical family.
PiecewiseSourceBudget.piecewise_central/rationalGrid_central/finiteVector_central
give the SAME anchor for rational approximants, even signed/large/zero delta.
finiteVector_norm_floor is unconditional; error theorems require delta>0.
No positivity assumption on every approximate coefficient is needed.

## Existing quantitative chain (no budget change)

A_k=amplificationQ k=(k+1)^2*2^(2*k), C_k=sourceLipschitzConstant k.
FiniteExp bounds use a tail interval when q<=-T and a Taylor interval otherwise;
complete_enclosure supplies membership plus width<=delta for q<=0, delta>0.
The actual exponential input is -p^2, so no positive-q enclosure is assumed.
piecewise_error: for delta>0, each rational-coordinate error <=delta*A_k/2.
finiteVector_error: Euclidean error <=sqrt(N)*delta*A_k/2.
normalization_stability(x,y,hx): normalized error <=2*norm(y-x)/norm(x);
reference norm floor1 removes conditioning loss, not the sqrt(N) accumulation.
Actual sourceDelta=epsilon/(4*N*A_k), NOT epsilon/(4*2^n*A_k).
normalized_source_error therefore gives epsilon/4 (a conservative bound);
C147 sourceDelta_factorization/allocated_sourceDegree_le bind this SAME delta,
not a new truncation or error allocation.

RadiusStability.radiusVector_source(k,n,L:Real) identifies radius pi*L with
the original sourceVector; source_normalize_target identifies its normalization.
normalized_radius_error gives 2*sqrt(N)*C_k*abs(Rhat-pi*L), retaining original L.
GlobalRadiusBudget uses rho=epsilon/(8*N*lipschitzQ k) and
Rhat=allocatedRadius(k,n,L,epsilon)=logRadius(L,rho). RadiusSupplier supplies
actual finite rational Machin sums, positivity and certified pi-error, not a
pi oracle. normalized_allocatedRadius_error is epsilon/4.
PiecewiseSourceBudget.normalized_original_error(k,n,L epsilon:Rat,hL,he)
already yields norm(normalize allocatedVector-targetVector(k,n,(L:Real)))<=epsilon/2.
PiecewiseConsumerChecks.original_amplitude_error_sq gives the actual sum of
Complex.normSq errors <=epsilon^2/4; allocatedVector_unit/nonzero also exist.
These are source declarations, not new compilation/publication credit.

## Representation and implementation cuts that remain

Existing allocatedRadius takes EXACT rational L. This covers that represented
subfamily, not every original positive Real L by an unnoticed cast.
For general L, the existing radius theorem still applies once an actual positive
rational Rhat is supplied with its error to pi*L. If Lhat approximates L,
abs(Rhat-pi*L)<=abs(Rhat-pi*Lhat)+pi*abs(Lhat-L). No current caller certificate
for the original Real-L representation was found in these inspected sources.
Do not invent its precision budget or replace the target by Lhat.

HermiteFiniteNorm.localSampleNorm_eq_sampleNorm concerns the OLD exact-real
rawSourceChain and bond2*k+6, not the new rational piecewise producer.
TensorTrainNormEnvironment.norm_eq_of_contract is the reusable Gram adapter;
new-chain norm and arithmetic bounds must use its ACTUAL chain/bond, not that
old source's 9*(n+1)*(2*k+6)^3 budget.
HermitePolynomialPreparation.exists_polynomial_preparation is ideal real-angle
action/cleanup for that original source; it is not finite QR/angle certification.

For actual scalar rounding y of a=allocatedVector, one still needs an actual
norm(y-a)<=alpha supplier (componentwise rounding costs sqrt(N), not dimension1).
The existing generic computed_nonzero and serialized_output_error /
normalizer_relative_error can then add 2*alpha + eta/(1-eta) + zeta to the
existing epsilon/2, with their stated smallness/domain premises supplied.
This is a residual CONDITION, not a newly authorized allocation of epsilon/2.
Finite QR/isometry/absorption must bound its actual vector/operator defect;
angle selection/synthesis must separately connect actual angles to that QR map.
SavedRounding.midpoint_error/outward_mem, SavedRyInterval.lifted_vector_error
and NominalStageTransport.actual_apply_error are local/serialized primitives,
not suppliers for this producer's missing QR/angle witnesses. No finite example
or partial scalar ledger proves these family-level premises.

## Three smallest interfaces to seal next (suggestions only)

1. wordIndex_public_LE: forall n,x:Word(n+1), wordIndex n x =
   primitiveBasisLEEquiv(n+1)(toBasis x). Dependencies: C20 recurrence,
   TensorTrainWord basisEquiv/toBasis and primitiveBasisLEEquiv_succ_value.
2. With eLE=(basisEquiv w).trans(primitiveBasisLEEquiv w), define a SPECIFICATION
   vector from contract(denoteChain(produceExplicitStored...)) at eLE.symm j.
   Prove it equals finiteVector for R>0, using produceExplicitStored_source
   and interface1. The vector is not an executable dense-table construction.
3. Specialize interface2 at existing allocatedRadius/sourceDelta and obtain
   the SAME epsilon/2 original-amplitude Euclidean statement for rational L,
   using allocatedRadius_positive and normalized_original_error. This is only
   the existing represented-input boundary, not the full arbitrary-Real-L root.

Literal import/API signatures and read extents are in the manifest. No model,
hypothesis, old budget or source file changed. Freeze and STOP.
