#!/usr/bin/env bash

set -euo pipefail

test -f _out/lean-gate.json
test -f _out/blueprint/html-multi/index.html

# The declaration inventory is generated from the exact current Lean checkout.
# This keeps the Library Explorer, Blueprint, and Underlying Lean Graph aligned
# with newly admitted proof modules instead of relying on a stale JSON snapshot.
python3 scripts/generate-aspbe-catalog.py
python3 scripts/generate-aspbe-catalog.py --check

# Research views and publication packets use the same source-of-truth inventory.
python3 website/scripts/research_atlas.py check
python3 -m unittest website.scripts.test_research_atlas
python3 -m unittest website.scripts.test_uncompute_intake
publication_base="${ASPBE_PUBLICATION_BASE:-origin/main}"
if [[ "${CI:-}" == "true" && "${GITHUB_REF:-}" == "refs/heads/main" ]]; then
  publication_base="HEAD^1"
fi
python3 website/scripts/check_research_publications.py --base "$publication_base"

python3 -m py_compile \
  website/scripts/build_site.py \
  website/scripts/sidebar_navigation.py \
  website/scripts/lean_graph.py \
  website/scripts/enrich_teaching_site.py \
  website/scripts/enrich_casebook.py \
  website/scripts/enrich_hermite_insight.py \
  website/scripts/enforce_robin_reader_contract.py \
  website/scripts/polish_casebook.py \
  website/scripts/enrich_harness_page.py \
  website/scripts/publish_extensions.py \
  website/scripts/publish_paper_pages.py \
  website/scripts/publish_taxonomy.py \
  website/scripts/finalize_taxonomy_navigation.py \
  website/scripts/repair_taxonomy_links.py \
  website/scripts/check_site.py \
  website/scripts/ide_server.py \
  website/scripts/qbe_task_runner.py \
  website/scripts/test_site_contracts.py \
  website/scripts/test_teaching_enrichment.py \
  website/scripts/test_casebook_enrichment.py \
  website/scripts/test_casebook_polish.py \
  website/scripts/test_hermite_insight.py \
  tools/export_robin_evolution.py \
  tools/replay_public_cases.py

python3 -m unittest \
  website.scripts.test_hermite_case \
  website.scripts.test_hermite_download_packet \
  website.scripts.test_hermite_insight \
  website.scripts.test_proof_inputs \
  website.scripts.test_lean_publication_gate \
  website.scripts.test_deployed_research \
  website.scripts.test_site_contracts \
  website.scripts.test_sidebar_navigation \
  website.scripts.test_quantumcomputingbench \
  website.scripts.test_qcb_diagnostics \
  website.scripts.test_qcb_math \
  website.scripts.test_qcb_expert \
  website.scripts.test_qcb_publication_contract \
  website.scripts.test_qcb_hierarchy \
  website.scripts.test_qcb_nonlean_workbook \
  website.scripts.test_teaching_enrichment \
  website.scripts.test_casebook_enrichment \
  website.scripts.test_casebook_polish

python3 website/scripts/publish_taxonomy.py --check-data

python3 website/scripts/build_site.py \
  --lean-gate-report _out/lean-gate.json \
  --output _out/site

python3 website/scripts/enrich_harness_page.py --root _out/site
python3 website/scripts/enrich_teaching_site.py --root _out/site
python3 website/scripts/enrich_casebook.py --root _out/site
python3 website/scripts/polish_casebook.py --root _out/site
python3 website/scripts/enforce_robin_reader_contract.py --root _out/site
python3 website/scripts/publish_extensions.py --root _out/site
python3 website/scripts/publish_paper_pages.py --root _out/site
python3 website/scripts/publish_taxonomy.py --root _out/site
python3 website/scripts/finalize_taxonomy_navigation.py --root _out/site
python3 website/scripts/repair_taxonomy_links.py --root _out/site
# Run after extension/taxonomy publication so the Hermite teaching layer and its
# graph lens cannot be overwritten by a later generic renderer.
python3 website/scripts/enrich_hermite_insight.py --root _out/site
python3 website/scripts/research_atlas.py publish --root _out/site
python3 website/scripts/quantumcomputingbench.py publish --root _out/site

rm -rf _site
mkdir -p _site/blueprint
cp -a _out/site/. _site/
cp -a _out/blueprint/. _site/blueprint/
touch _site/.nojekyll

python3 website/scripts/check_site.py --root _site --require-blueprint
python3 website/scripts/research_atlas.py check-site --root _site
python3 website/scripts/quantumcomputingbench.py check-site --root _site
if [[ "${CI:-}" == "true" ]]; then
  python3 -m pip install --quiet playwright
  python3 -m playwright install --with-deps chromium
  python3 website/scripts/test_research_browser.py --root _site --require-blueprint
  python3 website/scripts/test_math_browser.py --root _site --report _out/research-browser/math-browser-report.json
  python3 website/scripts/test_quantumcomputingbench_browser.py --root _site
  cp _out/qcb-browser/browser-report.json _site/data/quantumcomputingbench/browser-report.json
  cp _out/research-browser/browser-report.json _site/data/research/browser-report.json
