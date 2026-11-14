# Textbook checkpoint: representation hypotheses and phase-aware domains

Five existing targets receive additive, separately reviewed corrections. This
is a mathematical reader checkpoint, not a stable-data release or new Lean
formalization. Historical records, frozen preview data, source/graph identities,
families, splits and ordered step-node lists remain unchanged.

| Core | Current correction | Contract effect |
| --- | --- | --- |
| plan117 | Haar averaging, continuity and a shear discriminator | Answer only |
| plan118 | Algebraic Schur and the actual division-ring conclusion | Answer only |
| plan119 | Continuous Peter-Weyl regimes and coefficient normalization | Answer only |
| plan120 | General duality, basis dependence and character scope | First question version 2 |
| plan208 | Signed/complex amplitude domain and explicit phase correction | First question version 2; first premise replaced, precision premise retained |

## Recover the mathematical hypotheses, not merely the theorem name

**plan117:** averaging over a compact group needs an appropriate continuous
action and a finite-dimensional or suitable analytic setting. Compactness of
the abstract group is not a substitute for continuity of its representation.
The answer derives the positive Haar-averaging result, supplies a continuous
real shear witness for the noncompact obstruction, and constructs an abstract
discontinuous circle-group action using a Hamel-basis additive map. The latter
cannot be averaged as if it were a continuous finite-dimensional action. These
examples diagnose the original student argument rather than silently adding a
new premise. Complete reducibility is not itself the assertion that the given
inner product already makes the representation unitary.

**plan118:** for an irreducible algebraic representation over a general field,
the commutant is a division ring: kernels and images of nonzero intertwining
endomorphisms prove this directly. A scalar conclusion additionally requires
the relevant eigenvalue argument; finite dimension over an algebraically closed
field is a sufficient setting. The answer computes the real quarter-turn
commutant and the infinite-dimensional complex multiplication example
`End_G(C(t)) = C(t)`. It does not incorrectly classify every division ring as
`R`, `C` or `H`, nor treat algebraic closure alone as an infinite-dimensional
scalar-Schur theorem. Hilbert-space bounded operators and algebraic endomorphisms
are distinct interfaces.

**plan119:** finite averaging, continuous compact-group representation theory
and arbitrary abstract actions are different regimes. The answer retains the
original diagnostic question and reconstructs the valid compact-unitary
statement with normalized Haar measure. Raw matrix coefficients of a
`d`-dimensional irreducible representation have squared norm `1/d`; their
orthonormal versions require the factor `sqrt(d)`. The source's printed
orthonormality assertion is not accepted without this correction. The answer
derives the translation/conjugation orientation and separates finite integer
dimension counts from infinite cardinal or analytic completeness assertions.
External Haar/Peter-Weyl inputs are named, not represented as newly proved
library nodes.

**plan120:** the new question makes the old formula's ambiguous basis reading
explicit. In an arbitrary basis a unitary representation relative to its
underlying inner product need not have matrices unitary relative to the
coordinate standard metric. An orthonormal-basis reading can rescue the old
formula; the correction does not claim every reading was false. General duality
is characterized by an invariant nondegenerate bilinear pairing. Real-valued
characters imply self-duality in the stated finite-dimensional unitary setting,
using the compact closure of the image and finite-dimensional character theory,
not a general theorem for all algebraic representations. Counterexamples and
both directions of the annihilator correspondence remain part of the request.

## Replace an invalid premise visibly

**plan208:** a real `Ry(2 arccos |z|)` prepares magnitudes, not the full signed or
complex amplitude `z`. The current first premise therefore calls it a proposed
magnitude stage to assess; it no longer assumes its correctness. The second
finite-precision premise is retained literally. This is the narrow V3
question-and-assumptions migration, with a literal indexed edit map, six
semantic assessments and an exact-content distinct review. It does not permit
simultaneous convention/source/graph/split changes or arbitrary assumption
overrides.

For each existing entry, the normalized-state domain is the closed unit disk.
The answer constructs an explicit unitary completion and a phase-aware
correction, treats zero and boundary entries, and distinguishes a correct first
column from equality of complete unitaries or inverse actions. Phases remain
coherent across index superpositions. Empty index sets have no ordinary maximum
and need not supply a normalized label input; vacuous entry equations are not
state preparation.

Known positive entry bounds, exact weighted sparse decompositions and clean
entry interfaces are separate obligations. Under the specified nonempty square
interface the derived projected block has scale `s M`; entry normalization alone
does not construct that interface or permit duplicate nonzero pieces. Dense
entry bounds do not imply the same operator norm bound. Rectangular adapters,
zero outputs and postselection normalization are explicit cases.

At an endpoint, changing `z=1` to `w=1-delta` produces a square-root-size column
error. The stated whole-unitary estimate applies to the specified completion,
not all completions with that first column. A finite nonempty strict max-norm
bound really does give a positive gap; implementing finite-precision arithmetic
still needs an error budget or guard against crossing it. Clipping, if used,
must be charged as an approximation. Phase synthesis, reversible arithmetic,
scratch, inverses, PREP/SELECT and original oracle calls are not free gates.

## Compatible natural-language and Lean continuation

Re-export the current registry before contributing. The two tracks remain views
of one core registry, not competing datasets. Answer-only repairs retain the
nine-field question contract but invalidate approval of the old answer.
Plan120 and plan208 have new question contracts; old-contract formal proposals,
task identities, validation and receipts do not transfer. Plan208 recomputes
its active context and task hashes, while preserving predecessor hashes and
premises as history. The reader shows current assumptions before the question
and keeps historical premises in a separate folded audit panel.

Useful formal subtargets include the kernel/image division-ring argument,
finite normalized coefficient identities, annihilator duality, the two-by-two
phase-aware unitary, endpoint error and clean projected-block composition. A
proof of one subtarget must name its coverage rather than certify the complete
revised explanation. No additional native formal companion is admitted here.

Shared mechanisms also connect plan106/118, plan117/119/120 and plan207/208/209.
Record these as assessed subproof relations; shared nodes alone prove neither
whole-question equivalence nor independent train/test evidence. Inherited splits
remain unchanged pending global reconciliation. A genuinely new mathematical
target starts as an uncounted UUID proposal; a translation or corrected view
does not receive a second permanent core ID.

## Evidence and remaining acceptance gates

The full candidate, rubric, explanation and contract changes were reconstructed
by distinct actual reviewers, with exact predecessor/candidate/source/contract
bindings and disclosed exposure. Public-safe projections of the plan117/118
reviews remove only private host locators and bind their unchanged originals;
they do not invent a fresh reviewer or review. Root's bounded matching-byte,
text and rendered-source inspections are distinct from worker text-only source
access. Source statements are not automatically mathematical authority.

The current reader has **203 active core IDs and 10 reserved corrections** in
the preserved 213-obligation scope. Three native library-lemma formal companions
are unchanged. These counts do not assert completed semantic deduplication.
Global reconciliation is incomplete, isolated untrusted Lean evaluation remains
environment-blocked and model baselines remain unmeasured. The frozen preview
tag is unchanged. Website/build/browser/deployed readback evidence is recorded
separately at the exact commit; no stable promotion follows from this document.
