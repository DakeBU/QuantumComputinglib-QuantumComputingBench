# Stored rectangular elimination with explicit exact-real counters

Evidence class: **RETROSPECTIVE_IMPLEMENTATION_INFORMED**. This mathematical source was reconstructed after inspecting an existing implementation. It is neither a pre-proof source nor a historical account, and makes no novelty claim. It is frozen for independent source-first review; it does not supply a review verdict, compilation result, publication admission, or Exposition Seal.

## S1. Carrier, accounting, and scope

Let N,M,n be natural numbers; write [n]={0,…,n−1}. A vector of length n is an indexed stored sequence. A stored N-by-M real matrix A is a vector of N stored row vectors, each of length M. Its denotation is the mathematical matrix D(A)(i,j)=A[i][j]. There is no orthogonality, square-shape, nonnegative-entry, rank, normalization, determinant, or nonzero-pivot hypothesis anywhere in the stored module's theorems. The scalar carrier is the exact real field, not floating-point numbers or finite strings.

The eight operation labels are field, sqrt, angle, trig, compare, read, write, emit. A cost C assigns a natural number C(q) to each label q; addition, zero, natural scaling, and order are pointwise. Write e_q for the cost which is one at q and zero elsewhere. The declaration `Op` lists precisely these labels (with decidable equality and finite enumeration); `Cost` is this function space, and `tick(q)=e_q`.

A counted run of an arbitrary type α is the pair (value∈α,cost∈Cost). These are the two fields `Run.value` and `Run.cost`. The constructor `Run.pure(x)` returns (x,0). To bind (x,C) to f, evaluate f(x)=(y,E) and return (y,C+E). The `Monad Run` instance uses these two literal definitions. No lawfulness, evaluation trace, or implementation-runtime theorem is asserted by that instance. `charge(q,x)` returns (x,e_q). None of these definitions checks how x or f(x) was obtained: an arbitrary real expression may be packaged by pure for zero charge. A Run-valued callback may therefore hide arbitrary uncharged work. Costs are annotations accumulated by these definitions, not an enforcement theorem that all possible scalar work is charged.

The primitive definitions `add`, `sub`, `mul`, `div` return the exact real sum, difference, product, quotient, each with e_field. `sqrt` returns Real.sqrt with e_sqrt; `arccos` returns Real.arccos with e_angle; `cos`,`sin` return the exact respective functions with e_trig. `zeroTest(x)` returns the Boolean truth of x=0 and `signTest(x)` that of x<0, each with e_compare. These operations are total mathematical functions: in particular real division and square root retain their library total-function semantics outside the usual numerical valid loci. The elimination algorithm below avoids a zero denominator on its nonzero branch. The module does not restrict the public primitives' domains.

This is a stipulated extended exact-real stored-word RAM model. Exact comparisons and transcendental evaluation each cost a unit in their own counter. Counter arithmetic, proof checking, index/bound proofs, control flow, tuple packaging/projection, and ordinary list construction overhead apart from the emitted-record charge are outside the model. It is not Lean evaluator runtime, a finite-bit runtime, a memory-space bound, a numerical stability result, a gate-synthesis bound, or a polynomial-in-qubits theorem. If N=2^n, a polynomial in N need not be a polynomial in n. A log length alone is not a runtime bound.

## S2. Storage primitives and the input boundary

`read(xs,i)` returns xs[i] with e_read for any vector and i∈[n]. `replace(xs,i,x)` returns the vector with entry i set to x, charging n(e_read+e_write) regardless of whether x equals the old entry. Replacement is persistent, full-copy replacement; for an outer matrix vector the copied words are row references, not all entries inside each row.

For any function f:[n]→Run α, `collect(f)` first materializes the vector of counted entries E_i=f(i). Its value is the projected vector (E_i.value)_i and its cost is

    Σ_i E_i.cost + n(2e_read+2e_write).

This describes two materialized passes: store the counted entries, then access them for value projection/counter summation and store projected outputs. The n(2e_read+2e_write) is the literal accounting convention; no lower-level machine simulation of these passes is asserted. Counter words are metadata. Crucially, f(i) is represented by one stored counted result, not separately rerun to obtain its value and cost.

The theorems `collect_value` and `collect_cost` state, respectively, for every i∈[n] and operation q,

    collect(f).value[i]=f(i).value,
    collect(f).cost(q)=Σ_i f(i).cost(q)+n(2e_read(q)+2e_write(q)).

