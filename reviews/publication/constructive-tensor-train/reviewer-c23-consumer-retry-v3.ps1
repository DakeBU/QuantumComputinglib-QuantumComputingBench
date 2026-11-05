$cttRetryPath = Join-Path (Get-Location) 'reviews/publication/constructive-tensor-train/reviewer-c23-consumer-retry-v2.ps1'
$cttRetry = [IO.File]::ReadAllText($cttRetryPath)
$cttRetry = $cttRetry.Replace('ReviewerConsumerV2','ReviewerConsumerV3').Replace('consumer-v2.log','consumer-v3.log').Replace('consumer-check-v2.json','consumer-check-v3.json').Replace('consumer v2 exit','consumer v3 exit')
Invoke-Expression $cttRetry
