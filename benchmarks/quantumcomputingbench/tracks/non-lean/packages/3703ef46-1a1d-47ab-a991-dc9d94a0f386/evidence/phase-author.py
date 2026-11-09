"""Author-owned NL payload assembly; no model, Lean, or admission operation."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = "bb260f4e27360a0d3791b40cb22638af4b086fc9"
AUTHOR = "/root/batch2_phase"

P1_ANSWER = r"""Write \(T_q|y\rangle=|y+q\bmod M\rangle\). Relabel the finite Fourier sum by \(z=y+q\bmod M\). For the unique representative \(y\in\{0,\ldots,M-1\}\), the integers \(y\) and \(z-q\) differ by a multiple of \(M\), so their exponential factors agree. Therefore
\[
T_q|G_m\rangle
=M^{-1/2}\sum_z e^{2\pi i(z-q)/M}|z\rangle
=e^{-2\pi iq/M}|G_m\rangle.
\]
The sign is negative for the positive Fourier exponent specified in the question. A negative Fourier exponent, or subtraction instead of addition, reverses it. This is an exact modular identity, including wrapped additions.

First construct the promised adder. For a fixed bit \(Q_j\), adding \(2^j\) to \(Y\) when \(Q_j=1\) is a conditional increment of the suffix beginning at \(j\). The target bit \(Y_i\), for \(i\geq j\), flips exactly when
\[
Q_j\prod_{r=j}^{i-1}Y_r=1,
\]
where the empty product for \(i=j\) is one. These are the OLD suffix bits. Visiting \(i=m-1,m-2,\ldots,j\) preserves every lower controlling bit until all targets that need it have been processed. Thus the stated multi-controlled flips implement the binary carry rule, discard overflow modulo \(2^m\), and preserve \(Q\). In contrast, flipping from the low bit upward with these same controls would inspect changed bits and implement the wrong rule. Applying the increments for all \(j\) adds \(\sum_j2^jQ_j=q\) modulo \(M\), because each increment has the proved action on the word presented to it.

A NOT with two controls is one Toffoli. For \(k\geq3\) controls \(c_1,\ldots,c_k\), use \(k-2\) fresh-zero scratch bits. Compute \(a_1=c_1c_2\), then \(a_2=a_1c_3\), up to \(a_{k-2}=c_1\cdots c_{k-1}\), by \(k-2\) Toffolis. Flip the designated target with controls \(a_{k-2},c_k\), then reverse those \(k-2\) computations. None of the original controls has changed. The scratch returns exactly to zero, and the total is \(2k-3\) Toffolis. All targets, controls and scratch in this construction are distinct. The \(k=2\) formula gives one Toffoli and zero scratch; the one-control case is CNOT.

The suffix increment contains one CNOT at its lowest target. Its target \(i=j+d\), \(d\geq1\), has \(k=d+1\) controls and therefore costs \(2d-1\) Toffolis. Reuse the clean chain after each flip. The whole adder has
\[
C_{\mathrm{CX}}(m)=m,\qquad
T(m)=\sum_{d=1}^{m-1}(m-d)(2d-1)
=\frac{m(m-1)(2m-1)}6,
\qquad a_m=\max(m-2,0)
\]
Toffolis and simultaneously live scratch bits, respectively. The polynomial follows from the elementary sums of \(d\) and \(d^2\); it is also \(\sum_{r=1}^{m-1}r^2\). There are no X, H or phase gates in this adder. The result is a deliberately simple exact construction, not an optimality claim. Since each elementary gate is reversible and each scratch chain is uncomputed on every basis input, linearity gives the clean action on arbitrary entangled inputs as well.

Now let \(K\) denote chronological application of \(B\), this adder on \((Q,Y,A)\), and \(B^\dagger\) on \((X,Q,W)\). In the fixed order \((X,Q,W,Y,A)\), the basis-state transcript is
\[
\begin{aligned}
|x,0,0\rangle|G_m\rangle|0\rangle
&\xrightarrow{B}|x,q_x,\gamma_x\rangle|G_m\rangle|0\rangle\\
&\xrightarrow{\mathrm{ADD}}
e^{-2\pi iq_x/M}|x,q_x,\gamma_x\rangle|G_m\rangle|0\rangle\\
&\xrightarrow{B^\dagger}
e^{-2\pi iq_x/M}|x,0,0\rangle|G_m\rangle|0\rangle.
\end{aligned}
\]
The adder preserves both \(Q\) and \(W\), so the supplied full inverse really applies to the same \((q_x,\gamma_x)\) record that \(B\) produced. It is not enough to clear only \(Q\). The inverse is available here because the entire circuit list was supplied: reverse its order, since X, CNOT and Toffoli are all self-inverse. No controlled inverse of a black box has been assumed. For every normalized coherent input \(\sum_xc_x|x\rangle\), linearity gives
\[
K\left(\sum_xc_x|x\rangle|0_Q0_W\rangle|G_m\rangle|0_A\rangle\right)
=\left(\sum_xc_xe^{-2\pi iq_x/M}|x\rangle\right)
 |0_Q0_W\rangle|G_m\rangle|0_A\rangle.
\]
The catalyst factorizes exactly and all other ancillary registers are zero. The same argument holds with an untouched reference entangled with the data. Tracing out the supplier record instead would multiply data coherences by \(\langle q_{x'},\gamma_{x'}|q_x,\gamma_x\rangle\), generally deleting coherence between unequal records; it would also not return the promised workspace. Equal-record or single-input exceptions do not certify the arbitrary-input clean interface. Neither a measurement nor amplification is needed here.

