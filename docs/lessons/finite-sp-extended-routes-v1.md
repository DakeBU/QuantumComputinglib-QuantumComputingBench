# Finite primitive state-preparation contracts — retrospective AUTHOR/WIP

This packet describes the complete current implementation of three modules,
not the full algorithms of the papers whose names occur in their identifiers.
It is an implementation-informed, retrospective mathematical contract. The
historical formalizer is UNKNOWN. The present author read the actual complete
implementation, including private declarations and local proof terms; this is
not independent source-topology extraction. Nothing here is accepted evidence,
a fresh Lean build, a kernel-only result, a numerical simulation, or a source
fidelity verdict. Separate fresh workers must decode the frozen formal-only
track and review it against this proposed contract and the pinned raw sources.

## 1. Exact carrier and semantic conventions

For n wires, a basis assignment is a function b : Fin n → Fin 2. Flat indices
are k = Σ_j 2^j b(j), in Fin(2^n); wire q0 is least significant. We write
|q(n−1)…q0⟩ when displaying bit strings. In two wires, flat 1 is |01⟩,
not |10⟩; in three wires, flat 2 is |010⟩ and flat 4 is |100⟩.
`primitiveBasisLEEquiv` fixes this correspondence and `primitiveLEBits` is
its inverse. All states are complex column vectors of length 2^n. The
computational vector |k⟩ is the delta function, and |0^n⟩ selects column 0
under matrix-vector multiplication. There is no density-matrix, measurement,
sampling, or implicit normalization convention here.

Define R(c,s) = [[c,−s],[s,c]]. Standard physical RY(θ) is
R(cos(θ/2),sin(θ/2)), with the minus sign in the upper-right entry.
Let α = 2 arccos(3/5), β = 2 arccos(5/13), and γ = π/2.
The exact angle expressions are `ryAngle35`, `ryAngle513`, and
`bellRyAngle`; the zero angle is `ryAngleZero`. Since the relevant cosine
values lie in [−1,1], and sin(arccos c) is nonnegative, the unit-circle
equations give

    RY(α) = [[3/5,−4/5],[4/5,3/5]],
    RY(β) = [[5/13,−12/13],[12/13,5/13]],
    RY(γ) = [[a,−a],[a,a]], a = sqrt(2)/2 > 0,
    RY(0) = I.

These are exact real expressions embedded in ℂ, not rounded angles.
`standardRyMatrix_ryAngle35_explicit`,
`standardRyMatrix_ryAngle513_explicit`, and the Compact private
`standardRyMatrix_ryAngle513_explicit_paper` only expose the already available
rational entries after coercion; they introduce no second rotation semantics.
The Bell angle evaluation is π·(1/2)=π/2, and its matrix is the existing
`warmRobinUniformBitPrepare`. These are dependency results, not hypotheses
added to any finite state-preparation theorem.

CX(c,t) preserves the control and all non-target wires and flips the target
iff the control is 1. Its matrix entry at row r, column s is 1 precisely when
the bits of r equal this permutation applied to the bits of s, otherwise 0.
This is the full statement of `evalPrimitiveCircuitLE_singleton_cx_apply`,
for arbitrary n, two distinct typed wire indices, and arbitrary row/column.
The logical `distinct` argument is a wire-separation requirement, not an
assumed CX correctness theorem.

A circuit is a chronological list of typed X/RY/RZ/CX gates. Appending A then
B denotes U(B)U(A). Matrix reindexing by the single fixed LE equivalence
defines `evalPrimitiveCircuitLE`; it is not a second interpreter. All such
primitive circuit matrices are unitary by the reused semantic substrate.
Every equality below is exact as a complex vector/operator, including its
global and relative phases. No quotient by global phase is used.

## 2. UCRY specification and the exact compiler being counted

For target t, let κ_t(b) be b restricted to all other wires. Given a tuple
of control wires w_i distinct from t and an angle function A on their bits,
the uniformly controlled matrix is

    U_A(r,s) = 0                                      if κ_t(r) ≠ κ_t(s),
             RY(A((r(w_i))_i))[r(t),s(t)]             otherwise.

