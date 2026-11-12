# C257: operand-bit frontier for the actual rational QData producer

Classification: INTERNAL SOURCE-ONLY MATHEMATICAL FRONTIER / PROPOSED BIT-GROWTH INTERFACES. No Lean proof, compiler result, CPU/GCD bound or scientific-root certificate is supplied. The subject is the exact C248 `produceExplicitQData`, including its actual C23/C150 prefix and regenerated intermediates, not an alternative coefficient formula evaluated by a free callback.

## 1. Exact size model and proposed bound

For a natural a define `b(a)=Nat.size a`, equivalently the least t with `a<2^t`; b(0)=0 and b(1)=1. For signed integer z use b(|z|). For the canonical Rat fields p=x.num, q=x.den>0, define

```text
h(x) = max(1, b(|p|), b(q)).
```

The abstract canonical signed-numerator/positive-denominator pair encoding uses `1+b(|p|)+b(q)` payload bits, at most `2*h(x)+1`; container framing is not included. Inputs are already canonical Rat values, or validated encodings of them. Parsing/reducing a different unreduced input representation is a separate cost. Set `H_R=h(R)`, `H_delta=h(delta)` (or supplied upper bounds on them), and define

```text
W = n+1
T = tailCutoff delta
d = 4*T^2+2*T+1 = sourceDegree delta
m = 2*k+1
L = d+m
f(s) = (s+1)*b(s+1)                       -- s! < 2^f(s), including s=0
V = 3*k+2*b(k+1)+3
A = f(d)+f(k)+T+1

B_data = max(A+V, 1+L*(H_R+n+1))
B_work = 8+H_delta+2*H_R+W+T+2*f(L)+V+L*(H_R+n+1).
```

Proposed conclusions, to be statement-sealed and proved, are:

1. Every rational in the ACTUAL returned QData has h<=B_data.
2. Every canonical rational operand/result at the enumerated rational primitive sites in the ACTUAL QData computation, including its prefix, has h<=B_work.
3. Each standard unreduced per-primitive witness below, including its separate cross-products, has integer bit length <=`2*B_work+1`.

These are operand-size bounds, NOT operation-count or time budgets. The displayed constants are conservative arithmetic margins from the derivation, not an accepted or empirically fitted budget. The sharper B_data and denominator invariants are preferable interfaces; B_work is a convenient single envelope, not a minimality claim.

Since `T<=H_delta`, `L<=4*H_delta^2+2*H_delta+2*k+2`. Thus the proposed peak width has order

```text
O((k+H_delta^2+1)*(H_R+n+log(k+H_delta+2)) + H_delta).
```

Polynomial means in physical width n+1, order k and encoded rational heights, NOT in log(n+1) or log(k+1). The construction already writes linearly many physical stages/order-dependent data. A pure polynomial envelope follows also by b(s+1)<=s+1, if logarithms are inconvenient in a later Lean statement.

The leading terms are not merely artifacts of generic tick bounds. The actual new factorial pass materializes L!, whose bit length has order L*log L. For R=1/q with odd q>=3, a stage-0 bit-1 translation from monomial 0 to r has value `1/(q*2^n)^r`. Choosing the deterministic comparator destinations makes a corresponding same-component stored kernel entry nonzero. Its denominator already needs order r*(n+log q) bits. Here r=max(d,m) and L=d+m<=2r. These are symbolic families, not executed diagnostics or minimality certificates, but explain why removing both leading terms would be implausible.

## 2. Canonical versus unreduced arithmetic

For canonical operands x=p/q, y=r/s (q,s>0), the per-site raw witnesses are

```text
add/sub: numerator p*s +/- r*q, denominator q*s;
         also retain separate products p*s and r*q;
mul:     numerator p*r, denominator q*s;
div:     numerator p*s, signed denominator q*r.
```

If y=0, division's raw denominator is zero and the source's total Rat division returns canonical 0; this branch is explicitly retained. If both operand heights are <=B, products have bit length <=2B and the add/sub numerator <=2B+1. A normalized result is not fed into the next primitive as this unreduced pair: Rat's actual fields are canonical at each primitive boundary. A divisor-zero witness is not a valid nonzero common-denominator representation; the canonical-zero case must be separated.