The binary expansion of \(y\) factorizes the gradient:
\[
|G_m\rangle=
\bigotimes_{r=0}^{m-1}
\frac{|0\rangle+e^{i\theta_r}|1\rangle}{\sqrt2},
\qquad \theta_r=\frac{2\pi2^r}{2^m}.
\]
Thus apply H and then \(P(\theta_r)\) on each physical bit \(Y_r\). This preparation \(F_m\) costs \(m\) H and \(m\) P gates in the declared logical model. Its inverse applies \(P(-\theta_r)\) and then H on each bit. The physical ordering is little-endian; no bit reversal or hidden quantum Fourier transform is required.

For \(L\) uses of the same supplier, the exact total gate counts, starting with all ancillary registers zero, are
\[
\begin{array}{c|cc}
\text{gate class}&\text{catalyst returned}&\text{final coherent reset}\\\hline
X&2Lb_X&2Lb_X\\
\mathrm{CX}&2Lb_{\mathrm{CX}}+Lm&2Lb_{\mathrm{CX}}+Lm\\
\mathrm{CCX}&2Lb_{\mathrm{CCX}}+LT(m)&2Lb_{\mathrm{CCX}}+LT(m)\\
H&m&2m\\
P\text{ or }P^\dagger&m&2m
\end{array}
\]
There are \(L\) forward and \(L\) inverse supplier executions and \(L\) adders. Any separately chosen data-only unitaries are additional and must be charged separately. The maximum live width of the displayed implementation is
\[
n+2m+w+a_m.
\]
It includes the output word, all supplier garbage, the catalyst and the adder scratch; reusing zero scratch after each gate does not remove its peak-width cost. The same width suffices for final reset. In the first column \(Y\) returns as the specified nonzero catalyst, not as a clean-zero ancilla. In the second, \(F_m^\dagger\) restores it to zero after the last use. If a ready catalyst is already supplied, the initial \(m\) H and \(m\) P charge is an external preparation cost rather than a repeated per-use cost.

For the stability question, include every supplier, adder and interleaved data-only unitary in one unitary \(\mathcal C_L\). On the exact gradient sector it satisfies
\[
\mathcal C_L(|\psi\rangle|0_{QWA}\rangle|G_m\rangle)
=|\Phi_\psi\rangle|0_{QWA}\rangle|G_m\rangle,
\]
where \(|\Phi_\psi\rangle\) is the ideal data output for that entire sequence. Register notation here merely groups the already fixed wires. Put \(|\widetilde G_m\rangle=\widetilde F_m|0\rangle\). Unitarity of the WHOLE sequence yields
\[
\left\|\mathcal C_L(|\psi\rangle|0\rangle|\widetilde G_m\rangle)
-|\Phi_\psi\rangle|0\rangle|G_m\rangle\right\|_2
=\|\widetilde G_m-G_m\|_2\leq\eta.
\]
There is no factor \(L\): the sole error was in the initial vector, and exact unitary evolution preserves its norm. Q, W and A are in fact still restored exactly even for a non-eigenstate catalyst, because ADD preserves the supplier record and returns its own scratch on every Y basis state. Y can become entangled with the data; exact gradient return or exact factorization does not follow for \(\widetilde G_m\).

After the actual inverse \(\widetilde F_m^\dagger\), a triangle decomposition gives full clean-zero error at most
\[
\eta+\left\|\widetilde F_m^\dagger|G_m\rangle-|0^m\rangle\right\|_2
=\eta+\left\||G_m\rangle-\widetilde F_m|0^m\rangle\right\|_2\leq2\eta.
\]
Both outputs are unit vectors, so this bound can also be capped at 2. It is a bound, not an assertion of exact reset or an optimal constant. Errors in every adder or supplier would be a different model, where repeated-operation bounds can accumulate. Actual preparation/inverse gate costs must replace the ideal \(m\)-gate counts when \(\widetilde F_m\) is used; a vector-error certificate alone gives no synthesis cost.

At \(m=1\), \(|G_1\rangle=(|0\rangle-|1\rangle)/\sqrt2\), the adder is one CNOT, and \(T(1)=a_1=0\). This is the Boolean kickback special case. If one explicitly extends to \(m=0\), then \(M=1\), Q and Y are trivial, \(q_x=0\), and \(D_q=I\). No adder, catalyst preparation or scratch is needed; one can omit B entirely. If the redundant B-then-inverse route is nevertheless retained, its actual \(2L g_B\) cost and any W width remain. There is no division by a nonexistent bit index.

The finite-word supplier, exact reversible arithmetic, logical phase gates and optional approximate catalyst have separate contracts. No arbitrary real phase is claimed to have an efficient supplier, no accuracy to any unspecified real target phase is proved, and the supplied list length need not be polynomial. Exact dyadic P gates are allowed by the declared logical model; a fixed finite gate set, its approximation error, connectivity/depth, and any classical compiler require their own analysis. The source's phase-aware primitive program conventions do not identify its primitive-gate counts with these macro counts."""