For the first equality, vector construction stores f(i) at i and projection returns its first component. For the second, the stored vector's ith cost is f(i).cost; sum these and distribute natural scaling pointwise. These arguments require no hypothesis on f's charging honesty or computational behavior.

`StoredMatrix(N,M)` is the nested-vector carrier already defined; `denote` is D. For f:[N]→[M]→Run ℝ, `materialize(f)` is collect applied to i↦collect(j↦f(i,j)). Thus input callback evaluation is an explicit boundary, not silently an assumed constant-time matrix oracle. The exact statement `materialize_cost`, for each q, is

    materialize(f).cost(q)
      = Σ_i Σ_j f(i,j).cost(q)
        +(NM+N)(2e_read(q)+2e_write(q)).

Indeed each inner row contributes its callback sum and M times the storage charge; summing N rows gives NM copies, and the outer collect adds N. This charges only the callback's supplied counters plus storage, not any missing callback work. Materialization does not prove that an arbitrary callback used the primitive interface. It can be called for N=0 or M=0: when N=0 there are no row callbacks or charges; when M=0 and N>0 there are N empty row vectors and the outer 2N reads and 2N writes remain.

## S3. Literal angle and row formulas

Define r(x,y)=sqrt(x²+y²). The inherited exact preparation angle is represented by an `ExactAngle`: it is the rational-zero constructor when r=0, and otherwise the real constructor with value 2a, where

    a = −arccos(x/r) if y<0, and a=arccos(x/r) otherwise.

`ExactAngle.eval` maps these constructors to the real numbers 0 and 2a, respectively. The supplier's `pairNorm` is r, `splitAngle` is this exact expression, and `eliminationAngle(x,y)=−splitAngle(x,y).eval`. This is a literal definition, not a chosen solution of an existence predicate and not a quotient representative.

The counted `angle(x,y)` computes x*x, y*y, their sum, r, and the test r=0 in that order. If zero, it returns 0. Otherwise it computes x/r once, its arccos once, the test y<0 once, optionally 0−a to obtain the signed angle, then multiplies by 2 and subtracts from 0. The theorem `angle_value` identifies its value with eliminationAngle for every real x,y. To see this, x*x=x² and y*y=y² identify the two norms. In the zero branch both expressions are 0. In either nonzero sign branch they are the negative of twice the same signed arccos expression. There are no nonzero or sign premises to add.

For interpretation, r=0 iff x=y=0, since r²=x²+y² and both summands are nonnegative. When r>0, |x/r|≤1. If a is as above, cos(a)r=x and sin(a)r=y; the sign choice fixes the sine, including y=0. With θ=−2a, c=cos(θ/2), s=sin(θ/2), one obtains cx−sy=r and sx+cy=0 by substituting x=r cos(a), y=r sin(a) and cos²(a)+sin²(a)=1. This explains the distinct-row elimination mechanism. These polar identities are not extra assumptions or extra target-module theorems. In particular, one may not infer a distinct-row rotation law for a same-index update.

`coefficients(x,y)` runs angle once, divides θ by 2 once, computes cos and sin once each, and returns the ordered triple (θ,c,s). The theorem `coefficients_value` states precisely

    coefficients(x,y).value
      =(eliminationAngle(x,y), cos(eliminationAngle(x,y)/2),
        sin(eliminationAngle(x,y)/2)).

It follows by the angle identity and substitution into the three subsequent primitives. The half-angle and both trigonometric values are shared; they are not recomputed per matrix entry.

For any real c,s,u,v, `entryPair(c,s,u,v)` computes cu,sv,su,cv (four multiplications), then cu−sv and su+cv (one subtraction and one addition). The theorems `entryPair_value` and `entryPair_cost` give

    value=(cu−sv,su+cv),     cost(q)=6e_field(q).

Sequential bind adds exactly these six charges; tuple assembly is free in this model.

Given stored rows u,v of length M, `rowPair(u,v,c,s)` first collects an M-vector of entry pairs, reading u[j],v[j] and computing entryPair at each j. It then separately collects each of the first and second components by one read of the stored pair at each j. It returns the two materialized rows, not two callbacks. `rowPair_value` asserts the conjunction, for every j∈[M],

    first[j]=cu[j]−sv[j]  AND  second[j]=su[j]+cv[j].

