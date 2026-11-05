# C364 independent compatibility-preservation review

Verdict: ACCEPTED_FOR_SOURCE_LEVEL_COMPATIBILITY_PRESERVATION_ONLY. No source or patch changes are required by this bounded review. This is not a compiler-success certificate, maintenance-policy acceptance, ordinary source-assimilation acceptance, paper/BE research closure, publication admission, or main admission.

Reviewer identity: `/root/robin_compatibility_review_c364`, a separately delegated reviewer, not the C363 maintenance-case author or maintenance-policy author. This reviewer personally read the mandatory instructions, the complete C363 case and patch, both permitted historical boundary reports, and the bounded source ranges recorded in INPUT_MANIFEST.json. No subagents were used. Identity is actual run provenance, not a claim to have independently established historical formalizer/decoder identities.

## Frozen question and evidence

Only `QuantumBlockEncoding/RobinMatrix.lean` is reviewed, from base `af585d9cbbb299c1c8c48647627a2cb820ef536a` to subject `7c25a60c313a9c8103bdb14da4a71fc94be71470`. The latest user authorization prioritizes Lean 4.33/main release, limits Robin paper research to BE, and permits a reasonable protocol; it does not turn compatibility work into a scientific result. The repository substantive-worker skill was used as a review lens; its source/semantic/Lean separation is preserved. The explicit bounded assignment overrides its generic fetch/build/checkpoint workflow: none of those actions occurred here.

Independent raw-byte checks:

| Input | Bytes | SHA256 |
| --- | ---: | --- |
| Base module blob | 1294182 | `e957b6a5961ad2c22cfd154f17cbbec3e7668027b2f526d9f762798eb1c50038` |
| Subject module blob | 1294042 | `1cca5119ac056fe041b25c529909b9fb6c3e4995e04ebde2f69e83fce47a0835` |
| Current module file | 1294042 | `1cca5119ac056fe041b25c529909b9fb6c3e4995e04ebde2f69e83fce47a0835` |
| Exact supplied patch | 5426 | `9418ed5a4e1754b042d03084cab78ac171794cd35f71ed469ea94f0933df4bd2` |
| C363 case | 43246 | `8ef2dea9cd5ae2cda603bed83a79ce4122259d00d0981397272f864d1950c500` |

The module blobs have LF line endings, no CR bytes, and 26985 terminated lines each. Capturing the two `git show COMMIT:PATH` stdout streams as bytes, rather than hashing formatted shell output, gave the hashes above. The current file equals the subject. The complete supplied patch was applied in memory, validating every context/removal line; it reconstructs the subject exactly, with 26 added and 26 removed lines in 7 hunks. No Git apply or filesystem source edit was performed.

Important count correction: there are **7 hunks, 6 affected theorem declarations, and 5 changed proof bodies**. The first theorem has two hunks; another theorem has only the option insertion. There are not seven changed declarations.

## Per-hunk examination

All theorem names below are in `QuantumBlockEncoding.Examples.RobinHeat`. Ranges are inclusive and refer to the exact old/new module blobs. Every affected theorem's complete leading interface, including internal index-proof syntax and result-local lets, is byte-identical across the two blobs; individual fragment hashes are in the manifest.

1. `oneTermRobinBlockEncodingProofRoute_ofCleanFunctionOracleEntry`, old 1076-1162, new 1076-1164; first hunk at old 1139-1141/new 1139-1142. The local `hentry` proof changes from broad `simpa [...] using` to `change functionOraclePaperMatrix ... = (functionOraclePaperImage ...).cleanBranchAmplitude; exact functionOraclePaperMatrix_cleanBranch_entry ... hClean hBranch`. The same provider and both original hypotheses are retained. The full surrounding route definition and circuit-semantics definition were read. This changes only a local proof, not the gate, matrix, clean branch, basis, or public contract. Imported GHL definitions were not separately reread in this assignment; this is a source-preservation judgment, not an independently executed definitional-equality check.

