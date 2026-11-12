Finite real tensor trains on explicitly ordered circuit wires

This is retrospective local mathematics assembled from pre-existing local material. The historical formalizer is unknown. It is not an external-paper reconstruction, a pre-proof chronology, a novelty claim, or a finite-precision implementation. Exact existence, actual finite instruction lists, and classical computation of their real parameters are different assertions.

S1. Finite cores, occupied bonds, and local coordinates

Write [d]={0,...,d-1} for a natural dimension d, allowing d=0. A real core A from a left bond l to a right bond r has entries A(a,b,j), with a in [l], b in {0,1}, and j in [r]. Its flattened matrix has left-bond rows and (bit,right-bond) columns. Its fixed-bit slice is A(b). A chain C of N cores has the matrix contraction M_C(w)=A_0(w_0)...A_(N-1)(w_(N-1)); the empty chain at bond r contracts to I_r. Words are head-first: the empty word is unique and a nonempty word is a first bit paired with its tail. All initial and terminal labels are retained.

A chain is right-canonical when each flattened core satisfies A A^T=I on its left bond; the empty chain satisfies the condition. Its maximum bond includes both boundaries. Let r_t be the active dimension before site t; r_0 is the initial dimension, r_N is the terminal dimension, and r_t remains the terminal dimension after the last site. For a fixed physical bond [B], extract at each actual site the coefficient table

  P_t((b,j),a)=A_t(a,b,j) if a<r_t and j<r_(t+1), and 0 otherwise.

Real entries here are also regarded as complex numbers with zero imaginary part. After the last site define P_t=0. Thus the table has zero imaginary part for every time, whether or not the chain is canonical. It vanishes on every output label j>=r_(t+1). At an actual site of a canonical chain whose every bond is at most B, its occupied input columns are orthonormal:

  sum_(b in {0,1},j in [B]) conjugate(P_t((b,j),a)) P_t((b,j),c)
    = delta_(a,c),                  a,c in [r_t].

This follows by discarding the zero output tail and using A_t A_t^T=I. The actual-site restriction t<N is essential: the intentionally zero table after the schedule is not asserted to be an isometry.

A q-wire bond label is a function z:[q]->{0,1}. Its little-endian integer label is L_q(z)=sum_(i<q) 2^i z_i, a bijection onto [2^q]; L_0 is zero on the unique empty label. Put S=2^q. A local stage has q low bond wires and one highest fresh output wire. Its coordinate bijection sends the label obtained by appending bit b to z to (b,L_q(z)) in {0,1} x [S]. In particular the fresh-zero active input positions for a dimension l<=S are the distinct labels corresponding to (0,a), a in [l]. This injection need not be a prefix in some other enumeration of all local basis states.

S2. Prescribed columns and an unused orientation column

Let I be any finite named basis, V a real matrix with rows I and r columns, and e:[r]->I an injection specifying their physical column positions. Assume V^T V=I_r and r<|I|. There exists a real square matrix U on I such that

  U^T U=I,              det U=1,              U(i,e(a))=V(i,a)

for every row i and active a. The last equality preserves entire columns, not only a projected block. To see this, extend the orthonormal columns to an orthonormal basis, keeping them at the distinct prescribed labels. The resulting orthogonal matrix has determinant +1 or -1. If necessary multiply one unused column by -1. This diagonal sign flip is orthogonal with determinant -1, so it fixes the determinant without changing any prescribed column. A strict spare-column inequality guarantees such an unused label. Relabeling a finite basis in both rows and columns preserves the inner products and determinant, so the argument does not require numeric prefix positions.

The completion is generally nonunique; no canonical representative or efficient procedure for choosing it is specified. Without an unused column, determinant correction need not be possible while all columns remain fixed. For example, a completely prescribed determinant-minus-one orthogonal matrix cannot also have determinant plus one. Thus the strict dimension condition is a genuine hypothesis of this completion result.

S3. Exact real special-orthogonal matrices as finite instructions

The single-wire rotation convention is

  RY(theta) = [[cos(theta/2),-sin(theta/2)],
               [sin(theta/2), cos(theta/2)]].

The ambient finite instruction language also allows the single-wire bit flip X and the diagonal rotation RZ(theta)=diag(cos(theta/2)-i sin(theta/2),cos(theta/2)+i sin(theta/2)). Controlled-NOT flips its target when its control bit is one and fixes the control and other wires. A single-wire gate fixes every non-target wire, and control and target are distinct. Finite lists are chronological: later instruction matrices multiply on the left. The empty list denotes identity. Every instruction in this language is unitary, including at arbitrary exact real angles. The special-orthogonal construction below uses only RY and controlled-NOT; the general list/composition identities allow the full stated language.

