$ErrorActionPreference = 'Stop'
$cttReviewBase = 'reviews/publication/constructive-tensor-train'
$cttReviewCache = Join-Path (Get-Location) "$cttReviewBase/reviewer-c23-privatecache-v3"
$cttOriginalLib = Join-Path (Get-Location) '.lake/build/lib/lean/QuantumBlockEncoding'
$cttRebuilt = @('RealAmplitudePreparation','SequentialBondPreparation','ThinLQ','AdjacentGivens','RectangularGivens','ConstructiveThinLQ','TensorTrainCanonical','ConstructiveTensorTrain')
New-Item -ItemType Directory -Path (Join-Path $cttReviewCache 'QuantumBlockEncoding') -Force | Out-Null
foreach ($cttImport in Get-ChildItem -LiteralPath $cttOriginalLib -Recurse -File -Filter '*.olean') {
  if (($cttImport.DirectoryName -eq $cttOriginalLib) -and ($cttImport.BaseName -in $cttRebuilt)) { continue }
  $cttRelative = $cttImport.FullName.Substring($cttOriginalLib.Length + 1)
  $cttDest = Join-Path (Join-Path $cttReviewCache 'QuantumBlockEncoding') $cttRelative
  New-Item -ItemType Directory -Path (Split-Path -Parent $cttDest) -Force | Out-Null
  Copy-Item -LiteralPath $cttImport.FullName -Destination $cttDest
}
# Retain the failed v2 script intact. Execute only a versioned cache/log substitution.
$cttVersionedRunner = [IO.File]::ReadAllText((Join-Path (Get-Location) "$cttReviewBase/reviewer-c23-run-v2.ps1"))
$cttVersionedRunner = $cttVersionedRunner.Replace('privatecache-v2','privatecache-v3').Replace('-v2.log','-v3.log').Replace('checks-v2.json','checks-v3.json')
Invoke-Expression $cttVersionedRunner