The inspected actual Mathlib APIs include `Rat.pos`, `mk'_num_den`, `mul_eq_mkRat`, `pow_eq_mkRat`, `div_def'`, `num_den_mk`, `add_num_den`, `add_den_dvd_lcm`, `sub_den_dvd_lcm`, `mul_den_dvd`, and `mul_num/mul_den` with their normalization GCD. These support this exact semantic witness model and denominator divisibility. They do NOT certify the selected compiler's/native arithmetic's complete temporary-object trace, big-integer multiplication scratch, GCD implementation, allocation or time. The proposed raw-witness bound concerns the unreduced mathematical operands/products of each actual rational primitive call; a native-temporary refinement remains a separate dependency.

The essential common-denominator lemma is: if each canonical x_i has denominator dividing a fixed positive Q, every normalized partial sum also has denominator dividing Q (use lcm, not repeated denominator multiplication). If its absolute value is <=M, its canonical numerator is <=M*Q. This controls the next operation's actual operands. A generic recurrence `height_next <= 2*height_previous+1` would discard this structure and falsely suggest an exponential upper bound; an operation count alone cannot recover it.

## 3. Cutoff and setup, including signed/zero inputs

Write delta=a/c in canonical form. If delta<=0, natural ceil(1/delta)=0 and T=0, including total 1/0=0. If delta>0, a>=1 and ceil(c/a)<=c. Therefore `max 1 (Nat.ceil (1/delta))<=c<2^H_delta`, and the actual base-2 ceiling logarithm gives `T<=H_delta`. Large positive delta>=1 also has T=0. No positivity assumption is required for this bit statement. Real-exp/error meaning for nonpositive delta is NOT inferred.

The actual `Nat.clog` implementation was inspected, not replaced by an oracle: its helper squares a base only while base<N, then stops when N<=base, for fixed N=max(1,ceil(1/delta)). A recursively generated base is then <N^2 (apart from the initial base 2); its bit size is bounded by about 2*H_delta, not 2^H_delta. The numeric fuel N is not evidence of N mandatory executed iterations: the stopping branch matters. This is a useful containment observation, not a CPU proof for clog.

Both actual cutoff computations produce this same T: one in rightSetup and one regenerated in C248. The degree formula and L are polynomial in T,k. All four factorial passes (cache at m, setup at d, middle at m, new table at L) have degree <=L.

Grid step generation actually computes 2^W by a multiplication recurrence, then 2R, then divides. Canonically

```text
sigma = 2R/2^W = R/2^n,
sigma.den divides R.den*2^n,
h(sigma) <= H_R+n+1.
```

The numerator 2R and dyadic denominator 2^W themselves have heights <=H_R+1 and W+1. The regenerated minusR/minusStep are exact negations via qSub, not new large scalars. R may have either sign or be zero.

For every cut, s is one of -1,0,-T,T. The actual qAdd forms s+R before qDiv by sigma. If R=0 the division is 0 and source strict/inclusive raw rules are retained (strict cut 0, inclusive cut 1). If R=p/q!=0, the cut quotient has the exact representation

```text
(s+R)/sigma = ((p+s*q)*2^n)/p.
```

Hence its canonical height is <=`H_R+n+b(T+2)+1`; its pre-division canonical numerator operand is controlled by `|p+s*q| <= |p|+(T+1)*q`. The unreduced division products may have the larger sum of the two operand heights; they are covered by the raw bound, not erased by the later cancellation of q. Integer floor/ceil and the pre-min floor-plus-one result have at most a further constant bit margin. The STORED cuts lie in [0,2^W], with bit length <=W+1. Negative R can reverse the physical grid interpretation, but causes no failure of these absolute-size bounds. Only the source-value interpretation retains R>0.

clippedRun builds 2^T, 1/2^T, then 1/2^(T+1), with final height T+2. At T<=1, actual midpointFrom returns that clipped scalar and does NOT evaluate an active exponential or a radius expression. At T>1 it computes the finite sum `sum_(i=0..d) (-1)^i/i!` with the supplied factorial table. The original finite-exp bounds at -1 have this same midpoint because their two radius terms cancel; those radii are NOT evaluated by this producer, so their hypothetical bit sizes must not be charged or used as an actual witness here.

For active midpoint, all term and suffix-sum denominators divide d!. Every suffix's absolute value is <=3: a finite bound follows from `i!>=2^(i-1)` for i>=1 and the finite geometric sum, without analytic exp/f64 assumptions. In either branch |midpoint|<=3, with denominator dividing

