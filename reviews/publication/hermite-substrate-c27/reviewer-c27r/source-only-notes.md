# Independent source-only mathematical review: Hermite substrate c27r

## Identity, evidence boundary, and verdict

Reviewer role: `/root/hermite_substrate_source_review_c27r`, distinct source-first mathematical reviewer. The only mathematical input inspected was `../hermite-substrate-author-c27r/source-only.md`, SHA256 `b971e269ccf4f89dde39ba87eb385a9c6d200acb97d570738f2b5bbac85784fd`. Read completely before this record was written. Project process instructions inspected: `AGENTS.md`, `HARNESS.md`, `.agents/skills/qbe-substantive-worker/SKILL.md`, `.agents/skills/qbe-source-dependency-audit/SKILL.md`, `docs/theorem-publication-protocol.md`, `docs/proof-digestion-protocol.md`, and `docs/evidence-routed-memory-protocol.md`.

No implementation Lean, author mapping, decoder reconstruction, previous review, publication registry, graph/inventory, test result, compiler/cache result, Git, network, simulator, or other author artifact was inspected. No subagent was used. No main-repository file was written. This document is frozen phase-one evidence and must not be edited after sealing; later corrections need a successor artifact.

Verdict: **SOURCE-ONLY PASS WITH BOUNDARIES**. I found no mathematical contradiction in S1–S14 at their stated strength. This is not implementation acceptance, not a Proof Seal, not full-source-chain correctness, and not an efficient state-preparation or finite-bit certificate. No source repair is proposed. Formal correspondence remains unreviewed pending separate authorization.

Provenance remains exactly the source's: retrospective local mathematical exposition dated 17 October 2026, historical formalizer UNKNOWN. It is not an external paper, not evidence of a historical pre-proof contract, and not a novelty judgment.

## 1. Independently reconstructed statements and mathematical checks

### S1 — Literal Hermite polynomial and positive literal function

The definitions are finite sums and ordinary real polynomial operations. Write `t=p+1`. The second term is `t^(k+1) A_k(1-t)`, so both summands have degree at most `2k+1`. In the formal power-series ring, `(1-X)^(-k-1)` has coefficient `binom(k+q,k)` at degree q. Multiplication by the series with coefficient `1/m!` gives exactly the source's `a(k,r)`. Its truncation through degree k therefore satisfies

`(1-X)^(k+1) A_k(X) = sum_{j=0}^k X^j/j! mod X^(k+1)`.

Thus `B_k^(j)(0)=1` and `B_k^(j)(1)=0` for `j≤k`. Applying the chain rule to `B_k(p+1)` and `B_k(-p)` gives all the displayed endpoint jets, with the factor `(-1)^j` only at the right endpoint. This is a finite coefficient argument, not convergence of an analytic infinite series.

Uniqueness is sound: the difference of two degree-at-most-`2k+1` solutions has roots of multiplicity at least `k+1` at each of 0 and -1. These are distinct roots, so their product of degree `2k+2` divides the difference, forcing zero.

All coefficients of `A_k` are nonnegative and its constant coefficient is 1. For `0≤t≤1`, each summand of `P_k` is nonnegative; for `t<1` its first summand is positive, and at `t=1` its second summand is positive. Hence the claimed strict positivity includes both endpoints. The outside exponentials are positive.

The minimal case is included: for `k=0`, `A_0=1` and `P_0(p)=exp(-1)(-p)+(p+1)`. It has exactly the two required values and is positive on [-1,0]. No `k≥1` assumption is needed. Polynomial jets are derived properties, not definition fields.

### S2 — Arbitrary selection and threshold differentiation

At a fixed x with common value and derivative, the selected function also has that common value. At every punctured point its difference quotient is one of the two original quotients. A neighborhood on which both quotients are close to d also works for any selector, with no continuity or local constancy of the predicate required. This proves the common-slope claim.

For `J_c`, away from c the *threshold* predicate is locally constant. At c apply the common-slope result. The displayed derivative formula follows, with the right branch selected exactly at c. The source does not assert that an arbitrary-predicate selector has this global derivative formula without appropriate pointwise hypotheses.

### S3 — Exactly finite-order gluing and the literal endpoint convention

