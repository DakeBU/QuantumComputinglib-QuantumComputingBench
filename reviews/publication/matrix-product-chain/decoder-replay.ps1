param()
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
Set-Location -LiteralPath $repoRoot
$utf8 = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = $utf8
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$module = 'QuantumBlockEncoding/MatrixProductChain.lean'
$probe = 'reviews/publication/matrix-product-chain/decoder-probes.lean'
$log = 'reviews/publication/matrix-product-chain/decoder-lean-log.json'
function Hash-File([string]$name) {
  if (Test-Path -LiteralPath $name -PathType Leaf) {
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $name).Hash.ToLowerInvariant()
  }
  return $null
}
$localClosure = [System.Collections.Generic.HashSet[string]]::new()
function Visit-Source([string]$name) {
  if (-not $localClosure.Add($name)) { return }
  $body = [IO.File]::ReadAllText((Join-Path $repoRoot $name), $utf8)
  foreach ($match in [regex]::Matches($body, '(?m)^import\s+(QuantumBlockEncoding\.[A-Za-z0-9_.]+)')) {
    $child = $match.Groups[1].Value.Replace('.', '/') + '.lean'
    Visit-Source $child
  }
}
Visit-Source $module
$before = @()
foreach ($name in ($localClosure | Sort-Object)) {
  $olean = '.lake/build/lib/lean/' + $name.Substring(0, $name.Length - 5) + '.olean'
  $before += [ordered]@{ path=$name; source_sha256=(Hash-File $name); olean_path=$olean; olean_sha256=(Hash-File $olean); freshly_elaborated=($name -eq $module) }
}
$source = [IO.File]::ReadAllText((Join-Path $repoRoot $module), $utf8)
$probes = [IO.File]::ReadAllText((Join-Path $repoRoot $probe), $utf8)
$combined = $source + "`n" + $probes
$inputHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($utf8.GetBytes($combined))).ToLowerInvariant()
$startUtc = [DateTime]::UtcNow.ToString('o')
$timer = [Diagnostics.Stopwatch]::StartNew()
$captured = @($combined | & lake env lean --stdin 2>&1)
$exitCode = $LASTEXITCODE
$timer.Stop()
$publicOutput = ($captured | ForEach-Object { $_.ToString() }) -join "`n"
$publicOutput = $publicOutput.Replace($repoRoot, '<repo>').Replace($repoRoot.Replace('\','/'), '<repo>')
$publicOutput = [regex]::Replace($publicOutput, '[A-Za-z]:[\\/][^\r\n"'']+', '<local-path>')
$after = @()
foreach ($item in $before) {
  $after += [ordered]@{ path=$item.path; source_unchanged=((Hash-File $item.path) -eq $item.source_sha256); olean_unchanged=((Hash-File $item.olean_path) -eq $item.olean_sha256) }
}
$record = [ordered]@{
  schema_version=1; identity='matrix-product-source-blind-decoder-c16'; run_id='matrix-product-decoder-c16-20261009';
  command='native pwsh UTF-8 complete-source-plus-probes | lake env lean --stdin';
  start_utc=$startUtc; elapsed_seconds=$timer.Elapsed.TotalSeconds; exit_code=$exitCode;
  combined_input_sha256=$inputHash; module_sha256=(Hash-File $module); probe_sha256=(Hash-File $probe);
  replay_sha256=(Hash-File 'reviews/publication/matrix-product-chain/decoder-replay.ps1');
  closure_before=$before; closure_after=$after; output=$publicOutput;
  scope='Complete target source freshly elaborated, no target cached import, no output option, relevant providers use existing pinned compiled context; not a fresh transitive dependency build.'
}
[IO.File]::WriteAllText((Join-Path $repoRoot $log), ($record | ConvertTo-Json -Depth 16) + "`n", $utf8)
$record | ConvertTo-Json -Depth 16
exit $exitCode
