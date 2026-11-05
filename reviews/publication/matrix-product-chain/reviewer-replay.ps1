param()
$ErrorActionPreference = 'Stop'
$reviewRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
Set-Location -LiteralPath $reviewRoot
$reviewUtf8 = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = $reviewUtf8
[Console]::InputEncoding = $reviewUtf8
[Console]::OutputEncoding = $reviewUtf8
$reviewModule = 'QuantumBlockEncoding/MatrixProductChain.lean'
$reviewProbe = 'reviews/publication/matrix-product-chain/reviewer-probes.lean'
$reviewLog = 'reviews/publication/matrix-product-chain/reviewer-lean-log.json'
if (Test-Path -LiteralPath $reviewLog) { throw 'Frozen reviewer log already exists; use a separately named attempt.' }
function Review-Hash([string]$reviewName) {
  if (Test-Path -LiteralPath $reviewName -PathType Leaf) {
    return (Get-FileHash -LiteralPath $reviewName -Algorithm SHA256).Hash.ToLowerInvariant()
  }
  return $null
}
$reviewClosure = [Collections.Generic.HashSet[string]]::new()
function Review-Visit([string]$reviewName) {
  if (-not $reviewClosure.Add($reviewName)) { return }
  $reviewBody = [IO.File]::ReadAllText((Join-Path $reviewRoot $reviewName), $reviewUtf8)
  foreach ($reviewMatch in [regex]::Matches($reviewBody, '(?m)^import\s+(QuantumBlockEncoding\.[A-Za-z0-9_.]+)')) {
    Review-Visit ($reviewMatch.Groups[1].Value.Replace('.', '/') + '.lean')
  }
}
Review-Visit $reviewModule
$reviewBefore = @()
foreach ($reviewName in ($reviewClosure | Sort-Object)) {
  $reviewOlean = '.lake/build/lib/lean/' + $reviewName.Substring(0,$reviewName.Length-5) + '.olean'
  $reviewBefore += [ordered]@{path=$reviewName; source_sha256=(Review-Hash $reviewName); olean_path=$reviewOlean; olean_sha256=(Review-Hash $reviewOlean); freshly_elaborated=($reviewName -eq $reviewModule)}
}
$reviewCombined = [IO.File]::ReadAllText((Join-Path $reviewRoot $reviewModule),$reviewUtf8) + "`n" + [IO.File]::ReadAllText((Join-Path $reviewRoot $reviewProbe),$reviewUtf8)
$reviewInputHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($reviewUtf8.GetBytes($reviewCombined))).ToLowerInvariant()
$reviewTimer = [Diagnostics.Stopwatch]::StartNew()
$reviewCaptured = @($reviewCombined | & lake env lean --stdin 2>&1)
$reviewExit = $LASTEXITCODE
$reviewTimer.Stop()
$reviewOutput = ($reviewCaptured | ForEach-Object {$_.ToString()}) -join "`n"
$reviewOutput = $reviewOutput.Replace($reviewRoot,'<repo>').Replace($reviewRoot.Replace('\','/'),'<repo>')
$reviewOutput = [regex]::Replace($reviewOutput, '[A-Za-z]:[\\/][^\r\n"'']+', '<local-path>')
$reviewAfter = @()
foreach ($reviewItem in $reviewBefore) {
  $reviewAfter += [ordered]@{path=$reviewItem.path; source_unchanged=((Review-Hash $reviewItem.path) -eq $reviewItem.source_sha256); olean_unchanged=((Review-Hash $reviewItem.olean_path) -eq $reviewItem.olean_sha256)}
}
$reviewRecord = [ordered]@{
 schema_version=1; identity='matrix-product-source-first-reviewer-c16'; run_id='matrix-product-reviewer-c16-20261009';
 command='native pwsh UTF-8 full actual source plus own probes piped to lake env lean --stdin';
 elapsed_seconds=$reviewTimer.Elapsed.TotalSeconds; exit_code=$reviewExit;
 combined_input_sha256=$reviewInputHash; module_sha256=(Review-Hash $reviewModule); probe_sha256=(Review-Hash $reviewProbe);
 replay_sha256=(Review-Hash 'reviews/publication/matrix-product-chain/reviewer-replay.ps1');
 toolchain_sha256=(Review-Hash 'lean-toolchain'); manifest_sha256=(Review-Hash 'lake-manifest.json'); lakefile_sha256=(Review-Hash 'lakefile.lean');
 closure_before=$reviewBefore; closure_after=$reviewAfter; output=$reviewOutput;
 target_cached_import=$false; production_output_emitted=$false;
 scope='Whole actual target freshly elaborated with existing compiled provider context, not a fresh transitive dependency build or provider-wide semantic approval.'
}
[IO.File]::WriteAllText((Join-Path $reviewRoot $reviewLog),($reviewRecord | ConvertTo-Json -Depth 16)+"`n",$reviewUtf8)
$reviewRecord | ConvertTo-Json -Depth 16
exit $reviewExit
