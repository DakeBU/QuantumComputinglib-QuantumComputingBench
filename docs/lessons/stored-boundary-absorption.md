# Boundary absorption from stored matrix tables

Small matrix products become a scalar-boundary tensor train without building
a table of all bit strings. When the local matrices and boundary vectors are
already stored, boundary absorption can also carry an explicit operation
count for the very same returned chain. This count measures exact-real
arithmetic and stored-word traffic, not finite-bit machine time.

## Stored inputs and coefficient order

Fix natural numbers D, n and s, with positive word length N=n+1. Each stored
core A_i has D rows and 2D columns. Its column index represents a pair
(b,j), with b in {0,1} and j in Fin D, through finProdFinEquiv. Thus its
denotation is the real array A_i(a,(b,j)). The left and right boundaries
l,r are stored real vectors of length D.

A semantic kernel K(t,b) has D by D real slices. The finite-window condition
is precisely

\[
 A_i(a,(b,j))=K(s+i,b)_{a,j}
 \quad(0\le i<N).
\]

Only this stored window is constrained. K is specification data: the
producer never calls it, and no condition on positions outside the window is
needed. The desired coefficient is

\[
 a(x)=l^T K(s,x_0)K(s+1,x_1)\cdots K(s+N-1,x_{N-1})r.
\]

All data may be signed, singular or zero; D=0 is allowed. There is no
normalization, positivity, rank or successful-preparation premise.

## Returned chain and exact value

For the last core, compute each entry of the D by 2 output table from
already stored values:

\[
 T(a,(b,0))=\sum_{j<D} A_{N-1}(a,(b,j))r_j.
\]

Earlier cores retain their stored tables. Recursively, read the first table,
collect references to the remaining tables, construct the tail, and allocate
the first chain node. At the terminal step, read the final table, materialize
T, and allocate its core and empty-tail nodes. No all-word amplitude
expansion occurs.

Then absorb the left boundary into the first core B:

\[
 B(0,(b,j))=\sum_{a<D} l_a A(a,(b,j)).
\]

Materialize B and allocate its new first chain node; retain the already
constructed tail. For N=1 this initial operation acts on the newly
materialized terminal core, so both boundaries enter the same scalar core.

Finite-sum evaluation proves both displayed formulas for the actual returned
tables. Induction on n shows that the stored tail denotes the mathematical
right-boundary chain: its first core agrees by the window condition, and the
remaining window starts at s+1. The collected tail references denote exactly
the original entries at indices i+1. Left absorption then agrees with the
mathematical left-boundary operation. Consequently, if result is this single
stored run, its denoted chain equals the ordered mathematical construction
ofKernel(K,l,r,s,n), and every contracted coefficient equals a(x).

The constructed chain has scalar boundaries and maximum bond at most
max(D,1). This follows from the exact returned-value refinement and the
separate mathematical bond theorem, not from an assumed output property.

## Operation model and materialization

A run returns a value and eight natural-number counters: field operations,
square roots, angle evaluations, trigonometric calls, comparisons, reads,
writes and emitted rotation records. Binding runs adds these counters.
The total below is their sum. Boundary assembly uses only field, read and
write counters; it makes no square-root, angle or circuit-generation calls.

Reading one stored matrix entry costs two reads: one row reference and one
scalar. Reading a boundary entry costs one read. Each term of either boundary
sum therefore costs three reads, one multiplication and one addition,
including the addition to the recursively accumulated sum. An empty sum
returns zero and has zero term cost.

Collecting m outputs charges their callback work plus 2m reads and 2m writes
for the materialized counted values and projected results. Materializing an
u by v nested table therefore has overhead 2(uv+u) reads and the same number
of writes. Scalar callbacks must carry their own charges; a pure semantic
formula is not an uncharged producer.

Let R,W,F denote one read, write and field-operation counter unit. For a
terminal core and an initial core with outgoing dimension r_out, the exact
per-counter expressions are