```text
E = if T<=1 then 2^(T+1) else d!.
```

For a uniform right-boundary denominator later use `2^(T+1)*d!`, since clipped is still returned even in the active branch. T=0 gives d=1 and clipped=midpoint=1/2; T=1 likewise takes the clipped branch. No fictitious d=0 endpoint is substituted.

## 4. Factorials, actual source sums and signed middle

`factorials N` starts from integer 1, multiplies the last value by the integer next, increments next by 1, and copies existing rationals. All canonical denominators are 1; entries are i!, and next is N+1. As `N<=L`, every factorial is <2^f(L). A chooseFrom call first multiplies r! and (u-r)!, then divides u! by that product, with 0<=r<=u<=L. Even the crude intermediate bound `(L!)^2` has height <=2*f(L). The result is an INTEGER binomial, denominator 1, with value <=2^u. These facts must be supplied from actual generated factorials, not an arbitrary table-correctness premise on the public producer.

For source index i<=k, the actual cache sums

```text
a_i = sum_(r=0..i) choose(k+i-r,k)/r!.
```

The term's denominator divides r!, hence k!, and its magnitude is <=2^(2k). Every actually evaluated suffix sum is nonnegative, denominator divides k!, and magnitude <=`S=(k+1)*2^(2k)`. The scalar work before normalization inside chooseFrom can involve factorial products; its normalized integer result and the subsequent division by r! must both be traced, not replaced by an uncosted mathematical binomial lookup. Each addition of canonical suffix/term operands has raw denominator at most `(k!)^2`, but the normalized result returns to a divisor of k!, not a new product denominator that gets squared at every recursion depth.

weightedSources uses actual midpoint e and actual a_i, multiplying by the powers (-1)^(k+1) or (-1)^i, which remain +/-1 at every recurrence step. Its first vector has denominator dividing E*k! and magnitude <=3S; its second divides k! and has magnitude <=S. No pair of values is one scalar word in the bit model.

For middleFirstTerm retain BOTH guards `k+1<=j` and `j-(k+1)<=i`. For middleSecondTerm retain BOTH `i<=j` and `j-i<=k+1`. Only legal branches call chooseFrom. Illegal branches are canonical zero, not factorial quotients at truncated/out-of-range indices. Legal first binomials are <=2^k; legal second binomials <=2^(k+1). Therefore every weighted term and actual partial sum, and the final sum of the two middle sums, has denominator dividing E*k! and absolute value <=

```text
M = 5*(k+1)^2*2^(3k) < 2^V.
```

The factor 5 comes from `(k+1)*(3S*2^k + S*2^(k+1))`. This deliberately allows arbitrary signed partial sums; no false positivity assumption on middle coefficients is used. Since E divides `2^(T+1)*d!`, every such canonical numerator is <2^(A+V). This supplies the first part of B_data and a uniform bound for the middle arithmetic. The same denominator argument handles the final addition of the two sums, not just their mathematical final coefficient. At k=0 the source cache is (1) and the middle vector (1,1-e), consistent with the bounds; this is symbolic boundary analysis, not an executed diagnostic.

## 5. Actual translations, left powers and all right rows

At q<=n the positive stage weight is

```text
w = sigma*2^q*bit = R*bit/2^(n-q),
D_R = R.den*2^n.
```

Its canonical numerator has absolute value <=|R.num| and denominator divides D_R. The reflected weight is -w with the same size. The separate dyadic intermediate 2^q is an integer of height q+1; scaled weight and selected bit value are still actual operands before subsequent multiplication.

For source monomial i and destination j in one component, the legal translation is `choose(j,i)*w^(j-i)`; illegal i>j gives zero. The actual powQ recurrence multiplies by a FIXED base with exponent at most L, so its prefixes have linearly growing exponent/height, not a repeated-squaring exponent tower. A legal final translation numerator is bounded by `2^L*max(1,|R.num|^L)` and denominator divides `D_R^L`; its height is <=`1+L*(H_R+n+1)`. Diagonal exponent zero, bit=0, R=0 and degree-zero components all retain canonical 1 where required. Comparison multipliers are 0/1; the nested multiplications neither enlarge the normalized nonzero scalar nor remove their actual primitive sites. Different components return 0. All same/cross and reflected-sign cases are therefore included, not only active physical paths.

