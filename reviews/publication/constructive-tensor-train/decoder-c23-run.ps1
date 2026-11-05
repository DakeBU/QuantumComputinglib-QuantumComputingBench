param([ValidateSet('target','providers','target-fresh','checks','consumer')][string]$Stage,
  [ValidateRange(1,9)][int]$Attempt = 1)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$base = 'reviews/publication/constructive-tensor-train'
$cache = "$base/decoder-c23-cache"
$private = "$base/decoder-c23-private"
New-Item -ItemType Directory -Force -Path "$cache/QuantumBlockEncoding",$private | Out-Null
$seen = @{}
$providerInventory = [Collections.Generic.List[object]]::new()
function Visit-FormalImport([string]$module) {
  if ($seen.ContainsKey($module)) { return }
  $seen[$module] = $true
  $source = ($module.Replace('.','/')) + '.lean'
  if (!(Test-Path -LiteralPath $source)) { return }
  $imports = @()
  foreach ($line in (Get-Content -LiteralPath $source)) {
    if ($line -match '^import\s+([A-Za-z0-9_.]+)\s*$') { $imports += $Matches[1] }
  }
  foreach ($import in $imports) { Visit-FormalImport $import }
  if ($module -ne 'QuantumBlockEncoding.ConstructiveTensorTrain') {
    $inherited = '.lake/build/lib/lean/' + $module.Replace('.','/') + '.olean'
    $owned = $cache + '/' + $module.Replace('.','/') + '.olean'
    if (!(Test-Path -LiteralPath $owned) -and (Test-Path -LiteralPath $inherited)) {
      New-Item -ItemType Directory -Force -Path (Split-Path -Parent $owned) | Out-Null
      Copy-Item -LiteralPath $inherited -Destination $owned
    }
    $providerInventory.Add([ordered]@{module=$module;source=$source;
      source_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $source).Hash.ToLower();
      source_context='import-header traversal only unless separately recorded as fully read';
      imports=$imports;inherited_olean=$inherited;owned_olean=$owned;
      inherited_olean_sha256=if(Test-Path -LiteralPath $inherited){(Get-FileHash -Algorithm SHA256 -LiteralPath $inherited).Hash.ToLower()}else{$null};
      owned_olean_sha256=if(Test-Path -LiteralPath $owned){(Get-FileHash -Algorithm SHA256 -LiteralPath $owned).Hash.ToLower()}else{$null}})
  }
}
Visit-FormalImport 'QuantumBlockEncoding.ConstructiveTensorTrain'
[IO.File]::WriteAllText((Join-Path $root "$base/decoder-c23-provider-inventory-$Stage-attempt$Attempt.json"),
  ($providerInventory | ConvertTo-Json -Depth 10)+"`n",[Text.UTF8Encoding]::new($false))
