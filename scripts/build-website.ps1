param(
  [string]$PythonCommand = "python"
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

function Assert-RepositoryOutput([string]$RelativePath) {
  if ($RelativePath -notin @("_site", "_out/site", "_out/blueprint")) {
    throw "Not a designated website output"
  }
  $resolvedRepo = [IO.Path]::GetFullPath($repoRoot).TrimEnd([IO.Path]::DirectorySeparatorChar)
  $resolvedOutput = [IO.Path]::GetFullPath((Join-Path $resolvedRepo $RelativePath))
  if (-not $resolvedOutput.StartsWith($resolvedRepo + [IO.Path]::DirectorySeparatorChar,
      [StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing a website output outside the repository"
  }
  $ancestors = @($resolvedRepo)
  if ($RelativePath.StartsWith("_out/")) { $ancestors += Join-Path $resolvedRepo "_out" }
  $ancestors += $resolvedOutput
  foreach ($ancestor in $ancestors) {
    $item = $null
    try { $item = Get-Item -LiteralPath $ancestor -Force -ErrorAction Stop }
    catch [Management.Automation.ItemNotFoundException] { }
    if ($null -ne $item) {
      if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0 -or -not $item.PSIsContainer) {
        throw "Website output ancestry must contain ordinary directories only"
      }
    }
  }
  if (Test-Path -LiteralPath $resolvedOutput) {
    $pending = [Collections.Generic.Stack[string]]::new()
    $pending.Push($resolvedOutput)
    while ($pending.Count -gt 0) {
      foreach ($item in Get-ChildItem -LiteralPath ($pending.Pop()) -Force) {
        if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
          throw "Refusing to traverse a reparse point in website outputs"
        }
        if ($item.PSIsContainer) { $pending.Push($item.FullName) }
      }
    }
  }
  return $resolvedOutput
}

function Assert-NonemptyFile([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path -PathType Leaf) -or (Get-Item -LiteralPath $Path).Length -eq 0) {
    throw "Required nonempty website file is missing: $Path"
  }
}

function Assert-PageMarker([string]$Path, [string]$Marker, [bool]$Absent = $false) {
  Assert-NonemptyFile $Path
  $content = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
  if ($content.Contains($Marker) -eq $Absent) {
    throw "Website publication marker check failed: $Path : $Marker"
  }
}

[void](Assert-RepositoryOutput "_out/site")
[void](Assert-RepositoryOutput "_out/blueprint")
[void](Assert-RepositoryOutput "_site")
foreach ($required in @(
  "_out/lean-gate.json",
  "_out/blueprint/html-multi/index.html"
)) {
  Assert-NonemptyFile $required
}

