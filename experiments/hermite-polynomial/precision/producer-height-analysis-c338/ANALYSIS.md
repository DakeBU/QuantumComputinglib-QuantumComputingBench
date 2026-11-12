# C338 — actual producer height, source-only author analysis

Status: mathematical derivation / interface proposal, NOT a Lean proof, typecheck,
independent review, runtime result or scientific ROOT certificate. The numerical
producer, targets, hypotheses and counters are unchanged. C331 remains frozen.
This continues the author's prior Hermite work; it claims no fresh source-blindness.

## 1. Fixed parameters and actual call graph

Use C269's literal `height`, `integerBits`, canonical `Rat.num`/`Rat.den`:
`height q = max 1 (max (Nat.size q.num.natAbs) (Nat.size q.den))`.
Signs are separate encoding bits; `height 0 = height 1 = 1` and
`height (2^a : ℚ) = a+1`. A height cap B means STRICT magnitudes `< 2^B`.
Let

```
N = n+1                         (physical width, never n)
A = height R; B = height delta  (both >=1, arbitrary signed rational inputs)
T = tailCutoff delta; d = 4*T^2+2*T+1; m = 2*k+1
L = d+m; D = 18*d+18*k+54
f(t) = 1+t*Nat.size(t+1)        (a safe bits cap on t!)
```

C248 `produceExplicitQData` actually calls C23 `produceSourceCache k`, C150
`rightSetup`, `middleFromCache` on that returned cache and midpoint, then a second
`cutoffQ`, a second `gridStepRun N R`, two negations, `factorials L`, and
`materializePrepared`. Factorial passes have maxima m, d, m, L, respectively;
they are NOT a freely reused table. C150 `powQ` multiplies once per exponent
successor, NOT repeated squaring. The source-side `middleExpr`, Nat.choose formula
and old `actualBlocksQ` callbacks are specifications, not C248 numerical calls.
The one source-cache bind is not a theorem of physical one-evaluation/sharing.

## 2. Exhaustive rational-site inventory at this source granularity

Every row includes read/copied values, constants, and zero branches. “Raw” below
means the C269 mathematical `rawIntegers` at each actual scalar operation, NOT
all scratch integers of the native Rat implementation.

| Actual definitions/sites | Canonical rational intermediates that must be covered |
| --- | --- |
| C23 `factorials`, `extend` (31,21) | each next counter as a Rat integer, last factorial, product forming the next factorial, next+1, all copied factorial entries |
| C23 `chooseFrom` (63) | top=n!, first=r!, second=(n-r)!, their denominator product, quotient; guards always supply 0<=r<=n<=table bound |
| C23 `sourceEntry` / `sumEntries` (94,79) | each choose quotient divided by r!, EVERY recursive tail sum, including empty tail 0, not just final a_i |
| C150 `cutoffQ`, `gridStepRun`, strict/inclusive cuts (24–47) | 1/delta, every 2-power prefix, 2R, step, s+R, (s+R)/step for s=-1,0,-T,T; also actual qSub producing -T |
| C150 `clippedRun`, `midpointFrom`, `rightSetup` (49–95) | 2^t prefixes, 1/2^T then /2; reciprocals of actual i!; every (-1)^j prefix, signed reciprocal-factorial term, and every active midpoint tail sum. T<=1 returns clipped; no active midpoint sum is evaluated in that branch |
| C150 `weightedSources`, guarded middle terms, `middleFromCache` (39–88) | sigma, cache reads, e*a_i BEFORE sign, signed first/second vectors; each legal chooseFrom intermediate; each weighted product; EVERY first/second tail sum and their final addition. Failed guards return 0; do not divide an out-of-range factorial |
| C248 `translationQ`, kernel, left (83–162) | actual chooseFrom intermediates; 2^q prefixes; step*2^q BEFORE multiplying bit; w; every w^ell prefix; binomial*power; both nested mask multiplications. Left computes each origin^ell BEFORE masks (including 0^0=1), then two mask products. Cross-component kernel is 0 |
| C150 right / C248 wrapped right (99–136 / 166–174) | all 0/1 masks and 1-base flips, selected clipped/tail/middle coefficient, second*coefficient BEFORE first*inner. Decode/collect/bind/casts do not introduce another rational arithmetic supplier |

