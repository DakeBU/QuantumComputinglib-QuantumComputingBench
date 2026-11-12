import SetupCostProof

/-! Own-output audit commands, not prefilled successful output. -/
set_option pp.fullNames true
set_option pp.explicit true
set_option pp.universes true

#check HermiteCachedPiecewiseStored.rightSetup_total_le
#print HermiteCachedPiecewiseStored.rightSetup_total_le
#print axioms HermiteCachedPiecewiseStored.rightSetup_total_le
#print HermiteCachedPiecewiseStored.rightSetup
#print HermiteCachedPiecewiseStored.cutoffQ
#print HermiteCachedPiecewiseStored.gridStepRun
#print HermiteCachedPiecewiseStored.strictCutFrom
#print HermiteCachedPiecewiseStored.inclusiveCutFrom
#print HermiteCachedPiecewiseStored.clippedRun
#print HermiteCachedPiecewiseStored.midpointFrom
#print HermiteFiniteExp.tailCutoff
#print HermiteFiniteExpDegree.sourceDegree
#print HermiteFiniteExpDegree.degree
#print QuantumBlockEncoding.StoredRectangularGivens.total
#print QuantumBlockEncoding.StoredGivens.Run.bind
#print QuantumBlockEncoding.StoredGivens.collect
#check QuantumBlockEncoding.StoredGivens.collect_cost
#print HermiteChargedSourceCache.factorials
#check HermiteChargedSourceCache.factorials_cost_le
#print HermiteChargedSourceCache.sumEntries
#check HermiteCachedPiecewiseStored.cutoffQ_value
#check HermiteCachedPiecewiseStored.powQ_cost
