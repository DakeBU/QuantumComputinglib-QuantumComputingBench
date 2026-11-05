# Little endian basis indexing

Wire zero carries the least significant bit. This convention connects named
qubit states to flat matrix coordinates without reversing registers silently.
The statements below describe the whole existing PrimitiveBasisLE module as a
retrospective local contract. They do not certify an exporter, circuit action,
running time, or a new mathematical construction.

## Bits and integer coordinates

For a nonnegative integer \(q\), a basis state is a function
\(b:\{0,\ldots,q-1\}\to\{0,1\}\). Its integer coordinate belongs to
\(\{0,\ldots,2^q-1\}\). Define the conversion recursively by
\[
E_0(b)=0,\qquad
E_{q+1}(b)=b_0+2E_q(b_1,\ldots,b_q).
\]
This is a bijection, including the empty register: there is one empty bit
function and one coordinate zero. At the successor step, the least bit is
\(j\bmod2\) and the remaining coordinate is \(\lfloor j/2\rfloor\).
The remainder lies in \(\{0,1\}\), the quotient lies in
\(\{0,\ldots,2^q-1\}\), and division with remainder reconstructs \(j\).
Together with the previous bijection, these operations are inverse to the
displayed recursion.

Unrolling six steps gives
\[
E_6(b)=b_0+2b_1+4b_2+8b_3+16b_4+32b_5.
\]
Every one of the 64 bit assignments is in scope. No statement about numerical
amplitudes or a physical six-qubit circuit follows just from this coordinate
formula.

The formal equivalence is `QuantumBlockEncoding.primitiveBasisLEEquiv`.
Its zero, successor and six-wire equations are
`primitiveBasisLEEquiv_zero_apply`, `primitiveBasisLEEquiv_succ_value` and
`primitiveBasisLEEquiv_six_value` in that namespace. The proof builds a
bijection by separating the head bit, recursively converting the tail, and
using the finite product equivalence. Product order is significant: the tail
coordinate precedes the head bit, so the product index is twice the tail plus
the head, not \(2^q\) times the head plus the tail.

## Two wire inverse coordinates

For \(0\le j<4\), write
\[
B_2(j)_0=j\bmod2,\qquad
B_2(j)_1=\lfloor j/2\rfloor\bmod2.
\]
Then \(B_2=E_2^{-1}\). Both coordinate formulas remain exact when the
coordinate carrier is written as \(\mathrm{Fin}(2^2)\) rather than
\(\mathrm{Fin}(4)\). They describe the same carrier, not a new encoding.
In wire order \((0,1)\), the complete inverse table is
\[
0\mapsto(0,0),\quad1\mapsto(1,0),\quad
2\mapsto(0,1),\quad3\mapsto(1,1).
\]
The table verifies both the whole inverse and each coordinate equation. The
individual concrete inverse lemmas name these four cases explicitly; none
introduces an additional assumption.

Formal nodes: `primitiveBits2LE`, `primitiveBasisLEEquiv_two_symm`, its
`wire_zero` and `wire_one` variants, and its four suffixes `_0` through `_3`.
All theorem names carry the `QuantumBlockEncoding` namespace.

## Three wire inverse coordinates

For \(0\le j<8\), put
\[
B_3(j)_0=j\bmod2,\quad
B_3(j)_1=\lfloor j/2\rfloor\bmod2,\quad
B_3(j)_2=\lfloor j/4\rfloor\bmod2.
\]
This equals \(E_3^{-1}\), also on the carrier written as
\(\mathrm{Fin}(2^3)\). The complete table in wire order \((0,1,2)\) is
\[
\begin{array}{c|cccccccc}
j&0&1&2&3&4&5&6&7\\
B_3(j)&000&100&010&110&001&101&011&111.
\end{array}
\]
These strings list wire zero first; they are not conventional high-bit-first
binary numerals. Substitution of each index proves the inverse, the three
coordinate formulas and all eight concrete inverse cases.

Formal nodes: `primitiveBits3LE`, `primitiveBasisLEEquiv_three_symm`, its
`wire_zero`, `wire_one`, `wire_two` variants, and its eight suffixes `_0`
through `_7`.

## Context after deleting a target wire

Splitting a basis state at a target \(t\) returns its target bit and the
function restricted to the other named wires. Equality of the second components
means exactly that the two states agree on every non-target wire. It does not
require their target bits to agree.

For two wires, a one-bit code for the remaining context is
\[
C_{2,t}(j)=
\begin{cases}
\lfloor j/2\rfloor,&t=0,\\
j\bmod2,&t=1.
\end{cases}
\]
The quotient needs no extra modulo because \(j<4\). Two restricted bit
functions are equal if and only if these codes are equal: each code is exactly
the single retained bit. The same equation holds when inverse coordinates are
obtained through \(E_2^{-1}\) on the grid-sized carrier.

For three wires, retain the remaining wires in increasing order and use
\[
C_{3,t}(j)=
\begin{cases}
\lfloor j/2\rfloor,&t=0,\\
j\bmod2+2\lfloor j/4\rfloor,&t=1,\\
j\bmod4,&t=2.
\end{cases}
\]
For \(t=0\), the code contains bits 1 and 2. For \(t=1\), it contains
bits 0 and 2, with bit 2 weighted by two. For \(t=2\), it contains bits
0 and 1. In each case the code is the bijective two-bit little-endian encoding
of the restricted function. Thus two contexts are equal exactly when their
codes are equal. The same statement holds on the grid-sized carrier. In
particular, deleting the middle wire does not leave the high bit weighted by
four; that would be a different context code.

The four code definitions are `primitiveBits2LEWithout`,
`primitiveBits2LEGridWithout`, `primitiveBits3LEWithout` and
`primitiveBits3LEGridWithout`. Their equality certificates are
`splitPrimitiveWire_primitiveBits2LE_context_eq`,
`splitPrimitiveWire_primitiveBasisLEEquiv_two_symm_context_eq`,
`splitPrimitiveWire_primitiveBits3LE_context_eq` and
`splitPrimitiveWire_primitiveBasisLEEquiv_three_symm_context_eq`.
The restriction operation is the shared `splitPrimitiveWire`, not another
register semantics.

## Scope and formal evidence

The authoritative formal source is
[PrimitiveBasisLE.lean](../../QuantumBlockEncoding/PrimitiveBasisLE.lean).
It imports the shared primitive semantics. The general equivalence and its
recursive equation are structural Lean constructions; the fixed-width
identities use finite evaluation, including `native_decide`. Their trusted
evaluation dependencies must be retained in the independent axiom audit, not
described as a proof using only three foundational axioms without checking.

All inputs above are finite bit functions, bounded indices and legal targets.
There are no norm, phase, measurement, probability, oracle or cleanliness
assumptions. Coordinate relabelling alone is not a physical transformation;
no matrix conjugation, gate synthesis, arbitrary-width context deletion,
finite-bit runtime or executable exporter is certified here. Those consumers
need their own semantic and resource bridges. Whole-module admission remains
in the existing publication registry; an authored lesson is not independent
review or reader purification.
