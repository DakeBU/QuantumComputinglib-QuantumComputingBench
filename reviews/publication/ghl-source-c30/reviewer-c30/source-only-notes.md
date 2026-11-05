# Independent whole-source phase 1 notes — reviewer c30

Status: PHASE1_SOURCE_ONLY_SEALED_PENDING_FORMAL_COMPARISON. This is an independent reading of a retrospective local mathematical exposition, not a production proof, historical pre-proof seal, original-paper fidelity verdict, or implementation acceptance. Historical formalizer identity is UNKNOWN. The reviewer has not examined the implementation or any other person's graph, coverage, decoder, review, or gate output.

## 1. Frozen input and actual reading

The sole mathematical input is `$AUTHOR/final/source-only.md`, SHA256 `c774ecaf66c3d3c9586c41f7441b416ee77bfd54a3314e1d9ee66ff7151db6f5`, 27188 bytes, 253 lines. It was read completely once as raw text and again with all lines numbered, 1–253 inclusive, without output truncation. The expected digest matched the actual digest. Line references below are to these exact mathematical bytes. Path aliases are reviewer-added redaction, not modifications or alternative hashes of the mathematical input.

The seven mandated process inputs were completely read before the mathematical source: `$PROJECT/AGENTS.md` (284 lines); `$PROJECT/HARNESS.md` (492); `$PROJECT/.agents/skills/qbe-substantive-worker/SKILL.md` (87); `$PROJECT/.agents/skills/qbe-source-dependency-audit/SKILL.md` (94); `$PROJECT/docs/theorem-publication-protocol.md` (303); `$PROJECT/docs/proof-digestion-protocol.md` (317); `$PROJECT/docs/evidence-routed-memory-protocol.md` (190). Full input digests are in `phase1-seal.json`. No linked repository records were followed. Their ordinary implementation/build/search instructions are superseded for this role by the expressly source-only phase boundary.

Provenance claims in the exposition, including the claimed reading of an 8474-line historical module, are statements made by the source author, not observations independently verified here. In particular, reviewing all 253 lines is not reviewing those 8474 implementation lines. The citations in lines 9 and 176 have only the descriptive content provided here; the cited papers, local excerpts, and short notes were not opened.

## 2. Independent mathematical reconstruction

### 2.1 Algebraic substrate, not a quantum model

The coefficient algebra is a free rational expression grammar. An environment sends symbols to arbitrary rationals and recursively interprets addition, multiplication, and negation. Equal expressions have equal evaluation, but the converse fails: `x+0` and `x` have equal evaluation in every environment without being the same syntax tree. A name such as inverse-N or sine is just another free generator. No reciprocal, trigonometric, positivity, conjugation, or Hilbert-space law follows from its spelling.

Finite matrices are entry functions; evaluated multiplication is a finite sum. The zero-, one-, and two-survivor path arguments are finite-sum identities, with distinct surviving indices needed in the two-survivor case. This is sufficient for elementary matrix-entry manipulations once the actual zero conditions are proved. It is not a substitute for proving those zero conditions for the entire circuit. Temporal composition `g1,...,gk` means the column-vector matrix product `gk ... g1`.

### 2.2 Registers and compatible widths

Let `N=2^n`, `ell=ceilLog2(kappa)`, `w=n-ell` using truncated natural subtraction, and `mf=ceilLog2(n)+ceilLog2(G)+3`. The literal total width derived from the six displayed registers is

`T = mf + 1 + ell + w + n + 1`.

The row is at bits `[1,1+n)`, rotation ancilla at bit 0, and the next fixed n-bit region starts at `1+n`. The intended split of this region into w padded bits and ell sparse bits requires `ell<=n`. Without that condition `w+ell` exceeds n, so the displayed sparse/padded region is not the same n-bit region used by the fixed splice formula. This does not invalidate the literal total-width or indicator definition: `q=1+n+w+ell` remains at least `1+n` and below T. It does prevent silently using the compatible-width picture for arbitrary parameter records.

The stored signal count is `m=mf+ell+1`; actual non-system projection width is `mf+ell+w+2=m+w+1`. These counts differ even on valid parameters. Neither says all workspace is zero. The recorded `2n` pure-ancilla budget is not obtained simply by counting the visible padded and rotation wires. No normalization/block equation follows from stored normalizer `ND*Nf*kappa`, stored zero error, or a stored resource tuple.

### 2.3 Global addresses and inverse slots

For n>=3 the seven offsets are distinct residues in `[0,N)`: `(N-2,N-1,0,1,2,N-3,3)`. Define `Fs(r)=(os+r) mod N`. The active reverse pairing is `(0,4),(1,3),(2,2),(5,6)`. Paired sums are N except the zero pair, whose sum is zero. Thus `F_rho(s)(Fs(r))=r` when r<N. For default slot 7 this identity also holds because its offset and slot 2's offset are zero, but active-slot membership does not follow.

