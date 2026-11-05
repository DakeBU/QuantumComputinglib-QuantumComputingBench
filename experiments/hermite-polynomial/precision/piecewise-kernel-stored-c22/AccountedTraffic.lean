import StoredProducer

namespace HermitePiecewiseStored
open scoped BigOperators
open QuantumBlockEncoding StoredGivens StoredRectangularGivens HermitePiecewiseAssembly

/-- Number of scalar/row/core containers participating in one collection pass.
This indexes a real traffic ledger, not scalar evaluation runtime. -/
def passContainers (n D : ℕ) : ℕ := (n+1)*(2*D^2+D+1)+2*D

theorem produceQData_traffic (k n : ℕ) (R delta : ℚ) (op : Op) :
    (produceQData k n R delta).cost op =
      passContainers n (assemblySize k delta)*(2*tick .read op+2*tick .write op) := by
  simp [produceQData, bind, Run.bind, pure, Run.pure, collect_cost, passContainers]
  ring

theorem castVector_traffic {N : ℕ} (v : Vector ℚ N) (op : Op) :
    (castVector v).cost op = N*(3*tick .read op+2*tick .write op) := by
  simp [castVector, collect_cost, bind, Run.bind, pure, Run.pure, StoredGivens.read, charge]
  ring

theorem castCore_traffic {D : ℕ} (A : RationalCore D) (op : Op) :
    (castCore A).cost op = (2*D^2+D)*(3*tick .read op+2*tick .write op) := by
  simp [castCore, collect_cost, bind, Run.bind, castVector_traffic, StoredGivens.read, charge]
  ring

theorem castData_traffic {n D : ℕ} (data : RationalData n D) (op : Op) :
    (castData data).cost op = passContainers n D*(3*tick .read op+2*tick .write op) := by
  simp [castData, collect_cost, bind, Run.bind, pure, Run.pure,
    castCore_traffic, castVector_traffic, StoredGivens.read, charge, passContainers]
  ring

theorem produceData_traffic (k n : ℕ) (R delta : ℚ) (op : Op) :
    (produceData k n R delta).cost op =
      passContainers n (assemblySize k delta)*(5*tick .read op+4*tick .write op) := by
  simp only [produceData, bind, Run.bind, Pi.add_apply, produceQData_traffic, castData_traffic]
  ring

theorem produceData_accounted_total (k n : ℕ) (R delta : ℚ) :
    total (produceData k n R delta).cost = 9*passContainers n (assemblySize k delta) := by
  simp [total, produceData_traffic, tick]
  ring

private theorem total_add (a b : Cost) : total (a+b)=total a+total b := by
  simp only [total, Pi.add_apply]
  ring

/-- SAME returned run: actual rational materialization, explicit stored-data
casting/copies, and canonical assembly are counted. Missing scalar/setup costs
are not supplied as a hypothesis and are not claimed zero by this theorem. -/
theorem produceStored_accounted_traffic_le (k n : ℕ) (R delta : ℚ) :
    total (produceStored k n R delta).cost ≤
      9*passContainers n (assemblySize k delta)+
      20*(assemblySize k delta)^2+30*assemblySize k delta+5*n^2+7*n+31 := by
  simp only [produceStored, bind, Run.bind, total_add, produceData_accounted_total]
  have h := StoredMatrixProductChain.ofTable_total_cost_le
    (produceData k n R delta).value.tables
    (produceData k n R delta).value.left
    (produceData k n R delta).value.right
  omega

#print axioms produceQData_traffic
#print axioms produceData_accounted_total
#print axioms produceStored_accounted_traffic_le
end HermitePiecewiseStored
