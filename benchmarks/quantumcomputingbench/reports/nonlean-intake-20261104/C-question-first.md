# C1–C4 question-first independent derivations

Reviewer: nonlean_audit_tensor, a distinct worker in this intake. Source revision: `86b9e677566498da04faebcf4e5ed57f177c6bb1`.

## Exposure seal

Before creating this file I read the repository AGENTS.md, HARNESS.md, substantive-worker skill, theorem-publication, proof-digestion and evidence-routed-memory protocols; then only `_out/cohort-question-only/C1.json` through `C4.json` and their relevant frozen source text. I read the entire frozen HermiteCutRank, TensorTrainCanonical, TensorTrainNormEnvironment and HermiteBernstein modules, plus the RealAmplitudePreparation header and normSq/normalization regions and adjacent proof text. I have NOT opened the original qa payloads, answers, rubrics, reasoning maps, old reviews or self-reviews. The question-only files themselves contain author source metadata and target-node lists; these were visible and are not independent review evidence. This is question-first reconstruction with source access, not source-blind decoding. No Lean, generated Lean, model calls, builds, installations or commits were run. Source bytes and exact question bindings are in C-phase1-bindings.json, whose digest is appended below.

## C1: shifted-polynomial factorization

Let q(z)=sum_{k=0}^d c_k z^k, inserting zero coefficients above the degree (and for the zero polynomial). The binomial identity gives

q(a+b)=sum_{i=0}^d [sum_{k=i}^d c_k binom(k,i) a^(k-i)] b^i.

Set a_i(a)=sum_{k=i}^d c_k binom(k,i) a^(k-i), A(x,i)=a_i(u(x)) and B(i,y)=v(y)^i, for i=0,...,d. Then (AB)(x,y)=sum_i A(x,i)B(i,y)=q(u(x)+v(y)). Equivalently a_i(a) is the coefficient of X^i in the translated polynomial q(a+X), i.e. the Taylor polynomial at shift a. This requires no derivatives, no convergence and no injectivity of u or v. Only d+1 polynomial powers occur, regardless of index-set cardinalities.

For arbitrary index sets X,Y, regard a column as a function in R^X. Every column F(-,y) is a linear combination of the d+1 functions A(-,i); hence the algebraic dimension of the column span is at most d+1. Every finite submatrix consequently has ordinary matrix rank at most d+1 as well. This defines the unrestricted algebraic rank meaning explicitly; an infinite array need not define an operator on any chosen normed sequence space. For empty X or Y the column-space rank is zero; for d=0 there is one factor coordinate; for q=0 the factors still exist and rank is zero.

Source boundary: the frozen `polynomial_add_factorization` accepts arbitrary row and column types and only the inner type is finite. The cited `FactorsThrough.rank_le` and `polynomial_add_rank_le` ALSO have `[Fintype beta]`, a finite-column hypothesis. Therefore the unrestricted column-span argument above is an elementary NL extension, not literally the compiled source theorem's full interface. No arithmetic, state-preparation or gate-resource statement follows.

## C2: gauges and canonical rows

For each prefix k define P_A(s_1,...,s_k)=A_1^{s_1}...A_k^{s_k}. Induction using matched bond sizes and G_k G_k^{-1}=I gives

P_B(s_1,...,s_k)=G_0^{-1} P_A(s_1,...,s_k) G_k.

The induction starts with I=G_0^{-1}IG_0, so it also handles k=0. For the full word, endpoint fixing G_0=G_n=I gives P_B(s)=P_A(s) entry by entry. Thus f_B=f_A, S_B=sum_s f_B(s)^2=S_A and sqrt(S_B)=sqrt(S_A). Fixing both endpoint matrices is exactly what removes the leftover boundary action; without it the product is G_0^{-1}P_A(s)G_n, which need not have the same scalar amplitude. Accidental equality is possible (e.g. cancelling scalar endpoint factors), so identity endpoints are sufficient, not logically necessary for a particular train.

