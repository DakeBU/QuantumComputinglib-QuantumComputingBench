# Author-private whole-module coverage (not decoder evidence)

Role: retrospective source AUTHOR-curator, not independent decoder/reviewer.
Historical formalizer UNKNOWN. No old verdict, decoder reconstruction or reviewer
result was consulted. The natural source is `source-only.md`, sections S1–S14.
This private file MUST NOT be placed in the source-first reader's initial packet.

## Whole scope and environment

All five production files were read completely, including comments, imports,
ambient namespaces/open declarations, noncomputability markers, proofs and private
helpers. All substantive declarations below map to the natural source; none of
the five whole modules is excluded. Lexical public inventory is 12+10+9+24+16=71;
there are additionally 3 private cutoff helpers and 1 private kernel helper.
These are inventory counts, not formal elaboration counts or scientific progress.
There are 825 physical lines / 725 nonblank lines across the five files.

No production file changed; no Git, Lean, build, simulator or cache-management
command ran. Hashing is byte-level read-only. A pinned dependency *source file*
was inspected to verify executable sum/option/product layout, not to execute
or alter its cache. No test-build success is asserted by this author packet.

| Module | Complete ambient context |
| --- | --- |
| HermiteSmoothness | Imports HermitePolynomial, Mathlib Analysis.Calculus.ContDiff.Polynomial, Analysis.Calculus.Deriv.Slope, Topology.Piecewise; global `noncomputable section`; opens Filter Set Topology Polynomial and HermitePolynomial; namespace QuantumBlockEncoding.HermiteSmoothness; no local/scoped variables, notation or set_option. |
| HermiteTransferCores | Imports HermitePolynomial and Mathlib.Data.Matrix.Mul; global noncomputable section; open scoped BigOperators Matrix, open Matrix; namespace QuantumBlockEncoding.HermiteTransferCores; no local/scoped variables or options. |
| HermiteBinaryCutoff | Imports HermiteBoundaryInjection and StoredGivens; namespace QuantumBlockEncoding.HermiteBinaryCutoff; opens StoredGivens HermiteBoundaryInjection; below/search/compute individually noncomputable; no ambient variable, notation or option. |
| StoredHermiteChildGeometry | Imports StoredBinaryCoordinates and StoredHermiteGeometry; namespace QuantumBlockEncoding.StoredHermiteChildGeometry; opens StoredGivens StoredBinaryCoordinates StoredHermiteGeometry HermiteBoundaryInjection; child/children individually noncomputable; no ambient variable, scoped notation or option. |
| StoredHermiteKernelTable | Imports HermiteExplicitBond and StoredTensorTrain; namespace QuantumBlockEncoding.StoredHermiteKernelTable; opens StoredGivens StoredTensorTrain HermiteBoundaryInjection and scoped BigOperators; no noncomputable section, ambient variable or option. |

The imported Op inductive has a provider-local transparency option
`backward.isDefEq.respectTransparency false`; it is not ambient in these five
files and is not a mathematical premise. Provider dependency-source definitions
have their own scopes; no source theorem is inferred from an import alone.

## Complete declaration disposition

Line numbers refer to the raw module hashes in `source-freeze.md`. Every row is
NODE in the authored mathematical exposition; this is not a graph publication.
Helper bookkeeping is shown with its mathematical reason, not given independent
external-source credit.

### HermiteSmoothness: 12 public, no private

