# C23 internal same-object arithmetic and count review

Verdict: **ACCEPT_INTERNAL_BOUNDED_CONTRACT**. This is a distinct internal correctness/cost review, not the source-blind decoder, source-publication reviewer, main-admission gate, scientific ROOT, or finite-bit certificate. C23 remains a locally proved prerequisite pending parent integration/publication gates.

## Frozen scope and independence

The reviewed sources are `experiments/hermite-polynomial/precision/charged-coefficient-cache-c23/ChargedSourceCache.lean` (SHA256 `e8c7f4f51adeffeacbef5dd76f9dcc46402d691973e4fd37ddc92f957904fa4f`) and `CacheConsumerChecks.lean` (`197ba9a69db207dfe002d76819cce41fc6f30640fdfe2e77e1be545e93a541c8`). The author final manifest is bound by `b96de55a061b27e05efcff01df5ca0005278d9dec4f3dc61c75f09018554c104`. All three hashes matched before and after the focused gates.

Read order: AGENTS, HARNESS, substantive-worker skill and its three protocols; raw C23 sources and both statement seals; actual StoredGivens/StoredHermiteCoefficients definitions and C21 ActualCoefficients; then the first independent semantic/cost pass. Only after that pass were the author's final manifest, replay scripts, focused-verification receipt, result and handoff inspected for bindings and provider selection. Their conclusions were not the starting evidence. The finite-middle coefficient definition, coefficient-range numerator and Mathlib factorial quotient proof were also inspected to check range and denominator subtleties. Two process-only memory entries were consulted; neither supplied mathematical authority.

Direction: `C23_SAME_OBJECT_ARITHMETIC_AND_COUNT_AUDIT`. Gain: detect omitted operations, wrong returned objects, or coefficient bridge drift without another construction search. No subagents and no production/C23/frozen-cache/Git writes were made. Everything written is under this review directory.

## Arithmetic and binder audit

The producer is a deterministic computable rational `Run (Vector Rat (k+1))`. Its executable bodies do not call Nat.choose, Nat.factorial, an oracle, or a desired-output callback. They generate factorials by a stored multiplier and charged multiplication/addition, then evaluate each binomial by three stored factorial reads and charged multiplication/division. Each source summand additionally reads its factorial denominator, divides, and accumulates by a charged addition, including the last addition to zero.

Factorial induction supplies all helper `correct` premises internally. The public producer/consumer contract has only natural and finite-index typing inputs; there is no caller-supplied factorial correctness, denominator nonzero, target vector or cost premise. The new review lemmas `produced_factorial_positive`, `choose_denominator_nonzero` and `source_denominator_nonzero` check every division locus. Mathlib's `Nat.cast_choose` itself uses factorial positivity and characteristic zero, so division by zero has not been used as a silent fallback on the actual producer.

For `i : Fin (k+1)` and `r : Fin (i+1)`, `k <= k+i-r <= 2k` and `r <= i <= k`. The table extends through `2k+1`, so all accesses are valid (one final factorial is conservatively surplus). The output is exactly `sum r in range(i+1), choose(k+i-r,k)/r!`. C21's existing bridge applies because `i <= k` follows from the finite type. The full output range, the final entry `i=k`, and `k=0` are retained. No boundary or signed-middle coefficient is substituted.

The real bridge identifies this rational output, entrywise after casting, with the actual real `StoredHermiteCoefficients.sources` supplied by its actual factorial table. It does not identify the real Bernstein `compile` output, transport its cost, or erase its separately counted exponential.

## Operation audit

The eight counters are field, sqrt, angle, trig, compare, read, write, emit. Rational add/multiply/divide each charge one field tick. `collect` charges two reads and two writes per materialized result. An extension copies every old scalar, charging its read and one index comparison per output. Thus the quadratic bound includes persistent copying; it does not rely on in-place replacement or a free arbitrary matrix callback.

Independent count derivation: set `W=k+1`, `n=2k+1`, and `T=W(W+1)/2`. A factorial extension to index `j` contributes two field operations, `j+1` comparisons, `3j+3` reads, and `2j+2` writes. Initialization contributes two reads and two writes. Every source summand contributes four fields and four reads; the final source collection contributes `2W` reads and `2W` writes. Therefore the manually derived exact cache counters are:

| Counter | Derived count |
| --- | --- |
| field | `2W^2+6W-2` |
| compare | `2W^2+W-1` |
| read | `8W^2+7W-1` |
| write | `4W^2+4W` |
| sqrt/angle/trig/emit | `0` |
| total | `16W^2+18W-4` |