Thus every non-target wire, not just the named control tuple, is preserved.
Within an equal-context block either row or column supplies the same control
assignment. The generic compiler theorem supplies this complete operator
semantics. The finite entry theorems do not infer it from just a few samples.
Control tuples need not be injective in the general theorem: only
`∀ i, w_i ≠ t` is required. The concrete tuples used here are distinct.

The reused reference recursive compiler consumes the first control, recursively
compiles half-sums of its two angle branches, emits CX, compiles half-differences,
and emits CX again. For one control with branch angles A0,A1, its exact list is

    RY_t((A0+A1)/2); CX(c,t); RY_t((A0−A1)/2); CX(c,t).

On control 0 the effective angle is the sum of the two half angles, A0;
on control 1, X conjugates the second rotation to its negative, leaving A1.
The recursive proof repeats this per fixed non-target context. m controls
emit 2^m RY and 2(2^m−1) CX gates. This is the reference recursive compiler,
not an optimized Gray-code implementation. Zero-angle RY instructions and
canceling CX instructions remain in its list and are counted.

## 3. Bell route: complete natural statement and proof

The input is |00⟩. The exact target `bellState` is (a,0,0,a), with
`bellTarget.normalization` expanded to Σ_(k<4) normSq(bellState(k)) = 1.
The source string in the target is metadata, not a mathematical premise.
The typed list `bellPrimitiveCircuit` is

    RY_q0(π/2); CX(q0,q1).

`bellRyCircuit` and `bellCxCircuit` are its two singleton subcircuits;
`bellControl=0`, `bellTargetWire=1`, and their inequality is proved inside
the module. There are exactly two target wires and no other register.

By the one-wire lift formula, the first RY has column 0 equal to
(a,a,0,0): q1 must stay 0, while the q0 entries are the first column (a,a)
of RY(π/2). The four private `bellRy_entry_{00,10,20,30}` facts are exactly
these entries; the four `bellAfterRy_{0,1,2,3}` facts expose the same
coordinates of `bellAfterRy = a|0⟩+a|1⟩`. Componentwise equality proves
`bellRy_col_zero`, and the column-selection identity proves
`bellRy_prepares`.

CX(q0,q1) maps indices 0→0, 1→3, 2→2, 3→1. Only input columns 0 and 1
are required for this state, and all their four rows are explicitly proved:

| output row | CX[row,0] | CX[row,1] | a CX[row,0]+a CX[row,1] |
|---|---:|---:|---:|
| 0 | 1 | 0 | a |
| 1 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 |
| 3 | 0 | 1 | a |

The eight private CX entry declarations encode this table; the four
`bellCx_output_i` lemmas encode its final column. Matrix linearity on
a|0⟩+a|1⟩ then proves `bellCx_on_afterRy`. Applying the append matrix
identity and associativity of matrix-vector action composes the two stages,
proving `bellPrimitive_prepares_target` without a new premise. The Bell target
is normalized since 2a²=1, with normalization supplied by the existing target
provider. `bellPrimitiveRoute` packages that proof, this exact circuit, and
the exact vector equality in `ExactPrimitiveStatePreparationRoute 2`.

The root is not a proof that the evaluated Bell circuit equals the separate
provider matrix `bellMatrix` on every input. Only the common target/first
column is required; unitarity of the actual primitive circuit comes from the
generic primitive semantics rather than from identifying two unitary completions.

## 4. Dense fixed two-wire route: entries, linearity, composition

The target `mottonenDenseState` is

    ψ_M = (39,52,60,144)/169.

The input is |00⟩. `mottonenConditionalAngles` chooses α when q1=0 and
β when q1=1. Its public Compact definition is an alias of the EntryCertificates
definition, not a new angle function. `mottonenDenseUcryCircuit` is likewise
an alias of the same typed reference compiler output with control q1, target
q0, and its internally proved distinctness. `mottonenDensePrimitiveCircuit`
first applies RY_q1(β), then this UCRY circuit.

The root RY preserves q0 and creates

    χ_M = (5/13)|0⟩ + (12/13)|2⟩ = (5/13,0,12/13,0).

