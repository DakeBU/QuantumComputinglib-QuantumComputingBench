$ErrorActionPreference='Stop'
$taskRepoRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
$taskPriorLeanPath=$env:LEAN_PATH
Push-Location -LiteralPath $taskRepoRoot
try {
  New-Item -ItemType Directory -Force -Path "$PSScriptRoot/.cache/QuantumBlockEncoding" | Out-Null
  $env:LEAN_PATH="$PSScriptRoot/.cache;experiments/hermite-polynomial/precision/piecewise-kernel-producer/.cache;experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/.cache"
  $taskSources=@(
    @('QuantumBlockEncoding/HermiteTransferCores.lean','QuantumBlockEncoding/HermiteTransferCores'),
    @('QuantumBlockEncoding/MatrixProductChain.lean','QuantumBlockEncoding/MatrixProductChain'),
    @('QuantumBlockEncoding/StoredMatrixProductChain.lean','QuantumBlockEncoding/StoredMatrixProductChain'),
    @('QuantumBlockEncoding/StoredBinaryCoordinates.lean','QuantumBlockEncoding/StoredBinaryCoordinates'),
    @('experiments/hermite-polynomial/precision/coefficient-range/CoefficientRange.lean','CoefficientRange'),
    @('experiments/hermite-polynomial/precision/finite-exp/FiniteExp.lean','FiniteExp'),
    @('experiments/hermite-polynomial/precision/finite-exp-degree/FiniteExpDegree.lean','FiniteExpDegree'),
    @('experiments/hermite-polynomial/precision/finite-middle-source/FiniteMiddleSource.lean','FiniteMiddleSource'),
    @('experiments/hermite-polynomial/precision/finite-middle-source/ConsumerChecks.lean','ConsumerChecks'),
    @('experiments/hermite-polynomial/precision/global-radius-budget/GlobalRadiusBudget.lean','GlobalRadiusBudget'),
    @('experiments/hermite-polynomial/precision/piecewise-source-budget/PiecewiseSourceBudget.lean','PiecewiseSourceBudget'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-producer/ActualDecomposition.lean','ActualDecomposition'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/UniformComparison.lean','UniformComparison'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/UniformTranslation.lean','UniformTranslation'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/UniformThresholds.lean','UniformThresholds'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/IndexedKernel.lean','IndexedKernel'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/ActualCoefficients.lean','ActualCoefficients'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/ActualAssembly.lean','ActualAssembly'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/AssemblyConsumerChecks.lean','AssemblyConsumerChecks')
  )
  $taskBindings=@{}
  foreach ($taskSource in $taskSources) { $taskBindings[$taskSource[0]]=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskSource[0]).Hash.ToLower() }
  foreach ($taskPath in @('lean-toolchain','lake-manifest.json','tasks/SP-HERMITE-POLY-002.md','reports/process-memory.json','experiments/hermite-polynomial/precision/NormalizationStability.lean','experiments/hermite-polynomial/precision/radius-supplier/RadiusSupplier.lean','experiments/hermite-polynomial/precision/radius-stability/RadiusStability.lean','experiments/hermite-polynomial/precision/piecewise-source-budget/result.json','experiments/hermite-polynomial/precision/piecewise-kernel-producer/result.json','experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/result.json','experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/statement-seal-v1.json')) {
    $taskBindings[$taskPath]=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower()
  }
  $taskInherited=@{}
  foreach ($taskDir in @('piecewise-kernel-producer','piecewise-kernel-uniform-c20')) {
    $taskRoot="experiments/hermite-polynomial/precision/$taskDir"
    foreach ($taskFile in Get-ChildItem -Recurse -File -LiteralPath $taskRoot) {
      $taskRelative=$taskFile.FullName.Substring($taskRepoRoot.Length+1).Replace('\','/')
      $taskInherited[$taskRelative]=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskFile.FullName).Hash.ToLower()
    }
  }
  @{sources=$taskBindings;frozen_inherited=$taskInherited;lean_path_order=@('piecewise-kernel-assembly-c21/.cache','piecewise-kernel-producer/.cache','piecewise-kernel-uniform-c20/.cache');consumerchecks_resolution=@{logical_module='ConsumerChecks';fresh_source='experiments/hermite-polynomial/precision/finite-middle-source/ConsumerChecks.lean';selected_cache='piecewise-kernel-assembly-c21/.cache/ConsumerChecks.olean';shadow_excluded='piecewise-kernel-uniform-c20/.cache/ConsumerChecks.olean'}} | ConvertTo-Json -Depth 20 | Set-Content -Encoding utf8 -LiteralPath "$PSScriptRoot/pre-gate-bindings.json"
  foreach ($taskSource in $taskSources) {
    Write-Output "BEGIN $($taskSource[0])"
    lake env lean -o "$PSScriptRoot/.cache/$($taskSource[1]).olean" $taskSource[0]
    if ($LASTEXITCODE -ne 0) { throw "Fresh source failed:$($taskSource[0])" }
    Write-Output "PASS $($taskSource[0])"
  }
  foreach ($taskPath in $taskBindings.Keys) {
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower() -ne $taskBindings[$taskPath]) { throw "Binding changed:$taskPath" }
  }
  foreach ($taskPath in $taskInherited.Keys) {
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower() -ne $taskInherited[$taskPath]) { throw "Frozen inherited artifact changed:$taskPath" }
  }
  Write-Output 'ALL PRE-GATE SOURCE/SEAL/FROZEN BINDINGS UNCHANGED'
} finally { $env:LEAN_PATH=$taskPriorLeanPath; Pop-Location }