Writing inverse transpose as G^{-T}, the transformed local row Gram is

sum_t B_j^t(B_j^t)^T = G_{j-1}^{-1} [sum_t A_j^t G_j G_j^T (A_j^t)^T] G_{j-1}^{-T}.

For n=2 with all dimensions one choose A_1^0=A_2^0=[1], A_1^1=A_2^1=[0], and G_1=[2]. The original train is right-canonical, while the transformed row Grams are [4] and [1/4]. Its sole nonzero word amplitude remains 1. Thus arbitrary invertible gauges preserve global amplitudes but can destroy both local canonical equations.

If all internal gauges are orthogonal (GG^T=I), the fixed endpoints are orthogonal too. With original canonicality the bracket becomes I, and the outside product G_{j-1}^{-1}G_{j-1}^{-T}=I. Thus all transformed cores are canonical.

Conversely suppose BOTH trains are right-canonical and G_n=I. Starting at j=n, or inductively at any j with G_jG_j^T=I, the local equation becomes I=G_{j-1}^{-1}G_{j-1}^{-T}. Multiplying on the left by G_{j-1} and on the right by G_{j-1}^T gives G_{j-1}G_{j-1}^T=I. Backwards induction proves orthogonality of every internal gauge (and the initial one if it had not already been fixed). No cancellation through A_j, nonzero-state assumption, full-rank assumption or global uniqueness claim is needed.

At n=0 there is one empty word, product I_1, amplitude 1, mass and norm 1, and no local equations or internal gauges. At n=1 there are no internal gauges and B=A. A zero-dimensional endomorphism has the unique identity/inverse and is orthogonal; all product identities still hold with empty sums. If an internal bond is zero then every full contraction is zero, so S=0. Moreover with r_0=1 no entirely right-canonical train can contain a zero internal bond: at the first transition from a positive bond to zero, the preceding row Gram is zero rather than I. Thus that conditional canonicality premise is unrealizable in this case, whereas unconditional amplitude/mass invariance remains meaningful. No additional rank premises are justified.

Source boundary: the source supplies the chain ordering, slice absorption and canonical row semantics; it does not contain a named all-length gauge theorem. The gauge identities, counterexample and necessity proof here are independently derived NL algebra, not newly certified Lean roots.

## C3: cross environments and arbitrary boundaries

For a suffix after bond j, let P_{A,j}(u) and P_{B,j}(u) denote its ordered products, ending in common dimension r. A backwards induction proves

H_j=sum_{u in {0,1}^{n-j}} P_{A,j}(u) P_{B,j}(u)^T.

At j=n this is the one empty product I_r I_r^T=I_r. The induction expands H_j in the update and uses (B_j^t P_{B,j}(u))^T=P_{B,j}(u)^T(B_j^t)^T; associativity and finite distributivity combine (t,u) into the next suffix word. Hence

H_0(a,c)=sum_s sum_{b=1}^r P_A(s)_{ab}P_B(s)_{cb}.

The terminal sum is matrix multiplication's contraction index; terminal labels are retained as emitted coordinates, so omitting b generally loses mass and correlations. Even in an identical train an off-diagonal entry is the inner product of the emitted vectors from two distinct initial basis labels, not a sum of squares of one amplitude row. A two-train diagonal can also be negative.

Finite rearrangement gives

<Phi_A(v),Phi_B(w)>=sum_{s,b}(sum_a v_a P_A(s)_{ab})(sum_c w_c P_B(s)_{cb})=sum_{a,c}v_a H_0(a,c)w_c=v^T H_0 w.

