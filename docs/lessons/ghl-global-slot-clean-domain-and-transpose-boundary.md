# Retrospective local mathematical recovery — whole-module source freeze

This is a self-contained, implementation-informed mathematical recovery of a whole legacy module. It is not a pre-proof statement seal, a paper-fidelity finding, an independent review, a novelty claim, or a compiler certificate. The complete 8474-line target, including all proofs, private helpers, record fields, comments, and ambient commands, was read across two consecutive passes. The first WIP prefix and its historical scope remain unchanged; this is its separately stored whole-source successor.

## Evidence boundary

The accessible natural-language inputs are the bundled “Banded sparse access”, “Bulk indicator”, “Boundary rotations”, “One-term theorem”, “The clean gamma-three coefficient”, and composition/phase-audit sections of the source-excerpt file, and all sections of the short construction notes. These are locally edited excerpts/notes, not the full original paper. Their correction statements and references to later formal developments are retrospective commentary, not independently verified source text.

The intended external anchors recorded locally are arXiv:2506.20478, the Robin one-term construction and its figure/equation labels; its sparse-address citation is recorded as Lemma 2 invoking Lemma 1 of arXiv:2405.12855v3. Earlier local annotations use “Lemma 1” for the 2025 primitive. This packet preserves that distinction rather than reconciling unavailable original text by assertion. The original archive target ../outer_papers/quantum/GHL2025/main.tex is unavailable. No network or new-version source retrieval was done.

## M0. Mathematical carriers and what is merely syntax

A finite matrix of size r by c is an entry function on {0,...,r−1}×{0,...,c−1}. Multiplication is the finite ordered sum
\[
(AB)_{ij}=\sum_{k=0}^{m-1}A_{ik}B_{kj}.
\]
The implementation's coefficient carrier is a free expression syntax consisting of rational constants, named symbols, addition, multiplication, and negation. An environment assigns an arbitrary rational value to each symbol. Evaluation recursively interprets the expression. Syntactic equality is stronger than equality after evaluation; finite products retain zero summands in their syntax.

In particular, naming symbols for an inverse, a sine, a cosine, or a normalized coefficient imposes no algebraic or analytic relation. An arbitrary environment need not make an inverse symbol the reciprocal of a normalizer. There is no automatic real or complex Hilbert-space semantics, absolute square, square root, arccos, norm, or unitarity predicate on this syntax.

For a circuit list in temporal order g₁,...,gₖ, the matrix fold is gₖ⋯g₁. Alignment of gate labels with a supplied matrix list certifies label agreement, not the supplied matrices' physical meaning. A gate's “proved” field is a Boolean data field, not a proof term of unitarity.

The common path-isolation mechanism is finite-sum elimination: if every summand vanishes, the sum vanishes; if only k₀ survives, the sum is its k₀ term; if only distinct k₀,k₁ survive, it is their sum. One proves these by induction on a duplicate-free finite enumeration, splitting whether the head is a surviving index. Matrix-entry versions follow by evaluating the symbolic multiplication fold. These are ordinary finite arithmetic providers, not quantum oracle constructions.

## M1. Grid, formal resources, and two different wire counts

Write N=2ⁿ and let ceil-log₂(m) be zero at m=0 or 1, otherwise the smallest address width for m alternatives. Parameters n, κ, G, and a polynomial-degree cost are unrestricted natural data; the parameter record does not enforce κ>0, ceil-log₂κ≤n, a valid bulk window, or normalizer bounds.

Let ℓ=ceil-log₂κ, m_f=ceil-log₂n+ceil-log₂G+3, and w=n−ℓ, where subtraction is truncated natural subtraction. The visible registers, from the displayed high side to the low side, have widths
\[
m_f,\quad1,\quad\ell,\quad w,\quad n,\quad1.
\]
The low bit is the rotation ancilla; the next n bits encode the row; the next n-bit-address region is interpreted using a low padded slice and a high sparse-index slice when the widths are compatible. The indicator lies at bit 1+n+w+ℓ. Only with ℓ≤n does this simplify to 1+2n.

The theorem-facing stored signal count is
\[
m=\lceil\log_2 n\rceil+\lceil\log_2G\rceil+\ell+4.
\]
The concrete projection count is all non-system wires, namely m+w+1. Thus the matrix projection includes visible workspace beyond the theorem's signal parameter. The visible padded and final ancillas total w+1; this is not the claimed full 2n workspace budget. Counting wires cannot prove they return to zero.