The four private `mottonenRootState_i` facts list these coordinates. The
singleton-RY lift and β matrix prove `mottonenRootRy_col_zero` by all four
rows, and column selection gives `mottonenRootRy_prepares`.

For the UCRY, the context is exactly q1; its two 2×2 blocks on (0,1) and
(2,3) are RY(α) and RY(β). EntryCertificates proves the four nonzero entries
needed from input columns 0,2 and the general context-mismatch zero theorem.
Compact reuses those facts through four private aliases, then proves the
cross-context entries 02,12,20,30 are zero via `mottonenZeroEntry`:

| row r | U_M[r,0] | U_M[r,2] | (5/13)U_M[r,0]+(12/13)U_M[r,2] |
|---|---:|---:|---:|
| 0 | 3/5 | 0 | 39/169 |
| 1 | 4/5 | 0 | 52/169 |
| 2 | 0 | 5/13 | 60/169 |
| 3 | 0 | 12/13 | 144/169 |

Each row of the last column is a separate private
`mottonenDenseUcry_scalar_i` lemma. The scalar form of the reused two-basis
linearity theorem identifies the output of U_M on χ_M with that column,
yielding `mottonenDenseUcry_on_root`. Thus every coordinate and every
off-context zero needed for the action has a provider; no arbitrary-width
amplitude-loading assumption is inserted. Append semantics composes this
with root preparation and proves `mottonenDensePrimitive_prepares_target`.
Normalization is literal: 39²+52²+60²+144²=169². The imported normalization
proof and exact preparation theorem populate `mottonenDensePrimitiveRoute`.

This is a complete ideal primitive state-action witness for this one target.
It is not a formalization of a general Möttönen arbitrary complex-vector
algorithm, general phase-loading algorithm, or its optimum asymptotic cost.
In particular all chosen output amplitudes are positive reals. The separate
rational-quaternion `mottonenDenseMatrix` is not asserted equal to U of this
circuit. It provides the same target in a different matrix-level completion.

## 5. Sparse fixed three-wire route: complete support and preserved wires

The target is

    ψ_S = (3/13)|0⟩+(4/13)|2⟩+(12/13)|4⟩
        = (3,0,4,0,12,0,0,0)/13.

These are the three bit strings |000⟩, |010⟩, |100⟩. All n=3 wires are
part of the target register, not extra ancillas. In particular q0 stays 0
for this input, but it is still a target-register coordinate. The root
RY_q2(β) prepares

    χ_S = (5/13)|0⟩+(12/13)|4⟩.

The eight private `sparseRootState_i` coordinates are (5/13,0,0,0,12/13,0,0,0).
The singleton-RY formula, including the requirement that q0,q1 remain 0,
proves all eight rows of `sparseRootRy_col_zero`; `sparseRootRy_prepares`
then follows by column selection.

`sparseControlWire` sends its unique control position to q2, and the target
is q1. The inequality q2≠q1 is proved. `sparseConditionalAngles` chooses α
on q2=0 and 0 on q2=1. The exact reference compiler produces
`sparsePrunedUcryCircuit`; `sparsePrunedCircuit` is the root RY followed by
that list. “Pruned” is the route name, not evidence that the compiler erases
zero-angle instructions. Here both q0 and q2 are preserved by the UCRY.

The non-target context is (q0,q2), not merely the control bit q2.
EntryCertificates proves the four on-context entries below and a theorem
that any mismatch in the full context gives zero. Compact uses
`sparseZeroEntry` for every remaining entry in columns 0 and 4:

| row r | U_S[r,0] | U_S[r,4] | (5/13)U_S[r,0]+(12/13)U_S[r,4] |
|---|---:|---:|---:|
| 0 | 3/5 | 0 | 3/13 |
| 1 | 0 | 0 | 0 |
| 2 | 4/5 | 0 | 4/13 |
| 3 | 0 | 0 | 0 |
| 4 | 0 | 1 | 12/13 |
| 5 | 0 | 0 | 0 |
| 6 | 0 | 0 | 0 |
| 7 | 0 | 0 | 0 |

