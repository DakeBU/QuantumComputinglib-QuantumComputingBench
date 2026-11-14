# Supplementary natural-language workbook continuation

This additive contribution is pinned to main `036aea2a107d9258bba1c20b6e58cb6b9ee484f5`, graph `qcb-snapshot-ffa644f0da3031a1ce754b9a` and graph source `86b9e677566498da04faebcf4e5ed57f177c6bb1`. The re-exported registry contains 198 retained and 15 reserved cores. The two intake records cover 18 workbook entries.

The semantic catalog hash is `5269b9f2521e3bf14db293fea34895f6e44a387c2479c164407b4d16dd9a2247`. The source and comparison indexes bind the individual inputs.

Six public study candidates extend two families. The thirteen earlier public packets from two handoffs are compared separately from the published workbook. Their source and payload hashes remain in the comparison inventory.

| Packet | Proposed use | Coverage gain | Provisional band | Admission decision |
| --- | --- | --- | --- | --- |
| [G1s](question-sheets/G1s.html) | Public study, proposed training | Determine all one-gate locations consistent with measured populations and construct a compatible output for every signed input. | D2 | Pending identity, family exposure and official split. |
| [G2s](question-sheets/G2s.html) | Public study, proposed training | Prove the exact gate count on a line, including the cost of reversing the sign of a basis input. | D3 | Pending identity, family exposure and official split. |
| [G3s](question-sheets/G3s.html) | Public study, proposed training | Compute the optimal fidelity under a tree layer budget and construct an attaining circuit for signed amplitudes. | D4 | Pending identity, family exposure and official split. |
| [C1s](question-sheets/C1s.html) | Public study, proposed training | Test when a diagonal phase table can cross a permutation and give an interference witness when the test fails. | D2 | Pending identity, family exposure and official split. |
| [C2s](question-sheets/C2s.html) | Public study, proposed training | Classify diagonal changes of phase with fixed labels and pinned reference phases, and construct every permitted calibration. | D3 | Pending identity, family exposure and official split. |
| [C3s](question-sheets/C3s.html) | Public study, proposed training | Recover labeled cycle products in the distinct-length case and exhibit an ambiguity surviving all global power traces. | D4 | Pending identity, family exposure and official split. |

## Mathematical progression

**G1s.** Derive the prefix test in both directions for every possible input sign, identify all compatible edge locations in the equal-profile and unequal-profile cases, handle a zero pair, and diagnose two exact datasets.

**G2s.** Identify all separating cuts forced by the target, show they impose additive gate lower bounds, construct a signed preparation on the intervening path including zero target entries, settle both source-only signs and the one-site obstruction, and optimize source placement on multisite supports.

**G3s.** Bound arbitrary circuits by the coordinates reachable along time-ordered contacts, construct signed states on the chosen coordinates, join this with the sharp projection bound, solve the child scheduling problem by a polynomial dynamic program, and certify all requested depths on a tree where radius alone overstates fidelity.

**C1s.** Act on one basis ket to obtain weight \(a(x)b(p(x))\) and label \(q(p(x))\). Identify \(g=f\circ p\) and prove uniqueness. Give both directions of the exact orbit-invariance test and the single-constant test for \(f(p(x))/f(x)\), with a fixed sign convention for that constant. On two bits compute the table \(e^{i\theta(t\oplus c)}\), use the fixed control-zero columns to fix any common phase, and use a moved column to identify all angles. At \(\theta=\pi\) propagate a normalized two-term input through both orders, establish orthogonality, and explain equality of the basis-input output probabilities.

**C2s.** Derive the edge equation \(d_{p(x)}=(b_x/a_x)d_x\). Prove full-cycle consistency and compatibility of reference ratios with products of \(b_x/a_x\) along forward arcs. Show the cycle products classify an unpinned labeled cycle under diagonal conjugation, construct the phases from a base choice for each cycle, and show that every solution is obtained. An unpinned cycle has one free unit scalar, and a compatible pinned cycle has none. Include one reference, several references and fixed points. Construct two candidate devices with equal cycle products but inconsistent prescribed endpoints on a single cycle, and identify the specific failing arc.

**C3s.** Iterate the basis action and separate fixed labels of a power from nonreturning labels. Show that a length-\(\ell\) orbit contributes \(z^\ell-h_C\) to \(\det(zI-U)\) and contributes \(\ell h_C^{n/\ell}\) to \(t_n\) only when \(\ell\mid n\). For distinct lengths recover the product on the unique length-\(\ell\) cycle from \(t_\ell\) after subtracting all shorter divisor contributions, including the base case. With two fixed points and two transpositions, realize two assignments by unit phases and verify a common characteristic polynomial or equality of every trace, together with different within-length multisets. For the augmented observations, divide length-resolved traces by \(\ell\), use the first \(m_\ell\) power sums to reconstruct the monic polynomial of cycle products and all root multiplicities. Show that within-length permutations of products leave the reports invariant, and characterize unique labeled assignment for each length, including the cases of one cycle or identical products.