The stored normalizer is the symbolic product N_D N_f κ and the stored approximation error is zero. Merely storing a target matrix, this product, an error value, a layout, a circuit, and a resource record proves no block identity.

The gate-cost expressions are stored arithmetic/symbolic formulas, including O((∑Q_g)n log n+κn) and 2n pure ancillas. A more detailed expression retains a boundary-factor K₁+N−K₂. For a valid inclusive bulk [K₁,K₂], the actual number of exterior rows is K₁+N−K₂−1. In the stored example N=8,K₁=2,K₂=5, the metadata expression is 5 whereas the exterior set is {0,1,6,7}. This packet does not silently redefine the stored expression as an exact cardinality. No finite-bit rotation synthesis, input evaluation, depth/connectivity, or compiled resource theorem follows from these data.

## M2. Bulk classification and circuit transcripts

The bulk predicate is K₁≤i≤K₂; the boundary predicate is i<K₁ or K₂<i. The latter ignores its nominal grid-size argument, so its total natural-number carrier includes out-of-grid values. A physical grid restriction must be stated separately.

There are two distinct recorded operation lists. The active finite backend list contains indicator, bulk-amplitude operation, boundary rotation, sparse address, coefficient-function operation, a swap label with placeholder wire indices, and transpose-style sparse-address operation. A longer theorem-facing transcript also records sparse-register preparation/unpreparation, an explicit indicator cleanup, and a transposed-derivative address label before the swap. Equality of these label lists is a transcript identity, not equality of their circuit actions. The longer list is not automatically the active product.

The generic extraction provider selects the diagonal signal block with compound indices a·r+i and a·c+j:
\[
B_{ij}=U_{a r+i,\;a c+j}.
\]
A separate source-level target asks that this block equal the target divided by its normalizer. Records of selected branch contributions and cached entries expose the needed equality, but do not supply it. A stored selected contribution equals itself by construction; projection/summation still needs an actual matrix-expansion proof.

## M3. The seven global sparse slots

For the concrete fourth-order family, the active global slot offsets are
\[
(o_0,\ldots,o_6)=(N-2,N-1,0,1,2,N-3,3)
\]
and the total function assigns zero offset to other slots. Define
\[
F_s(i)=(o_s+i)\bmod N.
\]
This is the actual retained global-slot address formula, including zero-amplitude slots. It is not a row-dependent list of nonzero columns.

The reverse-slot table is
\[
(\rho(0),\ldots,\rho(6))=(4,3,2,1,0,6,5),
\]
with default value 2 outside that set. On slots below 7 it is an involution and hence injective. It always lands below 8; on active slots it lands below 7. For n≥3, N≥8, and i<N,
\[
F_{\rho(s)}(F_s(i))=i
\]
holds even for encoded s=7, because both the default offset and the selected reverse slot's offset are zero. That eighth encoded value is not thereby an active κ=7 source slot.

The proof is finite-table arithmetic. Opposite offsets add to N, the zero pair adds to zero, and reduction modulo N cancels a multiple of N. Composition has the shared form
\[
F_t(F_s(i))=(((o_t+o_s)\bmod N)+i)\bmod N.
\]
If 0≤a<N and i<N and (a+i) mod N=i, then a=0: split a+i<N and N≤a+i<2N. If a<2N and a mod N=0, then a is either 0 or N, by the same split. Thus for active slots s,t<7 a return to i forces their offset sum to be 0 or N. Inspection of the seven offsets, distinct for N≥8, forces t=ρ(s). Applying a reverse shift to equal addresses then proves same-row slot injectivity.

These conclusions are exact address arithmetic under their stated domain restrictions. They do not construct the primitive gate sequence, prove full-space reversibility of a register overwrite, establish a transpose as a physical inverse, or clean workspace.

## M4. The row-dependent historical candidate is different

A separate total row-local column function uses columns i−2+s on bulk rows for s<5; on row 0 it uses s<3, on row 1 s<4, on row N−2 it uses N−4+s for s<4, and on row N−1 it uses N−3+s for s<3. Unused slots return i. This merges distinct sparse inputs. For N=8,row 0, slots 0 and 3 have the same row-local column. A Boolean classifier can label slot 3 unused, but deleting it from a claimed κ-wide source domain changes the domain.