The row-6/column-4 zero is an on-context matrix entry of RY(0), not a
context-mismatch zero. That distinction matters and is preserved. In contrast,
the twelve Compact helper entries 10,30,40,50,60,70,04,14,24,34,54,74
all follow from unequal full contexts. The eight private
`sparsePrunedUcry_scalar_i` lemmas give the last column, and scalar
two-basis linearity proves `sparsePrunedUcry_on_root`. Composition proves
`sparsePruned_prepares_target`. Normalization is 3²+4²+12²=13²;
`sparsePrunedRoute` supplies it from the existing target provider and attaches
the exact circuit action, not a merely named preparation circuit.

## 6. Generic zero-angle identity and a genuine alternative route

`zeroAngleCompiledUcry_eval_eq_one` has arbitrary wire count and control count.
For any supplied control tuple whose entries are distinct from target t,
compiling the constant zero angle function denotes the complete identity
operator on all primitive basis states. It does not merely fix |0…0⟩.

Proof: use the existing compiler's block-diagonal specification. If row and
column contexts differ the matrix entry vanishes, as does the identity entry.
If contexts agree, RY(0)=I on the target bit. Under this equal-context
condition, equality of full basis assignments is equivalent to equality of
the target bits, because `splitPrimitiveWire` is an equivalence. Thus the
remaining delta equals the identity delta. This proof is valid with zero
controls, zero/other finite dimensions where the typed target exists, and
repeated control-wire entries; it does not assume an injective control tuple.

For the sparse dense-tree alternative, `sparseDenseControlWires` is the ordered
tuple (q1,q2), target q0, with both required inequalities proved. The
constant-zero two-control compiler list is `sparseZeroFillCircuit`.
`sparseZeroFill_eval_eq_one` instantiates the generic theorem; reindexing
identity proves `sparseZeroFill_evalLE_eq_one`. Therefore

    U_LE(sparseDenseTreeCircuit)
      = U_LE(sparseZeroFillCircuit) U_LE(sparsePrunedCircuit)
      = U_LE(sparsePrunedCircuit).

This is the full operator equality `sparseDenseTree_evalLE_eq_pruned`.
It implies `sparseDenseTree_prepares_target` and supplies a second record
`sparseDenseTreeRoute` for exactly the same ψ_S. Both routes remain valid
sufficient alternatives (an OR), not prerequisites simultaneously needed for
one state-action claim. The dense-tree proof currently reuses the pruned
proof and a full identity-block certificate; that Lean/proof dependency is an
AND and must not be confused with algorithmic OR sufficiency.

## 7. Exact costs, schedules and what they do not mean

`ExactPrimitiveStatePreparationRoute.cost` records auxiliaryQubits=0,
gateCount=circuit.resource.gates, depth=circuit.resource.depth, and
oracleCalls=circuit.resource.oracleCalls. The `Resource` gate count is
one-qubit count + CNOT count + oracleCalls. Typed primitive resources have
zero oracle calls and no added ancilla. Scheduling maintains a depth per
wire; a gate goes one layer after the largest depth on wires it touches.
Disjoint gates may overlap even when separated in the chronological list.

| exact route | target wires | RY | CX | (auxiliaryQubits, gateCount, depth, oracleCalls) |
|---|---:|---:|---:|---|
| Bell | 2 | 1 | 1 | (0,2,2,0) |
| dense fixed target | 2 | 3 | 2 | (0,5,4,0) |
| sparse pruned | 3 | 3 | 2 | (0,5,4,0) |
| sparse dense-tree | 3 | 7 | 8 | (0,15,13,0) |

These tuple equalities are exactly `bellVerified_cost`,
`mottonenDenseVerified_cost`, `sparsePrunedVerified_cost`, and
`sparseDenseTreeVerified_cost`. The body of each theorem is `by decide`;
this author did not execute it. The 1-control UCRY has four gates. Its
first target RY can be in layer 1 together with the disjoint root RY;
the succeeding shared-wire CX, RY, CX occupy layers 2,3,4. The two-control
zero fill adds 4 RY+6 CX, all retained even though its full operator is I.
Its first RY_q0 can occupy layer 1; the rest reach layers 5 through 13 after
meeting q2/q1 dependencies. This explains depth 13 rather than naïvely
adding list lengths or block depths.

