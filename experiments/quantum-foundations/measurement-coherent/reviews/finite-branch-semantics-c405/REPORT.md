# Independent finite-branch semantic and canonicality review

## Verdict and scope

**ACCEPT within the reviewed static mathematical scope.** The exact candidate implements the supplied original finite coherent-branch contract, without an excess logical premise or a second measurement/state/tensor API. It is a useful narrow adapter from operator completeness to Mathlib's existing finite Hilbert-product `LinearIsometry`. Its overlap theorem genuinely consumes that assembled isometry. This is not a production-admission, independent-compilation, full-paper, novelty, or PURIFIED verdict.

Reviewer: `/root/finite_branch_semantics_c405`, distinct from formalizer `/root/measurement_coherent_c403` and decoder `/root/finite_branch_blind_c404`. These slash-prefixed names are canonical agent task identities, not filesystem paths. The review belongs to the current delegated agent run; no separate runtime run identifier was exposed and none is invented.

All artifact names below are logical artifact names or repository-relative names. `measurement-coherent-c403/QuantumBlockEncoding/MeasurementCoherent.lean` is an experimental candidate artifact, not a production repository module merely because its namespace resembles one. The actual candidate was read in full and its **whole 2,121-byte file** hashes to `22ef9784a3fe636b9ea07cf622bce01572425e2706e540e547934ec078dba34c`.

## 1. Independent comparison sequence and evidence limits

After reading repository instructions and protocols, I read the comparison inputs in this order:

1. `measurement-coherent-c403/SOURCE_CONTRACT-v1.md`, whole-file SHA-256 `30b503b61d67e44deaa7c8e9fd4fcf520b5bcd3ce5cb4783e152babce51ff85b`.
2. `measurement-coherent-c403/FORMAL_PACKET-v1.md`, whole-file SHA-256 `2a1af6af46029820d070b3818a787b74414a28224acc976bf01265f88342aa79`.
3. The exact candidate source identified above.
4. `finite-branch-blind-c404/REPORT.md`, whole-file SHA-256 `bd7aa0f9d585fa2f1207088b3fb3c035ba206793ca325eff1f1b0782b324d36c`.

All supplied expected hashes matched actual bytes. I formed the source-first construction comparison before consulting implementation-dependent interpretations, and formed my semantic/canonicality assessment before reading later decoder display metadata. No author handoff, implementation claim/verdict, prior sibling reviewer verdict, or requested desired verdict was used. I read the reused predecessor in full and inspected the actual local Mathlib APIs, not just descriptions of them.

The source contract identifies itself as a comparison view of the already frozen `STATEMENT_SEAL-v1.md`, with digest `dfeff3145f5f0bf3010b4ad211e80bbc679551607635f2da2e24138e919661e3`. I did not create or change a target. That original seal's bytes and its historical pre-proof chronology were not independently audited here; the identified digest is a provenance assertion in the reviewed source view, not an additional actual-input pin.

I ran no Lean compilation, Git operation, package installation, network retrieval, or subagent. No formalizer execution artifact was read or adopted as independent evidence. A later parent message about focused compilation does not change this report's evidence layer. Source scans found no `sorry`, `admit`, declared `axiom`, `native_decide`, `unsafe`, or `set_option` in the candidate; this is a static observation, not a transitive proof-term axiom audit.

The repository `qbe-substantive-worker` instructions influenced this review by keeping source topology, visible Lean references, canonical reuse, mathematical scope and integration gates separate. They did not authorize source edits or relax any gate. `INPUT_PINS.json` records actual whole-file hashes and distinguishes full reads from excerpt inspections.

## 2. Source-first contract and binder audit

The mathematical contract is precisely: for any finite, possibly empty type `ι`, any independent complex Hilbert spaces `E,F`, and any bounded complex-linear family `M_i : E → F` satisfying

\[
\sum_{i\in\iota}M_i^\dagger M_i=I_E,
\]

construct the literal tuple map `Vψ = (M_i ψ)_i` into the finite Hilbert product, bundle it as a complex-linear isometry, expose its exact coordinates, and derive full complex overlap preservation through that isometry for arbitrary `ψ,φ`.