The `k=0` continuity case follows from matching values and one-sided continuity. In the induction from order k to k+1, differentiability follows from S2, the derivative is the threshold splice of `f'` and `g'`, and these derivatives are C^k with matching jets through k. This proves C^(k+1) by induction, with no extra derivative order silently assumed.

First splice `P_k` on the left of zero to `exp(-p)` on the right. Its derivatives near -1 agree with those of the polynomial. A second splice at -1 to `exp(p)` is therefore justified. The resulting function agrees with the literal `f_k` except for a possible choice of formula at zero, where the values coincide; at -1 the polynomial is already the selected branch. Thus equality holds everywhere.

The certified order is the *same k* used to build the polynomial. It does not imply C^(k+1) or C-infinity for a fixed function. As a useful boundary discriminator, for k=0 the polynomial slope is `1-exp(-1)`, whereas the exterior slopes at -1 and zero are `exp(-1)` and -1. Thus this case is continuous but not differentiable at the junctions, confirming that a stronger regularity reading would be false.

### S4 — Monomial row update, not Bernstein subdivision

The j-th coordinate of the row product is `sum_{i=0}^j x^i binom(j,i) w^(j-i)=(x+w)^j`. Terms with `i>j` vanish by the binomial coefficient, even when truncated subtraction gives exponent zero and `w=0`. Empty-list multiplication is identity. Induction over a finite list gives the accumulated translation; contraction with the actual monomial coefficient vector gives q at the final point, provided `degree(q)≤d`.

For the Hermite polynomial `d=2k+1`, there are `d+1=2k+2` coordinates. This is an algebraic amplitude representation only. No binary-word enumeration, orthogonality, isometry, numerical stability, efficient coefficient construction, or circuit realization follows.

### S5 — Exact cut and off-by-one audit

For `L>0`, h is positive and `h M=πL`, so `p_M=0`. Put `z=(-1+πL)/h=M-1/h<M`. The natural ceiling exists by the Archimedean property and is zero for `z≤0`. Since M is a natural upper bound, `0≤C≤M`.

For any natural j, `j<ceil_N(z)` iff `j<z`; if `z≤0` both sides are false, and otherwise this is the ordinary ceiling property. Multiplication by positive h yields the first strict cut equivalence. The same argument using `p_M=0` gives `p_j<0 iff j<M`; conjunction yields the middle interval equivalence. A grid hit at -1 goes into the middle part. The zero sample can use the right formula because both formulas equal 1 there.

The full sample register has `N=n+1` bits, not n bits, and has `2^(n+1)` points. `n=0`, `C=0`, `C=M`, and unrelated k are allowed. In particular the search domain is the left half with M cells, not all `2^(n+1)` sample points.

### S6 — Exact-real binary search: invariant and one returned value/counter pair

For r=0, the invariant permits only `C=s` or `C=s+1`. S5 says `p_s<-1 iff s<C`, so the single comparison chooses the correct value. This also explains why a one-cell interval cannot be assigned zero comparisons.

For r>0, `a+b/2=p_(s+2^(r-1))`. If the strict comparison holds, the midpoint index is below C, hence the right-half closed endpoint invariant holds. Otherwise C is at most the midpoint, and the left-half invariant holds. The equal-to--1 case takes this latter branch. Both branches reduce r, so induction proves the output C.

Let K(r) be the counter vector for the actual returned run. Its recurrence is `K(0)=e_compare` and `K(r+1)=2e_field+e_compare+K(r)`, independent of geometry or branch. Therefore `K(r)=2r e_field+(r+1)e_compare` on all inputs. The initialization costs two additional field operations. With `(r,s)=(n,0)`, the same run returns C and has `(2n+2)e_field+(n+1)e_compare`.

Value correctness uses positivity and the invariant. Counter correctness does not. Exact real comparison is a primitive of this selected model, not a finite-bit algorithm. Index arithmetic, exponentiation by 2, loop/counter bookkeeping and allocation are explicitly uncharged; zero read/write counters are not a memory-allocation theorem.

### S7–S8 — Supplied cached geometry and one child