`qAdd/qSub/qMul/qDiv` retain both input canonical fields for the local raw-pair
bound, even if a mask subsequently kills the result. Constants -1,0,1,2 and
natural-to-Rat casts of T and factorial next values are included. Run/index/cost
metadata are natural integers, addressed in section 5, not omitted rational sites.

## 3. Structured invariants, not operation-count exponentiation

These are derivations to formalize, not accepted theorems. The elementary bound
`t! <= (t+1)^t` gives `Nat.size(t!) <= f(t)`, including t=0. All factorial
values/next fields are bounded by f(L); chooseFrom's product has bits at most
2*f(L), and its result is an integer <=2^L. No factorial has bit size O(t!) here.

**Actual C23 suffixes.** For 0<=i<=k and 0<=s<=i+1 put

```
S(k,i,s) = sum_{s<=r<i+1} choose(k+i-r,k) / r!
Q_A = k!; M_A = (k+1)*2^(2*k)
H_A = f(k)+2*k+Nat.size(k+1)+1.
```

Each summand is nonnegative, <=2^(2k), and has canonical denominator dividing
r!, which divides k!. Consequently EVERY suffix S has denominator dividing Q_A,
`0 <= S <= (i+1-s)*2^(2k) <= M_A`. At s=0 this is the actual returned cache
entry by `sourceEntry_value` / `produceSourceCache_entry`; recursion of
`sumEntries` drops its first argument each step, so its internal accumulators are
these suffixes, not forward prefixes. C269's common-denominator bridge gives
height <=H_A. This avoids multiplying all denominators across O(k) additions.

**Actual midpoint and middle.** Define positive proof witnesses (not tables
built by the producer)

```
Q_E = 2^(T+1)*d!; Q_M = Q_E*k!
M_M = (d+1)*(k+1)^2*2^(3*k+2)
H_M = f(d)+f(k)+T+3*k+2*Nat.size(k+1)+Nat.size(d+1)+5.
```

In the active midpoint branch every signed 1/i! suffix has denominator dividing
d! and absolute value <=d+1. In the other branch e=1/2^(T+1), including T=0,1.
Thus actual e has denominator dividing Q_E and |e|<=d+1 in ALL cases. Tail
coefficients and clipped are also covered. Each weighted source has denominator
dividing Q_M. Legal middle binomials are integers <=2^(k+1); each of the two
middle suffixes has absolute value <=(k+1)*(d+1)*M_A*2^(k+1).
Their final sum has bound M_M, and every such value has denominator dividing
Q_M. The same envelope covers the weighted products before signs/guards.
Canonical heights are <=H_M by the literal C269 bridge. Signed cancellation is
never used to bound an unobserved intermediate. k=0 and empty suffixes are kept.

**Step, powers, translation, left.** Write R=u/v canonically, v>0, including
u=0. For 0<=q<N, the actual nonzero step-scaled base is
`+/- u/(v*2^(N-q-1))`; bit zero gives 0, but the scaled value is still computed.
Every power exponent ell is <=r<=L; its denominator divides
`(v*2^N)^ell` and its magnitude is <=2^(A*ell). Therefore a safe cap for the
entire translation/left family (including binomial multiplication) is

```
H_K = L*(A+N)+L+2.
```

Left bases +/-R use ell<=L; constants use ell=0. Binomial factors add <=L+1
bits, not a factor exponential in the number of other entries. `powQ` has ell
separate multiplications at each invocation. It is executed independently for
each table entry; no memoization of powers/binomials/zero-masked branches is
assumed. This is why bit width and operation count must remain separate.

