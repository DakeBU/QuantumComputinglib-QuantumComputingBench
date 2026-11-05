Finite real tensor trains: canonicalization, local embeddings, and Gram norms

This is a retrospective local mathematical source assembled from existing local exposition. The historical formalizer is not identified. It is not a pre-proof record, an external-paper reproduction, or a novelty claim. Existence, local matrix semantics, and syntactic real-arithmetic budgets are distinguished throughout.

S1. Finite carriers and contractions

For a natural number d, write [d]={0,...,d-1}; [0] is empty. Fix natural bond dimensions d_0,...,d_n, including zero dimensions. A real core at site i has entries A_i(a,b,j), where a is in [d_i], b is in {0,1}, and j is in [d_(i+1)]. Its bit slice A_i(b) is a d_i by d_(i+1) matrix. Equivalently the core is a matrix with left-bond rows and (bit,right-bond) columns.

The word carrier is recursive: W_0 has one empty word, and W_(n+1)={0,1} x W_n. Its finite enumeration is obtained from the singleton enumeration and the finite product enumeration. This supplies finite sums over words at every length; no separate cardinality theorem is needed here. The first core emits the first recursive word bit.

A chain C of length n with initial bond l and terminal bond r contracts at a word x to an l by r matrix M_C(x). An empty chain has l=r and M_C(empty)=I_r. If C has first core A and tail T, then

  M_C(b,y)=A(b) M_T(y).

These definitions retain all initial rows and all terminal columns. They do not identify recursive word order with a physical integer or reverse any bit order. A chain is right-canonical when every flattened core Q satisfies Q Q^T=I on its left bond. The empty chain is right-canonical. Let B(C) be the maximum of all its bond dimensions, including both boundaries.

S2. Absorption and finite thin factorization

If A has left bond l and right bond m and S is an m by s matrix, absorb S into A by

  A'(a,b,c)=sum_(j in [m]) A(a,b,j) S(j,c).

For each bit, A'(b)=A(b)S; this is matrix multiplication, not a change of emitted bit.

For every real l by (2r) matrix A, there exist R of size l by s and Q of size s by (2r), where s=min(l,2r), such that

  A=R Q,                 Q Q^T=I_s.

One may obtain this thin LQ factorization by extending an orthonormal basis of the row span to s orthonormal rows and expressing the original rows in those coordinates. When l exceeds 2r, taking R=A and Q=I_(2r) gives the required shape. No full-rank assumption is made. The number s is the specified carrier dimension, not numerical rank: a zero input need not have zero-dimensional Q.

For a core, flatten the column pair by e(b,j)=br+j, factor the resulting matrix, and relabel Q back along this bijection. When r=0 both column carriers are empty, so no inverse address is evaluated on an inhabitant. Finite-sum transport along e preserves both the factorization and row inner products. This is an existence construction; it does not specify a deterministic factor-selection algorithm or its cost.

S3. Tail-first canonicalization and full boundary mass

Every chain C with bonds d_0,...,d_n admits a right-canonical chain D with the same length and terminal bond, and a real residual matrix R, such that

  M_C(x)=R M_D(x)                 for every x in W_n.

The new bond dimensions s_i satisfy

  s_n=d_n,              s_i=min(d_i,2s_(i+1)) for i<n.

Call two chains rank-related when their tails are paired recursively with this dimension rule, starting from the same empty terminal chain. The rule puts no conditions on their numerical core entries. For every such pair, a nonempty new head dimension is at most its old dimension and at most twice the next new tail dimension. For a length-one pair ending at bond dimension one, the new initial bond is at most two. Every new bond is bounded by its old counterpart, and B(D)<=B(C). These bounds follow from the dimension relation alone, without assuming factorization or canonicality. The canonicalization above produces such a rank-related pair as well as its factorization and canonicality.

Proof proceeds from the tail. In the empty case take R=I_r and leave the chain unchanged. If the tail factors as M_T(y)=S M_E(y), factor the absorbed core A' as RQ. For each bit b,

  A(b) M_T(y)=A(b)S M_E(y)=A'(b)M_E(y)
             =R Q(b)M_E(y)=R M_D(b,y).

The new first core has orthonormal rows and the tail already is right-canonical. The dimension recurrence follows from the thin factorization at precisely this absorbed core. It allows zero bonds and rank-deficient cores without exceptional replacement values.

