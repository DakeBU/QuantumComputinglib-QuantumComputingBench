# Independent formal reconstruction — current nine-module packet

Decoder: `/root/robin_c49_current_formal_decoder`. Direction fingerprint:
`current-nine-formal-register-phase-context`. Historical formalizer: **UNKNOWN**.
This is mathematical interpretation of formal source read through EOF, not a
source-agreement verdict, fresh theorem verification, or publication admission.
No Lean compiler, native tactic, simulator, Git write, network request, or child
worker was run. The supplied production epoch is
`389dd817cad3f9ce69bbccc3d0cfe69c1dbfba9d`; that identifier is a pin, not proof
success. The formal config specifies `leanprover/lean4:v4.33.0`.

## 1. Exact reading scope and signature convention

All nine designated target files were read in full, including private helper,
imports, options, and all declaration bodies. The independent lexical inventory
has respectively 22, 23, 20, 16, 20, 19, 10, 75, and 10 explicit source
declarations, totaling 215. `declaration-inventory-c57.json` is the versioned
source-command-header annex: each whole-target entry retains an exactSourceHeader
extracted from its unchanged full source capture. The old sourceSignature field is
retained verbatim only as an obsolete lexical-prefix aid, not a command/type header.
Twelve where and six equation-clause boundaries were incorrect in that old aid;
the formal-only C57 successor repairs them, preserving entire declaration capture,
namespace, explicit private/noncomputable modifiers, ambient commands, source
positions, and capture hash. It includes the private
`Figure4T3.transportInput_eq_encode` helper. Source names are qualified by the
explicit namespace, not by guessed private compiler-generated names. No target
has a `variable` or `universe` command supplying an unrecorded ambient binder.
Exact source-command headers are not elaborated signatures: instance synthesis, inferred
universes, elaborated proof terms, and generated recursor/constructor names were
not obtained by running Lean.

Thirty-seven supplied provider projections were also read through EOF, with
their own byte pins and inventory. They remain bounded projections, **not
whole-module review**, even where a projection happens to expose much of a
small module. In particular only `bounded-nine/providers/.../RobinMatrix.lean.txt`
was read, never the full production `RobinMatrix.lean`. The filtered
`provider-range-map.json` records only formal file names, declaration kind/name,
and source/projection ranges. It does not import author adequacy judgements.
Import presence is not proof-term dependence of every declaration on that import.

The first raw pin comparison occurred after all nine initial target reads. The
file named `input-pins-pre.json` is the pre-written-reconstruction pin, not a
fictional pre-reading pin. Chronology and subsequent post/final pins preserve
that limitation.

Every raw target snapshot differs from the current production raw bytes. Own
tested in-memory comment redaction, preserving code whitespace and Strings and
separately converting line endings to LF, yields equal normalized hashes for
all nine targets and all three config files. The result is only
`COMMENT_REDACTED_FORMAL_CONTENT_MATCH`. Raw bytes are not equal. This does not
show elaboration/TCB noninterference, compilation, semantic source fidelity, or
full dependency equality. `hash-control.json` retains both raw hashes and both
normalized hashes, tests, counts, and booleans; no production prose was emitted.

## 2. Common algebra, basis, and execution semantics

`Matrix r c α` in the project is `Fin r → Fin c → α`; `_root_.Matrix I J ℂ`
is the indexed Mathlib matrix carrier. All concrete target constructions act on
complex amplitudes; the fixed data tables are integer/rational before casting.
`gridSize q = 2^q`. A physical basis assignment is
`PrimitiveBasis q = Fin q → Fin 2`. Wire zero is the least significant bit in
`primitiveBasisLEEquiv q`; for six wires its integer value is
`b0+2b1+4b2+8b3+16b4+32b5`. The zero-width equivalence has one basis assignment,
mapped to `Fin 1` value zero. `primitiveBits3LE j` extracts bits with `% 2`,
`/ 2`, and `/ 4`, all on `Fin 8`.

An equivalence `e : I ≃ J` reindexes a matrix to entries
`U(e.symm r,e.symm c)`. A permutation matrix has entry one precisely when
`row = permutation column`, and zero otherwise. The execution list is
chronological: `eval(g :: rest) = eval(rest) * eval(g)` and
`eval(left ++ right) = eval(right) * eval(left)`. This is important for every
unprepare/conjugation direction below.

The exact primitive gates are X, Ry, Rz, and CX on bounded physical wires, with
an explicit `control ≠ target` proof for CX. X flips a `Fin 2` value. CX flips
its target iff the control is nonzero (therefore one). Ry is

\[
 R_y(\theta)=\begin{pmatrix}\cos(\theta/2)&-\sin(\theta/2)\\
 \sin(\theta/2)&\cos(\theta/2)\end{pmatrix}.
\]

Rz is diagonal `exp(-i θ/2), exp(+i θ/2)`. A one-wire lift is zero between
basis states whose other-wire contexts differ, otherwise the appropriate
two-by-two matrix entry. Dagger negates Ry/Rz angles and reverses circuit order;
X and CX are self-adjoint. Matrices use exact equality, not equality modulo
phase.