A reverse-index candidate, given a target t and a new row r, returns t on rows 0 and 1, t+2−r on bulk rows, t−(N−4) on row N−2, and t−(N−3) on row N−1. With n≥3,s<8,i<N, applying the row-local forward map, then this reverse candidate, then the row-local map returns i; the candidate is below 8. The proof exhausts row regions and the eight sparse values, reducing each case to natural arithmetic and endpoint cases. Existence of this reverse-on-the-image witness does not imply injectivity of the original slot map. It does not rehabilitate the colliding model.

The active global formula and the old candidate remain separate objects. The source-domain classifiers for “clean padded input”, “active global slot”, and “row-local nonzero branch” also remain separate. Boolean partitions into valid and unused branches are classifier tautologies, not reversible extension constructions.

## M5. Register splicing and the precise safety claim

For a compound nonnegative basis index j, set
\[
L=2^{1+n},\qquad H=2^{1+2n},\qquad
l=j\bmod L,\qquad h=\lfloor j/H\rfloor.
\]
Extract the row as floor(j/2) mod N and the old address as floor(j/L) mod N. The padded and sparse parts of the latter are its low w bits and next ℓ bits.

Writing a computed address a into the address region is the literal splice
\[
I(j)=l+aL+hH.
\]
When a<N, l+aL<H since 0≤l<L and a+1≤N. It follows that I(j) mod L=l, floor(I(j)/L) mod N=a, and floor(I(j)/H)=h. Consequently the low ancilla-and-row region and every high bit above the address register are preserved. If j<2ᵀ and 1+2n≤T, then h<2^{T-(1+2n)} and the same inequality gives I(j)<2ᵀ.

The bit-slice bridge is
\[
((x\gg b)\mathbin{\&}(2^q-1))=\lfloor x/2^b\rfloor\bmod2^q.
\]
It follows bit by bit from masking and shifting. This converts physical-looking slice notation into ordinary division/remainder arithmetic.

For the active global address, a<N follows from modular reduction for every n,s,i; some wrapper signatures retain an unused assumption n≥2. That retained assumption is a local interface artifact, not a newly discovered paper premise. More restrictive injectivity facts elsewhere still require n≥3 and active slots below 7.

The forward candidate matrix has entries 1 exactly at row I(j) of column j, and zero elsewhere. Its transpose-style companion has entries 1 exactly when j=I(i). A finite image witness gives paired forward and transposed entries equal to 1. This does not prove bijectivity on all finite columns. Discarding nonzero padded bits can merge inputs; restricting attention to a clean locus does not itself choose a full-space unitary extension.

## M6. Coefficient tables and incompatible slot interpretations

Let a and b stand for the independent formal symbols for the left and right Robin boundary products. On bulk rows the five nonzero values in slots 0,...,4 are
\[
(-1/12,\;4/3,\;-5/2,\;4/3,\;-1/12).
\]
The active global-slot table has:

| Row | Nonzero slot:value entries |
| --- | --- |
| 0 | 2:−5/2+(7/3)a; 3:8/3; 4:−1/6 |
| 1 | 1:4/3−a/6; 2:−31/12; 3:4/3; 4:−1/12 |
| N−2 | 0:−1/12; 1:4/3; 2:−31/12; 3:4/3+b/6 |
| N−1 | 0:−1/6; 1:8/3; 2:−5/2−(7/3)b |

All remaining slots carry zero. The row tests prioritize the bulk branch and then the boundaries; for small n overlapping/truncated regions must be interpreted by that actual priority, not by assuming the large-grid stencil picture.

The old row-local coefficient table starts row 0's values in slot 0 and row 1's in slot 0. Hence global slot 2 on row 0 is the diagonal value, not the old third row-local entry. A guard showing these expressions differ is an exact syntax-level regression. It does not establish consistency with unavailable original PDE derivations, ghost-point elimination, physical grid scaling, or a compiled derivative matrix.

## M7. Indicator and controlled-rotation skeletons

The indicator sends j to j XOR (bulk(row(j)) shifted to the indicator bit). Its whole-file image, finite-range, and permutation arguments are reconstructed in M10 below. This is stronger than the gate record's true Boolean, but still separate from an analytic complex-matrix unitarity certificate or elementary-gate synthesis.

The active bulk-amplitude and boundary-amplitude candidates preserve every non-ancilla bit. Each applies, on its enabled indicator sector, a symbolic two-by-two block
\[
R(c,s)=\begin{pmatrix}c&-s\\s&c\end{pmatrix}
\]
on bit 0, and identity on the disabled sector. The bulk operation is enabled at indicator 1; the boundary operation at indicator 0. The row and sparse slot label the symbols c,s. This establishes a literal algebraic matrix formula, not trigonometric semantics or unitarity. An older diagonal-data helper scales bulk diagonal entries by row-local derivative values; it is not the active two-by-two rotation.