$raw = "$private/$Stage-attempt$Attempt-raw.log"
$public = "$base/decoder-c23-$Stage-attempt$Attempt.log"
$start = [DateTime]::UtcNow.ToString('o')
$libraryPaths = @((Join-Path $root $cache))
Get-ChildItem -LiteralPath '.lake/packages' -Directory | ForEach-Object {
  $candidate = Join-Path $_.FullName '.lake/build/lib/lean'
  if (Test-Path -LiteralPath $candidate) { $libraryPaths += $candidate }
}
$libraryPaths += (Join-Path $root '.lake/build/lib/lean')
$libraryPaths += ((& lean --print-libdir | Out-String).Trim())
$env:LEAN_PATH = $libraryPaths -join ';'
if ($Stage -eq 'target') {
  $argsLean = @('-o',"$cache/QuantumBlockEncoding/ConstructiveTensorTrain.olean",
    'QuantumBlockEncoding/ConstructiveTensorTrain.lean')
  $command = 'lean ' + ($argsLean -join ' ')
  $ErrorActionPreference = 'Continue'
  & lean @argsLean *> $raw
  $code = $LASTEXITCODE
} else {
  $leanFile = "$base/decoder-c23-$Stage.lean"
  if ($Stage -eq 'checks') {
    $packet = Get-Content -LiteralPath "$base/author-decoder-packet-v2.json" -Raw | ConvertFrom-Json
    $lines = @('import QuantumBlockEncoding.ConstructiveTensorTrain',
      'set_option pp.universes true')
    foreach ($decl in $packet.declarations) {
      $lines += "#check @$decl"
      $lines += "#print axioms $decl"
    }
    $lines += '#print QuantumBlockEncoding.ConstructiveTensorTrain.CoreFactorization'
    $lines += '#print QuantumBlockEncoding.ConstructiveTensorTrain.Result'
    [IO.File]::WriteAllText((Join-Path $root $leanFile),($lines -join "`n")+"`n",[Text.UTF8Encoding]::new($false))
  }
  $inner = '$env:LEAN_PATH = "' + $cache + ';" + $env:LEAN_PATH; '
  if ($Stage -eq 'providers') {
    $modules = @('RealAmplitudePreparation','SequentialBondPreparation','ThinLQ',
      'TensorTrainCanonical','AdjacentGivens','RectangularGivens','ConstructiveThinLQ')
    foreach ($module in $modules) {
      $inner += 'Write-Output "SOURCE ' + $module + '"; & lean -o "' +
        "$cache/QuantumBlockEncoding/$module.olean" + '" "QuantumBlockEncoding/' +
        $module + '.lean"; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }; '
    }
    $inner += 'exit 0'
  } elseif ($Stage -eq 'target-fresh') {
    $inner += '& lean -o "' + "$cache/QuantumBlockEncoding/ConstructiveTensorTrain.olean" +
      '" "QuantumBlockEncoding/ConstructiveTensorTrain.lean"; exit $LASTEXITCODE'
  } else {
    $inner += '& lean -o "' + "$cache/$Stage.olean" + '" "' + $leanFile +
      '"; exit $LASTEXITCODE'
  }
  $command = 'Direct lean commands in inner_command; LEAN_PATH prepends owned cache, then installed package build libraries, repository build library, Lean standard library'
  $ErrorActionPreference = 'Continue'
  if ($Stage -eq 'providers') {
    $code = 0
    & {
      foreach ($module in $modules) {
        Write-Output "SOURCE $module"
        & lean -o "$cache/QuantumBlockEncoding/$module.olean" "QuantumBlockEncoding/$module.lean"
        if ($LASTEXITCODE -ne 0) { $script:providerCode = $LASTEXITCODE; break }
      }
    } *> $raw
    if ($script:providerCode) { $code = $script:providerCode }
  } elseif ($Stage -eq 'target-fresh') {
    & lean -o "$cache/QuantumBlockEncoding/ConstructiveTensorTrain.olean" 'QuantumBlockEncoding/ConstructiveTensorTrain.lean' *> $raw
    $code = $LASTEXITCODE
  } else {
    & lean -o "$cache/$Stage.olean" $leanFile *> $raw
    $code = $LASTEXITCODE
  }
}
$end = [DateTime]::UtcNow.ToString('o')
$ErrorActionPreference = 'Stop'
$rawText = [IO.File]::ReadAllText((Join-Path $root $raw))
$clean = $rawText.Replace($root,'.').Replace($root.Replace('\','/'),'.')
$clean = $clean -replace '(?s)Cannot convert value ".*?" to type "System.Int32"', 'Cannot convert value "<inherited LEAN_PATH redacted>" to type "System.Int32"'
$clean = $clean -replace '[A-Za-z]:[\\/][^\r\n''" ]+', '[local-path-redacted]'
[IO.File]::WriteAllText((Join-Path $root $public),$clean,[Text.UTF8Encoding]::new($false))
$receipt = [ordered]@{stage=$Stage;command=$command;start_utc=$start;end_utc=$end;exit_code=$code;
  inner_command=if($inner){$inner.Replace('$env:LEAN_PATH = "' + $cache + ';" + $env:LEAN_PATH; ','')}else{$null};
  import_search_order=@($cache,'.lake/packages/*/.lake/build/lib/lean','.lake/build/lib/lean','<Lean-standard-library>');
  raw_log=$raw;public_log=$public;raw_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $raw).Hash.ToLower();
  public_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $public).Hash.ToLower();
  target_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath 'QuantumBlockEncoding/ConstructiveTensorTrain.lean').Hash.ToLower()}
if($Stage -in @('checks','consumer')) {
  $receipt.input_lean = $leanFile
  $receipt.input_lean_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $leanFile).Hash.ToLower()
}
[IO.File]::WriteAllText((Join-Path $root "$base/decoder-c23-$Stage-attempt$Attempt-receipt.json"),
  ($receipt | ConvertTo-Json -Depth 8)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output ($receipt | ConvertTo-Json -Depth 8)
Write-Output $clean
exit $code
