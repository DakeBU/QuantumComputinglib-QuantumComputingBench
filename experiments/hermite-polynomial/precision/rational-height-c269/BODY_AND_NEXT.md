# C269 canonical Rat height: definitions-only freeze candidate

No theorem proof, type probe, evaluation or accepted bit bound. Exactly FOUR
closed intended propositions are defined in Definitions.lean and named in
IntendedTypeChecks.lean. Parent actual typing precedes any Statement Seal or
proof authorization. C257's proposed whole-producer envelopes are not results.

## Literal definitions and four targets

Use actual Rat.num:Int, Rat.den:Nat and Nat.size, not a new rational carrier.
integerBits z=size(abs z); height q=max(1,bits(q.num),size(q.den)). Magnitude
bits exclude a sign bit. A canonical signed-magnitude pair payload would use
1+bits(num)+size(den) bits; framing, parsing and native allocation are excluded.

Witness is only an unreduced integer/natural pair, without assumed positivity
or correctness fields. witnessValue interprets it by Rat division;
witnessWidth=max(1,bits(numerator),size(denominator)). commonWitness(q,Q) is
(q.num*(Q/q.den),Q). Q=0 is defined as a raw pair but never asserted to be a
positive-denominator representation. There is no default witness claimed valid
outside the positive common-denominator locus.

Raw add/sub use (p*s +/- r*q,q*s), retaining BOTH separate cross-products.
Mul uses (p*r,q*s). Nonzero division uses numerator p*s with the sign of r
moved into that numerator, denominator q*abs(r). Divisor num=0 gives (0,1),
matching total Rat division. The division rawIntegers list STILL includes
p*s and signed q*r, even when r=0; these are mathematical unreduced integers,
not an assertion of a valid zero denominator or a native temporary trace.
operationValue is a one-operation semantic alias, never a second QData/cache
producer. No Run, desired-output callback, factorial implementation or Sites
relation is added. Actual C248/C23/C150 numerical bodies are untouched.

1. HeightBoundSpec: h(q)<=B iff 1<=B, abs(num)<2^B and den<2^B.
2. CommonDenominatorSpec: Q>0, q.den divides Q, abs(q)<=M (M:Nat) imply the
   explicit common witness represents q, its numerator magnitude<=M*Q, and
   h(q)<=max(1,size(M*Q),size Q). Signed q and M=0 are included.
3. PrimitiveRepresentationSpec: for every operation and canonical x,y, the
   raw witness denominator is positive, its value is the canonical operation
   result, that result's denominator divides the witness denominator, its
   numerator magnitude does not increase, and its height<=witnessWidth.
4. PrimitiveWidthSpec: witnessWidth and EVERY listed raw integer width are
   <=h(x)+h(y)+carry, with carry1 for add/sub,0 for mul/div. No operand-height
   promise is needed: these are the actual input heights by definition.

All four are UNPROVED Prop definitions, not axioms or theorem declarations.
Q,M,B are ordinary witnesses/typing parameters in foundational interfaces;
common-denominator and magnitude facts must later be produced internally for
the actual prefix, never added as small-cache/desired-result premises to the
scientific root. No native-cost hypothesis or hidden bundle is introduced.

## Hand boundary checks, not executed tests

| exact input or pair | hand result |
| --- | --- |
| canonical0,1,-1 | num magnitudes0,1,1; den1; heights1,1,1 |
| canonical1/2 and -1/2 | numerator magnitude1, denominator2; height2 |
| 2^t or 1/2^t, t>=0 | height t+1; equality with 2^B needs B+1, not B |
| HeightBoundSpec at B=0 | false on both sides; 1<=0 is false |
| q=0,M=0,Q>=1 | common numerator0; height1, no excluded zero case |
| q=1/2,Q=6,M=1 | common witness3/6; width3; canonical height2 |
| x=y=7/6, h(x)=h(y)=3 | add raw84/36, cross-products42,42; width7=3+3+1; canonical7/3 height3 |
| x=y=7/6 | mul raw49/36 width6; div raw42/42 width6, canonical1 height1 |
| x=-1/2,y=-1/3 | div raw+3/2, not -3/2; positive denominator retained |
| x/0, including0/0 | representation witness0/1 width1; signed raw denominator0 remains listed |

Bounds on magnitudes are NONSTRICT (<=M, <=M*Q); size caps are STRICT (<2^B),
using Nat.size_le. This avoids the power-of-two and zero off-by-one traps.
Sign-magnitude is not a two's-complement width convention. No claim is made
that a mathematical witness matches the selected native normalization algorithm.

## Reuse and the precise next missing dependency

Inspected Mathlib APIs: Rat.pos, num_den_mk, add_den_dvd_lcm,
sub_den_dvd_lcm, mul_den_dvd, add_num_den, mul_eq_mkRat, div_def', and
num_abs_eq_abs_num/den_abs_eq_den; Nat.size_zero/one/size_le/size_pow and
size_le_size. They motivate the targets but are NOT used in any new proof.

After parent typing and sealing, prove only these four foundation statements.
The first actual consumer should be C23 sumEntries/sourceEntry suffixes with
the ACTUAL generated factorial table: denominator divisibility by k! and the
actual signed/unsigned magnitude invariant must be proved for EVERY recursive
suffix, not only the final cached vector. Rat.add_den_dvd_lcm is the needed
closure edge, not a repeated denominator-product recurrence. Middle consumers
later retain signed weighted terms, both guards and both suffix sums.

Sites is deliberately NOT defined here. Existing Run records store output and
counters, not all primitive operands. The next observation contract must bind
each qAdd/qSub/qMul/qDiv invocation to its actual canonical arguments/result
under the literal sumEntries/powQ/bind branches, including empty suffix,
negative values and division by zero. It must prove coverage of actual source
execution structurally, not execute a second producer or assume a small trace.
Without that separately sealed coverage relation, these four foundations
cannot imply C257 B_work, whole QData data height or native temporary bounds.

Audit: definitions are literal mathematical functions, no choice/default
correctness oracle; no theorem proof body or new correctness premise on C248.
Source construction remains actual Rat primitives and actual source suffixes;
Lean graph adds only candidate definitions/Prop bodies, no proved edge or new
quantum representation. Root/value/error/normalization/physical sharing and
native bit/GCD/allocator/evaluator/synthesis/phase/cleanup/export remain open.
Failure class NONE at design layer; typing/API acceptance is pending, not a
mathematical impossibility. C257/C248 and all earlier packets preserved.
No C264 review, current runtime or other value-author proof opened. Prior own
cost-work exposure is retained, not used as bit-growth proof evidence. No
compiler/Python/script/lake/Git/network/subagent/evaluation or proof search.
qbe-substantive-worker, current protocol intake and process-memory
LOW-TOKEN-CONTROL-PLANE / VERIFIER-SEMANTIC-LEVEL govern. No parallel work or
self-approved publication; Purification/Exposition-Seal NOT_STARTED. Freeze/STOP.
