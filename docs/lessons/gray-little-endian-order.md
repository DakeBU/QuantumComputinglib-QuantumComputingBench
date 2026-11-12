# Gray order on little endian bit registers

Gray order lists bit strings so that successive labels differ at exactly one wire. This local mathematical convention supplies the coordinate ordering used by the compiler; it does not itself build a physical circuit or give its cost. The order below includes the empty register and fixes wire zero as the least significant bit.

## Bits and labels

For a natural width \(n\), a bit register is a function
\(x:\{0,\ldots,n-1\}\to\{0,1\}\). Its label belongs to
\(\{0,\ldots,2^n-1\}\). Flipping wire \(t\) replaces \(x_t\) by \(1-x_t\)
and leaves every other wire unchanged. Write this function as \(X_t x\);
the notation describes a bit function, not an operator certificate.

Define \(G_0(0)\) to be the unique empty bit function. For width \(n+1\),
write the label uniquely as \(i=2q+b\), where \(0\leq q<2^n\) and
\(b\in\{0,1\}\), and define

\[
G_{n+1}(2q+b)_0=b\mathbin{\mathrm{xor}}(q\bmod2),
\qquad
G_{n+1}(2q+b)_{t+1}=G_n(q)_t.
\]

Here xor means addition modulo two. The inverse is equally explicit:
recover \(q\) from the tail through \(G_n^{-1}\), set
\(b=x_0\mathbin{\mathrm{xor}}(q\bmod2)\), and return \(2q+b\).
Thus \(G_n\) is a bijection at every natural width. At width zero there is
one legal label, not an empty label set.

At width two the ordinary little endian integer coordinates of the outputs
are \(0,1,3,2\); at width three they are \(0,1,3,2,6,7,5,4\). These are
illustrations of the recursion, not the basis of the arbitrary-width proof.

## The parity twist

The auxiliary twist acts on a pair \((q,b)\) by
\[
T_n(q,b)=(q,b\mathbin{\mathrm{xor}}(q\bmod2)).
\]
It preserves \(q\) and is its own inverse, since flipping twice restores the
bit. Splitting a label into quotient and remainder, applying \(T_n\),
applying the tail bijection \(G_n\), and joining head and tail therefore
gives the bijection \(G_{n+1}\). This proof does not require distinct bits,
a nonzero width or a rank assumption.

For any natural integer \(i\), define the auxiliary head formula
\[
h(i)=(i\bmod2)\mathbin{\mathrm{xor}}(\lfloor i/2\rfloor\bmod2).
\]
For a legal width-\(n+1\) label this is precisely the head wire of \(G_{n+1}\);
its tail is \(G_n(\lfloor i/2\rfloor)\).
The head formula is defined for all natural \(i\), including integers outside
a particular finite register's label range. This extension concerns the
arithmetic formula only, not an off-range Gray register.

## Why adjacent labels change one wire

If \(i\) is even, its quotient by two does not change when one is added.
Its remainder changes from zero to one. Therefore
\(h(i+1)=1-h(i)\), while every tail bit remains unchanged.
The changed wire is wire zero.

If \(i\) is odd, write \(i=2q+1\). The next integer is \(2(q+1)\).
The quotient parity toggles as the remainder changes from one to zero,
so these changes cancel in xor:
\[
h(i+1)=h(i).
\]
The tail labels are now adjacent. By the induction hypothesis exactly one
tail wire changes; shifting that wire by one gives the changed physical
coordinate of the whole register.

Consequently, for every width \(n\) and legal labels \(a,b<2^n\) with
\(b=a+1\), there exists \(t<n\) such that
\[
G_n(b)=X_tG_n(a).
\]
Since a binary bit is never equal to its flip, this equality means exactly
one coordinate changes, not merely at most one. At width zero there are no
adjacent legal labels, so this statement has no exceptional fallback.

The finite bounds matter: the theorem does not assert adjacency between
\(2^n-1\) and zero. It does not identify the changed wire with a chosen
closed-form target algorithm; such an algorithm needs its own refinement
proof.

## Source construction and formal coverage

This is a retrospective local contract for the existing Gray coordinate
module, not a claim to have originated Gray coding or to have assimilated an
external paper. The mathematical proof uses quotient and remainder,
the parity involution, the recursive bijection and the two parity cases
for adjacency.

The complete bounded formal scope is:

- \(\mathtt{twist}\): the involution \(T_n\).
- \(\mathtt{equiv}\): the recursively defined bijection \(G_n\).
- \(\mathtt{headBit}\): the natural-number arithmetic function \(h\).
- \(\mathtt{equiv\_head}\) and \(\mathtt{equiv\_tail}\): the displayed recursion.
- \(\mathtt{headBit\_even}\) and \(\mathtt{headBit\_odd}\): the two displayed
  head transitions.
- \(\mathtt{adjacent}\): the arbitrary-width one-wire change conclusion.

The shared little endian bit carrier and wire-flip convention are
prerequisites. An imported module is not evidence that every Gray declaration
uses every theorem in that module.

## Four views and their limits

The source construction is the recursion and parity induction above.
The Lean view consists of the actual module, its eight public declarations
and their formal providers. A source proof step is not automatically an
elaborated Lean dependency.

The compressed mechanism is a parity twist on head and recursive tail,
followed by one-wire adjacency. Expanding it recovers the formulas and
both parity proof branches without hiding bounds.

A proposed conceptual transport relates integer Gray labels to named-wire
bit functions while retaining width and wire order. It is not a certified
categorical functor, a resource transport, or a matrix/circuit implication.

No state normalization, phase, oracle, ancilla cleanup, approximate accuracy,
postselection, gate count, depth, classical runtime, bit complexity or saved
exporter action is certified by this coordinate module. Those conclusions
require downstream contracts and proofs.