\[
\begin{aligned}
 C_{\rm terminalEntry}&=D(3R+2F),\\
 C_{\rm initialEntry}&=D(3R+2F),\\
 C_{\rm terminal}&=2D^2(3R+2F)+6D(R+W),\\
 C_{\rm initial}&=2r_{\rm out}D(3R+2F)
                  +(4r_{\rm out}+2)(R+W),\\
 C_{\rm tailTable}&=n(3R+2W).
\end{aligned}
\]

For example, the terminal table has 2D output entries, each with a D-term
sum, and materialization adds the 3D nested-vector overhead. The tailTable
formula includes one callback read and the four collect units per reference;
it copies references, not all scalar entries in the referenced cores.

Summing the eight counters gives the exact totals

\[
 C_{\rm terminal}=10D^2+12D,\qquad
 C_{\rm initial}=10r_{\rm out}D+8r_{\rm out}+4,\qquad
 C_{\rm tailTable}=5n.
\]

## Bound for the same returned run

A chain-node operation costs three reads and three writes. Reading the
first input table costs one read. The terminal tail run thus has total
10D^2+12D+13. Adding an earlier core costs 1+5(n+1)+6 beyond the shorter
tail. Induction, with this recurrence, gives the conservative bound

\[
 C_{\rm tailChain}\le10D^2+12D+5n^2+7n+13.
\]

For the subsequent left absorption, N=1 has outgoing dimension 1; a longer
chain has outgoing dimension D. The exact initial-core formula plus its
new node is in either case bounded by

\[
 C_{\rm closeLeft}\le10D^2+18D+18.
\]

Adding the two costs proves

\[
 C_{\rm ofTable}\le20D^2+30D+5n^2+7n+31.
\]

Value refinement and this cost inequality concern one and the same result.
The cost theorem needs only stored input data; the semantic window is needed
to identify its output with the chosen kernel. An entrywise version of the
window implies the full array equality by extensionality.

D=0 and N=1 remain in the theorem. In particular, the single output scalar
core still materializes its two zero entries; empty inner sums do not mean
that all materialization or node costs disappear.

## Exact Lean correspondence

The whole module is QuantumBlockEncoding.StoredMatrixProductChain.

| Mathematical object or step | Public Lean declarations |
| --- | --- |
| Stored right-boundary sums and table | terminalEntry, terminal |
| Stored left-boundary sums and table | initialEntry, initial |
| Tail reference collection and chain assembly | tailTable, tailChain, closeLeft, ofTable |
| Actual local table and reference values | terminal_value, initial_value, tailTable_value |
| Finite semantic window | Window, window_of_entries |
| Full returned-value refinement | tailChain_value, closeLeft_value, ofTable_refines |
| Exact per-counter costs | terminalEntry_cost, initialEntry_cost, terminal_cost, initial_cost, tailTable_cost |
| Exact total local costs | terminal_total_cost, initial_total_cost, tailTable_total_cost |
| Recursive and whole-run total bounds | tailChain_total_cost_le, closeLeft_tail_total_cost_le, ofTable_total_cost_le |
| Actual returned bond and joint certificate | ofTable_maxBond, ofTable_certified |

## Reuse and limits

The source construction graph has stored terminal materialization, reference
collection, left materialization and returned-value composition, with the
cost recurrence as a separate accounting branch. The Lean graph records
actual module/import ownership. The compressed spine is stored boundary
absorption, with the complete formulas above as its expansion. A conceptual
transport to state preparation still requires normalization, canonicalization,
physical register embedding, cleanup and circuit synthesis as a complete
AND-tail; boundary assembly alone supplies none of those conclusions.

Input tables and boundaries are already materialized. Generating their
entries, indexing/counter bookkeeping, integer or rational bit lengths,
GCD/reduction, precision, stable numerical arithmetic, machine allocation,
peak memory, physical gates and executable runtime are outside this
extended exact-real model. Its polynomial counter bound cannot be relabelled
as polynomial finite-bit preparation time.

This is a retrospective local mathematical contract for an existing module,
not a historical pre-proof seal, external-paper assimilation, novelty claim,
or complete Hermite scientific certificate.