| Line / declaration | Source coverage and exact input boundary |
| --- | --- |
| 22 splice | S2 literal threshold with strict left condition and right value at c. |
| 25 hasDerivAt_ite_of_eq | S2 arbitrary decidable predicate; two common derivatives at x AND equal values. No regularity premise on predicate. |
| 38 hasDerivAt_splice | S2 global differentiability of both branches; equal values AND derivatives at c; output derivative at every x. |
| 56 deriv_splice | S2 functional derivative identity under the same four branch premises. |
| 64 contDiff_splice | S3 finite natural k; both globally C^k; jets for EVERY j≤k, including j=0; induction includes continuity at k=0. |
| 92 iteratedDeriv_exp | S3 all natural j and all real x; no k or L premise. |
| 95 iteratedDeriv_exp_neg | S3 all j,x with exact (-1)^j factor. |
| 100 contDiff_right_splice | S3 global C^k for polynomial/right exponential join; polynomial jets are internally supplied, not binders. |
| 113 right_splice_eventuallyEq | S3 equality to polynomial on a neighborhood of -1, all k. |
| 120 contDiff_double_splice | S3 two global gluing applications. |
| 130 smoothInitial_eq_double_splice | S1/S3 all-real equality, especially p=0 where original ≤ versus strict branch differs. |
| 147 smoothInitial_contDiff | S3 actual f_k globally C^k for all natural k, including 0; no C^(k+1)/C∞ strengthening. |

### HermiteTransferCores: 10 public, no private

| Line / declaration | Source coverage and exact input boundary |
| --- | --- |
| 20 rowFeatures | S4 row x^i, i∈Fin(d+1). |
| 24 translationCore | S4 binomial entry, natural truncated subtraction; w arbitrary real. |
| 27 translationCore_below_diagonal | S4 zero for j<i because choose vanishes; no nonzero-w premise. |
| 32 rowFeatures_translationCore | S4 exact row update by binomial theorem for arbitrary d,x,w. |
| 53 transfer | S4 recursive sequential right multiplication; empty weights identity. |
| 57 transfer_rowFeatures | S4 origin+list sum, no binary restrictions. |
| 67 polynomialAmplitude | S4 coefficient-vector contraction, defined even without degree promise. |
| 70 polynomialAmplitude_eq_eval | S4 degree/natDegree≤d is a substantive SOURCE promise on q; zero polynomial included. |
| 82 sourceInterpolant_transfer | S1/S4 actual P_k and degree bound from provider, not assumed interpolation data. |
| 88 source_transfer_dimension | S4 exactly 2k+2 monomial coordinates; no sample-bit or complexity conclusion. |

### HermiteBinaryCutoff: 9 public plus 3 private

| Line / declaration | Source coverage and exact input boundary |
| --- | --- |
| 19 below | S6 one exact-real x<-1 comparison returning its actual truth value. |
| 24 search | S6 literal recursion including one-cell compare and natural index update. |
| 35 search_cost | S6 exact 2r field / r+1 compare, ALL arguments; other counters zero. |
| 46 private half_span | S6 interval-halving identity g*2^(r+1)/2=g*2^r; bookkeeping, no assumption. |
| 51 private middle_point | S5/S6 affine grid midpoint identity at natural start+2^r. |
| 59 search_value | S6 L>0 and start≤C≤start+2^r, grid lower/span fixed by statement; these are SOURCE invariant premises, not typing. |
| 95 compute | S6 πL multiplication, subtraction from zero, then n-level search; no ceiling evaluation. |
| 100 private root_span | S5/S6 h*2^n=πL valid for all real L; division denominator 2^n≠0. |
| 108 compute_value | S5/S6 L>0; root invariant supplied internally using C≤2^n. |
| 115 compute_cost | S6 exact vector for ALL n,L, independent of positivity. |
| 122 compute_comparisons | S6 projection n+1. |
| 126 compute_field_operations | S6 projection 2n+2. |

### StoredHermiteChildGeometry: 24 public, no private