For any vector z on a finite set, put mass(z)=sum_j z_j^2. For a row vector v on the initial bond define the complete chain mass

  Phi_C(v)=sum_(x in W_n) sum_(j in [r]) (v M_C(x))_j^2.

More generally, a real matrix Q on arbitrary finite row and column index sets with Q Q^T=I preserves row-vector mass: mass(vQ)=mass(v). Indeed (vQ)(vQ)^T=v Q Q^T v^T=vv^T. Applying this at the first core and summing over its two bit values proves, by induction, Phi_D(v)=mass(v) for every right-canonical D. The empty case uses the single empty word and I_r.

Combining this identity with the factorization gives

  Phi_C(v)=Phi_D(vR)=mass(vR).

The identity holds for any C,D,R satisfying the all-word factorization with D right-canonical; it does not depend on a particular choice of factors. Every terminal label is included. If the terminal bond is one and Phi_C(v)=1, the canonicalized residual boundary vR is normalized. For a chain with both boundaries one, taking the initial scalar vector (1) produces a real vector u and a right-canonical D satisfying

  mass(u)=1,          M_C(x)_(0,0)=sum_a u_a M_D(x)_(a,0),

provided sum_x M_C(x)_(0,0)^2=1. The amplitude equality comes from the produced factorization, not an assumed equality to a desired target. Signed amplitudes are preserved exactly. No mass is obtained by postselection or by discarding terminal labels.

S4. Real cores as complex input-column isometries

For a real core A with left bond l and right bond r, form the complex matrix V with output row (b,j) and input column a by

  V_((b,j),a)=A(a,b,j),

using the real-to-complex embedding. This reverses the matrix row/column roles relative to the flattened real core; the output bit remains part of the output row. If A A^T=I_l, then V^* V=I_l, where the superscript * denotes conjugate transpose. Its (a,c) entry is the sum over both bits and all right-bond labels of A(a,b,j)A(c,b,j), hence delta_(a,c). Real entries are essential to this use of transpose before embedding.

When the two bond dimensions agree, this matrix directly specifies the clean-input columns of a local square stage on a fresh bit and a bond. To state the local action precisely, let U be a complex square matrix indexed by {0,1} x [r], and suppose

  U_((b,j),(0,a))=V_((b,j),a)       for all b,j,a.

The other columns of U are not specified. For previous amplitudes v(p,a), adjoin a fresh zero bit, apply U while leaving the previous bit prefix passive, and append the new bit at the highest wire. If x is a physical bit string of length k+1, let x^- be its first k bits and let x_k be its last bit. The resulting amplitude at (x,j) is

  sum_a A(a,x_k,j) v(x^-,a).

The formula follows by expanding matrix-vector multiplication: equality of passive prefixes and the fresh-bit-zero condition collapse the other sums. No unitarity assumption is required for this algebraic identity, and no unitary completion or primitive circuit is constructed by it. Identifying these physical wire coordinates with an entire recursively ordered word chain requires a separate ordering/composition bridge.

S5. Zero-filled active bonds and padded local columns

For z on [d] and a physical carrier [B], define P_d^B z on [B] to be z_b when b<d and zero otherwise. If d<=B, the injection of an active label preserves its numeric value, P_d^B z agrees with z on every active label, and for every complex function f on [B],

  sum_(b in [B]) f(b) (P_d^B z)_b
    =sum_(a in [d]) f(a) z_a.

The proof separates the active prefix and uses zero for every inactive summand. Without d<=B the same table is only restriction to the physical labels and is not asserted to be a lossless embedding.

For a core A of dimensions l,r, define the padded coefficient table on output rows (b,j) in {0,1} x [B] and input labels a in [B] by

  Vtilde_((b,j),a)=A(a,b,j) if a<l and j<r, and 0 otherwise.

In particular all output labels j>=r have zero coefficient. Assume l<=B, and let a local square matrix U have exactly these entries on fresh-zero, active input columns: U_((b,j),(0,a))=Vtilde_((b,j),a) for every active a<l and every physical output (b,j). Other columns of U remain free; the zeros of the coefficient table do not impose zeros on all unused completion columns of U.

Embed previous amplitudes v(p,a) into [B] by P_l^B. The local action is then exactly

  (P_r^B w(x))_j,       w(x)_c=sum_(a in [l]) A(a,x_k,c) v(x^-,a).