Equivalently form K_A whose rows are initial labels and whose columns are pairs (s,b); then H_0=K_A K_B^T and Phi_A(v)=K_A^T v. For A=B, E_0=K_AK_A^T is symmetric and v^T E_0v=||K_A^Tv||^2>=0, proving positive semidefiniteness and the arbitrary-boundary norm formula. If E_0v=0 then the quadratic form is zero and every squared coordinate of K_A^Tv vanishes. Conversely if all emitted coordinates vanish, K_A^Tv=0 and E_0v=K_A(K_A^Tv)=0. Neither implication divides by a mass; zero vectors and zero trains are included. Canonicality would imply further identities but is not used.

A square cross environment need not be PSD: at n=1 with all relevant bonds dimension one take A_1^0=[1], B_1^0=[-1] and both t=1 slices zero. Then H_0=[-1], whose quadratic form at 1 is -1. Square cross environments need not even be symmetric.

At n=0, p_0=q_0=r, H_0=I_r, the emitted vector is the boundary itself and the pairing is v^Tw. If r=0 or an internal bond is zero (n>0), full products have zero entries or empty terminal coordinates, and H_0=0, consistently with all formulas. If p_0 or q_0 is zero the corresponding rectangular equation is vacuous on the empty rows/columns. For zero trains the same calculation gives zero environment/emissions. These cases do not require a normalized or scalar boundary.

Source boundary: the frozen `gram_eq_sum` proves the identical-train matrix identity, with all terminal labels implicit in matrix multiplication. The rectangular cross version, PSD/kernel consequences and arbitrary two-boundary pairing are NL extensions. `chainMass` already retains an arbitrary initial vector; scalar `norm` theorems specialize to bonds 1 and do not alone prove the rectangular extension.

## C4: Bernstein perturbations and normalized states

For 0<=t<=1 every factor in binom(d,r)t^r(1-t)^(d-r) is nonnegative, including 0^0=1. The binomial theorem yields sum_{r=0}^d B_{d,r}(t)=(t+(1-t))^d=1, including d=0 and both endpoints.

With e_r=ctilde_r-c_r, the triangle inequality and nonnegative partition give |ptilde(t)-p(t)|<=sum_r |e_r|B_{d,r}(t)<=eta. Therefore ||x-y||_2^2<=M eta^2 and ||x-y||_2<=delta:=eta sqrt(M). Positive mass implies ||x||_2>=sqrt(m)>0. The reverse triangle inequality gives

||y||_2>=||x||_2-||x-y||_2>=sqrt(m)-eta sqrt(M)>0.

Thus both normalizations are defined and delta<sqrt(m)<=||x||_2 verifies every premise of the supplied normalization interface. It yields

||x/||x||_2-y/||y||_2||_2<=2||x-y||_2/||x||_2<=2eta sqrt(M)/sqrt(m).

Under the realizable positive-mass premises M>=1. For 0<epsilon<2, the sufficient condition 0<=eta<=epsilon sqrt(m)/(2sqrt(M)) makes the last bound at most epsilon and also gives delta<=epsilon sqrt(m)/2<sqrt(m), hence a strictly positive lower bound for y. No division by sqrt(M) is meaningful at M=0.

At t=0 only B_{d,0}=1 survives, and at t=1 only B_{d,d}=1 survives; this remains true at d=0, where these are the same index. Consequently an actually sampled endpoint with |c_0|>=a>0 or |c_d|>=a>0 contributes at least a^2 to ||x||^2, so m=a^2 is valid. Repeated sample locations contribute repeatedly; only one such endpoint is required for this bound. Signed coefficients and values are retained, as the convex estimate bounds a perturbation rather than demanding p>=0. At eta=0, x=y and the normalized error is zero. If the original sampled mass is zero then x=0, its normalization is undefined, and no result above applies. At M=0 the squared mass is zero, so the positive-mass hypotheses contradict one another; it is not an example satisfying this theorem.

