# C132 controlled normalization diagnosis

State: UNCOMPILED_REPAIR_PROPOSAL. This is a proof-author diagnosis, not independent review, admission, or a proved successor.

## Frozen input and observed failure

The C128 live Draft 3 remains unchanged, SHA256 `6ebcf8afba356c6e2bbe2c33340daa3c705235eba36ff8c44ef20cce6e3b8de8`. The statement seal remains SHA256 `08934ea991afb879cc5becacbc65826feddbbb55faec1abc7906c0b67dacbb6a`.

Read the complete sanitized `C128/attempt-3-compiler-feedback.txt` and `C128/attempt-3.json`. Attempt 3 exited 1 after 65.922 seconds, without timeout, with a 3072 MiB cap, one thread, and 7412 MiB available memory. There is no accepted whole-file result or resulting operation-bridge olean. The record reports inherited dependency oleans, not a fresh transitive rebuild. All three failed attempts and their preserved sources remain in place.

The sole reported proof error is at the helper bridge's broad `simpa ... using congrArg ...`. The compiler reports that the supplied equality simplified to `True`, while the target simplified to a disjunction: the explicit two-term delta sum has the expected value, or the common conditional-CZ factor is zero. This is an observed mismatch between normalized proposition shapes. It is not a counterexample to the delta sum or the operation statement. The diagnostic also reports an unused `Fin.sum_univ_two` simp argument in the local finite-case proof.

No earlier supplier/API errors were reported in this attempt. That absence does not promote any declaration or the whole root to accepted status: the file failed and no output module exists.

## Causal diagnosis

The local `hsum` has exactly the needed mathematical content. Its two cases are bounded by `q : Fin 2`; it asserts that the Kronecker-delta sum selects the Hadamard coefficient at `q`. Transport through multiplication by the conditional-CZ sign is valid for every complex factor, without needing a nonzero-sign hypothesis.

The failed route asks the unrestricted simplifier to normalize both a transported proof's proposition and the actual helper target. Those expressions have different syntactic starting points: the former already has the explicit delta-sum statement, while the latter still contains a tuple-applied graph function and the helper's target-zero conditional. The actual feedback establishes that the two simplification routes reached incompatible proposition presentations. No exact internal simplifier rewrite trace was collected, so this diagnosis does not attribute the mismatch to an unobserved individual rewrite.

## Controlled successor

`SumAlignmentProbe.lean` isolates the exact post-`rw [hgraph]` leaf, retaining the tuple-applied graph function and the actual imported helper. It does not repeat CCX evaluation, matrix composition, isometry, completeness, or mass proofs.

The proposed route is:

1. Prove the same finite delta sum by explicit `fin_cases q`, using ordinary simplification only inside those two closed-index cases. Remove the previously reported unused explicit simp argument.
2. Use `change` to expose the actual leaf as `sign * (sum t, H[m,t] * delta(t,q) * amplitude)` on the left and the actual target-zero helper conditional on the right. Here the delta notation is only prose: the Lean code uses the original `if t = q then amplitude else 0`, not a new definition.
3. Apply only `rw [if_pos ht, hsum, mul_assoc]`. The first rewrite selects the already-proved target-zero branch; the second replaces the finite sum; the third aligns the helper's left-associated scalar product with the selected sum's right-associated product. No broad `simpa using`, common-factor cancellation, or sign-nonzero assumption is used.

The proposed live replacement is given literally in `proposed-live-delta.md`. Its acceptance depends on the parent's separately authorized tiny probe. The `change` conversion and controlled rewrites have not yet been compiler-checked.

## Scope and stop boundary

No live C128 file was edited by this successor. No operator definition, public theorem statement, source statement seal, helper source, assumption set, or dependency pin is changed. This is a normalization repair of one existing proof leaf, not a mathematical reformulation. The small probe introduces no correctness hypothesis: `ht` is the existing local branch case, not a new binder on the root or helper bridge.

No compiler, Lean evaluator, executable proof probe, Git, network, or child agent was run here. Only these new proposal files were written. Further probe execution and any full integration require the parent's explicit next authorization; the old three-attempt full-file cap is not silently extended.

The semantic scope remains the ideal finite-linear zero-input AND cleanup composition on the four-to-eight-dimensional carrier, identity use, both branch labels, exact phase and amplitude. This proposal supplies no adaptive execution, hardware reset, Born sampling, resource claim, arbitrary-use bridge, SP/BE root, production admission, or source-circuit final admission.