For a real determinant-one orthogonal matrix on D numeric basis labels, adjacent-row elimination gives D(D-1)/2 ordered two-level rotations, including harmless zero-angle rotations. Each pair sweep annihilates a lower entry using a signed angle that sends the two real entries to their nonnegative Euclidean length and zero; a zero pair uses angle zero. Previously fixed standard-basis columns, orthogonality, and determinant are preserved. Process columns in increasing order with bottom-up adjacent sweeps. The final remaining sign is plus because the determinant is one. Reversing the elimination list and negating its angles therefore realizes the original matrix, not its inverse.

For D=2^(q+1)=2S, order the basis internally by a binary Gray enumeration: consecutive labels differ on one wire. Each adjacent two-level rotation becomes a rotation of that target wire selected by the assignment on all q other wires, fixing every basis vector outside the selected pair. If the first endpoint has target bit one rather than zero, negate the physical rotation angle to preserve the ordered two-level matrix. Transport the input matrix into Gray coordinates and transport the resulting denotation back; the external named-wire basis is unchanged.

A selected rotation with q controls is realized by a recursive rotation/controlled-NOT list, not an opaque multiply controlled primitive. Its two control branches use half-sum and half-difference angle tables, separated and followed by a target flip controlled on the added control wire. The identity X RY(theta) X=RY(-theta) verifies the two branches. Starting with one rotation at q=0, this gives S rotations and 2(S-1) controlled-NOTs, on the existing q+1 wires without extra working wires. Consequently the complete special-orthogonal matrix is realized by an actual list of length

  [D(D-1)/2] [S+2(S-1)] <= 6 S^3.

The bound counts instructions, including zero-angle entries kept by this schedule. There are no oracle-call instructions. It is a gate-list bound with exact real angles, not a bound on computing those angles, reading an arbitrary input matrix, storing intermediate data, or synthesizing rotations over a finite gate alphabet. Gray order is internal bookkeeping, not an extra uncounted physical permutation.

S4. Local circuits produced from canonical cores

Suppose C is right-canonical, its maximum bond is at most S=2^q, and t<N is an actual site. Form the real matrix V whose rows are local q+1-wire labels and whose column a in [r_t] is the real part of P_t at that row's (bit,bond) coordinates and input label a. The table is real, and S1 gives V^T V=I. Its prescribed column position is the fresh-zero label (0,a) in those coordinates.

Since r_t<=S and S>0, there are strictly fewer active columns than the 2S local basis labels. S2 supplies an exact determinant-one orthogonal completion, and S3 supplies an actual rotation/controlled-NOT circuit c_t with at most 6 S^3 instructions and no oracle calls. For every output bit b, output bond label z, and input bond label a whose integer value L_q(a) is active, its matrix entries satisfy

  <z,b|c_t|a,0> = P_t((b,L_q(z)),L_q(a)).

The notation on the left lists q bond bits followed by the highest fresh bit. The equality covers every physical output, but only the occupied fresh-zero input columns. Other input columns of the completion remain free. Here orthogonality, determinant, and the displayed local-column equality are produced, not assumptions about a desired circuit. A shorter form may retain only circuit existence, the instruction bound, and the local-column equations; dropping the no-oracle field from that interface does not change the construction.

This local result includes q=0, where S=1 and the local stage has one wire. It imposes no positive lower bound on q and no full-rank promise on the original, pre-canonical cores. It makes no isometry or compilation claim for the zero schedule entries at t>=N; those times will not be executed.

S5. Absorbing a signed initial boundary

For a real vector u on [l], let B_u be the one-row matrix with B_u(0,a)=u_a. If sum_a u_a^2=1, then B_u B_u^T=I_1. If also A A^T=I_l, matrix associativity gives

  (B_u A)(B_u A)^T = B_u (A A^T) B_u^T = I_1.

The core B_u A keeps the emitted bit and the right bond. For every head-first word, replacing a first core A by B_u A changes the chain contraction to B_u times the previous contraction, with every terminal column retained. This contraction identity requires neither normalization of u nor canonicality of A; those two premises are needed for the row-isometry conclusion above.

Now let C be a nonempty real chain with both boundary dimensions one, maximum bond at most B, and original scalar amplitude square sum one. Tail-first thin factorization supplies a canonical chain E with the same terminal bond, a real initial vector u, and

  sum_a u_a^2=1,             M_C(w)_(0,0)=sum_a u_a M_E(w)_(a,0)

