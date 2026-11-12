# Formal-only independent compiler-family reconstruction

State: source-formal phase sealed; native/signature/axiom/private/generated checks NOT RUN.
Direction fingerprint: wholecompilerfamily/phase-and-control-spectator/formal-only-independent.

This packet reconstructs only actual comment-masked Lean definitions and propositions. No natural-language mathematical source, author packet, earlier mathematical review, registry conclusion, CI log, or source-comparison result was used. Formal string fields are retained as data, never as mathematical evidence. The three raw hashes were checked before comments were masked; comment masking preserves line positions. Imported project providers were masked by the same fail-closed tokenizer before inspection. No Lean invocation, Git operation, network access, canonical edit, or subagent occurred.

## Exact context and exhaustive scope

| Target | Raw SHA-256 | Named declarations |
| --- | --- | --- |
| PrimitiveMacros | bd5ada5cb61430ea9d32ce1b3adbd84e6b13d8c3fe2c1b6f2758da2a06903664 | 43 public |
| UniformlyControlledRy | 78d1aed9bb4068bcee138b665bd93a389463bbb591108837758a6d80752a1cf1 | 11 public, 8 private |
| CubicAmplitudePrimitive | 48c9a4a1c47c925c93493eede21eb7b492d23d2cb7dadf254782e4485c349cb3 | 25 public |

Total: 87 source declarations, 79 public and 8 private. The source inventory retains every complete defining/proof region and every source signature with all explicit/implicit binders and hypotheses. These are source signatures, NOT elaborated Lean types. Private scoped names are source labels, not asserted compiled private names. There are 110 lexical administrative/declaration regions, not 110 compiler-certified commands. All three whole files, including their proof bodies, were inspected.

Administrative coverage: PrimitiveMacros imports ReversibleClassical and Mathlib.Tactic; opens QuantumBlockEncoding.Robin.ComplexLCU; has outer QuantumBlockEncoding and nested MonomialProgram namespaces; two local `set_option maxHeartbeats 2000000 in` wrappers. UniformlyControlledRy imports PrimitiveSemantics; opens Robin.ComplexLCU and scoped Kronecker; has one inline simp attribute. CubicAmplitudePrimitive imports CubicStatePreparation, PrimitiveBasisLE, UniformlyControlledRy, Mathlib.Tactic; has nested CubicDiagonalOracle; opens Robin.ComplexLCU; has three inline simp attributes. All namespace ends are inventoried. No section variables, declared local instances, target-local notation, target-local universes, target-local axiom/opaque declarations, or other attributes occur in the three masked files. Generated declarations still require native enumeration.

The import-source pin file records 4,617 source modules (including implicit Init), 28 project providers, their direct import edges, raw source digests, and inherited olean digests where present. These hashes establish file identity only. They do not establish artifact freshness, compilation, trust closure, or that every imported declaration is used. The configuration binding pins Lean 4.33.0 and the complete manifest; the toolchain-file hash is 302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b, lakefile hash f6637c3a2467fdeee6b2de72505d0581c4a49793388197bd8e9e7df3f5817fc1, manifest hash 510171e8214a2ac5e00f16c1bf92ad474d2de42c4cd2dc2b3d411272f7b58763.

## Shared exact semantics

For q qubits the basis is the full function space Bq = (Fin q -> Fin 2); vector amplitudes are complex. A matrix has output row, input column and acts on column vectors. A chronological gate list [g1,...,gm] evaluates as U(gm)...U(g1). Program composition `left.seq right` performs left and then right. A program additionally carries the exact scalar exp(i phi); it is not a quotient modulo global phase.

For a target t, splitting the basis yields (target bit, every other wire). A one-qubit lift acts on that bit and the identity on the ENTIRE other-wire assignment. This is a named-wire semantics, not an assumed contiguous tensor order. Ry(theta) = [[cos(theta/2),-sin(theta/2)],[sin(theta/2),cos(theta/2)]], Rz(theta) = diag(exp(-i theta/2),exp(i theta/2)), X flips 0 and 1. CX preserves every wire except the distinct target and flips that target exactly when its control is 1.

ExactAngle is syntax for rationals, rational multiples of pi, twice-arccos rational amplitudes carrying a bound proof, twice-arccos-sqrt rational probabilities carrying bounds, arbitrary exact reals, addition, negation and rational scaling. Its semantics is exact-real; the presence of syntax is not a numerical angle-evaluation or finite-bit gate-synthesis theorem.

## PrimitiveMacros: phase-exact macros and the entire spectator sector

H is i Ry(pi/2) Rz(pi), exactly [[1,1],[1,-1]]/sqrt(2). P(theta) is exp(i theta/2)Rz(theta) = diag(1,exp(i theta)). Chronologically H is Rz(pi), Ry(pi/2) plus global phase pi/2; T is Rz(pi/4) plus phase pi/8; T-dagger is Rz(-pi/4) plus phase -pi/8. Discarding those program phases would change all the stated matrix equalities and would be unsafe under later coherent control.