| Public input | Classification and finding |
| --- | --- |
| Types `ι,E,F` | TYPING; `E` and `F` are not identified. |
| `[Fintype ι]` | TYPING for the finite outcome carrier; does not imply nonemptiness. |
| Normed additive group, complex inner-product, and completeness instances on both spaces | TYPING for the stipulated Hilbert spaces. Mathlib's bundled `ContinuousLinearMap.adjoint` requires completeness of both spaces. This is not an added finite-dimensionality or nontriviality premise. |
| `M : ι → E →L[ℂ] F` | SOURCE-supplied family; boundedness and complex linearity are carried by the existing Mathlib type. |
| `hM : ∑ i, (M i).adjoint.comp (M i) = 1` | SOURCE, exactly the supplied input-space completeness equation. |
| `ψ,φ : E`, and `i : ι` where present | Unrestricted universally quantified vectors/coordinate index, not normalization or nonzero assumptions. |

There are no project-owned Prop aliases or structures to hide extra hypotheses. No SOURCE proof ingredient was moved into a convenient additional binder. In particular the norm identity, overlap identity, normalization of the input, nonzero branches, dimension comparison and surjectivity are not hypotheses of the construction. There are no STANDING, RULED, or EXCESS logical premises.

Completeness is mathematically the right condition, not arbitrary convenience: for the literal tuple map, preservation of all overlaps gives `⟨ψ,(∑ M_i†M_i)φ⟩ = ⟨ψ,φ⟩` for all vectors, hence the operator identity by nondegeneracy. Norm preservation implies those overlaps by complex linearity/polarization. This necessity explanation is mathematical review, not an extra Lean theorem claimed in the candidate. No stronger mathematical minimality claim about alternative APIs for noncomplete spaces is made.

### Contract-construction coverage

Before inspecting the implementation, the contract suggested the route: form the finite tuple; use pointwise linearity; compute its squared norm as the sum of branch squared norms; apply the stipulated completeness relation; use complex-linear isometry preservation of inner products. That source-first route is separate from the source-reference account in Section 4. This original short contract contains no external paper proof whose historical topology is being reconstructed.

| Source region | Disposition |
| --- | --- |
| Frozen-contract provenance paragraph | Provenance only; no new target or external-source equivalence. |
| Finite/empty outcome and arbitrary Hilbert carriers | NODE: ambient quantifiers and edge-case audit. |
| Bounded family and input completeness equation | NODE: sole mathematical assumption. |
| Displayed `V_M` formula | NODE: literal branch collection into the finite Hilbert product. |
| Isometry, coordinate action, and displayed overlap formula | NODE: construction and two public consequences. |
| No normalization/nonzero/nonempty/finite-dimensional/equal-dimension premises | NODE: binder-minimality checks above. |
| Whole tuple rather than sum in `F`; conjugate-first convention | NODE: literal/phase audit below. |
| Coherent bookkeeping motivation | Interpretation supported at the linear-map/overlap layer; not a circuit or coherent-oracle access theorem. |
| Tensor, unitary/dilation, channel, density/trace, branch normalization, circuit, access, cleanup, resources, finite-bit exclusions | EXCLUDED from the target, explicitly retained as nonclaims. |

There is no unresolved mathematical source gap within this short target. Operational extensions are excluded boundaries, not discharged obligations.

## 3. Literal definition, convention and edge-case checks

`branchIsometry` is **literal**, not characterized-by-choice or quotient/representative-defined. Its body is `WithLp.toLp 2 (fun i => M i ψ)`. `WithLp.toLp` stores the supplied tuple with the inherited pointwise algebraic structure; it does not pick a basis, reorder indices, divide by norms, choose phases, supply a default branch, or identify a tensor register. `branchIsometry_apply` is `rfl` on the entire public carrier. Its proof parameter changes no coordinates. The `noncomputable` marker is not a fallback semantics or an efficiency theorem.

The scalar is exactly `ℂ`. `.comp (M i)` applies `M_i` first and its adjoint second, so `1` is `I_E`, not `I_F`. Mathlib's actual `inner_smul_left` and `inner_smul_right` confirm conjugate linearity in the first slot and linearity in the second. The checked API statements are `⟨x,A†y⟩ = ⟨Ax,y⟩` and `PiLp.inner_apply : ⟨x,y⟩ = ∑ i, ⟨x_i,y_i⟩`.

Consequently the desired equation has the correct complex orientation:

\[
\sum_i\langle M_i\psi,M_i\phi\rangle
=\left\langle\psi,\left(\sum_iM_i^\dagger M_i\right)\phi\right\rangle
=\langle\psi,\phi\rangle.
\]