`ExactAngle` is a syntax datatype: rational radians, rational multiples of π,
`2 arccos q` with proof `|q|≤1`, `2 arccos sqrt(q)` with proof `0≤q≤1`, an
arbitrary real, addition, negation, and rational scaling. Evaluating it is
noncomputable real arithmetic. The proof fields constrain the two rational
arccos constructors; they are not runtime numerical checks. In particular
`amplitudeRotation a = R_y(2 arccos a)` is defined for every real `a`, and is
unitary for every real `a`; only its `(0,0)=a` theorem needs `-1≤a≤1`.
For bounded a its lower off-diagonal is nonnegative `sqrt(1-a²)` and upper
off-diagonal is its negative. Negative a remains a signed amplitude, not an
absolute value.

A `PrimitiveProgram q` stores a circuit and `globalPhase : ExactAngle`.
Its matrix is `exp(i * angle.eval) • eval circuit`. Sequential composition
concatenates circuits and adds phase angles; dagger negates that phase. The
phase is not a quotient and cannot be discarded merely as physically global.
Provider H/T/T† macros use corrections π/2, π/8, -π/8, respectively. The H
circuit is Rz(π) then Ry(π/2), corrected to the usual H; T is corrected Rz(π/4)
and T† is corrected Rz(-π/4). CCX is H–a monomial CCZ construction–H. The read
proofs separately identify its permutation and its state-dependent phase,
then produce an exact permutation matrix. Thus the reversible compiler does
not assert a phase-insensitive truth-table substitute.

Uniformly controlled Ry is a total compiler for any `controls : Nat`, any wire
function, proof each control wire differs from target, and any angle function
on all `2^controls` assignments. Distinct control wires from each other are
**not** a premise. Repeated controls simply restrict which formal assignment
is realized. For zero controls it emits one Ry. Recursively it emits the tail
compiler for `(θ0+θ1)/2`, a head CX, the tail compiler for `(θ0-θ1)/2`, and a
second head CX. Its matrix is block diagonal on all non-target contexts, with
the Ry angle selected by the actual control bits. Read theorem counts are
`2^k` Ry and `2(2^k−1)` CX (natural subtraction); zero angles are still counted
as emitted gates. No finite-bit angle approximation is specified.

## 3. Explicit shared target and selection data

Let J be the integer matrix (row first, column second)

\[
\begin{pmatrix}
-30&32&-2&0&0&0&0&0\\
16&-31&16&-1&0&0&0&0\\
-1&16&-30&16&-1&0&0&0\\
0&-1&16&-30&16&-1&0&0\\
0&0&-1&16&-30&16&-1&0\\
0&0&0&-1&16&-30&16&-1\\
0&0&0&0&-1&16&-31&16\\
0&0&0&0&0&-2&32&-30
\end{pmatrix}.
\]

The rational `warmRobinTarget` A is J/12 entrywise, its explicit normalizer α
is `56/3`, and the normalized target is J/224. The supplied provider theorem
states that identity for all `row,column : Fin 8`. This matrix is not symmetric
(for example J01=32 and J10=16); it is centrosymmetric. The formal fixed table
and its α are sufficient to define the target without assuming a PDE or any
external source assertion.

For `s,j : Fin 8`, set
`o(s)=(s xor 3) mod 8`, `d(s,j)=(j+o(s)) mod 8`,
and `w(s,j)=J[d(s,j),j]`. All eight labels are genuine inputs. The seven-active
route uses `p(s)=1/7` for `s<7`, zero for `s=7`; its padded coefficient is
`w(s,j)/32` for `s<7`, but **one** for `s=7`. The zero selector probability,
not an omitted definition, removes that last label from the clean block.
The clean formula is `Σ_s [d(s,j)=i] p(s) a(s,j)=Jij/224`.
For each s, `d(s,·)` is a permutation. These are modular additions using an
xor-transformed **label**; they are not `j xor s`.

The Figure4 coefficient, in contrast, is `w(s,j)/32` on **all eight labels**.
It does not use the padded-one fallback. Its bulk predicate is exactly
`j=3 ∨ j=4`, an explicit decidable Prop. The bulk slot table is
`[0,-1,16,-30,16,-1,0,0]/32`; elsewhere a boundary table evaluates the same
J entry. The branch identity and coefficient bounds in the projections are
finite quantified statements, with native tactic invocations in their source.

## 4. ModularAdder3: full permutation versus clean arithmetic

`primitiveXProgram` is a singleton X with zero phase.
`compileReversibleGate` maps reversible X/CX/CCX to the exact macros, and
`compileReversibleProgram` recursively sequences them, starting from identity.
Their `_eval` theorems assert equality of whole matrices to the corresponding
permutation matrices at arbitrary width, not merely basis measurement equality.

`cleanC3XReversibleProgram` is CCX(c0,c1,w), CCX(w,c2,t), CCX(c0,c1,w).
Its definition requires only `c0≠c1,c0≠w,c1≠w,w≠c2,w≠t,c2≠t`.
`cleanC3XBasisEquiv` and the primitive program are defined under those same
guards. The theorem identifying its action with a triple-controlled X adds
`c0≠t,c1≠t` and `state w=0`. It does **not** add `c0≠c2` or `c1≠c2`.
The clean-action theorem flips t iff all three named control values are one,
otherwise it is identity, and restores w=0. The workspace theorem is a
consequence with exactly those extra guards. Without clean w, the named
three-CCX permutation remains total but this C3X identification is not stated.
The primitive-eval theorem is whole-space equality to that total permutation,
not whole-space equality to ideal C3X.