`BlockEncodingCost.betterThan` is the full lexicographic disjunction:
fewer gates OR (same gates AND (less depth OR (same depth AND (fewer
auxiliaries OR (same auxiliaries AND fewer oracle calls))))).
`sparsePruned_betterThan_denseTree` takes the first sufficient branch because
5<15. This is a comparison only of these exact same-target circuit lists.
It is not a lower bound, universal gate optimality, or asymptotic sparse-state
improvement. The other disjuncts stay part of the definition and are not
discarded as though the resource order had only one criterion.

This is ideal logical exact-real RY/CX cost with a wire-conflict scheduler.
There is no finite-bit angle approximation, Clifford+T compilation, hardware
connectivity/routing, noise, measurement/readout, classical preprocessing cost,
oracle construction cost, state-input query model, numerical runtime, or
uniform family complexity theorem. The zero oracle field describes the explicit
primitive lists; it does not establish free access to arbitrary input data.
No postselection or amplitude amplification occurs and there is no nontrivial
success branch. These unitaries act deterministically on the fixed clean input.

## 8. Expanded record/binder and definition boundary

The provider record `ExactPrimitiveStatePreparationRoute n` contains a
`StatePreparationTarget ℂ n`, a typed circuit, a proof of that target's
normalization predicate, and the actual equality U_LE(circuit)|0^n⟩=amplitudes.
The generic target record stores its normalization as an arbitrary Prop;
therefore the generic type alone is not a theorem of unit norm. Here all four
constructed records use the three concrete predicates displayed above, with
the corresponding imported norm-square proofs. Unitarity is derived for every
typed circuit; it is not a freely selectable `isUnitary : Prop` field of these
route records. Nothing is accepted merely because a record is named Verified.

Each finite root theorem and cost theorem has no extra external proof
hypothesis. The generic singleton CX and zero-UCRY lemmas take dimensions,
wire indices and wire-separation proofs; the entry-mismatch lemmas take row,
column and the precise mismatch proposition. Private `mottonenZeroEntry` and
`sparseZeroEntry` have the same exact context hypothesis as their supplier.
No producer theorem has been moved into a public finite root's premises.
The per-declaration audit covers every header, including binders implicit in
the exact source syntax and propositions expanded through provider definitions.

Every definition introduced by these three targets is literal relative to
this original fixed construction contract: explicit angle syntax, wire constants,
lists/compiler calls, finite linear combinations, direct provider aliases, or
proof-bearing record assembly. None uses classical choice to select a unique
object, none claims uniqueness of unitary completion, and none is a
quotient/representative modulo phase. `noncomputable` marks exact mathematical
semantics, not either a runtime proof or a runtime impossibility argument.

## 9. Source fidelity and remaining gates

The raw implementation is the pinned source for this retrospective packet.
All three complete modules are in scope, including their module comments,
private helpers, local let/have bindings, imports, local simp attributes and
exact theorem bodies. The coverage manifests dispose every source line;
the inventory JSON retains each complete raw/masked command binding, header,
body and extent. Line disposition is not independent semantic acceptance.

The module comments label finite Bell, Möttönen, Li--Luo and dense/sparse
benchmarks and describe scalar-certificate reuse. We adopt only the finite
literal claims supported above. The target source-string reference to Li--Luo
Eq. (2) is an identifier inside existing code, not evidence this author read
that paper/equation. Full named-paper correctness, their assumptions, full
algorithm topology, phase-loading steps and general complexity remain
SOURCE_GAP for any future external-paper claim. No local proof failure here
refutes a paper; no external-paper repair is proposed.

Next gates: (1) fresh formal-only decoding of the whole three-module group,
(2) distinct anti-anchored source/semantic review, including all inventory rows,
(3) independently reviewed source topology for any external-paper Anchor,
(4) exact-current-input Lean and Tests evidence and publication binding,
(5) integration and reader/exposition gates. This author package cannot
self-approve those gates. Purification and Exposition Seal remain PENDING.
No production declaration was changed and no new foundation was introduced.