This equality is valid with only l<=B. If r>B it states equality on the available physical output labels, not lossless transmission of the whole right bond. The proof uses the active-prefix sum identity and then separates j<r from j>=r.

If also r<=B and A A^T=I_l, the active padded columns are orthonormal:

  sum_(b in {0,1},j in [B]) conjugate(Vtilde_((b,j),a))
                            Vtilde_((b,j),c)=delta_(a,c).

The inactive output tail contributes zero, so the sum reduces to the unpadded isometry in S4. This result is about the specified active columns. Completing them to a whole unitary, choosing physical ancillas, and proving a complete multi-stage circuit remain separate tasks.

S6. Complete right Gram environments

For an arbitrary real chain, not necessarily right-canonical, define its right environment recursively by

  E_empty=I_r,          E_(A::T)=sum_(b=0,1) A(b) E_T A(b)^T.

Then

  E_C=sum_(x in W_n) M_C(x) M_C(x)^T.

For the empty chain the right side has the single term I_r I_r^T=I_r. In the inductive step expand by the first bit, substitute the tail identity, and distribute multiplication over the finite sum. The identity (AB)^T=B^T A^T fixes the multiplication order. Each matrix product sums all terminal labels; this is not a selected terminal sector.

For scalar boundaries l=r=1, the entry E_C(0,0) equals sum_x M_C(x)_(0,0)^2 and is nonnegative. Define

  N(C)=sqrt(E_C(0,0)).

Thus N(C) equals the square root of the complete amplitude square sum, its square equals that sum, and N(C)>0 whenever some amplitude is nonzero. Zero trains do not require a special fallback or a nonzero premise. The empty scalar-boundary chain has norm one.

If I is any finite index set, e:W_n -> I is a bijection, and M_C(x)_(0,0)=f(e(x)) for every word, transporting the finite sum gives

  N(C)=sqrt(sum_(i in I) f(i)^2).

The pointwise action, not an assumed norm-correctness result, supplies this target adapter. This is a real Euclidean norm statement, not a complex-core or physical state-preparation certificate.

S7. Symbolic storage and dense real-arithmetic schedule

If every intermediate environment is retained as a dense table, the number of scalar entries is defined by H(empty)=r^2 and H(A::T)=l^2+H(T), with l the current left bond. If B(C)<=D, each of the n+1 environments has at most D^2 entries, hence

  H(C)<=(n+1)D^2.

This counts specified entries, not actual allocation or peak live memory of a running program.

For one update with left bond l and right bond m, consider two dense matrix products for each bit: an (l by m)(m by m) product, followed by an (l by m)(m by l) product. Charge one multiplication and at most one addition for each inner-product term, then l^2 additions to combine the two bit contributions. The resulting syntactic real-operation budget is

  T(l,m)=4(l m^2+l^2 m)+l^2.

Define F(empty)=0 and F(A::T)=T(l,m)+F(T). For l,m<=D, both cubic products are at most D^3. If D>=1 then l^2<=D^3, so T(l,m)<=9D^3. If D=0, l=m=0 and the same bound is immediate. Induction over the n sites yields

  F(C)<=9nD^3.

The constant 9 is a bound coefficient, not a count of operation-counter categories. These definitions do not charge stored-input reads/writes, cache traversal, integer operations, square roots, angle evaluation, or emitted instructions. In particular the final scalar square root in S6 is not part of F. The terminal identity has zero budget by this stated syntactic convention. No eight-counter stored-operation model is substituted for this budget.

S8. Exact scope and remaining constructions

All displayed identities are exact finite mathematics with arbitrary real core entries, allowing empty and zero-dimensional carriers, deficient ranks, and signed amplitudes. No input generation or constant-time evaluation model for arbitrary core functions is supplied. Syntactic arithmetic and entry counts do not establish deterministic runtime, finite-bit error, numerical stability, actual caching, or physical space usage.

The local column conditions in S4-S5 are explicit conditional interfaces, not produced gate implementations. A physical consumer still needs a matching word/wire convention, a realized local unitary completion, composition through actual gates, ancilla/terminal cleanup, and suitable finite-angle/error/resource analysis. Those tasks are not consequences of a Gram norm identity or of the mere existence of a canonical factorization. No oracle construction, success probability, gate count, depth, connectivity, postselection benefit, or complete scientific state-preparation result is claimed here.
