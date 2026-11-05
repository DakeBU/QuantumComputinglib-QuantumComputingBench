$ErrorActionPreference='Stop'
$taskRepoRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
Push-Location -LiteralPath $taskRepoRoot
try {
  $taskBindings=Get-Content -Raw -LiteralPath "$PSScriptRoot/pre-gate-bindings.json" | ConvertFrom-Json -AsHashtable
  foreach ($taskSection in @('sources','frozen_c19_c20_c21')) {
    foreach ($taskPath in $taskBindings[$taskSection].Keys) {
      if ((Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower() -ne $taskBindings[$taskSection][$taskPath]) { throw "Proof/frozen binding changed:$taskPath" }
    }
  }
  $taskC21Root='experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21'
  if ((Get-FileHash -Algorithm SHA256 -LiteralPath "$taskC21Root/result.json").Hash.ToLower() -ne '01b5c0f605c33d767979273753992a6ec0833170a9703510e90ee74336f9746f') { throw 'C21 result differs from accepted checkpoint' }
  if ((Get-FileHash -Algorithm SHA256 -LiteralPath "$taskC21Root/final-binding-manifest.json").Hash.ToLower() -ne '92b4d401a9547cd980c6d954185ee5d41deb0e0308730a67fcea31494e919f2d') { throw 'C21 manifest differs from accepted checkpoint' }
  $taskC21=Get-Content -Raw -LiteralPath "$taskC21Root/final-binding-manifest.json" | ConvertFrom-Json -AsHashtable
  $taskInheritedSources=@{}
  foreach ($taskPrior in @($taskC21['pre_gate_bindings']['sources'],$taskC21['inherited_source_equality_to_frozen_receipts'])) {
    foreach ($taskPath in $taskPrior.Keys) {
      if ($taskPath.EndsWith('.lean') -or $taskPath -eq 'lean-toolchain' -or $taskPath -eq 'lake-manifest.json') {
        $taskCurrent=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower()
        if ($taskCurrent -ne $taskPrior[$taskPath]) { throw "Accepted inherited source differs:$taskPath" }
        $taskInheritedSources[$taskPath]=$taskCurrent
      }
    }
  }
  $taskFinal=Get-Content -Raw -LiteralPath "$PSScriptRoot/focused-v1.raw.log"
  if ($taskFinal -notmatch 'ALL PRE-GATE SOURCE/SEAL/FROZEN C19 C20 C21 BINDINGS UNCHANGED' -or $taskFinal -match 'sorryAx|error:') { throw 'Final fresh source gate failed' }
  $taskPassCount=([regex]::Matches($taskFinal,'(?m)^PASS ')).Count
  if ($taskPassCount -ne 8) { throw "Expected 8 fresh sources; found $taskPassCount" }
  foreach ($taskLean in Get-ChildItem -File -LiteralPath $PSScriptRoot -Filter '*.lean') {
    if ((Get-Content -Raw -LiteralPath $taskLean.FullName) -match '\bsorry\b|\badmit\b|\bnative_decide\b|\bunsafe\b|\bofReduceBool\b|(?m)^\s*axiom\b') { throw "Forbidden proof content:$($taskLean.Name)" }
  }
  $taskRaw=@{}
  foreach ($taskLog in Get-ChildItem -File -LiteralPath $PSScriptRoot -Filter '*.raw.log') {
    $taskPublic=$taskLog.Name.Replace('.raw.log','.public-v1.log')
    $taskText=(Get-Content -Raw -LiteralPath $taskLog.FullName).Replace($taskRepoRoot,'.').Replace($taskRepoRoot.Replace('\','/'),'.')
    if ($taskText -match '[A-Za-z]:[\\/]') { throw "Unexpected absolute path:$($taskLog.Name)" }
    $taskText | Set-Content -Encoding utf8 -LiteralPath (Join-Path $PSScriptRoot $taskPublic)
    $taskRaw[$taskLog.Name]=@{raw_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskLog.FullName).Hash.ToLower();private_ignored=$true;public_derivative=$taskPublic;public_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $PSScriptRoot $taskPublic)).Hash.ToLower()}
  }
  $taskRaw | ConvertTo-Json -Depth 10 | Set-Content -Encoding utf8 -LiteralPath "$PSScriptRoot/private-raw-provenance.json"
  $taskArtifacts=@{}
  $taskCaches=@{}
  foreach ($taskFile in Get-ChildItem -Recurse -File -LiteralPath $PSScriptRoot) {
    $taskRelative=$taskFile.FullName.Substring($PSScriptRoot.Length+1).Replace('\','/')
    if ($taskFile.Name -eq 'final-binding-manifest.json' -or $taskFile.Name -like '*.raw.log') { continue }
    $taskHash=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskFile.FullName).Hash.ToLower()
    if ($taskRelative.StartsWith('.cache/')) { $taskCaches[$taskRelative]=$taskHash } else { $taskArtifacts[$taskRelative]=$taskHash }
  }
  @{pre_gate_bindings=$taskBindings;accepted_inherited_source_equality=$taskInheritedSources;artifact_hashes=$taskArtifacts;ignored_cache_hashes=$taskCaches;raw_provenance='private-raw-provenance.json';fresh_source_passes=$taskPassCount;axiom_scope='new printed roots: propext/Classical.choice/Quot.sound only';transitive_cache_boundary='Other production and Mathlib imports inherited, not rebuilt wholesale';compiler_gate_process_exit=0;scientific_ROOT=$false;full_runtime_claim=$false;frozen_c19_c20_c21_unchanged=$true;user_pause_no_successor=$true;all_writes_stopped=$true} | ConvertTo-Json -Depth 35 | Set-Content -Encoding utf8 -LiteralPath "$PSScriptRoot/final-binding-manifest.json"
  function Assert-TaskStrings($taskValue) {
    if ($taskValue -is [string]) { if ($taskValue -match '[A-Za-z]:[\\/]') { throw 'Drive path in decoded public JSON' } }
    elseif ($taskValue -is [System.Collections.IDictionary]) { foreach ($taskKey in $taskValue.Keys) { Assert-TaskStrings ([string]$taskKey); Assert-TaskStrings $taskValue[$taskKey] } }
    elseif ($taskValue -is [System.Collections.IEnumerable]) { foreach ($taskItem in $taskValue) { Assert-TaskStrings $taskItem } }
  }
  foreach ($taskFile in Get-ChildItem -File -LiteralPath $PSScriptRoot | Where-Object { $_.Name -notlike '*.raw.log' }) {
    $taskText=Get-Content -Raw -LiteralPath $taskFile.FullName
    if ($taskText -match '[A-Za-z]:[\\/]') { throw "Drive path in public source/runner/log:$($taskFile.Name)" }
    if ($taskFile.Extension -eq '.json') { Assert-TaskStrings ($taskText | ConvertFrom-Json -AsHashtable) }
  }
  Write-Output "RESULT SHA256 $($taskArtifacts['result.json'])"
  Write-Output "RATIONAL SOURCE SHA256 $($taskArtifacts['RationalBlocks.lean'])"
  Write-Output "STORED SOURCE SHA256 $($taskArtifacts['StoredProducer.lean'])"
  Write-Output "STORED CACHE SHA256 $($taskCaches['.cache/StoredProducer.olean'])"
  Write-Output "CONSUMER CACHE SHA256 $($taskCaches['.cache/StoredConsumerChecks.olean'])"
  Write-Output "MANIFEST SHA256 $((Get-FileHash -Algorithm SHA256 -LiteralPath "$PSScriptRoot/final-binding-manifest.json").Hash.ToLower())"
  Write-Output 'ALL WRITES STOPPED; NO SUCCESSOR OPENED'
} finally { Pop-Location }