Apply collect_value three times and the entryPair formula; the pair used by both projection passes is the same stored result. For `rowPair_cost`, the first pass contributes per column 6 field, 2 input reads plus 2 collect reads, and 2 writes. Each projection pass adds 1 pair read, 2 collect reads, 2 writes. Summing all three gives

    rowPair.cost(q)=M(6e_field(q)+10e_read(q)+6e_write(q)).

All row claims also hold for M=0; the value equality then has no legal column index and all these costs vanish.

## S4. Stored row update and one elimination

`rotate(A,i,j,c,s)` is defined for ALL i,j∈[N], without i≠j. It reads both original rows, computes rowPair once, replaces row j by the second output, then replaces row i by the first. All other rows remain their original stored values. It does not short-circuit i=j. In that case both input rows are the same original row, and the last replacement wins: row i becomes (c−s)A[i]. It is not generally an orthogonal two-row transformation.

The inherited mathematical `rotateRows(B,i,j,θ)` is the entrywise function

    cos(θ/2)B(i,k)−sin(θ/2)B(j,k)  if row=i;
    sin(θ/2)B(i,k)+cos(θ/2)B(j,k)  if row≠i and row=j;
    B(row,k)                         otherwise.

First-branch priority is part of the definition, even when i=j. The theorem `rotate_value`, with arbitrary stored A, i,j and real θ, states

    D(rotate(A,i,j,cos(θ/2),sin(θ/2)).value)
      =rotateRows(D(A),i,j,θ).

For row i, the last replacement yields the first rowPair formula. For a row different from i but equal to j, it yields the second formula. For neither, both replacements preserve the entry. This proof covers i=j without adding distinctness. `rotate_cost` adds two initial row-reference reads and two full copies of N references to the rowPair cost:

    rotate.cost(q)=M(6e_field(q)+10e_read(q)+6e_write(q))
                   +2N(e_read(q)+e_write(q))+2e_read(q).

`Elimination(N,M)` is exactly a stored matrix and a real angle; neither field is a correctness certificate. `eliminate(A,i,j,col)` reads the two row references and their col entries, runs coefficients on those entries, runs rotate with the resulting c,s, and returns the new matrix together with θ. It reuses θ,c,s, but rotate itself rereads the two original row references. Its public input col lies in [M]; hence an actual call requires M>0 and N>0. There is no distinctness premise. The two refinement theorems are

    eliminate_angle: returned angle
      =eliminationAngle(D(A)(i,col),D(A)(j,col));
    eliminate_matrix: D(returned matrix)
      =eliminateEntry(D(A),i,j,col),

where the supplier's literal eliminateEntry is rotateRows with that exact angle. The first follows from coefficients_value after the four reads; the second also uses rotate_value. No pivot-zero, orthogonality, determinant, or rank theorem is being asserted for arbitrary i,j. If both pivot values are zero, θ=0 and the matrix is unchanged, but the coefficient/row/copy work still occurs. A nonzero same-index call still follows first-branch priority, not a two-distinct-rows elimination theorem.

## S5. Fused sweep, log, and action

`Sweep(N,M)` has two fields: a stored matrix and a finite list of inherited `Step(N)` records. A Step consists of first,second∈[N], an adjacency equality first+1=second on their natural values, and a real angle. Adjacency implies distinctness. Its mathematical matrix is rotateRows applied to the identity with these ordered rows and angle. The supplier's `applySteps` applies these matrices chronologically: the head matrix acts first, then the tail acts on that result. Thus no reversal of the emitted list is implicit.

For fixed A, col∈[M] and natural lo,count, a call to `columnSweep` requires the logical premise lo+count<N, including at count=0. Its literal recursion is:

* At count=0 return A and the empty log with zero cost.
* At count=k+1, set i=lo+k and j=lo+k+1, eliminate the current A at (i,j,col), recursively sweep its returned matrix with count=k, prepend the current angle's adjacent Step to the returned list with one emit charge, and return the recursive residual with that list.

The computation of the tail therefore uses the updated matrix, not the original matrix or a precomputed angle table. The list prepending is performed after the recursive call, but its head describes the earlier executed elimination. This is one producer returning both outputs, not two executions to recover residual and log. Zero pairs are not pruned; they produce a zero-angle Step and one emit charge. There are no non-prefix/column-order assumptions: col is any member of [M], independent of lo.

