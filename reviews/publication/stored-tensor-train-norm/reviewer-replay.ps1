$ErrorActionPreference = 'Stop'
$reviewerRoot = Split-Path (Split-Path (Split-Path $PSScriptRoot))
Push-Location -LiteralPath $reviewerRoot
try {
  $reviewerSource = [System.IO.File]::ReadAllText((Join-Path $reviewerRoot 'QuantumBlockEncoding/StoredTensorTrainNorm.lean'))
  $reviewerSha = (Get-FileHash -Algorithm SHA256 -LiteralPath 'QuantumBlockEncoding/StoredTensorTrainNorm.lean').Hash.ToLower()
  if ($reviewerSha -ne '000db174cba35e68c360bb59754bf6e75aec362c6a5bf8f003d96abf80810f88') { throw 'Frozen target changed' }
  $reviewerNames = [regex]::Matches($reviewerSource, '(?m)^(?:noncomputable )?(?:def|theorem) ([A-Za-z_][A-Za-z_0-9]*)') | ForEach-Object { $_.Groups[1].Value }
  if ($reviewerNames.Count -ne 29) { throw 'Public inventory changed' }
  $reviewerChecks = ($reviewerNames | ForEach-Object { "#check QuantumBlockEncoding.StoredTensorTrainNorm.$_`n#print axioms QuantumBlockEncoding.StoredTensorTrainNorm.$_" }) -join "`n"
  $reviewerProbes = [System.IO.File]::ReadAllText((Join-Path $PSScriptRoot 'reviewer-probes.lean'))
  ($reviewerSource + "`n" + $reviewerChecks + "`n" + $reviewerProbes) | lake env lean --stdin
  $reviewerExit = $LASTEXITCODE
} finally {
  Pop-Location
}
exit $reviewerExit