Left entries are `[a=1]*([b=1]*origin^j)`, with origins 0,-R,-R,0,R and j<=L. Their power prefixes have height <=`1+L*H_R`; multiplication by masks preserves the result bound, including 0^0=1. n=0 simply has q=0, w=R*bit and one stored physical table, not an empty-chain special case.

The five ACTUAL old rightEntry branches used by C248 are:

| branch | coefficient read/projected | flips |
|---|---|---|
| 1 | pure clipped | false,false |
| 2 | actual tail coefficient read 1/j! | false,true |
| 3 | actual returned middle coefficient read | true,false |
| 4 | pure clipped | true,true |
| 5 | actual tail coefficient read 1/j! | true,false |

Empty/full/interior accept dispatch always returns 0 or 1, and a flipped accept uses exact 1-base. Both nested right products have no larger normalized height than their coefficient. Tail coefficient denominators divide d!, clipped divides 2^(T+1), and middle divides E*k!. Thus every right denominator divides

```text
Q_right = 2^(T+1)*d!*k! < 2^A.
```

Together with the magnitude bounds above, every right height is <=A+V. All five rows, signs, zero masks and total-division branches are retained. A single OPTIONAL proof denominator for all returned QData is

```text
Q_all = Q_right * D_R^L.
```

It is a mathematical divisibility witness, not an extra integer the producer computes or a new cache whose cost is assumed zero. The max-form B_data is sharper than bounding every numerator via this universal product denominator.

All four factorial passes, all source/middle suffixes, setup quotients/dyadics and all translation/left power prefixes fit B_work using f(d),f(k)<=f(L) and the margins above. Hence the per-primitive raw bounds follow from canonical operand bounds, NOT from the old scalar tick total. There is no genuinely explosive unbounded squaring feedback in this rational producer: factorial numeric values are huge but have polynomial bit length; powers have bounded degree; sums retain fixed common denominators. The source clog helper's guarded squaring was separately checked above. Native implementation behavior remains a different question.

## 6. Proposed exact interfaces and missing proof cuts

No Lean source/proof search is started here. Before proof authoring, seal the exact definitions of h, raw-witness size, and any call-site relation, then seal statements tied to the exact C248/C23/C150 source hashes. Useful interfaces, in dependency order, are:

1. **Canonical representation / raw arithmetic.** For positive Q, `x.den divides Q` and `|x|<=M` imply `|x.num|<=M*Q`. A shared-denominator sum lemma covers EVERY suffix evaluated by actual sumEntries. Raw add/sub/mul/div witness widths are <=h(x)+h(y)+1, with division-by-zero separated. Use actual Rat fields, not a replacement rational representation.
2. **Cutoff/setup heights.** For all signed Rat delta, actual cutoffQ returns T<=h(delta); both actual cutoff results agree. Bound actual gridStepRun intermediates, cut numerators/quotients/pre-min floors, clipped and the actual T<=1/active midpoint dispatch. No public R>0/delta>0 premise is needed for size alone.
3. **Generated factorial / choose operands.** For each actual factorial pass N<=L, bound entries, next, multiplication operands and actual chooseFrom temporary denominator. Supply factorial correctness internally from the actual producer; do not add it as a public oracle.
4. **Source and middle partials.** For actual produceSourceCache, prove all source terms/suffixes share k! and magnitude <=S. For actual middleFromCache on actual cache/midpoint, prove both weights, guarded terms, both partial sums and their final addition share E*k! and magnitude <=M. A lemma only about the final middle vector is insufficient for intermediate-bit credit.
5. **Actual local tables/boundaries.** Bind powQ prefixes, legal/illegal translation branches, both signs, all masks and five right rows to the source call operands. Then every entry of actual `produceExplicitQData(...).run.value` satisfies B_data.
6. **Whole arithmetic-site frontier.** A structural finite `Sites`/trace specification must enumerate actual primitive INVOCATIONS and their actual canonical arguments throughout the four factorial passes, cache/setup/middle and materialization, without executing a second desired-output producer or assuming a cost/height callback. It can be a proof-only observation relation or instrumented refinement, but must be defined and sealed first. Prove all such canonical operands/results <=B_work, then all per-site unreduced witnesses <=2*B_work+1. This relation does not yet exist as an admitted interface in this packet; this is the precise remaining formal coverage cut.

