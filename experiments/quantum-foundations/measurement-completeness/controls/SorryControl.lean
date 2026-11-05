import QuantumBlockEncoding.MeasurementProbability

-- Fixed negative fixture only: Lean may exit zero, but sorryAx must reject it.
theorem measurementIntakeSorryControl : (0 : ℝ) = 1 := by sorry
#print axioms measurementIntakeSorryControl
