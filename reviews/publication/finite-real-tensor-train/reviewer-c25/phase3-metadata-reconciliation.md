# TTC/NORM: late author-metadata reconciliation

Status: `METADATA_MATCH_LIMITED_SOURCE_WITH_NONBLOCKING_PRECISION_NOTES`.
Reviewer: `ttc_norm_source_first_review_c25`.
No decoder result or compilation evidence has been read at this stage.

## Chronology and preserved independence

The parent separately authorized this stage AFTER the independent source-only
phase and the actual-source static comparison had both been frozen. All four
original artifact hashes remain unchanged:

| Artifact | SHA256 |
| --- | --- |
| source-only-notes.md | 84011962ce0cdaedbf27027c7f7c17c0b50562da716fd1b5d030a5a0dbb3051b |
| phase1-seal.json | fe9c73b69d5e0d48990d94ebb8becf6f82157bf0335161002c443cf2d15650f8 |
| phase2-static-comparison.md | 615f1be47ad998945e35bb370bd084d1b6fae812422e536fde7139ad359a39f5 |
| phase2-static-seal.json | b9e43c4f479343322e9ece9d4f3bad41220e6470aa223111b6cbae4d3e78bcff |

Only now was the late author packet opened. Its `outputs-manifest.json`
SHA256 is `8d48512050438af73e4560a56f1e1d68e15cb589990a5664eb5938253eebceef`,
matching the parent's supplied value. The source remains retrospective local
exposition, not an external paper/book, pre-proof record, historical
independence claim, or novelty certificate. Historical formalizer is UNKNOWN.

The author graph explicitly says it transcribes THIS reviewer's frozen
phase-1 source graph after the author already knew the implementation.
Its two independent-ground hashes exactly match the preserved phase-1
artifacts. Therefore the author's graph is NOT another independent blind
review, and the later author's alignment cannot replace phase-2 independent
actual-source comparison. Nothing here backdates a metadata packet as having
been received before either freeze.

The parent reports current production HEAD `70649f5` and prior author-input
HEAD `cf77fde090fff00fcb829d1684b85596eec4949f`, with baseline/origin main
`f2cba045611a0d11c5995c29607569726bf1d6c5`. I ran no Git command to verify
commit identities. I DID independently verify equality of the actual 202
production/test Lean input paths and their original bytes against the author
freeze. Current proof inputs therefore match this freeze without relying on
the reported commit labels. No 4.33 evidence is thereby claimed to certify
origin/main's different reported 4.29.1 environment.

## Material inspected and replay discipline

Read the allowed README, source-row candidate, source coverage, graph views,
formal context, both publication candidates, diagnostics, author freeze,
author self-test code and self-test result. Repeated Lean snapshots in formal
context were compared byte-for-byte to the actual files, rather than assumed
equivalent because their metadata hashes agree. An initial broad display of
context snapshots was truncated; subsequent structured projections and exact
byte comparisons covered the relevant metadata without pretending that the
truncated display itself was a complete new semantic read.

The full 49 obligation rows were compared against the already independently
reviewed target source, including all typing descriptions, logical premises,
conjunctive outputs and paragraph links. Truncated display intervals were
recovered by focused reads, including E13/E14 and TN-05 through TN-10. Six
full context snapshots plus two toolchain/manifest snapshots were verified
against actual bytes. This is snapshot integrity, not a new claim to have
semantically reviewed every unused declaration in all six provider files.

I did NOT open `author-decoder-packet.json`, any decoder/reconstruction output,
any independent other review or any compilation report. Its manifest path/hash
being visible is not content review. The author self-test source reads that
packet, so I did not execute the self-test wholesale. Instead I ran a separate
read-only integrity replay, with Python bytecode writes disabled, exercising
only the inspected metadata and unchanged public binding function. The public
checker's `validate_record`, `check`, Git helpers and main entrypoint were not
called. No Lean, simulator, Git, network, cache write, or sub-agent was used.

## Exact source coverage and actual named items