& $PythonCommand tools/check_hermite_artifacts.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand scripts/generate-aspbe-catalog.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand scripts/generate-aspbe-catalog.py --check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# Research views and publication packets use the same source-of-truth inventory.
& $PythonCommand website/scripts/research_atlas.py check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand -m unittest website.scripts.test_research_atlas
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand -m unittest website.scripts.test_uncompute_intake
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$publication_base = if ($env:ASPBE_PUBLICATION_BASE) { $env:ASPBE_PUBLICATION_BASE } else { "origin/main" }
if ($env:CI -eq "true" -and $env:GITHUB_REF -eq "refs/heads/main") { $publication_base = "HEAD^1" }
& $PythonCommand website/scripts/check_research_publications.py --base $publication_base
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $PythonCommand -m `
  py_compile `
  website/scripts/build_site.py `
  website/scripts/sidebar_navigation.py `
  website/scripts/lean_graph.py `
  website/scripts/enrich_teaching_site.py `
  website/scripts/enrich_casebook.py `
  website/scripts/enrich_hermite_insight.py `
  website/scripts/enforce_robin_reader_contract.py `
  website/scripts/polish_casebook.py `
  website/scripts/enrich_harness_page.py `
  website/scripts/publish_extensions.py `
  website/scripts/publish_paper_pages.py `
  website/scripts/publish_taxonomy.py `
  website/scripts/finalize_taxonomy_navigation.py `
  website/scripts/repair_taxonomy_links.py `
  website/scripts/check_site.py `
  website/scripts/ide_server.py `
  website/scripts/qbe_task_runner.py `
  website/scripts/test_site_contracts.py `
  website/scripts/test_teaching_enrichment.py `
  website/scripts/test_casebook_enrichment.py `
  website/scripts/test_casebook_polish.py `
  website/scripts/test_hermite_insight.py `
  tools/export_robin_evolution.py `
  tools/replay_public_cases.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $PythonCommand -m `
  unittest `
  website.scripts.test_hermite_case `
  website.scripts.test_hermite_download_packet `
  website.scripts.test_hermite_insight `
  website.scripts.test_proof_inputs `
  website.scripts.test_lean_publication_gate `
  website.scripts.test_deployed_research `
  website.scripts.test_site_contracts `
  website.scripts.test_sidebar_navigation `
  website.scripts.test_quantumcomputingbench `
  website.scripts.test_qcb_diagnostics `
  website.scripts.test_qcb_math `
  website.scripts.test_qcb_expert `
  website.scripts.test_qcb_publication_contract `
  website.scripts.test_qcb_hierarchy `
  website.scripts.test_qcb_nonlean_workbook `
  website.scripts.test_teaching_enrichment `
  website.scripts.test_casebook_enrichment `
  website.scripts.test_casebook_polish
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/publish_taxonomy.py --check-data
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $PythonCommand website/scripts/build_site.py `
  --lean-gate-report _out/lean-gate.json `
  --output _out/site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $PythonCommand website/scripts/enrich_harness_page.py --root _out/site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/enrich_teaching_site.py --root _out/site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/enrich_casebook.py --root _out/site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/polish_casebook.py --root _out/site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/enforce_robin_reader_contract.py --root _out/site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/publish_extensions.py --root _out/site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/publish_paper_pages.py --root _out/site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/publish_taxonomy.py --root _out/site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/finalize_taxonomy_navigation.py --root _out/site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/repair_taxonomy_links.py --root _out/site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/enrich_hermite_insight.py --root _out/site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/research_atlas.py publish --root _out/site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/quantumcomputingbench.py publish --root _out/site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$site = Assert-RepositoryOutput "_site"
[void](Assert-RepositoryOutput "_out/site")
[void](Assert-RepositoryOutput "_out/blueprint")
if (Test-Path -LiteralPath $site) {
  Remove-Item -LiteralPath $site -Recurse -Force
}
New-Item -ItemType Directory -Path (Join-Path $site "blueprint") -Force | Out-Null
foreach ($item in Get-ChildItem -LiteralPath "_out/site" -Force) {
  Copy-Item -LiteralPath $item.FullName -Destination $site -Recurse -Force
}
foreach ($item in Get-ChildItem -LiteralPath "_out/blueprint" -Force) {
  Copy-Item -LiteralPath $item.FullName -Destination (Join-Path $site "blueprint") -Recurse -Force
}
New-Item -ItemType File -Path (Join-Path $site ".nojekyll") -Force | Out-Null

& $PythonCommand website/scripts/check_site.py --root _site --require-blueprint
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/research_atlas.py check-site --root _site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/quantumcomputingbench.py check-site --root _site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
if ($env:CI -eq "true") {
  & $PythonCommand -m pip install --quiet playwright
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  & $PythonCommand -m playwright install chromium
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  & $PythonCommand website/scripts/test_research_browser.py --root _site --require-blueprint
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  & $PythonCommand website/scripts/test_quantumcomputingbench_browser.py --root _site
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  Copy-Item _out/qcb-browser/browser-report.json _site/data/quantumcomputingbench/browser-report.json
  Copy-Item _out/research-browser/browser-report.json _site/data/research/browser-report.json
}
& $PythonCommand website/scripts/check_source_links.py --root _site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/test_preview.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand scripts/sanitize-blueprint-paths.py --scan-only _site
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

foreach ($path in @(
  "_site/index.html", "_site/library/index.html", "_site/blueprint/html-multi/index.html",
  "_site/search-index.json", "_site/example-cases/index.html",
  "_site/example-cases/state-preparation/index.html", "_site/example-cases/block-encoding/index.html",
  "_site/papers/index.html", "_site/papers/state-preparation/index.html",
  "_site/papers/block-encoding/index.html", "_site/papers/ghl2025-robin/index.html",
  "_site/papers/mottonen-2005-state-preparation/index.html",
  "_site/papers/grover-rudolph-2002/index.html", "_site/papers/li-luo-sparse-state-2025/index.html",
  "_site/papers/low-kliuchnikov-schaeffer-2018/index.html", "_site/data/example-cases.json",
  "_site/data/papers.json", "_site/data/case-source-anchors.json", "_site/static/learning.css",
  "_site/static/casebook.css", "_site/static/ASPBE.png", "_site/static/aspbe_current_harness.webp",
  "_site/lean-graph/index.html", "_site/data/lean-graph.json",
  "_site/static/lean-graph.js", "_site/static/lean-graph.css",
  "_site/example-cases/hermite-smooth-state-preparation/index.html",
  "_site/build-report.json"
)) { Assert-NonemptyFile $path }

