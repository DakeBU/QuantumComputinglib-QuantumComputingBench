# Agent Guide for ASPBE

This repository is a Lean-first proof and circuit-construction project.

The public system name is **ASPBE: Automatic State Preparation and Block
Encoding for Quantum Computing**. The generated teaching website is
**QuantumComputinglib**. Historical `QBE-*` task IDs, `ABEISBlueprint` module
names, CLI role keys, and paths remain stable for reproducibility; do not
introduce new public prose that expands ABEIS or describes the website as
ABEIS.

## Mission

The current ASPBE construction engine starts with a concrete state-preparation,
block-encoding, or query-oracle contract. Replace abstract oracle assumptions
with explicit mathematical and circuit semantics, then prove in Lean that the
construction satisfies the requested state action, projected block, or oracle
condition. Export readable mathematics, theorem-linked circuit figures, and
optional executable artifacts without overstating the certified frontier.

QuantumComputinglib has a broader long-term textbook mission. State Preparation
and Block Encoding are Parts I and II; Quantum Information and Representation
Theory and Quantum Algorithms for Scientific Computation are peer Parts III
and IV with planned chapters until local admission. Their material uses the
same source/publication protocol and must reuse the shared lower Lean graph
whenever semantics agree. See `docs/quantum-domain-roadmap.md`. Planned
curriculum is not evidence of local theorem closure.

## Canonical Harness Protocol

The mandatory quantum-specific publication, source-blind review, graph and
reader gate is [docs/theorem-publication-protocol.md](docs/theorem-publication-protocol.md).
New or materially changed source-facing theorems/definitions also follow
[docs/proof-digestion-protocol.md](docs/proof-digestion-protocol.md) and [docs/evidence-routed-memory-protocol.md](docs/evidence-routed-memory-protocol.md): seal the
exact quantum contract before proof search, expand/classify binders, audit
literal/characterized/quotient definitions, reconstruct the source proof or
construction topology independently of implementation Lean, require exhaustive
source coverage, and run post-merge purification before calling the result
human-facing complete. Failed routes are typed and salvaged before cleanup; the control plane has no mathematical authority; routine coordination is deterministic/low-token by default; parallel Workers require distinct uncertainty; and multiple serious routes receive a common-blind-spot audit. Read both protocols before changing a production Lean
module or publishing a new source claim.
Use the bounded mechanism/route packet rather than dumping the complete graph.

Read these before nontrivial automated work:

- [`HARNESS.md`](HARNESS.md): ASPBE Harness v2, its progress metric, evidence
  gates, Master–Worker scheduling, and compatibility mapping;
- [`.agents/skills/qbe-frontier-master/SKILL.md`](.agents/skills/qbe-frontier-master/SKILL.md)
  for global frontier refresh and synthesis;
- [`.agents/skills/qbe-substantive-worker/SKILL.md`](.agents/skills/qbe-substantive-worker/SKILL.md)
  for one end-to-end mathematical objective.

The cognitive roles are now:

- **Frontier Master:** owns the frozen contract, global proof DAG, independent
  fork selection, evidence reconciliation, stale-work retirement, and final
  synthesis.
- **Universal Workers:** each own one substantive mathematical advance or sharp
  obstruction end to end. They may cross source reading, derivation, Lean,
  finite diagnostics, resource analysis, diagrams, and exposition.
- **Evidence gates:** source, semantic, Lean, integration, and exposition checks
  are acceptance functions. They are not permanent castes that limit what an
  agent may notice or contribute.

Existing `upper`, `middle`, `lower1`–`lower4`, and `reviewer` CLI/profile names
are backward-compatible execution slots. They do **not** restrict cognitive
scope. Where older documents describe fixed Upper/Middle/Lower personalities,
`HARNESS.md` governs new runs.

## What Counts as Progress

One Worker invocation should deliver a **substantive mathematical delta**:

- a named theorem or reusable interface needed by the root;
- an exact source-to-semantics bridge;
- a counterexample that retires a route;
- proof-DAG compression that removes repeated work;
- an integration theorem reaching a higher frontier node;
- or a theorem-linked explanation/figure that removes a material ambiguity.

Branches, commits, files, prompt volume, finite examples, and isolated local
lemmas are not progress by themselves. A failed attempt is useful only when it
returns a typed obstruction that changes the next global decision.

## Non-Negotiable Lean Gate

Every proof-bearing run must finish with:

```bash
lake build && lake build Tests
```

If the gate fails, the mathematical task is not done. Record the exact failure
and the highest still-certified frontier.