A phase-permutation matrix sends |s> to p(s)|f(s)>; it need not be unitary for arbitrary p. Its multiplication law is p(s)q(f(s)) and permutation g(f(s)), matching chronological composition. MonomialProgram stores an actual program, the phase function and permutation, and an equality proof. It imposes no separate phase-modulus premise; the program equality is the semantic field.

For pairwise distinct a,b,t the CCX middle is the chronological word

    CX(b,t), Tdg(t), CX(a,t), T(t), CX(b,t), Tdg(t), CX(a,t),
    T(b), T(t), CX(a,b), T(a), Tdg(b), CX(a,b).

Its permutation is the identity on the full Bq and its phase is -1 iff s(a)=s(b)=s(t)=1, otherwise +1. Independently expanding the T exponents, with A,B,T bits and xor interpreted as 0/1, gives

    -(T xor B) + (T xor A xor B) - (T xor A) + B + T + A - (A xor B) = 4ABT.

Thus the accumulated exp(i pi/4 times exponent) is exactly (-1)^(ABT), not merely a class modulo a scalar. H(t), middle, H(t) is therefore the phase-free permutation t -> t xor (a and b), preserving both controls and every other wire. HZH=X and HH=I are used in each fixed other-wire block. The block-diagonal CCZ/CCX and conjugation lemmas only require a!=t and b!=t and remain meaningful when a=b. The literal 6-CX, 7-T/Tdg middle and its compiled outer program require the additional a!=b binder. No clean input, scratch workspace, or discarded garbage is assumed: equality is on the full matrix for every finite q with valid wires. From the literal program one can count 6 CX and 11 one-qubit gates (7 phase macros + 4 gates in two H macros); these counts are decoder derivations, not new named resource theorems in this target.

## UniformlyControlledRy: repeated controls are allowed

Inputs are arbitrary natural q,k, a wire function w : Fin k -> Fin q, target t, proofs w(i)!=t, and a complete angle table alpha : Bk -> ExactAngle. There is NO injectivity requirement on w. At a fixed non-target assignment c, the selected control tuple is (c(w(0)),...,c(w(k-1))). The full block is Ry(eval(alpha(tuple))) on t with every non-target bit fixed. Consequently the equality preserves relative phases across different contexts and is valid for entangled inputs by linearity. Repeated controls just restrict which table entries are reachable. Unreachable table values do not create an added assumption or invalidate the recursive identity. k=0 includes the unique empty assignment; q=0 has no target inhabitant.

For k+1 controls, prependControlBit places the first logical control at index 0, and the rest use succ indices. Let alpha0(u)=alpha(0::u), alpha1(u)=alpha(1::u), alpha+=(alpha0+alpha1)/2 and alpha-=(alpha0-alpha1)/2, represented using ExactAngle constructors. The chronological recursion is

    Compile(tail,alpha+); CX(w(0),t); Compile(tail,alpha-); CX(w(0),t).

In a fixed spectator sector with head bit 0, the matrix is Ry(alpha-)Ry(alpha+)=Ry(alpha0). With head bit 1 it is X Ry(alpha-) X Ry(alpha+)=Ry(alpha1), using X Ry(beta) X=Ry(-beta). The proof performs precisely this blockwise induction; no relative or context-dependent phase is dropped. The separate recursively defined uniformlyControlledRyMatrix records the same product and is connected to the circuit by an induction equality; the stronger block-matrix theorem supplies the explicit state action.

The exact counts are R(k)=2^k Ry and C(k)=2(2^k-1) CX. The five-control specialization is 32 and 62. The compiler uses no additional wires or oracle constructors. This is an arbitrary finite-width theorem with exponentially sized explicit input tables and output circuits, not a claim of polynomial-time arbitrary-angle loading. No optimality, connectivity routing, numerical approximation, T count, classical table-preparation cost, or finite-bit synthesis is provided.

## CubicAmplitudePrimitive: a fixed 8-dimensional construction

There are exactly three wires: system low bit at 0, system high bit at 1, signal at 2. The logical control index is j=b0+2b1 in Fin 4. The imported formal definitions give gridSize(n)=2^n, gridPoint(n,j)=j/2^n and cubicAmplitude(n,j)=(j/2^n)^3. Hence a_j=(j/4)^3 for j=0,1,2,3; values are 0,1/64,1/8,27/64. The stored angle is twiceArccosRational(a_j) with an explicit |a_j|<=1 proof. The circuit is the two-control compiler at signal wire 2; the program phase is zero.

For encoded system j and signal s, encode(s,j) places j mod 2, floor(j/2) mod 2, and s on wires 0,1,2. The split context equality is exactly system-label equality, independently of signals. The resulting unitary preserves j and has signal block

    [[a_j, -sqrt(1-a_j^2)], [sqrt(1-a_j^2), a_j]].

