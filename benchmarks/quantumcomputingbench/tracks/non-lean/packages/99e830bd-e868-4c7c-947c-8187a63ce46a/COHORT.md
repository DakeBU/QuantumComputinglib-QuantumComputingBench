# State-preparation foundations and composition cohort

Twelve proposed contribution packets: four existing-core refinements and eight unadmitted candidates. This rendering is derived from the authoritative JSON payloads. Current exact-content review status is in `manifest.json` and the review reports; author-time uncertainty statements are preserved unchanged. No benchmark admission, new Lean verification or measured model difficulty is implied.

| Slot | Target | Identity kind |
| --- | --- | --- |
| A1 | [Exact normalization with the positivity boundary exposed](#a1) | existing_core_view |
| A2 | [Normalization stability and failure at vanishing mass](#a2) | new_candidate |
| A3 | [From an approximate clean block to a normalized accepted state](#a3) | new_candidate |
| A4 | [Exact half-angle rotation distance on any physical wire](#a4) | existing_core_view |
| B1 | [Local clean columns determine the full chronological run](#b1) | existing_core_view |
| B2 | [A phase for each prepared branch becomes a relative phase](#b2) | new_candidate |
| B3 | [Allocate precision across reused rotation parameters](#b3) | new_candidate |
| B4 | [Transport tensor-word amplitudes through physical bit reversal](#b4) | new_candidate |
| C1 | [Explicit shifted-polynomial factors and the degree-controlled rank bound](#c1) | existing_core_view |
| C2 | [Internal tensor-train gauges preserve amplitudes but need not preserve canonical rows](#c2) | new_candidate |
| C3 | [Tensor-train cross environments, Gram positivity and arbitrary initial boundaries](#c3) | new_candidate |
| C4 | [Bernstein coefficient perturbations to normalized sampled-state error](#c4) | new_candidate |

## A1

**Exact normalization with the positivity boundary exposed**

Core: `qcb-core-sp-006`. Split: `test_public`. Author: `/root/author_normalization`. [Authoritative payload](qa/A1.json).

### Mathematical target

The finite real sum-of-squares normalization identity, isolating positivity for cancellation from nonnegativity for the square-root identity.

### Assumptions

- the total squared norm S is strictly positive
- entries are real; normalization is by division by sqrt(S)

### Conventions

- normSq is the sum of squared entries; sqrt is the real nonnegative square root

### Question

Let f be a finite real amplitude table whose total squared Euclidean norm S = sum_b f(b)^2 is strictly positive. Prove that dividing every entry by sqrt(S) yields an exactly normalized state, i.e. sum_b (f(b)/sqrt(S))^2 = 1, and identify exactly where strict positivity of S is used.

### Reference answer

Write B for the finite index set of the table and put r=sqrt(S). Every f(b)^2 is nonnegative, so S>=0 follows from the definition of S before using the stronger premise S>0. The defining nonnegative square root therefore satisfies r^2=S. Strict positivity gives r>0 and hence r!=0; it also gives S!=0. These nonvanishing facts make the divisions and the final cancellation legitimate.

For every b, (f(b)/r)^2=f(b)^2/r^2. Since r is the same scalar for every b, finite distributivity gives
sum_(b in B) (f(b)/r)^2 = [sum_(b in B) f(b)^2]/r^2 = S/S = 1.
Thus the normalized real amplitude table has squared Euclidean norm one. Viewed as a complex amplitude vector by the usual inclusion of the reals, it has the same unit norm.

The roles of the hypotheses are separate: real squares and finiteness give nonnegative S and the finite-sum algebra; S>=0 suffices for (sqrt(S))^2=S; S>0 is used to exclude the zero denominator and justify S/S=1. Individual entries may be positive, negative or zero. In particular, positivity of every entry is unnecessary.

For the boundary diagnosis, if S=0, nonnegative summands force every f(b)=0, so no unit vector proportional to f exists. Ordinary normalization f/sqrt(S) is then undefined. An empty index set also has S=0, so it is excluded by the premise rather than an active positive-mass example. A zero-qubit table has one index, not an empty index set: a single nonzero entry c normalizes to c/|c|, which is -1 for c<0. This is an exact statement about the amplitude table, not a theorem that any particular preparation circuit loads arbitrary signed amplitudes. The inspected circuit first-column theorem has a separate nonnegative-entry premise. Under the source language's totalized real division, the zero table divided by zero evaluates to the zero table, whose squared norm is still zero; this does not extend the unit-state theorem to S=0.

### Partial-credit rubric

Score out of 10. Credit mathematically valid alternative derivations; the stated criteria assess correctness, not wording.

| Points | Criterion |
| --- | --- |
| 3 | Derives (f(b)/sqrt(S))^2=f(b)^2/(sqrt(S))^2 and factors the common denominator out of the finite sum; partial credit for correct entrywise algebra without the finite-sum step. |
| 2 | Derives S>=0 from the real sum of squares and uses the nonnegative-square-root identity (sqrt(S))^2=S; does not falsely require all f(b)>=0. |
| 3 | Uses S>0 to establish nonzero sqrt(S) and S, then performs the justified cancellation S/S=1; partial credit for a correct normalization chain with an unexplained cancellation. |
| 2 | Identifies nonvanishing as the exact extra use of strict positivity, distinct from S>=0 for the square root. A correct zero-mass diagnosis can demonstrate this distinction; circuit discussion and source-language division conventions are not required for full credit. |

### Common errors

- Claiming every amplitude must be nonnegative in order to normalize a real vector.
- Saying strict positivity is required for the square-root-square identity itself, instead of for nonvanishing/cancellation.
- Treating a zero-qubit table as an empty table or declaring the zero table a unit vector by assigning 0/0=0.
- Promoting the norm identity to arbitrary-signed circuit first-column correctness.

### Boundary cases

- {"case": "S=0", "resolution": "Outside the active strict-positivity premise; all entries vanish and there is no normalized proportional state."}
- {"case": "Empty index set", "resolution": "The sum is zero, so the active premise cannot hold."}
- {"case": "One-entry / zero-qubit table", "resolution": "For c!=0 the normalized entry is sign(c); this may be -1 without violating the norm identity."}
- {"case": "Mixed signs or some zero entries", "resolution": "Fully admitted whenever at least one entry is nonzero."}

### Difficulty annotation

```json
{
  "D0": {
    "facet": "Finite real squared norm; nonnegative square root; positivity versus nonvanishing; no circuit conclusion.",
    "adds_core": false
  },
  "D1_D4": {
    "provisional_route_band": "D2",
    "rationale": "The assessed work is local finite-sum algebra plus a load-bearing-hypothesis diagnosis. It is not merely lookup of a declaration; importing the exact identity would make a different D1 application route.",
    "measured": false,
    "taxonomy_source": "benchmarks/quantumcomputingbench/tracks/lean/COURSE.md:19-30",
    "not_graph_distance": true
  }
}
```

### Author-supplied reasoning map

These are natural-language mathematical dependencies, not extracted Lean proof-term dependencies. All required inputs at a step are conjunctive.

| Input | Kind | Statement |
| --- | --- | --- |
| i1 | assumption | B is finite and f:B→R. |
| i2 | assumption | S=sum_b f(b)^2. |
| i3 | assumption | S>0. |
| c1 | convention | sqrt is the nonnegative real square root; normalized entries divide by sqrt(S). |

**s1: Establish the square-root domain.**

Assumptions: ["Real entries and a finite sum."]. Required inputs (AND): i1, i2.

Conclusion: S>=0.

Justification: Every real square is nonnegative and finite sums preserve nonnegativity.


**s2: Establish nonvanishing before dividing.**

Assumptions: ["Strict positive mass."]. Required inputs (AND): i2, i3, c1.

Conclusion: r=sqrt(S)>0 and S!=0.

Justification: The positive real square root of a positive scalar is positive.


**s3: Identify the squared denominator.**

Assumptions: ["Only nonnegative mass is needed here."]. Required inputs (AND): s1, c1.

Conclusion: r^2=S.

Justification: Definition of the nonnegative square root.


**s4: Move the common denominator outside the sum.**

Assumptions: ["r!=0 is already established; all sums are finite."]. Required inputs (AND): i1, i2, c1, s2.

Conclusion: sum_b(f(b)/r)^2=S/r^2.

Justification: Apply the quotient-square identity entrywise and distribute division by one constant over the finite sum.


**s5: Join algebra, square root and nonzero cancellation.**

Assumptions: ["S!=0."]. Required inputs (AND): s2, s3, s4.

Conclusion: sum_b(f(b)/sqrt(S))^2=1.

Justification: Substitute r^2=S and cancel S/S.


**s6: Diagnose the excluded zero-mass boundary.**

Assumptions: ["For this diagnostic only replace i3 by S=0."]. Required inputs (AND): i1, i2, c1, s1.

Conclusion: All entries are zero, so normalization is undefined and no proportional unit vector exists.

Justification: A finite sum of nonnegative squares vanishes only when each summand vanishes. This uses no active example violating i3.

Reuse and reconvergence:

```json
{
  "reused_results": [
    {
      "id": "finite_real_sum_of_squares_nonnegative",
      "producer": "elementary algebra, represented locally by normSq_nonneg",
      "consumer_steps": [
        "s1",
        "s6"
      ]
    },
    {
      "id": "nonnegative_real_square_root_identity",
      "producer": "real square-root convention",
      "consumer_steps": [
        "s2",
        "s3"
      ]
    }
  ],
  "reconvergent_branches": [
    {
      "join_step": "s5",
      "branches": [
        "s2",
        "s3",
        "s4"
      ],
      "AND_semantics": "Nonvanishing, the square-root identity and finite-sum algebra are all necessary for this displayed cancellation route."
    }
  ]
}
```

### Sources and evidence boundary

- [QuantumBlockEncoding/RealAmplitudePreparation.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/RealAmplitudePreparation.lean): lines 310-317: theorem normalized_sum_sq (f : PrimitiveBasis n -> R) (positive : 0 < normSq f) : (sum b, (f b / Real.sqrt (normSq f)) ^ 2) = 1, proved by simp_rw [div_pow]; rw [Finset.sum_div]; Real.sq_sqrt (normSq_nonneg f); div_self (ne_of_gt positive) SHA-256 `a6ded7e65a7e42d5724529befb48eefc9505814136206dd96248fb59b3c45efa`. MIT (repository LICENSE)

Complete source checks, separate reading/import/conceptual/dependency records, overlap and uncertainty are in the JSON payload.

- No Lean, kernel, test-module or complete repository build was run by this author. Source existence and source hashes do not verify this natural-language answer.
- At the authoring freeze, independent exact-content mathematical review, semantic deduplication/split reconciliation and admission remain for distinct reviewers and maintainers. Later bound review/admission status belongs to the proposal and integration manifest, not this immutable author record.
- No model difficulty, model performance, source-paper fidelity or benchmark stability is claimed.

---


## A2

**Normalization stability and failure at vanishing mass**

Core: `candidate:e9e64f4c-3b9e-4c6f-958b-bb362c23e605`. Split: `unassigned_pending_reconciliation`. Author: `/root/author_normalization`. [Authoritative payload](qa/A2.json).

### Mathematical target

Derive a relative perturbation bound for normalized finite vectors and exhibit why small absolute error alone cannot control normalized direction near zero.

### Assumptions

- H is a finite-dimensional Euclidean space over R or C with d>=1; x is nonzero.
- The first assertion quantifies over arbitrary nonzero y; the perturbation corollary instead starts with arbitrary y and derives its nonvanishing from 0<=delta and ||x-y||<=delta<||x||.
- For the uniform-domain corollary a known m>0 satisfies ||x||>=m and delta<m.

### Conventions

- N(z)=z/||z|| is defined only for nonzero z; the denominator is the nonnegative Euclidean norm.
- Distances use exact vector representatives, including their phases; no phase optimization or density-matrix metric is implicit.
- The two-dimensional family is a mathematical boundary example; no oracle, circuit, arithmetic precision or efficiency promise is supplied.

### Question

Let H=F^d with F equal to R or C and finite d>=1, with Euclidean norm ||z||=(sum_j |z_j|^2)^(1/2). For nonzero z write N(z)=z/||z||; all distances compare these exact representatives, without minimizing over a global phase.

First prove the reusable statement: for arbitrary nonzero x,y in H,
||N(x)-N(y)|| <= 2||x-y||/||x||.
Then suppose x!=0, y is initially arbitrary, and a real delta satisfies 0<=delta and ||x-y||<=delta<||x||. Prove y!=0 before normalizing it, and deduce
||N(x)-N(y)|| <= min(2, 2 delta/||x||).
Give the uniform consequence on the domain ||x||>=m>0 when 0<=delta<m.

Show that no bound depending only on the absolute error delta and tending to zero with delta can hold uniformly when the reference norm may tend to zero: give an explicit family of real two-dimensional nonzero vectors with ||x_t-y_t||→0 but normalized distance bounded away from zero. Your family must even satisfy ||x_t-y_t||<||x_t|| for every t>0. Explain the boundaries delta=0, delta=||x||, x=0, and dimension zero. State what this result does and does not establish about a quantum state-preparation circuit or finite-bit computation.

### Reference answer

For any vectors u,v the triangle inequality gives ||u||<=||u-v||+||v|| and, after interchanging them, ||v||<=||u-v||+||u||. Hence | ||u||-||v|| |<=||u-v||.

For the first assertion put r=||x||>0, s=||y||>0 and e=||x-y||. Insert y/r between the two normalized vectors:
x/r-y/s = (x-y)/r + y(1/r-1/s).
The two summands have norms e/r and s|1/r-1/s|=|s-r|/r, respectively. The triangle and reverse-triangle inequalities therefore give
||N(x)-N(y)|| <= (e+|s-r|)/r <= 2e/r.
This proves the named shared result normalization-stability-2delta for all nonzero x,y, without any small-error hypothesis.

For the second assertion do not assume y is nonzero. Reverse triangle first gives ||y||>=||x||-||x-y||>=||x||-delta>0. Thus the two normalized vectors are well-defined. Applying the result just proved yields the bound 2delta/||x||. Each normalized vector has norm one, so the triangle inequality independently gives distance at most 2; taking the better bound gives min(2,2delta/||x||). When ||x||>=m>0 and delta<m, the same margin proves y!=0 and the uniform bound is min(2,2delta/m). The lower norm bound, together with the error bound, is what makes this a uniform stability assertion.

A family showing the failure of an absolute-error-only guarantee is, for t>0 in R^2,
x_t=t(1,0), y_t=t(1,1/2).
Their raw difference has norm delta_t=t/2, which tends to zero and satisfies delta_t<||x_t||=t. Their normalized vectors are (1,0) and (2/sqrt(5),1/sqrt(5)), so their normalized distance is the positive constant sqrt(2-4/sqrt(5)). If a universal function omega(delta) tended to zero and bounded these normalized distances, substituting delta_t and taking t→0 would contradict this fixed positive value. The theorem is consistent with this family: its relative error delta_t/||x_t|| remains 1/2.

If delta=0 and x!=0, then y=x and normalized distance is exactly zero. At the threshold delta=||x||, the allowed choice y=0 shows that a non-strict inequality does not ensure normalization exists; it does not say every y at that error threshold is zero. If x=0 then N(x) is undefined, and dimension zero contains no nonzero reference vector, so the theorem's nonzero premise cannot hold there. The normalization map is also not linear. The proof concerns finite-vector geometry only: it supplies neither a loading circuit, coherent phase alignment between independent circuit implementations, a finite-bit algorithm for norms, nor a resource guarantee.

### Partial-credit rubric

Score out of 10. Credit mathematically valid alternative derivations; the stated criteria assess correctness, not wording.

| Points | Criterion |
| --- | --- |
| 3 | Derives the generic nonzero-vector inequality by an explicit normalized-vector decomposition and reverse triangle, retaining denominator \|\|x\|\|. Partial credit for the correct decomposition or a correct equivalent proof with a justified constant. |
| 2 | Proves \|\|y\|\|>=\|\|x\|\|-delta>0 before using N(y); correctly obtains the stated min(2,2delta/\|\|x\|\|) bound using unit norms. |
| 1 | States and justifies the uniform lower-norm consequence min(2,2delta/m) with the margin delta<m, rather than treating a raw error alone as enough. |
| 3 | Gives a concrete two-dimensional family with raw error tending to zero, strict error<reference norm, and a rigorously computed positive normalized-distance limit; connects it to the impossibility of a universal delta-only bound tending to zero. Partial credit for a correct family missing the strict-margin check or limit argument. |
| 1 | Handles the zero-error and equality/zero-domain boundaries accurately and keeps the vector result separate from circuit or finite-bit claims. |

### Common errors

- Normalizing y before establishing y!=0.
- Replacing ||x|| by a constant without a lower-norm promise, or concluding absolute small error implies uniformly small normalized error.
- Using the equality threshold delta=||x|| to assert nonvanishing.
- Cancelling complex phases or silently replacing exact-vector distance by ray distance.
- Giving a counterexample family with only a global sign change and claiming it also proves a phase-quotient obstruction without checking that metric.
- Treating exact normalization source declarations or generic approximation certificates as a formal proof of this new stability theorem.

### Boundary cases

- {"case": "delta=0", "resolution": "y=x!=0 and the exact distance is zero."}
- {"case": "delta=||x||", "resolution": "y=0 is permitted, so strict margin is essential to automatic nonvanishing, although some nonzero y are also allowed."}
- {"case": "x=0 or d=0", "resolution": "No defined N(x); these are excluded domains, not counterexamples to the stated theorem."}
- {"case": "Norms tend to zero while relative error is fixed", "resolution": "The explicit t-family satisfies the strict margin but has a constant normalized separation."}
- {"case": "Complex phases", "resolution": "The same proof uses norm homogeneity and positive real denominators; no phase correction is hidden."}

### Difficulty annotation

```json
{
  "D0": {
    "facet": "Absolute versus relative error, nonzero normalization domain, Euclidean rather than phase-quotient distance.",
    "adds_core": false
  },
  "D1_D4": {
    "provisional_route_band": "D2",
    "rationale": "A local norm decomposition and reverse-triangle argument are joined to one explicit scaling counterexample. No parametric circuit induction or graph-distance surrogate is used.",
    "measured": false,
    "taxonomy_source": "benchmarks/quantumcomputingbench/tracks/lean/COURSE.md:19-30",
    "not_graph_distance": true
  }
}
```

### Author-supplied reasoning map

These are natural-language mathematical dependencies, not extracted Lean proof-term dependencies. All required inputs at a step are conjunctive.

| Input | Kind | Statement |
| --- | --- | --- |
| i1 | assumption | H=F^d is finite-dimensional Euclidean with d>=1 and F=R or C. |
| i2 | assumption | For the corollary, x!=0, y is initially arbitrary and 0<=delta with \|\|x-y\|\|<=delta<\|\|x\|\|. |
| i3 | assumption | For the lower-norm corollary, \|\|x\|\|>=m>0 and delta<m. |
| c1 | convention | N(z)=z/\|\|z\|\| is defined only for z!=0; exact representatives are compared. |

**s1: Prove reverse triangle.**

Assumptions: ["Any u,v in H."]. Required inputs (AND): i1.

Conclusion: | ||u||-||v|| |<=||u-v||.

Justification: Use triangle in both directions and combine the two scalar inequalities.


**s2: Prove the generic shared normalization inequality.**

Assumptions: ["Within this universal proof, u and v are arbitrary nonzero vectors, so r=\|\|u\|\| and s=\|\|v\|\| are positive."]. Required inputs (AND): i1, c1, s1.

Conclusion: For every nonzero u,v, ||N(u)-N(v)||<=2||u-v||/||u||.

Justification: Decompose (u-v)/r+v(1/r-1/s), use norm homogeneity and |s-r|<=||u-v||, then discharge the temporary universal nonzero hypotheses.


**s3: Establish the perturbed denominator.**

Assumptions: ["The strict perturbation margin."]. Required inputs (AND): i2, s1.

Conclusion: ||y||>=||x||-delta>0, hence y!=0.

Justification: Apply reverse triangle before any use of N(y).


**s4: Specialize the shared result and combine with the unit-vector cap.**

Assumptions: ["Both denominators are positive."]. Required inputs (AND): i1, i2, c1, s2, s3.

Conclusion: ||N(x)-N(y)||<=min(2,2delta/||x||).

Justification: Apply s2, substitute ||x-y||<=delta, and separately apply triangle to two unit vectors.


**s5: Make stability uniform on a norm-bounded domain.**

Assumptions: ["m>0."]. Required inputs (AND): i2, i3, s3, s4.

Conclusion: ||N(x)-N(y)||<=min(2,2delta/m).

Justification: Replace the positive denominator ||x|| by its lower bound m.


**s6: Compute a scaling family with persistent normalized error.**

Assumptions: ["For this boundary witness use H=R^2 and t>0."]. Required inputs (AND): i1, c1.

Conclusion: x_t=t(1,0), y_t=t(1,1/2), delta_t=t/2<||x_t||; normalized distance=sqrt(2-4/sqrt(5))>0.

Justification: Direct Euclidean norms give ||y_t||=t sqrt(5)/2; the scalar t cancels in normalization.


**s7: Rule out a delta-only modulus tending to zero.**

Assumptions: ["A purported uniform omega(delta) tends to zero as delta→0."]. Required inputs (AND): s6.

Conclusion: No such universal vanishing absolute-error bound exists, even under pointwise strict margin.

Justification: Apply omega to delta_t→0; the fixed positive distance from s6 contradicts the claimed limit.


**s8: Check endpoint domains.**

Assumptions: ["Each endpoint is a separate diagnostic, not an active impossible premise."]. Required inputs (AND): i1, i2, c1, s3.

Conclusion: delta=0 forces y=x; equality delta=||x|| allows y=0; x=0 or d=0 makes N(x) unavailable.

Justification: Use definiteness of the norm and the explicit y=0 threshold witness.

Reuse and reconvergence:

```json
{
  "reused_results": [
    {
      "id": "normalization-stability-2delta",
      "producer_step": "s2",
      "consumer_steps": [
        "s4"
      ],
      "external_consumers": [
        "A3",
        "C4"
      ],
      "not_hidden_cross_split_answer": true
    }
  ],
  "reconvergent_branches": [
    {
      "join_step": "s4",
      "branches": [
        "s2",
        "s3"
      ],
      "AND_semantics": "The universal lemma and the independently derived nonzero-y premise must both hold before specialization."
    }
  ]
}
```

### Sources and evidence boundary

- [QuantumBlockEncoding/RealAmplitudePreparation.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/RealAmplitudePreparation.lean): normSq:211-214; normalized_sum_sq:311-317 SHA-256 `a6ded7e65a7e42d5724529befb48eefc9505814136206dd96248fb59b3c45efa`. MIT (repository LICENSE)
- [QuantumBlockEncoding/ConcreteSemantics.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/ConcreteSemantics.lean): StateVector:29-30 SHA-256 `454c0c5e215ca197c5883bedf74882f392d259c7afeadc63912230437698ebe5`. MIT (repository LICENSE)
- [QuantumBlockEncoding/StatePreparation.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/StatePreparation.lean): StatePreparationTarget:19-22; ApproximateStatePreparationCandidate:65-69 SHA-256 `2585a3b5ef2a58a0f7fb33664552e9166373cec2815eddf2542c9db66cb5f52f`. MIT (repository LICENSE)

Complete source checks, separate reading/import/conceptual/dependency records, overlap and uncertainty are in the JSON payload.

- No Lean, kernel, test-module or complete repository build was run by this author. Source existence and source hashes do not verify this natural-language answer.
- At the authoring freeze, independent exact-content mathematical review, semantic deduplication/split reconciliation and admission remain for distinct reviewers and maintainers. Later bound review/admission status belongs to the proposal and integration manifest, not this immutable author record.
- No model difficulty, model performance, source-paper fidelity or benchmark stability is claimed.

---


## A3

**From an approximate clean block to a normalized accepted state**

Core: `candidate:bf862ffc-6597-4fd0-8b37-bf09f4eed230`. Split: `unassigned_pending_reconciliation`. Author: `/root/author_normalization`. [Authoritative payload](qa/A3.json).

### Mathematical target

Compose operator-norm block error, clean-branch geometry and normalization stability into output-state and success bounds, retaining the overlap margin and the cost of repetition.

### Assumptions

- n,m are nonnegative integers; system and ancilla dimensions are 2^n and 2^m, hence nonzero. All procedure workspace is included in the clean ancilla register.
- U is unitary on K tensor H; Jv=|0^m> tensor v and B=J†UJ.
- alpha>0, epsilon>=0, ||A-alpha B||<=epsilon in induced Euclidean operator norm, ||psi||=1, and s=||Apsi||>epsilon.
- For the repetition statement, trials use independent fresh preparations and the same ideal success measurement; input preparation, U and the success test are available operations with separately charged uses.
- The stated normalization-stability inequality is supplied; its nonzero and error-margin premises must be checked before application.

### Conventions

- Registers are ordered ancilla then system; matrix products act on column vectors from the rightmost factor first.
- Success is the projection P=JJ† onto all ancilla and workspace qubits being zero. The rejected branch is not erased or assumed clean.
- alpha is positive and the error convention is ||A-alpha B||<=epsilon; it is not ||A/alpha-B||<=epsilon.
- All vector distances compare exact representatives, with no phase minimization. The success probability follows the Born rule for the specified projector.
- One repetition attempt counts one input preparation, one U call and one success test; no amplitude-amplification, gate, precision or readout-cost theorem is supplied.

### Question

Let n,m be nonnegative integers, H=C^(2^n) the system space and K=C^(2^m) the ancilla space, in the fixed tensor order K tensor H. All workspace of the procedure is included in K and initialized to the computational basis state |0^m>. Define the isometry J:H→K tensor H by Jv=|0^m> tensor v, the projector P=JJ†, and the clean block B=J†UJ of a unitary U on K tensor H. Let A:H→H be a linear operator, let alpha>0 and epsilon>=0, and assume the induced Euclidean operator-norm bound ||A-alpha B||<=epsilon. A system input psi has ||psi||=1. Put s=||A psi|| and assume s>epsilon.

You may use the following supplied result, with all of its premises: for nonzero x,y in a finite-dimensional real or complex Euclidean space, ||x/||x||-y/||y||||<=2||x-y||/||x||; if ||x-y||<=delta<||x|| then y is nonzero.

Derive the full decomposition of UJpsi into its P and I-P branches. For the measurement with outcomes P and I-P, compute the success probability p and the normalized system vector conditional on P, proving every required nonzero statement. Prove
((s-epsilon)/alpha)^2 <= p <= min(1,((s+epsilon)/alpha)^2),
||Bpsi/||Bpsi|| - Apsi/s|| <= min(2,2epsilon/s),
and |p-s^2/alpha^2| <= epsilon(2s+epsilon)/alpha^2.
Explain why s^2/alpha^2 is only a nominal squared amplitude, not necessarily a probability under an approximate block promise, and why clean projection does not imply the whole output has clean ancillas.

If each independent fresh trial performs one preparation of psi with clean ancillas, one application of U and one test of P, derive the expected numbers of each operation until the first success and a bound in terms of s,epsilon,alpha. No inverse, reflection, controlled oracle or finite-bit implementation is granted. Discuss epsilon=0, s=0, the threshold s=epsilon>0, no ancilla qubits m=0, and zero system qubits n=0. Include an explicit admissible unitary witness showing why the strict margin cannot simply be removed. Do not infer universal postselection necessity for every possible procedure producing the same normalized target.

### Reference answer

Because the clean ancilla vector has norm one, J†J=I. Thus P=JJ† is an orthogonal projector, J preserves norms, and J† is a contraction. Unitarity of U implies ||UJpsi||=1 and ||Bv||=||J†UJv||<=||v||. In particular B is a contraction, even though A/alpha need only be close to one.

Set y=Bpsi and ell=(I-P)UJpsi. Then
UJpsi=P UJpsi+(I-P)UJpsi=J Bpsi+ell=Jy+ell,
with J†ell=0 and Jy perpendicular to ell. Hence ||y||^2+||ell||^2=1. The P measurement has success probability p=||PUJpsi||^2=||y||^2. When p>0 the accepted joint vector is J(y/||y||), whose ancillas are exactly clean and whose system vector is y/||y||. The rejected branch ell remains in the full premeasurement output; no deterministic cleanup has been proved.

To justify that p>0, put x=Apsi/alpha and delta=epsilon/alpha. The operator-norm promise and ||psi||=1 give
||x-y|| = ||(A-alpha B)psi||/alpha <= epsilon/alpha=delta.
Also ||x||=s/alpha>epsilon/alpha=delta, since alpha>0 and s>epsilon. Thus x!=0 and the supplied normalization lemma's strict-margin premise holds; equivalently, reverse triangle gives ||y||>=(s-epsilon)/alpha>0. All normalization denominators are now positive.

Triangle and reverse triangle give
(s-epsilon)/alpha <= ||y|| <= (s+epsilon)/alpha.
All terms on the left are nonnegative. Squaring these bounds and combining them with ||y||<=1 proves
((s-epsilon)/alpha)^2 <= p <= min(1,((s+epsilon)/alpha)^2).
The supplied result, applied to x and y, gives normalized distance at most 2(epsilon/alpha)/(s/alpha)=2epsilon/s. Since alpha>0, x/||x||=Apsi/s exactly, without an added phase. Both target and accepted system vectors have norm one, so their distance is independently at most 2. This gives the claimed minimum.

For the probability comparison put r=s/alpha and q=||y||. Reverse triangle gives |q-r|<=epsilon/alpha, and q<=r+epsilon/alpha. Therefore
|p-s^2/alpha^2|=|q^2-r^2|=|q-r|(q+r)
<= (epsilon/alpha)(2s/alpha+epsilon/alpha)
=epsilon(2s+epsilon)/alpha^2.
The reference value s^2/alpha^2 is not automatically at most one. For example, with no ancilla, U=I, alpha=1 and A=(1+epsilon)I for any epsilon>0, the norm error equals epsilon and s=1+epsilon, but the actual probability is one while s^2/alpha^2=(1+epsilon)^2>1. The bound compares real nonnegative quantities; it does not assert a nonexistent exact-block experiment with that nominal probability.

With independent fresh trials, the probability that the first success occurs on trial k is (1-p)^(k-1)p for k>=1. Since p>0, the geometric waiting time T has E[T]=sum_(k>=0) Pr(T>k)=sum_(k>=0)(1-p)^k=1/p. Each specified operation occurs once per trial, so the expected counts of input preparations, U calls and success tests are each 1/p, and each is at most alpha^2/(s-epsilon)^2. This includes the preparation and test costs; if fixed per-call costs are supplied, their sum is multiplied by 1/p. It does not supply amplitude amplification from forward U alone: that needs additional inverse/reflection or other algorithm-specific access and an analyzed stopping rule. It also supplies no finite-bit implementation or gate-cost bound.

For epsilon=0 with s>0, Bpsi=Apsi/alpha exactly, so p=s^2/alpha^2 and the conditional system vector is exactly Apsi/s. Zero error does not force p=1. If s=0, the intended normalized target is undefined; with exact encoding the success probability is zero, while under an approximate promise p is at most min(1,(epsilon/alpha)^2), and any successful vector still has no defined Apsi/s target. The hypotheses s>epsilon>=0 exclude s=0 from the active theorem.

The threshold s=epsilon>0 fails to guarantee success. For any t>0, take one ancilla qubit, U=X tensor I, alpha=1, A=tI, epsilon=t and any unit psi. Then B=0, ||A-alpha B||=t, s=t and p=0. This is an admissible unitary example for the weakened threshold, with a well-defined target Apsi/s=psi but no accepted branch. It does not contradict the strict theorem. For m=0 the ancilla space is one-dimensional, J is the canonical identity, P=I, B=U and p=1; the same estimates hold and ell=0. For n=0 the system is one-dimensional, not empty; all formulas remain valid for scalars and any m. There is no normalized input on a genuinely zero-dimensional system. Finally these success and repetition costs concern the displayed U-and-project procedure. For A=cI with c>0, the normalized target is simply psi and a different procedure may prepare it directly; nothing above proves universal postselection necessity.

### Partial-credit rubric

Score out of 10. Credit mathematically valid alternative derivations; the stated criteria assess correctness, not wording.

| Points | Criterion |
| --- | --- |
| 2 | Derives J†J=I, B contraction, the orthogonal full-output decomposition UJpsi=J Bpsi+ell, and p=\|\|Bpsi\|\|^2; distinguishes full output from the accepted clean branch. |
| 2 | Translates the scaled operator promise to \|\|Apsi/alpha-Bpsi\|\|<=epsilon/alpha and uses s>epsilon and alpha>0 to prove both required nonzero vectors. Partial credit for a correct raw bound without the nonzero-premise check. |
| 2 | Applies the supplied normalization result with the correct x,y,delta to obtain 2epsilon/s and the unit-vector cap; derives the squared success interval with nonnegative lower endpoint and p<=1. |
| 1 | Derives the probability comparison by factoring q^2-r^2 and explains with a valid example or equivalent argument why s^2/alpha^2 need not be a probability. |
| 1 | Derives the geometric mean 1/p and the alpha^2/(s-epsilon)^2 upper bound for all three charged operations; makes no unsupported amplification or finite-bit claim. |
| 2 | Provides an admissible unitary zero-success witness at s=epsilon>0, treats exact/kernel and zero-qubit cases consistently, and keeps procedure-specific postselection distinct from universal necessity. Partial credit for correct endpoint analysis with an incomplete witness. |

### Common errors

- Using epsilon rather than epsilon/alpha for the clean-branch vector error under the stated scaled convention.
- Dropping s>epsilon, dividing by ||Bpsi|| without proof, or replacing it by merely s>0 for approximate inputs.
- Identifying Bpsi or Apsi/alpha with the normalized conditional state or identifying their squared norm with an amplitude.
- Claiming UJpsi has no rejected branch because its projected clean block is controlled.
- Squaring a potentially negative s-epsilon lower bound outside the theorem domain.
- Calling s^2/alpha^2 a probability for every approximate block, or inferring free amplitude amplification from forward U access.
- Treating the conceptual BE-to-SP hyperedge or generic certificate Prop as formal verification of this analytic bridge.

### Boundary cases

- {"case": "epsilon=0 and s>0", "resolution": "Exact conditional target, p=s^2/alpha^2; success can still be small."}
- {"case": "s=epsilon>0", "resolution": "U=X tensor I, A=epsilon I, alpha=1 yields B=0 and p=0 under the weakened premise."}
- {"case": "s=0", "resolution": "Target Apsi/s undefined; exact success zero, approximate success at most (epsilon/alpha)^2, with no target-normalization guarantee."}
- {"case": "m=0", "resolution": "There is one ancilla basis label, J=I canonically, p=1 and no leakage."}
- {"case": "n=0", "resolution": "One-dimensional scalar system; a unit vector exists and formulas remain valid."}
- {"case": "Nominal squared amplitude exceeds one", "resolution": "A=(1+epsilon)I, U=I, alpha=1 is valid for epsilon>0; only p is a probability."}

### Difficulty annotation

```json
{
  "D0": {
    "facet": "Clean projection versus full output; scaled operator error versus normalized-vector error; probability versus amplitude; strict overlap margin.",
    "adds_core": false
  },
  "D1_D4": {
    "provisional_route_band": "D3",
    "rationale": "Joins unitary/projection geometry, operator action, a supplied normalization lemma and a geometric repetition model. Every AND premise is retained; supplying the shared lemma is disclosed rather than counted as independently re-proved depth.",
    "measured": false,
    "taxonomy_source": "benchmarks/quantumcomputingbench/tracks/lean/COURSE.md:19-30",
    "not_graph_distance": true
  }
}
```

### Author-supplied reasoning map

These are natural-language mathematical dependencies, not extracted Lean proof-term dependencies. All required inputs at a step are conjunctive.

| Input | Kind | Statement |
| --- | --- | --- |
| i1 | assumption | H=C^(2^n), K=C^(2^m), n,m>=0; all workspace is in K; Jv=\|0^m> tensor v and P=JJ†. |
| i2 | assumption | U is unitary on K tensor H and B=J†UJ. |
| i3 | assumption | alpha>0, epsilon>=0 and \|\|A-alpha B\|\|<=epsilon in induced Euclidean operator norm. |
| i4 | assumption | \|\|psi\|\|=1 and s=\|\|Apsi\|\|>epsilon. |
| l1 | supplied_obligation | For nonzero x,y, \|\|x/\|\|x\|\|-y/\|\|y\|\|\|\|<=2\|\|x-y\|\|/\|\|x\|\|; a bound \|\|x-y\|\|<=delta<\|\|x\|\| implies y!=0. |
| i5 | assumption | Independent fresh trials each charge one input preparation, one U call and one P test. |
| c1 | convention | Fixed ancilla-system order, exact vector phases, Born probability for the P outcome. |

**s1: Derive the clean isometry and projector identities.**

Assumptions: ["The clean ancilla ket is unit."]. Required inputs (AND): i1, c1.

Conclusion: J†J=I, P=P†=P^2, J preserves norms and J† contracts norms.

Justification: Tensor with a fixed unit vector preserves the inner product; its range projector is JJ†.


**s2: Establish contraction of the clean block.**

Assumptions: ["U unitary."]. Required inputs (AND): i2, s1.

Conclusion: ||Bv||<=||v|| for all v.

Justification: Compose the isometry J, norm-preserving U and contraction J†.


**s3: Split the entire output into orthogonal branches.**

Assumptions: ["Input psi is normalized."]. Required inputs (AND): i1, i2, i4, s1.

Conclusion: UJpsi=J Bpsi+ell, ell=(I-P)UJpsi, J†ell=0, ||Bpsi||^2+||ell||^2=1.

Justification: Use P and I-P, orthogonality and unitarity; no leakage term is discarded.


**s4: Convert operator error to an unnormalized vector error.**

Assumptions: ["alpha>0 and \|\|psi\|\|=1."]. Required inputs (AND): i3, i4.

Conclusion: For x=Apsi/alpha, y=Bpsi and delta=epsilon/alpha, ||x-y||<=delta and ||x||=s/alpha>delta.

Justification: Apply the induced operator norm to psi and divide by the positive normalizer.


**s5: Check the supplied lemma premises and nonzero accepted branch.**

Assumptions: ["Finite complex Euclidean carrier."]. Required inputs (AND): i1, i3, i4, l1, s4.

Conclusion: x!=0, y!=0 and ||y||>=(s-epsilon)/alpha>0.

Justification: The strict margin in s4 supplies l1; reverse triangle also gives the quantitative positive lower bound.


**s6: Identify the success probability and conditioned state.**

Assumptions: ["Born rule and p>0."]. Required inputs (AND): c1, s1, s3, s5.

Conclusion: p=||Bpsi||^2>0 and accepted joint state J(Bpsi/||Bpsi||).

Justification: Normalize the P branch only after s5; J is isometric.


**s7: Bound normalized output error.**

Assumptions: ["Both nonzero vectors and alpha>0."]. Required inputs (AND): i3, l1, s4, s5.

Conclusion: ||Bpsi/||Bpsi||-Apsi/s||<=min(2,2epsilon/s).

Justification: Apply l1 with s4; alpha cancels without phase because it is positive; unit-vector triangle supplies 2.


**s8: Bound success from both sides.**

Assumptions: ["All endpoints in the lower bound are nonnegative."]. Required inputs (AND): i3, i4, s2, s4, s5, s6.

Conclusion: ((s-epsilon)/alpha)^2<=p<=min(1,((s+epsilon)/alpha)^2).

Justification: Triangle/reverse triangle bound ||y||; square and combine with clean-block contraction.


**s9: Compare actual probability with the nominal squared target.**

Assumptions: ["q=\|\|y\|\|>=0 and r=s/alpha>0."]. Required inputs (AND): i3, i4, s4, s6.

Conclusion: |p-s^2/alpha^2|<=epsilon(2s+epsilon)/alpha^2.

Justification: Reverse triangle bounds |q-r|; q+r<=2r+epsilon/alpha and |q^2-r^2|=|q-r|(q+r).


**s10: Account for independent repetitions.**

Assumptions: ["The specified charged operations are available once per independent fresh attempt."]. Required inputs (AND): i5, s6, s8.

Conclusion: Expected count of each operation is 1/p<=alpha^2/(s-epsilon)^2.

Justification: Sum geometric tail probabilities; use the strictly positive success lower bound.


**s11: Diagnose the strict-margin and nominal-probability boundaries.**

Assumptions: ["Each witness uses its explicitly weakened or alternative parameter regime, not the theorem premise s>epsilon when it fails."]. Required inputs (AND): i1, i2, i3, c1.

Conclusion: At s=epsilon>0 a unitary X ancilla gives B=0; approximate A=(1+epsilon)I can have s^2/alpha^2>1.

Justification: Evaluate both finite-dimensional witnesses directly; neither requires extrapolating a graph edge.


**s12: Separate exact, kernel and zero-qubit interpretations.**

Assumptions: ["Endpoint reasoning remains conditional on the stated domains."]. Required inputs (AND): i1, i2, i3, i4, s3, s4, s6.

Conclusion: Exact nonzero branch has p=s^2/alpha^2; s=0 lacks a target; m=0 gives p=1; n=0 is a one-dimensional system.

Justification: Substitute into the definitions without inventing a normalized zero vector or an empty Hilbert-space input.

Reuse and reconvergence:

```json
{
  "reused_results": [
    {
      "id": "normalization-stability-2delta",
      "producer_slot": "A2",
      "supplied_in_question": true,
      "consumer_steps": [
        "s5",
        "s7"
      ]
    },
    {
      "id": "unitary_clean_compression_is_contractive",
      "producer_step": "s2",
      "consumer_steps": [
        "s8"
      ]
    },
    {
      "id": "positive_success_margin",
      "producer_step": "s5",
      "consumer_steps": [
        "s6",
        "s7",
        "s8",
        "s10"
      ]
    }
  ],
  "reconvergent_branches": [
    {
      "join_step": "s6",
      "branches": [
        "s3",
        "s5"
      ],
      "AND_semantics": "A geometrically identified clean branch and its proved nonzero amplitude are both necessary to form the conditioned state."
    },
    {
      "join_step": "s7",
      "branches": [
        "s4",
        "s5",
        "l1"
      ],
      "AND_semantics": "Correct raw error, checked nonzero premises and the supplied stability result all enter."
    },
    {
      "join_step": "s8",
      "branches": [
        "s2",
        "s4",
        "s5",
        "s6"
      ],
      "AND_semantics": "Contraction supplies p<=1; vector error and positive margin supply the squared interval; the probability interpretation supplies p=||y||^2."
    },
    {
      "join_step": "s10",
      "branches": [
        "i5",
        "s6",
        "s8"
      ],
      "AND_semantics": "Independent available trials, positive success and the lower bound are all needed for the claimed operation counts."
    }
  ]
}
```

### Sources and evidence boundary

- [QuantumBlockEncoding/ConcreteSemantics.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/ConcreteSemantics.lean): applyVec:55-58; productRegisterBlockProjection:201-204; clean branch bridge:249-294 SHA-256 `454c0c5e215ca197c5883bedf74882f392d259c7afeadc63912230437698ebe5`. MIT (repository LICENSE)
- [QuantumBlockEncoding/BlockEncoding.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/BlockEncoding.lean): intended scaled norm contract in comments:136-146; approximate candidate and certificate:148-163 SHA-256 `fe06f75a29822e28ccdbfedfb0b0e87f90872620fae7aed359085fad8fae64b4`. MIT (repository LICENSE)
- [QuantumBlockEncoding/RealAmplitudePreparation.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/RealAmplitudePreparation.lean): normalized_sum_sq:311-317, exact real normalization substrate only SHA-256 `a6ded7e65a7e42d5724529befb48eefc9505814136206dd96248fb59b3c45efa`. MIT (repository LICENSE)
- [benchmarks/quantumcomputingbench/manifests/release-v3/snapshot.json](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/benchmarks/quantumcomputingbench/manifests/release-v3/snapshot.json): nodes[id=transport:be-to-sp] and hyperedges[id=transport:be-to-sp], conceptual transport only SHA-256 `71a08777e01af1b6e5bd3dd88ba6443efe9aea41240c09303d4bcc0a7cd8058b`. MIT (repository LICENSE)

Complete source checks, separate reading/import/conceptual/dependency records, overlap and uncertainty are in the JSON payload.

- No Lean, kernel, test-module or complete repository build was run by this author. Source existence and source hashes do not verify this natural-language answer.
- At the authoring freeze, independent exact-content mathematical review, semantic deduplication/split reconciliation and admission remain for distinct reviewers and maintainers. Later bound review/admission status belongs to the proposal and integration manifest, not this immutable author record.
- No model difficulty, model performance, source-paper fidelity or benchmark stability is claimed.

---


## A4

**Exact half-angle rotation distance on any physical wire**

Core: `qcb-core-la-015`. Split: `test_public`. Author: `/root/author_normalization`. [Authoritative payload](qa/A4.json).

### Mathematical target

Prove the signed scalar-times-unitary difference formula for the stated RY convention and preserve its induced operator norm under identity spectators and fixed wire reindexing.

### Assumptions

- Finite-dimensional complex Hilbert spaces unless real amplitudes are explicitly specified
- All basis/register permutations are fixed and applied to both input and output

### Conventions

- Column-vector action; Euclidean induced operator norm for norm claims
- Source inspection only; no fresh formal verification

### Question

Define R(theta)=[[cos(theta/2),-sin(theta/2)],[sin(theta/2),cos(theta/2)]]. Derive the exact operator distance between R(a) and R(b), and prove it is at most |a-b|/2. Why does adding any number of untouched spectator qubits not multiply the distance by a dimension factor?

### Reference answer

All norms below are the Euclidean induced operator norm: ||M||=sup_(||v||=1)||Mv||, on the real plane or its complexification. Direct multiplication using cos^2(theta/2)+sin^2(theta/2)=1 shows R(theta)†R(theta)=I. Hence R(theta) is unitary (real orthogonal) and has operator norm one.

Put c=(a+b)/4 and h=(a-b)/4. The sum-difference identities give
cos(a/2)-cos(b/2)=-2 sin(c) sin(h),
sin(a/2)-sin(b/2)=2 cos(c) sin(h).
Keeping the minus sign of the upper-right entry, this gives
R(a)-R(b)=2 sin(h) [[-sin(c),-cos(c)],[cos(c),-sin(c)]]
=2 sin((a-b)/4) R((a+b)/2+pi).
This is exact matrix equality, including the sign of the real scalar; no phase has been discarded.

Norm homogeneity and the unitary norm-one identity therefore give
||R(a)-R(b)||=2|sin((a-b)/4)|.
Using |sin t|<=|t| proves ||R(a)-R(b)||<=|a-b|/2. The exact distance is always at most 2. In particular, equal angles give zero, a-b=4pi k gives zero for any integer k, and a-b=2pi(2k+1) gives distance 2. The last case differs by a minus sign as an exact matrix, which is not removed in this operator-distance convention.

For r>=0 untouched spectator qubits, the spectator space has dimension d=2^r>=1. In a tensor order with the target first, the difference is
(R(a)-R(b)) tensor I_d = 2 sin((a-b)/4) [R((a+b)/2+pi) tensor I_d].
The bracket is unitary, since its adjoint times itself is I_2 tensor I_d. Its induced operator norm is one on the nonzero tensor-product space; this argument applies to every input, including entangled target-spectator states. Thus the exact same distance holds after the lift. For a different fixed target-wire placement, both lifted gates are conjugated by the same basis-permutation unitary Q. Their difference is Q[(R(a)-R(b)) tensor I_d]Q†, and unitary conjugation preserves the induced norm, again giving the same value. There is no dimension multiplier because a unitary preserves vector length, whatever the dimension. One must not replace the induced norm by a sum of entry magnitudes or a Frobenius norm, which have different dimension behavior.

Zero spectators means d=1 and simply recovers the one-qubit result. A total register with zero qubits has no target wire on which this gate can act; it is not an additional distance-zero case. The result bounds exact matrix perturbation caused by changing a real angle; it does not compute rounded angles, synthesize gates over a discrete gate set, or certify finite-bit resource cost.

### Partial-credit rubric

Score out of 10. Credit mathematically valid alternative derivations; the stated criteria assess correctness, not wording.

| Points | Criterion |
| --- | --- |
| 3 | Derives the quarter-angle matrix identity needed for the sharp norm: either the signed factorization R(a)-R(b)=2 sin((a-b)/4) R((a+b)/2+pi), or D†D=4 sin²((a-b)/4) I for D=R(a)-R(b), or an equivalent complete spectral/induced-norm calculation. Partial credit for correct trigonometric differences or matrix products not fully assembled; do not require a particular proof route. |
| 2 | Uses the established matrix identity to obtain the exact distance 2\|sin((a-b)/4)\|, justifying equality rather than only an upper estimate. Accept orthogonality/unitarity and norm homogeneity, the Gram-matrix calculation, or a correct equivalent spectral/induced-norm argument. |
| 2 | Applies \|sin t\|<=\|t\| with the correct scaling to obtain \|a-b\|/2, retaining exact-vector/matrix phase conventions. |
| 3 | Proves spectator independence by a complete tensor-norm argument (including tensor unitarity, a Gram-matrix identity, or an equivalent induced-norm proof) and a common fixed unitary permutation/reindexing for wire placement. The argument covers all, including entangled, inputs; partial credit for a correct tensor proof without the fixed-placement explanation. |

### Common errors

- Using 2|sin((a-b)/2)| and thereby losing the physical half-angle convention.
- Dropping the sign of the scalar inside the exact factorization; absolute value belongs after taking the norm.
- Using a Frobenius/entrywise dimension bound for the induced operator norm.
- Checking only separable input vectors without a valid operator-norm argument for all joint states.
- Treating a 2pi angle change as identical under an exact matrix metric, or reindexing the two compared gates differently.
- Confusing zero spectators with zero total qubits and a nonexistent target wire.

### Boundary cases

- {"case": "a=b or a-b=4pi k", "resolution": "Exact distance zero."}
- {"case": "a-b=2pi(2k+1)", "resolution": "Exact distance two; the sign difference is retained."}
- {"case": "Zero spectators", "resolution": "Spectator space dimension one, so the one-qubit calculation is unchanged."}
- {"case": "Zero total qubits", "resolution": "There is no target wire; not an active gate instance."}
- {"case": "Entangled spectator input", "resolution": "Covered because the scalar factor multiplies a unitary on the entire tensor space."}

### Difficulty annotation

```json
{
  "D0": {
    "facet": "Physical half angle, exact sign/phase, induced operator norm and fixed spectator/wire placement.",
    "adds_core": false
  },
  "D1_D4": {
    "provisional_route_band": "D2",
    "rationale": "Local trigonometric matrix algebra, unitary norm evaluation and tensor/reindex reasoning. The inherited contract remains unchanged; an exact theorem supplied as an oracle would be a different D1 application route.",
    "measured": false,
    "taxonomy_source": "benchmarks/quantumcomputingbench/tracks/lean/COURSE.md:19-30",
    "not_graph_distance": true
  }
}
```

### Author-supplied reasoning map

These are natural-language mathematical dependencies, not extracted Lean proof-term dependencies. All required inputs at a step are conjunctive.

| Input | Kind | Statement |
| --- | --- | --- |
| i1 | assumption | a,b are real and R(theta) is the displayed half-angle matrix. |
| c1 | convention | Norm means the Euclidean induced operator norm and exact matrices are compared. |
| i2 | assumption | There are r>=0 untouched spectator qubits, and the same fixed basis/wire placement is used for both gates. |
| c2 | convention | Column-vector action; any fixed wire placement is represented by one common unitary permutation Q. |

**s1: Check rotation unitarity.**

Assumptions: ["Real angles."]. Required inputs (AND): i1.

Conclusion: R(theta)†R(theta)=I for every real theta.

Justification: Multiply the two-by-two matrices; use cos^2+sin^2=1 and cancellation of mixed terms.


**s2: Derive the exact signed difference.**

Assumptions: ["Same R convention for a and b."]. Required inputs (AND): i1.

Conclusion: R(a)-R(b)=2 sin((a-b)/4) R((a+b)/2+pi).

Justification: Sum-difference identities produce entries [-sin c,-cos c;cos c,-sin c] with c=(a+b)/4.


**s3: Evaluate the exact induced norm.**

Assumptions: ["The rotation carrier has positive dimension."]. Required inputs (AND): c1, s1, s2.

Conclusion: ||R(a)-R(b)||=2|sin((a-b)/4)|.

Justification: A unitary preserves every vector norm and has induced norm one; scale by the absolute value of the signed scalar.


**s4: Obtain the angle-error bound.**

Assumptions: ["Real sine argument."]. Required inputs (AND): i1, s3.

Conclusion: ||R(a)-R(b)||<=|a-b|/2.

Justification: Use |sin h|<=|h| at h=(a-b)/4.


**s5: Lift the signed factorization to all spectators.**

Assumptions: ["d=2^r>=1 and spectators carry identity."]. Required inputs (AND): i2, s1, s2.

Conclusion: (R(a)-R(b)) tensor I_d is the same scalar times a joint unitary.

Justification: Tensor distribution preserves the difference and scalar, and (R tensor I_d)†(R tensor I_d)=I.


**s6: Place the gate on an arbitrary fixed physical wire.**

Assumptions: ["A common permutation Q is used for both compared gates."]. Required inputs (AND): c1, c2, i2, s3, s5.

Conclusion: The lifted physical distance equals 2|sin((a-b)/4)|, independent of d.

Justification: Conjugating the joint unitary by Q preserves unitarity; induced norm one applies to all joint vectors, not merely product inputs.


**s7: Transfer the same linear bound and diagnose endpoints.**

Assumptions: ["Exact phase convention and a valid target wire."]. Required inputs (AND): i1, i2, c1, s3, s4, s6.

Conclusion: Spectator distance<=|a-b|/2; 4pi differences vanish, odd 2pi differences have distance 2; r=0 is allowed.

Justification: Substitute the sine values and note d=1 for zero spectators; a zero-total-qubit carrier has no gate target.

Reuse and reconvergence:

```json
{
  "reused_results": [
    {
      "id": "dimension-free-ry-distance",
      "producer_steps": [
        "s3",
        "s6",
        "s7"
      ],
      "external_consumers": [
        "B3"
      ],
      "not_hidden_cross_split_answer": true
    },
    {
      "id": "scalar_times_unitary_norm",
      "producer": "elementary induced norm identity",
      "consumer_steps": [
        "s3",
        "s6"
      ]
    }
  ],
  "reconvergent_branches": [
    {
      "join_step": "s3",
      "branches": [
        "s1",
        "s2"
      ],
      "AND_semantics": "Exact factorization and unitary norm one both enter the exact distance."
    },
    {
      "join_step": "s6",
      "branches": [
        "s5",
        "c2"
      ],
      "AND_semantics": "An untouched-spectator unitary lift and the same fixed wire permutation are both required for this dimension-free placement argument."
    }
  ]
}
```

### Sources and evidence boundary

- [QuantumBlockEncoding/PrimitiveRyPerturbation.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/PrimitiveRyPerturbation.lean): difference_factor28-37; liftedRy factor54-59; distance61-79 SHA-256 `57ad888af7a81ac5067f6655160fecf1f197a91b0414bc5e510786b9eed27e32`. MIT (repository LICENSE)

Complete source checks, separate reading/import/conceptual/dependency records, overlap and uncertainty are in the JSON payload.

- No Lean, kernel, test-module or complete repository build was run by this author. Source existence and source hashes do not verify this natural-language answer.
- At the authoring freeze, independent exact-content mathematical review, semantic deduplication/split reconciliation and admission remain for distinct reviewers and maintainers. Later bound review/admission status belongs to the proposal and integration manifest, not this immutable author record.
- No model difficulty, model performance, source-paper fidelity or benchmark stability is claimed.

---


## B1

**Local clean columns determine the full chronological run**

Core: `qcb-core-sp-007`. Split: `test_public`. Author: `/root/author_coherence`. [Authoritative payload](qa/B1.json).

### Mathematical target

Prove the unchanged all-length clean-column transfer identity by induction and identify precisely which local columns it does not use.

### Assumptions

- the only hypothesis is clean-column equality of each stage with the corresponding tensor core; no global state action is assumed
- the boundary is an explicit bond vector supplied to the run

### Conventions

- the last emitted core multiplies on the left (same order as circuit evaluation)
- transfer at length 0 is the identity matrix

### Question

In the sequential bond construction, a complete state after n emitted bits is produced by applying stage matrices in order, starting from an explicit bond boundary vector. Assume for each stage index t and each clean input column (fresh bit input = 0, bond input a) the stage entry equals the corresponding tensor core entry K t. Prove by induction on n that the full run amplitude at bit word x and final bond label b equals the matrix-vector product of the chronological transfer contraction of the cores with the boundary, (transfer K n x) applied to the boundary, read at b. State precisely which columns of the stages are therefore irrelevant.

### Reference answer

Let B be the finite set of bond labels, and write a physical bit word of length n as x=(x_0,...,x_{n-1}), in increasing wire order. Matrix rows are outputs and columns are inputs. Write β:B→C for the supplied boundary, U_t[(s,b),(r,a)] for a local stage, and K_t[(s,b),a] for its clean column. Define the slice A_t(s) by A_t(s)[b,a]=K_t[(s,b),a]. The transfer is T_0(empty)=I and T_{n+1}(x)=A_n(x_n)T_n(x_0,...,x_{n-1}). Thus the last emitted core multiplies on the left.

The one-step collapse is worth deriving rather than assuming a full-run action. Before stage n the fresh-bit-and-bond amplitude at (p,(r,a)) is 1_{r=0}v_n(p,a). The lifted stage has entry 1_{p'=p}U_n[(s,b),(r,a)], because previously emitted bits are passive. At output (x,b), with prefix x^-=(x_0,...,x_{n-1}) and new highest-wire bit x_n, its matrix-vector action is
  Σ_{p,r,a} 1_{p=x^-} U_n[(x_n,b),(r,a)] 1_{r=0} v_n(p,a)
  = Σ_a U_n[(x_n,b),(0,a)] v_n(x^-,a).
Both delta factors matter: one fixes the old prefix; the other selects the zero-input columns. No measurement is involved.

Now prove P(n): for every x of length n and every b∈B, v_n(x,b)=[T_n(x)β]_b. For n=0 there is one empty word, v_0(empty,b)=β_b, and [Iβ]_b=β_b, including an arbitrary unnormalized or zero boundary.

Assume P(n) for every prefix and every bond label. The one-step formula and the clean-column hypothesis give
  v_{n+1}(x,b)=Σ_a K_n[(x_n,b),a]v_n(x^-,a)
                =Σ_a A_n(x_n)[b,a][T_n(x^-)β]_a
                =[A_n(x_n)(T_n(x^-)β)]_b
                =[(A_n(x_n)T_n(x^-))β]_b
                =[T_{n+1}(x)β]_b.
The second equality uses the induction hypothesis for every summed bond label a. Associativity of finite matrix-vector multiplication justifies the fourth equality: both sides expand as Σ_a Σ_c A_n[b,a]T_n[a,c]β_c. The transfer recurrence then closes the induction. This is a chronological product; commuting or reversing its noncommuting factors would change the claimed amplitude.

For any fixed run length, the fresh-bit-input-1 columns of each stage actually used in the run never appear, at any output row. Holding all fresh-bit-input-0 columns fixed while changing the other columns therefore leaves the complete emitted-bit-and-bond vector unchanged. Stages after that length are also unused. The statement does not justify discarding any additional zero-input bond column without a separate support invariant. A particular boundary may cause accidental zeros, but this theorem provides a uniform conclusion for arbitrary boundaries. If stages are required elsewhere to be unitary completions, their remaining columns must still satisfy the unitary constraints; 'irrelevant to this run' does not mean arbitrary independent entries preserve unitarity.

The identity itself requires neither unitarity nor normalized β. It gives full amplitudes, not merely a projection or probabilities, and proves no terminal cleanup, local completion existence, flattened circuit placement, gate count or finite-bit compiler. Those are separate interfaces.

### Partial-credit rubric

Score out of 10. Credit mathematically valid alternative derivations; the stated criteria assess correctness, not wording.

| Points | Criterion |
| --- | --- |
| 1.5 | Establishes the quantified induction invariant and the length-zero case using the explicit boundary and identity transfer; partial credit for a correct base case without the all-bond quantifier. |
| 2.5 | Derives the one-step finite sum by separately collapsing the passive-prefix identity and fresh-zero input, with correct output/input indices; partial credit for the correct single sum without explaining both collapses. |
| 2 | Applies clean-column equality and the induction hypothesis at every summed bond label, preserving the actual prefix and last emitted bit; partial credit for identifying these two substitutions with an indexing slip that does not alter the strategy. |
| 2 | Recognizes the slice times transfer-applied-to-boundary, justifies matrix-vector associativity, and folds the recurrence with the newest slice on the LEFT; no full credit for a reversed noncommuting product. |
| 2 | Identifies fresh-bit-input-1 columns as uniformly unused and distinguishes this from unsupported freedom in zero-input bond columns or unitarity of arbitrary completions; partial credit for correctly naming the unused bit sector alone. |

### Common errors

- Assuming the desired full-run action instead of deriving it from local columns.
- Using an induction hypothesis only at the final b rather than at every intermediate a.
- Multiplying T_n A_n instead of A_n T_n.
- Calling fresh-zero insertion postselection.
- Treating all unused completion entries as independently free while still asserting unitarity.
- Assuming unit norm or terminal-bond cleanup from an algebraic transfer identity.

### Boundary cases

- {"case": "n=0", "consequence": "The empty-word run is β and the empty transfer is I; there is no stage or fresh-bit column to inspect."}
- {"case": "Zero or unnormalized boundary", "consequence": "The identity is linear and remains valid; normalization is not an active assumption."}
- {"case": "Empty bond carrier", "consequence": "There are no output bond labels, so the pointwise claim is vacuous; no normalized quantum state is inferred."}
- {"case": "Inactive padded bond labels", "consequence": "Ignoring their zero-input columns needs the separate support hypotheses; this unchanged core does not add them."}

### Difficulty annotation

```json
{
  "D0_facet": "Distinguish output rows from input columns, clean input from measurement, chronological order and completion freedom. This is a facet of the same core, not another question.",
  "provisional_route_band": "D4",
  "rationale": "An all-length parametric induction uses the one-step amplitude collapse and a universal bond-label invariant. The label follows the inspected construction route, not source size or graph distance.",
  "shortcut_disclosure": "Supplying the exact all-length result would reduce the task to a D1 application; this question asks for its induction.",
  "measured_model_difficulty": false
}
```

### Author-supplied reasoning map

These are natural-language mathematical dependencies, not extracted Lean proof-term dependencies. All required inputs at a step are conjunctive.

| Input | Kind | Statement |
| --- | --- | --- |
| I1 | convention | B is finite, amplitudes are complex, matrices use output rows/input columns; all sums are finite. |
| I2 | convention | v_0(empty,b)=β_b; each later step inserts a zero bit, applies identity on old bits tensor U_n, then regroups the new bit as the highest wire. |
| I3 | assumption | For every t,s,b,a, U_t[(s,b),(0,a)]=K_t[(s,b),a]. |
| I4 | convention | A_t(s)[b,a]=K_t[(s,b),a], T_0=I, and T_{n+1}(x)=A_n(x_n)T_n(x^-). |
| IH | supplied_obligation | Within the successor induction obligation only, assume P(n): v_n(p,a)=[T_n(p)β]_a for every p,a; this is discharged by induction, not a new public hypothesis. |

**S1: The zero-length identity holds.**

Assumptions: []. Required inputs (AND): I1, I2, I4.

Conclusion: P(0).

Justification: v_0=β and Iβ=β.


**S2: Only one prefix and the fresh-zero input survive the one-step matrix sum.**

Assumptions: []. Required inputs (AND): I1, I2.

Conclusion: v_{n+1}(x,b)=Σ_a U_n[(x_n,b),(0,a)]v_n(x^-,a).

Justification: Expand tensor identity and freshZero, then collapse both finite delta sums.


**S3: The successor amplitude is slice applied to the prior transfer vector.**

Assumptions: []. Required inputs (AND): I1, I3, I4, IH, S2.

Conclusion: v_{n+1}(x,b)=[A_n(x_n)(T_n(x^-)β)]_b.

Justification: Use clean columns AND the induction hypothesis for all a.


**S4: The successor induction implication closes in the correct order.**

Assumptions: []. Required inputs (AND): I1, I4, S3.

Conclusion: P(n) implies P(n+1).

Justification: Finite-sum associativity gives (A_n T_n)β, then use the transfer recurrence.


**S5: The full transfer identity holds at every length.**

Assumptions: []. Required inputs (AND): S1, S4.

Conclusion: For all n,x,b, v_n(x,b)=[T_n(x)β]_b.

Justification: Natural-number induction discharges IH.


**S6: Unused-column freedom has the precise clean-input scope.**

Assumptions: []. Required inputs (AND): I2, I3, S2, S5.

Conclusion: Changing fresh-bit-input-1 columns of used stages cannot change any complete run amplitude.

Justification: No such column appears in S2; no support or unitarity theorem is silently added.

Reuse and reconvergence:

```json
{
  "reused_results": [
    {
      "result": "Finite matrix-vector associativity",
      "consumers": [
        "S4"
      ],
      "status": "Elementary finite-sum identity explained explicitly."
    },
    {
      "result": "SequentialBondPreparation.step_apply and transfer/run definitions",
      "consumers": [
        "S1",
        "S2",
        "S4"
      ],
      "status": "Inspected source interfaces reconstructed in prose; no new kernel replay."
    }
  ],
  "reconvergent_branches": [
    {
      "branches": [
        "S1",
        "S4"
      ],
      "join": "S5",
      "meaning": "Base case AND successor implication are both required for the global induction."
    }
  ]
}
```

### Sources and evidence boundary

- [QuantumBlockEncoding/SequentialBondPreparation.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/SequentialBondPreparation.lean): lines 86-110: noncomputable def transfer K | 0,_ => 1 | n+1,x => coreSlice (K n) (x (Fin.last n)) * transfer K n (Fin.init x); theorem run_eq_transfer (U K) (cleanColumns : for all t bit b a, U t (bit,b) (0,a) = K t (bit,b) a) (boundary) (n x b) : run U boundary n (x,b) = (transfer K n x).mulVec boundary b, proved by induction with step_apply, cleanColumns, ih, mulVec_mulVec SHA-256 `ad4542b108d44f196f2a02f78e59b58f43d45b1e890709cf4c22e1222805d5c5`. MIT (repository LICENSE)

Complete source checks, separate reading/import/conceptual/dependency records, overlap and uncertainty are in the JSON payload.

- No Lean execution, kernel replay, axiom audit or production-source modification was performed for this packet.
- At authoring/freeze time, independent blind reconstruction and exact-content comparison were pending; later review status belongs in the package review manifest, not this author claim.
- Source inspection supports the stated interfaces and conventions; it does not formally verify the complete natural-language derivation.
- Frozen graph edges expose imports/ownership, not extracted theorem proof dependencies. Source-semantic legacy debt is not cleared.
- Model difficulty, model performance, global semantic deduplication and release admission remain unmeasured or unresolved.

---


## B2

**A phase for each prepared branch becomes a relative phase**

Core: `candidate:06369e40-07df-4a8c-9105-ac09ebc9b41c`. Split: `unassigned_pending_reconciliation`. Author: `/root/author_coherence`. [Authoritative payload](qa/B2.json).

### Mathematical target

Derive the exact retained-label norm formula, supportwise global-phase criterion and coherent diagonal correction for a finite family of branch preparations.

### Assumptions

- Λ is finite nonempty; H is finite-dimensional and nonzero; |0⟩ and each ψ_λ have norm one.
- The label basis is orthonormal and retained; W acts coherently and preserves its basis label.
- Each V_λ is unitary with exact complete-output action V_λ|0⟩=exp(iφ_λ)ψ_λ; all phases are real.
- The complex coefficients satisfy Σ_λ|c_λ|²=1.
- Exact phase values may be used to specify a mathematical correction, but an effective phase supplier or correction compiler is not assumed.

### Conventions

- Register order is label tensor complete data-and-work output.
- Norms are Euclidean vector norms; exact-vector error and minimization over a common global phase are different questions.
- The actual branch convention is exp(+iφ_λ) multiplying the desired branch, so the correcting label phase has the negative sign.
- No postselection, partial trace or work reset is performed.

### Question

Let Λ be a nonempty finite label set with orthonormal basis {|λ⟩}, and let H be a nonzero finite-dimensional complex Hilbert space. H contains the complete data-and-work output; no register is measured or discarded. Fix a unit clean input |0⟩∈H, unit vectors ψ_λ∈H, and unitary branch implementations V_λ satisfying V_λ|0⟩=exp(iφ_λ)ψ_λ for given real φ_λ. The ψ_λ need not be orthogonal. The label is retained by the controlled operation W=Σ_λ |λ⟩⟨λ|⊗V_λ. For complex coefficients c_λ with Σ_λ|c_λ|²=1, the intended output is Ψ=Σ_λ c_λ|λ⟩⊗ψ_λ.

Compute the actual output Ψ̃ and derive an exact formula for ||Ψ̃-exp(iχ)Ψ||² for every real common phase χ. Use it to give necessary and sufficient conditions, on the populated labels, for (a) exact vector equality and (b) equality up to one global phase. Explain why agreement of all isolated-branch output probabilities is insufficient for either coherent claim. Give an explicit two-label unitary example in which both isolated branches are physically correct but the intended and actual coherent outputs are orthogonal, and specify a label measurement that distinguishes them.

Construct a diagonal unitary acting only on the retained label that restores the intended vector exactly when the phases are known. Explain which phase access and implementation obligations remain: recording phases as classical metadata is not itself a gate. Include zero c_λ, a single populated label and common-phase cases. Do not assume output-state orthogonality, silently quotient the requested norm by phase, or infer cleanup of work not promised by the branch vectors.

### Reference answer

Linearity with the retained label gives
  Ψ̃=W(Σ_λ c_λ|λ⟩⊗|0⟩)=Σ_λ c_λ exp(iφ_λ)|λ⟩⊗ψ_λ.
Both Ψ and Ψ̃ have norm one. Indeed, the vectors |λ⟩⊗ψ_λ are orthonormal across distinct λ because their inner products contain ⟨λ|μ⟩=0; no orthogonality between ψ_λ and ψ_μ is needed. Their individual squared norms equal one.

For any real χ, subtract the specified representative exp(iχ)Ψ before taking the norm. Orthogonality of the retained labels kills every cross term, giving
  ||Ψ̃-exp(iχ)Ψ||²
    =Σ_λ |c_λ|² |exp(iφ_λ)-exp(iχ)|²
    =4 Σ_λ |c_λ|² sin²((φ_λ-χ)/2).
The last identity follows from |e^{ia}-e^{ib}|²=2-2cos(a-b). In particular, the exact-vector error corresponds to χ=0. It is not generally the error after choosing a favorable χ.

All summands are nonnegative. Exact equality Ψ̃=Ψ therefore holds if and only if exp(iφ_λ)=1 for every populated label c_λ≠0, equivalently φ_λ is an integer multiple of 2π on that support. Equality up to one common global phase holds if and only if all exp(iφ_λ) on that support are the same scalar exp(iχ). Necessity follows from the vanishing sum, and sufficiency follows by factoring the common scalar from Ψ̃. Empty coefficients impose no condition. The support cannot be empty because the coefficients are normalized. With one populated label the global-phase condition is automatic, while exact equality still requires its phase to be 1. A common nontrivial phase likewise gives global-phase equivalence but a nonzero exact-vector distance 2|sin(χ/2)|.

An isolated branch state e^{iφ_λ}ψ_λ gives the same probabilities as ψ_λ for every measurement on H. That statement compares one branch at a time and cannot remove different phases from a coherent superposition. For a concrete example take Λ={0,1}, H=C², |0⟩ the first computational basis vector, ψ_0=ψ_1=|0⟩, V_0=I and V_1=-I. Both implementations are unitary, with φ_0=0 and φ_1=π. For c_0=c_1=1/√2 the intended state is |+⟩⊗|0⟩ and the actual state is |−⟩⊗|0⟩. Their inner product is zero and their Euclidean distance is √2. Measuring the label in the {|+⟩,|−⟩} basis yields opposite deterministic outcomes. This example uses equal branch states, so orthogonality of branch outputs is manifestly unnecessary. The reduced data state happens to be the same; the distinction lies in retained-label coherence.

Define D=Σ_λ exp(-iφ_λ)|λ⟩⟨λ|. Its diagonal entries have modulus one, hence D†D=I. Direct substitution gives (D⊗I_H)Ψ̃=Ψ for every coefficient vector c, including zero coefficients. One could instead cancel relative phases to a chosen common reference if only global-phase equivalence were requested, but D as written restores the exact vector.

This is an existence and exact-action statement. The premise that controlled branch access exists is explicit; individual black-box availability does not make control free. Implementing D requires a physical realization of the label-dependent diagonal action, for example by compiling a finite known phase list from classical constants or by coherently evaluating a phase representation. Computation, precision and synthesis costs must be separately specified and charged. Arbitrary exact real phases need not have a supplied finite-string evaluation procedure. Classical metadata alone does not act on a register. If corrections are approximate, the same norm formula applies to their residual phases, but no accuracy or cost is certified here. H includes all work: the proof preserves the complete branch output ψ_λ and does not create cleanup that it lacked.

### Partial-credit rubric

Score out of 10. Credit mathematically valid alternative derivations; the stated criteria assess correctness, not wording.

| Points | Criterion |
| --- | --- |
| 1 | Obtains the actual controlled output by linearity and explains why normalization follows from retained orthogonal labels and unit branch norms. |
| 2.5 | Derives the exact weighted squared-norm formula for arbitrary χ, including absence of cross terms without assuming ψ_λ orthogonal, and the sine expression; partial credit for the correct complex-exponential formula alone. |
| 2 | Proves BOTH directions of the supportwise exact-vector and common-global-phase conditions; partial credit for sufficient conditions only or for one of the two equivalences. |
| 2 | Provides a legal two-label unitary witness, computes orthogonality/error and supplies a distinguishing label interference measurement; partial credit for a correct sign example without the measurement. |
| 1.5 | Constructs the negative-sign diagonal correction, verifies unitarity and cancellation for every input coefficient vector; a phase-list description without an operator/action earns partial credit only. |
| 1 | Separates metadata, effective phase access and implementation costs; handles zero coefficients and one/common populated phase without claiming absent work cleanup. |

### Common errors

- Dropping label-dependent phases because each isolated branch has the right probabilities.
- Replacing the weighted sum by a sum involving overlaps of ψ_λ even though labels remain orthogonal.
- Reporting exact-vector error after silently optimizing over χ.
- Demanding equal phases on labels with zero coefficient.
- Using +φ_λ in the correction instead of -φ_λ.
- Treating stored arbitrary real phases or controlled black-box access as a free effective compiler.

### Boundary cases

- {"case": "One populated label", "consequence": "Global-phase equivalence is automatic; exact equality still depends on that branch phase."}
- {"case": "Zero coefficients", "consequence": "Their phases do not affect this input; a correction valid for every c must still specify all labels."}
- {"case": "Common nonzero phase", "consequence": "All relative phases agree, but exact-vector distance is generally nonzero."}
- {"case": "Equal or nonorthogonal branch states", "consequence": "The formula remains valid because the label supplies orthogonality."}
- {"case": "No populated label or H dimension zero", "consequence": "These are incompatible with the stated normalization premises, not active quantum examples."}

### Difficulty annotation

```json
{
  "D0_facet": "Global versus relative phase, exact vector versus physical state, retained labels and correction access. No extra D0 core.",
  "provisional_route_band": "D3",
  "rationale": "Joins complete branch-action interfaces, controlled linearity and label orthogonality to obtain an exact norm identity, an iff criterion and a coherent correction. The local algebra itself is D2.",
  "shortcut_disclosure": "Supplying the full orthogonal-direct-sum norm result would shorten the main derivation; it is proved here.",
  "measured_model_difficulty": false
}
```

### Author-supplied reasoning map

These are natural-language mathematical dependencies, not extracted Lean proof-term dependencies. All required inputs at a step are conjunctive.

| Input | Kind | Statement |
| --- | --- | --- |
| I1 | assumption | Finite orthonormal retained label basis; common finite H and unit ψ_λ. |
| I2 | assumption | V_λ\|0⟩=e^{iφ_λ}ψ_λ and W=Σ\|λ⟩⟨λ\|⊗V_λ. |
| I3 | assumption | Σ\|c_λ\|²=1 and Ψ=Σc_λ\|λ⟩⊗ψ_λ. |
| I4 | convention | φ_λ and χ are real, exact-vector norm is used, and register order is label⊗H. |
| I5 | convention | The proposed mathematical correction may depend on known φ_λ; effective access and synthesis costs are not supplied. |

**S1: The label-decorated target vectors are orthonormal, and Ψ is normalized.**

Assumptions: []. Required inputs (AND): I1, I3.

Conclusion: ⟨λ⊗ψ_λ,μ⊗ψ_μ⟩=δ_{λμ}; ||Ψ||=1.

Justification: Factor tensor inner products; branch unit norms handle λ=μ.


**S2: Controlled linearity fixes actual amplitudes and their phase-referenced difference.**

Assumptions: []. Required inputs (AND): I1, I2, I3, I4.

Conclusion: Ψ̃-e^{iχ}Ψ=Σ c_λ(e^{iφ_λ}-e^{iχ})|λ⟩⊗ψ_λ.

Justification: Apply each controlled block to the same clean input.


**S3: The error is a diagonal weighted squared sum.**

Assumptions: []. Required inputs (AND): I4, S1, S2.

Conclusion: ||Ψ̃-e^{iχ}Ψ||²=4Σ|c_λ|²sin²((φ_λ-χ)/2).

Justification: Orthonormality AND the explicit difference eliminate cross terms; use the elementary exponential-modulus identity.


**S4: Exact equality and common-phase equivalence have supportwise iff criteria.**

Assumptions: []. Required inputs (AND): I3, I4, S3.

Conclusion: The phase must equal 1 for exact equality, or a common scalar for global-phase equality, on every c_λ≠0.

Justification: A finite sum of nonnegative terms vanishes iff every positively weighted term vanishes; prove converse by substitution.


**S5: Isolated-branch correctness does not certify coherent-family correctness.**

Assumptions: []. Required inputs (AND): I1, I2, I3, S2, S3.

Conclusion: I and -I on identical branch states give |+⟩ versus |−⟩ with distance √2 and distinguishable label outcomes.

Justification: Explicit normalized two-label witness computes both states and their inner product.


**S6: A negative-phase diagonal unitary restores the exact target.**

Assumptions: []. Required inputs (AND): I1, I2, I4, I5, S2.

Conclusion: D†D=I and (D⊗I)Ψ̃=Ψ for all c.

Justification: Unit modulus proves unitarity; coefficients cancel individually.


**S7: The correction has a separate realization and resource boundary.**

Assumptions: []. Required inputs (AND): I2, I5, S6.

Conclusion: No free coherent controls, finite-bit phase supplier, diagonal compiler or new work cleanup follows.

Justification: The proof specifies an operator; it contains no implementation algorithm or cost bound.

Reuse and reconvergence:

```json
{
  "reused_results": [
    {
      "result": "Exact program phase convention e^{+iφ}C from evalPrimitiveProgram/evalGlobalPhase",
      "consumers": [
        "S2",
        "S6"
      ],
      "status": "Inspected definition; the family norm and correction theorem are original NL derivations, not existing compiled declarations."
    },
    {
      "result": "Finite orthogonal direct-sum Pythagoras",
      "consumers": [
        "S1",
        "S3"
      ],
      "status": "Derived from tensor inner products, not inferred from graph proximity."
    }
  ],
  "reconvergent_branches": [
    {
      "branches": [
        "S1",
        "S2"
      ],
      "join": "S3",
      "meaning": "Normalization/orthogonality and actual controlled action are independent requirements for the exact norm formula."
    }
  ]
}
```

### Sources and evidence boundary

- [QuantumBlockEncoding/PrimitiveSemantics.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/PrimitiveSemantics.lean): Lines 412-442: evalGlobalPhase, its full unit-modulus proof, evalGlobalPhase_neg and evalPrimitiveProgram; lines 449-478 inspect sequencing, unitarity and adjoint phase conventions. SHA-256 `ded83cb43f8d6e79c50ac738bfd4faca5bc5aeb4c564114999a832db25418c62`. MIT (repository LICENSE)
- [QuantumBlockEncoding/PrimitiveCircuit.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/PrimitiveCircuit.lean): Lines 17-55: exact-angle data and evaluation, including arbitrary exact real warning; lines 103-106: primitive list plus stored global phase. SHA-256 `d5019ef58ce1ce65664d2a40979cdd652ca691c94743532c59dfe18cf2036d4c`. MIT (repository LICENSE)

Complete source checks, separate reading/import/conceptual/dependency records, overlap and uncertainty are in the JSON payload.

- No Lean execution, kernel replay, axiom audit or production-source modification was performed for this packet.
- At authoring/freeze time, independent blind reconstruction and exact-content comparison were pending; later review status belongs in the package review manifest, not this author claim.
- Source inspection supports the stated interfaces and conventions; it does not formally verify the complete natural-language derivation.
- Frozen graph edges expose imports/ownership, not extracted theorem proof dependencies. Source-semantic legacy debt is not cleared.
- Model difficulty, model performance, global semantic deduplication and release admission remain unmeasured or unresolved.
- No compiled declaration is claimed for the weighted coherent-family norm formula, the supportwise iff criterion or the diagonal-correction theorem.

---


## B3

**Allocate precision across reused rotation parameters**

Core: `candidate:cfa3fb2e-9733-4c13-8309-11f7d0541747`. Split: `unassigned_pending_reconciliation`. Author: `/root/author_coherence`. [Authoritative payload](qa/B3.json).

### Mathematical target

Find and prove the unique optimum of a weighted continuous precision cost under a multiplicity-weighted rotation-error budget; round to integer bits with a strict additive cost bound and compose the resulting circuit error with input/target errors.

### Assumptions

- The exact and approximate circuits are finite unitary circuits with identical order, gate types and physical targets; only the stated Y-rotation parameters change.
- For the optimization, r≥1, m_j are positive integers, c_j>0, and 0<η<1/2; C=Σ_j c_j.
- Each parameter j has one approximation reused at all m_j occurrences, with certified absolute angle error δ_j; no stochastic independence is assumed.
- The exact single-rotation norm identity and the multiplicity-weighted circuit bound are supplied interfaces in the question.
- The weighted logarithmic continuous cost and weighted linear integer-bit cost are explicit model assumptions, not physical complexity theorems; reuse is charged once only in that model.
- For the state-error composition, x,y,ψ have norm one, ρ,κ≥0, ||y-x||≤ρ and ||Ux-ψ||≤κ.
- Effective access to arbitrary exact angles and a certified finite-gate compiler are not assumed.

### Conventions

- Angles are real radians in the half-angle Y-rotation convention; raw absolute angle error is used, not untracked reduction modulo 2π.
- Matrix norms are induced Euclidean operator norms; state norms are Euclidean vector norms, with all work included.
- Later chronological gates multiply on the left and no gate commuting is allowed.
- T is a deterministic precision-supplier cost relaxation; the target is optimality under its sufficient error budget, not optimality for the actual physical circuit error.
- For r=0, empty sums have value zero; formulas dividing by C are not used.

### Question

Consider two positionally aligned finite unitary circuits on q≥0 qubits. Gates are chronological: if their matrices are U_0,...,U_{N-1}, the circuit matrix is U=U_{N-1}...U_0, with the empty product I; similarly define V. All gate types and physical targets agree position by position, and only real Y-rotation angles may differ. Let r≥1 distinct supplied angle parameters a_j, indexed by j=1,...,r, be rounded to ã_j, with parameter j occurring m_j≥1 times in the list; the same certified approximation is reused at those occurrences. All other gates are unchanged. The rotation convention is R(a)=[[cos(a/2),-sin(a/2)],[sin(a/2),cos(a/2)]].

You may use these supplied interfaces, without re-proving them: for the same physical target and any number of untouched spectators, ||R(a)-R(b)||=2|sin((a-b)/4)|≤|a-b|/2 in the induced Euclidean operator norm; and, for |ã_j-a_j|≤δ_j, chronological telescoping gives ||V-U||≤(1/2)Σ_j m_jδ_j. No statistical independence is assumed. The latter is a sufficient worst-case error certificate, not an exact expression for the circuit error.

Fix 0<η<1/2 and positive real precision weights c_j. Put C=Σ_j c_j. In an explicitly ASSUMED precision-cost model, a tolerance δ_j∈(0,1] has continuous cost c_j log₂(1/δ_j), paid once per distinct parameter; reuse has no additional precision-supplier charge in this model. Other computation and implementation costs are unspecified. Minimize T(δ)=Σ_j c_j log₂(1/δ_j) subject to Σ_j m_jδ_j≤2η. Prove a global and unique minimizer, compute its minimum value, and show why the upper caps δ_j≤1 do not become active. A valid proof may use the natural-logarithm inequality ln t≤t-1 for t>0, with equality only at t=1, or a fully justified convexity argument.

For integer precision b_j≥0, a certified supplier—IF available—returns |ã_j-a_j|≤2^{-b_j} at ideal model cost c_j b_j. Construct integer b_j by rounding the continuous solution; prove the resulting circuit error is at most η and its total weighted bit cost is at least the continuous optimum and less than that optimum plus C. Do not claim this rounded allocation is the exact integer optimum.

For unit inputs x,y and a unit target ψ with ||y-x||≤ρ and ||Ux-ψ||≤κ, derive the full-output state error of Vy. Finally handle an empty parameter set and η=0 separately, and explain why neither the error certificate nor this optimization proves a polynomial-time finite-bit angle supplier or finite-gate-set compiler for arbitrary real data. Preserve multiplicities and positional alignment; the primary assessed target is the allocation/rounding argument, not the supplied telescoping lemma.

### Reference answer

Write δ_j*=2ηc_j/(m_jC). Since r≥1 and c_j>0, C>0. Each δ_j*>0, and c_j/C≤1 together with m_j≥1 and 2η<1 gives δ_j*≤2η<1. Thus the individual upper caps are strictly inactive at this candidate. Its budget is exactly saturated:
  Σ_j m_jδ_j*=Σ_j 2ηc_j/C=2η.
The candidate is feasible, and its proposed cost is
  T*=Σ_j c_j log₂(m_jC/(2ηc_j)).
Equivalently, with w_j=c_j/C, T*=C log₂(1/(2η))+Σ_j c_j log₂ m_j−CΣ_j w_j log₂ w_j. This last form is optional; the summed logarithm already computes the minimum.

Here is a global proof. Let any feasible δ have positive coordinates and set t_j=δ_j/δ_j*. Then
  T(δ)-T* = -(1/ln 2)Σ_j c_j ln t_j
            ≥ (1/ln 2)Σ_j c_j(1-t_j)
            = (C/ln 2)(1-Σ_j m_jδ_j/(2η))
            ≥ 0.
The first inequality is -ln t≥1-t for t>0. Its equality condition is t=1, and every c_j is strictly positive. If T(δ)=T*, both nonnegative gaps must vanish, so every t_j=1. Conversely δ=δ* has equality throughout. Hence δ* is the unique global minimizer. Feasibility and this comparison prove existence directly; no compactness of a domain open at δ=0 is assumed. A parameter used more often gets tighter tolerance, other quantities equal. A larger cost weight permits looser tolerance because tightening that parameter is more expensive in this model.

Let b_j*=log₂(m_jC/(2ηc_j))=log₂(1/δ_j*)>0 and choose b_j=ceil(b_j*). These integers are at least one. Put δ'_j=2^{-b_j}. Since b_j≥b_j*, δ'_j≤δ_j*, so
  (1/2)Σ_j m_jδ'_j≤(1/2)Σ_j m_jδ_j*=η.
If the supplier certifies those actual angle errors and every reused occurrence preserves positional alignment, the supplied circuit interface yields ||V-U||≤η. Correlation between repeated copies is harmless: this is a worst-case triangle-inequality bound, not a variance calculation.

Since 0≤b_j-b_j*<1,
  T*≤Σ_j c_jb_j<T*+C.
The lower bound also follows because δ' is continuously feasible and T(δ')=Σ_j c_jb_j. If b_j* is integral, its increment is zero; the strict upper bound remains true. This is an additive guarantee for this rounding construction, not proof that independent ceilings give the exact integer optimum. Nor does δ* minimize actual circuit error at fixed physical gate cost: cancellations may make the sufficient budget loose.

For full-output state error, split
  Vy-ψ=V(y-x)+(V-U)x+(Ux-ψ).
Unitarity of V bounds the first term by ρ; ||x||=1 and the operator estimate bound the second by η; the target premise bounds the third by κ. Thus ||Vy-ψ||≤ρ+η+κ, reducing to η for an exact input and exact ideal target. All work remains included. Normalizing a postselected branch would require extra success/nonzero-branch information.

If r=0 there is no changed parameter, so alignment gives V=U, supplier cost and gate perturbation zero, and state error at most ρ+κ. Do not divide by C=0. A zero-qubit circuit cannot contain the rotations required by r≥1. If r≥1 and η=0, no positive δ satisfies the budget, and no finite b makes 2^{-b}=0. Exact representability or cancellations may still make particular physical implementations exact; the positive-tolerance model does not rule those out.

The model charges one precision result per distinct parameter and assumes its reuse. It supplies no implementation. Effective angle descriptions, certified approximation algorithms with dependence on input size/magnitude and b_j, data handling, and synthesis into a chosen finite gate set require separate contracts. If actual supplier time is T_j(b_j,input_j), charge Σ_j T_j(b_j,input_j); replacing it by Σ_j c_jb_j needs independent justification. Gate synthesis errors require a further operator-error budget with gate/ancilla costs counted. Arbitrary exact-real semantics and a tolerance allocation provide none of these missing algorithms.

### Partial-credit rubric

Score out of 10. Credit mathematically valid alternative derivations; the stated criteria assess correctness, not wording.

| Points | Criterion |
| --- | --- |
| 1 | Uses the supplied multiplicity-weighted bound with positional alignment and distinguishes its sufficient worst-case certificate from exact circuit error; does not assume independent errors. |
| 2 | Constructs δ_j*=2ηc_j/(m_jC), proves positivity and δ_j*<1, and computes budget saturation and the minimum-cost formula; partial credit for the proportional form with an omitted multiplicity or normalization factor. |
| 2.5 | Proves global optimality and uniqueness using a complete log-inequality or equivalent convex argument with positivity, feasibility and equality conditions; a stationary point alone earns partial credit. |
| 1.5 | Chooses integer b_j by ceilings and proves the rounded tolerance is no larger than δ_j*, yielding circuit error≤η; partial credit for a correct bit formula without error verification. |
| 1 | Proves T*≤Σ c_jb_j<T*+C by bounding every rounding increment and avoids claiming exact integer optimality. |
| 1 | Derives the state bound ρ+η+κ using the correct unitary/operator-norm triangle decomposition, rather than multiplying unrelated errors. |
| 1 | Handles r=0 and η=0 without illegal division/logarithms and states the effective-supplier/finite-gate synthesis boundary of the assumed cost model. |

### Common errors

- Dropping m_j because each parameter is computed once; reuse saves the stipulated supplier charge but not repeated operator-error contribution.
- Treating telescoping as exact circuit distance or using statistical cancellation without a model.
- Using δ_j proportional to 1/c_j rather than c_j/m_j.
- Giving only stationary equations without proving global optimality and uniqueness.
- Rounding b_j down and violating the error budget.
- Claiming independent ceilings are the exact discrete optimum.
- Calling ideal weighted bit cost a runtime theorem for arbitrary real angles.
- Applying the r≥1 formula at r=0 or finite-bit formula at η=0.

### Boundary cases

- {"case": "r=1", "consequence": "δ_1*=2η/m_1 and T*=c_1 log₂(m_1/(2η)); repeated uses remain charged in error."}
- {"case": "Equal weights and multiplicities", "consequence": "All parameters get the same tolerance; this is a specialization, not another core."}
- {"case": "r=0, including an empty circuit", "consequence": "V=U and supplier cost is zero; C=0 is not a denominator."}
- {"case": "η=0 with r≥1", "consequence": "The positive-tolerance feasible set is empty; exact representability or cancellations are separate possibilities."}
- {"case": "q=0", "consequence": "No target wire exists; only the r=0 branch is compatible."}
- {"case": "Integer real-valued optimum precision", "consequence": "That coordinate incurs zero rounding overhead; total overhead is still strictly below C."}
- {"case": "Zero c_j or m_j", "consequence": "Outside the active optimization assumptions; positivity is used for uniqueness and the formula."}

### Difficulty annotation

```json
{
  "D0_facet": "Absolute precision, reuse, supplier cost, operator error and full-state error are distinct. No extra D0 core.",
  "provisional_route_band": "D3",
  "rationale": "Joins a supplied error interface with constrained weighted optimization, integer rounding and input/target-error composition. The log comparison is D2 locally; the parametric telescoping proof is supplied rather than counted as new D4 work.",
  "shortcut_disclosure": "A4 exact RY distance and the weighted chronological error interface are explicitly supplied; the legacy uniform Hermite budget is not new coverage.",
  "measured_model_difficulty": false
}
```

### Author-supplied reasoning map

These are natural-language mathematical dependencies, not extracted Lean proof-term dependencies. All required inputs at a step are conjunctive.

| Input | Kind | Statement |
| --- | --- | --- |
| I1 | assumption | r≥1, m_j≥1 integers, c_j>0, 0<η<1/2, C=Σc_j. |
| I2 | supplied_obligation | Aligned unitary circuits with m_j occurrences and \|ã_j-a_j\|≤δ_j satisfy \|\|V-U\|\|≤(1/2)Σm_jδ_j. The exact spectator-independent rotation norm is 2\|sin((a-b)/4)\|≤\|a-b\|/2. |
| I3 | convention | T(δ)=Σc_jlog₂(1/δ_j), 0<δ_j≤1, Σm_jδ_j≤2η. Certified errors≤2^{-b_j} have ideal cost Σc_jb_j, once per parameter. |
| I4 | supplied_obligation | For t>0, ln t≤t-1, with equality iff t=1. |
| I5 | assumption | x,y,ψ are unit, \|\|y-x\|\|≤ρ, \|\|Ux-ψ\|\|≤κ, and ρ,κ≥0. |
| I6 | convention | Empty sums are zero; actual angle access, supplier runtime and finite-gate synthesis are unsupplied. |
| I7 | assumption | Separate empty-parameter case: r=0 replaces the r≥1 clause of I1; the circuits remain positionally aligned and every gate is unchanged. Empty sums define C=0 and supplier cost zero. |
| I8 | assumption | Separate zero-budget case: r≥1, m_j≥1 and c_j>0, but η=0 replaces the strict positive-budget clause of I1. Tolerances are still strictly positive and finite integer precisions still give 2^{-b_j}>0. |

**S1: The proportional allocation is feasible and strictly within the caps.**

Assumptions: []. Required inputs (AND): I1, I3.

Conclusion: δ_j*=2ηc_j/(m_jC)∈(0,1), Σm_jδ_j*=2η.

Justification: Use C>0, c_j/C≤1, m_j≥1 and 2η<1 together.


**S2: The log comparison proves the global minimum and its value.**

Assumptions: []. Required inputs (AND): I1, I3, I4, S1.

Conclusion: T(δ)≥T*=Σc_jlog₂(m_jC/(2ηc_j)) for every feasible δ.

Justification: Set t_j=δ_j/δ_j*, apply -ln t≥1-t with weights c_j, and use feasibility.


**S3: The minimizer is unique.**

Assumptions: []. Required inputs (AND): I1, I4, S1, S2.

Conclusion: T(δ)=T* iff δ=δ*.

Justification: Strictly positive weights and equality of all log-inequality gaps force t_j=1.


**S4: Ceilings give feasible integer tolerances.**

Assumptions: []. Required inputs (AND): I1, I3, S1.

Conclusion: b_j=ceil(log₂(m_jC/(2ηc_j)))≥1 and Σm_j2^{-b_j}≤2η.

Justification: Increasing precision decreases each tolerance.


**S5: Rounded cost lies in a strict additive interval.**

Assumptions: []. Required inputs (AND): I1, I3, S2, S4.

Conclusion: T*≤Σc_jb_j<T*+C.

Justification: Each increment is in [0,1), and the rounded tolerance vector is feasible.


**S6: The conditional physical circuit error meets the budget.**

Assumptions: []. Required inputs (AND): I2, I3, S4.

Conclusion: Certified suppliers and preserved alignment imply ||V-U||≤η.

Justification: Count every occurrence in the supplied interface; no independence is needed.


**S7: Input and target errors compose with the circuit bound.**

Assumptions: []. Required inputs (AND): I2, I5, S6.

Conclusion: ||Vy-ψ||≤ρ+η+κ.

Justification: Triangle decomposition uses unitarity of V AND unit x AND both state-error premises.


**S8: The empty-parameter case has identical circuits and zero supplier cost.**

Assumptions: ["Use the r=0 case in I7; do not assume I1 or use S1–S7."]. Required inputs (AND): I2, I3, I5, I6, I7.

Conclusion: V=U, the supplier cost and gate perturbation are zero, and ||Vy-ψ||≤ρ+κ; no division by C is used.

Justification: Every aligned gate is unchanged, so the full products agree. Empty sums give zero cost. The direct triangle decomposition V(y-x)+(Ux-ψ) uses unitarity and both state-error premises.


**S9: The zero-budget case with at least one parameter has no positive-tolerance feasible point.**

Assumptions: ["Use I8 with η=0 in place of I1; none of the positive-budget conclusions S1–S7 is a premise."]. Required inputs (AND): I3, I8.

Conclusion: No positive δ can satisfy Σm_jδ_j≤0, and no finite precision vector can satisfy the corresponding sufficient zero budget. This does not rule out exact representability or physical cancellation.

Justification: At least one summand is strictly positive, and all multiplicities and tolerances are positive. Every finite 2^{-b_j} is also positive; infeasibility concerns this sufficient model, not actual circuit cancellations.


**S10: An abstract error/cost model does not supply its own physical implementation.**

Assumptions: ["This interface limitation applies separately in each parameter regime."]. Required inputs (AND): I2, I3, I6.

Conclusion: Effective angle descriptions, actual supplier algorithms and finite-gate compilation remain additional obligations with separately justified costs.

Justification: The stated interfaces are conditional error bounds and an assumed objective. They contain neither a supplier algorithm nor a runtime or gate-synthesis guarantee.

Reuse and reconvergence:

```json
{
  "reused_results": [
    {
      "result": "dimension-free-ry-distance (A4)",
      "consumers": [
        "S6"
      ],
      "status": "Exact interface stated in the question; source support for the supplied circuit certificate, not hidden cross-split retrieval."
    },
    {
      "result": "Chronological aligned-circuit telescoping with nonuniform multiplicity-weighted tolerances",
      "consumers": [
        "S6",
        "S7"
      ],
      "status": "Explicitly supplied. Uniform source theorem inspected; the weighted extension is elementary NL interface reasoning, not a new compiled root."
    },
    {
      "result": "Log tangent inequality and equality condition",
      "consumers": [
        "S2",
        "S3"
      ],
      "status": "Elementary supplied fact; optimization and rounding are original NL derivations."
    }
  ],
  "reconvergent_branches": [
    {
      "branches": [
        "S2",
        "S4"
      ],
      "join": "S5",
      "meaning": "Continuous lower bound AND rounded feasibility give the cost interval."
    }
  ]
}
```

### Sources and evidence boundary

- [QuantumBlockEncoding/PrimitiveCircuitPerturbation.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/PrimitiveCircuitPerturbation.lean): Complete module lines 1-132 inspected: GateAligned/Aligned 16-23, local distance 39-46, chronological telescoping 49-76, uniform Hermite budget and consumer 88-119. SHA-256 `624109564cd82b0584fad717283e7b9116b36f1ef10d60b43a063c0ef2a1fbae`. MIT (repository LICENSE)
- [QuantumBlockEncoding/PrimitiveRyPerturbation.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/PrimitiveRyPerturbation.lean): Complete module lines 1-99 inspected: scalar-unitary difference 17-36, physical spectator lift 39-69, Lipschitz and actual primitive interfaces 72-97. SHA-256 `57ad888af7a81ac5067f6655160fecf1f197a91b0414bc5e510786b9eed27e32`. MIT (repository LICENSE)
- [QuantumBlockEncoding/PrimitiveSemantics.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/PrimitiveSemantics.lean): Lines 18-35 half-angle rotation/composition; 194-227 physical one-qubit lift; 323-339 gate denotation/unitarity; 374-396 chronological circuit denotation/unitarity/append. SHA-256 `ded83cb43f8d6e79c50ac738bfd4faca5bc5aeb4c564114999a832db25418c62`. MIT (repository LICENSE)
- [QuantumBlockEncoding/PrimitiveCircuit.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/PrimitiveCircuit.lean): Lines 17-55 exact angle data/evaluation and arbitrary exact-real warning; 94-106 primitive gates, lists and phase-aware programs. SHA-256 `d5019ef58ce1ce65664d2a40979cdd652ca691c94743532c59dfe18cf2036d4c`. MIT (repository LICENSE)

Complete source checks, separate reading/import/conceptual/dependency records, overlap and uncertainty are in the JSON payload.

- Optimization, uniqueness and rounded-cost claims are original NL derivations, not source compiled declarations.
- The weighted interface is supplied and follows per-occurrence telescoping; the inspected source root directly states a uniform length-times-delta bound.
- No numerical angle supplier, actual runtime model or finite-gate compiler is constructed.
- No Lean execution, kernel replay, axiom audit or production-source modification was performed.
- At authoring/freeze time, blind reconstruction and distinct exact-content comparison were pending; later review status belongs in the package review manifest. The author does not self-approve.
- No model difficulty/performance measurement, release admission or global deduplication is claimed.

---


## B4

**Transport tensor-word amplitudes through physical bit reversal**

Core: `candidate:c3875629-0a16-497e-b613-ab3272780702`. Split: `unassigned_pending_reconciliation`. Author: `/root/author_coherence`. [Authoritative payload](qa/B4.json).

### Mathematical target

Prove the all-length head-first word/public-index map, transport the full amplitude vector by wire reversal, and characterize when the uncorrected vector already agrees.

### Assumptions

- n is a natural number, all bond dimensions are finite positive integers, and A_i(b), ℓ and r have the stated compatible real dimensions.
- The scalar contraction is supplied to equal f(M(w)) for every word; no synthesis or efficient core-construction claim is assumed.
- Physical labels enumerate bits in increasing wire order, and the flat public index is little-endian.
- The raw table may be zero; a normalized state is requested only if its squared mass is positive.

### Conventions

- The first core consumes the first word bit. Row-oriented tensor contraction is ℓ A_0 A_1 ... A_{n-1} r.
- ρ_n reverses coordinates and is its own inverse; the n=0 word/basis label is unique and its integer index is 0.
- P is the linear basis permutation |x⟩↦|ρ_n x⟩; vector coefficients therefore transform as (Pv)_x=v_{ρ_n x}.
- The data vector alone is defined here. No bond cleanup, postselection or circuit implementation is inferred from an index identity.

### Question

Fix n≥0 and compatible positive finite bond dimensions d_0,...,d_n. For each i<n and bit b∈{0,1}, let A_i(b) be a real d_i-by-d_{i+1} matrix, with a row boundary ℓ and column boundary r. A head-first word w=(w_0,...,w_{n-1}) has scalar amplitude F(w)=ℓ A_0(w_0)...A_{n-1}(w_{n-1})r; for n=0 the empty product is the identity. The physical basis label x(w) puts w_i on wire i, where wire 0 is least significant. Define L_n(x)=Σ_{i=0}^{n-1}x_i2^i, reversal (ρ_n x)_i=x_{n-1-i}, and S_n(w)=L_n(ρ_n x(w)). Define the head-first integer recursively by M(empty)=0 and M(b::u)=b·2^{length(u)}+M(u).

Prove for every n that S_n(w)=M(w), that these word/index maps are bijective onto {0,...,2^n-1}, and that S_n applied to the word read from ρ_n x equals L_n(x). Give an all-length argument using the head/tail versus appended-high-bit recurrence, not just an example.

Now suppose a real sample table f:{0,...,2^n-1}→R satisfies F(w)=f(M(w)). Define v=Σ_w F(w)|x(w)⟩ and the intended little-endian vector t=Σ_x f(L_n(x))|x⟩. Derive the physical amplitude v_x. For the basis permutation P|x⟩=|ρ_n x⟩, prove Pv=t and determine exactly when v=t without applying P. Prove their squared masses agree and explain normalization when that mass is positive. Give an explicit non-palindromic three-bit word and sample table for which the uncorrected vectors differ, with both integer labels written out.

Explain why reversing physical wire labels is different from reversing the order of the generally noncommuting core matrices. Separate a mathematical basis relabeling from actually executing a wire-permutation circuit; no free routing, SWAP synthesis or tensor-train preparation algorithm is assumed. Include n=0, n=1, a reversal-invariant table and the zero table.

### Reference answer

The coordinate map w↦x(w) is a bijection: its inverse reads wires 0,1,...,n−1 as a head-first word. Reversal is an involution, since n−1−(n−1−i)=i for every valid wire. For n=0 there are no coordinates and the unique empty label is fixed.

The little-endian map is bijective by induction. At width n+1, write a low-wire-first bit list as (b,u); then L_{n+1}(b,u)=b+2L_n(u). Every j in {0,...,2^{n+1}−1} has a unique decomposition j=b+2q with b=j mod 2 and q=floor(j/2) in the width-n range. This gives existence and uniqueness of the inverse. In particular S_n, a composition of the word-to-basis bijection, reversal and L_n, is a bijection.

To connect it to the head-first integer, first note the high-bit append identity L_{n+1}(y followed by b)=L_n(y)+2^n b. Reversing the basis list of a head-first word b::u produces the reversed basis list of u followed by b at the highest wire. Consequently
  S_{n+1}(b::u)=S_n(u)+2^n b.
The empty case gives S_0(empty)=0. Induction using the same recurrence for M yields S_n(w)=M(w) at every length, including leading zeros. Equivalently M(w)=Σ_i w_i2^{n−1−i}. The range 0≤M(w)<2^n follows as well, without treating a leading zero as deletion of a wire. If one reads a word from ρ_n x, its basis list is ρ_n x; applying S_n then gives L_n(ρ_nρ_n x)=L_n(x). This is the required public-index bridge.

The raw emitted vector assigns coefficient F(w) to x(w), so
  v_x=F(word read from x)=f(M(word read from x))=f(L_n(ρ_n x)).
Thus reading a head-first sample integer directly as a low-wire physical integer generally reverses the sample table. It does not change the number of wires or any scalar amplitude value; it puts amplitudes at different physical labels.

Because ρ_n is its own inverse, P†=P and P²=I. For each output x, the coefficient of Pv is the unique source coefficient v_{ρ_n x}=f(L_n(ρ_nρ_n x))=f(L_n(x))=t_x. Hence Pv=t as complete vectors. Let rev_n(j)=L_n(ρ_n L_n^{-1}(j)), the integer permutation that reverses exactly n bits, retaining leading zeros. Then v=t if and only if f(rev_n(j))=f(j) for every j in the index range: necessity compares the two coefficients at x=L_n^{-1}(j), and sufficiency reverses that argument. It is a condition on the table, not a generic identity of all tables.

Reindexing the finite sum gives
  Σ_x |v_x|²=Σ_j f(j)²=Σ_x |t_x|²=:Z².
Alternatively, the unitary basis permutation P preserves the Euclidean norm. If Z>0 then P(v/Z)=t/Z and both are unit states; this is exact transport with no lost success probability. If Z=0, every real f(j)=0, v=t=0 and the unnormalized identities still hold, but division by Z does not define a state.

For a discriminator take n=3 and w=(1,0,0), explicitly written in increasing wire order. Its physical index is L_3(1,0,0)=1, whereas its head-first integer is M(1,0,0)=4. Choose f(j)=1 for j=4 and 0 otherwise. This table can satisfy the contraction premise with all bond dimensions one, ℓ=r=1, and scalar factors A_0(b)=1_{b=1}, A_1(b)=A_2(b)=1_{b=0}. Then v=|(1,0,0)⟩ has flat index 1, while t=|(0,0,1)⟩ has flat index 4. They are distinct normalized basis vectors. P exchanges the labels and corrects the vector. This is not a palindrome example that accidentally hides reversal.

At n=0 both indexing sets are singletons, the product is ℓr, P=I and the only table entry is f(0); positive mass gives its normalized signed scalar. At n=1 reversal is also the identity, so every table agrees. At larger widths reversal-invariant tables, including constants and the zero table, still give v=t.

The ordered product A_0(w_0)...A_{n−1}(w_{n−1}) is unchanged in all these equations. We changed which word is assigned to a physical label; we never commuted core matrices. Reversing their product may even be ill-typed for unequal bond dimensions, and generally changes the value when dimensions match. A passive change of basis convention is bookkeeping. If the physical output wires are fixed, realizing P is an additional wire permutation whose gate implementation, connectivity and cost need a separate argument. None of these index identities constructs the tensor-train emitter or proves its workspace cleanup.

### Partial-credit rubric

Score out of 10. Credit mathematically valid alternative derivations; the stated criteria assess correctness, not wording.

| Points | Criterion |
| --- | --- |
| 2 | Proves word-to-basis, reversal and little-endian bijectivity with correct all-length base and unique binary inverse; partial credit for correct maps without the bijection argument. |
| 2 | Derives the head-to-high-bit recurrence and S_n=M by induction, then the double-reversal public-index identity; a numerical example alone earns no more than partial credit. |
| 2 | Derives v_x=f(L_n(ρ_nx)) and proves Pv=t by tracking coefficients under the inverse permutation; partial credit for identifying bit reversal without its amplitude action. |
| 1 | Proves the necessary-and-sufficient table-invariance criterion for v=t, not merely a sufficient symmetry example. |
| 1 | Proves equal squared masses by bijective reindexing or unitarity and handles positive versus zero normalization. |
| 1 | Gives a genuine non-palindromic three-bit discriminator, including the two unequal integers and a sample table satisfying the contraction premise. |
| 1 | Keeps matrix-product order, wire permutation and implementation cost distinct; correctly handles n=0 and n=1 rather than treating zero qubits as an empty sample table. |

### Common errors

- Confusing the first tensor-word bit with the least significant sample digit.
- Testing only palindromic words such as (1,0,1), which cannot distinguish reversal.
- Claiming (Pv)_x=v_x after relabeling instead of tracking the inverse permutation.
- Reversing noncommuting core order to repair a wire-index mismatch.
- Dropping leading zero wires from rev_n.
- Normalizing the zero sample table or claiming a basis relabeling is a free physical circuit.

### Boundary cases

- {"case": "n=0", "consequence": "One empty word, one physical label and one sample index 0; the empty matrix product is identity and reversal is identity."}
- {"case": "n=1", "consequence": "Reversal is identity for both bits; no table mismatch is possible."}
- {"case": "Reversal-invariant f", "consequence": "The uncorrected vector already agrees exactly, even when n>1."}
- {"case": "Zero f", "consequence": "All raw identities hold with zero mass; no normalized output state is defined."}
- {"case": "Unequal bond dimensions", "consequence": "The forward contraction is well typed; reversing core multiplication is generally not."}

### Difficulty annotation

```json
{
  "D0_facet": "Head-first word order, low-wire physical order, little-endian numeric order and normalization are separate conventions. No extra D0 core.",
  "provisional_route_band": "D4",
  "rationale": "An all-length inductive coordinate representation is joined to a full-vector permutation and exact equality criterion. The small example is a discriminator, not the general proof.",
  "shortcut_disclosure": "Supplying both all-width sample-map identities would shorten the first half to a D1 application; the current question asks their reconstruction.",
  "measured_model_difficulty": false
}
```

### Author-supplied reasoning map

These are natural-language mathematical dependencies, not extracted Lean proof-term dependencies. All required inputs at a step are conjunctive.

| Input | Kind | Statement |
| --- | --- | --- |
| I1 | convention | Finite binary words, x(w)_i=w_i, L_n(x)=Σx_i2^i, ρ_n reverses exactly n coordinates, S_n=L_n∘ρ_n∘x. |
| I2 | convention | M(empty)=0 and M(b::u)=b2^{length(u)}+M(u). |
| I3 | assumption | Compatible row-oriented real core product F(w)=ℓA_0(w_0)...A_{n−1}(w_{n−1})r and F(w)=f(M(w)) for every word. |
| I4 | convention | v=Σ_w F(w)\|x(w)⟩, t=Σ_x f(L_n(x))\|x⟩, and P\|x⟩=\|ρ_nx⟩. |
| I5 | convention | Normalization may be formed only when Z²=Σ_j f(j)²>0; physical synthesis is not supplied. |

**S1: All three coordinate maps are bijections.**

Assumptions: []. Required inputs (AND): I1.

Conclusion: w↦x(w), ρ_n, L_n and S_n are bijective; ρ_n²=id.

Justification: Read coordinates, reverse twice, and induct on unique j=b+2q decomposition.


**S2: The sample index and head-first integer agree at every width.**

Assumptions: []. Required inputs (AND): I1, I2.

Conclusion: S_n(w)=M(w).

Justification: The empty case and head-first reversal becoming high-bit append give S_{n+1}(b::u)=S_n(u)+2^n b, matching M.


**S3: The reversed physical word maps to the original public integer.**

Assumptions: []. Required inputs (AND): I1, S1, S2.

Conclusion: S_n(word from ρ_nx)=L_n(x).

Justification: Double reversal cancels; the proved identity identifies the head-first numeric value.


**S4: The uncorrected emitter vector contains a reversed sample table.**

Assumptions: []. Required inputs (AND): I3, I4, S1, S2.

Conclusion: v_x=f(L_n(ρ_nx)).

Justification: Each physical x receives exactly one word coefficient, then apply the contraction premise and S_n=M.


**S5: Physical reversal transports the entire vector and characterizes accidental agreement.**

Assumptions: []. Required inputs (AND): I1, I4, S1, S4.

Conclusion: Pv=t; v=t iff f(rev_n(j))=f(j) for every j.

Justification: Coefficient transport uses the inverse permutation, equal to ρ_n; bijective L_n gives both directions of the iff.


**S6: Mass and normalization survive the coordinate transport.**

Assumptions: []. Required inputs (AND): I3, I4, I5, S1, S4, S5.

Conclusion: ||v||²=||t||²=Z², and P(v/Z)=t/Z when Z>0.

Justification: Reindex the finite sum; zero mass forces the raw vector to vanish and does not allow division.


**S7: An exact three-bit witness detects the wrong convention.**

Assumptions: []. Required inputs (AND): I1, I2, I3, I4, S4, S5.

Conclusion: For f=1_{j=4}, v has flat label 1 and t has flat label 4.

Justification: Compute LE(100)=1 and MSB(100)=4; rank-one scalar cores realize the table so the witness meets the premise.


**S8: The index bridge preserves the original contraction order but does not supply physical routing.**

Assumptions: []. Required inputs (AND): I3, I4, I5, S5.

Conclusion: No core commutation, TT compiler or free SWAP theorem is inferred.

Justification: All products remain in head-first order; P is only a specified mathematical basis permutation.

Reuse and reconvergence:

```json
{
  "reused_results": [
    {
      "result": "Head-first word, word-to-basis and sample-index definitions in TensorTrainCanonical/Schedule/Word",
      "consumers": [
        "S1",
        "S2",
        "S3"
      ],
      "status": "Inspected frozen definitions and proofs; all-length argument reconstructed here."
    },
    {
      "result": "Little-endian head and high-bit-append recurrences",
      "consumers": [
        "S1",
        "S2"
      ],
      "status": "Source interfaces primitiveBasisLEEquiv_succ_value and primitive_snoc_value; no new Lean execution."
    },
    {
      "result": "Finite permutation coefficient transport and norm preservation",
      "consumers": [
        "S5",
        "S6"
      ],
      "status": "Original NL composition proved explicitly; not claimed as an extracted theorem dependency."
    }
  ],
  "reconvergent_branches": [
    {
      "branches": [
        "S1",
        "S2"
      ],
      "join": "S4",
      "meaning": "Unique physical word and correct word/public-index value are both needed for the amplitude table."
    }
  ]
}
```

### Sources and evidence boundary

- [QuantumBlockEncoding/TensorTrainWord.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/TensorTrainWord.lean): Complete module lines 1-102 inspected: word/basis inverses lines 10-30, reversal and sampleEquiv lines 32-39, high-bit append lines 50-71, sampleEquiv_value lines 73-88, public bridge lines 90-100. SHA-256 `65406c2bfa5359d6b6c1559a5a5a3f686ad4417cac436a8a1aab696b7becbdf8`. MIT (repository LICENSE)
- [QuantumBlockEncoding/TensorTrainCanonical.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/TensorTrainCanonical.lean): Lines 18-43: real incoming-row/outgoing-column core slice, dependent Chain, head-first Word and ordered contract. SHA-256 `b8d1eb0651708ac2496be306e2d4b6f3025f7ea4d35a8c6907de02b89d1d981f`. MIT (repository LICENSE)
- [QuantumBlockEncoding/TensorTrainSchedule.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/TensorTrainSchedule.lean): Lines 17-20: wordOfBasis reads wire zero then tail; lines 68-110: transfer_shift and padded row/column contraction bridge inspected for convention reconciliation. SHA-256 `2cd10d741a8655132286cbba741293b6ab2a89c713d8553beebd2820b0aab8e3`. MIT (repository LICENSE)
- [QuantumBlockEncoding/PrimitiveBasisLE.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/PrimitiveBasisLE.lean): Lines 15-38: complete little-endian equivalence and successor-value theorem. SHA-256 `469c176f1f47732661d526b72de1f9906a3c335061f6a4c82766877ce5979fad`. MIT (repository LICENSE)
- [QuantumBlockEncoding/HermiteBoundaryInjection.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/HermiteBoundaryInjection.lean): Lines 22-41: MSB-first wordValue and coordinate identity; lines 785-788: length-qualified public-grid index. SHA-256 `a78c5a9e71e669048e5274cb55e3e10ccec326bccf26739713dd695bd15b2ca0`. MIT (repository LICENSE)

Complete source checks, separate reading/import/conceptual/dependency records, overlap and uncertainty are in the JSON payload.

- No Lean execution, kernel replay, axiom audit or production-source modification was performed for this packet.
- At authoring/freeze time, independent blind reconstruction and exact-content comparison were pending; later review status belongs in the package review manifest, not this author claim.
- Source inspection supports the stated interfaces and conventions; it does not formally verify the complete natural-language derivation.
- Frozen graph edges expose imports/ownership, not extracted theorem proof dependencies. Source-semantic legacy debt is not cleared.
- Model difficulty, model performance, global semantic deduplication and release admission remain unmeasured or unresolved.
- The amplitude transport/equality-criterion composition and resource distinction are original NL arguments; the source sample-map theorems do not formally certify those whole conclusions.
- No implementation of P, source tensor construction, local isometry synthesis or full flattened circuit was checked.

---


## C1

**Explicit shifted-polynomial factors and the degree-controlled rank bound**

Core: `qcb-core-sp-114`. Split: `dev`. Author: `/root/author_tensor_polynomial`. [Authoritative payload](qa/C1.json).

### Mathematical target

Construct finite-width factors for q(u(x)+v(y)) and derive the algebraic rank bound without imposing finite row or column sets.

### Assumptions

No extra assumptions are added to the immutable question.

### Conventions

The mathematical conventions are stated in the question.

### Question

Consider a bivariate real array F(x,y) = q(u(x) + v(y)), where q is a real polynomial of degree at most d and u, v are arbitrary real-valued functions of the row index x and column index y respectively. Prove that F factorizes as a matrix product A * B with inner dimension d+1, and conclude that the rank of F is at most d+1. Make explicit which polynomial identity provides the factorization and why only the degree of q — not the number of rows or columns — controls the inner dimension.

### Reference answer

Write q(z)=sum_{k=0}^d a_k z^k, padding with zero coefficients if its degree is smaller than d. Here d is a nonnegative integer, as required by the requested inner dimension. The zero polynomial is included by taking every a_k=0; no exact-degree or nonzero assumption is needed. For any real a and s the binomial theorem gives
q(a+s)=sum_{k=0}^d a_k sum_{i=0}^k binom(k,i) a^{k-i}s^i
       =sum_{i=0}^d [sum_{k=i}^d a_k binom(k,i)a^{k-i}]s^i.
Define c_i(a)=sum_{k=i}^d a_k binom(k,i)a^{k-i}. Equivalently c_i(a)=q^{(i)}(a)/i!: this is the exact shifted-polynomial Taylor identity, with no infinite series or remainder. It remains valid at a=0, since zeroth powers are 1, and all rearrangements are of finite sums.

Let X and Y be the original row and column index sets, without adding finiteness assumptions. Take the inner index set I={0,...,d} and define A(x,i)=c_i(u(x)) and B(i,y)=v(y)^i. Matrix multiplication here sums only over I, so it is defined even when X or Y is infinite. For each x in X and y in Y,
(AB)(x,y)=sum_{i=0}^d c_i(u(x))v(y)^i=q(u(x)+v(y))=F(x,y).
This supplies actual factors of the stated inner dimension, rather than merely asserting low rank.

For finite matrices, each column F(:,y) is a linear combination of the d+1 columns A(:,i), with coefficients B(i,y). Hence the column space of F is contained in their span, and rank F<=d+1. The same argument gives the algebraic column-rank interpretation for arbitrary index sets: regard columns as functions in the real vector space R^X, and take the dimension of the span of {F(:,y):y in Y}. It is a subspace of the span of d+1 explicitly exhibited functions. Equivalently every finite submatrix has rank at most d+1. The assertion does not require an infinite-dimensional Hilbert-space operator, convergence of an infinite sum, or an arbitrary infinite vector of column weights. Thus the unrestricted array question can be answered without silently imposing finite X and Y.

Only the d+1 possible powers of the shifted variable produce inner coordinates. Adding rows or columns changes where these factors are evaluated but does not create further shifted powers. Additivity separates u(x), which enters c_i, from v(y), which enters the monomial. The bound is an upper bound, not a universal equality or a minimum-width certificate: zero coefficients, repeated sample values or constant u or v can reduce the rank. For d=0, A(x,0)=a_0 and B(0,y)=1 give width one; the rank is zero if the array vanishes and at most one otherwise. Empty row or column sets have rank zero and the entrywise factorization is vacuous. No normalization, circuit construction or numerical evaluation cost follows from this algebraic factorization alone.

### Partial-credit rubric

Score out of 10. Credit mathematically valid alternative derivations; the stated criteria assess correctness, not wording.

| Points | Criterion |
| --- | --- |
| 3 | Derives the exact finite shifted-polynomial identity, either by the binomial sum c_i(a)=sum_{k=i}^d a_k binom(k,i)a^(k-i) or by a justified finite Taylor formula. Award 1 for recognizing a polynomial in the shift of degree at most d, and the other 2 for correct coefficients and exactness without a remainder. |
| 3 | Defines both factors with the correct index orientation A(x,i)=c_i(u(x)), B(i,y)=v(y)^i and verifies their product entry by entry. Award 1 for each correct factor and 1 for substitution proving equality. |
| 2 | Derives rank<=d+1 from containment of the column span in the span of d+1 explicit functions (or a valid finite-matrix product rank theorem with the unrestricted case accounted for). Award 1 for the spanning mechanism and 1 for the dimension bound. Do not require an unstated finite-row assumption. |
| 2 | Explains that polynomial degree controls width independently of row/column count, and that width is only an upper bound. Award 1 for the degree/size explanation and 1 for a correct zero, constant, empty-index or degeneracy boundary without changing the problem. |

### Common errors

- Using Taylor coefficients q^(i)(a) without dividing by i!.
- Expanding about u(x) but evaluating coefficients at v(y), destroying the specified separation.
- Treating a degree upper bound as exact rank, or claiming width d rather than d+1.
- Adding finite row and column sets as new premises instead of using the finite inner sum and algebraic span argument.
- Interpreting the factors as a circuit compiler or finite-bit complexity bound.

### Boundary cases

- {"case": "q=0", "resolution": "All factors A entries are zero; rank is zero. The requested d+1 width is still a valid witness."}
- {"case": "d=0 or constant q", "resolution": "The only inner index is 0 and v(y)^0=1, including v(y)=0."}
- {"case": "Empty or infinite outer index sets", "resolution": "The product still has only d+1 inner summands. Empty cases have rank zero; arbitrary outer sets use algebraic column span."}
- {"case": "Repeated sample values or smaller actual degree", "resolution": "Rank can be strictly smaller than the witness width."}

### Difficulty annotation

```json
{
  "D0": {
    "facet": "Distinguish finite inner width from outer array size, and an algebraic rank upper bound from an equality or circuit-resource statement.",
    "adds_core": false
  },
  "construction_band": "D3",
  "status": "provisional_mathematical_route_annotation_not_measured_difficulty",
  "rationale": "The route joins an exact shifted-polynomial representation, an entrywise factorization and the column-span rank interface. Degree control, finite inner indexing and variable separation must all survive that join; this is the existing course SP114 construction band.",
  "taxonomy_source": "benchmarks/quantumcomputingbench/tracks/lean/COURSE.md:19-30",
  "D1_D4_context": {
    "D1": "Precise statement reading and a disclosed library application.",
    "D2": "Local symbolic construction and entry/sum reasoning.",
    "D3": "Joining mathematical interfaces with every AND premise preserved.",
    "D4": "Parametric induction and global invariant/representation or degree control."
  },
  "shortcut_disclosure": "Supplying the full target theorem could reduce this to a library application; the question instead requests the stated derivation. Graph distance, source length and node count do not measure this band.",
  "model_calibration": "unmeasured"
}
```

### Author-supplied reasoning map

These are natural-language mathematical dependencies, not extracted Lean proof-term dependencies. All required inputs at a step are conjunctive.

| Input | Kind | Statement |
| --- | --- | --- |
| C1-I1 | assumption | q is a real polynomial of degree at most the nonnegative integer d. |
| C1-I2 | assumption | u:X->R and v:Y->R are arbitrary functions; F(x,y)=q(u(x)+v(y)). |
| C1-I3 | convention | Matrix multiplication over inner set {0,...,d} is a finite sum; for arbitrary outer sets algebraic rank is dimension of the column-function span. |

**C1-S1: Produce the exact shifted coefficients.**

Assumptions: ["Real polynomial, degree bound d."]. Required inputs (AND): C1-I1.

Conclusion: For all real a,s, q(a+s)=sum_{i=0}^d c_i(a)s^i.

Justification: Finite binomial expansion and collection of equal powers; c_i(a)=sum_{k=i}^d a_k binom(k,i)a^(k-i).


**C1-S2: Separate the row and column variables.**

Assumptions: ["The same q,u,v as in the question."]. Required inputs (AND): C1-S1, C1-I2.

Conclusion: F(x,y)=sum_i c_i(u(x))v(y)^i.

Justification: Substitute a=u(x), s=v(y).


**C1-S3: Assemble actual factors and verify equality.**

Assumptions: ["Finite inner sum, with no finiteness requirement on outer sets."]. Required inputs (AND): C1-S2, C1-I3.

Conclusion: A(x,i)=c_i(u(x)), B(i,y)=v(y)^i satisfy F=AB with width d+1.

Justification: Unfold finite matrix multiplication entrywise.


**C1-S4: Pass from the finite-width representation to rank.**

Assumptions: ["Columns are real functions on X."]. Required inputs (AND): C1-S3, C1-I3.

Conclusion: rank F<=d+1.

Justification: Every column of F lies in the span of the d+1 columns of A.


**C1-S5: Explain degree control and degenerate boundaries.**

Assumptions: ["d is only an upper degree bound; outer sets may be empty."]. Required inputs (AND): C1-I1, C1-I2, C1-I3, C1-S3, C1-S4.

Conclusion: Width depends on d, while zero/constant/empty/repeated-value arrays may have smaller rank.

Justification: The finite powers determine I; no step uses an outer size, nonzero coefficient, distinct value or nonempty row/column premise.

Reuse and reconvergence:

```json
{
  "reused_results": [
    {
      "id": "shifted-polynomial-identity",
      "producer": "C1-S1",
      "consumer_steps": [
        "C1-S2"
      ],
      "status": "Derived explicitly in this answer; source polynomial_add_factorization uses the corresponding shifted-polynomial coefficient identity."
    },
    {
      "id": "finite-width-column-span",
      "producer": "C1-S3",
      "consumer_steps": [
        "C1-S4",
        "C1-S5"
      ],
      "status": "Factorization witness reused for rank and boundary explanation."
    }
  ],
  "reconvergent_branches": "none: the substantive proof is a sequential representation-to-rank route; final boundary discussion reuses established facts but is not an independent proof diamond."
}
```

### Sources and evidence boundary

- [QuantumBlockEncoding/HermiteCutRank.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/HermiteCutRank.lean): lines 23-50: FactorsThrough F := exists A : Matrix a i R, B : Matrix i b R, F = A*B; FactorsThrough.rank_le : F.rank <= Fintype.card i; polynomial_add_factorization (p) (d) (hd: p.natDegree <= d) (u v) : FactorsThrough (i := Fin (d+1)) (fun x y => p.eval (u x + v y)) via A x i = (taylor (u x) p).coeff i, B i y = v y^i; polynomial_add_rank_le : rank <= d+1 SHA-256 `c0f038bd889c77163967c71df5f5987082f4b79ab7db2b7822efcdda7234aaf2`. MIT (repository LICENSE)

Complete source checks, separate reading/import/conceptual/dependency records, overlap and uncertainty are in the JSON payload.

- At authoring freeze, the proposed answer/rubric has not yet received distinct content-bound mathematical review.
- No Lean execution, new formal view, stable-release admission or model calibration occurred.
- The source rank theorem explicitly assumes a finite column type; the broader algebraic column-span explanation is an original NL justification of the existing unrestricted question, not a claim that the source theorem has a different signature.

---


## C2

**Internal tensor-train gauges preserve amplitudes but need not preserve canonical rows**

Core: `candidate:0983ca7d-38f9-46d0-8920-b798e5c0cd7b`. Split: `unassigned_pending_reconciliation`. Author: `/root/author_tensor_polynomial`. [Authoritative payload](qa/C2.json).

### Mathematical target

Derive all-length internal gauge telescoping, exact scalar-amplitude and norm invariance, and the precise distinction from local right-canonicality. Characterize preservation of full right-canonicality by orthogonal gauges when the terminal gauge is fixed.

### Assumptions

- n is a nonnegative integer; all bond dimensions are finite natural numbers, and both external bonds have dimension one.
- Each core slice A_j^s has the stated real matrix dimensions.
- Every internal G_j is invertible; the two external gauges are the identity. Right-canonicality is an additional premise only for the conditional preservation assertion.

### Conventions

- The first matrix emits the first bit; physical bit labels are never permuted by a gauge.
- Products are written in core order A_1...A_n. A real transpose is used, with no complex conjugation issue.
- A zero-dimensional matrix is interpreted as the unique linear endomorphism of the zero vector space; its identity is invertible. The empty word set for n=0 has one element.
- Equality of amplitudes is exact, not equality up to global phase. Squared mass is the sum of squares over all words.

### Question

Let n be a nonnegative integer and let r_0,...,r_n be finite bond dimensions with r_0=r_n=1. Internal dimensions may be zero. A real tensor train consists of two matrices A_j^0,A_j^1 of size r_{j-1} by r_j for each j=1,...,n. For a bit word s=(s_1,...,s_n), in first-core-first order, define the scalar amplitude f(s) as the sole entry of P_A(s)=A_1^{s_1}...A_n^{s_n}; the empty product for n=0 is the 1-by-1 identity. Its squared mass is S=sum_{s in {0,1}^n} f(s)^2 and its Euclidean norm is sqrt(S).

Choose any invertible real r_j-by-r_j matrix G_j for each internal bond j=1,...,n-1, and set G_0=G_n=I_1. Define transformed slices B_j^s=G_{j-1}^{-1} A_j^s G_j. Derive a telescoping identity for every prefix product and use it to prove that every scalar amplitude, the full squared mass and the Euclidean norm are unchanged for all n. State exactly what endpoint fixing contributes.

Call the train right-canonical if sum_{s=0}^1 A_j^s(A_j^s)^T=I_{r_{j-1}} at every j. Does an arbitrary invertible internal gauge preserve this condition? Derive the transformed local row-Gram matrix, give an explicit two-core counterexample if the universal claim fails, and prove that orthogonal internal gauges do preserve right-canonicality. Decide also whether orthogonality of every internal gauge is necessary when both the original and transformed trains are right-canonical and the terminal gauge is fixed to the identity; justify your conclusion from the local equations, not just the example. Cover n=0, n=1 and zero-dimensional internal bonds without adding nonzero-state or full-rank premises. All statements are exact real algebra, with no circuit or finite-precision cost claim.

### Reference answer

Fix a word and let P_{A,k}=A_1^{s_1}...A_k^{s_k}, with P_{A,0}=I_1, and define P_{B,k} similarly. The dimensions are r_0 by r_k. The invariant is P_{B,k}=G_0^{-1}P_{A,k}G_k. At k=0 it is I_1=G_0^{-1}G_0. If it holds at k-1, associativity and the inverse identity give
P_{B,k}=G_0^{-1}P_{A,k-1}G_{k-1}G_{k-1}^{-1}A_k^{s_k}G_k
       =G_0^{-1}P_{A,k}G_k.
No matrices have been commuted. This proves the invariant for every prefix and every n. At k=n both endpoint gauges are I_1, so P_B(s)=P_A(s), and hence the scalar f(s) is unchanged. Summing its unchanged square over all 2^n words gives S_B=S_A; taking the nonnegative square root gives equal Euclidean norms. If that mass is positive, normalized amplitudes also agree, but normalization is neither needed nor defined for a zero train. If endpoint gauges were allowed to vary, the product would be G_0^{-1}P_A(s)G_n; in the scalar-boundary case this can rescale the amplitudes. Thus fixed endpoints remove that residual boundary action, although other correlated endpoint choices can also preserve a particular amplitude.

For the canonicality question put L=G_{j-1} and R=G_j at one core, and use L^{-T}=(L^{-1})^T. Transposition reverses the factors, so
sum_s B_j^s(B_j^s)^T
 =L^{-1}[sum_s A_j^s R R^T (A_j^s)^T]L^{-T}.
Invertibility only supplies R R^{-1}=I, not R R^T=I; the inner row-Gram expression is therefore not generally the original one. Exact cancellation between adjacent cores is a different property from preservation of each core's row inner products.

For a counterexample choose n=2 and r_0=r_1=r_2=1. Let A_1^0=A_2^0=[1] and A_1^1=A_2^1=[0]. Both local row-Grams are [1], and the only nonzero amplitude is f(0,0)=1, so S=1. With G_1=[2] the transformed zero slices are B_1^0=[2] and B_2^0=[1/2], while the one slices stay zero. Their row-Grams are [4] and [1/4], so neither core is right-canonical. Nevertheless their 00 product is [1] and all other amplitudes are zero, exactly as predicted.

If every internal G_j is orthogonal, the endpoint identities are orthogonal too. In the displayed transformed Gram formula, R R^T=I and, for an originally right-canonical core, the bracket equals I. Since L^{-1}=L^T, the result is L^T L=I. This holds at every core, so the entire transformed train remains right-canonical. There is also a converse under the stated full-chain conditions. Suppose both A and B are right-canonical. At the terminal core G_n=I, and its transformed Gram equation is I=G_{n-1}^{-1}I G_{n-1}^{-T}. Multiplying on the left by G_{n-1} and on the right by G_{n-1}^T gives G_{n-1}G_{n-1}^T=I, so G_{n-1} is orthogonal. Repeat backward: if G_j is orthogonal, canonicality of both cores at position j forces G_{j-1}G_{j-1}^T=I. Thus every internal gauge is orthogonal. The global condition is therefore equivalent to orthogonality of all internal gauges when the input is right-canonical and the terminal gauge is fixed. Merely seeing a particular core retain its Gram, or a gauge act on an initial-boundary-unreachable direction, does not bypass this terminal-to-initial argument: right-canonicality tests every row of every tail core.

For n=0 there is one empty word and its amplitude is 1, so S=1; there are no core conditions or internal gauges. For n=1 there are no internal gauges and the sole core is unchanged. If an internal bond has dimension zero, any complete product crossing it is zero, so every scalar amplitude and the mass are zero. The same inverse/associativity argument holds on the zero space and uses no positive-state premise. Such a train cannot have every core right-canonical with the external left dimension one: at the first zero bond the incoming positive-dimensional row space would have zero output width and a zero row-Gram, which cannot be its identity. This does not undermine gauge invariance, whose hypotheses never assumed canonicality or nonzero mass. Gauge transformations preserve the typed bond dimensions; no claim of minimal rank or numerical conditioning follows.

### Partial-credit rubric

Score out of 10. Credit mathematically valid alternative derivations; the stated criteria assess correctness, not wording.

| Points | Criterion |
| --- | --- |
| 3 | Proves the correctly oriented prefix invariant P_B,k=G_0^{-1}P_A,k G_k by a valid base case and inductive adjacent cancellation. Award 1 for the invariant, 1 for the base/dimensions, 1 for the inductive step; reversing gauges or commuting noncommuting matrices loses the affected credit. |
| 2 | Uses both endpoint identities to obtain exact scalar-amplitude equality, then mass and norm equality. Award 1 for endpoint/amplitude reasoning and 1 for summing squares and the square root, without normalizing a zero state. |
| 2 | Derives the transformed local row-Gram L^{-1}[sum_s A_s RR^T A_s^T]L^{-T} and explains why invertibility alone is insufficient. Award 1 for the formula and 1 for identifying the transpose-versus-inverse issue. |
| 2 | Gives a legal two-core canonical input and nonorthogonal invertible gauge with explicit unchanged amplitudes and failed local Grams (1 point), and proves both orthogonal-gauge sufficiency and the converse for two fully canonical trains using backward induction from the fixed terminal gauge (1 point, with 0.5 for either direction). |
| 1 | Treats empty/single-core and zero-bond/zero-state boundaries consistently without adding full-rank or nonzero-state premises. A zero-bond train still obeys amplitude invariance even though full right-canonicality with scalar left boundary is infeasible. |

### Common errors

- Writing B_j=G_{j-1}A_jG_j^{-1} but attempting to prove the opposite convention without changing the invariant.
- Replacing G_j G_j^T by identity merely from invertibility.
- Inferring local canonicality from equality of the whole scalar amplitude vector.
- Assuming the first-core-first word order changes under internal gauges.
- Dividing a zero train by its norm or rejecting all zero-dimensional linear algebra as undefined.
- Assuming an unused initial-boundary direction allows a nonorthogonal gauge to preserve full right-canonicality; the terminal-to-initial row-Gram induction still forces every internal gauge orthogonal.

### Boundary cases

- {"case": "n=0", "resolution": "One empty word, identity scalar amplitude 1, mass 1, no internal transformations."}
- {"case": "n=1", "resolution": "No internal gauges; every core slice is unchanged."}
- {"case": "An internal dimension is zero", "resolution": "Complete scalar contractions vanish. Gauge invariance still holds; a fully canonical scalar-left train with such a bond is infeasible."}
- {"case": "Nonorthogonal gauge with a fully canonical input", "resolution": "At least one transformed core must fail canonicality when the terminal gauge is identity. The explicit two-core witness shows this directly; backward induction proves the general necessity."}
- {"case": "Unfixed external gauges", "resolution": "Only the conjugated/rescaled boundary action is guaranteed; exact unchanged amplitude no longer follows from internal cancellation alone."}

### Difficulty annotation

```json
{
  "D0": {
    "facet": "An internal basis change cancels in complete contractions, while orthonormality is a metric property of each local core.",
    "adds_core": false
  },
  "construction_band": "D4",
  "status": "provisional_mathematical_route_annotation_not_measured_difficulty",
  "rationale": "The central target is a prefix invariant proved for arbitrary chain length and all emitted words; the proof then contrasts global amplitude preservation with local Gram conditions. The all-length invariant, not node count, motivates D4.",
  "taxonomy_source": "benchmarks/quantumcomputingbench/tracks/lean/COURSE.md:19-30",
  "D1_D4_context": {
    "D1": "Precise statement reading and a disclosed library application.",
    "D2": "Local symbolic construction and entry/sum reasoning.",
    "D3": "Joining mathematical interfaces with every AND premise preserved.",
    "D4": "Parametric induction and global invariant/representation or degree control."
  },
  "shortcut_disclosure": "Supplying the full target theorem could reduce this to a library application; the question instead requests the stated derivation. Graph distance, source length and node count do not measure this band.",
  "model_calibration": "unmeasured"
}
```

### Author-supplied reasoning map

These are natural-language mathematical dependencies, not extracted Lean proof-term dependencies. All required inputs at a step are conjunctive.

| Input | Kind | Statement |
| --- | --- | --- |
| C2-I1 | assumption | Finite real core slices, dimensions r_j and first-core-first products with scalar external bonds. |
| C2-I2 | assumption | Internal G_j are invertible and G_0=G_n=I_1; B_j^s=G_{j-1}^{-1}A_j^sG_j. |
| C2-I3 | convention | S is the full finite word sum of squared scalar amplitudes and norm=sqrt(S). |
| C2-I4 | assumption | For the conditional canonicality claim, sum_s A_j^s(A_j^s)^T=I at each core. |
| C2-I5 | assumption | For the sufficient-condition branch, every internal G_j is orthogonal. |
| C2-I6 | assumption | For the converse branch only, every transformed core is right-canonical. |

**C2-S1: Prove the prefix gauge invariant.**

Assumptions: ["Correct dimensions and adjacent inverses."]. Required inputs (AND): C2-I1, C2-I2.

Conclusion: P_B,k=G_0^{-1}P_A,k G_k for 0<=k<=n.

Justification: Induct on k; base is the identity and the step cancels G_{k-1}G_{k-1}^{-1} by associativity.


**C2-S2: Recover exact full scalar amplitudes.**

Assumptions: ["Both external gauges are identity."]. Required inputs (AND): C2-S1, C2-I1, C2-I2.

Conclusion: For every word, f_B(s)=f_A(s).

Justification: Take k=n in the prefix invariant and apply the two endpoint identities.


**C2-S3: Recover mass and norm.**

Assumptions: ["No nonzero assumption is needed for sums of squares or the nonnegative square root."]. Required inputs (AND): C2-S2, C2-I3.

Conclusion: S_B=S_A and sqrt(S_B)=sqrt(S_A).

Justification: Substitute amplitude equality into each finite summand and take the same square root.


**C2-S4: Compute the transformed local row-Gram.**

Assumptions: ["Real transpose reverses factor order."]. Required inputs (AND): C2-I1, C2-I2.

Conclusion: Gram(B_j)=G_{j-1}^{-1}[sum_s A_j^s G_jG_j^T(A_j^s)^T]G_{j-1}^{-T}.

Justification: Expand each B_j^s(B_j^s)^T and pull out the factors independent of s.


**C2-S5: Prove the orthogonal-gauge sufficient condition.**

Assumptions: ["Original train is right-canonical; gauges including endpoints are orthogonal."]. Required inputs (AND): C2-S4, C2-I2, C2-I4, C2-I5.

Conclusion: Every transformed local Gram is identity.

Justification: Use G_jG_j^T=I, then original canonicality, then G_{j-1}^{-1}G_{j-1}^{-T}=I.


**C2-S5b: Prove orthogonality is necessary for two fully canonical trains.**

Assumptions: ["A is right-canonical and, for this converse, B is right-canonical; terminal gauge is identity."]. Required inputs (AND): C2-S4, C2-I2, C2-I4, C2-I6.

Conclusion: Every internal G_j is orthogonal.

Justification: Backward induction from G_n=I: if G_jG_j^T=I, the A and B row-Gram identities force I=G_{j-1}^{-1}G_{j-1}^{-T}, hence G_{j-1}G_{j-1}^T=I.


**C2-S6: Refute unrestricted canonicality preservation while confirming global invariance.**

Assumptions: ["n=2, all bonds one, A_j^0=1, A_j^1=0 and G_1=2 are legal inputs."]. Required inputs (AND): C2-I1, C2-I2, C2-I3, C2-S2, C2-S4.

Conclusion: Input Grams are 1; output Grams are 4 and 1/4; the only nonzero scalar amplitude remains 1.

Justification: Direct substitution supplies an exact witness and uses both the amplitude and local-Gram branches.


**C2-S7: Check empty and zero-dimensional cases.**

Assumptions: ["Empty products/sums and zero vector spaces retain their specified linear-algebra meaning."]. Required inputs (AND): C2-I1, C2-I2, C2-I3, C2-I4, C2-S1, C2-S3.

Conclusion: n=0 and n=1 have no internal change; a zero internal bond gives zero amplitudes and prevents full canonicality from scalar left boundary.

Justification: The unique empty word has identity contraction; a product through zero space is zero; the first zero bond cannot carry an isometry from its preceding positive-dimensional bond.

Reuse and reconvergence:

```json
{
  "reused_results": [
    {
      "id": "prefix-gauge-invariant",
      "producer": "C2-S1",
      "consumer_steps": [
        "C2-S2",
        "C2-S7"
      ],
      "status": "Original all-length NL derivation using the source contraction definition."
    },
    {
      "id": "local-transformed-Gram",
      "producer": "C2-S4",
      "consumer_steps": [
        "C2-S5",
        "C2-S6",
        "C2-S5b"
      ],
      "status": "Original NL matrix calculation; no dedicated frozen gauge theorem is asserted."
    }
  ],
  "reconvergent_branches": [
    {
      "branches": [
        "C2-S1 -> C2-S2",
        "C2-S4"
      ],
      "join": "C2-S6",
      "why": "The concrete witness is checked against both exact global amplitude invariance and failed local metric invariance."
    }
  ]
}
```

### Sources and evidence boundary

- [QuantumBlockEncoding/TensorTrainCanonical.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/TensorTrainCanonical.lean): Lines 18-47: real core/slice, ordered chain/word contraction and right-canonical row condition; lines 57-64: slice absorption; lines 119-168: boundary mass and canonical chain mass; entire 317-line module read. SHA-256 `b8d1eb0651708ac2496be306e2d4b6f3025f7ea4d35a8c6907de02b89d1d981f`. MIT (repository LICENSE)
- [QuantumBlockEncoding/TensorTrainNormEnvironment.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/TensorTrainNormEnvironment.lean): Lines 17-37: full matrix Gram recursion and sum-over-word semantics including terminal labels; lines 39-75: scalar norm and target reindex adapter; entire 140-line module read. SHA-256 `e684550c248817ac77e03a23e0af86d3b2c7f3d8b09bcdb2385702624f5ebe6c`. MIT (repository LICENSE)

Complete source checks, separate reading/import/conceptual/dependency records, overlap and uncertainty are in the JSON payload.

- At authoring freeze, original gauge theorem, counterexample and orthogonal-gauge characterization await distinct mathematical review.
- The frozen source supplies contraction, canonicality and mass definitions, not a dedicated theorem for this full gauge question.
- No kernel run, circuit synthesis, finite-bit stability, admission or measured model difficulty is claimed.

---


## C3

**Tensor-train cross environments, Gram positivity and arbitrary initial boundaries**

Core: `candidate:95850d89-ebfd-48a9-89bf-0221df041ac6`. Split: `unassigned_pending_reconciliation`. Author: `/root/author_tensor_polynomial`. [Authoritative payload](qa/C3.json).

### Mathematical target

Prove a two-train rectangular cross-environment identity for arbitrary length, specialize to the full positive-semidefinite Gram matrix, and derive cross-inner-products and initial-boundary mass without scalar-boundary or canonicality assumptions.

### Assumptions

- The two real trains have the same finite length, ordered two-valued physical indices and common terminal dimension r; their internal and initial dimensions may differ.
- All matrix sizes are finite natural numbers and match as specified.
- Initial vectors v and w are arbitrary real vectors, not assumed normalized or nonzero. The positive-semidefinite and kernel conclusions specialize to identical trains.

### Conventions

- A transpose is the ordinary real transpose; the inner product is sum of entrywise products.
- The first core emits s_1. Both trains use exactly the same word and terminal-label order, without any implicit reversal.
- An emitted vector retains the terminal label: its coordinates are all (s,b), so its dimension is 2^n*r.
- The empty word set has one element and an empty product is the identity. Finite sums over empty bond labels are zero.

### Question

Work over the real numbers. Let n>=0, let p_0,...,p_n and q_0,...,q_n be finite natural-number bond dimensions with p_n=q_n=r, and let A_j^0,A_j^1 have size p_{j-1} by p_j while B_j^0,B_j^1 have size q_{j-1} by q_j, for j=1,...,n. Zero dimensions are allowed. The two trains use the same ordered bit word s=(s_1,...,s_n) and the same terminal label b=1,...,r. Set P_A(s)=A_1^{s_1}...A_n^{s_n} and P_B(s)=B_1^{s_1}...B_n^{s_n}. For n=0 these are I_r and the set of words contains one empty word.

Define a rectangular cross environment backwards by H_n=I_r and H_{j-1}=sum_{t=0}^1 A_j^t H_j (B_j^t)^T. Derive, for all n, the full entry identity H_0(a,c)=sum_s sum_{b=1}^r P_A(s)_{ab} P_B(s)_{cb}. In particular, explain why the terminal index must be summed, and why off-diagonal entries contain cross-inner-products rather than squared amplitudes.

For arbitrary column vectors v in R^{p_0} and w in R^{q_0}, define emitted vectors on pairs (s,b) by Phi_A(v)_{s,b}=sum_a v_a P_A(s)_{ab} and Phi_B(w)_{s,b}=sum_c w_c P_B(s)_{cb}. Prove <Phi_A(v),Phi_B(w)>=v^T H_0 w.

Specialize to identical trains A=B and write E_0=H_0. Prove that E_0 is symmetric positive semidefinite, that ||Phi_A(v)||_2^2=v^T E_0 v for every initial vector v, and that v lies in the kernel of E_0 exactly when every emitted amplitude Phi_A(v)_{s,b} vanishes. Explain why no right-canonicality or normalized-boundary hypothesis is needed. Is a cross environment for two different trains necessarily positive semidefinite when it happens to be square? Give a counterexample if not. Check n=0, empty bond dimensions and zero trains. These are exact mathematical identities; no storage cost, finite-bit runtime or state-preparation circuit is part of the conclusion.

### Reference answer

At stage j let P_{A,>j}(s_{j+1},...,s_n)=A_{j+1}^{s_{j+1}}...A_n^{s_n}, a p_j-by-r matrix, and define P_{B,>j} similarly. The invariant of the backwards recursion is
H_j=sum_{s_{j+1},...,s_n} P_{A,>j}(s_{>j}) P_{B,>j}(s_{>j})^T.
For j=n the sum has one empty-word term I_r I_r^T=I_r, agreeing with H_n. Suppose it holds at j. Substitute into the update, distribute the finite sums and use (B_j^t P_{B,>j})^T=P_{B,>j}^T(B_j^t)^T. Then
H_{j-1}=sum_{t,s_{>j}} (A_j^t P_{A,>j})(B_j^t P_{B,>j})^T,
which is exactly the invariant for the suffix beginning at j. Backward induction establishes it at every stage, in particular H_0=sum_s P_A(s)P_B(s)^T. No canonicality relation was used.

The (a,c) entry of a product P_A(s)P_B(s)^T is sum_{b=1}^r P_A(s)_{ab}P_B(s)_{cb}. Therefore
H_0(a,c)=sum_s sum_b P_A(s)_{ab}P_B(s)_{cb}.
The terminal sum cannot be discarded unless r=1, because the emitted vector includes every terminal output label. Define U_A with rows a and columns (s,b) by U_A[a,(s,b)]=P_A(s)_{ab}, and define U_B similarly. The identity is H_0=U_A U_B^T. Each entry is the real inner product between the output vectors obtained from the two respective basis initial boundaries. Even for a single train, an off-diagonal entry compares two different initial-bond rows; it is not a sum of the squares of one row.

For arbitrary v,w, Phi_A(v)=U_A^T v and Phi_B(w)=U_B^T w. Hence
<Phi_A(v),Phi_B(w)>=v^T U_A U_B^T w=v^T H_0 w.
Entrywise, this is just the rearrangement of the finite sum over a,c,s,b, which is valid for arbitrary signed initial vectors. No positivity or normalization of those vectors is assumed.

For A=B we have E_0=U_A U_A^T, so E_0^T=E_0. The preceding boundary identity with w=v gives
v^T E_0 v=sum_{s,b}(sum_a v_a P_A(s)_{ab})^2=||Phi_A(v)||_2^2>=0.
This proves positive semidefiniteness and the complete arbitrary-boundary mass formula. In particular, the familiar scalar norm is only the p_0=r=1 specialization with initial scalar 1. Semidefiniteness is weaker than positive definiteness: E_0 can be singular, even zero. It is also weaker than entrywise nonnegativity. For example, with one core of left dimension two and terminal dimension one, A_1^0=(1,-1)^T and A_1^1=(0,0)^T give E_0=[[1,-1],[-1,1]], which is positive semidefinite despite negative off-diagonal entries.

If E_0 v=0, its quadratic form is zero. A finite sum of nonnegative real squares is zero only when each square is zero, so Phi_A(v) vanishes in every coordinate. Conversely, if every coordinate of Phi_A(v)=U_A^T v is zero, then E_0 v=U_A(U_A^T v)=0. Thus ker(E_0)=ker(U_A^T), exactly the invisible initial-boundary directions. This also explains why positivity does not require right-canonicality: a Gram matrix is positive semidefinite for any finite real matrix U_A, whereas canonicality is a stronger local isometry condition.

For distinct trains, H_0 may be rectangular, in which case positive semidefiniteness is not a property of that matrix at all. Even if it is square it need not be symmetric or positive semidefinite. For a concrete negative square example take n=1, all dimensions one, A_1^0=[1], A_1^1=[0], B_1^0=[-1], B_1^1=[0]. Then H_0=[-1], and the quadratic form at 1 is -1. These are ordinary cross-inner-products of two different output vectors, so the negative result is consistent with all identities.

When n=0, p_0=q_0=r, H_0=I_r, and the one empty-word output Phi_A(v) is precisely v on terminal labels. The boundary formula is <v,w>=v^T I_r w; the same-train quadratic form is ||v||^2. If r=0, every emitted vector has zero coordinates, H_n is the empty identity and all earlier cross environments vanish by their finite products; the same-train E_0 is zero. If an internal bond of A has dimension zero, every complete P_A is zero and H_0 is zero regardless of B; the analogous statement holds for B. If p_0=0 or q_0=0, the appropriate boundary vector is uniquely empty and the identities hold with their empty matrix dimensions. A zero train, including a train whose nonzero local data cancel to zero contractions, gives E_0=0; every initial boundary is then in the kernel. None of these zero cases requires division by a norm or construction of a normalized state.

### Partial-credit rubric

Score out of 10. Credit mathematically valid alternative derivations; the stated criteria assess correctness, not wording.

| Points | Criterion |
| --- | --- |
| 3 | States and proves the suffix-product invariant for the rectangular cross environment. Award 1 for the correct same-word product and dimensions, 1 for the one-empty-word identity base, and 1 for the backward step with correctly reversed transpose order. |
| 2 | Derives the full entry formula with both word and terminal sums (1 point), and then the cross-inner-product identity for arbitrary v,w by a valid finite-sum or U_A U_B^T argument (1 point). A scalar-only formula omitting terminal labels is insufficient. |
| 3 | For identical trains proves symmetry and nonnegative quadratic forms without canonicality (1 point), obtains the full arbitrary-boundary norm formula (1 point), and proves both directions of the kernel/vanishing-amplitudes equivalence (1 point). |
| 1 | Provides an actual pair of legal distinct trains with square cross environment that is not positive semidefinite, computing the offending value; also distinguishes rectangular cross environments from square Gram matrices. |
| 1 | Handles the one empty word at n=0 and zero-dimensional/zero-train cases consistently, without claiming positive definiteness, entrywise positivity or meaningful normalization of a zero emitted vector. |

### Common errors

- Keeping only scalar diagonal norms and thereby losing cross-inner-products between initial-bond labels.
- Dropping the terminal sum for r>1 or treating the terminal boundary as dimension one without a premise.
- Using the same-train Gram induction for two different trains without retaining the order A H B^T.
- Claiming every cross environment is positive semidefinite, or that positive semidefinite means every entry is nonnegative.
- Using zero quadratic form to assert a zero vector without the finite sum-of-squares or Gram factorization argument.
- Treating n=0 as no emitted coordinates even though the terminal labels remain.

### Boundary cases

- {"case": "n=0", "resolution": "One empty word and terminal coordinates remain; H_0=I_r and Phi_A(v)=v."}
- {"case": "r=0 or a zero internal dimension", "resolution": "Complete contractions have zero emitted amplitudes. Cross and same-train quadratic identities remain valid; the latter can be identically zero."}
- {"case": "Singular or zero Gram matrix", "resolution": "Allowed. Its kernel is exactly the boundary vectors with all emitted amplitudes zero; no positive-definite conclusion is warranted."}
- {"case": "Two distinct trains", "resolution": "The cross environment is generally rectangular and can be negative even when 1-by-1."}
- {"case": "Negative off-diagonal entries", "resolution": "Compatible with same-train positive semidefiniteness, as the explicit two-row witness demonstrates."}

### Difficulty annotation

```json
{
  "D0": {
    "facet": "A Gram matrix stores all pairwise initial-row inner products; its quadratic form is output mass for an arbitrary initial boundary, and PSD is not entrywise positivity.",
    "adds_core": false
  },
  "construction_band": "D4",
  "status": "provisional_mathematical_route_annotation_not_measured_difficulty",
  "rationale": "The cross-environment identity requires a suffix invariant for arbitrary chain length and preserves distinct internal dimensions and terminal labels. The subsequent Gram/PSD/kernel interfaces use that globally established representation; the classification is not based on graph size.",
  "taxonomy_source": "benchmarks/quantumcomputingbench/tracks/lean/COURSE.md:19-30",
  "D1_D4_context": {
    "D1": "Precise statement reading and a disclosed library application.",
    "D2": "Local symbolic construction and entry/sum reasoning.",
    "D3": "Joining mathematical interfaces with every AND premise preserved.",
    "D4": "Parametric induction and global invariant/representation or degree control."
  },
  "shortcut_disclosure": "Supplying the full target theorem could reduce this to a library application; the question instead requests the stated derivation. Graph distance, source length and node count do not measure this band.",
  "model_calibration": "unmeasured"
}
```

### Author-supplied reasoning map

These are natural-language mathematical dependencies, not extracted Lean proof-term dependencies. All required inputs at a step are conjunctive.

| Input | Kind | Statement |
| --- | --- | --- |
| C3-I1 | assumption | Two finite real trains with common word order, common terminal dimension r, and possibly different intermediate bond dimensions. |
| C3-I2 | assumption | H_n=I_r and H_{j-1}=sum_t A_j^t H_j(B_j^t)^T. |
| C3-I3 | convention | v,w are arbitrary initial column vectors; Phi values are the stated contractions, including all terminal labels. |
| C3-I4 | assumption | For the Gram/PSD/kernel branch, A=B with matching bond dimensions. |
| C3-I5 | convention | There is one empty word, empty product I, and finite sums over empty bond labels are zero. |

**C3-S1: Prove the suffix cross-environment invariant.**

Assumptions: ["Matching physical and terminal indices; transpose reverses the product."]. Required inputs (AND): C3-I1, C3-I2, C3-I5.

Conclusion: H_j=sum_{suffix words} P_A,>j P_B,>j^T for every j.

Justification: Backward induction: empty suffix gives I_r; distributing the update produces the sum over the current bit and tail word.


**C3-S2: Read every cross entry and a flattened matrix representation.**

Assumptions: ["All terminal labels must be retained."]. Required inputs (AND): C3-S1, C3-I1, C3-I5.

Conclusion: H_0(a,c)=sum_{s,b}P_A(s)_{ab}P_B(s)_{cb}, or H_0=U_A U_B^T.

Justification: Use the matrix-product entry formula and define U_A,U_B by columns (s,b).


**C3-S3: Evaluate arbitrary initial-boundary cross-inner-products.**

Assumptions: ["No normalization or sign restriction on boundaries."]. Required inputs (AND): C3-S2, C3-I3.

Conclusion: Phi_A(v)=U_A^T v and <Phi_A(v),Phi_B(w)>=v^T H_0 w.

Justification: Distribute finite sums, or multiply the displayed matrices with their exact dimensions.


**C3-S4: Specialize to a symmetric positive-semidefinite Gram matrix.**

Assumptions: ["Identical trains."]. Required inputs (AND): C3-S2, C3-S3, C3-I3, C3-I4.

Conclusion: E_0=U_A U_A^T is symmetric and v^T E_0 v=||Phi_A(v)||^2>=0.

Justification: Transpose the product and sum the squares of real output amplitudes.


**C3-S5: Identify the entire kernel.**

Assumptions: ["Identical trains; no positive-definiteness assumption."]. Required inputs (AND): C3-S2, C3-S4, C3-I3, C3-I4.

Conclusion: E_0 v=0 iff Phi_A(v)=0 coordinatewise.

Justification: Forward: zero quadratic form forces every squared coordinate zero. Reverse: U_A^T v=0 implies U_A U_A^T v=0.


**C3-S6: Refute positivity for different trains.**

Assumptions: ["n=1 and all bond dimensions one; A^0=1,B^0=-1,A^1=B^1=0."]. Required inputs (AND): C3-I1, C3-I2, C3-S2.

Conclusion: H_0=-1, a legal square cross environment with negative quadratic form.

Justification: Substitute the scalar slices; same-train premise is deliberately absent.


**C3-S7: Check empty and zero-dimensional outputs.**

Assumptions: ["Conventions cover zero dimensions and a single empty word."]. Required inputs (AND): C3-I1, C3-I2, C3-I3, C3-I4, C3-I5, C3-S1, C3-S3, C3-S4, C3-S5.

Conclusion: n=0 recovers I_r and the original boundary vector; zero output maps give zero Gram and full kernel.

Justification: Apply empty-product identities or products through the zero vector space; no normalization is introduced.

Reuse and reconvergence:

```json
{
  "reused_results": [
    {
      "id": "cross-environment-suffix-invariant",
      "producer": "C3-S1",
      "consumer_steps": [
        "C3-S2",
        "C3-S7"
      ],
      "status": "Original NL two-train extension of the inspected same-train source Gram semantics."
    },
    {
      "id": "full-cross-Gram-representation",
      "producer": "C3-S2",
      "consumer_steps": [
        "C3-S3",
        "C3-S4",
        "C3-S5",
        "C3-S6"
      ],
      "status": "Actually reused for boundary bilinear form, positivity/kernel specialization and the distinct-train boundary."
    }
  ],
  "reconvergent_branches": [
    {
      "branches": [
        "C3-S2 -> C3-S3",
        "C3-I4"
      ],
      "join": "C3-S4",
      "why": "The arbitrary-boundary bilinear form becomes a norm only when both train inputs and both boundaries coincide."
    }
  ]
}
```

### Sources and evidence boundary

- [QuantumBlockEncoding/TensorTrainNormEnvironment.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/TensorTrainNormEnvironment.lean): Lines 17-37: full matrix Gram recursion and sum-over-word semantics including terminal labels; lines 39-75: scalar norm and target reindex adapter; entire 140-line module read. SHA-256 `e684550c248817ac77e03a23e0af86d3b2c7f3d8b09bcdb2385702624f5ebe6c`. MIT (repository LICENSE)
- [QuantumBlockEncoding/TensorTrainCanonical.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/TensorTrainCanonical.lean): Lines 18-47: real core/slice, ordered chain/word contraction and right-canonical row condition; lines 57-64: slice absorption; lines 119-168: boundary mass and canonical chain mass; entire 317-line module read. SHA-256 `b8d1eb0651708ac2496be306e2d4b6f3025f7ea4d35a8c6907de02b89d1d981f`. MIT (repository LICENSE)

Complete source checks, separate reading/import/conceptual/dependency records, overlap and uncertainty are in the JSON payload.

- The two-train rectangular extension and full arbitrary-boundary/PSD/kernel explanation are original NL derivations, not claimed existing Lean theorem signatures.
- At authoring freeze, independent mathematical review and split/dedup reconciliation remain pending.
- No Lean run, computational complexity certification, new graph node or measured model performance is claimed.

---


## C4

**Bernstein coefficient perturbations to normalized sampled-state error**

Core: `candidate:3197f9f9-ed41-4610-9d9d-966014b9468c`. Split: `unassigned_pending_reconciliation`. Author: `/root/author_tensor_polynomial`. [Authoritative payload](qa/C4.json).

### Mathematical target

Compose Bernstein coefficient control, finite sample norm error, a positive sample-mass lower bound and the explicitly supplied normalization-stability interface, including endpoint and small-mass boundaries.

### Assumptions

- d,M are finite natural numbers and every sample t_j lies in [0,1].
- All coefficients are real and can have either sign; |ctilde_r-c_r|<=eta for all 0<=r<=d, with eta>=0.
- The raw sample mass satisfies ||x||_2^2>=m with m>0, and eta*sqrt(M)<sqrt(m).
- For the requested accuracy statement epsilon is a real number with 0<epsilon<2. For the endpoint alternative the stated endpoint is actually among the samples and the corresponding original coefficient has magnitude at least a>0.

### Conventions

- Sample labels j are retained in the same order in x and y; repeated locations still give separate coordinates.
- Samples themselves are signed amplitudes. Normalization divides by the positive Euclidean norm and does not replace an amplitude by its absolute value or square root.
- The comparison is Euclidean distance between the specified normalized real vectors, with their signs retained; no quotient by a global sign is taken.
- For M=0 the unique vector has squared mass zero. Degree zero has one basis element B_{0,0}=1 at both endpoints.

### Question

Let d and M be nonnegative integers. For r=0,...,d define the real Bernstein basis B_{d,r}(t)=binom(d,r)t^r(1-t)^{d-r}, with polynomial evaluation convention t^0=1 even at t=0. Let c_0,...,c_d and ctilde_0,...,ctilde_d be arbitrary signed real coefficients satisfying |ctilde_r-c_r|<=eta for every r, where eta>=0. Put p(t)=sum_{r=0}^d c_r B_{d,r}(t) and ptilde(t)=sum_{r=0}^d ctilde_r B_{d,r}(t). Choose M sample points t_1,...,t_M in [0,1], allowing repeated points and both endpoints, and define raw sample vectors x=(p(t_j)) and y=(ptilde(t_j)) in R^M. Assume a known lower bound ||x||_2^2>=m>0 and eta*sqrt(M)<sqrt(m).

You may use the following supplied result: For nonzero x,y in a finite-dimensional real or complex Euclidean space, ||x/||x||-y/||y|||| <= 2||x-y||/||x||; if ||x-y||<=delta<||x|| then y is nonzero.

Starting from the displayed basis formula, justify its nonnegativity on [0,1] and its partition of unity. Derive a uniform polynomial-value error bound, then a sample-vector Euclidean error bound. Prove an explicit positive lower bound for ||y||_2, check every premise needed to invoke the supplied result, and bound ||x/||x||_2-y/||y||_2||_2 in terms of eta, M and m. For a desired error 0<epsilon<2, give a sufficient coefficient-precision condition and justify that it also makes y nonzero.

Explain how a sampled endpoint with |c_0|>=a>0 or |c_d|>=a>0 provides a valid value of m, including d=0. Discuss signed values, eta=0, zero sampled mass, and M=0: do not treat contradictory positive-mass premises as a realizable empty-sample example or divide by sqrt(M) there. Finally give an explicit family with eta tending to zero but a fixed nonzero normalized-state error when the positive lower-mass bound is allowed to shrink. This should show why coefficient accuracy alone cannot give a uniform normalized-state guarantee independent of sample mass. This question concerns mathematical error propagation, not the gate cost or numerical evaluation error of a preparation algorithm.

### Reference answer

For 0<=t<=1, both t and 1-t are nonnegative, so every B_{d,r}(t) is nonnegative. The binomial theorem gives sum_{r=0}^d B_{d,r}(t)=(t+(1-t))^d=1, including d=0. These are the two facts used below; nonnegative coefficients are not required.

Let e_r=ctilde_r-c_r. For every t in [0,1],
|ptilde(t)-p(t)|=|sum_r e_r B_{d,r}(t)|
 <=sum_r |e_r|B_{d,r}(t)<=eta sum_r B_{d,r}(t)=eta.
Thus each sampled coordinate obeys |y_j-x_j|<=eta. Squaring these nonnegative inequalities and summing gives ||x-y||_2^2<=M eta^2, hence ||x-y||_2<=delta:=eta sqrt(M). Repeated points are still counted M times, so no distinctness or sampling-grid assumption is hidden in this estimate.

The original mass bound gives ||x||_2>=sqrt(m)>0, hence x is nonzero. The reverse triangle inequality then gives
||y||_2>=||x||_2-||x-y||_2>=sqrt(m)-eta sqrt(M)>0.
In particular y is nonzero. Alternatively the supplied nonzero criterion applies because ||x-y||<=delta and delta<sqrt(m)<=||x||. With both vectors nonzero in the same finite-dimensional real Euclidean space, the supplied normalized-distance inequality is now legal, and yields
||x/||x||_2-y/||y||_2||_2<=2||x-y||_2/||x||_2
 <=2 eta sqrt(M)/sqrt(m)=2 eta sqrt(M/m).
Every normalized vector in this calculation is well-defined; no zero vector has been normalized. The norm lower bound was proved from the sample-mass promise, not from coefficient positivity.

The assumptions already force M>=1: when M=0 the only raw vector has mass zero, contradicting m>0. Therefore in the feasible setting one may divide by sqrt(M). For 0<epsilon<2 it is sufficient to require
eta<=epsilon sqrt(m)/(2 sqrt(M)).
Then delta<=epsilon sqrt(m)/2<sqrt(m), so y is nonzero, and the displayed normalized-distance bound is at most epsilon. This is an absolute coefficient-error condition relative to a certified lower mass; it does not itself evaluate the norm or charge any computation used to obtain that certificate.

At t=0 all basis elements except r=0 vanish, and B_{d,0}(0)=1, so p(0)=c_0 and ptilde(0)=ctilde_0. At t=1 only r=d remains, so p(1)=c_d and ptilde(1)=ctilde_d. The formulas also hold at d=0, when c_0=c_d and the one basis element is 1. If the sample list includes 0 and |c_0|>=a>0, its single squared coordinate contributes at least a^2 to ||x||^2. Thus m=a^2 is valid; the same reasoning applies to a sampled 1 with |c_d|>=a. An endpoint coefficient does not supply this particular sample anchor when its endpoint is absent from the sample list. Other sample points and all signs remain unrestricted. A zero coefficient, or positivity without a quantitative lower bound, cannot by itself supply a positive numerical m. A polynomial can be nonzero as a function while all its chosen samples vanish.

If eta=0, the coefficient rows, polynomial values and sample vectors agree, and positive sample mass gives normalized error zero. If the raw sampled mass is zero, the question's m>0 premise is not satisfied and x/||x|| is undefined. For M=0 there are no feasible inputs under the positive-mass premise; the raw coordinate and error inequalities still read 0<=0, but the positive-mass normalized-state conclusion is not an active example. Nonnegative Bernstein weights control signed coefficient errors by the triangle inequality; negative sample values are valid amplitudes and must not be discarded.

To exhibit the small-mass obstruction, take d=1, M=2 and samples t_1=0,t_2=1. For any a>0 set c=(a,0), ctilde=(a,a/2), and eta=a/2. Then x=(a,0), y=(a,a/2), ||x||^2=a^2, and m=a^2 is a valid lower bound. Even the small-error premise holds: eta sqrt(M)=a/sqrt(2)<a=sqrt(m). As a tends to zero, eta tends to zero, but
x/||x||=(1,0),   y/||y||=(2/sqrt(5),1/sqrt(5)),
so their distance is sqrt(2-4/sqrt(5))>0, independent of a. The inputs satisfy the stated perturbation regime while their lower mass shrinks. Thus there is no normalized-state error guarantee tending to zero as a function of eta alone uniformly over such inputs; the dependence on relative error and sample mass is essential. The two normalized vectors are not proportional, so this is not merely a removable global-sign example.

### Partial-credit rubric

Score out of 10. Credit mathematically valid alternative derivations; the stated criteria assess correctness, not wording.

| Points | Criterion |
| --- | --- |
| 2 | Proves basis nonnegativity on the actual interval and partition of unity (1 point), then obtains \|ptilde(t)-p(t)\|<=eta using coefficient errors and nonnegative weights (1 point). Nonnegative coefficients must not be assumed. |
| 2 | Derives \|\|x-y\|\|<=eta sqrt(M) by summing squared coordinate errors (1 point), and derives \|\|x\|\|>=sqrt(m)>0 plus \|\|y\|\|>=sqrt(m)-eta sqrt(M)>0 with the strict small-error premise (1 point). |
| 2 | Checks that both vectors are nonzero in the same finite Euclidean space and correctly composes the supplied result to get normalized distance<=2 eta sqrt(M/m) (1 point); gives the sufficient precision eta<=epsilon sqrt(m)/(2 sqrt(M)) for 0<epsilon<2 and verifies nonzeroness, after establishing M>0 (1 point). |
| 2 | Shows sampled endpoints equal the corresponding coefficients and yield m=a^2 without positivity, including d=0 (1 point); correctly handles signed values, eta=0, zero sampled mass and the impossibility of M=0 under m>0 (1 point). |
| 2 | Supplies a legal explicit shrinking-mass family with eta->0 and computes a fixed positive normalized error (1 point), then explains why it refutes any mass-independent error guarantee vanishing with eta rather than contradicting the relative-error theorem (1 point). |

### Common errors

- Using a bound (d+1)eta and missing that partition of unity removes the degree factor in the sharp coefficient-to-value estimate.
- Replacing the Euclidean sample bound by eta rather than eta sqrt(M), or incorrectly using M eta as the intended square-root scaling.
- Invoking normalization stability before verifying nonzero original and perturbed vectors.
- Assuming signed coefficients or sample amplitudes must be nonnegative because the Bernstein weights are nonnegative.
- Claiming an endpoint coefficient anchors sample mass even when that endpoint is not sampled.
- Dividing by sqrt(M) at M=0 or presenting empty samples as compatible with positive mass.
- Inferring an absolute normalized-state accuracy guarantee from eta alone while the target mass can approach zero.

### Boundary cases

- {"case": "d=0", "resolution": "The sole basis function is 1; both endpoint formulas refer to c_0, with no exceptional division or negative exponent."}
- {"case": "M=0", "resolution": "Positive mass is infeasible. Raw bounds have a zero-vector interpretation; normalized states and the precision formula with 1/sqrt(M) are not instantiated."}
- {"case": "eta=0", "resolution": "Equal coefficients give equal raw and, under positive mass, normalized vectors."}
- {"case": "Signed values or zero coefficients", "resolution": "The perturbation argument uses absolute errors and nonnegative weights, not positivity of coefficients or all samples."}
- {"case": "Mass tends to zero", "resolution": "The explicit endpoint-sampled degree-one family has eta->0 and fixed positive normalized error; no uniform mass-free continuity guarantee follows."}
- {"case": "Endpoint sample with nonzero coefficient", "resolution": "A single actual sampled endpoint of magnitude at least a gives squared mass at least a^2, even if other samples vanish or have negative sign."}

### Difficulty annotation

```json
{
  "D0": {
    "facet": "Separate coefficient accuracy, raw sample-vector error and normalized-state error; normalization needs a quantitative positive mass, not sign restrictions.",
    "adds_core": false
  },
  "construction_band": "D3",
  "status": "provisional_mathematical_route_annotation_not_measured_difficulty",
  "rationale": "The route joins interval basis weights, finite-dimensional error accumulation, an independent positive-mass certificate and an explicitly supplied normalization-stability result. Each interface retains its interval, norm, nonzero and strict-error premises; the endpoint and shrinking-mass tests audit that composition.",
  "taxonomy_source": "benchmarks/quantumcomputingbench/tracks/lean/COURSE.md:19-30",
  "D1_D4_context": {
    "D1": "Precise statement reading and a disclosed library application.",
    "D2": "Local symbolic construction and entry/sum reasoning.",
    "D3": "Joining mathematical interfaces with every AND premise preserved.",
    "D4": "Parametric induction and global invariant/representation or degree control."
  },
  "shortcut_disclosure": "Supplying the full target theorem could reduce this to a library application; the question instead requests the stated derivation. Graph distance, source length and node count do not measure this band.",
  "model_calibration": "unmeasured"
}
```

### Author-supplied reasoning map

These are natural-language mathematical dependencies, not extracted Lean proof-term dependencies. All required inputs at a step are conjunctive.

| Input | Kind | Statement |
| --- | --- | --- |
| C4-I1 | assumption | d,M are finite natural numbers, basis B_{d,r} has the displayed polynomial formula, and every sample lies in [0,1]. |
| C4-I2 | assumption | Coefficient errors obey \|ctilde_r-c_r\|<=eta with eta>=0; raw vectors x,y are the evaluations at the same sample list. |
| C4-I3 | assumption | \|\|x\|\|^2>=m>0 and eta sqrt(M)<sqrt(m). |
| C4-I4 | convention | Euclidean norms and signed amplitudes are retained; empty samples give mass zero and zeroth powers evaluate to one. |
| C4-I5 | supplied_obligation | For nonzero x,y in a finite-dimensional real or complex Euclidean space, \|\|x/\|\|x\|\|-y/\|\|y\|\|\|\| <= 2\|\|x-y\|\|/\|\|x\|\|; if \|\|x-y\|\|<=delta<\|\|x\|\| then y is nonzero. |
| C4-I6 | assumption | For the precision branch 0<epsilon<2 and eta<=epsilon sqrt(m)/(2 sqrt(M)) after M>0 is established. |
| C4-I7 | assumption | For the endpoint branch an endpoint is actually sampled and its corresponding original coefficient has magnitude at least a>0. |

**C4-S1: Establish the two basis facts.**

Assumptions: ["Real samples in [0,1]; degree d>=0."]. Required inputs (AND): C4-I1, C4-I4.

Conclusion: B_{d,r}(t)>=0 and sum_{r=0}^d B_{d,r}(t)=1.

Justification: Nonnegative powers and binomial theorem; d=0 uses the constant polynomial convention.


**C4-S2: Bound each evaluated error.**

Assumptions: ["All coefficient errors are bounded by eta."]. Required inputs (AND): C4-S1, C4-I1, C4-I2.

Conclusion: |ptilde(t)-p(t)|<=eta for t in [0,1].

Justification: Triangle inequality and the nonnegative unit-sum weights.


**C4-S3: Accumulate errors over the full sample list.**

Assumptions: ["There are M coordinates, including repetitions."]. Required inputs (AND): C4-S2, C4-I1, C4-I2, C4-I4.

Conclusion: ||x-y||<=delta=eta sqrt(M).

Justification: Square the coordinate bounds, sum M terms and take nonnegative square roots.


**C4-S4: Produce the original nonzero and feasible-dimension facts.**

Assumptions: ["Positive lower sample mass."]. Required inputs (AND): C4-I1, C4-I3, C4-I4.

Conclusion: ||x||>=sqrt(m)>0 and M>=1.

Justification: Monotonicity of the square root; M=0 would give mass zero, contradicting m>0.


**C4-S5: Produce a positive perturbed norm.**

Assumptions: ["Strict error-to-mass inequality."]. Required inputs (AND): C4-S3, C4-S4, C4-I3.

Conclusion: ||y||>=sqrt(m)-eta sqrt(M)>0.

Justification: Reverse triangle inequality; in particular delta<||x||, so the supplied nonzero criterion also applies.


**C4-S6: Compose the supplied normalization interface.**

Assumptions: ["Both vectors nonzero, same finite Euclidean space, and the verified raw error and original norm bounds."]. Required inputs (AND): C4-I1, C4-I4, C4-I5, C4-S3, C4-S4, C4-S5.

Conclusion: ||x/||x||-y/||y||||<=2 eta sqrt(M/m).

Justification: Apply the supplied 2delta inequality, then substitute the proved numerator upper bound and positive denominator lower bound.


**C4-S7: Translate target accuracy into coefficient precision.**

Assumptions: ["0<epsilon<2 and M>0."]. Required inputs (AND): C4-I3, C4-I6, C4-S4, C4-S5, C4-S6.

Conclusion: The precision condition implies nonzero y and normalized error<=epsilon.

Justification: Multiplication by sqrt(M) yields delta<=epsilon sqrt(m)/2<sqrt(m), followed by the normalized bound.


**C4-S8: Supply a concrete mass certificate from a sampled endpoint.**

Assumptions: ["An endpoint is sampled and its original coefficient magnitude is at least a."]. Required inputs (AND): C4-I1, C4-I4, C4-I7.

Conclusion: p(0)=c_0, p(1)=c_d and m=a^2 is a valid positive lower mass.

Justification: Evaluate the basis at the endpoints; one squared coordinate supplies the bound, including d=0.


**C4-S9: Demonstrate the shrinking-mass obstruction and remaining boundaries.**

Assumptions: ["d=1,M=2,samples 0 and 1,c=(a,0),ctilde=(a,a/2),a>0."]. Required inputs (AND): C4-I1, C4-I2, C4-I4, C4-S3, C4-S4, C4-S6, C4-S8.

Conclusion: eta=a/2 tends to zero while normalized distance=sqrt(2-4/sqrt(5))>0; m=a^2 shrinks and the strict premise still holds.

Justification: Compute endpoint vectors and their norms directly; eta sqrt(2)=a/sqrt(2)<a. Separately eta=0 gives equality and zero mass/M=0 are infeasible under the positive-mass premise.

Reuse and reconvergence:

```json
{
  "reused_results": [
    {
      "id": "normalization-stability-2delta",
      "producer_slot": "A2",
      "supplied_input": "C4-I5",
      "consumer_steps": [
        "C4-S6"
      ],
      "status": "The exact interface is explicitly supplied in this question; no hidden access to A2 answer or assumption of a different split is required."
    },
    {
      "id": "Bernstein-nonnegative-unit-weights",
      "producer": "C4-S1",
      "consumer_steps": [
        "C4-S2"
      ],
      "status": "Derived from formula; grounded in inspected basis_nonneg and basis_sum."
    },
    {
      "id": "endpoint-evaluation",
      "producer": "C4-S8",
      "consumer_steps": [
        "C4-S9"
      ],
      "status": "The same coefficient-to-endpoint map supplies the positive-mass anchor and the explicit small-mass family."
    }
  ],
  "reconvergent_branches": [
    {
      "branches": [
        "C4-S1 -> C4-S2 -> C4-S3",
        "C4-S4"
      ],
      "join": "C4-S5",
      "why": "The independently derived raw error bound and positive original mass must both be present to conclude y nonzero."
    },
    {
      "branches": [
        "C4-S3",
        "C4-S4",
        "C4-S5",
        "C4-I5"
      ],
      "join": "C4-S6",
      "why": "Supplied normalization stability requires both nonzero vectors and combines a numerator error upper bound with a denominator norm lower bound."
    }
  ]
}
```

### Sources and evidence boundary

- [QuantumBlockEncoding/HermiteBernstein.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/HermiteBernstein.lean): Lines 21-32: exact Bernstein basis and interval nonnegativity; lines 327-346: partition of unity and coefficient bounds; lines 457-459: endpoint-zero evaluation; entire 479-line module read. SHA-256 `661618d9c10826491ee293c7c411ac2d55056426739f4bbfd3e7c410c05e4bff`. MIT (repository LICENSE)
- [QuantumBlockEncoding/RealAmplitudePreparation.lean](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/6b23dab68c2970062ddfd568ce94bce74b566483/QuantumBlockEncoding/RealAmplitudePreparation.lean): Lines 1-14: imports, namespace and convention header; lines 203-222: marginal and full squared norm; lines 310-324: normalized_sum_sq and positive-mass boundary. SHA-256 `a6ded7e65a7e42d5724529befb48eefc9505814136206dd96248fb59b3c45efa`. MIT (repository LICENSE)

Complete source checks, separate reading/import/conceptual/dependency records, overlap and uncertainty are in the JSON payload.

- At authoring freeze, the complete coefficient-to-normalized-state composition and shrinking-mass example await distinct content-bound review.
- The shared normalization theorem is supplied explicitly as an interface from planned slot A2; this consumer does not claim a new Lean proof of that theorem.
- The source basis and finite-table normalization lemmas do not by themselves certify this complete new question, gate complexity, floating-point implementation or any model result.
- At authoring freeze, a2/C4 and A3/C4 shared result exposure and the existing cross-split normalization fragments require semantic split reconciliation before admission.

---