**One candidate cap on the rational suffix.** Let

```
H_C = A+N+Nat.size(T+2)+2
H_* = max(B, 2*f(L), H_M, H_K, H_C, N+1, T+2).
```

The section 5 quotient argument supplies H_C; the inventory above then supports
height <=H_* for every canonical rational at a listed C248/C150/C23 numerical
site. Each C269 raw operation list would have integerBits <=2*H_*+1 using
`primitiveWidth`. This is a SOURCE-LEVEL coverage argument, not an existing
Lean Sites theorem. Normalization scratch and native evaluation are not covered
by the definition of rawIntegers. Crucially

```
H_* = O((B^2+k+1)*(A+N+log(B+k+2)) + B),
```

not `2^(number of field operations)`. The logarithmic bound on f can alternatively
be weakened to a polynomial using size(t+1)<=t+1 without losing polynomiality.

For the returned QData specifically, a common positive denominator is
`Q_data = (v*2^N)^L * Q_M`; an integer magnitude envelope is
`M_data = M_M + 2^(L*(A+1)) + 1`. These are proof witnesses, not a proposed
replacement representation/producer. C248 next casts to ℝ; actual `ofTable`
then performs terminal and initial boundary product-sums (not just copying).
Its rational-shadow common denominator could be Q_data^3, including n=0 where
both boundaries touch the same core, with magnitude <=D^2*M_data^3. Linking that
shadow to the actual ℝ operations is a SEPARATE bridge; C324 does not type-apply
to ℝ. No whole stored-producer bit theorem follows here.

## 4. Dependence on input epsilon is not just dyadic precision

For arbitrary delta, delta<=0 gives reciprocal<=0 in the natural ceil convention,
so T=0. For delta>0, `ceil(1/delta) <= delta.den < 2^B`; hence in either case
T<=B by `Nat.clog_le_iff_le_pow`. In particular d<=4*B^2+2*B+1.

The actual source allocation is

```
delta = epsilon / C
C = 2^(N+2*k+2)*(k+1)^2
E = height epsilon
height delta <= E+N+2*k+2+2*Nat.size(k+1).
```

This includes signed/zero epsilon as a height statement. On the existing
scientific domain epsilon>0, k+1<=2^k also gives
`T(delta) <= N+4*k+2+tailCutoff epsilon`, including epsilon>1. The sharper
precision scale controls degrees/loop counts, whereas E still controls reading
and dividing the exact rational input. R enters separately through A; no new
small-cache, positivity of R, or reduced-input-height assumption is introduced.

Two exact counterexamples to DROPPING those input dependencies (not to H_*):

* n=0, delta=1/2, R=2^(-b), b>=1: N=1,T=1, step=R and the +T quotient is
  2^b+1, although the final strict cut is just 2. The raw threshold work is
  not bounded by the bits of the capped cut independently of height R=b+1.
* k=n=0, epsilon=(2^b+1)/2^b, b>=1: tailCutoff epsilon=0 and T(delta)=3
  are fixed, but actual cutoff reciprocal is 2^(b+3)/(2^b+1), height b+4.
  Operation-scale/precision-only complexity cannot replace dependence on E.

Both are hand-derived infinite families; no scan or program was run.

## 5. Integer work and retained native gaps

For R!=0 the threshold quotient is
`(s*v+u)*2^(N-1)/u`, |s|<=T+1. This proves H_C even for R<0. For R=0,
Rat's TOTAL division gives quotient 0; there is no nonzero-radius premise.
`Rat.floor_def'`, `Rat.ceil_def'` and `FloorRing.toFloorSemiring` expose integer
division and toNat: Nat.ceil/floor quotient need <=H_C bits; floor+1 needs
<=H_C+1; the cap 2^N needs N+1 bits. Signed integer floor intermediates also
need operand-dependent bounds, not a cost of one comparison.