All 79 `exact_text` source paragraphs concatenate, with no added separator,
to the original 13,531 source bytes and SHA256
`895ec97fe7e95146ec8d374bdcbecf4edbf40ff7e787135d032e376841d773b7`.
Every paragraph byte offset, end offset and paragraph hash was checked.
The published lesson at
`docs/lessons/finite-real-tensor-train-canonicalization-and-gram.md` is now
byte-identical too. This is a real published lesson check, not a private file
being relabelled as a previously read public bundle.

The 79-paragraph layout has 9 reasoned EXCLUDED title/navigation paragraphs;
all 70 other paragraphs have NODE dispositions. Its source coverage matches
the frozen source-line analysis: P004–P008 carriers/contractions/canonicality,
P010–P016 absorption and thin factors, P018–P033 tail-first dimensions and
complete mass/normalization, P035–P042 complex columns/local action,
P044–P055 prefix padding/local column action/isometry, P057–P067 full Gram
norm/target adapter, P069–P076 literal H/T/F budgets and omissions,
P078–P079 exact scope and stronger-consumer boundaries. No substantive
paragraph is dropped because it lacks a separately named target theorem.

An independent scan of the two actual sources gives the same 49 hand-written
named items as the context and coverage: TC's 33 non-instance roots, NE's 15,
plus the named ambient `wordFintype` instance at TC line 33. Every name,
module and source-line anchor was checked; this is not a count-only match.
The two candidate declaration lists and obligation maps contain exactly their
33/15 public roots. `wordFintype` is explicitly present in full ambient context,
coverage and graph ownership; its inventory omission is not used as an audit
exemption. Generated Chain/RankReduced constructors and recursors stay in the
full source snapshots. No exact word-cardinality theorem is fabricated.

The per-result binder maps agree with actual source, especially:

- RankReduced's recursive `tail` premise and helper `h` premises are SOURCE;
- normalized canonicalization uses input `hv`, not a pre-normalized residual;
- scalar state uses the original amplitude square sum, not target-state action;
- equal-rank local step has only `hU` clean columns as its logical premise;
- padded local step has `hl` AND `columns`, and deliberately no outgoing `hr`;
- padded active isometry has `hl` AND `hr` AND real row orthogonality `hA`;
- norm's target adapter has source bijection `e` AND pointwise action `h`;
- H/F bounds use the stated maxBond/dimension bounds, not stored-operation costs.

All outputs remain AND-conjunctions where appropriate. Literal definitions
are not replaced by off-locus fallback semantics. Existential factors remain
noncanonical choices with no unique-factor or deterministic-runtime claim.

## Graph comparison

The source-construction view retains all E01–E22 complete AND tails from the
frozen phase-1 table and every corresponding mathematical head. The author
clarifies E11's per-specialization scalar endpoints and E18's nonzero-amplitude
condition for positivity; neither strengthens norm equality globally. Thin LQ
dimension branches are guarded OR-cases, not individually unconditional
algorithms. The Gram route does not require canonical factorization.

All seven independent SOURCE_GAP identities are distinct, OPEN and marked
not mathematical proof nodes. The four diagnostic discriminator labels remain
separate from proof nodes. The extra
`SOURCE_GAP-AUTHOR-STANDALONE-EXPLANATIONS` is transparently author-added,
not an eighth finding attributed to this independent source reconstruction.
Its P015/P022/P064 explanation boundary agrees with phase 2: provider-level
thin-factor mathematics, componentwise bond consequences and empty norm one
must not be assigned nonexistent standalone target theorem names. This added
gap label is an audit/no-dedicated-root caution, not evidence those ordinary
mathematical consequences are false or beyond the derivations reviewed here.

The 49-name author-obligation-alignment view is separately labelled proposed,
not independent source topology and not elaborated Lean theorem dependencies.
Its per-result premise nodes preserve the actual SOURCE binders and its
heads/outputs/paragraph links agree with coverage. It must be kept distinct
from E01–E22, even though both are currently AND-based presentations.

The Lean view's three target import edges match actual imports exactly:
TC imports ThinLQ and SequentialBondPreparation; NE imports TC. All 49
ownership mappings agree. The four listed provider import lists match the
actual complete snapshots. It asserts no theorem-dependency edges, so no
import is being promoted into a claim that every theorem uses every provider.