Composition is addition of residues. If `Ft(Fs(r))=r`, cancellation modulo N implies `(ot+os) mod N=0`. Each offset is below N, so their sum is below 2N and is 0 or N. Distinctness of the listed offsets gives `t=rho(s)` for active s,t. Alternatively, equality `Fs(r)=Ft(r)` cancels the common row residue; distinct offsets give s=t. This latter direct proof and the source's reverse-shift proof are ordinary mathematical alternatives for the same address-injectivity subclaim, not separately certified block-encoding constructions.

### 2.4 Historical row-local map

The row-local map discards unused sparse slots by sending them to the row. At N=8,row 0, slots 0 and 3 both map to column 0. A reverse-on-image witness can coexist with this collision: surjectivity onto an image or existence of a selected preimage is not injectivity of the original map. Rejecting slot 3 with a nonzero classifier changes a seven-slot domain and does not repair the map on that domain.

There is a source specification issue in the general reverse-on-image claim (line 91): the canonical row partition is not explicitly fixed in that paragraph. Under the customary stencil bulk `2<=i<=N-3`, its formulas can be checked by row and slot cases. Under arbitrary `K1,K2` from M1/M2 with bulk tested first, the claim is false. For N=8, all rows declared bulk, i=0,s=4: forward gives r=4; the proposed reverse on bulk r gives `0+2-4=0`; the second forward gives `4-2+0=2`, not i=0. This is a discriminator for the omitted convention, not an assertion about the unread implementation's actual bulk test. Phase 2 must supply the exact old row predicate and branch precedence before comparing this statement. I mark that condition as an unresolved local source specification, not a new external paper premise.

### 2.5 Splice safety and clean injectivity

Set `L=2^(1+n)` and `H=2^(1+2n)=L*N`. Every j decomposes uniquely as `l+b*L+h*H`, where `l=j mod L`, `b=(j div L) mod N`, and `h=j div H`. For a<N, replacing b by a gives `l+a*L < H`; hence no carry enters h, the low prefix is unchanged, and address extraction returns a. If j<2^T and `1+2n<=T`, the same h bound keeps the result below 2^T. The bit-mask identity in line 112 justifies interpreting the slices as quotient/remainder arithmetic, including q=0.

For `S(j,v)=l+v*L+h*H`, `S(S(j,v),u)=S(j,u)` requires v<N to preserve the first splice's high tail; u need not be bounded for this equality alone. To claim the final address is u or to claim finite-range safety, u<N is required. Replacing b by b reconstructs j exactly.

For compatible widths and `s<2^ell`, `c(s)=s*2^w` is below N, has zero padded bits, and decodes to s. Conversely every padded-clean address below N is exactly the clean encoding of its sparse slice. This is an ordinary natural-number representation theorem, not a quotient-representative choice.

Let D consist of finite basis indices that are padded-clean and have sparse slot <7, with n>=3,kappa=7,ell=3. Equal forward splice images give equal low prefixes and high tails. Low-prefix equality gives the same row; equality of the written addresses then gives the same active sparse slot. Clean reconstruction recovers equal original address blocks, and all parts of the original indices agree. This proves injectivity of the restricted map on D only.

### 2.6 Register exchange and indicator

The exchange map uses two disjoint n-bit slices and the XOR of their values. XORing that difference into both slices exchanges them, does not change any other bit, and leaves the same difference for the second application. Hence W is involutive on all nonnegative indices. For finite indices, both shifted masks must fit under 2^T; `T>=1+2n` follows from the displayed layout since `w+ell>=n` and mf>=3. Range preservation plus involution gives a finite bijection.

For the indicator, q lies outside the row slice. Toggling bit q therefore leaves the row and its bulk predicate unchanged; the second toggle cancels the first. Since q<T, range preservation holds. These two arguments are independent; neither needs the address map to be injective. A finite permutation matrix has exactly one 1 in every row and column. Over a later honest real/complex embedding it would be unitary, but neither that scalar embedding nor an analytic-unitary instance is among this phase's observations. A swap gate label `(0,0)` is not an elementary-gate realization of W.

### 2.7 Post-exchange preimage and restricted transpose column

Take j in D with row r, slot s, and a=Fs(r). The forward splice changes the address to a and leaves row r. After W, t has row a and address r, with low ancilla and higher tail unchanged. Define `C(j)=S(t,c(rho(s)))`. Since rho(s)<7<8 and ell=3,n>=3, this address fits, is clean, and decodes to rho(s). Its row is a. Applying I gives address `F_rho(s)(a)=r` and preserves every other region, so `I(C(j))=t`. C(j) belongs to D. Restricted injectivity makes it the only D-preimage of t.

The transpose-style matrix is defined entrywise by `Mtrans[u,v]=1 iff v=I(u)`, zero otherwise. Therefore for every u in D, its t-column is the Kronecker delta at C(j). This is a meaningful entire-column statement on the restricted row set, including all active zero-coefficient slots. It is stronger than exhibiting one nonzero entry, but weaker than a full-space one-hot column or inverse-unitary theorem.

