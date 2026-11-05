# QuantumComputinglib website

QuantumComputinglib is the textbook and browsing surface for **ASPBE: Automatic State
Preparation and Block Encoding for Quantum Computing**. It is generated from
the repository's current Lean inventory; it is not a second theorem database.

## Information architecture

The desktop layout uses a persistent book navigation on the left. Mobile
readers receive the same navigation as a drawer. Stable existing URLs are
preserved, including `library/`, `blueprint/html-multi/`, and `task-builder/`.
Lean Graph and Functor Hypergraph are primary navigation entries. The
**LEAN LIBS & TEXTBOOKS** disclosure contains the library and four book maps.
Landing pages offer a small number of choices; detailed explanations and
evidence remain available through subpages and native disclosures.

| Route | Purpose |
| --- | --- |
| `/` | QuantumComputinglib overview and the two ASPBE contracts |
| `/math-2-0/` | Nine Math 2.0 contribution directions, evidence and next steps |
| `/learning/` | Book map and reading order |
| `/chapters/<slug>/` | Formula, natural-language reading, proof idea, Lean statement, and source |
| `/library/` | Exhaustive generated ASPBE declaration inventory |
| `/lean-graph/` | Generated library modules, imports and declaration ownership |
| `/functor-hypergraph/` | Curated conceptual transports with explicit conditions |
| `/quantumcomputingbench/` | Model benchmark overview |
| `/quantumcomputingbench/tasks/` | Subject hierarchy, levels and filtered task search |
| `/quantumcomputingbench/run/` | CPU smoke, evaluation, expert review and Agentic Lean workflows |
| `/quantumcomputingbench/study/` | Mathematical reading, course and expert inspection routes |
| `/implementation-map/` | Mathematical goal → declaration → source → status → missing work |
| `/ecosystem/` | Honest atlas of local, imported, and reference-only quantum Lean libraries |
| `/ide/` | LaTeX/Lean workspace and local compiler client |
| `/task-builder/` | User-facing task builder and user-owned API runner client |
| `/community/` | Contribution guide and packet contract |
| `/contributors/` | Integrated external contributions and precise public credit |
| `/organizers/` | Current authors and contributor-credit policy |
| `/blueprint/html-multi/` | Existing Verso Blueprint |

State Preparation and Block Encoding remain separate teaching tracks and have
different acceptance predicates. A prepared state may become a dependency of
a later block-encoding construction, but this does not merge their certificates.

## Generated inputs

- `QuantumBlockEncoding/**/*.lean`: authoritative declarations.
- `web/library/declarations.json`: generated declaration inventory.
- `docs/blueprint-coverage.json`: generated coverage and exclusion audit.
- `website/content.py`: reviewed chapter order, explanations, and route status.
- `website/diagrams/*.mmd`: editable diagrams.
- `website/community/contribution.schema.json`: contributor handoff contract.

All declaration counts, statuses, source lines, module pages, and search entries
are generated. The site builder fails when reviewed content names a declaration
that is absent from the inventory.

## Live formalization workspace

The static site supports formula rendering, reviewed LaTeX↔Lean mappings,
copyable case-study constructions, dependency navigation, Lean editing, packet
export, and a prefilled GitHub submission request. With the optional local
translator, the direction selector supports both user LaTeX to a Lean draft
and user Lean to copyable LaTeX. GitHub Pages does **not** execute Lean.

After building `_site`, start the loopback-only companion server:

```bash
python3 website/scripts/ide_server.py --directory _site
```

Open `http://127.0.0.1:8000/ide/`. The server invokes
`lake env lean` on temporary files, serializes compiler requests, applies size
and time limits, removes temporary snippets, and never writes project source.
Do not expose this compiler endpoint through a public tunnel.

An optional local AI translator can be connected without baking a provider or
credential into QuantumComputinglib:

```bash
python3 website/scripts/ide_server.py \
  --directory _site \
  --translator-command "python3 website/scripts/codex_translator.py"
```