The supplier has an uncounted matrix `columnSweep` following the same elimination recursion, and `columnSweepSteps` following the same changing matrices while consing each computed angle. `columnSweep_matrix` and `columnSweep_steps` identify the stored producer's residual denotation and log with these respective supplier outputs. For induction at k+1, eliminate_matrix identifies the first updated matrix, eliminate_angle identifies its angle, and the induction hypothesis on that updated matrix identifies the tail. At zero both identities are immediate.

The theorem `columnSweep_steps_length` gives exactly count records: each recursive stage conses one and the zero case contributes none. This length result uses the log refinement and the supplier's corresponding inductive length theorem; it is not itself the operation-cost proof.

The theorem `columnSweep_action` states

    applySteps(returned steps,D(A))=D(returned residual).

Its complete supplier AND-tail is: the stored matrix refinement AND the stored log refinement AND the supplier's columnSweepSteps_action. To understand that last supplier, the plane matrix times an arbitrary rectangular matrix equals rotateRows: expand the matrix product, and the identity matrix picks out the two indicated rows with the specified coefficients. This holds with the same first-branch priority. One chronological head step therefore implements exactly eliminateEntry; induction on the changing matrix identifies the rest. Combine this action identity with both stored refinements to get the stated stored action. No assumption that the residual is identity or that A is a full SO matrix is used. A general SO decomposition and qubit compilation are separate interfaces, not conclusions of this module.

Although arbitrary stored matrices and materialization allow empty dimensions, no columnSweep call exists when N=0 or M=0: the strict row bound rules out N=0, and col∈[M] rules out M=0. A zero-count call is legal only when lo<N and a column exists; it returns A, empty log and zero counters. Positive count is automatically on adjacent distinct rows. Neither empty-dimension coverage elsewhere nor the zero recursion equation removes these binders.

## S6. Branch-sensitive and uniform costs

The following vector entries are in the fixed order (field,sqrt,angle,trig,compare,read,write,emit). Put r=sqrt(x²+y²).

| Construction or branch | Counter vector |
| --- | --- |
| angle, r=0 | (3,1,0,0,1,0,0,0) |
| angle, r≠0 and y≥0 | (6,1,1,0,2,0,0,0) |
| angle, r≠0 and y<0 | (7,1,1,0,2,0,0,0) |
| angleBudget | (7,1,1,0,2,0,0,0) |
| coefficients, r=0 | (4,1,0,2,1,0,0,0) |
| coefficients, r≠0 and y≥0 | (7,1,1,2,2,0,0,0) |
| coefficients, r≠0 and y<0 | (8,1,1,2,2,0,0,0) |
| coefficientBudget | (8,1,1,2,2,0,0,0) |
| entryPair | (6,0,0,0,0,0,0,0) |
| rowPair on length M | (6M,0,0,0,0,10M,6M,0) |
| rotate | (6M,0,0,0,0,10M+2N+2,6M+2N,0) |
| eliminationBudget(N,M) | (6M+8,1,1,2,2,10M+2N+6,6M+2N,0) |
| stepBudget(N,M) | (6M+8,1,1,2,2,10M+2N+6,6M+2N,1) |
| materialize storage, excluding callback counters | (0,0,0,0,0,2NM+2N,2NM+2N,0) |

The angle branch counts follow the literal operations in S3: three fields precede the zero test, while a nonzero branch adds division, doubling and final negation-as-subtraction, with one more subtraction only on the negative-y branch. Both coefficients branches still pay one field division and two trig evaluations after angle. Thus `angle_cost_le` bounds angle pointwise by angleBudget; `coefficients_cost_le` adds e_field+2e_trig to obtain coefficientBudget. These are inequalities, not assertions that every branch attains the budgets.

`eliminationBudget` is defined as coefficientBudget plus the rowPair term, two full outer copies, and 6 reads: four before coefficients and two inside rotate. `eliminate_cost_le` follows from coefficients_cost_le and the exact rotate_cost by adding these four earlier reads. It does not substitute an input-entry callback for the stored representation. `stepBudget=eliminationBudget+e_emit`. The theorem `stepBudget_fields` states the conjunction of all eight scalar equalities in its table row; expand and evaluate the eight indicator functions to obtain each equality.

For count=k+1, `columnSweep_cost_succ` is the exact pointwise recurrence

    C(A,k+1;q)=E(A,i,j,col;q)
                  +C(eliminate(A,i,j,col).value.matrix,k;q)+e_emit(q),

