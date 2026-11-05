import QuantumBlockEncoding.StoredBinaryCoordinates

namespace QuantumBlockEncoding.StoredBinaryCoordinates.Tests

open StoredGivens HermiteBoundaryInjection

example : (binaryReal 0 0).run.value = 0 := by
  simpa using binaryReal_value 0 0 (by norm_num)

example : (binaryReal 5 23).run.value = 23 := by
  exact binaryReal_value 5 23 (by norm_num)

example : (coordinate 3 5 (-7) (1/2)).run.value = -9/2 := by
  rw [coordinate_value _ _ _ _ (by norm_num)]
  norm_num [affinePoint]

example : (parents 2 3 (-2) (1/2)).run.value[0].lower = -2 := by
  simpa [affinePoint, boundarySchedule] using
    parents_lower 2 3 (-2) (1/2) (by norm_num) (0 : Fin 3)

example : (parents 2 3 (-2) (1/2)).run.value[1].lower = -2 := by
  simpa [affinePoint, boundarySchedule] using
    parents_lower 2 3 (-2) (1/2) (by norm_num) (1 : Fin 3)

example : (parents 2 3 (-2) (1/2)).run.value[2].lower = -1 := by
  have h := parents_lower 2 3 (-2) (1/2) (by norm_num) (2 : Fin 3)
  change (parents 2 3 (-2) (1/2)).run.value[2].lower =
    affinePoint (-2) (1/2) (boundarySchedule 3 1) at h
  norm_num [affinePoint, boundarySchedule] at h
  exact h

example : (parents 2 3 (-2) (1/2)).run.cost .field = 24 := by
  simp [parents_cost, tick]

example : (parents 2 3 (-2) (1/2)).run.cost .compare = 9 := by
  simp [parents_cost, tick]

example : (parents 2 3 (-2) (1/2)).run.cost .read = 6 := by
  simp [parents_cost, tick]

example : (parents 2 3 (-2) (1/2)).run.cost .write = 6 := by
  simp [parents_cost, tick]

example : (parents 2 3 (-2) (1/2)).quotientCalls = 12 := by
  norm_num [parents_quotients]

example : (parents 2 3 (-2) (1/2)).remainderCalls = 9 := by
  norm_num [parents_remainders]

/-- The half-grid boundary is legal, including the smallest source width. -/
example (n : ℕ) (origin step : ℝ) (t : Fin (n+1)) :
    (parents n (2^n) origin step).run.value[t.val].lower =
      affinePoint origin step (boundarySchedule (2^n) (n-t.val+1)) :=
  parents_lower n (2^n) origin step le_rfl t

#print axioms binaryReal_value
#print axioms parents_lower
#print axioms parents_cost

end QuantumBlockEncoding.StoredBinaryCoordinates.Tests