The schedule `s_r=2^r floor(C/2^r)` and `j_b=s_(r+1)+b 2^r` is a literal aligned schedule. `Full`, `Outside`, and `Partial` have the source's all-natural formulas. Their geometric names are interpreted only in the stated legal nonempty situation. For degenerate/reversed intervals, Full and Outside can both hold; one must not silently replace the formulas by an exclusive geometric trichotomy. Partial remains exactly `not Full and not Outside`.

The four flag comparisons compute those formulas when `last=first+size`. They cost four comparisons and two stored booleans.

The child has three initial reads, one bit selection, two charged natural additions, and three real field operations. The two flag calls cost eight comparisons and four writes. Reading the four flags adds four reads, and storing the seven payload words adds seven writes. Hence the exact vector is `(3,0,0,0,9,7,11,0)` in the source's order, with separate natural-addition count 2. Zero offsets do not waive additions or multiplication. The unused factor is neither read nor charged.

The five cache equalities are independent SOURCE promises:

1. parent.first = `s_(r+1)`;
2. parent.lower = `x(parent.first)`;
3. level.width = `g*2^r`;
4. span = `2^r`;
5. midpoint = `2^n`.

Substitution gives the aligned first index; affine distributivity gives both coordinates; the flag formulas then give four exact Full/Partial values. These seven output equalities are conclusions. The five premises are not typing: stale coordinates or widths have the same carriers but can make these conclusions false. No `g>0` or `r≤n` is needed for this purely algebraic equality refinement. The supplier does not itself produce any of the five cached ingredients.

### S9 — Two returned children, storage charges, and bounded endpoints

Both child runs are executed once. The length-two materializer adds two selection comparisons, four reads and four writes without rerunning callbacks. Twice the S8 vector plus this overhead equals `(6,0,0,0,20,18,26,0)`, whose component sum is 70. The separate count is four natural additions. Neither `70+4` nor 74 is an eight-counter sum; the operation classes must remain distinct.

The two-child refinement abbreviates the conjunction of all seven child equalities for *both* bits. It is not an extra oracle promise. Under the five coherence equalities both returned children have the claimed values and flags while this same run keeps the exact charges.

For the endpoint word bound, only parent.first coherence, span coherence, `cut≤2^n`, and `r≤n` are needed. Indeed `s_(r+1)≤cut`, `span≤2^n`, and `b≤1`, so each excluded endpoint is at most `3*2^n<2^(n+2)`. An unsigned n+2-bit word therefore suffices. Coordinates, width coherence, positive g, and the other child equalities are not necessary for this subclaim. No implementation bit-cost follows from this word-length bound.

### S10–S11 — Explicit finite layout, stored fields, and actual entry reads

There are `2+(1+P)+1=P+4=2k+6=D` tagged states. Middle coefficient j maps to `3+j`, ending at `D-2`, so the right tag `D-1` is distinct. This works for k=0 (`P=2,D=6`) without an empty coefficient block. The specified sum/optional-boundary layout is a literal bijection, not an unspecified cardinality choice.

The two field records contain exactly the seven listed data kinds; the middle row and shared matrix are stored vectors and stored rows. Their references count as words. The block meaning is literal and block diagonal. Boundary-to-coefficient orientation is a row; reversing it would change the target matrix.

The block dispatch charge is eight comparisons. Boundary-boundary work adds one read and one comparison; scalar work one read; middle-row work two reads; shared-matrix work three reads; cross-block/zero cases no numerical read. These satisfy the stated per-component bound 12. The complete reader adds one record read and 16 index-decoding comparisons, so it satisfies the stated conservative per-component bound 29 (indeed these listed charges are smaller). The eight-per-index decode charge is a declared conservative charge, not a claim of eight unavoidable actual tests. The described threshold/optional-boundary decoder has at most six tests and works for every legal integer bond index `0≤index<D`.

The value and resource statements need no source correctness of the stored fields. Index arithmetic and flattening are word arithmetic excluded from the charged counter model. No scalar function callback may be substituted for a stored row or matrix while retaining these costs.

### S12 — Whole stored two-slice table from the same run

Rows are incoming bonds, columns are `(bit,outgoing bond)`, flattened as `b*D+c`. There are exactly `2D^2` entry executions. Nested vector materialization stores the entries and D row references, giving the source's extra `(2D^2+D)*(2e_read+2e_write)`.