# Native equivalents of the canonical shell teaching/publication assertions.
Assert-PageMarker "_site/learning/index.html" 'id="start-here"'
Assert-PageMarker "_site/learning/index.html" 'id="quantum-access-models"'
Assert-PageMarker "_site/learning/index.html" 'Digital query oracle'
Assert-PageMarker "_site/learning/index.html" 'How to read a quantum circuit'
Assert-PageMarker "_site/chapters/block-encoding/index.html" 'data-reader-mode-choice="concept"'
Assert-PageMarker "_site/chapters/state-preparation/index.html" 'data-reader-mode-choice="lean"'
Assert-PageMarker "_site/example-cases/index.html" 'State Preparation'
Assert-PageMarker "_site/example-cases/index.html" 'Block Encoding'
Assert-PageMarker "_site/papers/index.html" 'State Preparation'
Assert-PageMarker "_site/papers/index.html" 'Block Encoding'
Assert-PageMarker "_site/index.html" 'data-taxonomy-nav="example-cases"'
Assert-PageMarker "_site/index.html" 'data-topic-links=' $true
Assert-PageMarker "_site/index.html" 'data-paper="ghl2025-robin" data-topic="block-encoding"'
Assert-PageMarker "_site/example-cases/bell-state-preparation/index.html" 'Source anchor.'
Assert-PageMarker "_site/example-cases/bell-state-preparation/index.html" ('M{0}tt{0}nen et al. Eq. (1) + Sec. III' -f [char]0x00F6)
Assert-PageMarker "_site/example-cases/mottonen-dense-state-preparation/index.html" 'Eq. (6)'
Assert-PageMarker "_site/example-cases/mottonen-dense-state-preparation/index.html" 'Fig. 3'
Assert-PageMarker "_site/example-cases/grover-rudolph-product-state-preparation/index.html" 'Grover'
Assert-PageMarker "_site/example-cases/grover-rudolph-product-state-preparation/index.html" 'Eq. (1), (3), (6)'
Assert-PageMarker "_site/example-cases/sparse-three-state-preparation/index.html" 'Li'
Assert-PageMarker "_site/example-cases/sparse-three-state-preparation/index.html" 'Eq. (1)'
Assert-PageMarker "_site/example-cases/sparse-three-state-preparation/index.html" 'Eq. (2)'
Assert-PageMarker "_site/papers/mottonen-2005-state-preparation/index.html" 'Eq. (6)'
Assert-PageMarker "_site/papers/mottonen-2005-state-preparation/index.html" 'Fig. 3'
Assert-PageMarker "_site/papers/grover-rudolph-2002/index.html" 'Eq. (5)'
Assert-PageMarker "_site/papers/li-luo-sparse-state-2025/index.html" 'Theorem 1'
Assert-PageMarker "_site/papers/low-kliuchnikov-schaeffer-2018/index.html" 'Table 2'
foreach ($paper in @("mottonen-2005-state-preparation", "grover-rudolph-2002", "li-luo-sparse-state-2025", "low-kliuchnikov-schaeffer-2018")) {
  Assert-PageMarker "_site/papers/$paper/index.html" 'Paper reproduction boundary'
}
foreach ($marker in @('id="case-tutorial"', 'GHL Eq. (9)', 'GHL Theorem 3', 'GHL Theorem 4',
    'id="paper-lean-alignment"', 'id="source-assumption-translation"',
    'Paper assumption / source issue.', 'Plain language.', 'Why it matters.', 'What ASPBE improves',
    'Advanced source-fidelity notes', 'data-collapsed-section="verification-status"',
    'data-collapsed-section="lean-certificate"')) {
  Assert-PageMarker "_site/example-cases/robin-ghl-one-term/index.html" $marker
}
foreach ($tuple in @('106,96,3,0', '312,266,5,0', '881,674,6,0')) {
  Assert-PageMarker "website/case-teaching.json" $tuple
}
Assert-PageMarker "_site/case-studies/robin/index.html" 'data-collapsed-section="correspondence"'
Assert-PageMarker "_site/example-cases/robin-ghl-one-term/index.html" '<h2>Source interpretation decisions</h2>' $true
Assert-PageMarker "_site/lean-graph/index.html" 'Underlying Lean Graph of Libraries'
Assert-PageMarker "_site/lean-graph/index.html" 'SemanticFidelity'
Assert-PageMarker "_site/case-studies/robin/index.html" 'Underlying Lean Graph of Libraries'
Assert-PageMarker "_site/case-studies/robin/index.html" '\(N=8\)'
Assert-PageMarker "_site/case-studies/robin/index.html" '\(A_k/(\mathcal N_D\mathcal N_f\kappa)\)'
Assert-PageMarker "_site/case-studies/robin/index.html" 'A_k/(N_D N_f kappa)' $true

