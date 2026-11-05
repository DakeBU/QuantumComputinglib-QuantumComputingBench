$ErrorActionPreference = 'Stop'
$decoderRoot = Split-Path (Split-Path (Split-Path $PSScriptRoot))
Push-Location -LiteralPath $decoderRoot
try {
  $decoderSource = [System.IO.File]::ReadAllText((Join-Path $decoderRoot 'QuantumBlockEncoding/StoredTensorTrainNorm.lean'))
  $decoderSha = (Get-FileHash -Algorithm SHA256 -LiteralPath 'QuantumBlockEncoding/StoredTensorTrainNorm.lean').Hash.ToLower()
  if ($decoderSha -ne '000db174cba35e68c360bb59754bf6e75aec362c6a5bf8f003d96abf80810f88') { throw 'Frozen target changed' }
  $decoderNames = [regex]::Matches($decoderSource, '(?m)^(?:noncomputable )?(?:def|theorem) ([A-Za-z_][A-Za-z_0-9]*)') | ForEach-Object { $_.Groups[1].Value }
  if ($decoderNames.Count -ne 29) { throw 'Public inventory changed' }
  $decoderChecks = ($decoderNames | ForEach-Object { "#check QuantumBlockEncoding.StoredTensorTrainNorm.$_`n#print axioms QuantumBlockEncoding.StoredTensorTrainNorm.$_" }) -join "`n"
  $decoderEdges = @'
namespace QuantumBlockEncoding.StoredTensorTrainNorm
open scoped BigOperators
open StoredGivens StoredTensorTrain TensorTrainCanonical
example {n l r : ℕ} (C : StoredChain n l r) (a c : Fin l) :
    denote (gram C).value a c = ∑ x : Word n, ∑ t : Fin r,
      contract (denoteChain C) x a t * contract (denoteChain C) x c t := by
  rw [gram_value, TensorTrainNormEnvironment.gram_eq_sum]
  simp [Matrix.sum_apply, Matrix.mul_apply, Matrix.transpose_apply]
example (r : ℕ) : denote (gram (StoredChain.nil r)).value = 1 := by
  rw [gram_value]
  rfl
example : (norm (StoredChain.nil 1)).value = 1 := by
  rw [norm_value]
  simp [TensorTrainNormEnvironment.norm, TensorTrainNormEnvironment.gram, denoteChain]
example (r : ℕ) : StoredRectangularGivens.total (gram (StoredChain.nil r)).cost =
    5 * r ^ 2 + 4 * r + 6 := by
  simp [gram, cacheNode, StoredRectangularGivens.total,
    StoredRectangularGivens.identity_cost, StoredRectangularGivens.identityBudget, nodeBudget, tick]
  ring
example : StoredRectangularGivens.total (norm (StoredChain.nil 1)).cost = 18 := by
  simp [StoredRectangularGivens.total, norm_cost, gram, cacheNode,
    StoredRectangularGivens.identity_cost, StoredRectangularGivens.identityBudget, nodeBudget, tick]
example {l : ℕ} (A : StoredCore l 0) (E : StoredMatrix 0 0) (bit : Fin 2)
    (a c : Fin l) : (secondEntry (firstPass A E bit).value A bit a c).value = 0 := rfl
example {m : ℕ} (bit : Fin 2) (j : Fin m) :
    (finProdFinEquiv (bit, j)).val = bit.val * m + j.val := by
  simp [finProdFinEquiv, Nat.mul_comm, Nat.add_comm]
example : StoredRectangularGivens.total (gram (StoredChain.nil 0)).cost = 6 := by
  simp [gram, cacheNode, StoredRectangularGivens.total,
    StoredRectangularGivens.identity_cost, StoredRectangularGivens.identityBudget, nodeBudget, tick]
#print QuantumBlockEncoding.StoredGivens.Run.bind
#print QuantumBlockEncoding.StoredGivens.collect
#print QuantumBlockEncoding.StoredGivens.materialize
#print QuantumBlockEncoding.StoredThinLQ.entry
#print QuantumBlockEncoding.StoredTensorTrain.sumEntries
end QuantumBlockEncoding.StoredTensorTrainNorm
'@
  ($decoderSource + "`n" + $decoderChecks + "`n" + $decoderEdges) | lake env lean --stdin
  $decoderExit = $LASTEXITCODE
} finally {
  Pop-Location
}
exit $decoderExit