fi
python3 website/scripts/check_source_links.py --root _site
python3 website/scripts/test_preview.py
python3 scripts/sanitize-blueprint-paths.py --scan-only _site

test -f _site/index.html
test -f _site/library/index.html
test -f _site/blueprint/html-multi/index.html
test -f _site/search-index.json
test -f _site/example-cases/index.html
test -f _site/example-cases/state-preparation/index.html
test -f _site/example-cases/block-encoding/index.html
test -f _site/example-cases/hermite-smooth-state-preparation/index.html
test -f _site/papers/index.html
test -f _site/papers/state-preparation/index.html
test -f _site/papers/block-encoding/index.html
test -f _site/papers/ghl2025-robin/index.html
test -f _site/papers/mottonen-2005-state-preparation/index.html
test -f _site/papers/grover-rudolph-2002/index.html
test -f _site/papers/li-luo-sparse-state-2025/index.html
test -f _site/papers/low-kliuchnikov-schaeffer-2018/index.html
test -f _site/data/example-cases.json
test -f _site/data/papers.json
test -f _site/data/case-source-anchors.json
test -f _site/static/learning.css
test -f _site/static/casebook.css
test -f _site/static/hermite-insight.css
test -f _site/static/ASPBE.png
test -f _site/static/aspbe_current_harness.webp

grep -q 'id="start-here"' _site/learning/index.html
grep -q 'id="quantum-access-models"' _site/learning/index.html
grep -q 'Digital query oracle' _site/learning/index.html
grep -q 'How to read a quantum circuit' _site/learning/index.html
grep -q 'data-reader-mode-choice="concept"' _site/chapters/block-encoding/index.html
grep -q 'data-reader-mode-choice="lean"' _site/chapters/state-preparation/index.html

grep -q 'State Preparation' _site/example-cases/index.html
grep -q 'Block Encoding' _site/example-cases/index.html
grep -q 'State Preparation' _site/papers/index.html
grep -q 'Block Encoding' _site/papers/index.html
grep -q 'data-taxonomy-nav="example-cases"' _site/index.html
! grep -q 'data-topic-links=' _site/index.html
grep -q 'data-paper="ghl2025-robin" data-topic="block-encoding"' _site/index.html

grep -q 'Source anchor.' _site/example-cases/bell-state-preparation/index.html
grep -q 'Möttönen et al. Eq. (1) + Sec. III' _site/example-cases/bell-state-preparation/index.html
grep -q 'Eq. (6)' _site/example-cases/mottonen-dense-state-preparation/index.html
grep -q 'Fig. 3' _site/example-cases/mottonen-dense-state-preparation/index.html
grep -q 'Grover' _site/example-cases/grover-rudolph-product-state-preparation/index.html
grep -q 'Eq. (1), (3), (6)' _site/example-cases/grover-rudolph-product-state-preparation/index.html
grep -q 'Li' _site/example-cases/sparse-three-state-preparation/index.html
grep -q 'Eq. (1)' _site/example-cases/sparse-three-state-preparation/index.html
grep -q 'Eq. (2)' _site/example-cases/sparse-three-state-preparation/index.html

grep -q 'Eq. (6)' _site/papers/mottonen-2005-state-preparation/index.html
grep -q 'Fig. 3' _site/papers/mottonen-2005-state-preparation/index.html
grep -q 'Eq. (5)' _site/papers/grover-rudolph-2002/index.html
grep -q 'Theorem 1' _site/papers/li-luo-sparse-state-2025/index.html
grep -q 'Table 2' _site/papers/low-kliuchnikov-schaeffer-2018/index.html
grep -q 'Paper reproduction boundary' _site/papers/mottonen-2005-state-preparation/index.html
grep -q 'Paper reproduction boundary' _site/papers/grover-rudolph-2002/index.html
grep -q 'Paper reproduction boundary' _site/papers/li-luo-sparse-state-2025/index.html
grep -q 'Paper reproduction boundary' _site/papers/low-kliuchnikov-schaeffer-2018/index.html

