# C306: first C295 dyadic-scale target, author candidate

Only the exact closed scaleDyadicBound is attempted. C295 already seals its
literal C276 body after actual C283 type formation. Other two budget and
same-run polynomial bounds are NOT attempted or claimed here.

Induction gives k+1 <= 2^k. Thus 4*(k+1)^2 <= 2^(2k+2). The literal cutoff
is clog2(max1(ceil(1/epsilon))); its selected power dominates 1/epsilon.
Multiplication by the preceding nonnegative factor bounds the reciprocal of
epsilon/(4*(k+1)^2) by 2^(2k+2+cutoff epsilon). Natural ceil and the clog/power
adjunction yield the desired cutoff bound. Add the unchanged n+1+2k and
normalize natural arithmetic. All positive rational epsilon are retained;
there is no epsilon<=1 restriction. R is not a binder of this first target.

Source/API scope: whole C147 allocated-degree source (26768957...), exact C276
typed bodies, C295 seal/signatures; actual primary Nat.Log lines381-455 include
complete clog_le_iff_le_pow/le_pow_clog bodies. The ceil/cast recipe is the
already compiled C147 proof pattern, not a claim of fresh transitive Mathlib
source-to-binary audit. No new definitions or implicit scientific assumptions.

This only relates the auxiliary scale to n_p=n+1, k and positive-part dyadic
precision. It does not prove either polynomial operation envelope, native
bit/GCD/CPU/allocator bounds, quantum gates/angles/cleanup, source-value or the
Hermite ROOT. No finite experiment or production behavior change. Parent
source/exact expanded own-output consumer/ordinary axioms gate is pending.
