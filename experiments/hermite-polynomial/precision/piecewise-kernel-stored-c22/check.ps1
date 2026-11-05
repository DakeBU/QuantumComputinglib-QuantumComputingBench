param([string]$Module='RationalBlocks',[string]$Receipt='rational-v1')
$ErrorActionPreference='Stop'
$taskRepoRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
$taskPriorLeanPath=$env:LEAN_PATH
Push-Location -LiteralPath $taskRepoRoot
try {
  New-Item -ItemType Directory -Force -Path "$PSScriptRoot/.cache" | Out-Null
  $env:LEAN_PATH="$PSScriptRoot/.cache;experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/.cache;experiments/hermite-polynomial/precision/piecewise-kernel-producer/.cache;experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/.cache"
  lake env lean -o "$PSScriptRoot/.cache/$Module.olean" "experiments/hermite-polynomial/precision/piecewise-kernel-stored-c22/$Module.lean" 2>&1 | Tee-Object -FilePath "$PSScriptRoot/$Receipt.raw.log"
  $taskExit=$LASTEXITCODE
  (Get-Content -Raw -LiteralPath "$PSScriptRoot/$Receipt.raw.log").Replace($taskRepoRoot,'.') | Set-Content -Encoding utf8 -LiteralPath "$PSScriptRoot/$Receipt.public-v1.log"
  Write-Output "LEAN_EXIT=$taskExit"
  exit $taskExit
} finally { $env:LEAN_PATH=$taskPriorLeanPath; Pop-Location }