For any component, using only S11's bound gives `29*(2D^2)+4D^2+2D=62D^2+2D≤64D^2≤72D^2` because D≥1 (here D≥6). Thus the advertised `72D^2` is safely conservative. Summing eight component bounds gives `576D^2`; this is not an exact equality. No field arithmetic, transcendental computation, emitted record, square root, inverse cosine, or trigonometric evaluation occurs in the reader/assembly routine.

The entry identity and cost bound concern one actual materializing run. This does not count generation of the supplied data, exponentials, source polynomial coefficients, subdivision/restriction, coordinates, excluded index arithmetic, or finite-bit conversion. A matrix callback would invalidate this argument.

### S13 — Literal Bernstein supplier formulas and their seven-way conjunction

All-carrier source formulas use `r=n-t` with truncated natural subtraction and total real division. Legal stage meaning additionally uses `L>0` and `0≤t≤n`; these are not needed merely to define a real number. For L=0, total division makes the formulas defined but provides no positive-grid interpretation.

The degree-d Bernstein basis is a basis of polynomials of degree at most d: its j-th element has first nonzero monomial coefficient `binom(d,j)` at degree j. This nonzero triangular coefficient matrix proves both existence and uniqueness of beta. The displayed finite ell formula is correct: expand `t^i(1-t)^(k+1)` to degree d by inserting `(t+(1-t))^(k-i)`. The term with `j=i+v` contributes `a(k,i) binom(k-i,v)/binom(d,j)`. Reflection sends coordinate j to d-j. Thus `beta_j=exp(-1) ell_j+ell_(d-j)` is exactly the source polynomial's Bernstein row, not an additional supplier assumption or scalar-evaluation oracle.

Repeated `D_z` performs de Casteljau subdivision. `L_z(c)` represents the restriction to `[0,z]`; reversal plus `L_(1-u)` and reversal back gives `R_u(c)`, representing restriction to `[u,1]`. Applying `L_((v-u)/(1-u))` therefore represents `[u,v]` when `u≠1`, including algebraically non-unit real parameters. Only source indices through d are used. The formula at `u=1` remains literal under total division but must not be advertised as general affine restriction there. On a legal fully included middle child, `size=2^r>0`, `first+size≤M`, and g>0 imply `x(first)<0`, hence `u<1`; no new kernel-output assumption is needed.

As row updates, S0 has outgoing coordinate j equal to `2^(-j) sum_{i≤j} binom(j,i)c_i`, and S1 has outgoing coordinate j equal to `2^(-(d-j)) sum_{i≥j} binom(d-j,i-j)c_i`. These are respectively left- and right-half de Casteljau coefficient rows. This interpretation is separate from the S4 monomial translation matrix.

For each bit, all seven clauses must hold together: left partial; guarded left injection; left-free scalar; middle partial; guarded entire middle injection vector; entire shared matrix; right scalar with the stage/bit guards. Entries are real equalities or Boolean equalities, not type formation. Disabled injections must actually store zero. A false partial flag does not cancel a nonzero boundary-to-coefficient or boundary-to-free injection entry; that entry occupies a different block position.

No clause states equality of the assembled table with the desired source kernel. They expose explicit raw fields, enabling a substantive conditional substitution theorem. Producing records meeting these clauses is a separate obligation and has no cost certificate here. The source defines the local kernel using these formulas; its agreement with a complete raw chain is not established in S13–S14.

### S14 — Conditional local identification and strict closure boundary

Define the local kernel by substituting S13's formulas into S11's block form. For each pair of tagged bonds, the relevant field equality proves block equality; cross-block cases are both zero. The complete seven-clause conjunction supplies every case. Applying this to both records and then S12's entry identity yields table equality for every incoming bond, bit and outgoing bond in the explicit finite layout. S12's cost bound remains valid because it concerns this same run and holds even for arbitrary records.

This is a local conditional materialized-table refinement, not proof that the field supplier exists efficiently, not a whole-chain contraction theorem, and not quantum state preparation. S4 and S13 cannot be identified solely from matching P-dimensional carriers. Their basis change and any downstream chain/compiler bridge remain outside this source, not silently discharged source nodes.

## 2. Exhaustive source-region coverage