The compressed spine is AUTHOR_PROPOSED_NOT_PURIFIED with lossless links to
coverage/context. The functor view has no certified transport or implication
hyperedges and is navigation-only. Neither view silently supplies SP/BE,
unitary completion, terminal cleanup, coherent-oracle or resource transports.

## Byte integrity and prospective binding replay

The read-only replay found no integrity mismatch:

- 12 manifest artifacts checked, excluding the deliberately unopened author
  decoder input; each original byte count and SHA256 matched;
- all 79 paragraphs reconstructed and individually checked;
- all 49 actual named declarations/context/coverage anchors matched;
- six formal snapshots and two toolchain/manifest snapshots matched;
- all 202 production/test Lean paths and bytes matched the freeze; five other
  fixed inputs and eight named provider/existing-lesson inputs also matched;
- coverage/context/graph cross-hashes and alignment links matched;
- current published lesson equals the reviewed immutable source.

The unchanged public checker's `binding_digest` was called directly with an
in-memory overlay of only the proposed source row and a byte-identical lesson
redirect. No canonical source or publication record was written. The source
row is currently absent from the canonical source registry. Its retrospective
identity, whole-module scope and exact-real/local/syntactic cost limit agree
with the independent static findings. Neither a repository URL nor
`primary-text-checked` is treated as external-paper provenance.

The replayed digests equal the proposed values:

| Module | Replayed prospective binding SHA256 |
| --- | --- |
| TensorTrainCanonical | 98bafeedc584e7ef69fbe6e980a1d5ab558367d63ab3dfb01bee2f727788ffcf |
| TensorTrainNormEnvironment | b0012c045d55fae10eff8fea86a493c4bb48e3cbe0586eae44fd0cd374346afa |

These are prospective payload/content bindings, not validation/admission.
Both candidates keep future decoder/reviewer paths explicitly unaccepted,
retrospective Statement Seal timing, pending purification/Exposition Seal,
and false main_admission/scientific_ROOT. `lakefile.lean` is separately frozen;
the public binding function does not include it, and I did not silently modify
the binding recipe to pretend otherwise.

## Nonblocking precision notes

1. `author-freeze.json.binding_recipe` says “literal twelve-field payload”.
   The actual unchanged checker lists ELEVEN fields:
   module, source_id, source_statement, source_anchor, lesson_path,
   declarations, obligation_map, assumption_deltas, graph_contribution,
   formalizer, residual_boundary. The actual executed digests match; this is
   a wording/count error, not a byte-binding or semantic failure. Correct it
   in any successor author recipe rather than implying a twelfth hashed field.

2. The source-mechanism graph's E07 recurrence tail is labelled
   STANDING_OR_TYPING_DEPENDENCY with public_theorem_premise=false. Read that
   as conceptual dimension-recurrence bookkeeping, NOT the public binder audit:
   actual RankReduced helper `h` premises are SOURCE in TC-12/13/22, as correctly
   preserved in coverage and author alignment. Its tail is explicitly present,
   so no dimension assumption is erased. A reader-facing successor should
   avoid suggesting that an arbitrary pair satisfies the recurrence without
   the RankReduced relation. This is annotation-scope caution, not a missing
   AND tail or newly detected formal mathematical defect.

## Reconciliation verdict and remaining gates

No blocking metadata/source/static inconsistency found. The bounded late
metadata is consistent with the independent source-only and actual-source
static review, with the two precision notes above. All seven semantic slots
remain as frozen: full real target/mass, exact finite/zero dimensions and
unbridged physical order, no oracle producer, conditional clean columns and
open global cleanup, signed amplitudes, exact norm without success/error
claims, and syntactic rather than actual/finite-bit/circuit resource bounds.

This result does NOT accept a decoder, compilation run, elaborated axiom
closure, final publication record, canonical registry admission, purification,
complete physical scientific ROOT, or whole textbook. Those materials and
gates remain separate and unseen/not run. No mathematical route is refuted;
failure class is NONE. Preserve all previous seals and this reconciliation.