These whole-cache exact polynomials are a source-level derivation, not advertised as a separately Lean-proved parametric equality. The review does additionally prove `sourceEntry_exact_cost` parametrically on the actual code: `(i+1)*(4*tick.read+4*tick.field)`. All four whole-cache finite tuples below agree with the derivation. The advertised parametric bound follows independently from the actual producer's checked per-category theorem: `52W^2` per category and `416W^2` over the eight-category total. The constant 416 is conservative, not an exact count.

| k | Returned values | Eight-counter tuple | Total |
| --- | --- | --- | --- |
| 0 | `[1]` | `[6,0,0,0,2,14,8,0]` | 30 |
| 1 | `[1,3]` | `[18,0,0,0,9,45,24,0]` | 96 |
| 2 | `[1,4,19/2]` | `[34,0,0,0,20,92,48,0]` | 194 |
| 3 | `[1,5,29/2,193/6]` | `[54,0,0,0,35,155,80,0]` | 324 |

No nonconstant rational arithmetic operation in the frozen producer was found outside its charged primitives. Natural index arithmetic, loop/recursion control, fixed record projections, proof checking, counter metadata and its summation are deliberately outside the model. Actual rational numerator/denominator bit lengths, GCD/reduction, allocator costs and evaluator/compiler execution are not bounded by this annotation model. A `Run` cost is not a general theorem about the physical cost of evaluating its cost function. These are explicit boundaries, not missing operations within the sealed scalar/word tier. No finite-bit upper bound or lower-bound improvement follows here.

## Independent same-object consumer and falsification checks

`IndependentConsumer.lean` imports the producer and the real stored provider, not the author's CacheConsumerChecks or joined theorem. `same_object_arithmetic_and_count` joins full-range equality to the actual C21 coefficient, every per-category bound and the eight-counter total on one explicit `let run := produceSourceCache k`. It derives the bridge and total from the raw producer roots. `lookup_same_object` then actually reads from that returned cache: the value is the same actual coefficient and the composed total is at most `416W^2+1`. This charges downstream lookup rather than silently treating it as free. It is a local consumer; the existing C22 producer has not thereby been changed to use the cache.

Two false broad readings are refuted by checked counterexamples. With a zero factorial table, `chooseFrom` at `(0,0)` returns zero rather than `choose(0,0)=1`; the helper's `correct` premise cannot be dropped. At `(k,i)=(0,2)`, `sourceCoefficientQ=5/2` but C21 `coefficientQ=2` because its natural factorial quotient formula is only bridged on `i<=k`. The full-carrier bridge is false, while the actual finite cache range never reaches this case. Unsupported finite-bit/full-C22 interpretations are rejected as unproved, not declared mathematically impossible.

## Replay, trust and failure preservation

Lean 4.33.0 directly elaborated the actual StoredGivens, StoredHermiteCoefficients, C21 ActualCoefficients and both frozen C23 sources into a new private output, then checked the independent consumer. Actual `--deps` selections are recorded in the gate JSON receipts. The complete project namespace was copied from author fresh-v3 as explicitly inherited lower providers, except the two project targets that were freshly recompiled. C21/C19/C20 paths remain inherited and ordered. Mathlib and transitive dependencies are inherited, pinned, and not claimed freshly rebuilt. `pre-gate.json` and every gate verify source/import/companion hashes before and after.

The final independent consumer reports 22 ordinary-axiom roots, including eight parametric roots, twelve finite value/count roots and two counterexamples. No final sorryAx, added axiom, native-decide trust axiom or imported joined-certificate substitution is accepted. Finite values use `decide +kernel`; finite counters use ordinary `decide`. They remain supporting cases, never arbitrary-k evidence.

Preserved failure 1: the initial replay scheduled C21 before the real stored provider, and its cached transitive decomposition required the excluded fresh namespace target. This was ENV_BLOCKED/provider order, not negative mathematics. The successful correction changes scheduling only. Preserved failure 2: ordinary `decide` could not reduce some rational/vector value cases; the first consumer source and raw/error logs are retained. This was IMPLEMENTATION_FAILED, not REFUTED. The successful kernel-reduction revision has no mathematical statement weakening. Failed elaboration's sorryAx reports are explicitly rejected, not counted as accepted proofs. Original-source byte backups and private raw-log hashes are retained; public paths are sanitized and relative.

Only focused internal gates were run. Full `lake build`, Tests, site/publication gates, source-blind round trip, global purification and Exposition Seal remain parent-owned requirements. This review does not refresh the public source admission registry or claim those gates passed.

## Disposition

The bounded actual rational source-cache correctness and scalar/word-count contract is accepted internally. No repair to frozen C23 is requested. The useful frontier gain is an independently checked same-object/charged-read contract and sharper operation/range diagnostics. Middle-coefficient construction, scalar setup, all local/boundary tables, cache consumption throughout C22, full preprocessing, numerical normalization, sequential state preparation, the original scientific ROOT and finite-bit runtime remain open.
