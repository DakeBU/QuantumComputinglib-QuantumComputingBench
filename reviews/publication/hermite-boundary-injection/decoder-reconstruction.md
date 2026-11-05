# Whole-module formal reconstruction

State: FROZEN_BEFORE_SOURCE_RELEASE. This is a reconstruction of the bound formal text, not a comparison with any natural source. Declaration numbers below are the independent ordered inventory in OUTPUT/declarations.json. Exact Lean headers, bodies, leading binder groups and byte/line boundaries are there; this document explains their mathematics and construction.

## Setting and target function

All coefficients and matrix entries in this module are real. Natural-number subtraction and division are truncated natural operations where their operands have type ℕ; expressions coerced to ℝ use real arithmetic. The matrices here are Mathlib's `_root_.Matrix`, namely indexed functions, not the project's separate dimension-indexed matrix abbreviation. No orthogonality, stochasticity or unitarity is part of the kernel definition.

Put d = 2k+1. To make the polynomial completely explicit, define

\[
a_r=\sum_{m=0}^{r}\binom{k+r-m}{k}/m!,\qquad
Q_k(t)=\sum_{r=0}^{k}a_rt^r,\qquad
E_k(t)=(1-t)^{k+1}Q_k(t).
\]

The imported literal definition `sourceInterpolant k` is the Taylor shift by 1 of the polynomial exp(-1) E_k(X) + E_k(1-X). Thus its evaluation is

\[
P_k(p)=e^{-1}E_k(p+1)+E_k(-p).
\]

These are explicit power-series truncation and polynomial operations, not classical choice of an unspecified interpolant. In particular, `sourceInterpolant` is a formal identifier and is not evidence about a withheld natural source. The imported sampled amplitude evaluates

\[
f_k(p)=\begin{cases}
e^p,&p<-1,\\
P_k(p),&-1\le p\le 0,\\
e^{-p},&0<p.
\end{cases}
\]

For the module's three-branch partition, the imported `smoothInitial_strict` moves p=0 to the third branch. This is valid because the imported endpoint-jet result gives P_k(0)=1. It does not move p=-1 out of the polynomial branch.