Generic lemmas may take an explicit common-denominator invariant, but the public QData root must discharge it from the actual prefix, not expose a free `correct cache`, `small intermediate`, native-GCD or cost assumption. Existing raw value theorem interfaces are available dependencies; none was rerun or freshly accepted in this stage. This is a concrete bound design awaiting statement seal/proofs, not an assertion that the above site-coverage theorem already exists.

## 7. Storage consequence, allocated precision and excluded claims

The actual rational output contains `N_Q=2*(n+1)*D^2+2*D` scalar positions, where `D=assemblySize k delta<=18*(L+2)`. Thus its canonical pair payload is PROPOSED to be at most `N_Q*(2*B_data+1)` bits, plus container/address encoding. Dense zero entries are still positions; no sparse storage or physical pointer sharing is assumed. Temporary object count, persistent-vector copies, stack/evaluator retention and garbage collection are not bounded by that output-payload expression.

There is one useful allocated-precision dependency, not a changed tolerance: from the ORIGINAL

```text
sourceDelta k n epsilon = epsilon/(4*2^(n+1)*(k+1)^2*2^(2*k)),
```

canonical input epsilon of height H_epsilon gives the proposed elementary bound

```text
h(sourceDelta k n epsilon) <= H_epsilon+n+2*k+3+2*b(k+1).
```

This follows by writing one unreduced numerator/denominator for that actual quotient, not by assuming precision allocation is free. R remains an explicit canonical rational input with height H_R. Substituting an allocated radius needs its OWN actual-body height/encoding theorem. No exact finite encoding of pi, an unspecified L, a real radius or a desired rounding is silently assumed. Original source/state error allocations remain unchanged; this packet supplies no approximation, normalization or error-budget result.

Even after the height statements are proved, every Rat primitive can repeatedly perform normalization/GCD. Neither that work nor integer quotient, ceiling/logarithm, comparison, native big-int scratch or allocation becomes unit-time. A bit-runtime theorem would additionally need a verified implementation/refinement with bit operation bounds for multiplication/division/GCD/comparison and full call/control/container counts. Only THEN could one combine those dependencies, with all hypotheses explicit. This packet deliberately stops before rational-to-real castData, real ofTable, QR/canonicalization, synthesis, gates, phase/cleanup/export and SP/BE scientific ROOT. Those layers cannot inherit a CPU or quantum-resource certificate from QData operand sizes.

## 8. Exposure and handoff

Exact input: C248 source SHA256 `bbdca858e3254f47f65a9dfc2752ded85a8afa48409c41d004c0c1848fe4ed7f`. C245/C247/C251 remain immutable. Prior Hermite source/runtime and Gaussian/governance exposure is retained; this is not a universal decoder. No C252/C253 author proof/results or new runtime packet was opened. The C248 source's old proposed scalar budget is visible from prior authorized source reading but is not evidence for this derivation. Current HARNESS/linked policy and source hashes are bound in the manifest.

Objective/frontier delta: replace the absent bit-growth argument by explicit common-denominator, partial-sum and per-primitive operand bounds with exact proposed formulas. Named evidence: raw source/API bodies and mathematical derivation only, no new Lean/CPU/finite receipt. Assumptions: canonical input encoding model; all signed/zero Rat branches retained; internal generated factorial/cache facts remain proof dependencies. Files changed: only this new three-file frontier packet. Reusable insight: normalized suffix denominators divide fixed factorial products, while each raw operation can temporarily square that denominator bound; the two size layers must not be confused. Failure class: no explosive rational recurrence identified; formal site coverage and native implementation refinement remain OPEN, not refuted mathematics. Salvage: previous packets unchanged, no discarded proof route. Process memory: retained required protocols/own source reviews; no new numerical review used. Direction fingerprint: actual operand algebra rather than tick-count-to-bit inference; no delegation. Default next action: parent check formulas and exact input bytes, define/seal the smallest source-site and denominator interfaces, then authorize proof. Purification/Exposition/ROOT: none. Residual risk: unproved bound applications/site coverage and absent native temporary/runtime model. No compiler, Python, scripts, lake, Git, network, subagent, finite diagnostic or new Lean proof search was used. STOP before author/runtime comparison.