| Line / declaration | Source coverage and exact input boundary |
| --- | --- |
| 19 Flags | S8 two Bool fields full,isPartial; both generated projections accounted for. |
| 24 flags | S8 four compare + two output writes; last excluded endpoint. |
| 32 flags_full | S7/S8 Full literal when last=first+size, all naturals. |
| 37 flags_partial | S7/S8 Partial literal, all naturals; no hidden valid-interval promise. |
| 43 flags_cost | S8 exact counter vector. |
| 48 Child | S8 first:Nat, lower/upper:R, four Bool flags; all seven fields covered. |
| 57 ChildRun | S6/S8 run containing actual value and eight counters; separate Nat integerAdditions. Parametric carrier α is TYPING. |
| 61 child | S8 literal stored-word algorithm for arbitrary parent/level/span/cut/midpoint/bit. |
| 82 child_first | S8 parent.first+(if bit then span else 0). |
| 88 child_lower | S8 parent.lower+(if bit then 1 else 0)*width. |
| 94 child_upper | S8 returned lower+width, not independent semantic oracle. |
| 99 child_flags | S8 all four exact predicates, no source-data promise. |
| 110 child_cost | S8 exact 3F+9C+7R+11W. |
| 118 child_integerAdditions | S8 exactly two, separate from Op total. |
| 123 child_refines | S8 full five SOURCE cache equalities; first/lower/upper and four source flags all OUTPUT. No L>0 or r≤n is in this signature. |
| 158 children | S9 false and true computed once; stored in that order; selection and collect costs. |
| 168 children_value | S9 Boolean-index projection of actual pair equals actual single child. |
| 174 children_cost | S9 exact 6F+20C+18R+26W. |
| 182 children_integerAdditions | S9 exactly four. |
| 187 children_total_cost | S9 sum of eight components exactly 70, NOT 74 and not integer-inclusive bitcost. |
| 195 Refines | S9 abbreviation for conjunction of seven output equalities, with all S8 formulas. |
| 204 children_refines | S9 conditional source refinement for either bit; the five inputs retained. |
| 216 children_certified | S9 both refinements AND 70 total AND 4 additions in ONE actual returned pair run. |
| 231 child_index_word_bound | S9 parent.first=schedule, span=2^r, cut≤2^n, r≤n; output first+span<2^(n+2). No coordinate, width or midpoint premise needed. |

### StoredHermiteKernelTable: 16 public plus 1 private

| Line / declaration | Source coverage and exact input boundary |
| --- | --- |
| 28 Fields | S10 all seven data fields, including Bool partial flags, scalar injections/free/right, Vector R P injection, nested stored P×P matrix. No semantic callback field. |
| 38 blockView | S11 entire tagged block matrix, both boundary states, all cross blocks zero. |
| 50 storedBlock | S11 actual field/reference reads and Bool selection; eight tag-dispatch compare overcharge. |
| 71 storedBlock_value | S11 exact value identity for arbitrary stored record. |
| 80 decode | S10/S11 executable explicit bondEquiv, eight charged comparisons for EACH index. |
| 83 entry | S11 field-record vector read, two decodes, actual block reader. |
| 90 entry_value | S11 record bit selection and exact decoded block value. |
| 98 assemble | S12 nested materialization; finProdFinEquiv.symm column decode; no source-kernel evaluation. |
| 102 assemble_value | S12 exact two-bit-slice table semantics. |
| 109 private tick_le_one | S6/S12 each indicator counter at most one; arithmetic bookkeeping for bounds. |
| 113 storedBlock_cost_le | S11 ≤12 for EACH Op, arbitrary fields and bonds. |
| 122 entry_cost_le | S11 ≤29 for EACH Op. |
| 133 assemble_cost_le | S12 ≤72D² for EACH Op, including nested row/vector storage costs. |
| 151 assemble_total_cost_le | S12 sum of eight counters ≤576D², not a bit-runtime bound. |
| 161 SourceCorrect | S13 seven SOURCE supplier clauses, all field equalities expanded; injection Full guards/disabled zeros essential. k,n,t natural, L real and bit∈Fin2; NO L>0 or t≤n premise on this total algebraic predicate. |
| 185 blockView_source | S13/S14 conditionally equal hermiteKernel at r=n-t; all bonds. Output equality not inserted among SourceCorrect fields. |
| 196 assemble_source | S14 BOTH records supplied with all seven conditions; actual returned table equals explicit-layout kernel for every a,out. Positivity/legal stage is not added to the equality theorem; interpretation as a physical source stage retains the usual L>0,t≤n convention. |

## Binders, definitions, and provider evidence