The expansion of the cleanup record is explained by this chain: t=W(I(j)); candidate image=t; candidate clean; address bound; transpose entry 1; no-spill and preserved row/address facts. These are consequences needed to construct the record, not independent public assumptions on a completed block encoding. C(j) retains a sparse label rho(s) and the new row a. It is not generally a zeroed sparse/signal workspace.

### 2.8 Coefficients, amplitude sectors, and f-oracle skeleton

The global coefficient table at lines 122–135 is literal data with two independent boundary symbols a,b. The old row-local ordering is a different table, so moving a coefficient by old slot position changes the target. Actual numerical support can shrink when boundary parameters cancel an expression; the global slot domain does not shrink with it. Small-grid overlap is resolved only by the actual bulk-first branch priority, not by drawing a nonoverlapping stencil.

The two active 2x2 amplitude matrices preserve every bit except bit 0 and act on complementary indicator sectors. Over real scalars `R(c,s)^T R(c,s)=(c^2+s^2)I`. Thus unitarity needs the relation `c^2+s^2=1`; free symbols alone do not provide it. To get the desired bulk accepted amplitude one needs genuine division by a nonzero ND, a suitable real coefficient and bound, and a complementary square root. For complex D the displayed real matrix would need an explicitly different conjugation-aware convention; none can be assumed silently.

The boundary formulas preserve an explicit mismatch. Writing x=D/ND, the displayed accepted amplitude is `sqrt((1+x)/2)`, not x. At x=0 it is `1/sqrt(2)` rather than zero; at x=-1 it is zero rather than -1. A doubled-angle convention can describe another target but is not an automatically approved repair of the stored half-angle formula. No source-only approval of either repair is issued.

The f-oracle is a partial matrix skeleton on clean input columns. A clean input j already has `z(j)=j`; its only allowed clean-output entry is `f_row(j)*nu_f` at j, and the other clean-output entries are zero. Dirty output entries and nonclean input columns are free symbols. This does not construct an orthogonal remainder, preserve the row label in garbage, or enforce norm/orthogonality. A diagonal raw-f helper is not this operator. The quoted external amplitude-oracle theorem and coordinate-oracle equation have not supplied their statements, access models, or proofs here.

### 2.9 Endpoint, not inferred closure

My independently reconstructed algebraic endpoint is the restricted t-column identity, with separate finite-basis permutation results for W and J. Full-space address unitarity, analytic amplitude oracles, coherent f evaluation, PREPARE/unprepare, indicator cleanup after the row exchange, matrix-product expansion, final zero-signal block equality, and actual costs are separate obligations. No implication from restricted column uniqueness or stored gamma metadata to the final block identity has been found in the source. The cited gamma-three display and Hamiltonian statements are only described, not given as reconstructible formulas in this input.

## 3. Exhaustive substantive-region disposition

Each SF item is my source graph node, not a declaration name or an imported author node. Ranges include displayed equations/tables and their explanatory prose. All mathematical definitions, arguments, boundary statements, and citation paragraphs have dispositions. Blank lines and section headings are EXCLUDED(format/navigation only); they carry no additional assertion.