The concrete 7-wire program has data a on wires 0,1,2 (LE), preserved addend b
on wires 3,4,5 (LE), and workspace wire 6. Chronologically its reversible gates
are CCX(3,0,6), CCX(6,1,2), CCX(3,0,6), CCX(3,0,1), CX(3,0),
CCX(4,1,2), CX(4,1), CX(5,2). For every basis state with wire6=0,
`a_out=(a_in+b_in) mod 8`, all three b bits are preserved, and wire6=0.
No carry bit or overflow information is returned. All 3-bit operand values,
including zero and seven, are quantified. The source proof is
`native_decide +revert`; it was read, **not executed or newly admitted here**.
`modularAdd3Primitive_eval` remains a whole-space exact permutation equality;
the arithmetic and workspace statements are conditional on clean workspace.
The final resource-faithfulness theorem is the definitional equality between
program.resource and circuit.resource, and oracleCalls=0 follows from the
primitive gate vocabulary. Neither is a new optimized gate-count theorem.

## 5. PaperSevenPrepare: complete selector unitary, not just a distribution

On three selector wires, high wire2 receives `2 acos sqrt(4/7)`;
middle wire1 is controlled by wire2, receiving π/2 when that control is zero
and `2 acos sqrt(2/3)` otherwise; low wire0 is controlled in order by wires1,2,
receiving zero only when both controls are one and π/2 otherwise.
`warmRobinUniformSevenPrepareCircuit` compiles those stages in that order.
Program phase is zero. Its defined matrix is L*(M*H), where each controlled
stage is the block-diagonal matrix already specified, and the flat selector
matrix P is its LE reindex to `Fin 8`. Eval and unitarity theorems hold on
the entire three-wire space. Counts are seven Ry and eight CX, and zero
primitive oracle calls.

`warmRobinPaperSevenPaddedSlot : Fin 8 → Option (Fin 7)` is some(s) for s<7,
none otherwise; its theorem says label7 is none. This Option function does not
restrict any physical label domain. The probability theorem states, for every
`slot : Fin 8`, `conj(Pslot,0)*Pslot,0 = if slot<7 then 1/7 else 0`.
It states no sampled confidence bound, no postselection success guarantee for
arbitrary input, and no approximation. The whole matrix definition, including
the minus sign in Ry's upper off-diagonal, fixes relative phases and its other
seven columns. Merely replacing P by a matrix with the same first-column
probabilities is not a permitted semantic replacement. Reading the principal
arccos/positive-sine definitions shows the first column has positive equal
real amplitudes on 0..6 and zero on7; the named probability theorem itself is
only the squared-entry assertion.

## 6. PaperSevenAmplitudePrimitive and PreparePrimitive: 8-wire embeddings

The physical logical-index map is
`bits ↦ (bits6,(selector,(system,bits7)))`, where system is LE bits0..2 and
selector is LE bits3..5. Thus coefficient is wire6 and an additional workspace
bit is wire7. `WarmRobinPaperSevenFullSystem = Fin 8 × Fin 2` includes both
workspace sectors. The bijective index and context-equivalence claims are
finite statements; their native proofs are read-only evidence here.

The amplitude control wires are exactly 0..5, target6. The angle function reads
system from control bits0..2 and selector from bits3..5, and returns
`2 acos(a(s,j))` with the padded a above. Wire7 is preserved and does not
affect the angle. Its block matrix is the reindexed amplitude lift on
`(coefficient, selector, (system,work))`, equal on all 256 basis rows/columns,
not just work=0 or coefficient=0. Both coefficient columns of Ry are covered.
The circuit is the six-control compiler and the program has zero phase;
`AmplitudeProgram_eval` is a whole-space equality, and its oracle statement
is zero by syntax. The uniform compiler implies 64 Ry and126 CX at this stage;
that derived count is not an additional target theorem.

The dependency projection also defines the total full-system permutation
on `(j,w)` explicitly: with bits a of j and b of o(s), form
`w1=w xor(b0 and a0)`, `a2'=a2 xor(w1 and a1)`,
`a1'=a1 xor(b0 and a0)`, `a0f=a0 xor b0`,
`a2''=a2' xor(b1 and a1')`, `a1f=a1' xor b1`, `a2f=a2'' xor b2`;
return `(a0f+2a1f+4a2f,w)`. This total dirty-work extension is not silently
identified with clean modular addition. No whole 8-wire block-encoding root
is claimed by the two target modules under this section.

