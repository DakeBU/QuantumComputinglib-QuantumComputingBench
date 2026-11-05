param(
  [string]$PythonCommand = "python",
  [string]$LakeCommand = "lake",
  [string[]]$LakeArguments = @()
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

if ($env:QBE_AGENT_INNER_CYCLE -eq "1") {
  [Console]::Error.WriteLine("build-all is disabled inside an ASPBE agent cycle; use the controller gate")
  exit 64
}

& $PythonCommand -m unittest tools.test_hermite_artifacts tools.test_technical_lemma_registry tools.test_verso_windows_compat tools.test_powershell_builds website.scripts.test_proof_inputs website.scripts.test_hermite_case website.scripts.test_lean_publication_gate
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand tools/check_hermite_artifacts.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand tools/qbe.py harness-check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand tools/check_process_memory.py check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand tools/check_public_figure_style.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand tools/test_proof_trust.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand tools/check_proof_trust.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand tools/check_technical_lemma_registry.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand -m unittest website.scripts.test_site_contracts tools.test_case_memory tools.test_robin_export tools.test_replay_public_cases
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand website/scripts/run_lean_gate.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand executable-exports/SP-HERMITE-001/qiskit/export.py --self-test
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand executable-exports/SP-HERMITE-001/qiskit/replay.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand tools/replay_public_cases.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand tools/export_robin_evolution.py --task QBE-ROBIN-BE-WARM-001 --arm warm
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand -m unittest tools.test_blueprint_catalog
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand scripts/generate-aspbe-catalog.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand scripts/generate-aspbe-catalog.py --check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $PythonCommand scripts/test-sanitize-blueprint-paths.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& scripts/build-blueprint.ps1 `
  -PythonCommand $PythonCommand `
  -LakeCommand $LakeCommand `
  -LakeArguments $LakeArguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& scripts/build-website.ps1 -PythonCommand $PythonCommand
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