for every word. Its maximum bond is no larger than that of C. This supplier factors each absorbed head with exactly min(old left dimension, twice the new tail dimension) orthonormal rows. The empty recursion returns an identity residual; the nonempty recursion absorbs the tail residual before factoring the head. Row-isometries preserve complete finite squared mass, so the input normalization implies the unit mass of u. It is not an extra free state-initialization assumption.

Because the chain is nonempty, write E=A::T and replace its first core by B_u A. The resulting chain D has both boundary dimensions one, is right-canonical, and has precisely the original scalar amplitude at every word. Its tail bond dimensions are unchanged. The original initial dimension one implies B>=1, so the new initial dimension one also respects the same maximum-bond bound. Signed entries of u are absorbed without taking absolute values, discarding a phase, or selecting a terminal sector.

This is existence with exact real choices. It is not a claim that the completion factors or u can be found within a stated classical runtime. Positivity of the chain length is used exactly to provide a first core into which the boundary can be absorbed.

S6. Empty initialization, finite-label transport, and terminal cleanup

For any q, L_q(z)=0 if and only if all q bits of z are zero. This follows recursively from L_(q+1)(z)=z_0+2 L_q(tail z), including the singleton q=0 case. Thus the vector on the physical bond that is one at integer label zero and zero elsewhere is exactly the all-zero input column of the empty circuit on q wires. Zero-filling the one-entry vector (1) into [S] prepares this same vector with zero instructions; no arbitrary normalized boundary is supplied for free.

Relabeling a finite bond set is algebraic transport, not a physical gate. If e:B->C is a bijection and U_t is a local square complex matrix on bit x C, define its transported matrix by

  U_t^e((b,j),(b',a))=U_t((b,e(j)),(b',e(a))).

Starting from any complex boundary v on B, the run with U_t and boundary v composed with e^(-1), evaluated at (x,c), equals the run with U_t^e and v at (x,e^(-1)(c)). Expand each local matrix-vector product and change its finite summation variable by e. The emitted bit prefix is not permuted by this bond-only transport. Neither unitarity nor a state-action hypothesis is needed for the transport identity.

Let D be any real chain of length N with both boundaries one and maximum bond at most S. Canonicality is not assumed in the following conditional action statement. Supply local circuits c_t for which, at each t<N, the active fresh-zero input columns equal P_t on all physical output rows, as in S4. No equations are required of c_t after the last site. Starting at the all-zero bond and adjoining a fresh zero output bit at each step, the complete sequential amplitude is

  delta_(z,0^q) M_D(w(y))_(0,0).

Here y=(y_0,...,y_(N-1)) lists bits in chronological emission order, w(y) is the head-first word with those same successive bits, and z is the final q-wire bond. At stage t the old prefix stays passive and y_t is appended as its highest new wire.

To prove the statement, the input initially has support only on the active rank one. The extracted core table maps every active input to the next active output rank and has zero coefficient outside it. Inductively, unused completion columns never act on occupied amplitude. Expanding one stage gives the padded real row-vector core contraction. Induction then gives the whole product M_D(w(y)), not a global-action premise. The terminal dimension is one, so its padded output is supported only at integer label zero; S6's zero-label identity turns this into all q bond bits being zero. This is full-state cleanup at every output amplitude, not projection, measurement, or postselection. Normalization is not needed for this conditional algebraic identity.

For N=0 there are no local-column premises and no stages. The only scalar-boundary empty chain contracts to I_1, and the empty circuit leaves the all-zero bond unchanged. This helper case does not justify absorbing an arbitrary signed scalar into a nonexistent first core.

S7. Head-first words, Boolean lists, and public little-endian samples

Map a head-first word to the basis function that puts its first bit at coordinate zero and recursively puts its tail at later coordinates. Conversely, read coordinate zero and recurse on the tail. The empty maps are unique, and induction shows that these two maps are mutually inverse. Convert a word to a Boolean list by replacing each bit by whether it is one; this list has exactly the word length. Let rev_N(x)_i=x_(N-1-i). Reversing twice is identity, also at N=0.

The public sample index of a head-first word w is obtained by first taking its basis function, then reversing it, then using L_N. Equivalently it is the most-significant-first list value J(w) given by

  J(empty)=0,             J(b::v)=2^(length v) b+J(v).

To verify this relation, appending a last bit satisfies

  L_(N+1)(append(x,b))=L_N(x)+2^N b.

Reversal changes a first-bit cons into a last-bit append, and induction gives the displayed recurrence for J. In particular the finite sample index formed directly from a Boolean word of length k+1 agrees with this word-to-sample map at that same positive width. The arithmetic is exact; length evidence only identifies the common carrier [2^(k+1)].

