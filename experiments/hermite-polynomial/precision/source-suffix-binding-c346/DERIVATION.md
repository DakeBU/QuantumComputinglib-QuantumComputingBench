# C346 — sealed actual suffix binding only

Continuing author package under C345; no independent-review claim. The sole
public root is `HermiteSourceSuffix.actualSuffix : ActualSuffixSpec`.
The C342 body/signature hashes are unchanged. `suffixEnvelope` and
`returnedCache` are not proved here; no other worker code is read.

1. `actualFactorials_entry` specializes original `factorials_value (2*k+1)`
   to the literal `actualFactorials k`. No supplied F/correctness hypothesis.
2. `actualSourceTerm_value` unfolds only the term's Run/read/division shell,
   applies actual `chooseFrom_value`, and discharges that internal correctness
   requirement using step 1. It returns exactly choose(k+i-r,k)/r!.
3. `suffix_eq_math` applies original `sumEntries_value`. The Fin domain is
   i+1-s; `Finset.sum_Ico_eq_sum_range` and `Fin.sum_univ_eq_sum_range`
   identify its original index s+r with the mathematical Ico sum. No cache
   final-value shortcut replaces the inner suffix obligation.
4. `suffix_zero` separately binds offset zero to the actual original
   `sourceEntry k (actualFactorials k) i`, using its original value API and
   the same actual factorial correctness. Ico(0,i+1)=range(i+1).
5. `tail_eq_next` expands the actual `f(r.succ)` tail observation, not a
   presumed equality built into its definition. Reindexing lengths uses
   i+1-(s+1)=i-s. Term indices satisfy s+(r+1)=(s+1)+r.
6. `suffix_head_tail` applies the exact Ico head split
   `Finset.sum_eq_sum_Ico_succ_bot h f`, consuming the independently bound
   next-offset tail from step 5.
7. `suffix_empty` uses i+1<=s to make Ico empty. Typed s:Fin(i+2)
   therefore retains the required s=i+1 case; no positivity/cache premise.
8. Final root splits only on the actual sealed nonempty branch and assembles
   these equalities. `ExactChecks` assigns it to the fully expanded C345
   conclusion and requests axioms of both the root and expanded assignment.

All helper hypotheses are index/branch evidence or the internally discharged
actual-table specialization; they add no public correctness, size, positivity,
precision or resource assumption. k=i=0, zero offset, and empty suffix remain.
No mathematical bound on signs/magnitude/denominator is claimed by this root.

The root concerns value observations of the literal sum recursion; it is not a
Run-cost equality, trace/Sites extraction, once-only/eager-sharing theorem,
native Rat/GCD scratch or bit/runtime certificate. Original normalized scientific
ROOT and finite-bit/export/circuit gaps remain open. The skill keeps these
boundaries and requires parent exact own-output verification after author freeze.

Bounded-author compiler permission was granted specifically for C346 after the
initial no-compiler instruction. Only the new task-local orchestration is used;
it reads C344 ZIP prefix/LEAN_PATH, checks pinned executable/providers and live
available memory, then runs direct Lean with M3072/j1/120s. It preserves full raw
records before display. This is not a provided project script or production
pipeline. At most three compile invocations including the consumer are allowed;
failed output is never put on a later import path. Actual outcomes belong in
the final input manifest/freeze, not inferred from this derivation.

Observed attempt 01: exit1/41.125s, no own olean. The factorial read needed an
explicit Fin specialization after simplification; the tail's forward Fin/range
rewrite did not match. Its warning and compiler-recovery sorryAx are preserved
and rejected; that failed output was never imported. Attempt 02 changes only
those two proof normalizations (reverse RHS range-to-Fin plus Fin.val in the
shift equality), exits0/39.344s and prints ordinary3, with no warnings.
Attempt 03 assigns its exact own output to the expanded sealed conclusion,
exits0/38.797s and prints ordinary3 for both roots; --deps selects that own hash.
Available memory immediately before these compiles was 6798/6510/6509 MiB.
Full raw logs/ZIPs and first failure remain. Three compile calls are complete;
the slot was returned immediately. This is author-local candidate verification,
NOT parent acceptance/independent rerun/clean transitive TCB or ROOT completion.
No option, heartbeat, target, linter or axiom policy was changed.
