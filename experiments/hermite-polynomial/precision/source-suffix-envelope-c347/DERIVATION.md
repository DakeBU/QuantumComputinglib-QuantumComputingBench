# C347: exact mathematical source-suffix envelope candidate

Objective: ONLY HermiteSourceSuffix.suffixEnvelope : SuffixEnvelopeSpec,
the SECOND C345 closed root. No other proof packet or runtime result read.
The preproof seal, whole sealed definitions/signatures and literal C342/C23
sources were read before authoring. C338 ANALYSIS was permitted but not needed
or opened; its assertions are not premises. This is an author packet, not review.

## Exact object and mathematical derivation

For arbitrary k:Nat, i:Fin(k+1), s:Fin(i.val+2), write
q=sum over r in Ico(s.val,i.val+1) of choose(k+i.val-r,k)/r!.
These are canonical rational operations and the exact sealed natural subtraction.
The PUBLIC conclusions are q.den|k!, 0<=q, q<=(i.val+1-s.val)*2^(2*k).
There are no extra public assumptions.

1. A term's canonical denominator divides its supplied natural denominator:
   rewrite (a:Rat)/(b:Rat) through actual Rat.natCast_div_eq_divInt, then
   Rat.den_dvd and Int.natCast_dvd_natCast. No equality of unreduced and
   canonical denominators is presumed.
2. For r in the actual Ico, r<i.val+1 and i.val<k+1 give r<=i.val<=k.
   Actual Nat.factorial_dvd_factorial therefore gives r!|k!. Compose with1.
3. The finite sum keeps the SAME k! denominator: empty sum has canonical
   denominator1; insert uses actual Rat.add_den_dvd_lcm, and Nat.lcm_dvd
   combines the two already-proved divisibilities into k!. A repeated
   product-denominator estimate would not establish this target and is not used.
4. Each term is nonnegative because both casts are nonnegative. The bound
   r!>=1 is derived from Nat.factorial_ne_zero, not supplied by the caller.
5. For every natural r, even outside the suffix, k+i.val-r<=2*k from i.val<=k.
   Nat.choose_le_choose then Nat.choose_le_two_pow at2*k gives the numerator
   <=2^(2*k). Cast to Rat. Actual div_le_self uses nonnegative numerator and
   factorial denominator>=1 to give the same bound for the whole term.
6. Sum pointwise bounds. Nat.card_Ico is exactly i.val+1-s.val, including
   empty intervals. Finset.sum_const, nsmul_eq_mul and Nat.cast_mul give the
   precise requested natural product cast into Rat, not an enlarged bound.

The three private helpers implement1,3,5. Fin/Ico inequalities are internal
typing consequences. Finset induction's hypothesis is a proof dependency,
not a public source-correctness premise. No C269 height/common-denominator
theorem or primitiveRepresentation root is assumed or re-proved.

## Endpoints

s=i.val+1 gives Ico(a,a)=empty: q=0, canonical denominator1 divides k!,
nonnegativity and the exact zero upper bound hold. This is the general empty
finite-sum branch, not a removed special case.
For k=i.val=0, i is the only Fin1 index. At s=0 the one term is choose(0,0)/0!=1,
with denominator1 and upper bound1. At s=1 the suffix is empty. No k>0,
nonempty, strict-sign or nonzero-divisor hypothesis was added. These are
symbolic endpoint derivations, not executed finite diagnostics or benchmarks.

## Actual-source reuse and remaining AND edge

C23 factorials/sourceEntry/sumEntries/produceSourceCache remain unchanged.
C342 fixes the actual factorial table in its observation definitions and
defines SourceSuffix as this literal Ico sum. This proof imports those exact
definitions, but only establishes the mathematical envelope for SourceSuffix.
The separately assigned ActualSuffixSpec equality/recursive-drop binding is
NOT proved, presumed, read from another author, or replaced by an oracle.
ReturnedCacheSpec requires that first root AND this second root; it is not
claimed here. The fixed C23 provider and interval/provider snapshots match
the C345 pins, with identical C23 bytes across the three inventoried caches.
That current hash observation is not a new compile, loader selection or
transitive source-to-binary/TCB certificate.

## Lean candidate, exact consumer and risks

SourceSuffixEnvelopeProof.lean imports only SourceSuffixDefinitions and
necessary primary Mathlib interfaces. Root has the exact sealed named type;
private local positivity/divisibility conditions are discharged internally.
ExactChecks.lean expands SourceSuffix and SuffixEnvelopeSpec literally in a
closed theorem consuming the named root, prints both actual definitions, and
requests root/expanded-consumer type and axiom queries.
Expected author commands: source has1 root axiom query; consumer has2 named
queries. These are COMMANDS, not runtime evidence or verified ordinary rows.

No compiler/lake/Python/project script/Git/network/subagent ran; no old file
was edited. All source is UNCOMPILED. Parent must check imports/own-provider
routing, exact Nat/Rat casts and exact_mod_cast availability, Finset induction
elaboration, and actual kernel/type/axiom output. No failure result is invented.
An API-location search of the nonexistent Algebra/GroupPower/Basic.lean path
returned missing-file only; the actual nsmul_eq_mul body was then located/read
in Algebra/Ring/Defs.lean. This is not a mathematical obstruction.

Prior author/reviewer context includes degree/setup, middle/same-run,
explicit VALUE/decoder and C311 cost work plus C320/C330/C334 rational
representation staged intake. This task is not an independent review of any
of that work; C311 was not reopened/reviewed. Other-worker proof is unopened.
Mandatory instruction/skill/protocol whole intake is retained and hashes
unchanged; the skill keeps proof ingredients as dependency edges.

## Frontier handoff and freeze

Mathematical delta: closed common-k! denominator + nonnegative + remaining-
length exponential envelope for the actual sealed Ico coefficient suffix.
Failure class: NONE identified mathematically; IMPLEMENTATION UNVALIDATED.
No accepted root, new axiom, hole, native_decide, unsafe code, trust/linter/
option change, or publication/ProofSeal/clean-TCB/PURIFIED claim.
Class C internal supplier only. Not an input-height/native integer/GCD scratch,
Sites/producer occurrence/bit/CPU/memory/evaluator or physical quantum bound,
not actual-cache joining or full scientific ROOT. Parent owns the bounded
source plus exact-own-consumer gate; genuine failures must be preserved in
a new successor. Freeze this packet and STOP.