To show why mass is indispensable, take d=1, M=2, sample points 0 and 1, and for h>0 use c=(2h,0), ctilde=(2h,h), eta=h, m=4h^2. Then x=(2h,0), y=(2h,h), coefficient errors are bounded by h, and eta sqrt(M)=h sqrt(2)<2h=sqrt(m), so even the strict perturbation premise holds at every h. Yet the normalized vectors are (1,0) and (2,1)/sqrt(5), with fixed error sqrt(2-4/sqrt(5))>0 as eta=h tends to zero and m tends to zero. This is stronger than a sign-flip example outside the strict premise.

Source boundary: Bernstein basis positivity, unity and coefficient convex bounds are present in the frozen module; endpoint-zero evaluation is explicit. Endpoint-one evaluation follows from the displayed formula. RealAmplitudePreparation supplies positive-mass normalization semantics on qubit-indexed tables, not the arbitrary-M stability bound. The latter is explicitly supplied by the question and is not a source theorem or a local newly compiled root. No gate cost, storage/runtime or evaluation-error conclusion is claimed.

## Exact phase-one bindings

```json
{
  "sealed_at_utc": "2026-11-04T08:50:23.933756+00:00",
  "question_only_payload_sha256": {
    "C1": "51ebd95c8875a3e72ded0a3edbc9e1b1bdc4a5f0a72a52f873c71a9a84ec41f4",
    "C2": "4fb2e6eedb946fc6a3c5d2908c6cc3fa2439804326d3a9901098cfbdfd3ba054",
    "C3": "9fbeae49b9aa561eca3952bc53e9f2a6489e7b76a644437ffe8dfeb56e19276e",
    "C4": "d8055f623b417d5e5b05add0401332a9c43511b5b0f1668df32789995911a526"
  },
  "question_utf8_sha256": {
    "C1": "5bf5f1b1c1c9fef2745ed19d82afb769865f4c9ba83230f9beee76dc6e62dc18",
    "C2": "267dd3396f5543531d781e4b6611d46d5c4348947b9f8e8ddd1baffd71b7cb2e",
    "C3": "776439a16abc8b20a757a0dc1e0a238a6defc29cf18d1dfb51cecf158a12720b",
    "C4": "ff9187905d07cd57e1adad33ff98abc17ff7c7c037ec8d7254ea176aa4d0a51e"
  },
  "frozen_sources": {
    "QuantumBlockEncoding/HermiteCutRank.lean": {
      "raw": "c0f038bd889c77163967c71df5f5987082f4b79ab7db2b7822efcdda7234aaf2",
      "lf": "c0f038bd889c77163967c71df5f5987082f4b79ab7db2b7822efcdda7234aaf2",
      "bytes": 11161
    },
    "QuantumBlockEncoding/TensorTrainCanonical.lean": {
      "raw": "b8d1eb0651708ac2496be306e2d4b6f3025f7ea4d35a8c6907de02b89d1d981f",
      "lf": "b8d1eb0651708ac2496be306e2d4b6f3025f7ea4d35a8c6907de02b89d1d981f",
      "bytes": 15386
    },
    "QuantumBlockEncoding/TensorTrainNormEnvironment.lean": {
      "raw": "e684550c248817ac77e03a23e0af86d3b2c7f3d8b09bcdb2385702624f5ebe6c",
      "lf": "e684550c248817ac77e03a23e0af86d3b2c7f3d8b09bcdb2385702624f5ebe6c",
      "bytes": 6063
    },
    "QuantumBlockEncoding/HermiteBernstein.lean": {
      "raw": "661618d9c10826491ee293c7c411ac2d55056426739f4bbfd3e7c410c05e4bff",
      "lf": "661618d9c10826491ee293c7c411ac2d55056426739f4bbfd3e7c410c05e4bff",
      "bytes": 20734
    },
    "QuantumBlockEncoding/RealAmplitudePreparation.lean": {
      "raw": "a6ded7e65a7e42d5724529befb48eefc9505814136206dd96248fb59b3c45efa",
      "lf": "a6ded7e65a7e42d5724529befb48eefc9505814136206dd96248fb59b3c45efa",
      "bytes": 19157
    }
  }
}
```
