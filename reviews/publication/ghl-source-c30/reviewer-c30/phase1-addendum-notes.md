# Independent natural-source addendum review — c30

Status: PHASE1_NATURAL_ADDENDUM_REVIEW_COMPLETE; formal comparison remains unauthorized and unperformed. This record supplements, and does not edit or supersede the bytes of, `$REVIEWER/source-only-notes.md` and `$REVIEWER/phase1-seal.json`.

## 1. Inputs, reading, provenance, and limited conclusion

The newly authorized mathematical input is `$AUTHOR/final/metadata/successor-v3/source-clarification-v2.md`, SHA256 `4f5bbe1ae34abad5a7c3ffeb46c2d876ccc325e802a974f954efb821ca3cf9eb`, 1967 bytes, 11 lines. I read all lines in raw and numbered form, without truncation. Its actual digest matches the supplied expected digest. No directory listing was required; no sibling metadata file was opened.

The original mathematical source `$AUTHOR/final/source-only.md` remains SHA256 `c774ecaf66c3d3c9586c41f7441b416ee77bfd54a3314e1d9ee66ff7151db6f5`. I had already read all 253 lines in phase 1 and now reread numbered lines 45–94, including M2 through M4. The seven process protocols read completely before the original phase remain the governing process inputs; no other repository material has been read. Prior source-only notes and seal were not edited; their original digests were checked again.

M14 acknowledges the author's receipt of one authorized clarification request after the original freeze. This addendum is therefore an independent verification of a visible, feedback-informed source successor, not a claim that the original source already explicitly contained the canonical guard. The author's claim to have rechecked implementation definitions/header is provenance only: I have not read those definitions or a formal statement and do not independently verify that claim. Historical formalizer identity remains UNKNOWN.

Conclusion at the natural-mathematics layer: M14 is sufficient to resolve GAP-01 for the combined original-source-plus-M14 explanation. It specifies the old row-local bulk predicate, both branch orders, and the exact restricted theorem domain. I can independently prove the resulting roundtrip below. This does not certify that these are the actual Lean definitions or that a Lean theorem has this type. GAP-01 remains a historically accurate omitted-specification finding on the original frozen source in isolation; its status is RESOLVED_BY_VISIBLE_NATURAL_SUCCESSOR, not retroactively absent.

## 2. Exact interpreted definitions

Let n be natural, N=2^n, and let natural subtraction be truncated. Write `B(r)` for the canonical predicate `2 <= r <= N-3`. This B is not the generic arbitrary-parameter interval predicate from M1/M2.

Combining the original M4 formulas with M14, define the row-local forward map A(i,s), in this ordered case structure:

1. If B(i), return `(i-2)+s` for s<5 and i otherwise.
2. Else if i=0, return s for s<3 and i otherwise.
3. Else if i=1, return s for s<4 and i otherwise.
4. Else if i=N-2, return `(N-4)+s` for s<4 and i otherwise.
5. Else if i=N-1, return `(N-3)+s` for s<3 and i otherwise.
6. Else return i.

Define the reverse candidate R(t,r), in this ordered case structure:

1. If r=0, return t.
2. Else if r=1, return t.
3. Else if B(r), return `(t+2)-r`.
4. Else if r=N-2, return `t-(N-4)`.
5. Else if r=N-1, return `t-(N-3)`.
6. Else return t.

For the statement under review assume n>=3, i<N, s<8. Put r=A(i,s) and q=R(i,r). The claim is `q<8` and `A(r,q)=i`. It is NOT `R(A(i,s),i)=s`, not uniqueness of s, and not invertibility of A as a full sparse-input map.

Since n>=3, N>=8. The five row regions `0`, `1`, `[2,N-3]`, `N-2`, and `N-1` are disjoint and exhaust rows below N. Thus branch precedence is explicitly specified on the total carrier, while on this restricted theorem domain it creates no overlaps. For every used branch below, arithmetic subtraction is ordinary subtraction because the corresponding inequalities establish absence of underflow.

## 3. Complete hand proof of the canonical roundtrip

### 3.1 Exterior input rows, used slots

These tables give every used slot for all four exterior row types. Here r is the first forward output and q is the reverse candidate. Each table entry also verifies q<5 and `A(r,q)=i`.