Pure carrier data (real scalars, natural orders, list/vector/index types and
decidability needed to select a branch) are TYPING. Analytic differentiability,
jet agreements, polynomial degree promises, L positivity, search invariants,
the five cache equalities, legal-word inequalities, and seven SourceCorrect
clauses are substantive SOURCE hypotheses of the respective *conditional*
statements, not TYPING. No RULED correction or EXCESS premise is introduced by
this natural source. This is an author classification, not an independent seal.

Polynomial jets/degree are supplied by HermitePolynomial and applied within
the smoothness/transfer proofs. Full guarded injection equality is a condition
only for the stored supplier interface, not newly presumed for the actual
polynomial or whole-chain algorithm. The source does not move derivative,
cutoff, coordinate, block equality or pair-value conclusions into hypotheses.

All five modules' definitions are literal formulas/data/procedures. The
polynomial provider has an explicit finite coefficient construction; the
uniqueness characterization used in S1 is a derived property, not an unchecked
choice. S13's Bernstein coefficients are explicitly expanded by a finite sum;
its equivalent characterization is ordinary polynomial-basis uniqueness.
There is no quotient/representative object in these five modules. Total real
division and natural saturated subtraction are retained outside the legal locus;
no invented fallback semantics or fake uniqueness is introduced.

Required provider expansions actually read: the full HermitePolynomial;
HermiteBoundaryInjection sections for Full/Outside/Partial, affinePoint,
selectedChild, blockInjectionRow, sharedCore, boundarySchedule, scalarCore,
leftFree/leftInject, gridStep/gridPointNat/cutIndex, rightFree/rightCore,
left/middle/right kernels and direct-sum bond; HermiteBernstein coefficient,
de Casteljau and restriction definitions; StoredGivens Op/Run/bind/charge,
field/read/collect/materialize; StoredBinaryCoordinates Point/parent contracts;
StoredHermiteGeometry TailLevel/cache widths; StoredThinLQ.entry and cost;
StoredTensorTrain StoredCore/denoteCore; HermiteExplicitBond bondEquiv/kernel.
Some larger provider files were read partially only; they are context, NOT
newly whole-module audited by this packet.

The dependency `Mathlib/Logic/Equiv/Fin/Basic.lean` was read at finSuccEquiv',
finSuccEquiv, finSumFinEquiv, finProdFinEquiv. In particular optional none is
index zero and product flattening is out+D*bit, corroborating S10/S12. The
six-test decoder inspection/overcharge is not an extracted runtime theorem;
the formal Run decoder charge is exactly eight comparisons by definition.

Genuine authored mathematical reuse (no reviewer artifacts):
`docs/hermite-polynomial-proof.md` supplies finite coefficient/jet/gluing prose;
`docs/lessons/hermite-affine-cut-separation.md` supplies strict natural-ceiling
and endpoint conventions; `docs/hermite-state-preparation.tex` supplies the
same polynomial formula and finite-order smoothness explanation. Their broader
state/circuit claims are not imported into this source. No frozen old source
was modified. The cubic C^1-versus-C^2 issue mentioned in existing exposition
is outside this new five-module contract and is not a new claimed discovery.

## Author diagnosis and recommended bounded review

No substantive false proposition in these five actual modules was found during
this read-only authoring pass; this is not an independent acceptance verdict.
Do not interpret lack of a local build/API environment as REFUTED mathematics.

One unified dependency source is coherent, with two bounded review lanes:
A=S1–S4 (polynomial/regularity and formula translation), B=S5–S14 (exact cut,
conditional cached geometry, conditional stored block assembly). They share
P_k, degree and endpoint conventions but do not form one claimed algorithm.
The stored Bernstein block route is not a consequence of the monomial transfer
theorem without an explicit representation bridge. All five whole modules stay
in scope even if independent reading is split across the two lanes.

Next dependency-ready work: independent source-first mathematics reading from
`source-only.md` alone, then independently bound formal round trip, supplier
composition and finite-bit/sourceproducer work. Publication metadata, graph
edits, production Lean, canonical promotion, build gates, and Exposition Seal
are deliberately not attempted here.