## Documentation and Pages Gate

When a change affects Lean declarations, Blueprint prose, the Library Explorer,
website content, diagrams, or deployment configuration, run:

```bash
bash scripts/build-all.sh
```

This records a current-commit Lean gate, checks the declaration inventory,
builds the Verso Blueprint and unified static site, and checks links, fragments,
source links, search counts, local-path leakage, preview authentication, and the
final Pages artifact layout.

Do not handwrite declaration counts in reader-facing content. Do not create
GitHub source links against an assumed branch; publication links must be
commit-pinned and generated by `website/scripts/build_site.py`.

## Figure and Textbook Gate

A circuit figure is complete only when a reader can identify:

- every input register and its bit order;
- which register is preserved and which is overwritten;
- the exact transformation after each gate/subcircuit block;
- the separate data path and carry/flag path;
- the operand and comparison convention;
- the named Lean theorem or explicit unproved obligation behind every
  advertised arrow;
- the difference between a finite diagnostic and an arbitrary-width theorem.

For example, a proof of complement arithmetic does not certify a printed adder
circuit until individual gate semantics are composed through the source
subcircuits to the figure-level theorem.

## Operating Loop

1. Freeze or revalidate the task contract and evidence class. For a source-facing Anchor, complete the Statement Seal before proof search; proof ingredients are dependency edges, never extra public hypotheses.
2. Refresh the global proof frontier, root theorem, blocking interfaces, and
   independent uncertainties.
3. Give each Universal Worker one objective large enough to produce a
   substantive advance, with the smallest sufficient context pack.
4. Let Workers use any relevant repository skill; do not stop useful reasoning
   at an old role boundary.
5. Require the structured handoff from `qbe-substantive-worker`.
6. Reconcile conventions and run cheap discriminators before expensive proof
   search when the target may be wrong.
7. Run the Lean gate and, for public changes, the full documentation gate.
8. Synthesize one global delta, update the proof DAG/conversion window, and
   retire stale or duplicate work. Keep Source Proof/Construction Graph topology
   separate from Lean implementation topology.
9. After integration, run the purification pass: remove dead/duplicate/wrapper-only
   residue, canonicalize shared quantum primitives, compress bookkeeping, and
   preserve lossless drill-down evidence before marking the result PURIFIED.
10. Log the attempt with `tools/qbe.py trial-log`; update task status only after
   the required gate succeeds.

When working in an automated cycle, read `runs/<run-id>/dialogue.md`, use the
compact context pack when available, and append a handoff before stopping. Lean
source of truth remains in `QuantumBlockEncoding/`; reviewed derivations live
in `docs/`, `paper-notes/`, conversion windows, and generated textbook pages.

## Project Commands

```bash
python3 tools/qbe.py status
python3 tools/qbe.py harness-check
python3 tools/qbe.py harness-audit
python3 tools/qbe.py list-literature
python3 tools/qbe.py new-task QBE-AUTO-004 --title "Formalize sparse access oracle"
python3 tools/qbe.py conversion-window QBE-AUTO-004 --title "Sparse access oracle"
python3 tools/qbe.py run-cycle QBE-AUTO-001 --cycle 1 --lower-count 2
python3 tools/qbe.py sleep-run QBE-AUTO-001 --cycles 8 --lower-count 3 --dry-run
python3 tools/qbe.py agent-note latest --role lower --message "substantive handoff"
python3 tools/qbe.py trial-log --task QBE-AUTO-001 --role lower --kind attempt --status blocked --notes "typed obstruction"
python3 tools/qbe.py trial-summary
```

The old slot names in these commands are compatibility syntax. A run may map
`upper` to the Frontier Master, `lower1`–`lower4` to independent Universal
Workers, `middle` to a Worker or synthesis pass, and `reviewer` to a
fresh-context evidence-gate pass.

## Skills Are Lenses, Not Job Boundaries

Use repository skills whenever they help the current objective:

- `qbe-source-dependency-audit` for source anchors and external dependencies;
- `qbe-hierarchical-proof-dag` for reusable theorem interfaces and scheduling;
- `qbe-proof-blueprint` and `qbe-proof-diagnostics` for the active frontier and
  trust review;
- `qbe-block-encoding-library` for route retrieval before inventing duplicate
  constructions;
- `python3 tools/qbe.py atlas-search "<query>" --clean-only` for separately
  licensed textbook lemmas after local ASPBE and Mathlib search;