| Input i | Used s | r=A(i,s) | q=R(i,r) | Second forward evaluation |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | A(0,0)=0 |
| 0 | 1 | 1 | 0 | A(1,0)=0 |
| 0 | 2 | 2 | 0 | A(2,0)=2-2=0 |
| 1 | 0 | 0 | 1 | A(0,1)=1 |
| 1 | 1 | 1 | 1 | A(1,1)=1 |
| 1 | 2 | 2 | 1 | A(2,1)=1 |
| 1 | 3 | 3 | 0 | A(3,0)=1 |
| N-2 | 0 | N-4 | 4 | A(N-4,4)=N-2 |
| N-2 | 1 | N-3 | 3 | A(N-3,3)=N-2 |
| N-2 | 2 | N-2 | 2 | A(N-2,2)=N-2 |
| N-2 | 3 | N-1 | 1 | A(N-1,1)=N-2 |
| N-1 | 0 | N-3 | 4 | A(N-3,4)=N-1 |
| N-1 | 1 | N-2 | 3 | A(N-2,3)=N-1 |
| N-1 | 2 | N-1 | 2 | A(N-1,2)=N-1 |

All intermediate r lie below N. In particular N-4 and N-3 are bulk rows because N>=8; rows2 and3 are bulk as well. These facts justify every selected branch in the table.

### 3.2 Bulk input row, used slots

Let `2<=i<=N-3` and `0<=s<5`. Then `r=i-2+s` lies in `[0,N-1]`. Split by the exhaustive region of r:

| Region of r | Forced facts | Reverse q | Verification |
| --- | --- | --- | --- |
| r=0 | i=2,s=0 | q=i=2 | A(0,2)=2=i |
| r=1 | (i,s)=(2,1) or (3,0) | q=i in {2,3} | q<4, so A(1,q)=q=i |
| 2<=r<=N-3 | r=i-2+s | q=i+2-r=4-s in {0,1,2,3,4} | q<5, so A(r,q)=r-2+q=i |
| r=N-2 | (i,s)=(N-3,3) or (N-4,4) | q=i-(N-4) in {1,0} | q<4, so A(N-2,q)=N-4+q=i |
| r=N-1 | i=N-3,s=4 | q=i-(N-3)=0 | A(N-1,0)=N-3=i |

For the bulk-r line, s<=4 implies r<=i+2, which licenses cancellation in the truncated reverse subtraction. All q here are below5 and hence below8. No arbitrary K1,K2 or separate assumption about coefficient nonvanishing is used.

### 3.3 All unused-slot cases

An unused slot returns r=i. Since i<N, its region is one of the five above. The reverse and second forward are:

| Region of i | Unused condition (with s<8) | q=R(i,i) | A(i,q) |
| --- | --- | --- | --- |
| i=0 | 3<=s | 0 | 0 |
| i=1 | 4<=s | 1 | 1 |
| 2<=i<=N-3 | 5<=s | 2 | i-2+2=i |
| i=N-2 | 4<=s | 2 | N-4+2=N-2=i |
| i=N-1 | 3<=s | 2 | N-3+2=N-1=i |

Each returned q is within the used-slot range of its row and below8. Together with sections3.1–3.2, this exhausts all five row regions and all eight sparse inputs. The proof actually yields q<5 in every case. That stronger mathematical observation is not presented as an observed formal theorem or a request to change a theorem signature.

## 4. What happens to the original counterinterpretation

The original phase-1 GAP-01 concerned the missing explicit separation between generic bulk `[K1,K2]` and the old canonical bulk. Its all-bulk example used N=8,i=0,s=4 and the alternate choice that all rows are bulk, with bulk tested first. M14 expressly rules out that alternate predicate for M4, so that example is not a counterexample to the now specified canonical claim.

Under the actual clarified formula at the same numerical i=0,s=4, canonical B(0) is false. Slot4 is unused on row0, so r=A(0,4)=0, q=R(0,0)=0, and A(0,0)=0=i. Thus the former interpretation-dependent failure disappears for the specified source target, not by introducing a new mathematical premise on K1,K2 but by selecting the previously under-described n-only function.

The collision remains: at N=8,i=0, both s=0 and s=3 give A(0,s)=0. Consequently the canonical reverse-on-image result does not rehabilitate the colliding row-local sparse model. It selects a returning slot and is consistent with many original slots sharing one image. The global modular seven-slot map remains a different definition; M14 creates no OR route substituting the old map for it.

The theorem guards still matter. For example n=1,N=2,i=0,s=2 meets i<N and s<8 but not n>=3. The clarified forward map sends it to r=2. Reverse at r=2 falls through to target0, and forward on row2 then falls through to2, not0. No n=1 theorem is claimed, and the example is merely a boundary check for the total definitions.