P2_ANSWER = r"""For a column coefficient vector \(c\in\mathbb C^N\), linearity gives \(Ec=\sum_j c_jEe_j\). With the stated inner-product convention,
\[
\|Ec\|_2^2=\sum_{j,k}\overline{c_j}c_k\langle Ee_j,Ee_k\rangle
=c^\dagger Gc,
\qquad G=E^\dagger E.
\]
Thus G is Hermitian positive semidefinite, its diagonal is \(G_{jj}=\|Ee_j\|_2^2\), and finite-dimensional spectral theory gives
\[
\|E\|^2=\max_{\|c\|_2=1}c^\dagger Gc=\lambda_{\max}(G).
\]
One may also expand the isometry identities to obtain \(G=2I-U^\dagger V-V^\dagger U\). The off-diagonal entries record coherent correlations of error vectors. Orthogonality of the columns of U and of V separately does not force the columns of their difference to be orthogonal.

Put \(r=(\sum_j\varepsilon_j^2)^{1/2}\). For every unit c, triangle inequality and scalar Cauchy-Schwarz give
\[
\|Ec\|_2\leq\sum_j|c_j|\|Ee_j\|_2
\leq\sum_j|c_j|\varepsilon_j\leq r.
\]
Equivalently \(\lambda_{\max}(G)\leq\operatorname{tr}G\leq r^2\). Since U and V are isometries, \(\|Uc\|_2=\|Vc\|_2=1\), so \(\|Ec\|_2\leq2\). Hence the universal bound is
\[
\boxed{\ \|V-U\|\leq\min\!\left\{2,\sqrt{\sum_j\varepsilon_j^2}\right\}.\ }
\]
There is no statistical-independence assumption or cancellation premise in this estimate.

Here is sharpness even among square unitaries, for each fixed nonnegative tolerance vector. If \(r=0\), choose \(U=V=I\); the zero upper bound is attained. If \(r>0\), define the real nonnegative unit vector \(s=\sum_j(\varepsilon_j/r)e_j\), its rank-one orthogonal projector \(P=|s\rangle\langle s|\), and \(\kappa=\min(2,r)\). Choose a real \(\theta\in[0,\pi]\) such that \(|e^{i\theta}-1|=\kappa\), for example \(\theta=2\arcsin(\kappa/2)\). Set
\[
U=I,\qquad V=I+(e^{i\theta}-1)P=(I-P)+e^{i\theta}P.
\]
The two orthogonal sectors \(\operatorname{ran}P\) and \(\ker P\) receive unit-modulus eigenvalues, so \(V^\dagger V=I\). More explicitly, the mixed products vanish because \(P(I-P)=0\), and both sector products sum to I. Moreover
\[
\|(V-I)e_j\|_2
=\kappa|\langle s,e_j\rangle|
=\kappa\frac{\varepsilon_j}{r}\leq\varepsilon_j,
\qquad \|V-I\|=\kappa\|P\|=\kappa.
\]
The inequality uses \(\kappa\leq r\). Thus the claimed bound cannot be decreased using only those column tolerances, even with full unitarity imposed. For \(r\leq2\), all specified column bounds are attained simultaneously; for \(r>2\), they remain valid upper bounds while the unitary cap is attained. Zero components of the tolerance vector create zero components of s and exactly zero corresponding column errors.

For a uniform tolerance \(\varepsilon_j=\varepsilon\), this reduces to
\[
\|V-U\|\leq\min\{2,\sqrt N\,\varepsilon\},
\]
with transition at \(\varepsilon=2/\sqrt N\). For \(N>1\) the dimension-free assertion \(\|E\|\leq\max_j\varepsilon_j\) is false in general. It is sometimes true for particular error geometry or loose tolerances; the counterexample refutes the universal implication, not every instance.

For a concrete operational witness, take \(N\geq2\),
\[
s=N^{-1/2}\sum_{j=0}^{N-1}e_j,\qquad
U=I,\qquad V=I-2|s\rangle\langle s|.
\]
Then \(V^\dagger V=I\), every column error is exactly \(2/\sqrt N\), and \(\|V-I\|=2\). The column errors tend to zero as N increases, including along qubit dimensions \(N=2^n\). On the saturating input s, the actual output is \(-s\). The vector distance is 2 but the two density matrices are identical, so their trace distance is 0: this input alone detects the chosen representative convention, not an operationally distinguishable physical state.

Now define \(t=(e_0-e_1)/\sqrt2\); it is a unit vector orthogonal to s. For the normalized input \(h=(s+t)/\sqrt2\),
\[
Uh=h=\frac{s+t}{\sqrt2},\qquad
Vh=k=\frac{-s+t}{\sqrt2},\qquad
\langle h,k\rangle=0.
\]
The vector difference is \(-\sqrt2s\), of norm \(\sqrt2\). With \(\rho=|h\rangle\langle h|\) and \(\sigma=|k\rangle\langle k|\), the difference has eigenvalue +1 on h, -1 on k and zero on their orthogonal complement. Therefore \(\|\rho-\sigma\|_1=2\) and the stipulated trace distance is 1. The projective measurement \(\{|h\rangle\langle h|,I-|h\rangle\langle h|\}\) returns its first outcome with probabilities 1 and 0. This establishes a fully distinguishable coherent-output failure despite small errors on every basis input.

The exact additional condition for a desired bound \(\|E\|\leq b\), \(b\geq0\), is \(G\preceq b^2I\). A concrete sufficient geometry for \(b=\max_j\varepsilon_j\) is pairwise orthogonality of the error columns: then G is diagonal and
\[
\|E\|=\max_j\|Ee_j\|_2\leq\max_j\varepsilon_j.
\]
In an explicitly label-preserving controlled comparison, differences of the form \(|j\rangle\otimes(v_j-u_j)\) are orthogonal for distinct j because the labels are orthogonal. That is an additional output interface. It does not follow merely by writing a coherent input as a linear combination. In the present reflection witness all error columns point in the same direction s, which is precisely the opposite geometry. The controlled-label comparison therefore does not contradict the sharp square-unitary result and supplies no free extra label or workspace cleanup.

If every tolerance is zero, exact equality on the entire input basis gives E=0 by linearity. Individual zero tolerances force only their own columns to agree. At \(N=1\), \(\min(2,\varepsilon_0)\) is still sharp for square unitaries, using a scalar phase. The reflection-interference example requires \(N\geq2\); in the one-dimensional square case all unitary output vectors differ only by global phase, although the representative-wise operator distance can be nonzero. Isometries into a larger output space remain covered by the bound but need not share that one-dimensional physical equivalence. No output phase is independently optimized for each input in this problem, and probability agreement is not the stated hypothesis. The proof concerns full columns, not scalar entrywise errors, and derives no circuit realization or oracle cost."""


