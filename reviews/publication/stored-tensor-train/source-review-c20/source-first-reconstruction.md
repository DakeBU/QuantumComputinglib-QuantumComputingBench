# Independent source-first reconstruction, c20

This record was written before opening the implementation, decoder packet,
decoder artifact, decoder evidence or publication candidate. The source is the
retrospective local lesson `docs/lessons/stored-tensor-train-canonicalization.md`,
SHA256 `9d1dd65a177d485c37240cba0b269c530ec3fdb615be0d103f81e5ae14abd9c0`.
This is a review-time seal, not a historical pre-proof Statement Seal.

For natural bonds d_0,...,d_n, including zero, each already stored real core
has shape d_i by 2*d_(i+1), with column b*d_(i+1)+j. A recursively ordered
word is emitted head first. The empty contraction is the terminal identity.
All terminal bond labels are retained: there is no clean-sector projection.

The deterministic backward procedure first canonicalizes the tail, absorbs
its stored residual S into the head by B(a,b,j)=sum_u A(a,b,u)*S(u,j), stores
all resulting entries, and applies the deterministic stored thin-LQ supplier
to B. It returns R and prepends the returned Q. Every flattened Q has
orthonormal rows across both bits and all right labels. The new row dimension
is min(l,2r), not the numerical rank. Deficient rank and zero pivots must not
introduce positivity or full-rank hypotheses.

Slice factorization and associativity give M_C(x)=R*M_E(x) for every word.
Erasing storage must give the exact deterministic semantic returned values,
not just an existence theorem or gauge-equivalent train. The initial boundary
v becomes w=vR. Right-canonicality yields full all-word/all-terminal mass
equal to sum_j w_j^2. Only the normalization consumer assumes mass one.

The eight counters are field operations, square roots, angles, trigonometric
calls, exact comparisons, reads, writes and emitted records. Each summand
charges four stored reads and two field operations, including addition to
zero. The two-pass entry and outer-row materialization contributes
(l*2r+l)*(two reads+two writes). Thus absorption total is
12*l*m*r+8*l*r+4*l. Thin LQ contributes at most
164D^3+108D^2+25D+2 for l,r<=D; recursion nodes charge six reads/writes
in total. The identity base is 5r^2+4r+6. Induction gives the whole-run
bound n*(176D^3+116D^2+29D+8)+5D^2+4D+6 when all input bonds are <=D.

This cost is for the actual stored exact-real producer. Input generation,
finite precision, stability, rational/integer bit lengths, allocation, peak
memory, gate count, physical basis/endian identification and terminal cleanup
are not supplied. A conceptual preparation transport remains an AND-tail of
normalization, physical embedding, isometry completion, finite-angle synthesis
and full terminal cleanup. No Hermite root, resource-winner or purification
approval follows.

The sealed JSON records an exhaustive section-level disposition, displayed
formulas, binder classes and source topology. Its approval is not claimed by
its author; the parent must independently inspect it before publication.