`PaperSevenPreparePrimitive` defines flat high/middle/low matrices for P and
their stage product equality. It relocates selector stages to target wires5,4,3,
with controls5 then controls4,5, preserving all other wires. Selector decode,
all three context iff lemmas, target-distinctness lemmas, and each stage's
physical `_eval` theorem explicitly account for coefficient6, system0..2, and
workspace7. The context condition is equality on every wire except the stage
target; it is not a clean-workspace assumption. Concatenating yields the
whole-space `Icoefficient ⊗ (P ⊗ IfullSystem)` under the physical equivalence.
The unprepare circuit reverses the list and daggers gates; its matrix is
the exact adjoint selector lift. These two modules provide embedded
amplitude/PREPARE semantics, not a theorem that workspace is clean for an
arbitrary larger caller.

## 7. Figure4PreparePrimitive and Figure4T3: 9-wire exact root

Here physical selector is LE wires0..2, physical system is LE wires3..5,
coefficient is wire6, indicator is wire7, and temporary workspace is wire8.
The full logical system is `Fin 8 × (Fin 2 × Fin 2)` and the logical index is
`(coefficient,(selector,(system,(indicator,work))))`. `EncodeBits` is the
explicit inverse encoding of those five components. `BitsIndex`, its
bijectivity, the equivalence/application/encode lemmas and selector decode
cover **all** basis assignments, not only clean sectors.

The high/middle/low selector controls use physical target wires2,1,0, with
controls2 and controls1,2. Distinctness and context iff statements are the
9-wire counterparts of the preceding section and retain coefficient6 and
the entire `(system,indicator,work)` context. Their three stage matrix
equalities compose into `after_prepare`, equality to the lift of the same P
on the full 512-dimensional space. Unprepare is the program dagger and its
theorem is the adjoint lift, also whole-space exact.

The bounded middle-program dependencies have these explicit meanings:

1. An indicator program toggles wire7 for system columns3 or4 when starting
   from encoded wire7=wire8=0, without altering slot, system, coefficient, or
   clean work. It uses two negated-control patterns and clean C3X machinery.
2. The bulk loader controls wires0,1,2,7, target6, and applies a coefficient
   rotation only if indicator=1. Otherwise it is identity. The boundary
   loader controls wires0..5,7, target6, and is active only when indicator=0
   **and** the decoded system column is not3 or4; otherwise identity. These
   guards define dirty/inconsistent-indicator behavior too, rather than
   assuming a caller cannot present such a state. Both use exact arccos
   angles and their derivative program is bulk then boundary.
3. Postloader order is DT sparse access, indicator-program dagger,
   homogeneous identity, a full three-bit register swap (nine CX), then D
   sparse-access dagger. The DT stage overwrites the selector/address with
   `d(slot,column)` while preserving system and work when work=0. D uses
   `DOffset(slot)=(slot+5) mod8` and performs modular addition to the address.
   Their inverse transport identity is
   `(d(slot,column)+DOffset(slot)) mod8=column`.
4. On transport input `(slot,column,coefficient,indicator(column),work0)`,
   postloader returns `(slot,d(slot,column),coefficient,indicator0,work0)`.
   Its inverse uses `column=(row+8-o(slot)) mod8`. The middle program is
   indicator, derivative loader, postloader, in that chronological order.

These clean statements do not characterize all dirty sectors. On all sectors
the exact gate lists and eval definitions still specify a total unitary.
`warmRobinFigure4LogicalMiddle` is **defined** as the reindex of that complete
physical middle-program matrix. Thus the whole-space primitive root equality
does not independently identify dirty middle behavior with an ideal clean
amplitude/SELECT operation; it identifies the actual matrix in logical
coordinates. The clean-entry theorem supplies the additional mathematical
content:

\[
M_{(c_r,s_r,i,0,0),(c_c,s_c,j,0,0)}=
 [s_r=s_c\land d(s_c,j)=i]\,
 R_y(2\arccos(w(s_c,j)/32))_{c_r,c_c}.
\]

The private transport/encode lemma reconciles physical and logical clean
indices. `warmRobinFigure4AllWorkspaceClean` quantifies every slot and column
in `Fin 8` and every coefficient bit, starting indicator=0 and implicit work=0
via `TransportInput`. After the indicator permutation and postloader
permutation, both outputs7 and8 equal zero. This statement is about those
permutations on basis assignments; it is not stated for arbitrary dirty
input, nor an unconditional claim that the selector/coefficient return zero.
The intervening loader rotates only coefficient6 and keeps the clean-context
sector, permitting the clean-entry composition used by the root proof.

The complete primitive program is PREPARE; middle; PREPARE†. Its whole matrix
is the reindex of `P_lift† * M * P_lift`. Compressing coefficient=0,
selector=0,indicator=0,work=0 on both sides yields

\[
\sum_{s=0}^7 |P_{s0}|^2 [d(s,j)=i]\,w(s,j)/32
=J_{ij}/224=A_{ij}/(56/3).
\]

The s=7 coefficient in this middle rotation is the all-label Figure4
coefficient, not padded one. Its selector weight is zero, so the same clean
formula results. The read root proof explicitly invokes bounds before using
the amplitudeRotation `(0,0)` identity, uses the selector probability theorem,
and splits active `<7` from the padded label.

