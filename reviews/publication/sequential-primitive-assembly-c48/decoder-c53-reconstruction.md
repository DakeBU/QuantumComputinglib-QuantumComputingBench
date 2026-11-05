# Independent formal reconstruction: SequentialPrimitiveAssembly

Decoder identity: `agent:sequential_c53_formal_decoder`. Historical formalizer: UNKNOWN. Mathematical inputs: the frozen FORMAL_ONLY_SOURCE_WITHHELD packet and the requested FORMAL_ONLY_REQUESTED_PROVIDER supplement named in `chronology-and-pins.json`. Natural sources and their desired conclusions were not read. This is an interpretation seal, not a source-comparison verdict, compilation report, publication approval, or Exposition Seal.

## 1. Exact ambient objects

Write P(k) = Fin k → Fin 2. A basis label is a wire-indexed function, including the unique empty function when k = 0. A circuit on k wires is a list of PrimitiveGate k. The four gate constructors are X(target), Ry(target,angle), Rz(target,angle), and CX(control,target,distinct), where `distinct : control ≠ target` is part of CX's data. All targets are bounded Fin indices. Nothing in the target restricts stages to Ry and CX.

Angles are ExactAngle expressions: rational, rational times π, twice arccos of a bounded rational, twice arccos of the square root of a rational in [0,1], arbitrary real, sum, negation, and rational scale. Their evaluation is exact real evaluation, not floating-point rounding or an effective finite-bit angle producer. Angle-constructor guards restrict those particular constructors only; arbitrary `.real` remains available.

Matrices are complex, with row = output and column = input. Let E(c) denote evalPrimitiveCircuit c. Its empty-list value is the identity, and E(g :: rest) = E(rest) E(g). Consequently E(left ++ right) = E(right) E(left): list order is chronological gate order.

The supplement defines realOrthogonalRotation(c,s) by the four entries (c,-s;s,c); realRotation(a) substitutes cos(a),sin(a). Thus the provider's standardRyMatrix(θ) = realRotation(θ/2) is (cos(θ/2),-sin(θ/2);sin(θ/2),cos(θ/2)). Rz(θ) is diagonal with entries cos(θ/2)-i sin(θ/2), cos(θ/2)+i sin(θ/2). X flips its target bit. CX does nothing when the control bit is zero and otherwise flips its distinct target. A one-qubit lift has zero entries unless all other wires agree. The supplementary equivPermutationMatrix(e) has entry 1 exactly when row = e(column), otherwise 0.

Every circuit evaluates to a unitary by a supplied provider theorem, but the decoder did not execute Lean or validate its proof terms. The target uses circuits, not PrimitiveProgram: no separate globalPhase field is appended. Equalities below are exact complex-entry equalities, not equalities modulo global phase.

Fin.append a x places a on the first block and x on the second. Fin.snoc appends one final wire. `lastBasisEquiv` splits a basis into Fin.init and its last bit. `liftGate` replaces each old wire i by i.castSucc, preserving numeric position and angle. `liftLastMatrix M` is M tensored with identity on the new last bit, in that basis convention:

    liftLastMatrix M (snoc a u) (snoc b v) = if u = v then M a b else 0.

## 2. Padding and placement

`pad c extra` repeatedly lifts c onto an additional unused last wire. Its matrix is `padMatrix E(c) extra`, recursively M at zero and liftLastMatrix at successor. For all m,t,a,b,x,y, without any positivity restriction,

    padMatrix M t (append a x) (append b y) = δ[x=y] M(a,b).

Padding preserves ryCount, cxCount, and gateCount exactly. Here δ[P] is 1 when P holds, otherwise 0; this notation only abbreviates the displayed Lean conditionals and is not a new object in the module.

`stageWires q t` maps old local-plus-history layout [bond(q), fresh(1), history(t)] to new global layout [bond(q), history(t), fresh(1)]. Numeric action:

    old bond i < q -> i;
    old fresh q -> q+t;
    old history q+1+j -> q+j, for j<t.

It is an explicit equivalence with an explicit inverse, not a choice or a partial map. Its basis pullback is

    (snoc (append b x) bit) ∘ stageWires(q,t) = append (snoc b bit) x.

`placeStage t c` pads c : circuit(q+1) by t and then renames all wires by this equivalence. PrimitiveWireRename.circuit maps each gate's indices, keeping its angle and chronological position. Its matrix renaming satisfies matrix(e,M)(r,c) = M(r∘e,c∘e). Consequently, for arbitrary complex M,

    placedMatrix t M (snoc (append a x) u) (snoc (append b y) v)
      = if x = y then M (snoc a u) (snoc b v) else 0.

Only the bond and fresh final wire are acted on. Every historical wire is exactly a spectator at this stage, including off-clean input sectors. Placement preserves each of ryCount, cxCount, and gateCount. Renaming is represented as a relabeling of gate indices; no SWAP network is inserted or costed.

## 3. Whole sequential circuit and its clean-input amplitudes

