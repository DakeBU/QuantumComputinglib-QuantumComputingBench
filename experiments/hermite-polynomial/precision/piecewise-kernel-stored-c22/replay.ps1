$ErrorActionPreference='Stop'
$taskRepoRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
$taskPriorLeanPath=$env:LEAN_PATH
Push-Location -LiteralPath $taskRepoRoot
try {
  New-Item -ItemType Directory -Force -Path "$PSScriptRoot/.cache/QuantumBlockEncoding" | Out-Null
  $env:LEAN_PATH="$PSScriptRoot/.cache;experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/.cache;experiments/hermite-polynomial/precision/piecewise-kernel-producer/.cache;experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/.cache"
  $taskSources=@(
    @('QuantumBlockEncoding/StoredGivens.lean','QuantumBlockEncoding/StoredGivens'),
    @('QuantumBlockEncoding/StoredTensorTrain.lean','QuantumBlockEncoding/StoredTensorTrain'),
    @('QuantumBlockEncoding/MatrixProductChain.lean','QuantumBlockEncoding/MatrixProductChain'),
    @('QuantumBlockEncoding/StoredMatrixProductChain.lean','QuantumBlockEncoding/StoredMatrixProductChain'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-stored-c22/RationalBlocks.lean','RationalBlocks'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-stored-c22/StoredProducer.lean','StoredProducer'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-stored-c22/AccountedTraffic.lean','AccountedTraffic'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-stored-c22/StoredConsumerChecks.lean','StoredConsumerChecks')
  )
  $taskBindings=@{}
  foreach ($taskSource in $taskSources) { $taskBindings[$taskSource[0]]=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskSource[0]).Hash.ToLower() }
  foreach ($taskPath in @('lean-toolchain','lake-manifest.json','tasks/SP-HERMITE-POLY-002.md','reports/process-memory.json','experiments/hermite-polynomial/precision/piecewise-kernel-stored-c22/statement-seal-v1.json','.lake/packages/mathlib/Mathlib/Data/Nat/Choose/Basic.lean','.lake/packages/mathlib/Mathlib/Data/Nat/Factorial/Basic.lean','.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Data/Nat/Choose/Basic.olean','.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Data/Nat/Factorial/Basic.olean')) {
    $taskBindings[$taskPath]=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower()
  }
  $taskFrozen=@{}
  foreach ($taskDir in @('piecewise-kernel-producer','piecewise-kernel-uniform-c20','piecewise-kernel-assembly-c21')) {
    foreach ($taskFile in Get-ChildItem -Recurse -File -LiteralPath "experiments/hermite-polynomial/precision/$taskDir") {
      $taskRelative=$taskFile.FullName.Substring($taskRepoRoot.Length+1).Replace('\','/')
      $taskFrozen[$taskRelative]=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskFile.FullName).Hash.ToLower()
    }
  }
  @{sources=$taskBindings;frozen_c19_c20_c21=$taskFrozen;lean_path_order=@('piecewise-kernel-stored-c22/.cache','piecewise-kernel-assembly-c21/.cache','piecewise-kernel-producer/.cache','piecewise-kernel-uniform-c20/.cache');consumerchecks_resolution=@{logical_module='ConsumerChecks';source='experiments/hermite-polynomial/precision/finite-middle-source/ConsumerChecks.lean';selected_cache='experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/.cache/ConsumerChecks.olean';c20_consumerchecks_excluded=$true}} | ConvertTo-Json -Depth 25 | Set-Content -Encoding utf8 -LiteralPath "$PSScriptRoot/pre-gate-bindings.json"
  foreach ($taskSource in $taskSources) {
    Write-Output "BEGIN $($taskSource[0])"
    lake env lean -o "$PSScriptRoot/.cache/$($taskSource[1]).olean" $taskSource[0]
    if ($LASTEXITCODE -ne 0) { throw "Fresh source failed:$($taskSource[0])" }
    Write-Output "PASS $($taskSource[0])"
  }
  foreach ($taskPath in $taskBindings.Keys) {
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower() -ne $taskBindings[$taskPath]) { throw "Proof binding changed:$taskPath" }
  }
  foreach ($taskPath in $taskFrozen.Keys) {
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower() -ne $taskFrozen[$taskPath]) { throw "Frozen artifact changed:$taskPath" }
  }
  Write-Output 'ALL PRE-GATE SOURCE/SEAL/FROZEN C19 C20 C21 BINDINGS UNCHANGED'
} finally { $env:LEAN_PATH=$taskPriorLeanPath; Pop-Location }
