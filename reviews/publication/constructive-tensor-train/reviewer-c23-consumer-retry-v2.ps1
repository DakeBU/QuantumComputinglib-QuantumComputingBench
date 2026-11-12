$ErrorActionPreference = 'Stop'
$cttBase = 'reviews/publication/constructive-tensor-train'
$cttRoot = (Get-Location).Path
$cttCache = Join-Path $cttRoot "$cttBase/reviewer-c23-privatecache-v3"
$cttSavedPath = $env:LEAN_PATH
$cttLibraryPath = (& lake env powershell -NoProfile -Command '$env:LEAN_PATH' | Out-String).Trim()
if($LASTEXITCODE -ne 0){throw 'Lake environment unavailable'}
$env:LEAN_PATH = "$cttCache;$cttLibraryPath"
try {
  $cttOutput = (& lean -o (Join-Path $cttCache 'ReviewerConsumerV2.olean') "$cttBase/reviewer-c23-consumer.lean" 2>&1 | Out-String)
  $cttExit = $LASTEXITCODE
  $cttOutput.Replace($cttRoot,'<repository>') | Out-File -LiteralPath "$cttBase/reviewer-c23-consumer-v2.log" -Encoding utf8
  @{reviewer_identity='ctt_source_first_reviewer_c23';run_identity='ctt-source-first-c23-20261010-v1';binding_sha256='9be3c975b10363ad36778d6dc9da4c7a941857f6571f3e2f6072c73d65a51c09';consumer_exit_code=$cttExit;consumer_source_sha256=(Get-FileHash -LiteralPath "$cttBase/reviewer-c23-consumer.lean" -Algorithm SHA256).Hash.ToLower();log="$cttBase/reviewer-c23-consumer-v2.log";fresh_eight_bound_sources_receipt="$cttBase/reviewer-c23-checks-v3.json";additional_import_olean_context='private copy of existing additional dependencies; not full repository fresh build';full_repository_gate='PENDING';site_gate='PENDING';purification='PENDING'} | ConvertTo-Json -Depth 6 | Out-File -LiteralPath "$cttBase/reviewer-c23-consumer-check-v2.json" -Encoding utf8
  Write-Output "consumer v2 exit $cttExit"
  Write-Output $cttOutput
} finally {$env:LEAN_PATH = $cttSavedPath}
