import QuantumBlockEncoding.Core

   
                      

                                                                           
                                                                               
                                                                
  

namespace QuantumBlockEncoding

   
                                                            

                                                                            
                                                                             
                                                                           
                                  
  
structure Resource where
  oneQubit : Nat := 0
  cnot : Nat := 0
  oracleCalls : Nat := 0
  pureAncilla : Nat := 0
  depth : Nat := 0
deriving Repr, DecidableEq

namespace Resource

                                                                             
def gates (r : Resource) : Nat := r.oneQubit + r.cnot + r.oracleCalls

def add (r s : Resource) : Resource where
  oneQubit := r.oneQubit + s.oneQubit
  cnot := r.cnot + s.cnot
  oracleCalls := r.oracleCalls + s.oracleCalls
  pureAncilla := r.pureAncilla + s.pureAncilla
  depth := r.depth + s.depth

   
                                                                             
                                        
  
def parallel (r s : Resource) : Resource where
  oneQubit := r.oneQubit + s.oneQubit
  cnot := r.cnot + s.cnot
  oracleCalls := r.oracleCalls + s.oracleCalls
  pureAncilla := Nat.max r.pureAncilla s.pureAncilla
  depth := Nat.max r.depth s.depth

instance : Zero Resource := ⟨{}⟩
instance : HAdd Resource Resource Resource := ⟨add⟩

def scale (k : Nat) (r : Resource) : Resource where
  oneQubit := k * r.oneQubit
  cnot := k * r.cnot
  oracleCalls := k * r.oracleCalls
  pureAncilla := k * r.pureAncilla
  depth := k * r.depth

def ofCounts (oneQubit cnot pureAncilla : Nat) : Resource where
  oneQubit := oneQubit
  cnot := cnot
  pureAncilla := pureAncilla
  depth := oneQubit + cnot

def ofCountsWithDepth (oneQubit cnot oracleCalls pureAncilla depth : Nat) : Resource where
  oneQubit := oneQubit
  cnot := cnot
  oracleCalls := oracleCalls
  pureAncilla := pureAncilla
  depth := depth

@[simp] theorem gates_eq (r : Resource) :
    r.gates = r.oneQubit + r.cnot + r.oracleCalls := rfl
@[simp] theorem zero_oneQubit : (0 : Resource).oneQubit = 0 := rfl
@[simp] theorem zero_cnot : (0 : Resource).cnot = 0 := rfl
@[simp] theorem zero_oracleCalls : (0 : Resource).oracleCalls = 0 := rfl
@[simp] theorem zero_pureAncilla : (0 : Resource).pureAncilla = 0 := rfl
@[simp] theorem zero_depth : (0 : Resource).depth = 0 := rfl
@[simp] theorem add_oneQubit (r s : Resource) :
    (r + s).oneQubit = r.oneQubit + s.oneQubit := rfl
@[simp] theorem add_cnot (r s : Resource) :
    (r + s).cnot = r.cnot + s.cnot := rfl
@[simp] theorem add_oracleCalls (r s : Resource) :
    (r + s).oracleCalls = r.oracleCalls + s.oracleCalls := rfl
@[simp] theorem add_pureAncilla (r s : Resource) :
    (r + s).pureAncilla = r.pureAncilla + s.pureAncilla := rfl
@[simp] theorem add_depth (r s : Resource) :
    (r + s).depth = r.depth + s.depth := rfl

end Resource

                                                               
inductive CostExpr where
  | nat (n : Nat)
  | atom (name : String)
  | add (a b : CostExpr)
  | mul (a b : CostExpr)
  | log (a : CostExpr)
  | sum (index : String) (body : CostExpr)
deriving Repr, DecidableEq

namespace CostExpr

instance : OfNat CostExpr n where
  ofNat := CostExpr.nat n

instance : HAdd CostExpr CostExpr CostExpr where
  hAdd := CostExpr.add

instance : HMul CostExpr CostExpr CostExpr where
  hMul := CostExpr.mul

def atoms (names : List String) : List CostExpr :=
  names.map CostExpr.atom

end CostExpr

                                  
structure AsymptoticResource where
  gates : CostExpr
  pureAncilla : CostExpr
deriving Repr, DecidableEq

namespace AsymptoticResource

def add (r s : AsymptoticResource) : AsymptoticResource where
  gates := r.gates + s.gates
  pureAncilla := r.pureAncilla + s.pureAncilla

instance : HAdd AsymptoticResource AsymptoticResource AsymptoticResource := ⟨add⟩

end AsymptoticResource

                                                           
def bandedSparseAccessResource (n l : Nat) : Resource :=
  Resource.ofCounts
    ((2 ^ l + 1) * (32 * n - 48))
    (25 * 2 ^ l * n - 36 * 2 ^ l + 32 * n - 48)
    (n - 1)

                                                              
def sparseAmplitudeOracleResource (l : Nat) : Resource :=
  Resource.ofCounts (2 ^ l) (2 ^ l) 0

                                                    
def indicatorResource (n : Nat) : Resource :=
  Resource.ofCounts (16 * n + 34) (12 * n - 4) (n - 1)

end QuantumBlockEncoding
