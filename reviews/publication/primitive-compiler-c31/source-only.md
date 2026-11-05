# Exact elementary macros, controlled rotations, and a finite cubic baseline

This is retrospective, implementation-informed local mathematics, not an external-paper reproduction, novelty claim, historical pre-proof seal, or compiler certificate. The historical formalizer is UNKNOWN. It recovers three complete legacy modules and their mathematical boundaries; independent reconstruction, actual signature/axiom inspection, and admission remain separate future work.

## S1. Conventions and exact angles

A basis state on q named wires is a function from {0,...,q−1} to {0,1}. Matrices use output rows and input columns. For gates listed in temporal order g1,...,gm the evaluated matrix is Gm⋯G1. A program also stores a global phase φ and denotes exp(iφ) times that product. An exact angle is symbolic mathematical data with a real evaluation; it is not a finite-bit approximation algorithm.

Use the standard matrices
\[
R_y(\theta)=\begin{pmatrix}\cos(\theta/2)&-\sin(\theta/2)\\\sin(\theta/2)&\cos(\theta/2)\end{pmatrix},\quad
R_z(\theta)=\operatorname{diag}(e^{-i\theta/2},e^{i\theta/2}),\quad
X=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]
All identities below preserve the full complex matrix, not merely outcome probabilities or equality modulo global phase. The underlying named-wire semantics does not by itself choose integer endianness.

Splitting off a target wire identifies a basis state with its target bit and the assignment of every other wire. A lifted one-qubit matrix has entry zero between distinct other-wire assignments, and otherwise has the corresponding two-by-two entry. Thus lifting preserves multiplication and scalar multiplication: a matrix-product sum collapses onto the common unchanged context. This is the shared algebraic dependency used below.

## S2. Exact H, T and inverse-T programs