with i=lo+k and j=lo+k+1. It follows because bind adds the eliminate, recursive-tail and charge costs and all final packaging is pure. This is an equality on the actual fused run, not a list-length proxy. For `columnSweep_cost_le`, induction gives tail≤k*stepBudget for the updated matrix, the elimination bound gives E≤eliminationBudget, and adding e_emit gives (k+1)*stepBudget. The base is the zero run. All inequalities are for every operation q individually and every legal A,col,lo,count,bound.

The theorem `columnSweep_emit` gives exactly C(A,count;emit)=count, independently of the length theorem. Elimination's emit counter is nonnegative and ≤eliminationBudget(emit)=0, hence is zero. The recurrence then adds exactly one at each stage. This proof's AND-tail is the successor cost recurrence AND the elimination emit-zero consequence AND induction, not merely the output list length.

The uniform vector bound is count times stepBudget. It counts all M columns of both rows, including columns unrelated to the eliminated pivot, all three collect passes, repeated stored row reads, full-copy replacements, scalar coefficient preprocessing, and emitted records. It excludes initial materialization unless that run is explicitly composed using bind; if composed, materialize_cost adds its complete supplied callback counters and storage counters once. No claim about finite-bit input evaluation, trigonometric approximation, roundoff accumulation, hardware instructions, qubit gates, or asymptotic polyqubit synthesis follows from these counters.

## S7. Binders, literal definitions, and coverage

All objects in this source are literal data/functions. There is no project-owned Prop bundle, typeclass hypothesis, classical-choice existence witness, quotient, or representative-independence condition in the stored interfaces. The Run, Elimination and Sweep records contain only data. The only inherited proof-bearing record is Step: its adjacency field is generated from the consecutive indices inside the sweep, not demanded as an additional public theorem hypothesis. The arbitrary Run-valued functions in collect and materialize are input DATA; charging honesty is explicitly not a theorem premise or conclusion.

The source's binders exhaust the module's binders: α,β are arbitrary types for generic counting/storage; natural dimensions form carriers; finite indices include their defining range inequalities; x,y,c,s,u,v,θ are arbitrary reals; A is any nested stored real matrix; u,v in rowPair are any stored M-rows; f is the appropriate generic counted callback; q ranges over all eight counters; and lo,count are naturals with the sole sweep premise lo+count<N. Type/carrier/index data are TYPING, and that strict sweep bound is a SOURCE domain condition (including in the successor recurrence). No orthogonality/distinctness/runtime-honesty hypotheses may be silently added. There are no STANDING or RULED assumptions and no intended EXCESS inputs. This classification is author evidence for review, not an independent verdict.

Coverage is exhaustive by sections: S1 covers Op, Cost, tick, Run including its fields, Run.pure, Run.bind, its Monad instance, charge, and all ten scalar/test primitives; S2 covers read, collect, replace, StoredMatrix, denote, materialize, collect_value, collect_cost, materialize_cost; S3 covers angle, angle_value, coefficients, coefficients_value, entryPair, entryPair_value, entryPair_cost, rowPair, rowPair_value, rowPair_cost; S4 covers rotate, rotate_value, rotate_cost, Elimination including both fields, eliminate, eliminate_angle, eliminate_matrix; S5 covers Sweep including both fields, columnSweep, columnSweep_matrix, columnSweep_steps, columnSweep_steps_length, columnSweep_action; S6 covers angleBudget, angle_cost_le, coefficientBudget, coefficients_cost_le, eliminationBudget, eliminate_cost_le, stepBudget, columnSweep_cost_succ, columnSweep_cost_le, stepBudget_fields, columnSweep_emit. The target has no private helper declarations. Automatically generated constructors/recursors and derived finite-enumeration machinery are not independent mathematical claims; their explicit carrier/fields/labels are covered here. Separate metadata records the mechanical source inventory and its limitations.

The construction graph is the storage substrate → cached scalar angle/coefficient producer → shared entry-pair materialization → persistent matrix update → one elimination → fused sweep. The cost proof graph is primitive charges AND collect/full-copy costs → exact row/update costs AND coefficient bound → elimination bound → successor recurrence AND induction → sweep bound/exact emission. The action graph is matrix refinement AND log refinement AND inherited chronological action → stored action. These are conjunctive supplier tails, not several independently sufficient arrows. They describe the existing implementation's reconstructed mathematical mechanism; source-first historical proof topology and elaborated Lean proof-term dependency extraction remain unclaimed.

Independent source-first review, source-blind decoding, comparison review, and integration/build/publication/purification gates are outstanding. This packet alone changes none of their statuses.