| Lines | Disposition | Independent identity / content |
| --- | --- | --- |
| 1–3 | EXCLUDED(process provenance, not mathematical evidence) | Retrospective status and unverified historical reading claim |
| 5 | EXCLUDED(heading) | Evidence-boundary label |
| 7–9 | NODE SF00 | Locally bundled provenance; unavailable original sources and competing lemma labels |
| 11 | EXCLUDED(heading) | M0 label |
| 13–17 | NODE SF01 | Entry matrices, finite multiplication, free expression grammar and evaluation |
| 19 | NODE SF02 | No automatic inverse/analytic semantics |
| 21 | NODE SF03 | Temporal matrix order; label/Boolean limits |
| 23 | NODE SF04 | Zero/one/two-survivor finite-sum proofs |
| 25 | EXCLUDED(heading) | M1 label |
| 27–33 | NODE SF05 | Parameters, truncated widths, physical slice convention and compatibility |
| 35–39 | NODE SF06 | Signal versus projection width; no cleanup from counts |
| 41 | NODE SF07 | Stored normalizer/error are data, not a block equality |
| 43 | NODE SF08 | Stored resource tier; boundary count discrepancy and finite-bit omissions |
| 45 | EXCLUDED(heading) | M2 label |
| 47 | NODE SF09 | Bulk/boundary predicates and separate finite-grid restriction |
| 49 | NODE SF10 | Two different transcripts; absent active PREPARE/cleanup bridges |
| 51–55 | NODE SF11 | Selected block formula and unresolved target equality |
| 57 | EXCLUDED(heading) | M3 label |
| 59–67 | NODE SF12 | Seven global offsets and total address map |
| 69–77 | NODE SF13 | Reverse table, active involution, default-slot distinction |
| 79–83 | NODE SF14 | Modular composition, return-pair uniqueness, slot injectivity |
| 85 | NODE SF15 | Address arithmetic/full-unitary separation |
| 87 | EXCLUDED(heading) | M4 label |
| 89 | NODE SF16 | Historical row-local map and explicit collision |
| 91 | NODE SF17 | Reverse-image claim; row-partition specification gap retained |
| 93 | NODE SF18 | Distinct classifiers; partitions are not reversible extensions |
| 95 | EXCLUDED(heading) | M5 label |
| 97–108 | NODE SF19 | Literal splice, no-carry slices, finite-range bound |
| 110–114 | NODE SF20 | Bit-slice/quotient-remainder bridge |
| 116 | NODE SF21 | Modular range proof; retained wrapper n>=2 not necessary here |
| 118 | NODE SF22 | Forward/transpose entry definitions, witness, and global collision risk |
| 120 | EXCLUDED(heading) | M6 label |
| 122–135 | NODE SF23 | Bulk and all four boundary coefficient tables, zero slots, priority |
| 137 | NODE SF24 | Old/global coefficient mismatch and PDE-fidelity boundary |
| 139 | EXCLUDED(heading) | M7 label |
| 141 | NODE SF25 | Indicator map and separation from analytic/gate certificates |
| 143–147 | NODE SF26 | Controlled R matrix, complementary enables, inactive diagonal helper |
| 149 | NODE SF27 | Bulk intended amplitude and missing analytic laws |
| 151 | NODE SF28 | Boundary half-angle mismatch, not an approved correction |
| 153 | NODE SF29 | Shared record fields do not supply analytic laws |
| 155 | EXCLUDED(heading) | M8 label |
| 157 | NODE SF30 | Process/obligation records and logical non-implications |
| 159 | NODE SF31 | Unspecified clean extension, prior-paper gate/resource transcript |
| 161 | EXCLUDED(heading) | M9 label |
| 163 | NODE SF32 | Formal f labels and free inverse |
| 165–174 | NODE SF33 | Clean-input coefficient-function matrix and unconstrained completion |
| 176 | NODE SF34 | Raw diagonal distinction; unavailable amplitude/coordinate citations and costs |
| 178 | EXCLUDED(heading) | M10 label |
| 180–184 | NODE SF35 | XOR exchange, bit semantics, involution |
| 186 | NODE SF36 | Shift/XOR finite-range proof and finite bijection |
| 188 | NODE SF37 | Indicator row invariance, range, involution and bijection |
| 190 | NODE SF38 | Permutation matrix entries; physical implementation boundary |
| 192 | EXCLUDED(heading) | M11 label |
| 194–206 | NODE SF39 | General splice, overwrite and exact reconstruction |
| 208 | NODE SF40 | Clean encoding and converse reconstruction |
| 210–212 | NODE SF41 | Active compound-index injectivity; explicit redundant width equality |
| 214 | EXCLUDED(heading) | M12 label |
| 216–222 | NODE SF42 | Explicit C, range, cleanliness, reverse-address image equality |
| 224 | NODE SF43 | Active candidate membership and unique D-preimage |
| 226 | NODE SF44 | Expanded cleanup record; premises versus later providers |
| 228–237 | NODE SF45 | Restricted transpose-column delta identity, including zero coefficients |
| 239 | NODE SF46 | Outside-D, full inverse, all-zero signal non-implications |
| 241 | NODE SF47 | Old-classifier counterexample retained on the global active domain |
| 243 | EXCLUDED(heading) | M13 label |
| 245–247 | NODE SF48 | Local-chain summary and independent permutation branch; audited above |
| 249 | NODE SF49 | Gamma/operator/resource metadata and explicit missing closure |
| 251 | NODE SF50 + EXCLUDED(Hamiltonian closure outside local claim) | Intended gamma/one-term targets remain nodes; other-module composition/phase comments and pipeline applications supply no local proof |
| 253 | NODE SF51 | Unknown original-paper topology; absence of fidelity/compile/admission inference |

Line 251 is not discarded wholesale: its intended gamma/one-term targets and scope restriction are SF50; only the asserted other-module Hamiltonian/application proofs are excluded from this module's mathematical closure. Process claims SF30/SF31 are retained to audit mistaken promotion, not counted as quantum theorems. No mathematical paragraph was excluded merely because it is difficult or unproved.

## 4. Independently reconstructed dependency hypergraph

Notation `{A,B,...} -> H` is a complete AND tail for the stated local inference. Conditions after `;` are part of the tail, not optional labels. Definitions with no incoming edge are literal input nodes. These are mathematical source dependencies, not claims about elaborated implementation dependencies.