The source does not replace this by its real part. A useful sign discriminator is `φ = i ψ`: both sides must be `i ‖ψ‖²`, not its conjugate. The tuple also carries superpositions with their original coefficients. Multiplying different supplied `M_i` by independent unit phases can preserve every probability while changing the tuple's relative coordinate phases. The construction is canonical **for the supplied family**, not canonical for a probability distribution or equivalence class of operator families.

| Case | Finding |
| --- | --- |
| Empty `ι` | The hypothesis becomes `0 = I_E`, forcing every input vector to be zero. The target is the unique empty tuple. The coordinate theorem is vacuous; there is no silently assumed witness for nonzero `E`. |
| Zero input vector | Every branch is zero, with no division or normalization. |
| Zero `E` | The hypothesis holds for the unique zero maps; the zero-source isometry exists for any allowed finite outcome type and `F`. It need not be onto a nonzero product. |
| Zero `F` or all-zero family | The premise forces `E` to be zero. No contradiction is hidden by a fallback output. |
| Rectangular maps | `E,F` are independent. Two coordinate projections from `ℂ²` to `ℂ` satisfy completeness and collectively give an isometry although each branch is noninjective. |
| Infinite-dimensional `E` and/or `F` | Allowed by both the signature and the used adjoint/isometry APIs. The sum remains finite; no infinite-series or finite-dimensional-matrix step is smuggled in. |
| Singleton outcome | Gives an ordinary isometric embedding, not automatic surjectivity. |
| Zero or overlapping individual branches | Permitted. Distinct coordinate subspaces in the product are orthogonal; the branch vectors inside the same `F` need not be orthogonal. |

For example `M_0=I, M_1=0` gives `ψ ↦ (ψ,0)` with a proper range for nonzero `E=F`. Also `M_0=M_1=I/√2` gives a tuple isometry, while summing its two coordinates in `F` scales the input by `√2`. These are algebraic discriminators, not executed simulations or new checked Lean examples. They rule out the tempting interpretations “unitary,” “each branch is an isometry,” and “sum the branches in `F`.”

## 4. Actual predecessor and Mathlib use

The complete predecessor file reviewed was repository-relative `experiments/quantum-foundations/measurement-completeness/QuantumBlockEncoding/MeasurementProbability.lean`, actual whole-file SHA-256 `33c1a01b8f1e752f22acbc12ae47faa503e5dc7ae5f3f4d73dff39eeb9505775`. It proves the unnormalized identity `∑ i, ‖M_i ψ‖² = ‖ψ‖²` by the adjoint relation, finite sum and `hM`. Its separate normalized-input probability bound is not imported as an extra premise or confused with the candidate's arbitrary-input contract. This review does not re-admit the predecessor's external attribution or publication history.

The candidate's visible source route is:

1. `WithLp.toLp` supplies the exact tuple; pointwise additivity and complex scalar compatibility come from each bounded linear map.
2. `PiLp.norm_sq_eq_of_L2` turns its squared norm into the branch sum.
3. `MeasurementProbability.sum_norm_sq_eq` supplies that sum's equality with the input squared norm.
4. `sq_eq_sq₀` cancels squares using both norms' nonnegativity, yielding the `norm_map'` field of the actual assembled `LinearIsometry`.
5. `sum_inner_eq` applies `(branchIsometry M hM).inner_map_map ψ φ` and simplifies only `PiLp.inner_apply` and the literal coordinate theorem.

The last step is a **genuine consumer** of the assembled map. It is not a separately proved adjoint-sum identity followed by an unused isometry wrapper; its proof expression explicitly invokes that map. Mathlib's actual `LinearIsometry.inner_map_map` uses the polarization identity, so the passage from all-vector norm preservation to full complex overlaps is justified by the library interface. `branchIsometry_apply` is necessary coordinate bookkeeping, not an independent substantive mathematics credit. The isometry assembly and its overlap consequence together are the modest reusable delta; counting each helper as a separate discovery would overstate it.

This is a source-visible dependency account, **not** an elaborated theorem-dependency export. It demonstrates the conceptual and written proof use of the predecessor; compilation must separately confirm that the imported declaration resolves to the pinned provider rather than a stale or shadowed artifact.

Actual Mathlib statements inspected include:

- `PiLp`/`WithLp` carrier and coordinate algebra, `PiLp.norm_sq_eq_of_L2`, product completeness and `PiLp.inner_apply`;
- `ContinuousLinearMap.adjoint`, both adjoint inner relations, and `apply_norm_sq_eq_inner_adjoint_left`;
- the actual `LinearIsometry` structure and `LinearIsometry.inner_map_map`;
- `LinearMap.isometryOfInner`, `LinearMap.norm_map_iff_inner_map_map`, and `ContinuousLinearMap.inner_map_map_iff_adjoint_comp_self` / `norm_map_iff_adjoint_comp_self` as nearby general-purpose alternatives;
- `sq_eq_sq₀` with its two nonnegativity hypotheses.

The read toolchain says Lean `v4.33.0`; the read manifest records Mathlib revision `db584cd6d46c92f209a44c0f1c829460d327499d`. I pinned the actual inspected dependency-file bytes; the manifest's declared revision is not a Git verification of the working tree and no binary freshness claim follows from it.

## 5. Bounded reuse and canonicality assessment

The bounded local search covered Lean sources under repository `QuantumBlockEncoding/` and `experiments/`, using the exact candidate/predecessor names, coherent-branch and branch-isometry phrases, sums of adjoint compositions, and `PiLp`/isometry interfaces. The scoped Mathlib search covered `Mathlib/Analysis/InnerProductSpace/`, `Mathlib/Analysis/Normed/Lp/` and the order lemma needed for square cancellation. Search results and selected definitions, not every source file in those trees, were reviewed.

No existing exact finite-family adapter with this completeness premise and literal tuple output was found in that bounded search. This is **not** an exhaustive library or literature novelty claim. Local real matrix orthogonal-completion and thin-LQ interfaces, inspected in `QuantumBlockEncoding/RealIsometryCompletion.lean` and `QuantumBlockEncoding/ThinLQ.lean`, use related `PiLp` substrate but have different real, finite-dimensional matrix contracts. They do not replace this arbitrary complex Hilbert-family adapter.

Mathlib already provides the essential mathematics and bundles. `isometryOfInner` and adjoint/isometry equivalences are alternative implementation substrates, not missing new quantum foundations. The submitted route appropriately reuses the predecessor's norm equality and then the generic inner-preservation theorem instead of copying either proof. `PiLp` congruence/reindexing interfaces found by search are not a family-assembly theorem with the present premise.

Canonical status within this scope: **acceptable narrow shared-node candidate, not wrapper-only manufacture**. There is one literal map, one coordinate adapter, and one actual internal consumer. No new state, tensor, measurement, density or channel structure is introduced. No genuine production downstream consumer, full external-library reuse audit, or post-integration duplicate/dead-code audit has been established by this bounded static review. Do not label the canonical-library production gate or purification complete just because an internal consumer exists. Generalization to arbitrary `RCLike` fields or outcome-dependent output spaces is optional future design, not a missing condition of this frozen complex, common-output contract.

The accurate direction is predecessor completeness lemma → branch isometry → full-overlap consumer. The new interface demonstrates and extends the usefulness of the prior completeness node; it does not retrospectively prove its publication gates, make the predecessor depend on its consumer, or close a higher physical construction. A compressed reader spine may display that three-stage mechanism while retaining the exact assumptions and expansion references. No functor, transport equivalence or novelty follows from that display.

## 6. Decoder round trip and public-safe display binding

The independent decoder reconstruction agrees with the contract and exact implementation on the quantifiers, adjoint order, arbitrary input pairs, literal tuple, conjugate-first convention, branch-phase freedom between different families, edge cases and isometry-versus-unitary boundary. Its derived contraction and dimension observations are consequences, not extra assumptions or additional declarations in the candidate. I found no semantic disagreement requiring repair.

The original decoder report and freeze contain private path spellings and are therefore not themselves public-safe presentation artifacts. After my own comparison, I independently read and hashed their separately authored public-display derivations:

- `finite-branch-blind-c404/PUBLIC_REPORT.md`: `3d06420ed667c8b8fbe5d69cd741d119cd5803f9271c2f2eebfaf0a17a411075`.
- `finite-branch-blind-c404/PUBLIC_FREEZE.json`: `81a5b4b16bd05864e22e9f76314013ef684a5402471b78c9c1625f70ad5e61a6`.

I verified exact text equality of the reproduced report body with the original after the specified input-path-to-logical-name substitution, excluding the explicit added display notice. I also verified structural JSON equality of the embedded original freeze with the actual original after only logical-path substitutions. The original freeze's actual hash is `43bda5da6243ace0d6710cf7fd4423634728c0116c078a3f0645b0b0fe1b4265`. The public report scan found no drive-absolute path spelling.

These observations preserve the original decoder identity, mathematics and original hashes; they do not invent a new independent decoder run or verdict. Publication must use the separately identified display artifacts while retaining the immutable original bindings. It must not silently replace the original hash by the public report's different hash.

## 7. What remains before production/QA admission

No additional mathematical premise is needed for the reviewed target. The remaining conditions are evidence and integration gates, not a request to strengthen the theorem:

1. Compile the exact candidate, exact predecessor provider, signatures and real consumers in the actual pinned runtime/context; record commands, exits and full source/dependency bindings. Confirm complete elaborated binder types, declaration inventory and transitive axiom/native disclosures. This reviewer has not performed that execution.
2. Establish the original Statement Seal's actual binding and pre-proof provenance, the final-signature association, explicit binder/definition and source-coverage records, and an honest whole-module publication packet with distinct formalizer/decoder/reviewer identities. Preserve the actual-byte pins here; re-review changed scientific inputs.
3. Integrate at a maintainer-selected canonical location/import boundary and record actual graph deltas. The candidate currently lives only in an experimental packet. Avoid duplicate semantic APIs, prove any required adapters, demonstrate the intended downstream integration or keep the limited internal-consumer status explicit. Source-visible references do not substitute for the compiler-backed graph evidence.
4. Run the repository's required `lake build`, `lake build Tests`, publication/atlas checks, full documentation/site/link/path-leakage gates and applicable browser/reader/CI checks on the integrated, source-bound candidate. Focused compilation is not these gates.
5. Provide an authored theorem-linked mathematical lesson with the same empty/zero/rectangular/infinite-dimensional, phase and excluded-operational semantics, plus linked exact Lean disclosures. Use the separately bound public-safe decoder display artifacts and scan the complete public packet for private paths; this report contains no private mapping.
6. After integration, perform dead/duplicate/wrapper/import/consumer cleanup and the independent Exposition Seal, retaining the lossless source and Lean drill-down. Only then can PURIFIED be considered. A small clean-looking file before integration is not that audit.

Tensor/register identifications, a surjective unitary or dilation, instruments/channels, density/trace semantics, normalized selected branches, physical circuits, coherent oracle access, ancilla cleanup, resource complexity and finite-bit algorithms remain outside this contract. They are not mandatory new tasks for admitting this small node, but any future claim about them needs its own explicit definitions, hypotheses, bridges and gates. Nothing here proves a full source paper or physical measurement implementation.

## 8. Compact handoff

- Objective/frontier: independently assess the finite coherent-branch candidate against its original mathematical contract and decoder round trip.
- Mathematical delta accepted: literal finite Hilbert-product isometry assembled from the predecessor's completeness norm identity, with exact coordinates and a genuine full-complex-overlap consumer.
- Failure class: `NONE` for this static semantic comparison; compilation/integration were not executed, not refuted.
- Salvage/rejected routes: no cleanup or salvage was performed; probability-only, sum-in-`F`, branchwise-isometry, surjective-unitary and physical-implementation readings are rejected as interpretations of this interface.
- Direction fingerprint: anti-anchored contract → formal interface → exact implementation → independent decoder comparison, then actual Mathlib and bounded canonicality checks; no duplicated proof search.
- Process-memory IDs: none consulted; no mathematical route selection or new dispatch occurred.
- Parallel/common-blind-spot scope: no subagents spawned. This is a distinct semantic uncertainty from the formalizer's execution and the decoder's reconstruction, not a comparison of competing construction routes.
- Default route: the submitted predecessor-norm → assembled-isometry → overlap route is suitable for this target; no exclusive superiority claim over other valid Mathlib proofs.
- Purification/Exposition Seal: pending integration; not issued here.
- Residual risk: low mathematical mismatch risk within the pinned small contract; actual elaboration, import resolution, transitive trust, publication chronology and production integration require their separate evidence.
- Recommendation: retain as an accepted experimental preparatory/canonical-adapter candidate; advance to source-bound compilation/publication/integration checks without expanding its scientific claim.
