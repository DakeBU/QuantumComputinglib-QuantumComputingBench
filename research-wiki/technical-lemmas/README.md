# Technical Lemma Memory

This retrieval layer stores reusable external lemmas, standard quantum
primitives, classical facts, and source-paper dependencies used by ABEIS tasks.

Every memory card should expose the same fields:

- `id`
- `source`
- `statement`
- `lean_decl`
- `lean_status`
- `used_by`
- `dependencies`
- `next_action`
- `tags`

Promoted local declarations must also appear in `registry.json`.  The registry
records the fully qualified name, source file, required imports, exact
signature, semantic layer, compatible shapes, successful and failed uses,
license/attribution, Lean version, and both local-declaration and broader-route
status.  Validate it with:

```bash
python3 tools/check_technical_lemma_registry.py
```

Allowed statuses:

- `paper-cited`
- `classic-unformalized`
- `contract-only`
- `obligation`
- `formalized`

This directory is retrieval memory.  A result closes a theorem only when the
referenced Lean declaration is build-tested for the exact statement being used.
`local_declaration_status: complete` never implies that a parent construction
or benchmark route is complete.

For block-encoding construction templates, use
`research-wiki/block-encoding-library/` first.  Technical-lemma cards should
record dependencies that a chosen construction card needs, not replace the
route selector.

## Planned source cards shared with the reader atlas

The Walsh phase supplier (`tl-walsh-diagonal-phase`) and diagonal-filter
consumer (`tl-diagonal-postselection`) are authored once as `technical_card`
objects in `website/research/atlas.json`. They have `lean_status: obligation`
and an empty `lean_decl`: they are **not** entries in the build-checked
declaration registry. The generated mechanism pages expose the same cards,
including failure modes and downloadable JSON. Retrieve them with:

```bash
python3 website/scripts/research_atlas.py context --route spw-walsh
python3 website/scripts/research_atlas.py context --route spw-diagonal
```

The packets carry pinned primary-source records, shared graph nodes and the
next acceptance step. The existing UCRY compiler, a fixed cubic diagonal
example or a Python Walsh/Gray backend does not close either source route.
