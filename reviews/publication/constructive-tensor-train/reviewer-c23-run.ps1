$ErrorActionPreference = 'Stop'
$cttRoot = (Get-Location).Path
$cttBase = 'reviews/publication/constructive-tensor-train'
$cttCache = Join-Path $cttRoot "$cttBase/reviewer-c23-privatecache-v1"
New-Item -ItemType Directory -Path (Join-Path $cttCache 'QuantumBlockEncoding') -Force | Out-Null
$cttContext = Get-Content -Raw "$cttBase/author-formal-context.json" | ConvertFrom-Json
$cttBound = @()
foreach ($cttFile in $cttContext.files) {
  $cttHash = (Get-FileHash -LiteralPath $cttFile.path -Algorithm SHA256).Hash.ToLower()
  if ($cttHash -ne $cttFile.sha256) { throw "Bound formal context mismatch: $($cttFile.path)" }
  $cttBound += @{path=$cttFile.path; sha256=$cttHash; matched=$true}
}
$cttOldLeanPath = $env:LEAN_PATH
$cttLakePath = (& lake env powershell -NoProfile -Command '[Environment]::GetEnvironmentVariable("LEAN_PATH")' | Out-String).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Lake environment discovery failed' }
$env:LEAN_PATH = "$cttCache;$cttLakePath"
$cttModules = @('RealAmplitudePreparation','SequentialBondPreparation','ThinLQ','AdjacentGivens','RectangularGivens','ConstructiveThinLQ','TensorTrainCanonical','ConstructiveTensorTrain')
$cttResults = @()
try {
  foreach ($cttModule in $cttModules) {
    Write-Output "START fresh module $cttModule"
    $cttOut = Join-Path $cttCache "QuantumBlockEncoding/$cttModule.olean"
    $cttLog = "$cttBase/reviewer-c23-fresh-$cttModule-v1.log"
    $cttOutput = (& lean -o $cttOut "QuantumBlockEncoding/$cttModule.lean" 2>&1 | Out-String)
    $cttExit = $LASTEXITCODE
    $cttOutput.Replace($cttRoot,'<repository>').Replace($cttCache,'<reviewer-privatecache>') | Out-File -LiteralPath $cttLog -Encoding utf8
    $cttResults += @{module=$cttModule; exit_code=$cttExit; log=$cttLog; fresh_source=$true; olean_sha256=$(if($cttExit -eq 0){(Get-FileHash -LiteralPath $cttOut -Algorithm SHA256).Hash.ToLower()}else{$null})}
    Write-Output "DONE $cttModule exit $cttExit"
    if ($cttExit -ne 0) { Write-Output $cttOutput; break }
  }
  if (($cttResults.Count -eq 8) -and ($cttResults[-1].exit_code -eq 0)) {
    Write-Output 'START independent consumer v1'
    $cttConsumer = "$cttBase/reviewer-c23-consumer.lean"
    $cttOutput = (& lean -o (Join-Path $cttCache 'ReviewerConsumer.olean') $cttConsumer 2>&1 | Out-String)
    $cttExit = $LASTEXITCODE
    $cttOutput.Replace($cttRoot,'<repository>') | Out-File -LiteralPath "$cttBase/reviewer-c23-consumer-v1.log" -Encoding utf8
    $cttResults += @{module='reviewer-c23-consumer'; exit_code=$cttExit; log="$cttBase/reviewer-c23-consumer-v1.log"; fresh_source=$true; source_sha256=(Get-FileHash -LiteralPath $cttConsumer -Algorithm SHA256).Hash.ToLower()}
    Write-Output "DONE consumer exit $cttExit"
    Write-Output $cttOutput
  }
} finally {
  $env:LEAN_PATH = $cttOldLeanPath
  @{reviewer_identity='ctt_source_first_reviewer_c23';run_identity='ctt-source-first-c23-20261010-v1';binding_sha256='121c0c8603b75ccde304783e94fa61abd82159768b0007da675da201f7501c24';formal_files=$cttBound;checks=$cttResults;fresh_target_and_context_sources=$true;mathlib_and_additional_transitive_imports='existing repository oleans; full repository gate not claimed';full_repository_gate='PENDING';site_gate='PENDING';purification='PENDING'} | ConvertTo-Json -Depth 8 | Out-File -LiteralPath "$cttBase/reviewer-c23-checks-v1.json" -Encoding utf8
}
