$ErrorActionPreference = 'Stop'
$taskRepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
Push-Location -LiteralPath $taskRepoRoot
try {
    .venv/Scripts/python.exe experiments/hermite-polynomial/precision/saved-stage-interpreter/replay.py --record full-v1
    if ($LASTEXITCODE -ne 0) { throw 'Full saved-stage interpreter replay failed' }
    .venv/Scripts/python.exe experiments/hermite-polynomial/precision/saved-stage-interpreter/freeze_result.py
    if ($LASTEXITCODE -ne 0) { throw 'Immutable result freeze failed' }
} finally {
    Pop-Location
}