Every substantive S1–S14 region has NODE disposition. The following subnode inventory covers formulas, definitions, statements, construction/proof paragraphs, and resource/boundary paragraphs. No mathematical citation occurs in this source. The provenance preamble is `EXCLUDED(nonmathematical provenance)` from the proof DAG but is retained as binding metadata. Boundary prose below is recorded as boundary nodes, not dropped as exposition.

| Region | Independently reconstructed source nodes | Disposition |
| --- | --- | --- |
| S1 | S1.coefficients; S1.literal-polynomial; S1.degree-jets; S1.formal-series-proof; S1.uniqueness; S1.literal-piecewise-function; S1.positivity; S1.no-evaluation-cost | NODE all |
| S2 | S2.threshold-selector; S2.arbitrary-selector-common-slope; S2.quotient-proof; S2.threshold-neighborhoods; S2.derivative-identity | NODE all |
| S3 | S3.finite-gluing; S3.base-continuity; S3.derivative-induction; S3.exponential-jets; S3.zero-splice; S3.minus-one-locality; S3.outer-splice; S3.literal-endpoint-equality; S3.fixed-order-boundary | NODE all |
| S4 | S4.monomial-row; S4.translation-matrix; S4.truncated-exponent-zero-case; S4.binomial-update; S4.list-empty-and-step; S4.polynomial-contraction; S4.Hermite-bond; S4.no-circuit-cost | NODE all |
| S5 | S5.grid-width-step; S5.natural-ceiling; S5.midpoint-and-cut-bound; S5.three-strict-cut-equivalences; S5.endpoint-assignment; S5.zero-width-index-cases | NODE all |
| S6 | S6.counter-model-and-composition; S6.search-base; S6.search-step; S6.uniform-counter-recurrence; S6.grid-invariant; S6.base-and-branch-proof; S6.initialization; S6.same-run-cut-and-cost; S6.exact-real-and-omissions | NODE all |
| S7 | S7.aligned-schedule; S7.affine-coordinate; S7.parent-and-level-records; S7.supplied-input-boundary; S7.grid-stage-specialization; S7.literal-interval-predicates; S7.degenerate-carrier-boundary | NODE all |
| S8 | S8.flag-routine-and-counter; S8.child-reads-and-selection; S8.four-output-formulas; S8.exact-counter-and-integer-count; S8.five-cache-promises; S8.seven-output-refinement; S8.no-positivity-or-stage-bound-needed | NODE all |
| S9 | S9.two-once-only-child-runs; S9.materializer-model; S9.two-child-counter-70; S9.separate-four-additions; S9.same-run-both-child-refinement; S9.endpoint-word-bound; S9.subset-premise-proof; S9.word-not-bit-cost-and-omissions | NODE all |
| S10 | S10.dimensions; S10.tagged-carrier-and-layout; S10.two-stored-field-records; S10.stored-matrix-access-model; S10.supplier-boundary | NODE all |
| S11 | S11.left-block; S11.middle-block; S11.right-and-cross-blocks; S11.dispatch-and-case-reads; S11.block-value-identity; S11.index-decoder-charges; S11.complete-entry-reader; S11.uniform-12-and-29-bounds | NODE all |
| S12 | S12.table-layout-and-flattening; S12.once-per-entry-materialization; S12.nested-storage-overhead; S12.per-component-72D2; S12.total-576D2; S12.same-run-entry-identity; S12.zero-arithmetic-and-rotation-components; S12.supplier-and-bit-cost-exclusions | NODE all |
| S13 | S13.all-carrier-stage-formulas; S13.legal-grid-guard; S13.shared-matrices; S13.Bernstein-characterization; S13.explicit-ell-and-beta; S13.de-Casteljau-L-and-R; S13.literal-Restrict; S13.u-ne-one-boundary-and-geometric-proof; S13.seven-supplier-clauses; S13.disabled-zero-requirement; S13.not-producer-or-desired-result-assumed | NODE all |
| S14 | S14.literal-local-kernel; S14.seven-clause-case-proof; S14.both-record-composition; S14.same-run-table-and-cost; S14.monomial-versus-Bernstein-boundary; S14.full-quantum-and-producer-exclusions | NODE all |