1. `{SF01, finite duplicate-free enumeration, the stipulated vanishing conditions, distinct survivors when two} -> SF04`. The three survivor counts are case-specific lemmas; no count alone proves a circuit action.
2. `{SF05} -> SF06` by summing widths and the stored m expression. `{SF09, 0<=K1<=K2<N} -> actual exterior cardinality in SF08`. Stored complexity is not an output of either edge.
3. `{SF12, SF13, n>=3, r<N} -> reverse address identity in SF13`. `{SF12, modular addition/cancellation, n>=3, s,t<7, r<N} -> SF14` including unique return pair and same-row injectivity. No coefficient or nonzero-amplitude test belongs to this tail.
4. `{SF16, N=8, row=0, slots=0 and 3, intended boundary branch} -> collision`. `{SF16, exact canonical row partition, SF17 reverse definition, n>=3, i<N, s<8, endpoint case arithmetic} -> SF17 reverse-on-image`; the row-partition input is GAP-01 until specified. This does not point to global injectivity.
5. `{SF05, SF19 literal formula, a<N, H=L*N} -> low/address/high no-carry identities`. Add `{j<2^T, 1+2n<=T}` for the finite-range conclusion. `{SF20, slice offsets/widths} -> agreement of physical slice notation and the arithmetic extraction`.
6. `{SF12, N=2^n>0} -> SF21 address range`. `{SF19, SF21} -> bounded forward image`. `{SF22 entry definitions, finite image witness} -> paired entry=1`. This last edge has no implication to a one-hot full transpose column.
7. `{SF19 quotient-remainder analysis, v<N} -> SF39 overwrite`. `{SF19 quotient-remainder decomposition} -> SF39 original-index reconstruction`. `{SF05, ell<=n, s<2^ell} -> SF40 clean encoding`. `{SF05, ell<=n, padded cleanliness, n-bit address bound} -> SF40 converse`.
8. `{SF14 same-row slot injectivity, SF19 low/high preservation, SF20 extraction bridge, SF40 converse, n>=3, kappa=7, ell=3, both inputs in D} -> SF41 restricted compound injectivity`.
9. `{SF20, disjoint equal-width row/address slices, SF35 XOR definition and cancellation} -> SF35 exchange involution`. `{SF05 total width, shifted-mask bounds, XOR range closure, j<2^T} -> SF36 range`. `{SF35 involution, SF36 range} -> finite exchange bijection`.
10. `{SF05 q location, SF09 bulk predicate depending only on row, SF20 row-slice bridge, SF25 toggle definition, XOR cancellation} -> SF37 indicator involution`. Add `{q<T, j<2^T}` for finite range. `{involution, finite range}` gives indicator finite bijection. `{either finite bijection, SF38 literal permutation entries} -> one 1 per row and column`.
11. `{SF13 reverse and active range, SF19 splice safety, SF35 slice exchange semantics, SF40 clean encoding, SF42 definition, n>=3,kappa=7,ell=3,j in D} -> C finite/clean, correct row/slot, I(C)=W(I(j))`. `{these outputs, rho(s)<7} -> C in D`.
12. `{SF41 injectivity on D, SF42 candidate image, C in D, t=W(I(j))} -> SF43 uniqueness`. `{SF22 transpose entry definition, SF42 candidate image, SF43 uniqueness, u in D} -> SF45 entire restricted-column formula`. `{SF19 no-spill/extraction outputs, SF42 outputs, t definition, transpose entry definition} -> SF44 expanded cleanup record`.
13. `{SF23 global coefficients, honest scalar interpretation, ND nonzero, actual division, real coefficient/bound, square-root complement, SF26 matrix formula} -> intended bulk accepted amplitude AND analytic unitarity` is GAP-03, not a closed edge. The boundary tail additionally requires a consistent amplitude/angle convention, GAP-04. SF29 shared fields do not replace any input.
14. `{SF32 f labels, SF33 cases} -> literal clean-branch entries`. `{actual coherent function evaluation, true Nf inverse/bound, normalized orthogonal completion, row/control/phase conventions, compatible workspace} -> intended analytic f oracle` is GAP-05/GAP-06. SF34 citations are unresolved dependency pointers, not tail proofs.
15. `{full-space sparse unitary and inverse, physical J and W semantics, analytic bulk/boundary/f operators, actual sparse PREPARE and unprepare, correct indicator cleanup, compatible register adapters, actual active-product identification, path-isolation hypotheses for all intermediate indices, final projection convention} -> advertised normalized one-term block equation` is GAP-02 through GAP-09. The normalized coefficient and zero-error metadata SF07/SF49 are not premises proving this head.
16. `{actual primitive realizations, their parameter-valid cost theorems, composition accounting, preprocessing/evaluation and synthesis model} -> claimed resource tuple` is GAP-10. No cost edge follows merely from counts, labels, or the block identity. `{one-term blocks, coefficient phases, Hamiltonian composition scheme, normalization/success/error accounting}` would be required for Hamiltonian composition; this is excluded from local closure and unresolved, not supplied here.