`PrimitiveFlatUnitary` reindexes the physical matrix by LE9. Its unitarity
comes from primitive program unitarity. `PrimitiveCleanIndex system` is LE9
of `TransportInput 0 system 0 0`, hence its integer value is `8*system`.
The clean-block theorem is entrywise equality at precisely these indices;
this is **not** the leading contiguous 8-by-8 block under the physical LE
ordering. `PrimitiveBlockContainsTarget` expands to the universal entrywise
equality at those clean indices against the explicit query target divided by
its normalizer. It contains no approximation or norm bound.

The presentation maps X→`oneQubit "X"`, Ry/Rz→`rotationY/Z ... "exact-angle"`,
and CX→`cnot`, forgetting the actual angle expression in that presentation.
It maps only the circuit field, so it also does not represent a program's
separate global-phase field. The actual certified matrix is the program eval,
which retains that scalar. Zero phase may not be inferred for Figure4's
assembled program merely because the selector/loader programs have zero phase:
the reversible macros carry phase corrections and the full assembly uses seq
and dagger on those program fields.
`PrimitiveResource` is the exact primitive program's resource, not a
certificate that those presentation Strings reconstruct its matrix.
The candidate fixes systemQubits3, auxiliary6, signal4, pureAncillas2;
`layoutMatches` is `4+2=6`. Its chosen `isUnitary` Prop is membership of the
actual flat matrix in the unitary group and its chosen block Prop is the
universal statement above. The refinement stores the actual program, the
entire reindexed `P†MP` target, and an equality proof. The verified record
supplies proofs of the candidate's two actual Props. No additional free
normalization/PREPARE/SELECT/correctness hypotheses are binders of the final
concrete root: the read proof route uses producers internally.

## 8. SymmetryFourSlotPrimitive: coordinate and cyclic-amplitude interface

The shared symmetry carrier is `(sector : Fin 2, pair : Fin 4)`. Pair-low
embeds pair as 0..3; pair-high is `7-pair`; the pair-system equivalence sends
sector0 to low and sector1 to high. `warmRobinPairBits` places pair bits on
physical0,1, sector on2. The two-CX coordinate circuit is CX(2,1), CX(2,0).
It toggles the two pair bits when sector1. Consequently its 3-bit LE output
is pair for sector0 and `7-pair` for sector1, matching `PairSystemEquiv`.
The image theorem quantifies all eight pair coordinates, and the bijectivity
theorem is that of the defined basis equivalence. Whole-space eval is the
exact permutation matrix; there is no clean-ancilla premise.

Let JLL(p,q)=J[p,q] and JLH(p,q)=J[p,7-q]. The plus and minus blocks are
`JLL+JLH` and `JLL−JLH`, respectively. The **cyclic** four-slot provider
permutation is `(q+s) mod4`, preserving sector, with explicit plus/minus
weight tables divided by56. `warmRobinFourSlotExactAngle s (sector,q)`
constructs `2 acos(weight/56)` with its bound proof. Its eval theorem unfolds
the angle, and `ExactRy_eq_rotation` identifies the full two-by-two Ry with
that cyclic-route amplitude rotation, including signs. This target module
does not construct a full cyclic four-slot primitive block encoding. Its
cyclic rotations are not the XOR-route rotations introduced next.

## 9. SymmetryXorFourSlotPrimitive: full 6-wire realization

Define `q xor s : Fin 4` by natural bitwise xor. The XOR weight is the plus
or minus sector matrix entry `Jsector[q xor s,q]`, divided by56. Selector
slots are all four labels with probability1/4, so their clean weighted sum
is the diagonal-sector matrix
`T((sector,p),(sector',q))=[sector=sector'] Jsector[p,q]/224`.
The XOR coefficient is its real cast; its rotation is `Ry(2 acos(coefficient))`.
No padding, exceptional label, or zero-probability selector is present.

The middle physical index is
`bits ↦ (bits5,(bits3+2bits4,(bits2,bits0+2bits1)))`:
pair wires0,1; sector2; selector3,4; coefficient5. The context equivalence
for target5 is bijective and the middle bit equivalence is obtained by
splitting that target and converting its five-wire context. Context/target
lemmas are identities on all basis assignments, not clean-sector assertions.

SELECT is CX(3,0) then CX(4,1), so it xors selector into pair while preserving
sector2, selector3,4 and coefficient5. The action theorem quantifies every
6-wire basis assignment and gives the integer xor identity plus those four
preservations. Its circuit eval first identifies the full permutation, then
the `_reindexed` theorem identifies the logical controlled-system lift.
The noOracleCalls theorem is syntactic.

Amplitude control wires0..4 target5 select all 32 pair/sector/selector
combinations. Its angle-eval and Ry-rotation theorems give the entire rotation.
The controlled-Ry equality uses equality of all non-target contexts and the
bijective context index, so it holds even coefficient input1. The amplitude
circuit/program evaluations are full-matrix equalities, phase zero, with
32 Ry and62 CX. Program.oracleCalls=0 is separate. The provider normalization
proof and coefficients are internal dependencies, not extra hypotheses.