No omitted bridge is necessary for the *stated local conditional targets*. Thus no in-scope mathematical SOURCE_GAP was found. A source-to-whole-chain bridge, field-record producer, normalization/isometry construction, circuit compiler, finite-bit analysis, or basis adapter would be a new explicit obligation if a broader target were asserted. Their absence is currently a boundary, not proof that they are impossible.

## 3. Source proof/construction topology, reconstructed without Lean

Each brace below is a complete AND tail; separate guarded branches are not independently unconditional arrows.

- `{S1.finite-coefficients, formal inverse coefficient identity} -> S1.jets-and-degree`; `{degree-bound, two matching jets, distinct endpoints} -> S1.uniqueness`; `{nonnegative coefficients, constant-one coefficient, interval factors} -> S1.positivity`.
- `{common value, common derivative} -> S2.arbitrary-selector-derivative`. `{global differentiability, threshold locality off c, matched value/slope at c, previous node} -> S2.splice-derivative`.
- `{C^k inputs, all jets through k equal} -> S3.C^k-splice` via the guarded base `k=0` OR induction `k>0`. `{S1.jets, exponential jets, finite-gluing, locality near -1, equality at zero} -> S3.f_k-C^k`.
- `{literal row/matrix, binomial theorem} -> S4.one-update`; `{one-update, list-empty/step} -> S4.list-update`; `{list-update, degree(q)≤d, true monomial coefficients} -> S4.polynomial-value`. This is a separate algebraic branch; it does not supply S13's Bernstein matrices.
- `{L>0, grid formula, natural-ceiling property} -> S5.cut-equivalences-and-bound`.
- `{search recurrence, counter composition} -> S6.all-input-cost`, independently of S5. `{S5.cut-equivalences, interval invariant, base/step split} -> S6.search-value`. `{initialization, S5.C≤M, hM=πL, search-value, all-input-cost} -> S6.same-run-root-value-and-cost`.
- `{four literal comparisons, Boolean conjunction/negation} -> S8.flags`. `{supplied cached words, literal child operations, flags, read/write charges} -> S8.literal-values-and-exact-cost`.
- `{S8.literal-values, ALL FIVE cache equalities, affine-coordinate identity} -> S8.seven-source-child-equalities`. No one cache equality alone is sufficient.
- `{two S8 runs, two selections, length-two materializer} -> S9.two-child-values-and-70-counter-plus-four-additions`. `{same two-child run, ALL FIVE equalities} -> S9.both-child-refinement-with-same-cost`.
- `{parent.first coherence, span coherence, cut≤2^n, r≤n, floor-schedule-bound} -> S9.n-plus-two-bit-endpoint`. This is a separate weaker-premise branch, not dependent on all five promises.
- `{S10.explicit-layout, stored-record-carrier, S11.block-form} -> S11.stored-block-meaning`; `{actual dispatch/read algorithm, stored-access model} -> S11.entry-value-and-cost` for arbitrary records.
- `{S11.entry-value-and-cost, D>=1, nested materializer, explicit table layout} -> S12.same-run-table-value-and-72D2/576D2-cost`.
- `{S1.literal-polynomial, Bernstein basis invertibility, finite degree elevation and reflection} -> S13.beta-characterization-and-formula`. `{de Casteljau recursion, reversal, u≠1} -> affine-restriction interpretation`; `{legal grid, Full middle child, positive size} -> u<1` supplies this guard where used. Literal Restrict remains defined without that interpretation.
- `{S11.block form, S13.literal field formulas} -> S14.source-local-kernel-definition`.
- `{ALL SEVEN supplier clauses for b=0, ALL SEVEN supplier clauses for b=1, S12.entry-identity, S10.layout, source-local-kernel-definition} -> S14.every-table-entry-identification`; combine with the independently uniform S12 bound for the same-run resource conclusion.

Guarded OR topology inside the source:

1. Literal f: `p<-1` OR `-1≤p≤0` OR `p>0`; endpoint formula equality justifies the nested-splice representation.
2. Selector derivative: off-threshold left OR off-threshold right OR threshold common-slope case.
3. Search: `r=0` OR `r>0`; within the latter, `middle<-1` OR its negation. The base case also has its comparison guard. Both recursive paths have identical cost recurrence.
4. Child bit: `b=0` OR `b=1`, with each selecting its actual offsets. For arbitrary intervals Full and Outside are *not* an unguarded exclusive partition.
5. Stored block reader: guarded disjoint tag-pair cases. All cases are required for the universal matrix theorem, even though one entry executes only one branch.
6. Supplier injection: Full OR not Full, with the latter storing zero; right factor: `r=n` OR `r≠n`, then the bit guard. These are literal guarded formulas, not optional supplier clauses.

There are no two alternative whole constructions claimed sufficient for one final quantum target in this source. In particular S4 and S13 are not OR routes to a proved state-preparation theorem, and the seven supplier clauses must never be represented as seven separately sufficient edges.

## 4. Expected public binder and definition audit

This is an expected-interface audit from the source, not an inspection of actual formal binders. Pure carriers and finite index types are TYPING. Mathematical inequalities and correctness equalities below are SOURCE. There is no RULED correction and no extra STANDING mathematical assumption supplied by this review.

| Target/interface | TYPING data | Legitimate SOURCE premises | Results that must remain dependency edges, not extra public assumptions |
| --- | --- | --- | --- |
| S1 polynomial/function properties | natural k; real argument; finite indices | no extra k restriction | degree, jets, positivity, existence/uniqueness |
| S2 selection | real functions, predicate, c/x/d | common value and common derivative; for global threshold result differentiability and matched junction data | selector/splice derivative conclusion |
| S3 general gluing | natural k, functions, c | globally C^k inputs and all matching jets | finite gluing theorem |
| S3 Hermite regularity | natural k | none beyond literal construction | S1 jets, exponential derivatives, generic gluing |
| S4 contraction | natural d; real weights/origin; polynomial | degree(q)≤d; coefficient row really is q's monomial coefficients | row update and q-evaluation identity |
| S5 grid / S6 search value | natural n/r/s; real L/a/b | L>0; generic search's coordinate/width/closed-endpoint invariant | exact cut, midpoint identity, search correctness |
| S6 counters | same input carriers | no geometry premises | uniform recurrence and exact counter vector |
| S8 literal / S9 literal | cached record carriers, naturals, bit | no coherence premise for literal equations/cost | literal returned values and counters |
| S8–S9 aligned refinement | same carriers, schedule parameters | all FIVE cache equalities | seven child values/flags, both-child refinement |
| S9 endpoint word bound | naturals | parent.first and span coherence, cut≤2^n, r≤n | endpoint bound; do not add unused coordinate/width equalities |
| S11–S12 reader/table | k, finite indices, two stored records | none about source correctness | entry identity and uniform assembly costs |
| S13 beta | k, coefficient index | none beyond literal P_k and degree d=2k+1 | Bernstein existence/uniqueness and explicit coefficient identity |
| S13 affine interpretation | real u/v and coefficient row | u≠1; legal-grid/full-child facts derive it at use site | polynomial restriction identity |
| S14 conditional table refinement | k/n/t/L, finite index layout, supplied stored records | all seven field clauses for EACH bit; legal L/stage guards only when claiming positive-grid stage interpretation | record block equality, final table equality, resource bound |

Forbidden EXCESS patterns would include assuming C^k of literal f_k; assuming its endpoint jets as definition fields; assuming the search already returns C; replacing five cache equalities by a type label; replacing all seven fields by a desired-result equality; assuming table/source-kernel equality in order to prove itself; or demanding a normalized/isometric quantum object absent from the source. Conversely, the explicit conditional field equalities are not EXCESS merely because they are strong: they are exactly the source's supplier contract, not a claim of an unconditional producer.

Definitions:

- Literal: a/A/B/P, piecewise f, J and predicate selector, monomial row/T, grid and natural cut formula, search and eight-counter run, schedule and affine coordinates, interval flags, child routine, tagged layout, stored record/block meaning, reader/materializer, S0/S1, ell/beta formula, de Casteljau transforms, total-divided Restrict, seven-clause contract, and source local kernel.
- Characterized objects: natural ceiling is uniquely characterized as the least natural upper bound (with existence for every real); P_k is additionally uniquely characterized by degree and jets; beta is uniquely characterized by the Bernstein expansion. Literal formulas independently identify the latter two. No fallback object or zero/default rescue is licensed.
- Quotient/representative: none. No chosen global phase, unitary dilation, spectral representative, or noncanonical bond bijection is introduced. The index layout is explicit. No false uniqueness is asserted for a quantum representative.