For the bulk intended amplitude, the contract asks c=D/N_D and s=sqrt(1−|D|²/N_D²). The shared symbolic stand-in for division is D times an independent named inverse. The outstanding links are N_D≠0, genuine division, |D|≤N_D, absolute-square interpretation, a real square-root complement, and the two-by-two unitary identity.

The boundary contract in the read implementation still records θ=arccos(D/N_D), c=sqrt((1+D/N_D)/2), and s=sqrt((1−D/N_D)/2). The bundled edited excerpt instead describes a doubled angle under the standard rotation convention. Those are distinct targets: with the displayed half-angle matrix, the single-angle formula does not directly make the zero-ancilla amplitude D/N_D. This is a retained local mismatch boundary, not a certified correction or an instruction to alter the legacy target.

Both routes share the same global coefficient table and normalizer-data record. Equalities of record fields only synchronize which unresolved analytic contract they reference; they do not discharge it.

## M8. Stored process decisions are not mathematical premises

Many objects in the read prefix are descriptions, citation strings, optional proposed images, process-permission Booleans, and default false obligation fields. Theorems that these defaults are false or that optional fields are absent are facts about records. They do not show an external theorem does not exist, prove a mathematical impossibility, establish paper correctness, or supply a missing oracle.

A clean-domain extension interface leaves the unused-branch image unspecified. A nested source-decision record says proof search is disabled. A prior-paper transcript names a first-row index unitary followed by modular addition and records a resource claim, but supplies no proof of those gates here. All of this remains data and unresolved dependency context. No decoder, reviewer, or previous acceptance record was used as mathematical evidence.

## M9. The coefficient-function clean branch and its unresolved completion

Assign each grid label i a distinct formal function symbol fᵢ. The intended normalized value is fᵢ times a named inverse symbol for N_f; no actual function evaluation, inverse law, or bound follows from the naming.

The function workspace occupies m_f bits starting immediately above the indicator. For a compound index j, extract that workspace value and clear those bits to obtain z(j). Record the row value separately. On a clean-workspace input column j, the literal matrix skeleton prescribes
\[
U_{i,j}=
\begin{cases}
f_{\operatorname{row}(j)}\,\nu_f,&i=z(j),\\
0,&i\ne z(j)\text{ and the output workspace is clean},\\
q_{i,j,\operatorname{row}(j)},&\text{otherwise},
\end{cases}
\]
where \(\nu_f\) and every \(q\) are free symbols. On a nonclean input column every entry is a completion symbol. Thus the clean branch is genuinely wired into the matrix formula, and off-branch clean-workspace entries really are zero. The unresolved rows are not merely an “orthogonal remainder” vector that has already been constructed: their entries are independent placeholders. In particular, the formula does not enforce preservation of the system label in those completion rows, normalizer bounds, column normalization, orthogonality, or full-space unitarity.

A separate diagonal helper stores raw fᵢ on its diagonal; it is not the active clean-branch matrix. The dependency transcript names the piecewise-polynomial amplitude-oracle theorem and coordinate-oracle equation in arXiv:2506.20478, with a citation to arXiv:2411.01131 Theorem 5. Those external theorem contents were not independently available. Their descriptions, claimed O((∑Q_g)n log n) cost and n−1 pure ancillas remain unresolved source/dependency data, not a construction in this module.

## M10. Exact register exchange and indicator basis permutations

Let b₁(j) and b₂(j) be the two n-bit slices beginning at positions 1 and 1+n. Set d=b₁ XOR b₂ and
\[
W(j)=j\operatorname{XOR}(d\ll1)\operatorname{XOR}(d\ll(1+n)).
\]
The difference d is below 2ⁿ. At each bit in the first slice, XOR with d changes b₁ to b₂; at each bit in the second it changes b₂ to b₁. Other bits are untouched. Consequently the new difference is b₂ XOR b₁=d. Applying the same two shifted masks twice cancels, so W(W(j))=j.

The finite-range argument is separate: an x<2ʷ shifted by b positions is below 2ᵀ when w+b≤T, because x·2ᵇ<2ʷ·2ᵇ≤2ᵀ. Both shifted masks fit in the total basis width, and XOR of values below 2ᵀ remains below 2ᵀ. Thus W restricts to a finite basis involution. Injectivity follows by applying W again; the preimage of y is W(y), so it is surjective.

