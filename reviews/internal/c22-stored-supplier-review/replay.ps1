param([string]$Attempt='consumer-v1')
$ErrorActionPreference='Stop'
$reviewRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../..')).Path
$oldLeanPath=$env:LEAN_PATH
$sourcePaths=@(
 'tasks/SP-HERMITE-POLY-002.md','lean-toolchain','lake-manifest.json',
 'experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/ActualAssembly.lean',
 'experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/ActualCoefficients.lean',
 'experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/IndexedKernel.lean',
 'experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/AssemblyConsumerChecks.lean',
 'experiments/hermite-polynomial/precision/piecewise-kernel-producer/ActualDecomposition.lean',
 'experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/UniformComparison.lean',
 'experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/UniformTranslation.lean',
 'experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/UniformThresholds.lean',
 'experiments/hermite-polynomial/precision/piecewise-source-budget/PiecewiseSourceBudget.lean',
 'experiments/hermite-polynomial/precision/finite-exp/FiniteExp.lean',
 'experiments/hermite-polynomial/precision/finite-exp-degree/FiniteExpDegree.lean',
 'experiments/hermite-polynomial/precision/finite-middle-source/FiniteMiddleSource.lean',
 'experiments/hermite-polynomial/precision/piecewise-kernel-stored-c22/RationalBlocks.lean',
 'experiments/hermite-polynomial/precision/piecewise-kernel-stored-c22/StoredProducer.lean',
 'experiments/hermite-polynomial/precision/piecewise-kernel-stored-c22/AccountedTraffic.lean',
 'experiments/hermite-polynomial/precision/piecewise-kernel-stored-c22/StoredConsumerChecks.lean',
 'QuantumBlockEncoding/StoredGivens.lean','QuantumBlockEncoding/StoredMatrixProductChain.lean',
 'QuantumBlockEncoding/StoredTensorTrain.lean','QuantumBlockEncoding/StoredThinLQ.lean',
 'QuantumBlockEncoding/MatrixProductChain.lean','QuantumBlockEncoding/TensorTrainCanonical.lean',
 'reviews/internal/c22-stored-supplier-review/IndependentConsumer.lean',
 'reviews/internal/c22-stored-supplier-review/replay.ps1')
function Get-ReviewBindings {
 $bindings=[ordered]@{}
 foreach ($relative in $sourcePaths) {
  $bindings[$relative]=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $reviewRoot $relative)).Hash.ToLowerInvariant()
 }
 foreach ($folder in @('piecewise-kernel-stored-c22','piecewise-kernel-assembly-c21','piecewise-kernel-producer','piecewise-kernel-uniform-c20')) {
  $prefix="experiments/hermite-polynomial/precision/$folder/.cache"
  foreach ($entry in (Get-ChildItem -LiteralPath (Join-Path $reviewRoot $prefix) -Filter '*.olean')) {
   $bindings["$prefix/$($entry.Name)"]=(Get-FileHash -Algorithm SHA256 -LiteralPath $entry.FullName).Hash.ToLowerInvariant()
  }
 }
 return $bindings
}
Push-Location -LiteralPath $reviewRoot
try {
 $before=Get-ReviewBindings
 $commit=(git rev-parse HEAD).Trim()
 $branch=(git branch --show-current).Trim()
 $env:LEAN_PATH='experiments/hermite-polynomial/precision/piecewise-kernel-stored-c22/.cache;experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/.cache;experiments/hermite-polynomial/precision/piecewise-kernel-producer/.cache;experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/.cache'
 $started=[DateTime]::UtcNow.ToString('o')
 $output=& lake env lean 'reviews/internal/c22-stored-supplier-review/IndependentConsumer.lean' 2>&1
 $leanExit=$LASTEXITCODE
 $after=Get-ReviewBindings
 $public=($output | Out-String).Replace($reviewRoot,'.').Replace($reviewRoot.Replace('\','/'),'.')
 [IO.File]::WriteAllText((Join-Path $PSScriptRoot "$Attempt.log"),$public,[Text.UTF8Encoding]::new($false))
 $changed=@($before.Keys | Where-Object { $before[$_] -ne $after[$_] })
 $receipt=[ordered]@{schema='c22-independent-review-v1';direction_fingerprint='C22_INDEPENDENT_SAME_OBJECT_AND_COST_BOUNDARY';scope='internal checkpoint review, not publication admission';branch=$branch;head=$commit;started_utc=$started;finished_utc=[DateTime]::UtcNow.ToString('o');lean_exit=$leanExit;changed_inputs=$changed;bindings_before=$before;bindings_after=$after;cache_policy='Existing caches read only; parent separately replays focused sources. This receipt binds selected source/cache context, not the complete transitive closure.';log_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $PSScriptRoot "$Attempt.log")).Hash.ToLowerInvariant()}
 [IO.File]::WriteAllText((Join-Path $PSScriptRoot "$Attempt.json"),($receipt | ConvertTo-Json -Depth 8),[Text.UTF8Encoding]::new($false))
 Write-Output $public
 Write-Output "LEAN_EXIT=$leanExit CHANGED_INPUTS=$($changed.Count)"
 exit $leanExit
} finally { $env:LEAN_PATH=$oldLeanPath; Pop-Location }