- `qbe-conversion-window` for Markdown/LaTeX/Lean correspondence;
- `qbe-math-writing` and `qbe-proof-export` for exact reader-facing proofs;
- `qbe-formalize-paper`, `qbe-cited-results`, and `qbe-verifier-feedback` when
  the objective requires them.

A Worker may combine all of these in one invocation. Preserve unexpected useful
ideas in the handoff even when they do not match the initial lens.

## Review Discipline

- Do not invent citations. Add unknown papers as candidates, then verify.
- Do not hide a mathematical gap with prose. Turn it into a named obligation.
- In faithful paper-reproduction mode, do not add hypotheses, side conditions,
  replacement circuits, swapped operands, or easier theorem variants.
- Prefer existing declarations and reusable interfaces over duplicated flat
  proof scripts.
- Do not mark a planned paper or figure as formalized until its advertised Lean
  root and tests compile.
- Do not promote a local arithmetic theorem as gate-level correctness without
  the gate/subcircuit composition bridge.
- Do not treat an ATLAS upstream build or quality score as an ASPBE proof. A
  narrow local adapter must pass the repository Lean gate before promotion.
- For open problems, include an acceptance test precise enough that Lean can
  eventually check it.
- Fresh-context review should inspect evidence and conventions, not merely the
  authoring agent's summary.

The shared conversation board is `runs/<run-id>/dialogue.md`; persistent memory
is `runs/trials.jsonl` plus `runs/trials_summary.csv`. Durable proof-frontier
state belongs in proof blueprints, conversion windows, named Lean declarations,
and task ledgers rather than only in chat history.

## External quantum Lean references and scope growth

Use Lean-QuantumInfo, lean-quantum, quantum-computing-lean, Lean-QuantumAlg-Bench
and Lean-QIT-Bench according to their recorded attribution and toolchain
boundaries. They are references or adapter candidates, not automatically local
dependencies or proof memory. Benchmark statement files remain unresolved
targets unless a separately checked proof/adaptor is admitted.

Before introducing a foundational quantum-information declaration (state,
density operator, partial trace, channel, distance, measurement, tensor-system
semantics, and similar objects), search local ASPBE, Mathlib, and these
attributed libraries. Prefer one reviewed adapter or one shared local node over
parallel domain-specific definitions. Toolchain or API mismatch is an explicit
frontier, not permission to copy a theorem and relabel it local.

The current automated synthesis emphasis remains gate-level oracle realization,
state-preparation certificates, and block-encoding certificates. Broader QIT and
scientific-computing chapters extend the shared graph without changing what
ASPBE currently claims to synthesize.

## Mathematical structure and research routes

The canonical authored records are `website/research/atlas.json`,
`website/research/state-preparation-wiki.json` and `website/research/sources.json`.
Current Progress is generated from these and the existing textbook/implementation
records. Do not create a competing completion ledger.

Before choosing a construction, run:

```bash
python3 website/scripts/research_atlas.py context --route spw-envelope
python3 website/scripts/research_atlas.py context --query "polynomial rank norm"
```

Every changed production module requires a current publication record binding
its entire source, toolchain/manifest, source statement, lesson, assumptions,
source-blind decoder and distinct independent reviewer, and graph delta.
Unchanged historical audit debt is not retroactively cleared. The mechanical
admission checker is `website/scripts/check_research_publications.py --base BASE`.

Keep actual Lean imports/ownership distinct from conceptual transports. Retain
complete AND tails and explicit failure maps. A contribution may be add-node,
shortcut, reorganisation or bridge; this is not an automatic novelty judgement.
Preserve SP/BE directionality and charge SELECT, input preparation, postselection
and amplification as appropriate. Read the full protocol for aesthetic,
finite-bit, source-fidelity and independent-review requirements.


## OpenAI Math upstream assimilation

Before using `openai/math`, read `docs/openai-math-assimilation-protocol.md`
and `research-wiki/openai-math-2026-intake.json`. The reviewed intake is commit
pinned; never use a floating upstream `main` to justify a theorem or completion
claim.

In particular, `OAI.InformationTheory.QuantumCircuit` and the larger QIT
clusters are adapter candidates, not automatic foundations. Search ASPBE,
Mathlib, and the already-audited quantum Lean libraries first. Any state,
channel, POVM, circuit, gate-order, tensor-order, Born-probability, or resource
semantics difference must be made explicit and bridged by a local compiled
adapter before downstream OpenAI theorems receive solid Lean-Graph edges.
Circuit-complexity lower bounds and QIT capacity results extend the library, but
must not be counted as block-encoding or state-preparation synthesis successes.
