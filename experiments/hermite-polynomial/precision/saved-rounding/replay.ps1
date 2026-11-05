$ErrorActionPreference = 'Stop'
$taskRepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
Push-Location -LiteralPath $taskRepoRoot
try {
    .venv/Scripts/python.exe experiments/hermite-polynomial/precision/saved-rounding/replay.py
    if ($LASTEXITCODE -ne 0) { throw 'Saved rounding focused replay failed' }
} finally {
    Pop-Location
}