OR structure is deliberately not manufactured. The historical row-local and active global maps are distinct target definitions, not interchangeable sufficient routes. Bulk-enabled and boundary-enabled rotations are complementary controlled sectors and both are needed for a full row-domain amplitude operation; they are not OR alternatives. The single-angle and doubled-angle descriptions are unresolved different contracts, not two verified routes. Finite n=1/n=3 specializations are not OR substitutes for arbitrary-width proofs. The direct modular-cancellation argument in section 2.3 and a reverse-shift argument are alternative proofs of the same narrow address-injectivity claim only. At the full block target there are zero demonstrated sufficient OR-routes in this source. A proposed finite clean-domain unitary extension versus the cited index-unitary/modular-add route may become candidate OR-routes only after separately specified contracts and constructions; neither is promoted here.

## 5. Source gaps and unresolved external dependencies

| ID | Missing source-level item | Why it matters / required next evidence |
| --- | --- | --- |
| GAP-01 | Exact historical bulk row partition and priority for SF17 | Resolve the counterinterpretation in section 2.4 before treating reverse-on-image as unconditional under M1 parameters |
| GAP-02 | Full-space sparse unitary extension, inverse, unused-branch action, and implementation of cited primitive | Restricted clean injection and transpose entries do not establish these; no clean ancilla assumption may create a missing extension |
| GAP-03 | Scalar interpretation, true normalizers, bounds, real rotations and unitarity | Free syntax has environments violating every claimed inverse/rotation law |
| GAP-04 | Consistent boundary accepted amplitude and angle convention | Existing formula differs at x=0 and negative x; no original-paper correction is certified |
| GAP-05 | Constructed f-oracle orthogonal completion, label preservation, coherent phase convention | Independent q entries need not be normalized or orthogonal and can change the row |
| GAP-06 | Exact external amplitude/coordinate/index-oracle statements and their access/resource assumptions | arXiv:2506.20478, arXiv:2405.12855v3 Lemma 1, and arXiv:2411.01131 Theorem 5 were not provided beyond descriptions; lemma labels differ locally |
| GAP-07 | PREPARE/unprepare, active-vs-long transcript bridge, indicator cleanup after row exchange | A reverse sparse label is not all-zero signal; indicator tied to old row may require actual cleanup proof |
| GAP-08 | Complete intermediate states/gamma formulas and product path expansion | Stored ranges/prefactors/orthogonal-remainder Boolean supply neither states nor transition equations |
| GAP-09 | Final selected block equals target/(ND*Nf*kappa), with projection width and all success sectors fixed | Generic extraction and self-equal cached contributions do not give the desired equality |
| GAP-10 | Uniform resource proofs at an explicit exact-real/query/logical/finite-bit tier | Stored complexity and ancilla budgets omit primitive implementations, evaluation, synthesis, depth, connectivity and readout |
| GAP-11 | Original-paper source fidelity/PDE derivation and Hamiltonian composition | Unavailable original text and formulas cannot be reconstructed from claimed labels; Hamiltonian composition is outside local closure |

These are not assertions that the missing mathematics is impossible or unavailable elsewhere. Only the collision and explicit wrong-amplitude examples rule out their particular overextended claims. The general absent bridges remain open source obligations. No API/toolchain/implementation failure is inferred from this source-only phase. The shell metadata parse error during this phase was immediately corrected and has no mathematical meaning.

## 6. Binder expectations for later anti-anchored comparison

No actual formal signature has been read. The following are source-derived expectations, not an assertion about the implementation. Classification is relative to this retrospective local source, never a finding that the original paper explicitly states these assumptions.

| Candidate mathematical claim | Expected inputs / classification | Inputs that must remain dependencies rather than excess public assumptions |
| --- | --- | --- |
| Free evaluation and finite matrix arithmetic | Dimensions, indices, environment: TYPING; expression and enumeration data: TYPING; stipulated zero/survivor hypotheses: SOURCE for these generic conditional lemmas | No unitarity follows; no invented norm instances |
| Literal parameter/layout formulas | Natural n,kappa,G,cost and fixed ceil-log convention: TYPING/STANDING | No hidden kappa>0, ell<=n, normalizer law in bare record constructors |
| Address inverse and active slot injection | n>=3, row<N, active slot bound(s): SOURCE locally; fixed offset/rho tables: STANDING; N=2^n: definition | An inverse-oracle circuit, coefficient nonvanishing, full-space bijection are not additional hypotheses |
| Splice no-carry and finite bound | a<N; for finite theorem j<2^T and 1+2n<=T: SOURCE locally; natural indices: TYPING | Modular address bound should be produced internally for the specialized global address; unused n>=2 is an interface artifact, not external source authority |
| Clean compound injection | n>=3,kappa=7,ell=3, both finite inputs padded-clean and slot<7: SOURCE/STANDING locally | Pairwise address distinctness and reconstruction are derived dependencies, not assumptions replacing their proofs; ell=3 is redundant but explicitly present in the exposition |
| Candidate image and restricted transpose column | Same specialized family; j in D; u in D for restricted column; t=W(I(j)) and C definition: SOURCE/definitional data | Candidate image equality, candidate clean/range, active injectivity, transpose entry=1 and cleanup record fields must be derived in the stronger theorem |
| Indicator and exchange finite permutations | Natural parameters; actual finite input width: TYPING/STANDING; literal map definitions | Do not add an assumed permutation, inverse identity or generic unitary to obtain the theorem being advertised |
| Intended analytic amplitude oracle | Actual scalar domain, coefficient family, meaningful normalizer and permitted source promises must be separately sealed; presently underspecified | Assuming c/s relations or a complete unitary as extra premises is valid only for a separately labeled generic conditional lemma, not closure of the advertised construction |
| Intended full normalized one-term block | Exact original target/signature unavailable; zero/nonzero normalizer and valid resource regime need explicit approved source contract | PREPARE correctness, SELECT/sparse action, unprepare, accepted branch, gamma identity, projection identity, unitary completion and resource bounds are construction dependencies, not convenience binders |