## Reading criterion scores

Record the points awarded for each criterion alongside the total. The table points to a convention or concept, one local deduction and one transfer task. The first criterion sometimes includes the first application of the concept. The three columns are examples from the full rubric. Apply each original weight once.

| Packet | Criterion containing D0 | Local reasoning example | Transfer or witness example |
| --- | --- | --- | --- |
| G1s | R1 (1 point) | R2 (2 points) | R3 (3 points) |
| G2s | R1 (1 point) | R2 (2 points) | R4 (2 points) |
| G3s | R1 (1 point) | R2 (2 points) | R4 (3 points) |
| C1s | R1 (2 points) | R2 (2 points) | R5 (2 points) |
| C2s | R1 (2 points) | R2 (2 points) | R5 (2 points) |
| C3s | R1 (2 points) | R2 (2 points) | R4 (2 points) |

## Review changes

The first full-content review requested changes to G2s. The original packets and verdicts are in `reviews/`. The current reports bind the corrected references and rubrics to the same frozen questions.

C3s also received a wording correction after its first acceptance. The boundary now attributes repeated roots to the polynomial reconstructed from the power sums. Both reviewed versions are retained.

## Files and scoring

Open [reader.html](reader.html) to inspect the complete material offline. Each of its five answer and evidence panels starts closed. Use the per-packet question sheets in the table for participant access. Each sheet contains only a title, assumptions, conventions and the question.

[Reader compatibility](evidence/reader-compatibility.json) records static checks on this and earlier readers and the browser restriction observed on the previous handoff. On a workstation with Python Playwright and local Chromium, run `python browser_check.py --chromium /path/to/chromium` for desktop, narrow-screen and keyboard checks.

[Printable questions](questions-print.pdf) contains the six public prompts with typeset mathematics, one question per sheet.

- [questions-only.jsonl](questions-only.jsonl) is the exact student projection. [references.jsonl](references.jsonl) and [grader-metadata.jsonl](grader-metadata.jsonl) join by slot and core ID. The two instructor exports also carry the exact item digest. Every rubric allocates ten points and admits mathematically equivalent proofs.
- [source-index.json](source-index.json) records Git and declaration-span hashes, frozen graph ownership, source-bound module import paths and a reverse index. [reasoning-topology.json](reasoning-topology.json) indexes chains, reuse and required join inputs. The reasoning maps distinguish supplied premises, deductions, independent join inputs, alternative routes and boundary conditions. [future-work.json](future-work.json) points to separately labelled planned work.
- [overlap-index.json](overlap-index.json) identifies canonical neighbors and their official splits, workbook and previous-delivery neighbors, shared subproofs and the decisive difference. [evidence/comparison-inventory.json](evidence/comparison-inventory.json) pins the populations screened. The baseline includes the public pilot’s 16 questions and the published descriptions of sealed assessment families.
- [review-index.json](review-index.json) binds independent question-only derivations and the comparisons of complete packets. The `reviews/` directories contain reviewer findings and any superseded artifacts. [evidence/intake-decisions.json](evidence/intake-decisions.json) summarizes the final decisions.
- [manifest.json](manifest.json) lists every package file and proposal with its raw byte length and SHA-256, plus the snapshot and catalog identity. [evidence/validation.json](evidence/validation.json) records the tests, rendering and comparison checks.

Public questions and references are study material. Difficulty bands describe the mathematical work requested. The 16 published pilot questions and public assessment descriptions were compared. No private question bank, pretraining history or model responses were used for overlap clearance.

[Matrix diagnostics](evidence/public-matrix-diagnostics.json) cover 153 labeled permutations and 315 signed-vector preparations. [Tree diagnostics](evidence/public-tree-diagnostics.json) compare the subtree recurrence with whole-tree matching enumeration on 2,310 finite instances. The general bounds and witnesses are in the reviewed derivations.

## Reproduce the validation

Extract the archive at the root of a full-history checkout of the pinned commit. Every repository-relative file in this contribution is new. Earlier packages and releases can coexist unchanged.

```sh
python benchmarks/quantumcomputingbench/tracks/non-lean/packages/b3a8eb51-c162-46a4-a117-021b837fe5c1/verify.py --repo /path/to/pinned/checkout
```

Public proposals also pass `python benchmarks/quantumcomputingbench/scripts/curriculum.py validate`. The print and standalone HTML questions are checked against the frozen JSON. Exact comparison covers only the named source populations. Official counting, split admission, human review, model performance and difficulty calibration remain pending.

Project-owned text is distributed under the pinned [MIT license](LICENSE.txt).
