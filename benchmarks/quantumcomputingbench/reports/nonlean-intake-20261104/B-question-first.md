# B1–B4 question-first independent derivation

Reviewer: `/root/nonlean_audit_coherence`. This artifact was saved before opening the raw contributed QA answers, rubrics, mechanism maps, continuation decision, existing benchmark catalog, semantic diagnostics, or previous reviews. Actual prior exposure: parent task instructions and its later request for notation-only formulas; repository AGENTS.md, HARNESS.md, substantive-worker skill and the three publication/digestion/memory protocols; `_out/cohort-question-only/B1.json` through `B4.json`; relevant Lean text obtained with `git show` at frozen commit `86b9e677566498da04faebcf4e5ed57f177c6bb1`. The question-only files contain source anchors and declaration names; B1's source anchor explicitly includes a theorem statement and its implementation proof ingredients. Thus this is question-first and answer/rubric-blind, not blind to the supplied source or its theorem proof. No Lean compilation, model execution or human review occurred.

Exact UTF-8 question-string, raw question-only file, and frozen source hashes are recorded in `B-question-first-bindings.json`, created in this same phase. The questions' source SHA-256 values all match the frozen Git blobs. This review establishes natural-language mathematics and source scope; declaration existence is not a new build certificate.

## B1: clean-column state contraction

Let B be the finite bond label set, h its arbitrary complex boundary vector, and let K_t(bit) have row b, column a equal to K_t(bit,b,a). Write v_n(x,b) for the recursively produced amplitude. Fresh-zero insertion and identity action on the emitted prefix imply exactly

    v_(n+1)(x,b) = sum_a U_n((x_n,b),(0,a)) v_n(prefix(x),a).

At n=0, v_0(empty,b)=h_b=(I h)_b. Assuming v_n(z,a)=(T_n(z)h)_a for every prefix and bond label, substitute the clean-column equality into that finite sum to obtain

    v_(n+1)(x,b) = sum_a K_n(x_n)_(b,a) (T_n(prefix(x))h)_a
                 = (K_n(x_n) T_n(prefix(x)) h)_b.

This is precisely the transfer recurrence. The complete conclusion holds for every n, every output word, and every final bond label; it is not only a projected success-sector identity. No norm, unitarity, unit boundary, support or terminal-cleanup hypothesis is required for the algebraic identity. Input columns whose fresh-bit input is 1 are irrelevant because their amplitudes are identically zero before that stage. At fixed length, stages t>=n are also unused. Under the unchanged question, **every** clean fresh-bit-0 bond-input column is part of the hypothesis; inactive bond columns cannot additionally be omitted without a support invariant. The separate supported theorem in source explains that additional variant, but cannot replace this question's contract. Unitarity, terminal cleanup, flattened wire placement and efficient circuit synthesis remain separate obligations.

Source correspondence: `SequentialBondPreparation.step_apply`, `transfer`, `run`, and `run_eq_transfer`, approximately lines 59–110. The source's supported extension at 125–174 is deliberately not substituted. Its mass theorem at 327–340 requires unitarity and adds a separate conclusion.

## B2: retained label makes branch phase coherent

Let p_lambda=|c_lambda|^2 and z_lambda=exp(i phi_lambda). Orthogonal labels, rather than orthogonality of the data vectors, give the actual complete output

    Psi_tilde = sum_lambda c_lambda z_lambda |lambda> tensor psi_lambda.

For every common phase chi, expand the squared norm using label orthogonality and unit branch vectors:

    ||Psi_tilde - exp(i chi) Psi||^2
      = sum_lambda p_lambda |z_lambda-exp(i chi)|^2
      = 2 - 2 sum_lambda p_lambda cos(phi_lambda-chi).

Each summand is nonnegative. Exact equality occurs iff z_lambda=1 on the populated support c_lambda!=0. Equality up to one global phase occurs iff all z_lambda are the same on that support. In particular, an unpopulated label imposes no constraint; a singleton support always agrees up to phase but agrees exactly only for phase 1; a common nontrivial phase gives global equivalence without exact vector equality. As an optional consequence, minimizing over chi gives squared distance 2-2|sum p_lambda z_lambda|, again a distinct question from raw vector error.

An explicit unitary witness uses two labels, H=C^2, clean input=psi_0=psi_1=|0>, c_0=c_1=1/sqrt(2), V_0=I, V_1=-I. Every isolated branch yields the intended ray and all its measurement probabilities, yet the intended output is |+> tensor |0> and the actual output is |-> tensor |0>. They are orthogonal. Measuring the **label in the X basis** distinguishes them with certainty; computational-basis label measurement does not. More generally isolated probabilities cannot certify a vector phase, and separate branch experiments do not constrain phase differences.

The mathematical correction D=sum_lambda exp(-i phi_lambda)|lambda><lambda| is unitary and (D tensor I)Psi_tilde=Psi. Knowing classical phase metadata does not supply a physical D, coherent label access, a computable phase supplier, precision guarantees or a finite-gate compiler. H already contains every data/work output; the argument resets no work. `evalPrimitiveProgram` supplies phase-aware single-program scalar semantics with the same positive sign and `evalGlobalPhase_neg` supplies its conjugate convention; neither source declaration itself proves this controlled-family result. The retained-label and unit-branch hypotheses are indispensable AND inputs to the norm argument.

## B3: precision allocation under the assumed sufficient budget

For r>=1, define C=sum c_j and

    delta_j^* = 2 eta c_j/(C m_j),
    T^* = sum_j c_j log_2(C m_j/(2 eta c_j)).