For n∈ℕ and L∈ℝ let N=2^(n+1), m=2^n, h=2πL/N and x_j=-πL+h j. The principal kernel equality (#118) assumes L>0 and a Boolean list of length n+1; it identifies a finite matrix contraction with f_k(x_j) at the integer j represented by that list. There is no normalization, state-preparation circuit, gate-count or numerical approximation assertion in that equality.

## Binary coordinates and dyadic blocks (#1–17)

`wordValue` (#1) reads its list most-significant bit first: the head contributes either 0 or 2^(tail length), then adds the tail value. The empty word has value 0. Induction proves the strict bound j<2^(word length) (#2). The imported coordinate recursion maps false to t/2 and true to (1+t)/2. Induction on the word shows that at t=0 its value is j/2^(word length) (#3); the head is consequently the most significant bit even though kernels use a remaining-width index.

For integer bounds ℓ,u and a block [a,a+s), `Full` (#4) means ℓ≤a and a+s≤u. `Outside` (#5) means a+s≤ℓ or u≤a. The anonymous instances (#6,#7) supply decidability of these arithmetic predicates. `Partial` (#8) means neither Full nor Outside, with a third decidability instance (#9). These are definitions over all natural bounds, including empty/reversed intervals, not an assumed well-ordered interval bundle.

If M>0 and [Mx,Mx+M) is Partial for [ℓ,MB), then x=ℓ/M (#10). The proof first obtains x<B and hence Mx+M≤MB, so failure of Full forces Mx<ℓ; failure of Outside gives ℓ<Mx+M. Euclidean division pins the unique quotient. Consequently two such partial prefixes are equal (#11). A unit block can never be Partial (#12), and specializing M=2^sWidth proves uniqueness for the middle-prefix power-of-two layout (#13). A root of size 2^(n+1) cannot be Full in an interval ending at 2^n (#14).

`affinePoint` (#15) is a+hj, with arbitrary real a,h. `injectedReadout` (#16) restricts the degree-d Bernstein coefficient vector for P_k to the shifted endpoints 1+x_first and 1+x_(first+2^q), subdivides along a q-bit word, and reads coefficient 0. Here q is the word length. Under x_first≠0 the result is exactly P_k(x_(first+j)) (#17). The nonzero hypothesis is not a positivity condition: the imported restriction formula divides by 1-u with u=1+x_first. The proof substitutes the imported subdivision formula and #3 and simplifies the affine arithmetic. Definitions remain total at x_first=0, but #17 does not assert the desired evaluation there.

## Finite polynomial transport (#18–29)

`unitCoefficient` (#18) is the Kronecker coefficient sequence for a finite index i≤d, extended to every natural index. `sharedCore` (#19) applies one half-subdivision to that sequence and takes its jth coefficient. With rows i and columns j, its entries are

\[
A_0(i,j)=\begin{cases}\binom ji/2^j&i\le j,\\0&i>j,\end{cases}\quad
A_1(i,j)=\begin{cases}\binom{d-j}{i-j}/2^{d-j}&j\le i,\\0&j>i.\end{cases}
\]

These are #20 and #21; the proofs use the half-restriction sum formulas and collapse the Kronecker sums. For the Bernstein basis B_(d,i)(t)=binomial(d,i)t^i(1-t)^(d-i), the row identity is Σ_j A_bit(i,j) B_(d,j)(t)=B_(d,i)(childCoordinate(bit,t)) (#22). This is derived from the imported half-subdivision evaluation on a unit coefficient sequence, not postulated as a property of an arbitrary core.

`sharedContract` (#23) has terminal vector δ_(i,0) and recursion C_(bit::tail)(i)=Σ_j A_bit(i,j) C_tail(j). It equals B_(d,i)(pathCoordinate(word,0)) (#24), by induction using #22 and the endpoint basis value. `injectedFiniteReadout` (#25) pairs the restricted coefficient row with this finite contraction. It agrees with the original coefficient-subdivision readout with no extra hypothesis (#26), and therefore has the polynomial evaluation formula when x_first≠0 (#27).

`boundaryReadout` (#28) routes a dyadic block recursively. A Full block uses `injectedReadout`; an Outside block returns zero; a Partial block descends into the child selected by the next most-significant bit. The child starts at first for false and first+2^(tail length) for true. At the empty word the remaining fallback is zero. The recursion decreases the list length.

If every sample point in [ℓ,u) has nonzero affine coordinate, then the output is P_k(x_(first+j)) on ℓ≤first+j<u and zero otherwise (#29). The proof uses #17 on Full blocks, #2 to justify membership/nonmembership, and the recursively updated start in the Partial case. The universal assumption `hvalid` is a genuine leading logical input; its internal ∀j and implications remain inside that single binder's type.

## One live boundary and polynomial injection (#30–44)

`InjectionBond k` (#30) is Option(Fin(d+1)): `none` denotes a boundary not yet resolved and `some i` denotes an active polynomial coefficient channel. Its cardinality is d+2=2k+3. No quantum register implementation is encoded by this type.

For a schedule s:ℕ→ℕ, `selectedChild` (#31) is s(r+1)+bit·2^r. `blockInjectionRow` (#32) is the Bernstein restriction row for [first,first+2^r). `injectionCore` (#33) has four blocks: none→none is the indicator that the selected child is Partial; none→some is the restriction row if the selected child is Full, else zero; some→none is zero; some→some is `sharedCore d bit`. Thus leaving the unresolved boundary channel activates the polynomial channel once, after which only shared subdivision remains.

`injectionContract` (#34) contracts these cores, indexed at each step by tail length. Its terminal value is zero on none and δ_(i,0) on some i. The some-channel contraction is exactly `sharedContract` regardless of origin, step, interval or schedule (#35).

`ScheduleValid` (#36) expands to: for every r<width and bit, if the selected child is Partial then s(r) equals its start. It is not an existence assertion or an assumption that every selected child is Partial. If this schedule property holds through the word length and the scheduled root block is Partial, the none-channel contraction equals `boundaryReadout` at that scheduled root (#37). The induction separates the next child into Full, Outside and Partial. Full uses #26, Outside vanishes, and Partial uses the schedule equality before invoking the induction hypothesis. The length-zero case contradicts #12.

The actual `boundarySchedule b r` (#38) is 2^r floor(b/2^r), the aligned dyadic block start containing the boundary b. Its child formula (#39) exposes the quotient at the next scale. For interval [ℓ,2^n), #10 proves ScheduleValid through width n+1 (#40). If ℓ≤2^n, its n+1 root start is zero (#41). When ℓ<2^n that oversized root is Partial (#42), combining #14 with failure of Outside.

For the opposite interval [0,u), a Partial block [Mx,Mx+M) with M>0 satisfies x=floor(u/M) (#43); failure of Full now forces u<Mx+M while failure of Outside gives Mx<u. Consequently `boundarySchedule u` is valid for that interval at every requested width (#44). The strict inequalities mean that an exactly aligned endpoint has no unresolved partial block; validity is then vacuous at that position.

## Generic scalar routing (#45–58)

`ScalarBond` (#45) is Option Unit, retaining a boundary channel and a single free scalar channel. `scalarFreeContract` (#46) is the product of free(r,bit) along the word, using r=tail length; the empty product is 1.

`scalarCore` (#47) copies the same Full/Partial branching as the polynomial core but injects the scalar inject(first,r), and uses free(r,bit) on the active channel. `scalarContract` (#48) has terminal zero on none and 1 on some unit; its active-channel value is the free product (#49). `scalarBoundaryReadout` (#50) returns inject(first,q) times the free product on a Full block, zero Outside, and otherwise descends.

For an arbitrary target T:ℕ→ℝ, the hypothesis in #51 is the exact compatibility equation

\[
\forall a,w,\quad \operatorname{inject}(a,|w|)\,F(w)=T(a+\operatorname{wordValue}(w)).
\]

Under this genuine leading logical input, scalarBoundaryReadout is the interval-masked target. This is a conditional generic supplier, not an unconditional theorem about arbitrary inject/free data. #52 independently proves that a valid schedule and a Partial root make scalarContract's none channel equal scalarBoundaryReadout. Its proof has the same three child cases as #37.

`leftFree` (#53) is 1 for true and exp(-h·2^r) for false. `leftInject` (#54) is exp(x_first+h(2^r-1)), where the subtraction inside this real exponential is real. Induction and exp(a+b)=exp(a)exp(b) show that the free product is exp(-h(2^q-1-j)) (#55). Hence the injected product is exp(x_(first+j)) (#56), supplying the compatibility input required by #51. #57 rewrites the injected scalar as exp(x_(first+2^r-1)); that index uses natural subtraction, justified by 2^r>0. For h≥0, the free factors lie in [0,1] (#58).

## Grid and threshold geometry (#59–71)

`gridStep` (#59) and `gridPointNat` (#60) are h and x_j defined above, extended to all natural j. For L>0 the step is positive (#61). On a finite grid index the extended coordinate equals the imported gridPoint (#62), while x_m=0 for every real L, including zero and negative L (#63). Positivity of L is needed for strict monotonicity (#64) and for x_j<0 iff j<m (#65).

`cutIndex` (#66) is c=Nat.ceil((-1+πL)/h). Natural ceiling takes values in ℕ, so a negative real threshold is truncated to 0. The imported positive-step affine-ceiling lemma proves x_j<-1 iff j<c (#67). Since x_m=0, this implies c≤m (#68). Algebra rewrites c as min(Nat.ceil(m-N/(2πL)),m) (#69); the minimum is redundant under L>0 but is literally part of that result.

The middle index interval c≤j<m is equivalent to -1≤x_j<0 (#70). For a Full positive-size middle block, its shifted restriction endpoints satisfy 0≤1+x_first<1+x_(first+size)≤1 (#71). This is a supplied geometric conclusion. It is not a new hypothesis of the final kernel identity, and it does not itself claim any matrix norm or unitary property.

## Exact three-branch readouts (#72–93)

`middleReadout` (#72) specializes boundaryReadout to origin -πL, step h, interval [c,m), and root start zero. Every coordinate in this interval is negative and therefore nonzero; #29 then yields the polynomial on -1≤x_j<0 and zero elsewhere (#73). If c=m the readout vanishes (#74).

`wordSampleIndex` (#75) packages the binary integer into Fin(N) using the genuine leading proof hbits:|word|=n+1. Its value is j; the proof field supplies only the bound. The private theorem `sampledAmplitude_word` (#76) unfolds the imported sample and #62 to identify it with f_k(x_j). It is included in this inventory despite being private.

For words of length n+1 and L>0, the middle readout is the imported sampled amplitude masked by c≤j<m (#77). Here the strict piecewise adapter uses P_k at the left endpoint -1 and excludes zero.

`middleFiniteReadout` (#78) is zero if c=m; otherwise it is the polynomial injectionContract with boundarySchedule(c), started at none. The proved schedule, zero root start and Partial root make it equal middleReadout (#79), and therefore the masked sampled amplitude (#80). The schedule validity is supplied internally, not retained as a premise of #79 or #80.

`leftFiniteReadout` (#81) is zero if c=0; otherwise it is the scalarContract for [0,c), with leftInject and leftFree. Under the same width and positivity conditions, #44, #41, #52, #51 and #56 give exp(x_j) for j<c and zero otherwise (#82). On a Full left block, the last included point has coordinate <-1, so leftInject is positive and at most 1 (#83). The stronger strict upper inequality is not claimed there. The left readout equals the sampled amplitude masked by j<c (#84).

`rightFree` (#85) is exp(-h2^r) for true and 1 for false, with factors in [0,1] when h≥0 (#86). Its product equals exp(-hj) (#87). `rightCore` (#88) replaces the factor at r=n with the indicator of a true bit and uses rightFree elsewhere. Words of length at most n never encounter this special site, so their products agree with rightFree (#89). `rightFiniteReadout` (#90) is the full free contraction of rightCore. For exactly n+1 bits, it is zero on j<m and exp(-x_j) on j≥m (#91). The first bit enforces the half-grid selection, while x_m=0 removes the origin offset. This identity does not require L>0. Its identification with the sampled amplitude mask does require L>0 (#92), to locate the physical coordinate branch.

The disjoint index intervals j<c, c≤j<m and j≥m exhaust all words since c≤m. Summing #84, #80 and #92 therefore gives the unmasked sampled amplitude (#93). This is an exact scalar identity, not a statement of three measurement outcomes or branch probabilities.

## Generic kernels and direct sum (#94–117)

`Kernel B` (#94) is a map (r,bit)↦a real B-by-B matrix. It does not carry a class law or a proof field. `kernelContract` (#95), for finite B, terminates at an arbitrary supplied right vector and recursively multiplies by K_(tail length,head). `kernelAmplitude` (#96) pairs that contraction with an arbitrary supplied left vector. For a word b_(q-1)...b_0 its order is left·K_(q-1,b_(q-1))...K_(0,b_0)·right; each intermediate bond is summed.

`sumKernel` (#97) makes the block-diagonal kernel on Sum B C, with zero cross-block entries. #98 and #99 prove by induction that the contraction restricted to either summand equals that summand's contraction. Finite sums over the disjoint sum then prove amplitude additivity (#100). The finite carrier instances in these declarations supply enumeration, not a logical assumption that an arbitrary construction is correct.

`injectionTerminal` (#101) is zero on none and δ_(i,0) on some i. `scalarTerminal` (#102) is zero on none and 1 on the active unit channel. The generic kernel contraction with the injection core and injection terminal equals injectionContract (#103); likewise for the scalar core (#104). A one-dimensional kernel carrying free(r,bit), with terminal 1, contracts to scalarFreeContract (#105). These identities follow directly by induction; no normalization or nonzero vector premise is used.

`leftKernel`, `middleKernel` and `rightKernel` (#106–108) package the three specialized cores. `leftInitial` (#109) puts weight 1 on none unless c=0, in which case it is zero, and zero on the active scalar channel. `middleInitial` (#110) similarly disables the none channel when c=m and is zero on every some i. These guards handle genuinely empty intervals without asserting that their root is Partial.

Their generic amplitudes equal leftFiniteReadout (#111), middleFiniteReadout (#112), and rightFiniteReadout (#113); the right kernel uses constant-one left/right vectors on Unit. The proofs unfold the initial vectors, split the optional/unique finite sums, and apply #103–105.

`HermiteFiniteBond` (#114) is the tagged sum ScalarBond ⊕ (InjectionBond k ⊕ Unit). The tags keep branch channels distinct. `hermiteKernel` (#115) takes the corresponding two nested direct sums. `hermiteInitial` (#116) combines leftInitial, middleInitial and the constant-one right initial vector; `hermiteTerminal` (#117) combines their terminal vectors. All these definitions are literal formulas on their full carriers.

## Final equalities and address data (#118–125)

Under k,n∈ℕ, L∈ℝ, L>0, bits:List Bool and |bits|=n+1, #118 states that the amplitude of this explicit finite kernel with its explicit boundary vectors equals sampledAmplitude k (n+1) L at wordSampleIndex. It unfolds the direct sum, applies #100 twice, rewrites the three component amplitudes by #111–113, and applies #93. All schedule, injection-compatibility and coordinate-nonzero conditions needed by the internal generic lemmas have been supplied in those preceding proofs. They are not additional leading binders of #118.

The bond has exactly 2k+6 elements (#119): two scalar routing elements, 2k+3 polynomial routing elements, and one right-tail element. `HermiteCoreAddress` (#120) is Fin(n+1)×Bool×Bond×Bond, with the product association literally recorded in the source. `hermiteCoreEntry` (#121) interprets the site address a.1 at remaining width n-a.1.val and reads the specified bit/row/column entry. Thus site zero corresponds to r=n and site n to r=0. The address carrier has 2(n+1)(2k+6)^2 elements (#122). This is the number of dense labelled entry addresses, including entries that happen to be zero, not an algorithmic runtime or a gate-count bound.

The file then separately proves InjectionBond's cardinality 2k+3 (#123), introduces `MiddleBond` as Option(Fin(2k+2)) (#124), and proves its cardinality 2k+3 (#125). MiddleBond is definitionally the same size presentation as InjectionBond but is not used to build the earlier hermiteKernel. The final namespace closes at line 1180. No additional theorem, instance or hidden section hypothesis occurs after #125 in this formal snapshot.

## Formal boundary retained

This reading establishes what the text defines and asserts, with a literal recomposition inventory. It does not establish that Lean accepts the code, that imported proof terms are axiom-clean, that a finite kernel can be converted to a quantum circuit at the stated address size, or that any natural-source statement matches it. No compiler, simulation, original repository mathematics, natural-source exposition, earlier decoder or reviewer result was consulted. Mathlib/Lean definitions remain imported library boundaries, not independently audited here. No omitted project-owned definition is required to state the reconstructed kernel meaning; no formal-definition supplement is requested.