For the indicator, its bit position q obeys q≥1+n and q<T for every parameter record, even when the informal simplification q=1+2n is inapplicable. A value shifted above position 1+n has no effect on the n-bit row slice. Therefore the bulk predicate is unchanged by the indicator map J. Its controlled toggle mask is the same on the second application, so J(J(j))=j. The toggle is either zero or one in-range bit, establishing finite-range preservation, then finite injectivity and surjectivity by the same involution argument. The fixed n=1 and n=3 cases are finite specializations, not the basis of this arbitrary-width argument.

For either map F, the literal zero/one matrix is \(P_{ij}=1\) iff \(i=F(j)\). Each column has its unique 1 at F(j); surjectivity gives a 1 in every row and injectivity makes that 1 unique. These are exact finite permutation-matrix statements. The module does not additionally instantiate an analytic unitary predicate, nor does the placeholder swap label on wire indices (0,0) constitute a physical decomposition of the n-register swap. No Clifford+T, connectivity, or finite-bit synthesis cost is deduced.

## M11. General address splices and reconstruction of clean indices

For any proposed n-bit address v, extend M5's splice to
\[
S(j,v)=(j\bmod L)+vL+\lfloor j/H\rfloor H.
\]
The same no-carry argument proves preservation of the low region and high tail and exact extraction of v. It also proves
\[
S(S(j,v),u)=S(j,u)\quad(v<N).
\]
No bound on u is needed for that algebraic overwrite identity. The original index reconstructs exactly:
\[
S(j,\operatorname{address}(j))=j.
\]
This is the two-level quotient/remainder decomposition of j, not a choice of a representative or a quotient type.

A clean encoded sparse value for a slot s is c(s)=s·2ʷ. Its padded low w bits vanish. If ℓ≤n and s<2^ℓ, then c(s)<2ⁿ; extracting its sparse slice recovers s. Conversely, under width compatibility and padded cleanliness, the old address register value equals c(extracted sparse slot): zero remainder modulo 2ʷ removes the low term in the quotient/remainder decomposition, and the n-bit range removes an additional sparse-slice wrap.

These facts let local address injectivity become full compound-index injectivity on the active domain. Assume n≥3, κ=7, ℓ=3, and both inputs are padded-clean with sparse slots <7. Equal images imply equal low prefixes and high tails, equal extracted rows, and equal written global addresses. M3 forces equal sparse slots. Clean reconstruction then forces equal original address regions, so the complete indices agree. This is injectivity on a stated subset, not on every padded-clean value or every full-space column.

The interfaces retain the explicit width equality ℓ=3 even though it follows from κ=7 and the local ceiling-log definition; this recovery does not silently remove that binder or treat it as an external source hypothesis.

## M12. Explicit post-exchange clean preimage and its precise uniqueness scope

Let a=F_s(r) for an active input with row r and slot s. After its address image and register exchange, the new row is a and the address block contains r. Define C(j) by keeping this post-exchange low region and high tail and splicing the clean encoded reverse slot c(ρ(s)) into the address block.

The reverse slot is below 8 and fits the three-bit sparse register. For n≥3 it fits the n-bit address region. Splice safety keeps C(j) finite whenever j is finite. It is padded-clean by construction, and its extracted sparse slot is ρ(s). The row is still a, so its recomputed address is
\[
F_{\rho(s)}(a)=F_{\rho(s)}(F_s(r))=r.
\]
Applying the forward image to C(j) therefore replaces its address block with the post-exchange address r while preserving all other regions, yielding the post-exchange index exactly. This is the mechanism behind the candidate-check Boolean, not merely an unexplained finite check.

Some intermediate interfaces ask only for a clean encoded source and allow the eighth encoded slot, whereas the final active domain also requires s<7. The former range/image consequences do not establish active-domain membership or uniqueness. On the active domain, ρ(s)<7, so C(j) is itself active. Any other active clean preimage of the same post-exchange index equals C(j) by M11's active-domain image injectivity.

The proof-carrying cleanup record expands to the following facts: the post index equals the register-exchanged image; the selected preimage maps to that post index; the preimage is padded-clean; its address is n-bit; the transpose-style matrix entry is 1; row/address/no-spill checks hold; and the post row/address agree with the corresponding preimage row/recomputed address. An early constructor accepts the post equality, image equality, clean condition, and range condition as premises. Later constructors actually supply them from the explicit candidate under the active family assumptions. These are dependencies of the stronger local theorem, not newly postulated premises of a final block-encoding claim.