# Preserve every canonical final-output assertion.
Assert-NonemptyFile "_site/static/hermite-insight.css"
Assert-PageMarker "_site/example-cases/hermite-smooth-state-preparation/index.html" 'id="hermite-insight"'
Assert-PageMarker "_site/example-cases/hermite-smooth-state-preparation/index.html" '48\,n_p(2k+6)^3'
Assert-PageMarker "_site/example-cases/hermite-smooth-state-preparation/index.html" 'Mathematical cross-pollination'
Assert-PageMarker "_site/example-cases/hermite-smooth-state-preparation/index.html" 'The new Bernstein–MPS circuit has at most 48 n_p (2k+6)^3 Ry/CNOT' $true
Assert-PageMarker "_site/lean-graph/index.html" 'id="hermite-topology"'
Assert-PageMarker "_site/lean-graph/index.html" '>BRIDGE<'
Assert-PageMarker "_site/lean-graph/index.html" '>SHORTCUT<'
Assert-PageMarker "_site/lean-graph/index.html" '>HUB<'
Assert-PageMarker "_site/lean-graph/index.html" '>REORGANIZATION<'
Assert-PageMarker "_site/lean-graph/index.html" 'compression corridor'
Assert-PageMarker "_site/lean-graph/index.html" 'theorem-level proof-term dependency'

$graph = Get-Content -LiteralPath "_site/data/lean-graph.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$nodes = @{}
foreach ($node in $graph.nodes) { $nodes[$node.id] = $node }
$edges = [Collections.Generic.HashSet[string]]::new()
foreach ($edge in $graph.edges) { [void]$edges.Add("$($edge.source)|$($edge.target)|$($edge.type)") }
$moduleId = "module:QuantumBlockEncoding.SemanticFidelityEvidence"
if (-not $nodes.ContainsKey($moduleId) -or $nodes[$moduleId].track -ne "system-evidence") {
  throw "Semantic-fidelity module missing or incorrectly classified in Lean Graph"
}
foreach ($leaf in @(
  "QuantumBlockEncoding.SemanticFidelity.verifiedOperatorBlockEncodingRoundTrip",
  "QuantumBlockEncoding.SemanticFidelity.approximateBlockEncodingNormRoundTrip",
  "QuantumBlockEncoding.SemanticFidelity.verifiedStatePreparationRoundTrip",
  "QuantumBlockEncoding.SemanticFidelity.oneTermRobinClaimRoundTrip",
  "QuantumBlockEncoding.SemanticFidelity.candidateImprovementRoundTrip",
  "QuantumBlockEncoding.SemanticFidelity.semanticRoundTripRegistry"
)) {
  $declarationId = "declaration:$leaf"
  if (-not $nodes.ContainsKey($declarationId) -or -not $edges.Contains("$moduleId|$declarationId|module-declares-leaf")) {
    throw "Missing semantic-fidelity Lean Graph declaration or edge: $leaf"
  }
}
foreach ($dependency in @("QuantumBlockEncoding.BlockEncoding", "QuantumBlockEncoding.StatePreparation", "QuantumBlockEncoding.GHL2025")) {
  if (-not $edges.Contains("module:$dependency|$moduleId|module-supports-importer")) {
    throw "Missing audited-module Lean Graph dependency: $dependency"
  }
}
foreach ($marker in @('id="harness-evolution"', 'Previous Harness', 'Current Harness', 'Upper strategist', 'Frontier Master')) {
  Assert-PageMarker "_site/workflow/index.html" $marker
}
if (-not (Test-Path -LiteralPath "_site/.nojekyll" -PathType Leaf)) {
  throw "Pages .nojekyll marker missing"
}

Write-Host "QuantumComputinglib assembled at _site/index.html"
