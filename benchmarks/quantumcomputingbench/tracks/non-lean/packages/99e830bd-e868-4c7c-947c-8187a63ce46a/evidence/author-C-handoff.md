# C-family author handoff

Author: `/root/author_tensor_polynomial`
Baseline: `6b23dab68c2970062ddfd568ce94bce74b566483`
Frozen graph: `qcb-snapshot-ffa644f0da3031a1ce754b9a` at `86b9e677566498da04faebcf4e5ed57f177c6bb1`

## Objective and mathematical delta

- C1 retains every literal SP114 contract field and supplies explicit binomial shifted coefficients, the finite inner-width witness and an algebraic column-span proof valid for arbitrary outer index sets. No successor or additional core.
- C2 derives a prefix gauge invariant for all lengths, exact scalar amplitude/mass/norm preservation and the full-chain canonicality boundary: with right-canonical input and fixed terminal gauge, the transformed chain is right-canonical iff all internal gauges are orthogonal.
- C3 derives rectangular two-train cross environments, all terminal-label cross-inner-products, arbitrary-boundary bilinear forms, and same-train PSD/kernel semantics. These extensions are original NL mathematics grounded in the inspected source definitions.
- C4 composes nonnegative unit-sum Bernstein weights, sample error accumulation, positive lower mass, nonzeroness and the explicitly supplied normalization-stability-2delta interface. It includes an epsilon precision rule, sampled endpoint anchors, signed values, empty-sample infeasibility and a shrinking-mass counterexample.

## Files and binding

| Slot | Core identity | SHA256 raw payload bytes |
| --- | --- | --- |
| C1 | `qcb-core-sp-114` | `6d1d47bda77a13c7781b076ffacf966d79ecce55e674209e77558d306af132b9` |
| C2 | `candidate:0983ca7d-38f9-46d0-8920-b798e5c0cd7b` | `dbe542a555a13baf4ca958f270b0e2257bf87cd656e2af47606d5c6765b263d1` |
| C3 | `candidate:95850d89-ebfd-48a9-89bf-0221df041ac6` | `c635422213fb601413c8a270169aabc91837961ac555213588c8404fdae82f9d` |
| C4 | `candidate:3197f9f9-ed41-4610-9d9d-966014b9468c` | `169c92c69d5319c413c9ae91ad8207e70f7728859ae1b32ec51495b39da34f54` |

Only `qa/C1.json` through `qa/C4.json` and this handoff were written by this author. Root owns proposal wrappers, freeze manifests and independent reviews. No payload edits are planned after this freeze-ready handoff.

## Source inspection

The complete local modules TensorTrainCanonical (317 lines), TensorTrainNormEnvironment (140), TensorTrainWord (102), HermiteBernstein (479) and HermiteCutRank (259) were read. TensorTrainWord fixes contextual word-order understanding; it is not falsely made a required support node for C2/C3. RealAmplitudePreparation was inspected only at its imports/header, normSq/normSq_nonneg definitions and complete normalized_sum_sq statement/proof with adjacent definitions (explicitly recorded as partial-module reading). All operative source bytes were compared with the frozen snapshot commit and LF hashes. Raw and LF hashes agree for those files. Repository MIT LICENSE was read and attribution is recorded. No external paper or website was used.

The author read author-guide.md, frozen coverage-plan.json, AGENTS.md, HARNESS.md, shared CONTRACT/ACCEPTANCE, benchmark/non-Lean AGENT_GOAL, relevant README, substantive-worker/master instructions, theorem-publication/proof-digestion/evidence-routed-memory protocols, and relevant polynomial, Hermite, rank/regularity, operator/bond, convention/guard, quantum-contract and field/tensor checkpoints. COURSE.md lines 19-30 supplies the difficulty taxonomy. Current SP114 and related current-reader records were inspected for exact contract and bounded overlap analysis. Root-produced access-baseline evidence was read; this author did not independently query remote PRs. Other authors' drafts were not read.

## Pre-freeze correction and exposure

The initial C2 draft incorrectly suggested that an unused incoming direction could permit a nonorthogonal gauge while preserving the entire canonical chain. During the author's own drafting check, the terminal-to-initial row-Gram argument exposed that mistake. The author corrected C2 before receiving root's separate message reporting the same substantive issue. Root independently noticed it while acting as integrating author, preserved the earlier payload in `evidence/history/C2-before-root-correction.json`, and recorded `evidence/pre-freeze-C2-finding.json` (reported canonical digest `150ab39ec51359929e2a740dabff006bfedab1de49551a064af1c79eecb9c514`). This is concurrent author/root detection, not an independent mathematical-review verdict. The current question, answer, rubric, boundary list and map all contain the backward-induction converse; the unsupported unused-direction example is removed. No existing core contract changed.

## Checks actually performed

Author-side mechanical checks passed for all four payloads: JSON parsing and required fields; total rubric weight 10; every active graph node and inspected-source declaration belongs to the frozen snapshot; source LF/raw hashes match inspected files and snapshot hashes; reasoning-map input IDs and preceding-step dependencies are topologically valid; reused-result consumers exist; questions contain no formal paths/names; new UUIDs are distinct and uncounted with unassigned splits. C1's nine contract fields equal current-reader.json literally, and its contract hash/snapshot/item digest equal current-registry.json. Difficulty bands are provisional C1=D3, C2=D4, C3=D4, C4=D3; D0 facets add no cores.

Finite diagnostics also passed: exact-rational shifted polynomial factorization at signed/zero arguments; three-core prefix gauge identities with noncommuting 2-by-2 internal gauges; two-train rectangular cross environments with different internal dimensions and terminal dimension two, including arbitrary signed initial boundaries; C4 strict-error comparisons for three positive scales and the numerical display of the fixed normalized distance 0.45950584109472237. These checks are diagnostics, not parametric proof, independent review or kernel evidence. Complete mathematical derivations are in the payload answers.

No Lean, system installation, container, model call, training, paid service, production-source edit, commit or push was performed. Root owns integrated benchmark tests and curriculum validation.

## Status, reuse and residual risk

Failure class: `NONE` for the current authored payloads. The abandoned C2 assertion is `REFUTED` by the backward canonicality argument and preserved in root evidence; the valid prefix and Gram algebra were retained. No process-memory IDs were consulted. Direction fingerprint: frozen-source tensor/polynomial representation invariants and quantitative normalization composition. Expected information gain: distinguish exact global representation identities from local canonicality and normalize only after all nonzero/error premises are supplied. Parallel assignment was root-authorized; no subagents were spawned by this author.

No self-approval, formal admission, novelty certification, measured model difficulty, stable-release claim or cross-split independence clearance is made. All four are authored and freeze-ready; distinct content-bound mathematical review remains pending at authoring freeze. The new candidates remain uncounted. Suggested canonicality and Gram bridges are original NL derivations, not new Lean nodes. Shared normalization is supplied verbatim in C4, so no hidden A2 answer retrieval is required; A2/A3/C4 exposure still needs reconciliation. C1 inherits dev. C2-C4 have `unassigned_pending_reconciliation`.

Recommended next step: root freeze exact payloads, issue question-only packets to the distinct derivation reviewer, then compare against these exact hashed answers and reconcile shared subproof/split exposure. Purification/Exposition Seal: not claimed; these are isolated benchmark proposals, not production theorem publication.