grep -q 'id="case-tutorial"' _site/example-cases/robin-ghl-one-term/index.html
grep -q 'GHL Eq. (9)' _site/example-cases/robin-ghl-one-term/index.html
grep -q 'GHL Theorem 3' _site/example-cases/robin-ghl-one-term/index.html
grep -q 'GHL Theorem 4' _site/example-cases/robin-ghl-one-term/index.html
grep -q 'id="paper-lean-alignment"' _site/example-cases/robin-ghl-one-term/index.html
grep -q 'id="source-assumption-translation"' _site/example-cases/robin-ghl-one-term/index.html
grep -q 'Paper assumption / source issue.' _site/example-cases/robin-ghl-one-term/index.html
grep -q 'Plain language.' _site/example-cases/robin-ghl-one-term/index.html
grep -q 'Why it matters.' _site/example-cases/robin-ghl-one-term/index.html
grep -q 'What ASPBE improves' _site/example-cases/robin-ghl-one-term/index.html
grep -q '106,96,3,0' website/case-teaching.json
grep -q '312,266,5,0' website/case-teaching.json
grep -q '881,674,6,0' website/case-teaching.json
grep -q 'Advanced source-fidelity notes' _site/example-cases/robin-ghl-one-term/index.html
grep -q 'data-collapsed-section="verification-status"' _site/example-cases/robin-ghl-one-term/index.html
grep -q 'data-collapsed-section="lean-certificate"' _site/example-cases/robin-ghl-one-term/index.html
grep -q 'data-collapsed-section="correspondence"' _site/case-studies/robin/index.html
! grep -q '<h2>Source interpretation decisions</h2>' _site/example-cases/robin-ghl-one-term/index.html

# Hermite presentation is a fail-closed publication surface: the reader must see
# the structural compression argument in math environments, not raw ASCII math.
grep -q 'id="hermite-insight"' _site/example-cases/hermite-smooth-state-preparation/index.html
grep -Fq '48\,n_p(2k+6)^3' _site/example-cases/hermite-smooth-state-preparation/index.html
grep -q 'Mathematical cross-pollination' _site/example-cases/hermite-smooth-state-preparation/index.html
! grep -Fq 'The new Bernstein–MPS circuit has at most 48 n_p (2k+6)^3 Ry/CNOT' _site/example-cases/hermite-smooth-state-preparation/index.html

test -f _site/lean-graph/index.html
test -f _site/data/lean-graph.json
test -f _site/static/lean-graph.js
test -f _site/static/lean-graph.css
grep -q 'Underlying Lean Graph of Libraries' _site/lean-graph/index.html
grep -q 'SemanticFidelity' _site/lean-graph/index.html
grep -q 'Underlying Lean Graph of Libraries' _site/case-studies/robin/index.html
grep -Fq '\(N=8\)' _site/case-studies/robin/index.html
grep -Fq '\(A_k/(\mathcal N_D\mathcal N_f\kappa)\)' _site/case-studies/robin/index.html
! grep -Fq 'A_k/(N_D N_f kappa)' _site/case-studies/robin/index.html
grep -q 'id="hermite-topology"' _site/lean-graph/index.html
grep -q '>BRIDGE<' _site/lean-graph/index.html
grep -q '>SHORTCUT<' _site/lean-graph/index.html
grep -q '>HUB<' _site/lean-graph/index.html
grep -q '>REORGANIZATION<' _site/lean-graph/index.html
grep -q 'compression corridor' _site/lean-graph/index.html
grep -q 'theorem-level proof-term dependency' _site/lean-graph/index.html

python3 - <<'PY'
import json
from pathlib import Path

payload = json.loads(Path('_site/data/lean-graph.json').read_text(encoding='utf-8'))
nodes = {node['id']: node for node in payload['nodes']}
edges = {(edge['source'], edge['target'], edge['type']) for edge in payload['edges']}
module_name = 'QuantumBlockEncoding.SemanticFidelityEvidence'
module_id = f'module:{module_name}'
assert module_id in nodes, 'semantic-fidelity module missing from published Lean Graph'
assert nodes[module_id]['track'] == 'system-evidence', nodes[module_id]
required_leaves = {
    'QuantumBlockEncoding.SemanticFidelity.verifiedOperatorBlockEncodingRoundTrip',
    'QuantumBlockEncoding.SemanticFidelity.approximateBlockEncodingNormRoundTrip',
    'QuantumBlockEncoding.SemanticFidelity.verifiedStatePreparationRoundTrip',
    'QuantumBlockEncoding.SemanticFidelity.oneTermRobinClaimRoundTrip',
    'QuantumBlockEncoding.SemanticFidelity.candidateImprovementRoundTrip',
    'QuantumBlockEncoding.SemanticFidelity.semanticRoundTripRegistry',
}
for full_name in required_leaves:
    declaration_id = f'declaration:{full_name}'
    assert declaration_id in nodes, f'missing semantic-fidelity graph leaf: {full_name}'
    assert (module_id, declaration_id, 'module-declares-leaf') in edges
for dependency in (
    'QuantumBlockEncoding.BlockEncoding',
    'QuantumBlockEncoding.StatePreparation',
    'QuantumBlockEncoding.GHL2025',
):
    assert (
        f'module:{dependency}', module_id, 'module-supports-importer'
    ) in edges, f'missing audited-module graph edge: {dependency}'
print('semantic-fidelity Lean Graph publication contract passed')
PY

grep -q 'id="harness-evolution"' _site/workflow/index.html
grep -q 'Previous Harness' _site/workflow/index.html
grep -q 'Current Harness' _site/workflow/index.html
grep -q 'Upper strategist' _site/workflow/index.html
grep -q 'Frontier Master' _site/workflow/index.html

test -f _site/.nojekyll

echo "QuantumComputinglib assembled at _site/index.html"
