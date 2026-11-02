# Contributing to ASPBE and QuantumComputinglib

ASPBE welcomes focused formalization, documentation, executable-validation,
and library-integration contributions. A contribution becomes part of
QuantumComputinglib only after it is reviewed, merged, and present in the
generated inventory.

## 1. Choose and agree on scope

Small corrections and narrowly scoped lemmas may go directly to a pull
request. Open a lemma proposal first when the work adds a new mathematical
contract, module, upstream dependency, construction family, or public API.

Before implementing a formal result, read
[the Proof Digestion Protocol](docs/proof-digestion-protocol.md), [the Evidence-Routed Memory Protocol](docs/evidence-routed-memory-protocol.md), and record:

- the plain-language and LaTeX statements and the exact Statement Seal for any source-facing Anchor;
- an exact source locator, upstream declaration, or `original result`;
- scalar type, dimensions, basis and register order, normalization, norm, and
  tolerance conventions;
- the intended owning module and declarations expected to be reused;
- whether the result is local, imported through an adapter, experimental, or
  part of a broader unfinished route.

Use the
[lemma proposal form](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/issues/new?template=lemma-contribution.yml)
or export a packet from the Live Formalization Workspace.

## 2. Develop in the owning module

Search the Library Explorer and source tree before adding a new declaration.
Prefer a small adapter or an existing theorem over a duplicate API. Put code in
the module that owns the mathematical concept and add a succinct source comment
when provenance is not obvious.

Submitted proof code must not use `sorry`, `admit`, new `axiom` declarations,
or a placeholder proposition that weakens the submitted mathematics. A proof
ingredient such as PREPARE correctness, SELECT semantics, an inverse identity,
normalization, a nonzero success branch, or resource bound is a dependency to be
proved/reused and applied inside the proof; it must not be smuggled into a sealed
source theorem as a new convenience binder. Keep
State Preparation and Block Encoding contracts distinct. A finite Qiskit,
NumPy, or QASM check is supporting evidence, not a replacement for a named Lean
certificate.

Documentation changes should preserve exact declaration names and distinguish
local declaration completion from completion of the wider construction route.

## 3. Verify the exact change

Run the focused target while developing, then run the complete gate before
requesting review.

Linux/macOS:

```bash
lake build
lake build ABEISTests
python3 tools/qbe.py check
bash scripts/build-all.sh
```

Windows PowerShell:

```powershell
lake build
lake build ABEISTests
python tools/qbe.py check
powershell -ExecutionPolicy Bypass -File scripts/build-all.ps1
```

For a documentation-only patch, the full site build is still required because
it checks declaration coverage, Blueprint references, internal links,
fragments, search counts, and source-link policy. Report any gate you could not
run instead of presenting it as passed.

## 4. Submit and receive credit

Keep the pull request focused. Its description must state:

- the mathematical result and source;
- the owning module and important API choices;
- local and broader-route status;
- the exact verification commands and results;
- executable evidence, if the contract requires it;
- the preferred contributor name and credit line.

Do not mix generated artifacts with unrelated refactors. Preserve upstream
license notices and authorship. Add `Co-authored-by` trailers when appropriate.
By submitting, you confirm that you have the right to provide the contribution
under this repository's Apache License 2.0, subject to LICENSE_SCOPE.md.

After integration, maintainers add the contributor and a precise summary of the
accepted work to `website/community/contributors.json`. QuantumComputinglib
then generates the public Contributors page from that record. Proposal,
locally checked, and integrated are separate statuses.

## Review policy

Maintainers review mathematical fidelity, hidden assumptions, module
ownership, proof trust, source attribution, compatibility, and documentation.
Large changes may be split into a foundation PR and one or more result PRs so
each proof boundary remains auditable.

## Source-faithful lessons and graph contributions

Read [the ASPBE publication protocol](docs/theorem-publication-protocol.md),
[the Proof Digestion Protocol](docs/proof-digestion-protocol.md),
[the Evidence-Routed Memory Protocol](docs/evidence-routed-memory-protocol.md), and
[the contributor packet](.agents/prompts/mathematical-contribution.md).
New or changed production modules need exact source/lesson bindings, assumption
comparisons, source-blind reconstruction, independent anti-anchored review, and
add-node/shortcut/reorganisation/bridge metadata. Local proof, full source-route
closure and experimental evidence must be kept separate. StatePreparationWiki
routes and Current Progress are generated from the canonical records, not from
manual percentages. Mobile/desktop, MathJax, theme, graph-label, source-link and
AND-tail checks are part of publication, not optional visual polish.
