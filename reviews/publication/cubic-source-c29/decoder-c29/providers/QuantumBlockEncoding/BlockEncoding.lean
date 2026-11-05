import QuantumBlockEncoding.Circuit

   
                             

                                                                               
                                                                          
                                                                               
                                                
  

namespace QuantumBlockEncoding

structure RegisterLayout where
  systemQubits : Nat
  signalQubits : Nat
  pureAncillas : Nat
deriving Repr, DecidableEq

namespace RegisterLayout

   
                                                                              
                                                                               
            
  
def auxiliaryQubits (layout : RegisterLayout) : Nat :=
  layout.signalQubits + layout.pureAncillas

end RegisterLayout

                                                                      
structure BlockEncodingSpec (α : Type u) (rows cols : Nat) where
  matrix : Matrix rows cols α
  normalizer : α
  error : α
  layout : RegisterLayout
  circuit : Circuit
  resource : Resource

   
                                                                      
                                                            

               
                         
                          
                                 
  
structure BlockEncodingCost where
  auxiliaryQubits : Nat
  gateCount : Nat
  depth : Nat
  oracleCalls : Nat
deriving Repr, DecidableEq

namespace BlockEncodingCost

def fromLayoutAndResource (layout : RegisterLayout) (resource : Resource) :
    BlockEncodingCost where
  auxiliaryQubits := layout.auxiliaryQubits
  gateCount := resource.gates
  depth := resource.depth
  oracleCalls := resource.oracleCalls

def fromSpec (spec : BlockEncodingSpec α rows cols) : BlockEncodingCost :=
  fromLayoutAndResource spec.layout spec.resource

                                                                               
def betterThan (x y : BlockEncodingCost) : Prop :=
  x.gateCount < y.gateCount ∨
  (x.gateCount = y.gateCount ∧
    (x.depth < y.depth ∨
      (x.depth = y.depth ∧
        (x.auxiliaryQubits < y.auxiliaryQubits ∨
          (x.auxiliaryQubits = y.auxiliaryQubits ∧
            x.oracleCalls < y.oracleCalls)))))

                                                                                
def noWorseThan (x y : BlockEncodingCost) : Prop :=
  x = y ∨ x.betterThan y

end BlockEncodingCost

   
                                                                          
                                                                       
                                      
  
structure QueryOperatorTarget (α : Type u) (rows cols : Nat) where
  operator : Matrix rows cols α
  normalizer : α
  source : String
  semanticContract : String
  freeParameters : List String := []

   
                                                                              
                                                                        
                                                                          
                                     
  
structure OperatorBlockEncodingCandidate (α : Type u) (systemQubits : Nat) where
  auxiliaryQubits : Nat
  target : QueryOperatorTarget α (gridSize systemQubits) (gridSize systemQubits)
  unitary :
    Matrix (gridSize (systemQubits + auxiliaryQubits))
      (gridSize (systemQubits + auxiliaryQubits)) α
  layout : RegisterLayout
  circuit : Circuit
  schedule : LayeredCircuit := []
  resource : Resource
  layoutMatches : layout.auxiliaryQubits = auxiliaryQubits
  isUnitary : Prop
  blockContainsTarget : Prop

namespace OperatorBlockEncodingCandidate

def cost (candidate : OperatorBlockEncodingCandidate α systemQubits) :
    BlockEncodingCost :=
  {
    auxiliaryQubits := candidate.auxiliaryQubits
    gateCount := candidate.resource.gates
    depth := candidate.resource.depth
    oracleCalls := candidate.resource.oracleCalls
  }

end OperatorBlockEncodingCandidate

                                                                                    
structure VerifiedOperatorBlockEncoding (α : Type u) (systemQubits : Nat) where
  candidate : OperatorBlockEncodingCandidate α systemQubits
  unitaryProof : candidate.isUnitary
  blockProof : candidate.blockContainsTarget

   
                                                                              

                                                                         
               

                                            

                                                                              
                                                                               
                                
  
structure ApproximateOperatorBlockEncodingCandidate
    (α : Type u) (systemQubits : Nat) where
  candidate : OperatorBlockEncodingCandidate α systemQubits
  epsilon : α
  approximationBound : Prop

   
                                                                             
                                                                          
                  
  
structure VerifiedApproximateOperatorBlockEncoding
    (α : Type u) (systemQubits : Nat) where
  approxCandidate : ApproximateOperatorBlockEncodingCandidate α systemQubits
  unitaryProof : approxCandidate.candidate.isUnitary
  approximationProof : approxCandidate.approximationBound

namespace VerifiedOperatorBlockEncoding

   
                                                                             
                                                                           
                                                                              
                                       
  
def asZeroErrorApprox [OfNat α 0]
    (v : VerifiedOperatorBlockEncoding α systemQubits) :
    VerifiedApproximateOperatorBlockEncoding α systemQubits where
  approxCandidate := {
    candidate := v.candidate
    epsilon := 0
    approximationBound := v.candidate.blockContainsTarget
  }
  unitaryProof := v.unitaryProof
  approximationProof := v.blockProof

end VerifiedOperatorBlockEncoding

   
                                                                             

                                                                           
                                                                            
                                                                               
                                                                               
                                                           
  
structure AdaptiveBlockEncodingPolicy (α : Type u) where
  maxExactIterations : Nat
  exactStallIterations : Nat
  requiredCost : BlockEncodingCost
  requestedEpsilon : α
  allowRelaxedEpsilon : Bool
  maxUpperAgents : Nat
  maxMiddleAgents : Nat
  maxLowerAgents : Nat
deriving Repr

                                                                       
inductive BlockEncodingSearchPhase where
  | exactSearch
  | exactConvergedApproxSearch
  | relaxedApproxSearch
  | stopped
deriving Repr, DecidableEq

   
                                                                          
                                                                             
                                                                             
                                                                        
  
structure VerifiedBlockEncoding (α : Type u) (rows cols : Nat) where
  spec : BlockEncodingSpec α rows cols
  isUnitary : Prop
  blockCorrect : Prop
  resourceBound : Prop
  unitaryProof : isUnitary
  blockProof : blockCorrect
  resourceProof : resourceBound

namespace VerifiedBlockEncoding

theorem unitary {α : Type u} {rows cols : Nat}
    (v : VerifiedBlockEncoding α rows cols) : v.isUnitary :=
  v.unitaryProof

theorem correct {α : Type u} {rows cols : Nat}
    (v : VerifiedBlockEncoding α rows cols) : v.blockCorrect :=
  v.blockProof

theorem resource_ok {α : Type u} {rows cols : Nat}
    (v : VerifiedBlockEncoding α rows cols) : v.resourceBound :=
  v.resourceProof

end VerifiedBlockEncoding

                                                                                
structure ConstructionClaim where
  name : String
  source : String
  target : String
  normalization : String
  layout : String
  resource : AsymptoticResource
deriving Repr, DecidableEq

end QuantumBlockEncoding