Selector PREPARE is Ry(π/2) on3 then on4; unprepare reverses/daggers it.
The uniform bit matrix B is `[[c,-c],[c,c]]` with c=√2/2. This is **not**
Hadamard `[[c,c],[c,-c]]`, and its negative entry must be retained. The flat
four-slot bit equivalence packs `(high,low)` as `2*high+low`; the explicit
`symm_pack` theorem returns `(high,low)`, not `(low,high)`. Low/high lifted
matrices act on the corresponding factor and multiply to P4, whose first
column is the constant1/2 and probabilities1/4. Their context iff and stage
eval lemmas account for every non-target wire. The complete middle circuit is
PREPARE; amplitude; SELECT; unprepare, giving
`U_mid=P4_lift† SELECT AMP P4_lift` on the whole 64-dimensional space.

The six-wire pair-coordinate circuit is again CX(2,1),CX(2,0), acts trivially
on wires3..5, and is involutive on the whole space. The symmetry prepare is
Ry(π/2) on2, i.e. `systemLift(B ⊗ I4)` in middle coordinates; its unprepare is
the adjoint, not itself. The primitive pair circuit is chronological
symmetry-unprepare; middle; symmetry-prepare, yielding
`U_pair=B_lift U_mid B_lift†`. The provider identity
`B*(T*B†)=J_pair/224` recovers pair-coordinate normalized J. It is a true
conjugation in this stated direction, including relative sector signs.

Original-bits equivalence first applies the involutive coordinate permutation
then the middle bits equivalence. The final primitive circuit is coordinate;
pair circuit; coordinate. Its whole-space equality is first to the reindexed
pair logical matrix, then to the flat XOR unitary using LE6. The exact index
theorem says `FourSlotIndexEquiv(OriginalBitsEquiv bits)=LE6(bits)`.
`FourSlotIndexEquiv` packs `(coefficient,slot,pair-system)` as
`32*coefficient+8*slot+PairSystemEquiv(pair-system)`.
Therefore `FourSlotCleanIndex system` has flat integer value `system` and the
primitive clean index is ordinary system LE bits on0..2, with selector3,4 and
coefficient5 zero. The clean-block theorem is entrywise J/224 at those basis
indices. Full circuit/program eval equalities cover every dirty signal
sector too; the block extraction is specifically coefficient=selector=0.
Neither the clean-block theorem nor unitary membership asserts deterministic
return of those three signal bits for every system input.

The primitive program uses zero global phase. Matrix unitarity is inherited
from gates, and there are no primitive oracle calls. The same four-case
presentation conversion as Figure4 discards exact angle values in favor of
`"exact-angle"`. The resource object equals the actual primitive circuit's
resource by definition. The candidate is system3, auxiliary3, signal3,
pureAncillas0; `layoutMatches` proves3+0=3. Its arbitrary Prop fields are
instantiated with actual flat-unitary membership and all clean target
entries, and the verified record supplies those two proofs. The primitive
refinement stores the circuit and whole reindexed flat target with exact
equality. The aliases `warmRobinFourSlotT3FlatUnitary` and
`warmRobinFourSlotPrimitiveVerifiedBlockEncoding` are exactly the XOR objects;
their unqualified four-slot name does not identify the earlier cyclic route.
`warmRobinFourSlotPrimitive_eval_eq_flatUnitary` is the same equality under
that definitional alias.

From the literal primitive composition one can count, without optimization,
38 Ry and68 CX for the complete six-wire circuit: amplitude32/62; selector
prepare+unprepare4 Ry; symmetry pair2 Ry; SELECT2 CX; two coordinate circuits
4 CX. This is a derivation from definitions/count theorems read, not a newly
executed count or an optimized synthesis certificate.

## 10. SystemConjugation: generic exact identities and all binders

The carrier is `LCUIndex C S H = C × (S × H)`. On every occurrence of matrix
multiplication or the relevant lifts, the source includes finite-type and
decidable-equality instances for C,S,H. `cleanSystemBlock` itself requires
none: it simply selects `(c0,(s0,i))` and `(c0,(s0,j))` entries. C and S need
not be qubits; c0,s0 need not be zero. Empty finite types are allowed where no
element binder is required; an explicit clean element binder cannot be
instantiated in an empty carrier. No dimension positivity premise is hidden.

`systemLift V = I_C ⊗ (I_S ⊗ V)`. Its entry is V on the H coordinates if
both C and S coordinates agree, zero otherwise. The adjoint-entry theorem
uses `conj(V[column.H,row.H])` with the same equality guards. Unitarity of
the lift requires an explicit unitary-membership premise for V.

The clean-row multiplication theorem additionally has `columnType : Type*`
with `Fintype columnType`, an arbitrary rectangular operator
`Matrix (LCUIndex C S H) columnType ℂ`, clean elements c0,s0, systemRow i,
and arbitrary column k. It expands `(systemLift V * O)((c0,s0,i),k)` to
`Σ_h V[i,h] O[(c0,s0,h),k]`. The dual clean-column theorem has an arbitrary
finite rowType, operator `Matrix rowType (LCUIndex C S H) ℂ`, row k,
systemColumn j, and expands multiplication by `star(systemLift V)` to
`Σ_h O[k,(c0,s0,h)] conj(V[j,h])`. No unitary hypothesis is needed for either
algebraic identity, despite the physical vocabulary.