Fix q : Nat and a total function stages : Nat → PrimitiveCircuit(q+1). Only stages 0 through n-1 occur at prefix length n. Define C(0) = [] on q wires and

    C(n+1) = map liftGate C(n) ++ placeStage n (stages n).

Thus stage 0 runs first, stage n runs after the lifted prefix, and a newly appended output wire starts as a fresh input wire. Internally the resulting layout is [bond(q), physical outputs in stage-time order(n)]. No measurement, reset, feed-forward, extra allocated workspace, or oracle instruction occurs in this construction.

The target separately defines A(0)=I and

    A(n+1) = placedMatrix n E(stages n) · liftLastMatrix A(n),

and proves E(C(n)) = A(n). This identity describes the whole matrix, not just its clean columns.

The provider Stage(B) is a matrix on Fin 2 × B, with bit first and bond second. For a local circuit c the adapter is exactly

    circuitStage(c)((bit,b),(bit',a)) = E(c)(snoc b bit, snoc a bit').

The provider run has boundary v : B→ℂ and is recursively

    run(U,v,0)(empty,b) = v(b),
    run(U,v,n+1)(snoc x bit,b)
      = Σ_a U(n)((bit,b),(0,a)) run(U,v,n)(x,a).

This uses the ZERO input column of the newly added bit at every step. It does not project any emitted output bit. `basisBoundary a` is the Kronecker delta on bond label a. For U(t)=circuitStage(stages t), the two clean-column theorems state, for every q,n,a,b,x,

    A(n)(append b x, append a zero_n)
      = E(C(n))(append b x, append a zero_n)
      = run(U,basisBoundary a,n)(x,b).

Equivalently this is the contraction over intermediate bond labels b_1,...,b_(n-1) of the local clean-column factors E(stages t)(snoc b_(t+1) x(t), snoc b_t 0), with b_0=a, b_n=b. For n=0 it is δ[b=a], using the empty product convention. This expansion is a mathematical reading of the recursion; the target itself states the recursive run equality.

The theorem `run_boundary_decomposition` allows ANY complex boundary v and ANY Stage family U on P(q), not just circuit-derived or unitary stages:

    run(U,v,n)(x,b) = Σ_a run(U,basisBoundary a,n)(x,b) v(a).

It needs no norm, support, nonzero, or positivity assumption. The proof expands the recursion, distributes finite sums, and interchanges their order. It does not assert that a general v is a normalized physical state.

## 4. Initial circuit and public output layout

`withInitial initial stages n = pad initial n ++ C(n)` executes initial on the q bond wires before stage 0. For every input bond basis a and output b, and every emitted basis x,

    E(withInitial)(append b x, append a zero_n)
      = run(U, v_a, n)(x,b),
    where v_a(c) = E(initial)(c,a).

The arbitrary a is not silently specialized to zero. Since initial is an actual circuit, v_a is a unitary matrix column; the target states the entry equality rather than packaging a normalized-state certificate. By linearity it also determines action on coherent bond superpositions in the clean physical-input sector, but this derived observation is not a separate theorem in the target.

`outputWires q n` maps internal [bond(q), history(n)] into public [physical(n), bond(q)], and REVERSES the physical block:

    old bond i -> n+i;
    old history q+j -> n-1-j.

Its inverse has the same physical reversal and restores the bond block. The basis theorem is

    (append x b) ∘ outputWires(q,n) = append b (x∘Fin.rev).

`publicCircuit` simply renames `withInitial` by outputWires. The exact final column theorem is

    E(publicCircuit)(append x b, append zero_n a)
      = run(U, (c ↦ E(initial)(c,a)), n)(x∘Fin.rev,b).

The stage-time bit t therefore occupies public physical wire n-1-t, and the bond wire i occupies public wire n+i. This reversal is separate from the little-endian numeric adapter in PrimitiveBasisLE: the target never calls primitiveBasisLEEquiv or converts its matrices to integer-indexed matrices. Where that provider is used elsewhere, its recursion gives wire 0 weight 1, wire 1 weight 2, etc.; that is not a license to remove the explicit reversal here.

No theorem in this target says that final bond b is fixed to zero or any other label, uncomputed, discarded, measured, or unentangled. All b remain in the output amplitude formula. The provider contains conditional terminal-core cleanup facts, but the target does not invoke them or supply their clean-column/support assumptions. Those facts cannot be promoted into unconditional cleanup for arbitrary stages.

## 5. Counts, guards, and zero dimensions

The target's stage-sum theorems give, separately for ryCount and cxCount,

    count(C(n)) = Σ_(t<n) count(stages t),
    count(withInitial) = count(initial) + Σ_(t<n) count(stages t).

For n,bound : Nat and the sole logical premise

    h : ∀ t < n, ryCount(stages t) + cxCount(stages t) ≤ bound,

both withInitial and publicCircuit satisfy

    ryCount + cxCount ≤ ryCount(initial) + cxCount(initial) + n*bound.

This bound counts only Ry and CX. X and Rz are valid, potentially numerous stage gates and contribute zero to both counters. Therefore this theorem is NOT a total primitive gate count, one-qubit gate count, circuit length, depth, connectivity, preprocessing, or finite-bit synthesis theorem without further restrictions. The theorem named assemble_noOracle is definitional: every PrimitiveCircuit.resource has oracleCalls=0, because that gate syntax has no oracle constructor. It does not certify an external query-oracle implementation or the cost of obtaining stage/initial lists and angles.

Resource has natural fields oneQubit,cnot,oracleCalls,pureAncilla,depth. A circuit's resource sets oneQubit to the sum counting X/Ry/Rz, cnot to the CX sum, oracleCalls=0 and pureAncilla=0, with a touched-wire schedule depth. Thus pureAncilla=0 here is a record convention, NOT a theorem that the n initially zero physical inputs were free to supply or that the q bond wires are cleaned. The target neither states a resource tuple theorem nor bounds depth.

All q,m,t,n,extra,bound are arbitrary natural numbers, including zero. There is no hidden positive-width, positive-rank, or nonzero-amplitude guard in the target. P(0) is a singleton, not an empty basis set. Fin 0 has no wire, so a PrimitiveCircuit 0 can only be the empty list. At n=0, assemble is the identity on q wires; withInitial is initial, outputWires q 0 preserves numeric bond positions, and publicCircuit is the corresponding renamed initial circuit. At q=0 the bond basis is a singleton, while each local stage still has one wire; the placement and output formulas remain well typed. At q=n=0 every involved circuit is empty and its unique entry is 1. At bound=0 the h premise prohibits Ry/CX in relevant stages, but still permits X/Rz; for n=0 h is vacuous. All displayed conditionals retain their unequal-basis zero branches, including nonclean input sectors for padding and placement. No classical choice, default fallback, quotient, or representative selection occurs in target definitions.

## 6. Seven quantum-semantic slots

| Slot | Actual reconstructed content and boundary |
| --- | --- |
| Target and normalization | Exact global-circuit columns from arbitrary initial bond basis a and zero physical input, equal to the recursive run over all physical and final-bond labels. No supplied target vector/core family, norm scalar, or standalone state-preparation package. Circuit unitarity is provider context, not a source-target identification. |
| Dimensions, field, order, basis | Complex matrices; q bond wires plus n emitted wires; local last wire is fresh; Stage uses bit×bond; internal history in stage order, public physical block reversed and bond block last. All natural dimensions, including zero. No Fourier transform/sign convention appears. |
| Access, controls, inverses | Inputs are explicit total functions returning gate lists and an explicit initial list. No oracle/coherent parameter-access model, inverse call, controlled-stage operation, or oracle construction bound. Individual CX requires distinct indices. |
| Ancillas, overwrite, garbage | Physical input wires are clean zero in the principal column theorem; history wires are spectators of later local stages. Bond may change at every stage and is retained as arbitrary b. No terminal cleanup, dirty-workspace model, final-bond decoupling, reset, or garbage-sector erasure is proved here. |
| Phase | Exact entry equality over ℂ, including any relative phases generated by valid Rz gates. No equality modulo phase, label-dependent phase quotient, or separate globalPhase wrapper is used. |
| Error, success, probability | No approximation parameter, norm error, confidence, accepted-sector projection, postselection, measurement, or amplification. Clean ZERO is an input condition, not a heralded success condition. No source-specific fidelity follows. |
| Resource tier | Exact-real X/Ry/Rz/CX lists. Padding and relabeling preserve selected syntactic counts. Prefix Ry/CX sums and conditional linear Ry+CX upper bound; oracleCalls=0 by syntax. No total-gate bound from Ry+CX, SWAP/connectivity cost, numerical precision, Clifford+T, classical production/runtime, readout, or asymptotic uniform family construction proof. |

## 7. Unresolved and deliberately unclaimed boundaries

The requested supplement closes the actual Ry-sign and permutation-direction definition gap. No missing project definition remains essential to the target's recursive amplitude/counter interpretation. Import-only API such as StatePreparationTarget, gridSize, BlockEncoding, and other Robin constructions is not needed for this target contract and is not recursively audited or admitted by this packet.

The target's source correspondence, historical authorship, statement/binder source classifications, source proof/construction graph, mathematical novelty, compilation success and axiom/proof-term closure remain UNKNOWN or NOT PERFORMED. The decoder read all target source through line 331 and provider context as recorded, but did not run Lean, native_decide, a compiler, a simulator, network access, Git, or child agents. Seeing `native_decide` inside an unused provider proof is a read event, not execution. No production source was edited.

The declaration inventory preserves exact target code and scope. The dependency map records source-read proof references and definitional support separately from imports; it is not an elaborated proof-term exporter. Only a future distinct source comparison can decide agreement with any withheld natural statement. Seal scope is this independent formal reconstruction and its exact input bindings only.