The adapter uses the locally authenticated Codex CLI in an ephemeral,
read-only session. It follows the current Codex configuration by default. Set
`ASPBE_CODEX_MODEL` only when a particular available model is required; no
model name or credential is stored in the website.

The adapter reads one JSON request on stdin and returns JSON with string fields
`code`, `latex`, and `plain`. Its output is labeled **agent draft**. It must still compile
and receive mathematical review. Without an adapter, the workspace offers an
explicit `True` scaffold that is labeled as a placeholder, never as a semantic
translation.

## User-owned API runner

The left navigation exposes **Run with your API**. To make its execution button
active on a local checkout, start the companion with the bundled bridge:

```bash
python3 website/scripts/ide_server.py \
  --directory _site \
  --runner-command "python3 website/scripts/qbe_task_runner.py --execute --cycles 1"
```

Open `http://127.0.0.1:8000/task-builder/`. The client sends a versioned task,
agent profile, and packet to `/api/run-task`. A supplied API key travels in the
Authorization header and is exposed to the selected child process only through
the provider-specific environment variable. It is not included in server logs
or written by the bridge. The bridge itself may create normal ASPBE task,
profile, run, and report artifacts.

Static GitHub Pages cannot run the harness. It can either generate/download the
packet or call a user-owned HTTPS endpoint that implements the same response
contract: `{ "ok": true, "output": "...", "dashboard": { ... } }`.

## Contribution boundary

The browser exports one versioned lemma packet containing:

- plain-language and LaTeX statements;
- imports, Lean code, proposed name, and dependencies;
- source provenance and contributor credit;
- compiler diagnostics tied to the exact editor text;
- license consent state.

The GitHub button opens a review request; it does not write to the repository or
mark a result integrated. Only maintainers assign `integrated` after the exact
declaration enters the inventory and passes the full ASPBE gate.

The complete route is documented in [`CONTRIBUTING.md`](../CONTRIBUTING.md):
scope, development in the owning module, whole-repository verification, and a
focused pull request. Accepted work is added to
`website/community/contributors.json`; the generated Contributors page never
lists an open proposal or a local draft as integrated.

## Build

Linux/macOS:

```bash
bash scripts/build-all.sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build-all.ps1
```

Website-only assembly requires a current `_out/lean-gate.json` and Blueprint:

```bash
bash scripts/build-website.sh
```

The final artifact is `_site/`. `website/scripts/check_site.py` checks required
routes, search counts, internal links, fragments, MathJax/Mermaid markers,
responsive/theme markers, and local-path leakage. Source links use a commit SHA
only when that source exists at a published ref and is clean in the checkout.

For a password-protected static preview, use `serve_preview.py`; credentials
come only from `ASPBE_PREVIEW_USERNAME` and `ASPBE_PREVIEW_PASSWORD` (the old
`ABEIS_PREVIEW_*` names remain accepted for compatibility). A
TryCloudflare URL is temporary preview infrastructure, not production hosting.

## Mathematical prose

Write inline formulas as `\(...\)` or `$...$`; reserve `\[...\]` and
`$$...$$` for displayed equations. Keep an entire equation inside one pair
of delimiters. Use code/preformatted blocks only for actual source, commands,
and deliberate copyable TeX. The reader also recovers complete explicitly
delimited formulas from legacy inline-code wrappers, without processing Lean
code, source downloads or editable text areas.

`math-reader.js` configures the shared MathJax startup and typesets newly added
mathematical prose. The engine, TeX extensions and fonts are pinned to MathJax
3.2.2 under `static/vendor/` and are published with the site; formula rendering
does not require a third-party CDN. Preserve that directory when copying assets.

After building, run `python website/scripts/test_math_browser.py --root SITE`.
This Playwright gate blocks external network access, compiles all unique
formulas, visits desktop/mobile reader pages, and checks delayed loading,
inline formulas, live insertion and preservation of code/editor contents.