`conjugateSystem V O = systemLift V * (O * star(systemLift V))`.
Its unitarity theorem requires **both** explicit unitary premises, one for V,
one for O, besides the finite/decidable instance binders. For arbitrary V,O
without unitary assumptions, the final theorem still states

\[
\operatorname{clean}(\operatorname{conjugateSystem}(V,O);c_0,s_0)
=V\,\operatorname{clean}(O;c_0,s_0)\,V^\dagger.
\]

It is proved by the two finite summation identities, with no success
probability, normalization, approximation, or physical gate realization
premise. The target's exactSourceHeader entries in the C57 annex preserve all
implicit types, typeclass binders, rectangular carrier parameters, and named
matrix/clean-index arguments.

## 11. Recursive record/Prop expansion and metadata boundaries

`RegisterLayout` has natural fields systemQubits, signalQubits, pureAncillas;
its auxiliary count is signal+pure. `QueryOperatorTarget α r c` has operator,
normalizer, `source : String`, `semanticContract : String`, and
`freeParameters : List String := []`. No positivity, normalization validity,
source truth, or free-parameter completeness proof is attached to those data
fields. Here the concrete source String is
`"Guseynov-Huang-Liu 2025, fixed N=8 homogeneous Robin instance"`; the contract
String is `"the coefficient=0 and selector=0 clean block equals A/(56/3) exactly"`.
They are retained verbatim formal Strings, not independently read natural
source or evidence that any source agrees. Concrete `freeParameters` is [].

`OperatorBlockEncodingCandidate α n` stores auxiliaryQubits, a target on
`2^n × 2^n`, a full matrix on `2^(n+aux)`, layout, a descriptive Circuit,
`schedule : LayeredCircuit := []`, Resource, the proof
`layout.signalQubits+layout.pureAncillas=auxiliaryQubits`, and two fields of
type **Prop**, `isUnitary` and `blockContainsTarget`. Generic candidates can
choose any propositions; the generic record type itself does not equate
these to the matrix semantics or prove them. The two target constructors
above explicitly choose the mathematical Props described in sections7 and9.
Their schedules are the default empty list, not an obtained depth-optimal
gate layering. `VerifiedOperatorBlockEncoding` stores the candidate and
inhabitants of exactly those two candidate Props. It does not add an
interpreter correctness field for the descriptive Circuit, a circuit cost
proof, a resource asymptotic theorem, or a canonical leading-block layout.

`PrimitiveRefinement q` stores circuit,target, proof `eval circuit=target`;
`PrimitiveProgramRefinement q` instead stores program,target, proof
`eval program=target`. Neither is an approximation record. Their resource
accessors return the underlying circuit/program resource. The equality
proofs in the concrete constructors close these refinements without extra
public convenience assumptions.

Provider-only records also do not silently certify stronger interfaces:
`Resource` is a tuple of naturals, each default0;
`StatePreparationTarget.normalization : Prop` and candidate.isUnitary are
supplied Props, with source default `""`; the concrete state certificate
requires the chosen normalization proof and an actual matrix-vector
preparation equality. `VerifiedBlockEncoding` similarly contains three
supplied Props and their proofs, not a fixed semantic schema.
`GHL2025.ObligationRecord` is description String, source String, and
`proved : Bool := false`, not a Lean proof. Its `DerivativeOracleContract`
has stencil, bandwidth, coefficient matrix, an ObligationRecord and the
equation bandwidth=stencil.width; `FunctionOracleContract` has functionPieces,
a coefficient-expression bound, and an ObligationRecord. The supplied Robin
composition uses `proved=false` records and only an actual matrix-coherence
equality. Those provider-only records are not prerequisites secretly proving
the concrete target root or general scientific algorithm closure. Empty
`List String` declarations with names containing OpenContracts are just
empty lists, and their `= []` theorems are reflexivity, not exhaustive
mathematical closure audits.

## 12. Seven semantic slots and explicit remaining frontier

| Slot | Reconstructed formal meaning and boundary |
| --- | --- |
| Target/normalization | Fixed A=J/12, α=56/3, exact clean entries J/224. Selector distributions1/7 and1/4. No arbitrary-size target family or normalized output-state root here. |
| Dimensions/scalars/order | Complex matrices over fixed finite carriers; LE physical indexing. Figure4 9 wires (512); PaperSeven embeddings8 (256); XOR6 (64). Conversions are explicit reindexings, not silent tensor swaps. |
| Oracle/access | No oracle primitive in the exact primitive language; compile-time exact coefficient tables/angle functions supply rotations. This does not prove efficient coherent access to externally supplied data. No arbitrary external oracle or parameter-label assumption in concrete roots. |
| Ancillas/workspace | Figure4 clean extraction fixes indicator7 and work8 as well as coefficient6/selector0..2; its index set is strided. Modular arithmetic needs work0. PaperSeven embeddings include both work7 sectors. XOR has three signal bits and no separate pure ancillas, with clean extraction only. |
| Phase | Exact Ry/Rz and exact program phase, not projective equality. Macros correct H/T phases. B=Ry(π/2), not H. Full conjugation directions and both coefficient columns preserved. Probability statements alone do not characterize complete unitaries. |
| Error/success | All stated equalities exact; no norm tolerance or sampled confidence. Clean-block correctness is not success probability1 or automatic signal cleanup. For an arbitrary normalized system vector ψ, the extracted unnormalized branch is Aψ/α; its squared norm would be branch probability under standard measurement semantics, but no new measurement/amplification theorem was executed or added here. |
| Resources | Exact-real logical X/Ry/Rz/CX counts and a touched-wire depth convention. Primitive `Resource` sets oracleCalls=0 and pureAncilla=0 by definition, even when the separate candidate layout lists clean work bits. No finite-bit/Clifford+T synthesis, preprocessing time/storage bound, connectivity/routing model, error accumulation, readout, postselection/amplification cost, or scientific-algorithm success theorem is supplied by these nine modules. |

