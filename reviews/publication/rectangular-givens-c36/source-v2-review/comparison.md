# Independent whole-module comparison against source v2

Verdict: source-v2 mathematics, the supplied complete formal target, and the
new source-blind decoder agree for all 19 explicit target declarations and
all six literal definition bodies. This is a semantic comparison acceptance,
not a final publication-binding wrapper or a claim of a fresh Lean build.

The source remains RETROSPECTIVE_IMPLEMENTATION_INFORMED. Phase1 and the
source-v2 natural/minimality seal were completed before any formal exposure.
Source v2: `91c442f1f8002be9d082257fbba0a79d551df3cdda499c6d1a2f539a686e0fd3`.
Formal seal: `e539fa2f2fd0cf48937e218096d01d05d5c446286fc9d33c4bf4edc62490dc60`.
Decoder identity: `/root/rectangular_formal_decoder_c36`.
Reviewer identity: `/root/rectangular_source_first_c36`.

## Actual comparison

Module0's two recurrences use the guard k<N, valid column k, count N-1-k,
and the result of the current one-column sweep as the next input. The trace
prepends that current column's list before the next-column list. The else
branch changes only k and remaining, not A. This is S2 literally, not an
existence certificate or a square-SO algorithm. The domain proof k+remaining<=M
ensures the active column exists. Natural truncated subtraction is safe under
k<N. At k=N-1 the count is zero; N=0 skips all columns; M=0 stops immediately.

Module1's `columnSweep` and `columnSweepSteps` execute the lower pair first
and recurse on `eliminateEntry A ...`, so both inner and outer recurrences
use updated matrices. `Step` stores two Fin N indices, the forward adjacency
equation, and a real angle. Its proof field implies distinctness and adds no
input-matrix constraint. The supplier's zeroing theorem has BOTH lower and
upper interval bounds; its outside theorem and zero-column preservation
theorem match source-v2 S1. Thus F1 is resolved by the actual interface, not
by silently changing the implementation.

Module2 defines `pairNorm` as the square root of the sum of squares and
`splitAngle` using the zero branch and exactly the two signed principal-acos
branches accepted in the sealed natural revision. Module5 evaluates rational
zero to zero and `.real v` to v. Module1 negates that evaluated split angle.
There is no remainder/modulo reduction or pruning rule. Consequently F2 is
resolved even for literal real-angle records. The half-angle rotation body
matches the source and Module3's real two-plane block. The y=0,x<0 branch
is -2pi, not a skipped identity. Neither zero pairs nor rank deficiency add
a precondition to A.

`UpperPrefix` expands to exactly the source's quantified strict-lower-zero
predicate. The one-column proof separates old columns from the newly processed
column, using interval zero preservation and zeroing respectively. The outer
prefix proof has an explicit skip argument deriving the next prefix from
row<N<=k, not from rank. The final zero-below theorem constructs the empty
prefix internally. The final public result does not assume Prefix(A,M).

`stepsMatrix` has cons equation U(rest)*matrix(head), while `applySteps`
executes the head before the rest. This agrees with U=Gs...G1. S2a supplies
actual computed action; the separate provider product/action theorem gives
transform(A)*A=reduced(A). Arbitrary-list orthogonality and determinant use
separate plane facts; neither assumes orthogonality of A. Finally the recovery
proof uses transform_mul AND transform_orthogonal. It does not use a supplied
identity residual, determinant alone, or triangularity alone.

The list bound uses exactly the supplier length theorem, concatenation length,
the induction hypothesis, and natural arithmetic. It does not import the
prefix argument. Zero-angle records are counted. There is no total runtime,
entry access, finite-bit, stability, qubit-polynomial, or gate-count theorem
in this module. Noncomputability is accurately disclosed; it neither proves
nor refutes efficient numerical extraction.

## Seven semantic slots

1. Target/normalization: unrestricted real rectangular A; actual computed
   residual and list; transform is N-by-N. No normalization, uniqueness,
   identity residual or full QR/LQ/thin-isometry certificate is advertised.
2. Dimensions/basis/order: N,M arbitrary naturals, including zero; Fin indices
   are zero-based; adjacent numerical rows; columns increase; rows sweep
   bottom-up; theta/2 convention; chronological last factor on the left.
   There is no physical-qubit, tensor or wire-order identification.