In particular |j,0> maps to a_j|j,0>+sqrt(1-a_j^2)|j,1>; |j,1> maps to -sqrt(1-a_j^2)|j,0>+a_j|j,1>. This full two-branch action is derived from the exact controlled-Ry matrix definitions. The named clean-entry theorem certifies the signal-0 matrix entries, equal to diag(a_j) with normalizer 1. Signal 1 is a genuine failure/other branch, not cleaned garbage. There are no pure workspace ancillas beyond this one signal and no theorem that unconditionally resets it. On a normalized system vector sum_j c_j|j>, the derived signal-0 probability is sum_j |c_j|^2 a_j^2; it may be zero (e.g. j=0), so neither deterministic output nor amplitude amplification is certified here.

Little-endian flattening is sum_w 2^w b_w, giving flat index j+4s and clean indices 0,1,2,3. The 8x8 matrix is therefore [[A,-S],[S,A]] with A=diag(a_j), S=diag(sqrt(1-a_j^2)). Reindexing preserves unitarity and the named clean-block theorem. This is a fixed n=2 block-encoding, NOT an arbitrary-n compiled cubic oracle or normalized cubic state-preparation theorem.

The target is a concrete complex diagonal operator, normalizer 1, with descriptive string fields (data only). The presentation drops actual angles to a generic `exact-angle` label; it is a display circuit, not a standalone numerical export. The candidate supplies one auxiliary signal, two system qubits, zero pure ancillas, the actual flat matrix and actual primitive-program resource. The imported candidate type itself stores arbitrary `isUnitary` and `blockContainsTarget` propositions; the verified wrapper proves only those stored propositions. Here the construction explicitly sets them to genuine matrix unitarity and the stated clean-index equalities, so this instance has mathematical content. There is no generic theorem in that interface linking every candidate's presentation circuit or resource to its matrix. This instance's linkage must be read from the definitions and the dedicated circuit/program equalities.

From the general compiler counts, this literal specialization has 4 Ry and 6 CX, no Rz/X and no oracle calls. All gates touch the signal wire, so the source depth recurrence gives depth 10. These specialized counts/depth are decoder derivations, not target-local named theorems. PrimitiveCircuit.resource computes one-qubit/CX counts, zero oracle calls, zero pure ancillas and wire-scheduled depth; program global phases have no resource charge. The two named resource facts assert zero oracle calls and definitional identity between program and primitive-circuit resource. They do not by themselves prove external runtime, finite-bit cost, target matrix size scaling, or an efficient angle producer.

## Exhaustive per-declaration contract expansion

`declaration-contracts.json` gives all 87 records, each with exact module/hash, source region, complete source signature, declaration kind/visibility, and the independently reconstructed meaning. `whole-module-inventory.private.json` additionally retains all 110 administrative and declaration regions. The four simp registrations and two local options are therefore bound rather than silently omitted. The sole target-local structure is MonomialProgram; its four fields and their dependent equality are preserved in full. There are no target-local declaration bundles whose hypotheses can be replaced by a source interpretation; all source-versus-formal binder classifications remain unavailable until the independent late comparison.

## Pending native obligations (not executed)

The prepared NativeSignatureProbe.pending.lean imports exactly the three targets and requests full-universe, explicit, fully-qualified `#check`, `#print`, and `#print axioms` output for all 79 public source declarations. It has not been run. `pending-native-requirements.json` specifies the additional mandatory private/generated/module-ownership work, unavailable from a source-name probe alone. The source inspection sees no target-local sorry/admit/axiom declaration, but this is NOT a kernel-axiom or hidden-generated-declaration certificate. In particular native_decide proof bodies require their actual resulting trust dependencies to be reported, not inferred away.

Any future native check must first revalidate target, config, provider and artifact bindings, run only under parent-controlled memory resources, enumerate all target-owned constants including `_private` and compiler-generated helpers/equations/recursors, print fully elaborated types and recursively collect axioms, compare with this source inventory, then run the applicable repository gates on a suitable host. Any source or config change invalidates this seal. A successful direct import of inherited oleans alone would not establish a fresh build of these raw source bytes.

## Handoff and explicit remaining boundaries

Mathematical delta: a complete independent formal-only reconstruction of the compiler family, including exact phase/spectator action, alias conditions, garbage sector, finite specialization, and cost-model limits. Files changed: assigned scratch packet and one temporary index/seal helper plus this temporary report; no production tree changes. Failure class: ENV_BLOCKED for native proof/signature/axiom acceptance, intentionally not attempted under the parent resource constraint; no mathematical route is retired. Salvage: complete source contracts and masked provider pins retained; none promoted as natively checked fragments. Process-memory IDs consulted: none; only normative process protocols. Expected information gain: expose the actual complete formal contracts before late source comparison. Parallel admission/common-blind-spot review and comparator choice: parent-owned, not performed by this decoder. Reader exposition review and all publication/admission determinations remain pending. This is solely a source-formal phase seal.