No RULED correction was supplied. Therefore no RULED binder is licensed. Any formal bundle later containing final block correctness, all-zero cleanup, unitarity, desired amplitudes, or the claimed resources as unadvertised premises must be recursively expanded and classified EXCESS for a source-facing construction claim, rather than accepted because the bundle has a convenient name. Generic conditional provider lemmas can legitimately assume their explicitly stated input equalities, but they must not be relabeled as the final unconditional construction.

## 7. Definition audit

Literal definitions: finite entry matrices; expression syntax and evaluation; ceil-log convention and natural-width arithmetic; bulk/boundary predicates; global offset/rho tables including defaults; row-local forward/reverse candidates; bit slices; splice I/S; clean encoding c; J and W; coefficient tables with branch priority; symbolic R matrix; f-oracle skeleton with arbitrary q symbols; transpose entries; selected-block extraction; C and D; stored counts/normalizer/error/gamma descriptions. Their literal status does not make their intended analytic interpretations true.

Characterized conclusions, not definitions by unexplained choice: uniqueness of the D-preimage follows from explicit C existence plus restricted injectivity. A future definition of C by unique characterization must first establish existence AND uniqueness on D; the current explicit formula already avoids that choice. The source does not characterize a unique full-space address extension or a unique orthogonal f completion. Many such extensions could exist, and the present skeleton need not be one. A default-zero completion cannot invent an on-source unitary.

Quotient/representative issues: modular addresses are literal residues, not quotient-type representatives; splice reconstruction is quotient/remainder arithmetic, not quotient choice. No global-phase quotient, purification choice, canonical dilation, spectral decomposition, or certified tensor-basis equivalence is given. If full unitary extensions are later selected, their nonuniqueness and independence of downstream projected conclusions from the chosen extension require separate obligations. No false uniqueness is licensed by the word 'completion'.

## 8. Seven quantum semantic slots

| Slot | Source-only reconstruction | Boundary or discriminatory test |
| --- | --- | --- |
| 1. Target and normalization | Local exact target is restricted transpose entries; advertised Robin block target only described; ND*Nf*kappa and error 0 are stored syntax | ND/Nf can be zero or nu independent; kappa=0 allowed in generic parameters; no normalized Hilbert state follows |
| 2. Dimensions/scalars/order/basis | Rational free-expression environments; high-to-low layout mf,1,ell,w,n,1; low bit0 ancilla; row next n; fixed n-bit address; column action, reverse temporal matrix order | ell>n breaks intended n-bit split; n<3 breaks active offset distinctness; no complex or Fourier-sign convention is supplied (Fourier unused, not silently fixed) |
| 3. Oracle access/inverses/controls | Global address formula is exact arithmetic; coefficient-function clean block and complementary indicator controls are literal; prior-oracle citations unresolved | Classical symbol labels do not imply coherent function evaluation, controlled access, inverse access, or constant-cost queries; transpose is not an inverse without global bijectivity |
| 4. Workspace and garbage | I preserves low/high regions but overwrites address; W exchanges row/address; J toggles indicator; C padded-clean with reverse sparse slot; f-completion may alter system label | D restriction indispensable; dirty-padding collision and encoded slot7 supply extra full-space preimages; m differs from actual projection width; no all-zero final signal |
| 5. Relative/global phase | Free signs retained in table and R; no equivalence modulo global phase invoked | Replacing signed x by nonnegative half-angle square root loses relative sign; parameter-dependent phases in f or completion cannot be discarded as one global phase |
| 6. Error/success/sectors | Matrix-entry equalities are exact; intended clean accepted amplitudes not normalized; stored error0 and remainder Boolean do not certify success probability | No absolute-square/Born rule, norm convention or probability bound is defined; accepted u in D does not exclude outside-D contributions; no amplification claim |
| 7. Cost tier | Only symbolic/query-like cost descriptions and wire counts; no supplied primitive/circuit implementation for several operators | Exact rational syntax is not exact-real analytic computation or finite-bit rotation synthesis; boundary-factor off-by-one; preprocessing, evaluation, inverse/control construction, depth/connectivity/readout unresolved |