For any public data basis function x, taking the head-first word of rev_N(x) and applying the word-to-sample map yields L_N(x): the two reversals cancel. Thus chronological head-first order, increasing emission-wire order, and public little-endian integer order are related by explicit maps; they are not silently identified. These index identities alone do not assert that a supplied chain contracts to any particular sampled function.

S8. One circuit on N+q wires and its actual list length

First assemble the stages internally on q low bond wires followed by N chronological data wires. At stage t place its local bond wires on the existing q bond wires and its local highest fresh wire at internal position q+t. Previous data wires remain passive. Lift the earlier instruction list over the next fresh zero bit and append the newly placed stage list. Matrix evaluation of this single list equals the sequential action, by induction and the passive-prefix matrix entries. The initial circuit can be padded and prepended; here it is empty by S5-S6.

For the public N+q-wire convention, place data on low wires 0,...,N-1 and bond on high wires N,...,N+q-1. Rewrite every instruction's wire labels so internal bond wire a goes to N+a and internal data wire q+t goes to N-1-t. This is construction of gates on their final named wires, not a free physical SWAP of an already prepared state. A separate hardware connectivity restriction would require its own routing and resource analysis.

For arbitrary supplied stage circuits satisfying S6's columns, the public circuit amplitude at public data x and bond z, from the all-zero input on every wire, is

  delta_(z,0^q) M_D(w(rev_N(x)))_(0,0).

This statement still does not require D to be canonical or normalized: those are needed by the existence construction of its stages, not by composition after the columns are supplied. It includes every data and bond basis label. The instruction relabeling explains why the reversal in S7 is present at this public boundary.

Padding, lifting, and placing a stage preserve its list length, and renaming each instruction preserves length. Therefore the assembled list length is exactly sum_(t=0)^(N-1) length(c_t). With an empty initial circuit the public list has the same sum. For any natural bound K such that each executed stage has length at most K, its public gate count is at most N K. This counts every instruction, not only rotations or an arithmetic-operation proxy. The empty N=0 sum and list have length zero.

S9. Complete positive-length exact-real existence

Fix a positive length N, any q>=0, and a real chain C of length N with both boundary dimensions one. Assume only that its maximum bond is at most S=2^q and

  sum_(head-first words w) M_C(w)_(0,0)^2 = 1.

S5 produces a canonical scalar-boundary D with the same amplitude function and the same maximum-bond bound. At every actual site S4 produces a local finite circuit, including its exact active columns and length at most 6 S^3. Choose such circuits for the finitely used sites; unused later sites may be assigned empty lists because no later column equation is requested. S6 starts from the genuine empty zero-initialization circuit and proves terminal cleanup, and S8 composes these into one public circuit c on N+q wires. Thus

  length(c)<=N (6 S^3),              oracle calls(c)=0,
  c is unitary on the entire N+q-wire space,
  <x,z|c|0^(N+q)> = delta_(z,0^q) M_C(w(rev_N(x)))_(0,0)

for every public x and z. The conclusions hold together for the same circuit. Full unitarity follows from the actual primitive instructions; it is not assumed as the desired final state action. The original signed amplitudes are exact, not merely their probabilities or their equality up to an unspecified global phase. There is no extra initial preparation cost in the instruction list because its signed boundary was absorbed into the first core.

The positivity restriction belongs to this complete boundary-absorption existence route. General transport, conditional sequential cleanup, public placement, word maps, and list-count identities above include their stated zero-length cases. The empty scalar chain already has its unique amplitude +1. These facts must not be replaced by a claim that an arbitrary zero-wire signed state was covered by the positive-length construction.

S10. Exact scope and remaining work

The gate model permits exact real RY angles and named-wire controlled-NOTs. The bound N*6*(2^q)^3 is a genuine length bound in that model. It is not a finite-bit, Clifford+T, nearest-neighbor, depth, preprocessing, or readout bound, and it does not become polynomial in another scientific input parameter merely by treating q as fixed. Nonunique factor and completion choices are not a deterministic stored-data algorithm, even though a finite instruction list exists.

Further obligations remain for a concrete sampled problem: an actual input/data producer and proof that the given cores represent its desired amplitudes with the required normalization; a deterministic refinement of factor/completion selection and angle computation with explicit storage and input-access costs; finite precision, numerical stability, rotation synthesis and accumulated error; hardware routing/depth and total resources; and any coherent oracle, inverse/control, block-encoding, accepted-branch or amplification transport. None is supplied by the instruction-count field or by a word-index bijection. This local exact-real circuit existence does not assert a new scientific algorithm or a complete preparation/block-encoding resource theorem for an externally specified function.