Define
\[
H=iR_y(\pi/2)R_z(\pi),\qquad
P(\theta)=e^{i\theta/2}R_z(\theta).
\]
Direct substitution gives
\[
H=\frac{\sqrt2}{2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad
P(\theta)=\operatorname{diag}(1,e^{i\theta}).
\]
The exponential factors are essential. The exact H program lists Rz(π), then Ry(π/2), with global phase π/2. The exact T and inverse-T programs list Rz(π/4) and Rz(−π/4), with global phases π/8 and −π/8 respectively. Temporal composition and the lifting identities give their full-register matrix equalities. Neither Ry(π/2) alone nor a phase-free Rz(π/4) is the same exact matrix as the corresponding macro.

## S3. Monomial matrices and chronological composition

On a finite index set, let σ be a permutation and p an arbitrary complex-valued function. Define
\[
M(p,\sigma)_{r,c}=\begin{cases}p(c),&r=\sigma(c),\\0,&\text{otherwise}.\end{cases}
\]
No unit-modulus hypothesis is needed for the following multiplication identity; therefore this general definition is not automatically a unitary matrix. If a left program executes before a right program, the composite permutation is σR∘σL and the composite phase at c is pL(c)pR(σL(c)). In the matrix-product sum the sole surviving intermediate index is σL(c), which proves the formula without an appeal to a simulator.

A controlled-X is such a matrix with phase one and its ordinary controlled-flip permutation. A phase P(θ) on target t has identity permutation and phase one when the bit t is zero, exp(iθ) when it is one. A proof-carrying monomial program stores a primitive program, p, σ, and the actual equality of their matrices. Its sequential constructor derives the new equality from the old two equalities and the multiplication identity; that equality is an internal dependency, not a proof that an unrelated oracle contract holds.

## S4. The exact controlled-controlled-X phase network

Take three pairwise distinct wires a,b,t. The temporal middle network is
\[
CX_{b,t},\ T_t^{-1},\ CX_{a,t},\ T_t,\ CX_{b,t},\ T_t^{-1},\ CX_{a,t},\ T_b,\ T_t,\ CX_{a,b},\ T_a,\ T_b^{-1},\ CX_{a,b}.
\]
The four flips of t restore t and the two flips of b restore b, so the middle permutation is identity. For initial bits a,b,t∈{0,1}, the accumulated phase is exp(iπE/4), where
\[
E=a+b+t-(t\oplus b)+(t\oplus b\oplus a)-(t\oplus a)-(b\oplus a).
\]
Checking the eight bit triples, or substituting x⊕y=x+y−2xy, gives E=4abt. The middle matrix is therefore diagonal with value −1 exactly when all three bits are one and value 1 otherwise. This includes every phase factor contributed by the exact T and inverse-T programs.

Conjugate that middle program by the exact H program on t. For each fixed other-wire assignment, the middle two-by-two block is Z when a=b=1 and identity otherwise. Direct two-by-two multiplication gives H²=I and HZH=X. Block-diagonal multiplication then gives the exact controlled-controlled-X permutation matrix on all basis states. The program and its proof-carrying refinement use only X, Ry, Rz and controlled-X primitives. This is a genuine elementary-macro semantic result, not merely a gate label or a classical truth-table annotation.

Some intermediate block identities only require a and b to differ from t; they need not assume a≠b. The final displayed elementary network does require all three distinct wires. Do not silently remove or propagate that stronger binder into every intermediate identity. No new finite-bit approximation, connectivity scheduling, or asymptotic synthesis-cost theorem is asserted by this matrix proof.

## S5. An independent controlled-rotation specification

Let w map n control positions to q named wires, let t be a target wire, and assume w(j)≠t for every control position. The control wires need not be injective. Let θ assign an exact real angle to each n-bit control tuple. For any assignment x of all non-target wires, read the tuple x∘w and place Ry(θ(x∘w)) on the target's two-dimensional block. Distinct non-target assignments never mix.

This is a backend-independent block-diagonal specification. With repeated control wires, only the consistent control tuples occur in a physical assignment; no assertion is made that inconsistent tuples can independently occur. For zero controls there is one empty tuple and the block matrix is exactly the lifted single Ry gate. A controlled-X similarly has block I when its selected context bit is zero and X when it is one. These facts follow directly from the basis-entry definitions and target/context splitting.

## S6. The recursive compiler and its full semantic identity

At zero controls, emit one Ry gate at the angle indexed by the empty tuple. For a nonempty tuple split the first control h from the remaining tuple u and set
\[
\alpha(u)=\frac{\theta(0,u)+\theta(1,u)}2,\qquad
\delta(u)=\frac{\theta(0,u)-\theta(1,u)}2.
\]
Execute recursively the tail-controlled α circuit, then CX(h,t), then recursively the tail-controlled δ circuit, then CX(h,t). The tail wires still differ from t, so the recursion is well-typed. A separate recursive matrix formula has the same chronological product in reverse matrix order; induction first proves that the emitted list evaluates to that recursive formula.

To establish the independent specification rather than stop at a matching recursive definition, fix the entire non-target context. The recursive calls preserve it. If h=0, the target block is Ry(δ)Ry(α)=Ry(α+δ)=Ry(θ(0,u)). If h=1 it is XRy(δ)XRy(α)=Ry(−δ)Ry(α)=Ry(θ(1,u)), using XRy(δ)X=Ry(−δ). Both cases have exact phases. Reassembling all unchanged context blocks proves equality with the independent controlled-rotation matrix. This argument also explains why injectivity of the control-wire map is unnecessary.

## S7. Reference costs are exponential, not the desired scalable route

Let r(n) and c(n) count emitted Ry and controlled-X gates. The recursion gives r(0)=1, c(0)=0, r(n+1)=2r(n), and c(n+1)=2c(n)+2. Consequently
\[
r(n)=2^n,\qquad c(n)=2(2^n-1).
\]
At five controls these are 32 and 62. The emitted primitive language has no opaque oracle instructions, hence its stored oracle-call count is zero. That zero does not make the cost polynomial: the angle table and circuit already have exponential size in the number of independent control bits. Angle evaluation, storage, classical generation, approximation precision and finite-bit synthesis are not included in this exact-real gate-count statement. No Gray-code optimization or polynomial-resource Hermite claim follows here.

## S8. A fully expanded two-control cubic amplitude baseline

Now fix exactly two little-endian system bits on named wires 0 and 1 and a signal bit on wire 2. If the system bits are b0,b1, let j=b0+2b1∈{0,1,2,3} and
\[
d_j=(j/4)^3\in\{0,1/64,1/8,27/64\}.
\]
These four rational values lie in [0,1]. Select the exact standard-Ry angle θj=2arccos(dj) and apply the preceding two-control compiler with the two system wires as controls and wire 2 as target. The program's explicit global phase is zero.

The compiler theorem gives its full matrix as the controlled block diagonal. Since cos(θj/2)=dj and sin(θj/2)=√(1−dj²), its action on a zero signal is
\[
|j\rangle|0\rangle\longmapsto
|j\rangle\bigl(d_j|0\rangle+\sqrt{1-d_j^2}|1\rangle\bigr).
\]
The named-wire statement is interpreted with its actual signal placement, not by pretending the displayed tensor order chooses flat endianness. The amplitude-bound proof is a finite rational check on four inputs, followed by exact casting into the real field; it is not a general n-qubit bound inferred from samples.

## S9. Clean extraction, flat indexing, and the certificate wrapper

Encode (s,j) by wire values (j mod 2, floor(j/2) mod 2, s). Extracting the two controls recovers j, and two encoded vectors have equal non-signal contexts if and only if their system indices agree, regardless of their signal values. These finite encoding identities turn the full controlled matrix into the exact clean-signal entry formula
\[
U_{(0,r),(0,c)}=\begin{cases}(r/4)^3,&r=c,\\0,&r\ne c.\end{cases}
\]
This is the cubic diagonal operator D2, not the rank-one state-loading operator. The ambient matrix is genuinely unitary because it is the evaluation of a primitive program; its clean block alone is a contraction, not a unitary on the system.

The separately proved little-endian basis equivalence maps this encoded basis to the flat integer j+4s. Reindexing the whole unitary along that equivalence preserves unitarity and transports the clean entries. The operator target has normalizer one, two system qubits and one signal qubit, with no additional pure workspace. The verified wrapper is supplied by the actual unitary and clean-entry theorems rather than by a true Boolean metadata flag.

The human circuit presentation retains gate kinds and wire numbers but writes an angle placeholder; it is not an angle-complete QASM emitter. The resource row is definitionally the emitted circuit/program resource and its oracle-call field is zero. The generic reference formulas specialize to four Ry and six controlled-X gates. Neither the presentation wrapper nor the verified block wrapper separately proves normalization of a desired prepared state, postselection/amplification cost, finite-bit rotation synthesis, or a family-wide executable acceptance theorem.

## S10. Source construction topology and remaining obligations

There are three interacting but distinct paths. Exact one-qubit macros plus monomial composition yield the phase network, then H-conjugation yields elementary controlled-controlled-X. Independently, one-target block lifting plus two-way angle splitting yields the controlled-rotation compiler and its exponential count formulas. The finite cubic path uses that compiler, the four rational amplitudes, the exact arccos identity and the little-endian adapter to obtain its clean block and verified operator wrapper. The first macro path is not a prerequisite of the two-control cubic proof merely because both use the same primitive language.

Private helpers for prepending control bits, half-sum/half-difference angle tables, the zero-control lifted block, the controlled-X block and its bit-flip entry all belong to the second path. They are internal providers, not separately credited external source results. Arbitrary monomial phases, inconsistent control assignments, zero controls, global phases, signal placement and rational-to-real-to-complex casts remain visible boundaries.

Open consumers are an efficient general n-qubit cubic arithmetic/rotation producer; polynomial-size structured Hermite preparation; uniform finite-bit precision and synthesis bounds; normalized state-action and success/amplification certificates; complete preprocessing/storage/depth/ancilla accounting; and independent executable family acceptance. The finite baseline is retained as a correctness regression, not promoted to any of these stronger goals.