def step(id_, claim, required, conclusion, justification, assumptions=None):
    return {"id": id_, "claim": claim, "assumptions": assumptions or [],
            "required_inputs": required, "conclusion": conclusion,
            "justification": justification}


P1_MAP = {
    "kind": "author_supplied_natural_language",
    "not_extracted_lean_dependencies": True,
    "inputs": [
        {"id": "I1", "statement": "m >= 1, M=2^m; register order and little-endian binary convention.", "kind": "typing_and_convention"},
        {"id": "I2", "statement": "The actual reversible gate list B, exact full clean-input action including gamma_x, and gate counts g_B.", "kind": "assumption"},
        {"id": "I3", "statement": "The positive-exponent normalized Fourier gradient and negative-phase target D_q.", "kind": "definition"},
        {"id": "I4", "statement": "Declared logical X/CNOT/Toffoli/H/dyadic-P gates and clean zero scratch.", "kind": "resource_model"},
        {"id": "I5", "statement": "L >= 1; coherent uses may be interleaved with data-only unitaries.", "kind": "assumption"},
        {"id": "I6", "statement": "For the stability branch only, actual unitary F_tilde, actual inverse, initial vector error <= eta, and otherwise exact circuits.", "kind": "conditional_assumption"},
        {"id": "I7", "statement": "Separate optional boundary replacing I1: m=0, M=1, Q/Y trivial and q_x=0. If a redundant supplier is retained, its entire X/W reversible list and count are still supplied.", "kind": "replacement_case_assumption"},
    ],
    "steps": [
        step("S1", "Descending controlled flips realize a suffix increment on every word.", ["I1", "I4"], "For target i >= j the OLD lower-bit carry is Q_j product_{r=j}^{i-1}Y_r; descending order preserves those controls.", "The binary carry rule AND descending order give addition modulo 2^m; overflow is dropped."),
        step("S2", "Conjunction chains realize each multi-controlled NOT and clean scratch.", ["I4"], "k controls cost 2k-3 Toffolis and k-2 scratch for k>=2; k=1 costs one CNOT.", "Compute k-1-control conjunction, apply target flip, then reverse the unchanged-control computation."),
        step("S3", "The complete adder has an arbitrary-width correctness and cost proof.", ["I1", "S1", "S2"], "ADD preserves Q, adds q to Y modulo M, and restores A; counts m CNOT, m(m-1)(2m-1)/6 Toffoli, max(m-2,0) scratch.", "Compose all weighted increments AND sum all controlled-flip costs; scratch is reused only after its return to zero."),
        step("S4", "Fourier translation gives the exact kickback eigenvalue, including wrap.", ["I1", "I3", "S3"], "T_q G_m=exp(-2pi i q/M) G_m.", "Relabel by z=y+q modulo M; changes by integer multiples of M do not change the exponential."),
        step("S5", "The supplied list provides the actual inverse and complete coherent cleanup.", ["I2", "S3", "S4"], "B;ADD;B-dagger implements D_q, returns QWA to zero and factorizes the gradient on every coherent input.", "B-dagger is the reversed self-inverse gate list; ADD preserves both q and gamma, so inverse cancellation AND the eigenvalue identity apply."),
        step("S6", "The gradient has a concrete product preparation and inverse.", ["I1", "I3", "I4"], "F_m uses m H and m dyadic P gates; F_m-dagger uses their reversed inverses.", "Factor the phase using the little-endian binary expansion of y."),
        step("S7", "Every use and initialization/reset have separate exact ledger entries.", ["I1", "I2", "I4", "I5", "S3", "S5", "S6"], "L times the supplier/inverse/adder counts plus one F_m, and optionally one F_m-dagger; width n+2m+w+max(m-2,0).", "Clean per-use registers can be reused; the nonzero catalyst is not a clean-zero ancilla until its final inverse preparation."),
        step("S8", "A single approximate initial catalyst has a norm-preserved error through all uses.", ["I5", "I6", "S3", "S5"], "Full error relative to ideal data tensor exact G_m is <= eta independent of L; QWA still clean, Y need not factorize.", "All operations form one unitary AND the exact-gradient sector has the required invariant action."),
        step("S9", "Actual approximate-preparation inverse gives a bounded, not exact, clean reset.", ["I6", "S8"], "Full error relative to ideal data tensor all zeros is <= 2 eta (also <=2).", "Triangle inequality combines propagated initial error with norm(F_tilde-dagger G_m - zero)=norm(G_m-F_tilde zero)."),
        step("S10", "One-bit and resource-model boundaries preserve the advertised meaning.", ["I1", "I2", "I4", "S3", "S6", "S7"], "m=1 is one-CNOT Boolean kickback; no supplier efficiency or fixed-finite-gate synthesis follows.", "Evaluate the nonnegative-width formulas at m=1; distinguish the declared ideal gate model and supplied list from additional compilation promises."),
        step("S11", "The explicitly separate zero-bit extension is an identity route.", ["I4", "I5", "I7"], "No catalyst or adder gates are needed and B may be omitted; retaining B and its reverse still costs 2L g_B and any supplier work width.", "The only word has q=0, so its phase is 1. The optional redundant supplied reversible list cancels with its reverse independently of any positive-width carry proof.", ["Use I7 in place of I1; none of S1-S10 is a premise for this boundary."]),
    ],
    "reused_results": [
        {"result": "Source fixed three-bit modular addition and three-control clean-chain pattern.", "consumers": ["S1", "S2", "S3"], "status": "Inspected finite-width substrate only; arbitrary-width proof and counts are derived explicitly here."},
        {"result": "Exact phase-aware program composition and dagger semantics.", "consumers": ["S4", "S5"], "status": "Inspected convention, not a compiled phase-gradient theorem."},
        {"result": "Boolean one-bit phase kickback (qcb-core-plan-519).", "consumers": ["S10"], "status": "Disclosed strict m=1 special case; not counted as the new assessed target."},
    ],
    "reconvergent_branches": [
        {"branches": ["S3", "S4", "I2"], "join": "S5", "meaning": "Correct/clean arithmetic AND Fourier eigenstate AND full reversible supplier are all needed."},
        {"branches": ["S5", "S6"], "join": "S7", "meaning": "Reusable action and actual initial preparation jointly justify amortized costs."},
        {"branches": ["I6", "S8"], "join": "S9", "meaning": "Actual inverse access and initial-state propagation jointly justify the final reset bound."},
    ],
    "case_scopes": {"exact_main": {"steps": ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S10"]}, "approximate_preparation": {"premise": "I6", "steps": ["S8", "S9"]}, "zero_bit_extension": {"replacement_premise": "I7", "excluded_main_premise": "I1", "steps": ["S11"], "note": "The identity route may omit B; retaining a redundant B/B-dagger still costs its gates."}},
}

P2_MAP = {
    "kind": "author_supplied_natural_language",
    "not_extracted_lean_dependencies": True,
    "inputs": [
        {"id": "I1", "statement": "N>=1; U,V are isometries with common finite complex input/output carriers.", "kind": "assumption"},
        {"id": "I2", "statement": "Every epsilon_j>=0 bounds the exact full-output column error norm.", "kind": "assumption"},
        {"id": "I3", "statement": "E=V-U; G_jk=<Ee_j,Ee_k>; inner product conjugate-linear first, induced Euclidean operator norm.", "kind": "definition_and_convention"},
        {"id": "I4", "statement": "Trace distance means one-half the trace norm, with no phase quotient in the vector/operator promise.", "kind": "convention"},
    ],
    "steps": [
        step("S1", "The complete coherent error is a Gram quadratic form.", ["I1", "I3"], "||Ec||^2=c-dagger G c, G=E-dagger E>=0, ||E||^2=lambda_max(G).", "Expand linearity with conjugation in the first argument; maximize the Hermitian quadratic form."),
        step("S2", "Column data give an l2 aggregate bound while isometry gives the cap.", ["I1", "I2", "I3", "S1"], "||E||<=min(2,r), r=sqrt(sum epsilon_j^2).", "Triangle plus Cauchy-Schwarz gives r; both outputs of a unit input have norm one, giving 2."),
        step("S3", "Legal square unitaries saturate every tolerance vector by a case split.", ["I1", "I2", "I3", "S2"], "At r=0 use U=V=I. For r>0, P=|s><s| with s_j=epsilon_j/r and V=I+(exp(i theta)-1)P, |exp(i theta)-1|=min(2,r), attain the bound.", "First separate r=0. In the r>0 branch, orthogonal P/I-P sectors prove unitarity AND individual column calculations prove each promised inequality; division occurs only there."),
        step("S4", "Uniform promises incur the sharp square-root-dimension factor.", ["I2", "S2", "S3"], "Uniform bound min(2,sqrt(N) epsilon), sharp; cap threshold 2/sqrt(N).", "Specialize the nonuniform theorem, with the zero case handled separately."),
        step("S5", "A reflection has vanishing basis-column errors and maximal operator distance.", ["I1", "I3", "S3"], "For uniform s, V=I-2|s><s| has column errors 2/sqrt(N), operator norm difference 2.", "Apply the rank-one projector formula at theta=pi.", ["Use N>=2 for the subsequent interference example."]),
        step("S6", "The operational counterexample is not merely a global-sign witness.", ["I1", "I4", "S5"], "s maps to -s with trace distance 0; h=(s+t)/sqrt2 maps to k=(-s+t)/sqrt2 orthogonal to h, vector distance sqrt2 and trace distance 1.", "t=(e0-e1)/sqrt2 is unit and orthogonal to s; compute inner products AND eigenvalues of |h><h|-|k><k|; a projection onto h distinguishes perfectly.", ["N>=2 as in S5; do not apply this construction at N=1."]),
        step("S7", "Orthogonal error columns are a sufficient additional geometry.", ["I2", "I3", "S1"], "Diagonal G gives ||E||=max_j||Ee_j||; generally G<=b^2 I iff ||E||<=b.", "Spectral order bounds the quadratic form; an explicit retained label forces cross-error inner products to vanish."),
        step("S8", "Zero and one-dimensional cases preserve the exact quantifiers.", ["I1", "I2", "I3", "I4", "S1", "S2"], "r=0 implies E=0 and is attained by U=V=I; N=1 still has the scalar-phase sharp cap, but no orthogonal t in the square one-dimensional output.", "Linearity extends zero columns; for N=1 the unitary is a scalar phase, distinct from larger-output isometries.", ["The r=0 branch excludes division by r in S3; the N=1 branch excludes the N>=2 witness S5-S6."]),
    ],
    "reused_results": [
        {"result": "Finite Hermitian spectral theorem, Cauchy-Schwarz and unitary norm preservation.", "consumers": ["S1", "S2", "S3", "S7"], "status": "Standard finite-dimensional mathematical tools; no new formal verification is claimed."},
        {"result": "Prior B2 retained-label orthogonality mechanism.", "consumers": ["S7"], "status": "Disclosed boundary comparison only; no phase-correction problem is recounted as new."},
    ],
    "reconvergent_branches": [
        {"branches": ["I1", "I2", "S1"], "join": "S2", "meaning": "The isometry cap AND all individual column promises enter the sharp upper bound."},
        {"branches": ["S2", "S3"], "join": "S4", "meaning": "An upper bound and a legal unitary attaining it are both required for sharpness."},
        {"branches": ["S5", "I4"], "join": "S6", "meaning": "The reflection action and precise physical-state metric give an operational witness distinct from global sign."},
    ],
    "case_scopes": {"sharpness_case_split": {"steps": ["S3"], "branches": ["r=0: identical unitaries, no division", "r>0: normalized rank-one phase construction"]}, "zero_tolerance_boundary": {"premise": "r=0", "steps": ["S8"]}, "operational_witness": {"premise": "N>=2", "steps": ["S5", "S6"]}, "one_dimension": {"premise": "N=1", "steps": ["S8"], "excluded_steps": ["S5", "S6"]}},
}


RUBRICS = {
    "P1": [
        ("r1", 1.5, "Derives the negative kickback eigenvalue by a modular change of variable and proves full coherent B/ADD/B-dagger action, including all supplier garbage and clean scratch; an untracked phase or omitted garbage cleanup loses credit."),
        ("r2", 2.0, "Proves the arbitrary-width descending carry-controlled increment and clean conjunction-chain implementation; derives m CNOT, m(m-1)(2m-1)/6 Toffoli and max(m-2,0) scratch. Equivalent exact count expressions earn full credit; finite examples alone do not."),
        ("r3", 1.0, "Constructs the little-endian product preparation and actual inverse using H then P on each bit, with exact phase convention and m+m preparation counts."),
        ("r4", 2.0, "Gives the complete L-use supplier/inverse/adder/preparation ledger and live width, distinguishing reusable nonzero catalyst return from final clean-zero reset; separately charges any interleaved data gates and does not infer supplier efficiency from m output bits."),
        ("r5", 2.0, "Uses one global unitary to prove <=eta full-output error independent of L from initial catalyst error alone, proves <=2eta after the actual approximate-preparation inverse, and explains why exact catalyst factorization/reset need not hold."),
        ("r6", 1.5, "Explains trace-out versus coherent cleanup, actual inverse availability, m=1 and optional m=0, and the distinction between the logical dyadic-phase model, finite words and unproved fixed-finite-gate synthesis/resource guarantees."),
    ],
    "P2": [
        ("r1", 1.5, "Derives the conjugation-correct quadratic form, PSD Gram matrix and largest-eigenvalue characterization; identifies off-diagonal error correlations rather than assuming errors orthogonal."),
        ("r2", 1.5, "Proves min(2,sqrt(sum epsilon_j^2)) using all column promises and the isometry cap, and states the sharp uniform sqrt(N) consequence and cap threshold."),
        ("r3", 3.0, "Constructs and verifies square unitaries attaining the bound for EVERY nonnegative tolerance vector, with r=0 separated, each column promise checked, and both r<=2 and r>2 handled. An arbitrary unconstrained matrix or only a uniform example earns partial credit."),
        ("r4", 2.0, "Provides the uniform rank-one reflection and an explicit orthogonal complement t; computes the distinguishable interference outputs, vector distance sqrt2, half-trace-norm distance 1 and a measurement, while correctly separating the global-sign input's physical trace distance 0."),
        ("r5", 1.0, "Gives a sufficient error-geometry condition such as orthogonal error columns, justified by the Gram matrix, and explains the retained-label boundary without pretending linearity supplies the extra output label."),
        ("r6", 1.0, "Handles zero tolerances and N=1, preserves complete-output/representative-wise assumptions and the distinction from entrywise or probability promises; no circuit or cleanup resource claim is inferred."),
    ],
}

COMMON_ERRORS = {
    "P1": [
        "Using a positive kickback phase with the specified positive Fourier exponent and addition.",
        "Incrementing low bits first while testing changed lower bits as if they were original carry bits.",
        "Charging a multi-controlled NOT as one Toffoli, or leaving its conjunction-chain scratch dirty.",
        "Applying inverse computation only to the output word while ignoring supplier garbage.",
        "Treating a returned gradient state as a clean-zero register, or charging preparation on every reuse without explanation.",
        "Obtaining B-dagger from unsupported forward-only black-box access instead of the supplied reversible gate list.",
        "Multiplying a single initial catalyst state error by L without analyzing the exact global unitary, or conversely claiming the approximate catalyst factorizes exactly.",
        "Promoting finite-word arithmetic and ideal dyadic phase gates to an unproved fixed-finite-gate synthesis or polynomial supplier theorem.",
    ],
    "P2": [
        "Using max_j epsilon_j without controlling cross-column error correlations.",
        "Assuming orthonormal columns of U and V make the difference columns orthogonal.",
        "Using an arbitrary error matrix to claim sharpness while failing the unitary/isometry premises.",
        "Omitting the norm-two isometry cap or dividing by r when all tolerances vanish.",
        "Offering only an overall-sign input as a physical distinguishability witness.",
        "Confusing vector distance 2, vector distance sqrt2, trace norm 2 and trace distance 1.",
        "Silently weakening the full-output Euclidean guarantee to measurement probabilities or independently chosen column phases.",
        "Counting the retained-label orthogonality comparison or the existing entrywise N-epsilon example as the new assessed result.",
    ],
}

BOUNDARIES = {
    "P1": [
        ("m=1", "The catalyst is the minus state; one CNOT and zero Toffoli/scratch implement the adder."),
        ("Explicit m=0 extension", "Target is identity, so all supplier calls can be omitted; a deliberately retained redundant B/B-dagger must still be charged."),
        ("Supplier garbage nonzero or colliding records", "B-dagger restores the exact full record; tracing only happens to preserve coherence within equal-record classes and does not satisfy the general clean interface."),
        ("Approximate catalyst", "QWA still return clean under exact reversible arithmetic, but Y may entangle with data; eta and 2eta are vector-error bounds, not exact resets."),
        ("Approximate gates on every use", "Outside the initial-catalyst-only error model; the no-L factor cannot be transferred without further analysis."),
        ("Gate model", "Dyadic phases are ideal declared logical gates; no optimality, fixed-finite-gate synthesis, connectivity or depth theorem is asserted."),
    ],
    "P2": [
        ("r=0", "Every error column is zero, so E=0; choose identical unitaries without normalizing an absent direction."),
        ("Some epsilon_j=0", "Those columns agree exactly; the rank-one saturating vector has zero corresponding components."),
        ("r>2", "The norm-two isometry cap is active; sharpness need only satisfy, not saturate, each loose column tolerance."),
        ("N=1", "The numerical bound is still sharp by scalar phases; the square one-dimensional case has no two-sector interference witness."),
        ("Retained orthogonal labels", "They can force orthogonal error columns, an additional interface absent from general square-unitary comparisons."),
        ("Phase-quotiented or probability promise", "A different hypothesis; the reference-wise Gram argument cannot silently adopt it."),
    ],
}


def overlap(slot):
    common = [
        {"id": "qcb-core-plan-208", "split": "test_public (reserved; withheld)", "relation": "Not repaired or reassigned. Current main withholds this reserved maxnorm/amplitude-completion target. Root inspected PR114 at ff361a6 and reported its additional single-prepared-column completion boundary; this worker has not independently inspected that branch object."},
        {"id": "assessment-v2/coherent_control_global_relative_phase; assessment-v3/promise_register_protocols", "split": "sealed/public metadata only", "relation": "Root's bounded reservation screen reports coherent-control/global-relative-phase and dirty-control/controlled-conjugation clusters. Full sealed questions are not available in this public workspace, so no complete semantic clearance is claimed."},
    ]
    if slot == "P1":
        related = [
            {"id": "prior-package-99e830bd/B2; candidate:06369e40-07df-4a8c-9105-ac09ebc9b41c", "split": "unassigned candidate", "relation": "B2 specifies abstract negative diagonal correction and explicitly lacks an effective phase supplier. P1's assessed delta is the actual reversible finite-word/gradient construction, arbitrary-width gate ledger and catalyst stability, not the B2 phase iff theorem."},
            {"id": "prior-package-99e830bd/B3", "split": "unassigned candidate", "relation": "B3 optimizes precision under an assumed supplier cost law; P1 supplies a different explicit modular computation/catalyst mechanism and does not re-solve that allocation."},
            {"id": "qcb-core-plan-519", "split": "test_public", "relation": "Boolean one-bit kickback is exactly the disclosed m=1 boundary, not new credit. P1 derives general m, supplier garbage cleanup, a constructive adder and preparation/reuse/reset costs."},
            {"id": "qcb-core-plan-207", "split": "test_public", "relation": "Compute-rotate-uncompute and trace-out boundaries are reused context. P1 changes the actual target and mechanism to a finite-word diagonal phase via a reusable translation eigenstate; amplitude-oracle loading is not retasked."},
            {"id": "qcb-core-plan-209", "split": "test_public", "relation": "Original-entry query/compute/uncompute accounting overlaps as a discipline, but does not supply P1's explicit adder, Fourier catalyst or nonaccumulating initial-catalyst error argument."},
        ]
        delta = "Uniform arbitrary-width modular phase-gradient construction from a supplied reversible finite-word producer, exact macro resources and full garbage cleanup, with an independent-of-use-count initial-catalyst error guarantee."
    else:
        related = [
            {"id": "qcb-core-plan-010", "split": "test_public", "relation": "Already assesses entrywise scalar error and an N-times-entry-error matrix example. P2 assesses full-column Euclidean promises, sharp nonuniform l2 aggregation/sqrt(N) scaling under actual unitarity, and an operationally distinguishable coherent input."},
            {"id": "prior-package-99e830bd/B2; candidate:06369e40-07df-4a8c-9105-ac09ebc9b41c", "split": "unassigned candidate", "relation": "Retained-label orthogonality is used only to explain a contrasting sufficient condition. No phase-correction theorem or weighted phase-error formula is counted anew."},
            {"id": "qcb-core-la-007", "split": "dev", "relation": "Two-column exact linearity is a basic reused ingredient. It does not supply a sharp global error bound or unitary constrained counterexample."},
            {"id": "qcb-core-plan-207", "split": "test_public", "relation": "Discarded-record dephasing is a different channel/cleanup boundary; P2 performs no trace-out and compares complete isometries."},
            {"id": "PR114/plan208 single-column completion boundary", "split": "test_public reserved branch proposal", "relation": "Root reports C_epsilon versus C_-epsilon with first-column error 2epsilon and operator error 2. P2 promises every basis column and proves the sharp sqrt(N) conversion; it neither repairs the reserved core nor re-counts that one-column failure. Branch content remains proposed, not current gold."},
        ]
        delta = "Sharp nonuniform full-basis-column-to-operator error theorem, attained by legal square unitaries for every tolerance vector, plus an orthogonal-output interference witness."
    return {"global_semantic_reconciliation": "pending", "assessed_delta": delta,
            "related_targets": related + common,
            "split_action": "Unassigned pending reconciliation; overlaps with public-test/dev and unresolved candidates forbid a clean training or independence claim.",
            "bounded_review_scope": "Current resolved public core/reader exports, prior B2/B3 and current intake addenda were read. Root-reported open/sealed reservations are marked as such; unavailable sealed questions were not inferred from metadata.",
            "dedup_review_required": True}


def build(slot, answer, reasoning):
    question_path = ROOT / "questions" / f"{slot}.json"
    question = json.loads(question_path.read_text())
    qhash = hashlib.sha256(question_path.read_bytes()).hexdigest()
    result = {k: v for k, v in question.items() if k not in {"schema_version", "source_commit", "freeze_stage"}}
    result.update({
        "schema_version": "qcb.nonlean_cohort_payload.v1",
        "contribution_type": "new_candidate",
        "mathematical_target": overlap(slot)["assessed_delta"],
        "family": "candidate-finite-word-phase-gradient-supplier" if slot == "P1" else "candidate-sharp-columnwise-coherent-error",
        "reference_answer": answer,
        "rubric": [{"id": id_, "weight": weight, "criterion": criterion} for id_, weight, criterion in RUBRICS[slot]],
        "common_errors": COMMON_ERRORS[slot],
        "boundary_cases": [{"case": case, "consequence": consequence} for case, consequence in BOUNDARIES[slot]],
        "difficulty": {
            "D0_facet": "Fourier sign, modular wrap, clean-zero versus reusable catalyst, finite words versus ideal phase gates." if slot == "P1" else "Full-output vectors versus physical states; columnwise versus operator error; exact representative and trace-distance normalization.",
            "provisional_route_band": "D4" if slot == "P1" else "D3",
            "rationale": "Joins an arbitrary-width Boolean construction, coherent supplier cleanup, a Fourier eigenstate, exact resource amortization and global-unitary error propagation." if slot == "P1" else "Requires a Gram characterization, sharp nonuniform upper bound, legal unitary saturation for all tolerances, and a separate physical interference witness.",
            "shortcut_disclosure": "The reversible supplier action is supplied; its algorithmic efficiency is not an assessed target. A supplied unit-cost adder would remove a central requested derivation." if slot == "P1" else "The rank-one phase construction is not supplied in the question. A generic unconstrained error matrix would evade the unitary sharpness obligation.",
            "measured_model_difficulty": False,
        },
        "reasoning_map": reasoning,
        "overlap": overlap(slot),
        "unverified": [
            "Original natural-language derivation only; no Lean execution, kernel replay, axiom audit or production-source change was performed.",
            "Author freeze is awaiting distinct answer-blind derivation and comparison. This author claims no independent review or approval.",
            "Source inspection grounds conventions and explicitly limited formal substrate, not the complete new mathematical target.",
            "Frozen graph identities represent declared source ownership and navigation, not extracted theorem-proof dependencies or new formal theorem closure.",
            "Global semantic deduplication, split assignment, release admission and measured model difficulty/performance remain unresolved.",
            "No paid model run, training, inference experiment, system installation, commit or push was performed by this worker.",
        ],
        "provenance": {
            "author_identity": AUTHOR, "baseline_commit": BASE,
            "frozen_graph_snapshot_id": question["snapshot_id"],
            "frozen_graph_source_commit": "86b9e677566498da04faebcf4e5ed57f177c6bb1",
            "question_only_path": str(question_path.relative_to(ROOT)),
            "question_only_sha256": qhash,
            "question_text_sha256": hashlib.sha256(question["question"].encode()).hexdigest(),
            "question_first_record": "evidence/phase-question-freeze.json",
            "evidence_class": "original_nl_construction_using_inspected_formal_substrate" if slot == "P1" else "original_nl_sharp_bound_and_unitary_counterexample_using_inspected_norm_conventions",
            "source_inspection": question["source_refs"],
            "imports_and_declaration_availability": {
                "source_imports": "ModularAdder3 imports PrimitiveMacros; PrimitiveSemantics supplies phase-aware program/dagger conventions. The chosen P/H/Toffoli logical model is explicitly separate from repository primitive counts." if slot == "P1" else "PrimitiveCircuitPerturbation imports PrimitiveRyPerturbation and ConstructiveHermitePreparation and opens Matrix.Norms.L2Operator; this is a convention anchor, not a columnwise-error implementation.",
                "availability": "All active target/support nodes were checked in the frozen release-v3 snapshot. Current source file bytes match the snapshot input hashes; no snapshot refresh is needed for these limited anchors.",
            },
            "conceptual_graph_relationships": [{"from": "Finite reversible word supplier + exact modular translation + Fourier eigenstate + full inverse" if slot == "P1" else "Complete column error geometry + isometry constraints", "to": "Coherent diagonal phase and resource/cleanup guarantee" if slot == "P1" else "Sharp coherent operator error and observable interference boundary", "relation": "Author-supplied conceptual AND transport; not a formal implication edge."}],
            "justified_mathematical_dependencies": [s["required_inputs"] for s in reasoning["steps"]],
            "graph_anchor_relation": "Formal substrate and conventions only. New arbitrary-width/catalyst/sharpness conclusions have no compiled root claimed here.",
            "review_state": "authored_awaiting_independent_review",
            "external_sources": {"inspected": [], "paper_fidelity_claim": False},
            "license_attribution": "Original English mathematical exposition; source substrate MIT, Copyright (c) 2026 Quantum Block Encoding contributors. Repository LICENSE inspected.",
            "generation": "No model evaluation, paid API, installation, training or Lean execution.",
        },
    })
    out = ROOT / "qa" / f"{slot}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(slot, hashlib.sha256(out.read_bytes()).hexdigest())


if __name__ == "__main__":
    build("P1", P1_ANSWER, P1_MAP)
    build("P2", P2_ANSWER, P2_MAP)