The point is feasible, since sum m_j delta_j^*=2 eta. Also 0<delta_j^*<1: 2 eta<1, c_j/C<=1, and m_j>=1. In fact every feasible delta_j satisfies delta_j<=2 eta/m_j<1, so the upper caps are inactive everywhere on the feasible set.

For any feasible delta, let t_j=delta_j/delta_j^*>0. By ln t<=t-1,

    (ln 2)(T(delta)-T^*) = -sum c_j ln t_j
      >= C-sum c_j t_j
      = C-(C/(2 eta))sum m_j delta_j >= 0.

Equality in total forces equality in every positive-weight log inequality, hence t_j=1 for all j. This proves attainment, global minimality and uniqueness, rather than only a stationary point. No independence or cancellation assumption enters this deterministic worst-case certificate.

Set b_j=ceil(log_2(1/delta_j^*)). These are nonnegative finite integers, and 2^(-b_j)<=delta_j^*. Conditional on the certified supplier, telescoping yields ||V-U||<=(1/2)sum m_j 2^(-b_j)<=eta. The integer tolerances are feasible in the continuous problem, so T^*<=sum c_j b_j. Since ceil z<z+1, their cost is strictly less than T^*+C. This does not prove exact integer optimality.

For full-output unit vectors, insert Vx and Ux and use unitarity:

    ||Vy-psi|| <= ||V(y-x)||+||(V-U)x||+||Ux-psi|| <= rho+eta+kappa.

The trivial unit-vector cap 2 may also be applied. If r=0, U=V, empty cost and rotation budget are zero; formulas dividing by C are not used and the state bound is rho+kappa. If eta=0 and r>0, the positive continuous tolerances cannot satisfy the budget, and no finite b_j can make the positive dyadic budget zero. Exact angles can give zero actual error through a separate exact argument; failure of the positive-tolerance sufficient certificate is not impossibility of an exact circuit.

The source supplies a uniform positional error theorem and the exact physical RY norm interface. The weighted, reused-parameter optimization and integer rounding above are new mathematical reasoning under question-supplied interfaces; they are not the existing source theorem. The question explicitly assumes the supplier cost model, and arbitrary `ExactAngle.real` carries no computable numeric export guarantee. Neither this optimization nor the error bound proves polynomial-time angle generation, storage/access complexity, or finite-gate synthesis. Reuse is charged once in this supplier model but m_j times in the error bound.

## B4: all-length index transport and vector correction

For little-endian labels, L_(k+1)(cons(b,x))=b+2L_k(x). For an appended high bit, L_(k+1)(snoc(x,b))=L_k(x)+2^k b. Reversing a head/tail word satisfies rho_(k+1)(cons(b,x(u)))=snoc(rho_k(x(u)),b). Thus

    S_(k+1)(b::u)=S_k(u)+2^k b=M(u)+2^k b=M(b::u),

with base S_0=M(empty)=0. This proves the all-length equality in the required head/tail versus appended-high-bit recurrence. Word-to-basis is a coordinate bijection. Reversal is an involutive coordinate bijection. L_n is bijective to [0,2^n): inductively its lowest bit is the parity of the index and the remaining index is its quotient by 2, uniquely reconstructing the tail. Their composition S_n is therefore bijective too, as is M by equality. Applying S to the word read from rho x gives L(rho(rho x))=L(x).

At physical label x, the unique word is w=wordOfBasis(x), hence

    v_x=F(w)=f(M(w))=f(L_n(rho_n x)).
    (Pv)_x=v_(rho_n x)=f(L_n(x))=t_x.

Consequently v=t without a permutation iff f(L_n(rho_n x))=f(L_n(x)) for every x, equivalently the sample table is invariant under the induced fixed-width bit-reversal permutation. Reindexing the finite sum proves

    ||v||^2=||t||^2=sum_(k=0)^(2^n-1) f(k)^2.

If this mass Z is positive, dividing by sqrt(Z) yields normalized vectors and the same exact Pv=t transport. At Z=0 every f(k)=0 and v=t=0; no normalized state exists. For n=0 or 1, reversal is the identity and all tables agree without correction. Any reversal-invariant table, including a constant table, agrees for all n.

For n=3 choose w=(1,0,0). Its physical little-endian label is L(x(w))=1, while S_3(w)=M(w)=4 and L(rho x(w))=4. Let f(4)=1 and f(k)=0 otherwise. Then v=|x=(1,0,0)> has flat index 1, and t=|x=(0,0,1)> has flat index 4. This table is realizable in the stated setup with all bond dimensions 1, ell=r=1, A_0(b)=[1 if b=1 else 0], and A_1(b)=A_2(b)=[1 if b=0 else 0]. The example is not merely incompatible table data.

Relabeling physical coordinates changes the correspondence between sample indices and emitted bits. It does not reverse the ordered product ell A_0(w_0)...A_(n-1)(w_(n-1)) r. Those matrices need not commute, and reversing their product may even be dimensionally undefined. A basis-coordinate relabeling is a mathematical permutation; implementing it on an existing physical register requires a routing/permutation circuit and its own cost proof. The source's `sampleEquiv_value`/`sampleEquiv_public` prove the index adapter; they do not certify efficient tensor construction, wire permutation synthesis, or a preparation algorithm.

## Pre-comparison scope conclusion

The four questions are mathematically answerable as stated. B1 matches a source theorem directly. B4 extends a source index theorem to vector coefficients by elementary finite reindexing. B2 is a coherent controlled-family extension of single-program phase semantics. B3's primary allocation target is a new optimization under supplied error interfaces and an assumed cost model. No current Lean root is claimed for those new extensions, and graph attachment must retain that distinction. Catalog novelty/duplication and raw answer quality have intentionally not yet been assessed.