The cutoff's natural ceiling c=max 1 ceil(1/delta) has <=B bits. Mathlib's
ACTUAL `Nat.clog.go` squares its base, with an early `c<=base` stop. Starting
at 2, its first stopping base is <c^2 when c>2 (c=2 is immediate). Thus these
bases need <=2B+1 bits, not a double-exponential height cap from blind squaring;
recursion depth is O(1+log(B+1)). This is a source algorithm observation, NOT
a native-cost certificate for division/squaring/fuel/compiled recursion.

Other actual natural work: d's square/add/subtract, m,L,D and array lengths;
Fin range counters; factorial next indices; legal triangular guards and Nat.sub;
four sum-tag tests and offsets in decode; two product quotient/remainders per
component decode plus the kernel output-pair decode; cut /2^q and %2; repeated
2^N/2^q caps; vector indexing, copying/allocation and all counter sums/products.
No full physical-grid enumeration 0..2^N occurs in QData materialization:
there are 2*N*D^2 kernel outputs and 2*D boundary outputs. Width N, not its
bit size alone, is an intended size parameter. Selected quotient/remainder
counters do not count every natural division above (notably floor/ceil/clog).

Source arithmetic-count structure is polynomial: factorial copies O(L^2),
source/middle O(k^2), setup O(d^2+N+T), materialization
O(N*D^2*(N+L)+D*L) scalar steps plus its indexing work. It does not share
translation calls across entries. Output storage alone has 2*N*D^2+2*D Rat
cells; a source-level upper allocation inventory must additionally account for
counted-record/projection vectors and persistent factorial prefixes O(L^2).
No peak-memory/GC/evaluator-sharing or CPU theorem is inferred. A future native
polynomial-time lift must fix algorithms/costs for canonical Rat normalization,
GCD scratch, integer mul/div, floors/logs/powers, array traversals and metadata.
The eight-counter partial ledger and selected index counters do not supply this.

## 6. Smallest next seal candidate (one concrete source-suffix interface)

Do not seal the global H_* claim or invent a universal Sites trace yet. First
freeze a mathematical observation (not a numerical producer)
`SourceSuffix k i s := S(k,i,s)` from section 3 with the exact finite Ico sum.
Candidate proposition, all binders shown:

```
forall (k : Nat) (i : Fin (k+1)) (s : Fin (i.val+2)),
  let q := SourceSuffix k i.val s.val
  q.den | k.factorial /\ 0 <= q /\
    q <= (((i.val+1-s.val)*2^(2*k) : Nat) : Rat)
```

Plus the same-object returned-cache conjunct under those SAME binders:
`let a := (produceSourceCache k).value[i.val];
a.den | k! /\ 0<=a /\ a<=((k+1)*2^(2*k) : Nat)` (cast to Rat).
No premise about table correctness, cache size, coefficient values, caller
bounds, tolerance, or performance is allowed. Proposed provider/import path:
unchanged `ChargedSourceCache` + C269 `Definitions`, with canonical Rat
divisibility and factorial/choose bounds imported explicitly at later type seal.
Use actual `factorials_value`, `chooseFrom_value`, `sumEntries_value`,
`sourceEntry_value`, `produceSourceCache_entry` as dependency names, not new
correctness assumptions. Internal reindexing must identify the literal dropped
`sumEntries` call with this Ico observation at EVERY s; final cache equality
alone is not suffix coverage. Empty s=i+1 and k=i=0 are mandatory seal cases.

After that local interface, the next real dependency is the signed actual
middle suffix envelope Q_M/M_M with e, cache, F and weights bound to the actual
returned constructors, not arbitrary vectors. Then a coverage relation for the
whole C248 call tree, integer/native lifts, and the exact-real assembly boundary
remain. This packet proposes no extra scientific assumption and reports no
new accepted root. No Lean file, proof search, compiler or numerical experiment
was used. Parent must type/form/freeze any chosen interface before proof work.