2. Same theorem, second hunk at old 1151/new 1152-1153. The `hnormalized` proof changes from `simpa [functionOracleAmplitudeProofRoute] using hentry` to `rw [hentry]; rfl`. Its type is unchanged. It still uses the established clean-entry equality to discharge the normalized-amplitude equality. The final conjunction still carries gate-unitary, function-contract, amplitude, LCU, block-projection, block-correctness and extraction flags equal to false. No flag became a proof of a physical operator.

3. `oneTermRobinGamma3BoundaryEvalGateMatricesColumn0Entry_eq_sevenGateMatrix_n3`, old 8199-8426, new 8202-8429. The sole change is `set_option maxRecDepth 10000 in` at new line 8191, immediately governing the following documented theorem. I read the entire 228-line theorem in bounded chunks, from its public environment binder through the support/tail-kill argument and final calculation. Its complete declaration bytes are otherwise identical (SHA256 `cda066ba447b7d7b87ba2ba1d3fed0429b5d0acd189a506b036a2a281f383cb4`). `in` makes this a single-command elaboration option, not a persistent namespace/global option or a mathematical hypothesis. It increases an elaboration limit, not proof authority. The theorem remains an evaluated active-column-zero diagnostic, not active/prepared equality or raw-fold closure. The old identical theorem was captured and byte-compared, not separately redisplayed and reinterpreted line by line.

4. `oneTermRobinGamma3BoundaryFactorSemanticsContractMapEval_n3`, old 11719-11735, new 11722-11738. `simpa [FactorSemanticsContractMap_n3] using (...)` becomes `dsimp [FactorSemanticsContractMap_n3, ProjectionAmplitudeFactorSemantics_n3]; exact ProjectionAmplitudeFactorEval_n3 env hND hNF hkappa hkappaSqrt`. The contract and factor definitions and the full provider theorem were read. The projected product, target entry and normalizer are the same forwarded fields. All four original inverse/square coefficient hypotheses remain in the public interface and are explicitly passed. No premise was added, removed or converted into an alleged physical PREPARE certificate.

5. `oneTermRobinGamma3BoundaryHWKappaCleanColumnContract_feedsTransposeBridge_n3`, old 12976-12993, new 12979-12998. The old `simpa [HWKappaCleanColumnContract_n3] using ... H hUniform` becomes explicit `dsimp` of the clean-column, adjoint-entry-convention and uniform-column-contract records at `hUniform` and the goal, then the same transpose/uniform-column provider with `H hUniform`. Complete definitions for those three records and the local provider were read, together with the embedded-entry interface. Matrix carrier 8x8, focused entry, symbol and conditional uniform-column binder are unchanged. A transpose-style symbolic interface is still not a proved physical adjoint/unitary theorem.

6. `oneTermRobinGamma3BoundaryCleanColumnBraRouteContract_feedsBraAmplitude_n3`, old 13226-13243, new 13231-13250. The old route-level `simpa` becomes explicit `dsimp` of the bra route, clean-column contract and bra-amplitude source map at `hUniform` and the goal, followed by the same clean-column transpose bridge. The full relevant forwarding records were read. This is proof elaboration over unchanged fields, not a new bra amplitude, a new matrix, a newly supplied source premise, or a dropped external hypothesis.

7. `oneTermRobinGamma3BoundaryHWKappaUniformAllSlots_to_productRouteFocusedCleanColumn_n3`, old 25103-25123, new 25110-25123. The long `simpa` list becomes `change H <2> <0> = Coeff.symbol "sqrt_kappa_inv"; exact hUniform <2>`, with the original finite-index proof syntax. I read the all-seven uniform-column definition, slot/clean index definitions, and the complete product/clean-column route records that forward the focused fields. The target is the same focused slot-2 specialization, and the all-seven assumption is still the theorem binder. This does not construct H or establish its preparation semantics. The patch has 3 added versus 1 removed `native_decide` tokens here: net +2 proof-site calls, not zero trust delta at the proof-term level. They certify finite-index bounds in this source; their generated dependencies have not been audited here.

Each hunk passes the assigned proof-body-or-single-local-option test. No new theorem, definition, structure field, public statement, binder, import, namespace, notation, or persistent elaboration command is introduced or changed.

## Why declaration coverage is preservation, not a new full audit

I removed only these whole proof-body ranges from each LF source in memory:

- Base: 1124-1162, 11732-11735, 12990-12993, 13240-13243, 25114-25123.
- Subject: 1124-1164, 11735-11738, 12993-12998, 13245-13250, 25121-25123; additionally only option line 8191.

The remaining strings are exactly equal: 1290743 UTF-8 bytes, SHA256 `6f3fe8cf9e81a1b4bf0c8cd9feaa2b162af6e8c63dfd55fdb7d7ad6c17d9dc8e`. The complete source patch reconstruction independently checks that no other edits are hidden outside the listed hunks. Together with full reading of the changed declarations, this covers every unchanged definition body, structure field, public theorem header, binder, attribute and ambient declaration by equality, without pretending to have reread their mathematical meaning.

The ambient module imports, namespace nesting and `open Coeff` were inspected. All six theorems lie in the same `QuantumBlockEncoding.Examples.RobinHeat` namespace. The residue comparison also preserves all ambient bytes not explicitly removed. The manifest separately records model-visible text ranges versus whole-blob mechanical capture/hash/equality; the latter is not semantic reading.

C104's reported 677-declaration/whole-formal review and C127's historical build/context association remain historical boundary evidence, not new C364 coverage. I read only their released Markdown reports, not their evidence packages. C363's list/count of 395 public/exported declarations and experimental flags is supplied metadata; I did not regenerate or semantically validate an inventory or reconcile it with the different historical 677-total/563-public terminology. No generated export or flag removal is certified here.

Unchanged source syntax is not an elaborated cross-toolchain equivalence theorem. Lean 4.33/Mathlib changes can affect elaboration and proof terms; the supplied old/new toolchain and manifest identities were read from C363, not independently fetched or rehashed. A real subject-bound library/Tests build and explicit trust debt remain separate. No compiler was run; no old toolchain was installed; no per-constant axioms, native artifacts, binary or complete imported-provider graph was inspected.

## Scientific boundary that is explicitly preserved

The raw active-fold route is not rescued. I additionally read the current exact negation declarations at 23644-23676, 23688-23694 and 26952-26959, whose source is unchanged by the byte comparison. The counterenvironment sets `f_3_0`, `N_f_inv`, `boundary_cos_half_0_2`, and `sqrt_kappa_inv` to 1 and other symbols to 0. The selected contribution evaluates to 1 while the current active raw entry evaluates to 0; exact unrestricted backend expansion, projection summation and raw entry=fold are refuted, not merely unproved flags. A conditional consequence with that refuted antecedent is not a new valid source route. The counterenvironment need not obey extra inverse laws absent from the refuted unrestricted target.

The prepared object remains a separate seven-diagonal compression, not an established full lifted two-index physical sandwich. The C104/C127 boundary still requires a correctly typed full physical prepared operator, off-diagonal/unused-sector control, genuine adjoint/unitary semantics, full normalized block extraction and resources. A matrix assigned to a singleton gate and a status record do not supply a unitary certificate. All-seven uniform-column, HENTRY and normalization/square hypotheses in the positive conditional chain are not newly discharged by these proof rewrites. The local transpose convention is not a proof of a physical complex adjoint. These are unchanged gaps, not a new impossibility claim about every repaired physical construction.

## Disposition and stop

No modification is required for this exact source-level preservation objective. C363's proposed narrow maintenance classification is consistent with this diff, but this reviewer does not approve a new admission policy or waive repository gates. Main/release integration, executable and website/reader gates, policy tests/review, source-association and per-constant trust/native disclosure remain the parent's separate tasks. This review must not be used to remove experimental status, declare source-assimilated BE completion, or claim the entire paper/PDE formalized.

Failure class for the assigned review: NONE. Initial D-drive sandbox access failed; a scoped read-only escalation succeeded. Two read-only diagnostic command mistakes (a PowerShell pipeline syntax error and a hash helper colliding with the `h` alias) were corrected; failed attempts supplied no evidence and wrote nothing. No fetch, network, scripts/Python, compilation, Git writes, policy edits, old artifact edits, or subagents occurred. Only this new three-file review directory is authored. Mathematical delta/root advance: none; useful output is bounded preservation evidence. Salvage/purification/Exposition Seal: not an authoring or research-completion run. STOP after freeze.