3. Oracle/coherence/inverse/control: no oracle-access premise or coherent
   parameter oracle is used. Matrix data are mathematical inputs. Recovery
   is the explicit transpose identity, not a circuit inverse implementation.
4. Ancillas/workspace/garbage: no quantum registers or cleanup contract exists.
   Matrices are overwritten only through the specified mathematical row
   update; outside rows are fixed. Classical memory/copy cost remains uncharged.
5. Phases/sign: exact signed real entries and rotation parameters are retained;
   no quotient by global or relative phase or row/basis permutation. Negative
   terminal pivots are allowed, and the selected -I axis operation is retained.
6. Error/success/norm: equalities are exact; no tolerance, numerical stability,
   accepted sector, measurement, success probability or amplification result.
   Pair norms are defined internally, not assumed nonzero.
7. Resource tier: exactly the abstract rotation-list length <=N*M. No scalar
   runtime, finite-bit precision, storage bound or primitive quantum resource
   refinement is established, even though some supplied providers also contain
   separate quantum compiler declarations outside the target claim.

## Binder and definition audit

All six target definitions are literal and were compared as full bodies.
`UpperPrefix` is the only target Prop definition; its whole body was expanded.
No project-owned class or Prop bundle hides a rank, circuit or normalization
condition. Concrete dimensions/carriers and finite index bounds are TYPING;
real scalars and chronology are STANDING conventions. The partial range
condition, selected pivot-in-row-range condition, prefix input to preservation,
and final below-diagonal comparison are SOURCE premises of those exact local
claims. Final output theorems have no logical input-matrix premises. There are
no EXCESS or newly RULED matrix assumptions. The versioned source clarification
changes only source precision and has its own independent repair record.

## Decoder and author-metadata comparison

The decoder independently reconstructed the same recurrences, supplier sign,
exact representative, prefix invariant, product convention, general-list
theorems, output chain and boundary cases. Its seven final named statements
agree with the independent source-first conclusions. Its 19-signature/six-body
ledger matches Module0 byte-for-byte at the source-text level. The read-only
`verify_packet.ps1` was inspected and executed: all eight payload hashes and
the binding match, and signature/body, mutation, missing-declaration, and
duplicate-declaration checks pass. This is lexical/integrity evidence, not
kernel elaboration or a proof-term census.

The old author-source-coverage file maps all 19 declaration names correctly,
but its provisional coarse graph is NOT accepted as complete. Its combined
S3b/S6.3 edge loses general-prefix and skip/induction structure. Its S6.5 head
combines orthogonality and determinant but the displayed tail only supplies
plane orthogonality; determinant needs its own plane-determinant tail.
Supplier length and other obligations also need explicit edges. The separate
independent comparison.json supplies lossless corrected tails. This is a
metadata/topology correction, not a change to the Lean theorem or source-v2
matrix contract. The author's `source_line` values denote formal source
lines, not natural-source line numbers; our mapping labels both explicitly.

The old publication candidate is AUTHOR_WIP_NOT_ADMITTED and still contains
v1 source/binding placeholders. It is not the current comparison contract or
accepted evidence. No final v2 prospective binding has been inspected or
adopted in this comparison. Parent-reported later binding identifiers are
coordination metadata only until their actual records are supplied and checked.

## Evidence strength and remaining boundary

All six supplied formal modules were read in full, as well as packet text,
seal/bindings, the relevant context-index fields and decoder's four exact
files. The large ambient digest dictionary is metadata only; no ambient file
content or complete transitive trust base is thereby inspected. Existing
current CI/cache build context is attributed to the parent/decoder evidence:
run 38992000018, job 117276254466 reportedly passed `lake build` and
`lake build Tests` at checkout 21276ccb2c6d5573b534ae5bd5c97b28ede0e13b,
with unchanged target raw bytes aa4b908e26c0e0b0bccc05034b839f170fb4a2641d96b713ff8d3fac731bcb52.
No fresh Lean, network, Git, production or registry writes were made here.
Source-signature reconstruction does not require inventing a demand for all
TCB bodies, proof-value printouts, or a generated-declaration census. Conversely
none of those unobserved outputs is claimed as checked.

Remaining work is exact prospective binding/final decoder-hash verification
and the repository owner's publication, graph integration and purification
gates. The independent semantic comparison itself has no unresolved mismatch.
The author graph must not be promoted unchanged as complete. Phase1 and the
natural-source-v2 seal remain immutable.