Let D denote the padded-clean, slot<7 finite input subset and let \(M^\mathsf{T}_{u,v}=1\) iff \(v=I(u)\). For an active source j and its post-exchange index t, the recovered matrix-entry statement is
\[
\forall u\in D,\qquad
M^\mathsf{T}_{u,t}=
\begin{cases}
1,&u=C(j),\\
0,&u\ne C(j).
\end{cases}
\]
The candidate entry is 1 because its image is t; another active row cannot have entry 1 by uniqueness. This is a real restricted-column result, including sparse slots whose coefficient happens to vanish. It is not merely the statement that some entry is nonzero.

The quantifier \(u\in D\) is indispensable. No claim about every row outside D is proved by this restricted theorem. It therefore does not show that the full transpose sends the entire post-exchange basis vector to a single clean basis vector, that all ancillas are clean, or that the transpose is the inverse of a full unitary. The selected preimage retains a reverse sparse slot and the new row; it is not the all-zero signal/workspace vector required by a completed block projection.

A concrete old boundary-collision source belongs to D although the old row-dependent nonzero classifier rejects it. The recorded local witness uses the active global-domain proof, demonstrating why that rejected classifier must not silently replace D.

## M13. Whole-module closure boundary and source topology

The complete local mechanism chain is:
finite expression/matrix carriers → literal register slices and global slots → modular inverse-slot arithmetic → bounded splice and clean reconstruction → active-domain image injectivity → explicit post-exchange preimage → active-domain uniqueness → restricted transpose-column formula.
Independently, bit-mask cancellation supplies the indicator and register-exchange finite permutations. The unresolved amplitude and coefficient-function routes do not become consequences of either permutation route.

The single-term normalization, zero error, resource tuple, intermediate gamma components, and one-/multi-dimensional Hamiltonian formulas are stored descriptions/records here. The gamma records store ranges, prefactors, and an “orthogonal remainder” Boolean, not full state vectors with a proved transition. The module neither composes the seven matrices into the advertised normalized Robin operator nor proves the full block-extraction equation. It also does not construct the one-dimensional or multidimensional Hamiltonian composition advertised by metadata.

The edited excerpt's gamma-three display, one-term theorem and resource description supply intended targets only. Its final Hamiltonian-composition and phase-audit comments concern a different composition module and are excluded from the present module's mathematical closure claim. The short pipeline notes likewise provide context rather than supplied oracle, Hamiltonian-simulation, or gate-synthesis proofs.

No unavailable proof paragraph, figure transformation, citation theorem, or source correction has been invented. The original-paper proof graph remains unavailable beyond the exact locally bundled excerpts. This whole-module recovery instead freezes the complete retrospective local mathematical graph and its boundaries. A later independent source comparison may examine fidelity; no such comparison, compilation, novelty conclusion, or main admission is asserted here.

## M14. Canonical bulk guard clarification — source-bound successor v2

This supplement clarifies the historical row-dependent candidate in M4. It does not rewrite the original frozen source or any implementation. In that section, “bulk” means exactly the canonical n-only predicate 2 ≤ r ≤ N−3, where N=2^n and subtraction is natural-number subtraction. It is not the arbitrary-parameter interval [K₁,K₂] used by the generic classifier discussion in M1/M2.

The forward candidate tests the canonical bulk predicate first, then row 0, then row 1, then row N−2, then row N−1, then its fallback. Within those regions its slot bounds are respectively 5,3,4,4,3; an unused slot returns the input row.

The reverse candidate tests row 0 first, row 1 second, then the canonical bulk predicate, then row N−2, then row N−1, then its fallback. Its outputs in that order are target, target, target+2−row, target−(N−4), target−(N−3), and target. This actual precedence matters on the total natural-number carrier, especially at small grids.

The recovered forward/reverse roundtrip is only the stated canonical-family result for n≥3, sparse index s<8, and input row i<N. No arbitrary K₁,K₂ version is claimed. These are the existing local formula and theorem guards, not added paper assumptions or a repaired Lean target.

Provenance: after the original source-only freeze, the parent supplied one explicitly authorized limited independent-phase clarification request concerning the meaning of bulk. The author received that specific feedback but read no reviewer/decoder file or other independent result. The two implementation definitions and the roundtrip header were directly rechecked before writing this supplement. The original source SHA-256 remains c774ecaf66c3d3c9586c41f7441b416ee77bfd54a3314e1d9ee66ff7151db6f5; the prospective lesson appends this visibly versioned supplement rather than pretending it was present initially.