## 5. Seven semantic slots and applicability/cost scope

1. **Target and normalization.** Positive literal real f_k, exact grid cut, exact classical runs, monomial amplitudes, and a conditional local real table. No normalization constant or normalized state is supplied or asserted.
2. **Dimensions/scalars/order.** Real scalars; arbitrary natural k including zero; d=2k+1, P=2k+2, D=2k+6. Grid width n means N=n+1 bits. Natural subtraction is truncated. Row vectors multiply matrices on the right. Table columns are bit-major `(b,c)` flattened `bD+c`; the tagged bond decoder is fixed. No unstated tensor/basis equivalence is used.
3. **Oracle/access.** Search has exact comparisons. Local assembly accesses supplied stored fields/rows/scalars; it does not evaluate source kernels by callback. No coherent parameter oracle, inverse, controlled access, or finite-input real-comparison implementation is promised. The field supplier remains conditional.
4. **Ancillas/workspace/garbage.** These are classical value/counter routines with charged record payloads and materialization. No quantum ancilla cleanup, overwritten quantum registers, reversible implementation, or garbage-sector theorem is asserted. Uncharged allocation/bookkeeping is not free quantum workspace.
5. **Phase.** Entries are real and literal, including signs where formulas permit them. Positivity of f_k is exact. There is no state considered only up to global phase and no relative-phase/coherent-label statement. Quantum phase semantics cannot be inferred from these algebraic prerequisites.
6. **Error/success.** All equalities and comparisons are exact. No approximation epsilon, probabilistic success/confidence, postselection branch, norm-error guarantee, rounding rule, or numerical stability statement appears. None should be invented as an omitted premise.
7. **Resources.** Eight nonnegative counters, in order: field arithmetic, sqrt, arccos, trig, comparisons, stored reads, stored writes, emitted records. S6 and S8–S9 give exact vectors in this model; S11–S12 give conservative bounds. The 70 counted operations and four separately charged natural additions must stay distinct. Endpoint word sufficiency is not word-operation implementation cost. Field-record generation, exponentials, coefficients, restriction/subdivision, coordinates, power/cast generation, index arithmetic, Boolean connectives, tuple access, loops and counter/proof bookkeeping are outside the respective selected charge models as explicitly stated. No gate/depth/connectivity, Clifford+T, bit-complexity, readout, or efficient whole-source-producer conclusion follows.

## 6. Final handoff and residuals

Objective/frontier: independently validate the complete S1–S14 local source mathematics and freeze a source-first expectation before formal exposure.

Mathematical delta: source-only reconstruction of polynomial/regularity, exact cut/search, cache-conditioned children, stored block assembly, and seven-clause conditional local refinement, including exhaustive coverage and complete AND/guarded-OR topology.

Failure class: NONE. No mathematics was retired; no source repair was needed. No environment result was used to make a mathematical claim. Salvage audit: not applicable to a failed route; reusable mathematical observations are the finite coefficient proof, common-slope selector lemma, exact cut invariant, subset-premise endpoint bound, Bernstein restriction guard, and conservative assembly-cost derivation.

Process-memory records consulted: none; out of scope for the sole-mathematical-input review. Direction fingerprint: fresh source-only mathematical/topological review with no implementation knowledge. Expected information gain: detect false mathematics, overstrong assumptions, omitted topology and cost-model drift before formal comparison. Parallel work/subagents: none used by this reviewer. Cross-route comparator: not applicable; no alternative complete quantum routes are claimed.

Purification/Exposition Seal: NOT REVIEWED; no main-repository or Lean node was inspected. This readable source-only record does not grant those statuses. Confidence is high for the exact local statements, subject to a later independent comparison of actual formal definitions/signatures and the source-blind reconstruction.

Next permitted action: report this frozen evidence and its actual SHA256 values, then wait for the parent to give separate formal-phase authorization. Do not modify these bytes during any later phase.