## 5. Source coverage and topology delta

| M14 lines | Disposition | Reviewer node |
| --- | --- | --- |
| 1 | EXCLUDED(heading/version label) | No independent mathematical claim |
| 3 | NODE AD01 | Canonical predicate, natural subtraction, explicit distinction from arbitrary bulk |
| 5 | NODE AD02 | Complete forward region precedence and slot bounds |
| 7 | NODE AD03 | Complete reverse precedence, outputs and fallback |
| 9 | NODE AD04 | n>=3,s<8,i<N theorem scope; no arbitrary-K claim; implementation-matching claim unverified here |
| 11 | NODE AD05 + EXCLUDED(as proof of implementation/fidelity) | Feedback-informed successor provenance and old SHA; claimed implementation recheck is author testimony, not reviewer evidence |
| Blank lines | EXCLUDED(format only) | No lost substantive content |

The original SF17 dependency is now refined, without editing the original artifact:

`{SF16 old forward formulas, SF17 old reverse formulas, AD01 canonical predicate, AD02 forward order, AD03 reverse order, AD04 n>=3 and i<N and s<8, natural arithmetic} -> {q<8 AND A(A(i,s),q)=i}`.

AD04's statement of the desired theorem is not itself a proof premise. Its legitimate tail contribution is only the declared domain. The proof is the exhaustive independent arithmetic in section3. The five input regions and used/unused slot conditions are exhaustive proof cases, not alternative sufficient construction OR-routes. The output conjunction contains both the candidate range and roundtrip equation. No edge is added to full-space injectivity, unitary extension, physical transpose-inverse, all-zero cleanup, normalized block identity, or resource certificates.

GAP-01 is resolved for the augmented natural-source explanation only. The other original gaps GAP-02 through GAP-11 retain their scope: full-space sparse extension/inverse; analytic scalars/normalizers/rotations; boundary angle convention; f-oracle completion/coherent access and exact external dependencies; PREPARE/unprepare and cleanup/transcript bridges; complete gamma/product expansion; final normalized block/projection identity; cost model/certificates; original-paper fidelity/PDE and out-of-scope Hamiltonian composition. M14 neither supplies nor claims those bridges.

## 6. Binder, definition, and seven-slot preservation checks

Definitions: A,B,R are literal ordered total natural functions. The canonical predicate is definitional, not an additional ad hoc hypothesis on a theorem with arbitrary bulk inputs. No characterization by choice, quotient/representative selection, unique inverse, or unitary completion is introduced.

Binder expectations for this narrow claim: n,i,s are natural data (TYPING); n>=3,i<N,s<8 are SOURCE hypotheses relative to the combined retrospective local text; N=2^n and the precise canonical A/R definitions are STANDING or definitional. K1,K2 are absent. There is no RULED correction and no license to insert proof ingredients as EXCESS binders. Correct branch selection, row-image range, q-range and the roundtrip equation are derived dependencies. The claim that these guards already match the unread implementation remains pending formal comparison.

The seven quantum slots are unchanged except for the more precise classical address definition: target is still a row-local returning-preimage identity, not a quantum normalized operator; scalar/dimension conventions are natural indices and N=2^n; no new oracle/inverse/control access is constructed; no workspace cleanup or full reversible extension is added; no phase convention is changed; no success/error/probability bound is added; no gate/query/finite-bit resource theorem is supplied. In particular the candidate range q<8 does not establish injectivity, let alone a coherent sparse oracle. The original collision is retained.

## 7. Immutable records and stop condition

The preserved original notes have SHA256 `2eead1cf1d5663b1cff9ebab130ac47354e0a94064688abd6321613d4fd7273b`. The preserved original seal has SHA256 `dd8f89ad322ce3fbbe7cd985aa5888635b140d8bfb31a7e9d1a4be9d31d23a9b`. These are the same values returned after original phase1; neither file was edited. Public logical paths in this addendum use only `$AUTHOR`, `$REVIEWER`, and `$PROJECT` aliases. The source digest always refers to original bytes, not a redacted rewrite.

Failure class for completing this addendum: NONE. There is no mathematical retirement of the canonical claim; its natural proof is supplied above. No formal, decoder, other metadata, CI, compilation, cache, or implementation runtime result was read. No Lean, Git, network, or subagent was used. No native acceptance, proof seal, final-root closure, merge, or purification is asserted. This phase ends after the separate addendum seal and actual artifact hashes; any formal comparison requires another explicit authorization.