## 9. Independent counterexamples and boundary pack

These are hand-derived discriminators from the supplied formulas, not executions or implementation findings.

1. Arbitrary inverse symbol: environment ND=2 and nuD=0 makes D*nuD=0 for D=1, while D/ND=1/2. Naming alone cannot establish division.
2. Arbitrary rotation symbols: c=2,s=0 gives R=2I, so R^T R=4I, not I. Even c=s=0 is permitted by free-symbol evaluation.
3. Boundary mismatch: x=0 yields accepted c=sqrt(1/2), not zero; x=-1 yields c=0, not -1. This tests amplitude and sign, not just probability.
4. Old row-local collision: N=8,row0, slots0 and3 ->0 under the intended boundary branch. Slot3 remains in the active seven-slot domain although its coefficient may be zero.
5. Eighth-slot collision at n=3: ell=3,w=0,L=16,H=128. With all higher bits and row/ancilla zero, u2=32 and u7=112 encode sparse slots2 and7. Both global offsets are zero, so I(u2)=I(u7)=0. For active j=u2, t=W(I(j))=0 and C(j)=u2. The full transpose t-column has ones at both u2 and u7, whereas its restriction to D has just the one at u2. This independently explains the exact scope of SF45.
6. Dirty-padding collision at n=4: ell=3,w=1,L=32,H=512. Indices128 and160 have row0, sparse slot2 and padding0/1 respectively. Both are sent to zero by the address map. The second lies outside D. Thus adding padded-space columns is not a harmless unitary completion.
7. Small-grid offsets: n=2,N=4 gives offsets `(2,3,0,1,2,1,3)`, so active slot0 and4 coincide and several inverse-pair uniqueness claims fail. At n=0, all addresses mod1 are zero. The n>=3 restriction is mathematical for active-slot injectivity, not merely cosmetic.
8. Width mismatch: n=1,kappa=7 gives ell=3,w=0. The sparse/padded display has width3 while the splice address has width1; q=5 rather than 1+2n=3. J may still be a permutation, but the compatible layout argument cannot be reused unchanged.
9. Bad completion: evaluate all f and q and nu symbols to zero. The literal f skeleton is the zero matrix, hence not a unitary. Alternatively arbitrary q can produce nonorthogonal columns or nonzero output on another row. A constructed orthogonal remainder is genuinely missing.
10. Resource cardinality: N=8,K1=2,K2=5 has exterior {0,1,6,7} of size4; K1+N-K2=5 is not its exact count. This need not refute an asymptotic upper bound, but refutes reading the expression as the exact exterior cardinality.
11. Historical bulk ambiguity: the all-bulk N=8,i=0,s=4 example in section 2.4 distinguishes unrestricted bulk parameters from the canonical boundary-stencil partition. It flags an omitted specification, not observed Lean behavior.
12. Invalid ranges: boundary predicate can hold for i>=N; n/G/kappa zero are allowed generic record data; bulk intervals may be invalid. Normalizer/product or clean-grid interpretation must not silently assume these cases away. Transpose equals adjoint only after real-valued coefficient interpretation; here entries0/1 are rational, but physical inverse still requires bijection.

## 10. Phase-2 boundary and handoff

This phase is whole-source, not a prefix or sample. All substantive input regions are accounted for above, the modular/splice/XOR/preimage arguments have been independently reconstructed, and source under-specification and analytic/full-space/resource gaps remain explicit. No author's separate sourcegraph or coverage has been compared yet. This phase does not certify historical module coverage, original-paper correctness, compiled statements, native acceptance, final root closure, merge, or purification.

Next phase requires separate authorization and a pinned formal comparison packet. It should compare actual types and ambient definitions against these expectations, particularly full carrier and D restrictions, ell<=n compatibility, the row-local partition, actual rotation conventions, arbitrary-symbol evaluation, active-vs-long transcript, and projection/success/resource semantics. The historical formalizer remains UNKNOWN; independence from this reviewer/any future decoder must be established with actual evidence, not invented identity strings.

Failure classification: NONE for completing the authorized phase-1 reading/seal. GAP-01 is a local source-specification issue and conditional counterinterpretation; named overclaims in section 9 are mathematically refuted, but the whole retrospective exposition is not retired. Salvage: modular inverse/slot injection, splice/clean reconstruction, XOR permutation arguments, and restricted-column reasoning are useful mathematical candidates, not admitted reusable Lean nodes. Process-memory entries consulted: none (out of scope). Direction fingerprint: whole-retrospective-source-first / exact-carriers-and-domains / independent-counterinterpretations / no-implementation. Parallel work/subagents: none. Common-blind-spot/comparator: not performed; no full-target verified alternative routes. Exposition/purification: not evaluated. Stop after sealing these notes and the phase1 manifest.
