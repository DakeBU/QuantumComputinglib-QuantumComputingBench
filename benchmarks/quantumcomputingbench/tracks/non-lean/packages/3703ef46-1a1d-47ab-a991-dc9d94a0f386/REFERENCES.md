# Batch 2 — reference solutions and rubrics

Read QUESTIONS.md separately when attempting the problems. References are public authored mathematics with the content-bound review status in review-index.json.

## E1 — Residual-certified mass through preparation and clean projection

### Reference solution

For any real matrix \(Z\) of the appropriate size, submultiplicativity and transpose invariance of the induced Euclidean operator norm give
\[
\lVert T_j(Z)\rVert\le\sum_t\lVert A_j^t\rVert^2\lVert Z\rVert\le L_j\lVert Z\rVert.
\]
The same estimate applies to \(T_j(Z-Z')\), since the transfer map is linear. No positivity, symmetry or canonicality of the approximate environments is used.

Set \(D_j=\widehat E_j-E_j\) and \(R_j=\widehat E_{j-1}-T_j(\widehat E_j)\). The terminal condition gives \(D_n=0\), and subtracting recurrences gives
\[
D_{j-1}=R_j+T_j(D_j),\qquad
\lVert D_{j-1}\rVert\le\varepsilon_j+L_j\lVert D_j\rVert.
\]
Define \(\beta_n=0\) and \(\beta_{j-1}=\varepsilon_j+L_j\beta_j\). Backward induction proves \(\lVert D_j\rVert\le\beta_j\), and expanding the scalar recurrence yields
\[
\boxed{\beta=\beta_0=\sum_{j=1}^n\varepsilon_j\prod_{k=1}^{j-1}L_k.}
\]
All factors are nonnegative. The first residual has coefficient \(1\); the second has \(L_1\); the last is amplified by \(L_1\cdots L_{n-1}\). The initial matrices are scalar, so their operator norm is the absolute value of their entry. With the supplied Gram identity,
\[
\bigl|\widehat E_0(1,1)-\lVert x\rVert^2\bigr|=\lVert D_0\rVert\le\beta.
\]
For \(n=0\), the sum is empty, \(\beta=0\), and \(E_0=\widehat E_0=I_1\). The single empty-word amplitude is \(1\).

The propagation weights cannot be discarded even when all approximate scalar environments are nonnegative. Take two scalar-bond cores
\[
A_1^0=2,\quad A_1^1=0,\quad A_2^0=A_2^1=0.
\]
Then \(x=0\), \(E_2=1\), and \(E_1=E_0=0\). Set
\[
(\widehat E_0,\widehat E_1,\widehat E_2)=(4,1,1),\quad
(L_1,L_2)=(4,0),\quad(\varepsilon_1,\varepsilon_2)=(0,1).
\]
These certificates hold: \(R_1=4-4\cdot1=0\) and \(R_2=1-0=1\). The correct \(\beta=4\) gives \(m=0\). Replacing it by \(\sum_j\varepsilon_j=1\) would falsely report positive mass \(4-1=3\) for the zero vector. This diagnostic does not satisfy the active \(m>0\) premise.

Now retain the active branch. The certified interval implies
\[
\lVert x\rVert\ge\sqrt m>0,\qquad
\lVert y\rVert\ge\lVert x\rVert-\lVert x-y\rVert
\ge\sqrt m-\delta>0.
\]
Thus both vectors are nonzero before normalization. The vectors \(\psi=x/\lVert x\rVert\) and \(\phi=y/\lVert y\rVert\) are unit, and the supplied stability inequality gives
\[
\lVert\phi-\psi\rVert\le\frac{2\lVert x-y\rVert}{\lVert x\rVert}
\le\frac{2\delta}{\sqrt m}.
\]
This retains signed real amplitudes as exact representatives.

Write \(\xi=|0^{a+n}\rangle\). The actual aligned-list estimate, the exact preparation action and the isometry of \(J\) give
\[
\Omega-J\psi=(V-U)\xi+J(\phi-\psi),\qquad
\lVert\Omega-J\psi\rVert\le\gamma+\frac{2\delta}{\sqrt m}=\tau.
\]
Independently, \(V\) is unitary, so \(\lVert\Omega\rVert=1\), while \(\lVert J\psi\rVert=1\). Both full-output norms matter below.

Set \(z=J^\dagger\Omega\) and \(\ell=(I-P)\Omega\). Since \(J^\dagger J=I\), the operator \(P=JJ^\dagger\) is an orthogonal projector and
\[
\Omega=Jz+\ell,\qquad J^\dagger\ell=0,\qquad
\lVert z\rVert^2+\lVert\ell\rVert^2=1.
\]
The Born success probability is \(p=\lVert z\rVert^2\). Put \(q=\lVert z\rVert\le1\) and \(h=\operatorname{Re}\langle\psi,z\rangle=\operatorname{Re}\langle J\psi,\Omega\rangle\). The squared distance of the full unit vectors gives
\[
2-2h=\lVert\Omega-J\psi\rVert^2\le\tau^2,
\qquad h\ge1-\tau^2/2>0.
\]
The final strict inequality uses \(\tau<1\). Cauchy–Schwarz then gives
\[
q\ge|\langle\psi,z\rangle|\ge h\ge1-\tau^2/2>0.
\]
The clean branch is therefore nonzero before conditioning, and
\[
\boxed{p=q^2\ge(1-\tau^2/2)^2.}
\]

The normalized accepted joint vector is \(J(z/q)\), so \(\psi_{\mathrm{acc}}=z/q\). Because \(h>0\) and \(q\le1\),
\[
\lVert\psi_{\mathrm{acc}}-\psi\rVert^2
=2-\frac{2h}{q}\le2-2h
=\lVert\Omega-J\psi\rVert^2\le\tau^2.
\]
Consequently \(\boxed{\lVert\psi_{\mathrm{acc}}-\psi\rVert\le\tau}\). This exact-representative argument does not minimize over phase. It also does not erase the rejected branch before measurement. The weaker leakage estimate \(\lVert\ell\rVert\le\tau\) would only yield \(p\ge1-\tau^2\); by itself it does not establish the stronger requested bounds.

The threshold \(\tau<1\) is sufficient. The same reasoning has \(h>0\) for every \(\tau<\sqrt2\), including \(\tau=1\), where it gives \(p\ge1/4\). A loose bound above \(1\) does not imply failure. For zero success at actual distance \(\sqrt2\), take \(n=0\), \(a=1\), \(x=y=(1)\), \(U=R(0)\) and \(V=R(\pi)\) on the sole ancilla. Then
\[
U|0\rangle=|0\rangle,\quad V|0\rangle=|1\rangle,\quad
P=|0\rangle\langle0|,\quad p=0,\quad
\lVert|1\rangle-|0\rangle\rVert=\sqrt2.
\]
The lists are aligned with \(d_1=\pi\) and conservative \(\gamma=\pi/2\), so this example deliberately lies outside the active \(\tau<1\) branch. Every unit vector perpendicular to the clean subspace has distance \(\sqrt2\) from every clean unit target.

If every residual certificate is zero, then \(\beta=0\) and the initial approximate entry is exact mass. That mass may still vanish; normalization continues to require \(m>0\). If \(\delta=0\), then \(y=x\). If \(\gamma=0\), then \(V=U\) in operator norm. If both errors vanish in the active branch, then \(\Omega=J\psi\), \(p=1\), and the accepted vector is exact. For \(n=0\), one has \(x=(1)\), \(\beta=0\), \(m=1\); the real scalar \(y\) is positive under \(\delta<1\), so \(\phi=\psi=(1)\). This is a one-dimensional system, not an empty vector. For \(a=0\), \(P=I\) and \(p=1\). A zero internal bond makes every full contraction zero; the certified interval forces \(m\le0\). It cannot satisfy the active normalization branch, and no zero vector is normalized.

The conclusion needs the complete conjunction of certified residuals and transfer bounds for the displayed exact cores, the Gram interpretation as the particular raw vector, positive certified mass, raw-data error to the particular second vector, complete exact preparation, actual unitary positional alignment and the specified projector. The proof constructs no floating-point residual certifier, rounded Gram algorithm, raw-data or norm supplier, preparation circuit, angle supplier, finite-gate-set compiler or runtime bound. The stored exact-real Gram source does not itself certify numerical residuals.

### Partial credit

- **2 points:** Proves the transfer bound, signed residual recurrence and backward induction, obtaining \(\beta=\sum_j\varepsilon_j\prod_{k<j}L_k\) with the correct product orientation and \(n=0\) convention. An unweighted or reversed product earns no propagation-formula credit.
- **1 points:** Gives a legal concrete scalar-bond false-certificate example, verifies its residuals and transfer bounds, and shows that the unweighted positive mass is false while the correct certificate does not imply positivity.
- **1.5 points:** Uses the Gram interpretation and \(m>0\) to establish \(x\ne0\), proves \(\lVert y\rVert\ge\sqrt m-\delta>0\) before normalization, and correctly invokes the supplied stability result. No proof of the supplied result is required.
- **1 points:** Combines the actual action \(U\xi=J\phi\), aligned operator error and data-normalization error to obtain \(\lVert\Omega-J\psi\rVert\le\tau\), retaining complete workspace and full unit norms.
- **2.5 points:** Derives the branch decomposition, uses positive real overlap \(h\ge1-\tau^2/2\) and \(q\le1\) to prove \(q>0\) before conditioning, and proves both \(p\ge(1-\tau^2/2)^2\) and accepted error at most \(\tau\). Equivalent complete geometric arguments earn full credit. The weaker \(1-\tau^2\) or \(2\tau\) bounds alone do not prove the requested conclusion.
- **1 points:** Treats \(\tau<1\) as sufficient, supplies a unitary zero-success example at actual distance \(\sqrt2\) in a separate regime, and handles \(n=0\), \(a=0\), zero errors/residuals and internal zero bonds without contradictory positive-mass premises.
- **1 points:** Keeps residual certification, raw error, actual complete preparation, alignment and projection as distinct required interfaces; distinguishes the mathematical estimate from an unprovided finite-bit supplier, compiler or runtime theorem.

Equivalent valid mathematical arguments receive the same substantive credit. Evidence status and formal identifiers are in the complete QA packet, outside the question.

### Boundary cases

- **case:** n=0 **scope:** valid specialization **conclusion:** One scalar amplitude 1, β=0, m=1; y>0 under δ<1; no empty state vector.
- **case:** a=0 **scope:** valid specialization **conclusion:** P=I and p=1; accepted vector is the whole unit output.
- **case:** all ε_j=0 **scope:** raw statement plus active branch if mass positive **conclusion:** β=0 and approximate initial mass equals true mass, which may still vanish.
- **case:** δ=γ=0 **scope:** active positive-mass branch **conclusion:** Exact complete clean target, p=1 and zero accepted error.
- **case:** zero internal bond or zero raw vector **scope:** diagnostic excludes m>0 **conclusion:** True mass 0 and certified m≤0; normalized target undefined.
- **case:** τ=1 or 1<τ<√2 **scope:** replace τ<1; retain other interfaces **conclusion:** Same positive-overlap proof still supplies the bounds; τ<1 was not claimed necessary.
- **case:** actual output distance √2, zero clean success **scope:** replace τ<1 by explicit aligned Ry(π) witness **conclusion:** No accepted state exists; full output is orthogonal to clean target.

### Common errors

- **error:** Use β=Σ ε_j or suffix rather than preceding-core amplification. **why wrong:** Residual at j is transported through T_1,...,T_{j−1}; large earlier cores can amplify it.
- **error:** Treat Ē_0≥0 or an approximate Gram matrix as automatically certifying positive true mass. **why wrong:** Only Ē_0−β is a validated lower bound; approximate-environment positivity is neither given nor sufficient.
- **error:** Normalize y before proving nonvanishing, or use small absolute δ without a positive certified margin. **why wrong:** The checked inequality δ<√m≤||x|| is the required nonzero producer.
- **error:** Replace actual circuit alignment with a generic assertion that angles are close. **why wrong:** Instruction order, target wires, list positions and exact phases are part of the supplied operator certificate.
- **error:** Apply a generic normalized-branch lemma to get only 2τ and claim it proves the requested τ bound. **why wrong:** The sharper result uses both full-output unit norms and positive real overlap h, together with q≤1.
- **error:** Assert τ=1 allows zero success or import τ<1 into the √2 witness. **why wrong:** τ<1 is sufficient, not sharp; the diagnostic replaces that premise.
- **error:** Use the source exact-real Gram routine as a floating-point error certifier. **why wrong:** It provides exact semantics and exact-real cost, not numerical certificates.

### Author-supplied reasoning map

These are declared mathematical inputs and scoped claims, not extracted Lean proof-term dependencies.

#### Inputs

- **E1-I1** (assumption): Finite real scalar-boundary cores, fixed word order, exact recurrence E_n=I and E_{j−1}=T_j(E_j); zero internal dimensions and one empty word allowed.
- **E1-I2** (assumption): Ē_n=I and certified ||Ē_{j−1}−T_j(Ē_j)||≤ε_j, Σ_t||A_j^t||²≤L_j, ε_j,L_j≥0.
- **E1-I3** (supplied_interface): E_0(1,1)=||x||².
- **E1-I4** (assumption): After β is derived, m=Ē_0−β>0 and ||x−y||≤δ<√m with δ≥0; active normalization branch only.
- **E1-I5** (supplied_interface): For nonzero u,v in the same finite Euclidean space, ||N(u)−N(v)||≤2||u−v||/||u||.
- **E1-I6** (assumption): Actual U,V unitary lists on K⊗H with same positional types/targets, only Ry angle errors d_k≥0; other gates/phases identical, chronological first-rightmost convention.
- **E1-I7** (supplied_interface): Under I6, ||V−U||≤γ=(1/2)Σ_k d_k.
- **E1-I8** (assumption): Jv=|0^a⟩⊗v, P=JJ† and ξ=|0^{a+n}⟩, all work in K; after φ is defined, Uξ=Jφ.
- **E1-I9** (assumption): τ=2δ/√m+γ<1, only imposed for the main conditional-output branch.
- **E1-I10** (convention): Exact vector representatives and conjugate-first inner product; Euclidean norm inequalities; Born probability for the stated orthogonal projector.

#### Steps

- **E1-S1: Bound each linear transfer map.** Inputs: E1-I1, E1-I2, E1-I10. Scope: active_or_raw_as_named. Conclusion: ||T_j(Z)||≤L_j||Z|| for every real Z of the right size. Justification: Triangle, submultiplicativity and transpose norm invariance.
- **E1-S2: Propagate certified residuals backwards.** Inputs: E1-I1, E1-I2, E1-S1. Scope: active_or_raw_as_named. Conclusion: D_n=0, D_{j−1}=R_j+T_j(D_j); ||D_0||≤β=Σ_j ε_jΠ_{k<j}L_k. Justification: Backward induction with β_n=0, β_{j−1}=ε_j+L_jβ_j, then scalar unrolling.
- **E1-S3: Certify a true raw-mass interval.** Inputs: E1-I1, E1-I3, E1-S2. Scope: active_or_raw_as_named. Conclusion: |Ē_0(1,1)−||x||²|≤β; the lower endpoint is m=Ē_0−β. Justification: The initial matrix is scalar so its operator norm is entry absolute value.
- **E1-S4: Refute dropping amplification weights.** Inputs: E1-I1, E1-I2, E1-S2, E1-S3. Scope: diagnostic: do not assume E1-I4 or positive mass. Conclusion: The explicit two-core zero train has Ē_0=4, Σ ε=1 but β=4 and true mass 0. Justification: Instantiate A_1^0=2,A_1^1=0,A_2^t=0, Ē=(4,1,1), ε=(0,1), L=(4,0).
- **E1-S5: Establish nonzero targets from the certified margin.** Inputs: E1-I1, E1-I4, E1-I10, E1-S3. Scope: active_or_raw_as_named. Conclusion: ||x||≥√m>0 and ||y||≥√m−δ>0. Justification: Monotone square root and reverse triangle before any normalization.
- **E1-S6: Consume normalization stability.** Inputs: E1-I1, E1-I4, E1-I5, E1-I10, E1-S5. Scope: active_or_raw_as_named. Conclusion: ψ,φ are unit and ||φ−ψ||≤2δ/√m. Justification: Apply the supplied interface only after S5 establishes both denominators positive.
- **E1-S7: Compose data and actual circuit errors.** Inputs: E1-I4, E1-I6, E1-I7, E1-I8, E1-I10, E1-S5, E1-S6. Scope: active_or_raw_as_named. Conclusion: Ω=Vξ is unit and ||Ω−Jψ||≤τ=2δ/√m+γ. Justification: Split Ω−Jψ=(V−U)ξ+J(φ−ψ); ξ and J preserve the required unit norms.
- **E1-S8: Decompose the actual full output.** Inputs: E1-I6, E1-I8, E1-I10, E1-S7. Scope: active_or_raw_as_named. Conclusion: z=J†Ω, ℓ=(I−P)Ω, Ω=Jz+ℓ, q²+||ℓ||²=1, q=||z||≤1, p=q². Justification: J†J=I yields orthogonal projection and norm decomposition; use Born rule.
- **E1-S9: Produce the clean nonzero branch and success bound.** Inputs: E1-I8, E1-I9, E1-I10, E1-S6, E1-S7, E1-S8. Scope: active_or_raw_as_named. Conclusion: h=Re⟨ψ,z⟩≥1−τ²/2>0, q≥h>0 and p≥(1−τ²/2)². Justification: Expand squared distance of the full unit outputs, then Cauchy–Schwarz. τ<1 is checked before dividing by q.
- **E1-S10: Normalize and retain the sharp vector error.** Inputs: E1-I8, E1-I9, E1-I10, E1-S6, E1-S7, E1-S8, E1-S9. Scope: active_or_raw_as_named. Conclusion: ψ_acc=z/q is defined and ||ψ_acc−ψ||²=2−2h/q≤2−2h≤τ². Justification: q≤1 and h>0 imply h/q≥h. This is exact-representative geometry, not phase minimization.
- **E1-S11: Check unnormalized boundaries.** Inputs: E1-I1, E1-I2, E1-I3, E1-S2, E1-S3. Scope: raw/diagnostic branch: E1-I4 not assumed. Conclusion: n=0 gives β=0 and mass1; zero residuals give exact mass; a zero internal bond gives mass0 and m≤0. Justification: Empty sums/products and products through a zero internal space.
- **E1-S12: Check realizable active specializations.** Inputs: E1-I4, E1-I6, E1-I7, E1-I8, E1-I9, E1-S5, E1-S6, E1-S7, E1-S8, E1-S10, E1-S11. Scope: active_or_raw_as_named. Conclusion: a=0 gives p=1; δ=γ=0 gives exact accepted target; n=0 has a one-dimensional positive target, while zero raw mass contradicts m>0. Justification: Substitute active specializations without normalizing excluded cases.
- **E1-S13: Analyze the sufficient threshold separately.** Inputs: E1-I1, E1-I2, E1-I3, E1-I4, E1-I6, E1-I7, E1-I8, E1-I10, E1-S6, E1-S7, E1-S8. Scope: replace E1-I9; do not inherit positive-success S9 or conditional-vector S10 as assumptions. Conclusion: For τ<√2 the geometric proof still has h>0; aligned U=Ry(0),V=Ry(π) gives p=0 at actual distance √2. Justification: Recompute h≥1−τ²/2 with the replaced threshold; separately instantiate the legal one-ancilla diagnostic.
- **E1-S14: Delimit the conditional composition and source layer.** Inputs: E1-I1, E1-I2, E1-I3, E1-I4, E1-I5, E1-I6, E1-I7, E1-I8, E1-I9, E1-S3, E1-S7, E1-S10. Scope: active_or_raw_as_named. Conclusion: No residual certifier, raw-data/preparation supplier, angle algorithm or finite-bit compiler/runtime has been constructed. Justification: The input certificate interfaces and the geometric conclusions have different evidentiary roles.

#### Reuse and route scopes

- **AND join policy:** Every required_inputs list is conjunctive within its stated scope. Raw/diagnostic steps exclude active positivity/conditioning assumptions where those are replaced. No consequence of success is used to prove its own denominator nonzero.
- **reused results:** **result:** Exact scalar Gram identity **supplied input:** E1-I3 **consumers:** E1-S3 **status:** Source-supported and supplied, not newly assessed exact Gram proof.; **result:** Normalization stability **supplied input:** E1-I5 **consumers:** E1-S6 **status:** Prior A2 mathematical fragment supplied; neither new core nor hidden producer-answer retrieval.; **result:** Aligned circuit telescoping **supplied input:** E1-I7 **consumers:** E1-S7 **status:** Prior B3 and existing source fragment supplied; no weighted precision optimization assessed.; **result:** Backward affine error unrolling **producer:** E1-S2 **consumers:** E1-S3; E1-S4; E1-S11 **status:** Assessed fragment shared with G1; requires exposure/split reconciliation before pooling.
- **reconvergent branches:** **branches:** residual transfer and exact Gram semantics: E1-S1/E1-S2/E1-S3; raw-data certificate: E1-I4 **join:** E1-S5 **why:** Both true norm lower bound and raw perturbation are needed to establish nonzero y.; **branches:** data normalization: E1-S6; actual circuit action/alignment: E1-I6/E1-I7/E1-I8 **join:** E1-S7 **why:** Neither a correct state target nor a small gate perturbation alone certifies the implemented full output.; **branches:** full-output closeness/unit norms: E1-S7; actual orthogonal projection: E1-S8; strict conditioning bound: E1-I9 **join:** E1-S9 **why:** All three are needed before normalized accepted output is legal.

### Evidence limitations

- No Lean, kernel, test-module, complete repository build, model response collection, inference experiment or training was performed by this author.
- Independent exact-content mathematical/source review and semantic deduplication remain pending; no author self-approval or transfer of prior workbook review is claimed.
- No global novelty, split independence, hidden-holdout status, model difficulty, benchmark stability or finite-bit supplier guarantee is claimed.

Full source roles, review bindings and provisional difficulty: [complete packet](qa/E1.json).

## E2 — Two-sided LCU from approximate clean columns

### Reference solution

The coefficient assumptions give \(\alpha>0\), and \(|\omega_j|=1\), including the chosen value for zero coefficients. Therefore
\[
\lVert l\rVert^2=\lVert r\rVert^2=\sum_j\frac{|c_j|}{\alpha}=1,
\qquad \overline{l_j}r_j=\frac{c_j}{\alpha}.
\]
For a zero coefficient both coordinates are zero; the choice of its phase does not affect them. The actual clean columns \(\widetilde l,\widetilde r\) also have norm one because their preparation operators are unitary.

For a vector \(v\in K\), define \(K_v:H\to K\otimes H\) by \(K_vu=v\otimes u\). Its operator norm is \(\lVert K_v\rVert=\lVert v\rVert\), since \(H\) is nonzero and \(\lVert v\otimes u\rVert=\lVert v\rVert\lVert u\rVert\). Its adjoint is \(K_v^\dagger=\langle v|\otimes I\), with the same norm. In particular these maps are isometries, or adjoint contractions, when \(v\) is unit.

The SELECT operator is unitary: its orthogonal selector blocks obey
\[
S^\dagger S=\sum_j|j\rangle\langle j|\otimes U_j^\dagger U_j=I,
\]
and the reverse product is likewise the identity. Tensoring each actual preparation with the identity preserves unitarity, and their adjoints and products are unitary. Hence the specified \(\widetilde W\) is unitary. Since \(J=K_{|0\rangle}\) is an isometry, \(\widetilde B=J^\dagger\widetilde WJ\) is a contraction. Also
\[
\lVert A/\alpha\rVert\le\sum_j\frac{|c_j|}{\alpha}\lVert U_j\rVert=1.
\]
These statements do not assert that the full output remains in the clean selector sector.

The clean input and output factors depend only on their specified columns:
\[
(Q_R\otimes I)J=K_{\widetilde r},\qquad
J^\dagger(Q_L^\dagger\otimes I)=K_{\widetilde l}^\dagger.
\]
Consequently
\[
\boxed{\widetilde B=K_{\widetilde l}^\dagger\widetilde S K_{\widetilde r}
=(\langle\widetilde l|\otimes I)\widetilde S(|\widetilde r\rangle\otimes I).}
\]
This formula holds even when \(\widetilde S\) mixes selector labels. With ideal \(S\), expanding the orthogonal selector blocks gives
\[
K_l^\dagger S K_r=\sum_j\overline{l_j}r_jU_j
=\frac1\alpha\sum_jc_jU_j=A/\alpha.
\]
The conjugation on the left column is essential.

One direct norm proof inserts the two ideal columns and ideal SELECT in three steps:
\[
\begin{aligned}
\widetilde B-A/\alpha
={}&K_{\widetilde l-l}^\dagger\widetilde S K_{\widetilde r}\\
&+K_l^\dagger(\widetilde S-S)K_{\widetilde r}\\
&+K_l^\dagger S K_{\widetilde r-r}.
\end{aligned}
\]
The norms of the three terms are at most \(\delta_L\), \(\eta\), and \(\delta_R\), respectively. Here the actual right column, ideal left column and both SELECT operators have norm one. Thus no extra product \(\delta_L\delta_R\) or dimension factor is needed:
\[
\lVert\widetilde B-A/\alpha\rVert\le\delta_L+\delta_R+\eta.
\]
Independently the two contraction estimates give \(\lVert\widetilde B-A/\alpha\rVert\le2\). Multiplying the better bound by positive \(\alpha\) proves
\[
\boxed{\lVert A-\alpha\widetilde B\rVert
\le\alpha\min\{2,\delta_L+\delta_R+\eta\}.}
\]
At no point was either complete preparation operator compared to an ideal unitary completion. Only its clean column and actual unitarity were used.

For the explicitly requested coefficient route, hold ideal \(S\) in the middle and set \(B_S=K_{\widetilde l}^\dagger S K_{\widetilde r}\). Its exact coefficients are
\[
B_S=\sum_j\overline{\widetilde l_j}\,\widetilde r_jU_j.
\]
For each index, write
\[
\overline{\widetilde l_j}\widetilde r_j-\overline{l_j}r_j
=\overline{(\widetilde l_j-l_j)}\widetilde r_j
+\overline{l_j}(\widetilde r_j-r_j).
\]
Summing absolute values and applying Cauchy–Schwarz twice gives
\[
\begin{aligned}
\sum_j\left|\overline{\widetilde l_j}\widetilde r_j-\frac{c_j}{\alpha}\right|
&\le\lVert\widetilde l-l\rVert\lVert\widetilde r\rVert
+\lVert l\rVert\lVert\widetilde r-r\rVert\\
&\le\delta_L+\delta_R.
\end{aligned}
\]
Since each \(U_j\) has operator norm one, this bounds \(\lVert B_S-A/\alpha\rVert\). Moreover,
\[
\lVert\widetilde B-B_S\rVert
=\lVert K_{\widetilde l}^\dagger(\widetilde S-S)K_{\widetilde r}\rVert\le\eta.
\]
Triangle inequality recovers the same approximate-block estimate and its contraction cap. These are two alternative proofs of the error bound. The problem requests the coefficient calculation as well, but neither proof is an additional assumption that the other must consume.

In the phase-referenced branch, replace the two reference vectors by \(l'=e^{i\theta_L}l\) and \(r'=e^{i\theta_R}r\). They are still unit. Put \(\Delta=\theta_R-\theta_L\) and \(e=\delta_L+\delta_R+\eta\). The exact ideal sandwich is now
\[
K_{l'}^\dagger S K_{r'}=e^{i\Delta}A/\alpha.
\]
Repeating the three-term norm estimate under the replaced hypotheses gives
\[
\lVert\alpha\widetilde B-e^{i\Delta}A\rVert\le\alpha e.
\]
For the originally requested exact representative, one obtains
\[
\boxed{\lVert A-\alpha\widetilde B\rVert
\le\min\left\{2\alpha,\ \alpha e+|1-e^{i\Delta}|\lVert A\rVert\right\}.}
\]
In particular this is at most
\[
\alpha\min\left\{2,\ e+2|\sin(\Delta/2)|\right\}.
\]
The universal cap still holds because the two block contractions are unchanged. The sufficient phase relation \(e^{i(\theta_R-\theta_L)}=1\) restores the previous bound; a common left/right phase cancels. This is not claimed necessary for every special target: \(A\) can vanish through cancellation even though \(\alpha>0\).

Separate fidelities alone do not control this relative phase. For example take selector dimension \(r=1\), any nonzero \(H\), \(c_1=1\), \(U_1=I\), \(Q_L=1\), \(Q_R=-1\), and \(\widetilde S=S=I\). Then \(l=r=1\), \(\widetilde l=1\), \(\widetilde r=-1\). Both separate squared fidelities equal \(1\), but \(\widetilde B=-I\) while \(A=I\), so
\[
\lVert A-\alpha\widetilde B\rVert=2.
\]
This realizes the phase branch with \(\theta_L=0\), \(\theta_R=\pi\) and zero phase-referenced errors. It does not satisfy zero exact-representative right-column error; that error is \(2\). The counterexample therefore does not contradict the main theorem.

For fixed \(\widetilde S\), the sandwich formula shows that unitary completions with the same two clean columns have exactly the same clean block, independently of every off-clean column. An explicit pair on \(\mathbb C^2\), with first coordinate clean, is
\[
Q=I_2,\qquad Q'=\operatorname{diag}(1,-1).
\]
They share the first column and \(\lVert Q-Q'\rVert=2\). Either can replace a preparation having that clean column without changing the sandwich. This particular pair has no nontrivial one-dimensional analogue, because a one-dimensional unitary is determined by its only column; the phase-fidelity counterexample nevertheless already works in that dimension.

Zero coefficients cause no division by zero in the phase definition because they use the stated separate branch, and their ideal coordinates vanish. Approximate columns can have weight on those coordinates, which is included in the same error bound. If \(\delta_L=\delta_R=\eta=0\) in the exact-representative branch, then \(\widetilde B=A/\alpha\) exactly. This still does not imply deterministic clean success. For example take two selector labels, \(c=(1,-1)\), \(U_1=U_2=I\), and exact columns \(l=(1,1)/\sqrt2\), \(r=(1,-1)/\sqrt2\). Then \(A=0\) and the ideal clean block is zero, although all components are unitary and \(\alpha=2\). The all-zero coefficient case is different: it has \(\alpha=0\), so the displayed normalization formulas are undefined and the active construction does not apply. The zero operator can be realized by other specified constructions, but dividing by this \(\alpha\) is not one.

The proof assumes actual coherent unitaries and the actual adjoint in the displayed composite. A source of prepared state samples alone does not provide an executable adjoint, a coherent SELECT implementation, an inverse of an unknown preparation procedure, or a certificate that unmentioned workspace is clean. All work here is explicitly in the given registers. No finite-bit precision supplier, gate synthesis or resource bound is derived. Clean projection defines an accepted branch; it is not a promise that the entire output is clean.

### Partial credit

- **1 points:** Checks \(\alpha>0\), unit norms of ideal and actual columns, the identity \(\overline{l_j}r_j=c_j/\alpha\), and SELECT/product unitarity plus the contraction facts used later.
- **1.5 points:** Derives the clean-column sandwich and the exact target \(A/\alpha\), with conjugation, register order and the actual left adjoint correct. Explains why only clean columns enter.
- **2 points:** Proves the additive \(\delta_L+\delta_R+\eta\) operator bound and independent cap \(2\), with no unneeded product or dimension factor, obtaining the scaled minimum. A valid direct or coefficient route suffices for this criterion.
- **1.5 points:** Computes the ideal-SELECT coefficients \(\overline{\widetilde l_j}\widetilde r_j\), derives their \(\ell^1\) deviation by Cauchy–Schwarz, and identifies the coefficient and direct sandwich routes as alternative sufficient proofs, not additional input assumptions.
- **2 points:** In the replaced phase branch, obtains \(e^{i(\theta_R-\theta_L)}A\), gives a correct explicit phase-mismatch error bound and sufficient cancellation condition, and verifies a unitary perfect-fidelity/wrong-block witness without incorrectly assigning zero exact-vector errors.
- **1 points:** Proves invariance under changes to off-clean columns for fixed \(\widetilde S\), and verifies a pair of unitary completions at distance \(2\) with the same clean column. This diagnostic overlaps known completion examples and is not a separate new core.
- **1 points:** Handles zero coefficients, \(r=1\), zero errors and the excluded \(\alpha=0\) case; distinguishes exact clean block from deterministic cleanup and available coherent unitaries/adjoints from mere state preparation access and finite-bit costs.

Equivalent valid mathematical arguments receive the same substantive credit. Evidence status and formal identifiers are in the complete QA packet, outside the question.

### Boundary cases

- **case:** Some coefficients zero **scope:** valid main branch **conclusion:** Their ideal columns vanish and phase is explicitly set to 1. Approximate leakage into them is covered by the same norm bound.
- **case:** Selector dimension one **scope:** valid main and phase branches **conclusion:** No unused completion columns, but independent left/right phase remains relevant to the exact scalar block.
- **case:** Exact-representative errors all zero **scope:** valid main branch **conclusion:** Exact \(\widetilde B=A/\alpha\); still no deterministic-success guarantee.
- **case:** Perfect separate fidelity **scope:** replace exact representative estimates by the phase-referenced estimates **conclusion:** The one-label sign witness gives exact block error \(2\), while zero phase-referenced errors hold.
- **case:** All coefficients zero **scope:** excluded diagnostic; replace the not-all-zero premise **conclusion:** \(A=0\) and \(\alpha=0\); normalized selector formulas are undefined and must not be evaluated.
- **case:** Coefficient cancellation with positive normalizer **scope:** valid main branch **conclusion:** Coefficients \((1,-1)\) and identical system unitaries give \(A=0\), \(\alpha=2\), and zero clean success in the exact construction.

### Common errors

- **error:** Use \(l_jr_j\) in general or \(\widetilde l_j\widetilde r_j\) without conjugating the left column. **why wrong:** The left factor is a bra supplied by the actual adjoint; complex conjugation determines both coefficients and phase difference.
- **error:** Assume the same PREPARE must appear on both sides for every LCU. **why wrong:** Squared selector weights are the same-column architecture. The explicitly specified two-sided interface uses conjugate left amplitudes times right amplitudes to encode complex coefficients.
- **error:** Require full preparation-unitary operator closeness to an ideal completion. **why wrong:** The projected sandwich depends only on the clean columns and actual unitarity. The unused columns may differ maximally.
- **error:** Add a mandatory \(\delta_L\delta_R\) term or a dimension factor. **why wrong:** The three-term decomposition uses actual unit vectors on the untouched sides; its bounds are additive without those losses.
- **error:** Use the ideal coefficient formula for a general selector-mixing middle operator. **why wrong:** The sum \(\sum_j\overline{\widetilde l_j}\widetilde r_jU_j\) applies to ideal block-diagonal SELECT. General \(\widetilde S\) is handled by an independent operator perturbation bound.
- **error:** Treat independent phase-optimized column errors or perfect fidelities as zero exact block error. **why wrong:** Left and right global phases leave a relative scalar phase on the block; it cancels only under the stated sufficient relation or a special target.
- **error:** Infer nonzero target or positive success from nonzero coefficient normalization. **why wrong:** Nonzero coefficients may cancel to \(A=0\), even with \(\alpha>0\). Unitarity only gives contraction, not deterministic clean success.

### Author-supplied reasoning map

These are declared mathematical inputs and scoped claims, not extracted Lean proof-term dependencies.

#### Inputs

- **E2-I1** (assumption): Nonzero finite complex spaces \(K,H\), fixed clean selector, order \(K\otimes H\), unitary system operators \(U_j\).
- **E2-I2** (assumption): Coefficients are not all zero; \(\alpha=\sum|c_j|\), with the displayed zero-safe phase and ideal column definitions.
- **E2-I3** (assumption): Actual \(Q_L,Q_R,\widetilde S\) are unitary; \(\widetilde W\) uses the actual \(Q_L^\dagger\); \(\widetilde l,\widetilde r\) are their clean columns and \(\widetilde B=J^\dagger\widetilde WJ\).
- **E2-I4** (assumption): Main branch: exact-representative errors \(\lVert\widetilde l-l\rVert\le\delta_L\), \(\lVert\widetilde r-r\rVert\le\delta_R\); all error parameters nonnegative.
- **E2-I5** (assumption): \(\lVert\widetilde S-S\rVert\le\eta\), where \(S=\sum_j|j\rangle\langle j|\otimes U_j\) and \(\eta\ge0\).
- **E2-I6** (convention): Euclidean norms, conjugate-first complex inner product, induced operator norm, tensor product norm and rightmost-first action.
- **E2-I7** (assumption): Phase branch REPLACES I4 by \(\lVert\widetilde l-e^{i\theta_L}l\rVert\le\delta_L\), \(\lVert\widetilde r-e^{i\theta_R}r\rVert\le\delta_R\), with real phases; retains I1,I2,I3,I5,I6.

#### Steps

- **E2-S1: Normalize the ideal coefficient columns.** Inputs: E2-I1, E2-I2, E2-I6. Scope: main_or_structural_as_named. Conclusion: \(\alpha>0\), \(\lVert l\rVert=\lVert r\rVert=1\), and \(\overline{l_j}r_j=c_j/\alpha\), including zero coefficients. Justification: Sum coefficient magnitudes and use the specified zero-safe phase branch.
- **E2-S2: Supply unitary and contraction interfaces.** Inputs: E2-I1, E2-I2, E2-I3, E2-I5, E2-I6, E2-S1. Scope: main_or_structural_as_named. Conclusion: \(S,\widetilde W\) are unitary; actual columns are unit; \(J\) is an isometry; \(\lVert\widetilde B\rVert,\lVert A/\alpha\rVert\le1\). Justification: Orthogonal SELECT blocks, adjoint/tensor/product closure, clean compression, and coefficient triangle bound.
- **E2-S3: Derive the clean-column-only sandwich.** Inputs: E2-I1, E2-I3, E2-I6. Scope: main_or_structural_as_named. Conclusion: \(\widetilde B=K_{\widetilde l}^\dagger\widetilde S K_{\widetilde r}\), where \(K_vu=v\otimes u\) and \(\lVert K_v\rVert=\lVert v\rVert\). Justification: Apply the actual preparation to the clean input and take the adjoint of the analogous left-column identity. No error estimates required.
- **E2-S4: Recover the exact target from the ideal sandwich.** Inputs: E2-I1, E2-I2, E2-I5, E2-I6, E2-S1, E2-S3. Scope: main_or_structural_as_named. Conclusion: \(K_l^\dagger S K_r=\sum_j\overline{l_j}r_jU_j=A/\alpha\). Justification: Expand the block-diagonal SELECT on orthogonal labels.
- **E2-S5: Prove the direct sandwich error estimate.** Inputs: E2-I1, E2-I3, E2-I4, E2-I5, E2-I6, E2-S1, E2-S2, E2-S3, E2-S4. Scope: main exact-representative branch. Conclusion: \(\lVert\widetilde B-A/\alpha\rVert\le\delta_L+\eta+\delta_R\). Justification: Three-term decomposition changes the left column, middle unitary and right column, using unit norms on untouched sides.
- **E2-S6: Identify the exact coefficients for ideal SELECT.** Inputs: E2-I1, E2-I3, E2-I5, E2-I6, E2-S3. Scope: main_or_structural_as_named. Conclusion: \(B_S=K_{\widetilde l}^\dagger S K_{\widetilde r}=\sum_j\overline{\widetilde l_j}\widetilde r_jU_j\). Justification: Expand the ideal SELECT. Do not substitute a selector-mixing middle operator into this coefficient formula.
- **E2-S7: Prove the coefficient error alternative.** Inputs: E2-I1, E2-I2, E2-I3, E2-I4, E2-I5, E2-I6, E2-S1, E2-S2, E2-S3, E2-S6. Scope: alternative main proof, no dependency on E2-S5. Conclusion: The coefficient \(\ell^1\) deviation is at most \(\delta_L+\delta_R\), and \(\lVert\widetilde B-A/\alpha\rVert\le\delta_L+\delta_R+\eta\). Justification: Split each conjugated product difference, apply Cauchy–Schwarz twice, use unit system operators and add the middle-operator perturbation.
- **E2-S8: Obtain the independent universal cap.** Inputs: E2-I1, E2-I2, E2-I3, E2-I6, E2-S2. Scope: main_or_structural_as_named. Conclusion: \(\lVert A-\alpha\widetilde B\rVert\le2\alpha\). Justification: Triangle inequality for two contractions followed by positive scaling.
- **E2-S9a: Conclude the requested estimate by the direct route.** Inputs: E2-I2, E2-S1, E2-S5, E2-S8. Scope: OR route A. Conclusion: \(\lVert A-\alpha\widetilde B\rVert\le\alpha\min\{2,\delta_L+\delta_R+\eta\}\). Justification: Scale the direct bound and take its minimum with the independent cap.
- **E2-S9b: Conclude the same estimate by the coefficient route.** Inputs: E2-I2, E2-S1, E2-S7, E2-S8. Scope: OR route B; E2-S5 is not a premise. Conclusion: \(\lVert A-\alpha\widetilde B\rVert\le\alpha\min\{2,\delta_L+\delta_R+\eta\}\). Justification: Scale the coefficient-route bound and take its minimum with the independent cap.
- **E2-S10: Transport the phase-referenced column estimates.** Inputs: E2-I1, E2-I2, E2-I3, E2-I5, E2-I6, E2-I7, E2-S1, E2-S2, E2-S3, E2-S4, E2-S8. Scope: phase branch replaces E2-I4; exact-error conclusions E2-S5/E2-S7/E2-S9 are not imported. Conclusion: For \(\Delta=\theta_R-\theta_L\), the target is \(e^{i\Delta}A\). Error relative to \(A\) is at most \(\min\{2\alpha,\alpha(\delta_L+\delta_R+\eta)+|1-e^{i\Delta}|\lVert A\rVert\}\). Justification: Reapply the three-term algebra to unit phase-shifted ideal columns, then triangle inequality to the target phase.
- **E2-S11: Exhibit the fidelity-versus-block obstruction.** Inputs: E2-I1, E2-I2, E2-I3, E2-I5, E2-I6, E2-I7, E2-S3, E2-S10. Scope: phase diagnostic; do not assume zero errors under E2-I4. Conclusion: One selector label with \(c_1=1,U_1=I,Q_L=1,Q_R=-1\) has both fidelities 1 but exact block error 2. Justification: Compute the scalar sandwich; the right exact-vector error is 2, while phase-referenced error is 0.
- **E2-S12: Show completion invariance and maximal off-column difference.** Inputs: E2-I1, E2-I3, E2-I6, E2-S3. Scope: main_or_structural_as_named. Conclusion: Identical clean columns give identical blocks for fixed \(\widetilde S\); \(I_2\) and \(\operatorname{diag}(1,-1)\) share a clean column at distance 2. Justification: Only the two columns occur in the sandwich; diagonal unitarity and norm computation verify the witness.
- **E2-S13: Analyze valid coefficient and dimension boundaries.** Inputs: E2-I1, E2-I2, E2-I3, E2-I4, E2-I5, E2-I6, E2-S1, E2-S2, E2-S3, E2-S4, E2-S9a. Scope: main_or_structural_as_named. Conclusion: Zero coefficients and selector dimension 1 are legal. Zero errors give the exact block, but coefficient cancellation may give \(A=0\), \(\alpha>0\) and success probability 0. Justification: Apply the same definitions and use exact two-label coefficients (1,−1) with identical system unitaries.
- **E2-S14: Diagnose the all-zero coefficient regime.** Inputs: E2-I1, E2-I6. Scope: replace E2-I2 by all-zero coefficients; do not import S1 or any normalized-column consequence. Conclusion: With all \(c_j=0\), both \(A\) and \(\alpha\) are zero; the normalized column formulas are undefined. Justification: Compute the unnormalized sums without dividing.
- **E2-S15: Separate the conditional operator interface from an implementation supplier.** Inputs: E2-I1, E2-I3, E2-I5, E2-I6, E2-S2, E2-S3, E2-S13. Scope: main_or_structural_as_named. Conclusion: A prepared-state source alone does not supply actual adjoints, coherent SELECT, unmentioned workspace cleanup or finite-bit resources. Justification: The mathematical proof consumes actual unitary interfaces; compression does not prove full-output cleanup.

#### Reuse and route scopes

- **AND join policy:** Each required_inputs list is conjunctive within its stated scope. The two error proofs are explicit OR alternatives. The phase branch replaces, rather than adds to, the exact-representative column premises. The all-zero diagnostic excludes the nonzero-normalizer premise.
- **reused results:** **result:** Tensor clean-column/adjoint-row interface **producer:** E2-S3 **consumers:** E2-S4; E2-S5; E2-S6; E2-S10; E2-S12 **status:** Original two-sided derivation grounded in source clean-column/row formulas, which use one PREPARE and an additional coefficient register.; **result:** Cauchy–Schwarz for two product vectors **producer:** E2-S7 **consumers:** E2-S9b **status:** Derived coefficient ℓ¹ route; no source theorem claim.; **result:** Exact block completion freedom **producer:** E2-S12 **consumers:**  **status:** Shares the completion diagnostic with current BE004/BE112; not counted as a separate new target.
- **reconvergent branches:** **branches:** complex coefficient normalization: E2-S1; clean-column sandwich: E2-S3; ideal SELECT action: E2-I5 **join:** E2-S4 **why:** Both selector columns and a correctly typed SELECT are required to recover the target operator.; **branches:** two exact-representative column certificates: E2-I4; middle operator certificate: E2-I5; unitary and sandwich facts: E2-S2/E2-S3/E2-S4 **join:** E2-S5 **why:** The additive block estimate requires all three error interfaces, not only a prepared state.
- **alternative routes:** **conclusion:** Requested scaled minimum block-error bound **routes:** E2-S5; E2-S8; E2-S9a; E2-S6; E2-S7; E2-S8; E2-S9b **relationship:** OR: either proof route is sufficient. The question also requests the coefficient identity, but that pedagogical request does not turn the proofs into jointly necessary assumptions.

### Evidence limitations

- No Lean, kernel, test-module, complete repository build, model response collection, inference experiment or training was performed by this author.
- Independent exact-content mathematical/source review and semantic deduplication remain pending; no author self-approval or transfer of prior workbook review is claimed.
- No global novelty, split independence, hidden-holdout status, model difficulty, benchmark stability or finite-bit supplier guarantee is claimed.

Full source roles, review bindings and provisional difficulty: [complete packet](qa/E2.json).

## G1 — Finite-grid Gram contraction: roundoff, range and a certified normalizer

### Reference solution

Write \(m=d_j\) and \(M=M_j\) within a single update. The arithmetic analysis concerns the supplied rounded algorithm. The exact Gram semantics in the question is a separate supplied interface.

First consider a scheduled dot product of length \(m\) with exact operands \(a_k,z_k\) at that call. Write \(p_k=Q_b(a_kz_k)=a_kz_k+\alpha_k\) and \(q_k=Q_b(q_{k-1}+p_k)=q_{k-1}+p_k+\beta_k\), with \(q_0=0\) and \(|\alpha_k|,|\beta_k|\le u\). Induction gives
\[
q_m-\sum_{k=1}^m a_kz_k=\sum_{k=1}^m(\alpha_k+\beta_k),
\qquad\left|q_m-\sum_{k=1}^m a_kz_k\right|\le2mu.
\]
The operands may themselves be outputs of earlier rounded calls: the bound is relative to their current stored values. On this unbounded fixed grid, each addition is in fact exact, so \(\beta_k=0\). Keeping the displayed conservative bound is legitimate and gives the constants requested.

For each bit \(t\), write
\[
\widehat T^t=A_j^t\widehat E_j+F^t,
\qquad \|F^t\|_{\max}\le2mu,
\]
\[
\widehat S^t=\widehat T^t(A_j^t)^T+G^t,
\qquad \|G^t\|_{\max}\le2mu.
\]
There are \(m\) terms in every dot product of both passes; the left bond size affects how many entries there are, not the error bound for one entry. The final addition introduces a matrix \(H\) with \(\|H\|_{\max}\le u\). Therefore
\[
\widehat E_{j-1}=\sum_t A_j^t\widehat E_j(A_j^t)^T+Z_j,
\quad Z_j=\sum_t[F^t(A_j^t)^T+G^t]+H.
\]
For one bit, \(\|F^t(A_j^t)^T\|_{\max}\le m(2mu)M\). Summing both bits gives
\[
\|Z_j\|_{\max}\le(4m^2M+4m+1)u=uR_j.
\]
Neither symmetry nor positive semidefiniteness of \(\widehat E_j\) was used.

For an arbitrary error matrix \(D\), each entry of \(A_j^tD(A_j^t)^T\) is a sum of \(m^2\) terms, each bounded by \(M^2\|D\|_{\max}\). Hence
\[
\left\|\sum_tA_j^tD(A_j^t)^T\right\|_{\max}
\le2m^2M^2\|D\|_{\max}=L_j\|D\|_{\max}.
\]
Subtract the exact update from the rounded update to obtain \(e_{j-1}\le L_je_j+uR_j\); the exact terminal identity gives \(e_n=0\). Define
\[
C_n=0,\qquad C_{j-1}=L_jC_j+R_j.
\]
Backward induction yields \(e_j\le uC_j\), with
\[
C_j=\sum_{k=j+1}^{n}R_k\prod_{\ell=j+1}^{k-1}L_\ell,
\qquad C_0=\sum_{k=1}^{n}R_k\prod_{\ell=1}^{k-1}L_\ell.
\]
All factors are nonnegative. The empty-product convention is essential: the residual produced at step 1 reaches the final scalar with coefficient one. No division by an \(L_j\) is used, so zero core bounds cause no singular formula.

Here is a range certificate for the same algorithm. Define
\[
B_n=1,\qquad B_{j-1}=L_jB_j+uR_j.
\]
Assuming \(\|\widehat E_j\|_{\max}\le B_j\), a rounded first-pass product has magnitude at most \(MB_j+u\). Its first \(k\) accumulated terms have magnitude at most \(kMB_j+2ku\), so every first-pass entry is bounded by
\[
F_j^{\rm range}=mMB_j+2mu.
\]
A rounded second-pass product is bounded by \(MF_j^{\rm range}+u\); its first \(k\) accumulated terms by \(kMF_j^{\rm range}+2ku\). Thus every second-pass entry is bounded by
\[
G_j^{\rm range}=mMF_j^{\rm range}+2mu.
\]
The final addition has magnitude at most \(2G_j^{\rm range}+u=B_{j-1}\). This closes the induction for the environment envelope. The exact pre-round products are bounded by \(MB_j\) and \(MF_j^{\rm range}\). A pre-round accumulator at its \(k\)-th addition is bounded by the corresponding displayed partial-sum bound (in fact its bound saves one \(u\)); the pre-round bit-sum is bounded by \(2G_j^{\rm range}\). Thus the bounds cover operands, products and all sums, not just \(\widehat s\).

Let \(K\) be the maximum of 1, all input bounds \(M_j\), all \(B_j\), \(M_jB_j+u\), \(F_j^{\rm range}\), \(M_jF_j^{\rm range}+u\), \(G_j^{\rm range}\), and \(\sqrt{B_0}+u\). The last term covers the square-root output when its input is nonnegative. There are finitely many finite terms. Choose an integer \(I\ge0\) with \(2^I>K+h\) and represent stored grid numbers in \([-2^I,2^I-h]\). Every scheduled value then lies strictly inside this range, so overflow cannot occur. Exact scalar products before rounding may use a widened temporary with \(2b\) fractional bits; that is a representation requirement, not a unit-cost bit-operation assertion. This range argument concerns the explicit multiply/add schedule and the input/output contract of the correctly rounded square-root primitive; it does not specify the internal algorithm or cost of that primitive.

For the normalization branch put \(r=\|x\|_2\), \(s=r^2\), and \(\Delta=uC_0\). The scalar Gram interface and the preceding bound give \(|\widehat s-s|\le\Delta\). If \(\Delta<\mu^2\), then
\[
\widehat s\ge\mu^2-\Delta>0.
\]
The square root is therefore defined on a positive argument. Rationalizing the difference gives
\[
|\sqrt{\widehat s}-r|
=\frac{|\widehat s-s|}{\sqrt{\widehat s}+r}
\le\frac{\Delta}{\sqrt{\mu^2-\Delta}+\mu}.
\]
After rounding the square root, set
\[
\theta=\frac{\Delta}{\sqrt{\mu^2-\Delta}+\mu}+u.
\]
Then \(|\widehat r-r|\le\theta\). If additionally \(\theta<\mu\), then \(\widehat r\ge\mu-\theta>0\), and exact division gives
\[
\left\|\frac{x}{\widehat r}-\frac{x}{r}\right\|_2
=r\left|\frac1{\widehat r}-\frac1r\right|
=\frac{|r-\widehat r|}{\widehat r}
\le\frac{\theta}{\mu-\theta}.
\]
The produced mathematical vector has norm \(r/\widehat r\), so a rounded normalizer generally does not give exact unit norm. The bound concerns rescaling error of the same numerator, not a claim about a different state direction or a physical circuit output.

One explicit precision choice establishes its own positivity premises. For \(\varepsilon>0\), define
\[
\tau=\frac{\varepsilon\mu^2}{(1+\varepsilon)(C_0+\mu)}>0
\]
and choose \(u\le\tau\). Since \(C_0\ge0\) and \(\mu>0\), this implies
\[
\Delta\le\frac{\varepsilon\mu^2 C_0}{(1+\varepsilon)(C_0+\mu)}<\mu^2.
\]
Thus \(\widehat s>0\) is proved before the square-root bound is invoked. Moreover
\[
\theta\le\frac\Delta\mu+u
=u\left(\frac{C_0}\mu+1\right)
\le\frac{\varepsilon\mu}{1+\varepsilon}<\mu.
\]
Consequently \(\widehat r>0\), and monotonicity of \(z/(\mu-z)\) for \(0\le z<\mu\) gives error at most \(\varepsilon\). Equivalently, a sufficient working precision is
\[
b\ge\max\left\{b_{\rm in},0,\left\lceil\log_2\frac1{2\tau}\right\rceil\right\}.
\]
This follows from \(u=2^{-b-1}\); the maximum with zero handles \(2\tau>1\). Once this \(b\) is selected, recompute the finite range envelope with that \(u\). The supplied core bounds \(M_j\) and therefore \(C_0\) do not depend on this subsequent precision choice.

For \(n=0\), the single amplitude, exact environment, rounded environment and rounded square root all equal 1; every error is zero. The recurrence has \(C_0=0\), and the conservative \(u\)-term in the general square-root bound need not be attained. If a nonempty chain has an identically zero core, then that update produces an exactly zero rounded environment, and all earlier updates remain zero; the exact mass is also zero. More generally, zero exact mass means every \(x_s=0\), so \(x/\|x\|\) is undefined. The raw-error theorem still applies, but the normalization branch's premise \(\mu>0\) with \(r\ge\mu\) cannot hold. No zero-mass example is claimed to satisfy that branch.

For the requested nonzero failure take \(n=1\), \(d_0=d_1=1\), \(b_{\rm in}=b\ge2\), \(A_1^0=[h]\) and \(A_1^1=[0]\). The first pass returns \(h\) exactly. The second pass rounds \(h^2\) to zero, because \(0<h^2<h/2\); its additions and the final bit-sum remain zero. Thus \(x=(h,0)\) has exact mass \(h^2>0\), but \(\widehat s=0\). The lower-mass/precision margin is deliberately not satisfied. Positivity alone supplies no uniform safe fixed precision over arbitrarily small masses. This legal schedule witness, and the local error/range analysis above, distinguish the finite-grid result from the supplied exact identity or an exact-real operation count. No supplier accuracy, bit runtime or gate synthesis is inferred.

### Partial credit

- **2 points:** Derives the dot-product rounding error and both matrix-pass residuals, correctly counting m terms per pass; obtains R_j=4m^2M+4m+1 or a rigorously justified tighter constant. Award 0.5 for the dot product, 1 for propagation of first-pass error through the transposed core, and 0.5 for two bits/final sum. Merely quoting a generic floating-point theorem does not establish this schedule.
- **1.5 points:** Derives L_j=2m^2M^2 from the entrywise double sum (0.5), establishes the backward recurrence with exact terminal error zero (0.5), and unrolls C_0 with products of earlier indices and valid empty products (0.5). No division by L_j is permitted without a separate zero case.
- **2 points:** Provides a noncircular backwards environment magnitude envelope (0.5), bounds both kinds of products and all partial sums/pre-round values (1), and selects a finite signed range including the square-root input/output with sufficient precision for temporary products (0.5). Only bounding the final scalar earns at most 0.5 here.
- **2 points:** Uses the independent mu bound to prove positivity of s_hat from a strict squared-mass margin (0.5); derives a square-root perturbation bound with the rounding error included (0.5); proves r_hat positive before division (0.5); and obtains the exact rescaling-error identity and a valid quantitative bound, noting non-unit norm (0.5). Do not demand the reference rationalization form if an equivalent justified bound is supplied.
- **1.5 points:** Gives an explicit u condition and integer b choice that independently imply all positivity and epsilon-error premises, in that order. Award 1 for a correct sufficient condition with its strictness proof and 0.5 for a correct logarithmic/integer precision conversion respecting b_in. A circular appeal to assumed positivity does not earn the first point.
- **1 points:** Computes a legal one-core nonzero grid input that rounds to zero (0.5), and handles n=0/zero mass with scoped premises plus the exact-real versus finite-grid/circuit boundary (0.5). A valid alternative counterexample and a general boundary argument receive equal credit.

Equivalent valid mathematical arguments receive the same substantive credit. Evidence status and formal identifiers are in the complete QA packet, outside the question.

### Boundary cases

- **case:** Empty chain **resolution:** The unique amplitude and both exact/rounded normalizers are 1; C_0=0, exact error zero.
- **case:** An identically zero core **resolution:** Both exact and rounded final mass vanish; raw-error analysis applies, but positive-mass normalization assumptions are incompatible.
- **case:** Zero exact mass without a positive certificate **resolution:** The target normalized vector is undefined; no normalization conclusion is made.
- **case:** A working precision too coarse for the mass **resolution:** The one-core h input at b>=2 has mass h^2>0 yet rounds to zero; it deliberately fails the sufficient margin.
- **case:** A zero amplification coefficient L_j **resolution:** The sum/product recurrence stays defined, with no division by L_j.
- **case:** Tighter roundoff accounting **resolution:** Grid additions are exact, so valid tighter constants and consistent derived thresholds are accepted.

### Common errors

- Using an operator-norm bound as if it were the entrywise maximum norm, omitting the m^2 factor.
- Forgetting that first-pass rounding is multiplied by the transposed core in the second pass.
- Unrolling the backwards recursion with later rather than earlier L factors.
- Claiming rounded environments remain PSD or assuming the computed mass is positive before checking a margin.
- Applying the square-root or reciprocal formula at a zero/nonpositive computed scalar.
- Giving a precision implication that quietly retains the strictness premise it was supposed to prove.
- Treating exact fixed-grid additions as worse than their stated upper error bound invalidates no estimate, but claiming every addition necessarily incurs u is false.
- Claiming a grid error certificate is a bit-runtime theorem or a unitary implementation.

### Author-supplied reasoning map

These are declared mathematical inputs and scoped claims, not extracted Lean proof-term dependencies.

#### Inputs

- **G1-I1** (assumption): Finite positive bond dimensions, scalar boundaries, exactly represented dyadic cores, supplied entry bounds M_j and b>=b_in; one empty word.
- **G1-I2** (supplied_interface): Exact Gram update and E_0(1,1)=||x||^2, explicitly supplied in the question.
- **G1-I3** (arithmetic_model): Specified two-pass Q_b schedule, |Q_b(z)-z|<=u, terminal identity exact, and correctly rounded sqrt only on a nonnegative input.
- **G1-I4** (conditional_branch_assumption): For normalization only, independent r=||x||>=mu>0.
- **G1-I5** (conditional_branch_assumption): For the precision branch only, requested epsilon>0; choose b respecting b_in.

#### Steps

- **G1-S1: Bound a scheduled dot product relative to its stored operands.** Inputs: G1-I1, G1-I3. Scope: main. Conclusion: Error <=2m u; partial error is the sum of multiplication/addition rounding terms. Justification: Expand q_k=q_{k-1}+a_k z_k+alpha_k+beta_k and sum. The grid makes additions exact, but the conservative bound remains valid.
- **G1-S2: Isolate one complete local-update residual.** Inputs: G1-I1, G1-I3, G1-S1. Scope: main. Conclusion: Ehat_{j-1}=sum_t A_j^t Ehat_j(A_j^t)^T+Z_j with ||Z_j||_max<=uR_j. Justification: First-pass error is multiplied by A^T; sum its m M amplification, second-pass error and final addition over two bits.
- **G1-S3: Propagate environment error through the exact local map.** Inputs: G1-I1, G1-I2, G1-S2. Scope: main. Conclusion: e_{j-1}<=L_j e_j+uR_j with e_n=0. Justification: Bound each of the two m-by-m index sums by m^2 M_j^2 e_j and subtract the exact recurrence.
- **G1-S4: Unroll the backwards error invariant.** Inputs: G1-S3. Scope: main. Conclusion: C_n=0, C_{j-1}=L_j C_j+R_j, e_j<=u C_j, C_0=sum_k R_k product_{ell<k}L_ell. Justification: Backward induction and finite distributivity; no division by potentially zero L_j.
- **G1-S5: Bound every scheduled intermediate magnitude.** Inputs: G1-I1, G1-I3, G1-S1, G1-S2. Scope: main. Conclusion: B_n=1, B_{j-1}=L_j B_j+uR_j bounds environments; first products/partial sums <=M_j B_j+u / k M_j B_j+2ku, and analogous second-pass bounds use F_j=m M_jB_j+2mu. Justification: Use the current environment envelope as an operand bound; bound both pass accumulators before closing the next environment bound.
- **G1-S6: Choose a finite representable range without overflow.** Inputs: G1-I1, G1-I3, G1-S5. Scope: main. Conclusion: Finite K covering inputs, all products, sums, environments and sqrt input/output allows 2^I>K+h and range [-2^I,2^I-h]. Justification: The finite list of bounds is finite. Widen temporary products to retain 2b fractional bits before rounding. This does not specify a bit runtime or internal sqrt algorithm.
- **G1-S7: Derive a conditional normalizer-error interface.** Inputs: G1-I2, G1-I3, G1-I4, G1-S4. Additional/scoped assumptions: The two strict inequalities are antecedents of the stated implication, not globally assumed facts.. Scope: conditional_theorem. Conclusion: IF Delta=uC_0<mu^2, s_hat>0 and theta=Delta/(sqrt(mu^2-Delta)+mu)+u bounds |r_hat-r|. IF also theta<mu, r_hat>0 and the rescaled-vector error is <=theta/(mu-theta). Justification: First lower-bound s_hat, then rationalize the square-root difference, add its rounding error, establish positive r_hat, and only then divide.
- **G1-S8: Make precision supply the strict margins.** Inputs: G1-I1, G1-I4, G1-I5, G1-S4. Scope: precision_branch. Conclusion: Choosing u<=tau=epsilon mu^2/((1+epsilon)(C_0+mu)) gives Delta<mu^2 and theta<=epsilon mu/(1+epsilon)<mu; b>=max(b_in,0,ceil(log2(1/(2tau)))) suffices. Justification: C_0>=0 and mu>0 give strictness directly. Define theta only after proving Delta<mu^2. No positive computed mass or rounded norm is presupposed.
- **G1-S9: Apply the conditional interface after precision supplies its antecedents.** Inputs: G1-S7, G1-S8, G1-I5. Scope: precision_branch. Conclusion: Both rounded scalars are positive and the exact rescaling error is at most epsilon. Justification: AND join: quantitative error interface plus independently produced strict margins; monotonicity of z/(mu-z).
- **G1-S10: Check unconditional empty and zero-core arithmetic boundaries.** Inputs: G1-I1, G1-I2, G1-I3. Scope: raw_boundary. Conclusion: n=0 gives exact scalar/sqrt 1 and error zero; an identically zero core gives exact and rounded final mass zero. Justification: Use the empty product or Q_b(0)=0 throughout the schedule. The raw theorem has no positive-mass premise.
- **G1-S11: Separate zero mass from the normalization domain.** Inputs: G1-I2. Additional/scoped assumptions: Replace the positive-mass branch by r=0; do not retain G1-I4.. Scope: excluded_domain_diagnostic. Conclusion: If exact mass is zero, every coordinate is zero and normalization is undefined; no mu>0 lower certificate can then hold. Justification: Finite nonnegative sum of squares and the definition of normalization.
- **G1-S12: Construct a nonzero input that loses mass under rounding.** Inputs: G1-I1, G1-I3. Additional/scoped assumptions: Retain the raw arithmetic model; do not impose the sufficient precision margin of G1-S8.. Scope: counterexample. Conclusion: For n=1, A^0=h,A^1=0,b_in=b>=2, x=(h,0) has positive mass but s_hat=0. Justification: First pass gives h; 0<h^2<h/2 makes the second-pass product round to zero, independently of ties.

#### Reuse and route scopes

- **AND join policy:** Every required_inputs list is conjunctive. G1-S7 is an implication; G1-S8 proves its antecedents independently, and G1-S9 is the application. Zero-mass and coarse-precision diagnostics explicitly replace or omit the normalization/precision branch premises.
- **reused results:** **id:** exact-scalar-Gram-semantics **source nodes:** declaration:QuantumBlockEncoding.TensorTrainNormEnvironment.gram_scalar **supplied input:** G1-I2 **consumer steps:** G1-S3; G1-S7; G1-S10; G1-S11 **assessment:** Supplied, not re-assessed as the prior C3 exact Gram theorem.; **id:** backwards-residual-unrolling **producer step:** G1-S4 **external overlap:** E1 has a separate operator-residual certificate using the same elementary recurrence topology; no independent-scoring clearance.
- **reconvergent branches:** **join:** G1-S3 **branches:** G1-S2; G1-I2 **why:** Rounded local residual and exact local update jointly determine total error.; **join:** G1-S9 **branches:** G1-S7; G1-S8 **why:** A conditional analytic interface needs a separately established strict nonzero margin.

### Evidence limitations

- No Lean invocation, toolchain installation, formal proof admission, model evaluation or paid API was performed.
- The finite-grid and approximate-isometry results are original natural-language derivations; exact frozen source anchors do not establish their formal compilation.
- Independent exact-content review, semantic deduplication, split reconciliation and maintainer admission are pending at authoring time.
- No bit-operation complexity, physical circuit implementation or whole-graph coverage is claimed.

Full source roles, review bindings and provisional difficulty: [complete packet](qa/G1.json).

## G2 — Sequential approximate isometries: multiplicative mass and target-error growth

### Reference solution

Let \(D_j=V_j^\dagger V_j-I\). This operator is Hermitian, and for every incoming bond vector \(z\), Cauchy–Schwarz and the induced norm give
\[
\big|\|V_jz\|_2^2-\|z\|_2^2\big|
=|\langle z,D_jz\rangle|
\le\eta_j\|z\|_2^2.
\]
Thus \((1-\eta_j)\|z\|^2\le\|V_jz\|^2\le(1+\eta_j)\|z\|^2\). To retain entangled prefixes, choose an orthonormal basis \(\{e_p\}\) of the already-emitted-bit space and write an arbitrary vector as \(y=\sum_pe_p\otimes z_p\). The vectors \(z_p\) need not be proportional or normalized. Orthogonality of the prefix labels gives
\[
\|y\|^2=\sum_p\|z_p\|^2,
\qquad\|(I\otimes V_j)y\|^2=\sum_p\|V_jz_p\|^2.
\]
Sum the bond inequalities to obtain the same factors \(1\pm\eta_j\) for every such \(y\). The basis regrouping in the question changes no norm. This proof does not assume the state factors between prefix and bond.

Apply that one-step bound to \(y=T_{j-1}v\). Since every \(1-\eta_j\) is positive, forward induction from \(T_0=I\) gives
\[
a_n\|v\|^2\le\|T_nv\|^2\le b_n\|v\|^2,
\quad a_n=\prod_{j=1}^n(1-\eta_j),\quad b_n=\prod_{j=1}^n(1+\eta_j).
\]
Equivalently \(a_nI\preceq T_n^\dagger T_n\preceq b_nI\). Diagonalize the finite-dimensional Hermitian operator \(T_n^\dagger T_n-I\): its eigenvalues belong to \([a_n-1,b_n-1]\). Therefore
\[
\|T_n^\dagger T_n-I\|_{\rm op}
\le\max\{1-a_n,b_n-1\}.
\]
One may simplify the maximum to \(b_n-1\): expansion of \(\prod(1+\eta_j)+\prod(1-\eta_j)\) contains twice the nonnegative even-degree elementary terms, including 1, so it is at least 2. The maximum form already proves the requested certificate. No replacement of \(b_n\) by \(1+\sum\eta_j\) is valid in general, because the positive cross terms are then lost. A weaker lower estimate \(a_n\ge1-\sum\eta_j\) is valid for \(0\le\eta_j\le1\), but may be nonpositive and is not needed.

For endpoint sharpness take every bond dimension one and let \(V_j^\pm z=\sqrt{1\pm\eta_j}\,z|0\rangle\), retaining the one-dimensional bond. Its local Gram operator is \((1\pm\eta_j)I\), so its defect is exactly \(\eta_j\). On initial scalar 1 the complete output is \(\prod_j\sqrt{1\pm\eta_j}\,|0\cdots0\rangle\), whose squared norm is exactly \(b_n\) for the plus train or \(a_n\) for the minus train. These are two legal trains, each attaining the corresponding endpoint; no claim is made that a single scalar train simultaneously attains unequal endpoints. In particular the upper global Gram bound can be attained.

Mass preservation does not identify a target. For \(n=1\) with one-dimensional input and terminal bonds, take \(V_1z=z|0\rangle\) and \(W_1z=z|1\rangle\). Both have Gram operator \([1]\), yet their outputs from 1 have inner product zero and Euclidean distance \(\sqrt2\), even after an arbitrary global phase is attached to either output. Their pure-state overlap fidelity is zero. Gram checks control how the map distorts input norms and inner products; they contain no alignment information with a specified emitted target vector or train. This obstruction uses no nonzero defect at all.

Now retain the additional hypotheses in the comparison branch. Write the lifted, regrouped maps as \(A_j=I\otimes V_j\) and \(B_j=I\otimes W_j\). The same prefix decomposition proves \(\|A_j\|_{\rm op}\le\sqrt{1+\eta_j}\), that \(B_j\) is an exact isometry, and that \(\|A_j-B_j\|_{\rm op}\le\epsilon_j\). The last assertion follows by applying \(\|(V_j-W_j)z_p\|\le\epsilon_j\|z_p\|\), squaring and summing; it is valid on entangled inputs as well. Hence \(\|S_{j-1}v\|=1\) when \(\|v\|=1\).

Set \(q_j=\|T_jv-S_jv\|\). Then \(q_0=0\), and the exact difference identity is
\[
T_jv-S_jv=A_j(T_{j-1}v-S_{j-1}v)+(A_j-B_j)S_{j-1}v.
\]
The triangle inequality yields
\[
q_j\le\sqrt{1+\eta_j}\,q_{j-1}+\epsilon_j.
\]
Induction unrolls this forward recurrence as
\[
q_n\le\sum_{k=1}^n\epsilon_k\prod_{j=k+1}^n\sqrt{1+\eta_j}.
\]
The discrepancy inserted at stage \(k\) is applied to an exact ideal prefix of norm one. It is subsequently propagated through the actual later maps \(V_{k+1},\ldots,V_n\), explaining precisely the later-stage weights. A telescoping expansion with ideal later maps would use different, earlier-stage growth factors; it must not be mixed with this recurrence.

The simple additive replacement fails even in dimension one. Use two stages, \(v=1\), \(W_jz=z|0\rangle\), and \(V_jz=(5/4)z|0\rangle\). Then
\[
\epsilon_1=\epsilon_2=1/4,\qquad
\eta_1=\eta_2=(5/4)^2-1=9/16<1.
\]
These are exact local operator differences and Gram defects. The output difference is
\[
\|(25/16)|00\rangle-|00\rangle\|=9/16>1/2=\epsilon_1+\epsilon_2.
\]
The stated weighted bound is \((1/4)(5/4)+1/4=9/16\), so it is attained in this example. The norm of the actual output is \(25/16\); this is exactly why ordinary unitary telescoping cannot be imported unchanged. Nothing here identifies an unnormalized linear action with a physical channel.

For \(n=0\), \(T_0=S_0=I\), both products are one, the global Gram defect is zero and the comparison sum is zero. For the zero input \(v=0\), linearity makes both outputs zero and the mass inequalities hold with equality; this replaces the comparison branch's unit-input premise rather than asserting that zero is a unit vector. When all \(\eta_j=0\), every \(V_j\) is an exact isometry, the mass is preserved and the weighted comparison bound reduces to \(\sum_j\epsilon_j\); target fidelity still needs the comparison hypotheses, as the orthogonal example shows.

For the requested strictness diagnostic replace one local restriction by \(\eta_j=1\). With one-dimensional bonds and \(n=1\), take \(V_1=0\); then \(\|V_1^\dagger V_1-I\|=1\) but the output from 1 has zero mass. The nonnegative lower factor becomes zero, so the positive lower-mass conclusion is lost. This witness is outside the original strict \(\eta_j<1\) regime. Under that original regime a supplied map is injective, which already forces \(d_{j-1}\le2d_j\); the proof does not assert existence of such maps for incompatible dimensions.

Finally, rectangular approximate maps with norm gain are not themselves unitary gates. A unitary realization, a finite gate set and its approximation cost, and a physical preparation mechanism would need separate constructions. Nor does norm preservation force a chosen terminal bond label: an exact one-stage isometry may output \(|0\rangle\otimes|1\rangle\) in a two-dimensional terminal bond while the desired clean label is \(|0\rangle\). Thus the theorem retains the entire terminal bond and proves neither its cleanup nor a synthesis result.

### Partial credit

- **2 points:** Derives the local quadratic-form bounds from the Hermitian Gram defect (1), and extends them to all passive-prefix inputs by a valid orthogonal-block, spectral or tensor-operator argument without assuming a product state (1).
- **2 points:** Proves the all-length lower/upper mass products, including the empty base and positivity of the lower factors (1); deduces the global operator Gram norm bound from all-vector/Hermitian control (0.5); gives legal scalar trains attaining each endpoint (0.5). An unsupported replacement by an additive upper mass bound loses the affected credit.
- **1 points:** Provides and computes a defect-zero pair with orthogonal outputs (0.5), and clearly distinguishes norm/inner-product control from target alignment (0.5). A mere global-phase example is insufficient for the expressly requested orthogonal witness.
- **2.5 points:** In the separate comparison branch, justifies spectator-stable bounds for V_j-W_j and exact ideal-prefix norm one (0.5), derives the ordered difference recurrence (1), and proves the requested sum with later-stage growth products (1). May use an equivalent telescoping proof if it produces the stated bound and preserves all additional hypotheses.
- **1 points:** Supplies an actual two-stage example satisfying eta_j<1 and the local epsilon bounds, computes an output error greater than epsilon_1+epsilon_2, and explains the nonisometric growth. The rational 5/4 example is not required specifically.
- **1.5 points:** Handles n=0, v=0 and eta=0 in their proper scopes (0.5); gives a legal eta=1 zero-output diagnostic while explicitly replacing the strict premise (0.5); and distinguishes the retained terminal bond and approximate linear maps from physical unitary synthesis/cleanup claims (0.5).

Equivalent valid mathematical arguments receive the same substantive credit. Evidence status and formal identifiers are in the complete QA packet, outside the question.

### Boundary cases

- **case:** Empty chain **resolution:** Both compositions are identities, mass factors are one and comparison error is zero.
- **case:** Zero input **resolution:** Mass equality and zero outputs hold by linearity; this does not satisfy the comparison branch unit-input premise.
- **case:** Exact local isometries **resolution:** Mass is exact and target-error weights are one, but target alignment remains a separate condition.
- **case:** Defect bound equals one **resolution:** Replace eta<1 by eta=1; the zero map can annihilate a nonzero input, so positive lower mass fails.
- **case:** Incompatible dimensions **resolution:** Eta<1 implies injectivity and therefore d_{j-1}<=2d_j; supplied-map premises have no realization otherwise.
- **case:** Nontrivial terminal bond **resolution:** The entire terminal bond remains part of the output; norm control does not select a clean label.

### Common errors

- Assuming prefix/bond product structure and omitting entangled inputs.
- Replacing the multiplicative upper mass bound by 1+sum eta without its positive cross terms.
- Inferring target fidelity from exact local orthogonality or normalization.
- Applying unitary telescoping to V_j while its norm can exceed one.
- Placing earlier-stage rather than later-stage growth weights in the stated recurrence proof.
- Using the comparison result without an ideal isometry supplier and local target alignment.
- Treating eta=1 or v=0 counterexamples as satisfying strict-defect or unit-input premises.
- Identifying an unnormalized linear action with a physical deterministic channel or asserting terminal cleanup from mass alone.

### Author-supplied reasoning map

These are declared mathematical inputs and scoped claims, not extracted Lean proof-term dependencies.

#### Inputs

- **G2-I1** (assumption): Finite complex bond spaces, column-map convention, standard product metric and chronological norm-preserving regrouping.
- **G2-I2** (assumption): Main branch: ||V_j^dagger V_j-I||_op<=eta_j with 0<=eta_j<1.
- **G2-I3** (assumption): Arbitrary initial vector v for the mass theorem.
- **G2-I4** (conditional_branch_assumption): Comparison branch only: W_j exact isometries and ||V_j-W_j||_op<=epsilon_j, epsilon_j>=0.
- **G2-I5** (conditional_branch_assumption): Comparison branch only: ||v||=1.
- **G2-I6** (premise_replacement): Strictness diagnostic only: replace the relevant eta_j<1 condition by eta_j=1.

#### Steps

- **G2-S1: Obtain local quadratic-form bounds.** Inputs: G2-I1, G2-I2. Scope: main. Conclusion: (1-eta_j)||z||^2<=||V_jz||^2<=(1+eta_j)||z||^2 for every incoming z. Justification: D=V^dagger V-I is Hermitian; Cauchy-Schwarz bounds |<z,Dz>| by eta||z||^2.
- **G2-S2: Preserve the inequalities under passive prefixes, including entangled states.** Inputs: G2-I1, G2-S1. Scope: main. Conclusion: The same bounds hold for I_prefix tensor V_j on every prefix/bond vector; its norm is <=sqrt(1+eta_j). Justification: Expand y=sum_p e_p tensor z_p in an orthonormal prefix basis and sum squared norms. No factorization of y is assumed.
- **G2-S3: Establish the all-length multiplicative invariant.** Inputs: G2-I1, G2-I2, G2-I3, G2-S2. Scope: main. Conclusion: a_n||v||^2<=||T_nv||^2<=b_n||v||^2, a_n=product(1-eta), b_n=product(1+eta). Justification: Forward induction from T_0=I, multiplying nonnegative local factors.
- **G2-S4: Convert all-vector mass control to global operator Gram control.** Inputs: G2-I1, G2-S3. Scope: main. Conclusion: ||T_n^dagger T_n-I||<=max(1-a_n,b_n-1), and optionally <=b_n-1. Justification: The Hermitian quadratic-form bounds locate every eigenvalue; the optional simplification uses the nonnegative even-degree expansion.
- **G2-S5: Demonstrate sharp mass endpoints with actual trains.** Inputs: G2-I1, G2-I2. Scope: sharpness_witness. Conclusion: Dimension-one maps V_j^plus/minus z=sqrt(1 plus/minus eta_j) z|0> attain b_n/a_n respectively. Justification: Compute each scalar Gram defect and the product amplitude. These are separate witnesses, not simultaneous endpoints of one scalar map.
- **G2-S6: Refute target fidelity from Gram tests.** Inputs: G2-I1. Scope: counterexample. Conclusion: V z=z|0> and W z=z|1> both have zero defect and orthogonal outputs from 1. Justification: Direct inner product and norm computation. The exact-isometry property is checked for this witness; no zero local-target difference is assumed.
- **G2-S7: Supply all comparison operator bounds on the actual spaces.** Inputs: G2-I1, G2-I2, G2-I4, G2-I5, G2-S2. Scope: comparison_branch. Conclusion: Lifted actual maps have norm <=sqrt(1+eta_j), lifted differences have norm <=epsilon_j, and ||S_jv||=1. Justification: Repeat the orthogonal-prefix argument for V_j-W_j; exact ideal isometries preserve the unit initial norm.
- **G2-S8: Derive and unroll the ordered comparison recurrence.** Inputs: G2-I1, G2-I4, G2-I5, G2-S7. Scope: comparison_branch. Conclusion: q_j<=sqrt(1+eta_j)q_{j-1}+epsilon_j, q_0=0, hence q_n<=sum_k epsilon_k product_{j>k}sqrt(1+eta_j). Justification: Insert A_j(T_{j-1}-S_{j-1})+(A_j-B_j)S_{j-1}; the actual later maps propagate each inserted discrepancy.
- **G2-S9: Refute a naive additive comparison with legal nonisometric growth.** Inputs: G2-I1. Scope: counterexample. Conclusion: Two scalar stages V=(5/4)|0>, W=|0>, eta=9/16, epsilon=1/4 have error 9/16>1/2; the weighted bound equals 9/16. Justification: Compute both Grams, local differences and the two-stage output explicitly. All comparison premises are verified for this example.
- **G2-S10: Check empty-chain and zero-input mass boundaries.** Inputs: G2-I1, G2-I3. Scope: raw_boundary. Conclusion: At n=0 T_0=I and mass factors are one; at v=0 all actual outputs vanish. Justification: Definitions and linearity; this node does not retain the comparison unit-input premise.
- **G2-S11: Check comparison empty-chain and exact-isometry specializations.** Inputs: G2-I1, G2-I2, G2-I4, G2-I5, G2-S8. Scope: comparison_boundary. Conclusion: For n=0 the comparison error is zero; if every eta_j=0 then growth factors are one and the comparison bound is sum epsilon_j. Justification: Empty sum or substitution in the already proved bound; alignment hypotheses remain present.
- **G2-S12: Demonstrate loss of strict lower mass at defect one.** Inputs: G2-I1, G2-I6. Additional/scoped assumptions: G2-I6 replaces G2-I2 for this witness; do not assume eta<1.. Scope: excluded_domain_diagnostic. Conclusion: With n=1 and scalar bonds V=0 has defect one and sends initial 1 to zero. Justification: Compute V^dagger V-I=-I; the lower factor is zero.
- **G2-S13: Keep physical synthesis and cleanup separate.** Inputs: G2-I1, G2-I2. Scope: scope_boundary. Conclusion: The mathematics is a bound on full emitted vectors retaining the terminal bond; neither unitary synthesis nor a chosen clean label follows. Justification: The expanding scalar witness is not a unitary column; even an exact isometry can put terminal amplitude on a non-clean label. Under eta<1 supplied maps must be injective, so incompatible dimensions are unrealizable.

#### Reuse and route scopes

- **AND join policy:** Comparison steps require both ideal-isometry/local-alignment premises and the approximate-map growth control. Mass-only, orthogonality, zero-input and eta=1 diagnostics do not inherit irrelevant comparison premises. The eta=1 witness explicitly replaces strictness.
- **reused results:** **id:** spectator-stable-local-operator-bounds **producer step:** G2-S2 **consumer steps:** G2-S3; G2-S7 **assessment:** Derived for all prefix/bond vectors, not inferred from product inputs.; **id:** exact-sequential-mass **source nodes:** declaration:QuantumBlockEncoding.SequentialBondPreparation.amplitudeMass_run **relationship:** Exact source theorem is context and eta=0 special setting; no new approximate theorem is asserted compiled.
- **reconvergent branches:** **join:** G2-S8 **branches:** G2-S2; G2-I4; G2-I5; G2-S7 **why:** Target alignment must be joined with controlled actual growth and a unit ideal prefix; norm control alone is insufficient.

### Evidence limitations

- No Lean invocation, toolchain installation, formal proof admission, model evaluation or paid API was performed.
- The finite-grid and approximate-isometry results are original natural-language derivations; exact frozen source anchors do not establish their formal compilation.
- Independent exact-content review, semantic deduplication, split reconciliation and maintainer admission are pending at authoring time.
- No bit-operation complexity, physical circuit implementation or whole-graph coverage is claimed.

Full source roles, review bindings and provisional difficulty: [complete packet](qa/G2.json).

## P1 — A reversible finite-bit phase supplier with a reusable gradient catalyst

### Reference solution

Write \(T_q|y\rangle=|y+q\bmod M\rangle\). Relabel the finite Fourier sum by \(z=y+q\bmod M\). For the unique representative \(y\in\{0,\ldots,M-1\}\), the integers \(y\) and \(z-q\) differ by a multiple of \(M\), so their exponential factors agree. Therefore
\[
T_q|G_m\rangle
=M^{-1/2}\sum_z e^{2\pi i(z-q)/M}|z\rangle
=e^{-2\pi iq/M}|G_m\rangle.
\]
The sign is negative for the positive Fourier exponent specified in the question. A negative Fourier exponent, or subtraction instead of addition, reverses it. This is an exact modular identity, including wrapped additions.

First construct the promised adder. For a fixed bit \(Q_j\), adding \(2^j\) to \(Y\) when \(Q_j=1\) is a conditional increment of the suffix beginning at \(j\). The target bit \(Y_i\), for \(i\geq j\), flips exactly when
\[
Q_j\prod_{r=j}^{i-1}Y_r=1,
\]
where the empty product for \(i=j\) is one. These are the OLD suffix bits. Visiting \(i=m-1,m-2,\ldots,j\) preserves every lower controlling bit until all targets that need it have been processed. Thus the stated multi-controlled flips implement the binary carry rule, discard overflow modulo \(2^m\), and preserve \(Q\). In contrast, flipping from the low bit upward with these same controls would inspect changed bits and implement the wrong rule. Applying the increments for all \(j\) adds \(\sum_j2^jQ_j=q\) modulo \(M\), because each increment has the proved action on the word presented to it.

A NOT with two controls is one Toffoli. For \(k\geq3\) controls \(c_1,\ldots,c_k\), use \(k-2\) fresh-zero scratch bits. Compute \(a_1=c_1c_2\), then \(a_2=a_1c_3\), up to \(a_{k-2}=c_1\cdots c_{k-1}\), by \(k-2\) Toffolis. Flip the designated target with controls \(a_{k-2},c_k\), then reverse those \(k-2\) computations. None of the original controls has changed. The scratch returns exactly to zero, and the total is \(2k-3\) Toffolis. All targets, controls and scratch in this construction are distinct. The \(k=2\) formula gives one Toffoli and zero scratch; the one-control case is CNOT.

The suffix increment contains one CNOT at its lowest target. Its target \(i=j+d\), \(d\geq1\), has \(k=d+1\) controls and therefore costs \(2d-1\) Toffolis. Reuse the clean chain after each flip. The whole adder has
\[
C_{\mathrm{CX}}(m)=m,\qquad
T(m)=\sum_{d=1}^{m-1}(m-d)(2d-1)
=\frac{m(m-1)(2m-1)}6,
\qquad a_m=\max(m-2,0)
\]
Toffolis and simultaneously live scratch bits, respectively. The polynomial follows from the elementary sums of \(d\) and \(d^2\); it is also \(\sum_{r=1}^{m-1}r^2\). There are no X, H or phase gates in this adder. The result is a deliberately simple exact construction, not an optimality claim. Since each elementary gate is reversible and each scratch chain is uncomputed on every basis input, linearity gives the clean action on arbitrary entangled inputs as well.

Now let \(K\) denote chronological application of \(B\), this adder on \((Q,Y,A)\), and \(B^\dagger\) on \((X,Q,W)\). In the fixed order \((X,Q,W,Y,A)\), the basis-state transcript is
\[
\begin{aligned}
|x,0,0\rangle|G_m\rangle|0\rangle
&\xrightarrow{B}|x,q_x,\gamma_x\rangle|G_m\rangle|0\rangle\\
&\xrightarrow{\mathrm{ADD}}
e^{-2\pi iq_x/M}|x,q_x,\gamma_x\rangle|G_m\rangle|0\rangle\\
&\xrightarrow{B^\dagger}
e^{-2\pi iq_x/M}|x,0,0\rangle|G_m\rangle|0\rangle.
\end{aligned}
\]
The adder preserves both \(Q\) and \(W\), so the supplied full inverse really applies to the same \((q_x,\gamma_x)\) record that \(B\) produced. It is not enough to clear only \(Q\). The inverse is available here because the entire circuit list was supplied: reverse its order, since X, CNOT and Toffoli are all self-inverse. No controlled inverse of a black box has been assumed. For every normalized coherent input \(\sum_xc_x|x\rangle\), linearity gives
\[
K\left(\sum_xc_x|x\rangle|0_Q0_W\rangle|G_m\rangle|0_A\rangle\right)
=\left(\sum_xc_xe^{-2\pi iq_x/M}|x\rangle\right)
 |0_Q0_W\rangle|G_m\rangle|0_A\rangle.
\]
The catalyst factorizes exactly and all other ancillary registers are zero. The same argument holds with an untouched reference entangled with the data. Tracing out the supplier record instead would multiply data coherences by \(\langle q_{x'},\gamma_{x'}|q_x,\gamma_x\rangle\), generally deleting coherence between unequal records; it would also not return the promised workspace. Equal-record or single-input exceptions do not certify the arbitrary-input clean interface. Neither a measurement nor amplification is needed here.

The binary expansion of \(y\) factorizes the gradient:
\[
|G_m\rangle=
\bigotimes_{r=0}^{m-1}
\frac{|0\rangle+e^{i\theta_r}|1\rangle}{\sqrt2},
\qquad \theta_r=\frac{2\pi2^r}{2^m}.
\]
Thus apply H and then \(P(\theta_r)\) on each physical bit \(Y_r\). This preparation \(F_m\) costs \(m\) H and \(m\) P gates in the declared logical model. Its inverse applies \(P(-\theta_r)\) and then H on each bit. The physical ordering is little-endian; no bit reversal or hidden quantum Fourier transform is required.

For \(L\) uses of the same supplier, the exact total gate counts, starting with all ancillary registers zero, are
\[
\begin{array}{c|cc}
\text{gate class}&\text{catalyst returned}&\text{final coherent reset}\\\hline
X&2Lb_X&2Lb_X\\
\mathrm{CX}&2Lb_{\mathrm{CX}}+Lm&2Lb_{\mathrm{CX}}+Lm\\
\mathrm{CCX}&2Lb_{\mathrm{CCX}}+LT(m)&2Lb_{\mathrm{CCX}}+LT(m)\\
H&m&2m\\
P\text{ or }P^\dagger&m&2m
\end{array}
\]
There are \(L\) forward and \(L\) inverse supplier executions and \(L\) adders. Any separately chosen data-only unitaries are additional and must be charged separately. The maximum live width of the displayed implementation is
\[
n+2m+w+a_m.
\]
It includes the output word, all supplier garbage, the catalyst and the adder scratch; reusing zero scratch after each gate does not remove its peak-width cost. The same width suffices for final reset. In the first column \(Y\) returns as the specified nonzero catalyst, not as a clean-zero ancilla. In the second, \(F_m^\dagger\) restores it to zero after the last use. If a ready catalyst is already supplied, the initial \(m\) H and \(m\) P charge is an external preparation cost rather than a repeated per-use cost.

For the stability question, include every supplier, adder and interleaved data-only unitary in one unitary \(\mathcal C_L\). On the exact gradient sector it satisfies
\[
\mathcal C_L(|\psi\rangle|0_{QWA}\rangle|G_m\rangle)
=|\Phi_\psi\rangle|0_{QWA}\rangle|G_m\rangle,
\]
where \(|\Phi_\psi\rangle\) is the ideal data output for that entire sequence. Register notation here merely groups the already fixed wires. Put \(|\widetilde G_m\rangle=\widetilde F_m|0\rangle\). Unitarity of the WHOLE sequence yields
\[
\left\|\mathcal C_L(|\psi\rangle|0\rangle|\widetilde G_m\rangle)
-|\Phi_\psi\rangle|0\rangle|G_m\rangle\right\|_2
=\|\widetilde G_m-G_m\|_2\leq\eta.
\]
There is no factor \(L\): the sole error was in the initial vector, and exact unitary evolution preserves its norm. Q, W and A are in fact still restored exactly even for a non-eigenstate catalyst, because ADD preserves the supplier record and returns its own scratch on every Y basis state. Y can become entangled with the data; exact gradient return or exact factorization does not follow for \(\widetilde G_m\).

After the actual inverse \(\widetilde F_m^\dagger\), a triangle decomposition gives full clean-zero error at most
\[
\eta+\left\|\widetilde F_m^\dagger|G_m\rangle-|0^m\rangle\right\|_2
=\eta+\left\||G_m\rangle-\widetilde F_m|0^m\rangle\right\|_2\leq2\eta.
\]
Both outputs are unit vectors, so this bound can also be capped at 2. It is a bound, not an assertion of exact reset or an optimal constant. Errors in every adder or supplier would be a different model, where repeated-operation bounds can accumulate. Actual preparation/inverse gate costs must replace the ideal \(m\)-gate counts when \(\widetilde F_m\) is used; a vector-error certificate alone gives no synthesis cost.

At \(m=1\), \(|G_1\rangle=(|0\rangle-|1\rangle)/\sqrt2\), the adder is one CNOT, and \(T(1)=a_1=0\). This is the Boolean kickback special case. If one explicitly extends to \(m=0\), then \(M=1\), Q and Y are trivial, \(q_x=0\), and \(D_q=I\). No adder, catalyst preparation or scratch is needed; one can omit B entirely. If the redundant B-then-inverse route is nevertheless retained, its actual \(2L g_B\) cost and any W width remain. There is no division by a nonexistent bit index.

The finite-word supplier, exact reversible arithmetic, logical phase gates and optional approximate catalyst have separate contracts. No arbitrary real phase is claimed to have an efficient supplier, no accuracy to any unspecified real target phase is proved, and the supplied list length need not be polynomial. Exact dyadic P gates are allowed by the declared logical model; a fixed finite gate set, its approximation error, connectivity/depth, and any classical compiler require their own analysis. The source's phase-aware primitive program conventions do not identify its primitive-gate counts with these macro counts.

### Partial credit

- **1.5 points:** Derives the negative kickback eigenvalue by a modular change of variable and proves full coherent B/ADD/B-dagger action, including all supplier garbage and clean scratch; an untracked phase or omitted garbage cleanup loses credit.
- **2.0 points:** Proves the arbitrary-width descending carry-controlled increment and clean conjunction-chain implementation; derives m CNOT, m(m-1)(2m-1)/6 Toffoli and max(m-2,0) scratch. Equivalent exact count expressions earn full credit; finite examples alone do not.
- **1.0 points:** Constructs the little-endian product preparation and actual inverse using H then P on each bit, with exact phase convention and m+m preparation counts.
- **2.0 points:** Gives the complete L-use supplier/inverse/adder/preparation ledger and live width, distinguishing reusable nonzero catalyst return from final clean-zero reset; separately charges any interleaved data gates and does not infer supplier efficiency from m output bits.
- **2.0 points:** Uses one global unitary to prove <=eta full-output error independent of L from initial catalyst error alone, proves <=2eta after the actual approximate-preparation inverse, and explains why exact catalyst factorization/reset need not hold.
- **1.5 points:** Explains trace-out versus coherent cleanup, actual inverse availability, m=1 and optional m=0, and the distinction between the logical dyadic-phase model, finite words and unproved fixed-finite-gate synthesis/resource guarantees.

Equivalent valid mathematical arguments receive the same substantive credit. Evidence status and formal identifiers are in the complete QA packet, outside the question.

### Boundary cases

- **case:** m=1 **consequence:** The catalyst is the minus state; one CNOT and zero Toffoli/scratch implement the adder.
- **case:** Explicit m=0 extension **consequence:** Target is identity, so all supplier calls can be omitted; a deliberately retained redundant B/B-dagger must still be charged.
- **case:** Supplier garbage nonzero or colliding records **consequence:** B-dagger restores the exact full record; tracing only happens to preserve coherence within equal-record classes and does not satisfy the general clean interface.
- **case:** Approximate catalyst **consequence:** QWA still return clean under exact reversible arithmetic, but Y may entangle with data; eta and 2eta are vector-error bounds, not exact resets.
- **case:** Approximate gates on every use **consequence:** Outside the initial-catalyst-only error model; the no-L factor cannot be transferred without further analysis.
- **case:** Gate model **consequence:** Dyadic phases are ideal declared logical gates; no optimality, fixed-finite-gate synthesis, connectivity or depth theorem is asserted.

### Common errors

- Using a positive kickback phase with the specified positive Fourier exponent and addition.
- Incrementing low bits first while testing changed lower bits as if they were original carry bits.
- Charging a multi-controlled NOT as one Toffoli, or leaving its conjunction-chain scratch dirty.
- Applying inverse computation only to the output word while ignoring supplier garbage.
- Treating a returned gradient state as a clean-zero register, or charging preparation on every reuse without explanation.
- Obtaining B-dagger from unsupported forward-only black-box access instead of the supplied reversible gate list.
- Multiplying a single initial catalyst state error by L without analyzing the exact global unitary, or conversely claiming the approximate catalyst factorizes exactly.
- Promoting finite-word arithmetic and ideal dyadic phase gates to an unproved fixed-finite-gate synthesis or polynomial supplier theorem.

### Author-supplied reasoning map

These are declared mathematical inputs and scoped claims, not extracted Lean proof-term dependencies.

#### Inputs

- **I1** (typing_and_convention): m >= 1, M=2^m; register order and little-endian binary convention.
- **I2** (assumption): The actual reversible gate list B, exact full clean-input action including gamma_x, and gate counts g_B.
- **I3** (definition): The positive-exponent normalized Fourier gradient and negative-phase target D_q.
- **I4** (resource_model): Declared logical X/CNOT/Toffoli/H/dyadic-P gates and clean zero scratch.
- **I5** (assumption): L >= 1; coherent uses may be interleaved with data-only unitaries.
- **I6** (conditional_assumption): For the stability branch only, actual unitary F_tilde, actual inverse, initial vector error <= eta, and otherwise exact circuits.
- **I7** (replacement_case_assumption): Separate optional boundary replacing I1: m=0, M=1, Q/Y trivial and q_x=0. If a redundant supplier is retained, its entire X/W reversible list and count are still supplied.

#### Steps

- **S1: Descending controlled flips realize a suffix increment on every word.** Inputs: I1, I4. Conclusion: For target i >= j the OLD lower-bit carry is Q_j product_{r=j}^{i-1}Y_r; descending order preserves those controls. Justification: The binary carry rule AND descending order give addition modulo 2^m; overflow is dropped.
- **S2: Conjunction chains realize each multi-controlled NOT and clean scratch.** Inputs: I4. Conclusion: k controls cost 2k-3 Toffolis and k-2 scratch for k>=2; k=1 costs one CNOT. Justification: Compute k-1-control conjunction, apply target flip, then reverse the unchanged-control computation.
- **S3: The complete adder has an arbitrary-width correctness and cost proof.** Inputs: I1, S1, S2. Conclusion: ADD preserves Q, adds q to Y modulo M, and restores A; counts m CNOT, m(m-1)(2m-1)/6 Toffoli, max(m-2,0) scratch. Justification: Compose all weighted increments AND sum all controlled-flip costs; scratch is reused only after its return to zero.
- **S4: Fourier translation gives the exact kickback eigenvalue, including wrap.** Inputs: I1, I3, S3. Conclusion: T_q G_m=exp(-2pi i q/M) G_m. Justification: Relabel by z=y+q modulo M; changes by integer multiples of M do not change the exponential.
- **S5: The supplied list provides the actual inverse and complete coherent cleanup.** Inputs: I2, S3, S4. Conclusion: B;ADD;B-dagger implements D_q, returns QWA to zero and factorizes the gradient on every coherent input. Justification: B-dagger is the reversed self-inverse gate list; ADD preserves both q and gamma, so inverse cancellation AND the eigenvalue identity apply.
- **S6: The gradient has a concrete product preparation and inverse.** Inputs: I1, I3, I4. Conclusion: F_m uses m H and m dyadic P gates; F_m-dagger uses their reversed inverses. Justification: Factor the phase using the little-endian binary expansion of y.
- **S7: Every use and initialization/reset have separate exact ledger entries.** Inputs: I1, I2, I4, I5, S3, S5, S6. Conclusion: L times the supplier/inverse/adder counts plus one F_m, and optionally one F_m-dagger; width n+2m+w+max(m-2,0). Justification: Clean per-use registers can be reused; the nonzero catalyst is not a clean-zero ancilla until its final inverse preparation.
- **S8: A single approximate initial catalyst has a norm-preserved error through all uses.** Inputs: I5, I6, S3, S5. Conclusion: Full error relative to ideal data tensor exact G_m is <= eta independent of L; QWA still clean, Y need not factorize. Justification: All operations form one unitary AND the exact-gradient sector has the required invariant action.
- **S9: Actual approximate-preparation inverse gives a bounded, not exact, clean reset.** Inputs: I6, S8. Conclusion: Full error relative to ideal data tensor all zeros is <= 2 eta (also <=2). Justification: Triangle inequality combines propagated initial error with norm(F_tilde-dagger G_m - zero)=norm(G_m-F_tilde zero).
- **S10: One-bit and resource-model boundaries preserve the advertised meaning.** Inputs: I1, I2, I4, S3, S6, S7. Conclusion: m=1 is one-CNOT Boolean kickback; no supplier efficiency or fixed-finite-gate synthesis follows. Justification: Evaluate the nonnegative-width formulas at m=1; distinguish the declared ideal gate model and supplied list from additional compilation promises.
- **S11: The explicitly separate zero-bit extension is an identity route.** Inputs: I4, I5, I7. Additional/scoped assumptions: Use I7 in place of I1; none of S1-S10 is a premise for this boundary.. Conclusion: No catalyst or adder gates are needed and B may be omitted; retaining B and its reverse still costs 2L g_B and any supplier work width. Justification: The only word has q=0, so its phase is 1. The optional redundant supplied reversible list cancels with its reverse independently of any positive-width carry proof.

#### Reuse and route scopes

- **reused results:** **result:** Source fixed three-bit modular addition and three-control clean-chain pattern. **consumers:** S1; S2; S3 **status:** Inspected finite-width substrate only; arbitrary-width proof and counts are derived explicitly here.; **result:** Exact phase-aware program composition and dagger semantics. **consumers:** S4; S5 **status:** Inspected convention, not a compiled phase-gradient theorem.; **result:** Boolean one-bit phase kickback (qcb-core-plan-519). **consumers:** S10 **status:** Disclosed strict m=1 special case; not counted as the new assessed target.
- **reconvergent branches:** **branches:** S3; S4; I2 **join:** S5 **meaning:** Correct/clean arithmetic AND Fourier eigenstate AND full reversible supplier are all needed.; **branches:** S5; S6 **join:** S7 **meaning:** Reusable action and actual initial preparation jointly justify amortized costs.; **branches:** I6; S8 **join:** S9 **meaning:** Actual inverse access and initial-state propagation jointly justify the final reset bound.
- **case scopes:** **exact main:** **steps:** S1; S2; S3; S4; S5; S6; S7; S10 **approximate preparation:** **premise:** I6 **steps:** S8; S9 **zero bit extension:** **replacement premise:** I7 **excluded main premise:** I1 **steps:** S11 **note:** The identity route may omit B; retaining a redundant B/B-dagger still costs its gates.

### Evidence limitations

- Original natural-language derivation only; no Lean execution, kernel replay, axiom audit or production-source change was performed.
- Author freeze is awaiting distinct answer-blind derivation and comparison. This author claims no independent review or approval.
- Source inspection grounds conventions and explicitly limited formal substrate, not the complete new mathematical target.
- Frozen graph identities represent declared source ownership and navigation, not extracted theorem-proof dependencies or new formal theorem closure.
- Global semantic deduplication, split assignment, release admission and measured model difficulty/performance remain unresolved.
- No paid model run, training, inference experiment, system installation, commit or push was performed by this worker.

Full source roles, review bindings and provisional difficulty: [complete packet](qa/P1.json).

## P2 — Sharp coherent error from approximate basis-column guarantees

### Reference solution

For a column coefficient vector \(c\in\mathbb C^N\), linearity gives \(Ec=\sum_j c_jEe_j\). With the stated inner-product convention,
\[
\|Ec\|_2^2=\sum_{j,k}\overline{c_j}c_k\langle Ee_j,Ee_k\rangle
=c^\dagger Gc,
\qquad G=E^\dagger E.
\]
Thus G is Hermitian positive semidefinite, its diagonal is \(G_{jj}=\|Ee_j\|_2^2\), and finite-dimensional spectral theory gives
\[
\|E\|^2=\max_{\|c\|_2=1}c^\dagger Gc=\lambda_{\max}(G).
\]
One may also expand the isometry identities to obtain \(G=2I-U^\dagger V-V^\dagger U\). The off-diagonal entries record coherent correlations of error vectors. Orthogonality of the columns of U and of V separately does not force the columns of their difference to be orthogonal.

Put \(r=(\sum_j\varepsilon_j^2)^{1/2}\). For every unit c, triangle inequality and scalar Cauchy-Schwarz give
\[
\|Ec\|_2\leq\sum_j|c_j|\|Ee_j\|_2
\leq\sum_j|c_j|\varepsilon_j\leq r.
\]
Equivalently \(\lambda_{\max}(G)\leq\operatorname{tr}G\leq r^2\). Since U and V are isometries, \(\|Uc\|_2=\|Vc\|_2=1\), so \(\|Ec\|_2\leq2\). Hence the universal bound is
\[
\boxed{\ \|V-U\|\leq\min\!\left\{2,\sqrt{\sum_j\varepsilon_j^2}\right\}.\ }
\]
There is no statistical-independence assumption or cancellation premise in this estimate.

Here is sharpness even among square unitaries, for each fixed nonnegative tolerance vector. If \(r=0\), choose \(U=V=I\); the zero upper bound is attained. If \(r>0\), define the real nonnegative unit vector \(s=\sum_j(\varepsilon_j/r)e_j\), its rank-one orthogonal projector \(P=|s\rangle\langle s|\), and \(\kappa=\min(2,r)\). Choose a real \(\theta\in[0,\pi]\) such that \(|e^{i\theta}-1|=\kappa\), for example \(\theta=2\arcsin(\kappa/2)\). Set
\[
U=I,\qquad V=I+(e^{i\theta}-1)P=(I-P)+e^{i\theta}P.
\]
The two orthogonal sectors \(\operatorname{ran}P\) and \(\ker P\) receive unit-modulus eigenvalues, so \(V^\dagger V=I\). More explicitly, the mixed products vanish because \(P(I-P)=0\), and both sector products sum to I. Moreover
\[
\|(V-I)e_j\|_2
=\kappa|\langle s,e_j\rangle|
=\kappa\frac{\varepsilon_j}{r}\leq\varepsilon_j,
\qquad \|V-I\|=\kappa\|P\|=\kappa.
\]
The inequality uses \(\kappa\leq r\). Thus the claimed bound cannot be decreased using only those column tolerances, even with full unitarity imposed. For \(r\leq2\), all specified column bounds are attained simultaneously; for \(r>2\), they remain valid upper bounds while the unitary cap is attained. Zero components of the tolerance vector create zero components of s and exactly zero corresponding column errors.

For a uniform tolerance \(\varepsilon_j=\varepsilon\), this reduces to
\[
\|V-U\|\leq\min\{2,\sqrt N\,\varepsilon\},
\]
with transition at \(\varepsilon=2/\sqrt N\). For \(N>1\) the dimension-free assertion \(\|E\|\leq\max_j\varepsilon_j\) is false in general. It is sometimes true for particular error geometry or loose tolerances; the counterexample refutes the universal implication, not every instance.

For a concrete operational witness, take \(N\geq2\),
\[
s=N^{-1/2}\sum_{j=0}^{N-1}e_j,\qquad
U=I,\qquad V=I-2|s\rangle\langle s|.
\]
Then \(V^\dagger V=I\), every column error is exactly \(2/\sqrt N\), and \(\|V-I\|=2\). The column errors tend to zero as N increases, including along qubit dimensions \(N=2^n\). On the saturating input s, the actual output is \(-s\). The vector distance is 2 but the two density matrices are identical, so their trace distance is 0: this input alone detects the chosen representative convention, not an operationally distinguishable physical state.

Now define \(t=(e_0-e_1)/\sqrt2\); it is a unit vector orthogonal to s. For the normalized input \(h=(s+t)/\sqrt2\),
\[
Uh=h=\frac{s+t}{\sqrt2},\qquad
Vh=k=\frac{-s+t}{\sqrt2},\qquad
\langle h,k\rangle=0.
\]
The vector difference is \(-\sqrt2s\), of norm \(\sqrt2\). With \(\rho=|h\rangle\langle h|\) and \(\sigma=|k\rangle\langle k|\), the difference has eigenvalue +1 on h, -1 on k and zero on their orthogonal complement. Therefore \(\|\rho-\sigma\|_1=2\) and the stipulated trace distance is 1. The projective measurement \(\{|h\rangle\langle h|,I-|h\rangle\langle h|\}\) returns its first outcome with probabilities 1 and 0. This establishes a fully distinguishable coherent-output failure despite small errors on every basis input.

The exact additional condition for a desired bound \(\|E\|\leq b\), \(b\geq0\), is \(G\preceq b^2I\). A concrete sufficient geometry for \(b=\max_j\varepsilon_j\) is pairwise orthogonality of the error columns: then G is diagonal and
\[
\|E\|=\max_j\|Ee_j\|_2\leq\max_j\varepsilon_j.
\]
In an explicitly label-preserving controlled comparison, differences of the form \(|j\rangle\otimes(v_j-u_j)\) are orthogonal for distinct j because the labels are orthogonal. That is an additional output interface. It does not follow merely by writing a coherent input as a linear combination. In the present reflection witness all error columns point in the same direction s, which is precisely the opposite geometry. The controlled-label comparison therefore does not contradict the sharp square-unitary result and supplies no free extra label or workspace cleanup.

If every tolerance is zero, exact equality on the entire input basis gives E=0 by linearity. Individual zero tolerances force only their own columns to agree. At \(N=1\), \(\min(2,\varepsilon_0)\) is still sharp for square unitaries, using a scalar phase. The reflection-interference example requires \(N\geq2\); in the one-dimensional square case all unitary output vectors differ only by global phase, although the representative-wise operator distance can be nonzero. Isometries into a larger output space remain covered by the bound but need not share that one-dimensional physical equivalence. No output phase is independently optimized for each input in this problem, and probability agreement is not the stated hypothesis. The proof concerns full columns, not scalar entrywise errors, and derives no circuit realization or oracle cost.

### Partial credit

- **1.5 points:** Derives the conjugation-correct quadratic form, PSD Gram matrix and largest-eigenvalue characterization; identifies off-diagonal error correlations rather than assuming errors orthogonal.
- **1.5 points:** Proves min(2,sqrt(sum epsilon_j^2)) using all column promises and the isometry cap, and states the sharp uniform sqrt(N) consequence and cap threshold.
- **3.0 points:** Constructs and verifies square unitaries attaining the bound for EVERY nonnegative tolerance vector, with r=0 separated, each column promise checked, and both r<=2 and r>2 handled. An arbitrary unconstrained matrix or only a uniform example earns partial credit.
- **2.0 points:** Provides and verifies any valid unitary family with all basis-column errors tending to zero and maximal operator distance, plus an explicit normalized interference input with orthogonal outputs and a distinguishing measurement. Computes vector distance sqrt2 and half-trace-norm distance 1 for that input, and correctly separates a saturating global-sign input with physical trace distance 0. The uniform rank-one reflection is one sufficient route; equivalent valid constructions receive the same credit.
- **1.0 points:** Gives a sufficient error-geometry condition such as orthogonal error columns, justified by the Gram matrix, and explains the retained-label boundary without pretending linearity supplies the extra output label.
- **1.0 points:** Handles zero tolerances and N=1, preserves complete-output/representative-wise assumptions and the distinction from entrywise or probability promises; no circuit or cleanup resource claim is inferred.

Equivalent valid mathematical arguments receive the same substantive credit. Evidence status and formal identifiers are in the complete QA packet, outside the question.

### Boundary cases

- **case:** r=0 **consequence:** Every error column is zero, so E=0; choose identical unitaries without normalizing an absent direction.
- **case:** Some epsilon_j=0 **consequence:** Those columns agree exactly; the rank-one saturating vector has zero corresponding components.
- **case:** r>2 **consequence:** The norm-two isometry cap is active; sharpness need only satisfy, not saturate, each loose column tolerance.
- **case:** N=1 **consequence:** The numerical bound is still sharp by scalar phases; the square one-dimensional case has no two-sector interference witness.
- **case:** Retained orthogonal labels **consequence:** They can force orthogonal error columns, an additional interface absent from general square-unitary comparisons.
- **case:** Phase-quotiented or probability promise **consequence:** A different hypothesis; the reference-wise Gram argument cannot silently adopt it.

### Common errors

- Using max_j epsilon_j without controlling cross-column error correlations.
- Assuming orthonormal columns of U and V make the difference columns orthogonal.
- Using an arbitrary error matrix to claim sharpness while failing the unitary/isometry premises.
- Omitting the norm-two isometry cap or dividing by r when all tolerances vanish.
- Offering only an overall-sign input as a physical distinguishability witness.
- Confusing vector distance 2, vector distance sqrt2, trace norm 2 and trace distance 1.
- Silently weakening the full-output Euclidean guarantee to measurement probabilities or independently chosen column phases.
- Counting the retained-label orthogonality comparison or the existing entrywise N-epsilon example as the new assessed result.

### Author-supplied reasoning map

These are declared mathematical inputs and scoped claims, not extracted Lean proof-term dependencies.

#### Inputs

- **I1** (assumption): N>=1; U,V are isometries with common finite complex input/output carriers.
- **I2** (assumption): Every epsilon_j>=0 bounds the exact full-output column error norm.
- **I3** (definition_and_convention): E=V-U; G_jk=<Ee_j,Ee_k>; inner product conjugate-linear first, induced Euclidean operator norm.
- **I4** (convention): Trace distance means one-half the trace norm, with no phase quotient in the vector/operator promise.

#### Steps

- **S1: The complete coherent error is a Gram quadratic form.** Inputs: I1, I3. Conclusion: ||Ec||^2=c-dagger G c, G=E-dagger E>=0, ||E||^2=lambda_max(G). Justification: Expand linearity with conjugation in the first argument; maximize the Hermitian quadratic form.
- **S2: Column data give an l2 aggregate bound while isometry gives the cap.** Inputs: I1, I2, I3, S1. Conclusion: ||E||<=min(2,r), r=sqrt(sum epsilon_j^2). Justification: Triangle plus Cauchy-Schwarz gives r; both outputs of a unit input have norm one, giving 2.
- **S3: Legal square unitaries saturate every tolerance vector by a case split.** Inputs: I1, I2, I3, S2. Conclusion: At r=0 use U=V=I. For r>0, P=|s><s| with s_j=epsilon_j/r and V=I+(exp(i theta)-1)P, |exp(i theta)-1|=min(2,r), attain the bound. Justification: First separate r=0. In the r>0 branch, orthogonal P/I-P sectors prove unitarity AND individual column calculations prove each promised inequality; division occurs only there.
- **S4: Uniform promises incur the sharp square-root-dimension factor.** Inputs: I2, S2, S3. Conclusion: Uniform bound min(2,sqrt(N) epsilon), sharp; cap threshold 2/sqrt(N). Justification: Specialize the nonuniform theorem, with the zero case handled separately.
- **S5: A reflection has vanishing basis-column errors and maximal operator distance.** Inputs: I1, I3, S3. Additional/scoped assumptions: Use N>=2 for the subsequent interference example.. Conclusion: For uniform s, V=I-2|s><s| has column errors 2/sqrt(N), operator norm difference 2. Justification: Apply the rank-one projector formula at theta=pi.
- **S6: The operational counterexample is not merely a global-sign witness.** Inputs: I1, I4, S5. Additional/scoped assumptions: N>=2 as in S5; do not apply this construction at N=1.. Conclusion: s maps to -s with trace distance 0; h=(s+t)/sqrt2 maps to k=(-s+t)/sqrt2 orthogonal to h, vector distance sqrt2 and trace distance 1. Justification: t=(e0-e1)/sqrt2 is unit and orthogonal to s; compute inner products AND eigenvalues of |h><h|-|k><k|; a projection onto h distinguishes perfectly.
- **S7: Orthogonal error columns are a sufficient additional geometry.** Inputs: I2, I3, S1. Additional/scoped assumptions: For the general norm-order equivalence, the scalar threshold b is real and nonnegative. The diagonal-Gram assertion does not need an additional threshold.. Conclusion: Diagonal G gives ||E||=max_j||Ee_j||; for every real b>=0, G<=b^2 I iff ||E||<=b. Justification: Spectral order bounds the quadratic form; an explicit retained label forces cross-error inner products to vanish.
- **S8: Zero and one-dimensional cases preserve the exact quantifiers.** Inputs: I1, I2, I3, I4, S1, S2. Additional/scoped assumptions: The r=0 branch excludes division by r in S3; the N=1 branch excludes the N>=2 witness S5-S6.. Conclusion: r=0 implies E=0 and is attained by U=V=I; N=1 still has the scalar-phase sharp cap, but no orthogonal t in the square one-dimensional output. Justification: Linearity extends zero columns; for N=1 the unitary is a scalar phase, distinct from larger-output isometries.

#### Reuse and route scopes

- **reused results:** **result:** Finite Hermitian spectral theorem, Cauchy-Schwarz and unitary norm preservation. **consumers:** S1; S2; S3; S7 **status:** Standard finite-dimensional mathematical tools; no new formal verification is claimed.; **result:** Prior B2 retained-label orthogonality mechanism. **consumers:** S7 **status:** Disclosed boundary comparison only; no phase-correction problem is recounted as new.
- **reconvergent branches:** **branches:** I1; I2; S1 **join:** S2 **meaning:** The isometry cap AND all individual column promises enter the sharp upper bound.; **branches:** S2; S3 **join:** S4 **meaning:** An upper bound and a legal unitary attaining it are both required for sharpness.; **branches:** S5; I4 **join:** S6 **meaning:** The reflection action and precise physical-state metric give an operational witness distinct from global sign.
- **case scopes:** **sharpness case split:** **steps:** S3 **branches:** r=0: identical unitaries, no division; r>0: normalized rank-one phase construction **zero tolerance boundary:** **premise:** r=0 **steps:** S8 **operational witness:** **premise:** N>=2 **steps:** S5; S6 **one dimension:** **premise:** N=1 **steps:** S8 **excluded steps:** S5; S6

### Evidence limitations

- Original natural-language derivation only; no Lean execution, kernel replay, axiom audit or production-source change was performed.
- Author freeze is awaiting distinct answer-blind derivation and comparison. This author claims no independent review or approval.
- Source inspection grounds conventions and explicitly limited formal substrate, not the complete new mathematical target.
- Frozen graph identities represent declared source ownership and navigation, not extracted theorem-proof dependencies or new formal theorem closure.
- Global semantic deduplication, split assignment, release admission and measured model difficulty/performance remain unresolved.
- No paid model run, training, inference experiment, system installation, commit or push was performed by this worker.

Full source roles, review bindings and provisional difficulty: [complete packet](qa/P2.json).