Depth is computed by folding a map from each wire to its last layer: a gate
gets one plus the maximum depth over its touched wires, updating those wires;
the circuit depth is maximum final wire depth. Independent disjoint gates can
share a depth in this convention, but there is no connectivity graph. Resource
`oneQubit` counts X,Ry,Rz equally and `cnot` counts CX. Program global phase has
no resource charge. The separate generic presentation Circuit uses String
labels and its resource convention need not equal this primitive depth;
neither candidate asserts such an equality. Logical count equalities therefore
must not be advertised as synthesis or implementation-time bounds.

All definitions needed for the mathematical statements of the nine targets
have explicit meanings within the read targets and bounded projections. No
additional **essential target semantic definition** is presently unresolved.
However this is not a claim of complete imported implementation review:
Mathlib/Lean trust, omitted provider declarations and proofs, actual compiler
acceptance including native tactic TCB, whole dependent-module audits, natural
source fidelity, finite-bit synthesis and scientific-root success remain
outside this packet. None is filled by a desired theorem name or a prior
verdict. Source/comparison release has not occurred. An opaque current
publication digest has not been supplied, so no final publication binding
wrapper is fabricated.

The decoder has not classified formal binders as SOURCE/STANDING/RULED or
EXCESS: those categories require the withheld natural source and human ruling.
It records the actual formal typing instances, equality/boundedness/clean-work
premises, and universal domains instead. There is no source-necessity verdict.

## 13. Source-read proof-route dependency map

These are hand-traced uses in source bodies, not elaborated proof-term edges:

* Reversible root: exact H/T/T† phase/monomial identities → exact CCX macro;
  primitive X/CX/CCX eval → gate compiler → program compiler → modular
  whole permutation. The separately read native clean-action theorem gives
  modular addition and workspace; resource claims follow definitions.
* Selector root: exact-angle eval + controlled-Ry compiler semantics → three
  stages → complete selector unitary; trig squares and finite label cases →
  selector probabilities. Physical decode/context bijections → embedded
  stage identities → PREPARE and adjoint identities at8/9 wires.
* PaperSeven amplitude root: all-label coefficient bound → arccos/Ry identity;
  full context bijection + controlled-Ry block theorem → full amplitude lift.
* Figure4 root: compiled reversible indicator/DT/D/swap semantics + guarded
  loaders + clean transport/inverse identities → clean middle entry;
  selector probability + coefficient bound → weighted clean formula;
  fixed rational table theorem → J/224=A/α. Whole eval equality and generic
  primitive unitarity → refinement and verified candidate. The whole middle
  target is the actual middle reindex, not an independently assumed ideal.
* Four-slot coordinate root: literal two-CX basis action → pair-coordinate
  image/permutation; cyclic weight bounds → exact cyclic Ry interface only.
* XOR root: coefficient bound/context bijection + controlled Ry → amplitude
  lift; two CX → XOR SELECT; two uniform Ry → selector lift;
  these compose to `P† SELECT AMP P`. System conjugation algebra + exact B
  stage → pair matrix; involutive coordinate conjugation + LE index identity
  → full flat unitary. Provider weighted formula and centrosymmetric J
  identities give the clean J/224 block; concrete Prop choices and proofs
  populate verification/refinement records.
* Generic system conjugation root: Kronecker entries + finite sums → clean-row
  and clean-column identities → exact compressed conjugation. Generic unitary
  membership closure separately requires its two explicit premises.

The proof source contains `native_decide`/`native_decide +revert` in finite
bijections, basis actions, context iff checks and data identities. The inventory
retains each occurrence in the whole captured declaration. Reading their
syntax is not executing those tactics, checking their result, or certifying
compiler-admitted theorem closure. The protocol build gate was not performed
in this decoder role and no gate-success statement is made.


## C57 annex-only successor lineage

The original mathematical reconstruction is retained verbatim apart from the
three explicit annex-description replacements recorded in annex-delta-c57.json.
The original reading was source-blind. This later repair consumed only the two
pinned formal-header feedback objects, not any natural source, comparison
sections or verdict. All original seals and the actual privacy and18-header
artifact failures remain immutable negative findings. Historical statements in
the reconstruction about unavailable binding digests describe the original run;
the separately versioned C54 and C57 wrappers associate the reconstruction with
the same parent-provided opaque nine-module bindings without reading their
natural-source rows or eleven field contents. This is not a new full
mathematical review or source agreement. Independent targeted C47 re-review
remains required.
